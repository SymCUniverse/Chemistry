#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import system3_clean_ru0001_layer_extension_v1 as ext
import system3_clean_ru0001_numerical_v1 as base

RECOVERY_SCHEMA = 'h-ru0001-layer-extension-timeout-recovery-v0.1'
RECOVERY_STATUS = 'FROZEN_AFTER_MECHANICAL_TIMEOUT_BEFORE_RECOVERY_RESULTS'
RECOVERY_GIT_BLOB_SHA = '829aff32ddd3e6ebb95e9af9034242b923cb361b'


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f'blob {len(data)}\0'.encode() + data).hexdigest()


def load(path: str | Path) -> dict[str, Any]:
    row = json.loads(Path(path).read_text())
    if not isinstance(row, dict):
        raise SystemExit(f'MECHANICAL_HOLD: JSON object required: {path}')
    return row


def write(path: str | Path, row: dict[str, Any]):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(row, indent=2, sort_keys=True) + '\n')


def contract(protocol_path: Path, source_path: Path, recovery_path: Path, l15_path: Path):
    p, s = ext.contract(protocol_path, source_path)
    r = load(recovery_path)
    l15 = load(l15_path)

    if r.get('schema') != RECOVERY_SCHEMA or r.get('status') != RECOVERY_STATUS:
        raise SystemExit('MECHANICAL_HOLD: recovery record identity mismatch')
    if git_blob_sha(recovery_path) != RECOVERY_GIT_BLOB_SHA:
        raise SystemExit('MECHANICAL_HOLD: recovery record blob identity mismatch')

    lin = r['lineage']
    if sha256(protocol_path) != lin['original_protocol_sha256']:
        raise SystemExit('MECHANICAL_HOLD: original protocol SHA256 mismatch')
    if git_blob_sha(protocol_path) != lin['original_protocol_git_blob_sha']:
        raise SystemExit('MECHANICAL_HOLD: original protocol git blob mismatch')
    if sha256(source_path) != lin['source_evidence_sha256']:
        raise SystemExit('MECHANICAL_HOLD: source evidence SHA256 mismatch')
    if git_blob_sha(l15_path) != lin['valid_l15_interim_git_blob_sha']:
        raise SystemExit('MECHANICAL_HOLD: L15 interim evidence git blob mismatch')

    if l15.get('status') != 'VALID_INTERIM_LAYER_EVIDENCE_NOT_BATCH_ADJUDICATED':
        raise SystemExit('MECHANICAL_HOLD: L15 interim status mismatch')
    m = l15['measurement']
    f = p['frozen_numerical_settings']
    if int(m['layers']) != 15 or m['runner_reported_status'] != 'VALID_EXTENSION_LAYER':
        raise SystemExit('MECHANICAL_HOLD: L15 measurement identity mismatch')
    if m['runner_reported_protocol_sha256'] != sha256(protocol_path):
        raise SystemExit('MECHANICAL_HOLD: L15 protocol provenance mismatch')
    if l15['lineage']['source_evidence_sha256'] != sha256(source_path):
        raise SystemExit('MECHANICAL_HOLD: L15 source provenance mismatch')
    if l15['lineage']['artifact_digest'] != r['completed_valid_evidence']['artifact_digest']:
        raise SystemExit('MECHANICAL_HOLD: L15 artifact digest mismatch')
    if abs(float(m['surface_excess_ev_per_surface_atom']) - float(r['completed_valid_evidence']['surface_excess_ev_per_surface_atom'])) > 1e-12:
        raise SystemExit('MECHANICAL_HOLD: L15 numerical evidence mismatch')
    if list(m['kmesh']) != list(f['surface_kmesh']) or float(m['total_vacuum_angstrom']) != float(f['total_vacuum_angstrom']):
        raise SystemExit('SCIENTIFIC_HOLD: L15 frozen grid drift')
    if int(m['ecutwfc_ry']) != int(f['ecutwfc_ry']) or int(m['ecutrho_ry']) != int(f['ecutrho_ry']):
        raise SystemExit('SCIENTIFIC_HOLD: L15 cutoff drift')

    failures = r['mechanical_failures']
    if [int(x['layers']) for x in failures] != [17, 19]:
        raise SystemExit('MECHANICAL_HOLD: recovery failed-layer set drift')
    for x in failures:
        if x.get('classification') != 'MECHANICAL_TIMEOUT_NO_VALID_MEASUREMENT':
            raise SystemExit('SCIENTIFIC_HOLD: non-mechanical failure entered timeout recovery')
        if x.get('timeout') is not True or int(x.get('return_code', 0)) != -15 or int(x.get('energy_count', -1)) != 0 or x.get('job_done') is not False:
            raise SystemExit('MECHANICAL_HOLD: source timeout evidence mismatch')

    ex = r['recovery_execution']
    if ex['failed_layers_only'] != [17, 19] or ex['recompute_valid_l15'] is not False or ex['reuse_partial_timed_out_outputs'] is not False:
        raise SystemExit('MECHANICAL_HOLD: recovery routing drift')
    if int(ex['original_per_layer_timeout_seconds']) != int(p['execution']['per_layer_timeout_seconds']):
        raise SystemExit('MECHANICAL_HOLD: original timeout mismatch')
    if int(ex['recovery_per_layer_timeout_seconds']) != 14400:
        raise SystemExit('MECHANICAL_HOLD: recovery timeout drift')
    if int(ex['workflow_job_timeout_minutes']) != 300:
        raise SystemExit('MECHANICAL_HOLD: recovery job timeout drift')
    if ex['timeout_change_classification'] != 'MECHANICAL_WALL_CLOCK_HEADROOM_ONLY':
        raise SystemExit('SCIENTIFIC_HOLD: timeout recovery classification drift')

    dc = r['decision_contract']
    if dc['adjudication_rule_unchanged'] is not True or float(dc['tolerance_ev_per_surface_atom']) != float(f['absolute_surface_excess_tolerance_ev_per_surface_atom']):
        raise SystemExit('SCIENTIFIC_HOLD: decision rule or tolerance drift')
    if int(dc['terminal_reference_layers']) != 19 or dc['next_batch_if_hold'] != [21, 23, 25]:
        raise SystemExit('SCIENTIFIC_HOLD: decision routing drift')
    if dc['if_pass'] != 'RUN_COUPLED_ENDPOINT_RECHECK_BEFORE_RELAXATION':
        raise SystemExit('SCIENTIFIC_HOLD: coupled gate guard missing')
    if any(bool(v) for v in r['controls'].values()):
        raise SystemExit('SCIENTIFIC_HOLD: recovery controls report scientific drift')

    return p, s, r, l15


