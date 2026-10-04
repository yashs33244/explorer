# Diagram kit: classes, two styles, logos

Every diagram is one inline `<svg class="hd" viewBox="0 0 800 H">` (H from 300 to 900, no width or height attributes) styled only with these classes. The same file renders in two styles, chosen by `data-dstyle` on the page or on one figure:

- `hand` (default): Excalidraw look. White canvas, rough ink outlines, solid pastel fills, hard offset shadows under boxes and notes, and every label in Excalifont (regular weight, slightly larger, see below). Accent (`acc`) lines are violet.
- `clean`: FigJam-like. Plain white canvas, flat saturated fills, thin near-black outlines, small corners, no shadows, one sans font. Accent lines are blue.

Never name a color in a legend ("blue: order path"): the accent is violet in one style and blue in the other. Draw a sample line or say "colored".

Both styles work in light and dark themes, so never write a hex color, an inline `fill`/`stroke`/`style`, a `<style>`, `<script>` or `<foreignObject>`.

## Shapes

| Class | Use |
|---|---|
| `d-blob`, `d-blob2` | dashed group behind related parts (filled / paper) |
| `d-box` + `g0`..`g5` | a component, a step, an entity. `rx` 10 to 14 |
| `d-band` + `g0`..`g5` | a wide stripe: a layer, a phase, a quadrant, a stage |
| `d-lane`, `d-lane alt`, `d-lanehead` | swimlane rows and their header cell |
| `d-note` + `g1`..`g5` | sticky note (default yellow). Pair with `d-tn` text |
| `d-fill` + `g0`..`g5` | solid fill: chart bars, pie slices, heat cells, dots. Add `o1`/`o2`/`o3` for 25/50/75% opacity |
| `d-soft` + `g0`..`g5` | translucent fill with a solid outline: Venn and Euler sets, ranges |
| `d-grid`, `d-axis` | chart gridlines and axes |
| `d-tag`, `d-tag acc` | small pill behind a short label |
| `d-line`, `d-lineacc`, `d-fillacc`, `d-fillink`, `d-fillpaper` | icon strokes and fills (see `assets/icons.md`) |
| `d-edge` (+ `dash`, `acc`, `thick`) | connectors. Always a marker head when direction matters |
| `d-badge` + `d-bt` | numbered step circle (r 11) and its digit |

## Text

Sizes are for `clean`. In `hand` every label is Excalifont at weight 400: `d-h` 18px, `d-t` 15px, `d-tn` 14px, `d-bt` 13px, the rest 12.5px.

| Class | Size | Use |
|---|---|---|
| `d-h` | 16 bold display | a heading inside the drawing (a layer name, a quadrant title) |
| `d-t` | 14 semibold | box titles |
| `d-s` | 12 muted | box subtitles, axis ticks |
| `d-m` | 12 mono | code, paths, field names |
| `d-k` | 12 mono caps | small kicker above a heading |
| `d-lab` | 12 with halo | arrow labels (the halo keeps a crossing line from striking through) |
| `d-tw` | 12 bold on solid | text sitting on a `d-fill` shape |
| `d-tn` | 13 semibold | text on a sticky note |

Width estimates for `clean`: 14px bold about 7.3px per character, 12px about 6.2px, 16px display about 8.6px. Excalifont in `hand` is wider: budget about 8.5px per character for `d-t`, 10px for `d-h` and 7px for 12.5px text, and size boxes for that, since the same box holds both. Keep at least 10px of padding inside a box.

## Logos

For a named product (a database, a framework, a cloud service) use a logo slot instead of a generic icon:

```svg
<image class="d-logo" data-logo="postgresql.org" data-name="PostgreSQL" x="40" y="30" width="26" height="26"/>
```

Leave out `href`. `scripts/logos.js` fills it at render and build time from logo.dev, inlined as a data URI, with a light tile behind it so dark marks stay visible. It needs a logo.dev publishable key: `LOGO_DEV_TOKEN` in the environment, or `~/.config/explorer/logo-dev.env`. **If a guide needs logos and there is no key, ask the user to sign up at https://logo.dev, copy the publishable key (it starts with `pk_`) and give it to you; store it in that file and never commit it.** Without a key every slot becomes a monogram circle, so the diagram still works. Use the product's real primary domain. A project on a foundation subdomain (`kafka.apache.org`, `flink.apache.org`) always gets a monogram, because Logo.dev returns the foundation's feather for all of them; `logos.js` warns when two domains return the same image. Logos are trademarks of their owners, provided by Logo.dev.

## Ids and markers

Every id starts with `<key>-d<N>-` (the catalog uses `<slug>-d1-`). Define a marker per SVG:

```svg
<defs><marker id="KEY-d1-ah" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,1 L9,5 L0,9 z" class="d-fillink"/></marker></defs>
```

## Render and look

```bash
scripts/render.sh d1.svg hand.jpg  light hand
scripts/render.sh d1.svg clean.jpg light clean
scripts/render.sh d1.svg dark.png  dark  clean     # check the dark theme too
```

To check a drawing against the look it copies, put the two side by side: `scripts/compare.sh reference.png hand.jpg compare.jpg` (needs `uv`; `compare.jpg` is git-ignored). After a change to `style.css` or `filters.svg`, re-render the whole gallery with `scripts/render.sh --catalog`; `build-catalog.js` warns about stale renders.

Read every image. Fix overlaps, clipped text, labels struck through by lines, arrows that point the wrong way, and anything outside the viewBox. The reference to match is `diagram-types/software/layered-architecture/`.
