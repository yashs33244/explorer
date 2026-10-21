"""
Renders one storyboard scene with Manim. render.py calls this once per scene:

    .venv/bin/python engine.py spec.json out.mp4 [--still out.png]

spec.json is {"scene": {...storyboard scene...}, "duration": s,
"words": [{"w", "start", "end"}], "steps": [{"time", "action", "target"}]}.
Layouts: title, repomap, flow, table, points, figure (see figure.py).
"""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import theme as th  # noqa: E402

th.register_fonts()

from manim import (BOLD, AnimationGroup, Camera, FadeIn, Group, ImageMobject, Rectangle, RoundedRectangle,  # noqa: E402
                   Scene, VGroup, config, tempconfig)

import figure as fig  # noqa: E402

import kit  # noqa: E402
from kit import px  # noqa: E402

LAYOUTS = ("title", "repomap", "flow", "table", "points", "figure")
ACTIONS = ("show", "highlight", "dim", "flow")
RUN = {"show": 0.7, "highlight": 0.5, "dim": 0.5, "flow": 1.2}


class StoryboardError(ValueError):
    pass


@dataclass
class Item:
    id: str
    mob: object
    deps: list[str] = field(default_factory=list)
    show: object = None        # () -> Animation
    highlight: object = None
    dim: object = None
    flow: object = None
    extra_on_show: list = field(default_factory=list)   # mobjects that appear with it (static tints)


def _anim(item: Item, action: str):
    fn = getattr(item, action)
    if fn is None:
        if action == "show":
            return FadeIn(item.mob)
        if action == "dim":
            return item.mob.animate.set_opacity(0.22)
        raise StoryboardError(f"target {item.id!r} does not support {action!r}")
    return fn()


def content_box(scene: dict) -> tuple[float, float, float, float]:
    top = kit.HEADING_BOTTOM + 34 if scene.get("heading") else th.TOP
    if scene.get("heading") and not scene.get("kicker"):
        top -= 40
    bottom = th.HEIGHT - th.CAPTION_H - 28
    return th.MARGIN, top, th.WIDTH - 2 * th.MARGIN, bottom - top


# ---------- layouts ----------

def build_title(s: dict) -> dict[str, Item]:
    card = kit.TitleCard(s.get("title", ""), s.get("kicker"), s.get("subtitle"), s.get("tldr"))
    return {k: Item(k, v) for k, v in card.parts.items()}


def _edges(s: dict, items: dict[str, Item], graph: dict) -> None:
    for i, e in enumerate(s.get("edges", [])):
        eid = e.get("id", f"edge:{i}")
        for end in ("from", "to"):
            if e.get(end) not in graph:
                raise StoryboardError(f"scene {s['id']}: edge {eid} {end} {e.get(end)!r} is not a node id")
        edge = kit.OrthoEdge(graph[e["from"]], graph[e["to"]], e.get("style", "solid"), e.get("label"),
                             prefer=e.get("route"), label_side=e.get("label_side", "auto"),
                             label_at=e.get("label_at", "auto"))
        edge.set_z_index(3)
        items[eid] = Item(eid, edge, deps=[e["from"], e["to"]], show=edge.show,
                          highlight=edge.highlight, flow=edge.flow)


