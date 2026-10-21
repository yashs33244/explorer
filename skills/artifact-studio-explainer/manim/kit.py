"""
Reusable primitives in the artifact-studio look, for 1920x1080 Manim scenes.

All sizes are screen pixels. Every primitive is a VGroup with a few named
parts and three animation helpers: show(), highlight() and dim(). Edges also
have flow(), a dot that travels the path.
"""

from __future__ import annotations

from functools import lru_cache
from statistics import median

import numpy as np
from manim import (
    BOLD,
    DOWN,
    LEFT,
    NORMAL,
    SEMIBOLD,
    UP,
    AnimationGroup,
    Circle,
    Create,
    DashedVMobject,
    Dot,
    FadeIn,
    Line,
    MoveAlongPath,
    Polygon,
    Rectangle,
    RoundedRectangle,
    Succession,
    Text,
    Transform,
    VGroup,
    VMobject,
)
from manim.constants import CapStyleType

import theme as th
from theme import ACC, ACC_SOFT, BG, HIGHLIGHT, INK, LINE, MUTED, at, px, stroke

_SHAPE_SIZE = 192.0


def _shape_size(content: str) -> float:
    # Pango wraps lines past a fixed canvas width, so long strings shape smaller.
    n = len(content)
    return 192.0 if n <= 50 else 96.0 if n <= 110 else 48.0
_DESCENDERS = frozenset("gjpqyQJ,;()[]{}|/\\_@$")


# ---------- text ----------

def T(content: str, size: float = 24, font: str = th.BODY, color: str = INK, weight: str = NORMAL) -> Text:
    """Text at `size` px em. Shaped large then scaled so kerning survives."""
    fam = th.family(font)
    shape = _shape_size(content)
    t = Text(content, font=fam, font_size=shape, color=color, weight=weight, disable_ligatures=True)
    t.scale(th.font_size(size) / shape)
    t.content, t.fam, t.size_px, t.weight_name = content, fam, max(size, th.MIN_TEXT), weight
    return t


@lru_cache(maxsize=256)
def _cap_height_px(fam: str, size: float, weight: str) -> float:
    t = Text("H", font=fam, font_size=_SHAPE_SIZE, weight=weight)
    return t.height / px(1) * th.font_size(size) / _SHAPE_SIZE


def text_width(content: str, size: float = 24, font: str = th.BODY, weight: str = NORMAL) -> float:
    return _text_width(content, size, th.family(font), weight)


@lru_cache(maxsize=4096)
def _text_width(content: str, size: float, fam: str, weight: str) -> float:
    if not content.strip():
        return 0.0
    shape = _shape_size(content)
    t = Text(content, font=fam, font_size=shape, weight=weight, disable_ligatures=True)
    return t.width / px(1) * th.font_size(size) / shape


def place(t: Text, x: float, y: float, align: str = "center") -> Text:
    """Put text with its optical centre (half cap height above baseline) at x, y px."""
    p = at(x, y)
    if align == "left":
        t.shift([p[0] - t.get_left()[0], 0, 0])
    elif align == "right":
        t.shift([p[0] - t.get_right()[0], 0, 0])
    else:
        t.shift([p[0] - t.get_center()[0], 0, 0])
    chars, glyphs = glyph_chars(t)
    if chars is not None:
        bottoms = [g.get_bottom()[1] for c, g in zip(chars, glyphs)
                   if c not in _DESCENDERS and not c.isspace() and g.has_points()]
        base = median(bottoms) if bottoms else t.get_bottom()[1]
    else:
        base = t.get_bottom()[1]
    cap = px(_cap_height_px(t.fam, t.size_px, t.weight_name))
    t.shift([0, (p[1] - cap / 2) - base, 0])
    return t


def glyph_chars(t: Text):
    """Pair each submobject with its character. With ligatures off, spaces get a submobject too."""
    subs = list(t.submobjects)
    if len(subs) == len(t.content):
        return list(t.content), subs
    chars = [c for c in t.content if not c.isspace()]
    if len(subs) == len(chars):
        return chars, subs
    return None, subs


