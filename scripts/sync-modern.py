#!/usr/bin/env python3
"""Copy the modern diagram style from codebase-explorer's style.css into artifact-studio's page template.

The template is light only, so the dark-theme token blocks are dropped. Run after editing the modern block;
`--check` (used by scripts/check.sh) exits 1 when the template copy is out of date.
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSS = ROOT / 'skills/codebase-explorer/assets/style.css'
TPL = ROOT / 'skills/artifact-studio/assets/page-template.html'
BEGIN, END = '/* modern-style:begin */', '/* modern-style:end */'


def light_block():
    s = CSS.read_text()
    block = s[s.index(BEGIN):s.index(END) + len(END)]
    block = re.sub(r'@media \(prefers-color-scheme: dark\) \{\n.*?\n  \}\n\}\n', '', block, flags=re.S)
    block = re.sub(r':root\[data-theme="dark"\]\[data-dstyle="modern"\].*?\n\}\n', '', block, flags=re.S)
    return block.replace(BEGIN, BEGIN + '\n/* generated from codebase-explorer/assets/style.css by scripts/sync-modern.py, light only; do not edit here */', 1)


def main():
    t = TPL.read_text()
    new = light_block()
    if BEGIN in t:
        out = t[:t.index(BEGIN)] + new + t[t.index(END) + len(END):]
    else:
        out = t.replace('</style>', new + '\n</style>', 1)
    if '--check' in sys.argv:
        if out != t:
            sys.exit('page-template.html modern block is stale: run scripts/sync-modern.py')
        return
    TPL.write_text(out)
    print('synced modern style into', TPL.relative_to(ROOT))


if __name__ == '__main__':
    main()
