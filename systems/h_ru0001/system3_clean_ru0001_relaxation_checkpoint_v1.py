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
import sys
import time
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import system3_clean_ru0001_numerical_v1 as base

RELAX_PROTOCOL_SCHEMA = 'h-ru0001-clean-ru0001-relaxation-protocol-v0.1'
RELAX_PROTOCOL_STATUS = 'FROZEN_BEFORE_SYSTEM3_CLEAN_SURFACE_RELAXATION_RESULTS'
ROBUSTNESS_SCHEMA = 'h-ru0001-l17-foundational-robustness-result-v0.1'
ROBUSTNESS_PASS = 'ROBUSTNESS_SUPPORTED'
PASS_EVIDENCE_SCHEMA = 'h-ru0001-successor-fixed-grid-pass-evidence-v0.1'
PASS_EVIDENCE_STATUS = 'VALID_ADJUDICATED_P0_Q_SUCCESSOR_FIXED_GRID_PASS_EVIDENCE'
RELAX_RESULT_SCHEMA = 'h-ru0001-clean-relaxation-result-v0.1'
REPRO_RESULT_SCHEMA = 'h-ru0001-clean-relaxation-reproduction-result-v0.1'
FINAL_SCHEMA = 'h-ru0001-clean-relaxation-and-reproduction-adjudication-v0.1'
PW_SHA256 = '2b1ede22d276b1d4dab3e31212f306e88ae57e00f33ce6b532b849493a457855'
RU_SHA256 = 'ed637e8481a2fddda6a93863a92f8b0b857379b9db23325a4664e3df0a6f45bd'
SUCCESSOR_PROTOCOL_SHA256 = 'ffe50f7cfe5dbf5ce8c19da2449c00067fc795d38a3abe695bb16a0c41a07f48'
RY_TO_EV = base.RY_TO_EV
BOHR_TO_ANG = 0.529177210903
RY_PER_BOHR_TO_EV_PER_ANG = RY_TO_EV / BOHR_TO_ANG
FORCE_LIMIT_EV_PER_ANG = 0.02
FORC_CONV_THR_RY_PER_BOHR = FORCE_LIMIT_EV_PER_ANG / RY_PER_BOHR_TO_EV_PER_ANG
SEGMENT_MAX_SECONDS = 13800
EXTERNAL_TIMEOUT_SECONDS = 14700
MAX_SEGMENTS = 4
HEARTBEAT_SECONDS = 300
TAG = 'system3_clean_ru0001_L17_V15_K24_relax'
ENERGY_RE = re.compile(r'!\s+total energy\s+=\s+([-+0-9.Ee]+)\s+Ry')
FORCE_RE = re.compile(r'atom\s+(\d+)\s+type\s+\d+\s+force\s+=\s+([-+0-9.Ee]+)\s+([-+0-9.Ee]+)\s+([-+0-9.Ee]+)')
CLEAN_STOP_MARKER = 'Maximum CPU time exceeded'


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


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
        files.append({'path': rel, 'sha256': sha256(p), 'size_bytes': size})
    return {
        'schema': 'system3-clean-relax-qe-native-restart-manifest-v0.1',
        'file_count': len(files),
        'size_bytes': total,
        'files': files,
    }


def verify_runtime(pw: Path, pseudo_dir: Path) -> None:
    ru = pseudo_dir / 'Ru.nc.pbe.z_16.oncvpsp4.sg15.v0.upf'
    if not pw.is_file() or sha256(pw) != PW_SHA256:
        raise SystemExit('MECHANICAL_HOLD: pw.x identity mismatch')
    if not ru.is_file() or sha256(ru) != RU_SHA256:
        raise SystemExit('MECHANICAL_HOLD: Ru pseudopotential identity mismatch')


