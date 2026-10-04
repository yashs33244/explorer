# Hand-drawn SVG diagram guide

Look to match: soft lavender line art, like a product illustration. Dashed blobs group related parts, rounded boxes carry a color group, small line icons give each part a face, thick friendly strokes, numbered violet badges give the order. See `assets/icons.md` for copy-paste icons and `assets/style.css` (bottom half) for the classes.

## Three diagrams per topic

1. `architecture`: components and how they connect. Who talks to whom, what is shared, what is in memory and what is on disk. Group in dashed blobs, label every arrow with a verb.
2. `lifecycle`: one concrete scenario in time order (a swimlane or a flow) with numbered badges. Return what each number means.
3. `structure`: the anatomy of the key layout (a page, a directory tree, a record, a state machine), annotated with real field or directory names.

## Rules

- One `<svg class="hd" viewBox="0 0 800 H" role="img" aria-label="...">` with H between 340 and 640, no width or height attributes.
- Classes only: `d-blob d-blob2 d-box g0..g5 d-line d-lineacc d-fillacc d-fillink d-fillpaper d-t d-s d-m d-edge (dash, acc) d-lab d-badge d-bt`. No hex colors, no inline fill or stroke colors, no `<style>`, `<script>`, `<foreignObject>` or images.
- Every id starts with `<key>-d<N>-`.
- Text is at least 12 units, labels are 1 to 5 words. Put sentences in the caption, not the drawing. Estimate text width at about 7.3px per character for 14px bold and 6.2px for 12px.
- Align to a grid, keep even gaps, nothing touching, nothing outside the viewBox, text fully inside its box.
- Arrows need a marker head and a verb label. Offset arrow endpoints so two arrows never share one arrowhead.
- Show the real mechanism, not a list of names.

## Render loop

```bash
scripts/render.sh d1.svg d1.light.png light   # then Read the PNG
scripts/render.sh d1.svg d1.dark.png dark     # then Read the PNG
python3 -c "import xml.dom.minidom,sys;xml.dom.minidom.parse(sys.argv[1]);print('xml ok')" d1.svg
```

Fix what you see, up to 3 rounds. Typical problems the critic found: a label struck through by a curve, a badge covering a label, an arrow whose direction contradicts the caption, a dashed arrow that reads as "always" when it means "only if", numbered badges with no legend.
