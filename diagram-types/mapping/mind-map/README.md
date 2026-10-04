# Mind map

A mind map puts one topic in the center and branches the subtopics around it, each with its own leaves. This example is a platform team's onboarding map for Kubernetes on EKS: five branches (workloads, networking, security, storage, observability) radiate from the cluster, and each branch lists the resource kinds or tools a new engineer meets first.

| Hand-drawn | Clean |
|---|---|
| ![hand-drawn](hand.jpg) | ![clean](clean.jpg) |

## Use it to explain

- The surface area of a platform or framework to someone new to it, grouped by concern.
- How a large topic (an incident review, a migration) splits into workstreams before planning.
- Which tools sit under each area of a stack, with logos for the real products.

Not for: dependencies or order between items (use `flowchart` or `concept-map`).

## Anatomy

| Part | Class | Rule |
|---|---|---|
| Central topic | `circle.d-box g0` + `d-h` | One per map, with the product logo and a short context line in `d-s` |
| Branch | `d-box g1`..`g5` + `d-t` | One color per branch, one or two words |
| Branch connector | `d-edge thick` | Curves out of the circle radially, no arrowheads |
| Leaf | `d-tag` + `d-m` | Mono for resource kinds; add a `d-logo` for real tools |
| Leaf connector | `d-edge` | Thin curves fanning out from the outer side of the branch |

## Tips

- Keep leaves on the outer side of each branch so connectors never cross the center.
- Four or five branches with three to five leaves each stays readable at 800 wide.
- A branch at the bottom can lay its leaves out in a row to use the width.

Reference: Figma template Mind map

Source: [example.svg](example.svg)
