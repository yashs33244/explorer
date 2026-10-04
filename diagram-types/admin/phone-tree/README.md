# Phone tree

A tree of person cards where each person calls the people directly below them, so news fans out without one person making every call. Badges set the call order, time tags show when each level should be reached, and a dashed link shows the fallback when someone does not answer. The example is a SEV1 escalation for a checkout outage: PagerDuty pages the incident commander, who calls the payments eng lead, comms lead and VP Engineering, who each call their own people.

| Hand-drawn | Clean |
|---|---|
| ![hand-drawn](hand.jpg) | ![clean](clean.jpg) |

## Use it to explain

- A SEV1 or security incident escalation path, with who calls whom and by when.
- Release-day or freeze notifications that must reach every service owner.
- A disaster recovery runbook's contact chain when Slack itself is down.

Not for: reporting lines or ownership (use `org-chart`).

## Anatomy

| Part | Class | Rule |
|---|---|---|
| Trigger | `d-tag acc` + `d-logo` | The alert that starts the tree, above the root |
| Person card | `d-box g1`..`g4` + avatar icon | Name `d-t`, role `d-s`, first action `d-m`, tool logo bottom left |
| Branch colour | `g` per subtree | A level-2 caller and the people they call share a colour |
| Call order | `d-badge` | On the card corner, restarts at 1 under each caller |
| Deadline | `d-tag` | T+0, T+5m, T+10m, the same for the whole level |
| Call | `d-edge` with marker | Orthogonal bus from parent bottom to child top |
| Fallback | `d-edge dash` + `d-lab` | Between siblings: no answer, call the next |

## Tips

- Keep each caller to three calls or fewer; a wide level means the tree needs another layer.
- Put the first action on every card, so the call itself carries the instruction.
- State the no-answer rule under the drawing; the dashed link only shows one example.

Reference: Figma template Phone tree

Source: [example.svg](example.svg)
