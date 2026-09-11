#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import system3_clean_ru0001_numerical_v1 as base

PREPARATION_PROTOCOL_BLOB_SHA = "daa3a9560d0e9ed9ed3c7fdc086507a5a4db5d60"
EXTENSION_PROTOCOL_BLOB_SHA = "952e1358b3af4ce637f3c9283e475adc1ae30b0f"
HOLD_BLOB_SHA = "5f975b604eda3942eef87d215fb1eaf096f17cef"
SUCCESSOR_SCHEMA = "h-ru0001-successor-fixed-grid-protocol-v0.1"
CASE_SCHEMA = "h-ru0001-successor-fixed-grid-fresh-case-v0.1"
RESULT_SCHEMA = "h-ru0001-successor-fixed-grid-qualification-result-v0.1"
TOL = 0.001
TIMEOUT_SECONDS = 19800
ALLOWED_SELECTED_K = (20, 24)


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


def file_sha256(path: Path) -> str:
    return sha256(path)


def static_lineage(prep_path: Path, extension_path: Path, hold_path: Path):
    prep, extension, hold = load(prep_path), load(extension_path), load(hold_path)
    if git_blob_sha(prep_path) != PREPARATION_PROTOCOL_BLOB_SHA:
        raise SystemExit("MECHANICAL_HOLD: successor preparation protocol blob drift")
    if git_blob_sha(extension_path) != EXTENSION_PROTOCOL_BLOB_SHA:
        raise SystemExit("MECHANICAL_HOLD: original extension protocol blob drift")
    if git_blob_sha(hold_path) != HOLD_BLOB_SHA:
        raise SystemExit("MECHANICAL_HOLD: original coupled HOLD blob drift")
    if hold.get("status") != "CLEAN_SURFACE_COUPLED_CONVERGENCE_HOLD" or hold.get("adjudication", {}).get("failed_axis") != "kmesh":
        raise SystemExit("SCIENTIFIC_HOLD: source HOLD identity mismatch")
    if prep.get("phase") != "P0_Q" or prep.get("status") != "FROZEN_BEFORE_K24_K28_DIAGNOSTIC_RESULTS":
        raise SystemExit("SCIENTIFIC_HOLD: successor preparation lineage drift")
    if float(prep["candidate_selection"]["tolerance_ev_per_surface_atom"]) != TOL:
        raise SystemExit("SCIENTIFIC_HOLD: preparation tolerance drift")
    if float(extension["frozen_numerical_settings"]["absolute_surface_excess_tolerance_ev_per_surface_atom"]) != TOL:
        raise SystemExit("SCIENTIFIC_HOLD: original surface tolerance drift")
    return prep, extension, hold


