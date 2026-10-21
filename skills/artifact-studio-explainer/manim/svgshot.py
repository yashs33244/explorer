"""
Render a kit SVG to high-res PNGs with headless Chrome, inside the artifact page CSS.

    .venv/bin/python svgshot.py svg/KEY.svg [--width 4000]

One PNG per data-step state: state N shows the [data-step] groups with a step
number <= N (the rest get visibility:hidden, so the layout never moves), plus
"all" with nothing hidden. Output goes to manim/cache/figures/<hash>/ and is
reused while the svg, the page CSS, the width and this script stay the same.
Prints a JSON map {state: png path}.

Chrome: $CHROME if set, else the macOS app, else google-chrome, chromium and
friends on PATH.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
MAC_CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
CHROME_NAMES = ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser")
TEMPLATE = HERE.parent.parent / "artifact-studio" / "assets" / "page-template.html"
CACHE = HERE / "cache" / "figures"
CACHE_WARN = 500 * 1024 * 1024   # bytes, print the cache path and size past this
MAX_PIXELS = 120_000_000         # widest render is lowered so width * height stays under this
VERSION = "svgshot-2"
FONTS = (("Figtree", "Figtree.ttf"), ("Bricolage Grotesque", "BricolageGrotesque.ttf"),
         ("JetBrains Mono", "JetBrainsMono.ttf"))
FONTS_LINK = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:'
              'opsz,wght@12..96,500;12..96,700&family=Figtree:wght@400;500;600;700&family='
              'JetBrains+Mono:wght@400;500&display=swap">')


def chrome() -> str:
    """Path of the Chrome or Chromium binary. Raises RuntimeError naming $CHROME."""
    env = os.environ.get("CHROME")
    if env:
        found = env if os.path.isfile(env) and os.access(env, os.X_OK) else shutil.which(env)
        if not found:
            raise RuntimeError(f"CHROME={env!r} is not an executable file; point $CHROME at Chrome or Chromium")
        return found
    if os.path.isfile(MAC_CHROME):
        return MAC_CHROME
    for name in CHROME_NAMES:
        found = shutil.which(name)
        if found:
            return found
    raise RuntimeError("figure scenes need Google Chrome or Chromium and none was found "
                       f"(looked for {MAC_CHROME} and {', '.join(CHROME_NAMES)} on PATH); "
                       "install one or set $CHROME=/path/to/chrome")


def require() -> None:
    """Fails early, with a clear message, when a figure render cannot work here."""
    chrome()
    page_css()


def page_css() -> str:
    if not TEMPLATE.is_file():
        raise RuntimeError(f"figure scenes need the artifact-studio skill next to this one; missing {TEMPLATE} "
                           "(install artifact-studio too, or clone the whole repo)")
    html = TEMPLATE.read_text()
    m = re.search(r"<style>(.*?)</style>", html, re.S)
    if not m:
        raise RuntimeError(f"no <style> block in {TEMPLATE}")
    return m.group(1)


def viewbox(svg_text: str) -> tuple[float, float, float, float]:
    m = re.search(r"<svg\b[^>]*?\bviewBox\s*=\s*[\"']([^\"']+)[\"']", svg_text, re.S)
    if m:
        nums = [float(v) for v in re.split(r"[\s,]+", m.group(1).strip())]
        if len(nums) == 4 and nums[2] > 0 and nums[3] > 0:
            return tuple(nums)  # type: ignore[return-value]
    # only plain numbers (or px) count; "100%" and other units say nothing about the box
    w = re.search(r"<svg\b[^>]*?\bwidth\s*=\s*[\"']\s*([\d.]+)\s*(?:px)?\s*[\"']", svg_text, re.S)
    h = re.search(r"<svg\b[^>]*?\bheight\s*=\s*[\"']\s*([\d.]+)\s*(?:px)?\s*[\"']", svg_text, re.S)
    if w and h and float(w.group(1)) > 0 and float(h.group(1)) > 0:
        return 0.0, 0.0, float(w.group(1)), float(h.group(1))
    raise ValueError("svg has no usable viewBox; add viewBox=\"0 0 W H\" to the <svg> tag "
                     "(width and height in % or other units do not give its size)")


def steps(svg_text: str) -> list[int]:
    return sorted({int(v) for v in re.findall(r"data-step\s*=\s*[\"'](\d+)[\"']", svg_text)})


def cap_width(width: int, vw: float, vh: float) -> int:
    """width, lowered for tall figures so the PNG stays under MAX_PIXELS."""
    return max(1, min(int(width), int((MAX_PIXELS * vw / vh) ** 0.5)))


def allow_pixels() -> None:
    """Lets PIL open renders up to MAX_PIXELS without a decompression bomb error."""
    from PIL import Image
    if Image.MAX_IMAGE_PIXELS is not None and Image.MAX_IMAGE_PIXELS < MAX_PIXELS:
        Image.MAX_IMAGE_PIXELS = MAX_PIXELS


def image_size(svg_text: str, width: int) -> tuple[int, int]:
    _, _, vw, vh = viewbox(svg_text)
    width = cap_width(width, vw, vh)
    return width, max(1, round(width * vh / vw))


def _html(svg_text: str, css: str, w: int, h: int, hide: list[int]) -> str:
    local = all((HERE / "fonts" / f).is_file() for _, f in FONTS)
    fonts = "".join(
        f'@font-face{{font-family:"{fam}";src:url("{(HERE / "fonts" / f).as_uri()}");font-weight:100 900;}}'
        for fam, f in FONTS) if local else ""
    link = "" if local else FONTS_LINK   # the committed fonts keep renders offline; Google Fonts is the fallback
    hide_css = "".join(f'svg [data-step="{n}"]{{visibility:hidden !important;}}' for n in hide)
    svg = re.sub(r"<\?xml[^>]*\?>", "", svg_text)
    return (f'<!doctype html><html><head><meta charset="utf-8">{link}<style>{css}</style><style>{fonts}'
            f'html,body{{margin:0;padding:0;background:#fff;width:{w}px;height:{h}px;overflow:hidden;}}'
            f'body>svg{{display:block;width:{w}px !important;height:{h}px !important;max-width:none !important;'
            f'max-height:none !important;margin:0 !important;}}'
            f'svg *{{transition:none !important;animation:none !important;}}{hide_css}</style></head>'
            f'<body>{svg}</body></html>')


def _shoot(html: str, w: int, h: int, out: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="svgshot-") as td:
        page = Path(td) / "page.html"
        page.write_text(html)
        tmp_png = Path(td) / "shot.png"
        cmd = [chrome(), "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
               "--no-default-browser-check", "--allow-file-access-from-files",
               f"--user-data-dir={Path(td) / 'profile'}", "--force-device-scale-factor=1",
               f"--window-size={w},{h}", "--virtual-time-budget=6000", "--default-background-color=FFFFFFFF",
               f"--screenshot={tmp_png}", page.as_uri()]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        if r.returncode != 0 or not tmp_png.exists():
            raise RuntimeError(f"chrome screenshot failed: {r.stderr.strip()[-800:]}")
        from PIL import Image
        allow_pixels()
        # write beside the final path, then rename: an interrupted save never leaves a cached half PNG
        part = out.with_name(f".{out.stem}.{os.getpid()}.{threading.get_ident()}.png")
        try:
            with Image.open(tmp_png) as im:
                if im.size != (w, h):
                    # chrome can trim a few px off the window; pad or crop back to the exact size
                    canvas = Image.new("RGB", (w, h), "white")
                    canvas.paste(im.convert("RGB").crop((0, 0, min(w, im.width), min(h, im.height))), (0, 0))
                    canvas.save(part, format="PNG")
                else:
                    im.convert("RGB").save(part, format="PNG")
            os.replace(part, out)
        finally:
            part.unlink(missing_ok=True)


def _warn_cache_size() -> None:
    total = sum(p.stat().st_size for p in CACHE.rglob("*.png") if p.is_file())
    if total > CACHE_WARN:
        print(f"svgshot: figure cache is {total / 1024 ** 2:.0f} MB at {CACHE}; delete it to free space "
              "(renders are redone on demand)", file=sys.stderr)


def shoot(svg_path: Path, width: int = 4000) -> dict[str, Path]:
    """All states of one svg as PNGs, cached. Keys: "all", "0", "1", ..."""
    svg_text = Path(svg_path).read_text()
    css = page_css()
    allow_pixels()
    nsteps = steps(svg_text)
    w, h = image_size(svg_text, width)
    key = hashlib.sha256("\0".join([VERSION, svg_text, css, str(w)]).encode()).hexdigest()[:20]
    folder = CACHE / key
    states = {"all": []}
    if nsteps:
        for n in [0] + nsteps:
            states[str(n)] = [s for s in nsteps if s > n]
    paths = {k: folder / f"state-{k}.png" for k in states}
    todo = [k for k, p in paths.items() if not p.exists()]
    if todo:
        chrome()   # a missing browser fails here once, not in every worker
        folder.mkdir(parents=True, exist_ok=True)
        with ThreadPoolExecutor(max_workers=min(4, len(todo))) as pool:
            list(pool.map(lambda k: _shoot(_html(svg_text, css, w, h, states[k]), w, h, paths[k]), todo))
        _warn_cache_size()
    return paths


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print(__doc__, file=sys.stderr)
        sys.exit(2)
    width = int(args[args.index("--width") + 1]) if "--width" in args else 4000
    got = shoot(Path(args[0]), width)
    print(json.dumps({k: str(v) for k, v in got.items()}, indent=1))
