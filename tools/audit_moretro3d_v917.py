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
        raise SystemExit("ECHEC V9.20: " + label)
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
check('gfx->setCursor(CX - 72, 238); gfx->print("PokeTama")' in ino and
      'gfx->setCursor(CX - 81, 280); gfx->print("Moretro3D")' in ino and
      'drawStarterCentered("PokeTama", 48, 3' in ino and
      'drawStarterCentered("Moretro3D", 86, 2' in ino,
      "marque centree au demarrage et sur la langue")
check('#include "brand_logo.h"' in ino and
      'drawBrandLogo(CX - BRAND_LOGO_W / 2, 36)' in ino and
      (root / "brand_logo.h").is_file() and
      (root / "assets" / "moretro3d-logo-transparent.png").is_file(),
      "logo Moretro3D transparent embarque au demarrage")
check(ino.count("gfx->fillRoundRect(96,368,274,46,14,UI_TRACK)") == 2 and
      ino.count("x >= 96 && x <= 370 && y >= 368 && y <= 414") == 2,
      "boutons retour centres et remontes dans le rond")
check("drawStarterCentered(T(S_CHOOSE_GENERATION), 92, 1, UI_INK)" in ino and
      "drawStarterCentered(generation, gy + 22, 2, UI_INK)" in ino and
      "drawStarterCentered(generation, 112, 2, UI_INK)" in ino,
      "titres de generation noirs")
check("gfx->fillScreen(UI_WHITE);" in ino and
      "drawStarterThumbCentered(th, CX, 190, 8)" in ino and
      "gfx->fillRoundRect(84,358,140,50,14,UI_TRACK)" in ino and
      "gfx->fillRoundRect(242,358,140,50,14,UI_BAR_OK)" in ino,
      "fiche starter blanche adaptee a l'ecran rond")
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
check(manifest["name"] == "PokeTama Moretro3D - V9.20", "manifest Moretro3D")
check(manifest["version"] == "1.45.0-moretro3d-v9.20-brand-logo", "version Web coherente")
check('VERSION="1.45.0-moretro3d-v9.20-brand-logo"' in build, "version de compilation coherente")
check("PokeTama Moretro3D" in html and "Installer le firmware Moretro3D" in html,
      "page firmware Moretro3D")
check("Moretro3D/Test-1" in readme, "page GitHub Moretro3D/Test-1")
check(not re.search(r"\b(Care for|Could not|Connect the board|Done \()", html), "page utilisateur entierement en francais")
print("AUDIT MORETRO3D V9.20 OK")