def validate_successor(successor_path: Path, prep_path: Path, extension_path: Path, hold_path: Path):
    prep, extension, hold = static_lineage(prep_path, extension_path, hold_path)
    successor = load(successor_path)
    if successor.get("schema") != SUCCESSOR_SCHEMA:
        raise SystemExit("MECHANICAL_HOLD: successor protocol schema mismatch")
    if successor.get("status") != "FROZEN_AFTER_P0_Q_DIAGNOSTIC_BEFORE_SUCCESSOR_QUALIFICATION_RESULTS" or successor.get("phase") != "P0_Q":
        raise SystemExit("SCIENTIFIC_HOLD: successor protocol phase/status mismatch")
    prov = successor.get("selection_provenance", {})
    if prov.get("preparation_protocol_git_blob_sha") != PREPARATION_PROTOCOL_BLOB_SHA:
        raise SystemExit("MECHANICAL_HOLD: successor preparation provenance mismatch")
    if prov.get("selection_was_informed_by_P0_Q_qualification_evidence") is not True:
        raise SystemExit("SCIENTIFIC_HOLD: successor qualification-informed lineage not declared")
    if prov.get("selection_evidence_is_untouched_P1_confirmation") is not False:
        raise SystemExit("SCIENTIFIC_HOLD: successor mislabels qualification evidence as untouched P1")
    if prov.get("original_K16_coupled_hold_preserved") is not True:
        raise SystemExit("SCIENTIFIC_HOLD: original K16 HOLD not preserved")
    selected = successor["frozen_scientific_settings"]["surface_kmesh"]
    if selected not in ([20, 20, 1], [24, 24, 1]):
        raise SystemExit("SCIENTIFIC_HOLD: successor selected kmesh outside prospectively allowed candidates")
    selected_k = int(selected[0])
    if selected_k not in ALLOWED_SELECTED_K:
        raise SystemExit("SCIENTIFIC_HOLD: successor selected kmesh invalid")

    src = extension["frozen_numerical_settings"]
    dst = successor["frozen_scientific_settings"]
    scalar_equal = {
        "layers": int(src["minimum_eligible_layers"]) <= int(dst["layers"]),
        "a_angstrom": float(dst["a_angstrom"]) == float(src["a_angstrom"]),
        "c_angstrom": float(dst["c_angstrom"]) == float(src["c_angstrom"]),
        "bulk_energy_ev_per_atom": float(dst["bulk_energy_ev_per_atom"]) == float(src["bulk_energy_ev_per_atom"]),
        "ecutwfc_ry": int(dst["ecutwfc_ry"]) == int(src["ecutwfc_ry"]),
        "ecutrho_ry": int(dst["ecutrho_ry"]) == int(src["ecutrho_ry"]),
        "exchange_correlation": dst["exchange_correlation"] == src["exchange_correlation"],
        "occupations": dst["occupations"] == src["occupations"],
        "smearing": dst["smearing"] == src["smearing"],
        "degauss_ry": float(dst["degauss_ry"]) == float(src["degauss_ry"]),
        "electron_conv_thr": float(dst["electron_conv_thr"]) == float(src["electron_conv_thr"]),
        "electron_maxstep": int(dst["electron_maxstep"]) == int(src["electron_maxstep"]),
        "mixing_beta": float(dst["mixing_beta"]) == float(src["mixing_beta"]),
    }
    if not all(scalar_equal.values()):
        bad = [k for k, ok in scalar_equal.items() if not ok]
        raise SystemExit(f"SCIENTIFIC_HOLD: successor scientific settings drift: {bad}")
    if int(dst["layers"]) != 17 or float(dst["total_vacuum_angstrom"]) != 15.0:
        raise SystemExit("SCIENTIFIC_HOLD: successor base geometry rule drift")

    q = successor.get("fresh_successor_qualification", {})
    if q.get("all_four_cases_must_be_fresh") is not True or q.get("reuse_diagnostic_energies_as_PASS_evidence") is not False:
        raise SystemExit("SCIENTIFIC_HOLD: fresh successor qualification firewall drift")
    if float(q.get("absolute_surface_excess_tolerance_ev_per_surface_atom")) != TOL:
        raise SystemExit("SCIENTIFIC_HOLD: successor qualification tolerance drift")
    expected_base = {"layers": 17, "total_vacuum_angstrom": 15.0, "kmesh": selected}
    expected_endpoints = {
        "kmesh": {"layers": 17, "total_vacuum_angstrom": 15.0, "kmesh": [28, 28, 1]},
        "vacuum": {"layers": 17, "total_vacuum_angstrom": 25.0, "kmesh": selected},
        "layers": {"layers": 19, "total_vacuum_angstrom": 15.0, "kmesh": selected},
    }
    if q.get("base_case") != expected_base or q.get("endpoint_cases") != expected_endpoints:
        raise SystemExit("SCIENTIFIC_HOLD: successor fresh coupled case set drift")
    fw = successor.get("firewalls", {})
    if any(bool(fw.get(k)) for k in (
        "original_K16_hold_rewritten",
        "diagnostic_relabelled_as_P1_confirmation",
        "thresholds_changed",
        "kinetic_inputs_used",
        "chi_used",
        "System2_outcomes_used",
        "paid_compute_required",
        "direct_relaxation_before_successor_PASS",
    )):
        raise SystemExit("SCIENTIFIC_HOLD: successor protocol firewall opened")
    return successor, extension, hold


