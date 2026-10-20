# 1. One kit, one catalog

Status: accepted (2026-10)

Every skill in this repo draws with the CSS classes of `skills/codebase-explorer` and renders with its `render.sh`, and every figure type must exist in `diagram-types/catalog.json`.

Why: pages from different skills should read as if one person drew them, and a figure type that is not in the catalog has no example, no anatomy and no render to copy from.

Cost: the kit CSS lives in two places (the page template and the renderer's `style.css`), and they must change together. Nothing checks that yet.
