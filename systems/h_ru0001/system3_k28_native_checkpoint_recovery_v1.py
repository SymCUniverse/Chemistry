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

RECOVERY_SCHEMA = 'h-ru0001-post-hold-k28-native-checkpoint-recovery-v0.1'
RECOVERY_STATUS = 'FROZEN_AFTER_K28_MECHANICAL_TIMEOUT_BEFORE_CHECKPOINT_RECOVERY_RESULTS'
RECOVERY_BLOB_SHA = '84e7634338cb4b273d437f00cb9411e12228e48f'
DIAGNOSTIC_PROTOCOL_BLOB_SHA = 'b943664b17abaef3c478cffbf66b1600c558a09f'
HOLD_BLOB_SHA = '5f975b604eda3942eef87d215fb1eaf096f17cef'
K24_EVIDENCE_BLOB_SHA = '5e847f901eb6c837099da60c8877fb49eabf2f00'
PW_SHA256 = '2b1ede22d276b1d4dab3e31212f306e88ae57e00f33ce6b532b849493a457855'
RU_SHA256 = 'ed637e8481a2fddda6a93863a92f8b0b857379b9db23325a4664e3df0a6f45bd'
TAG = 'post_hold_kmesh_L17_V15_K28'
ENERGY_RE = re.compile(r'!\s+total energy\s+=\s+([-+0-9.Ee]+)\s+Ry')
CLEAN_STOP_MARKER = 'Maximum CPU time exceeded'
K28_RESULT = 'SYSTEM3_POST_HOLD_K28_RESULT.json'
K24_RESULT = 'SYSTEM3_POST_HOLD_K24_RESULT.json'


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
        'schema': 'system3-k28-qe-native-restart-manifest-v0.1',
        'file_count': len(files),
        'size_bytes': total,
        'files': files,
    }


