#!/usr/bin/env python3
"""Installe Mimiqui #778 dans l'emplacement interne 385 de l'édition spéciale."""
from pathlib import Path
import shutil
import struct

import make_thumbs
import pack_pmd


root = Path(__file__).resolve().parents[1]
mons = root / "tools" / "sdcard" / "mons"
thumbs_path = mons / "thumbs.bin"


def thumbnail_blob(sprite_path: Path) -> bytes:
    w, h, palette, data = make_thumbs.read_pmd_idle_frame0(sprite_path)
    nw, nh, new_palette, new_data = make_thumbs.shrink(w, h, palette, data)
    return (struct.pack("<3B", nw, nh, len(new_palette)) +
            struct.pack(f"<{len(new_palette)}H", *new_palette) + new_data)


def replace_thumbnail(slot: int, blob: bytes) -> None:
    raw = thumbs_path.read_bytes()
    if raw[:4] != b"TPTH":
        raise RuntimeError("thumbs.bin invalide")
    count = struct.unpack_from("<H", raw, 4)[0]
    if count < slot:
        print(f"Miniature Mimiqui différée: thumbs.bin contient seulement {count} entrées")
        return
    offsets = struct.unpack_from(f"<{count}I", raw, 6)
    blobs = []
    for index, offset in enumerate(offsets):
        end = offsets[index + 1] if index + 1 < count else len(raw)
        blobs.append(raw[offset:end])
    blobs[slot - 1] = blob
    header_size = 6 + count * 4
    new_offsets = []
    position = header_size
    for item in blobs:
        new_offsets.append(position)
        position += len(item)
    with thumbs_path.open("wb") as stream:
        stream.write(b"TPTH")
        stream.write(struct.pack("<H", count))
        stream.write(struct.pack(f"<{count}I", *new_offsets))
        for item in blobs:
            stream.write(item)


for shiny in (False, True):
    pack_pmd.pack(778, shiny)
    source = mons / f"p{'s' if shiny else ''}778.bin"
    target = mons / f"p{'s' if shiny else ''}385.bin"
    shutil.copyfile(source, target)
    source.unlink()

replace_thumbnail(385, thumbnail_blob(mons / "p385.bin"))
print("Édition spéciale: Mimiqui #778 installé dans le slot interne 385")
