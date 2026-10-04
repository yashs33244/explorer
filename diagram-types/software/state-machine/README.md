# State machine

Rounded boxes for the states an object can be in, arrows for the events that move it between them, a filled dot for the start and a double border for terminal states. The example is the Payment.status column in a checkout service, moved by our own API calls, Stripe webhooks and a timer: created, requires_action, processing, succeeded, failed and canceled, with a note on the event every transition emits.

| Hand-drawn | Clean |
|---|---|
| ![hand-drawn](hand.jpg) | ![clean](clean.jpg) |

## Use it to explain

- The status column of an entity (orders, payments, deployments, jobs) and which transitions are legal.
- Which transitions our code triggers and which come from outside (webhooks, timers, users).
- Retry and cancel paths, and which states are final, before writing the enum and guards.

Not for: a process with many decisions and no persistent status (use `flowchart`).

## Anatomy

| Part | Class | Rule |
|---|---|---|
| Start | `d-fillink` circle | One filled dot with an arrow into the first state |
| State | `d-box g0`..`g5` | Status name in `d-t`, meaning in `d-s`, centred; colour by outcome |
| Terminal state | two nested `d-box` | Double border, no outgoing arrows |
| Transition | `d-edge` (+ `acc`, `dash`) + `d-lab` | Labelled with the event or call; `acc` for our API calls, `dash` for timers |
| Side effect note | `d-note` + `d-tn`, `d-m` | Behaviour shared by every transition, such as an emitted event |
| Legend | `d-edge` samples + `d-s` | Explains each edge style and the terminal border |

## Tips

- Name states exactly as the code or API spells them, so the diagram doubles as documentation.
- Route loops (retry) with right angles away from the main path so they do not cross other arrows.
- Lay out the happy path on one row left to right, and put error and cancel states below it.

Reference: Figma template State machine

Source: [example.svg](example.svg)
