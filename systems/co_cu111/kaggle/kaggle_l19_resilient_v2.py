#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
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
ROUTE = CO / 'KAGGLE_L19_RESILIENT_ROUTE_v0.2.json'
PROTOCOL = CO / 'SYSTEM2_PBE_SURFACE_CONVERGENCE_L19_v0.1.json'
HOLD = CO / 'L19_PERSONAL_FREE_CACHE_RESOURCE_HOLD_v0.1.json'
PREPARE = KDIR / 'kaggle_l19_prepare_v1.sh'
SEGMENTER = KDIR / 'kaggle_l19_segment_v1.sh'
RUNNER = CO / 'pbe_surface_depth_stack_v1.py'
CURRENT = WORK / 'symc_l19_current'
HISTORY = WORK / 'symc_l19_history'
BOOT = TMP / 'symc_l19_bootstrap'
STAGE = TMP / 'symc_l19_persist_stage'
RESTORE = TMP / 'symc_l19_restore'
PERSIST_STATUS = WORK / 'KAGGLE_L19_PERSISTENCE_STATUS.json'
FINAL_RESULT = WORK / 'L19_CONVERGENCE_RESULT.json'
ARCHIVE_NAME = 'symc_l19_checkpoint.qebin'
META_NAME = 'L19_CHECKPOINT_META.json'
META_SCHEMA = 'symc-kaggle-l19-durable-checkpoint-v0.2'
STATE_SCHEMA = 'co-cu111-pbe-surface-depth-qe-restart-state-v0.1'


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(8 << 20), b''):
            h.update(block)
    return h.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    row = json.loads(path.read_text())
    if not isinstance(row, dict):
        raise RuntimeError(f'JSON object required: {path}')
    return row


def write_json(path: Path, row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(row, indent=2, sort_keys=True) + '\n')


