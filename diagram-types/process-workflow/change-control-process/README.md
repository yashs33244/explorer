# Change control process

A strip of adjacent stage columns that a production change must pass through, from request to closure. Each column names its stage, its owner and the artifact it produces, and blue boxes show the work in that stage. Dashed loops underneath show where a change goes back: a CAB rejection returns to the RFC and an SLO breach rolls the rollout back. The example is CHG-4821, a NOT NULL column added to a large Postgres orders table.

| Hand-drawn | Clean |
|---|---|
| ![hand-drawn](hand.jpg) | ![clean](clean.jpg) |

## Use it to explain

- How a risky production database migration moves from RFC to approval, rollout and verification.
- Who owns each gate (author, DBA, CAB, on-call, SRE) and which artifact proves it passed.
- The failure paths: rejection back to the author and rollback on an SLO breach.

Not for: a fast CI/CD pipeline with no human gates; use a pipeline or flowchart.

## Anatomy

| Part | Class | Rule |
|---|---|---|
| Stage column | `d-band g0..g5` | adjacent columns, one colour each, equal width |
| Stage number and name | `d-badge` + `d-bt`, `d-h` | numbered left to right |
| Owner | `d-logo` + `d-s` | the tool of record and the role that owns the gate |
| Artifact | `d-m` | ticket, file or dashboard the stage produces |
| Work step | `d-box g4` | title plus two facts; the approve stage may hold two |
| Pre-condition | `d-note` + `d-tn` | checks that must hold before the step |
| Forward flow | `d-edge` | short solid arrows between work boxes, all at the same weight |
| Return loops | `d-edge dash` + `d-lab` | below the strip, label under the line |

## Tips

- Keep work boxes the same size in every column so the strip reads as one row.
- Step the boxes down after the decision so every arrow stays straight.
- Always draw the rollback loop; a change process without one is incomplete.

Reference: Figma template Change control process

Source: [example.svg](example.svg)
