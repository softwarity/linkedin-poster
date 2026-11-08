#!/usr/bin/env bash
# Builds meerkat-cluster.gif from the SVG. Needs Docker only.
set -euo pipefail
cd "$(dirname "$0")"
python3 make-svg.py
docker run --rm -v "$PWD:/work" -w /work mcr.microsoft.com/playwright:v1.61.1-noble \
  sh -c "npm i --no-save --silent playwright@1.61.1 >/dev/null 2>&1 && node render.mjs meerkat-cluster.svg .frames"
docker run --rm -v "$PWD:/work" linuxserver/ffmpeg -loglevel error -y -framerate 12 -i /work/.frames/f%03d.png \
  -vf "fps=12,split[a][b];[a]palettegen=max_colors=96[p];[b][p]paletteuse=dither=none" -loop 0 /work/meerkat-cluster.gif
rm -rf .frames node_modules package.json package-lock.json
echo meerkat-cluster.gif
