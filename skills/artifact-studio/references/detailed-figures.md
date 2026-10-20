# Detailed, isometric and interactive figures (the anatomy skill)

The kit diagrams in this skill are flat, clean and fast to draw. Some figures need more: the user asks for "more detail", "isometric", "3D", "premium", "Linear-style", "show it as a real thing", or the idea is a mechanism that a box-and-arrow figure flattens (a cache key, a rate limiter, back-pressure, a lock, a scheduler, a shared GPU context). For those, build the figure with the **anatomy** skill (github.com/wheresryan22/anatomy, MIT) and embed it in the page.

Anatomy turns the idea into a working physical object (a pin-tumbler lock for a cache key, a gantry plotter for one GPU context serving many canvases) built from 40 to 150 small shaded isometric parts, with a live readout and calm motion driven by a small true model.

## When to use which

| The reader needs | Use |
|---|---|
| Parts, flows, order, data shape, a repo map, a chart | a kit diagram (`choosing-diagrams.md`); it is interactive on the page already (hover, focus, steps) |
| The same structure, with more labels and room | a kit diagram at `"size": "bleed"`, or an overview plus a detail figure |
| To *feel* how a mechanism behaves: thresholds, matching, capacity, wear, a moving part | an anatomy figure |
| Something the user explicitly asks to be isometric, 3D or highly detailed | an anatomy figure |
| Fire, water, light, glow as part of the explanation | an anatomy figure with its WebGL layer |

At most one or two anatomy figures per page: they are the hero, kit diagrams carry the rest. Never redraw a kit diagram as an isometric object just for looks.

## How

1. **Install once.** `npx skills add wheresryan22/anatomy -g -a claude-code` (or clone it into your agent's skills folder). Needs Node 20.10+ and Chrome.
2. **Load the anatomy skill** and follow its workflow: size it (a page figure is a **Figure**: one mechanism, 40 to 80 parts), collect the true numbers, invent the object, write the parts list, build, then verify with its capture and audit scripts.
3. **Match the page.** Build the light theme (`node build.mjs --light`): artifact pages are light only. Keep the card's title short and the readout true.
4. **Keep the source with the page,** not in this repo: `anatomy/<name>/build.mjs` next to `body.html`, writing `anatomy/<name>/<name>-light.html`.
5. **Embed it.** In `figs.json`:

   ```json
   {"d3": {"type": "anatomy", "src": "anatomy/lock/lock-light.html", "height": 620,
           "why": "Why does an unchanged input skip the work?",
           "title": "The cache key as a lock", "caption": "Each pin is one input hash. The plug turns only when every pin sits at the shear line."}}
   ```

   `build.py` embeds the built page live with `iframe srcdoc` (the artifact stays one file), adds the type chip and the Full screen button, and keeps the caption and badges under it. `src` is relative to the `figs.json` that names it (also in site mode).
6. **Check it on the page,** not only alone: render the built page and look at the figure at desktop width and at 390px.

## In the explainer video

For a scene that shows an anatomy object, record its idle tour or a scripted sequence with anatomy's `scripts/drive.mjs` (contact sheet or frames), and place the frames in the video scene of whichever video tool you use (for example the local `artifact-studio-explainer` skill, which is not part of this repo). Narrate what the readout shows.
