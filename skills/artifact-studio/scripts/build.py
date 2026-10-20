#!/usr/bin/env python3
"""Assemble artifact pages from body HTML, SVG diagrams and figs.json.

One page:

  build.py --title "Page Name" --body body.html --svg svg/ --figs figs.json --out page.html

A site (an index page plus one page per topic, all in one folder):

  build.py --site site.json --out site/

body.html is plain HTML for the page content. Put {{fig:KEY}} where a diagram goes;
KEY matches svg/KEY.svg and an entry in figs.json:

  {"d1": {"type": "layered-architecture",                # catalog slug or catalog name
          "why": "What runs where?",                     # the reader question it answers
          "title": "Where the fields flow",
          "caption": "One or two sentences.",
          "badges": ["step one", "step two"],          # numbered legend (optional)
          "legend": [["--cl1-f", "label"]]}}            # colour chips (optional)

"type" must be a type in the explorer repo's diagram-types/catalog.json; see
../references/choosing-diagrams.md for which type answers which question.

site.json (paths are relative to the site.json folder):

  {"title": "Site title",                 # top nav and index h1
   "kicker": "roadmap",                   # optional, index kicker
   "lede": "One paragraph for the index.",
   "note": "Status line.",                # optional, index note
   "intro": "intro.html",                 # optional HTML between the lede and the page cards ({{fig:KEY}} allowed)
   "intro_figs": "intro.figs.json",       # optional, figs for intro
   "svg": "svg",                          # default SVG folder for every page
   "pages": [
     {"slug": "overview",                 # writes overview.html (a-z, 0-9, -)
      "title": "Overview",                # nav label and page h1
      "summary": "One line for the card.",  # optional; defaults to the body's p.lede
      "group": "Decide",                  # optional; consecutive pages with one group share a heading on the index
      "body": "overview.html",
      "figs": "overview.figs.json",       # optional
      "svg": "svg"}]}                     # optional, overrides the site default

Every page gets the same top nav (current page marked), an "On this page" list built
from its <section id> and h2 (sticky on the left on wide screens), and Previous / Next
links. A page body without an h1 gets a generated header. After writing, every href in
every file is checked: the target file must exist in the folder and #ids must exist.

The page template (light theme, clean diagram classes, wide tables, centred diagrams,
Full screen overlay, site nav) lives in ../assets/page-template.html.
"""
import argparse, difflib, html, json, os, re, sys

HERE = os.path.dirname(os.path.realpath(__file__))
TEMPLATE = os.path.join(HERE, '..', 'assets', 'page-template.html')
CATALOG = os.path.join(HERE, '..', '..', '..', 'diagram-types', 'catalog.json')
DASHES = re.compile('[\\u2014\\u2013]')
SLUG = re.compile(r'^[a-z0-9][a-z0-9-]*$')
TAGS = re.compile(r'<[^>]+>')


def load_types():
    """Map every catalog slug and lower-cased catalog name to its display name."""
    types = {}
    for t in json.load(open(CATALOG)):
        types[t['slug']] = t['name']
        types[t['name'].lower()] = t['name']
    return types


def check_types(figs, types):
    for key, spec in figs.items():
        given = spec.get('type', '')
        name = types.get(given) or types.get(given.lower())
        if not name:
            near = difflib.get_close_matches(given.lower(), types.keys(), n=3, cutoff=0.4)
            sys.exit(f'{key}: unknown diagram type "{given}"; use a slug from '
                     'codebase-explorer/references/diagram-types.md' + (f' (closest: {", ".join(near)})' if near else ''))
        spec['type'] = name
        if not spec.get('why'):
            print(f'warning: {key} has no "why" (the reader question it answers)', file=sys.stderr)
    if len(figs) >= 3 and len({s['type'] for s in figs.values()}) == 1:
        print(f'warning: all {len(figs)} diagrams are "{next(iter(figs.values()))["type"]}"; '
              'pick one type per reader question (references/choosing-diagrams.md)', file=sys.stderr)


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
    wide = ' wide' if spec.get('wide') else ''  # wide figures (timelines, long flows) fill the content width
    return (f'<figure class="fig{wide}" data-title="{title}"><div class="figbar">'
            f'<span class="ftype">{html.escape(spec.get("type", ""))}</span>'
            f'<button class="fzoom" type="button" aria-label="Open {title} full screen">Full screen</button></div>'
            f'<div class="figscroll">{svg}</div><figcaption>{html.escape(spec.get("caption", ""))}</figcaption>{extra}</figure>')