def build_repomap(s: dict) -> dict[str, Item]:
    x0, y0, w0, h0 = content_box(s)
    conts = s.get("containers", [])
    if not conts:
        raise StoryboardError(f"scene {s['id']}: repomap needs containers")
    gap = 40
    auto = [c for c in conts if "x" not in c]
    cw = (w0 - gap * (len(auto) - 1)) / max(1, len(auto))
    inner = 22
    legend_room = 70 if s.get("legend") else 0
    room = h0 - legend_room
    most = max(len(c.get("chips", [])) for c in conts)
    # largest chip text that fits the tallest stack and the widest label
    for size in (28, 26, 24, 22):
        chip_gap = round(size * 0.6)
        need = kit.Container.HEADER + most * (size + 22) + max(0, most - 1) * chip_gap + inner
        wide = max([kit.text_width(ch["label"], size, th.MONO, BOLD) + 28
                    for c in conts for ch in c.get("chips", [])], default=0)
        if need <= room * 0.85 and wide <= cw - 2 * inner:
            break
    if need > room:
        raise StoryboardError(f"scene {s['id']}: containers need {need:.0f}px, room is {room:.0f}px")
    ch = need
    # centre the container row (plus legend) in the content box
    y_row = y0 + max(0, (h0 - (ch + legend_room)) / 2)
    items: dict[str, Item] = {}
    graph: dict[str, kit.Element] = {}
    ai = 0
    for c in conts:
        if "x" in c:
            x, y, w, h = c["x"], c["y"], c["w"], c["h"]
        else:
            x, y, w, h = x0 + ai * (cw + gap), y_row, cw, ch
            ai += 1
        box = kit.Container(c["title"], c.get("path"), x, y, w, h, c.get("group", ai))
        box.set_z_index(0)
        items[c["id"]] = Item(c["id"], box, deps=[c["parent"]] if c.get("parent") else [],
                              show=box.show, highlight=box.highlight)
        graph[c["id"]] = box
        cy = y + kit.Container.HEADER
        for chip in c.get("chips", []):
            chip_w = None if not chip.get("full") else w - 2 * inner
            ch_ = kit.Chip(chip["label"], x + inner, cy, chip_w, chip.get("bold", False), chip.get("dashed", False),
                           size=size)
            if ch_.w > w - 2 * inner:
                raise StoryboardError(f"scene {s['id']}: chip {chip['label']!r} is wider than its container")
            ch_.set_z_index(2)
            items[chip["id"]] = Item(chip["id"], ch_, deps=[c["id"]], highlight=ch_.highlight, show=ch_.show)
            graph[chip["id"]] = ch_
            if chip.get("badge") is not None:
                b = kit.Badge(chip["badge"], x + inner + ch_.w + 26, cy + ch_.h / 2)
                b.set_z_index(4)
                items[f"badge:{chip['id']}"] = Item(f"badge:{chip['id']}", b, deps=[chip["id"]], show=b.show)
            cy += ch_.h + chip_gap
    _edges(s, items, graph)
    if s.get("legend"):
        lg = kit.legend(y_row + ch + 50)
        items["legend"] = Item("legend", lg)
    return items


def build_flow(s: dict) -> dict[str, Item]:
    x0, y0, w0, h0 = content_box(s)
    nodes = s.get("nodes", [])
    if not nodes:
        raise StoryboardError(f"scene {s['id']}: flow needs nodes")
    for i, n in enumerate(nodes):
        n.setdefault("col", i)
        n.setdefault("row", 0)
    ncol = max(n["col"] for n in nodes) + 1
    nrow = max(n["row"] for n in nodes) + 1
    cell_w, cell_h = w0 / ncol, h0 / nrow
    items: dict[str, Item] = {}
    graph: dict[str, kit.Element] = {}
    for n in nodes:
        w = min(n.get("w", 300), cell_w - 90)
        h = n.get("h", 128 if n.get("sub") else 104)
        if h > cell_h - 40:
            raise StoryboardError(f"scene {s['id']}: too many flow rows for the frame")
        x = x0 + n["col"] * cell_w + (cell_w - w) / 2
        y = y0 + n["row"] * cell_h + (cell_h - h) / 2
        b = kit.Box(n["label"], x, y, w, h, n.get("sub"), n.get("group"))
        b.set_z_index(2)
        items[n["id"]] = Item(n["id"], b, show=b.show, highlight=b.highlight)
        graph[n["id"]] = b
        if n.get("badge") is not None:
            bd = kit.Badge(n["badge"], x + 4, y + 4)
            bd.set_z_index(4)
            items[f"badge:{n['id']}"] = Item(f"badge:{n['id']}", bd, deps=[n["id"]], show=bd.show)
    _edges(s, items, graph)
    return items


