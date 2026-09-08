#!/usr/bin/env python3
"""Resilient Kaggle microcheckpoint wrapper for frozen L15-vs-L17 diagnostic.

Scientific inputs remain governed by SYSTEM2_PBE_L15_L17_SITE_DEPTH_DIAGNOSTIC_v0.2.json.
This wrapper changes only execution bookkeeping:
- the frozen QE input max_seconds=16200 is retained;
- an official QE prefix.EXIT clean-stop request is created after a short interval;
- clean EXIT-file stops are admitted as exact-restart checkpoints;
- more than six execution fragments are allowed because microsegments are not
  scientific protocol segments. A completed case is later materialized into the
  original segment-6 final-state shape for the unchanged adjudicator.
"""
from __future__ import annotations

import argparse
import copy
import json
import signal
import sys
import threading
import time
from pathlib import Path

CO_DIR = Path(__file__).resolve().parent.parent
if str(CO_DIR) not in sys.path:
    sys.path.insert(0, str(CO_DIR))

import pbe_l15_l17_site_depth_diagnostic_v2 as v2  # type: ignore

v1 = v2.v1
ORIGINAL_LOAD_PROTOCOL = v2.load_protocol_v2
ORIGINAL_CLASSIFY_SCF = v1.classify_scf
EXIT_REQUEST_MARKER: Path | None = None
ROUTE_PATH: Path | None = None
EXIT_AFTER_SECONDS = 1200
MAX_MICROSEGMENTS = 120


def load_route(path: Path) -> dict:
    row = json.loads(path.read_text())
    if row.get("schema") != "symc-kaggle-l15-l17-resilient-checkpoint-route-v0.2":
        raise SystemExit("MECHANICAL_HOLD: wrong resilient checkpoint route schema")
    if row.get("status") != "FROZEN_BEFORE_FIRST_SCIENTIFIC_L15_L17_PRODUCTION_RESULT":
        raise SystemExit("MECHANICAL_HOLD: resilient checkpoint route is not frozen")
    cp = row["checkpointing"]
    if int(cp["frozen_input_qe_max_seconds"]) != 16200:
        raise SystemExit("SCIENTIFIC_HOLD: frozen QE max_seconds changed")
    if cp["scheduled_exit_mechanism"] != "QE_PREFIX_EXIT_FILE":
        raise SystemExit("MECHANICAL_HOLD: unexpected microcheckpoint mechanism")
    fw = row["frozen_science_firewall"]
    for key in (
        "scientific_settings_changed", "thresholds_changed", "ecutwfc_changed",
        "ecutrho_changed", "geometry_changed", "coverage_changed", "kmesh_changed",
        "esm_changed", "pseudopotentials_changed", "pw_binary_changed",
        "execution_rank_changed", "l15_l17_sensitivity_gate_changed",
        "paid_compute_used", "automatic_paid_escalation",
    ):
        if fw.get(key) is not False:
            raise SystemExit(f"SCIENTIFIC_HOLD: route firewall drift: {key}")
    if fw.get("original_l17_hold_preserved") is not True:
        raise SystemExit("SCIENTIFIC_HOLD: original L17 hold not preserved")
    return row


def amended_load_protocol(path: Path) -> dict:
    """Validate the frozen protocol first, then expand only execution bookkeeping."""
    p = ORIGINAL_LOAD_PROTOCOL(path)
    q = copy.deepcopy(p)
    q["execution"]["maximum_scf_segments"] = MAX_MICROSEGMENTS
    # Deliberately do NOT change qe_max_seconds_per_segment. The actual QE input
    # remains at the frozen 16200 s; auxiliary user-request EXIT files stop it sooner.
    if int(q["execution"]["qe_max_seconds_per_segment"]) != 16200:
        raise SystemExit("SCIENTIFIC_HOLD: QE max_seconds drift")
    return q


def classify_scf_resilient(text: str, rc: int, wrapper_timeout: bool) -> dict:
    """Accept official QE clean EXIT-file stops as exact-restart checkpoints."""
    lower = text.lower()
    if wrapper_timeout:
        raise SystemExit("MECHANICAL_HOLD: external timeout before guaranteed QE checkpoint")
    if rc != 0 or "error in routine" in lower or "mpi_abort" in lower:
        raise SystemExit(f"MECHANICAL_HOLD: pw.x failed before admissible checkpoint, rc={rc}")

    job_done = "job done" in lower
    scf_converged = "convergence has been achieved" in lower or "end of self-consistent calculation" in lower
    energies = [float(x) * v1.RY_TO_EV for x in v1.ENERGY_RE.findall(text)]
    if job_done and scf_converged and energies:
        return {
            "status": "COMPLETE",
            "job_done": True,
            "clean_max_seconds_stop": "maximum cpu time exceeded" in lower,
            "scf_converged": True,
            "energy_ev": energies[-1],
        }

    marker_ok = EXIT_REQUEST_MARKER is not None and EXIT_REQUEST_MARKER.is_file()
    if marker_ok and job_done:
        return {
            "status": "CHECKPOINT",
            "job_done": True,
            "clean_max_seconds_stop": False,
            "scf_converged": False,
            "energy_ev": None,
        }

    # Preserve the original frozen classifier for a true max_seconds clean stop.
    return ORIGINAL_CLASSIFY_SCF(text, rc, wrapper_timeout)


def write_exit_request(exit_file: Path, marker: Path, reason: str) -> None:
    exit_file.parent.mkdir(parents=True, exist_ok=True)
    row = {
        "schema": "symc-qe-clean-exit-request-v0.1",
        "reason": reason,
        "requested_epoch": time.time(),
        "exit_file": str(exit_file),
        "scientific_settings_changed": False,
        "thresholds_changed": False,
    }
    marker.write_text(json.dumps(row, indent=2, sort_keys=True) + "\n")
    exit_file.touch()
    print(f"QE_CLEAN_EXIT_REQUESTED: {reason}", flush=True)


