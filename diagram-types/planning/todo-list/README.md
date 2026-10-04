# To do list

A clipboard checklist: a titled list of tasks, each with a checkbox, an owner and a due day, grouped under priority headers, with a progress bar and a done mark at the foot. The example is the release checklist for `payments-api v4.2.0`: P0 blockers (branch cut, migration dry-run, contract tests, webhook secret rotation), P1 should-ship work (SDK regeneration, canary, latency alert, rollback runbook) and P2 nice-to-haves, with 6 of 11 done and one open P0 holding the tag.

| Hand-drawn | Clean |
|---|---|
| ![hand-drawn](hand.jpg) | ![clean](clean.jpg) |

## Use it to explain

- What has to be true before a release is tagged, and which open item is blocking it.
- A launch, migration or incident follow-up list where every task needs an owner and a date.
- How work is triaged into must, should and could for one sprint or cutover.

Not for: tasks that depend on each other or run over weeks (use a `gantt-chart` or `project-plan`).

## Anatomy

| Part | Class | Rule |
|---|---|---|
| Board and clip | `d-box g2`, `d-box g4` | One clipboard frame, clip centred on the top edge |
| Paper | `d-fillpaper` | Holds everything else, 24px inside the board |
| Title | `d-k`, `d-h`, `d-m` | Kicker for the list kind, heading for the thing shipped, deadline right-aligned in mono |
| Priority header | `d-tag` / `d-tag acc` + `d-t`, `d-s` | Pill with P0, P1, P2 and a one-line meaning; the highest priority gets `acc` |
| Priority stripe | `d-fill g3`, `g5`, `g4` | Thin bar beside each group's rows |
| Task row | `d-fill g1` + `d-line` check, or `d-fillpaper` box | Done tasks muted in `d-s`, open tasks bold in `d-tn` |
| Owner, due | `d-m`, `d-s` | Fixed columns, due right-aligned |
| Progress | `d-fillpaper` track + `d-fill g1` bar, big `d-fill g1` check | Bar width is done over total |

## Tips

- Keep each task under six words; the detail lives in the ticket.
- Open tasks in bold, done tasks muted, so the eye lands on what is left.
- Say in the footer line what the remaining items block, not just the count.

Reference: Figma template To-do list

Source: [example.svg](example.svg)
