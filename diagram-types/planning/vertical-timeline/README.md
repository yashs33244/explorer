# Vertical timeline

A vertical timeline runs time down a single spine, split into coloured phase segments, with event cards branching off to the left and right. Alternating sides lets each card carry a timestamp, a title and a detail line without crowding. The example is the timeline of incident INC-2291: a 5xx rate alert on checkout-api at 14:02 UTC, the incident channel, the suspect deploy, the Argo CD rollback, recovery, resolution and the postmortem two days later, with its action items on a sticky note.

| Hand-drawn | Clean |
|---|---|
| ![hand-drawn](hand.jpg) | ![clean](clean.jpg) |

## Use it to explain

- An incident from first alert to postmortem, with UTC timestamps and who acted at each step.
- The history of a service or repo: launch, rewrites, migrations, deprecations.
- A deploy or release that went through several gated stages over hours or days.
- Not for: parallel work streams or overlapping durations; use a Gantt chart or a swimlane diagram.

## Anatomy

| Part | Class | Rule |
|---|---|---|
| Phase segment | `d-box g3` / `g5` / `g2` / `g1` | stacked on one spine, height covers the events in that phase |
| Spine end | `d-box g4` path | the last phase ends in an arrowhead pointing forward in time |
| Event card | `d-box` | alternate left and right, same width, never overlapping on one side |
| Timestamp | `d-tag acc` + `d-m` | top left of the card, one time zone stated in the header |
| Event title / detail | `d-t` / `d-s` | title says what happened, detail says the evidence |
| Tool | `d-logo` | top right of the card, the system where the event happened |
| Connector | `d-edge` + `d-fillink` dot | horizontal, dot on the spine marks the exact moment |
| Follow-ups | `d-note g2` + `d-tn` | beside the last phase, joined by a dashed `d-edge` |

## Tips

- Put each event inside the phase it belongs to; a card next to the wrong colour reads as a mistake.
- Keep spacing even rather than proportional to time unless the gaps are the point.
- State the time zone once in the header and use 24 hour times in every tag.

Reference: Figma template Vertical timeline

Source: [example.svg](example.svg)
