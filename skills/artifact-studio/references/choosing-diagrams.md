# Choosing diagrams for a page

A page earns a diagram only where a picture answers a reader's question better than a sentence or a table. Pick each figure in four steps, then record the choice in `figs.json`. Every slug below is a folder in the explorer repo's `diagram-types/` and a row in `../codebase-explorer/references/diagram-types.md`; start from that folder's `example.svg`.

Selection rules adapted from diagram-design (MIT, github.com/cathrynlavery/diagram-design), drawn with this repo's kit.

## 1. Gate: should this be a diagram at all?

| The content is | Use |
|---|---|
| A list of things, or rows a 3-column table can hold | a table |
| Attributes that change but topology that does not | a before/after table |
| One shape, or two boxes and an arrow | a sentence |
| Parts, flows, order, overlap, position, proportion or change in shape | a diagram (go to step 2) |

## 2. Start from the page's job

Write the questions the reader brings to this page (two to five for most pages; a full roadmap or design doc may need up to eight), then take one figure per question from the row that matches the page. Never draw two figures that answer the same question; never answer a "how much" question with boxes and arrows.

| Page | Reader asks | Figure (slug) | Keep as tables |
|---|---|---|---|
| Repo or codebase architecture | How is the repo cut, and which way may dependencies point? | `repo-map` (bleed), then `sequence-diagram` for the build or request path | components with paths, "where to change what" |
| Design doc, architecture | What are the parts and who calls whom? | `layered-architecture`, `c4-model`, `system-context` | APIs, config, fields |
| | How does one request or job run? | `sequence-diagram`, `request-lifecycle` | |
| | What crosses the boundary, what is checked at the edge, and where does data land? | `boundary-architecture` (beats `cloud-architecture` when trust and ownership matter more than which cloud services run it) | |
| | What is the data shape? What states can it be in? | `er-diagram`, `class-diagram`, `state-machine` | |
| Proposal, decision record | What changes? | `architecture-delta` | costs, risks |
| | How do the options compare? | `product-comparison` (verdict), `coverage-matrix` (parity), `radar-chart` (scores) | |
| | Why this choice? Build or buy? | `decision-tree`, `wardley-map` | |
| Roadmap, plan | What lands when? (the main roadmap figure) | `horizontal-timeline`; `vertical-timeline` when there are many dated items | exit criteria, owners |
| | What ships in which slice? | `story-map` | |
| | What blocks what, in which order? | `dependency-graph` | |
| | Exact dates, durations and overlaps (detailed scheduling only) | `gantt-chart` | |
| | Who owns which stream? | `project-org-chart`, `cross-functional-flowchart` | |
| | What must be true before launch? | `todo-list` | success metrics |
| Comparison, gap analysis | Who supports what, where are the gaps? | `coverage-matrix` | per-cell evidence |
| | Where do the options overlap? | `venn-diagram` | |
| | What to do first? | `quad-chart` | |
| Investigation, postmortem | What caused it? | `fishbone` | evidence log |
| | What happened when? | `vertical-timeline` | |
| | Which exchange or branch failed? | `sequence-diagram`, `flowchart` | |
| | Why does it keep getting worse? | `causal-loop` | |
| | Did the metric move after the fix? | `line-chart` | |
| Status, metrics report | How is it trending? | `line-chart` | raw numbers |
| | How do items compare on one metric? | `bar-graph` | |
| | How did we get from total A to total B? | `waterfall-chart` | |
| | Where does the total go? | `treemap` (many parts), `pie-chart` (up to 5), `sankey-diagram` (across stages) | |
| | When or where does it cluster? | `heat-map` | |
| Migration | What moves where, and in what order? | `architecture-delta`, `tech-stack-mapping`, `horizontal-timeline` (`gantt-chart` only for a detailed schedule) | cutover checklist |
| Explainer, onboarding | What are the words and how do they relate? | `concept-map`, `mind-map` | glossary |
| | How does it work inside? | `layered-architecture`, `sequence-diagram`, `state-machine` | |
| Process, runbook | Which branch do I take? Who hands off to whom? | `flowchart`, `cross-functional-flowchart`, `phone-tree` | commands |

## 3. When behaviour carries the meaning, pick the pattern first

If the point is how something behaves (waits, fails, is enforced, is blocked), choose one pattern, then draw it with its layout type. One pattern per figure.

| The reader must understand | Pattern | Layout type |
|---|---|---|
| Many arrivals compete for finite capacity | fan-in queue: sources, visible queue slots with a count, a capacity label with units, admitted and rejected outcomes | `data-pipeline` |
| The same questions repeat across stages | stage x slot grid with explicit "none" cells | `project-plan`, or a table |
| A loose conversation becomes a structured record | source excerpt, named transform, record with provenance links and unknown fields | `data-pipeline` |
| Why two similar requests got different outcomes | two traces over the same ordered rules, PASS / FAIL / SKIPPED / NOT REACHED as text, first divergence marked | `flowchart` |
| Which routes cross a trust boundary and which are blocked | labelled boundaries, permitted and forbidden ingress, blocked paths stop at the boundary | `boundary-architecture` (edge checks, ownership of stores), `cloud-architecture`, `network-diagram` |
| Which controls apply where | controls grouped by enforcement point, actor and timing, gaps shown | `layered-architecture` |
| How defences compensate and what risk remains | ordered layers, what escapes each one, final residual risk | `layered-architecture` |
| What a system is made of, block by block | stable ids per block, noun names | `functional-decomposition` |
| One subject's phases, waits, retries and terminal outcomes | main rail, separate recovery band, separate terminal band | `state-machine` |

