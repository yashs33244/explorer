# explorer

Turn any codebase or system into an interactive beginner field guide: hand-drawn SVG diagrams, a walk through the real files, tables that scroll inside the page, and interview questions you can tick off. Built as a Claude Code skill.

![The generated page](docs/img/hero.png)

## What you get

- Three hand-drawn SVG diagrams per topic: how it connects, a numbered lifecycle, and the anatomy.
- A step-by-step walk through the real code with file and function names.
- Tables sized by content, scrolling inside the page, with a sticky header.
- 8 to 10 interview questions per topic with simple answers and a common trap.
- Light and dark themes, wide margins, phone friendly, no dependencies.

| Architecture | Lifecycle |
|---|---|
| ![architecture](docs/img/diagram-architecture.png) | ![lifecycle](docs/img/diagram-lifecycle.png) |

![A scrolling table](docs/img/table.png)

## Install the skill

```bash
git clone https://github.com/yashs33244/explorer.git
cd explorer
./install.sh          # symlinks skills/codebase-explorer into ~/.claude/skills
```

Then ask Claude Code something like: "Use the codebase-explorer skill to build a field guide for this repo."

## Try the example

```bash
node skills/codebase-explorer/scripts/build-page.js \
  --config examples/postgres/explorer.config.json \
  --topics examples/postgres/topics \
  --diagrams examples/postgres/diagrams \
  --out examples/postgres/page.html
open examples/postgres/page.html
```

`examples/postgres` is a real guide: 20 topics, 63 diagrams, 190 questions and a 37-row contribution backlog table.

## Layout

```
skills/codebase-explorer/
  SKILL.md                 the skill (pipeline, quality bar, gotchas)
  scripts/build-page.js    JSON + SVG -> one HTML page (no dependencies)
  scripts/render.sh        look at diagrams and sections in headless Chrome
  scripts/layout.js        automatic diagram fallback
  assets/                  style.css (page and diagram kit), app.js, icons.md
  references/              topic schema, diagram guide, Workflow template
examples/postgres/         a complete guide to learn from
docs/how-it-works.md       how the diagrams and facts were produced
```

## Requirements

Node 18+, Google Chrome for previews (`CHROME=/path/to/chrome` to override). Publishing and the multi-agent workflow use Claude Code's Artifact and Workflow tools.

## Honesty note

The example's facts were read from the PostgreSQL source and checked by a second pass, and many commands were run against Homebrew PostgreSQL 16. The guide says so, and says which commands were not run. Function names move between releases, so confirm against the version you build.

MIT licensed.
