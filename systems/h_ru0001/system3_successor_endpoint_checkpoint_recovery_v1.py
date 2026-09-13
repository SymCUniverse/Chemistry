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

RECOVERY_SCHEMA = 'h-ru0001-successor-failed-endpoints-checkpoint-recovery-v0.1'
RECOVERY_STATUS = 'FROZEN_AFTER_MECHANICAL_TIMEOUTS_BEFORE_RECOVERY_RESULTS'
RECOVERY_BLOB_SHA = '2c0dc34f45ba8484d3306d32583401980279fbd1'
SUCCESSOR_BLOB_SHA = 'e7de4718ccd6f4679690d578a16e10de2f2524e0'
PRESERVED_BLOB_SHA = '56cbf54b380d789c233561a9c1a79837fcddd9d7'
QUALIFICATION_RUNNER_BLOB_SHA = 'd51e3eb5a0d4c2924adc2216a53a73c4db92351a'
PREPARATION_BLOB_SHA = 'daa3a9560d0e9ed9ed3c7fdc086507a5a4db5d60'
SUCCESSOR_SHA256 = 'ffe50f7cfe5dbf5ce8c19da2449c00067fc795d38a3abe695bb16a0c41a07f48'
PW_SHA256 = '2b1ede22d276b1d4dab3e31212f306e88ae57e00f33ce6b532b849493a457855'
RU_SHA256 = 'ed637e8481a2fddda6a93863a92f8b0b857379b9db23325a4664e3df0a6f45bd'
CASE_SCHEMA = 'h-ru0001-successor-fixed-grid-fresh-case-v0.1'
CASE_STATUS = 'VALID_FRESH_SUCCESSOR_FIXED_GRID_CASE'
ENERGY_RE = re.compile(r'!\s+total energy\s+=\s+([-+0-9.Ee]+)\s+Ry')
CLEAN_STOP_MARKER = 'Maximum CPU time exceeded'
ALLOWED_ENDPOINTS = ('kmesh', 'layers')
PRESERVED_CASES = ('base', 'vacuum')


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


def result_filename(case: str) -> str:
    return f'SYSTEM3_SUCCESSOR_{case.upper()}_RESULT.json'


def case_tag(case: str) -> str:
    if case == 'kmesh':
        return 'successor_kmesh_L17_V15_K28_28_1'
    if case == 'layers':
        return 'successor_layers_L19_V15_K24_24_1'
    raise SystemExit(f'MECHANICAL_HOLD: unsupported recovery endpoint {case}')


def recursive_manifest(root: Path, case: str) -> dict[str, Any]:
    files = []
    total = 0
    for p in sorted(x for x in root.rglob('*') if x.is_file()):
        rel = p.relative_to(root).as_posix()
        size = p.stat().st_size
        total += size
        files.append({'path': rel, 'sha256': sha256(p), 'size_bytes': size})
    return {
        'schema': 'system3-successor-qe-native-restart-manifest-v0.1',
        'case': case,
        'file_count': len(files),
        'size_bytes': total,
        'files': files,
    }


