# Geographic organization structure

An org chart split by location: one leader at the top, a card per regional hub (city, time zone, site lead, headcount) and the teams based in each hub underneath. Because every hub sits in a different time zone, the example adds the follow-the-sun on-call rota that hands the pager from one hub to the next.

| Hand-drawn | Clean |
|---|---|
| ![hand-drawn](hand.jpg) | ![clean](clean.jpg) |

## Use it to explain

- Which engineering hub owns which service, so an incident in a region pages the right team.
- How on-call follows the sun across Bangalore, Berlin, Toronto and San Francisco, and where the handoffs fall in UTC.
- Where to open a new team when a time zone has no coverage or a hub is over capacity.

Not for: reporting lines inside one office (use `org-chart`) or how a request moves between services.

## Anatomy

| Part | Class | Rule |
|---|---|---|
| Global lead card | `d-box` body + `d-box g4` header path | one card on top, person avatar in the colored header, totals in the white body |
| Hub card | `d-box` + `d-box g1`..`g5` header | city and time zone in the header, site lead and headcount below; one color per hub |
| Reporting lines | `d-edge` | elbow bus from the lead to every hub, no arrowheads |
| Hub teams | `d-blob2` + `d-box gN` + `d-logo` | dashed group per hub, team boxes in the hub color with the main product logo |
| On-call band | `d-band`, `d-tag`, `d-edge` + marker, `d-lab` | UTC shift pills in hub order, handoff arrows, dashed return arrow closes the loop |

## Tips

- Order the hub columns by time zone so the handoff arrows read left to right.
- Keep one color per hub and reuse it on its teams, so location reads at a glance.
- Put headcount on the site lead line; it is the number people ask for first.

Reference: Figma template Geographic organization structure

Source: [example.svg](example.svg)
