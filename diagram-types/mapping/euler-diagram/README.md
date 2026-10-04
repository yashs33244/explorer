# Euler diagram

An Euler diagram draws only the set relationships that actually exist: a set fully inside another is a circle inside a circle, and sets with nothing in common sit apart instead of being forced into an empty overlap as a Venn diagram would. The example nests production services by policy (all services, stateful, needs backups, holds PII) so the containment rules read at a glance, and keeps batch jobs as a disjoint set with their own policy.

| Hand-drawn | Clean |
|---|---|
| ![hand-drawn](hand.jpg) | ![clean](clean.jpg) |

## Use it to explain

- Policy containment in a service catalog: every PII store is backed up, every backed-up service is stateful.
- Permission scopes where one role's grants are a strict subset of another's (viewer inside editor inside admin).
- Which workloads a rule applies to, and which workloads sit entirely outside it (cron jobs, one-off scripts).
- Not for: sets that partly overlap in arbitrary ways (use a Venn diagram) or counts you want compared exactly (use a bar chart).

## Anatomy

| Part | Class | Rule |
|---|---|---|
| Set | `d-soft g1`..`g5` | One color per set. Nested sets are drawn after their parent so they stack on top. |
| Set name | `d-h` + `d-s` | Name and count in the band the set does not share with its child. |
| Member | `d-tag` + `d-m` | Two or three real members per region, placed in that region only. |
| Disjoint set | `d-soft g5` | Separate circle with clear space between it and every other set. |
| Reading rule | `d-note` + `d-tn` | One sentence that states the containment chain in words. |

## Tips

- Make nested circles internally tangent at the bottom, as in the template, so each ring keeps a wide band at the top for its label.
- Put members in the innermost set they belong to; a tag in a ring means "in this set but not the inner one".
- Keep disjoint sets visibly apart; a near-touch reads as an overlap.

Reference: Figma template Euler Diagram

Source: [example.svg](example.svg)
