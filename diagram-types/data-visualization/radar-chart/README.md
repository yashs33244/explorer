# Radar chart

Several axes radiate from one centre, each scored on the same scale, and every option becomes a polygon, so its strengths and weaknesses show as a shape. The example compares PostgreSQL and Cassandra as the event store for a service on six axes: read latency, write scale, cost at 10 TB, ops simplicity, consistency and ecosystem. It also has a score table and the decision.

| Hand-drawn | Clean |
|---|---|
| ![hand-drawn](hand.jpg) | ![clean](clean.jpg) |

## Use it to explain

- Two or three databases, queues or frameworks on a shortlist.
- A service's maturity scores (tests, observability, docs, on-call) against a target.
- A team's skills coverage before and after a hire.

Not for: more than three options (the shapes overlap) or values with different units (normalise to one scale first).

## Anatomy

| Part | Class | Rule |
|---|---|---|
| Rings | `d-band g0`, `d-fillpaper`, `d-grid` | One ring per score step; outer disc tinted like the template |
| Spoke | `d-edge dash` | One per axis, evenly spaced, starting at the top |
| Scale ticks | `d-lab` | Along the top spoke only, drawn after the shapes so the halo keeps them readable |
| Option shape | `d-soft g4` / `d-soft g3` | Translucent polygon so both stay visible |
| Vertex | `d-fill g<n>` r 5 | Marks the exact score on each axis |
| Axis label | `d-t` | Outside the outer ring; anchor away from the centre |
| Legend | `d-box g<n>` + `d-logo` | Product name, version and total |
| Score table and decision | `d-s`, `d-t`, `d-note` | The exact numbers and the call |

## Tips

- Make "higher is better" true on every axis (ops simplicity, not ops effort).
- Draw the weaker option first so the stronger one is not hidden.
- Put the deciding constraint in a note; the shape alone does not make the call.

Reference: Figma template Radar chart

Source: [example.svg](example.svg)
