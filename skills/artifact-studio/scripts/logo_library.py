#!/usr/bin/env python3
"""Build and query the local logo library that artifact pages inline their logos from.

    python3 logo_library.py account                       credits left this month (free call)
    python3 logo_library.py sync brands.json [--budget N]  fetch brands in priority order, spending at most N credits
    python3 logo_library.py add DOMAIN [--name N]         fetch one brand (2 credits)
    python3 logo_library.py find claude                    look a brand up by name, alias or domain
    python3 logo_library.py sheets OUT_DIR [--per 30]      numbered contact sheets for checking logos by eye

brands.json is a list of {"name", "domain", "aliases": [], "category", "tier": core|frequent|occasional, "also": []};
only name and domain are required. Tier, then list order, sets the fetch order.

Logos come from the Logo.dev API with the secret key (GET /v2/brands/logo, 2 credits per brand; an unknown brand is
free), which is the route Logo.dev allows for storing logos: its docs forbid building a copy from the img.logo.dev CDN
or fetching the CDN from a script. The free Community plan has 500 credits a month and cannot buy more, so a sync
fetches the most-used brands first and leaves the rest "queued" for the next run. Logo.dev answers a subdomain with
its parent's logo (aws.amazon.com shows Amazon), so a subdomain whose parent is also listed is not looked up: it is
kept as "parent" and logos.js gives it a monogram unless a better domain is listed. Two domains with one brand_id
are one brand: the second is recorded under the first's "also" instead of storing the logo twice.

The key comes from ~/.config/explorer/logo-dev.env (LOGO_DEV_SECRET_KEY, the sk_ key) or the environment. It is only
sent in the Authorization header: never in a URL, an argument, a log or the library. Download URLs (they expire, and
search results embed the publishable key) are never stored. The library (PNG files, manifest.json, index.html) is
local and gitignored: Logo.dev grants no licence to the logos and bulk redistribution is not fair use, so this public
repo ships the scripts, not the images. Pages may show logos as part of finished work; on the free plan a commercial
project must also link "Logos provided by Logo.dev" from a public page.
"""
import argparse, concurrent.futures, datetime, hashlib, html, json, os, re, shutil, subprocess, sys, threading, time
import urllib.error, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.realpath(__file__))
LIB = os.path.abspath(os.environ.get('EXPLORER_LOGOS') or os.path.join(HERE, '..', 'assets', 'logos'))
MANIFEST = os.path.join(LIB, 'manifest.json')
ENV = os.path.expanduser('~/.config/explorer/logo-dev.env')
API = 'https://api.logo.dev'
DOMAIN = re.compile(r'^[a-z0-9-]+(\.[a-z0-9-]+)+$')
PNG = b'\x89PNG\r\n\x1a\n'
TIERS = {'core': 0, 'frequent': 1, 'occasional': 2}
# hosts where each subdomain is its own site, so a subdomain is not its parent's brand
SHARED_HOSTS = ('github.io', 'gitlab.io', 'vercel.app', 'netlify.app', 'pages.dev', 'readthedocs.io', 'web.app',
                'herokuapp.com', 'fly.dev', 'workers.dev', 'substack.com', 'medium.com', 'notion.site')
FOUNDATIONS = ('apache.org',)  # projects on a foundation subdomain share its mark; they get a monogram
ATTRIBUTION = 'Logos provided by Logo.dev (https://logo.dev). Logos are trademarks of their owners.'
LOCK = threading.Lock()


class OutOfCredits(Exception):
    pass


def secret():
    key = os.environ.get('LOGO_DEV_SECRET_KEY', '').strip()
    if not key and os.path.exists(ENV):
        for line in open(ENV):
            m = re.match(r'^LOGO_DEV_SECRET_KEY=(\S+)', line)
            if m:
                key = m.group(1)
    if not key:
        sys.exit(f'no LOGO_DEV_SECRET_KEY: put the sk_ key from logo.dev in {ENV} (chmod 600, never commit it)')
    return key