## 4. Otherwise, match the shape

| If you are showing | Slug |
|---|---|
| Folders, packages and crates of one repo, with links, vendored copies and runtime calls | `repo-map` |
| A mechanism the reader should feel (thresholds, matching, capacity), or an isometric, 3D or "more detailed" request | `anatomy` (see `detailed-figures.md`) |
| Components and connections in one snapshot | `layered-architecture`, `c4-model` |
| Callers, the check at the edge, the parts inside and the stores outside one trust boundary | `boundary-architecture` |
| Structural change between before and after, with a change ledger | `architecture-delta` |
| What depends on what, fan-in, cycles, build order | `dependency-graph` |
| Items x capabilities with full / partial / none | `coverage-matrix` |
| Decision logic with branches | `flowchart`, `decision-tree` |
| Time-ordered messages between actors | `sequence-diagram` |
| States, transitions and guards | `state-machine` |
| Entities, fields and keys | `er-diagram` |
| Events or milestones placed in time (a roadmap) | `horizontal-timeline`, `vertical-timeline` (many dated items) |
| Handoffs between teams | `cross-functional-flowchart` |
| Two-axis positioning | `quad-chart` |
| Value chain against evolution, build vs buy | `wardley-map` |
| Scope sliced into releases | `story-map` |
| Tasks on a calendar with durations and dependencies (detailed scheduling) | `gantt-chart` |
| A quantity splitting and merging across stages | `sankey-diagram` |
| A start total bridged to an end total | `waterfall-chart` |
| Part of whole, many parts, nested | `treemap` |
| A trend over time, or before vs after a change | `line-chart` |
| Causes of one effect, grouped | `fishbone` |
| Overlap between sets | `venn-diagram`, `euler-diagram` |

If two types fit, pick the one whose main axis carries the answer (time, hierarchy, flow, position or proportion). Too much for one figure: draw an overview and a detail.

## 5. Budgets and drawing rules

Per figure: at most 9 primary nodes, 12 connectors, accent (`acc`) on 1 or 2 elements, and 2 callout notes. Type caps: architecture delta 8 components and 8 ledger rows; dependency graph 9 nodes, 14 edges, 1 cycle; story map 5 activities, 3 slices, 12 cards; sankey 3 stages, 8 nodes, 12 flows; treemap 8 cells; waterfall 8 bars; line chart 5 series; wardley 9 components, 2 movement arrows; fishbone 6 bones with 3 causes each; sequence 5 lifelines; swimlane 5 lanes; ER 8 entities; quadrant 12 items; repo map 9 containers and 60 chips.

Focus and margins:

- One idea per diagram: it answers one reader question, and a second question gets a second figure.
- More than about 9 nodes or 3 bands (lanes, layers, rows of groups): split it into an overview and a detail, or into two figures.
- Keep at least 32 units of clear margin inside the viewBox on every side: nothing (text, logo, box, stroke) closer than 32 to the viewBox edge. With `viewBox="0 0 800 H"` draw between x=32 and x=768. To give an existing layout room without moving it, widen the viewBox (for example `-12 -12 824 H+24` for content drawn from 20).
- Prefer fewer, larger labels: a 1 to 3 word `d-t` label beats a sentence in `d-s`. Move detail to the caption, the badge legend or a table under the figure.

Colour for structure diagrams (`er-diagram`, `class-diagram`, database schemas, `directory-tree` and other "what is it made of" figures):

- Neutral by default: white boxes (`d-box` with no g-colour), thin ink outline, and a light grey header band (`d-band` with no g-colour) for the table or class name. Relationship diamonds and notes stay neutral too (`d-box`, `d-blob2`).
- Colour carries at most one meaning, and that meaning gets a legend entry. On a change review that meaning is new or changed fields (a `d-band g1` header on a changed table, or a `d-soft g1` strip behind new rows); otherwise it can be the filled primary key tag (`d-tag acc`), as in the catalog examples. Never colour tables only to tell them apart.

Drawing:

- Connectors are orthogonal: right-angle elbows, straight only when both ends align. No diagonals except in charts.
- Labels use `d-lab` beside the segment, never on it; 1 to 5 words; every action arrow has a verb.
- No stacked strokes: offset parallel routes by 12px or more. Each connector on a shared box edge gets its own attach point.
- No line passes behind a box that is not one of its ends; reroute it.
- Draw edges before boxes so lines sit underneath.
- Meaning never rides on colour alone: pair fills with a shape, sign or word (tick, `~`, `-`, `+`, "ruled out"). Each colour means one thing per figure, and the legend says what.
- Legends sit as a strip under the drawing, not floating inside it.

## 6. Record the choice

In `figs.json`, set `"type"` to the slug (or its catalog name) and `"why"` to the reader question the figure answers:

```json
{"d2": {"type": "dependency-graph", "why": "What blocks what, in which order?", "title": "Build order", "caption": "..."}}
```

`scripts/build.py` rejects a type that is not in the catalog, suggests the nearest slugs, warns when `why` is missing, and warns when a page with three or more figures uses only one type.
