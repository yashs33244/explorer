# Vision board

A single board with a headline goal across the top and a loose mosaic of tiles below it: squares, wide panels, circles and a diamond, each holding one aspiration with a number that proves it. The example is a platform team's FY2027 vision, "ship on Friday, sleep on Saturday": 40 deploys a day, a Backstage to GitHub Actions to Argo CD golden path, quiet on-call, p99 and SLO targets, a 30% AWS cost cut, retiring Jenkins and tracing every service with OpenTelemetry.

| Hand-drawn | Clean |
|---|---|
| ![hand-drawn](hand.jpg) | ![clean](clean.jpg) |

## Use it to explain

- Where an engineering team wants to be in a year, with one measurable target per theme.
- The handful of platform bets (golden path, cost, observability) that a roadmap will later break down.
- What "done" looks like for a migration, such as retiring a CI system or reaching full trace coverage.

Not for: the plan, owners or dates to get there (use `project-plan` or `gantt-chart`).

## Anatomy

| Part | Class | Rule |
|---|---|---|
| Board | `d-box` | One frame around everything, like a pinned page |
| Headline | `d-box g3` + `d-k`, `d-h` | The one-sentence vision, full width at the top |
| Tile | `d-box g1`..`g5` + `d-k`, `d-h`, `d-s` | Kicker names the theme, heading states the target as a number |
| Target dot | `d-fill g3` + `d-tw`, `d-fillpaper` circle | Short SLO-style targets in circles between tiles |
| Bet | diamond `d-box g4` + `d-logo` | A one-off decision, such as retiring a tool |
| Proof | `d-fill` bars, `d-fillpaper` track | A tiny chart or progress bar inside the tile |
| Tools | `d-logo` | Real products behind the goal |

## Tips

- Every tile needs a number; "better on-call" is a wish, "14 to 3 pages a week" is a vision.
- Vary tile shapes and sizes so the board reads as a collage, not a table.
- Keep it to six or seven tiles; more turns it into a backlog.

Reference: Figma template Vision board

Source: [example.svg](example.svg)
