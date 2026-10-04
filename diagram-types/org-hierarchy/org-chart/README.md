# Organization chart

A top-down tree of who reports to whom: one root, a row of leads joined by an elbow bus, and each lead's teams hanging off a spine below them. The example is a 64-person engineering org: the VP of Engineering, four heads (platform, product engineering, data, SRE), and the twelve teams under them, each with its headcount and the main system it runs (EKS, GitHub Actions, Stripe checkout, Kafka CDC, Snowflake, PagerDuty, Datadog).

| Hand-drawn | Clean |
|---|---|
| ![hand-drawn](hand.jpg) | ![clean](clean.jpg) |

## Use it to explain

- Which team owns which system, so a new engineer knows who to page or ask for review.
- How headcount is spread across platform, product, data and SRE before a reorg or hiring plan.
- Where on-call and incident ownership sit relative to the teams that ship the code.

Not for: a temporary project team with workstreams and milestones (use `project-org-chart`).

## Anatomy

| Part | Class | Rule |
|---|---|---|
| Root | `d-box g3` + person icon | One box at the top centre, name in `d-t`, title in `d-s` |
| Lead | `d-box g1`..`g5` | One colour per branch, same width, evenly spaced in one row |
| Headcount pill | `d-fill gN` + `d-tw` | Solid pill in the branch colour on root and leads |
| Reporting line | `d-edge` | Elbow bus from root to leads, a left spine from lead to teams, no arrowheads |
| Team | `d-box gN` + `d-logo` | Same colour as its lead, logo of the main system, role in `d-s`, headcount in a `d-tag` |

## Tips

- Keep one colour per branch so a reader can follow a lead's teams without tracing lines.
- Stack teams vertically under each lead once there are more than two; fanning them sideways runs out of width fast.
- Put the system each team owns on its card; names alone do not tell anyone where to route a question.

Reference: Figma template Organization chart

Source: [example.svg](example.svg)
