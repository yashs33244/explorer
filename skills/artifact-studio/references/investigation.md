# Investigation and RCA pages

Use this shape for an RCA, a "why does X not show up" investigation, or a "how does this system work" explainer
that ends in a decision. The reader is an engineer who is new to the system: they read diagrams and short points,
not paragraphs. `examples/rca/` is a working page in this shape.

## Section order

| # | Section | What it holds | Form |
|---|---|---|---|
| top | Header, `div.problem`, `.tldr` | Problem box: who, what they see, when (real date), why. TL;DR: what the thing is, where it lives, the one-line fix | 4 to 5 bullets each |
| 01 | What was reported | The report quoted word for word (who, date, channel), then three cards: **Problem in one line**, **Solution in one line**, **Not the cause** (the tempting wrong answer, ruled out with evidence) | `.callout.warn` quote + `.cards` |
| 02 | What X is, from first principles | Start from the need ("every call costs money, so each needs one durable record"), then a Q&A table that answers the questions a newcomer asks | bullets + table |
| 03 | The big picture | Every store and every path, and which one the broken screen reads. Mark what never happens with a dashed red arrow | hand-drawn figure |
| 04 | Who writes it | The write path hop by hop: a numbered box per hop listing the exact fields, plus a payload card per hop below the figure | hand-drawn figure + `pre.http` cards |
| 05 | The data | The table as a schema card, the columns that decide the bug highlighted, and a case table (which input lands as which row) | `er-diagram` + table |
| 06 | Who reads it | Every reader, its route, who may call it, and the reader that is missing | hand-drawn figure + table |
| 07 | Options and choice | Each option with Before, After, Pros, Cons, Choice; the chosen ones marked | table |
| 08 | What others proposed | A teammate's proposal quoted, whether it matches the evidence, its caveat analysed with risks and conditions | `.callout.ok` + before/after pair + bullets |
| 09 | What we tested | Each check, its result and how it was run; the part not built yet in a `tr.bad` row | table |
| 10 | Code to read, in order | The files a newcomer should read, why, and where each runs | table |
| 11 | Failure modes | Failure, effect, guard; then a **Not verified** line | table |

Drop a section that does not apply; never reorder the first three.

## Tables, column by column

- **Q&A (02):** Question | **Answer** (`th.key`) | Where it is defined (`file:line`). Rows: Is it a table? Which DB? Which repo owns it?
  Who writes it? Who sends it data? Who reads it? Retention? Volume (a `.metric`).
- **Case table (05):** Input or key used | the deciding columns | **the column that decides** (`th.key`) | Whose it looks like. The
  case that causes the bug is `tr.bad`.
- **Options (07):** Option | Before | After | Pros | Cons | **Choice** (`th.key`, a `.pill`: ok = do now, next = later, todo = hold).
  The chosen row is `tr.key`. Follow with one `<mark>` sentence naming the choice.
- **Tested (09):** Check | **Result** (`th.key`) | How (script path, test name, command). Never claim a check that was not run.
- **Code to read (10):** # | **File** (`th.key`) | Why | Runtime (pod, browser, database, doc). Mark the files the fix touches `tr.key`.
- **Failure modes (11):** Failure | Effect | **Guard** (`th.key`).

## Figures

- Flow, request and architecture figures are hand-drawn (`scripts/handdrawn.py`, SKILL.md "Hand-drawn diagrams").
- Number the boxes in the order a request moves; the number also starts the box title (`2  check the token`).
- Each box lists real fields in mono: method and path, headers with the deciding one in orange, body keys, reply.
- Red mono notes beside arrows carry the request line and collapsed bodies (`req { .. }`, `res { items: [] }`).
- Stores are ellipses named by engine and table: `DB (postgres)\npayments.receipts`.
- Pods and processes are dashed zones labelled with the runtime (`your app process`, `api pod`, `worker pod`).
- A before/after pair uses the same grid; only the new parts change colour (green), and the caption says so.

## Wording

- Problem first in every section; the solution follows.
- One `<mark>` per section, on the sentence a skimmer must not miss.
- Short plain sentences, bullets under about 12 words, no em dash, no names unless the user asks.
- Quote people exactly; label made-up ids and values "illustrative values".
- End with what is not verified and the exact check that would settle it.
