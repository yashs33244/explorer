#!/bin/bash
# Render with headless Chrome so you can LOOK at the result (Read the PNG).
#   render.sh diagram.svg out.png|out.jpg [light|dark] [hand|clean]   one SVG inside the real page CSS, sized to fit, 2x
#   render.sh --page page.html out.png [width] [height]  the top of a built page
#   render.sh --section page.html id out.png [width] [height] [light|dark] [hand|clean]   one section of a built page, alone
#   render.sh --catalog                                  re-render every diagram-types/*/*/hand.jpg and clean.jpg
# Needs Google Chrome and node. Set CHROME=/path/to/chrome to override.
# .jpg output also needs sips (macOS) or ImageMagick (magick); .png needs neither. A .jpg is scaled to 1200px wide.
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
CSS="$HERE/../assets/style.css"
CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
TMP="${TMPDIR:-/tmp}/explorer-render-$$"; mkdir -p "$TMP"; trap 'rm -rf "$TMP"' EXIT
DEFS="$(cat "$HERE/../assets/filters.svg")"
FONTS='<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700&family=Figtree:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap">'
shot() { "$CHROME" --headless=new --disable-gpu --hide-scrollbars --window-size="$2" --virtual-time-budget=6000 --screenshot="$3" "file://$1" >/dev/null 2>&1; }
case "$1" in
  --catalog)
    DT="$HERE/../../../diagram-types"
    node -e 'for (const t of require(process.argv[1])) console.log(t.category + "/" + t.slug)' "$DT/catalog.json" | while read -r D; do
      "$0" "$DT/$D/example.svg" "$DT/$D/hand.jpg" light hand && "$0" "$DT/$D/example.svg" "$DT/$D/clean.jpg" light clean
    done
    exit 0 ;;
  --page)
    { echo '<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body style="margin:0">'; cat "$2"; echo '</body></html>'; } > "$TMP/page.html"
    OUT="$3"; shot "$TMP/page.html" "${4:-1300},${5:-1600}" "$OUT" ;;
  --section)
    SEC=$(node -e 'const s=require("fs").readFileSync(process.argv[1],"utf8");const i=s.indexOf("<section class=\"topic\" id=\""+process.argv[2]+"\"");if(i<0){console.error("no section "+process.argv[2]);process.exit(1)}const j=s.indexOf("</section>",i);process.stdout.write(s.slice(i,j+10))' "$2" "$3")
    OUT="$4"; THEME="${7:-light}"
    { echo "<!doctype html><html data-theme=\"$THEME\" data-dstyle=\"${8:-hand}\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">$FONTS<style>"; cat "$CSS"; echo "</style></head><body>$DEFS<div class=\"shell\" style=\"display:block\"><main class=\"main\">$SEC</main></div></body></html>"; } > "$TMP/section.html"
    shot "$TMP/section.html" "${5:-1300},${6:-1100}" "$OUT" ;;
  *)
    SVG="$1"; OUT="$2"; THEME="${3:-light}"; STYLE="${4:-hand}"
    # the figure is 860px wide; the window height follows the viewBox so there is no empty band below
    H=$(node -e 'const s=require("fs").readFileSync(process.argv[1],"utf8");const m=s.match(/viewBox="\s*[-\d.]+[ ,]+[-\d.]+[ ,]+([\d.]+)[ ,]+([\d.]+)/);if(!m){console.error("no viewBox");process.exit(1)}console.log(Math.ceil(830*m[2]/m[1])+62)' "$SVG")
    node "$HERE/logos.js" "$SVG" "$TMP/in.svg"
    { echo "<!doctype html><html data-theme=\"$THEME\" data-dstyle=\"$STYLE\"><head><meta charset=\"utf-8\">$FONTS<style>"; cat "$CSS"; echo 'body{padding:14px;margin:0}.fig{width:860px;padding:14px 15px}.fig svg,.fig svg.hd{max-height:none;max-width:none;min-width:0;width:830px}</style></head><body>'; echo "$DEFS"; echo '<figure class="fig"><div class="figscroll">'; cat "$TMP/in.svg"; echo '</div></figure></body></html>'; } > "$TMP/diagram.html"
    case "$OUT" in
      *.jpg|*.jpeg) "$CHROME" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=2 --window-size="888,$H" --virtual-time-budget=8000 --screenshot="$TMP/shot.png" "file://$TMP/diagram.html" >/dev/null 2>&1
        if command -v sips >/dev/null; then sips -s format jpeg -s formatOptions 82 --resampleWidth 1200 "$TMP/shot.png" --out "$OUT" >/dev/null
        elif command -v magick >/dev/null; then magick "$TMP/shot.png" -resize 1200x -quality 82 "$OUT"
        else echo "jpg output needs sips (macOS) or ImageMagick (magick); render a .png instead" >&2; exit 1; fi ;;
      *) "$CHROME" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=2 --window-size="888,$H" --virtual-time-budget=8000 --screenshot="$OUT" "file://$TMP/diagram.html" >/dev/null 2>&1 ;;
    esac ;;
esac
[ -s "$OUT" ] && echo "rendered $OUT" || { echo "render failed (is Chrome installed? set CHROME=...)" >&2; exit 1; }
