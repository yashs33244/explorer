# Bubble map

One central bubble for the thing being described, ringed by smaller bubbles that each hold one adjective about it, joined by straight spokes. It is a thinking-map form: it describes, it does not rank or sequence. The example describes the Redis orders cache with eight adjectives (fast, bounded, shared, volatile, stale-prone, key-addressed, read-heavy, costly), each backed by a setting or a number (stale-prone, for example, is a 300 s TTL with no invalidation on write).

| Hand-drawn | Clean |
|---|---|
| ![hand-drawn](hand.jpg) | ![clean](clean.jpg) |

## Use it to explain

- The character of a component to a new engineer before they touch it, such as a cache, queue or index.
- The properties a service must keep through a rewrite or migration.
- How a team talks about a dependency during incident review.

Not for: how parts connect or call each other (use `layered-architecture` or a flowchart) or ideas that branch into sub-ideas (use a mind map).

## Anatomy

| Part | Class | Rule |
|---|---|---|
| Subject | `d-box g3` circle + `d-logo` | Largest bubble in the centre, logo, name in `d-h`, address in `d-m` |
| Adjective bubble | `d-soft g3` circle | Same radius for all, evenly spaced on an ellipse around the subject |
| Adjective | `d-t` | One word, centred |
| Evidence | `d-s` + `d-m` | The fact and the setting or number that backs the adjective |
| Spoke | `d-edge` | Straight line edge to edge, no arrowheads |

## Tips

- Use adjectives only; nouns turn it into a mind map.
- Back every adjective with a number or config value so it can be checked.
- Six to eight bubbles fit an 800 wide canvas without crowding.

Reference: Figma template Bubble map

Source: [example.svg](example.svg)