def contract(args: argparse.Namespace) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    rp = Path(args.recovery).resolve()
    sp = Path(args.successor_protocol).resolve()
    ep = Path(args.preserved_evidence).resolve()
    for path, blob in ((rp, RECOVERY_BLOB_SHA), (sp, SUCCESSOR_BLOB_SHA), (ep, PRESERVED_BLOB_SHA)):
        if git_blob_sha(path) != blob:
            raise SystemExit(f'MECHANICAL_HOLD: frozen blob drift: {path.name}')
    recovery, successor, preserved = map(load, (rp, sp, ep))
    if recovery.get('schema') != RECOVERY_SCHEMA or recovery.get('status') != RECOVERY_STATUS:
        raise SystemExit('SCIENTIFIC_HOLD: successor endpoint recovery record not frozen')
    if recovery.get('scope') != 'MECHANICAL_EXECUTION_RECOVERY_ONLY':
        raise SystemExit('SCIENTIFIC_HOLD: successor endpoint recovery escaped mechanical-only scope')
    if successor.get('schema') != 'h-ru0001-successor-fixed-grid-protocol-v0.1':
        raise SystemExit('SCIENTIFIC_HOLD: successor protocol schema mismatch')
    if successor.get('status') != 'FROZEN_AFTER_P0_Q_DIAGNOSTIC_BEFORE_SUCCESSOR_QUALIFICATION_RESULTS':
        raise SystemExit('SCIENTIFIC_HOLD: successor protocol state drift')
    if sha256(sp) != SUCCESSOR_SHA256:
        raise SystemExit('MECHANICAL_HOLD: successor protocol SHA-256 drift')
    if successor.get('frozen_scientific_settings', {}).get('surface_kmesh') != [24, 24, 1]:
        raise SystemExit('SCIENTIFIC_HOLD: selected K24 successor identity drift')
    q = successor.get('fresh_successor_qualification', {})
    if q.get('all_four_cases_must_be_fresh') is not True or q.get('reuse_diagnostic_energies_as_PASS_evidence') is not False:
        raise SystemExit('SCIENTIFIC_HOLD: fresh successor evidence firewall drift')
    if float(q.get('absolute_surface_excess_tolerance_ev_per_surface_atom')) != 0.001:
        raise SystemExit('SCIENTIFIC_HOLD: successor 1 meV threshold drift')
    if preserved.get('status') != 'VALID_FRESH_SUCCESSOR_CASES_PRESERVED':
        raise SystemExit('MECHANICAL_HOLD: preserved base/vacuum evidence status mismatch')
    for case in PRESERVED_CASES:
        row = preserved.get('cases', {}).get(case, {}).get('result', {})
        if row.get('schema') != CASE_SCHEMA or row.get('status') != CASE_STATUS or row.get('case') != case:
            raise SystemExit(f'MECHANICAL_HOLD: preserved {case} result identity mismatch')
        if not row.get('job_done') or row.get('timeout') or int(row.get('return_code', 1)) != 0:
            raise SystemExit(f'MECHANICAL_HOLD: preserved {case} is not valid completed evidence')
        if row.get('fresh_successor_case') is not True or row.get('diagnostic_energy_reused') is not False:
            raise SystemExit(f'SCIENTIFIC_HOLD: preserved {case} evidence firewall drift')
        if row.get('successor_protocol_sha256') != SUCCESSOR_SHA256:
            raise SystemExit(f'MECHANICAL_HOLD: preserved {case} successor provenance mismatch')
    lineage = recovery['lineage']
    if lineage['successor_protocol']['git_blob_sha'] != SUCCESSOR_BLOB_SHA:
        raise SystemExit('MECHANICAL_HOLD: recovery successor lineage drift')
    if lineage['valid_base_vacuum_evidence']['git_blob_sha'] != PRESERVED_BLOB_SHA:
        raise SystemExit('MECHANICAL_HOLD: recovery preserved-evidence lineage drift')
    if lineage['qualification_runner']['git_blob_sha'] != QUALIFICATION_RUNNER_BLOB_SHA:
        raise SystemExit('MECHANICAL_HOLD: qualification runner lineage drift')
    for case in ALLOWED_ENDPOINTS:
        failed = recovery['failed_attempts'][case]
        if failed['classification'] != 'MECHANICAL_WALL_CLOCK_TIMEOUT':
            raise SystemExit(f'SCIENTIFIC_HOLD: {case} failure classification drift')
        if failed['job_done'] or int(failed['valid_final_energy_count']) != 0:
            raise SystemExit(f'SCIENTIFIC_HOLD: invalid timed-out {case} promoted as evidence')
        if failed['partial_output_may_be_used_for_adjudication'] is not False or failed['partial_state_reused'] is not False:
            raise SystemExit(f'SCIENTIFIC_HOLD: failed {case} partial-output firewall drift')
    cp = recovery['checkpoint_recovery']
    if cp['method'] != 'QE_NATIVE_RESTART_ACROSS_FRESH_STANDARD_GITHUB_JOBS':
        raise SystemExit('MECHANICAL_HOLD: recovery method drift')
    if int(cp['segment_max_seconds']) != 13800 or int(cp['external_wrapper_timeout_seconds']) != 14700:
        raise SystemExit('MECHANICAL_HOLD: checkpoint time contract drift')
    if int(cp['maximum_predeclared_segments']) != 3:
        raise SystemExit('MECHANICAL_HOLD: maximum segment count drift')
    acc = recovery['acceptance']
    for key in ('recovered_endpoint_valid_only_if_JOB_DONE', 'recovered_endpoint_valid_only_if_return_code_zero', 'recovered_endpoint_valid_only_if_final_total_energy_present', 'base_and_vacuum_must_be_materialized_from_preserved_valid_evidence_not_rerun', 'final_adjudication_must_use_original_successor_qualification_runner'):
        if acc[key] is not True:
            raise SystemExit(f'SCIENTIFIC_HOLD: recovery acceptance firewall drift: {key}')
    if float(acc['final_tolerance_ev_per_surface_atom']) != 0.001 or acc['relaxation_only_if_final_status'] != 'CLEAN_SURFACE_FIXED_GRID_PASS':
        raise SystemExit('SCIENTIFIC_HOLD: final acceptance rule drift')
    prov = recovery['provenance']
    if prov['mechanical_only_change'] is not True or prov['original_K16_coupled_hold_preserved'] is not True:
        raise SystemExit('SCIENTIFIC_HOLD: recovery provenance identity drift')
    for key in ('scientific_settings_changed','thresholds_changed','evidence_firewall_changed','kinetic_inputs_used','chi_used','published_H_Ru_outcomes_used','System2_outcomes_used','paid_compute_used'):
        if prov[key] is not False:
            raise SystemExit(f'SCIENTIFIC_HOLD: recovery provenance firewall opened: {key}')
    return recovery, successor, preserved


