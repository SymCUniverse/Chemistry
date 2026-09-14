#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any

RY_TO_EV = 13.605693122994
PW_SHA256 = '2b1ede22d276b1d4dab3e31212f306e88ae57e00f33ce6b532b849493a457855'
RU_SHA256 = 'ed637e8481a2fddda6a93863a92f8b0b857379b9db23325a4664e3df0a6f45bd'
SCHEMA = 'h-ru0001-clean-relaxation-checkpoint-qualification-protocol-v0.1'
STATUS = 'FROZEN_NON_EVIDENTIARY_MECHANICAL_QUALIFICATION'
PREFIX = 'system3_relax_checkpoint_qual_toy'
CLEAN_STOP_MARKER = 'Maximum CPU time exceeded'
RESTART_ERROR_PATTERNS = [
    'cannot restart', 'restart file not found', 'error in routine read_file',
    'bad restart', 'incompatible restart', 'error reading restart'
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def load(path: str | Path) -> dict[str, Any]:
    obj = json.loads(Path(path).read_text(encoding='utf-8'))
    if not isinstance(obj, dict):
        raise SystemExit(f'MECHANICAL_HOLD: JSON object required: {path}')
    return obj


def write(path: str | Path, obj: dict[str, Any]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, sort_keys=True) + '\n', encoding='utf-8')


def recursive_manifest(root: Path) -> dict[str, Any]:
    files = []
    total = 0
    for p in sorted(x for x in root.rglob('*') if x.is_file()):
        rel = p.relative_to(root).as_posix()
        size = p.stat().st_size
        total += size
        files.append({'path': rel, 'size_bytes': size, 'sha256': sha256(p)})
    return {
        'schema': 'system3-relax-checkpoint-qual-manifest-v0.1',
        'file_count': len(files),
        'size_bytes': total,
        'files': files,
    }


def validate_protocol(p: dict[str, Any]) -> None:
    if p.get('schema') != SCHEMA or p.get('status') != STATUS:
        raise SystemExit('SCIENTIFIC_HOLD: qualification protocol identity/status drift')
    if p.get('scientific_evidence') is not False or p.get('admissibility') != 'NONE_MECHANICAL_EXECUTION_QUALIFICATION_ONLY':
        raise SystemExit('SCIENTIFIC_HOLD: qualification was promoted toward scientific evidence')
    toy = p['toy_relaxation']
    expected = {
        'layers': 5,
        'total_vacuum_angstrom': 12.0,
        'kmesh': [6, 6, 1],
        'ecutwfc_ry': 50,
        'ecutrho_ry': 200,
        'a_angstrom': 2.7252915734660723,
        'c_angstrom': 4.294686728521268,
        'outer_fractional_z_perturbation': 0.025,
        'movable_atoms': 'outer one layer on each face',
        'movable_components': 'z only',
        'forc_conv_thr_ry_per_bohr': 1e-10,
        'etot_conv_thr_ry': 1e-12,
        'nstep': 500,
    }
    for k, v in expected.items():
        if toy.get(k) != v:
            raise SystemExit(f'MECHANICAL_HOLD: toy contract drift: {k}')
    cp = p['checkpoint_contract']
    if int(cp['segment_1_max_seconds']) != 75 or int(cp['segment_2_max_seconds']) != 75:
        raise SystemExit('MECHANICAL_HOLD: segment timing drift')
    if int(cp['external_wrapper_timeout_seconds']) != 150:
        raise SystemExit('MECHANICAL_HOLD: wrapper timing drift')
    if cp['segment_1_restart_mode'] != 'from_scratch' or cp['segment_2_restart_mode'] != 'restart':
        raise SystemExit('MECHANICAL_HOLD: restart-mode contract drift')
    if cp['disk_io'] != 'medium' or cp['fresh_runner_boundary_required'] is not True:
        raise SystemExit('MECHANICAL_HOLD: checkpoint contract drift')
    for k, v in p['firewalls'].items():
        if v is not False:
            raise SystemExit(f'SCIENTIFIC_HOLD: qualification firewall opened: {k}')


def verify_runtime(pw: Path, pseudo_dir: Path) -> None:
    ru = pseudo_dir / 'Ru.nc.pbe.z_16.oncvpsp4.sg15.v0.upf'
    if not pw.is_file() or sha256(pw) != PW_SHA256:
        raise SystemExit('MECHANICAL_HOLD: pw.x identity mismatch')
    if not ru.is_file() or sha256(ru) != RU_SHA256:
        raise SystemExit('MECHANICAL_HOLD: Ru pseudopotential identity mismatch')


