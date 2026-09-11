#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_json(rel: str):
    with (ROOT / rel).open("r", encoding="utf-8") as f:
        return json.load(f)


def text(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def git_blob_sha(rel: str) -> str:
    data = (ROOT / rel).read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


adopt = load_json("governance/CHEMISTRY_GENERAL_PROTOCOL_v0.7.1A_ADOPTION_v0.1.json")
assert adopt["status"] == "ACTIVE_PROSPECTIVE_GOVERNANCE_MAPPING"
assert adopt["chemistry_phase_mapping"]["P0_Q"]["role"] == "controlled_qualification_and_model_iteration"
assert adopt["scientific_controls"]["threshold_retuning_from_observed_failure_allowed"] is False
assert adopt["scientific_controls"]["failed_gate_reclassification_allowed"] is False
assert adopt["current_lane_classification"]["H_Ru0001_post_hold_K20_K24_K28"]["may_directly_authorize_relaxation"] is False

state = load_json("systems/h_ru0001/SYSTEM3_STATE_LEDGER_v0.2.json")
assert state["branch"] == "personal-free-compute"
assert state["general_protocol_phase"] == "P0_Q"
surface = state["readiness"]["SURFACE_READY"]
assert surface["status"] == "HOLD"
assert surface["coupled_recheck"]["status"] == "CLEAN_SURFACE_COUPLED_CONVERGENCE_HOLD"
assert surface["coupled_recheck"]["failed_axis"] == "kmesh"
assert surface["coupled_recheck"]["relaxation_authorized"] is False
assert surface["post_hold_diagnostic"]["phase"] == "P0_Q"
assert surface["post_hold_diagnostic"]["may_rewrite_original_hold"] is False
assert surface["post_hold_diagnostic"]["may_authorize_relaxation"] is False

hold = load_json("systems/h_ru0001/SYSTEM3_POST_EXTENSION_COUPLED_HOLD_RECORD_v0.1.json")
assert hold["status"] == "CLEAN_SURFACE_COUPLED_CONVERGENCE_HOLD"
assert hold["classification"] == "SCIENTIFIC_NUMERICAL_HOLD_NOT_MECHANICAL_FAILURE"
assert hold["adjudication"]["failed_axis"] == "kmesh"
assert hold["adjudication"]["relaxation_entry_authorized"] is False
assert hold["interpretation"]["failure_may_not_be_reclassified_as_mechanical"] is True
assert hold["interpretation"]["threshold_retuning_allowed"] is False
assert abs(hold["absolute_deltas_ev_per_surface_atom"]["kmesh"] - 0.0024786851754470263) < 1e-15
assert abs(hold["absolute_deltas_ev_per_surface_atom"]["vacuum"] - 0.0000029932525649201125) < 1e-18
assert abs(hold["absolute_deltas_ev_per_surface_atom"]["layers"] - 0.0003073526058869902) < 1e-15

kp = load_json("systems/h_ru0001/SYSTEM3_POST_HOLD_KMESH_DIAGNOSTIC_PROTOCOL_v0.1.json")
assert kp["status"] == "FROZEN_BEFORE_POST_HOLD_K24_K28_RESULTS"
assert kp["frozen_scientific_settings"]["kmesh_ladder"] == [[20, 20, 1], [24, 24, 1], [28, 28, 1]]
assert kp["frozen_scientific_settings"]["terminal_reference"] == [28, 28, 1]
assert kp["frozen_scientific_settings"]["absolute_surface_excess_tolerance_ev_per_surface_atom"] == 0.001
fw = kp["promotion_firewall"]
assert fw["original_coupled_hold_remains_historical_fact"] is True
assert fw["diagnostic_may_directly_emit_CLEAN_SURFACE_FIXED_GRID_PASS"] is False
assert fw["diagnostic_may_authorize_relaxation"] is False
assert fw["threshold_retuning_allowed"] is False

preflight = load_json("systems/h_ru0001/SYSTEM3_REPRODUCIBILITY_PREFLIGHT_v0.1.json")
assert preflight["status"] == "PRE_RECONCILIATION_PACKAGE_PREP_COMPLETE_PENDING_COMPUTE_DEPENDENT_EVIDENCE"
assert preflight["current_evidence_inventory"]["coupled_recheck"]["run_id"] == 34535678952
assert preflight["current_evidence_inventory"]["post_hold_kmesh_diagnostic"]["run_id"] == 34560002560
assert preflight["final_assembly_firewalls"]["historical_HOLDs_must_ship"] is True
assert preflight["final_assembly_firewalls"]["raw_outputs_override_summaries_in_conflict"] is True

manuscript = text("systems/h_ru0001/SYSTEM3_MANUSCRIPT_INTEGRATION_v0.2.md")
for required in (
    "CLEAN_SURFACE_COUPLED_CONVERGENCE_HOLD",
    "P0-Q",
    "Function Map",
    "Limit Map",
    "cannot retroactively relabel the original candidate",
):
    assert required in manuscript, required

closeout = text("systems/h_ru0001/SYSTEM3_PRE_RECONCILIATION_CLOSEOUT_v0.1.md")
assert "NON_COMPUTE_PRE_RECONCILIATION_WORK_CLOSED" in closeout
assert "K24 and K28" in closeout
assert "Do not loosen the 1 meV threshold" in closeout

quantum = text("systems/h_ru0001/SYSTEM3_QUANTUM_IMPLEMENTATION_READINESS_AUDIT_v0.1.md")
assert "PRODUCTION_PIMD_AUTHORIZED = false" in quantum
assert "VERSION_DEPENDENT_AND_MUST_BE_QUALIFIED" in quantum

diss = text("systems/h_ru0001/SYSTEM3_DISSIPATION_COORDINATE_LITERATURE_AUDIT_v0.1.md")
assert "DISSIPATION_NOT_ESTABLISHED" in diss
assert "NO_QUALIFIED_INDEPENDENT_COORDINATE_MATCHED_H_RU0001_DIFFUSION_FRICTION_SOURCE_IDENTIFIED_IN_CURRENT_PUBLIC_SEARCH" in diss

decisions = load_json("governance/PROGRAM_DECISION_LEDGER_ADDENDUM_2026-09-11.json")
ids = [row["id"] for row in decisions["entries"]]
assert len(ids) == len(set(ids))
assert ids == [f"DEC-2026-09-11-{n:03d}" for n in range(15, 22)]

assert git_blob_sha("systems/co_cu111/kaggle/FRESH_SESSION_BOOTSTRAP_v1.sh") == "a8a8abf8703a121a9d6ebfe4dcfbd609658c28ba"
assert git_blob_sha("systems/co_cu111/kaggle/FRESH_SESSION_L19_v1.sh") == "9b60ed51b22ad975b213866253e4eb306d17dea1"

status = text("PROGRAM_CLOSURE_STATUS_2026-09-11.md")
assert "K16 to K20 delta = 0.0024786851754470263" in status
assert "No live Kaggle status is claimed here" in status
assert "Everything else listed in the pre-reconciliation closeout has been removed from the current waiting backlog" in status

print("PRE_RECONCILIATION_CLOSEOUT_VALIDATION_PASS")
print("H_RU_ORIGINAL_COUPLED_HOLD_PRESERVED=true")
print("RELAXATION_AUTHORIZED=false")
print("CURRENT_PHASE=P0_Q")
print("CO_CU_LAUNCHER_BLOBS_UNCHANGED=true")
