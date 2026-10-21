# Shared by stills.sh and render.sh: locate daybook reel and check its setup.
REEL="${DAYBOOK_REEL:-}"
if [ -z "$REEL" ]; then
  echo "set DAYBOOK_REEL to your daybook reel checkout to use the Studio engine, or use the Manim engine in manim/" >&2
  exit 1
fi
if [ ! -f "$REEL/src/studio.ts" ]; then
  echo "daybook reel with the Studio composition not found at $REEL (set DAYBOOK_REEL)" >&2
  exit 1
fi
if [ ! -d "$REEL/node_modules" ] || [ ! -d "$REEL/render/node_modules" ]; then
  echo "installing reel dependencies (one time)" >&2
  (cd "$REEL" && bun install --frozen-lockfile) && (cd "$REEL/render" && npm ci)
fi