def wrap(content: str, size: float, max_w: float, font: str = th.BODY, weight: str = NORMAL) -> list[str]:
    words, lines, cur = content.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if cur and text_width(trial, size, font, weight) > max_w:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines or [""]


def text_block(lines: list[str], size: float, x: float, y_top: float, font: str = th.BODY,
               color: str = INK, weight: str = NORMAL, align: str = "left", leading: float = 1.35) -> VGroup:
    """Lines of text, first line's cap top at y_top px."""
    g = VGroup()
    cap = _cap_height_px(th.family(font), max(size, th.MIN_TEXT), weight)
    for i, line in enumerate(lines):
        t = T(line, size, font, color, weight)
        place(t, x, y_top + cap / 2 + i * size * leading, align)
        g.add(t)
    return g


def block_height(n_lines: int, size: float, leading: float = 1.35) -> float:
    return (n_lines - 1) * size * leading + size * 0.72


def rrect(x: float, y: float, w: float, h: float, r: float = 10, fill: str = BG, fill_op: float = 1.0,
          line: str = INK, line_px: float = 1.5, line_op: float = 1.0) -> RoundedRectangle:
    rect = RoundedRectangle(corner_radius=px(r), width=px(w), height=px(h))
    rect.move_to(at(x + w / 2, y + h / 2))
    rect.set_fill(fill, fill_op).set_stroke(line, stroke(line_px), line_op)
    return rect


def dashed(mob: VMobject, dash_px: float = 10, perimeter_px: float | None = None) -> DashedVMobject:
    per = perimeter_px or 2 * (mob.width + mob.height) / px(1)
    return DashedVMobject(mob, num_dashes=max(8, int(per / dash_px / 2)), dashed_ratio=0.55)


class Element(VGroup):
    """Base: bounding box in px plus default animations."""

    kind = "element"

    def box_px(self) -> tuple[float, float, float, float]:
        return self.x, self.y, self.w, self.h

    def anchor(self, side: str) -> tuple[float, float]:
        x, y, w, h = self.box_px()
        return {
            "left": (x, y + h / 2), "right": (x + w, y + h / 2),
            "top": (x + w / 2, y), "bottom": (x + w / 2, y + h),
        }[side]

    def show(self):
        return FadeIn(self, shift=UP * px(10))

    def highlight(self):
        return AnimationGroup()

    def dim(self):
        return self.animate.set_opacity(0.22)


# ---------- chip ----------

class Chip(Element):
    """Mono label in a small rounded rect. bold = entry point, dashed = in transition."""

    kind = "chip"

    def __init__(self, label: str, x: float, y: float, w: float | None = None, bold: bool = False,
                 dashed_: bool = False, size: float = 22):
        super().__init__()
        weight = BOLD if bold else NORMAL
        self.w = w or text_width(label, size, th.MONO, weight) + 28
        self.h = size + 22
        self.x, self.y = x, y
        rect = rrect(x, y, self.w, self.h, r=8, line=INK, line_px=3 if bold else 1.5)
        if dashed_:
            outline = dashed(rect.copy().set_fill(opacity=0), dash_px=8)
            rect.set_stroke(opacity=0)
            self.add(rect, outline)
            self.outline = outline
        else:
            self.add(rect)
            self.outline = rect
        self.rect = rect
        self.label = place(T(label, size, th.MONO, INK, weight), x + self.w / 2, y + self.h / 2)
        self.add(self.label)

    def highlight(self):
        return AnimationGroup(
            self.rect.animate.set_fill(ACC_SOFT, 1),
            self.outline.animate.set_stroke(ACC, stroke(3), 1),
            self.label.animate.set_color(ACC),
        )


# ---------- box node ----------

