# 9 box talent matrix

A three by three grid with performance on the x axis and potential on the y axis. Each box has a name, an action and the people placed in it, and the colors run from red at bottom left to green at top right.

| Hand-drawn | Clean |
|---|---|
| ![hand-drawn](hand.jpg) | ![clean](clean.jpg) |

## Use it to explain

- Where each engineer in an org lands in a calibration, with level and area.
- What the next step is per box: staff track for stars, a launch to lead for growth, a PIP or role change for box 1.
- Where the bench strength is for critical systems (who in box 8 or 9 can own the ledger or infra).

Not for: a single person's review or a reporting tree (use `org-chart`).

## Anatomy

| Part | Class | Rule |
|---|---|---|
| Cell | `d-box g3` / `g5` / `g2` / `g1`, plus `d-fill g1 o1` overlay | color by diagonal score: red, orange, yellow, yellow-green, green |
| Box number and name | `d-k`, `d-h` | BOX 1 bottom left to BOX 9 top right |
| Action | `d-s` | one short verb phrase per box |
| Person chip | `d-tag` + `d-fillacc` dot + `d-s` | name initial, level, area |
| Axes | `d-axis` + marker, `d-s` ticks, `d-k` titles | potential up, performance right; rotated y title |

## Tips

- Use the same number scheme every cycle so people can compare boxes across halves.
- Keep at most three chips per box; move overflow into a count.
- State the performance window on the axis title.

Reference: Figma template 9 box talent matrix

Source: [example.svg](example.svg)
