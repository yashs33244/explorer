# 4. Modern is the default diagram style

Status: accepted (2026-11)

Diagrams now open in a third style, `modern`, modelled on the architecture diagrams that Cloudflare and Figma publish on their engineering blogs: a dotted canvas, white cards with a coloured outline and a stacked-card offset, monospace uppercase names, tinted group zones and small chip labels on edges. `clean` and `hand` stay available through the page switch, `diagramStyle` and `build.py --style`.

Why: engineers onboarding to a system read these product diagrams every day, so the look signals "real architecture" rather than a whiteboard sketch or a template. The style is pure CSS over the existing kit classes, so every catalog type and every existing page changed without touching an SVG.

Cost: monospace uppercase titles run about 10 percent wider than the sans the other styles use. New diagrams size box titles for it, and `scripts/check-overflow.py` measures every catalog example; the modern style adds no overflow beyond the clean style's known intentional cases. The page template carries a generated, light-only copy of the modern rules (`scripts/sync-modern.py`), which `check.sh` keeps in step with `style.css`.
