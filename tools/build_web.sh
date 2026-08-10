#!/bin/bash
# Build TamaPoke pour le Web Flasher.
# Le sketch est copié dans un dossier temporaire nommé "TamaPoke"
# afin qu'Arduino CLI trouve toujours TamaPoke.ino, quel que soit
# le nom du dépôt GitHub (ex: Test-1).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

FQBN="esp32:esp32:esp32s3:CDCOnBoot=cdc,FlashSize=16M,PSRAM=opi,PartitionScheme=app3M_fat9M_16MB"
VERSION="1.29.1-moretro-ui1"

echo "Préparation du sketch TamaPoke..."
TMP="$(mktemp -d "${TMPDIR:-/tmp}/tamapoke-ci.XXXXXX")"
trap 'rm -rf "$TMP"' EXIT

SKETCH="$TMP/TamaPoke"
BUILD="$TMP/build"
mkdir -p "$SKETCH" "$BUILD" "$ROOT/web/firmware"

# Arduino exige que le fichier .ino principal porte le même nom que
# le dossier du sketch. On copie donc toutes les sources dans TamaPoke/.
cp "$ROOT/TamaPoke.ino" "$SKETCH/TamaPoke.ino"
cp "$ROOT"/*.cpp "$SKETCH/" 2>/dev/null || true
cp "$ROOT"/*.h   "$SKETCH/" 2>/dev/null || true

echo "Compilation..."
arduino-cli compile \
  --fqbn "$FQBN" \
  --build-path "$BUILD" \
  "$SKETCH"

echo "Copie des binaires pour le Web Flasher..."
cp "$BUILD/TamaPoke.ino.bootloader.bin" "$ROOT/web/firmware/tamapoke-$VERSION-bootloader.bin"
cp "$BUILD/TamaPoke.ino.partitions.bin" "$ROOT/web/firmware/tamapoke-$VERSION-partitions.bin"
cp "$BUILD/boot_app0.bin" "$ROOT/web/firmware/tamapoke-$VERSION-boot_app0.bin"
cp "$BUILD/TamaPoke.ino.bin" "$ROOT/web/firmware/tamapoke-$VERSION-app.bin"

echo "Firmware OK."
ls -lh "$ROOT/web/firmware/tamapoke-$VERSION-app.bin"

echo "Empaquetage des sprites..."
python3 "$ROOT/tools/pack_bundle.py"

echo "BUILD TERMINE"
