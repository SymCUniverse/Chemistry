#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
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

RECOVERY_SCHEMA = 'h-ru0001-l19-second-timeout-native-checkpoint-recovery-v0.1'
RECOVERY_STATUS = 'FROZEN_AFTER_SECOND_MECHANICAL_TIMEOUT_BEFORE_CHECKPOINT_RECOVERY_RESULTS'
RECOVERY_BLOB_SHA = '929d8de8720c755bd7bbc059b0a2f9c1f68266c0'
EXTENSION_BLOB_SHA = '952e1358b3af4ce637f3c9283e475adc1ae30b0f'
SOURCE_BLOB_SHA = 'ee7ff62d563ca5c96bb70b43c3a2ba3cc8ee21ca'
L15_BLOB_SHA = 'ad5022922ef59ffcbed8943ee8419ad2c27cbc8d'
L17_BLOB_SHA = '08ccb8b1dc37a1ff81c868db9db0285f97b6efc8'
PW_SHA256 = '2b1ede22d276b1d4dab3e31212f306e88ae57e00f33ce6b532b849493a457855'
RU_SHA256 = 'ed637e8481a2fddda6a93863a92f8b0b857379b9db23325a4664e3df0a6f45bd'
ENERGY_RE = re.compile(r'!\s+total energy\s+=\s+([-+0-9.Ee]+)\s+Ry')
CLEAN_STOP_MARKER = 'Maximum CPU time exceeded'
TAG = 'slab_L19_V15_K16_16_1_extension'


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def load(path: str | Path) -> dict[str, Any]:
    obj = json.loads(Path(path).read_text())
    if not isinstance(obj, dict):
        raise SystemExit(f'MECHANICAL_HOLD: JSON object required: {path}')
    return obj


def write(path: str | Path, obj: dict[str, Any]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, sort_keys=True) + '\n')


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def recursive_manifest(root: Path) -> dict[str, Any]:
    files = []
    total = 0
    for p in sorted(x for x in root.rglob('*') if x.is_file()):
        rel = p.relative_to(root).as_posix()
        size = p.stat().st_size
        total += size
        files.append({'path': rel, 'sha256': sha256(p), 'size_bytes': size})
    return {
        'schema': 'system3-l19-qe-native-restart-manifest-v0.1',
        'file_count': len(files),
        'size_bytes': total,
        'files': files,
    }


