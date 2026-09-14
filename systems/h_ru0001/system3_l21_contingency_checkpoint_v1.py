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

PROTOCOL_SCHEMA = 'h-ru0001-l19-contingency-layer-sufficiency-protocol-v0.1'
PROTOCOL_STATUS = 'FROZEN_BEFORE_L19_OR_L21_CONTINGENCY_RESULT_AVAILABLE'
PROTOCOL_BLOB_SHA = '1424e99002d36fe2cf609386a2a824deeb5e7072'
PROTOCOL_SHA256 = '8bbe74e6345af5e28612db3804147a348ad826ee508ac677c77538bd7336f536'
SUCCESSOR_SHA256 = 'ffe50f7cfe5dbf5ce8c19da2449c00067fc795d38a3abe695bb16a0c41a07f48'
PW_SHA256 = '2b1ede22d276b1d4dab3e31212f306e88ae57e00f33ce6b532b849493a457855'
RU_SHA256 = 'ed637e8481a2fddda6a93863a92f8b0b857379b9db23325a4664e3df0a6f45bd'
ENERGY_RE = re.compile(r'!\s+total energy\s+=\s+([-+0-9.Ee]+)\s+Ry')
CLEAN_STOP_MARKER = 'Maximum CPU time exceeded'
TAG = 'l19_contingency_terminal_L21_V15_K24_24_1'
RESULT_NAME = 'SYSTEM3_L21_CONTINGENCY_RESULT.json'
CASE_SCHEMA = 'h-ru0001-l19-contingency-l21-fresh-case-v0.1'
CASE_STATUS = 'VALID_FRESH_L21_CONTINGENCY_CASE'


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


def contract(args: argparse.Namespace) -> tuple[dict[str, Any], dict[str, Any]]:
    pp = Path(args.protocol).resolve()
    sp = Path(args.successor_protocol).resolve()
    if git_blob_sha(pp) != PROTOCOL_BLOB_SHA or sha256(pp) != PROTOCOL_SHA256:
        raise SystemExit('MECHANICAL_HOLD: frozen L19 contingency protocol drift')
    protocol = load(pp)
    successor = load(sp)
    if protocol.get('schema') != PROTOCOL_SCHEMA or protocol.get('status') != PROTOCOL_STATUS:
        raise SystemExit('SCIENTIFIC_HOLD: L19 contingency protocol not frozen')
    if sha256(sp) != SUCCESSOR_SHA256:
        raise SystemExit('MECHANICAL_HOLD: active successor protocol drift')
    if protocol['lineage']['active_successor_protocol_sha256'] != SUCCESSOR_SHA256:
        raise SystemExit('MECHANICAL_HOLD: successor lineage mismatch')
    pair = protocol['prospective_pair']
    if pair['base'] != {
        'kmesh': [24, 24, 1],
        'layers': 19,
        'result_must_not_be_known_or_inserted_at_freeze': True,
        'source': 'active fresh successor qualification only if it returns a valid completed L19/V15/K24 result',
        'source_run_id': 34769372617,
        'total_vacuum_angstrom': 15.0,
    }:
        raise SystemExit('SCIENTIFIC_HOLD: L19 contingency base identity drift')
    if pair['terminal_reference'] != {
        'kmesh': [24, 24, 1],
        'layers': 21,
        'must_be_fresh_after_this_freeze': True,
        'total_vacuum_angstrom': 15.0,
    }:
        raise SystemExit('SCIENTIFIC_HOLD: L21 terminal identity drift')
    if float(protocol['criterion']['tolerance_ev_per_surface_atom']) != 0.001:
        raise SystemExit('SCIENTIFIC_HOLD: 1 meV criterion drift')
    if protocol['acceptance']['no_relaxation_authorization_from_this_test'] is not True:
        raise SystemExit('SCIENTIFIC_HOLD: contingency lane improperly authorizes relaxation')
    for key, val in protocol['firewalls'].items():
        if key == 'paid_compute_required':
            if val is not False:
                raise SystemExit('SCIENTIFIC_HOLD: paid compute firewall drift')
        elif val is not False:
            raise SystemExit(f'SCIENTIFIC_HOLD: firewall opened: {key}')
    cp = protocol['checkpoint_execution']
    if int(cp['segment_max_seconds']) != 13800 or int(cp['external_wrapper_timeout_seconds']) != 14700:
        raise SystemExit('MECHANICAL_HOLD: checkpoint timing drift')
    if int(cp['maximum_predeclared_segments']) != 3:
        raise SystemExit('MECHANICAL_HOLD: segment count drift')
    return protocol, successor


