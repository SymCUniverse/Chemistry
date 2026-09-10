#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import system3_clean_ru0001_numerical_v1 as base

PARENT_SCHEMA = 'h-ru0001-clean-surface-layer-extension-protocol-v0.3'
PARENT_STATUS = 'FROZEN_BEFORE_L15_L17_L19_EXTENSION_RESULTS'
GUARD_SCHEMA = 'h-ru0001-post-extension-coupled-gate-guard-v0.1'
GUARD_STATUS = 'FROZEN_BEFORE_L15_L17_L19_EXTENSION_RESULTS'
HOLD_SCHEMA = 'h-ru0001-clean-surface-layer-extension-result-v0.3'
HOLD_STATUS = 'CLEAN_SURFACE_LAYER_EXTENSION_HOLD'
CONT_SCHEMA = 'h-ru0001-clean-surface-layer-extension-continuation-v0.4'
CONT_STATUS = 'FROZEN_AFTER_L15_L17_L19_HOLD_BEFORE_L21_L23_L25_RESULTS'
CONT_GUARD_SCHEMA = 'h-ru0001-post-continuation-coupled-gate-guard-v0.2'
CONT_GUARD_STATUS = 'FROZEN_AFTER_L15_L17_L19_HOLD_BEFORE_L21_L23_L25_RESULTS'
NEW_LAYERS = [21, 23, 25]
TOL = 0.001


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def load(path: str | Path) -> dict[str, Any]:
    row = json.loads(Path(path).read_text())
    if not isinstance(row, dict):
        raise SystemExit(f'MECHANICAL_HOLD: JSON object required: {path}')
    return row


def write(path: str | Path, row: dict[str, Any]):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(row, indent=2, sort_keys=True) + '\n')


def parent_contract(parent_path: Path, guard_path: Path):
    p = load(parent_path)
    g = load(guard_path)
    if p.get('schema') != PARENT_SCHEMA or p.get('status') != PARENT_STATUS:
        raise SystemExit('SCIENTIFIC_HOLD: parent extension protocol identity drift')
    if g.get('schema') != GUARD_SCHEMA or g.get('status') != GUARD_STATUS:
        raise SystemExit('SCIENTIFIC_HOLD: lineage guard identity drift')
    f = p['frozen_numerical_settings']
    if float(f['absolute_surface_excess_tolerance_ev_per_surface_atom']) != TOL:
        raise SystemExit('SCIENTIFIC_HOLD: parent 1 meV threshold drift')
    if p['extension_batch']['new_layers'] != [15, 17, 19] or p['extension_batch']['terminal_reference_layers'] != 19:
        raise SystemExit('SCIENTIFIC_HOLD: parent layer ladder drift')
    d = p['decision']
    if d['next_batch_if_hold'] != NEW_LAYERS or d['user_reauthorization_required_for_same_rule_next_batch'] is not False:
        raise SystemExit('SCIENTIFIC_HOLD: L21/L23/L25 preauthorization missing')
    gd = g['decision_routing']['if_layer_extension_hold']
    if gd['registered_next_batch'] != NEW_LAYERS or gd['user_reauthorization_required_for_same_rule'] is not False:
        raise SystemExit('SCIENTIFIC_HOLD: guard L21/L23/L25 routing drift')
    if g['decision_routing']['if_layer_extension_pass']['direct_relaxation_entry_forbidden'] is not True:
        raise SystemExit('SCIENTIFIC_HOLD: coupled recheck bypass opened')
    if any(bool(v) for v in p['evidence_firewall'].values()):
        raise SystemExit('SCIENTIFIC_HOLD: parent evidence firewall opened')
    return p, g


