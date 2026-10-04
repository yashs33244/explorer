# UML diagram (use case)

A UML use case diagram: stick-figure actors outside a dashed system boundary, the goals they reach as ellipses inside it, solid association lines, and dashed `«include»` and `«extend»` arrows between use cases. The example models a CI/CD platform used by a developer, a reviewer and an Argo CD release bot, from pushing a branch to promoting and rolling back a release.

| Hand-drawn | Clean |
|---|---|
| ![hand-drawn](hand.jpg) | ![clean](clean.jpg) |

## Use it to explain

- Who uses an internal platform (CI/CD, a deploy tool, an admin API) and what each actor may trigger
- Which steps always run as part of another (`«include»`, such as unit tests inside every CI run)
- Optional behaviour and its condition (`«extend»`, such as rollback only if smoke tests fail)

Not for: ordering or timing of steps; use `flowchart`, `sequence-diagram` or `state-machine`.

## Anatomy

| Part | Class | Rule |
|---|---|---|
| System boundary | `d-blob2` + `d-h` + `d-k` | One dashed box; only use cases inside, actors outside |
| Actor | `d-line` stick figure + `d-t` + `d-s` | People on the left, automated systems on the right |
| Use case | `ellipse.d-box g0..g5` + `d-t` | A verb phrase; color groups the cases one actor drives |
| Extension condition | `d-s` inside the ellipse | The guard for an `«extend»` case, for example "if smoke fails" |
| Association | `d-edge` | Solid, no arrowhead, actor to use case |
| Include or extend | `d-edge dash` + open `d-line` marker + `d-lab` | Open arrowhead as UML specifies; include points to the included case; extend points to the base case |
| Legend | `d-k` + `d-edge` + `d-s` | Explains the three line types |

## Tips

- Name use cases as goals ("Promote to prod"), not screens or buttons.
- Keep it to a dozen ellipses; split the system if it needs more.
- Watch arrow direction: `«extend»` points from the optional case to the base, the opposite of `«include»`.

Reference: Figma template UML diagram (use case)

Source: [example.svg](example.svg)
