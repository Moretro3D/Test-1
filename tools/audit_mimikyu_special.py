#!/usr/bin/env python3
from pathlib import Path
import re
import struct
import sys


root = Path(__file__).resolve().parents[1]
errors = []


def check(ok, message):
    print(("OK   " if ok else "FAIL ") + message)
    if not ok:
        errors.append(message)


dex = (root / "dex.h").read_text(encoding="utf-8")
pet = (root / "pet.cpp").read_text(encoding="utf-8")
ino = (root / "TamaPoke.ino").read_text(encoding="utf-8")
i18n = (root / "i18n.cpp").read_text(encoding="utf-8")
html = (root / "web" / "index.html").read_text(encoding="utf-8")

check('"MIMIKYU", 0, 0, R_EVO' in dex and "TYPE_GHOST, TYPE_FAIRY" in dex,
      "slot spécial Mimiqui Spectre/Fée sans évolution")
check("firstPartner ? 385 : pickEggSpecies()" in pet and "starterPick = false" in pet,
      "premier œuf Mimiqui sans écran starter")
check('dex == 385 ? 778 : dex' in ino, "affichage numéro national 778")
check('dex == 385' in i18n and '"MIMIQUI"' in i18n, "nom français Mimiqui")
check('id="special"' in html and "mimikyu.pak?" in html, "bouton USB Mimiqui")

for name in ("p385.bin", "ps385.bin"):
    path = root / "tools" / "sdcard" / "mons" / name
    raw = path.read_bytes() if path.is_file() else b""
    check(raw[:4] == b"TPK2" and len(raw) > 50000, f"sprite animé {name}")

pack = root / "web" / "mimikyu.pak"
raw = pack.read_bytes() if pack.is_file() else b""
check(raw[:4] == b"TPAK" and len(raw) > 200000, "paquet USB Mimiqui")

if errors:
    print(f"AUDIT MIMIQUI ÉCHEC: {len(errors)} erreur(s)")
    sys.exit(1)
print("AUDIT MIMIQUI OK")
