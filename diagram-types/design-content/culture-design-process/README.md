# Culture design process

A culture canvas: a shared purpose in a circle at the centre, surrounded by blocks for values, priorities, behaviours, rituals, feedback, decision making and norms, with a four-phase strip on top (discover, define, design, embed) and a badge in each block naming the phase that fills it. The example is an engineering org setting up blameless postmortems and code review norms: values like "blameless by default", a weekly incident review, RFCs that end in ADRs, and rules enforced in CI with CODEOWNERS.

| Hand-drawn | Clean |
|---|---|
| ![hand-drawn](hand.jpg) | ![clean](clean.jpg) |

## Use it to explain

- How a blameless postmortem practice turns into concrete rituals, tracked actions and CI checks.
- The code review norms a team agrees on, and which of them are enforced by tooling.
- Where a new engineering habit is in its rollout, from discovery to embedded in onboarding.

Not for: the steps of one incident response (use `flowchart` or `sequence-diagram`).

## Anatomy

| Part | Class | Rule |
|---|---|---|
| Phase strip | `d-box` + `d-badge` + `d-edge acc` | Four boxes left to right, numbered, joined by short arrows |
| Block | `d-box g0`..`g5` | Seven blocks in a 3, 2, 2 grid; six colours, so only two blocks that never touch share one |
| Block text | `d-k`, `d-t`, `d-s`, `d-m` | Badge and kicker, one-line commitment, two concrete lines |
| Purpose | `circle.d-box` | Centre circle overlapping the middle row, text kept clear of the blocks |
| Tool | `d-logo` | Top right of a block when a product enforces it, kept clear of the circle |

## Tips

- Write each block as a commitment ("review within 1 day"), not a topic ("code review").
- Keep block text on the outer side so the circle never covers it.
- Name the tool or file that makes a norm real; a norm with no enforcement point drifts.

Reference: Figma template Culture design process

Source: [example.svg](example.svg)