class Box(Element):
    """A node: title text, optional mono sub label, optional group tint."""

    kind = "box"

    def __init__(self, label: str, x: float, y: float, w: float, h: float, sub: str | None = None,
                 group: int | None = None, size: float = 26):
        super().__init__()
        self.x, self.y, self.w, self.h = x, y, w, h
        fill = th.GROUP_TINT[group % 6] if group is not None else BG
        line = th.GROUP_DEEP[group % 6] if group is not None else INK
        self.rect = rrect(x, y, w, h, r=12, fill=fill, line=line, line_px=2)
        self.add(self.rect)
        lines = wrap(label, size, w - 28, th.BODY, SEMIBOLD)[:2]
        sub_h = 22 * 1.5 if sub else 0
        total = block_height(len(lines), size) + sub_h
        top = y + (h - total) / 2
        self.label = text_block(lines, size, x + w / 2, top, th.BODY, INK, SEMIBOLD, "center")
        self.add(self.label)
        if sub:
            self.sub = place(T(sub, 22, th.MONO, th.MUTED), x + w / 2, top + total - 22 * 0.36)
            self.add(self.sub)

    def highlight(self):
        # Transform the whole group: animating self.rect alone re-adds it on top and hides the label.
        target = self.copy()
        target.rect.set_fill(ACC_SOFT, 1).set_stroke(ACC, stroke(3.5))
        return Transform(self, target)


# ---------- container ----------

class Container(Element):
    """Rounded group box: coloured title, mono path label, faint tinted fill."""

    kind = "container"
    HEADER = 64

    def __init__(self, title: str, path: str | None, x: float, y: float, w: float, h: float, group: int = 0):
        super().__init__()
        g = group % 6
        self.x, self.y, self.w, self.h, self.group = x, y, w, h, g
        self.rect = rrect(x, y, w, h, r=16, fill=th.GROUP_TINT[g], fill_op=0.55,
                          line=th.GROUP_DEEP[g], line_px=2)
        self.title = place(T(title, 28, th.BODY, th.GROUP_INK[g], BOLD), x + 20, y + 34, "left")
        self.add(self.rect, self.title)
        if path:
            room = w - 40 - self.title.width / px(1) - 16
            label = path
            while label and text_width(label, 22, th.MONO) > room and len(label) > 4:
                label = label[:-2]
            if label != path:
                label = label[:-1] + "~"
            if room > 40:
                self.path = place(T(label, 22, th.MONO, MUTED), x + w - 20, y + 34, "right")
                self.add(self.path)

    def show(self):
        return AnimationGroup(Create(self.rect), FadeIn(VGroup(*self.submobjects[1:])))

    def highlight(self):
        # Same as Box: keep the chips and title above the recoloured rect.
        target = self.copy()
        target.rect.set_stroke(ACC, stroke(4)).set_fill(ACC_SOFT, 0.7)
        return Transform(self, target)


# ---------- badge ----------

class Badge(Element):
    kind = "badge"

    def __init__(self, n: int | str, cx: float, cy: float, r: float = 19):
        super().__init__()
        self.x, self.y, self.w, self.h = cx - r, cy - r, 2 * r, 2 * r
        c = Circle(radius=px(r)).move_to(at(cx, cy)).set_fill(th.GROUP_FILL[2], 1).set_stroke(INK, stroke(1.5))
        self.add(c, place(T(str(n), 22, th.BODY, INK, BOLD), cx, cy))

    def show(self):
        return FadeIn(self, scale=0.6)


# ---------- orthogonal edge ----------