def contract(args: argparse.Namespace) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    rp = Path(args.recovery).resolve()
    pp = Path(args.protocol).resolve()
    sp = Path(args.source_evidence).resolve()
    l15p = Path(args.l15_interim).resolve()
    l17p = Path(args.l17_interim).resolve()
    if git_blob_sha(rp) != RECOVERY_BLOB_SHA:
        raise SystemExit('MECHANICAL_HOLD: checkpoint recovery record blob mismatch')
    if git_blob_sha(pp) != EXTENSION_BLOB_SHA:
        raise SystemExit('MECHANICAL_HOLD: extension protocol blob mismatch')
    if git_blob_sha(sp) != SOURCE_BLOB_SHA:
        raise SystemExit('MECHANICAL_HOLD: source evidence blob mismatch')
    if git_blob_sha(l15p) != L15_BLOB_SHA or git_blob_sha(l17p) != L17_BLOB_SHA:
        raise SystemExit('MECHANICAL_HOLD: preserved valid L15/L17 evidence blob mismatch')
    r = load(rp)
    p = load(pp)
    s = load(sp)
    if r.get('schema') != RECOVERY_SCHEMA or r.get('status') != RECOVERY_STATUS:
        raise SystemExit('SCIENTIFIC_HOLD: checkpoint recovery record not frozen')
    if r.get('scope') != 'MECHANICAL_EXECUTION_RECOVERY_ONLY':
        raise SystemExit('SCIENTIFIC_HOLD: recovery escaped mechanical-only scope')
    if r['lineage']['extension_protocol']['sha256'] != sha256(pp):
        raise SystemExit('MECHANICAL_HOLD: extension SHA256 lineage mismatch')
    if r['lineage']['source_evidence']['sha256'] != sha256(sp):
        raise SystemExit('MECHANICAL_HOLD: source SHA256 lineage mismatch')
    f = r['frozen_scientific_settings']
    pf = p['frozen_numerical_settings']
    pairs = [
        ('a_angstrom', 'a_angstrom'), ('c_angstrom', 'c_angstrom'),
        ('bulk_energy_ev_per_atom', 'bulk_energy_ev_per_atom'),
        ('ecutwfc_ry', 'ecutwfc_ry'), ('ecutrho_ry', 'ecutrho_ry'),
        ('degauss_ry', 'degauss_ry'), ('electron_conv_thr', 'electron_conv_thr'),
        ('mixing_beta', 'mixing_beta'), ('electron_maxstep', 'electron_maxstep'),
        ('total_vacuum_angstrom', 'total_vacuum_angstrom'),
        ('absolute_surface_excess_tolerance_ev_per_surface_atom', 'absolute_surface_excess_tolerance_ev_per_surface_atom'),
    ]
    for a, b in pairs:
        if float(f[a]) != float(pf[b]):
            raise SystemExit(f'SCIENTIFIC_HOLD: frozen L19 setting drift: {a}')
    if f['surface_kmesh'] != pf['surface_kmesh'] or int(f['layers']) != 19:
        raise SystemExit('SCIENTIFIC_HOLD: L19 grid identity drift')
    if float(f['absolute_surface_excess_tolerance_ev_per_surface_atom']) != 0.001:
        raise SystemExit('SCIENTIFIC_HOLD: 1 meV acceptance threshold drift')
    if any(bool(v) for v in p['evidence_firewall'].values()):
        raise SystemExit('SCIENTIFIC_HOLD: evidence firewall opened')
    if any(r['provenance'][k] is not False for k in [
        'scientific_settings_changed', 'thresholds_changed', 'evidence_firewall_changed',
        'layer_selection_rule_changed', 'kinetic_inputs_used', 'chi_used',
        'published_H_Ru_outcomes_used', 'System2_outcomes_used', 'paid_compute_used']):
        raise SystemExit('SCIENTIFIC_HOLD: checkpoint recovery provenance drift')
    if r['checkpoint_recovery']['method'] != 'QE_NATIVE_RESTART_ACROSS_FRESH_STANDARD_GITHUB_JOBS':
        raise SystemExit('MECHANICAL_HOLD: checkpoint recovery method drift')
    if int(r['checkpoint_recovery']['segment_max_seconds']) != 13800:
        raise SystemExit('MECHANICAL_HOLD: checkpoint segment time drift')
    attempts = r['failed_l19_attempts']
    if [x['timeout_seconds'] for x in attempts] != [7200, 14400]:
        raise SystemExit('MECHANICAL_HOLD: source timeout lineage incomplete')
    if any(x['valid'] or x['measured'] or x['job_done'] for x in attempts):
        raise SystemExit('SCIENTIFIC_HOLD: invalid timeout promoted as evidence')
    return r, p, s


def verify_runtime(r: dict[str, Any], pw: Path, pseudo_dir: Path) -> Path:
    ru = pseudo_dir / 'Ru.nc.pbe.z_16.oncvpsp4.sg15.v0.upf'
    if sha256(pw) != PW_SHA256 or sha256(pw) != r['runtime_identity']['pw_x_sha256']:
        raise SystemExit('MECHANICAL_HOLD: pw.x identity mismatch')
    if not ru.is_file() or sha256(ru) != RU_SHA256 or sha256(ru) != r['runtime_identity']['ru_pseudo_sha256']:
        raise SystemExit('MECHANICAL_HOLD: Ru pseudopotential identity mismatch')
    return ru


def build_input(r: dict[str, Any], pseudo_dir: Path, outdir: Path, restart_mode: str) -> str:
    f = r['frozen_scientific_settings']
    txt = base.slab_input(
        float(f['a_angstrom']), float(f['c_angstrom']), 19,
        float(f['total_vacuum_angstrom']), int(f['ecutwfc_ry']), int(f['ecutrho_ry']),
        tuple(f['surface_kmesh']), pseudo_dir.resolve(), str(outdir.resolve()), TAG,
    )
    control_insert = (
        f" restart_mode='{restart_mode}',\n"
        " disk_io='medium',\n"
        f" max_seconds={float(r['checkpoint_recovery']['segment_max_seconds']):.6f},\n"
    )
    needle = " calculation='scf',\n"
    if needle not in txt:
        raise SystemExit('MECHANICAL_HOLD: unable to bind QE checkpoint controls')
    return txt.replace(needle, needle + control_insert, 1)