def verify_runtime(extension: dict[str, Any], pw: Path, pseudo_dir: Path) -> None:
    runtime = extension["runtime_identity"]
    ru = pseudo_dir / "Ru.nc.pbe.z_16.oncvpsp4.sg15.v0.upf"
    if not pw.is_file() or not ru.is_file():
        raise SystemExit("MECHANICAL_HOLD: exact QE runtime or Ru pseudopotential missing")
    if file_sha256(pw) != runtime["pw_x_sha256"]:
        raise SystemExit("MECHANICAL_HOLD: pw.x SHA-256 mismatch")
    if file_sha256(ru) != runtime["ru_pseudo_sha256"]:
        raise SystemExit("MECHANICAL_HOLD: Ru pseudopotential SHA-256 mismatch")


def case_config(successor: dict[str, Any], case: str) -> dict[str, Any]:
    q = successor["fresh_successor_qualification"]
    if case == "base":
        return q["base_case"]
    if case in ("kmesh", "vacuum", "layers"):
        return q["endpoint_cases"][case]
    raise SystemExit("MECHANICAL_HOLD: case must be base, kmesh, vacuum, or layers")


def run_case(args) -> None:
    successor_path = Path(args.successor_protocol).resolve()
    prep_path = Path(args.preparation_protocol).resolve()
    extension_path = Path(args.extension_protocol).resolve()
    hold_path = Path(args.hold).resolve()
    successor, extension, _ = validate_successor(successor_path, prep_path, extension_path, hold_path)
    pw = Path(args.pw).resolve()
    pseudo = Path(args.pseudo_dir).resolve()
    verify_runtime(extension, pw, pseudo)
    cfg = case_config(successor, args.case)
    s = successor["frozen_scientific_settings"]
    layers = int(cfg["layers"])
    vacuum = float(cfg["total_vacuum_angstrom"])
    kmesh = tuple(int(v) for v in cfg["kmesh"])
    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    tag = f"successor_{args.case}_L{layers}_V{vacuum:g}_K{kmesh[0]}_{kmesh[1]}_{kmesh[2]}"
    input_text = base.slab_input(
        float(s["a_angstrom"]),
        float(s["c_angstrom"]),
        layers,
        vacuum,
        int(s["ecutwfc_ry"]),
        int(s["ecutrho_ry"]),
        kmesh,
        pseudo,
        "__OUTDIR__",
        tag,
    )
    row = base.execute_qe(out, pw, input_text, TIMEOUT_SECONDS, tag)
    gamma = (float(row["energy_ev"]) - layers * float(s["bulk_energy_ev_per_atom"])) / 2.0
    cell_z, _ = base.slab_geometry(float(s["a_angstrom"]), float(s["c_angstrom"]), layers, vacuum)
    row.update({
        "schema": CASE_SCHEMA,
        "status": "VALID_FRESH_SUCCESSOR_FIXED_GRID_CASE",
        "case": args.case,
        "layers": layers,
        "total_vacuum_angstrom": vacuum,
        "cell_z_angstrom": cell_z,
        "kmesh": list(kmesh),
        "surface_excess_ev_per_surface_atom": gamma,
        "successor_protocol_sha256": sha256(successor_path),
        "preparation_protocol_git_blob_sha": PREPARATION_PROTOCOL_BLOB_SHA,
        "original_K16_coupled_hold_preserved": True,
        "fresh_successor_case": True,
        "diagnostic_energy_reused": False,
        "scientific_settings_changed": False,
        "thresholds_changed": False,
        "kinetic_inputs_used": False,
        "chi_used": False,
        "paid_compute_used": False,
        "mechanical_timeout_seconds": TIMEOUT_SECONDS,
    })
    result_path = out / f"SYSTEM3_SUCCESSOR_{args.case.upper()}_RESULT.json"
    write(result_path, row)
    print(json.dumps(row, indent=2, sort_keys=True))
    print(f"SYSTEM3_SUCCESSOR_{args.case.upper()}_VALID")


