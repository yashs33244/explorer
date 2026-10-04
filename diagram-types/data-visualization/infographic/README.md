# Infographic

A single card made of several small charts, each answering one question with one number, so a reader gets the whole story at a glance. The example is one year of an open source repo. It has issue and PR outcomes by type, contributors by region, headline counts, weekly npm downloads, lines by language and hours to first review, with one takeaway at the bottom.

| Hand-drawn | Clean |
|---|---|
| ![hand-drawn](hand.jpg) | ![clean](clean.jpg) |

## Use it to explain

- A project's or platform team's year in review.
- A quarterly reliability report: uptime, incidents, MTTR, top causes.
- A migration's results: services moved, cost saved, latency before and after.

Not for: one detailed analysis (use the single chart that fits) or anything readers must compare across panels exactly.

## Anatomy

| Part | Class | Rule |
|---|---|---|
| Card | `d-fillpaper` | One rounded card holding a 3 by 2 grid of panels |
| Panel heading | `d-k` + `d-t` | Kicker names the topic, title states the finding |
| Segmented bars | `d-fill g<n>` | Parts of 100%, label segments of 20% or more |
| Hub and spoke | `d-box g<n>` circles + `d-edge` | Total in the hub, one spoke per group |
| Big numbers | `d-box g<n>` circles + `d-h` | Four headline counts with units |
| Area chart | `d-band g4` + `d-fill g1` + `d-axis` | One series, a labelled event dot (`d-badge`) |
| Donut | `d-fill g<n>` arc paths | Total in the middle, legend below |
| Bars | `d-fill g<n>` + `d-axis` | Value above each bar, period below |
| Takeaway | `d-note` + `d-tn` | One sentence across the bottom |

## Tips

- Keep each panel to one question; six panels is the limit at 800 wide.
- Give every panel a title that states the result ("120k to 410k"), not just the metric name.
- Reuse one colour per meaning across panels (green is good here).

Reference: Figma template Infographic

Source: [example.svg](example.svg)
