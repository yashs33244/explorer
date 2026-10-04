# Directory tree

An indented folder tree with a trunk line, one colored row per top-level folder, its children nested underneath, and sticky notes on the right that say what each folder is for and who owns it. The example annotates a pnpm and Turborepo monorepo: CI workflows, deployable apps, shared packages, backend services, infrastructure and the root config files.

| Hand-drawn | Clean |
|---|---|
| ![hand-drawn](hand.jpg) | ![clean](clean.jpg) |

## Use it to explain

- Where code lives in a monorepo and which folders are deployable versus imported
- Ownership boundaries: which team owns `services/billing-api/` and who gets paged
- How a repo layout maps to CI: which paths trigger which workflow, where Terraform runs

Not for: call flows or runtime behaviour between services; use `request-lifecycle` or `sequence-diagram`.

## Anatomy

| Part | Class | Rule |
|---|---|---|
| Root folder | `d-box` + `d-t` | One box at top-left; a `d-s` line beside it says what the repo is |
| Trunk and branches | `d-edge` | Straight lines only: one vertical trunk, a short horizontal branch per row |
| Top-level folder | `d-box g0..g5` + `d-m` | One color per folder, name in mono with a trailing slash |
| Child folder or file | `d-logo` or file icon + `d-m` | A logo slot when the child is built on a named product, a file icon otherwise |
| Purpose column | `d-s` | Every child gets 2 to 5 words, aligned on one x |
| Annotation | `d-note` + `d-tn`, `d-s`, `d-m` | One note per top-level folder: the rule, the consequence, the owner |
| Pointer | `d-edge dash` + marker | From the folder row to its note, never crossing a child row |

## Tips

- Keep one row pitch (32 units) for every line so the tree reads as a listing.
- Show two or three children per folder; the point is the shape, not a full `ls -R`.
- Put the rule that surprises people in the note (for example "apply only from main"), not a restatement of the name.

Reference: Figma template Directory tree

Source: [example.svg](example.svg)
