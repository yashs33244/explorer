# Excalidraw diagrams and database tables

Two rules from the user, applied on every page:

1. **Engineering diagrams are drawn in Excalidraw** and embedded in the page.
2. **Database tables are drawn as schema-designer cards** (`scripts/er_diagram.py`).

The kit SVG figures stay for charts, timelines, matrices and other non-engineering figures.

## Excalidraw figures

What counts as an engineering diagram: architecture, request or data flow, sequence, component
or repo map, deployment or network path, state or decision flow, PR or dependency plan.

1. Write a layout spec (`spec/KEY.json`). The format is in the docstring of `scripts/excalidraw.py`:
   - `zones`: dashed hachure areas with a label, for repos, clusters or regions.
   - `nodes`: boxes with `id`, `x`, `y`, `w`, `h`, `text` (use `\n`), `color` and `shape` (rectangle, ellipse or diamond).
   - `edges`: `from`, `to`, an optional `label`, `dashed`, `side` (`h` or `v`) and explicit `points`.
   - `texts`: free text.
2. Generate the scene with `python3 scripts/excalidraw.py spec/KEY.json exc/KEY.excalidraw`.
3. Describe it in figs.json:

   ```json
   {"KEY": {"type": "excalidraw", "src": "exc/KEY.excalidraw", "theme": "light",
            "why": "...", "title": "...", "aria": "one sentence", "caption": "...", "size": "wide"}}
   ```

   The figure follows the page theme (dark by default); set `theme` only to override it.
4. build.py draws the scene **at build time**: headless Chrome runs Excalidraw 0.17.6's own
   `restoreElements` and `exportToSvg`, and the SVG is inlined in the page (cached in
   `~/.cache/artifact-studio/excalidraw`). The reader's browser loads no React, no CDN and no
   fonts, so what you checked is what they see. If Chrome is missing, the build warns and falls
   back to drawing in the browser.
   - The SVG gets class `hd`, so Full screen, zoom and pan work.
   - A "Download for Excalidraw" button saves `KEY.excalidraw.json`, which opens at excalidraw.com.
5. Publish with `capabilities: {"downloads": true}`. The claude.ai viewer only saves files
   through that capability, and `.excalidraw` is not on its extension allowlist, which is why the
   file is `.json`. Outside claude.ai the button falls back to a plain download.

Why build time: Excalidraw's exported SVG asks for its Virgil font from a CDN path that does not
resolve, and a hosted page may block font downloads anyway. The reader then sees a wider fallback
serif that overflows every shape. Hence the defaults below.

Defaults in `excalidraw.py`:
- Helvetica (`fontFamily` 2), a system font, so build-time measuring matches the reader.
- Clean strokes (`roughness` 0). Set `"rough": true` in the spec for the hand-drawn look.
- Box text is centred by the generator; a diamond's text gets its middle half.
- A node too small for its text grows, with a warning. A label longer than its arrow segment
  warns. Treat every warning as a layout bug: move nodes, do not ignore it.

Layout rules:
- Node `size` 18 (the default). Size boxes for their text: about 10 px per character at size 18,
  plus 32 px; 22 px per line plus 24 px of height.
- Diamonds need twice the text box: at least 280 by 170 for three short lines.
- Keep the whole scene under about 1,400 units wide, or the text shrinks below 13 px on a laptop.
  Five columns do not fit: put the decision and its outcomes on a second row.
- Leave at least 130 units between boxes joined by a labelled arrow; 1 to 3 words per label.
- Lay out in lanes or rows, so arrows run straight or with one elbow. Use `side` and `points`
  to keep an arrow from crossing a box.
- Colours are Excalidraw's palette names: grey, red, pink, violet, blue, cyan, green, yellow, orange and white. Use red for failures, green for new parts and yellow for decisions.

Check by eye before publishing, every time (you cannot judge a diagram from its JSON): build,
screenshot the section with headless Chrome, read the PNG, fix and repeat. Two or three rounds
is normal.

## Database tables (schema designer style)

Whenever a page shows database tables, kind detail tables or a schema change, draw them with
`scripts/er_diagram.py`, never as plain boxes or a neutral ER figure.

Each table is a dark card:
- a coloured header bar, with colour per schema or domain (violet, blue, green, red, orange, teal, grey);
- one row per column with a key mark (gold for PK, red for FK), the column name, the type in italic mono and `NN` for not null;
- a green tint and bar on new or changed columns.

Relationship lines join the related columns, with a crow's foot on the many side and a double
bar on the one side. A legend explains PK, FK, NN, new and the many side.

```bash
python3 scripts/er_diagram.py spec/schema.json > svg/schema.svg
```

Use figs.json type `er-diagram`. The colours are `--er-*` tokens in `assets/page-template.html`, so
the cards stay dark on light and dark pages alike.

Always pair the figure with a migrations table with these columns: kind or table, migration, column, type, what null means, and who writes it.
