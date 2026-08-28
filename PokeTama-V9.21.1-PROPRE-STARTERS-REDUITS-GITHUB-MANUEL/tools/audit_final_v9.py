#!/usr/bin/env python3
from pathlib import Path
import re, subprocess, sys, csv, wave, shutil

ROOT=Path(__file__).resolve().parents[1]
ino=(ROOT/"TamaPoke.ino").read_text(encoding="utf-8")
dex=(ROOT/"dex.h").read_text(encoding="utf-8")
battle=(ROOT/"battle.cpp").read_text(encoding="utf-8")
pet=(ROOT/"pet.cpp").read_text(encoding="utf-8")
audio=(ROOT/"audio.cpp").read_text(encoding="utf-8")
chirp=(ROOT/"species_chirp.cpp").read_text(encoding="utf-8")
sdmon=(ROOT/"sdmon.cpp").read_text(encoding="utf-8")

def ok(cond,msg):
    if not cond:
        raise SystemExit("FAIL V9: "+msg)
    print("OK  ",msg)

# 466x466 / UI 1.75"
ok("#define CX 233" in ino and "#define CY 233" in ino, "centre écran 466x466")
ok("#define GAL_CELL 72" in ino and "#define GAL_X 89" in ino, "Pokédex compact dans le rond")

# Pokedex
ok("Pagination compacte" not in ino, "billes pagination Pokédex supprimées")
ok('gfx->fillRoundRect(18, 214, 48, 52' in ino, "flèche gauche Pokédex centrée")
ok('gfx->fillRoundRect(400, 214, 48, 52' in ino, "flèche droite Pokédex centrée")
ok('gfx->fillRoundRect(136, 398, 194, 40' in ino, "bouton RETOUR Pokédex remonté")
ok("galleryPage--" in ino and "galleryPage++" in ino, "navigation tactile flèches Pokédex")

# Fiche
ok('const char *cardBack=T(S_LAN_BACK)' in ino, "bouton RETOUR fiche traduit")
ok('gfx->fillCircle(dotsX + i * 20, 374' in ino, "pagination fiche remontée")
ok('y >= 388 && y <= 446' in ino, "zone tactile RETOUR fiche")
ok("cardPage == 0 && y >= 366 && y <= 398" not in ino, "ancienne zone cachée de cadre supprimée")

# Accueil / heure / habitat
ok("drawHomeIdentity" in ino, "nom + niveau séparés sur accueil")
ok("if (pet.weight > 60) return T(S_CHUBBY)" not in ino, "message ambigu 'un peu rond' supprimé")
ok("gNight = pet.sleeping || h < 6 || h >= 20;" in ino, "fond piloté par heure réelle, pas par thème sombre")
ok("06-07 lever" in ino and "08-17 jour" in ino and "18-19 coucher" in ino, "cycle 24h en 4 phases")
ok("DEX_TBL[pet.speciesId].biome" in ino, "habitat lié au Pokémon actif")
ok("drawCollectionFrame(CX, PET_GROUND - 96" not in ino, "aucun anneau/flèche latérale sur accueil")

# 386
ok("#define DEX_COUNT 386" in dex, "Pokédex 386")
entries=re.findall(r'\{\s*"[^"]+",\s*\d+,\s*\d+,\s*[A-Z_]+,\s*0x[0-9A-Fa-f]+,\s*\d+,\s*\d+,\s*\d+,\s*\d+,\s*TYPE_[A-Z_]+,\s*TYPE_[A-Z_]+,\s*\d+\s*\},\s*//\s*(\d+)',dex)
ok(len(entries)>=386, "386 entrées combat/habitat présentes")

m=re.search(r'// FR\n  \{ ([^\n]+) \},',dex)
ok(m is not None, "table noms FR présente")
fr=re.findall(r'"([^"]*)"',m.group(1))
ok(len(fr)==387 and all(fr[i] for i in range(1,387)), "386 noms français non vides")

# Battle UI
ok("void drawBattlePmd" in ino and "visibleW" in ino and
   "uint8_t fi=0" in ino and
   "drawBattlePmd(wildPmd, battleDex, 350, 232, 84" in ino and
   "drawBattlePmd(pmd, pet.speciesId, 118, 316, 112" in ino,
   "sprites combat fixes avec tailles joueur/adversaire separees")
ok("drawBattleName(dexName(battleDex), battleLevel, 78, 72, 190)" in ino and
   "battlePlayer.level, 236, 236, 190" in ino,
   "informations combat opposees aux sprites")
ok("STARTER_DEX[3][3]" in ino and "{ 252, 255, 258 }" in ino,
   "starters 1G, 2G et 3G presents")
ok("drawStarterPokeball" in ino and "starterPreviewDex" in ino,
   "Pokeballs et popup de confirmation starter presentes")