def validate_contract(protocol: dict[str, Any], evidence: dict[str, Any], robustness: dict[str, Any]) -> None:
    if protocol.get('schema') != RELAX_PROTOCOL_SCHEMA or protocol.get('status') != RELAX_PROTOCOL_STATUS:
        raise SystemExit('SCIENTIFIC_HOLD: relaxation protocol identity/status mismatch')
    if protocol.get('scope') != 'NON_KINETIC_CLEAN_SURFACE_RELAXATION_AND_REPRODUCTION':
        raise SystemExit('SCIENTIFIC_HOLD: relaxation scope drift')
    if evidence.get('schema') != PASS_EVIDENCE_SCHEMA or evidence.get('status') != PASS_EVIDENCE_STATUS:
        raise SystemExit('MECHANICAL_HOLD: fixed-grid PASS evidence identity mismatch')
    src = evidence.get('source', {})
    if src.get('successor_protocol_sha256') != SUCCESSOR_PROTOCOL_SHA256:
        raise SystemExit('MECHANICAL_HOLD: successor protocol provenance mismatch')
    res = evidence.get('result', {})
    if res.get('status') != protocol['entry_gate']['required_status']:
        raise SystemExit('SCIENTIFIC_HOLD: required fixed-grid PASS missing')
    if int(res.get('selected_layers', 0)) != 17 or float(res.get('selected_total_vacuum_angstrom', 0.0)) != 15.0:
        raise SystemExit('SCIENTIFIC_HOLD: L17/V15 foundation identity drift')
    if res.get('selected_surface_kmesh') != [24, 24, 1]:
        raise SystemExit('SCIENTIFIC_HOLD: K24 foundation identity drift')
    if robustness.get('schema') != ROBUSTNESS_SCHEMA or robustness.get('status') != ROBUSTNESS_PASS:
        raise SystemExit('FOUNDATIONAL_HOLD: robustness challenge has not supported inheritance')
    if robustness.get('relaxation_inheritance_authorized') is not True:
        raise SystemExit('FOUNDATIONAL_HOLD: robustness result does not authorize inherited relaxation')
    if robustness.get('minimum_fixed_grid_pass_preserved') is not True or robustness.get('original_K16_coupled_hold_preserved') is not True:
        raise SystemExit('SCIENTIFIC_HOLD: historical lineage firewall drift')
    if float(protocol['relaxation']['force_max_ev_per_angstrom']) != FORCE_LIMIT_EV_PER_ANG:
        raise SystemExit('SCIENTIFIC_HOLD: force criterion drift')
    if protocol['relaxation']['ion_dynamics'] != 'bfgs' or protocol['relaxation']['cell_dynamics'] != 'fixed':
        raise SystemExit('SCIENTIFIC_HOLD: relaxation method drift')
    if protocol['relaxation']['movable_atoms'] != 'outer two Ru layers on each face' or protocol['relaxation']['movable_components'] != 'z only':
        raise SystemExit('SCIENTIFIC_HOLD: relaxation degree-of-freedom drift')
    if float(protocol['reproduction_gate']['absolute_total_energy_difference_max_ev']) != 0.001:
        raise SystemExit('SCIENTIFIC_HOLD: reproduction energy criterion drift')
    if any(bool(v) for v in protocol['evidence_firewall'].values()):
        raise SystemExit('SCIENTIFIC_HOLD: relaxation evidence firewall opened')


def selected_settings(evidence: dict[str, Any]) -> dict[str, Any]:
    return {
        'layers': 17,
        'vacuum': 15.0,
        'kmesh': [24, 24, 1],
        'a': 2.7252915734660723,
        'c': 4.294686728521268,
        'ecutwfc': 70,
        'ecutrho': 280,
    }


def build_positions(settings: dict[str, Any]) -> tuple[float, list[tuple[float, float, float, int, int, int]]]:
    cell_z, rows = base.slab_geometry(settings['a'], settings['c'], settings['layers'], settings['vacuum'])
    out = []
    n = settings['layers']
    movable = {0, 1, n - 2, n - 1}
    for i, (x, y, z) in enumerate(rows):
        flags = (0, 0, 1) if i in movable else (0, 0, 0)
        out.append((x, y, z, *flags))
    return cell_z, out


