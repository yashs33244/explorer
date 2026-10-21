---
name: artifact-studio
description: Default for building ANY artifact or artefact page or multi-page artifact site (design doc, proposal, explainer, roadmap, plan, review, report, comparison, investigation) with light theme, clean FigJam-style SVG diagrams chosen per reader question (architecture delta, coverage matrix, dependency graph, story map, timeline, Wardley map, sankey, waterfall, line chart, treemap, fishbone and the rest of the catalog), wide tables with filters and highlighted key columns and rows, interactive diagrams (hover focus, badge and legend linking, step-through, zoom and pan), bleed-width repo maps, deeper engineering pages, detailed isometric figures through the anatomy skill, full-screen diagrams, and for sites an index, top nav, per-page section list and Previous / Next links. Use whenever the user asks to create, build, update or publish an artifact/artefact or an HTML page or site to share, or says "make an artefact", "explain with diagrams", "design artifact", "proposal page", "roadmap page", "multi-page artifact", "explain this repo architecture", "more detailed diagram", "isometric diagram". For a full codebase field guide with interview questions use codebase-explorer instead.
---

# Artifact Studio

One self-contained page, or a small multi-page site, that explains a decision, design or system with clean diagrams and wide tables. It reuses the diagram kit, diagram catalog and renderer from `codebase-explorer` (sibling skill in the same repo), but for one subject, not a multi-topic field guide.

Use one page by default. Use **site mode** when the subject has more than about 6 sections or several audiences (for example a roadmap with an overview, one page per stream and a risks page): an `index.html` with a card per page, plus one HTML file per page, all in one folder.

## References (load when the step needs them)

| File | Load when |
|---|---|
| `references/choosing-diagrams.md` | choosing any figure (step 2) |
| `references/highlighting.md` | writing the body and tables (step 3) |
| `references/engineering.md` | the page is about software: design, repo, migration, incident, review |
| `references/interactive.md` | adding node focus or step-through to a figure |
| `references/detailed-figures.md` | the user wants more detail, isometric, 3D or a "real object" figure (anatomy skill) |
| `references/style-guide.md` | tokens, fonts, figure sizes |
| `references/checklist.md` | before publishing (step 8) |
| `../../diagram-types/technical/repo-map/README.md` | drawing a repo map with `scripts/repo_map.py` |

## Defaults (always, unless the user says otherwise)

- **Light theme only.** White background, every color token on bare `:root`, no dark-mode blocks, explicit `body` background. Do not zero the `html` padding.
- **Clean diagram style only.** Inline SVG using the kit classes from `../codebase-explorer/references/diagram-kit.md`. No hand-drawn filter, no style toggle.
- **Right diagram for the question.** Each figure answers one reader question and its type comes from `references/choosing-diagrams.md`; never default to boxes and arrows for numbers, comparisons, plans or causes.
- **Diagrams centred with room to breathe**, each with a **Full screen** button that opens a viewport overlay (Close button, Esc, backdrop click). Default view fits the content width, inside 16 to 64px of side padding in the figure frame (more on wider screens), so no drawing touches the frame. Every diagram also keeps at least 32 units of clear margin inside its viewBox on every side.
- **Neutral structure diagrams.** ER, class, schema and other "what is it made of" figures use white `d-box` boxes, a thin ink outline and a light grey `d-band` header with no g-colour; colour carries at most one meaning (for example new or changed fields) and the legend says which.
- **Diagrams get the room.** Inline figures run up to 1080px wide inside 16 to 64px of side padding; `"size": "bleed"` runs wider than the text column for repo maps and dense architecture, keeping about 40px of air on each side (`references/style-guide.md`).
- **Highlight the point.** One `<mark>` per section for the sentence that matters, `b.k` for key terms, `.metric` for numbers that matter, callouts for risks and decisions; every table marks its deciding column (`th.key`) or rows (`tr.key`) (`references/highlighting.md`).
- **Always interactive, never required.** Every figure is interactive: wrap each part in `<g data-node>` and each link in `<g data-edge>` so hover focuses a part and its neighbours, and wrap the beats of any ordered figure (a sequence, a flow, a timeline) in `<g data-step>`; `build.py` warns about a figure with neither. Figures also link badges and legends to the drawing and zoom and pan full screen. Tables with 6 or more rows get a filter box, sortable headers and column selects. The static page stays complete (`references/interactive.md`).
- **Engineering depth.** For software subjects, explain what exists, how it runs, where it lives in the code, what breaks and how we know it works, with real paths and detailed figure walkthroughs; build with `--kind engineering` (`references/engineering.md`).
- **Wide tables with small margins.** Page up to `min(1480px, 100% - 40px)`, 16 to 20px side gutters, prose about 75ch. Each table sits in `.tablewrap` (scrolls sideways in its own box; sticky header when long). Columns sized by content.
- **Plain short sentences.** No em dash anywhere. No first person unless the user wants it. No names of people unless the user asks.
- **Honest.** Every file, function, number and command is real; mark anything unchecked as "not verified"; label illustrative numbers.

All of this is already in `assets/page-template.html`.

## Pipeline

