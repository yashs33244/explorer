# SMART goal planning

A five-column board that tests one goal against the SMART criteria: Specific, Measurable, Achievable, Relevant and Time-bound. Each coloured header holds one letter, and the column under it collects the evidence for that criterion as sticky notes, with the tool or setting that backs it at the foot. The example is an engineering goal for the payments platform team: cut checkout-api p95 latency from 480ms to 200ms, measured in Datadog APM, made achievable by an N+1 query fix and a Redis price cache, tied to checkout conversion and the platform OKR, with milestones up to November 15. A goal-statement band at the bottom folds the five columns into one sentence.

| Hand-drawn | Clean |
|---|---|
| ![hand-drawn](hand.jpg) | ![clean](clean.jpg) |

## Use it to explain

- A performance or reliability target (latency, error budget, cost per request) before a team commits a quarter to it.
- Why an OKR key result is or is not credible: which column has no evidence.
- The plan behind an SLO change, from the metric definition to the rollout dates.

Not for: tracking work day by day once the goal is set (use `gantt-chart` or `project-plan`).

## Anatomy

| Part | Class | Rule |
|---|---|---|
| Criterion header | `d-box g1`, `g5`, `g0`, `g4`, `g3` + `d-h` (scaled letter) + `d-t` | One colour per letter, in SMART order, same width |
| Column body | `d-box` | One white cell per criterion, same height across the row |
| Evidence | `d-note` + `d-tn` | Two short lines per note; yellow for facts, pink for an exclusion, blue for a constraint or baseline |
| Backing tool | `d-logo` + `d-t` + `d-m` | Foot of the column: the product and the exact metric, key or setting |
| Milestones | `d-edge` + `d-fill` dots + `d-t`/`d-s` | Vertical timeline in the T column; the final date gets a larger `g3` dot |
| Goal statement | `d-band g2` + `d-k` + `d-t` | One sentence spanning all columns |

## Tips

- Write numbers on the notes (480ms, 250ms alert, 20% capacity); a SMART board without numbers is a wish list.
- If a column ends up with one weak note, that is the finding: say so in the caption.
- Keep the goal statement under 90 characters so it fits on one line.

Reference: Figma template SMART goals

Source: [example.svg](example.svg)