def main() -> None:
    global EXIT_REQUEST_MARKER, ROUTE_PATH, EXIT_AFTER_SECONDS, MAX_MICROSEGMENTS

    ap = argparse.ArgumentParser()
    ap.add_argument("--route", required=True)
    ap.add_argument("--protocol", required=True)
    ap.add_argument("--surface-protocol", required=True)
    ap.add_argument("--stage-a-result", required=True)
    ap.add_argument("--bundle", required=True)
    ap.add_argument("--pseudo-dir", required=True)
    ap.add_argument("--pw", required=True)
    ap.add_argument("--l15-root", required=True)
    ap.add_argument("--l17-root", required=True)
    ap.add_argument("--depth", required=True, choices=["L15", "L17"])
    ap.add_argument("--site", required=True, choices=["top", "bridge", "fcc_hollow", "hcp_hollow"])
    ap.add_argument("--microsegment", required=True, type=int)
    ap.add_argument("--out", required=True)
    ap.add_argument("--prior-root")
    args = ap.parse_args()

    ROUTE_PATH = Path(args.route).resolve()
    route = load_route(ROUTE_PATH)
    EXIT_AFTER_SECONDS = int(route["checkpointing"]["scheduled_exit_request_seconds"])
    MAX_MICROSEGMENTS = int(route["checkpointing"]["maximum_microcheckpoints_per_case"])
    if args.microsegment < 1 or args.microsegment > MAX_MICROSEGMENTS:
        raise SystemExit("MECHANICAL_HOLD: microsegment outside frozen resilient route bound")
    if args.microsegment > 1 and not args.prior_root:
        raise SystemExit("MECHANICAL_HOLD: --prior-root required after microsegment 1")

    # Patch only the in-memory execution state machine after both source files
    # have independently validated their frozen contracts.
    v1.load_protocol = amended_load_protocol
    v1.classify_scf = classify_scf_resilient

    out_root = Path(args.out).resolve()
    out_root.mkdir(parents=True, exist_ok=True)
    prefix = f"co_cu111_l15l17_{args.depth.lower()}_{args.site}"
    exit_file = out_root / "qe_checkpoint" / f"{prefix}.EXIT"
    marker = out_root / "MICROCHECKPOINT_EXIT_REQUEST.json"
    EXIT_REQUEST_MARKER = marker

    stop_watchdog = threading.Event()

    def watchdog() -> None:
        if not stop_watchdog.wait(EXIT_AFTER_SECONDS):
            write_exit_request(exit_file, marker, f"SCHEDULED_{EXIT_AFTER_SECONDS}_SECOND_MICROCHECKPOINT")

    def signal_handler(signum: int, _frame) -> None:  # type: ignore[no-untyped-def]
        if not marker.exists():
            try:
                write_exit_request(exit_file, marker, f"BEST_EFFORT_SIGNAL_{signum}")
            except Exception as exc:  # pragma: no cover - best effort under shutdown
                print(f"BEST_EFFORT_EXIT_REQUEST_FAILED: {exc}", flush=True)
        # Intentionally do not raise/exit here. QE needs time to observe the EXIT
        # file, finish at a safe point, and write restart data.

    for sig in (signal.SIGTERM, signal.SIGHUP, signal.SIGINT):
        signal.signal(sig, signal_handler)

    t = threading.Thread(target=watchdog, name="qe-clean-exit-watchdog", daemon=True)
    t.start()

    ns = argparse.Namespace(
        protocol=args.protocol,
        surface_protocol=args.surface_protocol,
        stage_a_result=args.stage_a_result,
        bundle=args.bundle,
        pseudo_dir=args.pseudo_dir,
        pw=args.pw,
        l15_root=args.l15_root,
        l17_root=args.l17_root,
        depth=args.depth,
        site=args.site,
        out=args.out,
        segment=args.microsegment,
        prior_root=args.prior_root,
    )

    try:
        v1.command_scf_segment(ns)
    finally:
        stop_watchdog.set()
        t.join(timeout=2)

    state_path = out_root / "L15_L17_SITE_SCF_STATE.json"
    if not state_path.is_file():
        raise SystemExit("MECHANICAL_HOLD: microsegment returned without state")
    state = json.loads(state_path.read_text())
    state["microcheckpoint_execution_route"] = str(ROUTE_PATH)
    state["microcheckpoint_execution_route_sha256"] = v1.sha256(ROUTE_PATH)
    state["microcheckpoint_sequence"] = int(args.microsegment)
    state["frozen_input_qe_max_seconds"] = 16200
    state["scheduled_exit_request_seconds"] = EXIT_AFTER_SECONDS
    state["scientific_settings_changed"] = False
    state["thresholds_changed"] = False
    if state.get("status") == "CHECKPOINT" and marker.is_file():
        req = json.loads(marker.read_text())
        state["checkpoint_semantics"] = "QE_CLEAN_EXIT_FILE_EXACT_RESTART"
        state["clean_user_exit_stop"] = True
        state["clean_exit_request_reason"] = req.get("reason")
        state["clean_exit_requested_epoch"] = req.get("requested_epoch")
        if not state.get("checkpoint_manifest_sha256"):
            raise SystemExit("MECHANICAL_HOLD: clean EXIT stop lacks checkpoint manifest")
        v1.verify_checkpoint_manifest(out_root, state["checkpoint_manifest_sha256"])
    else:
        state["clean_user_exit_stop"] = False
    state_path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")
    print(json.dumps(state, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
