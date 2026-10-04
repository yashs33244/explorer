# Project plan

A project plan is a table: a header row naming the project and its target, column headers, and one row per phase with its deliverable, owner, due date and status. The status column is colour coded so risk stands out at a glance. The example plans the split of a Rails monolith into services with the strangler fig pattern: domain mapping, an EKS and Istio platform, extracting orders behind Kong, splitting the database with Debezium CDC, extracting payments and retiring the monolith routes.

| Hand-drawn | Clean |
|---|---|
| ![hand-drawn](hand.jpg) | ![clean](clean.jpg) |

## Use it to explain

- A migration broken into phases, with an owner and a date for each deliverable.
- Where a multi-team platform project stands this week, and which phase is at risk.
- What a rewrite depends on, by showing blocked phases next to the ones they wait on.
- Not for: overlapping durations or dependencies over time; use a Gantt chart or a roadmap.

## Anatomy

| Part | Class | Rule |
|---|---|---|
| Header label | `d-fill g0` + `d-tw` | PROJECT and TARGET, paired with a white value cell |
| Column header | `d-fill g0` + `d-tw` | caps, one word: PHASE, DELIVERABLE, OWNER, DUE, STATUS |
| Cell | `d-box` | same height per row, 6 unit gaps between cells |
| Phase | `d-badge` + `d-t` | numbered in execution order |
| Deliverable | `d-t` + `d-s` + `d-logo` | the artifact, a detail line and the main tool |
| Due date | `d-m` | day and month only |
| Status | `d-box g1` / `g2` / `g3` / plain | done, in progress, at risk, not started, with a reason in `d-s` |
| Key | `d-k` + swatches | below the table, same order as the colours |

## Tips

- Give every row one named owner; a team name alone hides who to ask.
- Always add a reason under At risk and Not started.
- Keep deliverables concrete (a service, a cluster, a deleted route), not activities.

Reference: Figma template Project plan

Source: [example.svg](example.svg)
