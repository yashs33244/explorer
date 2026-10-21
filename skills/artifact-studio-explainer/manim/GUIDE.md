# Manim engine

The default engine for the explainer skill, built on Manim Community. It draws engineering scenes that move: repo maps, request paths, data flows, tables that build row by row, and the artifact's own SVG figures with zooms and a red highlighter, each step timed to the narration.

The optional Studio engine (daybook reel) is only for people with a daybook reel checkout; see `../SKILL.md`. Use it when the user asks for it or the scenes are mostly text. One video uses one engine.

Tested on macOS. Linux should work with Chrome or Chromium and espeak-ng, but is not tested.

## Setup (once)

```bash
manim/setup.sh
```

It makes `manim/.venv` with uv on Python 3.12 (newer Pythons may lack wheels) and installs `manim==0.22.0` (pinned: `engine.py` patches manim internals). Needs uv, ffmpeg, cairo and pango (macOS: `brew install uv ffmpeg cairo pango pkgconf`). Figtree, Bricolage Grotesque and JetBrains Mono are committed in `manim/fonts/` with their OFL licences. No LaTeX: the engine never uses `MathTex` or `Tex`.

The `figure` layout also needs Chrome. It uses `$CHROME` if set, else `/Applications/Google Chrome.app` if it exists, else the first of `google-chrome`, `google-chrome-stable`, `chromium`, `chromium-browser` on PATH; with none it fails and says to set `CHROME`.

## Commands

```bash
cd skills/artifact-studio-explainer/manim
.venv/bin/python render.py <folder>/storyboard.json --stills    # last frame of each scene to <out>/stills/
.venv/bin/python render.py <folder>/storyboard.json --no-voice  # silent mp4, 150 wpm timing
.venv/bin/python render.py <folder>/storyboard.json             # voiced mp4
```

Options: `--out DIR` (default `<folder>/out`; stills go to `stills/` inside it too), `--only SCENE_ID` (renders that scene to `<out>/<id>.mp4`, `explainer.mp4` is left alone), `--jobs N` (scenes render in parallel). Output: `<out>/explainer.mp4`. Work files (per scene wav, json spec and mp4) stay in `<out>/work/`.

Loop: write the storyboard, run `--stills`, read every PNG, fix, repeat. Then render with voice and read two or three frames from the mp4 (`ffmpeg -ss T -i explainer.mp4 -frames:v 1 f.png`).

## Voice and timing

- Voice, first that works: daybook reel's kokoro (`$DAYBOOK_REEL/src/voice.ts` under bun, `meta.voice`, default `af_heart`), then macOS `say`, then `espeak-ng`. With none, the run fails and says how to get a voice or to pass `--no-voice`. The run prints which voice each scene used.
- Each sentence is voiced on its own. Common abbreviations (`e.g.`, `i.e.`, `vs.`, `Dr.`) do not end a sentence.
- Word timing is **estimated**, not aligned. ffmpeg trims leading and trailing silence, then the speech span is shared across words by character count, with extra weight for the pause after `,` and `.`. Good enough for reveals and captions; it can drift a few hundred ms inside long sentences. Keep sentences short.
- A reveal lands 0.12 s before its phrase starts. Scene length is audio plus 0.6 s. Each scene's audio is padded to its video length before the concat, so drift never builds up across scenes.

## Storyboard

```json
{
  "meta": { "title": "...", "voice": "af_heart" },
  "scenes": [
    { "id": "s2-map", "layout": "repomap", "kicker": "01 . layout", "heading": "Where the pieces live",
      "narration": "One to four short sentences.",
      "build": [ { "at": "phrase from the narration", "action": "show", "target": "some-id" } ],
      "...layout data...": "see below" }
  ]
}
```

