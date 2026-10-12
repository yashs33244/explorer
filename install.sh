#!/bin/bash
# Symlink the skills into Claude Code's skills folder so every project can use them.
# Set CLAUDE_SKILLS_DIR to install somewhere else (another agent's skills folder).
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
DEST="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
mkdir -p "$DEST"
for SKILL in codebase-explorer artifact-studio artifact-studio-explainer; do
  [ -f "$HERE/skills/$SKILL/SKILL.md" ] || continue
  ln -sfn "$HERE/skills/$SKILL" "$DEST/$SKILL"
  echo "installed: $DEST/$SKILL -> $HERE/skills/$SKILL"
done
