# Interactive figures and tables

Every page built by `build.py` is interactive with no extra work, and a little markup unlocks more. Everything degrades to the full static figure without JavaScript, in print and under reduced motion.

## Free on every figure

| Interaction | How it works | Needs |
|---|---|---|
| Badge linking | Hover or Tab to a row of the badge list under a figure and its numbered badge in the drawing gets an accent ring (and the other way round) | numbered `d-badge` + `d-bt` in the SVG, `badges` in figs.json |
| Legend filter | Hover a colour chip or line style in the legend and only the parts with that colour or line style stay in view | `legend` in figs.json: `["--cl1-f", "..."]`, `["line dash", "..."]`, `["line dot", "..."]` |
| Full screen | Viewport overlay; wheel or `+` / `-` to zoom, drag to pan, `Fit` to reset; Esc closes | nothing |
| Table tools | Filter box, sortable headers, column selects, highlighted-rows toggle | see `highlighting.md` |

## Required on every figure

Every kit figure carries `data-node` / `data-edge` groups, `data-step` groups, or both; `build.py` warns when a figure has neither. Charts mark each bar, point or cell as a `data-node` so hovering one dims the rest.

## The markup

**Node focus.** Wrap each part in `<g data-node="id">` and each link in `<g data-edge="from to">` (or put `data-edge` on the path). Hovering or tabbing to a part dims everything except it, its links and its direct neighbours; a click pins the focus, Esc or a click on empty space clears it. When parts are nested in the DOM (a `data-node` group inside another), focusing a container keeps its parts lit, focusing a part keeps its containers lit, and moving from a part onto its container hands focus to the container. `repo_map.py` writes a `data-node` for every container (as siblings, not nested) and a `data-edge` for every edge that has `from` and `to`. Enter or Space pins from the keyboard.

```svg
<g data-node="api"><rect class="d-box g4" .../><text class="d-t" ...>api</text></g>
<g data-edge="web api"><path class="d-edge" d="..."/><text class="d-lab" ...>calls</text></g>
```

**Step-through.** Wrap each beat in `<g data-step="N">` (N from 1), the same groups the explainer video reveals. The figure bar gets `<  step 2 / 5  >  All`: later steps fade out, the current one is outlined in accent. The page opens on All, so nothing is hidden by default. Use it for request paths, build pipelines and anything with an order.

Rules:

- Interaction never hides meaning. The static figure (All) is complete; focus and steps only take things away for a moment.
- Ids and `data-node` names are short, unique within the figure and match the words in the caption and tables.
- Keyboard first: every hover has a focus equivalent (parts and badge rows are tabbable).
- Detailed, isometric or 3D objects with live motion come from the anatomy skill (`detailed-figures.md`), not from scripting a kit SVG.
