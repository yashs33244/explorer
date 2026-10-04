# SVG diagram guide

Every diagram is drawn once and shows in two styles: **hand-drawn** (Excalidraw look: rough ink outlines, pastel fills, hard offset shadows, Excalifont labels) and **clean** (FigJam-like: flat fills, thin outlines, no shadows). The page has a switch; `explorer.config.json` sets the default with `"diagramStyle": "hand" | "clean"`. The class kit, both styles and logos are in `references/diagram-kit.md`. Copy-paste icons are in `assets/icons.md`.

## Pick the form that fits the content

Do not draw everything as boxes and arrows. Choose the diagram type whose shape matches what you are explaining. `references/diagram-types.md` maps "what you want to explain" to a type, and every type has a drawn example with its anatomy in `diagram-types/<category>/<type>/` in the explorer repo. Start from that example's SVG. Some common choices:

| Explaining | Type |
|---|---|
| tiers, and what runs where | `layered-architecture` |
| which tools a system uses, or a migration from one stack to another | `tech-stack-mapping` (with logos) |
| who calls whom over time | `sequence-diagram` |
| a process with branches | `flowchart`, or `cross-functional-flowchart` when teams hand off |
| states and the events that move between them | `state-machine` |
| tables and keys | `er-diagram` |
| one request end to end | `request-lifecycle` |
| the system from outside | `system-context`, then `c4-model` |
| a folder layout | `directory-tree` |

## Three diagrams per topic

1. `architecture`: components and how they connect. Usually `layered-architecture`, `c4-model`, `network-diagram` or `tech-stack-mapping`. Label every arrow with a verb.
2. `lifecycle`: one concrete scenario in time order, with numbered badges. Usually `sequence-diagram`, `request-lifecycle`, `flowchart` or `cross-functional-flowchart`. Say what each number means.
3. `structure`: the anatomy of the key layout. Usually `er-diagram`, `state-machine`, `directory-tree` or `class-diagram`, annotated with real field or directory names.

Put the chosen slug in `meta.json` as `"type"`.

## Rules

- One `<svg class="hd" viewBox="0 0 800 H" role="img" aria-label="...">` with H between 300 and 900, no width or height attributes.
- Classes only (the full list is in `references/diagram-kit.md`). No hex colors, no inline fill or stroke colors, no `<style>`, `<script>` or `<foreignObject>`. The only image allowed is a logo slot, `<image class="d-logo" data-logo="domain">`.
- Every id starts with `<key>-d<N>-`.
- Text is at least 12 units, labels are 1 to 5 words. Put sentences in the caption, not the drawing. Estimate text width at about 7.3px per character for 14px bold and 6.2px for 12px.
- Align to a grid, keep even gaps, nothing touching, nothing outside the viewBox, text fully inside its box.
- Arrows need a marker head and a verb label. Offset arrow endpoints so two arrows never share one arrowhead.
- Show the real mechanism, not a list of names.

## Render loop

```bash
scripts/render.sh d1.svg d1.hand.png light hand    # then Read the PNG
scripts/render.sh d1.svg d1.clean.png dark clean   # then Read the PNG
python3 -c "import xml.dom.minidom,sys;xml.dom.minidom.parse(sys.argv[1]);print('xml ok')" d1.svg
```

Fix what you see, up to 3 rounds. Typical problems the critic found: a label struck through by a curve, a badge covering a label, an arrow whose direction contradicts the caption, a dashed arrow that reads as "always" when it means "only if", numbered badges with no legend.
