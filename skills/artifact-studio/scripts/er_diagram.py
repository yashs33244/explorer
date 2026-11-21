#!/usr/bin/env python3
"""Draw database tables as an ER figure in the "schema designer" style.

Each table is a dark card with a coloured header bar (colour = schema or domain), one row per
column with a key mark, the column name, its type in italics and NN for NOT NULL. Lines join
the related columns, with a crow's foot on the many side and a bar on the one side. New or
changed columns get a green bar so a migration reads at a glance.

    python3 er_diagram.py spec.json > svg/KEY.svg

spec = {
  "key": "schema",                       # id prefix, unique per page
  "aria": "What the figure shows, one sentence.",
  "width": 800,                          # optional; height is computed
  "tables": [
    {"id": "provider", "title": "model.model_provider", "group": "blue", "x": 40, "y": 40,
     "w": 300,                           # optional, default 300
     "cols": [
       {"n": "id", "t": "uuid", "pk": true, "nn": true},
       {"n": "data_policy", "t": "text", "nn": true, "new": true},
       {"n": "secret_id", "t": "text(64)", "fk": true}]}
  ],
  "rels": [{"from": "model.provider_id", "to": "provider.id", "many": "from"}],
  "legend": true                         # adds a key for PK, FK, NN and new
}

Groups: violet, blue, green, red, orange, teal, grey. Colours come from the page's --er-*
tokens (assets/page-template.html), so the SVG carries no hex values.
"""
import json
import sys
from html import escape as e

HEAD, ROW, PAD = 30, 22, 8


def table_box(t):
    w = t.get("w", 300)
    h = HEAD + len(t["cols"]) * ROW + PAD
    return t["x"], t["y"], w, h


def col_y(t, name):
    for i, c in enumerate(t["cols"]):
        if c["n"] == name:
            return t["y"] + HEAD + i * ROW + ROW / 2 + 3
    sys.exit(f'{t["id"]} has no column {name}')


def key_icon(x, y, kind):
    cls = "er-pk" if kind == "pk" else "er-fk"
    # a small key: ring plus shaft and two teeth
    return (f'<g class="{cls}"><circle cx="{x + 4}" cy="{y}" r="3.6" fill="none" stroke-width="2"/>'
            f'<path d="M{x + 7.6},{y} H{x + 15} M{x + 12},{y} V{y + 3.5} M{x + 15},{y} V{y + 3.5}" '
            f'fill="none" stroke-width="2"/></g>')


