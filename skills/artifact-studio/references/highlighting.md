# Highlighting: make the point findable

A reader skims first. Every page tells a skimmer, in under ten seconds, what the answer is and where the evidence sits. Highlighting is how: a few marks, each meaning one thing, never decoration.

## The marks

| Mark | Markup | Use it for | Budget |
|---|---|---|---|
| The sentence that matters | `<mark>...</mark>` | The conclusion of a section, the one fact that changes a decision | 1 per section |
| Key term | `<b class="k">term</b>` | A name the reader must carry into later sections (first use only) | 3 to 5 per section |
| A number that matters | `<span class="metric">412 ms</span>` | The figure the argument rests on: a latency, a count, a cost | 1 to 3 per section |
| Callout | `<div class="callout warn">` (`ok`, `risk`, or plain) with `<span class="lbl">Risk</span>` | A warning, a constraint, a decision, an open question | 1 per section |
| Status | `<span class="pill ok|next|todo|ill">` | Done, next, to build, illustrative | per row |
| Bold | `<strong>` | Plain emphasis inside a sentence | sparing |

Rules:

- **One meaning per mark.** Yellow means "the point". Accent means "a name to remember". Do not use a mark to make text look busy.
- **Highlight the answer, not the topic.** "Postgres" is a topic; "<mark>writes block for up to 2 s during the vacuum</mark>" is an answer.
- **If everything is highlighted, nothing is.** Above budget, delete marks until the page reads like a page again.
- Never rely on colour alone: a marked row also carries a word (a status pill, "chosen", "blocked") so it survives printing and colour blindness.

## Tables

Most pages hold their evidence in tables, so tables carry the strongest highlights.

| What | Markup | Effect |
|---|---|---|
| The column that answers the question | `<th class="key">` | The whole column is tinted and its header gets an accent rule (the script copies the class to every cell) |
| The rows that matter (chosen option, the failing case, the hot path) | `<tr class="key">` | Yellow row with a left bar; also gets the "Highlighted rows only" toggle |
| Good and bad rows | `<tr class="good">`, `<tr class="bad">` | Green or red tint with a left bar; pair with a word or pill |
| Rows that do not apply | `<tr class="dim">` | Muted text |
| Numbers | `<th class="num">` | Right aligned, tabular figures, numeric sort |
| A filter dropdown for a column | `<th data-filter>` | Adds a select with the column's distinct values |
| A column that should not sort | `<th data-nosort>` | No sort on click |

Every table with four or more columns marks **one** key column or at least one key row. `build.py` warns when it does not.

### Filters and sorting

Every table with 6 or more body rows gets tools automatically, with no extra markup:

- a filter box that matches any cell text, with a live "N of M rows" count,
- click-to-sort on every header (numbers sort as numbers, keyboard works: Tab then Enter),
- one select per `th[data-filter]` column,
- a "Highlighted rows only" toggle when any row is `tr.key`.

Use `<div class="tablewrap" data-filter="on">` to force the tools on a short table, `data-filter="off"` to remove them (for a 6-row comparison you want read top to bottom). Long tables also take `class="tablewrap tall"` for a sticky header.

Put the table's rows in the order the reader should read them; sorting is for the reader, not a substitute for a good default order. Mark `data-filter` on columns with a few repeating values (status, owner, layer, kind), never on free text.

## Figures

- Accent (`acc`) on 1 or 2 elements: the path or part the caption talks about.
- The caption's first sentence states what to see: "The only path that crosses the trust boundary is the webhook." Bold (`<b>`) the part name in the caption when it names one.
- Numbered badges point at the 3 to 6 places the walkthrough explains; on engineering pages each badge gets a detailed row (see `engineering.md`).

## Example

```html
<p>The worker retries forever. <mark>A poisoned job blocks its whole queue until someone deletes it by hand.</mark>
The fix adds a <b class="k">dead-letter queue</b> after <span class="metric">5 attempts</span>.</p>

<div class="tablewrap"><table>
  <thead><tr><th>Option</th><th class="key">Blocks the queue?</th><th data-filter>Effort</th><th>Notes</th></tr></thead>
  <tbody>
    <tr><td>Retry forever (today)</td><td>Yes</td><td>None</td><td>Current behaviour</td></tr>
    <tr class="key"><td>Dead-letter after 5</td><td>No</td><td>Small</td><td><span class="pill ok">Chosen</span></td></tr>
  </tbody>
</table></div>
```
