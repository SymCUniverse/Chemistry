#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

EVIDENCE_SCHEMA = "h-ru0001-successor-fixed-grid-pass-evidence-v0.1"
EVIDENCE_STATUS = "VALID_ADJUDICATED_P0_Q_SUCCESSOR_FIXED_GRID_PASS_EVIDENCE"
L21_SCHEMA = "h-ru0001-l19-contingency-l21-fresh-case-v0.1"
L21_STATUS = "VALID_FRESH_L21_CONTINGENCY_CASE"
OUT_SCHEMA = "h-ru0001-l17-foundational-robustness-result-v0.1"
TOL = 0.001
EXPECTED_RUN = 34769372617
EXPECTED_ARTIFACT = 10331758561
EXPECTED_ARTIFACT_DIGEST = "7052924a6f4d327ec035e0b569992d280a62618a3ccf6dec51e273d675c46ab6"
EXPECTED_SUCCESSOR_PROTOCOL_SHA256 = "ffe50f7cfe5dbf5ce8c19da2449c00067fc795d38a3abe695bb16a0c41a07f48"
EXPECTED_CONTINGENCY_PROTOCOL_SHA256 = "8bbe74e6345af5e28612db3804147a348ad826ee508ac677c77538bd7336f536"


def load(path: str | Path) -> dict[str, Any]:
    obj = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(obj, dict):
        raise SystemExit(f"MECHANICAL_HOLD: JSON object required: {path}")
    return obj


