#!/usr/bin/env python3
"""Write a hand-drawn Excalidraw scene: numbered boxes holding left-aligned field lists, request
text in red beside the arrows, stores as ellipses, dashed zones for processes.

Use it when the reader wants every header and field of a flow on the drawing itself, the way an
engineer sketches a request on a whiteboard. For plain boxes and arrows use excalidraw.py.

    python3 handdrawn.py spec.json out.excalidraw

spec = {
  "rough": true,                                   # hand-drawn strokes (default true)
  "zones":    [{"x": 40, "y": 110, "w": 500, "h": 600, "label": "your app process", "color": "grey"}],
  "boxes":    [{"x": 60, "y": 140, "w": 460, "h": 300, "color": "blue",
                "title": "1  request to the gateway",
                "lines": ["POST /v1/chat/completions",
                          "headers",
                          ["  authorization: Bearer <TOKEN>", "orange"],
                          "body",
                          "  model: \\"gpt\\""]}],
  "ellipses": [{"x": 80, "y": 800, "w": 420, "h": 160, "text": "DB (postgres)\\nusers", "color": "green"}],
  "arrows":   [{"points": [[520, 260], [700, 260]], "color": "blue", "dashed": false,
                "label": {"x": 560, "y": 228, "text": "1  POST"}}],
  "notes":    [{"x": 360, "y": 368, "text": "GET /api/v1/tokens\\n  res { .. }", "color": "red",
                "font": "mono", "size": 14}]
}

Colours: ink, blue, red, orange, green, grey, violet (Excalidraw's palette; dark pages invert
them at render time). Box titles, zone labels, ellipse text and arrow labels use the hand-drawn
Virgil face; box lines and notes use the Cascadia mono face unless "font": "hand". Arrows take
absolute points, so an elbow is three points. build.py loads both faces before drawing the scene
and embeds them in the page, so the reader needs no font CDN.

Layout rules that keep it readable: about 0.6 x size units per mono character and 1.25 x size
per line; leave 140 or more units between boxes joined by a labelled arrow; put request text
beside an arrow in a clear lane, never across a box; keep a scene under about 1,900 units wide
and use "size": "bleed" in figs.json for wide ones.
"""
import json
import sys

COLORS = {"ink": "#1e1e1e", "blue": "#1971c2", "red": "#e03131", "orange": "#e8590c",
          "green": "#2f9e44", "grey": "#868e96", "violet": "#6741d9"}
HAND, MONO = 1, 3


class Scene:
    def __init__(self, rough=True):
        self.els, self.n, self.rough = [], 0, 1 if rough else 0

    def _id(self):
        self.n += 1
        return self.n

    def _base(self, kind, x, y, w, h, color, **kw):
        el = {"id": f"e{self._id()}", "type": kind, "x": x, "y": y, "width": w, "height": h,
              "angle": 0, "strokeColor": COLORS.get(color, color), "backgroundColor": "transparent",
              "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid",
              "roughness": self.rough, "opacity": 100, "groupIds": [], "frameId": None,
              "roundness": None, "seed": self._id() * 7919, "version": 1,
              "versionNonce": self._id(), "isDeleted": False, "boundElements": [], "updated": 1,
              "link": None, "locked": False}
        el.update(kw)
        return el

    def text(self, x, y, s, color="ink", size=14, family=MONO):
        lines = s.split("\n")
        w = max(len(line) for line in lines) * size * (0.6 if family == MONO else 0.55)
        h = len(lines) * size * 1.25
        self.els.append(self._base("text", x, y, w, h, color, text=s, originalText=s,
                                   fontSize=size, fontFamily=family, textAlign="left",
                                   verticalAlign="top", containerId=None, lineHeight=1.25,
                                   baseline=int(size)))
        return h

    def box(self, b):
        color = b.get("color", "ink")
        self.els.append(self._base("rectangle", b["x"], b["y"], b["w"], b["h"], color,
                                   strokeStyle="dashed" if b.get("dashed") else "solid",
                                   roundness={"type": 3}))
        cy = b["y"] + 14
        if b.get("title"):
            cy += self.text(b["x"] + 16, cy, b["title"], color, b.get("title_size", 20), HAND) + 10
        for line in b.get("lines", []):
            s, c = (line[0], line[1]) if isinstance(line, list) else (line, "ink")
            cy += self.text(b["x"] + 16, cy, s, c, b.get("size", 14))
        if cy > b["y"] + b["h"]:
            print(f'warning: box "{b.get("title", "")}" needs {round(cy - b["y"] + 14)} units of '
                  f'height, has {b["h"]}', file=sys.stderr)

    def zone(self, z):
        color = z.get("color", "grey")
        self.els.append(self._base("rectangle", z["x"], z["y"], z["w"], z["h"], color,
                                   strokeStyle="dashed", strokeWidth=1, roundness={"type": 3}))
        if z.get("label"):
            self.text(z["x"] + 16, z["y"] - 30, z["label"], color, 20, HAND)

    def ellipse(self, e):
        color, size = e.get("color", "ink"), e.get("size", 18)
        self.els.append(self._base("ellipse", e["x"], e["y"], e["w"], e["h"], color))
        lines = e.get("text", "").split("\n")
        tw = max(len(line) for line in lines) * size * 0.55
        th = len(lines) * size * 1.25
        self.text(e["x"] + (e["w"] - tw) / 2, e["y"] + (e["h"] - th) / 2, e.get("text", ""),
                  color, size, HAND)

    def arrow(self, a):
        pts = a["points"]
        x0, y0 = pts[0]
        rel = [[px - x0, py - y0] for px, py in pts]
        xs, ys = [p[0] for p in rel], [p[1] for p in rel]
        color = a.get("color", "ink")
        self.els.append(self._base("arrow", x0, y0, max(xs) - min(xs), max(ys) - min(ys), color,
                                   strokeStyle="dashed" if a.get("dashed") else "solid",
                                   points=rel, lastCommittedPoint=None, startBinding=None,
                                   endBinding=None, startArrowhead=None, endArrowhead="arrow",
                                   roundness={"type": 2} if len(pts) == 2 else None))
        if a.get("label"):
            lab = a["label"]
            self.text(lab["x"], lab["y"], lab["text"], lab.get("color", color),
                      lab.get("size", 18), HAND)

    def note(self, n):
        self.text(n["x"], n["y"], n["text"], n.get("color", "red"), n.get("size", 14),
                  HAND if n.get("font") == "hand" else MONO)


def build(spec):
    scene = Scene(spec.get("rough", True))
    for z in spec.get("zones", []):
        scene.zone(z)
    for b in spec.get("boxes", []):
        scene.box(b)
    for e in spec.get("ellipses", []):
        scene.ellipse(e)
    for a in spec.get("arrows", []):
        scene.arrow(a)
    for n in spec.get("notes", []):
        scene.note(n)
    return {"type": "excalidraw", "version": 2, "source": "https://excalidraw.com",
            "elements": scene.els, "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None},
            "files": {}}


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: handdrawn.py spec.json out.excalidraw")
    with open(sys.argv[1]) as f:
        spec = json.load(f)
    with open(sys.argv[2], "w") as f:
        json.dump(build(spec), f, indent=1)
    print("wrote", sys.argv[2])