def ortho_route(a: Element, b: Element, prefer: str | None = None) -> list[tuple[float, float]]:
    ax, ay, aw, ah = a.box_px()
    bx, by, bw, bh = b.box_px()
    gap = 6
    horizontal = prefer == "h" or (prefer is None and (bx >= ax + aw + 12 or ax >= bx + bw + 12))
    if horizontal:
        right = bx >= ax + aw
        x1 = ax + aw + gap if right else ax - gap
        x2 = bx - gap if right else bx + bw + gap
        y1, y2 = ay + ah / 2, by + bh / 2
        if abs(y1 - y2) < 4:
            return [(x1, y1), (x2, y1)]
        # overlapping vertical spans: run straight across at a shared y
        lo, hi = max(ay, by) + 10, min(ay + ah, by + bh) - 10
        if lo <= hi:
            yy = (lo + hi) / 2
            return [(x1, yy), (x2, yy)]
        xm = (x1 + x2) / 2
        return [(x1, y1), (xm, y1), (xm, y2), (x2, y2)]
    down = by >= ay + ah
    y1 = ay + ah + gap if down else ay - gap
    y2 = by - gap if down else by + bh + gap
    x1, x2 = ax + aw / 2, bx + bw / 2
    if abs(x1 - x2) < 4:
        return [(x1, y1), (x1, y2)]
    lo, hi = max(ax, bx) + 10, min(ax + aw, bx + bw) - 10
    if lo <= hi:
        xx = (lo + hi) / 2
        return [(xx, y1), (xx, y2)]
    ym = (y1 + y2) / 2
    return [(x1, y1), (x1, ym), (x2, ym), (x2, y2)]


class OrthoEdge(Element):
    """Right-angle edge. style: solid (depends on), dashed (vendored copy), dotted (calls at runtime)."""

    kind = "edge"

    def __init__(self, a: Element, b: Element, style: str = "solid", label: str | None = None,
                 color: str = INK, prefer: str | None = None, label_side: str = "auto", label_at: str = "auto"):
        super().__init__()
        if style not in ("solid", "dashed", "dotted"):
            raise ValueError(f"edge style must be solid, dashed or dotted, got {style!r}")
        pts = ortho_route(a, b, prefer)
        # leave room for the arrow head
        (px1, py1), (px2, py2) = pts[-2], pts[-1]
        dx, dy = np.sign(px2 - px1), np.sign(py2 - py1)
        head = 14
        body = pts[:-1] + [(px2 - dx * head * 0.8, py2 - dy * head * 0.8)]
        self.path = VMobject().set_points_as_corners([at(*p) for p in pts])
        line = VMobject().set_points_as_corners([at(*p) for p in body])
        line.set_stroke(color, stroke(2.2)).set_fill(opacity=0)
        length = sum(abs(p[0] - q[0]) + abs(p[1] - q[1]) for p, q in zip(body, body[1:]))
        if style == "dashed":
            line = DashedVMobject(line, num_dashes=max(3, int(length / 18)), dashed_ratio=0.6)
        elif style == "dotted":
            line = DashedVMobject(line, num_dashes=max(3, int(length / 11)), dashed_ratio=0.3)
            line.set_cap_style(CapStyleType.ROUND)
            line.set_stroke(width=stroke(3.2))
        self.line = line
        tip_pts = [(px2, py2),
                   (px2 - dx * head - dy * head * 0.5, py2 - dy * head - dx * head * 0.5),
                   (px2 - dx * head + dy * head * 0.5, py2 - dy * head + dx * head * 0.5)]
        self.tip = Polygon(*[at(*p) for p in tip_pts]).set_fill(color, 1).set_stroke(color, stroke(1))
        self.add(self.line, self.tip)
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        self.x, self.y, self.w, self.h = min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys)
        self.label = None
        if label:
            self.label = self._label(pts, label, label_side, label_at)
            self.add(self.label)

    def _label(self, pts, label, side, where):
        # label sits on a white mask beside one segment: the first one if it has room
        # (near the source, away from the target box), else the longest; or label_at start/end/longest
        segs = list(zip(pts, pts[1:]))

        def seg_len(sg):
            return abs(sg[0][0] - sg[1][0]) + abs(sg[0][1] - sg[1][1])

        t = T(label, 22, th.BODY, MUTED)
        tw, th_ = t.width / px(1), 22
        longest = max(segs, key=seg_len)
        if where == "start" or (where == "auto" and seg_len(segs[0]) >= tw + 40):
            seg = segs[0]
        elif where == "end":
            seg = segs[-1]
        else:
            seg = longest
        (x1, y1), (x2, y2) = seg
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        if abs(y1 - y2) < 1:   # horizontal segment: label above it
            cx, cy = mx, my - 22 if side != "below" else my + 22
        else:                  # vertical segment: label to the right
            cx = mx + tw / 2 + 14 if side != "left" else mx - tw / 2 - 14
            cy = my
        place(t, cx, cy)
        mask = rrect(cx - tw / 2 - 8, cy - th_ / 2 - 7, tw + 16, th_ + 14, r=6, fill=BG, line=BG, line_px=0.1,
                     line_op=0)
        return VGroup(mask, t)

    def show(self):
        parts = [Create(self.line), FadeIn(self.tip)]
        if self.label is not None:
            parts.append(FadeIn(self.label))
        return Succession(*parts, lag_ratio=1.0)

    def highlight(self):
        anims = [self.line.animate.set_stroke(ACC), self.tip.animate.set_fill(ACC).set_stroke(ACC)]
        if self.label is not None:
            anims.append(self.label[1].animate.set_color(ACC))
        return AnimationGroup(*anims)

    def flow(self):
        dot = Dot(radius=px(9), color=ACC).move_to(self.path.get_start()).set_z_index(5)
        return Succession(
            FadeIn(dot, run_time=0.1),
            AnimationGroup(MoveAlongPath(dot, self.path), self.highlight()),
            dot.animate.set_opacity(0),
        )


