#!/usr/bin/env python3
"""Entry program for news-image-20261122.

Publishes this repository's front page -- "The World in One Page" for
Sunday 22 November 2026 -- to /output/entry.png.

The artwork is committed next to this file as entry.png (drawn at build
time by render.py), so this program only has to copy it, byte for byte.
That keeps the entry fully deterministic: no network, no clock, no
randomness, nothing beyond the Python standard library. Run it twice
and both runs write exactly the same bytes.

The copy goes through a temporary file in the same directory and is
then renamed over the target, so a reader never sees a half-written
image even if a run is interrupted.
"""

import hashlib
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
OUTPUT_DIR = "/output"
OUTPUT = os.path.join(OUTPUT_DIR, "entry.png")

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1024 * 1024  # the competition's 1 MiB cap


def read_source():
    with open(SOURCE, "rb") as fh:
        data = fh.read()
    if not data.startswith(PNG_MAGIC):
        raise SystemExit("entry.png beside main.py is not a PNG image")
    if len(data) > MAX_BYTES:
        raise SystemExit("entry.png exceeds the 1 MiB size cap")
    return data


def publish(data):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    tmp = os.path.join(OUTPUT_DIR, ".entry.png.part")
    with open(tmp, "wb") as fh:
        fh.write(data)
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, OUTPUT)


def png_dimensions(data):
    """Width and height from the PNG IHDR chunk, or None if absent."""
    if len(data) < 24 or data[12:16] != b"IHDR":
        return None
    return struct.unpack(">II", data[16:24])


def main():
    data = read_source()
    publish(data)
    digest = hashlib.sha256(data).hexdigest()
    dims = png_dimensions(data)
    size = f"{dims[0]}x{dims[1]}" if dims else "unknown size"
    print(f"wrote {OUTPUT}: {len(data)} bytes, {size}, sha256 {digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
