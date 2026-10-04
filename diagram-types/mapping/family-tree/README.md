# Family tree

A family tree lays out lineage left to right, one column per generation, with elbow connectors from each parent to its children. The example traces PostgreSQL from Berkeley Postgres (1986) through the 1996 open source release to its forks and rewrites (Netezza, Greenplum, ParAccel, Citus, Aurora, Neon) and their descendants (Cloudberry, Redshift, Cosmos DB for PostgreSQL, Databricks Lakebase), colored by kind of fork.

| Hand-drawn | Clean |
|---|---|
| ![hand-drawn](hand.jpg) | ![clean](clean.jpg) |

## Use it to explain

- The lineage of a codebase, protocol or library and which products descend from it.
- How internal services were split out of a monolith over successive rewrites.
- Fork history of a dependency, so a team knows which upstream a vendored copy tracks.
- Not for: who calls whom at runtime (use a dependency graph) or reporting lines (use an org chart).

## Anatomy

| Part | Class | Rule |
|---|---|---|
| Origin | `d-box g0` (diamond path) | One root at the left, the only diamond. |
| Generation header | `d-k` | One kicker per column, naming the generation. |
| Member | `d-box g1`..`g3` + `d-logo` | Name and "year, what changed"; color by kind of fork. |
| Lineage | `d-edge` | Elbow connectors from a shared trunk; solid means code was forked. |
| Hand-off | `d-edge dash` + `d-lab` | Dashed arrow with a verb for licensing or acquisition. |
| Group frame | `d-blob` | One dashed frame behind the whole tree, like the template's panel. |

## Tips

- Sort children within a column by year so the vertical order is also a timeline.
- Use solid lines for code descent and dashed for ownership changes; say so in the legend.
- Keep one generation per column even when a branch has no children yet.

Reference: Figma template Family Tree

Source: [example.svg](example.svg)