def verify_runtime(pw: Path, pseudo_dir: Path) -> None:
    ru = pseudo_dir / 'Ru.nc.pbe.z_16.oncvpsp4.sg15.v0.upf'
    if not pw.is_file() or sha256(pw) != PW_SHA256:
        raise SystemExit('MECHANICAL_HOLD: pw.x identity mismatch')
    if not ru.is_file() or sha256(ru) != RU_SHA256:
        raise SystemExit('MECHANICAL_HOLD: Ru pseudopotential identity mismatch')


def recursive_manifest(root: Path) -> dict[str, Any]:
    files = []
    total = 0
    for p in sorted(x for x in root.rglob('*') if x.is_file()):
        rel = p.relative_to(root).as_posix()
        size = p.stat().st_size
        total += size
        files.append({'path': rel, 'sha256': sha256(p), 'size_bytes': size})
    return {
        'schema': 'system3-l21-contingency-qe-native-restart-manifest-v0.1',
        'file_count': len(files),
        'size_bytes': total,
        'files': files,
    }


def validate_previous(previous: Path) -> tuple[bool, Path | None]:
    complete = previous / 'COMPLETE.json'
    result = previous / RESULT_NAME
    if complete.is_file():
        c = load(complete)
        if c.get('status') != CASE_STATUS or not result.is_file() or sha256(result) != c.get('result_sha256'):
            raise SystemExit('MECHANICAL_HOLD: completed L21 bundle failed integrity check')
        return True, result
    manifest_path = previous / 'checkpoint_manifest.json'
    state = previous / 'restart_state'
    if not manifest_path.is_file() or not state.is_dir():
        raise SystemExit('MECHANICAL_HOLD: previous L21 checkpoint bundle incomplete')
    expected = load(manifest_path)
    actual = recursive_manifest(state)
    if expected != actual:
        raise SystemExit('MECHANICAL_HOLD: recursive L21 checkpoint manifest mismatch')
    save = state / f'{TAG}.save'
    if not save.is_dir() or not (save / 'data-file-schema.xml').is_file():
        raise SystemExit('MECHANICAL_HOLD: L21 native QE save directory missing')
    return False, None


def build_input(protocol: dict[str, Any], pseudo_dir: Path, outdir: Path, restart_mode: str) -> str:
    s = protocol['frozen_scientific_settings']
    cfg = protocol['prospective_pair']['terminal_reference']
    txt = base.slab_input(
        float(s['a_angstrom']), float(s['c_angstrom']), int(cfg['layers']),
        float(cfg['total_vacuum_angstrom']), int(s['ecutwfc_ry']), int(s['ecutrho_ry']),
        tuple(int(v) for v in cfg['kmesh']), pseudo_dir.resolve(), str(outdir.resolve()), TAG,
    )
    insert = (
        f" restart_mode='{restart_mode}',\n"
        " disk_io='medium',\n"
        f" max_seconds={float(protocol['checkpoint_execution']['segment_max_seconds']):.6f},\n"
    )
    needle = " calculation='scf',\n"
    if needle not in txt:
        raise SystemExit('MECHANICAL_HOLD: unable to bind QE checkpoint controls')
    return txt.replace(needle, needle + insert, 1)


