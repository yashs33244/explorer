# Topic file and config schema

## `topics/<key>.json`

```json
{
  "key": "wal",
  "title": "WAL, checkpoints and recovery",
  "short": "WAL",
  "one_liner": "max 25 words, plain",
  "analogy": "an everyday comparison, max 30 words",
  "big_picture": ["4 to 6 bullets, each max 22 words"],
  "flow": [{ "step": "Name", "detail": "what happens", "where": "path/to/file.c: function_name" }],
  "diagram": { "claim": "one sentence", "nodes": [{ "id": "a", "label": "max 3 words", "group": "lane" }], "edges": [{ "from": "a", "to": "b", "label": "verb" }] },
  "key_files": [{ "path": "real/path", "what": "max 14 words" }],
  "interview": [{ "q": "question", "answer": ["2 to 5 short bullets"], "trap": "optional common wrong answer" }],
  "contributor_tips": ["where a beginner could start"],
  "glossary": [{ "term": "x", "meaning": "max 15 words" }],
  "more": ["extra follow-up questions or facts, optional"],
  "try_it": [{ "cmd": "a real command", "shows": "what you will see" }],
  "file_tree": [{ "path": "a/real/path", "what": "meaning" }]
}
```

Only `title`, `one_liner`, `big_picture` are required by the builder. Missing sections are skipped. If a topic has no hand-drawn diagrams the builder draws an automatic top-to-bottom diagram from `diagram.nodes` and `diagram.edges`.

## `diagrams/<key>/meta.json`

```json
[{ "file": "d1.svg", "role": "architecture", "title": "short heading", "caption": "one plain sentence",
   "badges": [{ "n": 1, "meaning": "what step 1 is" }] }]
```

Roles: `architecture`, `lifecycle`, `structure`.

## `explorer.config.json`

| Field | Meaning |
|---|---|
| `title`, `brandSub`, `storageKey` | name shown in the rail, subtitle, localStorage key for the "Got it" ticks |
| `kicker`, `heroTitle`, `heroLede` | the hero text |
| `how` | three small cards `[{title, text}]` |
| `overviewKey` | topic key whose diagrams open the page |
| `lifecycle` | `{title, steps:[{name, text, topic}]}`, a true sequence linking to topics |
| `callouts` | `[{style: "soft" or "more", title, items:[{bold, text}]}]` |
| `groups` | `[{name, topics:[keys]}]`, defines nav order and part numbers |
| `navLabels` | optional short names per key |
| `tryItNote` | caption under every try-it table |
| `extraSections` | `[{id, navLabel, kicker, title, lede, table:{file, columns, tallAfter, caption}, htmlFile}]` |
| `footer` | closing sentence |

Table columns: `{key, label, kind}` where kind is `text` (default), `num`, `pill`, `code`, `link`, `muted` or `nowrap`. Rows are an array of objects in the JSON file.
