---
name: artifact-studio
description: Default for building ANY artifact or artefact page (design doc, proposal, explainer, plan, review, report, comparison) with light theme, clean SVG diagrams, wide tables and full-screen diagrams. Use whenever the user asks to create, build, update or publish an artifact/artefact or an HTML page to share, or says "make an artefact", "explain with diagrams", "design artifact", "proposal page". For a full codebase field guide with interview questions use codebase-explorer instead.
---

# Artifact Studio

One self-contained page that explains a decision, design or system with clean diagrams and wide tables. It reuses the diagram kit, diagram catalog and renderer from `codebase-explorer` (sibling skill in the same repo), but only for a single page, not a multi-topic field guide.

## Defaults (always, unless the user says otherwise)

- **Light theme only.** White background, every color token on bare `:root`, no dark-mode blocks, explicit `body` background. Do not zero the `html` padding.
- **Clean diagram style only.** Inline SVG using the kit classes from `../codebase-explorer/references/diagram-kit.md`. No hand-drawn filter, no style toggle.
- **Diagrams centred**, each with a **Full screen** button that opens a viewport overlay (Close button, Esc, backdrop click). Default view fits the content width.
- **Wide tables with small margins.** Page up to `min(1400px, 94vw)`, 16 to 24px side gutters, prose about 75ch. Each table sits in `.tablewrap` (scrolls sideways in its own box; sticky header when long). Columns sized by content.
- **Plain short sentences.** No em dash anywhere. No first person unless the user wants it. No names of people unless the user asks.
- **Honest.** Every file, function, number and command is real; mark anything unchecked as "not verified"; label illustrative numbers.

All of this is already in `assets/page-template.html`.

## Pipeline

1. **Scope.** One subject, one audience, one job for the page. Pick 3 to 6 sections and 2 to 5 diagrams. Ground facts in real code, tickets and runs, not memory.
2. **Write `body.html`.** Plain HTML using the template classes:
   - header: `<header class="top">` with `.kicker`, `h1`, `.lede`, `.note` (status line), `nav.toc`
   - sections: `<section id="x"><p class="num">01</p><h2>...</h2>...</section>`
   - tables: `<div class="tablewrap"><table>...</table></div>`
   - status chips: `<span class="pill ok|next|todo|ill">`, callouts: `.tldr`, `.note`, cards: `.cards > .card`, two columns: `.grid2`
   - a diagram goes where you write `{{fig:KEY}}`
3. **Draw diagrams** as `svg/KEY.svg`. For each, pick the type whose form fits the content from `../codebase-explorer/references/diagram-types.md` and start from that type's `example.svg` in the repo's `diagram-types/` folder. Follow `../codebase-explorer/references/diagram-guide.md`: every arrow labelled with a verb, 12px minimum text, ids prefixed with the key, numbered badges that match a legend, no hex colors, no style or script tags.
4. **Check each diagram by eye**: `../codebase-explorer/scripts/render.sh svg/KEY.svg /tmp/KEY.png light clean`, Read the PNG, fix overlaps, clipped text and wrong arrows (up to 3 rounds).
5. **Describe figures** in `figs.json`: `{"KEY": {"type": "...", "title": "...", "caption": "...", "badges": [...], "legend": [["--cl1-f", "label"]]}}`.
6. **Build**: `python3 scripts/build.py --title "Page Name" --body body.html --svg svg --figs figs.json --out page.html`. It fails if a `{{fig:KEY}}` has no entry, and replaces any stray em or en dash.
7. **Look once** at the whole page (headless Chrome screenshot, or the Artifact preview) and fix what is visibly broken.
8. **Publish.** `page.html` is one self-contained file: open it locally or host it anywhere. If your agent has an Artifact tool, publish with it: `<title>` is a 2 to 4 word name, `description` one sentence, `icon` one generic word. Republish the same file path to keep the URL, and remind the user the page is private until shared.

`examples/basic/` is a minimal working body, figs.json and diagram.

## Work boundary

This skill lives in a public repo. Never copy private work content (company code, tickets, page bodies) into it; keep each page's sources in the session scratchpad or your own project folder.