- `id`: letters, digits, `-`, `_`. Unique.
- `narration`: spoken and captioned word by word. No em dash anywhere (the run fails on one).
- `build[]`: `at` is a few words copied from the narration; the step fires as the voice reaches them. **A phrase not found in the narration fails the run before any render.** Case and punctuation are ignored, apostrophes are dropped and hyphens split words (`step by step` matches `step-by-step`). If a phrase repeats, the first hit at or after the previous step wins; a phrase found only before the previous step fails the run.
- `action`:
  - `show`: the target starts hidden and appears at the phrase. Anything never shown by a step is on screen from the start, unless it sits on something hidden (a chip in a hidden container, an edge to a hidden node); then it appears with that parent.
  - `highlight`: accent stroke and acc-soft fill on chips, boxes, containers; accent on edges; a `#fff1b8` band on table rows and points; an acc-soft tint on a table column.
  - `flow`: an accent dot travels along an edge and the edge turns accent. Edges only.
  - `dim`: fades the target to 22 percent.
- Showing something before its parent, or highlighting it before it is shown, fails with a message.
- `kicker` and `heading` (optional, not on `title`): mono accent kicker and a display heading at the top left.

### Layouts

**title**: `kicker`, `title`, `subtitle`, `tldr` (acc-soft box with an accent rule). Targets: `kicker`, `title`, `subtitle`, `tldr`. Open every video with one that states the answer.

**repomap**: `containers[]` in one row, equal widths: `{id, title, path, group (0-5 colour), chips: [{id, label, bold, dashed, badge}]}`. `bold` = entry point, `dashed` = in transition or vendored. Optional `x, y, w, h` (px) on a container places it by hand, for nested boxes. `edges[]`: `{id, from, to, style, label, route, label_at}` between chip or container ids. `style`: `solid` = depends on or links, `dashed` = vendored or pinned copy, `dotted` = calls at runtime. `route: "h" | "v"` forces the elbow direction; `label_at: "start" | "end" | "longest"`. `legend: true` adds the style key under the row. Chip text sizes itself (28 to 22 px) to fit.

**flow**: `nodes[]` `{id, label, sub, group, col, row, badge, w, h}` on a grid (default: one row, `col` = order). `edges[]` as above. Use for request paths and data flows; `flow` the edges in the order the request travels.

**table**: `columns[]`, `rows[][]` (wrap `` `code` `` in backticks for mono), `key` (column index tinted acc-soft, bold accent header), `highlight_rows` (static `#fff1b8` rows). Targets: `header`, `row:N`, `col:N`, `key`. Show rows one by one; a column tint grows with the rows. Text sizes itself (30 to 22 px); too tall fails.

**points**: `points[]` `{id, text, sub, n}` with numbered yellow badges. Good closer ("what to do"). Highlight one with a band.

**figure**: shows the artifact's REAL diagram instead of redrawing it. `{layout: "figure", kicker?, heading?, svg_file?: "svg/KEY.svg", frames?: ["anatomy/frames/01.png", ...], start_step?: N, narration, build}`. Exactly one of `svg_file` or `frames`; paths are relative to the storyboard.

- **Source.** `svgshot.py` renders the svg inside the artifact page CSS (the `<style>` of `artifact-studio/assets/page-template.html`, with the committed fonts in `manim/fonts` loaded as local files and the Google Fonts link only as a fallback) with headless Chrome, white, no padding, 4000 px wide or wider (up to 8000) when a focus rect needs it, but never past about 120 million pixels, so a tall figure renders narrower. On screen a source pixel is never stretched past 1.2 screen pixels (`MAX_UPSCALE` in `figure.py`), which keeps zoomed text sharp. One PNG per `data-step` state (state N shows groups with step <= N, the rest `visibility:hidden`, so nothing moves) plus `all`. Cached in `manim/cache/figures/<hash>/` by svg, CSS, width and script version. Run by hand: `.venv/bin/python svgshot.py svg/KEY.svg [--width 4000]`.
- **Frame.** The figure fills the frame: 64 px left and right, 32 px at the top, a slim kicker and heading line at the top left (56 px band, only when set), the caption bar at the bottom. Every video frame is resampled straight from the high-res PNG (Lanczos) into that area, so zoomed text stays sharp; the cut where a zoom meets the frame edge fades to white.
- **Start.** svg with steps: state `start_step`, else 0 when the build has a `step` action, else `all`. svg without steps: `all`. frames: frame 1.
- **Actions** (timed by `at` like every layout):
  - `step` target N: crossfade (0.5 s) to state N. N must be 0 or a `data-step` value that exists in the svg.
  - `focus` target `"x,y,w,h"`: an eased 1 s camera move so the rect fills about 80 percent of the drawing area, never zoomed past 3x the whole figure (`MAX_ZOOM` in `figure.py`), then the red highlighter draws on it.
  - `mark` target `"x,y,w,h"`: the red highlighter on that rect. If the rect is outside the current view, the camera first glides so it sits near the centre, then the highlighter draws.
  - `all`: no target; zoom back to the whole figure and clear the highlighter.
  - `frame` target N (frames only, 1 based): crossfade to frame N.
