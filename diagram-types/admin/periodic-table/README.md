# Periodic table (of things)

A grid shaped like the periodic table: tall edge columns, a low middle block and a detached strip below, where each cell holds a number, a two-letter symbol, a logo and a name, and colour marks the family. The shape makes a large catalogue scannable and invites "which element are we missing". The example is a platform team's DevOps tool table: source control and CI on the left, build, delivery and IaC in the middle block, observability (Prometheus, Grafana, Thanos, OTel) and security on the right, cloud and collaboration in the strip.

| Hand-drawn | Clean |
|---|---|
| ![hand-drawn](hand.jpg) | ![clean](clean.jpg) |

## Use it to explain

- The tools a platform or SRE team runs, grouped by job, with a logo per product.
- An internal service catalogue, where each element is a service and the family is its domain.
- A tooling radar review: which cells are adopted, trialled or retired this year.

Not for: how the tools connect at runtime (use `tech-stack-mapping` or `layered-architecture`).

## Anatomy

| Part | Class | Rule |
|---|---|---|
| Element cell | `d-box g0`..`g5` | Same size everywhere, small gap, number top left |
| Logo | `d-logo` | Top right of the cell, the product's real domain |
| Symbol | `d-h` | Two letters, first capital |
| Name | `d-s` | Ten characters or fewer so it fits the cell |
| Family | `g` colour | One colour per column group, matching the key |
| Key | `d-blob2`, sample cell, swatches | In the empty space between the tall columns, like a real table |
| Strip | `d-box g0`, `d-k` row labels | Detached rows below for the families that do not fit the main shape |

## Tips

- Number cells in reading order, row by row, as a real table does.
- Keep the iconic shape (tall edges, low middle); a plain grid loses the reason to use this type.
- Pick short names ("OTel", "JFrog") rather than shrinking the font.

Reference: Figma template Periodic table (of things)

Source: [example.svg](example.svg)