def render(spec):
    k = spec["key"]
    tables = {t["id"]: t for t in spec["tables"]}
    bottom = max(t["y"] + table_box(t)[3] for t in spec["tables"])
    W = spec.get("width", 800)
    H = bottom + (70 if spec.get("legend", True) else 32)
    out = [f'<svg class="hd" viewBox="0 0 {W} {H}" role="img" aria-label="{e(spec["aria"])}" '
           'xmlns="http://www.w3.org/2000/svg">']
    # relationships first, so cards sit on top of line ends
    for r in spec.get("rels", []):
        (ta, ca), (tb, cb) = r["from"].split("."), r["to"].split(".")
        A, B = tables[ta], tables[tb]
        ax, _, aw, _ = table_box(A)
        bx, _, bw, _ = table_box(B)
        ya, yb = col_y(A, ca), col_y(B, cb)
        if ax + aw <= bx:          # A left of B
            x1, x2, d1, d2 = ax + aw, bx, 1, -1
        elif bx + bw <= ax:        # A right of B
            x1, x2, d1, d2 = ax, bx + bw, -1, 1
        else:                      # stacked: leave and enter on the left side
            x1, x2, d1, d2 = ax, bx, -1, -1
        mx = (x1 + x2) / 2 if d1 != d2 else min(x1, x2) - 26
        path = f'M{x1},{ya} H{mx} V{yb} H{x2}'
        many_a = r.get("many", "from") == "from"

        def end(x, y, d, many):
            if many:  # crow's foot opening toward the table
                return (f'<path class="er-rel" d="M{x + 14 * d},{y} L{x},{y - 6} M{x + 14 * d},{y} L{x},{y + 6} '
                        f'M{x + 14 * d},{y} L{x},{y}"/><path class="er-rel" d="M{x + 18 * d},{y - 6} V{y + 6}"/>')
            return (f'<path class="er-rel" d="M{x + 9 * d},{y - 6} V{y + 6}"/>'
                    f'<path class="er-rel" d="M{x + 14 * d},{y - 6} V{y + 6}"/>')

        out.append(f'<g data-edge="{k}-{ta} {k}-{tb}"><path class="er-rel" d="{path}"/>'
                   + end(x1, ya, d1, many_a) + end(x2, yb, d2, not many_a)
                   + (f'<text class="er-lab" x="{mx}" y="{min(ya, yb) - 10}" text-anchor="middle">{e(r["label"])}</text>' if r.get("label") else '')
                   + '</g>')
    for t in spec["tables"]:
        x, y, w, h = table_box(t)
        g = t.get("group", "grey")
        out.append(f'<g data-node="{k}-{t["id"]}">')
        out.append(f'<rect class="er-card" x="{x}" y="{y}" width="{w}" height="{h}" rx="6"/>')
        out.append(f'<path class="er-head er-{g}" d="M{x},{y + 6} a6,6 0 0 1 6,-6 H{x + w - 6} a6,6 0 0 1 6,6 V{y + HEAD} H{x} Z"/>')
        out.append(f'<text class="er-title" x="{x + w / 2}" y="{y + 20}" text-anchor="middle">{e(t["title"])}</text>')
        for i, c in enumerate(t["cols"]):
            ry = y + HEAD + i * ROW
            cy = ry + ROW / 2 + 4
            if c.get("new"):
                out.append(f'<rect class="er-new" x="{x + 1}" y="{ry + 2}" width="{w - 2}" height="{ROW - 2}"/>'
                           f'<rect class="er-newbar" x="{x}" y="{ry + 2}" width="3" height="{ROW - 2}"/>')
            if c.get("pk"):
                out.append(key_icon(x + 10, cy - 4, "pk"))
            elif c.get("fk"):
                out.append(key_icon(x + 10, cy - 4, "fk"))
            out.append(f'<text class="er-col" x="{x + 32}" y="{cy}">{e(c["n"])}</text>')
            out.append(f'<text class="er-type" x="{x + w - 44}" y="{cy}" text-anchor="end">{e(c.get("t", ""))}</text>')
            if c.get("nn"):
                out.append(f'<text class="er-nn" x="{x + w - 12}" y="{cy}" text-anchor="end">NN</text>')
        out.append('</g>')
    if spec.get("legend", True):
        ly = H - 30
        out.append(f'<g>{key_icon(40, ly - 4, "pk")}<text class="er-leg" x="62" y="{ly}">primary key</text>'
                   f'{key_icon(170, ly - 4, "fk")}<text class="er-leg" x="192" y="{ly}">foreign key</text>'
                   f'<text class="er-nn" x="300" y="{ly}">NN</text><text class="er-leg" x="326" y="{ly}">not null</text>'
                   f'<rect class="er-new" x="420" y="{ly - 13}" width="26" height="17"/><rect class="er-newbar" x="420" y="{ly - 13}" width="3" height="17"/>'
                   f'<text class="er-leg" x="454" y="{ly}">new or changed column</text>'
                   f'<path class="er-rel" d="M610,{ly - 4} H650 M636,{ly - 4} L650,{ly - 10} M636,{ly - 4} L650,{ly + 2}"/>'
                   f'<text class="er-leg" x="658" y="{ly}">many side</text></g>')
    out.append('</svg>')
    return "\n".join(out)


if __name__ == "__main__":
    print(render(json.load(open(sys.argv[1]))))