1. **Scope.** One subject, one audience, one job for the page. Pick 3 to 6 sections per page; more than that, split into pages and use site mode. Ground facts in real code, tickets and runs, not memory.
2. **Choose the figures** with `references/choosing-diagrams.md`: write the questions the reader brings (2 to 5 for most pages, up to 8 for a full roadmap or design doc), take one figure per question from the row for this kind of page (design doc, proposal, roadmap, comparison, investigation, report, migration, explainer, runbook), pick a behaviour pattern first when waits, failures, enforcement or risk carry the point, and keep as a table anything a table says as well. No two figures answer the same question; numbers get a chart, not boxes and arrows.
3. **Write `body.html`.** Plain HTML using the template classes:
   - header: `<header class="top">` with `.kicker`, `h1`, `.lede`, `.note` (status line), `nav.toc` (single page only; site mode generates the section list)
   - sections: `<section id="x"><p class="num">01</p><h2>...</h2>...</section>`
   - tables: `<div class="tablewrap"><table>...</table></div>`
   - status chips: `<span class="pill ok|next|todo|ill">`, callouts: `.tldr`, `.note`, `.callout warn|risk|ok`, cards: `.cards > .card`, two columns: `.grid2`
   - highlights: `<mark>`, `<b class="k">`, `<span class="metric">`; table marks: `th.key`, `th.num`, `th[data-filter]`, `tr.key|good|bad|dim`
   - a diagram goes where you write `{{fig:KEY}}`
4. **Draw diagrams** as `svg/KEY.svg` (repo maps: write a spec and run `scripts/repo_map.py spec.json > svg/KEY.svg`; detailed or isometric objects: build with the anatomy skill per `references/detailed-figures.md`), starting from the chosen type's `example.svg` in the repo's `diagram-types/` folder (anatomy in its README). Follow `../codebase-explorer/references/diagram-guide.md` and the budgets and connector rules in `references/choosing-diagrams.md`: one idea per figure, at most 9 primary nodes, 3 bands and 12 connectors (over budget: split into an overview and a detail), at least 32 units of clear margin inside the viewBox on every side, fewer and larger labels, accent on 1 or 2 elements, orthogonal connectors, every action arrow labelled with a verb, 12px minimum text, ids prefixed with the key, numbered badges that match a legend, no hex colors, no style or script tags. Structure diagrams follow the neutral colour rule above.
5. **Check each diagram by eye**: `../codebase-explorer/scripts/render.sh svg/KEY.svg /tmp/KEY.png light clean`, Read the PNG, fix overlaps, clipped text and wrong arrows (up to 3 rounds).
6. **Describe figures** in `figs.json`: `{"KEY": {"type": "<catalog slug>", "why": "<reader question>", "title": "...", "caption": "...", "badges": [...], "legend": [["--cl1-f", "label"], ["line dash", "vendored"]], "size": "bleed"}}`. `size` is optional: `wide` fills the text column (timelines), `bleed` nearly the window (repo maps default to it). A badge can be a string or `{"t": "name", "d": "what happens here", "file": "path"}`, which renders a detailed walkthrough under the figure; engineering pages use the detailed form. An anatomy figure is `{"type": "anatomy", "src": "anatomy/x-light.html", "height": 620, ...}`.
7. **Build** one page: `python3 scripts/build.py --title "Page Name" --body body.html --svg svg --figs figs.json --out page.html [--kind engineering]`. It fails if a `{{fig:KEY}}` has no entry or a `type` is not in the catalog, warns when `why` is missing, every figure has the same type, nothing is highlighted, a wide table has no key column or row, or (engineering) the page lacks failure modes, verification, real paths or detailed badges, and replaces any stray em or en dash.

   Or build a **site**: `python3 scripts/build.py --site site.json --out site/`, where `site.json` (paths relative to it) is

   ```json
   {"title": "Site title", "kicker": "roadmap", "lede": "One paragraph for the index.", "note": "Status line.",
    "svg": "svg",
    "pages": [{"slug": "overview", "title": "Overview", "summary": "One line for the index card.",
               "body": "overview.html", "figs": "overview.figs.json"},
              {"slug": "risks", "title": "Risks", "body": "risks.html"}]}
   ```

   `kicker`, `note`, `summary` (defaults to the page's `p.lede`), `group` (consecutive pages with the same group share a heading on the index, for example "Decide" and "Reference"), `figs`, per-page `svg`, and `intro` / `intro_figs` (HTML shown on the index between the lede and the cards, for example the conclusion) are optional. The build writes `index.html` (title, lede, intro, one card per page) and `<slug>.html` per page. Every page gets the same top nav with the current page marked, an "On this page" list built from its `<section id>` and `h2` (sticky on the left on wide screens, on top on narrow ones), and Previous / Next links. A page body without an `h1` gets a generated header with the page title, and its `p.lede` moves into that header.
8. **Run the checklist** (`references/checklist.md`) and **look once** at the whole page (headless Chrome screenshot, or the Artifact preview) and fix what is visibly broken. For a site, look at `index.html` and at least one page: `../codebase-explorer/scripts/render.sh --page site/index.html /tmp/index.png`.
9. **Publish.** `page.html` (or the site folder) is self-contained: open it locally or host it anywhere. If your agent has an Artifact tool, publish with it: `<title>` is a 2 to 4 word name, `description` one sentence, `icon` one generic word. Republish the same file path to keep the URL, and remind the user the page is private until shared.

`examples/basic/` is a minimal working body, figs.json and diagram.

## Work boundary

This skill lives in a public repo. Never copy private work content (company code, tickets, page bodies) into it; keep each page's sources in the session scratchpad or your own project folder.
