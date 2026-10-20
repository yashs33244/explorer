#!/usr/bin/env python3
"""Lay out a repo map (nested containers of mono chips) as a kit SVG.

  repo_map.py spec.json > svg/KEY.svg

A repo map shows how a repository is cut into parts and what each part depends
on: containers for top-level folders or layers, chips for crates, packages or
modules inside them, other repositories beside it, runtime services under it,
and three line styles for links, vendored copies and runtime calls. This script
does the tedious part (chip widths, wrapping, container heights, text sizes on
the kit classes). Edges stay explicit: you give each one its path, because the
route is an editorial choice. Render the result with
../codebase-explorer/scripts/render.sh and fix what you see.

spec.json:

  {"key": "rm",                                  # id prefix (the figure key)
   "width": 1200,                                # viewBox width; height is computed
   "zones": [
     {"id": "apps", "x": 56, "y": 96, "w": 520,  # top-left and width; height is auto
      "h": 300,                                  # optional fixed height (parent zones)
      "g": 0,                                    # colour group 0-5 (omit for ink)
      "title": "Process roots", "path": "apps/",
      "note": "One or two short sentences under the title.",
      "tab": true,                               # draw the title as a tab on the top edge (the repo itself)
      "dash": true,                              # dashed outline: external or in transition
      "chips": ["apps/web", ["apps/api", "on"], ["payments -> pay-svc", "dash"]],
      "groups": [{"label": "Data", "chips": ["db", "migrations"], "note": "Optional line."}]}],
   "edges": [{"d": "M 300 200 V 260", "style": "solid|dash|dot", "g": 0, "arrow": true,
              "from": "apps", "to": "mods",              # zone ids: hover a zone to light its links
              "label": "imports", "lx": 310, "ly": 236, "anchor": "start"}],
   "notes": [{"x": 56, "y": 640, "w": 520, "text": "Layer rule: ..."}],
   "legend": true}                               # line-style legend strip at the bottom

Chip "on" = entry point (bold outline), "dash" = moving or symlinked. "->" in text
becomes an arrow. Zones are drawn first (they are backgrounds), then edges on top,
so end each edge on a zone border or a chip, never across a chip's text.
"""
import html, json, re, sys

MONO, SANS, HEAD, NOTE = 7.25, 6.4, 8.6, 7.2   # approximate px per character: d-m, d-s, d-zt, d-tn
CHIP_H, CHIP_GAP, PAD = 22, 6, 14


def esc(t):
    return html.escape(str(t).replace('->', '→'), quote=True)


ID = re.compile(r'^[A-Za-z0-9_-]+$')
STYLES = {'solid': '', 'dash': ' dash', 'dot': ' dot'}


def group(obj, where):
    """The colour group as ' gN', or '' when there is none; anything but 0-5 is an error."""
    g = obj.get('g')
    if g is None:
        return ''
    if g not in range(6):
        sys.exit(f'{where}: "g" must be 0 to 5, not {g!r}')
    return f' g{g}'


def need(obj, keys, where):
    missing = [k for k in keys if k not in obj]
    if missing:
        sys.exit(f'{where}: missing {", ".join(missing)} (see the docstring of repo_map.py)')


def wrap(text, width, per_char):
    words, lines, cur = str(text).split(), [], ''
    for w in words:
        trial = (cur + ' ' + w).strip()
        if cur and len(trial) * per_char > width:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    return lines + ([cur] if cur else [])


def chip_w(text):
    return round(len(str(text).replace('->', '>')) * MONO + 16)


