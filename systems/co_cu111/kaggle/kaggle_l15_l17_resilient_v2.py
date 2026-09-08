#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
from typing import Any

REPO = Path('/kaggle/working/Chemistry')
WORK = Path('/kaggle/working')
TMP = Path('/kaggle/tmp')
CO = REPO / 'systems/co_cu111'
KDIR = CO / 'kaggle'
ROUTE = CO / 'KAGGLE_L15_L17_RESILIENT_CHECKPOINT_ROUTE_v0.2.json'
PROTOCOL = CO / 'SYSTEM2_PBE_L15_L17_SITE_DEPTH_DIAGNOSTIC_v0.2.json'
RUNNER = CO / 'pbe_l15_l17_site_depth_diagnostic_v2.py'
MICRO = KDIR / 'kaggle_l15_l17_microsegment_v2.py'
TEST = CO / 'test_pbe_l15_l17_site_depth_diagnostic_v2.py'
ZIP = CO / 'personal_bootstrap/co-cu111-l15-l17-site-depth-inputs-v2.zip'
ZIP_SHA = 'babc1533a8c894420762c734e853a5009497cada508441573f8cef552e6ca257'
PW_SHA = '2b1ede22d276b1d4dab3e31212f306e88ae57e00f33ce6b532b849493a457855'
BOOT = TMP / 'symc_l15_l17_resilient_bootstrap'
ACTIVE = TMP / 'symc_l15_l17_active'
NEXT = TMP / 'symc_l15_l17_next'
RESTORE = TMP / 'symc_l15_l17_restore'
STAGE = TMP / 'symc_l15_l17_persist_stage'
RESULTS = WORK / 'symc_l15_l17_results'
PREFLIGHT = WORK / 'KAGGLE_L15_L17_PREFLIGHT.json'
PERSIST_STATUS = WORK / 'KAGGLE_L15_L17_PERSISTENCE_STATUS.json'
FINAL_RESULT = RESULTS / 'L15_L17_SITE_DEPTH_DIAGNOSTIC_RESULT.json'
ARCHIVE_NAME = 'symc_checkpoint.qebin'
META_NAME = 'CHECKPOINT_META.json'
META_SCHEMA = 'symc-kaggle-l15-l17-durable-checkpoint-v0.2'
ORDER = [
    ('L15', 'top'), ('L15', 'bridge'), ('L15', 'fcc_hollow'), ('L15', 'hcp_hollow'),
    ('L17', 'top'), ('L17', 'bridge'), ('L17', 'fcc_hollow'), ('L17', 'hcp_hollow'),
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(8 << 20), b''):
            h.update(block)
    return h.hexdigest()


def write_json(path: Path, row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(row, indent=2, sort_keys=True) + '\n')


def load_json(path: Path) -> dict[str, Any]:
    row = json.loads(path.read_text())
    if not isinstance(row, dict):
        raise RuntimeError(f'JSON object required: {path}')
    return row


