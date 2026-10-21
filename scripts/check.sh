#!/bin/bash
# Repo gate: run before every push. Exits non-zero on the first failure.
#   catalog files and links, the example page, the repo map example, python and shell syntax, no em dash.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TMP="${TMPDIR:-/tmp}/explorer-check-$$"; mkdir -p "$TMP"; trap 'rm -rf "$TMP"' EXIT
AS="$ROOT/skills/artifact-studio"

echo "1. catalog"
node "$ROOT/skills/codebase-explorer/scripts/build-catalog.js"

echo "2. example page"
python3 "$AS/scripts/build.py" --title Basic --body "$AS/examples/basic/body.html" --svg "$AS/examples/basic/svg" \
  --figs "$AS/examples/basic/figs.json" --out "$TMP/basic.html" 2> "$TMP/warn.txt"
if [ -s "$TMP/warn.txt" ]; then cat "$TMP/warn.txt"; echo "the example page must build with no warnings" >&2; exit 1; fi

echo "3. repo map example is up to date"
RM="$ROOT/diagram-types/technical/repo-map"
python3 "$AS/scripts/repo_map.py" "$RM/spec.json" > "$TMP/rm.svg" 2>/dev/null
cmp -s "$TMP/rm.svg" "$RM/example.svg" || { echo "example.svg is stale: rerun repo_map.py spec.json > example.svg" >&2; exit 1; }

echo "4. python and shell syntax"
EX="$ROOT/skills/artifact-studio-explainer"
PYTHONPYCACHEPREFIX="$TMP/pycache" python3 -m py_compile "$AS/scripts/build.py" "$AS/scripts/repo_map.py" "$EX"/manim/*.py "$EX"/scripts/*.py
for f in "$EX"/manim/*.sh "$EX"/scripts/*.sh; do bash -n "$f"; done

echo "5. no em dash"
if git -C "$ROOT" ls-files -z --cached --others --exclude-standard -- '*.md' '*.html' '*.py' '*.js' '*.json' '*.css' '*.sh' '*.svg' \
   | xargs -0 grep -l $'\xe2\x80\x94' 2>/dev/null; then echo "em dash found in the files above" >&2; exit 1; fi

echo "all checks passed"
