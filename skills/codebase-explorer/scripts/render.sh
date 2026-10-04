#!/bin/bash
# Render with headless Chrome so you can LOOK at the result (Read the PNG).
#   render.sh diagram.svg out.png [light|dark]         one SVG inside the real page CSS
#   render.sh --page page.html out.png [width] [height]  the top of a built page
#   render.sh --section page.html id out.png [width] [height] [light|dark]   one section of a built page, alone
# Needs Google Chrome and node. Set CHROME=/path/to/chrome to override.
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
CSS="$HERE/../assets/style.css"
CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
TMP="${TMPDIR:-/tmp}/explorer-render"; mkdir -p "$TMP"
FONTS='<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700&family=Figtree:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap">'
shot() { "$CHROME" --headless=new --disable-gpu --hide-scrollbars --window-size="$2" --virtual-time-budget=6000 --screenshot="$3" "file://$1" >/dev/null 2>&1; }
case "$1" in
  --page)
    { echo '<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body style="margin:0">'; cat "$2"; echo '</body></html>'; } > "$TMP/page.html"
    OUT="$3"; shot "$TMP/page.html" "${4:-1300},${5:-1600}" "$OUT" ;;
  --section)
    SEC=$(node -e 'const s=require("fs").readFileSync(process.argv[1],"utf8");const i=s.indexOf("<section class=\"topic\" id=\""+process.argv[2]+"\"");if(i<0){console.error("no section "+process.argv[2]);process.exit(1)}const j=s.indexOf("</section>",i);process.stdout.write(s.slice(i,j+10))' "$2" "$3")
    OUT="$4"; THEME="${7:-light}"
    { echo "<!doctype html><html data-theme=\"$THEME\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">$FONTS<style>"; cat "$CSS"; echo "</style></head><body><div class=\"shell\" style=\"display:block\"><main class=\"main\">$SEC</main></div></body></html>"; } > "$TMP/section.html"
    shot "$TMP/section.html" "${5:-1300},${6:-1100}" "$OUT" ;;
  *)
    SVG="$1"; OUT="$2"; THEME="${3:-light}"
    { echo "<!doctype html><html data-theme=\"$THEME\"><head><meta charset=\"utf-8\">$FONTS<style>"; cat "$CSS"; echo 'body{padding:16px}</style></head><body><figure class="fig"><div class="figscroll">'; cat "$SVG"; echo '</div></figure></body></html>'; } > "$TMP/diagram.html"
    shot "$TMP/diagram.html" "900,1000" "$OUT" ;;
esac
[ -s "$OUT" ] && echo "rendered $OUT" || { echo "render failed (is Chrome installed? set CHROME=...)" >&2; exit 1; }
