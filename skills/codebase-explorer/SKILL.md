---
name: codebase-explorer
description: Turn a codebase, system or subject into an interactive beginner field guide with hand-drawn SVG diagrams, step-by-step walkthroughs, interview questions, scrollable tables and a published artifact. Use when the user asks to explore, explain or onboard them onto a repo or technology "with diagrams", says "explorer", "field guide", "teach me this codebase", or wants an interview-style tour of how something works.
---

# Codebase Explorer

Builds one self-contained page that teaches a codebase the way an expert would interview a newcomer: for each topic a plain explanation, three hand-drawn SVG diagrams, a walk through the real files, a table of what to open, try-it commands and 8 to 10 interview questions with simple answers. It was first built for PostgreSQL (see `examples/postgres` in the explorer repo: 20 topics, 63 diagrams, 190 questions).

## When to use

- "Explain this repo/system to me from scratch, with diagrams."
- "Onboard me so I can contribute." "Quiz me on how X works."
- Any time the answer is better as pictures plus a guided tour than as chat text.

Skip it for a one-fact question or a small bug fix.

## What you need

- `node` (the builder has no dependencies) and Google Chrome (to look at diagrams; `scripts/render.sh`).
- The Artifact tool to publish. Load the `artifact-design` skill first, as that tool requires.
- Optional: `/graphify <repo>` to map a large repo first and pick topics from its communities.
- The Workflow tool for the multi-agent run, only when the user opted into orchestration (for example said "ultracode" or "use a workflow"). Without that, do the same steps with a few Agent calls, one topic at a time, and cap the guide at 5 to 8 topics.

## The pipeline

1. **Scope.** Decide the subject root, the audience (default: complete beginner who wants to contribute), 8 to 20 topics and how to group them (for example Run it, Engine, Data and safety, Scale, Extend). Order topics in the order a newcomer should learn them. Use graphify communities or the directory tree to find them. Create a work dir, for example `.explorer/<name>/` with `topics/`, `diagrams/`, and `explorer.config.json`.
2. **Research (one agent per topic).** Each agent reads the real source, and runs the real thing when it can (scratch dir, spare port, always cleaned up), then writes `topics/<key>.json` following `references/topic-schema.md`. Ask for easy-to-hard interview questions with a "common trap" where a misconception is likely. Every path, function and command must be real.
3. **Verify (a second, skeptical agent per topic).** It checks paths with `ls`, names with grep, and each answer's technical accuracy. In the PostgreSQL run it found real mistakes in about a third of the topics (wrong file, backwards visibility rule, misnamed process types). Apply its corrections to the topic JSON before drawing.
4. **Draw (three SVGs per topic).** Roles: `architecture` (who talks to whom), `lifecycle` (numbered scenario in time order) and `structure` (the anatomy: a page layout, a directory tree, a record). Follow `references/diagram-guide.md` and the style kit in `assets/style.css`. The drawing agent must render each file with `scripts/render.sh`, Read the PNG, and fix overlaps, clipped text and wrong arrows, up to 3 rounds, in light and dark.
5. **Critique, then fix.** A separate agent renders every diagram again and looks for overlap, tiny text, unlabeled arrows, wrong facts and out-of-bounds elements. Fix major issues, then re-render.
6. **Assemble.** Write `diagrams/<key>/meta.json` (file, role, title, caption, badge legend) for each topic and run

   ```bash
   node <skill>/scripts/build-page.js --config explorer.config.json --topics topics --diagrams diagrams --out page.html
   ```

   Add extra sections to the config for tables (a backlog, a glossary, a comparison) or a closing roadmap. Look at the result once: `scripts/render.sh --page page.html out.png` and `--section page.html <id> out.png`, then Read the PNGs.
7. **Publish.** Pass the HTML to the Artifact tool (title is a short name, `description` is one sentence, icon is one generic word). Update the same file path to keep the URL. State what was run for real and what was not.

`references/workflow-template.js` is a ready Workflow script for steps 2 to 5. Pass the subject, repo path, scratch dir, skill dir and topic list as `args`.

## Quality bar (these were all learned the hard way)

- **Honesty first.** Never invent a file, function, command or number. Say which facts came from a real run and which are from reading. If a tool (Docker, a server) was unavailable, say the related commands are untested.
- **Diagrams are inline SVG**, hand-drawn style, styled only with the kit classes so they work in both themes. 12px minimum text, 1 to 5 words per label, every arrow labeled with a verb, numbered badges that match a legend, ids prefixed with the topic key. No hex colors, no style or script tags.
- **Diagrams fit one screen.** The CSS caps each at about 78vh and scrolls sideways on narrow screens instead of shrinking text.
- **Tables fit one page.** Use the builder's table helper: columns are sized by content (long sentences get the most room, numbers and tags stay narrow), tables over 8 rows scroll vertically inside the page with a sticky header, and wide tables scroll sideways inside their own box.
- **Wide margins.** Page gutters are `clamp(20px, 6vw, 104px)`. Keep that.
- **No em dash character** anywhere in generated text. The builder replaces any that slip through.
- Both themes: define tokens on `:root`, redefine under `prefers-color-scheme: dark` and `[data-theme]`, set an explicit body background.
- Do not post, push or claim anything outward-facing as part of the exploration.

## Gotchas

- Headless Chrome clamps window width to about 500px. To check phone layout, put the page in a 390px-wide `<iframe>`.
- Jumping to `#section` before a screenshot gives a blank image. Use `render.sh --section` instead.
- `calc()` percentages on table columns are ignored. Use plain percentages (the builder does).
- Duplicate ids across many inline SVGs break `url(#marker)`. Prefix every id with the topic key.
- Research agents that run servers must use their own temp dir and port and stop and delete them. Check for leftovers at the end.
- The page for 20 topics is about 800 KB. That is fine (limit is 16 MB).
