#!/usr/bin/env python3
from __future__ import annotations

import argparse, hashlib, json, math, sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import system3_clean_ru0001_numerical_v1 as base

PROTOCOL_BLOB_SHA = "b943664b17abaef3c478cffbf66b1600c558a09f"
HOLD_BLOB_SHA = "5f975b604eda3942eef87d215fb1eaf096f17cef"
SURFACE_BLOB_SHA = "e865b27f9a2455f6902eb27ca59d3274f0808902"
GUARD_BLOB_SHA = "e2a4c743fa097f3a04d7a29708c6e0cf10b29d81"
# Mechanical wall-clock allowance only. The 2026-09-11 K24/K28 attempt
# reached the previous 14,400 s cap with no final energy or JOB DONE.
# No scientific setting, threshold, evidence firewall, or interpretation is
# changed by increasing this execution allowance.
TIMEOUT_SECONDS = 19800


def load(path: str | Path) -> dict[str, Any]:
    row = json.loads(Path(path).read_text())
    if not isinstance(row, dict):
        raise SystemExit(f"MECHANICAL_HOLD: JSON object required: {path}")
    return row


def write(path: str | Path, row: dict[str, Any]) -> None:
    p = Path(path); p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(row, indent=2, sort_keys=True) + "\n")


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def contract(protocol_path: Path, hold_path: Path, surface_path: Path, guard_path: Path):
    protocol, hold, surface, guard = map(load, [protocol_path, hold_path, surface_path, guard_path])
    expected = [(protocol_path, PROTOCOL_BLOB_SHA), (hold_path, HOLD_BLOB_SHA), (surface_path, SURFACE_BLOB_SHA), (guard_path, GUARD_BLOB_SHA)]
    for path, blob in expected:
        if git_blob_sha(path) != blob:
            raise SystemExit(f"MECHANICAL_HOLD: frozen blob drift: {path.name}")
    if hold.get("status") != "CLEAN_SURFACE_COUPLED_CONVERGENCE_HOLD":
        raise SystemExit("SCIENTIFIC_HOLD: diagnostic requires preserved coupled HOLD")
    if hold.get("adjudication", {}).get("failed_axis") != "kmesh":
        raise SystemExit("SCIENTIFIC_HOLD: source HOLD is not kmesh-specific")
    if guard["coupled_endpoint_recheck"]["hold_status"] != "CLEAN_SURFACE_COUPLED_CONVERGENCE_HOLD":
        raise SystemExit("SCIENTIFIC_HOLD: guard decision drift")
    s = protocol["frozen_scientific_settings"]
    if s["kmesh_ladder"] != [[20,20,1],[24,24,1],[28,28,1]] or s["terminal_reference"] != [28,28,1]:
        raise SystemExit("SCIENTIFIC_HOLD: diagnostic ladder drift")
    if float(s["absolute_surface_excess_tolerance_ev_per_surface_atom"]) != 0.001:
        raise SystemExit("SCIENTIFIC_HOLD: tolerance drift")
    fw = protocol["promotion_firewall"]
    if fw["diagnostic_may_directly_emit_CLEAN_SURFACE_FIXED_GRID_PASS"] or fw["diagnostic_may_authorize_relaxation"]:
        raise SystemExit("SCIENTIFIC_HOLD: promotion firewall opened")
    if fw["threshold_retuning_allowed"] or fw["scientific_settings_changed"] or fw["published_H_Ru_kinetics_or_barriers_used"] or fw["chi_used"] or fw["System2_outcomes_used"] or fw["paid_compute_used"]:
        raise SystemExit("SCIENTIFIC_HOLD: evidence/science firewall opened")
    if surface["relaxation_gate"]["required_after_numerical_pass"] is not True:
        raise SystemExit("SCIENTIFIC_HOLD: original relaxation gate drift")
    return protocol, hold


def run_case(args):
    pp, hp, sp, gp = map(lambda x: Path(x).resolve(), [args.protocol, args.hold, args.surface_protocol, args.guard])
    protocol, hold = contract(pp, hp, sp, gp)
    k = int(args.kmesh)
    if k not in (24, 28):
        raise SystemExit("MECHANICAL_HOLD: only predeclared K24 or K28 is allowed")
    s = protocol["frozen_scientific_settings"]
    pw = Path(args.pw).resolve(); pseudo = Path(args.pseudo_dir).resolve()
    if not pw.is_file() or not (pseudo / "Ru.nc.pbe.z_16.oncvpsp4.sg15.v0.upf").is_file():
        raise SystemExit("MECHANICAL_HOLD: exact runtime/pseudopotential files missing")
    out = Path(args.out).resolve(); out.mkdir(parents=True, exist_ok=True)
    tag = f"post_hold_kmesh_L17_V15_K{k}"
    text = base.slab_input(float(s["a_angstrom"]), float(s["c_angstrom"]), int(s["layers"]), float(s["total_vacuum_angstrom"]), int(s["ecutwfc_ry"]), int(s["ecutrho_ry"]), (k,k,1), pseudo, "__OUTDIR__", tag)
    row = base.execute_qe(out, pw, text, TIMEOUT_SECONDS, tag)
    gamma = (float(row["energy_ev"]) - int(s["layers"]) * float(s["bulk_energy_ev_per_atom"])) / 2.0
    row.update({
        "schema": "h-ru0001-post-hold-kmesh-diagnostic-case-v0.1",
        "status": "VALID_POST_HOLD_KMESH_DIAGNOSTIC_CASE",
        "layers": int(s["layers"]), "total_vacuum_angstrom": float(s["total_vacuum_angstrom"]), "kmesh": [k,k,1],
        "surface_excess_ev_per_surface_atom": gamma,
        "protocol_git_blob_sha": git_blob_sha(pp), "hold_git_blob_sha": git_blob_sha(hp),
        "original_hold_preserved": True, "relaxation_authorized": False,
        "scientific_settings_changed": False, "thresholds_changed": False,
        "chi_used": False, "kinetic_inputs_used": False, "paid_compute_used": False,
        "mechanical_timeout_seconds": TIMEOUT_SECONDS
    })
    write(out / f"SYSTEM3_POST_HOLD_K{k}_RESULT.json", row)
    print(json.dumps(row, indent=2, sort_keys=True)); print(f"SYSTEM3_POST_HOLD_K{k}_VALID")