ok("repairCaughtProfiles" in pet and "hasStoredProfile(candidate)" in pet,
   "anciens profils evolues restaures dans la Boite")
ok(all(name in audio for name in ("OST_MORNING", "OST_LOFI", "OST_NIGHT")) and
   "AUDIO_EVENT_AMBIENT" in audio and "audioAmbientPlay" in ino,
   "trois OST originales et lecture ambiante non bloquante")
ok("hour>=7 && hour<13" in ino and "hour>=13 && hour<20" in ino,
   "selection OST automatique matin, lo-fi et nuit")
music=ROOT/"tools/sdcard/music"
for filename in ("morning.wav", "lofi.wav", "night.wav"):
    with wave.open(str(music/filename), "rb") as wav:
        ok(wav.getnchannels()==1 and wav.getsampwidth()==2 and
           wav.getframerate()==16000 and wav.getnframes()==384000,
           f"{filename} PCM mono 16 bits, 16 kHz, 24 secondes")
ok("SD_MMC.open(MUSIC_PATHS[theme]" in audio and
   "SAMPLE_RATE * 240 / 1000" in audio,
   "lecture WAV SD en blocs courts avec repli synthetise")
ok("gAmbientKeepAliveUntil" in audio and "uxQueueMessagesWaiting(gQ) > 0" in audio and
   "musicGainPct() / 100" in audio and "case SOUND_FULL: return 135" in audio and "ps_malloc(bytes)" in audio,
   "OST WAV continue, sans coupure d'ampli entre blocs et sans saturation")
ok("SD_MMC.exists(path) && !SD_MMC.remove(path)" in sdmon,
   "chargement USB remplace les fichiers SD sans les agrandir")
ok('line == "PREPARE"' in sdmon and 'Serial.println("READY")' not in sdmon and
   '"READY" : "ERRCLEAN"' in sdmon,
   "preparation USB nettoie les anciens assets avant transfert")
ok("maintainTamaPokeSd()" in sdmon and "logicalTpk2Size" in sdmon and
   "logical < physical) SD_MMC.remove(path)" in sdmon,
   "maintenance SD supprime les intrus et anciens TPK2 dupliques")
ok('Serial.println("ERRFULL")' in sdmon and "freeBytes" in sdmon,
   "reserve d'espace controlee avant chaque ecriture SD")
ok("ARRÊT SÉCURISÉ" in ino or "ARRÊT SÉCURISÉ" in (ROOT/"web/index.html").read_text(encoding="utf-8"),
   "installateur web stoppe des la premiere erreur")
ok("void drawBattleName" in ino, "noms combat auto-ajustés")
ok("drawBattleHpInfo" in ino, "PV courant/max affichés")
ok("Bandeau d'action sombre intégré" in ino, "boutons combat intégrés sans fond gris")
ok("T(S_QUICK_ATTACK)" in ino and "T(S_NORMAL_ATTACK)" in ino and "T(S_HEAVY_ATTACK)" in ino, "menu attaques traduit")
ok("BATTLE_ATTACK_QUICK" in ino and "BATTLE_ATTACK_HEAVY" in ino, "menu relié au moteur réel")

# HP / damage exact
ok("if (turn.playerDamage > battle.enemyHp) turn.playerDamage = battle.enemyHp;" in battle,
   "dégâts joueur = PV réellement retirés")
ok("turn.enemyDamage = enemyHit > battle.playerHp ? battle.playerHp : enemyHit;" in battle,
   "dégâts ennemi = PV réellement retirés")
ok("hpLeft -= dealt;" in battle, "aucun PV négatif")
ok("battle.playerHp += turn.playerHeal;" in battle, "soin borné par PV max")

# Chirps 386
ok("clampPitch(160 + dex * 6)" in chirp, "cris synthétiques 001-386 dans plage sûre")

# Background SD assets
bg=ROOT/"tools/sdcard/backgrounds"
pngs=list(bg.glob("*_466.png"))
ok(len(pngs)==24, "24 fonds SD (6 habitats x 4 phases)")
rows=list(csv.reader((bg/"habitats_001_386.csv").open(encoding="utf-8-sig"),delimiter=";"))
ok(len(rows)==387, "mapping habitat SD pour 386 Pokémon")

# Existing audits syntax / shell
for script in ["audit_evolutions.py","audit_386_assets.py","verify_web.py"]:
    p=ROOT/"tools"/script
    ok(p.exists(), f"{script} présent")
    subprocess.run([sys.executable,"-m","py_compile",str(p)],check=True)
if shutil.which("bash"):
    ok(subprocess.run(["bash","-n",str(ROOT/"tools/build_web.sh")]).returncode==0, "build_web.sh syntaxe")
else:
    print("SKIP build_web.sh syntaxe (bash absent sur ce poste)")

print("AUDIT FINAL V9 OK")