def validate_hold(hold_path: Path, parent_path: Path, p: dict[str, Any]):
    h = load(hold_path)
    if h.get('schema') != HOLD_SCHEMA or h.get('status') != HOLD_STATUS:
        raise SystemExit('SCIENTIFIC_HOLD: continuation requires an actual L15/L17/L19 HOLD')
    if h.get('selected_layers') is not None or int(h.get('terminal_reference_layers', 0)) != 19:
        raise SystemExit('SCIENTIFIC_HOLD: source HOLD selection/terminal mismatch')
    if h.get('next_batch_if_hold') != NEW_LAYERS:
        raise SystemExit('SCIENTIFIC_HOLD: source HOLD does not authorize L21/L23/L25')
    if float(h.get('tolerance_ev_per_surface_atom', -1)) != TOL:
        raise SystemExit('SCIENTIFIC_HOLD: source HOLD tolerance drift')
    if h.get('protocol_sha256') != sha256(parent_path):
        raise SystemExit('MECHANICAL_HOLD: source HOLD parent protocol hash mismatch')
    if h.get('source_evidence_sha256') != p['source_evidence']['sha256']:
        raise SystemExit('MECHANICAL_HOLD: source HOLD evidence hash mismatch')
    if h.get('scientific_settings_changed') is not False or h.get('thresholds_changed') is not False:
        raise SystemExit('SCIENTIFIC_HOLD: source HOLD reports scientific drift')
    if h.get('kinetic_inputs_used') is not False or h.get('chi_used') is not False or h.get('paid_compute_used') is not False:
        raise SystemExit('SCIENTIFIC_HOLD: source HOLD firewall/provenance violation')
    rows = h.get('combined_layers')
    if not isinstance(rows, list) or [int(r['layers']) for r in rows] != [5, 7, 9, 11, 13, 15, 17, 19]:
        raise SystemExit('MECHANICAL_HOLD: source HOLD combined ladder incomplete')
    return h


def prepare(args):
    parent_path = Path(args.parent_protocol).resolve()
    guard_path = Path(args.guard).resolve()
    hold_path = Path(args.hold_result).resolve()
    p, g = parent_contract(parent_path, guard_path)
    h = validate_hold(hold_path, parent_path, p)
    timeout_s = int(args.per_layer_timeout_seconds)
    if timeout_s < int(p['execution']['per_layer_timeout_seconds']):
        raise SystemExit('MECHANICAL_HOLD: continuation timeout may not be smaller than the parent registered timeout')
    f = dict(p['frozen_numerical_settings'])
    protocol = {
        'schema': CONT_SCHEMA,
        'status': CONT_STATUS,
        'effective_date': args.effective_date,
        'system': 'H/Ru(0001)',
        'scope': 'NON_KINETIC_CLEAN_SURFACE_LAYER_DEPTH_CONTINUATION',
        'purpose': 'Execute the already preauthorized same-rule L21/L23/L25 continuation after a valid L15/L17/L19 HOLD without changing scientific settings, threshold, evidence firewall, or interpretation.',
        'lineage': {
            'parent_protocol_path': str(args.parent_protocol),
            'parent_protocol_sha256': sha256(parent_path),
            'parent_guard_path': str(args.guard),
            'parent_guard_sha256': sha256(guard_path),
            'source_hold_path': str(args.hold_result),
            'source_hold_sha256': sha256(hold_path),
            'source_hold_status': HOLD_STATUS
        },
        'frozen_numerical_settings': f,
        'extension_batch': {
            'source_layers': [5, 7, 9, 11, 13, 15, 17, 19],
            'new_layers': NEW_LAYERS,
            'combined_ladder': [5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25],
            'terminal_reference_layers': 25,
            'increment_layers': 2,
            'selection_rule': p['extension_batch']['selection_rule']
        },
        'execution': {
            'runner_label': 'ubuntu-24.04',
            'execution_mode': p['execution']['execution_mode'],
            'mpi_ranks': p['execution']['mpi_ranks'],
            'OMP_NUM_THREADS': p['execution']['OMP_NUM_THREADS'],
            'OPENBLAS_NUM_THREADS': p['execution']['OPENBLAS_NUM_THREADS'],
            'MKL_NUM_THREADS': p['execution']['MKL_NUM_THREADS'],
            'per_layer_timeout_seconds': timeout_s,
            'timeout_change_is_mechanical_only': True,
            'parallel_independent_layers': True
        },
        'runtime_identity': dict(p['runtime_identity']),
        'decision': {
            'pass_status': 'CLEAN_SURFACE_LAYER_EXTENSION_PASS',
            'pass_next_gate': 'COUPLED_ENDPOINT_RECHECK_WITH_L25_TERMINAL',
            'hold_status': 'CLEAN_SURFACE_LAYER_EXTENSION_HOLD',
            'hold_next_gate': 'SCIENTIFIC_REVIEW_REQUIRED_BEFORE_ANY_FURTHER_LAYER_EXTENSION',
            'further_batch_preauthorized': False,
            'threshold_retuning_allowed': False,
            'automatic_adsorption_progression': False
        },
        'evidence_firewall': dict(p['evidence_firewall']),
        'provenance': {
            'continuation_trigger': HOLD_STATUS,
            'continuation_rule': 'Use the already preauthorized +2 odd-layer sequence L21/L23/L25 only.',
            'scientific_settings_changed': False,
            'thresholds_changed': False,
            'kinetic_inputs_used': False,
            'chi_used': False,
            'paid_compute_used': False
        }
    }
    guard2 = {
        'schema': CONT_GUARD_SCHEMA,
        'status': CONT_GUARD_STATUS,
        'effective_date': args.effective_date,
        'system': 'H/Ru(0001)',
        'scope': 'NON_KINETIC_CLEAN_SURFACE_PROGRESSION_CONTROL',
        'lineage': {
            'parent_guard_path': str(args.guard),
            'parent_guard_sha256': sha256(guard_path),
            'continuation_protocol_path': str(args.out_protocol),
            'source_hold_path': str(args.hold_result),
            'source_hold_sha256': sha256(hold_path)
        },
        'decision_routing': {
            'if_continuation_pass': {
                'required_action': 'RUN_COUPLED_ENDPOINT_RECHECK_BEFORE_RELAXATION',
                'direct_relaxation_entry_forbidden': True,
                'required_entry_status_for_relaxation': 'CLEAN_SURFACE_FIXED_GRID_PASS'
            },
            'if_continuation_hold': {
                'required_action': 'STOP_FOR_SCIENTIFIC_REVIEW_BEFORE_FURTHER_LAYER_EXTENSION',
                'further_batch_preauthorized': False
            }
        },
        'coupled_endpoint_recheck': {
            'required': True,
            'absolute_surface_excess_tolerance_ev_per_surface_atom': TOL,
            'base_point': {'layers': 'FROM_CONTINUATION_SELECTION', 'total_vacuum_angstrom': 15.0, 'kmesh': [16, 16, 1]},
            'one_axis_endpoint_substitutions': {
                'kmesh': {'layers': 'FROM_CONTINUATION_SELECTION', 'total_vacuum_angstrom': 15.0, 'kmesh': [20, 20, 1]},
                'vacuum': {'layers': 'FROM_CONTINUATION_SELECTION', 'total_vacuum_angstrom': 25.0, 'kmesh': [16, 16, 1]},
                'layers': {'layers': 25, 'total_vacuum_angstrom': 15.0, 'kmesh': [16, 16, 1]}
            },
            'pass_status': 'CLEAN_SURFACE_FIXED_GRID_PASS',
            'hold_status': 'CLEAN_SURFACE_COUPLED_CONVERGENCE_HOLD'
        },
        'frozen_controls': {
            'electronic_settings_changed': False,
            'surface_geometry_rule_changed': False,
            'kmesh_selection_changed': False,
            'vacuum_selection_changed': False,
            'layer_selection_rule_changed': False,
            'thresholds_changed': False,
            'kinetic_inputs_used': False,
            'chi_used': False,
            'published_H_Ru_outcomes_used': False,
            'System2_outcomes_used': False,
            'paid_compute_used': False
        }
    }
    write(args.out_protocol, protocol)
    write(args.out_guard, guard2)
    print('SYSTEM3_L21_L23_L25_CONTINUATION_PROTOCOL_PREPARED')
    print(f'SOURCE_HOLD_SHA256={sha256(hold_path)}')
    print(f'PER_LAYER_TIMEOUT_SECONDS={timeout_s}')