def flow_chips(chips, x, y, width, out, where):
    """Place chips left to right, wrapping; return the y below the last row."""
    cx, cy = x, y
    for c in chips:
        text, mode = (c, '') if isinstance(c, str) else (c[0], c[1] if len(c) > 1 else '')
        w = chip_w(text)
        if w > width:
            print(f'warning: {where}: chip "{text}" is {w} wide but the zone fits {width}; widen the zone or shorten it', file=sys.stderr)
        if cx > x and cx + w > x + width:
            cx, cy = x, cy + CHIP_H + CHIP_GAP
        cls = 'd-chip' + (f' {mode}' if mode else '')
        tcls = 'd-mb' if mode == 'on' else 'd-m'
        out.append(f'<rect class="{cls}" x="{cx}" y="{cy}" width="{w}" height="{CHIP_H}"/>'
                   f'<text class="{tcls}" x="{cx + 8}" y="{cy + 15}">{esc(text)}</text>')
        cx += w + CHIP_GAP
    return cy + CHIP_H if chips else y


def zone(z, out, key):
    need(z, ('id', 'x', 'y', 'w', 'title'), f'zone {z.get("id", "?")}')
    if not ID.match(str(z['id'])):
        sys.exit(f'zone {z["id"]!r}: ids are letters, digits, - and _ only (they become data-node and data-edge values)')
    x, y, w = z['x'], z['y'], z['w']
    g = group(z, f'zone {z["id"]}')
    inner = w - 2 * PAD
    body = []
    if z.get('tab'):
        tw = round(len(z['title']) * MONO + 24)
        body.append(f'<rect class="d-band" x="{x + 16}" y="{y - 12}" width="{tw}" height="24"/>'
                    f'<text class="d-mb" x="{x + 28}" y="{y + 4}">{esc(z["title"])}</text>')
        cy = y + 22
    else:
        title = f'<text class="d-zt{g}" x="{x + PAD}" y="{y + 24}">{esc(z["title"])}</text>'
        if z.get('path'):
            px = x + PAD + round(len(z['title']) * HEAD) + 10
            title += f'<text class="d-m{g}" x="{px}" y="{y + 24}">{esc(z["path"])}</text>'
        body.append(title)
        cy = y + 30
    for line in wrap(z.get('note', ''), inner, SANS):
        cy += 17
        body.append(f'<text class="d-s" x="{x + PAD}" y="{cy}">{esc(line)}</text>')
    if z.get('chips'):
        cy = flow_chips(z['chips'], x + PAD, cy + 10, inner, body, f'zone {z["id"]}')
    for grp in z.get('groups', []):
        cy += 22
        body.append(f'<text class="d-g" x="{x + PAD}" y="{cy}">{esc(grp["label"])}</text>')
        cy = flow_chips(grp.get('chips', []), x + PAD, cy + 8, inner, body, f'zone {z["id"]}')
        for line in wrap(grp.get('note', ''), inner, SANS):
            cy += 17
            body.append(f'<text class="d-s" x="{x + PAD}" y="{cy}">{esc(line)}</text>')
    fit = cy - y + PAD + 2
    if z.get('h') and z['h'] < fit:
        print(f'warning: zone {z["id"]}: "h" is {z["h"]} but its content needs {fit}', file=sys.stderr)
    h = z.get('h') or fit
    dash = ' dash' if z.get('dash') else ''
    node = '' if z.get('tab') else f' data-node="{esc(z["id"])}"'  # the repo outline itself is a frame, not a part
    out.append(f'<g id="{esc(key)}-{esc(z["id"])}"{node}><rect class="d-zone{g}{dash}" x="{x}" y="{y}" width="{w}" height="{h}"/>'
               + ''.join(body) + '</g>')
    return y + h


