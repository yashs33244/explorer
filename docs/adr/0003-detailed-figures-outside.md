# 3. Detailed and isometric figures come from anatomy, not the kit

Status: accepted (2026-10)

When a reader needs to feel a mechanism, or the user asks for an isometric, 3D or highly detailed figure, the page embeds a figure built with the anatomy skill (github.com/wheresryan22/anatomy, MIT) instead of stretching the flat kit. The anatomy skill is installed beside these skills, never copied into this repo.

Why: anatomy already solves solid parts, painter's order, motion and audits. Rebuilding that in the kit would double the work and drift from upstream.

Cost: an embedded anatomy page adds about 130 KB or more, so a page uses at most one or two.