def continuation_contract(protocol_path: Path, guard_path: Path, hold_path: Path):
    p = load(protocol_path)
    g = load(guard_path)
    if p.get('schema') != CONT_SCHEMA or p.get('status') != CONT_STATUS:
        raise SystemExit('SCIENTIFIC_HOLD: continuation protocol not frozen')
    if g.get('schema') != CONT_GUARD_SCHEMA or g.get('status') != CONT_GUARD_STATUS:
        raise SystemExit('SCIENTIFIC_HOLD: continuation guard not frozen')
    lin = p['lineage']
    if sha256(hold_path) != lin['source_hold_sha256'] or g['lineage']['source_hold_sha256'] != lin['source_hold_sha256']:
        raise SystemExit('MECHANICAL_HOLD: continuation source HOLD hash mismatch')
    h = load(hold_path)
    if h.get('status') != HOLD_STATUS:
        raise SystemExit('SCIENTIFIC_HOLD: continuation source is not HOLD')
    if p['extension_batch']['new_layers'] != NEW_LAYERS or p['extension_batch']['terminal_reference_layers'] != 25:
        raise SystemExit('SCIENTIFIC_HOLD: continuation ladder drift')
    if float(p['frozen_numerical_settings']['absolute_surface_excess_tolerance_ev_per_surface_atom']) != TOL:
        raise SystemExit('SCIENTIFIC_HOLD: continuation threshold drift')
    if g['coupled_endpoint_recheck']['one_axis_endpoint_substitutions']['layers']['layers'] != 25:
        raise SystemExit('SCIENTIFIC_HOLD: continuation coupled terminal drift')
    if any(bool(v) for v in p['evidence_firewall'].values()) or any(bool(v) for v in g['frozen_controls'].values()):
        raise SystemExit('SCIENTIFIC_HOLD: continuation firewall opened')
    return p, g, h


