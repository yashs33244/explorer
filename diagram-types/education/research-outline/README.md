# Research paper outline

A vertical chain of section boxes, topped by a folder-tabbed title card, with arrows that say how each part leads to the next. It shows the argument of a paper before a single paragraph is written. The example outlines the Raft paper (Ongaro and Ousterhout, USENIX ATC 2014): thesis, why Paxos is hard (sections 1-3), the algorithm with its four subsections (terms, election, replication, safety), practical extensions, the evaluation, and related work, with etcd, Consul and CockroachDB as adopters.

| Hand-drawn | Clean |
|---|---|
| ![hand-drawn](hand.jpg) | ![clean](clean.jpg) |

## Use it to explain

- The structure of a design doc or RFC before it is drafted: problem, proposal, alternatives, rollout.
- How a systems paper the team is reading argues its case, section by section.
- An engineering blog post or postmortem write-up, so reviewers agree on the story first.

Not for: a decision with branches (use `flowchart`) or the components of the system itself (use `layered-architecture`).

## Anatomy

| Part | Class | Rule |
|---|---|---|
| Title card | `d-box g1` + tab `d-box g0` | Folder tab on top, venue and authors in `d-k`, title in `d-h`, thesis in `d-s` |
| Section block | `d-box g2`..`g5`, `g0` | Full width, one colour per part, section numbers in `d-k` |
| Subsection | `d-tag` or `d-box` | Tags for a list of sections, small boxes when each needs a two-line gist |
| Evidence | `d-tag acc` | Highlighted pills for results the paper claims |
| Reading order | `d-badge` + `d-bt` | Numbered circles on the left, one per block |
| Link | `d-edge acc` + `d-lab` | One short downward arrow per gap, labelled with a verb |
| Impact | `d-logo` | Real products that adopted the work |

## Tips

- Label each arrow with how the parts relate ("answers with", "checked by"), not just "next".
- Give the core contribution the tallest block and break it into subsections.
- Keep five to seven blocks; more means sections should be merged.

Reference: Figma template Research paper outline

Source: [example.svg](example.svg)
