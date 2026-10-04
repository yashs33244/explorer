# Website flowchart (sitemap)

A tree of a site's pages, root at the top, top-level sections in one row and their child pages stacked below, each card showing the page title and its URL path. Top-level cards list the sections on that page, and dashed cards mark external links and redirects. The example is the Relay API docs site: Home links to Get started, Guides, API reference, SDKs and Changelog, each with its child pages (`/api/payments`, `/sdks/python`, `/changelog.rss`), GitHub and the status page as external links, and old v2 docs redirecting with a 301.

| Hand-drawn | Clean |
|---|---|
| ![hand-drawn](hand.jpg) | ![clean](clean.jpg) |

## Use it to explain

- The URL structure of a docs site or web app, and which routes a router or static site generator must serve.
- Where a new page belongs and which redirects a restructure needs.
- Which pages pull in external systems (status page, GitHub) that can break the site.

Not for: the layout inside one page (use `wireframe`) or a user's path through screens (use `ux-workflow`).

## Anatomy

| Part | Class | Rule |
|---|---|---|
| Root page | `d-box g3` | Top centre, with its main sections as rows |
| Section page | `d-box g0`..`g5` | One colour per branch, title in `d-t`, path in `d-m` |
| Page section | `d-fillpaper` + `d-s` | Two or three rows inside a top-level card |
| Child page | `d-box` same `g` | Indented under its parent, stacked, path in `d-m` |
| External or redirect | `d-blob2` | Dashed card; a redirect states its status code |
| Link | `d-edge` | Bus from the root, then a trunk with stubs for children |
| Legend | small shapes + `d-s` | One row at the bottom |

## Tips

- Show the real path on every card; the paths are what engineers review.
- Keep one colour per branch so children read as belonging to their section.
- Cap a branch at five children; collapse the rest into one "and 12 more" card.

Reference: Figma template Website flowchart

Source: [example.svg](example.svg)
