# Heat map

A grid of cells where two categories meet, each cell coloured by how much happens there, so clusters and gaps show up before anyone reads a number. The example shows 224 production deploys of a payments API in one quarter, by weekday and two-hour UTC slot. It shows a Tuesday to Thursday midday peak, an empty Friday afternoon behind a change freeze, and two weekend hotfixes.

| Hand-drawn | Clean |
|---|---|
| ![hand-drawn](hand.jpg) | ![clean](clean.jpg) |

## Use it to explain

- When deploys, incidents or pages happen, by day and hour.
- Error rate per service per region, to find the one hot pair.
- Test flakiness per suite per CI runner, or cache misses per endpoint per hour.

Not for: exact comparisons between a few values (use a bar chart) or a trend over time (use a line chart).

## Anatomy

| Part | Class | Rule |
|---|---|---|
| Cell | `d-fill g1`, `g2 o2`, `g2`, `g5`, `g3` | One level per bucket, cool to hot; equal size, no gaps |
| Cell value | `d-t` | Centred; leave zero cells blank so the empty areas stand out |
| Row and column labels | `d-t`, `d-s` | Rows right-aligned to the grid, columns centred over cells |
| Row total | `d-fill g0` + `d-s` | Small bar beside each row, scaled to the largest row |
| Highlight | `d-edge acc` / `d-edge dash acc` | Solid outline for a hot spot, dashed for a rule or gap |
| Legend | `d-fill` swatches + `d-s` | Name the bucket ranges, not just the colours |
| Takeaway | `d-note` + `d-tn` | One finding per note, with the number |

## Tips

- Use 4 to 6 buckets with round ranges; more levels are hard to tell apart.
- Pick bins that fit the question (two-hour slots here keep 12 columns readable at 800 wide).
- Outline the one region you want people to look at, and put the number in a note.

Reference: Figma template Heat map

Source: [example.svg](example.svg)
