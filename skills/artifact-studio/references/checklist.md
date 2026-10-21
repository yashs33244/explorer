# Pre-publish checklist (taste gate)

Run it before publishing. `build.py` checks the starred items and warns; the rest are on you.

## Answer and emphasis

- [ ] The first screen states the answer (a `.tldr` with one `<mark>`), not the topic.
- [ ] Something on the page is highlighted (`mark`, `b.k`, `.metric`, a callout, a key column or row). *
- [ ] Each section has at most one `<mark>`, a few `b.k` key terms on first use, and `.metric` on the numbers that matter.
- [ ] Every table has a `<thead>`, and every table with 4 or more columns marks the deciding column (`th.key`) or the rows that matter (`tr.key`). *
- [ ] Repeating-value columns (status, owner, layer) carry `data-filter`; long tables are `tall`.

## Figures

- [ ] One reader question per figure, recorded as `why`; the type comes from `choosing-diagrams.md`. *
- [ ] Not every figure is the same type. *
- [ ] Within budget (9 nodes, 12 connectors, 2 accents) or split into overview and detail.
- [ ] Rendered and read as a PNG; no overlaps, clipped text, wrong arrows; 32 units of margin.
- [ ] Big figures use `"size": "bleed"`; repo maps are drawn with `repo_map.py`.
- [ ] Every figure is interactive: parts and links carry `data-node` / `data-edge`, ordered figures carry `data-step`. *
- [ ] Detailed, isometric or 3D requests went to the anatomy skill (`detailed-figures.md`), light theme.

## Engineering pages (`--kind engineering`)

- [ ] A failure modes or risks section. *
- [ ] A verification section with real commands. *
- [ ] A components table with real paths in `<code>`. *
- [ ] Each figure's badges are detailed (`t`, `d`, `file`). *
- [ ] Invariants are stated with what enforces each.

## Honesty and form

- [ ] Every file, function, number and command is real; anything unchecked says "not verified"; estimates say `est.`.
- [ ] No em dash anywhere (the build replaces strays). *
- [ ] Looked at the built page at desktop width and at 390px.