def slab_geometry(a: float, c: float, layers: int, vacuum: float) -> tuple[float, list[tuple[float,float,float]]]:
    dz = c / 2.0
    cell_z = (layers - 1) * dz + vacuum
    mid = (layers - 1) / 2.0
    rows = []
    for j in range(layers):
        x, y = (0.0, 0.0) if j % 2 == 0 else (2.0/3.0, 1.0/3.0)
        z_ang = (j - mid) * dz
        rows.append((x, y, 0.5 + z_ang / cell_z))
    return cell_z, rows


def build_input(protocol: dict[str, Any], pseudo_dir: Path, state: Path, restart_mode: str, max_seconds: int) -> str:
    t = protocol['toy_relaxation']
    cell_z, rows = slab_geometry(float(t['a_angstrom']), float(t['c_angstrom']), int(t['layers']), float(t['total_vacuum_angstrom']))
    perturb = float(t['outer_fractional_z_perturbation'])
    rows[0] = (rows[0][0], rows[0][1], rows[0][2] - perturb)
    rows[-1] = (rows[-1][0], rows[-1][1], rows[-1][2] + perturb)
    atoms = []
    for i, (x, y, z) in enumerate(rows):
        flags = (0, 0, 1) if i in (0, len(rows)-1) else (0, 0, 0)
        atoms.append(f'Ru {x:.15f} {y:.15f} {z:.15f} {flags[0]} {flags[1]} {flags[2]}')
    a = float(t['a_angstrom'])
    kx, ky, kz = [int(x) for x in t['kmesh']]
    return f'''&CONTROL
 calculation='relax',
 prefix='{PREFIX}',
 pseudo_dir='{pseudo_dir.resolve()}',
 outdir='{state.resolve()}',
 restart_mode='{restart_mode}',
 disk_io='medium',
 max_seconds={float(max_seconds):.6f},
 nstep={int(t['nstep'])},
 forc_conv_thr={float(t['forc_conv_thr_ry_per_bohr']):.12e},
 etot_conv_thr={float(t['etot_conv_thr_ry']):.12e},
 tprnfor=.true.,
 tstress=.true.,
 verbosity='high',
/
&SYSTEM
 ibrav=0,
 nat={int(t['layers'])},
 ntyp=1,
 ecutwfc={int(t['ecutwfc_ry'])},
 ecutrho={int(t['ecutrho_ry'])},
 input_dft='PBE',
 occupations='smearing',
 smearing='mv',
 degauss=0.02,
/
&ELECTRONS
 conv_thr=1.0d-9,
 mixing_beta=0.3,
 electron_maxstep=200,
/
&IONS
 ion_dynamics='bfgs',
/
ATOMIC_SPECIES
Ru 101.07 Ru.nc.pbe.z_16.oncvpsp4.sg15.v0.upf
CELL_PARAMETERS angstrom
{a:.12f} 0.0 0.0
{-0.5*a:.12f} {math.sqrt(3.0)*0.5*a:.12f} 0.0
0.0 0.0 {cell_z:.12f}
ATOMIC_POSITIONS crystal
{chr(10).join(atoms)}
K_POINTS automatic
{kx} {ky} {kz} 0 0 0
'''


def wait(proc: subprocess.Popen, stdout: Path, timeout: int) -> tuple[int, bool, float]:
    start = time.time()
    next_hb = 30
    while True:
        rc = proc.poll()
        elapsed = time.time() - start
        if rc is not None:
            return int(rc), False, elapsed
        if elapsed >= timeout:
            proc.terminate()
            try:
                rc = proc.wait(timeout=30)
            except subprocess.TimeoutExpired:
                proc.kill(); rc = proc.wait(timeout=10)
            return int(rc), True, time.time() - start
        if elapsed >= next_hb:
            size = stdout.stat().st_size if stdout.exists() else 0
            print(f'BFGS_CHECKPOINT_QUAL_HEARTBEAT elapsed_s={int(elapsed)} stdout_bytes={size}', flush=True)
            next_hb += 30
        time.sleep(5)


def bfgs_markers(manifest: dict[str, Any]) -> list[str]:
    markers = []
    for f in manifest['files']:
        p = f['path'].lower()
        if 'bfgs' in p or p.endswith('.update') or 'restart' in p:
            markers.append(f['path'])
    return markers