# ---------- table ----------

class Table(Element):
    """Header row plus rows. key = column index tinted acc-soft, hl_rows tinted #fff1b8."""

    kind = "table"
    SIZE = 24

    def __init__(self, columns: list[str], rows: list[list[str]], x: float, y: float, w: float,
                 key: int | None = None, max_h: float | None = None, size: float = 24):
        super().__init__()
        s = size
        self.x, self.y, self.w = x, y, w
        ncol = len(columns)
        for r in rows:
            if len(r) != ncol:
                raise ValueError(f"table row {r} has {len(r)} cells, header has {ncol}")
        pad = 18

        def font_of(cell: str):
            return (th.MONO, cell[1:-1]) if len(cell) > 1 and cell.startswith("`") and cell.endswith("`") else (th.BODY, cell)

        natural = []
        for c in range(ncol):
            ws = [text_width(columns[c], s, th.BODY, BOLD)]
            for r in rows:
                f, txt = font_of(r[c])
                ws.append(text_width(txt, s, f))
            natural.append(max(ws) + 2 * pad)
        total = sum(natural)
        if total <= w:
            widths = [n + (w - total) * n / total for n in natural]
        else:  # shrink the widest columns, wrap their text
            widths = list(natural)
            while sum(widths) > w:
                i = max(range(ncol), key=lambda k: widths[k])
                widths[i] -= sum(widths) - w if sum(widths) - w < 20 else 20
                if widths[i] < 120:
                    raise ValueError("table too wide for the frame: shorten cell text or drop a column")
        xs = [x + sum(widths[:i]) for i in range(ncol)]

        def cell_lines(cell, c, weight=NORMAL):
            f, txt = font_of(cell)
            return f, wrap(txt, s, widths[c] - 2 * pad, f, weight)

        lead = 1.3
        head_lines = [cell_lines(h, c, BOLD) for c, h in enumerate(columns)]
        rpad = round(s * 1.4)
        head_h = max(block_height(len(l), s, lead) for _, l in head_lines) + rpad
        row_cells = [[cell_lines(cell, c) for c, cell in enumerate(r)] for r in rows]
        row_hs = [max(block_height(len(l), s, lead) for _, l in rc) + rpad for rc in row_cells]
        self.h = head_h + sum(row_hs)
        if max_h is not None and self.h > max_h:
            raise ValueError(f"table is {self.h:.0f}px tall, room is {max_h:.0f}px: fewer rows or shorter text")

        # one acc-soft tint per cell, so a column tint grows with the rows as they build;
        # the key column starts tinted, any other column at opacity 0
        self.cell_tints = [[] for _ in range(ncol)]

        def cell_tint(c, top, hgt):
            r = Rectangle(width=px(widths[c]), height=px(hgt)).move_to(at(xs[c] + widths[c] / 2, top + hgt / 2))
            r.set_fill(ACC_SOFT, 1 if c == key else 0).set_stroke(opacity=0).set_z_index(0)
            self.cell_tints[c].append(r)
            return r

        self.header = VGroup()
        for c, (f, lines) in enumerate(head_lines):
            color = ACC if c == key else INK
            self.header.add(text_block(lines, s, xs[c] + pad, y + rpad / 2, th.BODY, color, BOLD, leading=lead))
        self.header.add(Line(at(x, y + head_h), at(x + w, y + head_h)).set_stroke(INK, stroke(2)))
        for c in range(ncol):
            self.header.add(cell_tint(c, y, head_h))
        self.rows, self.row_tints = [], []
        cy = y + head_h
        for i, rc in enumerate(row_cells):
            rh = row_hs[i]
            tint = Rectangle(width=px(w), height=px(rh - 1)).move_to(at(x + w / 2, cy + rh / 2))
            tint.set_fill(HIGHLIGHT, 0.85).set_stroke(opacity=0)
            self.row_tints.append(tint)
            row = VGroup()
            for c, (f, lines) in enumerate(rc):
                row.add(text_block(lines, s, xs[c] + pad, cy + rpad / 2, f, INK, leading=lead).set_z_index(2))
            if i < len(row_cells) - 1:
                row.add(Line(at(x, cy + rh), at(x + w, cy + rh)).set_stroke(LINE, stroke(1.5)).set_z_index(2))
            for c in range(ncol):
                row.add(cell_tint(c, cy, rh))
            self.rows.append(row)
            cy += rh
        self.xs, self.widths, self.key = xs, widths, key
        self.add(self.header)  # rows and tints are added by the engine (they build step by step)


