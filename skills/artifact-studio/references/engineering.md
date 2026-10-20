# Engineering pages: explain it so a reviewer can act

Use this when the page is about software: a design doc, an implementation plan, a repo or system architecture, a migration, an incident, a performance investigation, a code review. An engineering reader wants to know **what exists, how it runs, where it lives in the code, what breaks, and how we know it works**. A pretty overview without file paths is not enough.

Build with `--kind engineering` (or `"kind": "engineering"` on a site page) so `build.py` checks the depth below.

## The sections

Pick the sections that apply, in this order. A design doc or architecture page usually needs all of the first six.

| # | Section | Answers | Figure (see `choosing-diagrams.md`) | Table |
|---|---|---|---|---|
| 1 | Answer first | What is this, what is the decision or conclusion, in 3 sentences | none, a `.tldr` with one `<mark>` | none |
| 2 | Context and constraints | Why now, what must stay true, what is out of scope | none or `system-context` | constraints and non-goals |
| 3 | Parts and boundaries | What are the parts, who may depend on whom | `repo-map` for a repo, `layered-architecture` or `boundary-architecture` for a system, `architecture-delta` for a change | **components table**: part, path in `<code>`, owns, depends on, entry point |
| 4 | How one request or job runs | The hot path, step by step | `sequence-diagram` or `request-lifecycle`, numbered badges | step table: step, file and function in `<code>`, what it reads and writes |
| 5 | Data | What is stored, its shape and its states | `er-diagram`, `state-machine` | fields: name, type, source, used by |
| 6 | Failure modes | What can go wrong and what happens then | `flowchart` (branches), `state-machine` (retries), `fishbone` (incident causes) | **failure table**: failure, detection, effect, mitigation, status |
| 7 | Change plan | What changes, in which order, how it rolls back | `architecture-delta`, `dependency-graph`, `horizontal-timeline` | steps with exit criteria |
| 8 | Verification | How we know it works: tests, checks, metrics, commands | `line-chart` for a metric that moved | checks: what, command in `<code>`, result, status |
| 9 | Open questions | What is not decided yet, who decides | none | question, options, needed by |

## Depth rules

- **Every part has an address.** A component named in a figure appears in a table with its real path (`skills/artifact-studio/scripts/build.py`), and its entry point (function, command, binary).
- **Every figure is explained in detail.** Use detailed badges in `figs.json` so each numbered spot gets a row under the figure with what happens there and where:

  ```json
  "badges": [{"t": "Build", "d": "build.py swaps each {{fig:KEY}} for the figure and checks its type against the catalog.", "file": "scripts/build.py"},
             {"t": "Lint", "d": "Warnings for missing highlights, a missing why, and one-type pages."}]
  ```

- **Walk the hot path in order.** After the sequence figure, a numbered list or step table explains each step in one to three sentences: the function, the input, the output, the side effect.
- **Name the contracts.** For each boundary in the parts figure, say what crosses it (a file format, an HTTP route, a CLI flag, a JSON schema) and who validates it.
- **State the invariants.** The rules that must never break ("core never imports apps", "every diagram has a viewBox") go in a `.callout` with a label, and say what enforces each one (a lint, a test, a review, nothing yet).
- **Failure modes are concrete.** "Network error" is not a failure mode; "Chrome is missing, so render.sh exits 1 and the build has no screenshots" is.
- **Numbers carry units and a source.** "p95 412 ms (Grafana, 2026-10-20)", or mark them `est.` / `illustrative`.
- **Commands are copyable.** Every command in `<pre><code>` runs from a stated directory.
- **Honest status.** Use pills for done, next, to build and illustrative; write "not verified" for anything you did not run.

## Repo architecture pages

When the subject is a repository (how it is cut, what depends on what), lead with a `repo-map` figure at `"size": "bleed"`, drawn with `scripts/repo_map.py` (see `diagram-types/technical/repo-map/README.md`; give edges `from` and `to` so hover focus works), then:

1. a components table (one row per container: path, what it holds, depends on, entry point, key column = "depends on"),
2. the layer rules in a callout, with what enforces them,
3. the build or request path as a `sequence-diagram` or `flowchart`,
4. a "where to change what" table (I want to... / edit this file / then run), key column = "edit this file",
5. external dependencies and runtime services in a table.

## More detail than a kit diagram can hold

When the user asks for a more detailed, isometric or 3D view of a mechanism (how the cache decides, how the limiter fills), add one anatomy figure for it (`detailed-figures.md`) and keep the structure in kit diagrams.

## Explainer video for an engineering page

When the page also gets a video, use the Manim engine of the `artifact-studio-explainer` skill if you have it installed (it is local and not part of this repo) for scenes that move (repo map build-up, request path, highlighted table build). The page and the video share the same figures, wording and highlights; the video narrates the badges in order.
