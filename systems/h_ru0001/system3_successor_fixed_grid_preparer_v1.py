#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any

PREPARATION_PROTOCOL_BLOB_SHA = "daa3a9560d0e9ed9ed3c7fdc086507a5a4db5d60"
DIAGNOSTIC_PROTOCOL_BLOB_SHA = "b943664b17abaef3c478cffbf66b1600c558a09f"
HOLD_BLOB_SHA = "5f975b604eda3942eef87d215fb1eaf096f17cef"
DIAGNOSTIC_RESULT_SCHEMA = "h-ru0001-post-hold-kmesh-diagnostic-result-v0.1"
SUCCESSOR_SCHEMA = "h-ru0001-successor-fixed-grid-protocol-v0.1"
TOL = 0.001


def load(path: str | Path) -> dict[str, Any]:
    row = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(row, dict):
        raise SystemExit(f"MECHANICAL_HOLD: JSON object required: {path}")
    return row


def write(path: str | Path, row: dict[str, Any]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(row, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def static_contract(prep_path: Path, diag_path: Path, hold_path: Path):
    prep, diag, hold = load(prep_path), load(diag_path), load(hold_path)
    if git_blob_sha(prep_path) != PREPARATION_PROTOCOL_BLOB_SHA:
        raise SystemExit("MECHANICAL_HOLD: successor preparation protocol blob drift")
    if git_blob_sha(diag_path) != DIAGNOSTIC_PROTOCOL_BLOB_SHA:
        raise SystemExit("MECHANICAL_HOLD: diagnostic protocol blob drift")
    if git_blob_sha(hold_path) != HOLD_BLOB_SHA:
        raise SystemExit("MECHANICAL_HOLD: original coupled HOLD blob drift")
    if prep.get("status") != "FROZEN_BEFORE_K24_K28_DIAGNOSTIC_RESULTS":
        raise SystemExit("SCIENTIFIC_HOLD: successor preparation was not prospectively frozen")
    if prep.get("phase") != "P0_Q":
        raise SystemExit("SCIENTIFIC_HOLD: successor preparation phase drift")
    if hold.get("status") != "CLEAN_SURFACE_COUPLED_CONVERGENCE_HOLD" or hold.get("adjudication", {}).get("failed_axis") != "kmesh":
        raise SystemExit("SCIENTIFIC_HOLD: preserved source HOLD identity mismatch")
    if prep["source_lineage"]["original_K16_hold_must_remain"] is not True:
        raise SystemExit("SCIENTIFIC_HOLD: original K16 HOLD preservation disabled")
    if prep["candidate_selection"]["diagnostic_ladder"] != [[20, 20, 1], [24, 24, 1], [28, 28, 1]]:
        raise SystemExit("SCIENTIFIC_HOLD: successor candidate ladder drift")
    if float(prep["candidate_selection"]["tolerance_ev_per_surface_atom"]) != TOL:
        raise SystemExit("SCIENTIFIC_HOLD: successor tolerance drift")
    if prep["fresh_successor_qualification"]["reuse_diagnostic_energies_as_successor_PASS_evidence"] is not False:
        raise SystemExit("SCIENTIFIC_HOLD: diagnostic evidence reuse firewall opened")
    fw = prep["firewalls"]
    prohibited_true = [
        "original_K16_coupled_hold_rewritten",
        "diagnostic_relabelled_as_P1_confirmation",
        "threshold_retuning_allowed",
        "published_H_Ru_kinetics_used",
        "published_H_Ru_barriers_used",
        "published_site_ordering_used",
        "chi_used",
        "expected_ChemSA_used",
        "System2_outcomes_used",
        "paid_compute_required",
        "direct_relaxation_from_diagnostic",
    ]
    if any(bool(fw[k]) for k in prohibited_true):
        raise SystemExit("SCIENTIFIC_HOLD: successor preparation firewall opened")
    return prep, diag, hold


def select_candidate(k20: float, k24: float, k28: float, tol: float = TOL):
    values = [k20, k24, k28]
    if not all(math.isfinite(v) for v in values):
        raise ValueError("non-finite k-mesh diagnostic value")
    d20 = abs(k20 - k28)
    d24 = abs(k24 - k28)
    if d24 > tol:
        selected = None
    elif d20 <= tol:
        selected = [20, 20, 1]
    else:
        selected = [24, 24, 1]
    return selected, {"K20_vs_K28": d20, "K24_vs_K28": d24}


def validate_diagnostic_result(path: Path, diag_path: Path, hold_path: Path):
    row = load(path)
    if row.get("schema") != DIAGNOSTIC_RESULT_SCHEMA:
        raise SystemExit("MECHANICAL_HOLD: diagnostic result schema mismatch")
    if row.get("original_coupled_hold_preserved") is not True:
        raise SystemExit("SCIENTIFIC_HOLD: diagnostic does not preserve original coupled HOLD")
    if row.get("CLEAN_SURFACE_FIXED_GRID_PASS_emitted") is not False or row.get("relaxation_authorized") is not False:
        raise SystemExit("SCIENTIFIC_HOLD: diagnostic illegally promoted itself")
    if row.get("successor_protocol_required_before_any_production_promotion") is not True:
        raise SystemExit("SCIENTIFIC_HOLD: successor protocol firewall missing")
    if row.get("scientific_settings_changed") is not False or row.get("thresholds_changed") is not False:
        raise SystemExit("SCIENTIFIC_HOLD: diagnostic reports scientific drift")
    if row.get("chi_used") is not False or row.get("kinetic_inputs_used") is not False or row.get("paid_compute_used") is not False:
        raise SystemExit("SCIENTIFIC_HOLD: diagnostic evidence/cost firewall violation")
    if row.get("protocol_sha256") != sha256(diag_path):
        raise SystemExit("MECHANICAL_HOLD: diagnostic protocol SHA-256 mismatch")
    if row.get("hold_sha256") != sha256(hold_path):
        raise SystemExit("MECHANICAL_HOLD: diagnostic HOLD SHA-256 mismatch")
    values = row.get("surface_excess_ev_per_surface_atom", {})
    try:
        k20 = float(values["K20"])
        k24 = float(values["K24"])
        k28 = float(values["K28"])
    except Exception as exc:
        raise SystemExit(f"MECHANICAL_HOLD: incomplete diagnostic values: {exc}")
    selected, deltas = select_candidate(k20, k24, k28)
    observed = row.get("absolute_deltas_ev_per_surface_atom", {})
    for key, value in deltas.items():
        if key not in observed or abs(float(observed[key]) - value) > 1e-12:
            raise SystemExit(f"MECHANICAL_HOLD: diagnostic delta mismatch for {key}")
    if float(row.get("tolerance_ev_per_surface_atom")) != TOL:
        raise SystemExit("SCIENTIFIC_HOLD: diagnostic result tolerance drift")
    return row, selected, deltas


def build_successor(prep: dict[str, Any], diagnostic_result: dict[str, Any], diagnostic_path: Path, selected: list[int], deltas: dict[str, float]):
    m = prep["successor_scientific_model"]
    q = prep["fresh_successor_qualification"]
    values = diagnostic_result["surface_excess_ev_per_surface_atom"]
    return {
        "schema": SUCCESSOR_SCHEMA,
        "status": "FROZEN_AFTER_P0_Q_DIAGNOSTIC_BEFORE_SUCCESSOR_QUALIFICATION_RESULTS",
        "phase": "P0_Q",
        "system": "H/Ru(0001)",
        "selection_provenance": {
            "preparation_protocol_git_blob_sha": PREPARATION_PROTOCOL_BLOB_SHA,
            "diagnostic_result_sha256": sha256(diagnostic_path),
            "diagnostic_result_original_status": diagnostic_result["status"],
            "diagnostic_values_ev_per_surface_atom": values,
            "diagnostic_deltas_ev_per_surface_atom": deltas,
            "selected_kmesh": selected,
            "selection_was_informed_by_P0_Q_qualification_evidence": True,
            "selection_evidence_is_untouched_P1_confirmation": False,
            "original_K16_coupled_hold_preserved": True,
        },
        "frozen_scientific_settings": {
            "layers": int(m["layers"]),
            "total_vacuum_angstrom": float(m["total_vacuum_angstrom"]),
            "surface_kmesh": selected,
            "a_angstrom": float(m["a_angstrom"]),
            "c_angstrom": float(m["c_angstrom"]),
            "bulk_energy_ev_per_atom": float(m["bulk_energy_ev_per_atom"]),
            "ecutwfc_ry": int(m["ecutwfc_ry"]),
            "ecutrho_ry": int(m["ecutrho_ry"]),
            "exchange_correlation": m["exchange_correlation"],
            "occupations": m["occupations"],
            "smearing": m["smearing"],
            "degauss_ry": float(m["degauss_ry"]),
            "electron_conv_thr": float(m["electron_conv_thr"]),
            "electron_maxstep": int(m["electron_maxstep"]),
            "mixing_beta": float(m["mixing_beta"]),
            "surface_geometry": m["surface_geometry"],
            "electrostatics": m["electrostatics"],
        },
        "fresh_successor_qualification": {
            "all_four_cases_must_be_fresh": True,
            "reuse_diagnostic_energies_as_PASS_evidence": False,
            "base_case": {"layers": 17, "total_vacuum_angstrom": 15.0, "kmesh": selected},
            "endpoint_cases": {
                "kmesh": {"layers": 17, "total_vacuum_angstrom": 15.0, "kmesh": [28, 28, 1]},
                "vacuum": {"layers": 17, "total_vacuum_angstrom": 25.0, "kmesh": selected},
                "layers": {"layers": 19, "total_vacuum_angstrom": 15.0, "kmesh": selected},
            },
            "absolute_surface_excess_tolerance_ev_per_surface_atom": TOL,
            "pass_status": q["pass_status"],
            "hold_status": q["hold_status"],
            "require_JOB_DONE": True,
            "require_exact_engine_and_Ru_pseudopotential_hashes": True,
        },
        "routing": {
            "on_pass": "ENTER_EXISTING_CLEAN_SURFACE_RELAXATION_PROTOCOL",
            "on_hold": "PRESERVE_HOLD_AND_DO_NOT_RELAX",
            "relaxation_required_entry_status": "CLEAN_SURFACE_FIXED_GRID_PASS",
        },
        "firewalls": {
            "original_K16_hold_rewritten": False,
            "diagnostic_relabelled_as_P1_confirmation": False,
            "thresholds_changed": False,
            "kinetic_inputs_used": False,
            "chi_used": False,
            "System2_outcomes_used": False,
            "paid_compute_required": False,
            "direct_relaxation_before_successor_PASS": False,
        },
    }


def prepare(args) -> None:
    prep_path = Path(args.preparation_protocol).resolve()
    diag_path = Path(args.diagnostic_protocol).resolve()
    hold_path = Path(args.hold).resolve()
    result_path = Path(args.diagnostic_result).resolve()
    prep, _, _ = static_contract(prep_path, diag_path, hold_path)
    result, selected, deltas = validate_diagnostic_result(result_path, diag_path, hold_path)
    if selected is None:
        decision = {
            "schema": "h-ru0001-successor-fixed-grid-preparation-decision-v0.1",
            "status": "NO_SUCCESSOR_FIXED_GRID_FROM_CURRENT_DIAGNOSTIC",
            "phase": "P0_Q",
            "diagnostic_result_sha256": sha256(result_path),
            "diagnostic_result_original_status": result["status"],
            "absolute_deltas_ev_per_surface_atom": deltas,
            "tolerance_ev_per_surface_atom": TOL,
            "original_K16_coupled_hold_preserved": True,
            "relaxation_authorized": False,
            "thresholds_changed": False,
        }
        write(args.out, decision)
        print(json.dumps(decision, indent=2, sort_keys=True))
        print(decision["status"])
        return
    successor = build_successor(prep, result, result_path, selected, deltas)
    write(args.out, successor)
    print(json.dumps(successor, indent=2, sort_keys=True))
    print("SUCCESSOR_FIXED_GRID_PROTOCOL_PREPARED")
    print(f"SELECTED_KMESH={selected[0]}")


def self_test(args) -> None:
    prep_path = Path(args.preparation_protocol).resolve()
    diag_path = Path(args.diagnostic_protocol).resolve()
    hold_path = Path(args.hold).resolve()
    static_contract(prep_path, diag_path, hold_path)
    sel, d = select_candidate(1.0004, 1.0003, 1.0)
    assert sel == [20, 20, 1] and d["K20_vs_K28"] <= TOL and d["K24_vs_K28"] <= TOL
    sel, d = select_candidate(1.0014, 1.0004, 1.0)
    assert sel == [24, 24, 1] and d["K20_vs_K28"] > TOL and d["K24_vs_K28"] <= TOL
    sel, d = select_candidate(1.0014, 1.0011, 1.0)
    assert sel is None and d["K24_vs_K28"] > TOL
    print("SYSTEM3_SUCCESSOR_FIXED_GRID_PREPARER_SELF_TEST_PASS")
    print("TOLERANCE_EV_PER_SURFACE_ATOM=0.001")
    print("SELECTION_RULE=SMALLEST_SUFFIX_QUALIFIED_NONTERMINAL_KMESH")
    print("FRESH_SUCCESSOR_COUPLED_REQUALIFICATION_REQUIRED=true")
    print("ORIGINAL_K16_HOLD_PRESERVED=true")


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--preparation-protocol", required=True)
    common.add_argument("--diagnostic-protocol", required=True)
    common.add_argument("--hold", required=True)
    p = sub.add_parser("self-test", parents=[common])
    p.set_defaults(func=self_test)
    p = sub.add_parser("prepare", parents=[common])
    p.add_argument("--diagnostic-result", required=True)
    p.add_argument("--out", required=True)
    p.set_defaults(func=prepare)
    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
