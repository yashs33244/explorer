#!/usr/bin/env node
/*
 * logos.js - fill logo slots with inlined logos: <image class="d-logo" data-logo="example.com" .../> in diagram
 * SVGs, and <img class="logo" data-logo="example.com" alt="Example"> in page text and tables.
 *
 *   node logos.js in.svg out.svg         one SVG file
 *   node logos.js --inline < in > out    any HTML or SVG on stdin: both kinds of slot (artifact-studio build.py)
 *   node logos.js --find codex           look a brand up in the logo library by name, alias or domain
 *   require('./logos.js').inject(svg) / .injectHtml(html)
 *
 * Logos come only from the local logo library (artifact-studio/assets/logos, override with EXPLORER_LOGOS), which
 * artifact-studio/scripts/logo_library.py fills through the Logo.dev API with the secret key. This script never
 * fetches img.logo.dev: Logo.dev's terms forbid building a stored copy from its CDN or fetching the CDN from a
 * script. A slot names a domain, or a brand name or alias from the library manifest ("Claude Code"). A brand not in
 * the library becomes a monogram and the run prints the command that adds it (2 credits). Each logo is inlined as a
 * data: URI, so a page works offline and carries no key.
 */
const fs = require('fs');
const path = require('path');

const LIBRARY = process.env.EXPLORER_LOGOS || path.join(__dirname, '..', '..', 'artifact-studio', 'assets', 'logos');
const ADD = `python3 ${path.join(__dirname, '..', '..', 'artifact-studio', 'scripts', 'logo_library.py')} add`;

let manifestCache = null;
function manifest() {
  if (!manifestCache) {
    try { manifestCache = JSON.parse(fs.readFileSync(path.join(LIBRARY, 'manifest.json'), 'utf8')).entries || []; }
    catch (e) { manifestCache = []; }
  }
  return manifestCache;
}

// a slot may name a domain, a domain the library moved (Logo.dev knew the brand under another one), or a brand name.
// The slot's own domain always wins; "also" and names only point to entries that hold a logo, because an entry's
// alternative domains can belong to other brands (a project's github.com page, a parent company).
function resolve(ref) {
  const r = String(ref || '').trim().toLowerCase().replace(/^https?:\/\//, '').replace(/^www\./, '').replace(/\/.*$/, '');
  const entries = manifest();
  if (entries.some(e => e.domain === r)) return r;
  const withFile = entries.filter(e => e.file);
  const hit = withFile.find(e => (e.also || []).includes(r)) ||
    withFile.find(e => e.name.toLowerCase() === r || (e.aliases || []).some(a => a.toLowerCase() === r));
  return hit ? hit.domain : r;
}

const warned = new Set();
const seen = new Map(); // bytes hash -> first domain, to warn when two domains share one image
function fetchLogo(domain) {
  const file = path.join(LIBRARY, domain.replace(/[^a-z0-9.-]/gi, '_') + '.png');
  if (!fs.existsSync(file)) {
    if (!warned.has(domain)) {
      warned.add(domain);
      const e = manifest().find(x => x.domain === domain);
      const why = !e ? `is not in the logo library; add it with: ${ADD} ${domain} --name NAME`
        : e.status === 'wrong' ? 'is marked wrong in the logo library (Logo.dev\'s image is not the brand\'s mark)'
        : e.status === 'parent' ? `is a subdomain Logo.dev answers with its parent's mark (${e.parent || 'the parent'})`
        : e.status === 'queued' ? `is queued for the next credit cycle; fetch it now with: ${ADD} ${domain} --name "${e.name}"`
        : `has no logo on Logo.dev (${e.status})`;
      console.warn(`logos: ${domain} ${why}, so it gets a monogram`);
    }
    return null;
  }
  const buf = fs.readFileSync(file);
  const h = require('crypto').createHash('md5').update(buf).digest('hex');
  if (seen.has(h) && seen.get(h) !== domain) console.warn(`logos: ${domain} and ${seen.get(h)} share one image; one of them shows the wrong brand`);
  else seen.set(h, domain);
  return 'data:image/png;base64,' + buf.toString('base64');
}

const attr = (tag, name) => { const m = tag.match(new RegExp('\\s' + name + '="([^"]*)"')); return m ? m[1] : ''; };

function inject(svg) {
  return svg.replace(/<image\b[^>]*\bdata-logo="[^"]*"[^>]*?(?:\/>|>\s*<\/image>)/g, (tag) => {
    const domain = resolve(attr(tag, 'data-logo'));
    const uri = fetchLogo(domain);
    const x = +attr(tag, 'x') || 0, y = +attr(tag, 'y') || 0, w = +attr(tag, 'width') || 28, h = +attr(tag, 'height') || 28;
    // a light tile behind every logo keeps dark marks (GitHub, Next.js) visible in the dark theme
    if (uri) return `<rect class="d-logo-plate" x="${x - 3}" y="${y - 3}" width="${w + 6}" height="${h + 6}" rx="7"/>` + tag.replace(/\s(?:xlink:)?href="[^"]*"/g, '').replace(/^<image\b/, `<image href="${uri}"`);
    const name = attr(tag, 'data-name') || domain;
    const letter = (name.match(/[a-z0-9]/i) || ['?'])[0].toUpperCase();
    const cx = x + w / 2, cy = y + h / 2, r = Math.min(w, h) / 2;
    return `<g class="d-logo-mono"><circle class="d-logo-fb" cx="${cx}" cy="${cy}" r="${r}"/><text class="d-lfb" x="${cx}" y="${cy + 4.5}">${letter}</text></g>`;
  });
}

// <img class="logo" data-logo="vercel.com" alt="Vercel"> in page text or a table cell: the src is filled the same
// way; without a logo the tag becomes a small monogram, so the row still reads
function injectHtml(page) {
  return page.replace(/<img\b[^>]*\bdata-logo="[^"]*"[^>]*>/g, (tag) => {
    const ref = attr(tag, 'data-logo');
    const uri = fetchLogo(resolve(ref));
    if (uri) return tag.replace(/\ssrc="[^"]*"/g, '').replace(/^<img\b/, `<img src="${uri}"`);
    const name = attr(tag, 'alt') || ref;
    const letter = (name.match(/[a-z0-9]/i) || ['?'])[0].toUpperCase();
    return `<span class="logo logo-mono" aria-hidden="true">${letter}</span>`;
  });
}

function find(text) {
  const q = String(text || '').trim().toLowerCase();
  const hits = manifest().filter(e => e.name.toLowerCase().includes(q) || e.domain.includes(q) ||
    [...(e.aliases || []), ...(e.also || [])].some(a => a.toLowerCase().includes(q)));
  if (!hits.length) console.log(`no brand matches "${text}" in ${LIBRARY}; add one with: ${ADD} DOMAIN --name NAME`);
  for (const e of hits) console.log(`${e.domain.padEnd(32)} ${e.name}  [${e.category}; ${e.status}${e.same_as ? ', same brand as ' + e.same_as.join(', ') : ''}]`);
}

module.exports = { inject, injectHtml, resolve };

if (require.main === module) {
  const [, , inp, out] = process.argv;
  if (inp === '--inline') {
    process.stdout.write(injectHtml(inject(fs.readFileSync(0, 'utf8'))));
  } else if (inp === '--find') {
    find(process.argv.slice(3).join(' '));
  } else if (inp && out) {
    fs.writeFileSync(out, inject(fs.readFileSync(inp, 'utf8')));
  } else {
    console.error('usage: logos.js in.svg out.svg | logos.js --inline < in > out | logos.js --find NAME');
    process.exit(1);
  }
}
