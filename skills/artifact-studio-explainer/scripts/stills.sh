#!/bin/bash
# One PNG per scene (everything revealed), no voice: <folder>/studio-out/stills/
set -euo pipefail
DIR="$(cd "${1:?usage: stills.sh <folder with storyboard.json>}" && pwd)"
source "$(dirname "$0")/_reel.sh"
cd "$REEL" && bun run src/studio.ts "$DIR/storyboard.json" --out-dir "$DIR/studio-out" --stills
