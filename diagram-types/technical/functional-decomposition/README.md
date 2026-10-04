# Functional decomposition diagram

A functional decomposition diagram breaks one capability into the functions that make it up, then breaks those into sub-functions, until each leaf is small enough to own, build and test on its own. This example decomposes a checkout service into validate cart, calculate total and take payment, and walks each branch down to real function names such as `checkStock()` and `idempotencyKey()`. Branches are colored by the team that owns them, so the tree also reads as an ownership map.

| Hand-drawn | Clean |
|---|---|
| ![hand-drawn](hand.jpg) | ![clean](clean.jpg) |

## Use it to explain

- How a service or endpoint splits into functions before writing code or tickets.
- Which team owns which branch of a feature that spans several teams.
- Where a refactor should cut a large module into smaller, testable units.

Not for: the order things happen in (use a flowchart or sequence diagram) or runtime dependencies between services (use an architecture diagram).

## Anatomy

| Part | Class | Rule |
|---|---|---|
| Root capability | `d-box g0` + `d-t`, `d-m` | One box at the top, with the endpoint or entry point |
| Function and sub-function | `d-box g2`..`g5` + `d-t`, `d-m` | Verb phrase title, real function name below; one color per branch |
| Tree connector | `d-edge` | Elbow bracket: down from parent, across, down to each child; no arrowheads |
| Stop rule | `d-note` + `d-tn` | State when a box is small enough to stop splitting |
| Branch legend | `d-fill` + `d-s` | Map each branch color to its owner |

## Tips

- Title every box with a verb phrase; nouns turn the tree into an org chart.
- Branches may stop at different depths; do not pad shallow branches with filler boxes.
- A long vertical connector that skips a row is fine and keeps deeper levels aligned.

Reference: Figma template Functional decomposition diagram

Source: [example.svg](example.svg)