def request(url, headers=None):
    """GET a URL; returns (status, body bytes, headers). Errors never echo the URL or the key."""
    req = urllib.request.Request(url, headers={'User-Agent': 'explorer-logo-library/2', **(headers or {})})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read(), r.headers
    except urllib.error.HTTPError as e:
        return e.code, e.read() or b'', e.headers
    except (urllib.error.URLError, TimeoutError, OSError):
        return 0, b'', {}


def api(path, sk, params=None):
    url = API + path + ('?' + urllib.parse.urlencode(params) if params else '')
    for attempt in range(12):
        status, body, headers = request(url, {'Authorization': f'Bearer {sk}', 'Accept': 'application/json'})
        if status == 202:      # still indexing: free retries, usually ready within a minute
            time.sleep(int(headers.get('Retry-After') or 30)); continue
        if status == 429:
            time.sleep(int(headers.get('RateLimit-Reset') or 30) + 1); continue
        if status in (0, 500, 502, 503, 504):
            time.sleep(2 ** min(attempt, 5)); continue
        if status == 402:
            raise OutOfCredits()
        try:
            data = json.loads(body) if body else {}
        except ValueError:
            data = {}
        return status, data, headers
    return 0, {}, {}


def account(sk):
    status, data, _ = api('/v2/account', sk)
    if status != 200:
        sys.exit(f'account check failed (HTTP {status}); is the sk_ key right?')
    return data['data']


def logo(domain, sk):
    """Look one domain up. Returns (image dict or None, billed)."""
    status, data, headers = api('/v2/brands/logo', sk, {'domain': domain})
    billed = headers.get('Credits-Charged', '0') == '1' if headers else False
    return (data.get('data') if status == 200 else None), billed


def download(url):
    sep = '&' if '?' in url else '?'
    status, body, headers = request(url + sep + urllib.parse.urlencode({'size': 128, 'format': 'png'}))
    return body if status == 200 and body.startswith(PNG) else None


def search(name, sk):
    status, data, _ = api('/v2/search', sk, {'q': name, 'method': 'match', 'limit': 5})
    hits = [{'name': r.get('name', ''), 'domain': str(r.get('domain', '')).lower()} for r in (data.get('data') or [])
            if isinstance(r, dict) and r.get('domain')] if status == 200 else []
    return [h for h in hits if h['name'].lower() == name.lower()] + [h for h in hits if h['name'].lower() != name.lower()]


def load_manifest():
    try:
        return json.load(open(MANIFEST))
    except (OSError, ValueError):
        return {'entries': []}


def clean(b):
    d = str(b.get('domain', '')).strip().lower().removeprefix('https://').removeprefix('http://')
    d = d.removeprefix('www.').split('/')[0]
    return {'name': str(b.get('name') or d).strip(), 'domain': d, 'aliases': sorted(set(b.get('aliases') or [])),
            'also': sorted(set(b.get('also') or [])), 'category': b.get('category') or 'other',
            'tier': b.get('tier') if b.get('tier') in TIERS else 'occasional'}


def parent_of(domain, listed):
    """The listed parent whose logo Logo.dev would return for this subdomain, or None."""
    labels = domain.split('.')
    if len(labels) <= 2 or any(domain.endswith('.' + h) for h in SHARED_HOSTS):
        return None
    parent = '.'.join(labels[-2:])
    if parent in FOUNDATIONS:
        return parent
    return parent if parent in listed else None


