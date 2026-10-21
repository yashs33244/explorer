"""
The "figure" layout: the artifact's real kit diagram (or a list of PNG frames),
full screen, with camera moves and a red highlighter. No manim import here, so
render.py can validate a storyboard without loading manim.

Coordinates:
  - svg figures: focus and mark rects are "x,y,w,h" in the svg viewBox units
    (negative viewBox origins are handled).
  - frame figures: rects are in the frame's own pixels.

Each video frame is composed directly from the high-res source: the current
camera window (a rect in source pixels) is resampled with Lanczos straight to
the drawing area, so text stays sharp at any zoom the source allows.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from pathlib import Path

FIG_ACTIONS = ("step", "focus", "mark", "all", "frame")
MOVE = 1.0          # s, camera move
FADE = 0.5          # s, crossfade between states or frames
DRAW = 0.45         # s, highlighter draw in
OUT = 0.3           # s, highlighter fade out
FOCUS_FILL = 0.8    # the focus rect fills this share of the drawing area
MAX_ZOOM = 3.0      # never zoom in more than this over the whole figure: deeper loses context
EDGE = 0.04         # a mark this close to the view edge counts as outside it
MAX_UPSCALE = 1.2   # screen px per source px, never zoom past this (keeps text sharp)
BASE_WIDTH = 4000   # px, default svg render width
MAX_WIDTH = 8000    # px, widest svg render
EDGE_FADE = 14      # px, white fade at the drawing area edges

# drawing area on the 1920x1080 frame (px)
PAD = 32
SIDE = 64           # px left and right of a figure: room to breathe beside dense diagrams
HEAD_H = 56
CAPTION_H = 104


class FigureError(ValueError):
    pass


def area(scene: dict) -> tuple[int, int, int, int]:
    top = PAD + (HEAD_H if (scene.get("heading") or scene.get("kicker")) else 0)
    bottom = 1080 - CAPTION_H - 16
    return SIDE, top, 1920 - 2 * SIDE, bottom - top


def parse_rect(target, sid: str, action: str) -> tuple[float, float, float, float]:
    parts = [p for p in re.split(r"[\s,]+", str(target or "").strip()) if p]
    try:
        nums = [float(p) for p in parts]
    except ValueError:
        nums = []
    if len(nums) != 4 or not all(math.isfinite(n) for n in nums) or nums[2] <= 0 or nums[3] <= 0:
        raise FigureError(f"scene {sid}: {action} target must be \"x,y,w,h\" with w and h above 0, got {target!r}")
    return nums[0], nums[1], nums[2], nums[3]


@dataclass
class Source:
    kind: str                                  # "svg" or "frames"
    paths: list[Path]
    vb: tuple[float, float, float, float]      # coordinate box of the rects (viewBox, or 0,0,w,h)
    steps: list[int] = field(default_factory=list)
    size: tuple[int, int] = (0, 0)             # source image size (px), set once rendered


def load_source(scene: dict, base: Path) -> Source:
    """Checks the files and returns what the figure is drawn from. Raises FigureError."""
    sid = scene.get("id")
    svg, frames = scene.get("svg_file"), scene.get("frames")
    if bool(svg) == bool(frames):
        raise FigureError(f"scene {sid}: figure needs exactly one of svg_file or frames")
    if svg:
        p = (base / svg).resolve()
        if not p.is_file():
            raise FigureError(f"scene {sid}: svg_file not found: {p}")
        import svgshot
        text = p.read_text()
        try:
            vb = svgshot.viewbox(text)
        except ValueError as e:
            raise FigureError(f"scene {sid}: {p.name}: {e}") from None
        try:
            svgshot.require()
        except RuntimeError as e:
            raise FigureError(f"scene {sid}: {e}") from None
        return Source("svg", [p], vb, svgshot.steps(text))
    if not isinstance(frames, list) or not all(isinstance(f, str) for f in frames):
        raise FigureError(f"scene {sid}: frames must be a list of png paths")
    paths = [(base / f).resolve() for f in frames]
    missing = [str(p) for p in paths if not p.is_file()]
    if missing:
        raise FigureError(f"scene {sid}: frame file not found: {', '.join(missing)}")
    from PIL import Image
    sizes = set()
    for p in paths:
        with Image.open(p) as im:
            sizes.add(im.size)
    if len(sizes) > 1:
        raise FigureError(f"scene {sid}: frames differ in size {sorted(sizes)}; use one size")
    w, h = sizes.pop()
    return Source("frames", paths, (0.0, 0.0, float(w), float(h)), size=(w, h))


def check_steps(scene: dict, src: Source, steps: list[dict]) -> None:
    """Validates every figure action against the source. steps: [{action, target}]."""
    sid = scene.get("id")
    vx, vy, vw, vh = src.vb
    # svgshot renders a state for 0 and for each data-step value, so only those are valid targets
    valid = [0] + [n for n in src.steps if n != 0]
    if "start_step" in scene:
        if src.kind != "svg" or not src.steps:
            raise FigureError(f"scene {sid}: start_step needs an svg with data-step groups")
        s0 = scene["start_step"]
        if isinstance(s0, bool) or not isinstance(s0, int) or s0 not in valid:
            raise FigureError(f"scene {sid}: start_step must be one of {valid}, got {s0!r}")
    for st in steps:
        a, t = st.get("action"), st.get("target")
        if a not in FIG_ACTIONS:
            raise FigureError(f"scene {sid}: figure action must be one of {FIG_ACTIONS}, got {a!r}")
        if a == "step":
            if src.kind != "svg" or not src.steps:
                raise FigureError(f"scene {sid}: step needs an svg with data-step groups; this figure has none")
            if isinstance(t, bool) or not isinstance(t, int) and not (isinstance(t, str) and t.isdigit()):
                raise FigureError(f"scene {sid}: step target must be a number, got {t!r}")
            if int(t) not in valid:
                raise FigureError(f"scene {sid}: step {t} is not a data-step in the svg; use one of {valid}")
        elif a == "frame":
            if src.kind != "frames":
                raise FigureError(f"scene {sid}: frame needs a frames list, this figure is an svg")
            if isinstance(t, bool) or not isinstance(t, int) and not (isinstance(t, str) and t.isdigit()):
                raise FigureError(f"scene {sid}: frame target must be a number, got {t!r}")
            if not 1 <= int(t) <= len(src.paths):
                raise FigureError(f"scene {sid}: frame {t} is out of range (1 to {len(src.paths)})")
        elif a in ("focus", "mark"):
            x, y, w, h = parse_rect(t, sid, a)
            tol = 0.02 * max(vw, vh)
            if x < vx - tol or y < vy - tol or x + w > vx + vw + tol or y + h > vy + vh + tol:
                raise FigureError(f"scene {sid}: {a} rect {t!r} is outside the figure "
                                  f"(box {vx:g},{vy:g},{vw:g},{vh:g})")


def svg_width(scene: dict, src: Source, steps: list[dict]) -> int:
    """Render width so the tightest focus lands near 1 screen px per source px."""
    _, _, aw, ah = area(scene)
    need = BASE_WIDTH
    for st in steps:
        if st.get("action") == "focus":
            _, _, w, h = parse_rect(st["target"], scene.get("id"), "focus")
            screen_per_unit = min(aw * FOCUS_FILL / w, ah * FOCUS_FILL / h)
            need = max(need, math.ceil(src.vb[2] * screen_per_unit))
    import svgshot
    return svgshot.cap_width(min(MAX_WIDTH, need), src.vb[2], src.vb[3])


# ---------- timeline ----------

def smooth(t: float) -> float:
    t = min(1.0, max(0.0, t))
    return t * t * (3 - 2 * t) if t < 1 else 1.0


def ease(t: float) -> float:
    """ease in out cubic"""
    t = min(1.0, max(0.0, t))
    return 4 * t ** 3 if t < 0.5 else 1 - (-2 * t + 2) ** 3 / 2


@dataclass
class View:
    cx: float
    cy: float
    w: float          # window width in source px; height follows the drawing area aspect


@dataclass
class Move:
    t0: float
    dur: float
    a: View
    b: View


@dataclass
class Marker:
    rect: tuple[float, float, float, float]   # source px
    t_in: float
    t_out: float = math.inf


@dataclass
class Fade:
    t0: float
    a: str
    b: str


class Timeline:
    def __init__(self, scene: dict, src: Source, steps: list[dict], duration: float):
        self.ax, self.ay, self.aw, self.ah = area(scene)
        self.aspect = self.aw / self.ah
        self.src = src
        iw, ih = src.size
        self.iw, self.ih = iw, ih
        self.k = iw / src.vb[2]                   # source px per rect unit
        self.full = View(iw / 2, ih / 2, max(iw, ih * self.aspect))
        self.min_w = self.aw / MAX_UPSCALE
        if src.kind == "svg":
            if not src.steps:
                start = "all"
            elif "start_step" in scene:
                start = str(scene["start_step"])
            elif any(st["action"] == "step" for st in steps):
                start = "0"
            else:
                start = "all"
        else:
            start = "1"
        self.start = start
        self.moves: list[Move] = []
        self.markers: list[Marker] = []
        self.fades: list[Fade] = []
        cur_state = start
        evs = sorted(steps, key=lambda s: s["time"])
        mv_times = [s["time"] for s in evs if s["action"] in ("focus", "all")]
        for st in evs:
            t, a = st["time"], st["action"]
            if a in ("step", "frame"):
                nxt = str(int(st["target"]))
                if nxt != cur_state:
                    self.fades.append(Fade(t, cur_state, nxt))
                    cur_state = nxt
            elif a in ("focus", "all"):
                later = [m for m in mv_times if m > t + 1e-6]
                dur = min(MOVE, (later[0] - t) if later else MOVE, max(0.2, duration - t))
                goal = self.full if a == "all" else self.fit(self.to_src(st["target"]))
                self.moves.append(Move(t, dur, self.view(t), goal))
                self._end_marker(t)
                if a == "focus":
                    self.markers.append(Marker(self.to_src(st["target"]), t + 0.35 * dur))
            elif a == "mark":
                self._end_marker(t)
                r = self.to_src(st["target"])
                cur = self.view(t)
                if not self.inside(cur, r):
                    # the named part is off screen: glide to it, keeping at least the current zoom-out
                    later = [m for m in mv_times if m > t + 1e-6]
                    dur = min(MOVE, (later[0] - t) if later else MOVE, max(0.2, duration - t))
                    # centred on the mark, so it lands mid screen rather than at the clipped edge
                    x, y, w, h = r
                    goal = self.place(x + w / 2, y + h / 2, max(cur.w, self.fit(r).w))
                    self.moves.append(Move(t, dur, cur, goal))
                    self.markers.append(Marker(r, t + 0.35 * dur))
                else:
                    self.markers.append(Marker(r, t))

    def _end_marker(self, t: float) -> None:
        for m in self.markers:
            if m.t_out == math.inf:
                m.t_out = max(t, m.t_in)

    def to_src(self, target) -> tuple[float, float, float, float]:
        x, y, w, h = parse_rect(target, "", "rect")
        vx, vy = self.src.vb[0], self.src.vb[1]
        return (x - vx) * self.k, (y - vy) * self.k, w * self.k, h * self.k

    def inside(self, v: View, r) -> bool:
        x, y, w, h = r
        vh = v.w / self.aspect
        mx, my = v.w * EDGE, vh * EDGE
        return (x >= v.cx - v.w / 2 + mx and x + w <= v.cx + v.w / 2 - mx and
                y >= v.cy - vh / 2 + my and y + h <= v.cy + vh / 2 - my)

    def fit(self, r) -> View:
        x, y, w, h = r
        vw = max(w / FOCUS_FILL, h * self.aspect / FOCUS_FILL, self.min_w, self.full.w / MAX_ZOOM)
        return self.place(x + w / 2, y + h / 2, vw)

    def place(self, cx: float, cy: float, vw: float) -> View:
        """A window of width vw centred on (cx, cy), kept within the figure."""
        vw = min(vw, self.full.w)
        vh = vw / self.aspect

        def clamp(c, half, size):
            lo, hi = sorted((half, size - half))
            return min(hi, max(lo, c))
        return View(clamp(cx, vw / 2, self.iw), clamp(cy, vh / 2, self.ih), vw)

    def view(self, t: float) -> View:
        v = self.full
        for m in self.moves:
            if t < m.t0:
                break
            p = ease((t - m.t0) / m.dur) if m.dur > 0 else 1.0
            # zoom moves feel even when the window width interpolates geometrically
            w = m.a.w * (m.b.w / m.a.w) ** p
            v = View(m.a.cx + (m.b.cx - m.a.cx) * p, m.a.cy + (m.b.cy - m.a.cy) * p, w)
        return v

    def state(self, t: float) -> tuple[str, str | None, float]:
        """(state, next state or None, blend 0..1)"""
        cur = self.start
        for f in self.fades:
            if t < f.t0:
                break
            p = (t - f.t0) / FADE
            if p < 1:
                return f.a, f.b, smooth(p)
            cur = f.b
        return cur, None, 0.0

    def to_screen(self, v: View, r) -> tuple[float, float, float, float]:
        s = self.aw / v.w
        x0, y0 = v.cx - v.w / 2, v.cy - (v.w / self.aspect) / 2
        x, y, w, h = r
        return self.ax + (x - x0) * s, self.ay + (y - y0) * s, w * s, h * s

    def marks(self, t: float) -> list[tuple[tuple[float, float, float, float], float, float]]:
        """[(screen rect, draw progress 0..1, opacity 0..1)]"""
        v = self.view(t)
        out = []
        for m in self.markers:
            if t < m.t_in or t >= m.t_out + OUT:
                continue
            draw = smooth((t - m.t_in) / DRAW)
            op = 1.0 if t < m.t_out else 1 - (t - m.t_out) / OUT
            out.append((self.to_screen(v, m.rect), draw, max(0.0, op)))
        return out


# ---------- compositor ----------

class Compositor:
    """Source images in, one drawing-area RGBA array out per frame."""

    def __init__(self, tl: Timeline, files: dict[str, Path]):
        self.tl = tl
        self.files = files
        self.cache: dict[str, object] = {}
        self.last_key = None
        self.last = None

    def image(self, key: str):
        from PIL import Image
        import svgshot
        svgshot.allow_pixels()
        if key not in self.cache:
            if len(self.cache) >= 3:
                self.cache.pop(next(iter(self.cache)))
            with Image.open(self.files[key]) as im:
                self.cache[key] = im.convert("RGB")
        return self.cache[key]

    def crop(self, key: str, v: View):
        """The window v of state key, resampled to the drawing area (white outside the source)."""
        from PIL import Image
        tl = self.tl
        aw, ah = tl.aw, tl.ah
        vh = v.w / tl.aspect
        x0, y0 = v.cx - v.w / 2, v.cy - vh / 2
        s = aw / v.w
        out = Image.new("RGB", (aw, ah), "white")
        # destination pixels covered by the source, snapped to whole pixels; the
        # source box is solved back from them so the mapping stays exact
        dx0 = max(0, math.ceil((0 - x0) * s - 1e-6))
        dy0 = max(0, math.ceil((0 - y0) * s - 1e-6))
        dx1 = min(aw, math.floor((tl.iw - x0) * s + 1e-6))
        dy1 = min(ah, math.floor((tl.ih - y0) * s + 1e-6))
        if dx1 - dx0 < 1 or dy1 - dy0 < 1:
            return out
        box = (max(0.0, x0 + dx0 / s), max(0.0, y0 + dy0 / s),
               min(float(tl.iw), x0 + dx1 / s), min(float(tl.ih), y0 + dy1 / s))
        img = self.image(key)
        part = img.resize((dx1 - dx0, dy1 - dy0), Image.LANCZOS, box=box,
                          reducing_gap=3.0 if s < 0.5 else None)
        out.paste(part, (dx0, dy0))
        return out

    def frame(self, t: float):
        """RGBA uint8 array for the drawing area at time t."""
        import numpy as np
        from PIL import Image
        v = self.tl.view(t)
        a, b, p = self.tl.state(t)
        key = (round(v.cx, 3), round(v.cy, 3), round(v.w, 3), a, b, round(p, 3))
        if key == self.last_key:
            return self.last
        img = self.crop(a, v)
        if b is not None and p > 0:
            img = Image.blend(img, self.crop(b, v), p)
        arr = np.asarray(img.convert("RGBA")).copy()
        # soften the cut where a zoomed figure meets the frame edge
        n = EDGE_FADE
        ramp = np.linspace(0.0, 1.0, n, endpoint=False)[:, None]
        for sl, r in ((np.s_[:n], ramp), (np.s_[-n:], ramp[::-1])):
            rows = arr[sl, :, :3].astype(np.float32)
            arr[sl, :, :3] = (255 - (255 - rows) * r[:, :, None]).astype(np.uint8)
            cols = arr[:, sl, :3].astype(np.float32)
            arr[:, sl, :3] = (255 - (255 - cols) * r.T[:, :, None]).astype(np.uint8)
        self.last_key, self.last = key, arr
        return arr
