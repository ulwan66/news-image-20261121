#!/usr/bin/env python3
"""Copy the pre-rendered front page to /output/entry.png (Python 3.13, stdlib only).

The image beside this file sums up the world news of Saturday 21 November
2026; the program copies it, byte for byte, so both graded runs are identical.
Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import hashlib
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def _check_png(path):
    """The shipped image must be a whole PNG within the gate's caps."""
    with open(path, "rb") as f:
        head = f.read(33)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("entry.png is not a PNG")
    if head[12:16] != b"IHDR":
        raise SystemExit("entry.png has no IHDR chunk")
    width = int.from_bytes(head[16:20], "big")
    height = int.from_bytes(head[20:24], "big")
    if width > 1024 or height > 1024:
        raise SystemExit("entry.png is larger than 1024x1024")
    if os.path.getsize(path) > 1048576:
        raise SystemExit("entry.png is larger than 1 MiB")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    _check_png(src)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    # Self-check: the copy must match the shipped image exactly, so both
    # graded runs write identical bytes (size and hash, not just size).
    if os.path.getsize(src) != os.path.getsize(dst):
        raise SystemExit("entry.png copy size mismatch")
    if _sha256(src) != _sha256(dst):
        raise SystemExit("entry.png copy hash mismatch")


if __name__ == "__main__":
    main()
