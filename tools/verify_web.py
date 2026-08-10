#!/usr/bin/env python3
from pathlib import Path
import json
import sys

root = Path(__file__).resolve().parents[1]
web = root / "web"
manifest_path = web / "manifest.json"
index_path = web / "index.html"
sprites_path = web / "sprites.pak"

errors = []

def require(path, label, min_size=1):
    if not path.is_file():
        errors.append(f"{label} absent: {path.relative_to(root)}")
        return
    if path.stat().st_size < min_size:
        errors.append(f"{label} trop petit/vide: {path.relative_to(root)} ({path.stat().st_size} octets)")

require(index_path, "index.html", 100)
require(manifest_path, "manifest.json", 50)
require(sprites_path, "sprites.pak", 1024)

try:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
except Exception as exc:
    errors.append(f"manifest.json invalide: {exc}")
    manifest = {}

builds = manifest.get("builds", [])
if len(builds) != 1:
    errors.append(f"manifest: 1 build attendu, trouvé {len(builds)}")
else:
    build = builds[0]
    if build.get("chipFamily") != "ESP32-S3":
        errors.append(f"manifest chipFamily incorrect: {build.get('chipFamily')!r}")
    parts = build.get("parts", [])
    expected_offsets = [0, 32768, 57344, 65536]
    offsets = [p.get("offset") for p in parts]
    if offsets != expected_offsets:
        errors.append(f"offsets manifest incorrects: {offsets} != {expected_offsets}")
    for part in parts:
        rel = part.get("path", "")
        if not rel:
            errors.append("manifest: part sans path")
            continue
        require(web / rel, f"firmware {rel}", 512)

if index_path.is_file():
    html = index_path.read_text(encoding="utf-8", errors="replace")
    if 'manifest="manifest.json' not in html:
        errors.append("index.html ne référence pas manifest.json")
    if "esp-web-tools" not in html:
        errors.append("index.html ne charge pas ESP Web Tools")

if errors:
    print("ECHEC VERIFICATION WEB:")
    for err in errors:
        print(" -", err)
    sys.exit(1)

print("VERIFICATION WEB OK")
print(" - index.html OK")
print(" - manifest.json OK")
print(" - ESP32-S3 OK")
print(" - offsets firmware OK")
print(" - 4 binaires firmware OK")
print(" - sprites.pak OK")
