# PostgreSQL example

A complete guide built with the skill: 20 topics, 63 hand-drawn SVG diagrams, 190 interview questions and a 37-row contribution backlog table.

- `topics/*.json`: researched and fact-checked topic data
- `diagrams/<topic>/d1..d3.svg` and `meta.json`: the hand-drawn diagrams
- `backlog.json`: rows for the scrolling table (researched 2026-10-04, statuses change daily)
- `explorer.config.json`: groups, hero, callouts and extra sections
- `roadmap.html`: the closing "first patch" section

Build it from the repo root:

```bash
node skills/codebase-explorer/scripts/build-page.js --config examples/postgres/explorer.config.json --topics examples/postgres/topics --diagrams examples/postgres/diagrams --out examples/postgres/page.html
```