def wait_with_heartbeat(proc: subprocess.Popen, stdout: Path, external_timeout: int, interval: int) -> tuple[int, bool, float]:
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
            print(f'L21_CONTINGENCY_HEARTBEAT elapsed_s={int(elapsed)} stdout_bytes={size}', flush=True)
            next_heartbeat += interval
        time.sleep(15)


def run_segment(args: argparse.Namespace) -> None:
    protocol, successor = contract(args)
    seg = int(args.segment)
    if seg < 1 or seg > int(protocol['checkpoint_execution']['maximum_predeclared_segments']):
        raise SystemExit('MECHANICAL_HOLD: segment outside frozen range')
    pw = Path(args.pw).resolve()
    pseudo = Path(args.pseudo_dir).resolve()
    verify_runtime(pw, pseudo)
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
        complete, result = validate_previous(previous)
        if complete:
            shutil.copy2(result, out / RESULT_NAME)
            write(out / 'COMPLETE.json', load(previous / 'COMPLETE.json'))
            print(f'SYSTEM3_L21_CONTINGENCY_SEGMENT_{seg}_PASSTHROUGH_COMPLETE')
            return
        shutil.copytree(previous / 'restart_state', state)
        restart_mode = 'restart'

    inp = out / f'l21_segment_{seg}.in'
    stdout = out / f'l21_segment_{seg}.out'
    inp.write_text(build_input(protocol, pseudo, state, restart_mode), encoding='utf-8')
    env = dict(os.environ)
    env.update(OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1')
    with inp.open('rb') as fi, stdout.open('wb') as fo:
        proc = subprocess.Popen([str(pw)], stdin=fi, stdout=fo, stderr=subprocess.STDOUT, env=env)
        rc, external_kill, elapsed = wait_with_heartbeat(
            proc, stdout,
            int(protocol['checkpoint_execution']['external_wrapper_timeout_seconds']),
            int(protocol['checkpoint_execution']['heartbeat_interval_seconds']),
        )
    text = stdout.read_text(errors='replace')
    energies = [float(x) * base.RY_TO_EV for x in ENERGY_RE.findall(text)]
    job_done = 'JOB DONE.' in text
    clean_stop = CLEAN_STOP_MARKER in text
    if external_kill:
        raise SystemExit('MECHANICAL_HOLD: external wrapper killed L21 before native checkpoint persistence')

    meta = {
        'schema': 'h-ru0001-l21-contingency-checkpoint-segment-v0.1',
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
        s = protocol['frozen_scientific_settings']
        cfg = protocol['prospective_pair']['terminal_reference']
        layers = int(cfg['layers'])
        vacuum = float(cfg['total_vacuum_angstrom'])
        gamma = (energies[-1] - layers * float(s['bulk_energy_ev_per_atom'])) / 2.0
        cell_z, _ = base.slab_geometry(float(s['a_angstrom']), float(s['c_angstrom']), layers, vacuum)
        row = {
            'schema': CASE_SCHEMA,
            'status': CASE_STATUS,
            'case': 'L21_terminal_reference',
            'tag': TAG,
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
            'contingency_protocol_sha256': PROTOCOL_SHA256,
            'active_successor_protocol_sha256': SUCCESSOR_SHA256,
            'fresh_after_contingency_freeze': True,
            'scientific_settings_changed': False,
            'thresholds_changed': False,
            'kinetic_inputs_used': False,
            'chi_used': False,
            'paid_compute_used': False,
            'checkpoint_recovery_segment': seg,
            'restart_mode': restart_mode,
            'relaxation_authorized': False,
        }
        result_path = out / RESULT_NAME
        write(result_path, row)
        write(out / 'COMPLETE.json', {
            'status': CASE_STATUS,
            'segment_completed': seg,
            'result_sha256': sha256(result_path),
        })
        shutil.rmtree(state, ignore_errors=True)
        print(json.dumps(row, indent=2, sort_keys=True))
        print(f'SYSTEM3_L21_CONTINGENCY_VALID_ON_CHECKPOINT_SEGMENT_{seg}')
        return

    if not clean_stop:
        raise SystemExit('MECHANICAL_HOLD: L21 segment neither completed nor produced a verified QE max_seconds clean stop')
    save = state / f'{TAG}.save'
    if not save.is_dir() or not (save / 'data-file-schema.xml').is_file():
        raise SystemExit('MECHANICAL_HOLD: QE clean stop did not preserve a valid L21 native save directory')
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
    print(f'SYSTEM3_L21_CONTINGENCY_SEGMENT_{seg}_CHECKPOINT_READY')


def finalize(args: argparse.Namespace) -> None:
    protocol, successor = contract(args)
    bundle = Path(args.bundle).resolve()
    complete, result = validate_previous(bundle)
    if not complete or result is None:
        raise SystemExit('MECHANICAL_HOLD: all predeclared L21 recovery segments exhausted without valid completion')
    row = load(result)
    if row.get('schema') != CASE_SCHEMA or row.get('status') != CASE_STATUS:
        raise SystemExit('MECHANICAL_HOLD: final L21 result identity mismatch')
    cfg = protocol['prospective_pair']['terminal_reference']
    if row.get('kmesh') != cfg['kmesh'] or int(row.get('layers', 0)) != 21 or float(row.get('total_vacuum_angstrom')) != 15.0:
        raise SystemExit('MECHANICAL_HOLD: final L21 configuration mismatch')
    if row.get('contingency_protocol_sha256') != PROTOCOL_SHA256:
        raise SystemExit('MECHANICAL_HOLD: final L21 provenance mismatch')
    shutil.copy2(result, args.out)
    print('SYSTEM3_L21_CONTINGENCY_CHECKPOINT_RECOVERY_FINALIZED_VALID')


def self_test(args: argparse.Namespace) -> None:
    protocol, successor = contract(args)
    cp = protocol['checkpoint_execution']
    assert cp['segment_max_seconds'] < cp['external_wrapper_timeout_seconds'] < cp['github_job_timeout_minutes'] * 60
    assert cp['maximum_predeclared_segments'] == 3
    cfg = protocol['prospective_pair']['terminal_reference']
    assert cfg == {'layers': 21, 'total_vacuum_angstrom': 15.0, 'kmesh': [24, 24, 1], 'must_be_fresh_after_this_freeze': True}
    txt = build_input(protocol, Path('/tmp/pseudo'), Path('/tmp/state'), 'from_scratch')
    for needle in ("restart_mode='from_scratch'", "disk_io='medium'", 'max_seconds=13800.000000', 'ecutwfc=70', 'ecutrho=280', '21'):
        assert needle in txt
    assert protocol['criterion']['tolerance_ev_per_surface_atom'] == 0.001
    print('SYSTEM3_L21_CONTINGENCY_SELF_TEST_PASS')
    print('PHASE=P0_Q')
    print('BASE=L19_V15_K24_FROM_ACTIVE_GATE_IF_VALID')
    print('TERMINAL=L21_V15_K24_FRESH')
    print('FROZEN_TOLERANCE_EV_PER_SURFACE_ATOM=0.001')
    print('RELAXATION_AUTHORIZED=false')


def add_common(sp: argparse.ArgumentParser) -> None:
    sp.add_argument('--protocol', required=True)
    sp.add_argument('--successor-protocol', required=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd', required=True)
    sp = sub.add_parser('self-test')
    add_common(sp)
    sp.set_defaults(func=self_test)
    sp = sub.add_parser('run-segment')
    add_common(sp)
    sp.add_argument('--segment', type=int, required=True)
    sp.add_argument('--previous')
    sp.add_argument('--pw', required=True)
    sp.add_argument('--pseudo-dir', required=True)
    sp.add_argument('--out', required=True)
    sp.set_defaults(func=run_segment)
    sp = sub.add_parser('finalize')
    add_common(sp)
    sp.add_argument('--bundle', required=True)
    sp.add_argument('--out', required=True)
    sp.set_defaults(func=finalize)
    args = ap.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
