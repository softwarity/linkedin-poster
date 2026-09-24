#!/usr/bin/env bash
# Sends one post to the Worker: send-draft.sh posts/<project>/<slug>/<lang>.txt
# The image, if any, is the image.{gif,png,jpg} next to it, described by alt.<lang>.txt (or alt.txt).
set -euo pipefail
post=$1

case "$post" in posts/*/*/??.txt) ;; *) echo "::error::post must match posts/<project>/<slug>/<lang>.txt: $post"; exit 1 ;; esac
test -f "$post" || { echo "::error::$post not found"; exit 1; }
dir=$(dirname "$post")
project=$(echo "$post" | cut -d/ -f2)
work=$(mktemp -d)

jq -n --rawfile text "$post" --arg project "$project" '{text: ($text | rtrimstr("\n")), project: $project}' > "$work/payload.json"

image=$(ls "$dir"/image.* 2>/dev/null | head -1 || true)
if [ -n "$image" ]; then
  base64 -w0 "$image" > "$work/image.b64"
  lang=$(basename "$post" .txt)
  alt=$(cat "$dir/alt.$lang.txt" 2>/dev/null || cat "$dir/alt.txt" 2>/dev/null || echo "$project")
  jq --rawfile data "$work/image.b64" --arg type "$(file -b --mime-type "$image")" --arg alt "$alt" \
    '.image = {data: $data, type: $type, alt: ($alt | rtrimstr("\n"))}' "$work/payload.json" > "$work/p.json"
  mv "$work/p.json" "$work/payload.json"
fi

echo "Sending $post"
curl -sS --fail-with-body -X POST "$WORKER_URL/drafts" \
  -H "Authorization: Bearer $WORKER_SHARED_SECRET" \
  -H "Content-Type: application/json" \
  --data-binary @"$work/payload.json" | jq .
