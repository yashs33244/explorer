#!/usr/bin/env bash
# Isolated Manim Community env for the explainer's Manim engine.
# Python 3.12 is pinned because newer system Pythons may have no wheels.
# Needs: uv, ffmpeg, cairo and pango, and Chrome or Chromium for figure scenes.
#   macOS: brew install uv ffmpeg cairo pango pkgconf
#   Linux: apt install ffmpeg libcairo2-dev libpango1.0-dev pkg-config espeak-ng (and uv, Chrome or Chromium)
# Tested on macOS. Linux should work with Chrome or Chromium and espeak-ng, but is not tested.
# No LaTeX: the engine uses Text only.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"

for bin in uv ffmpeg; do
  command -v "$bin" >/dev/null || { echo "missing $bin: brew install $bin (or apt install $bin)" >&2; exit 1; }
done

# cairo and pango: manim builds pycairo and manimpango against them when no wheel fits.
if command -v pkg-config >/dev/null; then
  for lib in cairo pango; do
    pkg-config --exists "$lib" || echo "warning: pkg-config cannot find $lib: brew install $lib (or apt install lib${lib}*-dev)" >&2
  done
else
  echo "warning: no pkg-config, cannot check cairo and pango: brew install pkgconf cairo pango (or apt install pkg-config libcairo2-dev libpango1.0-dev)" >&2
fi

# Chrome renders figure scenes (svgshot.py): $CHROME, then the macOS app, then one on PATH.
CHROME_BIN="${CHROME:-}"
MAC_CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
if [ -z "$CHROME_BIN" ] && [ -x "$MAC_CHROME" ]; then CHROME_BIN="$MAC_CHROME"; fi
if [ -z "$CHROME_BIN" ]; then
  for b in google-chrome google-chrome-stable chromium chromium-browser; do
    if command -v "$b" >/dev/null; then CHROME_BIN="$(command -v "$b")"; break; fi
  done
fi
if [ -z "$CHROME_BIN" ]; then
  echo "warning: no Chrome or Chromium found; figure scenes need one. Install it or set CHROME=/path/to/chrome" >&2
fi

if [ ! -x .venv/bin/python ]; then
  uv venv --python 3.12 .venv
fi
VIRTUAL_ENV="$HERE/.venv" uv pip install --python .venv/bin/python manim==0.22.0

# Fonts are committed in fonts/. This copy is only a fallback for a checkout without them.
# theme.py falls back to system fonts if none is found.
SRC_DIRS=()
[ -n "${DAYBOOK_REEL:-}" ] && SRC_DIRS+=("$DAYBOOK_REEL/render/public/fonts/studio")
for f in Figtree.ttf BricolageGrotesque.ttf JetBrainsMono.ttf; do
  [ -f "fonts/$f" ] && continue
  for d in ${SRC_DIRS[@]+"${SRC_DIRS[@]}"}; do
    if [ -f "$d/$f" ]; then mkdir -p fonts; cp "$d/$f" fonts/; cp "$d"/OFL-*.txt fonts/ 2>/dev/null || true; break; fi
  done
  [ -f "fonts/$f" ] || echo "note: $f not found; text falls back to a system font" >&2
done

.venv/bin/python -c "import manim, manimpango; print('manim', manim.__version__)"
echo "ok: run .venv/bin/python render.py <storyboard.json>"
