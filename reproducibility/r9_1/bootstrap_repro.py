#!/usr/bin/env python3
"""Materialize the CSA R9.1 reviewer reproducibility snapshot from payload.b64."""
from __future__ import annotations
import base64, hashlib, io, sys, zipfile
from pathlib import Path

EXPECTED_SHA256 = "c6959a485564eecdbe14fe1347bb53622463c59ce7838bf34acd80e8fd79f59c"

def safe_extract(zf: zipfile.ZipFile, dest: Path) -> None:
    root = dest.resolve()
    for info in zf.infolist():
        target = (dest / info.filename).resolve()
        if root != target and root not in target.parents:
            raise RuntimeError(f"unsafe archive path: {info.filename}")
    zf.extractall(dest)

def main() -> int:
    here = Path(__file__).resolve().parent
    b64_path = here / "payload.b64"
    if not b64_path.exists():
        print("payload.b64 is missing", file=sys.stderr)
        return 2
    payload = base64.b64decode(b64_path.read_text(encoding="ascii"))
    got = hashlib.sha256(payload).hexdigest()
    if got != EXPECTED_SHA256:
        print(f"PAYLOAD_SHA256=FAIL expected={EXPECTED_SHA256} got={got}", file=sys.stderr)
        return 2
    dest = here / "r9_1_repro"
    dest.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(io.BytesIO(payload)) as zf:
        safe_extract(zf, dest)
    print(f"PAYLOAD_SHA256=PASS {got}")
    print(f"EXTRACTED_TO={dest}")
    print("See README.md for the reviewer commands.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