def sync(path, budget=None, refresh=False, workers=4):
    sk = secret()
    acct = account(sk)
    left = acct['credits']['remaining']
    cap = min(budget, left) if budget is not None else max(0, left - 40)  # keep 40 credits for ad hoc adds
    print(f'{acct["plan"]} plan: {left} credits left (renews {acct["credits"]["renews_at"][:10]}); spending at most {cap}')
    os.makedirs(LIB, exist_ok=True)
    brands, seen = [], set()
    for raw in json.load(open(path)):
        b = clean(raw)
        if not DOMAIN.match(b['domain']):
            print(f'skip {b["name"]!r}: {b["domain"]!r} is not a domain', file=sys.stderr)
        elif b['domain'] not in seen:
            seen.add(b['domain'])
            brands.append(b)
    brands.sort(key=lambda b: TIERS[b['tier']])  # stable: list order within a tier
    old = {e['domain']: e for e in load_manifest().get('entries', [])}
    spent = [0]
    results = {}

    def one(b):
        domain = b['domain']
        prev = old.get(domain, {})
        if os.path.exists(os.path.join(LIB, domain + '.png')) and not refresh:
            return b, {**prev, 'status': 'ok'}
        parent = parent_of(domain, seen)
        if parent:
            return b, {'status': 'parent', 'parent': parent}
        with LOCK:
            if spent[0] + 2 > cap:
                return b, {'status': 'queued'}
            spent[0] += 2
        try:
            img, billed = logo(domain, sk)
            if not img:
                if billed:   # a known brand with no logo image: billed, so remember it and do not retry each sync
                    return b, {'status': 'no-logo'}
                with LOCK:
                    spent[0] -= 2  # unknown brands are free
                for hit in search(b['name'], sk)[:2]:
                    if hit['domain'] == domain or not DOMAIN.match(hit['domain']):
                        continue
                    with LOCK:
                        if spent[0] + 2 > cap:
                            return b, {'status': 'queued'}
                        spent[0] += 2
                    img, _ = logo(hit['domain'], sk)
                    if img:
                        return b, save(hit['domain'], img, 'resolved', also=[domain])
                return b, {'status': 'missing'}
            return b, save(domain, img, 'ok')
        except OutOfCredits:
            return b, {'status': 'queued'}

    with concurrent.futures.ThreadPoolExecutor(workers) as pool:
        for b, res in pool.map(one, brands):
            results[b['domain']] = (b, res)

    entries = dict(old)
    for domain, (b, res) in results.items():
        target = res.get('domain', domain)
        prev = entries.get(target, {})
        also = sorted((set(prev.get('also', [])) | set(b['also']) | set(res.get('also', []))) - {target})
        e = {k: v for k, v in prev.items() if k not in ('status', 'parent')}
        e.update({'name': b['name'], 'domain': target, 'also': also, 'aliases': b['aliases'],
                  'category': b['category'], 'tier': b['tier'], **{k: v for k, v in res.items() if k != 'also'}})
        entries[target] = e
        if target != domain:
            entries.pop(domain, None)
    write_manifest(entries)
    counts = {}
    for _, res in results.values():
        counts[res['status']] = counts.get(res['status'], 0) + 1
    print(f'{len(results)} brands: ' + ', '.join(f'{v} {k}' for k, v in sorted(counts.items()))
          + f'; about {spent[0]} credits spent')
    if counts.get('queued'):
        print(f'{counts["queued"]} brands are queued: run sync again after the credits renew')


def save(domain, img, status, also=()):
    """Download the logo through the API's signed URL and keep the file and its metadata, never the URL."""
    png = download(img.get('url', ''))
    if not png:
        return {'status': 'download-failed', 'domain': domain}
    tmp = os.path.join(LIB, f'.{domain}.png.tmp')
    open(tmp, 'wb').write(png)
    os.replace(tmp, os.path.join(LIB, domain + '.png'))
    src = img.get('source') or {}
    return {'status': status, 'domain': domain, 'also': list(also), 'brand_id': img.get('brand_id'),
            'etag': img.get('etag'), 'source_format': src.get('format'), 'is_vector': src.get('is_vector'),
            'has_transparency': src.get('has_transparency'), 'fetched': datetime.date.today().isoformat()}


