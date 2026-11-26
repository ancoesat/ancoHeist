#!/usr/bin/env bash
# Build TTF, OTF and WOFF2 from the UFO source.
set -euo pipefail
cd "$(dirname "$0")/.."

UFO=sources/AncoHeist-Black.ufo
rm -rf fonts && mkdir -p fonts/ttf fonts/otf fonts/webfonts

fontmake -u "$UFO" -o ttf --output-dir fonts/ttf --flatten-components
fontmake -u "$UFO" -o otf --output-dir fonts/otf --flatten-components

python3 - <<'EOF'
from fontTools.ttLib import TTFont
f = TTFont("fonts/ttf/AncoHeist-Black.ttf")
f.flavor = "woff2"
f.save("fonts/webfonts/AncoHeist-Black.woff2")
print("woff2 done")
EOF
ls -la fonts/*/