def fill_figs(body, figs, svg_dir, types):
    """Check figure types, then swap every {{fig:KEY}} for its figure."""
    check_types(figs, types)
    for key, spec in figs.items():
        mark = '{{fig:' + key + '}}'
        if mark not in body:
            sys.exit(f'body has no {mark}')
        body = body.replace(mark, figure(key, spec, svg_dir))
    left = re.findall(r'\{\{fig:[^}]+\}\}', body)
    if left:
        sys.exit(f'no figs.json entry for {left}')
    return body


def page_html(title, body, nav=''):
    page = open(TEMPLATE).read().replace('{{TITLE}}', html.escape(title)).replace('{{NAV}}', nav).replace('{{BODY}}', body)
    return DASHES.sub('-', page)


def build_single(a):
    if not a.title or not a.body:
        sys.exit('single page mode needs --title and --body (or use --site site.json)')
    body = open(a.body).read()
    figs = json.load(open(a.figs)) if a.figs else {}
    page = page_html(a.title, fill_figs(body, figs, a.svg, load_types()))
    open(a.out, 'w').write(page)
    print(f'{a.out}: {len(page)} bytes, {len(figs)} diagrams')


# ---- site mode ---------------------------------------------------------------

def text(fragment):
    return html.unescape(TAGS.sub('', fragment)).strip()


def sections(body):
    """(id, number, h2 text) for every <section id> that has an h2."""
    out = []
    for m in re.finditer(r'<section\b[^>]*\bid="([^"]+)"[^>]*>(.*?)</section>', body, re.S):
        h2 = re.search(r'<h2\b[^>]*>(.*?)</h2>', m.group(2), re.S)
        if not h2:
            continue
        num = re.search(r'<p class="num">(.*?)</p>', m.group(2)[:h2.start()], re.S)
        out.append((m.group(1), text(num.group(1)) if num else '', text(h2.group(1))))
    return out


def lede(body):
    m = re.search(r'<p class="lede">(.*?)</p>', body, re.S)
    return text(m.group(1)) if m else ''


def site_nav(site_title, pages, current):
    mark = lambda slug: ' aria-current="page"' if slug == current else ''
    items = ''.join(f'<li><a href="{p["slug"]}.html"{mark(p["slug"])}>{html.escape(p["title"])}</a></li>' for p in pages)
    return (f'<nav class="sitenav" aria-label="Pages"><div class="sitenav-in">'
            f'<a class="sitehome" href="index.html"{mark("index")}>{html.escape(site_title)}</a><ol>{items}</ol></div></nav>\n')


def page_toc(secs):
    if not secs:
        return ''
    items = ''.join(f'<li><a href="#{html.escape(i)}">' + (f'<span>{html.escape(n)}</span>' if n else '') +
                    f'{html.escape(t)}</a></li>' for i, n, t in secs)
    return f'<aside class="pagetoc"><nav aria-label="On this page"><p class="kicker">On this page</p><ol>{items}</ol></nav></aside>'


def prev_next(pages, i):
    prev = ('index.html', 'Contents') if i == 0 else (f'{pages[i - 1]["slug"]}.html', pages[i - 1]['title'])
    out = f'<a class="prev" href="{prev[0]}"><span>Previous</span>{html.escape(prev[1])}</a>'
    if i + 1 < len(pages):
        out += f'<a class="next" href="{pages[i + 1]["slug"]}.html"><span>Next</span>{html.escape(pages[i + 1]["title"])}</a>'
    return f'<nav class="prevnext" aria-label="Previous and next page">{out}</nav>'


def check_links(out_dir, names):
    """Every relative href must name a file in out_dir, and every #id must exist there."""
    ids = {n: set(re.findall(r'\bid="([^"]+)"', open(os.path.join(out_dir, n)).read())) for n in names}
    bad = []
    for n in names:
        for href in re.findall(r'\bhref="([^"]*)"', open(os.path.join(out_dir, n)).read()):
            if re.match(r'^[a-z][a-z0-9+.-]*:', href, re.I) or href.startswith('//'):
                continue  # http(s), mailto and other absolute links are not checked
            path, _, frag = href.partition('#')
            target = path or n
            if target not in ids:
                bad.append(f'{n}: {href} (no file {target})')
            elif frag and frag not in ids[target]:
                bad.append(f'{n}: {href} (no id "{frag}" in {target})')
    if bad:
        sys.exit('broken links:\n  ' + '\n  '.join(bad))