def build_table(s: dict, targeted_hl: set[str], state: dict) -> dict[str, Item]:
    x0, y0, w0, h0 = content_box(s)
    key = s.get("key")
    key_targeted = key is not None and ({"key", f"col:{key}"} & targeted_hl)
    t, err = None, None
    for size in (30, 28, 26, 24, 22):
        try:
            t = kit.Table(s["columns"], s["rows"], x0, y0, w0, key=None if key_targeted else key,
                          max_h=h0, size=size)
            break
        except ValueError as e:
            err = e
    if t is None:
        raise StoryboardError(f"scene {s['id']}: {err}")
    if t.h < h0 * 0.7:   # a short table sits a third of the way down, not glued to the heading
        t = kit.Table(s["columns"], s["rows"], x0, y0 + (h0 - t.h) / 3, w0,
                      key=None if key_targeted else key, max_h=h0, size=size)
    items: dict[str, Item] = {}
    for part in t.header[:len(s["columns"]) + 1]:
        part.set_z_index(2)
    items["header"] = Item("header", t.header)
    static_rows = set(s.get("highlight_rows", []))
    visible = state.setdefault("visible", set())
    for c in range(len(s["columns"])):
        head_txt = t.header[c]

        def hl(c=c, head_txt=head_txt):
            # tint the cells already on screen with an animation, the rest instantly
            # (they fade in tinted when their row shows)
            tints = t.cell_tints[c]
            on = [tints[0]] + [tints[i + 1] for i in range(len(t.rows)) if f"row:{i}" in visible]
            for r in tints:
                if r not in on:
                    r.set_fill(opacity=1)
            return AnimationGroup(*[r.animate.set_fill(opacity=1) for r in on],
                                  head_txt.animate.set_color(th.ACC))
        cid = f"col:{c}"
        items[cid] = Item(cid, VGroup(), deps=["header"], highlight=hl)
        if c == key:
            items["key"] = items[cid]
    for i, row in enumerate(t.rows):
        tint = t.row_tints[i].set_z_index(1)
        rid = f"row:{i}"
        it = Item(rid, row, deps=["header"], highlight=lambda tint=tint: FadeIn(tint))
        if i in static_rows and rid not in targeted_hl:
            it.extra_on_show.append(tint)
        items[rid] = it
    return items


def build_points(s: dict) -> dict[str, Item]:
    x0, y0, w0, h0 = content_box(s)
    pts = s.get("points", [])
    if not pts:
        raise StoryboardError(f"scene {s['id']}: points layout needs points")
    tx = x0 + 76

    def measure(size):
        sub_size = max(24, round(size * 0.72))
        rows = []
        for p in pts:
            lines = kit.wrap(p["text"], size, w0 - 96, th.BODY)
            sub = kit.wrap(p["sub"], sub_size, w0 - 96, th.BODY) if p.get("sub") else []
            h = kit.block_height(len(lines), size) + (size * 0.55 + kit.block_height(len(sub), sub_size) if sub else 0)
            rows.append((lines, sub, h))
        gap = round(size * 1.5)
        return sub_size, rows, gap, sum(r[2] for r in rows) + gap * (len(rows) - 1)

    for size in (40, 36, 32, 28):
        sub_size, rows, gap, total = measure(size)
        if total <= h0 - 20:
            break
    else:
        raise StoryboardError(f"scene {s['id']}: points overflow the frame, use fewer or shorter points")
    items: dict[str, Item] = {}
    y = y0 + max(10, (h0 - total) / 3)
    for i, (p, (lines, sub, h)) in enumerate(zip(pts, rows)):
        cap = size * 0.7
        g = VGroup(kit.Badge(p.get("n", i + 1), x0 + 24, y + cap / 2, r=max(19, size * 0.55)))
        g.add(kit.text_block(lines, size, tx, y, th.BODY, th.INK))
        if sub:
            g.add(kit.text_block(sub, sub_size, tx, y + kit.block_height(len(lines), size) + size * 0.55,
                                 th.BODY, th.MUTED))
        band = Rectangle(width=px(w0), height=px(h + gap * 0.7)).move_to(kit.at(x0 + w0 / 2, y + h / 2))
        band.set_fill(th.HIGHLIGHT, 0.85).set_stroke(opacity=0).set_z_index(0)
        g.set_z_index(1)
        pid = p.get("id", f"point:{i}")
        items[pid] = Item(pid, g, highlight=lambda band=band: FadeIn(band))
        y += h + gap
    return items


def build(scene: dict, steps: list[dict], state: dict) -> tuple[dict[str, Item], VGroup]:
    layout = scene.get("layout")
    if layout not in LAYOUTS:
        raise StoryboardError(f"scene {scene.get('id')}: layout must be one of {LAYOUTS}, got {layout!r}")
    hl = {st["target"] for st in steps if st["action"] == "highlight"}
    items = {
        "title": lambda: build_title(scene),
        "repomap": lambda: build_repomap(scene),
        "flow": lambda: build_flow(scene),
        "table": lambda: build_table(scene, hl, state),
        "points": lambda: build_points(scene),
    }[layout]()
    fixed = VGroup()
    if layout != "title" and scene.get("heading"):
        fixed.add(kit.heading(scene["heading"], scene.get("kicker")))
    return items, fixed


# ---------- scheduling ----------

