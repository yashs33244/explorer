# Tech stack mapping

A tech stack mapping lays the stack out as layers, one per concern (compute, database, CI/CD, observability, cache, edge), and puts the tool used today next to the tool planned for each layer. This example maps a platform migration: Heroku to AWS ECS Fargate, MySQL to PostgreSQL, Jenkins to GitHub Actions, New Relic to Datadog, Redis re-hosted on ElastiCache alongside compute, and Cloudflare kept at the edge. Each arrow carries the kind of move and a status tag, so one picture shows both the target and how far along the migration is.

| Hand-drawn | Clean |
|---|---|
| ![hand-drawn](hand.jpg) | ![clean](clean.jpg) |

## Use it to explain

- Which tools a system uses for each concern, with real logos.
- A migration plan: what moves, what stays, and the status of each move.
- Why the migration order matters (for example, CI/CD first so the new deploy path exists before compute moves).

Not for: how the tools talk to each other at runtime (use a cloud or layered architecture diagram) or the dates of each step (use a gantt chart).

## Anatomy

| Part | Class | Rule |
|---|---|---|
| Column headers | `d-k` | Concern, current, move, target |
| Concern layer | `d-lane`, `d-lane alt`, `d-lanehead` | One row per concern, name and purpose in the head cell |
| Tool | `d-box` + `d-logo`, `d-t`, `d-s` | Real logo, product and version, one fact about how it is run |
| Migration arrow | `d-edge acc thick` | Verb label (`move`, `replicate`, `rewrite`) above in `d-lab` |
| Kept tool | `d-edge dash` + target box in the current color | Shows the layer was considered, not forgotten |
| Status | `d-tag`, `d-tag acc` | Short status under the arrow; `acc` marks finished moves |

## Tips

- Include layers that do not change; a missing row reads as an unconsidered concern.
- Put versions in the box (MySQL 5.7, PostgreSQL 16); version jumps are often the real risk.
- Color target boxes differently from current ones so the eye reads left to right as before and after.

Reference: Figma template Tech stack mapping

Source: [example.svg](example.svg)
