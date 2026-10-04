# Balance wheel

Six areas arranged around a hub and joined to it by spokes, each scored on the same 0 to 10 scale, so a reader sees at once which areas are healthy and which are neglected. The example scores the engineering health of a payments-api team for Q3: tests (8), docs (4), on-call (5), deploy frequency (9), security (6) and onboarding (3), each with the tool behind it and the metric that justifies the score, with the two lowest flagged as the Q4 focus.

| Hand-drawn | Clean |
|---|---|
| ![hand-drawn](hand.jpg) | ![clean](clean.jpg) |

## Use it to explain

- A team or service health check across tests, docs, on-call load, delivery speed, security and onboarding.
- Why a team is spending next quarter on docs and onboarding instead of more features.
- How two services or two quarters compare, by drawing one wheel each with the same six areas.

Not for: comparing several options on many axes at once (use `radar-chart`) or tracking one metric over time (use `bar-graph`).

## Anatomy

| Part | Class | Rule |
|---|---|---|
| Hub | `d-fillpaper` circle + `d-t`, `d-s` | The thing being assessed and its average score |
| Spoke | `d-edge` | One straight line from the hub to each area, drawn under the boxes |
| Area | `d-box g0`..`g5` | Six boxes at 60 degree steps, two top, two sides, two bottom, as in the template |
| Area header | `d-logo` + `d-t` + `d-h` | Tool logo, area name, score on the right |
| Evidence | `d-s`, `d-m` | The metric behind the score and the tool or fact that explains it |
| Score bar | `d-fill gN`, unfilled `o1` | Ten cells, filled up to the score |
| Focus flag | `d-tag acc` + `d-k` | On the lowest areas only |

## Tips

- Every score needs a metric under it, or the wheel becomes an opinion poll.
- Keep exactly the same areas from quarter to quarter so wheels can be compared.
- Flag at most two areas for focus; flagging everything means nothing is prioritised.

Reference: Figma template Balance wheel

Source: [example.svg](example.svg)