def schedule(scene: dict, items: dict[str, Item], steps: list[dict]) -> tuple[set[str], list[tuple[float, list]]]:
    for st in steps:
        if st["action"] not in ACTIONS:
            raise StoryboardError(f"scene {scene['id']}: action must be one of {ACTIONS}, got {st['action']!r}")
        if st["target"] not in items:
            raise StoryboardError(
                f"scene {scene['id']}: target {st['target']!r} not found. Known ids: {', '.join(sorted(items))}")
    shown_at = {st["target"]: st["time"] for st in steps if st["action"] == "show"}
    memo: dict[str, float] = {}

    def appear(iid: str, stack=()) -> float:
        if iid in memo:
            return memo[iid]
        if iid in stack:
            raise StoryboardError(f"scene {scene['id']}: dependency loop at {iid}")
        dep_t = max([appear(d, stack + (iid,)) for d in items[iid].deps], default=0.0)
        if iid in shown_at:
            if shown_at[iid] + 1e-6 < dep_t:
                raise StoryboardError(
                    f"scene {scene['id']}: {iid!r} is shown before what it sits on ({items[iid].deps}); "
                    "move its phrase later or show the parent first")
            memo[iid] = shown_at[iid]
        else:
            memo[iid] = dep_t
        return memo[iid]

    for iid in items:
        appear(iid)
    for st in steps:
        if st["action"] != "show" and st["time"] + 1e-6 < memo[st["target"]]:
            raise StoryboardError(f"scene {scene['id']}: {st['action']} on {st['target']!r} before it is shown")
    initial = {i for i, t in memo.items() if t == 0.0 and i not in shown_at}
    events: dict[float, list] = {}
    for iid, t in memo.items():
        if iid in initial:
            continue
        events.setdefault(round(t, 3), []).append(("show", iid))
    for st in steps:
        if st["action"] != "show":
            events.setdefault(round(st["time"], 3), []).append((st["action"], st["target"]))
    return initial, sorted(events.items())


class StoryScene(Scene):
    spec: dict = {}

    def construct(self):
        spec = self.spec
        scene, steps, duration = spec["scene"], spec["steps"], spec["duration"]
        if scene.get("layout") == "figure":
            return _construct_figure(self, spec)
        state: dict = {"visible": set()}
        items, fixed = build(scene, steps, state)
        initial, events = schedule(scene, items, steps)
        state["visible"].update(initial)
        caption = kit.CaptionBar(spec["words"])
        self.add(caption)
        start = VGroup(fixed, *[items[i].mob for i in initial], *[m for i in initial for m in items[i].extra_on_show])
        t = 0.0
        fps = config.frame_rate
        if len(start):
            self.play(FadeIn(start), run_time=0.4)
            t = 0.4
        for k, (et, acts) in enumerate(events):
            if et > t + 0.5 / fps:
                self.wait(et - t)
                t = et
            nxt = events[k + 1][0] if k + 1 < len(events) else duration
            want = max(RUN[a] for a, _ in acts)
            run = max(3 / fps, min(want, nxt - t - 0.5 / fps, duration - t))
            anims = []
            state["visible"].update(iid for a, iid in acts if a == "show")
            for action, iid in acts:
                it = items[iid]
                anims.append(_anim(it, action))
                if action == "show":
                    anims.extend(FadeIn(m) for m in it.extra_on_show)
            self.play(AnimationGroup(*anims), run_time=run)
            t += run
        if duration > t:
            self.wait(duration - t)


# ---------- figure layout ----------

MARK_RED = "#e5484d"
MARK_STROKE = 5.5     # px on screen
MARK_FILL = 0.13
MARK_PAD = 6          # px around the named rect
MARK_R = 12


class ScreenImage(ImageMobject):
    """An opaque image already at screen size, blitted 1:1 at (x, y) px.

    manim's own image path resamples through a perspective transform (soft at
    1:1) and breaks on newer Pillow, so the camera gets a direct copy instead.
    """

    def __init__(self, arr, x: int, y: int):
        super().__init__(arr, scale_to_resolution=th.HEIGHT)
        self.screen_xy = (x, y)
        h, w = arr.shape[:2]
        self.move_to(th.at(x + w / 2, y + h / 2))


_display_image = Camera.display_image_mobject


def _display_image_fast(self, image_mobject, pixel_array):
    if isinstance(image_mobject, ScreenImage):
        x, y = image_mobject.screen_xy
        arr = image_mobject.pixel_array
        h, w = arr.shape[:2]
        pixel_array[y:y + h, x:x + w] = arr
        return
    _display_image(self, image_mobject, pixel_array)