def run_segment(args: argparse.Namespace) -> None:
    p = load(args.protocol); validate_protocol(p)
    pw = Path(args.pw).resolve(); pseudo = Path(args.pseudo_dir).resolve(); verify_runtime(pw, pseudo)
    seg = int(args.segment)
    if seg not in (1, 2):
        raise SystemExit('MECHANICAL_HOLD: only qualification segments 1 and 2 are defined')
    out = Path(args.out).resolve()
    if out.exists(): shutil.rmtree(out)
    out.mkdir(parents=True)
    state = out / 'restart_state'
    prior_manifest = None
    if seg == 1:
        if args.previous:
            raise SystemExit('MECHANICAL_HOLD: segment 1 must be fresh')
        state.mkdir()
        restart_mode = 'from_scratch'
    else:
        if not args.previous:
            raise SystemExit('MECHANICAL_HOLD: segment 2 requires transported checkpoint')
        previous = Path(args.previous).resolve()
        expected = load(previous / 'checkpoint_manifest.json')
        actual = recursive_manifest(previous / 'restart_state')
        if expected != actual:
            raise SystemExit('MECHANICAL_HOLD: transported checkpoint manifest mismatch')
        prior_manifest = actual
        prior_markers = bfgs_markers(actual)
        if not prior_markers:
            raise SystemExit('MECHANICAL_HOLD: no BFGS/restart-state marker found before fresh-runner resume')
        shutil.copytree(previous / 'restart_state', state)
        restart_mode = 'restart'
    max_seconds = int(p['checkpoint_contract'][f'segment_{seg}_max_seconds'])
    inp = out / f'qual_segment_{seg}.in'; stdout = out / f'qual_segment_{seg}.out'
    inp.write_text(build_input(p, pseudo, state, restart_mode, max_seconds), encoding='utf-8')
    env = dict(os.environ); env.update(OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1')
    with inp.open('rb') as fi, stdout.open('wb') as fo:
        proc = subprocess.Popen([str(pw)], stdin=fi, stdout=fo, stderr=subprocess.STDOUT, env=env)
        rc, wrapper_kill, elapsed = wait(proc, stdout, int(p['checkpoint_contract']['external_wrapper_timeout_seconds']))
    text = stdout.read_text(errors='replace')
    lower = text.lower()
    if wrapper_kill:
        raise SystemExit('MECHANICAL_HOLD: external wrapper killed toy relaxation before native checkpoint')
    if any(pattern in lower for pattern in RESTART_ERROR_PATTERNS):
        raise SystemExit('MECHANICAL_HOLD: QE reported restart failure')
    clean_stop = CLEAN_STOP_MARKER in text
    job_done = 'JOB DONE.' in text
    if seg == 1 and not clean_stop:
        raise SystemExit('MECHANICAL_HOLD: segment 1 did not exercise native max_seconds checkpoint stop')
    if seg == 2 and not (clean_stop or job_done):
        raise SystemExit('MECHANICAL_HOLD: resumed segment neither completed nor reached native max_seconds stop')
    save = state / f'{PREFIX}.save'
    if not save.is_dir() or not (save / 'data-file-schema.xml').is_file():
        raise SystemExit('MECHANICAL_HOLD: native QE save directory missing')
    manifest = recursive_manifest(state)
    markers = bfgs_markers(manifest)
    if not markers:
        raise SystemExit('MECHANICAL_HOLD: no BFGS/restart-state marker found after segment')
    changed = None
    if prior_manifest is not None:
        old = {f['path']: f['sha256'] for f in prior_manifest['files']}
        new = {f['path']: f['sha256'] for f in manifest['files']}
        changed = sorted(k for k in set(old) | set(new) if old.get(k) != new.get(k))
        if not changed:
            raise SystemExit('MECHANICAL_HOLD: fresh-runner resume did not advance any checkpoint state')
    write(out / 'checkpoint_manifest.json', manifest)
    meta = {
        'schema': 'h-ru0001-clean-relaxation-checkpoint-qualification-segment-v0.1',
        'segment': seg,
        'restart_mode': restart_mode,
        'return_code': int(rc),
        'elapsed_s': elapsed,
        'native_max_seconds_stop': clean_stop,
        'job_done': job_done,
        'input_sha256': sha256(inp),
        'output_sha256': sha256(stdout),
        'pw_x_sha256': sha256(pw),
        'ru_pseudo_sha256': sha256(pseudo / 'Ru.nc.pbe.z_16.oncvpsp4.sg15.v0.upf'),
        'manifest_sha256': sha256(out / 'checkpoint_manifest.json'),
        'manifest_file_count': manifest['file_count'],
        'manifest_size_bytes': manifest['size_bytes'],
        'bfgs_or_restart_markers': markers,
        'changed_files_after_resume': changed,
        'scientific_evidence': False,
    }
    write(out / f'SEGMENT_{seg}_QUALIFICATION_METADATA.json', meta)
    print(json.dumps(meta, indent=2, sort_keys=True))
    print(f'SYSTEM3_BFGS_CHECKPOINT_QUAL_SEGMENT_{seg}_VALID')


def finalize(args: argparse.Namespace) -> None:
    p = load(args.protocol); validate_protocol(p)
    bundle = Path(args.bundle).resolve()
    m2 = load(bundle / 'SEGMENT_2_QUALIFICATION_METADATA.json')
    manifest = load(bundle / 'checkpoint_manifest.json')
    if recursive_manifest(bundle / 'restart_state') != manifest:
        raise SystemExit('MECHANICAL_HOLD: final qualification bundle manifest mismatch')
    if m2.get('segment') != 2 or m2.get('restart_mode') != 'restart':
        raise SystemExit('MECHANICAL_HOLD: final segment metadata mismatch')
    if m2.get('scientific_evidence') is not False:
        raise SystemExit('SCIENTIFIC_HOLD: mechanical qualification was promoted')
    if not m2.get('bfgs_or_restart_markers') or not m2.get('changed_files_after_resume'):
        raise SystemExit('MECHANICAL_HOLD: BFGS/restart state was not demonstrated across handoff')
    result = {
        'schema': 'h-ru0001-clean-relaxation-checkpoint-qualification-v0.1',
        'status': 'QUALIFIED',
        'effective_date': '2026-09-14',
        'calculation_type': 'relax',
        'fresh_runner_checkpoint_handoff_verified': True,
        'bfgs_restart_state_verified': True,
        'artifact_transport_manifest_exact': True,
        'runtime_hashes_reverified': True,
        'segment_2_native_stop_or_completion_verified': bool(m2.get('native_max_seconds_stop') or m2.get('job_done')),
        'segment_2_restart_error_detected': False,
        'scientific_evidence': False,
        'admissibility': 'NONE_MECHANICAL_EXECUTION_QUALIFICATION_ONLY',
        'toy_settings_may_be_inherited': False,
        'production_relaxation_authorized_by_this_result': False,
        'qualification_protocol': str(Path(args.protocol).as_posix()),
        'qualification_segment_2_metadata': m2,
    }
    write(args.out, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    print('SYSTEM3_CLEAN_RELAXATION_CHECKPOINT_QUALIFIED')


def self_test(args: argparse.Namespace) -> None:
    p = load(args.protocol); validate_protocol(p)
    txt = build_input(p, Path('/tmp/pseudo'), Path('/tmp/state'), 'from_scratch', 75)
    assert "calculation='relax'" in txt and "ion_dynamics='bfgs'" in txt
    assert "restart_mode='from_scratch'" in txt and "disk_io='medium'" in txt
    assert 'max_seconds=75.000000' in txt and 'nstep=500' in txt
    atom_lines = [ln for ln in txt.splitlines() if ln.startswith('Ru ')][1:]
    assert len(atom_lines) == 5
    flags = [tuple(map(int, ln.split()[-3:])) for ln in atom_lines]
    assert flags[0] == (0,0,1) and flags[-1] == (0,0,1)
    assert all(f == (0,0,0) for f in flags[1:-1])
    print('SYSTEM3_BFGS_CHECKPOINT_QUALIFIER_SELF_TEST_PASS')
    print('SCIENTIFIC_EVIDENCE=false')


def main() -> None:
    ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest='cmd', required=True)
    sp = sub.add_parser('self-test'); sp.add_argument('--protocol', required=True); sp.set_defaults(func=self_test)
    sp = sub.add_parser('run-segment'); sp.add_argument('--protocol', required=True); sp.add_argument('--segment', type=int, required=True); sp.add_argument('--previous'); sp.add_argument('--pw', required=True); sp.add_argument('--pseudo-dir', required=True); sp.add_argument('--out', required=True); sp.set_defaults(func=run_segment)
    sp = sub.add_parser('finalize'); sp.add_argument('--protocol', required=True); sp.add_argument('--bundle', required=True); sp.add_argument('--out', required=True); sp.set_defaults(func=finalize)
    args = ap.parse_args(); args.func(args)


if __name__ == '__main__':
    main()