def validate_previous(previous: Path) -> tuple[bool, Path | None]:
    complete = previous / 'COMPLETE.json'
    if complete.is_file():
        c = load(complete)
        result = previous / 'SYSTEM3_LAYER_L19_RESULT.json'
        if c.get('status') != 'VALID_EXTENSION_LAYER' or not result.is_file() or sha256(result) != c.get('result_sha256'):
            raise SystemExit('MECHANICAL_HOLD: completed previous segment bundle failed integrity check')
        return True, result
    manifest_path = previous / 'checkpoint_manifest.json'
    state = previous / 'restart_state'
    if not manifest_path.is_file() or not state.is_dir():
        raise SystemExit('MECHANICAL_HOLD: previous checkpoint bundle incomplete')
    expected = load(manifest_path)
    actual = recursive_manifest(state)
    if expected != actual:
        raise SystemExit('MECHANICAL_HOLD: recursive checkpoint manifest mismatch')
    save = state / f'{TAG}.save'
    if not save.is_dir() or not (save / 'data-file-schema.xml').is_file():
        raise SystemExit('MECHANICAL_HOLD: native QE save directory missing')
    return False, None


def run_segment(args: argparse.Namespace) -> None:
    r, p, s = contract(args)
    pw = Path(args.pw).resolve()
    pseudo = Path(args.pseudo_dir).resolve()
    verify_runtime(r, pw, pseudo)
    seg = int(args.segment)
    if seg < 1 or seg > int(r['checkpoint_recovery']['maximum_predeclared_segments']):
        raise SystemExit('MECHANICAL_HOLD: segment outside frozen range')
    out = Path(args.out).resolve()
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    state = out / 'restart_state'
    previous = Path(args.previous).resolve() if args.previous else None
    if seg == 1:
        if previous is not None:
            raise SystemExit('MECHANICAL_HOLD: segment 1 must start without previous state')
        restart_mode = 'from_scratch'
        state.mkdir()
    else:
        if previous is None:
            raise SystemExit('MECHANICAL_HOLD: resumed segment requires previous bundle')
        already_complete, result = validate_previous(previous)
        if already_complete:
            shutil.copy2(result, out / 'SYSTEM3_LAYER_L19_RESULT.json')
            c = load(previous / 'COMPLETE.json')
            c['passthrough_segment'] = seg
            write(out / 'COMPLETE.json', c)
            print(f'SYSTEM3_L19_SEGMENT_{seg}_PASSTHROUGH_COMPLETE')
            return
        shutil.copytree(previous / 'restart_state', state)
        restart_mode = 'restart'
    inp = out / f'l19_segment_{seg}.in'
    stdout = out / f'l19_segment_{seg}.out'
    txt = build_input(r, pseudo, state, restart_mode)
    inp.write_text(txt)
    env = dict(os.environ)
    env.update(OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1')
    start = time.time()
    external_timeout = int(r['checkpoint_recovery']['external_wrapper_timeout_seconds'])
    external_kill = False
    with inp.open('rb') as fi, stdout.open('wb') as fo:
        proc = subprocess.Popen([str(pw)], stdin=fi, stdout=fo, stderr=subprocess.STDOUT, env=env)
        try:
            rc = proc.wait(timeout=external_timeout)
        except subprocess.TimeoutExpired:
            external_kill = True
            proc.terminate()
            try:
                rc = proc.wait(timeout=30)
            except subprocess.TimeoutExpired:
                proc.kill()
                rc = proc.wait(timeout=10)
    elapsed = time.time() - start
    text = stdout.read_text(errors='replace')
    energies = [float(x) * base.RY_TO_EV for x in ENERGY_RE.findall(text)]
    job_done = 'JOB DONE.' in text
    clean_stop = CLEAN_STOP_MARKER in text
    if external_kill:
        raise SystemExit('MECHANICAL_HOLD: external wrapper killed L19 before native checkpoint persistence')
    meta = {
        'schema': 'h-ru0001-l19-native-checkpoint-segment-v0.1',
        'segment': seg,
        'restart_mode': restart_mode,
        'return_code': int(rc),
        'elapsed_s': elapsed,
        'job_done': job_done,
        'clean_qe_max_seconds_stop': clean_stop,
        'energy_count': len(energies),
        'input_sha256': sha256(inp),
        'output_sha256': sha256(stdout),
        'pw_x_sha256': sha256(pw),
        'ru_pseudo_sha256': sha256(pseudo / 'Ru.nc.pbe.z_16.oncvpsp4.sg15.v0.upf'),
        'scientific_settings_changed': False,
        'thresholds_changed': False,
        'paid_compute_used': False,
    }
    write(out / f'SEGMENT_{seg}_METADATA.json', meta)
    if job_done and rc == 0 and energies:
        f = r['frozen_scientific_settings']
        gamma = (energies[-1] - 19 * float(f['bulk_energy_ev_per_atom'])) / 2.0
        cell_z, _ = base.slab_geometry(float(f['a_angstrom']), float(f['c_angstrom']), 19, float(f['total_vacuum_angstrom']))
        row = {
            'schema': 'h-ru0001-layer-extension-case-v0.1',
            'status': 'VALID_EXTENSION_LAYER',
            'tag': TAG,
            'execution_state': {'PLANNED': True, 'EXECUTED': True, 'MEASURED': True, 'VALID': True, 'ADJUDICATED': False},
            'return_code': 0,
            'timeout': False,
            'job_done': True,
            'energy_count': len(energies),
            'elapsed_s': elapsed,
            'energy_ev': energies[-1],
            'layers': 19,
            'surface_excess_ev_per_surface_atom': gamma,
            'total_vacuum_angstrom': float(f['total_vacuum_angstrom']),
            'cell_z_angstrom': cell_z,
            'kmesh': list(f['surface_kmesh']),
            'ecutwfc_ry': int(f['ecutwfc_ry']),
            'ecutrho_ry': int(f['ecutrho_ry']),
            'input_sha256': sha256(inp),
            'output_sha256': sha256(stdout),
            'protocol_sha256': sha256(Path(args.protocol).resolve()),
            'source_evidence_sha256': sha256(Path(args.source_evidence).resolve()),
            'checkpoint_recovery_record_sha256': sha256(Path(args.recovery).resolve()),
            'checkpoint_recovery_segment': seg,
            'restart_mode': restart_mode,
            'scientific_settings_changed': False,
            'thresholds_changed': False,
            'paid_compute_used': False,
        }
        result_path = out / 'SYSTEM3_LAYER_L19_RESULT.json'
        write(result_path, row)
        write(out / 'COMPLETE.json', {
            'status': 'VALID_EXTENSION_LAYER',
            'segment_completed': seg,
            'result_sha256': sha256(result_path),
            'batch_adjudicated': False,
        })
        shutil.rmtree(state, ignore_errors=True)
        print(json.dumps(row, indent=2, sort_keys=True))
        print(f'SYSTEM3_L19_VALID_ON_CHECKPOINT_SEGMENT_{seg}')
        return
    if not clean_stop:
        raise SystemExit('MECHANICAL_HOLD: L19 segment neither completed nor produced a verified QE max_seconds clean stop')
    save = state / f'{TAG}.save'
    if not save.is_dir() or not (save / 'data-file-schema.xml').is_file():
        raise SystemExit('MECHANICAL_HOLD: QE clean stop did not preserve a valid native save directory')
    manifest = recursive_manifest(state)
    write(out / 'checkpoint_manifest.json', manifest)
    write(out / 'CHECKPOINT.json', {
        'status': 'VALID_NATIVE_QE_CHECKPOINT_NOT_SCIENTIFIC_EVIDENCE',
        'segment': seg,
        'checkpoint_manifest_sha256': sha256(out / 'checkpoint_manifest.json'),
        'file_count': manifest['file_count'],
        'size_bytes': manifest['size_bytes'],
        'scientific_result_available': False,
    })
    print(f'SYSTEM3_L19_SEGMENT_{seg}_CHECKPOINT_READY')


def materialize_interim(args: argparse.Namespace) -> None:
    r, p, s = contract(args)
    layer = int(args.layers)
    if layer not in {15, 17}:
        raise SystemExit('MECHANICAL_HOLD: only preserved L15/L17 may be materialized')
    src = load(args.l15_interim if layer == 15 else args.l17_interim)
    if src.get('status') != 'VALID_INTERIM_LAYER_EVIDENCE_NOT_BATCH_ADJUDICATED':
        raise SystemExit('MECHANICAL_HOLD: interim evidence status mismatch')
    m = src['measurement']
    if int(m['layers']) != layer or not m['job_done'] or m['return_code'] != 0 or m['timeout']:
        raise SystemExit('MECHANICAL_HOLD: interim measurement is not valid')
    row = {
        'schema': 'h-ru0001-layer-extension-case-v0.1',
        'status': 'VALID_EXTENSION_LAYER',
        'tag': m['tag'],
        'execution_state': {'PLANNED': True, 'EXECUTED': True, 'MEASURED': True, 'VALID': True, 'ADJUDICATED': False},
        'return_code': 0,
        'timeout': False,
        'job_done': True,
        'energy_count': int(m['energy_count']),
        'elapsed_s': float(m['elapsed_s']),
        'energy_ev': float(m['energy_ev']),
        'layers': layer,
        'surface_excess_ev_per_surface_atom': float(m['surface_excess_ev_per_surface_atom']),
        'total_vacuum_angstrom': float(m['total_vacuum_angstrom']),
        'cell_z_angstrom': float(m['cell_z_angstrom']),
        'kmesh': list(m['kmesh']),
        'ecutwfc_ry': int(m['ecutwfc_ry']),
        'ecutrho_ry': int(m['ecutrho_ry']),
        'input_sha256': m['input_sha256'],
        'output_sha256': m['output_sha256'],
        'protocol_sha256': sha256(Path(args.protocol).resolve()),
        'source_evidence_sha256': sha256(Path(args.source_evidence).resolve()),
        'scientific_settings_changed': False,
        'thresholds_changed': False,
        'paid_compute_used': False,
        'materialized_from_interim_evidence': True,
    }
    write(args.out, row)
    print(f'SYSTEM3_L{layer}_INTERIM_MATERIALIZED')


def finalize(args: argparse.Namespace) -> None:
    r, p, s = contract(args)
    bundle = Path(args.bundle).resolve()
    complete, result = validate_previous(bundle)
    if not complete or result is None:
        raise SystemExit('MECHANICAL_HOLD: all predeclared L19 checkpoint segments exhausted without valid completion')
    row = load(result)
    if row.get('status') != 'VALID_EXTENSION_LAYER' or int(row.get('layers', 0)) != 19:
        raise SystemExit('MECHANICAL_HOLD: final L19 result identity mismatch')
    if row.get('protocol_sha256') != sha256(Path(args.protocol).resolve()) or row.get('source_evidence_sha256') != sha256(Path(args.source_evidence).resolve()):
        raise SystemExit('MECHANICAL_HOLD: final L19 result provenance mismatch')
    if row.get('scientific_settings_changed') is not False or row.get('thresholds_changed') is not False:
        raise SystemExit('SCIENTIFIC_HOLD: final L19 result reports scientific drift')
    shutil.copy2(result, args.out)
    print('SYSTEM3_L19_CHECKPOINT_RECOVERY_FINALIZED_VALID')


def self_test(args: argparse.Namespace) -> None:
    r, p, s = contract(args)
    assert r['checkpoint_recovery']['segment_max_seconds'] < r['checkpoint_recovery']['external_wrapper_timeout_seconds']
    assert r['checkpoint_recovery']['external_wrapper_timeout_seconds'] < r['checkpoint_recovery']['github_job_timeout_minutes'] * 60
    assert r['acceptance']['batch_adjudication_must_use_original_extension_runner_and_unchanged_suffix_rule'] is True
    assert r['acceptance']['layer_extension_pass_must_feed_original_coupled_endpoint_recheck'] is True
    assert r['acceptance']['direct_relaxation_after_layer_extension_pass_forbidden'] is True
    assert r['acceptance']['hold_route_if_original_adjudicator_returns_hold'] == [21, 23, 25]
    txt = build_input(r, Path('/tmp/pseudo'), Path('/tmp/restart_state'), 'from_scratch')
    for needle in ["restart_mode='from_scratch'", "disk_io='medium'", 'max_seconds=13800.000000', 'ecutwfc=70', 'ecutrho=280', '16 16 1 0 0 0']:
        assert needle in txt
    print('SYSTEM3_L19_NATIVE_CHECKPOINT_RECOVERY_SELF_TEST_PASS')
    print('MECHANICAL_ONLY=true')
    print('SEGMENT_MAX_SECONDS=13800')
    print('MAX_SEGMENTS=3')
    print('FROZEN_TOLERANCE_EV_PER_SURFACE_ATOM=0.001')
    print('PASS_REQUIRES_COUPLED_ENDPOINT_RECHECK=true')


def add_common(sp: argparse.ArgumentParser) -> None:
    sp.add_argument('--protocol', required=True)
    sp.add_argument('--source-evidence', required=True)
    sp.add_argument('--recovery', required=True)
    sp.add_argument('--l15-interim', required=True)
    sp.add_argument('--l17-interim', required=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd', required=True)
    sp = sub.add_parser('self-test'); add_common(sp); sp.set_defaults(func=self_test)
    sp = sub.add_parser('run-segment'); add_common(sp)
    sp.add_argument('--segment', type=int, required=True); sp.add_argument('--previous')
    sp.add_argument('--pw', required=True); sp.add_argument('--pseudo-dir', required=True); sp.add_argument('--out', required=True)
    sp.set_defaults(func=run_segment)
    sp = sub.add_parser('materialize-interim'); add_common(sp)
    sp.add_argument('--layers', type=int, required=True); sp.add_argument('--out', required=True); sp.set_defaults(func=materialize_interim)
    sp = sub.add_parser('finalize'); add_common(sp)
    sp.add_argument('--bundle', required=True); sp.add_argument('--out', required=True); sp.set_defaults(func=finalize)
    args = ap.parse_args(); args.func(args)


if __name__ == '__main__':
    main()
