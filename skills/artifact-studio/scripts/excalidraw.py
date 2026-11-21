#!/usr/bin/env python3
"""Write an Excalidraw scene (.excalidraw) from a small layout spec.

Engineering diagrams on artifact-studio pages are drawn in Excalidraw: build.py embeds the
scene, renders it in the browser with Excalidraw's own exporter, and offers the .excalidraw
file for download so anyone can open and edit it at excalidraw.com.

    python3 excalidraw.py spec.json out.excalidraw

spec = {
  "zones": [{"x": 20, "y": 20, "w": 400, "h": 300, "label": "app-model-gateway", "color": "blue"}],
  "nodes": [{"id": "gw", "x": 40, "y": 60, "w": 220, "h": 70,
             "text": "Model gateway\\nmodel/src/catalog.rs", "color": "green",
             "shape": "rectangle"}],           # rectangle | ellipse | diamond; color: see COLORS
  "edges": [{"from": "gw", "to": "reg", "label": "reads", "dashed": false,
             "side": "auto"}],                 # side: auto | h | v (which faces to connect)
  "texts": [{"x": 40, "y": 10, "text": "Title", "size": 28}]
}

Coordinates are Excalidraw scene units (about px). Elements carry only the fields that matter;
build.py runs Excalidraw's restoreElements() and exportToSvg() at build time in headless Chrome.
Defaults: Helvetica (system font), clean lines ("rough": true at the top level for hand-drawn),
node text size 18 ("size" per node), edge labels 15, text centred in its shape. Warnings for a
box that grew to fit its text or a label longer than its arrow are layout bugs: fix the spec.
"""
import json
import sys

COLORS = {  # Excalidraw's own palette (light); its dark mode inverts these at render time
    "grey": "#e9ecef", "red": "#ffc9c9", "pink": "#fcc2d7", "violet": "#d0bfff",
    "blue": "#a5d8ff", "cyan": "#99e9f2", "green": "#b2f2bb", "yellow": "#ffec99",
    "orange": "#ffd8a8", "white": "#ffffff", "none": "transparent",
}
STROKE = {"grey": "#868e96", "red": "#e03131", "violet": "#6741d9", "blue": "#1971c2",
          "green": "#2f9e44", "yellow": "#f08c00", "orange": "#e8590c", "cyan": "#0c8599",
          "pink": "#c2255c"}
INK = "#1e1e1e"
_seed = [1000]
# Helvetica (2) is a system font: nothing to download, so the text measured at build time is the
# text the reader sees. Excalidraw's Virgil (1) loads from a CDN that a hosted page may block.
FAMILY = 2
ROUGHNESS = [0]          # 0 clean lines; spec {"rough": true} gives the hand-drawn look
CHAR_W = 0.56            # average Helvetica glyph width as a share of font size (rounded up)
LINE_H = 1.25
WARN = []


def text_size(s, size):
    lines = s.split("\n")
    return max(len(l) for l in lines) * size * CHAR_W, len(lines) * size * LINE_H


def fit(n, size):
    """Grow a node until its text fits with padding. A diamond's usable box is about half its size."""
    tw, th = text_size(n["text"], size)
    diamond = n.get("shape") == "diamond"
    need_w = tw * (2.0 if diamond else 1.0) + (24 if diamond else 32)
    need_h = th * (2.0 if diamond else 1.0) + (16 if diamond else 24)
    if need_w > n["w"] or need_h > n["h"]:
        WARN.append(f'node {n["id"]}: grew from {n["w"]}x{n["h"]} to fit its text; check the spacing around it')
        n["x"] -= max(0, need_w - n["w"]) / 2
        n["y"] -= max(0, need_h - n["h"]) / 2
        n["w"], n["h"] = max(n["w"], round(need_w)), max(n["h"], round(need_h))


def nid():
    _seed[0] += 1
    return _seed[0]


def base(kind, eid, x, y, w, h, **kw):
    el = {"id": eid, "type": kind, "x": x, "y": y, "width": w, "height": h, "angle": 0,
          "strokeColor": INK, "backgroundColor": "transparent", "fillStyle": "solid",
          "strokeWidth": 2, "strokeStyle": "solid", "roughness": ROUGHNESS[0], "opacity": 100,
          "groupIds": [], "frameId": None, "roundness": None, "seed": nid(), "version": 1,
          "versionNonce": nid(), "isDeleted": False, "boundElements": [], "updated": 1,
          "link": None, "locked": False}
    el.update(kw)
    return el


def text_el(eid, x, y, w, h, s, size=18, container=None, align="center", family=None):
    family = FAMILY if family is None else family
    return base("text", eid, x, y, w, h, text=s, originalText=s, fontSize=size, fontFamily=family,
                textAlign=align, verticalAlign="middle" if container else "top",
                containerId=container, lineHeight=1.25, autoResize=True)


def anchor(n, toward, side):
    """Point on n's border facing `toward`, plus the axis used."""
    cx, cy = n["x"] + n["w"] / 2, n["y"] + n["h"] / 2
    tx, ty = toward["x"] + toward["w"] / 2, toward["y"] + toward["h"] / 2
    horiz = side == "h" or (side == "auto" and abs(tx - cx) * n["h"] > abs(ty - cy) * n["w"])
    if horiz:
        return (n["x"] + n["w"] if tx > cx else n["x"], cy), "h"
    return (cx, n["y"] + n["h"] if ty > cy else n["y"]), "v"