def verify_runtime(p: dict[str, Any], pw: Path, pseudo_dir: Path):
    ext.verify_runtime(p, pw, pseudo_dir)


def run_layer(args):
    pp = Path(args.protocol).resolve()
    sp = Path(args.source_evidence).resolve()
    rp = Path(args.recovery).resolve()
    lp = Path(args.l15_interim).resolve()
    p, s, r, l15 = contract(pp, sp, rp, lp)
    layer = int(args.layers)
    if layer not in r['recovery_execution']['failed_layers_only']:
        raise SystemExit('SCIENTIFIC_HOLD: only timed-out L17/L19 may use this recovery lane')

    pw = Path(args.pw).resolve()
    pseudo = Path(args.pseudo_dir).resolve()
    verify_runtime(p, pw, pseudo)
    f = p['frozen_numerical_settings']
    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    tag = f'slab_L{layer}_V15_K16_16_1_extension'
    txt = base.slab_input(
        float(f['a_angstrom']), float(f['c_angstrom']), layer,
        float(f['total_vacuum_angstrom']), int(f['ecutwfc_ry']), int(f['ecutrho_ry']),
        tuple(f['surface_kmesh']), pseudo, '__OUTDIR__', tag
    )
    timeout_s = int(r['recovery_execution']['recovery_per_layer_timeout_seconds'])
    row = base.execute_qe(out, pw, txt, timeout_s, tag)
    gamma = (float(row['energy_ev']) - layer * float(f['bulk_energy_ev_per_atom'])) / 2.0
    cell_z, _ = base.slab_geometry(float(f['a_angstrom']), float(f['c_angstrom']), layer, float(f['total_vacuum_angstrom']))
    source_failure = next(x for x in r['mechanical_failures'] if int(x['layers']) == layer)
    row.update({
        'schema': 'h-ru0001-layer-extension-case-v0.1',
        'status': 'VALID_EXTENSION_LAYER',
        'layers': layer,
        'surface_excess_ev_per_surface_atom': gamma,
        'total_vacuum_angstrom': float(f['total_vacuum_angstrom']),
        'cell_z_angstrom': cell_z,
        'kmesh': list(f['surface_kmesh']),
        'ecutwfc_ry': int(f['ecutwfc_ry']),
        'ecutrho_ry': int(f['ecutrho_ry']),
        'protocol_sha256': sha256(pp),
        'source_evidence_sha256': sha256(sp),
        'mechanical_recovery_record_git_blob_sha': git_blob_sha(rp),
        'mechanical_recovery_timeout_seconds': timeout_s,
        'source_failed_job_id': int(source_failure['job_id']),
        'source_failed_output_sha256': source_failure['output_sha256'],
        'scientific_settings_changed': False,
        'thresholds_changed': False,
        'paid_compute_used': False
    })
    path = out / f'SYSTEM3_LAYER_L{layer}_RESULT.json'
    write(path, row)
    print(json.dumps(row, indent=2, sort_keys=True))
    print(f'SYSTEM3_LAYER_L{layer}_RECOVERY_VALID')


