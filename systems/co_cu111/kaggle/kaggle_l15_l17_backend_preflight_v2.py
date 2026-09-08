#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

# Import v3 first so its fail-closed Kaggle Not-found handling patches v2.
import kaggle_l15_l17_resilient_v3 as safe  # type: ignore  # noqa: F401
import kaggle_l15_l17_resilient_v2 as base  # type: ignore


def main() -> None:
    route = base.load_route()
    kagglehub, datasets_helpers, username = base.kaggle_api()

    rows = base.slot_rows(kagglehub, username, route)
    if rows:
        newest = rows[0]
        print(json.dumps({
            "schema": "symc-kaggle-l15-l17-backend-preflight-v0.2",
            "status": "PASS_EXISTING_VERIFIED_SLOT_METADATA",
            "username": username,
            "slot": newest.get("_slot"),
            "dataset_slug": newest.get("dataset_slug"),
            "checkpoint_serial": newest.get("checkpoint_serial"),
            "snapshot_status": newest.get("snapshot_status"),
            "archive_bytes": newest.get("archive_bytes"),
            "route_sha256": newest.get("route_sha256"),
            "scientific_compute_started": False,
        }, indent=2, sort_keys=True), flush=True)
        print("KAGGLE_PRIVATE_CHECKPOINT_BACKEND_PREFLIGHT_PASS_EXISTING_SLOT", flush=True)
        return

    print("NO_EXISTING_CHECKPOINT_SLOTS: creating tiny private backend probe", flush=True)
    base.RESULTS.mkdir(parents=True, exist_ok=True)
    slot, serial, elapsed = base.persist_snapshot(
        kagglehub,
        datasets_helpers,
        username,
        route,
        None,
        0,
        "BACKEND_PREFLIGHT_ONLY",
        None,
        None,
        None,
        None,
    )

    rows = base.slot_rows(kagglehub, username, route)
    if not rows:
        raise SystemExit("MECHANICAL_HOLD: backend probe upload returned but no readable slot metadata exists")
    newest = rows[0]
    if newest.get("_slot") != slot or int(newest.get("checkpoint_serial", -1)) != serial:
        raise SystemExit("MECHANICAL_HOLD: backend probe metadata sequence mismatch")
    if newest.get("snapshot_status") != "BACKEND_PREFLIGHT_ONLY":
        raise SystemExit("MECHANICAL_HOLD: backend probe snapshot status mismatch")

    # The backend-only archive is tiny, so verify the full download/hash/untar path too.
    restored_slot, restored_serial = base.restore_newest(kagglehub, username, rows)
    if restored_slot != slot or restored_serial != serial:
        raise SystemExit("MECHANICAL_HOLD: backend probe restore sequence mismatch")

    print(json.dumps({
        "schema": "symc-kaggle-l15-l17-backend-preflight-v0.2",
        "status": "PASS_CREATED_UPLOADED_READ_BACK_AND_RESTORED",
        "username": username,
        "slot": slot,
        "checkpoint_serial": serial,
        "persistence_seconds": elapsed,
        "archive_bytes": newest.get("archive_bytes"),
        "archive_sha256": newest.get("archive_sha256"),
        "scientific_compute_started": False,
        "scientific_settings_changed": False,
        "thresholds_changed": False,
    }, indent=2, sort_keys=True), flush=True)
    print("KAGGLE_PRIVATE_CHECKPOINT_BACKEND_PREFLIGHT_PASS", flush=True)


if __name__ == "__main__":
    main()
