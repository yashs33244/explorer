# Bracket planner

A single-elimination bracket drawn from both edges toward the middle: first-round pairs on the far left and right, each pair joined by an elbow connector into the next round, until two finalists meet beside a central winner node. The example is an internal platform engineering hackathon: eight teams (reliability tools on the left, cost and delivery tools on the right) are scored by judges, and Canary Cat, an auto rollback tool, beats Flake Hunt in the final.

| Hand-drawn | Clean |
|---|---|
| ![hand-drawn](hand.jpg) | ![clean](clean.jpg) |

## Use it to explain

- A hackathon, demo day or design-review shootout where projects advance round by round.
- A head-to-head evaluation of vendors or libraries (four databases, two survive the load test, one wins the bake-off).
- A canary or A/B tournament where build candidates are eliminated pairwise until one ships.

Not for: rankings with no pairwise matches (use a bar chart or a scorecard) or anything where losers can come back.

## Anatomy

| Part | Class | Rule |
|---|---|---|
| Round label | `d-k` | One kicker above each column, mirrored on both sides |
| Entrant | `d-box g3` / `d-box g4` | One colour per half; name in `d-t`, project in `d-s` |
| Score | `d-t` or `d-s`, `text-anchor="end"` | Bold for the side that advances, muted for the side that goes out |
| Match connector | `d-edge` | Elbow: out of both boxes, down the middle, into the next round |
| Winner node | circle `d-box g2` + `d-fillacc` star | Sits between the two finalists |
| Champion | `d-k`, `d-h`, `d-s`, `d-m` | Centred under the winner node |
| Legend | `d-tag` + `d-fill g3`/`g4` | Says what each half and each bold score means |

## Tips

- Keep the bracket a power of two; give byes a muted `d-box g0` box rather than leaving a hole.
- The advancing team appears again in the next round, so the score styling only has to show who won, not why.
- Put the scoring rule in the header so a reader trusts the numbers.

Reference: Figma template Bracket planner

Source: [example.svg](example.svg)
