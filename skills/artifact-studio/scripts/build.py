#!/usr/bin/env python3
"""Assemble an artifact page from body.html, SVG diagrams and figs.json.

  build.py --title "Page Name" --body body.html --svg svg/ --figs figs.json --out page.html

body.html is plain HTML for the page content. Put {{fig:KEY}} where a diagram goes;
KEY matches svg/KEY.svg and an entry in figs.json:

  {"d1": {"type": "Layered architecture", "title": "Where the fields flow",
          "caption": "One or two sentences.",
          "badges": ["step one", "step two"],          # numbered legend (optional)
          "legend": [["--cl1-f", "label"]]}}            # colour chips (optional)

The page template (light theme, clean diagram classes, wide tables, centred diagrams,
Full screen overlay) lives in ../assets/page-template.html.
"""
import argparse, html, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, '..', 'assets', 'page-template.html')
DASHES = re.compile('[\\u2014\\u2013]')


def figure(key, spec, svg_dir):
    svg = open(os.path.join(svg_dir, f'{key}.svg')).read()
    svg = svg.replace(' xmlns="http://www.w3.org/2000/svg"', '', 1)
    title = html.escape(spec['title'])
    extra = ''
    if spec.get('badges'):
        extra += '<ol class="badges">' + ''.join(
            f'<li><b>{i + 1}</b><span>{html.escape(s)}</span></li>' for i, s in enumerate(spec['badges'])) + '</ol>'
    if spec.get('legend'):
        extra += '<div class="legend">' + ''.join(
            f'<span><i style="background:var({c})"></i>{html.escape(l)}</span>' for c, l in spec['legend']) + '</div>'
    return (f'<figure class="fig" data-title="{title}"><div class="figbar">'
            f'<span class="ftype">{html.escape(spec.get("type", ""))}</span>'
            f'<button class="fzoom" type="button" aria-label="Open {title} full screen">Full screen</button></div>'
            f'<div class="figscroll">{svg}</div><figcaption>{html.escape(spec.get("caption", ""))}</figcaption>{extra}</figure>')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--title', required=True)
    ap.add_argument('--body', required=True)
    ap.add_argument('--svg', default='svg')
    ap.add_argument('--figs', default=None)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()

    body = open(a.body).read()
    figs = json.load(open(a.figs)) if a.figs else {}
    for key, spec in figs.items():
        mark = '{{fig:' + key + '}}'
        if mark not in body:
            sys.exit(f'body has no {mark}')
        body = body.replace(mark, figure(key, spec, a.svg))
    left = re.findall(r'\{\{fig:[^}]+\}\}', body)
    if left:
        sys.exit(f'no figs.json entry for {left}')

    page = open(TEMPLATE).read().replace('{{TITLE}}', html.escape(a.title)).replace('{{BODY}}', body)
    page = DASHES.sub('-', page)
    open(a.out, 'w').write(page)
    print(f'{a.out}: {len(page)} bytes, {len(figs)} diagrams')


if __name__ == '__main__':
    main()