# ---------- caption bar ----------

class CaptionBar(VGroup):
    """Bottom subtitles: current phrase, current word in accent. Driven by an updater."""

    SIZE = 34

    def __init__(self, words: list[dict], max_w: float = th.WIDTH - 2 * th.MARGIN - 80):
        super().__init__()
        top = th.HEIGHT - th.CAPTION_H
        self.bar = Rectangle(width=px(th.WIDTH), height=px(th.CAPTION_H)).move_to(at(th.WIDTH / 2, top + th.CAPTION_H / 2))
        self.bar.set_fill(BG, 1).set_stroke(opacity=0)
        self.rule = Line(at(0, top), at(th.WIDTH, top)).set_stroke(LINE, stroke(1.5))
        self.add(self.bar, self.rule)
        self.words = words
        self.chunks: list[tuple[int, int]] = []   # [start, end) word indices
        start = 0
        for i, w in enumerate(words):
            text = " ".join(x["w"] for x in words[start:i + 1])
            if i > start and text_width(text, self.SIZE) > max_w:
                self.chunks.append((start, i))
                start = i
            elif w["w"][-1:] in ".?!" or (w["w"][-1:] in ",;:" and i - start >= 5):
                self.chunks.append((start, i + 1))
                start = i + 1
        if start < len(words):
            self.chunks.append((start, len(words)))
        self.lines, self.glyphs = [], []
        cy = top + th.CAPTION_H / 2
        for a, b in self.chunks:
            t = place(T(" ".join(x["w"] for x in words[a:b]), self.SIZE, th.BODY, INK, NORMAL), th.WIDTH / 2, cy)
            chars, _ = glyph_chars(t)
            spans, k = [], 0
            with_spaces = chars is not None and len(chars) == len(t.content)
            for x in words[a:b]:
                n = len(x["w"])
                spans.append((k, k + n))
                k += n + (1 if with_spaces else 0)
            self.glyphs.append(spans if chars is not None else None)
            t.set_opacity(0)
            self.lines.append(t)
            self.add(t)
        self.t = 0.0
        self.cur = (-1, -1)
        self.set_z_index(10)
        self.add_updater(CaptionBar._tick)

    def _tick(self, dt):
        self.t += dt
        wi = -1
        for i, w in enumerate(self.words):
            if w["start"] <= self.t:
                wi = i
        if wi < 0:
            state = (-1, -1)
        else:
            ci = next(c for c, (a, b) in enumerate(self.chunks) if a <= wi < b)
            state = (ci, wi)
        if state == self.cur:
            return
        prev_c = self.cur[0]
        self.cur = state
        ci, wi = state
        if prev_c != ci and prev_c >= 0:
            self.lines[prev_c].set_opacity(0)
        if ci < 0:
            return
        line = self.lines[ci]
        line.set_opacity(1).set_color(INK)
        spans = self.glyphs[ci]
        if spans is not None:
            a = self.chunks[ci][0]
            s0, s1 = spans[wi - a]
            for g in line.submobjects[s0:s1]:
                g.set_color(ACC)


