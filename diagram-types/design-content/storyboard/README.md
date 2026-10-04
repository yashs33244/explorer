# Storyboard

A storyboard tells a story as a row of framed panels, each with a small scene and a caption under it, read left to right and top to bottom. The example replays incident INC-482 on a checkout API in six panels: a deploy fails on a database migration, an alert pages on-call, the service is rolled back, the migration is fixed, the release goes out again through a canary, and a postmortem files action items. Each frame shows the artifact an engineer actually saw at that moment, and the caption gives the time and what changed.

| Hand-drawn | Clean |
|---|---|
| ![hand-drawn](hand.jpg) | ![clean](clean.jpg) |

## Use it to explain

- How an incident unfolded, from the first failed deploy to the postmortem, for a review or onboarding.
- What a user or operator sees at each step of a new release or migration runbook.
- How a feature moves from a PR to a canary to full rollout, one frame per stage.

Not for: branching logic or parallel teams; use a flowchart or a cross-functional flowchart.

## Anatomy

| Part | Class | Rule |
|---|---|---|
| Panel frame | `d-lane` | equal size, three per row, same gaps |
| Scene | `d-box`, `d-fill`, `d-tag`, icons | one artifact per frame: a pipeline, a chart, a diff |
| Tool | `d-logo` + `d-m` | top-left of the frame, names the system on screen |
| Panel order | `d-edge` | short arrow in the gap between frames of a row |
| Step number | `d-badge` + `d-bt` | under the frame, left of the title |
| Caption | `d-t` + `d-s` | title, then time and outcome in two short lines |
| Decision | `d-note` | only in the final panel, for what was agreed |

## Tips

- Put the time in every caption so the board doubles as a timeline.
- Draw what was on screen (graph, diff, command), not people talking.
- Keep each scene to one idea; if a frame needs two, split it into two panels.

Reference: Figma template Storyboard

Source: [example.svg](example.svg)
