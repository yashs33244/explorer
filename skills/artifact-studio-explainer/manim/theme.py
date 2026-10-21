"""
artifact-studio light theme as Manim constants.

Tokens mirror the :root block of ../artifact-studio/assets/page-template.html.
Every size in this engine is in 1920x1080 screen pixels; px() converts to
manim units at the last moment. Text is set with Text only (no LaTeX).
"""

from __future__ import annotations

import logging
from pathlib import Path

import numpy as np

# ---------- frame ----------
FPS = 30
WIDTH = 1920
HEIGHT = 1080
# manim's default frame is 8 units tall, so one pixel is 8/1080 units.
PX = 8.0 / HEIGHT
MARGIN = 48          # side margin, px
TOP = 48             # top margin, px
CAPTION_H = 104      # bottom caption bar height, px
MIN_TEXT = 22        # smallest text on a 1080p frame, px

# ---------- colours ----------
BG = "#ffffff"
INK = "#1e1e1e"
MUTED = "#5c5c5c"
FAINT = "#e2e2e2"
LINE = "#e6e6e6"
SOFT = "#f7f7f8"
CODE_BG = "#f6f7f9"
ACC = "#1f7aec"
ACC_SOFT = "#e8f1fe"
OK = "#1b8a5a"
OK_SOFT = "#e3f6ec"
WARN = "#9a6400"
WARN_SOFT = "#fff4d6"
TODO = "#b3372a"
TODO_SOFT = "#fde8e4"
HIGHLIGHT = "#fff1b8"

# group fills (--clN-f), tints (--clN-t), deep strokes (--clN-d)
GROUP_FILL = ["#dcb8ff", "#74dfb0", "#ffd43b", "#ff9d8c", "#8ec3ff", "#ffb45e"]
GROUP_TINT = ["#f0e2ff", "#d2f6e5", "#fff1b8", "#ffdcd5", "#d8eaff", "#ffe3c2"]
GROUP_DEEP = ["#b57cff", "#2ec98a", "#ffc21a", "#ff6f5e", "#3a9eff", "#ff9933"]
# darker title ink per group, readable on white (deep tones are too light for text)
GROUP_INK = ["#7a3fcf", "#16794f", "#8a6400", "#b3372a", "#1f63c4", "#a65300"]

# ---------- fonts ----------
FONT_DIR = Path(__file__).resolve().parent / "fonts"
FONT_FILES = {
    "Figtree": "Figtree.ttf",
    "Bricolage Grotesque": "BricolageGrotesque.ttf",
    "JetBrains Mono": "JetBrainsMono.ttf",
}
FALLBACKS = {
    "Figtree": ["Helvetica Neue", "Helvetica", "Sans"],
    "Bricolage Grotesque": ["Figtree", "Avenir Next", "Helvetica Neue", "Sans"],
    "JetBrains Mono": ["JetBrainsMono Nerd Font Mono", "Menlo", "Monaco", "Monospace"],
}
BODY = "Figtree"
DISPLAY = "Bricolage Grotesque"
MONO = "JetBrains Mono"

# manim Text: font_size 48 draws a 90 px em (measured with Figtree cap height).
FONT_SIZE_PER_PX = 48.0 / 90.0
# stroke_width 1 is 1.35 px on a 1080p frame.
PX_PER_STROKE = 1.35

_resolved: dict[str, str] = {}


def register_fonts() -> dict[str, str]:
    """Register the bundled fonts with pango and map each role to a family.

    Must run before the first Text is built: manim caches the font list on
    first use. A missing file falls back to the first installed alternative.
    """
    if _resolved:
        return _resolved
    import manimpango

    for family, fname in FONT_FILES.items():
        path = FONT_DIR / fname
        if path.exists() and manimpango.register_font(str(path)):
            _resolved[family] = family
    installed = set(manimpango.list_fonts())
    for family in FONT_FILES:
        if family in _resolved:
            continue
        if family in installed:
            _resolved[family] = family
            continue
        alt = next((f for f in FALLBACKS[family] if f in installed), "Sans")
        logging.warning("font %s not found, using %s (run setup.sh to copy fonts)", family, alt)
        _resolved[family] = alt
    # manim warns about fonts it cannot see in its cached list; ours are fine.
    logging.getLogger("manim").setLevel(logging.ERROR)
    return _resolved


def family(name: str) -> str:
    return register_fonts().get(name, name)


def px(value: float) -> float:
    return value * PX


def font_size(em_px: float) -> float:
    return max(em_px, MIN_TEXT) * FONT_SIZE_PER_PX


def stroke(px_width: float) -> float:
    return px_width / PX_PER_STROKE


def at(x_px: float, y_px: float) -> np.ndarray:
    """Screen pixels (origin top-left, y down) to a manim point."""
    return np.array([(x_px - WIDTH / 2) * PX, (HEIGHT / 2 - y_px) * PX, 0.0])


def to_px(point: np.ndarray) -> tuple[float, float]:
    return point[0] / PX + WIDTH / 2, HEIGHT / 2 - point[1] / PX
