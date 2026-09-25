#!/usr/bin/env bash
# Builds app-gateway.<lang>.gif from the SVGs. Needs Docker only.
set -euo pipefail
cd "$(dirname "$0")"
python3 make-svg.py
for lang in fr en; do
  docker run --rm -v "$PWD:/work" -w /work mcr.microsoft.com/playwright:v1.61.1-noble \
    sh -c "npm i --no-save --silent playwright@1.61.1 >/dev/null 2>&1 && node render.mjs app-gateway.$lang.svg .frames-$lang"
  # Two-pass palette: sharp text, small file (LinkedIn accepts up to 250 frames).
  docker run --rm -v "$PWD:/work" linuxserver/ffmpeg -loglevel error -y -framerate 12 -i /work/.frames-$lang/f%03d.png \
    -vf "fps=12,split[a][b];[a]palettegen=max_colors=64[p];[b][p]paletteuse=dither=none" -loop 0 /work/app-gateway.$lang.gif
  rm -rf ".frames-$lang"
  echo "app-gateway.$lang.gif"
done
rm -rf node_modules package.json package-lock.json