def contract(args: argparse.Namespace) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    rp = Path(args.recovery).resolve()
    pp = Path(args.protocol).resolve()
    hp = Path(args.hold).resolve()
    kp = Path(args.k24_evidence).resolve()
    expected = [
        (rp, RECOVERY_BLOB_SHA),
        (pp, DIAGNOSTIC_PROTOCOL_BLOB_SHA),
        (hp, HOLD_BLOB_SHA),
        (kp, K24_EVIDENCE_BLOB_SHA),
    ]
    for path, blob in expected:
        if git_blob_sha(path) != blob:
            raise SystemExit(f'MECHANICAL_HOLD: frozen blob drift: {path.name}')
    recovery, protocol, hold, k24 = map(load, [rp, pp, hp, kp])
    if recovery.get('schema') != RECOVERY_SCHEMA or recovery.get('status') != RECOVERY_STATUS:
        raise SystemExit('SCIENTIFIC_HOLD: K28 recovery record not frozen')
    if recovery.get('scope') != 'MECHANICAL_EXECUTION_RECOVERY_ONLY':
        raise SystemExit('SCIENTIFIC_HOLD: K28 recovery escaped mechanical-only scope')
    if protocol.get('status') != 'FROZEN_BEFORE_POST_HOLD_K24_K28_RESULTS':
        raise SystemExit('SCIENTIFIC_HOLD: diagnostic protocol state drift')
    if hold.get('status') != 'CLEAN_SURFACE_COUPLED_CONVERGENCE_HOLD' or hold.get('adjudication', {}).get('failed_axis') != 'kmesh':
        raise SystemExit('SCIENTIFIC_HOLD: source coupled HOLD identity mismatch')
    if k24.get('status') != 'VALID_POST_HOLD_KMESH_DIAGNOSTIC_CASE_PRESERVED':
        raise SystemExit('MECHANICAL_HOLD: preserved K24 evidence status mismatch')
    k24r = k24.get('result', {})
    if k24r.get('status') != 'VALID_POST_HOLD_KMESH_DIAGNOSTIC_CASE' or k24r.get('kmesh') != [24, 24, 1]:
        raise SystemExit('MECHANICAL_HOLD: preserved K24 result identity mismatch')
    if not k24r.get('job_done') or k24r.get('timeout') or int(k24r.get('return_code', 1)) != 0:
        raise SystemExit('MECHANICAL_HOLD: preserved K24 is not valid completed evidence')
    if abs(float(k24r['surface_excess_ev_per_surface_atom']) - 1.0945347456436139) > 1e-15:
        raise SystemExit('MECHANICAL_HOLD: preserved K24 value drift')
    ps = protocol['frozen_scientific_settings']
    rs = recovery['frozen_scientific_settings']
    for key in [
        'layers', 'total_vacuum_angstrom', 'a_angstrom', 'c_angstrom',
        'bulk_energy_ev_per_atom', 'ecutwfc_ry', 'ecutrho_ry', 'exchange_correlation',
        'occupations', 'smearing', 'degauss_ry', 'electron_conv_thr',
        'electron_maxstep', 'mixing_beta', 'surface_geometry', 'electrostatics',
        'absolute_surface_excess_tolerance_ev_per_surface_atom',
    ]:
        if rs[key] != ps[key]:
            raise SystemExit(f'SCIENTIFIC_HOLD: frozen K28 setting drift: {key}')
    if rs['surface_kmesh'] != [28, 28, 1] or ps['terminal_reference'] != [28, 28, 1]:
        raise SystemExit('SCIENTIFIC_HOLD: K28 terminal grid identity drift')
    if float(rs['absolute_surface_excess_tolerance_ev_per_surface_atom']) != 0.001:
        raise SystemExit('SCIENTIFIC_HOLD: 1 meV decision threshold drift')
    cp = recovery['checkpoint_recovery']
    if cp['method'] != 'QE_NATIVE_RESTART_ACROSS_FRESH_STANDARD_GITHUB_JOBS':
        raise SystemExit('MECHANICAL_HOLD: K28 checkpoint method drift')
    if int(cp['segment_max_seconds']) != 13800 or int(cp['external_wrapper_timeout_seconds']) != 14700:
        raise SystemExit('MECHANICAL_HOLD: K28 checkpoint time contract drift')
    if int(cp['maximum_predeclared_segments']) != 3:
        raise SystemExit('MECHANICAL_HOLD: K28 maximum segment count drift')
    failed = recovery['lineage']['failed_K28_attempt']
    if failed['classification'] != 'MECHANICAL_WALL_CLOCK_TIMEOUT' or failed['job_done'] or int(failed['valid_final_energy_count']) != 0:
        raise SystemExit('SCIENTIFIC_HOLD: invalid K28 timeout promoted as evidence')
    if failed['partial_output_may_be_used_for_adjudication'] is not False or failed['native_checkpoint_was_preserved'] is not False:
        raise SystemExit('SCIENTIFIC_HOLD: failed K28 partial-output firewall drift')
    acc = recovery['acceptance']
    for key in [
        'K28_valid_only_if_JOB_DONE', 'K28_valid_only_if_return_code_zero',
        'K28_valid_only_if_final_total_energy_present',
        'K24_must_be_materialized_from_preserved_valid_evidence_not_rerun',
        'final_diagnostic_must_use_original_frozen_K20_K24_K28_rule',
        'diagnostic_may_not_emit_CLEAN_SURFACE_FIXED_GRID_PASS',
        'diagnostic_may_not_authorize_relaxation', 'successor_protocol_required_after_diagnostic',
    ]:
        if acc[key] is not True:
            raise SystemExit(f'SCIENTIFIC_HOLD: K28 recovery acceptance firewall drift: {key}')
    prov = recovery['provenance']
    if prov['mechanical_only_change'] is not True or prov['original_K16_coupled_hold_preserved'] is not True:
        raise SystemExit('SCIENTIFIC_HOLD: K28 recovery provenance identity drift')
    for key in [
        'scientific_settings_changed', 'thresholds_changed', 'evidence_firewall_changed',
        'kinetic_inputs_used', 'chi_used', 'published_H_Ru_outcomes_used',
        'System2_outcomes_used', 'paid_compute_used',
    ]:
        if prov[key] is not False:
            raise SystemExit(f'SCIENTIFIC_HOLD: K28 recovery provenance firewall opened: {key}')
    return recovery, protocol, hold, k24


def verify_runtime(recovery: dict[str, Any], pw: Path, pseudo_dir: Path) -> Path:
    ru = pseudo_dir / 'Ru.nc.pbe.z_16.oncvpsp4.sg15.v0.upf'
    if not pw.is_file() or sha256(pw) != PW_SHA256 or sha256(pw) != recovery['runtime_identity']['pw_x_sha256']:
        raise SystemExit('MECHANICAL_HOLD: pw.x identity mismatch')
    if not ru.is_file() or sha256(ru) != RU_SHA256 or sha256(ru) != recovery['runtime_identity']['ru_pseudo_sha256']:
        raise SystemExit('MECHANICAL_HOLD: Ru pseudopotential identity mismatch')
    return ru


