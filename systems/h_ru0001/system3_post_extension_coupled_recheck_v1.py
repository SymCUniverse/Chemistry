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

import system3_clean_ru0001_layer_extension_v1 as ext
import system3_clean_ru0001_numerical_v1 as base

GUARD_BLOB_SHA = "e2a4c743fa097f3a04d7a29708c6e0cf10b29d81"
EXTENSION_BLOB_SHA = "952e1358b3af4ce637f3c9283e475adc1ae30b0f"
SURFACE_BLOB_SHA = "e865b27f9a2455f6902eb27ca59d3274f0808902"
RELAXATION_BLOB_SHA = "748d882349a9ea5f5d646807bff2e1ddfe34e5b6"
RESULT_SCHEMA = "h-ru0001-clean-surface-layer-extension-result-v0.3"
PASS_STATUS = "CLEAN_SURFACE_LAYER_EXTENSION_PASS"
COUPLED_TIMEOUT_SECONDS = 14400


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def load(path: str | Path) -> dict[str, Any]:
    row = json.loads(Path(path).read_text())
    if not isinstance(row, dict):
        raise SystemExit(f"MECHANICAL_HOLD: JSON object required: {path}")
    return row


def write(path: str | Path, row: dict[str, Any]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(row, indent=2, sort_keys=True) + "\n")


def static_contract(guard_path: Path, extension_path: Path, surface_path: Path, relaxation_path: Path):
    guard = load(guard_path)
    extension = load(extension_path)
    surface = load(surface_path)
    relaxation = load(relaxation_path)

    if git_blob_sha(guard_path) != GUARD_BLOB_SHA:
        raise SystemExit("MECHANICAL_HOLD: coupled gate guard blob drift")
    if git_blob_sha(extension_path) != EXTENSION_BLOB_SHA:
        raise SystemExit("MECHANICAL_HOLD: extension protocol blob drift")
    if git_blob_sha(surface_path) != SURFACE_BLOB_SHA:
        raise SystemExit("MECHANICAL_HOLD: original surface protocol blob drift")
    if git_blob_sha(relaxation_path) != RELAXATION_BLOB_SHA:
        raise SystemExit("MECHANICAL_HOLD: relaxation protocol blob drift")

    lineage = guard["lineage"]
    if lineage["original_surface_protocol"]["git_blob_sha"] != SURFACE_BLOB_SHA:
        raise SystemExit("MECHANICAL_HOLD: guard surface lineage mismatch")
    if lineage["layer_extension_protocol"]["git_blob_sha"] != EXTENSION_BLOB_SHA:
        raise SystemExit("MECHANICAL_HOLD: guard extension lineage mismatch")
    if lineage["relaxation_protocol"]["git_blob_sha"] != RELAXATION_BLOB_SHA:
        raise SystemExit("MECHANICAL_HOLD: guard relaxation lineage mismatch")

    tol = float(guard["coupled_endpoint_recheck"]["absolute_surface_excess_tolerance_ev_per_surface_atom"])
    if tol != 0.001:
        raise SystemExit("SCIENTIFIC_HOLD: coupled tolerance drift")
    if float(extension["frozen_numerical_settings"]["absolute_surface_excess_tolerance_ev_per_surface_atom"]) != tol:
        raise SystemExit("SCIENTIFIC_HOLD: extension/coupled tolerance mismatch")
    if float(surface["numerical_gate"]["absolute_surface_excess_tolerance_ev_per_surface_atom"]) != tol:
        raise SystemExit("SCIENTIFIC_HOLD: original/coupled tolerance mismatch")
    if surface["numerical_gate"]["joint_endpoint_recheck"]["required"] is not True:
        raise SystemExit("SCIENTIFIC_HOLD: original coupled recheck no longer required")
    if relaxation["entry_gate"]["required_status"] != "CLEAN_SURFACE_FIXED_GRID_PASS":
        raise SystemExit("SCIENTIFIC_HOLD: relaxation entry gate drift")

    coupled = guard["coupled_endpoint_recheck"]
    if coupled["base_point"] != {"layers": "FROM_LAYER_EXTENSION_SELECTION", "total_vacuum_angstrom": 15.0, "kmesh": [16, 16, 1]}:
        raise SystemExit("SCIENTIFIC_HOLD: coupled base-point drift")
    endpoints = coupled["one_axis_endpoint_substitutions"]
    if endpoints["kmesh"] != {"layers": "FROM_LAYER_EXTENSION_SELECTION", "total_vacuum_angstrom": 15.0, "kmesh": [20, 20, 1]}:
        raise SystemExit("SCIENTIFIC_HOLD: kmesh endpoint drift")
    if endpoints["vacuum"] != {"layers": "FROM_LAYER_EXTENSION_SELECTION", "total_vacuum_angstrom": 25.0, "kmesh": [16, 16, 1]}:
        raise SystemExit("SCIENTIFIC_HOLD: vacuum endpoint drift")
    if endpoints["layers"] != {"layers": 19, "total_vacuum_angstrom": 15.0, "kmesh": [16, 16, 1]}:
        raise SystemExit("SCIENTIFIC_HOLD: layer endpoint drift")
    if coupled["pass_status"] != "CLEAN_SURFACE_FIXED_GRID_PASS" or coupled["hold_status"] != "CLEAN_SURFACE_COUPLED_CONVERGENCE_HOLD":
        raise SystemExit("SCIENTIFIC_HOLD: coupled decision labels drift")
    if any(bool(v) for v in guard["frozen_controls"].values()):
        raise SystemExit("SCIENTIFIC_HOLD: guard reports scientific-control drift")
    if any(bool(v) for v in extension["evidence_firewall"].values()):
        raise SystemExit("SCIENTIFIC_HOLD: extension evidence firewall opened")
    if any(bool(v) for v in surface["evidence_firewall"].values()):
        raise SystemExit("SCIENTIFIC_HOLD: surface evidence firewall opened")

    return guard, extension, surface, relaxation