def verify_runtime(recovery: dict[str, Any], pw: Path, pseudo_dir: Path) -> None:
    ru = pseudo_dir / 'Ru.nc.pbe.z_16.oncvpsp4.sg15.v0.upf'
    if not pw.is_file() or sha256(pw) != PW_SHA256 or sha256(pw) != recovery['runtime_identity']['pw_x_sha256']:
        raise SystemExit('MECHANICAL_HOLD: pw.x identity mismatch')
    if not ru.is_file() or sha256(ru) != RU_SHA256 or sha256(ru) != recovery['runtime_identity']['ru_pseudo_sha256']:
        raise SystemExit('MECHANICAL_HOLD: Ru pseudopotential identity mismatch')


def endpoint_config(successor: dict[str, Any], case: str) -> dict[str, Any]:
    if case not in ALLOWED_ENDPOINTS:
        raise SystemExit(f'MECHANICAL_HOLD: recovery supports only {ALLOWED_ENDPOINTS}')
    return successor['fresh_successor_qualification']['endpoint_cases'][case]


def build_input(recovery: dict[str, Any], successor: dict[str, Any], case: str, pseudo_dir: Path, outdir: Path, restart_mode: str) -> str:
    cfg = endpoint_config(successor, case)
    s = successor['frozen_scientific_settings']
    tag = case_tag(case)
    txt = base.slab_input(
        float(s['a_angstrom']), float(s['c_angstrom']), int(cfg['layers']),
        float(cfg['total_vacuum_angstrom']), int(s['ecutwfc_ry']), int(s['ecutrho_ry']),
        tuple(int(v) for v in cfg['kmesh']), pseudo_dir.resolve(), str(outdir.resolve()), tag,
    )
    insert = (
        f" restart_mode='{restart_mode}',\n"
        " disk_io='medium',\n"
        f" max_seconds={float(recovery['checkpoint_recovery']['segment_max_seconds']):.6f},\n"
    )
    needle = " calculation='scf',\n"
    if needle not in txt:
        raise SystemExit('MECHANICAL_HOLD: unable to bind QE checkpoint controls')
    return txt.replace(needle, needle + insert, 1)


def validate_previous(previous: Path, case: str) -> tuple[bool, Path | None]:
    complete = previous / 'COMPLETE.json'
    result_name = result_filename(case)
    if complete.is_file():
        c = load(complete)
        result = previous / result_name
        if c.get('status') != CASE_STATUS or c.get('case') != case or not result.is_file() or sha256(result) != c.get('result_sha256'):
            raise SystemExit(f'MECHANICAL_HOLD: completed previous {case} bundle failed integrity check')
        return True, result
    manifest_path = previous / 'checkpoint_manifest.json'
    state = previous / 'restart_state'
    if not manifest_path.is_file() or not state.is_dir():
        raise SystemExit(f'MECHANICAL_HOLD: previous {case} checkpoint bundle incomplete')
    expected = load(manifest_path)
    actual = recursive_manifest(state, case)
    if expected != actual:
        raise SystemExit(f'MECHANICAL_HOLD: recursive {case} checkpoint manifest mismatch')
    save = state / f'{case_tag(case)}.save'
    if not save.is_dir() or not (save / 'data-file-schema.xml').is_file():
        raise SystemExit(f'MECHANICAL_HOLD: {case} native QE save directory missing')
    return False, None


