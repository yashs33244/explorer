#!/bin/bash
# Symlink the skill into Claude Code's skills folder so every project can use it.
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
DEST="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
mkdir -p "$DEST"
ln -sfn "$HERE/skills/codebase-explorer" "$DEST/codebase-explorer"
echo "installed: $DEST/codebase-explorer -> $HERE/skills/codebase-explorer"
