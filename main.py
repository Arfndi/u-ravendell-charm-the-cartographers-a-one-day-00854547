"""Treasure-map entry for u-ravendell-charm-the-cartographers-a-one-day-00854547.

The island map shipped with this program (entry.png, a 1024x683 JPEG)
shows a fictional island with six readable place names: Skull Rock,
Whispering Bay, The Sunken Galleon, Palm Grove, Dead Man's Cove, and
X Marks the Spot. Running this file copies that picture to
/output/entry.png. No drawing happens here and nothing is fetched
from the network.
"""

import hashlib
import os
import shutil
import sys

ENTRY = "entry.png"
EXPECTED = "8d81ca2a9da1320b152a5bd4f19e7dc3b2cd471a4b1a730a01cb82ca41061403"
MAX_BYTES = 1_048_576


def fail(message):
    print(f"entry check failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def file_sha256(path):
    hasher = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            block = handle.read(1 << 16)
            if not block:
                break
            hasher.update(block)
    return hasher.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, ENTRY)
    target_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(target_dir, exist_ok=True)
    target = os.path.join(target_dir, ENTRY)
    if file_sha256(source) != EXPECTED:
        fail("shipped entry.png does not match its recorded hash")
    shutil.copyfile(source, target)
    with open(target, "rb") as handle:
        head = handle.read(2)
    if head != b"\xff\xd8":
        fail("copied entry.png is not a JPEG file")
    if os.path.getsize(target) > MAX_BYTES:
        fail("copied entry.png is larger than the 1 MiB limit")
    if file_sha256(target) != EXPECTED:
        fail("copied entry.png differs from the shipped image")
    print(f"wrote {target} ({os.path.getsize(target)} bytes)")


if __name__ == "__main__":
    main()