def build_relax_input(settings: dict[str, Any], pseudo_dir: Path, outdir: Path, restart_mode: str) -> str:
    cell_z, positions = build_positions(settings)
    atoms = '\n'.join(
        f'Ru {x:.15f} {y:.15f} {z:.15f} {fx} {fy} {fz}'
        for x, y, z, fx, fy, fz in positions
    )
    kx, ky, kz = settings['kmesh']
    return f'''&CONTROL
 calculation='relax',
 prefix='{TAG}',
 pseudo_dir='{pseudo_dir.resolve()}',
 outdir='{outdir.resolve()}',
 restart_mode='{restart_mode}',
 disk_io='medium',
 max_seconds={SEGMENT_MAX_SECONDS:.6f},
 forc_conv_thr={FORC_CONV_THR_RY_PER_BOHR:.12e},
 tprnfor=.true.,
 tstress=.true.,
 verbosity='high',
/
&SYSTEM
 ibrav=0,
 nat={settings['layers']},
 ntyp=1,
 ecutwfc={settings['ecutwfc']},
 ecutrho={settings['ecutrho']},
 input_dft='PBE',
 occupations='smearing',
 smearing='mv',
 degauss=0.02,
/
&ELECTRONS
 conv_thr=1.0d-10,
 mixing_beta=0.3,
 electron_maxstep=200,
/
&IONS
 ion_dynamics='bfgs',
/
ATOMIC_SPECIES
Ru 101.07 Ru.nc.pbe.z_16.oncvpsp4.sg15.v0.upf
CELL_PARAMETERS angstrom
{settings['a']:.12f} 0.0 0.0
{-0.5*settings['a']:.12f} {math.sqrt(3.0)*0.5*settings['a']:.12f} 0.0
0.0 0.0 {cell_z:.12f}
ATOMIC_POSITIONS crystal
{atoms}
K_POINTS automatic
{kx} {ky} {kz} 0 0 0
'''


def parse_final_positions(text: str, layers: int) -> list[list[float]] | None:
    marker = 'Begin final coordinates'
    idx = text.rfind(marker)
    if idx < 0:
        return None
    tail = text[idx:]
    apos = tail.find('ATOMIC_POSITIONS')
    if apos < 0:
        return None
    lines = tail[apos:].splitlines()[1:]
    coords: list[list[float]] = []
    for line in lines:
        s = line.strip()
        if not s or s.startswith('End final coordinates'):
            break
        parts = s.split()
        if len(parts) < 4 or parts[0] != 'Ru':
            if coords:
                break
            continue
        coords.append([float(parts[1]), float(parts[2]), float(parts[3])])
        if len(coords) == layers:
            break
    return coords if len(coords) == layers else None


def final_force_metrics(text: str, layers: int) -> dict[str, float] | None:
    matches = FORCE_RE.findall(text)
    if len(matches) < layers:
        return None
    last = matches[-layers:]
    by_atom = {int(i): (float(x), float(y), float(z)) for i, x, y, z in last}
    if len(by_atom) != layers:
        return None
    norms = [math.sqrt(x*x + y*y + z*z) * RY_PER_BOHR_TO_EV_PER_ANG for x, y, z in by_atom.values()]
    movable_indices = [1, 2, layers - 1, layers]
    movable_z = [abs(by_atom[i][2]) * RY_PER_BOHR_TO_EV_PER_ANG for i in movable_indices]
    return {
        'max_all_atom_force_norm_ev_per_angstrom': max(norms),
        'max_abs_movable_z_force_ev_per_angstrom': max(movable_z),
    }


def wait_with_heartbeat(proc: subprocess.Popen, stdout: Path) -> tuple[int, bool, float]:
    start = time.time()
    next_hb = HEARTBEAT_SECONDS
    while True:
        rc = proc.poll()
        elapsed = time.time() - start
        if rc is not None:
            return int(rc), False, elapsed
        if elapsed >= EXTERNAL_TIMEOUT_SECONDS:
            proc.terminate()
            try:
                rc = proc.wait(timeout=30)
            except subprocess.TimeoutExpired:
                proc.kill()
                rc = proc.wait(timeout=10)
            return int(rc), True, time.time() - start
        if elapsed >= next_hb:
            size = stdout.stat().st_size if stdout.exists() else 0
            print(f'CLEAN_RELAX_HEARTBEAT elapsed_s={int(elapsed)} stdout_bytes={size}', flush=True)
            next_hb += HEARTBEAT_SECONDS
        time.sleep(15)


def validate_previous(previous: Path) -> tuple[bool, Path | None]:
    complete = previous / 'RELAX_COMPLETE.json'
    result = previous / 'SYSTEM3_CLEAN_RELAXATION_RESULT.json'
    if complete.is_file():
        c = load(complete)
        if c.get('status') != 'VALID_COMPLETED_RELAXATION' or not result.is_file() or sha256(result) != c.get('result_sha256'):
            raise SystemExit('MECHANICAL_HOLD: completed relaxation bundle integrity failure')
        return True, result
    mp = previous / 'checkpoint_manifest.json'
    state = previous / 'restart_state'
    if not mp.is_file() or not state.is_dir():
        raise SystemExit('MECHANICAL_HOLD: prior relaxation checkpoint incomplete')
    if load(mp) != recursive_manifest(state):
        raise SystemExit('MECHANICAL_HOLD: prior relaxation checkpoint manifest mismatch')
    save = state / f'{TAG}.save'
    if not save.is_dir() or not (save / 'data-file-schema.xml').is_file():
        raise SystemExit('MECHANICAL_HOLD: native QE relaxation save directory missing')
    return False, None


