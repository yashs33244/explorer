# Marketing mix (4Ps)

Four overlapping circles for Product, Price, Place and Promotion around the thing being launched, with the shared ground of each neighbouring pair written in the overlaps and a detail card per P outside the circles. The example is the v1.0 launch of shipctl, a deploy CLI for platform teams: a single Go binary, a free OSS core with paid Team and Enterprise plans, distribution through Homebrew, apt, Docker and a GitHub Action, and promotion through a quickstart, Show HN and a KubeCon talk.

| Hand-drawn | Clean |
|---|---|
| ![hand-drawn](hand.jpg) | ![clean](clean.jpg) |

## Use it to explain

- How a developer tool or SDK will be packaged, priced, distributed and announced at launch.
- Where engineering choices (one static binary, a free tier with the full CLI) carry go-to-market decisions.
- Which channels an internal platform uses to reach its users (docs, CLI install, Slack, demos).

Not for: comparing the tool against competitors (use `venn-diagram` or a positioning map).

## Anatomy

| Part | Class | Rule |
|---|---|---|
| P circle | `d-soft g1`..`g4` | Four equal circles in a 2x2, overlapping their neighbours |
| P title | `d-h` | In the part of the circle no other circle covers |
| Pair overlap | `d-s` | Two short lines naming what the pair shares |
| Core | `d-fill g5` + `d-tw` | Small solid circle in the middle naming the product and version |
| Detail card | `d-box g1`..`g4` + `d-logo` | Same colour as its circle, three bullets and one `d-m` line |
| Link | `d-edge dash` | Dashed arrow from each card to its circle |

## Tips

- Keep overlap text to two lines of about 12 characters; the lenses are narrow.
- Match each card colour to its circle so the eye pairs them without arrows.
- Put the target user in a footer pill; every P should make sense for that user.

Reference: Figma template Marketing mix

Source: [example.svg](example.svg)
