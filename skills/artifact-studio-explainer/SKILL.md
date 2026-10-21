---
name: artifact-studio-explainer
description: Default for explainer videos. Turns a topic, investigation, design or codebase question into a narrated 1920x1080 MP4 in the artifact-studio look (light theme, clean SVG kit diagrams that build step by step, repo maps, flows, wide tables, spoken-word captions), rendered locally with the bundled Manim engine (artifact figures full screen, zoomed, with a red highlighter on whatever the narration names). Optionally renders with daybook reel's Studio composition when the user has a daybook reel checkout. Use whenever the user says "create an explainer video about X", "make a video explaining X", "explainer video", "turn this artefact into a video", or wants a walkthrough video of an issue, design or system. Optionally also makes a Claude Motion film of the same storyboard for sharing.
---

# Artifact Studio Explainer

One storyboard, written by you, becomes a narrated video that looks like an artifact-studio page in motion. The default engine is Manim, bundled in `manim/`: it lays out the scenes, voices them, times every reveal to the narration and writes one MP4.

**Platforms.** Tested on macOS. Linux should work with Chrome or Chromium and espeak-ng, but is not tested. Needs uv, ffmpeg, cairo and pango; the `figure` layout also needs Chrome (see `manim/GUIDE.md`).

This skill replaces the generic "which video skill?" question for explainer videos. For a music video, a promo reel or a hand-drawn cartoon, use the other video skills.

## Defaults (always, unless the user says otherwise)

- **artifact-studio look.** White page, Figtree / Bricolage Grotesque / JetBrains Mono, kit diagrams, chips, wide tables. Same rules: no em dash, plain short sentences, honest ("not verified", "est." on estimates), no names of people unless asked.
- **Wide and dense.** Prefer a full-width figure, repo map or table over one big shape. Diagrams short and wide: viewBox 800 wide by 260 to 480 high.
- **Narrated.** One narration per scene, 1 to 4 sentences, spoken plainly. Captions follow the voice word by word.
- **Built, not shown.** Every scene reveals in the order the narration speaks: each `build` step fires as the voice reaches its `at` phrase.
- **4 to 12 scenes, 1.5 to 5 minutes.** Open with a title scene that states the answer (tldr), close with a "what to do" table or points scene.

## Engines

- **Manim (default, `manim/GUIDE.md`).** Use it for every video unless the user asks for Studio. Layouts: `title`, `repomap`, `flow`, `table`, `points` and `figure`. The `figure` layout shows the artifact's real kit SVG (or anatomy frames) full screen and sharp, steps through `data-step` groups, zooms with `focus` and rings whatever the narration names with a red highlighter (`mark`).
- **Studio (optional).** daybook reel's Studio composition, for people who have a daybook reel checkout. See the last section. Use it only when `$DAYBOOK_REEL` points at a checkout and the user asks for it, or the scenes are mostly text. One video uses one engine.

## Pipeline (Manim)

1. **Setup, once.** `skills/artifact-studio-explainer/manim/setup.sh`. Run every command below from `manim/`.
2. **Scope.** One question, one audience. Ground every fact in real code, tickets, runs or an existing artifact (read it with the Artifact tool). If the topic already has an artifact page, reuse its diagrams, tables and wording.
3. **Pick a work folder.** Work content (company code, tickets, internal designs) goes in a work folder outside this repo, such as `<your work tree>/explainers/<slug>/`. Personal topics go in the session scratchpad or your own projects folder. Never write a topic's storyboard into this skill's repo.
4. **Write `storyboard.json`** in that folder. The format (layouts, build actions, every field) is in `manim/GUIDE.md`. Start from `manim/examples/demo/storyboard.json`.
5. **Draw figures** as `svg/KEY.svg` with the artifact-studio kit (`../codebase-explorer/references/diagram-kit.md`, `diagram-guide.md`, types in `diagram-types.md`), or reuse the artifact's own SVGs. Wrap each beat in `<g data-step="N">` (N from 1). A `step` target must be 0 or a `data-step` value that exists in the svg. Width 800, height at most 480.
6. **Time the reveals with `at`.** Every build step has `"at": "phrase"`, a few words copied from that scene's narration. A phrase not found in the narration, or found only before the previous step, fails the run.
7. **Check stills before voicing.** `.venv/bin/python render.py <folder>/storyboard.json --stills` writes the last frame of each scene to `stills/` in the output folder (`--out`, default `<folder>/out`). Read every PNG. Fix clipped text, overflowing tables, crowded figures, wrong marks, empty space. Repeat until clean.
8. **Render.** `.venv/bin/python render.py <folder>/storyboard.json` voices each scene and writes `<folder>/out/explainer.mp4`. `--only SCENE_ID` renders one scene to `out/<id>.mp4` and leaves `explainer.mp4` alone. Then read 3 or 4 frames at scene midpoints (`ffmpeg -ss T -i explainer.mp4 -frames:v 1 f.png`) to confirm reveals and captions.
9. **Hand over** the mp4 path and its length. Say which voice was used (the run prints it per scene: kokoro, say or espeak-ng). With no voice available the run fails and says how to get one; `--no-voice` makes a silent cut.
10. **Optional: Claude Motion film.** If the user wants a shareable, scrubbable, commentable version, start one from the Motion artifact type (`Artifact` `list` with `scope: "types"`, then follow that type's own instructions). Motion films are wordless and run in a browser player: put the narration on screen as captions, keep the same scenes, and export MP4 from its page. The narrated MP4 stays the primary output.

## Updating

Change the Manim look in `manim/theme.py` (tokens, fonts), `manim/kit.py` (shapes) and `manim/engine.py` (layouts), and keep `manim/GUIDE.md` in step. Old storyboards must keep rendering: add optional fields, never rename or remove one.

## Studio engine (optional, needs daybook reel)

Only for people with a daybook reel checkout. Set `DAYBOOK_REEL` to it; the scripts fail with a clear message when it is missing.

- Storyboard format: `$DAYBOOK_REEL/src/studio/storyboard-guide.md` (not in this repo). Check a draft with `node studio-contract.ts check <storyboard.json>` in `$DAYBOOK_REEL/render`. Example: `examples/cache/storyboard.json`.
- Stills: `scripts/stills.sh <folder>` writes `<folder>/studio-out/stills/`.
- Render: `scripts/render.sh <folder>` writes `<folder>/studio-out/explainer.mp4`.
- To change its look, edit `render/src/studio/` in daybook reel and keep its storyboard guide in step.

## Files

- `manim/GUIDE.md` - the Manim engine: setup, storyboard format, layouts, actions, look rules
- `manim/setup.sh` - one-time env (uv, Python 3.12, manim 0.22.0)
- `manim/render.py` - storyboard to voiced, captioned MP4
- `manim/examples/demo/` - a small working Manim storyboard
- `scripts/` and `examples/cache/` - the optional Studio engine and its example