def build_input(recovery: dict[str, Any], pseudo_dir: Path, outdir: Path, restart_mode: str) -> str:
    f = recovery['frozen_scientific_settings']
    txt = base.slab_input(
        float(f['a_angstrom']), float(f['c_angstrom']), int(f['layers']),
        float(f['total_vacuum_angstrom']), int(f['ecutwfc_ry']), int(f['ecutrho_ry']),
        tuple(f['surface_kmesh']), pseudo_dir.resolve(), str(outdir.resolve()), TAG,
    )
    control_insert = (
        f" restart_mode='{restart_mode}',\n"
        " disk_io='medium',\n"
        f" max_seconds={float(recovery['checkpoint_recovery']['segment_max_seconds']):.6f},\n"
    )
    needle = " calculation='scf',\n"
    if needle not in txt:
        raise SystemExit('MECHANICAL_HOLD: unable to bind K28 QE checkpoint controls')
    return txt.replace(needle, needle + control_insert, 1)


def validate_previous(previous: Path) -> tuple[bool, Path | None]:
    complete = previous / 'COMPLETE.json'
    if complete.is_file():
        c = load(complete)
        result = previous / K28_RESULT
        if c.get('status') != 'VALID_POST_HOLD_KMESH_DIAGNOSTIC_CASE' or not result.is_file() or sha256(result) != c.get('result_sha256'):
            raise SystemExit('MECHANICAL_HOLD: completed previous K28 segment bundle failed integrity check')
        return True, result
    manifest_path = previous / 'checkpoint_manifest.json'
    state = previous / 'restart_state'
    if not manifest_path.is_file() or not state.is_dir():
        raise SystemExit('MECHANICAL_HOLD: previous K28 checkpoint bundle incomplete')
    expected = load(manifest_path)
    actual = recursive_manifest(state)
    if expected != actual:
        raise SystemExit('MECHANICAL_HOLD: recursive K28 checkpoint manifest mismatch')
    save = state / f'{TAG}.save'
    if not save.is_dir() or not (save / 'data-file-schema.xml').is_file():
        raise SystemExit('MECHANICAL_HOLD: K28 native QE save directory missing')
    return False, None


def wait_with_heartbeat(proc: subprocess.Popen, stdout: Path, external_timeout: int, interval: int) -> tuple[int, bool, float]:
    start = time.time()
    next_heartbeat = float(interval)
    external_kill = False
    while True:
        rc = proc.poll()
        elapsed = time.time() - start
        if rc is not None:
            return int(rc), external_kill, elapsed
        if elapsed >= external_timeout:
            external_kill = True
            proc.terminate()
            try:
                rc = proc.wait(timeout=30)
            except subprocess.TimeoutExpired:
                proc.kill()
                rc = proc.wait(timeout=10)
            return int(rc), external_kill, time.time() - start
        if elapsed >= next_heartbeat:
            size = stdout.stat().st_size if stdout.exists() else 0
            print(f'K28_CHECKPOINT_HEARTBEAT elapsed_s={int(elapsed)} stdout_bytes={size}', flush=True)
            next_heartbeat += interval
        time.sleep(15)


