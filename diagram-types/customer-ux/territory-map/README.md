# Territory map

Abstract regions on a canvas, each one territory owned by a team, with pins for the assets inside it and dashed boundaries for the dividing rule. Here the rule is timezone: four SRE teams (Seattle, Dublin, Bengaluru, Tokyo) each own the cloud regions in their band, hand the pager west every six hours (Seattle hands back to Tokyo at 00:00 UTC), and a 24 hour strip below shows the follow-the-sun PagerDuty schedule with no gaps.

| Hand-drawn | Clean |
|---|---|
| ![hand-drawn](hand.jpg) | ![clean](clean.jpg) |

## Use it to explain

- Which team owns which cloud regions, so an incident in ap-south-1 escalates to Core SRE whoever holds the pager.
- How a follow-the-sun rotation hands off and proves 24 hour coverage.
- Ownership boundaries for regional infrastructure, data residency zones or shard ranges.

Not for: network paths between regions (use `network-diagram` or `cloud-architecture`).

## Anatomy

| Part | Class | Rule |
|---|---|---|
| Canvas | `d-band g0` | One frame holding all territories |
| Boundary | `d-edge dash` + `d-k` | Vertical divider per timezone band, labelled at the top, stopping above the handoff arrows |
| Territory | `d-soft g1`..`g4` + `d-t`, `d-s` | Abstract blob, owning team and its home city |
| Asset pin | `d-fill` + `d-fillpaper` + `d-m` | Teardrop in the territory colour, region code beside it |
| Handoff | `d-edge acc` + `d-lab` | Arrow from one territory to the next with the UTC time |
| Coverage strip | `d-fill gN o1`, `d-fill gN`, `d-axis` | Faded full day, solid primary window, hour ticks |

## Tips

- Keep shapes abstract; real borders invite arguments about geography instead of ownership.
- Use the same colour for a team's territory, pins and coverage bar so the eye links them.
- Add the coverage strip whenever territories rotate, so gaps and overlaps are visible.

Reference: Figma template Territory map

Source: [example.svg](example.svg)
