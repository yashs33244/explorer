# Sequence diagram

Participants across the top, time running down, and one horizontal arrow per message between their dashed lifelines. Activation bars show when a participant is busy handling a call. The example is an OAuth 2.0 authorization code login with PKCE: the browser, a Next.js backend-for-frontend, Auth0, a profile API and Postgres, in 13 numbered messages.

| Hand-drawn | Clean |
|---|---|
| ![hand-drawn](hand.jpg) | ![clean](clean.jpg) |

## Use it to explain

- An auth or payment handshake where order and redirects matter.
- One API request fanning out to services, caches and databases.
- Retries, timeouts or callbacks between a client, a queue and a worker.

Not for: static structure (use a component or C4 diagram) or long processes with many branches (use a flowchart).

## Anatomy

| Part | Class | Rule |
|---|---|---|
| Participant | `d-box g<n>` + `d-logo` | One per column, evenly spaced; name in `d-t`, role in `d-s` |
| Lifeline | `d-edge dash` | Vertical, from the header to below the last message |
| Activation | `d-fillpaper` | 12 wide, centred on the lifeline, spans the work |
| Request | `d-edge` + marker | Solid, label above in `d-lab` with the real verb and path |
| Response | `d-edge dash` + marker | Dashed, pointing back to the caller |
| Key call | `d-edge acc` | Highlights the security-critical steps |
| Self call | `d-edge` loop | Short bracket out and back to the same bar |
| Step number | `d-badge` + `d-bt` | Left margin, one per message row |

## Tips

- Use a fixed row pitch (36 here) so the eye reads time as distance.
- End arrows at the edge of the activation bar, not at the lifeline.
- Write labels as the real call (`POST /token`), not prose.
- Five or six participants is the limit at 800 wide; split the scenario beyond that.

Reference: Figma template Sequence diagram

Source: [example.svg](example.svg)
