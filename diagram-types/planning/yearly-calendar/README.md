# Yearly calendar

A yearly calendar shows twelve months as two columns of six rows, each with a coloured month tab and a strip for that month's dates. Here every strip carries a day scale with week ticks, so dates land where they fall in the month. The example is a 2026 release train: a release every four weeks on Tuesday, the v7.0 major in September, and code freezes for New Year, a SOC 2 audit, quarter close, Black Friday and the holidays.

| Hand-drawn | Clean |
|---|---|
| ![hand-drawn](hand.jpg) | ![clean](clean.jpg) |

## Use it to explain

- Release train dates and the freeze windows a team must plan around.
- Recurring infra events across a year: certificate renewals, DR drills, cluster upgrades.
- When on-call load or compliance work clusters, so roadmaps avoid those months.
- Not for: day level detail of one month, or work with durations and dependencies; use a calendar planner or a Gantt chart.

## Anatomy

| Part | Class | Rule |
|---|---|---|
| Month tab | `d-box g0` to `g5` | same colour per row in both columns, short month name |
| Month strip | `d-box` | equal width, one row per month |
| Day scale | `d-axis` + `d-grid` ticks | days 1 to 31, ticks on days 1, 8, 15, 22, 29 |
| Release | `d-fill g4` circle | on the axis at its day, version in `d-t` above, day in `d-m` below |
| Major release | `d-fill g0` circle, larger | marks breaking or API changes |
| Freeze | `d-soft g3` | spans its days, name in `d-s` above |
| Key | `d-k` + swatches | below the grid |

## Tips

- Use one cadence and say it in the header so gaps in the pattern read as decisions.
- Keep labels above the axis and days below so they never collide.
- Clamp labels near the strip edge so they stay inside the month.

Reference: Figma template Yearly calendar

Source: [example.svg](example.svg)