def dump(path: str | Path, obj: dict[str, Any]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def validate_evidence(e: dict[str, Any]) -> tuple[float, float]:
    if e.get("schema") != EVIDENCE_SCHEMA or e.get("status") != EVIDENCE_STATUS:
        raise SystemExit("MECHANICAL_HOLD: fixed-grid PASS evidence identity mismatch")
    src = e.get("source", {})
    if int(src.get("run_id", -1)) != EXPECTED_RUN or int(src.get("artifact_id", -1)) != EXPECTED_ARTIFACT:
        raise SystemExit("MECHANICAL_HOLD: fixed-grid source identity mismatch")
    if src.get("artifact_digest_sha256") != EXPECTED_ARTIFACT_DIGEST:
        raise SystemExit("MECHANICAL_HOLD: fixed-grid artifact digest mismatch")
    if src.get("successor_protocol_sha256") != EXPECTED_SUCCESSOR_PROTOCOL_SHA256:
        raise SystemExit("MECHANICAL_HOLD: successor protocol provenance mismatch")
    r = e.get("result", {})
    if r.get("status") != "CLEAN_SURFACE_FIXED_GRID_PASS":
        raise SystemExit("SCIENTIFIC_HOLD: foundational source is not the earned fixed-grid PASS")
    if int(r.get("selected_layers", 0)) != 17 or r.get("selected_surface_kmesh") != [24, 24, 1]:
        raise SystemExit("SCIENTIFIC_HOLD: selected L17/K24 foundation identity drift")
    if float(r.get("selected_total_vacuum_angstrom", 0.0)) != 15.0:
        raise SystemExit("SCIENTIFIC_HOLD: selected V15 foundation identity drift")
    if float(r.get("tolerance_ev_per_surface_atom", -1)) != TOL:
        raise SystemExit("SCIENTIFIC_HOLD: 1 meV tolerance drift")
    if r.get("all_four_cases_fresh") is not True or r.get("diagnostic_energies_reused_as_PASS_evidence") is not False:
        raise SystemExit("SCIENTIFIC_HOLD: fixed-grid evidence firewall drift")
    if r.get("original_K16_coupled_hold_preserved") is not True:
        raise SystemExit("SCIENTIFIC_HOLD: historical K16 HOLD was not preserved")
    vals = r.get("surface_excess_ev_per_surface_atom", {})
    g17 = float(vals["L17_V15_K24_base"])
    g19 = float(vals["L19_V15_K24_layers"])
    if not (math.isfinite(g17) and math.isfinite(g19)):
        raise SystemExit("MECHANICAL_HOLD: non-finite foundation energy")
    return g17, g19


def validate_l21(l21: dict[str, Any]) -> tuple[bool, str | None, float | None]:
    if l21.get("schema") != L21_SCHEMA or l21.get("status") != L21_STATUS:
        return False, "L21 result schema/status mismatch", None
    if l21.get("case") != "L21_terminal_reference":
        return False, "L21 case identity mismatch", None
    if int(l21.get("layers", 0)) != 21 or float(l21.get("total_vacuum_angstrom", 0.0)) != 15.0:
        return False, "L21 layer/vacuum identity mismatch", None
    if l21.get("kmesh") != [24, 24, 1]:
        return False, "L21 k-mesh identity mismatch", None
    if l21.get("job_done") is not True or int(l21.get("return_code", 1)) != 0 or l21.get("timeout") is not False:
        return False, "L21 did not complete as valid QE evidence", None
    if l21.get("fresh_after_contingency_freeze") is not True:
        return False, "L21 is not fresh after contingency freeze", None
    if l21.get("contingency_protocol_sha256") != EXPECTED_CONTINGENCY_PROTOCOL_SHA256:
        return False, "L21 contingency protocol provenance mismatch", None
    if l21.get("active_successor_protocol_sha256") != EXPECTED_SUCCESSOR_PROTOCOL_SHA256:
        return False, "L21 successor protocol provenance mismatch", None
    for key in ("scientific_settings_changed", "thresholds_changed", "kinetic_inputs_used", "chi_used", "paid_compute_used"):
        if l21.get(key) is not False:
            return False, f"L21 firewall violation: {key}", None
    try:
        gamma = float(l21["surface_excess_ev_per_surface_atom"])
    except (KeyError, TypeError, ValueError):
        return False, "L21 surface excess missing or non-numeric", None
    if not math.isfinite(gamma):
        return False, "L21 surface excess is non-finite", None
    return True, None, gamma


def adjudicate(e: dict[str, Any], l21: dict[str, Any]) -> dict[str, Any]:
    g17, g19 = validate_evidence(e)
    valid, why, g21 = validate_l21(l21)
    base = {
        "schema": OUT_SCHEMA,
        "system": "H/Ru(0001)",
        "phase": "P0_Q",
        "tolerance_ev_per_surface_atom": TOL,
        "minimum_fixed_grid_pass_preserved": True,
        "original_K16_coupled_hold_preserved": True,
        "thresholds_changed": False,
        "relaxation_was_used_to_rescue_gate": False,
        "automatic_deeper_layer_ladder_authorized": False,
        "source_fixed_grid_run_id": EXPECTED_RUN,
        "source_fixed_grid_artifact_id": EXPECTED_ARTIFACT,
    }
    if not valid or g21 is None:
        return {
            **base,
            "status": "INVALID_CHALLENGE",
            "reason": why,
            "relaxation_inheritance_authorized": False,
            "next_action": "Preserve the fixed-grid PASS, keep the foundational hold, and repair or explicitly disposition the bounded L21 challenge without changing its scientific criterion.",
        }
    d17 = abs(g21 - g17)
    d19 = abs(g21 - g19)
    p17 = d17 <= TOL
    p19 = d19 <= TOL
    status = "ROBUSTNESS_SUPPORTED" if p17 and p19 else "FOUNDATION_REOPENED"
    return {
        **base,
        "status": status,
        "surface_excess_ev_per_surface_atom": {"L17": g17, "L19": g19, "L21": g21},
        "absolute_deltas_ev_per_surface_atom": {"L17_to_L21": d17, "L19_to_L21": d19},
        "checks": {"L17_to_L21_within_tolerance": p17, "L19_to_L21_within_tolerance": p19},
        "relaxation_inheritance_authorized": bool(p17 and p19),
        "next_action": (
            "Enter the already-frozen clean-surface relaxation and reproduction gate; stop automatic layer-depth escalation."
            if p17 and p19
            else "Do not relax L17; reopen only the materially affected layer-depth foundation while preserving the earned minimum fixed-grid PASS and historical K16 HOLD."
        ),
    }


def self_test() -> None:
    evidence = {
        "schema": EVIDENCE_SCHEMA,
        "status": EVIDENCE_STATUS,
        "source": {
            "run_id": EXPECTED_RUN,
            "artifact_id": EXPECTED_ARTIFACT,
            "artifact_digest_sha256": EXPECTED_ARTIFACT_DIGEST,
            "successor_protocol_sha256": EXPECTED_SUCCESSOR_PROTOCOL_SHA256,
        },
        "result": {
            "status": "CLEAN_SURFACE_FIXED_GRID_PASS",
            "selected_layers": 17,
            "selected_total_vacuum_angstrom": 15.0,
            "selected_surface_kmesh": [24, 24, 1],
            "tolerance_ev_per_surface_atom": TOL,
            "all_four_cases_fresh": True,
            "diagnostic_energies_reused_as_PASS_evidence": False,
            "original_K16_coupled_hold_preserved": True,
            "surface_excess_ev_per_surface_atom": {
                "L17_V15_K24_base": 1.0,
                "L19_V15_K24_layers": 1.0002,
            },
        },
    }

    def l21(gamma: float) -> dict[str, Any]:
        return {
            "schema": L21_SCHEMA,
            "status": L21_STATUS,
            "case": "L21_terminal_reference",
            "layers": 21,
            "total_vacuum_angstrom": 15.0,
            "kmesh": [24, 24, 1],
            "job_done": True,
            "return_code": 0,
            "timeout": False,
            "fresh_after_contingency_freeze": True,
            "contingency_protocol_sha256": EXPECTED_CONTINGENCY_PROTOCOL_SHA256,
            "active_successor_protocol_sha256": EXPECTED_SUCCESSOR_PROTOCOL_SHA256,
            "scientific_settings_changed": False,
            "thresholds_changed": False,
            "kinetic_inputs_used": False,
            "chi_used": False,
            "paid_compute_used": False,
            "surface_excess_ev_per_surface_atom": gamma,
        }

    assert adjudicate(evidence, l21(1.0004))["status"] == "ROBUSTNESS_SUPPORTED"
    assert adjudicate(evidence, l21(1.0013))["status"] == "FOUNDATION_REOPENED"
    bad = l21(1.0004)
    bad["kmesh"] = [20, 20, 1]
    assert adjudicate(evidence, bad)["status"] == "INVALID_CHALLENGE"
    print("SYSTEM3_L17_FOUNDATIONAL_ROBUSTNESS_ADJUDICATOR_SELF_TEST_PASS")
    print("KNOWN_GOOD_PASS_TEST=true")
    print("KNOWN_BAD_FAILURE_TEST=true")
    print("INVALID_CHALLENGE_REFUSAL_TEST=true")
    print("TOLERANCE_EV_PER_SURFACE_ATOM=0.001")


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sp = sub.add_parser("self-test")
    sp.set_defaults(func=lambda _: self_test())
    sp = sub.add_parser("adjudicate")
    sp.add_argument("--evidence", required=True)
    sp.add_argument("--l21", required=True)
    sp.add_argument("--out", required=True)

    def run(args: argparse.Namespace) -> None:
        result = adjudicate(load(args.evidence), load(args.l21))
        dump(args.out, result)
        print(json.dumps(result, indent=2, sort_keys=True))
        print(result["status"])

    sp.set_defaults(func=run)
    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
