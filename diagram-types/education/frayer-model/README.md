# Frayer model

A square split into four quadrants around a central pill that names one concept: definition, characteristics, examples and non-examples. It pins down a fuzzy term by showing what it is and, just as important, what it is not. The example defines idempotency: a one-line definition with `f(f(x)) = f(x)`, the traits of an idempotent API (client key, stored response, TTL), real examples (Stripe idempotency keys, Postgres upsert, Kafka idempotent producer, `kubectl apply`) and non-examples that cause double charges or duplicate rows.

| Hand-drawn | Clean |
|---|---|
| ![hand-drawn](hand.jpg) | ![clean](clean.jpg) |

## Use it to explain

- A term a codebase leans on (idempotency, eventual consistency, backpressure) to new engineers before they touch the code.
- The line between a safe pattern and a look-alike that breaks, such as an upsert versus a bare `qty = qty - 1`.
- A team convention, such as what counts as a "breaking change" in an API review.

Not for: how the concept works step by step over time (use `sequence-diagram` or `flowchart`).

## Anatomy

| Part | Class | Rule |
|---|---|---|
| Quadrant | `d-band g1`..`g4` | Four equal bands, small gap, one colour each, fixed order: definition, characteristics, examples, non-examples |
| Quadrant header | `d-k`, `d-h` | Kicker plus title; left-aligned on the left quadrants, right-aligned on the right ones |
| Concept pill | `d-box g0` on a `path` | Centred on the cross, fully rounded (a path with arc ends, since clean mode squares off `rect` corners), `d-k` + `d-h` + `d-s` |
| Definition and traits | `d-t`, `d-m`, `d-fillacc` dots | One sentence for the definition, one short line per trait |
| Example row | `d-box` + `d-logo` + `d-lineacc` tick | Product logo, name in `d-t`, the exact setting or code in `d-m` |
| Non-example row | `d-box` + `d-lineacc` cross | Name in `d-t`, the consequence in `d-m` |

## Tips

- Keep content away from the inner corners; the concept pill covers them.
- Make every non-example a near miss that looks right, not an obvious wrong answer.
- Put the real code or config in `d-m` so the example is copyable.

Reference: Figma template Frayer model

Source: [example.svg](example.svg)
