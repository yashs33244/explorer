# Weekly schedule planning

Five folder cards stacked with an offset, one per weekday, each with a tab naming the day and a strip of time-stamped pills for that day's commitments. The front card is the last day and has room for the highlights and the week's totals. The example is Sprint 41, week 2, for a payments-platform team: standups, grooming, a design review and the RC cut as meeting pills, protected focus blocks as filled pills, and a Friday ship day with the sprint review, retro, the v4.12.0 release and the PagerDuty on-call handoff.

| Hand-drawn | Clean |
|---|---|
| ![hand-drawn](hand.jpg) | ![clean](clean.jpg) |

## Use it to explain

- The ceremony rhythm of a sprint week and where focus time survives between them.
- What happens on ship day: review, retro, release and on-call handoff in order.
- How much of a week goes to meetings versus focus, as a quick total for a retro.

Not for: exact durations or overlaps across days (use `time-blocking`).

## Anatomy

| Part | Class | Rule |
|---|---|---|
| Day folder | `d-box g1`..`g4`, plain `d-box` for the front card | Stepped path: tab then body; each card offset 30 right and 90 down |
| Tab | `d-h` + `d-s` | Day name on the left, date right aligned |
| Meeting pill | `d-tag` + `d-m` + `d-s` | Start time in mono, then the meeting |
| Focus pill | `d-fill g0` + `d-tw` | Filled, so focus reads differently from meetings |
| Highlight | `d-tag acc` + `d-logo` + `d-t` | Release and handoff on the front card, with the tool's logo |
| Totals | `d-k` + pills | Under a `d-grid` rule on the front card |

## Tips

- Only the strip under each tab is visible, so keep a day to four pills.
- Put the busiest or most important day on the front card.
- Reuse the same pill style across days so meetings and focus compare at a glance.

Reference: Figma template Weekly schedule planning

Source: [example.svg](example.svg)