def edge(e, out, key, i):
    need(e, ('d',), f'edge {i}')
    if e.get('label'):
        need(e, ('lx', 'ly'), f'edge {i} ("{e["label"]}")')
    if e.get('style', 'solid') not in STYLES:
        sys.exit(f'edge {i}: "style" is solid, dash or dot, not {e["style"]!r}')
    style = STYLES[e.get('style', 'solid')]
    g = group(e, f'edge {i}')
    for end in ('from', 'to'):
        if e.get(end) is not None and not ID.match(str(e[end])):
            sys.exit(f'edge {i}: "{end}" {e[end]!r} is not a zone id')
    marker = f' marker-end="url(#{key}-ah{g.strip()[1:]})"' if e.get('arrow', True) else ''
    link = f' data-edge="{esc(e["from"])} {esc(e["to"])}"' if e.get('from') and e.get('to') else ''
    parts = [f'<path id="{esc(key)}-e{i}" class="d-edge{style}{g}" d="{esc(e["d"])}"{marker}/>']
    if e.get('label'):
        anchor = e.get('anchor', 'start')
        if anchor not in ('start', 'middle', 'end') or not all(isinstance(e[k], (int, float)) for k in ('lx', 'ly')):
            sys.exit(f'edge {i}: "lx" and "ly" are numbers and "anchor" is start, middle or end')
        parts.append(f'<text class="d-lab" x="{e["lx"]}" y="{e["ly"]}" text-anchor="{anchor}">{esc(e["label"])}</text>')
    out.append(f'<g{link}>' + ''.join(parts) + '</g>' if link else ''.join(parts))


def legend(y, width, out):
    """Line styles and chip styles in a strip, wrapping to a second row on narrow maps; returns the last row's y."""
    items = [('line', '', 'depends on (links)'), ('line', ' dash', 'vendored, pinned copy or submodule'),
             ('line', ' dot', 'calls at runtime'), ('chip', ' on', 'entry point'), ('chip', ' dash', 'moving or symlinked')]
    x = 56
    for kind, style, label in items:
        span = 46 + round(len(label) * SANS)
        if x > 56 and x + span > width - 40:
            x, y = 56, y + 30
        if kind == 'line':
            out.append(f'<path class="d-edge{style}" d="M {x} {y} H {x + 36}"/>')
        else:
            out.append(f'<rect class="d-chip{style}" x="{x + 7}" y="{y - 11}" width="22" height="22"/>')
        out.append(f'<text class="d-s" x="{x + 46}" y="{y + 4}">{esc(label)}</text>')
        x += span + 36
    return y


def main():
    if len(sys.argv) != 2:
        sys.exit('usage: repo_map.py spec.json > svg/KEY.svg')
    spec = json.load(open(sys.argv[1]))
    need(spec, ('zones',), sys.argv[1])
    key, width = spec.get('key', 'rm'), spec.get('width', 1200)
    edges, zones = [], []
    bottom = 0
    for i, e in enumerate(spec.get('edges', [])):
        edge(e, edges, key, i)
    for z in spec['zones']:
        end = zone(z, zones, key)
        print(f'zone {z["id"]}: y {z["y"]} to {end}', file=sys.stderr)  # place the next zone and edges from these
        bottom = max(bottom, end)
    for n in spec.get('notes', []):
        need(n, ('x', 'y', 'w', 'text'), 'note')
        lines = wrap(n['text'], n['w'] - 24, NOTE)
        h = 16 + 17 * len(lines)
        zones.append(f'<rect class="d-note" x="{n["x"]}" y="{n["y"]}" width="{n["w"]}" height="{h}"/>' + ''.join(
            f'<text class="d-tn" x="{n["x"] + 12}" y="{n["y"] + 22 + 17 * j}">{esc(l)}</text>' for j, l in enumerate(lines)))
        bottom = max(bottom, n['y'] + h)
    tail = []
    if spec.get('legend', True):
        bottom = legend(bottom + 40, width, tail) + 12
    height = bottom + 36
    groups = sorted({'' if e.get('g') is None else str(e['g']) for e in spec.get('edges', [])})
    markers = ''.join(
        f'<marker id="{key}-ah{g}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        f'<path class="d-fillink{" g" + str(g) if g != "" else ""}" d="M0 0 L10 5 L0 10 z"/></marker>' for g in groups)
    title = esc(spec.get('title', 'Repo map'))
    print(f'<svg xmlns="http://www.w3.org/2000/svg" class="hd" viewBox="0 0 {width} {height}" role="img" '
          f'aria-labelledby="{key}-title"><title id="{key}-title">{title}</title><defs>{markers}</defs>'
          + ''.join(zones) + ''.join(edges) + ''.join(tail) + '</svg>')


if __name__ == '__main__':
    main()
