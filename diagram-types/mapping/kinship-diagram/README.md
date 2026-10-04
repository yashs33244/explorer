# Kinship diagram

A kinship diagram borrows anthropology's family notation (shapes for kinds of member, `=` for a union, a sibship bar for children) and applies it to software lineage. Here it traces the Node.js runtime: Node.js 0.12 and the io.js fork merge, and the merged line has three kinds of child: Node.js 4 (whose own children are later LTS lines and an archived fork), a patched fork inside Electron and a vendored copy in NW.js. Shape tells you what kind of relative a codebase is, so you can see at a glance who still ships upstream fixes and who has to backport them.

| Hand-drawn | Clean |
|---|---|
| ![hand-drawn](hand.jpg) | ![clean](clean.jpg) |

## Use it to explain

- Which forks and vendored copies of a library exist, and which ones need a CVE patch backported by hand.
- How a split community (a fork) later merged back into one release line.
- Where a dependency in your monorepo actually comes from: upstream, a downstream fork, or a frozen vendored copy.

Not for: version-by-version release timelines (use a gantt or timeline) or runtime call relationships (use a dependency graph).

## Anatomy

| Part | Class | Rule |
|---|---|---|
| Maintained line | `d-box g1` circle | the upstream release line, logo in the centre |
| Hard fork | `d-box g4` polygon | a triangle; it ships its own releases |
| Vendored copy | `d-box g2` rect | a square; code copied into another repo |
| Union | `d-edge thick` | an `=` sign between two parents, descent line drops from it |
| Sibship bar | `d-edge thick` | one horizontal bar per set of children, rounded corners |
| Archived | `d-edge thick` | a diagonal slash through the shape |
| Name and status | `d-t`, `d-s`, `d-m` | name on top, one-line status below; `d-m` for a path |
| Legend | `d-blob2` | always explain the shape code |

## Tips

- Keep one generation per row; put labels beside shapes in rows that have children so descent lines never cross text.
- Use a real date on the union line ("merged Sep 2015"); it is the event readers ask about.
- A slash is cheaper than a colour for "dead": it survives greyscale and both themes.

Reference: Figma template Kinship diagram

Source: [example.svg](example.svg)