def run(cmd: list[str], *, cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    print('+ ' + ' '.join(cmd), flush=True)
    return subprocess.run(cmd, cwd=cwd, check=check, text=True)


def load_route() -> dict[str, Any]:
    row = load_json(ROUTE)
    if row.get('schema') != 'symc-kaggle-l19-resilient-route-v0.2':
        raise SystemExit('MECHANICAL_HOLD: wrong L19 Kaggle route schema')
    if row.get('status') != 'FROZEN_BEFORE_KAGGLE_L19_RESULT':
        raise SystemExit('SCIENTIFIC_HOLD: L19 Kaggle route is not frozen before result')
    if sha256(PROTOCOL) != row['scientific_protocol_sha256']:
        raise SystemExit('MECHANICAL_HOLD: L19 scientific protocol hash drift')
    hold = load_json(HOLD)
    if hold.get('status') != row['source_mechanical_hold_status']:
        raise SystemExit('MECHANICAL_HOLD: source GitHub storage-hold identity drift')
    ex = row['execution']
    if ex.get('execution_mode') != 'DIRECT_ONE_RANK' or int(ex.get('mpi_ranks', -1)) != 1:
        raise SystemExit('SCIENTIFIC_HOLD: L19 execution-rank drift')
    if int(ex.get('qe_max_seconds_per_segment', -1)) != 16200:
        raise SystemExit('SCIENTIFIC_HOLD: L19 QE max_seconds drift')
    if int(ex.get('maximum_relax_segments', -1)) != 6 or int(ex.get('maximum_scf_segments', -1)) != 4:
        raise SystemExit('SCIENTIFIC_HOLD: L19 restart runway drift')
    for key, value in row['frozen_science_firewall'].items():
        if key == 'original_l17_hold_preserved':
            if value is not True:
                raise SystemExit('SCIENTIFIC_HOLD: original L17 hold not preserved')
        elif value is not False:
            raise SystemExit(f'SCIENTIFIC_HOLD: L19 firewall drift: {key}')
    return row


def kaggle_api():
    try:
        import kagglehub
        from kagglehub import datasets_helpers
        from kagglehub.exceptions import BackendError, NotFoundError
    except Exception as exc:
        raise SystemExit(f'MECHANICAL_HOLD: kagglehub unavailable: {exc}') from exc
    try:
        who = kagglehub.whoami()
    except Exception as exc:
        raise SystemExit(f'MECHANICAL_HOLD: Kaggle native authentication failed: {exc}') from exc
    username = who.get('username') if isinstance(who, dict) else None
    if not username and isinstance(who, dict):
        username = who.get('userName')
    if not username:
        raise SystemExit(f'MECHANICAL_HOLD: unable to resolve Kaggle username from {who!r}')
    return kagglehub, datasets_helpers, BackendError, NotFoundError, str(username)


def locate_downloaded(path_value: str, name: str) -> Path:
    p = Path(path_value)
    if p.is_file() and p.name == name:
        return p
    if p.is_dir():
        hits = [x for x in p.rglob(name) if x.is_file()]
        if len(hits) == 1:
            return hits[0]
    raise FileNotFoundError(f'Unable to locate {name} below {p}')


def explicit_not_found(exc: Exception, BackendError, NotFoundError) -> bool:
    if isinstance(exc, NotFoundError):
        return True
    if isinstance(exc, BackendError):
        compact = str(exc).lower().replace(' ', '')
        return '\"code\":5' in compact and 'notfound' in compact
    return False


def read_slot_meta(kagglehub, username: str, slug: str, BackendError, NotFoundError) -> dict[str, Any] | None:
    try:
        value = kagglehub.dataset_download(f'{username}/{slug}', path=META_NAME)
        path = locate_downloaded(value, META_NAME)
        row = load_json(path)
    except Exception as exc:
        if explicit_not_found(exc, BackendError, NotFoundError):
            print(f'L19_CHECKPOINT_SLOT_EMPTY_CONFIRMED: {slug}', flush=True)
            return None
        raise RuntimeError(f'L19_CHECKPOINT_SLOT_READ_HOLD: {slug}: {exc}') from exc
    if row.get('schema') != META_SCHEMA:
        raise RuntimeError(f'L19_CHECKPOINT_SLOT_METADATA_HOLD: schema mismatch in {slug}')
    if row.get('dataset_slug') != slug:
        raise RuntimeError(f'L19_CHECKPOINT_SLOT_METADATA_HOLD: slug mismatch in {slug}')
    if row.get('route_sha256') != sha256(ROUTE):
        raise RuntimeError(f'L19_CHECKPOINT_SLOT_METADATA_HOLD: route hash mismatch in {slug}')
    if row.get('protocol_sha256') != sha256(PROTOCOL):
        raise RuntimeError(f'L19_CHECKPOINT_SLOT_METADATA_HOLD: protocol hash mismatch in {slug}')
    return row


def slot_rows(kagglehub, username: str, route: dict[str, Any], BackendError, NotFoundError) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for slot in ('a', 'b'):
        slug = route['durable_persistence'][f'dataset_slug_{slot}']
        row = read_slot_meta(kagglehub, username, slug, BackendError, NotFoundError)
        if row is not None:
            row = dict(row)
            row['_slot'] = slot
            rows.append(row)
    return sorted(rows, key=lambda r: int(r.get('checkpoint_serial', -1)), reverse=True)


def state() -> dict[str, Any] | None:
    p = CURRENT / 'SURFACE_DEPTH_RESTART_STATE.json'
    if not p.is_file():
        return None
    row = load_json(p)
    if row.get('schema') != STATE_SCHEMA:
        raise SystemExit('MECHANICAL_HOLD: L19 local state schema mismatch')
    if row.get('case_id') != 'L19-V40-K36-extension-audit':
        raise SystemExit('MECHANICAL_HOLD: L19 local state case mismatch')
    if row.get('scientific_settings_changed') is not False or row.get('thresholds_changed') is not False:
        raise SystemExit('SCIENTIFIC_HOLD: L19 local state reports scientific drift')
    if row.get('status') not in {'CHECKPOINT', 'COMPLETE'} or row.get('stage') not in {'relax', 'scf'}:
        raise SystemExit('MECHANICAL_HOLD: L19 local state status/stage invalid')
    return row


def build_archive() -> Path:
    shutil.rmtree(STAGE, ignore_errors=True)
    STAGE.mkdir(parents=True, exist_ok=True)
    archive = STAGE / ARCHIVE_NAME
    cmd = ['tar', '-cf', str(archive)]
    added = False
    for path in (CURRENT, HISTORY):
        if path.exists():
            cmd += ['-C', str(path.parent), path.name]
            added = True
    if FINAL_RESULT.is_file():
        cmd += ['-C', str(FINAL_RESULT.parent), FINAL_RESULT.name]
        added = True
    if not added:
        marker = TMP / 'symc_l19_empty_snapshot.txt'
        marker.write_text('L19 backend preflight only\n')
        cmd += ['-C', str(marker.parent), marker.name]
    run(cmd)
    return archive


def wait_remote(kagglehub, username: str, slug: str, serial: int, BackendError, NotFoundError, timeout_s: int = 1200) -> dict[str, Any]:
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        row = read_slot_meta(kagglehub, username, slug, BackendError, NotFoundError)
        if row is not None and int(row.get('checkpoint_serial', -1)) == serial:
            return row
        time.sleep(5)
    raise RuntimeError('L19 remote metadata verification timed out')


def persist(kagglehub, datasets_helpers, username: str, route: dict[str, Any], BackendError, NotFoundError, current_slot: str | None, serial: int, snapshot_status: str) -> tuple[str, int]:
    target = 'b' if current_slot == 'a' else 'a'
    slug = route['durable_persistence'][f'dataset_slug_{target}']
    archive = build_archive()
    new_serial = serial + 1
    s = state()
    meta = {
        'schema': META_SCHEMA,
        'checkpoint_serial': new_serial,
        'dataset_slot': target,
        'dataset_slug': slug,
        'snapshot_status': snapshot_status,
        'stage': s.get('stage') if s else None,
        'segment': s.get('segment') if s else None,
        'qe_status': s.get('status') if s else None,
        'archive_name': ARCHIVE_NAME,
        'archive_bytes': archive.stat().st_size,
        'archive_sha256': sha256(archive),
        'route_sha256': sha256(ROUTE),
        'protocol_sha256': sha256(PROTOCOL),
        'created_epoch': time.time(),
        'scientific_settings_changed': False,
        'thresholds_changed': False,
        'original_l17_hold_preserved': True,
        'paid_compute_used': False,
    }
    write_json(STAGE / META_NAME, meta)
    handle = f'{username}/{slug}'
    try:
        datasets_helpers.delete_dataset(username, slug)
        time.sleep(5)
    except Exception as exc:
        if not explicit_not_found(exc, BackendError, NotFoundError):
            existing = read_slot_meta(kagglehub, username, slug, BackendError, NotFoundError)
            if existing is not None:
                raise RuntimeError(f'could not retire L19 target slot {target}: {exc}') from exc
    print(f'L19_PERSISTING_PRIVATE_CHECKPOINT: slot={target} serial={new_serial} bytes={meta["archive_bytes"]}', flush=True)
    started = time.time()
    kagglehub.dataset_upload(handle, str(STAGE), version_notes=f'SymC CO/Cu111 L19 checkpoint serial {new_serial}')
    remote = wait_remote(kagglehub, username, slug, new_serial, BackendError, NotFoundError)
    if remote.get('archive_sha256') != meta['archive_sha256'] or int(remote.get('archive_bytes', -1)) != meta['archive_bytes']:
        raise RuntimeError('L19 remote checkpoint metadata mismatch after upload')
    receipt = {
        'schema': 'symc-kaggle-l19-persistence-status-v0.2',
        'status': 'REMOTE_CHECKPOINT_VERIFIED',
        'slot': target,
        'checkpoint_serial': new_serial,
        'snapshot_status': snapshot_status,
        'archive_bytes': meta['archive_bytes'],
        'archive_sha256': meta['archive_sha256'],
        'persistence_seconds': time.time() - started,
        'scientific_settings_changed': False,
        'thresholds_changed': False,
        'paid_compute_used': False,
    }
    write_json(PERSIST_STATUS, receipt)
    print(json.dumps(receipt, indent=2, sort_keys=True), flush=True)
    return target, new_serial


def restore(kagglehub, username: str, rows: list[dict[str, Any]]) -> tuple[str | None, int]:
    if not rows:
        return None, 0
    for meta in rows:
        slot = str(meta['_slot'])
        try:
            value = kagglehub.dataset_download(f'{username}/{meta["dataset_slug"]}', path=ARCHIVE_NAME)
            archive = locate_downloaded(value, ARCHIVE_NAME)
            if archive.stat().st_size != int(meta['archive_bytes']) or sha256(archive) != meta['archive_sha256']:
                raise RuntimeError('archive size/SHA mismatch')
            shutil.rmtree(RESTORE, ignore_errors=True)
            RESTORE.mkdir(parents=True, exist_ok=True)
            run(['tar', '-xf', str(archive), '-C', str(RESTORE)])
            for path in (CURRENT, HISTORY):
                restored = RESTORE / path.name
                if restored.exists():
                    shutil.rmtree(path, ignore_errors=True)
                    shutil.move(str(restored), str(path))
            restored_result = RESTORE / FINAL_RESULT.name
            if restored_result.is_file():
                shutil.copy2(restored_result, FINAL_RESULT)
            s = state()
            print(f'L19_RESTORED_DURABLE_CHECKPOINT: slot={slot} serial={meta["checkpoint_serial"]} state={s}', flush=True)
            return slot, int(meta['checkpoint_serial'])
        except Exception as exc:
            print(f'L19_CHECKPOINT_SLOT_RESTORE_REJECTED: slot={slot} reason={exc}', flush=True)
    raise SystemExit('MECHANICAL_HOLD: L19 remote slots exist but none passed verification')


def next_step(s: dict[str, Any] | None) -> tuple[str, int] | None:
    if s is None:
        return 'relax', 1
    stage = str(s['stage'])
    seg = int(s['segment'])
    status = str(s['status'])
    if stage == 'relax':
        if seg < 6:
            return 'relax', seg + 1
        if status != 'COMPLETE':
            return None
        return 'scf', 1
    if stage == 'scf':
        if seg < 4:
            return 'scf', seg + 1
        return None
    raise SystemExit('MECHANICAL_HOLD: unrecognized L19 stage')


def adjudicate() -> int:
    relax_root = HISTORY / 'relax_segment_6'
    if not (relax_root / 'SURFACE_DEPTH_RESTART_STATE.json').is_file():
        raise SystemExit('MECHANICAL_HOLD: persisted L19 final relaxation state missing')
    if not (CURRENT / 'SURFACE_DEPTH_RESTART_STATE.json').is_file():
        raise SystemExit('MECHANICAL_HOLD: persisted L19 final SCF state missing')
    cp = run([
        sys.executable, str(RUNNER), 'adjudicate',
        '--protocol', str(PROTOCOL),
        '--source-result-root', str(BOOT / 'source_l17_result'),
        '--relax-root', str(relax_root),
        '--scf-root', str(CURRENT),
        '--out', str(FINAL_RESULT),
    ], check=False)
    if not FINAL_RESULT.is_file():
        raise SystemExit('MECHANICAL_HOLD: L19 adjudicator produced no result')
    print(FINAL_RESULT.read_text(), flush=True)
    return cp.returncode


def main() -> None:
    TMP.mkdir(parents=True, exist_ok=True)
    route = load_route()
    run(['bash', str(PREPARE), str(REPO)])
    kagglehub, datasets_helpers, BackendError, NotFoundError, username = kaggle_api()
    print(f'KAGGLE_NATIVE_AUTH_PASS: {username}', flush=True)
    rows = slot_rows(kagglehub, username, route, BackendError, NotFoundError)
    current_slot, serial = restore(kagglehub, username, rows)
    if current_slot is None:
        current_slot, serial = persist(kagglehub, datasets_helpers, username, route, BackendError, NotFoundError, None, 0, 'BACKEND_PREFLIGHT_ONLY')
        print('KAGGLE_L19_PRIVATE_BACKEND_PREFLIGHT_PASS', flush=True)

    while True:
        s = state()
        step = next_step(s)
        if step is None:
            if s is None:
                raise SystemExit('MECHANICAL_HOLD: L19 state vanished')
            if s['stage'] == 'relax' and int(s['segment']) == 6 and s['status'] != 'COMPLETE':
                current_slot, serial = persist(kagglehub, datasets_helpers, username, route, BackendError, NotFoundError, current_slot, serial, 'RELAX_RUNWAY_HOLD')
                raise SystemExit('SCIENTIFIC_HOLD: L19 relaxation incomplete inside frozen six-segment runway')
            if s['stage'] == 'scf' and int(s['segment']) == 4:
                if s['status'] != 'COMPLETE':
                    current_slot, serial = persist(kagglehub, datasets_helpers, username, route, BackendError, NotFoundError, current_slot, serial, 'SCF_RUNWAY_HOLD')
                    raise SystemExit('SCIENTIFIC_HOLD: L19 fixed-geometry SCF incomplete inside frozen four-segment runway')
                rc = adjudicate()
                current_slot, serial = persist(kagglehub, datasets_helpers, username, route, BackendError, NotFoundError, current_slot, serial, 'FINAL_ADJUDICATED')
                if rc == 0:
                    print('KAGGLE_L19_PASS_SURFACE_DEPTH_CONVERGED', flush=True)
                else:
                    print('KAGGLE_L19_HOLD_NEXT_ODD_DEPTH_RUNG_AUTHORIZED', flush=True)
                return
            raise SystemExit('MECHANICAL_HOLD: L19 terminal state not understood')

        stage, segment = step
        print(f'L19_RUNNING: stage={stage} segment={segment}', flush=True)
        cp = run(['bash', str(SEGMENTER), stage, str(segment), str(REPO)], check=False)
        if cp.returncode != 0:
            raise SystemExit(f'MECHANICAL_HOLD: L19 segment driver failed rc={cp.returncode}; prior remote checkpoint remains safe')
        s2 = state()
        if s2 is None or s2.get('stage') != stage or int(s2.get('segment', -1)) != segment:
            raise SystemExit('MECHANICAL_HOLD: L19 segment did not persist expected state')
        current_slot, serial = persist(kagglehub, datasets_helpers, username, route, BackendError, NotFoundError, current_slot, serial, f'{stage.upper()}_{segment}_{s2["status"]}')
        print(f'L19_DURABLE_ADVANCE_PASS: stage={stage} segment={segment} slot={current_slot} serial={serial}', flush=True)


if __name__ == '__main__':
    main()