def verify_runtime(p: dict[str, Any], pw: Path, pseudo_dir: Path):
    ru = pseudo_dir / 'Ru.nc.pbe.z_16.oncvpsp4.sg15.v0.upf'
    if sha256(pw) != p['runtime_identity']['pw_x_sha256']:
        raise SystemExit('MECHANICAL_HOLD: pw.x hash mismatch')
    if not ru.is_file() or sha256(ru) != p['runtime_identity']['ru_pseudo_sha256']:
        raise SystemExit('MECHANICAL_HOLD: Ru pseudo hash mismatch')


def run_layer(args):
    pp = Path(args.protocol).resolve(); gp = Path(args.guard).resolve(); hp = Path(args.hold_result).resolve()
    p, g, h = continuation_contract(pp, gp, hp)
    layer = int(args.layers)
    if layer not in NEW_LAYERS:
        raise SystemExit('SCIENTIFIC_HOLD: unregistered continuation layer')
    pw = Path(args.pw).resolve(); pseudo = Path(args.pseudo_dir).resolve(); verify_runtime(p, pw, pseudo)
    f = p['frozen_numerical_settings']; out = Path(args.out).resolve(); out.mkdir(parents=True, exist_ok=True)
    tag = f'slab_L{layer}_V15_K16_16_1_extension_continuation'
    txt = base.slab_input(float(f['a_angstrom']), float(f['c_angstrom']), layer, float(f['total_vacuum_angstrom']), int(f['ecutwfc_ry']), int(f['ecutrho_ry']), tuple(f['surface_kmesh']), pseudo, '__OUTDIR__', tag)
    row = base.execute_qe(out, pw, txt, int(p['execution']['per_layer_timeout_seconds']), tag)
    gamma = (float(row['energy_ev']) - layer * float(f['bulk_energy_ev_per_atom'])) / 2.0
    row.update({'schema': 'h-ru0001-layer-continuation-case-v0.4', 'status': 'VALID_EXTENSION_LAYER', 'layers': layer, 'surface_excess_ev_per_surface_atom': gamma, 'total_vacuum_angstrom': float(f['total_vacuum_angstrom']), 'kmesh': list(f['surface_kmesh']), 'ecutwfc_ry': int(f['ecutwfc_ry']), 'ecutrho_ry': int(f['ecutrho_ry']), 'protocol_sha256': sha256(pp), 'guard_sha256': sha256(gp), 'source_hold_sha256': sha256(hp), 'scientific_settings_changed': False, 'thresholds_changed': False, 'paid_compute_used': False})
    write(out / f'SYSTEM3_LAYER_L{layer}_RESULT.json', row)
    print(f'SYSTEM3_LAYER_L{layer}_CONTINUATION_VALID')