def adjudicate(args):
    pp, hp, sp, gp = map(lambda x: Path(x).resolve(), [args.protocol, args.hold, args.surface_protocol, args.guard])
    protocol, hold = contract(pp, hp, sp, gp)
    root = Path(args.results_root).resolve()
    vals = {20: float(hold["measured_surface_excess_ev_per_surface_atom"]["kmesh_L17_V15_K20"])}
    for k in (24, 28):
        hits = list(root.rglob(f"SYSTEM3_POST_HOLD_K{k}_RESULT.json"))
        if len(hits) != 1:
            raise SystemExit(f"MECHANICAL_HOLD: expected one K{k} result, found {len(hits)}")
        row = load(hits[0])
        if row.get("status") != "VALID_POST_HOLD_KMESH_DIAGNOSTIC_CASE" or row.get("kmesh") != [k,k,1]:
            raise SystemExit(f"MECHANICAL_HOLD: K{k} identity mismatch")
        if row.get("protocol_git_blob_sha") != git_blob_sha(pp) or row.get("hold_git_blob_sha") != git_blob_sha(hp):
            raise SystemExit(f"MECHANICAL_HOLD: K{k} provenance mismatch")
        vals[k] = float(row["surface_excess_ev_per_surface_atom"])
    if not all(math.isfinite(v) for v in vals.values()):
        raise SystemExit("MECHANICAL_HOLD: non-finite diagnostic value")
    tol = float(protocol["frozen_scientific_settings"]["absolute_surface_excess_tolerance_ev_per_surface_atom"])
    deltas = {"K20_vs_K28": abs(vals[20]-vals[28]), "K24_vs_K28": abs(vals[24]-vals[28])}
    converged = all(v <= tol for v in deltas.values())
    result = {
        "schema": "h-ru0001-post-hold-kmesh-diagnostic-result-v0.1",
        "status": protocol["decision_labels"]["converged"] if converged else protocol["decision_labels"]["not_converged"],
        "surface_excess_ev_per_surface_atom": {f"K{k}": vals[k] for k in (20,24,28)},
        "absolute_deltas_ev_per_surface_atom": deltas,
        "tolerance_ev_per_surface_atom": tol,
        "original_coupled_hold_preserved": True,
        "CLEAN_SURFACE_FIXED_GRID_PASS_emitted": False,
        "relaxation_authorized": False,
        "successor_protocol_required_before_any_production_promotion": True,
        "scientific_settings_changed": False, "thresholds_changed": False,
        "chi_used": False, "kinetic_inputs_used": False, "paid_compute_used": False,
        "protocol_sha256": sha256(pp), "hold_sha256": sha256(hp)
    }
    write(args.out, result); print(json.dumps(result, indent=2, sort_keys=True)); print(result["status"])


def self_test(args):
    pp, hp, sp, gp = map(lambda x: Path(x).resolve(), [args.protocol, args.hold, args.surface_protocol, args.guard])
    protocol, hold = contract(pp, hp, sp, gp)
    assert protocol["promotion_firewall"]["original_coupled_hold_remains_historical_fact"] is True
    assert hold["adjudication"]["relaxation_entry_authorized"] is False
    assert TIMEOUT_SECONDS == 19800
    print("SYSTEM3_POST_HOLD_KMESH_DIAGNOSTIC_SELF_TEST_PASS")
    print("LADDER=K20,K24,K28")
    print("ORIGINAL_COUPLED_HOLD_PRESERVED=true")
    print("RELAXATION_AUTHORIZED=false")
    print("MECHANICAL_TIMEOUT_SECONDS=19800")


def main():
    ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest="cmd", required=True)
    common = argparse.ArgumentParser(add_help=False)
    for name in ["protocol","hold","surface-protocol","guard"]:
        common.add_argument("--"+name, required=True)
    x=sub.add_parser("self-test", parents=[common]); x.set_defaults(func=self_test)
    x=sub.add_parser("run-case", parents=[common]); x.add_argument("--kmesh", type=int, required=True); x.add_argument("--pw", required=True); x.add_argument("--pseudo-dir", required=True); x.add_argument("--out", required=True); x.set_defaults(func=run_case)
    x=sub.add_parser("adjudicate", parents=[common]); x.add_argument("--results-root", required=True); x.add_argument("--out", required=True); x.set_defaults(func=adjudicate)
    args=ap.parse_args(); args.func(args)

if __name__ == "__main__":
    main()