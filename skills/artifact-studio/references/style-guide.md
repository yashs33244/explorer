# Style guide: the one theme

The single source of truth is the `:root` block of `assets/page-template.html`. The diagram tokens (`--cl-*`, `--clN-f`, `--clN-t`, `--clN-x`) are mirrored in the clean block of `../codebase-explorer/assets/style.css`, which `render.sh` uses: change a diagram token in both files or in neither. The page-only tokens (`--acc-ink`, `--mark`, status colours) live only in the template. Diagrams never carry hex colours; they use kit classes, and the classes resolve to these tokens.

## Tokens

| Role | Token | Value | Used for |
|---|---|---|---|
| Page | `--bg`, `--paper` | `#ffffff` | Page and card background (light only) |
| Ink | `--ink` | `#1e1e1e` | Text, outlines |
| Muted | `--muted` | `#5c5c5c` | Secondary text, sublabels |
| Rules | `--line`, `--faint` | `#e6e6e6`, `#e2e2e2` | Borders, grid |
| Accent | `--acc`, `--acc-soft` | `#1f7aec`, `#e8f1fe` | Links, rules and outlines, the 1 or 2 focal parts of a figure |
| Accent text | `--acc-ink` | `#1660c9` | Key terms, `.metric`, key column header, section numbers (4.5:1 or better on white and on `--acc-soft`) |
| Marker | `--mark` | `#fff1b8` | The highlighted sentence, key rows |
| Status | `--ok`, `--warn`, `--todo` (+ `-soft`) | green, amber, red | Pills, callouts, good and bad rows |
| Group fills | `--cl0-f` .. `--cl5-f` | purple, green, yellow, coral, blue, orange | Kit boxes (`d-box gN`) |
| Group tints | `--cl0-t` .. `--cl5-t` | light versions | Bands and containers (`d-band gN`, `d-zone gN`) |
| Group ink | `--cl0-x` .. `--cl5-x` | dark versions, 4.5:1 on white | Container titles, paths and coloured edges in repo maps |

Fonts: Bricolage Grotesque for headings (`h1`, `h2`, `d-h`, `d-zt`), Figtree for text, JetBrains Mono for code, paths, chips and kickers only.

## Figure sizes

| Size | figs.json | Width on a 1440px screen | Use for |
|---|---|---|---|
| inline (default) | nothing | up to 1180px, height capped at 88vh | most figures (viewBox 800 wide) |
| wide | `"size": "wide"` | the full text column | timelines, long flows, short and wide figures |
| bleed | `"size": "bleed"` | nearly the whole window (12px gutters) | repo maps, dense architecture (viewBox 1200 to 1400 wide); default for `repo-map` |

The page column is `min(1480px, 100% - 40px)`: small side margins so tables and figures get the room, prose capped at 75ch. In site mode a bleed figure stays inside the page column so it never covers the "On this page" list.

Every SVG keeps at least 32 units of clear margin inside its viewBox, text at 12px or more in viewBox units, and draws with kit classes only (no hex, no `style` or `script` tags).