def write_manifest(entries):
    by_brand, by_hash = {}, {}
    for e in sorted(entries.values(), key=lambda e: (TIERS.get(e.get('tier'), 2), e['domain'])):
        f = os.path.join(LIB, e['domain'] + '.png')
        if os.path.exists(f):
            data = open(f, 'rb').read()
            e.update(file=e['domain'] + '.png', bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
            if e.get('status') in (None, 'cached', 'fetched'):
                e['status'] = 'ok'
            if e.get('brand_id'):
                by_brand.setdefault(e['brand_id'], []).append(e['domain'])
            by_hash.setdefault(e['sha256'], []).append(e['domain'])
        else:
            e['file'] = None
            for k in ('sha256', 'bytes'):
                e.pop(k, None)
    for e in entries.values():
        twins = sorted({d for group in (by_brand.get(e.get('brand_id'), []), by_hash.get(e.get('sha256'), []))
                        for d in group if d != e['domain']}) if e.get('file') else []
        if twins:
            e['same_as'] = twins
        else:
            e.pop('same_as', None)
    ordered = sorted(entries.values(), key=lambda e: (e['category'], e['name'].lower()))
    doc = {'generated': datetime.date.today().isoformat(), 'source': 'Logo.dev API (/v2/brands/logo)',
           'attribution': ATTRIBUTION, 'count': sum(1 for e in ordered if e.get('file')), 'entries': ordered}
    tmp = MANIFEST + '.tmp'
    json.dump(doc, open(tmp, 'w'), indent=1)
    os.replace(tmp, MANIFEST)
    open(os.path.join(LIB, 'index.html'), 'w').write(contact_sheet(ordered))
    dupes = [e for e in ordered if e.get('same_as')]
    if dupes:
        print('one brand or one image under several domains (keep the one that names the brand):')
        for e in dupes:
            print(f'  {e["domain"]} = {", ".join(e["same_as"])}')


SHEET_CSS = """
:root { --bg: #ffffff; --card: #f6f8fa; --ink: #1f2328; --muted: #59636e; --line: #d1d9e0; --plate: #ffffff;
  --warn: #9a6700; --bad: #cf222e; }
@media (prefers-color-scheme: dark) { :root { --bg: #0d1117; --card: #151b23; --ink: #e6edf3; --muted: #9da7b3;
  --line: #30363d; --plate: #e6edf3; --warn: #d29922; --bad: #f85149; } }
* { box-sizing: border-box; }
body { margin: 0; padding: 24px 20px 48px; background: var(--bg); color: var(--ink);
  font: 14px/1.4 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }
h1 { font-size: 22px; margin: 0 0 4px; } h2 { font-size: 13px; letter-spacing: .08em; text-transform: uppercase;
  color: var(--muted); margin: 28px 0 10px; }
.note { color: var(--muted); margin: 0 0 14px; }
input { width: min(420px, 100%); padding: 8px 10px; border: 1px solid var(--line); border-radius: 8px;
  background: var(--card); color: var(--ink); font: inherit; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(168px, 1fr)); gap: 10px; }
.tile { background: var(--card); border: 1px solid var(--line); border-radius: 10px; padding: 12px;
  display: flex; gap: 10px; align-items: center; min-width: 0; }
.plate { width: 44px; height: 44px; flex: none; border-radius: 9px; background: var(--plate);
  display: grid; place-items: center; }
.plate img { width: 34px; height: 34px; object-fit: contain; }
.plate.none { border: 1px dashed var(--line); background: transparent; color: var(--muted); font-weight: 700; }
.name { font-weight: 600; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.dom { font: 12px ui-monospace, SFMono-Regular, Menlo, monospace; color: var(--muted); overflow: hidden;
  text-overflow: ellipsis; white-space: nowrap; }
.flag { font-size: 11px; color: var(--warn); } .flag.bad { color: var(--bad); }
.meta { min-width: 0; }
footer { margin-top: 32px; color: var(--muted); font-size: 12px; }
"""

STATUS_NOTE = {'queued': 'queued: next credit cycle', 'parent': 'subdomain: shows its parent', 'missing': 'no logo on Logo.dev',
               'no-logo': 'brand has no logo', 'download-failed': 'download failed', 'wrong': 'wrong mark: not used'}


def tile(e):
    esc = html.escape
    mark = (f'<div class="plate"><img src="{esc(e["file"])}" alt="" loading="lazy"></div>' if e.get('file')
            else f'<div class="plate none">{esc(e["name"][:1].upper())}</div>')
    flag = ''
    if e.get('status') in STATUS_NOTE:
        flag = f'<div class="flag{" bad" if e["status"] in ("missing", "wrong") else ""}">{STATUS_NOTE[e["status"]]}</div>'
    elif e.get('same_as'):
        flag = f'<div class="flag">same brand as {esc(", ".join(e["same_as"]))}</div>'
    words = ' '.join([e['name'], e['domain'], *e.get('aliases', []), *e.get('also', []), e['category'], e.get('status', '')]).lower()
    return (f'<div class="tile" data-q="{esc(words)}">{mark}<div class="meta"><div class="name">{esc(e["name"])}</div>'
            f'<div class="dom">{esc(e["domain"])}</div>{flag}</div></div>')


def contact_sheet(entries):
    groups = {}
    for e in entries:
        groups.setdefault(e['category'], []).append(e)
    body = ''.join(f'<section><h2>{html.escape(c)} ({len(es)})</h2><div class="grid">{"".join(tile(e) for e in es)}'
                   '</div></section>' for c, es in sorted(groups.items()))
    n = sum(1 for e in entries if e.get('file'))
    return f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Logo Library</title><style>{SHEET_CSS}</style></head><body>
<h1>Logo library</h1><p class="note">{n} logos, {len(entries) - n} without one yet. Local only: do not publish this page.
Use the domain in a diagram, <code>&lt;image class="d-logo" data-logo="DOMAIN" .../&gt;</code>, or in text,
<code>&lt;img class="logo" data-logo="DOMAIN" alt="Name"&gt;</code>.</p>
<input id="q" type="search" placeholder="Filter by name, domain, category or status" autofocus>
{body}
<footer>{html.escape(ATTRIBUTION)} Generated {datetime.date.today().isoformat()}.</footer>
<script>
document.getElementById('q').addEventListener('input', function (ev) {{
  var q = ev.target.value.trim().toLowerCase();
  document.querySelectorAll('.tile').forEach(function (t) {{ t.hidden = q && t.dataset.q.indexOf(q) < 0; }});
  document.querySelectorAll('section').forEach(function (s) {{ s.hidden = !s.querySelector('.tile:not([hidden])'); }});
}});
</script></body></html>
"""


def find(text):
    q = text.strip().lower()
    hits = [e for e in load_manifest().get('entries', [])
            if q in e['name'].lower() or q in e['domain'] or any(q in a.lower() for a in e.get('aliases', []) + e.get('also', []))]
    if not hits:
        print(f'no brand matches {text!r}; add it with: python3 {os.path.relpath(__file__)} add DOMAIN --name NAME')
    for e in hits:
        status = e.get('status', '?') + (f', same brand as {", ".join(e["same_as"])}' if e.get('same_as') else '')
        print(f'{e["domain"]:32} {e["name"]}  [{e["category"]}; {status}]')


def find_chrome():
    for c in ('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', shutil.which('google-chrome'),
              shutil.which('chromium'), shutil.which('chromium-browser')):
        if c and os.path.exists(c):
            return c
    return None


def sheets(out, per=30):
    """Numbered contact sheets for checking by eye that every logo is its brand's mark. Local only."""
    entries = [e for e in load_manifest().get('entries', []) if e.get('file')]
    if not entries:
        sys.exit(f'library is empty; run sync first ({LIB})')
    os.makedirs(out, exist_ok=True)
    chrome = find_chrome()
    css = ('body{margin:0;padding:16px;background:#fff;color:#111;font:15px -apple-system,sans-serif}'
           '.g{display:grid;grid-template-columns:repeat(6,1fr);gap:10px}'
           '.t{border:1px solid #ddd;border-radius:10px;padding:10px;text-align:center}'
           '.t img{width:88px;height:88px;object-fit:contain;display:block;margin:4px auto 8px}'
           '.n{font-weight:700;font-size:14px}.d{font:12px Menlo,monospace;color:#555;word-break:break-all}'
           '.i{font:12px Menlo,monospace;color:#999}')
    made = []
    for k in range(0, len(entries), per):
        batch = entries[k:k + per]
        tiles = ''.join(f'<div class="t"><div class="i">#{k + i + 1}</div><img src="file://{os.path.join(LIB, e["file"])}">'
                        f'<div class="n">{html.escape(e["name"])}</div><div class="d">{html.escape(e["domain"])}</div></div>'
                        for i, e in enumerate(batch))
        name = f'sheet-{k // per + 1:02d}'
        page = os.path.join(out, name + '.html')
        open(page, 'w').write(f'<!doctype html><meta charset="utf-8"><style>{css}</style><div class="g">{tiles}</div>')
        json.dump([{'n': k + i + 1, 'name': e['name'], 'domain': e['domain'], 'category': e['category']}
                   for i, e in enumerate(batch)], open(os.path.join(out, name + '.json'), 'w'), indent=1)
        if chrome:
            rows = -(-len(batch) // 6)
            subprocess.run([chrome, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files',
                            f'--window-size=1200,{32 + rows * 178}', f'--screenshot={os.path.join(out, name + ".png")}',
                            '--virtual-time-budget=4000', 'file://' + page],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=60)
        made.append(name)
    print(f'{len(made)} sheets in {out}' + ('' if chrome else ' (HTML only: no Chrome for PNGs)'))


def mark(domain, status):
    """Record a verdict from the eye check, for example 'wrong' for a mark that is not the brand's."""
    doc = load_manifest()
    entries = {e['domain']: e for e in doc.get('entries', [])}
    if domain not in entries:
        sys.exit(f'{domain} is not in the library')
    entries[domain]['status'] = status
    if status == 'wrong':
        f = os.path.join(LIB, domain + '.png')
        if os.path.exists(f):
            os.remove(f)
    write_manifest(entries)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest='cmd', required=True)
    sub.add_parser('account')
    s = sub.add_parser('sync'); s.add_argument('brands'); s.add_argument('--budget', type=int)
    s.add_argument('--refresh', action='store_true')
    a = sub.add_parser('add'); a.add_argument('domain'); a.add_argument('--name'); a.add_argument('--category', default='other')
    f = sub.add_parser('find'); f.add_argument('text')
    h = sub.add_parser('sheets'); h.add_argument('out'); h.add_argument('--per', type=int, default=30)
    m = sub.add_parser('mark'); m.add_argument('domain'); m.add_argument('status', choices=['ok', 'wrong'])
    args = p.parse_args()
    if args.cmd == 'account':
        acct = account(secret())
        c = acct['credits']
        print(f'{acct["plan"]} plan: {c["remaining"]} of {c["monthly_allowance"]} credits left, renews {c["renews_at"][:10]}'
              f' (a logo costs 2; an unknown brand is free)')
    elif args.cmd == 'sync':
        sync(args.brands, args.budget, args.refresh)
    elif args.cmd == 'add':
        tmp = os.path.join(LIB, '.add.json')
        os.makedirs(LIB, exist_ok=True)
        json.dump([{'name': args.name or args.domain, 'domain': args.domain, 'category': args.category, 'tier': 'core'}],
                  open(tmp, 'w'))
        try:
            sync(tmp, budget=4)
        finally:
            os.remove(tmp)
    elif args.cmd == 'find':
        find(args.text)
    elif args.cmd == 'mark':
        mark(args.domain, args.status)
    else:
        sheets(args.out, args.per)


if __name__ == '__main__':
    main()
