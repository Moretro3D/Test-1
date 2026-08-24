#!/usr/bin/env python3
"""Crée le paquet USB des sprites et de la miniature Mimiqui."""
from pathlib import Path
import struct


root = Path(__file__).resolve().parents[1]
mons = root / "tools" / "sdcard" / "mons"
output = root / "web" / "mimikyu.pak"
names = ("p385.bin", "ps385.bin", "thumbs.bin")
entries = [(f"mons/{name}", (mons / name).read_bytes()) for name in names]

with output.open("wb") as stream:
    stream.write(b"TPAK")
    stream.write(struct.pack("<H", len(entries)))
    for name, data in entries:
        encoded = name.encode("utf-8")
        stream.write(struct.pack("<B", len(encoded)))
        stream.write(encoded)
        stream.write(struct.pack("<I", len(data)))
    for _, data in entries:
        stream.write(data)

print(f"{output}: sprites normal/shiny + miniature Mimiqui, {output.stat().st_size} octets")
