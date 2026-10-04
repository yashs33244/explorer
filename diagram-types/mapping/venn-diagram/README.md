# Venn diagram

A Venn diagram shows what sets share and what is unique to each by overlapping circles. With three sets there are seven regions: three exclusive, three pairwise and one shared by all. The example compares relational SQL, NoSQL and NewSQL databases while picking a store for an orders service: exclusive traits sit in each outer region, shared traits in the overlaps, and a sticky note records the decision.

| Hand-drawn | Clean |
|---|---|
| ![hand-drawn](hand.jpg) | ![clean](clean.jpg) |

## Use it to explain

- How three database families, queues or frameworks overlap before choosing one for a service.
- Which responsibilities two teams or two services share, and which belong to only one.
- Which features are common to all deployment targets and which need per-target code.

Not for: more than three sets, or overlaps you need to quantify; use a comparison table or a matrix.

## Anatomy

| Part | Class | Rule |
|---|---|---|
| Set | `d-soft g2` / `g3` / `g4` circle | equal radius, centres on an equilateral triangle so all seven regions exist |
| Set name | `d-t` | inside the exclusive region, under its logos |
| Example products | `d-logo` | two real products per set, in the exclusive region |
| Trait | `d-s` | 1 to 3 words per line, centred in its region |
| All-three region | `d-k` + `d-s` | kicker "ALL THREE" so the centre reads at a glance |
| Decision | `d-note` + `d-tn` | outside the circles, says what the comparison concluded |

## Tips

- Keep every label well inside its region; shorten words rather than let text cross an outline.
- Put the trait that drives the decision in a pairwise region so the overlap does the explaining.
- Use the same radius for all three sets; unequal circles imply a size the data does not have.

Reference: Figma template Venn diagram

Source: [example.svg](example.svg)
