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
        raise SystemExit("ECHEC V9.19.1: " + label)
    print("OK  ", label)

all_public = "\n".join((ino, dex, pet, html, readme, build, json.dumps(manifest)))
check("MIMIKYU" not in all_public.upper() and "MIMIQUI" not in all_public.upper(), "aucune edition Mimiqui")
check("ShadowEnemyx" not in all_public, "aucun ancien lien ShadowEnemyx")
check('uint16_t displayedDexNumber(int16_t dex) { return dex; }' in ino, "numeros nationaux 001-386")
check('"JIRACHI"' in dex, "Jirachi restaure au numero 385")
check("{ 1, 4, 7 }" in ino and "{ 152, 155, 158 }" in ino and "{ 252, 255, 258 }" in ino,
      "neuf starters 1G/2G/3G")
check("starterLanguageChosen" in ino and "LANGUAGE / LANGUE" in ino, "choix de langue avant generation")
check("starterName=dexName" in ino, "noms des trois starters affiches")
check("STARTER_COLORS[3]" in ino and "// plante" in ino and "// feu" in ino and "// eau" in ino,
      "couleurs Plante vert, Feu rouge, Eau bleu")
check('gfx->setCursor(CX - 72, 176); gfx->print("PokeTama")' in ino and
      'gfx->setCursor(CX - 81, 224); gfx->print("Moretro3D")' in ino and
      'drawStarterCentered("PokeTama", 48, 3' in ino and
      'drawStarterCentered("Moretro3D", 86, 2' in ino,
      "marque centree au demarrage et sur la langue")
check(ino.count("gfx->fillRoundRect(82,392,302,52,14,UI_TRACK)") == 2 and
      ino.count("x >= 82 && x <= 384 && y >= 392 && y <= 444") == 2,
      "boutons retour centres en bas")
check("gfx->fillScreen(UI_WHITE);" in ino and
      "drawStarterThumbCentered(th, CX, 190, 8)" in ino and
      "gfx->fillRoundRect(50,392,176,52,14,UI_TRACK)" in ino and
      "gfx->fillRoundRect(240,392,176,52,14,UI_BAR_OK)" in ino,
      "fiche starter blanche plein ecran")
check("panel->setBrightness(0)" in ino and "gfx->flush();\n  panel->setBrightness(120);" in ino,
      "splash complet avant allumage AMOLED")
check("if (!screenOff) return false;" in ino, "aucun light-sleep ecran visible")
check("if (now - lastPwr > 60)" in ino and "markUiDirty();\n          render();" in ino,
      "reveil PWR rapide avec frame complet")
check("starterPick ? 1 : pickEggSpecies()" in pet and "if (starterPick) return" in pet,
      "aucune eclosion aleatoire avant choix")
check("speciesId = dex" in (root / "pet.h").read_text(encoding="utf-8") and
      "dexCaught[(dex - 1) >> 3]" in (root / "pet.h").read_text(encoding="utf-8"),
      "starter installe directement sans oeuf")
check("speciesId == 133 && caughtTotal <= 1" in pet,
      "ancienne sauvegarde Evoli reparee")
check("case 252: case 255: case 258:" in (root / "pet.h").read_text(encoding="utf-8") and
      "case 133" not in (root / "pet.h").read_text(encoding="utf-8"), "Evoli refuse comme starter")
check(manifest["name"] == "PokeTama Moretro3D - V9.19.1", "manifest Moretro3D")
check(manifest["version"] == "1.44.1-moretro3d-v9.19.1-brand-center", "version Web coherente")
check('VERSION="1.44.1-moretro3d-v9.19.1-brand-center"' in build, "version de compilation coherente")
check("PokeTama Moretro3D" in html and "Installer le firmware Moretro3D" in html,
      "page firmware Moretro3D")
check("Moretro3D/Test-1" in readme, "page GitHub Moretro3D/Test-1")
check(not re.search(r"\b(Care for|Could not|Connect the board|Done \()", html), "page utilisateur entierement en francais")
print("AUDIT MORETRO3D V9.19.1 OK")
