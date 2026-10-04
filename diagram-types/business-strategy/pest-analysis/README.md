# PEST analysis

Four circles in a 2x2 for the Political, Economic, Social and Technological forces outside the team's control, each with an icon, three factors and a tag pointing to the decision it drove, beside a title column that states the subject and the numbered decisions. The example is the launch of a managed vector database on AWS and GCP: EU data residency, a price war with Pinecone and Weaviate, developers expecting a free tier, and HNSW indexes that are heavy on RAM.

| Hand-drawn | Clean |
|---|---|
| ![hand-drawn](hand.jpg) | ![clean](clean.jpg) |

## Use it to explain

- The outside forces that shape a platform launch, such as regulation forcing a new cloud region.
- Why a pricing or API decision was made, by tracing it back to a market or technology factor.
- Risks to a migration or build-vs-buy choice that come from outside the codebase.

Not for: the team's own strengths and weaknesses (use a `quad-chart` laid out as a SWOT).

## Anatomy

| Part | Class | Rule |
|---|---|---|
| Subject | `d-tag acc` + `d-k`, `d-h`, `d-s` | Left column: kicker, subject, scope and owner |
| Decisions | `d-box g0` + `d-badge` | Numbered list of what the analysis led to |
| Factor circle | `d-soft g4`, `g5`, `g1`, `g3` | 2x2, touching, one colour per letter |
| Factor icon | `d-fillpaper`, `d-line`, `d-lineacc` | Building, chart, people, gear, centred at the top |
| Factors | `d-h` + `d-s` | Letter and name, then three short factors, centred |
| Trace tag | `d-tag acc` or `d-tag` | "drives N" pointing to the decisions; `acc` marks high impact |

## Tips

- Every factor should be outside the team's control; anything the team can change belongs elsewhere.
- Link each circle to a numbered decision, or the analysis is a list of worries.
- Keep factors to about 26 characters so they stay inside the circle at the widest line.

Reference: Figma template PEST analysis

Source: [example.svg](example.svg)
