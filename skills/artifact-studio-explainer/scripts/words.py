#!/usr/bin/env python3
"""Print each scene's narration with 0-based word indexes, for at_word."""
import json
import sys

if len(sys.argv) != 2:
    sys.exit("usage: words.py storyboard.json")
board = json.load(open(sys.argv[1]))
for scene in board["scenes"]:
    words = scene.get("narration", "").split()
    print(f"\n[{scene['id']}] {scene.get('type')}  ({len(words)} words)")
    print("  " + " ".join(f"{i}:{w}" for i, w in enumerate(words)))
