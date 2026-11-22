#!/usr/bin/env python3
"""Publish the 22 November 2026 front page to /output/entry.png.

The picture itself -- "The World in One Page" for Sunday 22 November
2026 -- was drawn ahead of time by render.py and is stored in this
repository as entry.png. All that is left for the entry program is to
deliver that file, unchanged, to the output directory.

Delivery is deliberately boring: standard library only, no network,
no clock, no randomness. The bytes are checked against the PNG
signature and the competition's size cap, staged under a temporary
name inside the output directory, flushed to disk, and then moved
into place with os.replace, so the published file is never observed
half-written and two runs leave identical bytes behind.
"""

import hashlib
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
ASSET = os.path.join(ROOT, "entry.png")
DEST_DIR = "/output"
DEST = os.path.join(DEST_DIR, "entry.png")
SIGNATURE = b"\x89PNG\r\n\x1a\n"
SIZE_CAP = 1048576  # 1 MiB, the largest image the contest accepts


def load_asset():
    with open(ASSET, "rb") as fh:
        blob = fh.read()
    if not blob.startswith(SIGNATURE):
        raise SystemExit("entry.png is missing its PNG signature")
    if len(blob) > SIZE_CAP:
        raise SystemExit("entry.png is larger than the 1 MiB cap")
    return blob


def deliver(blob):
    os.makedirs(DEST_DIR, exist_ok=True)
    staging = os.path.join(DEST_DIR, ".staging-entry.png")
    with open(staging, "wb") as fh:
        fh.write(blob)
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(staging, DEST)


def report(blob):
    digest = hashlib.sha256(blob).hexdigest()
    print(f"published {DEST} -- {len(blob)} bytes, sha256 {digest}")


if __name__ == "__main__":
    payload = load_asset()
    deliver(payload)
    report(payload)
    sys.exit(0)
