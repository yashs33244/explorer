# Employee journey map

Phases of an employee's path laid out left to right, each with a coloured header and a body, and a row of cards above naming who guides that phase. Below sit a mood curve and one pain note per phase with its fix. The example is a new backend engineer on payments-platform going from laptop setup on day 1, through a first PR and owning a feature, to a first on-call shift in week 8.

| Hand-drawn | Clean |
|---|---|
| ![hand-drawn](hand.jpg) | ![clean](clean.jpg) |

## Use it to explain

- An engineering onboarding plan: what a new hire does each week, with which tools, and who owns that phase.
- Where onboarding loses days (access, flaky CI, missing runbooks) and the fix each team owns.
- The readiness path into an on-call rotation, from shadowing to primary.

Not for: an org's reporting lines (use an `org-chart`) or a dated project plan (use a `gantt-chart`).

## Anatomy

| Part | Class | Rule |
|---|---|---|
| Title | `d-k`, `d-h`, `d-m` | Journey kind, who and from-to, team in mono on the right |
| Guide card | `d-box` + `d-soft gN` avatar + person icon | Name in `d-t`, role in `d-s`; dashed `d-edge dash` down into the phase |
| Phase header | `d-box g1`..`g4` + `d-k`, `d-t` | Time span as kicker, phase goal as title, solid arrow to the next phase |
| Phase body | `d-box` + `d-k`, `d-s`, `d-m` | Three things done, then tool `d-logo` slots |
| Mood | `d-lane`, `d-grid`, `d-edge acc thick`, `d-fill` dots, `d-lab` | One dot per phase, label states the event behind it |
| Pain | `d-note g4` + `d-k`, `d-tn`, `d-s` | One pain per phase and the fix that addresses it |

## Tips

- Name the time span in each header ("Week 1", "Weeks 2 to 6") so the pace is visible.
- Keep to four or five phases; the template's power is the side-by-side read.
- Put commands and labels a new hire will type (`make dev`, `good-first-issue`) in mono.

Reference: Figma template Employee journey map

Source: [example.svg](example.svg)
