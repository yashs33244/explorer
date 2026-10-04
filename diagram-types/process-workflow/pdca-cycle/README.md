# Plan Do Check Act (PDCA)

A four-quadrant wheel with clockwise arrows around it for one improvement loop: Plan a hypothesis, Do a small experiment, Check the measurement, Act by standardising or starting the next cycle. Each quadrant links to a card with the concrete evidence for that phase. The example is cycle 3 of an effort to cut flaky tests in a monorepo CI, from a 4.1% flaky rate down to 1.3%.

| Hand-drawn | Clean |
|---|---|
| ![hand-drawn](hand.jpg) | ![clean](clean.jpg) |

## Use it to explain

- An iterative reliability fix such as reducing flaky CI tests, with the metric before and after.
- A performance tuning loop: hypothesis, canary change, measured p99, rollout as default.
- Why a team runs small pilots (one service) before changing shared test fixtures for everyone.

Not for: a one-off linear process or a project timeline; use a flowchart or Gantt chart.

## Anatomy

| Part | Class | Rule |
|---|---|---|
| Quadrants | `d-fill g4`, `g3`, `g5`, `g1` | Plan top left, then clockwise: Do, Check, Act |
| Quadrant name | `d-h` + `d-tw` | the phase and a two-word question or verb |
| Hub | `d-fillpaper` circle | the cycle number and sprint |
| Cycle arrows | `d-edge thick` arcs | four clockwise arcs, one per boundary |
| Evidence card | `d-box` same colour + `d-logo` | three facts and one mono line (metric, tag or file) |
| Leader | `d-edge dash` | joins the quadrant to its card, no arrowhead |

## Tips

- Put a number in Plan and the same number in Check so the loop shows its effect.
- Keep Do small: one service or one team, so Check is cheap.
- Make Act name the next cycle's target, which closes the loop.

Reference: Figma template Plan Do Check Act (PDCA)

Source: [example.svg](example.svg)
