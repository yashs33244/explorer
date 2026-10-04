# Work anniversary celebration

A certificate: a double frame, an avatar between two stars, a name ribbon, then what the person actually shipped. The example marks Ravi Menon's 3 years on the platform team with a timeline of milestones (Terraform modules, a zero-downtime EKS upgrade across 40 clusters, an Argo CD rollout to 300 services, a Backstage golden path) and three stats.

| Hand-drawn | Clean |
|---|---|
| ![hand-drawn](hand.jpg) | ![clean](clean.jpg) |

## Use it to explain

- An engineer's impact over several years, told through the systems they shipped.
- How a platform evolved (IaC, cluster upgrades, GitOps, developer portal) through one person's work.
- Team milestones for a service or repo anniversary, such as "5 years of the payments API".

Not for: performance reviews or detailed project history (use `horizontal-timeline` or `project-plan`).

## Anatomy

| Part | Class | Rule |
|---|---|---|
| Frame | two `d-box g2` rects | Outer and inner border, like a printed certificate |
| Avatar | `d-box g4` circle + `d-fill g4` head and shoulders | Centred at the top |
| Stars | `d-fill g2` five-point paths | One each side of the avatar |
| Ribbon | `d-box` tails, folds and centre rect + `d-h`, `d-s` | Name and tenure; draw tails, then folds, then the centre |
| Milestone line | `d-edge acc` + `d-tag` years + `d-fill` dots | One stop per year, latest highlighted |
| Milestone | `d-logo` + `d-t`, `d-s` | Real product logo, what shipped, one result |
| Stats | `d-box g1`, `g3`, `g0` + `d-h`, `d-s` | Three numbers, one tile each |

## Tips

- Pick one milestone per year and give each a measurable result.
- Use logos for the systems shipped so the timeline reads at a glance.
- Keep the ribbon text under about 40 characters so it fits the centre panel.

Reference: Figma template Work anniversary celebration

Source: [example.svg](example.svg)
