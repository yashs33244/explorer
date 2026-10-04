# Gantt chart

Tasks as rows, time as columns, and one bar per task spanning its planned dates, coloured by status. A legend explains the colours, arrows show finish-to-start dependencies, a red line marks today and a diamond marks the launch milestone. The example is the payments v2 API release over eight weeks: the spec and OAuth scopes are done, pagination has slipped past today, gateway rate limits are in progress, and SDK codegen, a critical load test, v1 deprecation headers and docs lead to GA on Fri Oct 24.

| Hand-drawn | Clean |
|---|---|
| ![hand-drawn](hand.jpg) | ![clean](clean.jpg) |

## Use it to explain

- A release plan: which workstreams run in parallel and what has to finish before launch.
- Where a slip lands: which bars sit to the left of the today line but are not done.
- The critical path through a migration or a platform upgrade, and who owns each step.

Not for: work with no dates or a continuous kanban flow (use a board), or a long-range roadmap of themes (use a timeline).

## Anatomy

| Part | Class | Rule |
|---|---|---|
| Legend | `d-box g1`/`g4`/`g3`/`g0`, `d-blob`, diamond `d-box g2` | Top right; one swatch per status, same order as the colours in use |
| Time column header | `d-box g2` + `d-k`, `d-s` | Week number and start date, equal widths |
| Week gridline | `d-grid` | One per column boundary, behind the bars |
| Task label | `d-box g2` + `d-t` | Numbered, left column, one row each |
| Task bar | `d-box g1` done, `g4` in progress, `g3` delayed, `g0` pending | Owner in `d-m` inside the bar start |
| Critical task | `d-blob` | Dashed bar for the task with no slack |
| Dependency | `d-edge acc` + marker | Finish to start: out of the bar end, into the next bar start |
| Today | `d-fill g3` line + `d-fill g3` label with `d-tw` | Full height, label under the chart |
| Milestone | diamond `d-box g2` + `d-t` | Zero length; name and date beside it |

## Tips

- Leave at least a quarter column between dependent bars so the arrowhead has room.
- Keep owner text short enough to fit inside the narrowest bar; a mono `@team` handle works.
- Order rows so a dependency arrow never has to cross another task's bar; put a long parallel task below the chain it runs beside.
- Say the dependency type once in a footnote rather than labelling every arrow.

Reference: Figma template Gantt chart (structure from the Excalidraw Gantt chart example: legend, column headers, labelled rows, today line)

Source: [example.svg](example.svg)
