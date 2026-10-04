# SIPOC diagram

Five columns, Suppliers, Inputs, Process, Outputs and Customers, that scope a process from what feeds it to who consumes what it makes. The Process column holds five or so numbered steps in order, and lines link each supplier to its input, each input to the step that uses it, each step to the output it produces and each output to its customer. The example scopes a pull request CI pipeline: developers, GitHub, the npm registry and Vault supply a commit, a webhook event, locked dependencies and short-lived registry credentials; checkout, build, test, scan and push turn them into a check status, a JUnit report, an SBOM and a container image for branch protection, reviewers, the security team and Argo CD.

| Hand-drawn | Clean |
|---|---|
| ![hand-drawn](hand.jpg) | ![clean](clean.jpg) |

## Use it to explain

- The boundary of a CI or release pipeline before redesigning it: what comes in, what must come out.
- Which downstream teams break if a pipeline step changes (follow the lines to Customers).
- The supply chain of a build for a security review: every external supplier and the artifact it influences.

Not for: timing or waste in the flow (use `value-stream-map`) or the detailed branching inside a step (use `flowchart`).

## Anatomy

| Part | Class | Rule |
|---|---|---|
| Column header | `d-box g1`, `g5`, `g0`, `g4`, `g3` + scaled `d-h` letter + `d-t` | S I P O C in order, one colour each |
| Column body | `d-box` | Equal width and height; notes sit on a shared row grid |
| Item | `d-note` + `d-tn` + `d-s` | Name on line one, the concrete artifact on line two; `d-logo` top right for real products |
| Process step | `d-note g5` + `d-badge`/`d-bt` | Numbered top to bottom, joined by short downward `d-edge` arrows |
| Link | `d-edge` with marker | Straight line between neighbouring columns; offset endpoints so no two arrows share a head |
| Scope band | `d-band g2` + `d-k` + `d-t` | Trigger, boundary, owner and target under the table |

## Tips

- Fill P first with 4 to 7 steps, then O and C, then I and S; working outward keeps the scope honest.
- Put related items on the same row so most links are straight.
- Leave a cell empty rather than invent an item to fill it.

Reference: Figma template SIPOC

Source: [example.svg](example.svg)