def build_site(a):
    root = os.path.dirname(os.path.abspath(a.site))
    rel = lambda p: os.path.join(root, p)
    site = json.load(open(a.site))
    title, pages = site.get('title'), site.get('pages') or []
    if not title or not pages:
        sys.exit(f'{a.site}: needs "title" and a non-empty "pages" list')
    seen = set()
    for p in pages:
        for k in ('slug', 'title', 'body'):
            if not p.get(k):
                sys.exit(f'{a.site}: every page needs "{k}" ({p})')
        if not SLUG.match(p['slug']) or p['slug'] == 'index' or p['slug'] in seen:
            sys.exit(f'{a.site}: slug "{p["slug"]}" must be unique, lower-case a-z 0-9 -, and not "index"')
        seen.add(p['slug'])
    os.makedirs(a.out, exist_ok=True)
    types = load_types()
    default_svg = site.get('svg', 'svg')
    written, cards, total = [], [], 0

    for i, p in enumerate(pages):
        body = open(rel(p['body'])).read()
        figs = json.load(open(rel(p['figs']))) if p.get('figs') else {}
        try:
            body = fill_figs(body, figs, rel(p.get('svg', default_svg)), types)
        except SystemExit as e:
            sys.exit(f'{p["slug"]}: {e}')
        summary = p.get('summary') or lede(body)
        if not summary:
            print(f'warning: {p["slug"]} has no "summary" and no p.lede for its index card', file=sys.stderr)
        if '<h1' not in body:
            # The body's own p.lede moves into the generated header, so it is shown once.
            m = re.search(r'<p class="lede">.*?</p>', body, re.S)
            head_lede = m.group(0) if m else (f'<p class="lede">{html.escape(summary)}</p>' if summary else '')
            if m:
                body = body[:m.start()] + body[m.end():]
            body = (f'<header class="top"><p class="kicker">{html.escape(title)}</p><h1>{html.escape(p["title"])}</h1>'
                    + head_lede + '</header>\n' + body)
        secs = sections(body)
        if not secs:
            print(f'warning: {p["slug"]} has no <section id> with an h2, so no "On this page" list', file=sys.stderr)
        main = f'<div class="sitepage">{page_toc(secs)}<main class="pagemain">\n{body}\n{prev_next(pages, i)}</main></div>'
        name = f'{p["slug"]}.html'
        page = page_html(f'{p["title"]} | {title}', main, site_nav(title, pages, p['slug']))
        open(os.path.join(a.out, name), 'w').write(page)
        written.append(name)
        total += len(figs)
        print(f'{name}: {len(page)} bytes, {len(figs)} diagrams, {len(secs)} sections')
        cards.append((p.get('group', ''),
                      f'<li><a class="pagecard" href="{name}"><p class="num">{i + 1:02d}</p>'
                      f'<strong>{html.escape(p["title"])}</strong><span class="sum">{html.escape(summary)}</span></a></li>'))

    head = '<header class="top">' + (f'<p class="kicker">{html.escape(site["kicker"])}</p>' if site.get('kicker') else '')
    head += f'<h1>{html.escape(title)}</h1>'
    head += f'<p class="lede">{html.escape(site["lede"])}</p>' if site.get('lede') else ''
    head += f'<p class="note">{html.escape(site["note"])}</p>' if site.get('note') else ''
    head += '</header>'
    intro = ''
    if site.get('intro'):
        figs = json.load(open(rel(site['intro_figs']))) if site.get('intro_figs') else {}
        try:
            intro = fill_figs(open(rel(site['intro'])).read(), figs, rel(default_svg), types)
        except SystemExit as e:
            sys.exit(f'index intro: {e}')
        total += len(figs)
    groups = []  # consecutive pages with the same "group" share one heading and card grid
    for g, card in cards:
        if not groups or groups[-1][0] != g:
            groups.append((g, []))
        groups[-1][1].append(card)
    toc = ''.join((f'<h2 class="cardgroup">{html.escape(g)}</h2>' if g else '') + f'<ol class="pagecards">{"".join(cs)}</ol>'
                  for g, cs in groups)
    body = f'{head}\n{intro}\n<nav aria-label="Contents">{toc}</nav>'
    page = page_html(title, body, site_nav(title, pages, 'index'))
    open(os.path.join(a.out, 'index.html'), 'w').write(page)
    written.insert(0, 'index.html')
    print(f'index.html: {len(page)} bytes, {len(pages)} page cards')

    check_links(a.out, written)
    print(f'{a.out}: {len(written)} files, {total} diagrams, all links resolve')


def main():
    ap = argparse.ArgumentParser(description='Build one artifact page, or a multi-page site with --site.')
    ap.add_argument('--title')
    ap.add_argument('--body')
    ap.add_argument('--svg', default='svg')
    ap.add_argument('--figs', default=None)
    ap.add_argument('--site', help='site.json; then --out is the output folder')
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    build_site(a) if a.site else build_single(a)


if __name__ == '__main__':
    main()