def adjudicate(args):
    pp = Path(args.protocol).resolve(); gp = Path(args.guard).resolve(); hp = Path(args.hold_result).resolve()
    p, g, h = continuation_contract(pp, gp, hp)
    combined = [{'layers': int(r['layers']), 'surface_excess_ev_per_surface_atom': float(r['surface_excess_ev_per_surface_atom']), 'source': 'source_hold'} for r in h['combined_layers']]
    root = Path(args.results_root).resolve()
    for layer in NEW_LAYERS:
        hits = list(root.rglob(f'SYSTEM3_LAYER_L{layer}_RESULT.json'))
        if len(hits) != 1:
            raise SystemExit(f'MECHANICAL_HOLD: expected one L{layer} result, found {len(hits)}')
        r = load(hits[0])
        if r.get('status') != 'VALID_EXTENSION_LAYER' or int(r.get('layers', 0)) != layer:
            raise SystemExit(f'MECHANICAL_HOLD: L{layer} result identity mismatch')
        if r.get('protocol_sha256') != sha256(pp) or r.get('guard_sha256') != sha256(gp) or r.get('source_hold_sha256') != sha256(hp):
            raise SystemExit(f'MECHANICAL_HOLD: L{layer} provenance hash mismatch')
        if r.get('scientific_settings_changed') is not False or r.get('thresholds_changed') is not False:
            raise SystemExit(f'SCIENTIFIC_HOLD: L{layer} reports drift')
        combined.append({'layers': layer, 'surface_excess_ev_per_surface_atom': float(r['surface_excess_ev_per_surface_atom']), 'energy_ev': float(r['energy_ev']), 'input_sha256': r['input_sha256'], 'output_sha256': r['output_sha256'], 'elapsed_s': float(r['elapsed_s']), 'source': 'continuation_v1'})
    combined.sort(key=lambda x: x['layers'])
    if [r['layers'] for r in combined] != p['extension_batch']['combined_ladder']:
        raise SystemExit('MECHANICAL_HOLD: continuation combined ladder incomplete')
    ref = combined[-1]['surface_excess_ev_per_surface_atom']
    deltas = [abs(r['surface_excess_ev_per_surface_atom'] - ref) for r in combined]
    selected = None
    for i, r in enumerate(combined[:-1]):
        if r['layers'] < int(p['frozen_numerical_settings']['minimum_eligible_layers']):
            continue
        if all(d <= TOL for d in deltas[i:]):
            selected = r['layers']; break
    passed = selected is not None
    result = {'schema': 'h-ru0001-clean-surface-layer-extension-result-v0.4', 'status': p['decision']['pass_status'] if passed else p['decision']['hold_status'], 'next_gate': p['decision']['pass_next_gate'] if passed else p['decision']['hold_next_gate'], 'selected_layers': selected, 'terminal_reference_layers': 25, 'terminal_surface_excess_ev_per_surface_atom': ref, 'tolerance_ev_per_surface_atom': TOL, 'combined_layers': combined, 'deltas_to_terminal_ev_per_surface_atom': deltas, 'source_hold_sha256': sha256(hp), 'protocol_sha256': sha256(pp), 'guard_sha256': sha256(gp), 'scientific_settings_changed': False, 'thresholds_changed': False, 'kinetic_inputs_used': False, 'chi_used': False, 'paid_compute_used': False}
    write(args.out, result)
    print(result['status'])


def self_test(args):
    p, g = parent_contract(Path(args.parent_protocol).resolve(), Path(args.guard).resolve())
    assert p['decision']['next_batch_if_hold'] == NEW_LAYERS
    rows = [{'layers': 21, 'surface_excess_ev_per_surface_atom': 1.0}, {'layers': 23, 'surface_excess_ev_per_surface_atom': 1.0004}, {'layers': 25, 'surface_excess_ev_per_surface_atom': 1.0002}]
    idx, deltas = base.suffix_selection(rows, TOL, eligible=lambda r: r['layers'] >= 7)
    assert idx == 0 and max(deltas) <= TOL
    rows2 = [{'layers': 21, 'surface_excess_ev_per_surface_atom': 1.0}, {'layers': 23, 'surface_excess_ev_per_surface_atom': 1.003}, {'layers': 25, 'surface_excess_ev_per_surface_atom': 1.0002}]
    idx2, _ = base.suffix_selection(rows2, TOL, eligible=lambda r: r['layers'] >= 7)
    assert idx2 is None
    print('SYSTEM3_L21_L23_L25_CONTINUATION_PREPARATION_SELF_TEST_PASS')
    print('NEW_LAYERS=21,23,25')
    print('TOLERANCE_EV_PER_SURFACE_ATOM=0.001')
    print('DIRECT_RELAXATION_BYPASS=false')
    print('FURTHER_BATCH_PREAUTHORIZED=false')


def main():
    ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest='cmd', required=True)
    x = sub.add_parser('self-test'); x.add_argument('--parent-protocol', required=True); x.add_argument('--guard', required=True); x.set_defaults(func=self_test)
    x = sub.add_parser('prepare'); x.add_argument('--parent-protocol', required=True); x.add_argument('--guard', required=True); x.add_argument('--hold-result', required=True); x.add_argument('--out-protocol', required=True); x.add_argument('--out-guard', required=True); x.add_argument('--per-layer-timeout-seconds', type=int, required=True); x.add_argument('--effective-date', required=True); x.set_defaults(func=prepare)
    common = argparse.ArgumentParser(add_help=False); common.add_argument('--protocol', required=True); common.add_argument('--guard', required=True); common.add_argument('--hold-result', required=True)
    x = sub.add_parser('run-layer', parents=[common]); x.add_argument('--layers', type=int, required=True); x.add_argument('--pw', required=True); x.add_argument('--pseudo-dir', required=True); x.add_argument('--out', required=True); x.set_defaults(func=run_layer)
    x = sub.add_parser('adjudicate', parents=[common]); x.add_argument('--results-root', required=True); x.add_argument('--out', required=True); x.set_defaults(func=adjudicate)
    a = ap.parse_args(); a.func(a)

if __name__ == '__main__':
    main()
