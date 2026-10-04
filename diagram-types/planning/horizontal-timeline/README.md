# Timeline (horizontal)

A thick arrow running left to right as the spine, with events hung off it on stems that alternate above and below so the cards never collide. Era labels sit inside the arrow and the card colour groups events into the same eras. The example is Kubernetes major releases from v1.0 in 2015 to v1.33 in 2025: core APIs (Deployments, RBAC), extensibility (CRDs), the runtime cleanup (dockershim deprecated then removed, PodSecurityPolicy removed) and maturity, with sidecar containers going GA.

| Hand-drawn | Clean |
|---|---|
| ![hand-drawn](hand.jpg) | ![clean](clean.jpg) |

## Use it to explain

- The release history of a framework or platform a codebase depends on, and why an upgrade is hard.
- A service's own history: launch, rewrites, migrations, major incidents.
- Deprecation windows: when an API was marked deprecated and when it was actually removed.

Not for: overlapping work with durations and owners (use `gantt-chart`) or more than about ten events (use `vertical-timeline`).

## Anatomy

| Part | Class | Rule |
|---|---|---|
| Spine | path `d-box g0` | Arrow from left edge to a head on the right; time flows with it |
| Era label | `d-t` on the spine | Between dots, never on top of one |
| Event dot | `d-fill g0` | On the spine edge where the stem lands |
| Stem | `d-edge` | Straight vertical, alternating up and down |
| Event card | `d-box g1`..`g5` | Version and date in `d-m` (not `d-k`, which uppercases `v1.0`), change in `d-t`, impact in `d-s` |
| Header | `d-logo` + `d-k`, `d-h` | Product logo and repo name, title, scale note on the right |

## Tips

- Say whether spacing is to scale; release-spaced timelines are easier to read but hide long gaps.
- Colour cards by era, not by importance, so the eras read as runs of one colour.
- Keep each card to three short lines; put detail in the caption.

Reference: Figma template Timeline (horizontal)

Source: [example.svg](example.svg)
