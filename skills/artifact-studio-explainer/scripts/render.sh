#!/bin/bash
# Voice, align and render: <folder>/studio-out/explainer.mp4. Extra flags pass
# through to reel's studio.ts (--voice am_michael, --no-voice, --out x.mp4).
set -euo pipefail
DIR="$(cd "${1:?usage: render.sh <folder with storyboard.json> [flags]}" && pwd)"
shift
source "$(dirname "$0")/_reel.sh"
cd "$REEL" && bun run src/studio.ts "$DIR/storyboard.json" --out-dir "$DIR/studio-out" "$@"
