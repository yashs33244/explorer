# Online calendar planner

A month grid of seven day columns and five week rows inside a framed card, with a title bar on top and the blank days before the 1st merged into one cell that holds the legend. Each event is a short colour-coded chip inside its day, so a reader sees the rhythm of a month at a glance. The example is October 2026 for a payments-platform team: Sprint 41 and 42 planning, reviews and retros, three releases with their code freezes, weekly PagerDuty on-call handoffs, a PostgreSQL 16 upgrade window, a failover drill, a postmortem and a game day.

| Hand-drawn | Clean |
|---|---|
| ![hand-drawn](hand.jpg) | ![clean](clean.jpg) |

## Use it to explain

- How a team's sprint cadence, release trains and code freezes line up across one month.
- Which weeks carry risky infra changes (database upgrades, failover drills) and who is on call when they land.
- Where the release calendar and the on-call rotation collide, before a launch is scheduled.

Not for: hour-by-hour planning of a single day or week (use `time-blocking` or `weekly-schedule`).

## Anatomy

| Part | Class | Rule |
|---|---|---|
| Card frame | `d-band g1` | One frame around the title bar and the whole grid |
| Title bar | `d-box g1` + `d-k`, `d-h` | Team in the kicker, month and sprints in the heading |
| Source logos | `d-logo` + `d-s` | The tools the events are synced from, top right |
| Day header | `d-lanehead` + `d-t` | Mon to Sun, centred |
| Day cell | `d-box` (weekdays), `d-lane alt` (weekends) | Date number top left in `d-t`, days of the next month in `d-s` |
| Leading blank days | `d-box g0` | Merged into one cell that holds the legend |
| Event chip | `d-fill g1`..`g5` + `d-tw` | One chip per event, full cell width, at most three per day, 13 characters max |

## Tips

- Give each event kind one colour and keep it across the whole month; the legend is the key.
- Name events by their artefact (v4.12 release, INC-2231 PM), not by a generic word like "meeting".
- If a day needs more than three chips, the month is too busy for this view: split it into a weekly schedule.

Reference: Figma template Online calendar planner

Source: [example.svg](example.svg)