# ---------- title card / heading ----------

def heading(title: str, kicker: str | None = None) -> VGroup:
    g = VGroup()
    y = th.TOP
    if kicker:
        g.add(place(T(kicker.upper(), 22, th.MONO, ACC), th.MARGIN, y + 11, "left"))
        y += 40
    g.add(place(T(title, 46, th.DISPLAY, INK, BOLD), th.MARGIN, y + 20, "left"))
    return g


HEADING_BOTTOM = th.TOP + 40 + 56   # px where content may start under a kicker plus heading


class TitleCard(VGroup):
    """kicker, big display title, subtitle, a tldr box with an accent rule."""

    def __init__(self, title: str, kicker: str | None = None, subtitle: str | None = None,
                 tldr: str | None = None):
        super().__init__()
        x = th.MARGIN + 96
        maxw = th.WIDTH - 2 * x
        lines = wrap(title, 88, maxw, th.DISPLAY, BOLD)
        parts = []
        h_title = block_height(len(lines), 88, 1.12)
        sub_lines = wrap(subtitle, 34, maxw, th.BODY) if subtitle else []
        tldr_lines = wrap(tldr, 30, maxw - 64, th.BODY) if tldr else []
        total = (68 if kicker else 0) + h_title + (40 + block_height(len(sub_lines), 34) if subtitle else 0) \
            + (56 + block_height(len(tldr_lines), 30) + 48 if tldr else 0)
        y = (th.HEIGHT - th.CAPTION_H - total) / 2
        self.parts = {}
        if kicker:
            self.parts["kicker"] = place(T(kicker.upper(), 24, th.MONO, ACC), x, y + 12, "left")
            y += 68
        self.parts["title"] = text_block(lines, 88, x, y, th.DISPLAY, INK, BOLD, leading=1.12)
        y += h_title
        if subtitle:
            y += 40
            self.parts["subtitle"] = text_block(sub_lines, 34, x, y, th.BODY, MUTED)
            y += block_height(len(sub_lines), 34)
        if tldr:
            y += 56
            bh = block_height(len(tldr_lines), 30) + 48
            box = rrect(x, y, maxw, bh, r=10, fill=ACC_SOFT, line=ACC_SOFT, line_px=0.1)
            rule = Rectangle(width=px(6), height=px(bh)).move_to(at(x + 3, y + bh / 2)).set_fill(ACC, 1).set_stroke(opacity=0)
            body = text_block(tldr_lines, 30, x + 36, y + 24, th.BODY, INK)
            self.parts["tldr"] = VGroup(box, rule, body)
        for p in self.parts.values():
            parts.append(p)
        self.add(*parts)


def legend(y: float, x: float = th.MARGIN) -> VGroup:
    """Edge style key: solid, dashed, dotted."""
    g = VGroup()
    items = [("solid", "depends on"), ("dashed", "vendored copy"), ("dotted", "calls at runtime")]
    for style, text in items:
        a = Element(); a.x, a.y, a.w, a.h = x, y - 1, 1, 2
        b = Element(); b.x, b.y, b.w, b.h = x + 64, y - 1, 1, 2
        e = OrthoEdge(a, b, style)
        t = place(T(text, 22, th.BODY, MUTED), x + 80, y, "left")
        g.add(e, t)
        x += 80 + t.width / px(1) + 40
    return g
