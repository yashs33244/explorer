# Hiring process flowchart

A stage board for an engineering hiring loop: one coloured column per interview stage, a card per candidate with a pass or reject mark, and a sticky note holding the bar for that stage. Reading left to right shows where candidates drop out and how long the loop takes. The example tracks a backend engineer req for a payments platform team through recruiter screen, coding round, system design, then team match and offer.

| Hand-drawn | Clean |
|---|---|
| ![hand-drawn](hand.jpg) | ![clean](clean.jpg) |

## Use it to explain

- How an engineering interview loop is staged and which tool runs each round (ATS, live coding pad, whiteboard, e-sign).
- Where a req loses candidates, for example a system design round that rejects for missing sharding.
- The pass bar or rubric each interviewer panel applies, so new interviewers calibrate.

Not for: org charts, team topology or on-call rotations; use an org chart or swimlane instead.

## Anatomy

| Part | Class | Rule |
|---|---|---|
| Stage header | `d-box g0..g5` + `d-logo` | one colour per stage, tool logo left, title and length below |
| Stage column | `d-band g0..g5` | same colour as its header, holds the cards |
| Candidate card | `d-fillpaper` + `d-box gN` avatar | anonymised id and one-line evidence, never a real name |
| Pass / reject mark | `d-fill g1` / `d-fill g3` + `d-line` | top right of the card, check or cross |
| Stage bar | `d-note` + `d-tn` | two short lines: the bar, rubric or prompt |
| Flow rule | `d-edge` + `d-lab` | one arrow under the board stating how candidates advance |

## Tips

- Use candidate ids, not names; the diagram is about the process.
- Fewer cards per column as you move right makes the funnel visible without a chart.
- Put the final funnel numbers (screened, hired, days) on the last sticky.

Reference: Figma template Hiring process flowchart

Source: [example.svg](example.svg)
