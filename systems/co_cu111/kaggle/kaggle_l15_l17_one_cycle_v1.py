#!/usr/bin/env python3
from __future__ import annotations

import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

# Import v3 first so its fail-closed Kaggle empty-slot handling patches v2.
import kaggle_l15_l17_resilient_v3 as safe  # type: ignore  # noqa: F401
import kaggle_l15_l17_resilient_v2 as base  # type: ignore


def main() -> None:
    base.TMP.mkdir(parents=True, exist_ok=True)
    base.RESULTS.mkdir(parents=True, exist_ok=True)

    route = base.load_route()
    base.verify_repo_and_bootstrap(route)
    kagglehub, datasets_helpers, username = base.kaggle_api()

    rows = base.slot_rows(kagglehub, username, route)
    if not rows:
        raise SystemExit('MECHANICAL_HOLD: no durable checkpoint exists for one-cycle resume qualification')

    current_slot, serial = base.restore_newest(kagglehub, username, rows)
    if current_slot is None:
        raise SystemExit('MECHANICAL_HOLD: durable checkpoint metadata existed but no slot restored')

    case = base.next_case()
    if case is None:
        raise SystemExit('MECHANICAL_HOLD: all cases are already complete; one-cycle resume is unnecessary')
    depth, site = case

    astate = base.active_state()
    if astate is None:
        raise SystemExit('MECHANICAL_HOLD: restored durable snapshot has no active checkpoint')
    if astate.get('status') != 'CHECKPOINT':
        raise SystemExit('MECHANICAL_HOLD: restored active state is not CHECKPOINT')
    if astate.get('depth') != depth or astate.get('site') != site:
        raise SystemExit('MECHANICAL_HOLD: restored checkpoint does not match first incomplete case')

    microsegment = int(astate['segment']) + 1
    print(
        f'ONE_CYCLE_RESUME_START: {depth}:{site} microsegment={microsegment} '
        f'from_slot={current_slot} serial={serial}',
        flush=True,
    )

    state, compute_elapsed = base.run_microsegment(depth, site, microsegment, base.ACTIVE)
    status = state.get('status')

    if status == 'CHECKPOINT':
        shutil.rmtree(base.ACTIVE, ignore_errors=True)
        shutil.move(str(base.NEXT), str(base.ACTIVE))
        base.verify_active_checkpoint(base.ACTIVE)
        new_slot, new_serial, persist_elapsed = base.persist_snapshot(
            kagglehub,
            datasets_helpers,
            username,
            route,
            current_slot,
            serial,
            'ACTIVE_CHECKPOINT',
            base.ACTIVE,
            depth,
            site,
            microsegment,
        )
        durable_interval = compute_elapsed + persist_elapsed
        print(
            f'ONE_CYCLE_DURABLE_CHECKPOINT_PASS: {depth}:{site} '
            f'microsegment={microsegment} slot={new_slot} serial={new_serial} '
            f'compute_s={compute_elapsed:.1f} persist_s={persist_elapsed:.1f} '
            f'durable_interval_s={durable_interval:.1f}',
            flush=True,
        )
        if durable_interval <= 1800:
            print('DURABLE_EXPOSURE_TARGET_30_MIN_PASS', flush=True)
        else:
            print('DURABLE_EXPOSURE_TARGET_30_MIN_HOLD', flush=True)
        return

    if status == 'COMPLETE':
        shutil.rmtree(base.ACTIVE, ignore_errors=True)
        base.materialize_complete(depth, site, microsegment, base.NEXT)
        shutil.rmtree(base.NEXT, ignore_errors=True)
        new_slot, new_serial, persist_elapsed = base.persist_snapshot(
            kagglehub,
            datasets_helpers,
            username,
            route,
            current_slot,
            serial,
            'CASE_COMPLETE',
            None,
            depth,
            site,
            microsegment,
        )
        durable_interval = compute_elapsed + persist_elapsed
        print(
            f'ONE_CYCLE_CASE_COMPLETE_PASS: {depth}:{site} '
            f'microsegment={microsegment} slot={new_slot} serial={new_serial} '
            f'compute_s={compute_elapsed:.1f} persist_s={persist_elapsed:.1f} '
            f'durable_interval_s={durable_interval:.1f}',
            flush=True,
        )
        if durable_interval <= 1800:
            print('DURABLE_EXPOSURE_TARGET_30_MIN_PASS', flush=True)
        else:
            print('DURABLE_EXPOSURE_TARGET_30_MIN_HOLD', flush=True)
        return

    raise SystemExit(f'MECHANICAL_HOLD: unexpected resumed microsegment status {status}')


if __name__ == '__main__':
    main()