def wait_with_heartbeat(proc: subprocess.Popen, stdout: Path, external_timeout: int, interval: int, case: str) -> tuple[int, bool, float]:
    start = time.time()
    next_heartbeat = float(interval)
    while True:
        rc = proc.poll()
        elapsed = time.time() - start
        if rc is not None:
            return int(rc), False, elapsed
        if elapsed >= external_timeout:
            proc.terminate()
            try:
                rc = proc.wait(timeout=30)
            except subprocess.TimeoutExpired:
                proc.kill()
                rc = proc.wait(timeout=10)
            return int(rc), True, time.time() - start
        if elapsed >= next_heartbeat:
            size = stdout.stat().st_size if stdout.exists() else 0
            print(f'SUCCESSOR_{case.upper()}_RECOVERY_HEARTBEAT elapsed_s={int(elapsed)} stdout_bytes={size}', flush=True)
            next_heartbeat += interval
        time.sleep(15)


def run_segment(args: argparse.Namespace) -> None:
    recovery, successor, preserved = contract(args)
    case = args.case
    if case not in ALLOWED_ENDPOINTS:
        raise SystemExit('MECHANICAL_HOLD: invalid recovery case')
    seg = int(args.segment)
    if seg < 1 or seg > int(recovery['checkpoint_recovery']['maximum_predeclared_segments']):
        raise SystemExit('MECHANICAL_HOLD: segment outside frozen range')
    pw = Path(args.pw).resolve()
    pseudo = Path(args.pseudo_dir).resolve()
    verify_runtime(recovery, pw, pseudo)
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
        complete, result = validate_previous(previous, case)
        if complete:
            shutil.copy2(result, out / result_filename(case))
            c = load(previous / 'COMPLETE.json')
            c['passthrough_segment'] = seg
            write(out / 'COMPLETE.json', c)
            print(f'SYSTEM3_SUCCESSOR_{case.upper()}_SEGMENT_{seg}_PASSTHROUGH_COMPLETE')
            return
        shutil.copytree(previous / 'restart_state', state)
        restart_mode = 'restart'
    inp = out / f'{case}_segment_{seg}.in'
    stdout = out / f'{case}_segment_{seg}.out'
    inp.write_text(build_input(recovery, successor, case, pseudo, state, restart_mode), encoding='utf-8')
    env = dict(os.environ)
    env.update(OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1')
    with inp.open('rb') as fi, stdout.open('wb') as fo:
        proc = subprocess.Popen([str(pw)], stdin=fi, stdout=fo, stderr=subprocess.STDOUT, env=env)
        rc, external_kill, elapsed = wait_with_heartbeat(
            proc, stdout, int(recovery['checkpoint_recovery']['external_wrapper_timeout_seconds']),
            int(recovery['checkpoint_recovery']['heartbeat_interval_seconds']), case,
        )
    text = stdout.read_text(errors='replace')
    energies = [float(x) * base.RY_TO_EV for x in ENERGY_RE.findall(text)]
    job_done = 'JOB DONE.' in text
    clean_stop = CLEAN_STOP_MARKER in text
    if external_kill:
        raise SystemExit(f'MECHANICAL_HOLD: external wrapper killed {case} before native checkpoint persistence')
    meta = {
        'schema': 'h-ru0001-successor-endpoint-checkpoint-segment-v0.1',
        'case': case,
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
        'fresh_successor_case': True,
        'diagnostic_energy_reused': False,
        'scientific_settings_changed': False,
        'thresholds_changed': False,
        'paid_compute_used': False,
    }
    write(out / f'SEGMENT_{seg}_METADATA.json', meta)
    if job_done and rc == 0 and energies:
        cfg = endpoint_config(successor, case)
        s = successor['frozen_scientific_settings']
        layers = int(cfg['layers'])
        vacuum = float(cfg['total_vacuum_angstrom'])
        gamma = (energies[-1] - layers * float(s['bulk_energy_ev_per_atom'])) / 2.0
        cell_z, _ = base.slab_geometry(float(s['a_angstrom']), float(s['c_angstrom']), layers, vacuum)
        row = {
            'schema': CASE_SCHEMA,
            'status': CASE_STATUS,
            'case': case,
            'tag': case_tag(case),
            'layers': layers,
            'total_vacuum_angstrom': vacuum,
            'cell_z_angstrom': cell_z,
            'kmesh': list(cfg['kmesh']),
            'energy_ev': energies[-1],
            'surface_excess_ev_per_surface_atom': gamma,
            'elapsed_s': elapsed,
            'return_code': 0,
            'timeout': False,
            'job_done': True,
            'energy_count': len(energies),
            'input_sha256': sha256(inp),
            'output_sha256': sha256(stdout),
            'successor_protocol_sha256': SUCCESSOR_SHA256,
            'preparation_protocol_git_blob_sha': PREPARATION_BLOB_SHA,
            'original_K16_coupled_hold_preserved': True,
            'fresh_successor_case': True,
            'diagnostic_energy_reused': False,
            'scientific_settings_changed': False,
            'thresholds_changed': False,
            'kinetic_inputs_used': False,
            'chi_used': False,
            'paid_compute_used': False,
            'mechanical_timeout_seconds': int(recovery['checkpoint_recovery']['external_wrapper_timeout_seconds']),
            'checkpoint_recovery_segment': seg,
            'restart_mode': restart_mode,
            'recovery_record_sha256': sha256(Path(args.recovery).resolve()),
        }
        result_path = out / result_filename(case)
        write(result_path, row)
        write(out / 'COMPLETE.json', {
            'status': CASE_STATUS,
            'case': case,
            'segment_completed': seg,
            'result_sha256': sha256(result_path),
        })
        shutil.rmtree(state, ignore_errors=True)
        print(json.dumps(row, indent=2, sort_keys=True))
        print(f'SYSTEM3_SUCCESSOR_{case.upper()}_VALID_ON_CHECKPOINT_SEGMENT_{seg}')
        return
    if not clean_stop:
        raise SystemExit(f'MECHANICAL_HOLD: {case} segment neither completed nor produced a verified QE max_seconds clean stop')
    save = state / f'{case_tag(case)}.save'
    if not save.is_dir() or not (save / 'data-file-schema.xml').is_file():
        raise SystemExit(f'MECHANICAL_HOLD: QE clean stop did not preserve a valid {case} native save directory')
    manifest = recursive_manifest(state, case)
    write(out / 'checkpoint_manifest.json', manifest)
    write(out / 'CHECKPOINT.json', {
        'status': 'VALID_NATIVE_QE_CHECKPOINT_NOT_SCIENTIFIC_EVIDENCE',
        'case': case,
        'segment': seg,
        'checkpoint_manifest_sha256': sha256(out / 'checkpoint_manifest.json'),
        'file_count': manifest['file_count'],
        'size_bytes': manifest['size_bytes'],
        'scientific_result_available': False,
    })
    print(f'SYSTEM3_SUCCESSOR_{case.upper()}_SEGMENT_{seg}_CHECKPOINT_READY')


def materialize_preserved(args: argparse.Namespace) -> None:
    recovery, successor, preserved = contract(args)
    case = args.case
    if case not in PRESERVED_CASES:
        raise SystemExit('MECHANICAL_HOLD: only preserved base/vacuum may be materialized')
    row = preserved['cases'][case]['result']
    write(args.out, row)
    print(f'SYSTEM3_SUCCESSOR_{case.upper()}_PRESERVED_EVIDENCE_MATERIALIZED')


def finalize(args: argparse.Namespace) -> None:
    recovery, successor, preserved = contract(args)
    case = args.case
    bundle = Path(args.bundle).resolve()
    complete, result = validate_previous(bundle, case)
    if not complete or result is None:
        raise SystemExit(f'MECHANICAL_HOLD: all predeclared {case} recovery segments exhausted without valid completion')
    row = load(result)
    cfg = endpoint_config(successor, case)
    if row.get('schema') != CASE_SCHEMA or row.get('status') != CASE_STATUS or row.get('case') != case:
        raise SystemExit(f'MECHANICAL_HOLD: final recovered {case} result identity mismatch')
    if row.get('kmesh') != cfg['kmesh'] or int(row.get('layers', 0)) != int(cfg['layers']) or float(row.get('total_vacuum_angstrom')) != float(cfg['total_vacuum_angstrom']):
        raise SystemExit(f'MECHANICAL_HOLD: final recovered {case} configuration mismatch')
    if row.get('successor_protocol_sha256') != SUCCESSOR_SHA256:
        raise SystemExit(f'MECHANICAL_HOLD: final recovered {case} provenance mismatch')
    if row.get('fresh_successor_case') is not True or row.get('diagnostic_energy_reused') is not False:
        raise SystemExit(f'SCIENTIFIC_HOLD: final recovered {case} freshness firewall violation')
    if row.get('scientific_settings_changed') is not False or row.get('thresholds_changed') is not False:
        raise SystemExit(f'SCIENTIFIC_HOLD: final recovered {case} scientific drift')
    shutil.copy2(result, args.out)
    print(f'SYSTEM3_SUCCESSOR_{case.upper()}_CHECKPOINT_RECOVERY_FINALIZED_VALID')


def self_test(args: argparse.Namespace) -> None:
    recovery, successor, preserved = contract(args)
    cp = recovery['checkpoint_recovery']
    assert cp['segment_max_seconds'] < cp['external_wrapper_timeout_seconds'] < cp['github_job_timeout_minutes'] * 60
    assert cp['maximum_predeclared_segments'] == 3
    assert recovery['acceptance']['base_and_vacuum_must_be_materialized_from_preserved_valid_evidence_not_rerun'] is True
    for case, expected in (
        ('kmesh', {'layers':17,'total_vacuum_angstrom':15.0,'kmesh':[28,28,1]}),
        ('layers', {'layers':19,'total_vacuum_angstrom':15.0,'kmesh':[24,24,1]}),
    ):
        assert endpoint_config(successor, case) == expected
        txt = build_input(recovery, successor, case, Path('/tmp/pseudo'), Path('/tmp/state'), 'from_scratch')
        for needle in ("restart_mode='from_scratch'", "disk_io='medium'", 'max_seconds=13800.000000', 'ecutwfc=70', 'ecutrho=280'):
            assert needle in txt
    assert successor['fresh_successor_qualification']['absolute_surface_excess_tolerance_ev_per_surface_atom'] == 0.001
    print('SYSTEM3_SUCCESSOR_ENDPOINT_CHECKPOINT_RECOVERY_SELF_TEST_PASS')
    print('MECHANICAL_ONLY=true')
    print('PRESERVE_BASE_AND_VACUUM=true')
    print('RECOVER_ENDPOINTS=kmesh,layers')
    print('SEGMENT_MAX_SECONDS=13800')
    print('MAX_SEGMENTS=3')
    print('FROZEN_TOLERANCE_EV_PER_SURFACE_ATOM=0.001')
    print('RELAXATION_AUTHORIZED=false')


def add_common(sp: argparse.ArgumentParser) -> None:
    sp.add_argument('--recovery', required=True)
    sp.add_argument('--successor-protocol', required=True)
    sp.add_argument('--preserved-evidence', required=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd', required=True)
    sp = sub.add_parser('self-test'); add_common(sp); sp.set_defaults(func=self_test)
    sp = sub.add_parser('run-segment'); add_common(sp)
    sp.add_argument('--case', choices=ALLOWED_ENDPOINTS, required=True)
    sp.add_argument('--segment', type=int, required=True); sp.add_argument('--previous')
    sp.add_argument('--pw', required=True); sp.add_argument('--pseudo-dir', required=True); sp.add_argument('--out', required=True)
    sp.set_defaults(func=run_segment)
    sp = sub.add_parser('materialize-preserved'); add_common(sp)
    sp.add_argument('--case', choices=PRESERVED_CASES, required=True); sp.add_argument('--out', required=True)
    sp.set_defaults(func=materialize_preserved)
    sp = sub.add_parser('finalize'); add_common(sp)
    sp.add_argument('--case', choices=ALLOWED_ENDPOINTS, required=True); sp.add_argument('--bundle', required=True); sp.add_argument('--out', required=True)
    sp.set_defaults(func=finalize)
    args = ap.parse_args(); args.func(args)


if __name__ == '__main__':
    main()
