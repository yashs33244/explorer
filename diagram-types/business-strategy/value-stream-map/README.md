# Value stream mapping

Numbered columns, one per stage of the flow, each showing the queue in front of the stage (an inventory triangle with its wait time), the process box with cycle time, percent complete and accurate, and who does the work, plus a kaizen note with the planned fix. A timeline ladder underneath puts wait above the line and work below it, and a summary band gives lead time, work time and flow efficiency. The example maps payments-svc from commit to production: code review in GitHub, CI on GitHub Actions, staging through Argo CD and release behind LaunchDarkly flags, where 33.5 hours of lead time hold only 2 hours of work.

| Hand-drawn | Clean |
|---|---|
| ![hand-drawn](hand.jpg) | ![clean](clean.jpg) |

## Use it to explain

- Where a change spends its time between merge and production, and that most of it is waiting, not working.
- Which delivery bottleneck to attack first (an 18 hour review queue beats a 22 minute build).
- The before state for a DORA lead-time improvement, with each stage's fix pinned to it.

Not for: the branching logic of a pipeline (use `flowchart`) or which services the pipeline touches (use `data-pipeline`).

## Anatomy

| Part | Class | Rule |
|---|---|---|
| Stage column | `d-band g2`, `g5`, `g3`, `g0` | One per stage, left to right, equal width, numbered with a scaled `d-h` |
| Queue | `d-fill g2` triangle + `d-tw` "I" + `d-t`/`d-s` | Wait time and the reason it waits, above the process box |
| Process box | `d-box` + `d-logo` + `d-m`/`d-s` rows | Tool name, then C/T, %C&A and who, separated by a `d-grid` rule |
| Push arrow | `d-edge thick` | Between process boxes, drawn after all columns so no band covers it |
| Kaizen | `d-k` + `d-note g4` | One planned fix per stage |
| Timeline ladder | `d-edge thick` step path + `d-lab` | Wait on the high step, work on the low step, aligned to each column |
| Summary | `d-box g1` + `d-k` + `d-h` | Lead time, work time, flow efficiency, biggest wait |

## Tips

- Use medians from real data (deploy logs, PR timestamps) and say the window in the header.
- Flow efficiency is work time over lead time; under 10% is normal and is the point of the map.
- Keep each kaizen note to one change you could ship in a sprint.

Reference: Figma template Value stream map

Source: [example.svg](example.svg)
