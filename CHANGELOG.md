# Changelog

## 1.2.0 (2026-10)

- Publish `artifact-studio-explainer`, the explainer video skill. Its bundled Manim engine is the default; the Studio engine is optional and needs a daybook reel checkout. Tested on macOS; Linux should work with Chrome or Chromium and espeak-ng, but is not tested.
- Manim engine: a `figure` layout that shows the page's real SVG figures full screen and sharp, steps through `data-step` groups, zooms with `focus` (capped at 3x) and rings the part being explained with a red highlighter (`mark`), moving the camera first when that part is off screen. Anatomy figures play as captured frames.
- Manim engine: voices each sentence separately, because kokoro truncates long input, and times the words inside each sentence's measured span.
- artifact-studio: `line acc` legend entries, a clear error for unknown legend keys, and about 40px of space beside bleed figures.
- README: the explainer skill, the four-readers showcase and a video frame.

## 1.1.0 (2026-10)

- artifact-studio: figures up to 1180px wide and a "bleed" size for big maps; smaller side margins.
- artifact-studio: highlight classes (`mark`, `b.k`, `.metric`, `.callout`), key columns and rows in tables (`th.key`, `tr.key|good|bad|dim`).
- artifact-studio: tables with 6 or more rows get a filter box, sortable headers, column selects (`th[data-filter]`) and a highlighted-rows toggle.
- artifact-studio: interactive figures: badge and legend linking, node focus (`data-node`, `data-edge`), step-through (`data-step`), zoom and pan in full screen.
- artifact-studio: `--kind engineering` checks, detailed figure badges, and `references/engineering.md` for deeper engineering pages.
- artifact-studio: anatomy figures (`"type": "anatomy"`) for detailed and isometric objects, embedded live.
- New diagram type `repo-map` and `scripts/repo_map.py` to lay one out; new kit classes `d-zone`, `d-zt`, `d-chip`, `d-mb`, `d-edge.dot`.
- New references: highlighting, engineering, interactive, detailed-figures, style-guide, checklist.
- Repo: `.claude-plugin/` manifest, `scripts/check.sh`, `docs/adr/`, this changelog and CONTRIBUTING.md.

## 1.0.0 (2026-10)

- codebase-explorer, artifact-studio and the catalog of 101 diagram types, with hand-drawn and clean styles.
