#!/usr/bin/env python3
"""List diagram text that runs past the box it sits in.

Renders every diagram-types/*/*/example.svg (or the SVGs you pass) inside the real kit CSS in one style,
finds the smallest box under the start of each title, detail line or label, and reports text whose
right or left edge crosses that box. Exits 1 when anything overflows.

    python3 scripts/check-overflow.py                    # modern style, whole catalog
    python3 scripts/check-overflow.py --style clean
    python3 scripts/check-overflow.py path/to/d1.svg path/to/d2.svg

Needs Python Playwright with Chromium (pip install playwright && playwright install chromium).
Text deliberately placed outside a box, or on a circle, can show up here; read the render before changing it.
"""
import argparse, glob, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.parent
CSS = (HERE.parent / 'assets' / 'style.css').read_text()

MEASURE = '''() => {
  const out = [];
  const boxes = [...document.querySelectorAll('rect.d-box, rect.d-band, rect.d-tag, rect.d-chip, rect.d-lanehead, rect.d-note')]
    .map(r => r.getBoundingClientRect());
  for (const t of document.querySelectorAll('text.d-t, text.d-s, text.d-zt, text.d-mb, text.d-tn, text.d-m')) {
    const b = t.getBoundingClientRect(); if (!b.width) continue;
    const cx = b.left + Math.min(6, b.width / 2), cy = b.top + b.height / 2;
    let best = null;
    for (const r of boxes) if (cx >= r.left && cx <= r.right && cy >= r.top && cy <= r.bottom)
      if (!best || r.width * r.height < best.width * best.height) best = r;
    if (best && (b.right > best.right - 1 || b.left < best.left + 1))
      out.push({ text: t.textContent.slice(0, 48), cls: t.getAttribute('class'), over: Math.round(b.right - best.right) });
  }
  return out;
}'''


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('svgs', nargs='*', help='SVG files; default is every catalog example')
    ap.add_argument('--style', choices=['modern', 'clean', 'hand'], default='modern')
    a = ap.parse_args()
    files = a.svgs or sorted(glob.glob(str(ROOT / 'diagram-types' / '*' / '*' / 'example.svg')))
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit('needs Python Playwright: pip install playwright && playwright install chromium')
    found = {}
    with sync_playwright() as p:
        browser = p.chromium.launch(args=['--no-sandbox'])
        page = browser.new_page(viewport={'width': 900, 'height': 900})
        for f in files:
            svg = Path(f).read_text()
            page.set_content(f'<!doctype html><html data-theme="light" data-dstyle="{a.style}"><head><style>{CSS}</style></head>'
                             f'<body><figure class="fig" style="width:860px"><div class="figscroll">{svg}</div></figure></body></html>')
            page.evaluate('document.fonts.ready')
            hits = page.evaluate(MEASURE)
            if hits:
                found[f] = hits
        browser.close()
    for f, hits in found.items():
        print(f)
        for h in hits:
            print(f"  {h['cls']:<8} {h['over']:>4}px  {h['text']}")
    total = sum(len(h) for h in found.values())
    print(f'{a.style}: {total} overflowing texts in {len(found)} of {len(files)} diagrams')
    sys.exit(1 if total else 0)


if __name__ == '__main__':
    main()