def run_segment(args: argparse.Namespace) -> None:
    recovery, protocol, hold, k24 = contract(args)
    pw = Path(args.pw).resolve()
    pseudo = Path(args.pseudo_dir).resolve()
    verify_runtime(recovery, pw, pseudo)
    seg = int(args.segment)
    if seg < 1 or seg > int(recovery['checkpoint_recovery']['maximum_predeclared_segments']):
        raise SystemExit('MECHANICAL_HOLD: K28 segment outside frozen range')
    out = Path(args.out).resolve()
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    state = out / 'restart_state'
    previous = Path(args.previous).resolve() if args.previous else None
    if seg == 1:
        if previous is not None:
            raise SystemExit('MECHANICAL_HOLD: K28 segment 1 must start without previous state')
        restart_mode = 'from_scratch'
        state.mkdir()
    else:
        if previous is None:
            raise SystemExit('MECHANICAL_HOLD: resumed K28 segment requires previous bundle')
        already_complete, result = validate_previous(previous)
        if already_complete:
            shutil.copy2(result, out / K28_RESULT)
            c = load(previous / 'COMPLETE.json')
            c['passthrough_segment'] = seg
            write(out / 'COMPLETE.json', c)
            print(f'SYSTEM3_K28_SEGMENT_{seg}_PASSTHROUGH_COMPLETE')
            return
        shutil.copytree(previous / 'restart_state', state)
        restart_mode = 'restart'
    inp = out / f'k28_segment_{seg}.in'
    stdout = out / f'k28_segment_{seg}.out'
    inp.write_text(build_input(recovery, pseudo, state, restart_mode), encoding='utf-8')
    env = dict(os.environ)
    env.update(OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1')
    external_timeout = int(recovery['checkpoint_recovery']['external_wrapper_timeout_seconds'])
    heartbeat = int(recovery['checkpoint_recovery']['heartbeat_interval_seconds'])
    with inp.open('rb') as fi, stdout.open('wb') as fo:
        proc = subprocess.Popen([str(pw)], stdin=fi, stdout=fo, stderr=subprocess.STDOUT, env=env)
        rc, external_kill, elapsed = wait_with_heartbeat(proc, stdout, external_timeout, heartbeat)
    text = stdout.read_text(errors='replace')
    energies = [float(x) * base.RY_TO_EV for x in ENERGY_RE.findall(text)]
    job_done = 'JOB DONE.' in text
    clean_stop = CLEAN_STOP_MARKER in text
    meta = {
        'schema': 'h-ru0001-k28-native-checkpoint-segment-v0.1',
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
        'kinetic_inputs_used': False,
        'chi_used': False,
        'paid_compute_used': False,
        'original_K16_coupled_hold_preserved': True,
    }
    write(out / f'SEGMENT_{seg}_METADATA.json', meta)
    if external_kill:
        raise SystemExit('MECHANICAL_HOLD: external wrapper killed K28 before native checkpoint persistence')
    if job_done and rc == 0 and energies:
        f = recovery['frozen_scientific_settings']
        gamma = (energies[-1] - int(f['layers']) * float(f['bulk_energy_ev_per_atom'])) / 2.0
        row = {
            'schema': 'h-ru0001-post-hold-kmesh-diagnostic-case-v0.1',
            'status': 'VALID_POST_HOLD_KMESH_DIAGNOSTIC_CASE',
            'tag': TAG,
            'execution_state': {'PLANNED': True, 'EXECUTED': True, 'MEASURED': True, 'VALID': True, 'ADJUDICATED': False},
            'return_code': 0,
            'timeout': False,
            'job_done': True,
            'energy_count': len(energies),
            'elapsed_s': elapsed,
            'energy_ev': energies[-1],
            'layers': int(f['layers']),
            'total_vacuum_angstrom': float(f['total_vacuum_angstrom']),
            'kmesh': list(f['surface_kmesh']),
            'surface_excess_ev_per_surface_atom': gamma,
            'protocol_git_blob_sha': DIAGNOSTIC_PROTOCOL_BLOB_SHA,
            'hold_git_blob_sha': HOLD_BLOB_SHA,
            'original_hold_preserved': True,
            'relaxation_authorized': False,
            'scientific_settings_changed': False,
            'thresholds_changed': False,
            'chi_used': False,
            'kinetic_inputs_used': False,
            'paid_compute_used': False,
            'checkpoint_recovery_record_sha256': sha256(Path(args.recovery).resolve()),
            'checkpoint_recovery_segment': seg,
            'restart_mode': restart_mode,
            'input_sha256': sha256(inp),
            'output_sha256': sha256(stdout),
        }
        result_path = out / K28_RESULT
        write(result_path, row)
        write(out / 'COMPLETE.json', {
            'status': 'VALID_POST_HOLD_KMESH_DIAGNOSTIC_CASE',
            'segment_completed': seg,
            'result_sha256': sha256(result_path),
            'diagnostic_adjudicated': False,
        })
        shutil.rmtree(state, ignore_errors=True)
        print(json.dumps(row, indent=2, sort_keys=True))
        print(f'SYSTEM3_K28_VALID_ON_CHECKPOINT_SEGMENT_{seg}')
        return
    if not clean_stop:
        raise SystemExit('MECHANICAL_HOLD: K28 segment neither completed nor produced a verified QE max_seconds clean stop')
    save = state / f'{TAG}.save'
    if not save.is_dir() or not (save / 'data-file-schema.xml').is_file():
        raise SystemExit('MECHANICAL_HOLD: K28 QE clean stop did not preserve a valid native save directory')
    manifest = recursive_manifest(state)
    write(out / 'checkpoint_manifest.json', manifest)
    write(out / 'CHECKPOINT.json', {
        'status': 'VALID_NATIVE_QE_CHECKPOINT_NOT_SCIENTIFIC_EVIDENCE',
        'segment': seg,
        'checkpoint_manifest_sha256': sha256(out / 'checkpoint_manifest.json'),
        'file_count': manifest['file_count'],
        'size_bytes': manifest['size_bytes'],
        'scientific_result_available': False,
        'original_K16_coupled_hold_preserved': True,
    })
    print(f'SYSTEM3_K28_SEGMENT_{seg}_CHECKPOINT_READY')


def materialize_k24(args: argparse.Namespace) -> None:
    recovery, protocol, hold, k24 = contract(args)
    row = dict(k24['result'])
    if row.get('status') != 'VALID_POST_HOLD_KMESH_DIAGNOSTIC_CASE' or row.get('kmesh') != [24, 24, 1]:
        raise SystemExit('MECHANICAL_HOLD: K24 evidence cannot be materialized')
    row['materialized_from_preserved_valid_evidence'] = True
    row['preserved_evidence_record_git_blob_sha'] = K24_EVIDENCE_BLOB_SHA
    write(args.out, row)
    print('SYSTEM3_K24_PRESERVED_EVIDENCE_MATERIALIZED')


def finalize(args: argparse.Namespace) -> None:
    recovery, protocol, hold, k24 = contract(args)
    bundle = Path(args.bundle).resolve()
    complete, result = validate_previous(bundle)
    if not complete or result is None:
        raise SystemExit('MECHANICAL_HOLD: all predeclared K28 checkpoint segments exhausted without valid completion')
    row = load(result)
    if row.get('status') != 'VALID_POST_HOLD_KMESH_DIAGNOSTIC_CASE' or row.get('kmesh') != [28, 28, 1]:
        raise SystemExit('MECHANICAL_HOLD: final K28 result identity mismatch')
    if row.get('protocol_git_blob_sha') != DIAGNOSTIC_PROTOCOL_BLOB_SHA or row.get('hold_git_blob_sha') != HOLD_BLOB_SHA:
        raise SystemExit('MECHANICAL_HOLD: final K28 result provenance mismatch')
    if row.get('scientific_settings_changed') is not False or row.get('thresholds_changed') is not False:
        raise SystemExit('SCIENTIFIC_HOLD: final K28 result reports scientific drift')
    shutil.copy2(result, args.out)
    print('SYSTEM3_K28_CHECKPOINT_RECOVERY_FINALIZED_VALID')


def self_test(args: argparse.Namespace) -> None:
    recovery, protocol, hold, k24 = contract(args)
    cp = recovery['checkpoint_recovery']
    assert cp['segment_max_seconds'] < cp['external_wrapper_timeout_seconds']
    assert cp['external_wrapper_timeout_seconds'] < cp['github_job_timeout_minutes'] * 60
    assert recovery['acceptance']['K24_must_be_materialized_from_preserved_valid_evidence_not_rerun'] is True
    assert recovery['acceptance']['final_diagnostic_must_use_original_frozen_K20_K24_K28_rule'] is True
    assert recovery['acceptance']['diagnostic_may_not_authorize_relaxation'] is True
    txt = build_input(recovery, Path('/tmp/pseudo'), Path('/tmp/restart_state'), 'from_scratch')
    for needle in ["restart_mode='from_scratch'", "disk_io='medium'", 'max_seconds=13800.000000', 'ecutwfc=70', 'ecutrho=280', '28 28 1 0 0 0']:
        assert needle in txt
    print('SYSTEM3_K28_NATIVE_CHECKPOINT_RECOVERY_SELF_TEST_PASS')
    print('MECHANICAL_ONLY=true')
    print('K24_REUSED_NOT_RERUN=true')
    print('SEGMENT_MAX_SECONDS=13800')
    print('MAX_SEGMENTS=3')
    print('FROZEN_TOLERANCE_EV_PER_SURFACE_ATOM=0.001')
    print('RELAXATION_AUTHORIZED=false')


def add_common(sp: argparse.ArgumentParser) -> None:
    sp.add_argument('--recovery', required=True)
    sp.add_argument('--protocol', required=True)
    sp.add_argument('--hold', required=True)
    sp.add_argument('--k24-evidence', required=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd', required=True)
    sp = sub.add_parser('self-test'); add_common(sp); sp.set_defaults(func=self_test)
    sp = sub.add_parser('run-segment'); add_common(sp)
    sp.add_argument('--segment', type=int, required=True); sp.add_argument('--previous')
    sp.add_argument('--pw', required=True); sp.add_argument('--pseudo-dir', required=True); sp.add_argument('--out', required=True)
    sp.set_defaults(func=run_segment)
    sp = sub.add_parser('materialize-k24'); add_common(sp)
    sp.add_argument('--out', required=True); sp.set_defaults(func=materialize_k24)
    sp = sub.add_parser('finalize'); add_common(sp)
    sp.add_argument('--bundle', required=True); sp.add_argument('--out', required=True); sp.set_defaults(func=finalize)
    args = ap.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
