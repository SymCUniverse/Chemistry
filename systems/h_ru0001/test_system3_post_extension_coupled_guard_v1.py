#!/usr/bin/env python3
"""Fail-closed validator for the System 3 H/Ru(0001) post-extension gate.

This test preserves the original frozen numerical progression:
layer-extension PASS -> coupled endpoint recheck -> CLEAN_SURFACE_FIXED_GRID_PASS
-> relaxation. It does not adjudicate any scientific result.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

SURFACE_PATH = ROOT / "SYSTEM3_CLEAN_RU0001_SURFACE_PROTOCOL_v0.2.json"
EXTENSION_PATH = ROOT / "SYSTEM3_CLEAN_RU0001_LAYER_EXTENSION_PROTOCOL_v0.3.json"
RELAXATION_PATH = ROOT / "SYSTEM3_CLEAN_RU0001_RELAXATION_PROTOCOL_v0.1.json"
GUARD_PATH = ROOT / "SYSTEM3_POST_EXTENSION_COUPLED_GATE_GUARD_v0.1.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    framed = f"blob {len(data)}\0".encode("ascii") + data
    return hashlib.sha1(framed).hexdigest()


def main() -> None:
    surface = load(SURFACE_PATH)
    extension = load(EXTENSION_PATH)
    relaxation = load(RELAXATION_PATH)
    guard = load(GUARD_PATH)

    # The guard must bind the exact frozen source documents it claims to preserve.
    assert git_blob_sha(SURFACE_PATH) == guard["lineage"]["original_surface_protocol"]["git_blob_sha"]
    assert git_blob_sha(EXTENSION_PATH) == guard["lineage"]["layer_extension_protocol"]["git_blob_sha"]
    assert git_blob_sha(RELAXATION_PATH) == guard["lineage"]["relaxation_protocol"]["git_blob_sha"]

    # Original surface protocol requires the coupled endpoint recheck.
    joint = surface["numerical_gate"]["joint_endpoint_recheck"]
    assert joint["required"] is True
    assert surface["decision"]["pass_status"] == "CLEAN_SURFACE_FIXED_GRID_PASS"
    assert surface["decision"]["coupled_hold_status"] == "CLEAN_SURFACE_COUPLED_CONVERGENCE_HOLD"

    # Layer-extension PASS is only an intermediate state, never the relaxation entry state.
    assert extension["decision"]["pass_status"] == "CLEAN_SURFACE_LAYER_EXTENSION_PASS"
    assert extension["decision"]["pass_status"] != surface["decision"]["pass_status"]
    pass_route = guard["decision_routing"]["if_layer_extension_pass"]
    assert pass_route["required_action"] == "RUN_COUPLED_ENDPOINT_RECHECK_BEFORE_RELAXATION"
    assert pass_route["extension_pass_is_not_clean_surface_fixed_grid_pass"] is True
    assert pass_route["direct_relaxation_entry_forbidden"] is True

    # Relaxation remains fail-closed on the original fixed-grid PASS.
    assert relaxation["entry_gate"]["required_status"] == "CLEAN_SURFACE_FIXED_GRID_PASS"
    assert guard["lineage"]["relaxation_protocol"]["required_entry_status"] == "CLEAN_SURFACE_FIXED_GRID_PASS"

    # The same frozen 1 meV/surface-atom acceptance criterion must survive every gate.
    surface_tol = surface["numerical_gate"]["absolute_surface_excess_tolerance_ev_per_surface_atom"]
    extension_tol = extension["frozen_numerical_settings"]["absolute_surface_excess_tolerance_ev_per_surface_atom"]
    guard_tol = guard["coupled_endpoint_recheck"]["absolute_surface_excess_tolerance_ev_per_surface_atom"]
    assert surface_tol == extension_tol == guard_tol == 0.001

    # Coupled endpoint substitutions must remain exactly the original terminal endpoints.
    coupled = guard["coupled_endpoint_recheck"]
    assert coupled["required"] is True
    assert coupled["base_point"]["layers"] == "FROM_LAYER_EXTENSION_SELECTION"
    assert coupled["base_point"]["total_vacuum_angstrom"] == 15.0
    assert coupled["base_point"]["kmesh"] == [16, 16, 1]
    endpoints = coupled["one_axis_endpoint_substitutions"]
    assert endpoints["kmesh"]["kmesh"] == [20, 20, 1]
    assert endpoints["kmesh"]["total_vacuum_angstrom"] == 15.0
    assert endpoints["vacuum"]["total_vacuum_angstrom"] == 25.0
    assert endpoints["vacuum"]["kmesh"] == [16, 16, 1]
    assert endpoints["layers"]["layers"] == 19
    assert endpoints["layers"]["total_vacuum_angstrom"] == 15.0
    assert endpoints["layers"]["kmesh"] == [16, 16, 1]
    assert coupled["pass_status"] == "CLEAN_SURFACE_FIXED_GRID_PASS"
    assert coupled["hold_status"] == "CLEAN_SURFACE_COUPLED_CONVERGENCE_HOLD"

    # A scientific HOLD continues the same preauthorized odd-layer ladder, without retuning.
    hold_route = guard["decision_routing"]["if_layer_extension_hold"]
    assert hold_route["required_action"] == "FOLLOW_PREAUTHORIZED_NEXT_ODD_LAYER_BATCH_AFTER_NEW_HASH_BINDING"
    assert hold_route["registered_next_batch"] == [21, 23, 25]
    assert hold_route["user_reauthorization_required_for_same_rule"] is False
    assert extension["decision"]["next_batch_if_hold"] == [21, 23, 25]
    assert extension["decision"]["new_hash_binding_required_before_next_batch_compute"] is True
    assert extension["decision"]["threshold_retuning_allowed"] is False

    # Preserve all evidence firewalls and record that the guard changed no scientific control.
    assert all(value is False for value in surface["evidence_firewall"].values())
    assert all(value is False for value in extension["evidence_firewall"].values())
    assert all(value is False for value in guard["frozen_controls"].values())
    assert guard["audit_finding"]["scientific_acceptance_rule_changed"] is False
    assert guard["audit_finding"]["threshold_changed"] is False

    print("PASS: System3 post-extension coupled-gate lineage is fail-closed and unchanged.")


if __name__ == "__main__":
    main()
