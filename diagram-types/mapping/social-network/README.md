# Social network diagram

A social network diagram draws people (or services) as nodes and their relationships as edges, so clusters, hubs and bridges stand out. The example is a quarter of code review across three teams: each team clusters around its lead, a staff engineer bridges all three, node size and the number inside show PRs reviewed, and dashed edges are cross-team reviews.

| Hand-drawn | Clean |
|---|---|
| ![hand-drawn](hand.jpg) | ![clean](clean.jpg) |

## Use it to explain

- Who reviews whose code, and where review load or knowledge is concentrated on one person (bus factor).
- Which engineers bridge teams on shared code such as an SDK or an API contract.
- Ownership and communication paths before a reorg or a service split.

Not for: call graphs or data flow between services where direction and order matter; use a dependency graph or sequence diagram.

## Anatomy

| Part | Class | Rule |
|---|---|---|
| Team cluster | `d-blob` ellipse + `d-k` | one dashed group per team, label outside the blob |
| Person | `d-fill g1`..`g5` circle | colour by team; radius grows with the square root of the metric |
| Bridge person | `d-fillpaper` circle | the neutral node that connects clusters |
| Metric | `d-tw` (or `d-t` on paper) | the number that sets the node size, inside the circle |
| Name | `d-lab` | beside the node, halo keeps edges from striking through |
| Relationship | `d-edge`, `d-edge thick` | thick for the heaviest pairs; undirected, so no arrowheads |
| Cross-team link | `d-edge dash` + `d-lab` | dashed, labelled with why the teams meet |

## Tips

- Scale radius by the square root of the metric so area, not diameter, tracks the number.
- Keep the hub of each cluster in the middle and leaves fanned out so edges do not cross.
- Label only the edges that carry a story (heaviest pairs, cross-team links).

Reference: Figma template Social network diagram

Source: [example.svg](example.svg)
