# Contributing

## Before you push

```bash
scripts/check.sh
```

It checks the catalog (every type folder has its files and links), builds the example page with no warnings, checks the repo map example is up to date, compiles the Python scripts, and fails on any em dash.

## Adding a diagram type

1. Make `diagram-types/<category>/<slug>/` with `example.svg` (kit classes only, no hex colours, 32 units of margin), `README.md` (what it is, Use it to explain, Not for, Anatomy, Tips).
2. Render all three styles: `skills/codebase-explorer/scripts/render.sh example.svg modern.jpg light modern`, and the same with `clean` and `hand`. Then run `python3 skills/codebase-explorer/scripts/check-overflow.py example.svg` to catch titles that outgrow their box in the modern style.
3. Add a row to `diagram-types/catalog.json`, then run `node skills/codebase-explorer/scripts/build-catalog.js`.
4. If a page should pick it, add a row to `skills/artifact-studio/references/choosing-diagrams.md`.

## Changing the kit

A kit class lives in two files: `skills/artifact-studio/assets/page-template.html` (pages) and `skills/codebase-explorer/assets/style.css` (renders, all three styles). Change both, run `python3 scripts/sync-modern.py` after any change inside the modern block, document the class in `skills/codebase-explorer/references/diagram-kit.md`, then re-render the catalog with `render.sh --catalog`.

## Writing rules

Plain short sentences, no em dash, no private or work content (this repo is public). Decisions that shape the repo get a short record in `docs/adr/`.