def adjudicate_values(base_gamma: float, endpoint_values: dict[str, float], tol: float = TOL):
    deltas = {name: abs(value - base_gamma) for name, value in endpoint_values.items()}
    return all(value <= tol for value in deltas.values()), deltas


def adjudicate(args) -> None:
    successor_path = Path(args.successor_protocol).resolve()
    prep_path = Path(args.preparation_protocol).resolve()
    extension_path = Path(args.extension_protocol).resolve()
    hold_path = Path(args.hold).resolve()
    successor, _, _ = validate_successor(successor_path, prep_path, extension_path, hold_path)
    root = Path(args.results_root).resolve()
    rows: dict[str, dict[str, Any]] = {}
    for case in ("base", "kmesh", "vacuum", "layers"):
        hits = list(root.rglob(f"SYSTEM3_SUCCESSOR_{case.upper()}_RESULT.json"))
        if len(hits) != 1:
            raise SystemExit(f"MECHANICAL_HOLD: expected one fresh {case} result, found {len(hits)}")
        row = load(hits[0])
        if row.get("schema") != CASE_SCHEMA or row.get("status") != "VALID_FRESH_SUCCESSOR_FIXED_GRID_CASE" or row.get("case") != case:
            raise SystemExit(f"MECHANICAL_HOLD: fresh successor {case} identity mismatch")
        if row.get("successor_protocol_sha256") != sha256(successor_path):
            raise SystemExit(f"MECHANICAL_HOLD: fresh successor {case} protocol provenance mismatch")
        if row.get("fresh_successor_case") is not True or row.get("diagnostic_energy_reused") is not False:
            raise SystemExit(f"SCIENTIFIC_HOLD: fresh successor {case} evidence reuse violation")
        if row.get("original_K16_coupled_hold_preserved") is not True:
            raise SystemExit(f"SCIENTIFIC_HOLD: fresh successor {case} loses original HOLD")
        if row.get("scientific_settings_changed") is not False or row.get("thresholds_changed") is not False:
            raise SystemExit(f"SCIENTIFIC_HOLD: fresh successor {case} reports scientific drift")
        if row.get("kinetic_inputs_used") is not False or row.get("chi_used") is not False or row.get("paid_compute_used") is not False:
            raise SystemExit(f"SCIENTIFIC_HOLD: fresh successor {case} firewall violation")
        expected = case_config(successor, case)
        if int(row["layers"]) != int(expected["layers"]) or float(row["total_vacuum_angstrom"]) != float(expected["total_vacuum_angstrom"]) or row["kmesh"] != expected["kmesh"]:
            raise SystemExit(f"MECHANICAL_HOLD: fresh successor {case} configuration mismatch")
        if not math.isfinite(float(row["surface_excess_ev_per_surface_atom"])):
            raise SystemExit(f"MECHANICAL_HOLD: non-finite fresh successor {case} value")
        rows[case] = row
    base_gamma = float(rows["base"]["surface_excess_ev_per_surface_atom"])
    endpoints = {name: float(rows[name]["surface_excess_ev_per_surface_atom"]) for name in ("kmesh", "vacuum", "layers")}
    passed, deltas = adjudicate_values(base_gamma, endpoints, TOL)
    q = successor["fresh_successor_qualification"]
    result = {
        "schema": RESULT_SCHEMA,
        "status": q["pass_status"] if passed else q["hold_status"],
        "phase": "P0_Q",
        "selected_layers": 17,
        "selected_total_vacuum_angstrom": 15.0,
        "selected_surface_kmesh": successor["frozen_scientific_settings"]["surface_kmesh"],
        "base_surface_excess_ev_per_surface_atom": base_gamma,
        "endpoint_surface_excess_ev_per_surface_atom": endpoints,
        "absolute_deltas_ev_per_surface_atom": deltas,
        "tolerance_ev_per_surface_atom": TOL,
        "all_endpoints_within_tolerance": passed,
        "successor_protocol_sha256": sha256(successor_path),
        "original_K16_coupled_hold_preserved": True,
        "qualification_informed_by_P0_Q_diagnostic": True,
        "untouched_P1_confirmation": False,
        "all_four_cases_fresh": True,
        "diagnostic_energies_reused_as_PASS_evidence": False,
        "relaxation_authorized": passed,
        "next_gate": "H_RU0001_CLEAN_SURFACE_RELAXATION_AND_REPRODUCTION" if passed else None,
        "scientific_settings_changed": False,
        "thresholds_changed": False,
        "kinetic_inputs_used": False,
        "chi_used": False,
        "paid_compute_used": False,
    }
    write(args.out, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    print(result["status"])


def validate_protocol_cmd(args) -> None:
    successor, _, _ = validate_successor(
        Path(args.successor_protocol).resolve(),
        Path(args.preparation_protocol).resolve(),
        Path(args.extension_protocol).resolve(),
        Path(args.hold).resolve(),
    )
    print("SYSTEM3_SUCCESSOR_FIXED_GRID_PROTOCOL_VALID")
    print(f"SELECTED_KMESH={successor['frozen_scientific_settings']['surface_kmesh'][0]}")
    print("FRESH_FOUR_CASE_REQUALIFICATION_REQUIRED=true")


def self_test(args) -> None:
    static_lineage(
        Path(args.preparation_protocol).resolve(),
        Path(args.extension_protocol).resolve(),
        Path(args.hold).resolve(),
    )
    passed, deltas = adjudicate_values(1.0, {"kmesh": 1.0004, "vacuum": 0.9994, "layers": 1.0008})
    assert passed and max(deltas.values()) <= TOL
    passed, deltas = adjudicate_values(1.0, {"kmesh": 1.0011, "vacuum": 0.9994, "layers": 1.0008})
    assert not passed and deltas["kmesh"] > TOL
    print("SYSTEM3_SUCCESSOR_FIXED_GRID_QUALIFICATION_SELF_TEST_PASS")
    print("CASES=BASE,K28,V25,L19")
    print("ALL_FOUR_CASES_MUST_BE_FRESH=true")
    print("TOLERANCE_EV_PER_SURFACE_ATOM=0.001")
    print("RELAXATION_REQUIRES_CLEAN_SURFACE_FIXED_GRID_PASS=true")


def add_common(parser):
    parser.add_argument("--preparation-protocol", required=True)
    parser.add_argument("--extension-protocol", required=True)
    parser.add_argument("--hold", required=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("self-test")
    add_common(p)
    p.set_defaults(func=self_test)
    p = sub.add_parser("validate-protocol")
    add_common(p)
    p.add_argument("--successor-protocol", required=True)
    p.set_defaults(func=validate_protocol_cmd)
    p = sub.add_parser("run-case")
    add_common(p)
    p.add_argument("--successor-protocol", required=True)
    p.add_argument("--case", choices=["base", "kmesh", "vacuum", "layers"], required=True)
    p.add_argument("--pw", required=True)
    p.add_argument("--pseudo-dir", required=True)
    p.add_argument("--out", required=True)
    p.set_defaults(func=run_case)
    p = sub.add_parser("adjudicate")
    add_common(p)
    p.add_argument("--successor-protocol", required=True)
    p.add_argument("--results-root", required=True)
    p.add_argument("--out", required=True)
    p.set_defaults(func=adjudicate)
    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
