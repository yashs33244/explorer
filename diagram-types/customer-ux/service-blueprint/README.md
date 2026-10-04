# Service blueprint

A grid of stages across the top and four lanes down the side: what the user does, what they see (frontstage), what the team runs behind it (backstage), and the infrastructure that supports it. Dashed lines of interaction, visibility and internal interaction split the lanes, and vertical arrows show which hidden system answers each visible step. The example is self-serve Postgres provisioning: a developer picks an engine, confirms cost, copies the DSN and watches metrics, while the console, provision-api, a Temporal workflow, Vault, a metrics proxy, AWS quotas, a Kubernetes CNPG operator, Postgres and Prometheus do the work.

| Hand-drawn | Clean |
|---|---|
| ![hand-drawn](hand.jpg) | ![clean](clean.jpg) |

## Use it to explain

- Which backend services sit behind each screen of a self-serve product flow.
- Where a user-visible step depends on a slow or failure-prone backstage system (quota checks, workflow retries).
- Who owns each layer when an onboarding flow breaks, and which handoff to instrument.

Not for: the message order between two services (use `sequence-diagram`).

## Anatomy

| Part | Class | Rule |
|---|---|---|
| Stage header | `d-tag acc` + `d-t` | One pill per column, numbered in journey order |
| Lane | `d-lane`, `d-lane alt` | Four lanes, alternating fill, full width |
| Lane header | `d-lanehead g1`..`g4` + `d-t`, `d-s` | Lane name and its role (frontstage, backstage) |
| Separator line | `d-edge dash` + `d-lab` | Interaction, visibility, internal interaction, labelled at the left |
| Step | `d-box g1`..`g4` + `d-t`, `d-s`, `d-m` | One colour per lane; title, detail, real route or setting |
| Product | `d-logo` | Logo slot when the step is a named product |
| Dependency | `d-edge` + `d-lab` | Downward arrow with the verb or call |
| Journey flow | `d-edge acc` | Left to right along the user lane only |

## Tips

- Keep every column to one stage, even if a lane is empty there; gaps show where nothing backstage is needed.
- Put real routes, workflow names and secret paths in `d-m` so on-call engineers can find them.
- The line of visibility is the point of the diagram: anything below it that can fail needs a user-facing state above it.

Reference: Figma template Service blueprint

Source: [example.svg](example.svg)