def materialize_l15(args):
    pp = Path(args.protocol).resolve()
    sp = Path(args.source_evidence).resolve()
    rp = Path(args.recovery).resolve()
    lp = Path(args.l15_interim).resolve()
    p, s, r, l15 = contract(pp, sp, rp, lp)
    m = l15['measurement']
    row = {
        'schema': 'h-ru0001-layer-extension-case-v0.1',
        'status': 'VALID_EXTENSION_LAYER',
        'layers': 15,
        'tag': m['tag'],
        'surface_excess_ev_per_surface_atom': float(m['surface_excess_ev_per_surface_atom']),
        'energy_ev': float(m['energy_ev']),
        'energy_count': int(m['energy_count']),
        'elapsed_s': float(m['elapsed_s']),
        'cell_z_angstrom': float(m['cell_z_angstrom']),
        'total_vacuum_angstrom': float(m['total_vacuum_angstrom']),
        'kmesh': list(m['kmesh']),
        'ecutwfc_ry': int(m['ecutwfc_ry']),
        'ecutrho_ry': int(m['ecutrho_ry']),
        'job_done': bool(m['job_done']),
        'return_code': int(m['return_code']),
        'timeout': bool(m['timeout']),
        'input_sha256': m['input_sha256'],
        'output_sha256': m['output_sha256'],
        'protocol_sha256': sha256(pp),
        'source_evidence_sha256': sha256(sp),
        'scientific_settings_changed': False,
        'thresholds_changed': False,
        'paid_compute_used': False,
        'materialized_from_committed_interim_evidence': True,
        'source_artifact_digest': l15['lineage']['artifact_digest']
    }
    out = Path(args.out).resolve()
    write(out, row)
    print('SYSTEM3_L15_COMMITTED_EVIDENCE_MATERIALIZED')


def self_test(args):
    p, s, r, l15 = contract(
        Path(args.protocol).resolve(), Path(args.source_evidence).resolve(),
        Path(args.recovery).resolve(), Path(args.l15_interim).resolve()
    )
    assert p['extension_batch']['new_layers'] == [15, 17, 19]
    assert r['recovery_execution']['failed_layers_only'] == [17, 19]
    assert r['decision_contract']['next_batch_if_hold'] == [21, 23, 25]
    assert r['decision_contract']['if_pass'] == 'RUN_COUPLED_ENDPOINT_RECHECK_BEFORE_RELAXATION'
    print('SYSTEM3_LAYER_EXTENSION_TIMEOUT_RECOVERY_SELF_TEST_PASS')
    print('FAILED_LAYERS=17,19')
    print('RECOVERY_TIMEOUT_SECONDS=14400')
    print('TOLERANCE_EV_PER_SURFACE_ATOM=0.001')
    print('COUPLED_ENDPOINT_RECHECK_REQUIRED_AFTER_PASS=true')


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd', required=True)
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument('--protocol', required=True)
    common.add_argument('--source-evidence', required=True)
    common.add_argument('--recovery', required=True)
    common.add_argument('--l15-interim', required=True)

    x = sub.add_parser('self-test', parents=[common])
    x.set_defaults(func=self_test)

    x = sub.add_parser('run-layer', parents=[common])
    x.add_argument('--layers', type=int, required=True)
    x.add_argument('--pw', required=True)
    x.add_argument('--pseudo-dir', required=True)
    x.add_argument('--out', required=True)
    x.set_defaults(func=run_layer)

    x = sub.add_parser('materialize-l15', parents=[common])
    x.add_argument('--out', required=True)
    x.set_defaults(func=materialize_l15)

    a = ap.parse_args()
    a.func(a)


if __name__ == '__main__':
    main()
