# Dichotomous key

A dichotomous key identifies something by a chain of yes or no questions: each question splits the remaining options in two until one answer is left. The example picks a datastore for a new service with six numbered questions (relational schema, global writes, analytics scans, key lookups, latency, full-text search) ending in seven real stores, and highlights the path orders-svc took to PostgreSQL.

| Hand-drawn | Clean |
|---|---|
| ![hand-drawn](hand.jpg) | ![clean](clean.jpg) |

## Use it to explain

- A tech-selection rule a team agreed on, such as which datastore, queue or runtime a new service should use.
- Incident triage: is it one region, is it one tenant, did a deploy just go out, until you reach the runbook.
- Classifying an alert, a ticket or a dependency into exactly one bucket with no judgement calls.
- Not for: decisions with weighted tradeoffs or more than two answers per question (use a decision matrix or a flowchart).

## Anatomy

| Part | Class | Rule |
|---|---|---|
| Question | `d-box g0` / `g5` + `d-t` | Phrased as a yes or no question, at most four words. |
| Question number | `d-badge` + `d-bt` | Numbered in reading order so people can say "we stopped at 3". |
| Branch | `d-edge` + `d-lab` | Exactly two per question, labelled yes and no; yes always on the left. |
| Highlighted path | `d-edge acc` | One worked example traced from root to leaf. |
| Answer | `d-box g1` + `d-logo` | Leaf with the product logo, name and a two-word use case. |

## Tips

- Keep every leaf on one row so the answers can be scanned and compared side by side.
- Color the side of the tree on the highlighted path differently from the other side.
- Ask the most splitting question first; a lopsided first split makes the tree deep on one side.

Reference: Figma template Dichotomous Key

Source: [example.svg](example.svg)