def run_relax_segment(args: argparse.Namespace) -> None:
    protocol = load(args.protocol)
    evidence = load(args.pass_evidence)
    robustness = load(args.robustness)
    validate_contract(protocol, evidence, robustness)
    pw = Path(args.pw).resolve()
    pseudo = Path(args.pseudo_dir).resolve()
    verify_runtime(pw, pseudo)
    seg = int(args.segment)
    if seg < 1 or seg > MAX_SEGMENTS:
        raise SystemExit('MECHANICAL_HOLD: relaxation segment outside predeclared range')
    out = Path(args.out).resolve()
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    state = out / 'restart_state'
    previous = Path(args.previous).resolve() if args.previous else None
    if seg == 1:
        if previous is not None:
            raise SystemExit('MECHANICAL_HOLD: segment 1 may not inherit prior state')
        state.mkdir()
        restart_mode = 'from_scratch'
    else:
        if previous is None:
            raise SystemExit('MECHANICAL_HOLD: resumed segment requires previous bundle')
        complete, result = validate_previous(previous)
        if complete and result is not None:
            shutil.copy2(result, out / 'SYSTEM3_CLEAN_RELAXATION_RESULT.json')
            write(out / 'RELAX_COMPLETE.json', load(previous / 'RELAX_COMPLETE.json'))
            print(f'SYSTEM3_CLEAN_RELAX_SEGMENT_{seg}_PASSTHROUGH_COMPLETE')
            return
        shutil.copytree(previous / 'restart_state', state)
        restart_mode = 'restart'
    settings = selected_settings(evidence)
    inp = out / f'relax_segment_{seg}.in'
    stdout = out / f'relax_segment_{seg}.out'
    inp.write_text(build_relax_input(settings, pseudo, state, restart_mode), encoding='utf-8')
    env = dict(os.environ)
    env.update(OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1')
    with inp.open('rb') as fi, stdout.open('wb') as fo:
        proc = subprocess.Popen([str(pw)], stdin=fi, stdout=fo, stderr=subprocess.STDOUT, env=env)
        rc, external_kill, elapsed = wait_with_heartbeat(proc, stdout)
    text = stdout.read_text(errors='replace')
    energies = [float(x) * RY_TO_EV for x in ENERGY_RE.findall(text)]
    job_done = 'JOB DONE.' in text
    clean_stop = CLEAN_STOP_MARKER in text
    if external_kill:
        raise SystemExit('MECHANICAL_HOLD: external wrapper killed relaxation before native checkpoint persistence')
    write(out / f'RELAX_SEGMENT_{seg}_METADATA.json', {
        'schema': 'h-ru0001-clean-relax-checkpoint-segment-v0.1',
        'segment': seg,
        'restart_mode': restart_mode,
        'return_code': int(rc),
        'elapsed_s': elapsed,
        'job_done': job_done,
        'clean_qe_max_seconds_stop': clean_stop,
        'energy_count': len(energies),
        'input_sha256': sha256(inp),
        'output_sha256': sha256(stdout),
        'scientific_settings_changed': False,
        'thresholds_changed': False,
    })
    if job_done and rc == 0 and energies:
        coords = parse_final_positions(text, settings['layers'])
        forces = final_force_metrics(text, settings['layers'])
        if coords is None or forces is None:
            raise SystemExit('MECHANICAL_HOLD: completed relaxation lacks parseable final geometry or forces')
        force_pass = forces['max_abs_movable_z_force_ev_per_angstrom'] <= FORCE_LIMIT_EV_PER_ANG
        row = {
            'schema': RELAX_RESULT_SCHEMA,
            'status': 'VALID_COMPLETED_RELAXATION' if force_pass else 'CLEAN_SURFACE_FORCE_HOLD',
            'segment_completed': seg,
            'layers': 17,
            'total_vacuum_angstrom': 15.0,
            'kmesh': [24, 24, 1],
            'energy_ev': energies[-1],
            'final_positions_crystal': coords,
            'force_metrics': forces,
            'force_limit_ev_per_angstrom': FORCE_LIMIT_EV_PER_ANG,
            'force_gate_pass': force_pass,
            'job_done': True,
            'return_code': 0,
            'timeout': False,
            'input_sha256': sha256(inp),
            'output_sha256': sha256(stdout),
            'pw_x_sha256': sha256(pw),
            'ru_pseudo_sha256': sha256(pseudo / 'Ru.nc.pbe.z_16.oncvpsp4.sg15.v0.upf'),
            'robustness_status': ROBUSTNESS_PASS,
            'chi_used': False,
            'kinetic_inputs_used': False,
            'scientific_settings_changed': False,
            'thresholds_changed': False,
        }
        rp = out / 'SYSTEM3_CLEAN_RELAXATION_RESULT.json'
        write(rp, row)
        write(out / 'RELAX_COMPLETE.json', {'status': row['status'], 'result_sha256': sha256(rp)})
        shutil.rmtree(state, ignore_errors=True)
        print(json.dumps(row, indent=2, sort_keys=True))
        print(row['status'])
        return
    if not clean_stop:
        raise SystemExit('MECHANICAL_HOLD: relaxation neither completed nor produced verified QE max_seconds clean stop')
    save = state / f'{TAG}.save'
    if not save.is_dir() or not (save / 'data-file-schema.xml').is_file():
        raise SystemExit('MECHANICAL_HOLD: relaxation clean stop did not preserve a valid QE save directory')
    manifest = recursive_manifest(state)
    write(out / 'checkpoint_manifest.json', manifest)
    write(out / 'CHECKPOINT.json', {
        'status': 'VALID_NATIVE_QE_CHECKPOINT_NOT_SCIENTIFIC_EVIDENCE',
        'segment': seg,
        'file_count': manifest['file_count'],
        'size_bytes': manifest['size_bytes'],
        'scientific_result_available': False,
    })
    print(f'SYSTEM3_CLEAN_RELAX_SEGMENT_{seg}_CHECKPOINT_READY')


def build_repro_input(relax: dict[str, Any], pseudo_dir: Path, outdir: Path) -> str:
    settings = {'layers': 17, 'vacuum': 15.0, 'kmesh': [24, 24, 1], 'a': 2.7252915734660723, 'c': 4.294686728521268, 'ecutwfc': 70, 'ecutrho': 280}
    cell_z, _ = base.slab_geometry(settings['a'], settings['c'], settings['layers'], settings['vacuum'])
    atoms = '\n'.join(f'Ru {x:.15f} {y:.15f} {z:.15f}' for x, y, z in relax['final_positions_crystal'])
    return f'''&CONTROL
 calculation='scf',
 prefix='system3_clean_ru0001_relax_reproduction',
 pseudo_dir='{pseudo_dir.resolve()}',
 outdir='{outdir.resolve()}',
 tprnfor=.true.,
 tstress=.true.,
 verbosity='high',
/
&SYSTEM
 ibrav=0,
 nat=17,
 ntyp=1,
 ecutwfc=70,
 ecutrho=280,
 input_dft='PBE',
 occupations='smearing',
 smearing='mv',
 degauss=0.02,
/
&ELECTRONS
 conv_thr=1.0d-10,
 mixing_beta=0.3,
 electron_maxstep=200,
/
ATOMIC_SPECIES
Ru 101.07 Ru.nc.pbe.z_16.oncvpsp4.sg15.v0.upf
CELL_PARAMETERS angstrom
{settings['a']:.12f} 0.0 0.0
{-0.5*settings['a']:.12f} {math.sqrt(3.0)*0.5*settings['a']:.12f} 0.0
0.0 0.0 {cell_z:.12f}
ATOMIC_POSITIONS crystal
{atoms}
K_POINTS automatic
24 24 1 0 0 0
'''


def run_reproduction(args: argparse.Namespace) -> None:
    relax = load(args.relax_result)
    if relax.get('schema') != RELAX_RESULT_SCHEMA or relax.get('status') != 'VALID_COMPLETED_RELAXATION' or relax.get('force_gate_pass') is not True:
        raise SystemExit('SCIENTIFIC_HOLD: valid force-converged relaxation required before reproduction')
    pw = Path(args.pw).resolve(); pseudo = Path(args.pseudo_dir).resolve(); verify_runtime(pw, pseudo)
    out = Path(args.out).resolve(); out.mkdir(parents=True, exist_ok=True)
    tmp = out / 'tmp'; tmp.mkdir(exist_ok=True)
    inp = out / 'reproduction.in'; stdout = out / 'reproduction.out'
    inp.write_text(build_repro_input(relax, pseudo, tmp), encoding='utf-8')
    env = dict(os.environ); env.update(OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1')
    start = time.time()
    with inp.open('rb') as fi, stdout.open('wb') as fo:
        proc = subprocess.Popen([str(pw)], stdin=fi, stdout=fo, stderr=subprocess.STDOUT, env=env)
        try:
            rc = proc.wait(timeout=19800)
            timed_out = False
        except subprocess.TimeoutExpired:
            timed_out = True; proc.terminate()
            try: rc = proc.wait(timeout=30)
            except subprocess.TimeoutExpired: proc.kill(); rc = proc.wait(timeout=10)
    text = stdout.read_text(errors='replace')
    energies = [float(x) * RY_TO_EV for x in ENERGY_RE.findall(text)]
    valid = (not timed_out) and rc == 0 and 'JOB DONE.' in text and bool(energies)
    row = {
        'schema': REPRO_RESULT_SCHEMA,
        'status': 'VALID_FRESH_REPRODUCTION_SCF' if valid else 'MECHANICAL_REPRODUCTION_HOLD',
        'energy_ev': energies[-1] if energies else None,
        'job_done': 'JOB DONE.' in text,
        'return_code': int(rc),
        'timeout': timed_out,
        'elapsed_s': time.time() - start,
        'input_sha256': sha256(inp),
        'output_sha256': sha256(stdout),
        'pw_x_sha256': sha256(pw),
        'ru_pseudo_sha256': sha256(pseudo / 'Ru.nc.pbe.z_16.oncvpsp4.sg15.v0.upf'),
        'fresh_independent_scf': True,
        'scientific_settings_changed': False,
        'thresholds_changed': False,
    }
    write(out / 'SYSTEM3_CLEAN_RELAXATION_REPRODUCTION_RESULT.json', row)
    if not valid:
        raise SystemExit('MECHANICAL_HOLD: fresh reproduction SCF did not complete validly')
    print(json.dumps(row, indent=2, sort_keys=True))
    print(row['status'])


def adjudicate(args: argparse.Namespace) -> None:
    protocol = load(args.protocol); relax = load(args.relax_result); repro = load(args.reproduction_result)
    if relax.get('schema') != RELAX_RESULT_SCHEMA or repro.get('schema') != REPRO_RESULT_SCHEMA:
        raise SystemExit('MECHANICAL_HOLD: relaxation/reproduction result schema mismatch')
    if relax.get('status') != 'VALID_COMPLETED_RELAXATION' or relax.get('force_gate_pass') is not True:
        status = 'CLEAN_SURFACE_FORCE_HOLD'; passed = False
    elif repro.get('status') != 'VALID_FRESH_REPRODUCTION_SCF' or repro.get('energy_ev') is None:
        status = 'CLEAN_SURFACE_REPRODUCTION_HOLD'; passed = False
    else:
        delta = abs(float(relax['energy_ev']) - float(repro['energy_ev']))
        passed = delta <= float(protocol['reproduction_gate']['absolute_total_energy_difference_max_ev'])
        status = protocol['decision']['pass_status'] if passed else protocol['decision']['reproduction_hold_status']
    delta = None if repro.get('energy_ev') is None or relax.get('energy_ev') is None else abs(float(relax['energy_ev']) - float(repro['energy_ev']))
    row = {
        'schema': FINAL_SCHEMA,
        'status': status,
        'phase': 'P0_Q',
        'relaxation_energy_ev': relax.get('energy_ev'),
        'reproduction_energy_ev': repro.get('energy_ev'),
        'absolute_total_energy_difference_ev': delta,
        'reproduction_tolerance_ev': float(protocol['reproduction_gate']['absolute_total_energy_difference_max_ev']),
        'force_gate_pass': relax.get('force_gate_pass') is True,
        'reproduction_gate_pass': bool(passed),
        'surface_ready': bool(passed),
        'next_gate': protocol['decision']['pass_next_gate'] if passed else None,
        'substrate_certificate_may_be_issued_after_provenance_packaging': bool(passed),
        'chi_used': False,
        'kinetic_inputs_used': False,
        'thresholds_changed': False,
        'scientific_settings_changed': False,
    }
    write(args.out, row)
    print(json.dumps(row, indent=2, sort_keys=True))
    print(status)


def self_test(args: argparse.Namespace) -> None:
    protocol = load(args.protocol); evidence = load(args.pass_evidence)
    fake_robust = {
        'schema': ROBUSTNESS_SCHEMA,
        'status': ROBUSTNESS_PASS,
        'relaxation_inheritance_authorized': True,
        'minimum_fixed_grid_pass_preserved': True,
        'original_K16_coupled_hold_preserved': True,
    }
    validate_contract(protocol, evidence, fake_robust)
    s = selected_settings(evidence)
    txt = build_relax_input(s, Path('/tmp/pseudo'), Path('/tmp/state'), 'from_scratch')
    assert "calculation='relax'" in txt
    assert "ion_dynamics='bfgs'" in txt
    assert "restart_mode='from_scratch'" in txt and "disk_io='medium'" in txt
    assert f'max_seconds={SEGMENT_MAX_SECONDS:.6f}' in txt
    assert 'K_POINTS automatic\n24 24 1 0 0 0' in txt
    atom_lines = [ln for ln in txt.splitlines() if ln.startswith('Ru ')][1:]
    assert len(atom_lines) == 17
    flags = [tuple(map(int, ln.split()[-3:])) for ln in atom_lines]
    assert [i for i, f in enumerate(flags) if f == (0, 0, 1)] == [0, 1, 15, 16]
    assert all(f in ((0, 0, 0), (0, 0, 1)) for f in flags)
    synthetic = '''Begin final coordinates\nATOMIC_POSITIONS (crystal)\n''' + '\n'.join(f'Ru 0 0 {i/20:.8f}' for i in range(17)) + '''\nEnd final coordinates\n'''
    assert len(parse_final_positions(synthetic, 17) or []) == 17
    fake_forces = '\n'.join(f'atom {i} type 1 force = 0.0 0.0 {1e-4 if i in (1,2,16,17) else 2e-4}' for i in range(1,18))
    fm = final_force_metrics(fake_forces, 17); assert fm is not None and fm['max_abs_movable_z_force_ev_per_angstrom'] < FORCE_LIMIT_EV_PER_ANG
    assert abs(FORC_CONV_THR_RY_PER_BOHR - 0.000777876152459555) < 1e-15
    print('SYSTEM3_CLEAN_RU0001_RELAXATION_IMPLEMENTATION_SELF_TEST_PASS')
    print('PRODUCTION_EXECUTION_AUTHORIZED=false')
    print('REQUIRES_COMMITTED_ROBUSTNESS_SUPPORTED=true')
    print('LAYERS=17 VACUUM=15 K=24x24x1')
    print('MOVABLE_LAYERS=outer_two_each_face Z_ONLY')
    print(f'FORCE_LIMIT_EV_PER_ANGSTROM={FORCE_LIMIT_EV_PER_ANG}')
    print(f'FORC_CONV_THR_RY_PER_BOHR={FORC_CONV_THR_RY_PER_BOHR:.15f}')


def add_contract_args(sp: argparse.ArgumentParser) -> None:
    sp.add_argument('--protocol', required=True)
    sp.add_argument('--pass-evidence', required=True)


def main() -> None:
    ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest='cmd', required=True)
    sp = sub.add_parser('self-test'); add_contract_args(sp); sp.set_defaults(func=self_test)
    sp = sub.add_parser('run-relax-segment'); add_contract_args(sp); sp.add_argument('--robustness', required=True); sp.add_argument('--segment', type=int, required=True); sp.add_argument('--previous'); sp.add_argument('--pw', required=True); sp.add_argument('--pseudo-dir', required=True); sp.add_argument('--out', required=True); sp.set_defaults(func=run_relax_segment)
    sp = sub.add_parser('run-reproduction'); sp.add_argument('--relax-result', required=True); sp.add_argument('--pw', required=True); sp.add_argument('--pseudo-dir', required=True); sp.add_argument('--out', required=True); sp.set_defaults(func=run_reproduction)
    sp = sub.add_parser('adjudicate'); sp.add_argument('--protocol', required=True); sp.add_argument('--relax-result', required=True); sp.add_argument('--reproduction-result', required=True); sp.add_argument('--out', required=True); sp.set_defaults(func=adjudicate)
    args = ap.parse_args(); args.func(args)


if __name__ == '__main__':
    main()
