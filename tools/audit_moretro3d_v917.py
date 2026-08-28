#!/usr/bin/env python3
from pathlib import Path
import json
import re

root = Path(__file__).resolve().parents[1]
ino = (root / "TamaPoke.ino").read_text(encoding="utf-8")
dex = (root / "dex.h").read_text(encoding="utf-8")
pet = (root / "pet.cpp").read_text(encoding="utf-8")
html = (root / "web" / "index.html").read_text(encoding="utf-8")
readme = (root / "README.md").read_text(encoding="utf-8")
manifest = json.loads((root / "web" / "manifest.json").read_text(encoding="utf-8"))
build = (root / "tools" / "build_web.sh").read_text(encoding="utf-8")

def check(value, label):
    if not value:
        raise SystemExit("ECHEC V9.17: " + label)
    print("OK  ", label)

all_public = "\n".join((ino, dex, pet, html, readme, build, json.dumps(manifest)))
check("MIMIKYU" not in all_public.upper() and "MIMIQUI" not in all_public.upper(), "aucune edition Mimiqui")
check("ShadowEnemyx" not in all_public, "aucun ancien lien ShadowEnemyx")
check('uint16_t displayedDexNumber(int16_t dex) { return dex; }' in ino, "numeros nationaux 001-386")
check('"JIRACHI"' in dex, "Jirachi restaure au numero 385")
check("{ 1, 4, 7 }" in ino and "{ 152, 155, 158 }" in ino and "{ 252, 255, 258 }" in ino,
      "neuf starters 1G/2G/3G")
check("starterName=dexName" in ino, "noms des trois starters affiches")
check("STARTER_COLORS[3]" in ino and "// plante" in ino and "// feu" in ino and "// eau" in ino,
      "couleurs Plante vert, Feu rouge, Eau bleu")
check("panel->setBrightness(0)" in ino and "gfx->flush();\n  panel->setBrightness(120);" in ino,
      "splash complet avant allumage AMOLED")
check("if (!screenOff) return false;" in ino, "aucun light-sleep ecran visible")
check("if (now - lastPwr > 60)" in ino and "markUiDirty();\n          render();" in ino,
      "reveil PWR rapide avec frame complet")
check(manifest["name"] == "TamaPoke Moretro3D - V9.17 Normal", "manifest Moretro3D")
check(manifest["version"] == "1.42.0-moretro3d-v9.17-normal", "version Web coherente")
check('VERSION="1.42.0-moretro3d-v9.17-normal"' in build, "version de compilation coherente")
check("TamaPoke Moretro3D" in html and "Installer le firmware Moretro3D" in html,
      "page firmware Moretro3D")
check("Moretro3D/Test-1" in readme, "page GitHub Moretro3D/Test-1")
check(not re.search(r"\b(Care for|Could not|Connect the board|Done \()", html), "page utilisateur entierement en francais")
print("AUDIT MORETRO3D V9.17 OK")
