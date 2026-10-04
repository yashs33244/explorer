# Clock / time zone

A 24-hour dial cut into wedges, one per hour, coloured by who owns that hour, with an inner ring that names each owner and their local hours. It turns "what time is it for them" into a shape you can read at a glance. The example is a follow-the-sun PagerDuty rotation for payments-api: Bangalore, London, San Francisco and Sydney each hold a 7 hour shift, the four 1 hour overlaps are the handoffs, and an accent hand marks now (14:40 UTC).

| Hand-drawn | Clean |
|---|---|
| ![hand-drawn](hand.jpg) | ![clean](clean.jpg) |

## Use it to explain

- A follow-the-sun on-call rotation and where the handoff overlaps sit.
- Batch job, backup and deploy windows across regions, and which ones collide with peak traffic.
- Which teams share working hours for a cross-region incident or release call.

Not for: a sequence of dated milestones (use `gantt-chart` or `horizontal-timeline`).

## Anatomy

| Part | Class | Rule |
|---|---|---|
| Hour wedge | `d-fill g1`..`g4` | 24 wedges of 15 degrees, 00 at the top, clockwise, coloured by owner |
| Overlap wedge | `d-fill g5` + `d-badge` | One per handoff, numbered to match the handoff list |
| Owner sector | `d-box g1`..`g4`, `d-t`, `d-s` | Inner ring, city code and local hours at the sector middle |
| Hour labels | `d-s` | Two digits just outside the ring |
| Now hand | `d-edge acc thick` | From the centre to the ring, explained in a one-line legend |
| Shift cards | `d-box g0` + `d-fill` swatch, `d-m` | Name, UTC range in mono, time zone and local hours |
| Handoff list | `d-badge`, `d-m`, `d-t` | Time and "from to", plus a sticky with what a handoff covers |

## Tips

- Always draw the dial in UTC and put local times in labels; a dial in one city's time misleads the other three.
- Keep the hand away from sector labels; check where it crosses before choosing the time.
- Name the overlap explicitly; a rotation with no overlap wedges is a rotation with no handoff.

Reference: Figma template Clock / time zone

Source: [example.svg](example.svg)
