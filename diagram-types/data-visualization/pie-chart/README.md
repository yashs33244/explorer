# Pie chart

A pie chart splits one total into parts, with each slice's angle showing its share. This example is the platform team's September AWS bill of $181.9k, split by service: EC2 compute takes 41%, RDS Postgres 22%, S3 14%, data transfer 12% and the rest 11%. Slices start at twelve o'clock, largest first and clockwise, a legend table on the right gives the dollar amount and what each line covers, and a sticky note flags the slice that moved.

| Hand-drawn | Clean |
|---|---|
| ![hand-drawn](hand.jpg) | ![clean](clean.jpg) |

## Use it to explain

- Where a cloud bill goes, by service, team or environment.
- How traffic, storage or error volume splits across a handful of sources.
- Which one share is large enough to be worth an optimisation project.

Not for: more than about six parts, comparing two months side by side, or values that do not add up to one total (use a bar graph).

## Anatomy

| Part | Class | Rule |
|---|---|---|
| Slice | `path.d-fill g0`..`g5` | Start at 12 o'clock, largest first, clockwise; shares sum to 100% |
| Slice share | `d-tw` | Percent inside the slice at about two thirds of the radius |
| Legend row | `d-fill` swatch + `d-t`, `d-s` | Same order as the slices, name plus what it covers |
| Amount column | `d-t`, `d-s` right aligned | Real dollar amount and percent, with a total row under a `d-grid` rule |
| Vendor | `d-logo` | One logo for the vendor whose bill this is |
| Finding | `d-note` + `d-tn` | What changed and the action to take |

## Tips

- Merge small parts into an "Other" slice and name what is in it.
- Print the absolute amount next to the percent; shares alone hide the size of the bill.
- Keep slice colors identical between the pie and its legend.

Reference: Figma template Pie chart

Source: [example.svg](example.svg)