def run(cmd: list[str], *, cwd: Path | None = None, check: bool = True, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    print('+ ' + ' '.join(cmd), flush=True)
    return subprocess.run(cmd, cwd=cwd, check=check, text=True, env=env)


def load_route() -> dict[str, Any]:
    row = load_json(ROUTE)
    if row.get('schema') != 'symc-kaggle-l15-l17-resilient-checkpoint-route-v0.2':
        raise SystemExit('MECHANICAL_HOLD: wrong resilient route schema')
    if row.get('status') != 'FROZEN_BEFORE_FIRST_SCIENTIFIC_L15_L17_PRODUCTION_RESULT':
        raise SystemExit('MECHANICAL_HOLD: resilient route not frozen')
    if int(row['checkpointing']['frozen_input_qe_max_seconds']) != 16200:
        raise SystemExit('SCIENTIFIC_HOLD: frozen input max_seconds drift')
    if int(row['checkpointing']['scheduled_exit_request_seconds']) != 900:
        raise SystemExit('MECHANICAL_HOLD: unexpected scheduled EXIT cadence')
    fw = row['frozen_science_firewall']
    for key in (
        'scientific_settings_changed', 'thresholds_changed', 'ecutwfc_changed', 'ecutrho_changed',
        'geometry_changed', 'coverage_changed', 'kmesh_changed', 'esm_changed', 'pseudopotentials_changed',
        'pw_binary_changed', 'execution_rank_changed', 'l15_l17_sensitivity_gate_changed',
        'paid_compute_used', 'automatic_paid_escalation',
    ):
        if fw.get(key) is not False:
            raise SystemExit(f'SCIENTIFIC_HOLD: route firewall drift: {key}')
    if fw.get('original_l17_hold_preserved') is not True:
        raise SystemExit('SCIENTIFIC_HOLD: original L17 hold not preserved')
    return row


def verify_repo_and_bootstrap(route: dict[str, Any]) -> None:
    if not (REPO / '.git').is_dir():
        raise SystemExit('MECHANICAL_HOLD: repository missing; use the self-bootstrap notebook cell')
    branch = subprocess.check_output(['git', '-C', str(REPO), 'rev-parse', '--abbrev-ref', 'HEAD'], text=True).strip()
    if branch != 'personal-free-compute':
        raise SystemExit(f'MECHANICAL_HOLD: wrong branch {branch}')

    run([sys.executable, str(TEST), '-v'])
    run([sys.executable, str(RUNNER), 'self-test', '--protocol', str(PROTOCOL)])
    if sha256(ZIP) != ZIP_SHA:
        raise SystemExit('MECHANICAL_HOLD: bootstrap ZIP hash mismatch')

    shutil.rmtree(BOOT, ignore_errors=True)
    BOOT.mkdir(parents=True, exist_ok=True)
    run(['unzip', '-q', str(ZIP), '-d', str(BOOT)])
    run(['sha256sum', '-c', 'engine/meta/STAGE_A_ENGINE.sha256'], cwd=BOOT)
    pw = BOOT / 'engine/bin/pw.x'
    pw.chmod(pw.stat().st_mode | 0o111)
    if sha256(pw) != PW_SHA:
        raise SystemExit('MECHANICAL_HOLD: exact pw.x hash mismatch')

    run([
        sys.executable, str(RUNNER), 'preflight',
        '--protocol', str(PROTOCOL),
        '--l15-root', str(BOOT / 'source_l15/l15_audit'),
        '--l17-root', str(BOOT / 'source_l17_relax'),
        '--out', str(PREFLIGHT),
    ])
    pre = load_json(PREFLIGHT)
    if pre.get('status') != 'PASS':
        raise SystemExit('MECHANICAL_HOLD: L15/L17 production preflight did not pass')
    print('KAGGLE_L15_L17_RESILIENT_PREFLIGHT_PASS', flush=True)


def kaggle_api():
    try:
        import kagglehub
        from kagglehub import datasets_helpers
    except Exception as exc:
        raise SystemExit(f'MECHANICAL_HOLD: kagglehub unavailable: {exc}') from exc
    try:
        who = kagglehub.whoami()
    except Exception as exc:
        raise SystemExit(f'MECHANICAL_HOLD: Kaggle native authentication failed before QE launch: {exc}') from exc
    username = None
    if isinstance(who, dict):
        username = who.get('username') or who.get('userName')
    if not username:
        raise SystemExit(f'MECHANICAL_HOLD: unable to resolve authenticated Kaggle username from {who!r}')
    print(f'KAGGLE_NATIVE_AUTH_PASS: {username}', flush=True)
    return kagglehub, datasets_helpers, str(username)


def locate_downloaded(path_value: str, name: str) -> Path:
    p = Path(path_value)
    if p.is_file():
        return p
    if p.is_dir():
        hits = [x for x in p.rglob(name) if x.is_file()]
        if len(hits) == 1:
            return hits[0]
    raise FileNotFoundError(f'Unable to locate {name} below {p}')


def read_slot_meta(kagglehub, username: str, slug: str) -> dict[str, Any] | None:
    handle = f'{username}/{slug}'
    try:
        value = kagglehub.dataset_download(handle, path=META_NAME)
        p = locate_downloaded(value, META_NAME)
        row = load_json(p)
    except Exception:
        return None
    if row.get('schema') != META_SCHEMA:
        return None
    if row.get('dataset_slug') != slug:
        return None
    if row.get('route_sha256') != sha256(ROUTE):
        return None
    return row


def slot_rows(kagglehub, username: str, route: dict[str, Any]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for slot in ('a', 'b'):
        slug = route['durable_persistence'][f'dataset_slug_{slot}']
        row = read_slot_meta(kagglehub, username, slug)
        if row is not None:
            row = dict(row)
            row['_slot'] = slot
            out.append(row)
    return sorted(out, key=lambda r: int(r.get('checkpoint_serial', -1)), reverse=True)


def verify_active_checkpoint(root: Path) -> None:
    state_path = root / 'L15_L17_SITE_SCF_STATE.json'
    if not state_path.is_file():
        raise SystemExit('MECHANICAL_HOLD: restored active checkpoint lacks state')
    state = load_json(state_path)
    if state.get('status') != 'CHECKPOINT':
        raise SystemExit('MECHANICAL_HOLD: restored active state is not CHECKPOINT')
    if not state.get('checkpoint_manifest_sha256'):
        raise SystemExit('MECHANICAL_HOLD: restored active state lacks checkpoint manifest hash')
    sys.path.insert(0, str(CO))
    import pbe_l15_l17_site_depth_diagnostic_v2 as v2  # type: ignore
    v2.verify_checkpoint_manifest(root, state['checkpoint_manifest_sha256'])
    print('RESTORED_EXACT_CHECKPOINT_MANIFEST_PASS', flush=True)


def restore_newest(kagglehub, username: str, rows: list[dict[str, Any]]) -> tuple[str | None, int]:
    if not rows:
        return None, 0
    for meta in rows:
        slot = str(meta['_slot'])
        slug = str(meta['dataset_slug'])
        handle = f'{username}/{slug}'
        try:
            value = kagglehub.dataset_download(handle, path=ARCHIVE_NAME)
            archive = locate_downloaded(value, ARCHIVE_NAME)
            if archive.stat().st_size != int(meta['archive_bytes']):
                raise RuntimeError('remote checkpoint archive size mismatch')
            digest = sha256(archive)
            if digest != meta['archive_sha256']:
                raise RuntimeError('remote checkpoint archive SHA256 mismatch')
            shutil.rmtree(RESTORE, ignore_errors=True)
            RESTORE.mkdir(parents=True, exist_ok=True)
            run(['tar', '-xf', str(archive), '-C', str(RESTORE)])

            restored_results = RESTORE / RESULTS.name
            if restored_results.exists():
                shutil.rmtree(RESULTS, ignore_errors=True)
                shutil.move(str(restored_results), str(RESULTS))
            else:
                RESULTS.mkdir(parents=True, exist_ok=True)

            restored_active = RESTORE / ACTIVE.name
            shutil.rmtree(ACTIVE, ignore_errors=True)
            if restored_active.exists():
                shutil.move(str(restored_active), str(ACTIVE))
                verify_active_checkpoint(ACTIVE)
            print(f'RESTORED_DURABLE_CHECKPOINT: slot={slot} serial={meta["checkpoint_serial"]}', flush=True)
            return slot, int(meta['checkpoint_serial'])
        except Exception as exc:
            print(f'CHECKPOINT_SLOT_RESTORE_REJECTED: slot={slot} reason={exc}', flush=True)
            continue
    raise SystemExit('MECHANICAL_HOLD: checkpoint slots exist but none passed archive/hash/restart verification')


def completed_case(depth: str, site: str) -> bool:
    p = RESULTS / depth / site / 'segment6/L15_L17_SITE_SCF_STATE.json'
    if not p.is_file():
        return False
    row = load_json(p)
    return (
        row.get('status') == 'COMPLETE'
        and row.get('energy_ev') is not None
        and row.get('depth') == depth
        and row.get('site') == site
        and int(row.get('segment', -1)) == 6
        and row.get('scientific_settings_changed') is False
        and row.get('original_l17_hold_preserved') is True
        and row.get('absolute_clean_surface_pass_claimed') is False
    )


def results_summary() -> list[str]:
    return [f'{d}:{s}' for d, s in ORDER if completed_case(d, s)]


def build_archive(active_root: Path | None) -> Path:
    shutil.rmtree(STAGE, ignore_errors=True)
    STAGE.mkdir(parents=True, exist_ok=True)
    archive = STAGE / ARCHIVE_NAME
    cmd = ['tar', '-cf', str(archive)]
    added = False
    if active_root is not None and active_root.exists():
        cmd += ['-C', str(active_root.parent), active_root.name]
        added = True
    if RESULTS.exists():
        cmd += ['-C', str(RESULTS.parent), RESULTS.name]
        added = True
    if not added:
        marker = TMP / 'symc_empty_snapshot_marker.txt'
        marker.write_text('no active checkpoint and no results yet\n')
        cmd += ['-C', str(marker.parent), marker.name]
    run(cmd)
    return archive


def wait_for_remote_meta(kagglehub, username: str, slug: str, serial: int, timeout_s: int = 900) -> dict[str, Any]:
    deadline = time.time() + timeout_s
    last = None
    while time.time() < deadline:
        row = read_slot_meta(kagglehub, username, slug)
        if row is not None:
            last = row
            if int(row.get('checkpoint_serial', -1)) == serial:
                return row
        time.sleep(5)
    raise RuntimeError(f'remote checkpoint metadata did not become readable in {timeout_s}s; last={last!r}')


def persist_snapshot(
    kagglehub,
    datasets_helpers,
    username: str,
    route: dict[str, Any],
    current_slot: str | None,
    serial: int,
    status: str,
    active_root: Path | None,
    depth: str | None,
    site: str | None,
    microsegment: int | None,
) -> tuple[str, int, float]:
    target = 'b' if current_slot == 'a' else 'a'
    slug = route['durable_persistence'][f'dataset_slug_{target}']
    handle = f'{username}/{slug}'
    archive = build_archive(active_root)
    new_serial = serial + 1
    meta = {
        'schema': META_SCHEMA,
        'checkpoint_serial': new_serial,
        'dataset_slot': target,
        'dataset_slug': slug,
        'snapshot_status': status,
        'depth': depth,
        'site': site,
        'microsegment': microsegment,
        'archive_name': ARCHIVE_NAME,
        'archive_bytes': archive.stat().st_size,
        'archive_sha256': sha256(archive),
        'route_sha256': sha256(ROUTE),
        'protocol_sha256': sha256(PROTOCOL),
        'created_epoch': time.time(),
        'completed_cases': results_summary(),
        'scientific_settings_changed': False,
        'thresholds_changed': False,
        'original_l17_hold_preserved': True,
        'paid_compute_used': False,
    }
    write_json(STAGE / META_NAME, meta)

    try:
        datasets_helpers.delete_dataset(username, slug)
        time.sleep(5)
    except Exception as exc:
        existing = read_slot_meta(kagglehub, username, slug)
        if existing is not None:
            raise RuntimeError(f'could not retire old target slot {target}: {exc}') from exc

    print(f'PERSISTING_PRIVATE_KAGGLE_CHECKPOINT: slot={target} bytes={meta["archive_bytes"]}', flush=True)
    started = time.time()
    kagglehub.dataset_upload(handle, str(STAGE), version_notes=f'SymC L15/L17 checkpoint serial {new_serial}')
    remote = wait_for_remote_meta(kagglehub, username, slug, new_serial)
    if remote.get('archive_sha256') != meta['archive_sha256'] or int(remote.get('archive_bytes', -1)) != meta['archive_bytes']:
        raise RuntimeError('remote checkpoint metadata does not match uploaded archive')
    elapsed = time.time() - started
    status_row = {
        'schema': 'symc-kaggle-l15-l17-persistence-status-v0.2',
        'status': 'REMOTE_CHECKPOINT_VERIFIED',
        'slot': target,
        'checkpoint_serial': new_serial,
        'persistence_seconds': elapsed,
        'archive_bytes': meta['archive_bytes'],
        'archive_sha256': meta['archive_sha256'],
        'durable_exposure_target_seconds': 1800,
        'scientific_settings_changed': False,
        'thresholds_changed': False,
    }
    write_json(PERSIST_STATUS, status_row)
    print(json.dumps(status_row, indent=2, sort_keys=True), flush=True)
    shutil.rmtree(STAGE, ignore_errors=True)
    return target, new_serial, elapsed


def materialize_complete(depth: str, site: str, microsegment: int, complete_root: Path) -> None:
    src_state = complete_root / 'L15_L17_SITE_SCF_STATE.json'
    row = load_json(src_state)
    if row.get('status') != 'COMPLETE' or row.get('energy_ev') is None:
        raise SystemExit('MECHANICAL_HOLD: cannot materialize non-complete case')
    actual_sha = sha256(src_state)
    case = RESULTS / depth / site
    actual = case / f'actual_microsegment_{microsegment}'
    final6 = case / 'segment6'
    shutil.rmtree(actual, ignore_errors=True)
    shutil.rmtree(final6, ignore_errors=True)
    actual.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(complete_root, actual)
    actual_state = actual / 'L15_L17_SITE_SCF_STATE.json'
    actual_named = actual / 'ACTUAL_COMPLETE_STATE.json'
    actual_state.rename(actual_named)

    final6.mkdir(parents=True, exist_ok=True)
    final = dict(row)
    final['segment'] = 6
    final['actual_completion_microsegment'] = microsegment
    final['source_actual_complete_state_sha256'] = actual_sha
    final['materialized_for_original_segment6_adjudicator'] = True
    final['carried_forward_without_recomputation'] = True
    final['scientific_settings_changed'] = False
    final['thresholds_changed'] = False
    final['original_l17_hold_preserved'] = True
    final['absolute_clean_surface_pass_claimed'] = False
    final['microcheckpoint_execution_route_sha256'] = sha256(ROUTE)
    write_json(final6 / 'L15_L17_SITE_SCF_STATE.json', final)
    print(f'CASE_FINAL_STATE_MATERIALIZED: {depth}:{site} actual_microsegment={microsegment}', flush=True)


def next_case() -> tuple[str, str] | None:
    for depth, site in ORDER:
        if not completed_case(depth, site):
            return depth, site
    return None


def active_state() -> dict[str, Any] | None:
    p = ACTIVE / 'L15_L17_SITE_SCF_STATE.json'
    if not p.is_file():
        return None
    return load_json(p)


def run_microsegment(depth: str, site: str, microsegment: int, prior: Path | None) -> tuple[dict[str, Any], float]:
    shutil.rmtree(NEXT, ignore_errors=True)
    NEXT.mkdir(parents=True, exist_ok=True)
    cmd = [
        sys.executable, str(MICRO),
        '--route', str(ROUTE),
        '--protocol', str(PROTOCOL),
        '--surface-protocol', str(CO / 'SYSTEM2_PBE_SURFACE_SITE_ORDERING_PROTOCOL_v0.1.json'),
        '--stage-a-result', str(BOOT / 'stage_a_decision/PBE_STAGE_A_NUMERICAL_EXTENSION_RESULT.json'),
        '--bundle', str(CO / 'PBE_PSEUDOPOTENTIAL_BUNDLE_v0.1.json'),
        '--pseudo-dir', str(BOOT / 'engine/pseudos'),
        '--pw', str(BOOT / 'engine/bin/pw.x'),
        '--l15-root', str(BOOT / 'source_l15/l15_audit'),
        '--l17-root', str(BOOT / 'source_l17_relax'),
        '--depth', depth,
        '--site', site,
        '--microsegment', str(microsegment),
        '--out', str(NEXT),
    ]
    if prior is not None:
        cmd += ['--prior-root', str(prior)]
    env = dict(os.environ)
    env.update({'OMP_NUM_THREADS': '1', 'OPENBLAS_NUM_THREADS': '1', 'MKL_NUM_THREADS': '1'})
    started = time.time()
    cp = run(cmd, check=False, env=env)
    elapsed = time.time() - started
    if cp.returncode != 0:
        raise SystemExit(f'MECHANICAL_HOLD: microsegment runner failed rc={cp.returncode}; prior durable checkpoint remains safe')
    state_path = NEXT / 'L15_L17_SITE_SCF_STATE.json'
    if not state_path.is_file():
        raise SystemExit('MECHANICAL_HOLD: microsegment completed without state')
    state = load_json(state_path)
    if state.get('depth') != depth or state.get('site') != site or int(state.get('segment', -1)) != microsegment:
        raise SystemExit('MECHANICAL_HOLD: microsegment state sequence mismatch')
    if state.get('scientific_settings_changed') is not False or state.get('thresholds_changed') is not False:
        raise SystemExit('SCIENTIFIC_HOLD: microsegment reports scientific drift')
    return state, elapsed


def adjudicate() -> int:
    RESULTS.mkdir(parents=True, exist_ok=True)
    cp = run([
        sys.executable, str(RUNNER), 'adjudicate',
        '--protocol', str(PROTOCOL),
        '--root', str(RESULTS),
        '--out', str(FINAL_RESULT),
    ], check=False)
    if not FINAL_RESULT.is_file():
        raise SystemExit('MECHANICAL_HOLD: adjudicator returned without result')
    row = load_json(FINAL_RESULT)
    print(json.dumps(row, indent=2, sort_keys=True), flush=True)
    return cp.returncode


def main() -> None:
    TMP.mkdir(parents=True, exist_ok=True)
    RESULTS.mkdir(parents=True, exist_ok=True)
    route = load_route()
    verify_repo_and_bootstrap(route)
    kagglehub, datasets_helpers, username = kaggle_api()

    rows = slot_rows(kagglehub, username, route)
    current_slot, serial = restore_newest(kagglehub, username, rows)

    if current_slot is None:
        current_slot, serial, _ = persist_snapshot(
            kagglehub, datasets_helpers, username, route,
            None, 0, 'BACKEND_PREFLIGHT_ONLY', None, None, None, None,
        )
        print('KAGGLE_PRIVATE_CHECKPOINT_BACKEND_PREFLIGHT_PASS', flush=True)

    while True:
        case = next_case()
        if case is None:
            rc = adjudicate()
            current_slot, serial, _ = persist_snapshot(
                kagglehub, datasets_helpers, username, route,
                current_slot, serial, 'FINAL_ADJUDICATED', None, None, None, None,
            )
            if rc == 0:
                print('KAGGLE_L15_L17_ALL_CASES_COMPLETE_AND_ADJUDICATED', flush=True)
            else:
                print('KAGGLE_L15_L17_SCIENTIFIC_HOLD_PRESERVED_AFTER_ADJUDICATION', flush=True)
            return

        depth, site = case
        astate = active_state()
        prior: Path | None = None
        microsegment = 1
        if astate is not None:
            if astate.get('status') != 'CHECKPOINT':
                raise SystemExit('MECHANICAL_HOLD: active state is not a checkpoint')
            if astate.get('depth') != depth or astate.get('site') != site:
                raise SystemExit('MECHANICAL_HOLD: restored active checkpoint does not match first incomplete case')
            prior = ACTIVE
            microsegment = int(astate['segment']) + 1
        print(f'RUNNING_CASE: {depth}:{site} microsegment={microsegment}', flush=True)

        state, compute_elapsed = run_microsegment(depth, site, microsegment, prior)
        status = state.get('status')
        if status == 'CHECKPOINT':
            shutil.rmtree(ACTIVE, ignore_errors=True)
            shutil.move(str(NEXT), str(ACTIVE))
            verify_active_checkpoint(ACTIVE)
            current_slot, serial, persist_elapsed = persist_snapshot(
                kagglehub, datasets_helpers, username, route,
                current_slot, serial, 'ACTIVE_CHECKPOINT', ACTIVE, depth, site, microsegment,
            )
            durable_interval = compute_elapsed + persist_elapsed
            print(f'DURABLE_CHECKPOINT_COMPLETE: {depth}:{site} microsegment={microsegment} interval_s={durable_interval:.1f}', flush=True)
            if durable_interval > 1800:
                print('WARNING_DURABLE_INTERVAL_EXCEEDED_30_MINUTE_TARGET', flush=True)
            continue

        if status == 'COMPLETE':
            shutil.rmtree(ACTIVE, ignore_errors=True)
            materialize_complete(depth, site, microsegment, NEXT)
            shutil.rmtree(NEXT, ignore_errors=True)
            current_slot, serial, persist_elapsed = persist_snapshot(
                kagglehub, datasets_helpers, username, route,
                current_slot, serial, 'CASE_COMPLETE', None, depth, site, microsegment,
            )
            print(f'CASE_COMPLETE_DURABLY_PERSISTED: {depth}:{site} persistence_s={persist_elapsed:.1f}', flush=True)
            continue

        raise SystemExit(f'MECHANICAL_HOLD: unexpected microsegment status {status}')


if __name__ == '__main__':
    main()
