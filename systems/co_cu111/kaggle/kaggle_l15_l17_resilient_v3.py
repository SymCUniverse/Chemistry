#!/usr/bin/env python3
"""Safety wrapper for resilient L15/L17 Kaggle orchestration.

Only an explicit Kaggle NotFound response is treated as an empty checkpoint
slot. Network, authentication, backend, malformed-metadata, and route-hash
errors fail closed before any existing slot can be overwritten.
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import kaggle_l15_l17_resilient_v2 as base  # type: ignore


def _is_explicit_kaggle_not_found(exc: Exception) -> bool:
    """Recognize only Kaggle's explicit dataset-not-found responses.

    kagglehub 0.x may surface a missing dataset either as NotFoundError or as
    BackendError carrying the JSON backend payload {"error":{"code":5}} with
    "Not found". Treat no other backend/network/authentication failure as empty.
    """
    from kagglehub.exceptions import BackendError, NotFoundError

    if isinstance(exc, NotFoundError):
        return True
    if isinstance(exc, BackendError):
        compact = str(exc).lower().replace(" ", "")
        return '"code":5' in compact and "notfound" in compact
    return False


def safe_read_slot_meta(kagglehub, username: str, slug: str):
    handle = f"{username}/{slug}"
    try:
        value = kagglehub.dataset_download(handle, path=base.META_NAME)
        p = base.locate_downloaded(value, base.META_NAME)
        row = base.load_json(p)
    except Exception as exc:
        if _is_explicit_kaggle_not_found(exc):
            print(f"CHECKPOINT_SLOT_EMPTY_CONFIRMED: {slug}", flush=True)
            return None
        raise RuntimeError(
            f"CHECKPOINT_SLOT_READ_HOLD: {slug} could not be read safely; "
            "refusing to treat the slot as empty"
        ) from exc

    if row.get("schema") != base.META_SCHEMA:
        raise RuntimeError(f"CHECKPOINT_SLOT_METADATA_HOLD: unrecognized metadata in {slug}")
    if row.get("dataset_slug") != slug:
        raise RuntimeError(f"CHECKPOINT_SLOT_METADATA_HOLD: dataset slug mismatch in {slug}")
    if row.get("route_sha256") != base.sha256(base.ROUTE):
        raise RuntimeError(f"CHECKPOINT_SLOT_METADATA_HOLD: execution-route hash mismatch in {slug}")
    return row


base.read_slot_meta = safe_read_slot_meta

if __name__ == "__main__":
    base.main()