def build(spec):
    els = []
    for z in spec.get("zones", []):
        zid = f"zone-{nid()}"
        c = z.get("color", "grey")
        els.append(base("rectangle", zid, z["x"], z["y"], z["w"], z["h"], strokeColor=STROKE.get(c, INK),
                        backgroundColor=COLORS.get(c, c), fillStyle="hachure", strokeStyle="dashed",
                        strokeWidth=1, opacity=60, roundness={"type": 3}))
        if z.get("label"):
            els.append(text_el(f"{zid}-t", z["x"] + 14, z["y"] + 8, len(z["label"]) * 11, 25, z["label"],
                               size=18, align="left", family=z.get("family")))
    ROUGHNESS[0] = 1 if spec.get("rough") else 0
    nodes = {}
    for n in spec.get("nodes", []):
        fit(n, n.get("size", 18))
        nodes[n["id"]] = n
        c = n.get("color", "white")
        shape = n.get("shape", "rectangle")
        tid = f'{n["id"]}-t'
        els.append(base(shape, n["id"], n["x"], n["y"], n["w"], n["h"],
                        backgroundColor=COLORS.get(c, c), strokeColor=STROKE.get(n.get("stroke", ""), INK),
                        roundness={"type": 3} if shape == "rectangle" else {"type": 2},
                        boundElements=[{"type": "text", "id": tid}]))
        # Place the bound text centred ourselves: the exporter keeps the x/y it is given, so a box
        # the size of the shape leaves the text at the top. A diamond's text sits in its middle half.
        size = n.get("size", 18)
        tw, th = text_size(n["text"], size)
        inner = n["w"] * (0.5 if shape == "diamond" else 1) - 16
        els.append(text_el(tid, n["x"] + (n["w"] - inner) / 2, n["y"] + (n["h"] - th) / 2, inner, th, n["text"],
                           size=size, container=n["id"], family=n.get("family")))
    for i, e in enumerate(spec.get("edges", [])):
        a, b = nodes[e["from"]], nodes[e["to"]]
        (x1, y1), ax = anchor(a, b, e.get("side", "auto"))
        (x2, y2), _ = anchor(b, a, ax if e.get("side", "auto") == "auto" else e["side"])
        dx, dy = x2 - x1, y2 - y1
        if e.get("points"):
            x1, y1 = e["points"][0]
            pts = [[px - x1, py - y1] for px, py in e["points"]]
            dx, dy = pts[-1]
        elif abs(dx) < 2 or abs(dy) < 2:
            pts = [[0, 0], [dx, dy]]
        elif ax == "h":
            pts = [[0, 0], [dx / 2, 0], [dx / 2, dy], [dx, dy]]
        else:
            pts = [[0, 0], [0, dy / 2], [dx, dy / 2], [dx, dy]]
        aid = f"edge-{i}"
        arrow = base("arrow", aid, x1, y1, abs(dx), abs(dy), points=pts, lastCommittedPoint=None,
                     strokeStyle="dashed" if e.get("dashed") else "solid", roundness=None,
                     strokeColor=STROKE.get(e.get("color", ""), INK),
                     startBinding={"elementId": a["id"], "focus": 0, "gap": 4},
                     endBinding={"elementId": b["id"], "focus": 0, "gap": 4},
                     startArrowhead="arrow" if e.get("both") else None, endArrowhead="arrow",
                     elbowed=False)
        els.append(arrow)
        if e.get("label"):
            # a free label beside the middle segment: a bound label would mask a short arrow
            (sx, sy), (ex, ey) = pts[(len(pts) - 1) // 2], pts[(len(pts) - 1) // 2 + 1]
            mx, my = x1 + (sx + ex) / 2, y1 + (sy + ey) / 2
            size = e.get("size", 15)
            w = len(e["label"]) * size * CHAR_W
            seg = max(abs(ex - sx), abs(ey - sy))
            if abs(ex - sx) >= abs(ey - sy) and w + 28 > seg:
                WARN.append(f'edge {e["from"]}->{e["to"]}: label "{e["label"]}" ({w:.0f}) is longer than its '
                            f'segment ({seg:.0f}); move the nodes apart or shorten the label')
            if abs(ex - sx) >= abs(ey - sy):   # horizontal segment: label above it
                lx, ly = mx - w / 2, my - size * 1.6
            else:                              # vertical segment: label to its right
                lx, ly = mx + 8, my - size * 0.6
            els.append(text_el(f"{aid}-t", lx, ly, w, size * 1.25, e["label"], size=size, align="left"))
        for el in els:
            if el["id"] in (a["id"], b["id"]):
                el["boundElements"].append({"type": "arrow", "id": aid})
    for t in spec.get("texts", []):
        els.append(text_el(f"text-{nid()}", t["x"], t["y"], t.get("w", len(t["text"]) * t.get("size", 18) * 0.55),
                           t.get("size", 18) * 1.25, t["text"], size=t.get("size", 18), align="left",
                           family=t.get("family")))
    return {"type": "excalidraw", "version": 2, "source": "artifact-studio",
            "elements": els, "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None}, "files": {}}


if __name__ == "__main__":
    spec = json.load(open(sys.argv[1]))
    json.dump(build(spec), open(sys.argv[2], "w"), indent=1)
    for w in WARN:
        print("warning:", w, file=sys.stderr)
    print("wrote", sys.argv[2])