def validate_extension_pass(result_path: Path, extension_path: Path, extension: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    result = load(result_path)
    if result.get("schema") != RESULT_SCHEMA or result.get("status") != PASS_STATUS:
        raise SystemExit("SCIENTIFIC_HOLD: coupled recheck requires a valid layer-extension PASS")
    if result.get("protocol_sha256") != sha256(extension_path):
        raise SystemExit("MECHANICAL_HOLD: extension result protocol provenance mismatch")
    if result.get("scientific_settings_changed") is not False or result.get("thresholds_changed") is not False:
        raise SystemExit("SCIENTIFIC_HOLD: extension result reports scientific drift")
    if result.get("kinetic_inputs_used") is not False or result.get("chi_used") is not False or result.get("paid_compute_used") is not False:
        raise SystemExit("SCIENTIFIC_HOLD: prohibited evidence or compute route entered extension result")

    expected = extension["extension_batch"]["combined_ladder"]
    rows = result.get("combined_layers")
    if not isinstance(rows, list) or [int(r["layers"]) for r in rows] != expected:
        raise SystemExit("MECHANICAL_HOLD: extension PASS ladder incomplete or reordered")
    if int(result.get("terminal_reference_layers", 0)) != 19:
        raise SystemExit("SCIENTIFIC_HOLD: extension terminal endpoint drift")
    if float(result.get("tolerance_ev_per_surface_atom")) != 0.001:
        raise SystemExit("SCIENTIFIC_HOLD: extension result tolerance drift")

    selected = result.get("selected_layers")
    if not isinstance(selected, int) or selected < 7 or selected >= 19:
        raise SystemExit("SCIENTIFIC_HOLD: invalid selected non-terminal layer")
    base_row = next((r for r in rows if int(r["layers"]) == selected), None)
    terminal_row = next((r for r in rows if int(r["layers"]) == 19), None)
    if base_row is None or terminal_row is None:
        raise SystemExit("MECHANICAL_HOLD: selected or terminal layer evidence missing")
    for label, row in (("base", base_row), ("terminal", terminal_row)):
        value = float(row["surface_excess_ev_per_surface_atom"])
        if not math.isfinite(value):
            raise SystemExit(f"MECHANICAL_HOLD: non-finite {label} surface excess")
    return result, base_row, terminal_row


def runtime_contract(extension: dict[str, Any], pw: Path, pseudo_dir: Path) -> None:
    ext.verify_runtime(extension, pw, pseudo_dir)


def run_endpoint(args) -> None:
    gp = Path(args.guard).resolve()
    ep = Path(args.extension_protocol).resolve()
    sp = Path(args.surface_protocol).resolve()
    rp = Path(args.relaxation_protocol).resolve()
    xp = Path(args.extension_result).resolve()
    guard, extension, _, _ = static_contract(gp, ep, sp, rp)
    extension_result, base_row, _ = validate_extension_pass(xp, ep, extension)

    endpoint = args.endpoint
    if endpoint not in ("kmesh", "vacuum"):
        raise SystemExit("MECHANICAL_HOLD: endpoint must be kmesh or vacuum")

    selected = int(extension_result["selected_layers"])
    cfg = guard["coupled_endpoint_recheck"]["one_axis_endpoint_substitutions"][endpoint]
    layers = selected
    vacuum = float(cfg["total_vacuum_angstrom"])
    kmesh = tuple(int(x) for x in cfg["kmesh"])

    f = extension["frozen_numerical_settings"]
    pw = Path(args.pw).resolve()
    pseudo_dir = Path(args.pseudo_dir).resolve()
    runtime_contract(extension, pw, pseudo_dir)

    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    tag = f"coupled_{endpoint}_L{layers}_V{vacuum:g}_K{kmesh[0]}_{kmesh[1]}_{kmesh[2]}"
    text = base.slab_input(
        float(f["a_angstrom"]), float(f["c_angstrom"]), layers, vacuum,
        int(f["ecutwfc_ry"]), int(f["ecutrho_ry"]), kmesh,
        pseudo_dir, "__OUTDIR__", tag
    )
    row = base.execute_qe(out, pw, text, COUPLED_TIMEOUT_SECONDS, tag)
    gamma = (float(row["energy_ev"]) - layers * float(f["bulk_energy_ev_per_atom"])) / 2.0
    cell_z, _ = base.slab_geometry(float(f["a_angstrom"]), float(f["c_angstrom"]), layers, vacuum)
    row.update({
        "schema": "h-ru0001-coupled-endpoint-case-v0.1",
        "status": "VALID_COUPLED_ENDPOINT",
        "endpoint": endpoint,
        "layers": layers,
        "surface_excess_ev_per_surface_atom": gamma,
        "base_surface_excess_ev_per_surface_atom": float(base_row["surface_excess_ev_per_surface_atom"]),
        "total_vacuum_angstrom": vacuum,
        "cell_z_angstrom": cell_z,
        "kmesh": list(kmesh),
        "ecutwfc_ry": int(f["ecutwfc_ry"]),
        "ecutrho_ry": int(f["ecutrho_ry"]),
        "guard_git_blob_sha": git_blob_sha(gp),
        "extension_protocol_sha256": sha256(ep),
        "extension_result_sha256": sha256(xp),
        "mechanical_timeout_seconds": COUPLED_TIMEOUT_SECONDS,
        "scientific_settings_changed": False,
        "thresholds_changed": False,
        "kinetic_inputs_used": False,
        "chi_used": False,
        "paid_compute_used": False
    })
    path = out / f"SYSTEM3_COUPLED_{endpoint.upper()}_RESULT.json"
    write(path, row)
    print(json.dumps(row, indent=2, sort_keys=True))
    print(f"SYSTEM3_COUPLED_{endpoint.upper()}_VALID")


def adjudicate_values(base_gamma: float, k_gamma: float, v_gamma: float, l_gamma: float, tol: float) -> tuple[bool, dict[str, float]]:
    deltas = {
        "kmesh": abs(k_gamma - base_gamma),
        "vacuum": abs(v_gamma - base_gamma),
        "layers": abs(l_gamma - base_gamma),
    }
    return all(value <= tol for value in deltas.values()), deltas


def adjudicate(args) -> None:
    gp = Path(args.guard).resolve()
    ep = Path(args.extension_protocol).resolve()
    sp = Path(args.surface_protocol).resolve()
    rp = Path(args.relaxation_protocol).resolve()
    xp = Path(args.extension_result).resolve()
    guard, extension, _, _ = static_contract(gp, ep, sp, rp)
    extension_result, base_row, terminal_row = validate_extension_pass(xp, ep, extension)

    root = Path(args.results_root).resolve()
    endpoints: dict[str, dict[str, Any]] = {}
    for endpoint in ("kmesh", "vacuum"):
        hits = list(root.rglob(f"SYSTEM3_COUPLED_{endpoint.upper()}_RESULT.json"))
        if len(hits) != 1:
            raise SystemExit(f"MECHANICAL_HOLD: expected one {endpoint} coupled result, found {len(hits)}")
        row = load(hits[0])
        if row.get("status") != "VALID_COUPLED_ENDPOINT" or row.get("endpoint") != endpoint:
            raise SystemExit(f"MECHANICAL_HOLD: {endpoint} coupled result identity mismatch")
        if row.get("guard_git_blob_sha") != git_blob_sha(gp):
            raise SystemExit(f"MECHANICAL_HOLD: {endpoint} guard provenance mismatch")
        if row.get("extension_protocol_sha256") != sha256(ep) or row.get("extension_result_sha256") != sha256(xp):
            raise SystemExit(f"MECHANICAL_HOLD: {endpoint} extension provenance mismatch")
        if row.get("scientific_settings_changed") is not False or row.get("thresholds_changed") is not False:
            raise SystemExit(f"SCIENTIFIC_HOLD: {endpoint} reports scientific drift")
        if row.get("kinetic_inputs_used") is not False or row.get("chi_used") is not False or row.get("paid_compute_used") is not False:
            raise SystemExit(f"SCIENTIFIC_HOLD: {endpoint} evidence firewall violation")
        endpoints[endpoint] = row

    base_gamma = float(base_row["surface_excess_ev_per_surface_atom"])
    l19_gamma = float(terminal_row["surface_excess_ev_per_surface_atom"])
    tol = float(guard["coupled_endpoint_recheck"]["absolute_surface_excess_tolerance_ev_per_surface_atom"])
    passed, deltas = adjudicate_values(
        base_gamma,
        float(endpoints["kmesh"]["surface_excess_ev_per_surface_atom"]),
        float(endpoints["vacuum"]["surface_excess_ev_per_surface_atom"]),
        l19_gamma,
        tol,
    )
    coupled = guard["coupled_endpoint_recheck"]
    result = {
        "schema": "h-ru0001-post-extension-coupled-recheck-result-v0.1",
        "status": coupled["pass_status"] if passed else coupled["hold_status"],
        "next_gate": coupled["pass_next_gate"] if passed else None,
        "selected_layers": int(extension_result["selected_layers"]),
        "base_surface_excess_ev_per_surface_atom": base_gamma,
        "endpoint_surface_excess_ev_per_surface_atom": {
            "kmesh": float(endpoints["kmesh"]["surface_excess_ev_per_surface_atom"]),
            "vacuum": float(endpoints["vacuum"]["surface_excess_ev_per_surface_atom"]),
            "layers": l19_gamma,
        },
        "absolute_deltas_ev_per_surface_atom": deltas,
        "tolerance_ev_per_surface_atom": tol,
        "all_endpoints_within_tolerance": passed,
        "extension_result_sha256": sha256(xp),
        "guard_git_blob_sha": git_blob_sha(gp),
        "extension_protocol_sha256": sha256(ep),
        "direct_relaxation_before_this_adjudication_forbidden": True,
        "scientific_settings_changed": False,
        "thresholds_changed": False,
        "kinetic_inputs_used": False,
        "chi_used": False,
        "paid_compute_used": False,
    }
    write(args.out, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    print(result["status"])


def self_test(args) -> None:
    gp = Path(args.guard).resolve()
    ep = Path(args.extension_protocol).resolve()
    sp = Path(args.surface_protocol).resolve()
    rp = Path(args.relaxation_protocol).resolve()
    guard, extension, _, relaxation = static_contract(gp, ep, sp, rp)
    assert extension["decision"]["pass_status"] == PASS_STATUS
    assert guard["decision_routing"]["if_layer_extension_pass"]["direct_relaxation_entry_forbidden"] is True
    assert relaxation["entry_gate"]["required_status"] == "CLEAN_SURFACE_FIXED_GRID_PASS"
    passed, deltas = adjudicate_values(1.0, 1.0004, 0.9993, 1.0008, 0.001)
    assert passed and max(deltas.values()) <= 0.001
    failed, deltas2 = adjudicate_values(1.0, 1.0004, 0.9988, 1.0008, 0.001)
    assert not failed and deltas2["vacuum"] > 0.001
    print("SYSTEM3_POST_EXTENSION_COUPLED_RECHECK_SELF_TEST_PASS")
    print("TOLERANCE_EV_PER_SURFACE_ATOM=0.001")
    print("ENDPOINTS=K20,V25,L19")
    print("DIRECT_RELAXATION_FORBIDDEN_UNTIL_CLEAN_SURFACE_FIXED_GRID_PASS=true")


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--guard", required=True)
    common.add_argument("--extension-protocol", required=True)
    common.add_argument("--surface-protocol", required=True)
    common.add_argument("--relaxation-protocol", required=True)

    x = sub.add_parser("self-test", parents=[common])
    x.set_defaults(func=self_test)

    x = sub.add_parser("run-endpoint", parents=[common])
    x.add_argument("--extension-result", required=True)
    x.add_argument("--endpoint", choices=["kmesh", "vacuum"], required=True)
    x.add_argument("--pw", required=True)
    x.add_argument("--pseudo-dir", required=True)
    x.add_argument("--out", required=True)
    x.set_defaults(func=run_endpoint)

    x = sub.add_parser("adjudicate", parents=[common])
    x.add_argument("--extension-result", required=True)
    x.add_argument("--results-root", required=True)
    x.add_argument("--out", required=True)
    x.set_defaults(func=adjudicate)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