- **Rects.** For an svg, `x,y,w,h` are viewBox units (the numbers in the svg source; a negative viewBox origin is handled). For frames, they are the frame's own pixels.
- **The red highlighter.** Whatever the voice names is ringed in red so the viewer can follow: a rounded rect, `#e5484d` stroke 5.5 px on screen, 13 percent red fill, 6 px outside the rect, drawn in over 0.45 s. It lives in screen space, so it tracks the figure through zooms and keeps its line width. A new `mark` or `focus` fades the previous one out (0.3 s); `all` clears it. Mark something on every sentence that points at a part of the figure.
- **Picking rects.** Open the svg and copy the numbers of the element you name: a `<rect x y width height>` is the rect as is; for a group (a zone with its chips, a step's arrows and labels) take the union of its parts plus the text that belongs to it. Keep mark rects tight (the highlighter adds its own 6 px). For `focus`, include some context. Zoom stops at 3x the whole figure, so a small rect fills less than 80 percent: a rect 150 units wide on an 800 wide svg would want about 4x and gets 3x. A `mark` outside the zoomed view moves the camera first, so check stills to see where the view ends up.
- **Failing early.** Before any render: unknown action, a rect that is not four numbers with w and h above 0 or lies outside the figure, a step that is not 0 or an existing `data-step` value, `step` on an svg without steps, `frame` without frames, a missing svg or frame file, an svg without a usable `viewBox` (a percentage width or height is not enough), frames of different sizes.

## Look rules

- artifact-studio light theme only (`theme.py`): white ground, ink `#1e1e1e`, muted `#5c5c5c`, line `#e6e6e6`, accent `#1f7aec`, acc-soft `#e8f1fe`, highlight `#fff1b8`, group fills and tints `--cl0` to `--cl5`.
- Figtree for text, Bricolage Grotesque for headings, JetBrains Mono for chips, paths and code.
- 1920x1080, 30 fps, 48 px side margins, caption bar 104 px at the bottom. No text under 22 px (`theme.MIN_TEXT` clamps it).
- Right-angle edges only, arrow head at the target, label on a white mask beside the line.
- Plain short sentences. Honest labels ("est." on estimates). No em dash.

## Files

- `setup.sh`: env (uv, Python 3.12, manim 0.22.0)
- `fonts/`: Figtree, Bricolage Grotesque, JetBrains Mono and their OFL licences
- `theme.py`: tokens, fonts, px helpers
- `kit.py`: Chip, Box, Container, OrthoEdge, Badge, Table, CaptionBar, TitleCard, heading, legend
- `engine.py`: layouts, build scheduling, one scene render (`engine.py spec.json out.mp4 [--still out.png]`)
- `render.py`: storyboard runner (voice, timing, figure checks and svg shots, parallel scene renders, mux, concat)
- `figure.py`: figure layout checks, camera timeline, highlighter timing, frame compositor (no manim import)
- `svgshot.py`: svg to high-res PNG per `data-step` state with headless Chrome, cached
- `examples/demo/storyboard.json`: title, repo map, table

## Limits

- Word timing is estimated (see above). A real aligner (whisper or Parakeet word timestamps) would be the upgrade.
- Repo map auto layout is one row of containers with stacked chips. Deeper nesting needs hand placed `x, y, w, h`.
- Edges are routed with simple elbows and do not avoid other boxes. If an edge crosses a box, reorder containers or set `route`.
- figure: needs Chrome or Chromium (see Setup; first render of an svg takes about 10 to 15 s, then it is cached). The full view of a big figure (a 1300 wide repo map) has small text; use `focus` to read it. Hidden steps keep their space, so a figure built in steps shows blank room until the step lands. Rects are not snapped to elements; a wrong number marks the wrong place, so check stills.