Camera.display_image_mobject = _display_image_fast


def figure_heading(scene: dict) -> VGroup:
    """One slim line, top left: mono kicker then the heading, inside the top 56 px band."""
    g = VGroup()
    x, cy = fig.SIDE, fig.PAD + 22
    if scene.get("kicker"):
        k = kit.place(kit.T(scene["kicker"].upper(), 22, th.MONO, th.ACC), x, cy, "left")
        g.add(k)
        x = th.to_px(k.get_right())[0] + 22
    if scene.get("heading"):
        g.add(kit.place(kit.T(scene["heading"], 34, th.DISPLAY, th.INK, BOLD), x, cy, "left"))
    return g


def figure_files(scene: dict, steps: list[dict], base: Path) -> tuple[fig.Source, dict[str, Path]]:
    src = fig.load_source(scene, base)
    fig.check_steps(scene, src, steps)
    if src.kind == "svg":
        import svgshot
        width = fig.svg_width(scene, src, steps)
        files = svgshot.shoot(src.paths[0], width)
        src.size = svgshot.image_size(src.paths[0].read_text(), width)
    else:
        files = {str(i + 1): p for i, p in enumerate(src.paths)}
    return src, files


def marker(rect, draw: float, op: float) -> VGroup:
    x, y, w, h = rect
    x, y, w, h = x - MARK_PAD, y - MARK_PAD, w + 2 * MARK_PAD, h + 2 * MARK_PAD
    r = min(MARK_R, w / 2, h / 2)
    fill = RoundedRectangle(width=px(w), height=px(h), corner_radius=px(r)).move_to(th.at(x + w / 2, y + h / 2))
    fill.set_fill(MARK_RED, MARK_FILL * op * draw).set_stroke(opacity=0)
    line = RoundedRectangle(width=px(w), height=px(h), corner_radius=px(r)).move_to(th.at(x + w / 2, y + h / 2))
    line.set_fill(opacity=0).set_stroke(MARK_RED, th.stroke(MARK_STROKE), opacity=op)
    if draw < 1:
        full = line.copy()
        line.pointwise_become_partial(full, 0, max(1e-3, draw))
    return VGroup(fill, line)


def _construct_figure(self, spec: dict) -> None:
    scene, steps, duration = spec["scene"], spec["steps"], spec["duration"]
    try:
        src, files = figure_files(scene, steps, Path(spec.get("base", ".")))
    except fig.FigureError as e:
        raise StoryboardError(str(e)) from None
    tl = fig.Timeline(scene, src, steps, duration)
    comp = fig.Compositor(tl, files)
    still = bool(config.save_last_frame)
    clock = {"t": duration if still else 0.0}
    img = ScreenImage(comp.frame(clock["t"]), tl.ax, tl.ay).set_z_index(0)
    marks = VGroup().set_z_index(5)

    def tick(_m, dt):
        if not still:
            clock["t"] += dt
        t = min(clock["t"], duration)
        img.pixel_array = comp.frame(t)
        marks.submobjects = [marker(r, d, o) for r, d, o in tl.marks(t)]

    holder = Group(img, marks)
    holder.add_updater(tick)
    tick(holder, 0)
    self.add(kit.CaptionBar(spec["words"]))
    head = figure_heading(scene).set_z_index(6)
    self.add(holder, head)
    self.wait(duration)



def render(spec: dict, out: Path, still: Path | None = None) -> None:
    tmp = Path(tempfile.mkdtemp(prefix="manim-"))
    opts = {
        "pixel_width": th.WIDTH, "pixel_height": th.HEIGHT, "frame_rate": th.FPS,
        "background_color": th.BG, "media_dir": str(tmp), "disable_caching": True,
        "progress_bar": "none", "verbosity": "WARNING", "output_file": spec["scene"]["id"],
        "write_to_movie": still is None, "save_last_frame": still is not None,
    }
    try:
        with tempconfig(opts):
            StoryScene.spec = spec
            sc = StoryScene()
            sc.render()
            fw = sc.renderer.file_writer
            src = Path(fw.image_file_path if still is not None else fw.movie_file_path)
            dst = still if still is not None else out
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(src, dst)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__, file=sys.stderr)
        return 2
    spec = json.loads(Path(argv[0]).read_text())
    still = Path(argv[argv.index("--still") + 1]) if "--still" in argv else None
    try:
        render(spec, Path(argv[1]), still)
    except StoryboardError as e:
        print(f"storyboard error: {e}", file=sys.stderr)
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
