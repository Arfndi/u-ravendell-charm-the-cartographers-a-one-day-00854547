"""u-ravendell-charm-the-cartographers-a-one-day-00854547 entry: treasure map.

The map is a hand-drawn-style treasure map of a fictional island, with six
legible place labels: Skull Rock, Whispering Bay, The Sunken Galleon, Palm
Grove, Dead Man's Cove, and X Marks the Spot. The picture was generated
fresh for this entry and is shipped beside this program as entry.png
(1024x683 JPEG, under the 1 MiB gate). This program does no drawing and
needs no network: it copies the image shipped beside it.
"""

import hashlib
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
SOURCE = os.path.join(HERE, "entry.png")
DESTINATION = os.path.join(OUT, "entry.png")

# SHA-256 of the shipped entry.png, so a corrupted copy fails loudly.
EXPECTED_SHA256 = "8d81ca2a9da1320b152a5bd4f19e7dc3b2cd471a4b1a730a01cb82ca41061403"


def main():
    os.makedirs(OUT, exist_ok=True)
    shutil.copyfile(SOURCE, DESTINATION)
    verify_copy()


def _sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_copy():
    """Fail loudly instead of silently shipping a bad copy.

    The gate rejects a truncated or corrupted entry, so confirm the
    shipped image is the expected one, the output is byte-identical
    to it, and the output still starts with the JPEG SOI marker.
    """
    if _sha256(SOURCE) != EXPECTED_SHA256:
        raise SystemExit("shipped entry.png is not the expected image")
    with open(DESTINATION, "rb") as f:
        magic = f.read(2)
    if magic != b"\xff\xd8":
        raise SystemExit("entry.png output is not a JPEG (bad SOI marker)")
    if os.path.getsize(DESTINATION) > 1048576:
        raise SystemExit("entry.png output exceeds the 1 MiB gate")
    if _sha256(SOURCE) != _sha256(DESTINATION):
        raise SystemExit("entry.png output differs from the shipped image")


if __name__ == "__main__":
    main()
