# REAN model

A two-by-two grid of the four stages a person moves through before they care about a product: Reach (they hear of it), Engage (they try it), Activate (they really use it) and Nurture (they stay and give back). Each cell lists the channels that drive that stage and the one number that measures it, and a strip underneath shows the conversion between stages. The example is tracekit, an open source tracing CLI: Show HN, GitHub and dev.to for reach; Homebrew, the docs quickstart and a StackBlitz sandbox for engagement; a GitHub Action, the npm SDK and OpenTelemetry export for activation; Discord office hours, first issues and monthly releases for nurture, with the funnel from 48k visits to 85 contributors.

| Hand-drawn | Clean |
|---|---|
| ![hand-drawn](hand.jpg) | ![clean](clean.jpg) |

## Use it to explain

- How an open source project or developer tool turns visitors into contributors, and which channel feeds which stage.
- Where a developer platform's adoption leaks, by putting the measured conversion between stages under the grid.
- Which team owns which stage (DevRel for reach, docs for engagement, SDK team for activation, maintainers for nurture).

Not for: a single user's step-by-step path through a product (use `customer-journey`) or a strict drop-off chart (use `marketing-funnel`).

## Anatomy

| Part | Class | Rule |
|---|---|---|
| Stage cell | `d-box g0`, `g3`, `g4`, `g1` | R top-left, E top-right, A bottom-left, N bottom-right, square corners, cells touching |
| Stage letter | `d-h` scaled 3.2x | One big letter per cell, top-left, as in the template |
| Stage header | `d-h`, `d-s` | Stage name and a one-line meaning beside the letter |
| Stage metric | `d-tag` + `d-m` | The single number for that stage, top-right of the cell |
| Channel card | `d-fillpaper` + `d-logo` + `d-t`, `d-s` | Three per cell, product logo, short name, what it does |
| Measure line | `d-k` + `d-m` | How the stage is measured, at the bottom of the cell |
| Funnel strip | `d-tag acc` + `d-edge acc` + `d-lab` | Stage counts left to right, conversion rate on each arrow |

## Tips

- Keep the letters in reading order (R, E across the top, A, N across the bottom) so the grid reads as a sequence.
- Give every stage a number; a REAN grid without metrics is a list of channels.
- Put conversion rates outside the grid so the cells stay about channels, not maths.

Reference: Figma template REAN model

Source: [example.svg](example.svg)
