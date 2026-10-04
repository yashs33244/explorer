#!/bin/bash
# Put a reference image and our render side by side with labels, to check a diagram against the look it copies.
#   compare.sh reference.png ours.jpg out.jpg ["Reference label"] ["Ours label"]
# Needs uv (uvx fetches Pillow on first use).
set -e
REF="$1"; OURS="$2"; OUT="$3"; LA="${4:-Reference}"; LB="${5:-Ours}"
[ -f "$REF" ] && [ -f "$OURS" ] && [ -n "$OUT" ] || { echo "usage: compare.sh reference.png ours.jpg out.jpg [label] [label]" >&2; exit 1; }
uvx --quiet --with pillow python - "$REF" "$OURS" "$OUT" "$LA" "$LB" <<'PY'
import sys
from PIL import Image, ImageDraw, ImageFont
ref, ours, out, la, lb = sys.argv[1:6]
H = 900
def fit(p):
    im = Image.open(p).convert('RGB')
    return im.resize((max(1, round(im.width * H / im.height)), H), Image.LANCZOS)
a, b = fit(ref), fit(ours)
pad, top = 24, 56
canvas = Image.new('RGB', (a.width + b.width + pad * 3, H + top + pad), (246, 246, 248))
canvas.paste(a, (pad, top)); canvas.paste(b, (a.width + pad * 2, top))
d = ImageDraw.Draw(canvas)
try: font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 26)
except Exception: font = ImageFont.load_default()
d.text((pad, 16), la, fill=(30, 30, 30), font=font); d.text((a.width + pad * 2, 16), lb, fill=(30, 30, 30), font=font)
canvas.save(out, quality=85)
print('wrote', out)
PY
