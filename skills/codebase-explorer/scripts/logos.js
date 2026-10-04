#!/usr/bin/env node
/*
 * logos.js - fill <image class="d-logo" data-logo="example.com" .../> slots in diagram SVGs.
 *
 *   node logos.js in.svg out.svg        or   require('./logos.js').inject(svgString)
 *
 * With a logo.dev publishable key (LOGO_DEV_TOKEN in the environment, or in ~/.config/explorer/logo-dev.env)
 * each logo is fetched once into ~/.cache/explorer-logos and inlined as a data: URI, so the page works offline
 * and the key never lands in a committed file. Without a key, or if a fetch fails, the slot becomes a
 * monogram circle drawn with the kit classes. Get a free key at https://logo.dev (use the pk_ one).
 */
const fs = require('fs');
const os = require('os');
const path = require('path');
const { execFileSync } = require('child_process');

const CACHE = path.join(os.homedir(), '.cache', 'explorer-logos');

function token() {
  if (process.env.LOGO_DEV_TOKEN) return process.env.LOGO_DEV_TOKEN.trim();
  const f = path.join(os.homedir(), '.config', 'explorer', 'logo-dev.env');
  if (!fs.existsSync(f)) return '';
  const m = fs.readFileSync(f, 'utf8').match(/^LOGO_DEV_TOKEN=(\S+)/m);
  return m ? m[1] : '';
}

// size 64 with retina gives a 128px PNG: sharp for a 28px slot on a 2x screen, about a quarter of the bytes of 256px
function fetchFile(domain, key) {
  const file = path.join(CACHE, domain.replace(/[^a-z0-9.-]/gi, '_') + '@128.png');
  if (!fs.existsSync(file)) {
    if (!key) return null;
    fs.mkdirSync(CACHE, { recursive: true });
    const url = `https://img.logo.dev/${encodeURIComponent(domain)}?token=${key}&size=64&format=png&retina=true`;
    try { execFileSync('curl', ['-fsSL', '--max-time', '15', '-o', file, url], { stdio: 'ignore' }); } catch (e) { try { fs.unlinkSync(file); } catch (_) {} return null; }
  }
  return fs.readFileSync(file);
}

// logo.dev answers some product subdomains with the parent's mark. For a vendor (cloud.google.com, azure.microsoft.com)
// the vendor logo is fine, but a foundation hosts projects with their own brands: every *.apache.org project would
// get the same Apache feather, so Kafka, Flink and Cassandra would look alike. Those slots fall back to a monogram.
const FOUNDATIONS = new Set(['apache.org']);
const seen = new Map(); // bytes hash -> first domain, to warn when two domains share one image
function fetchLogo(domain, key) {
  const buf = fetchFile(domain, key);
  if (!buf) return null;
  const labels = domain.split('.');
  if (labels.length > 2 && FOUNDATIONS.has(labels.slice(-2).join('.'))) {
    const parent = fetchFile(labels.slice(-2).join('.'), key);
    if (parent && parent.equals(buf)) return null;
  }
  const h = require('crypto').createHash('md5').update(buf).digest('hex');
  if (seen.has(h) && seen.get(h) !== domain) console.warn(`logos: ${domain} and ${seen.get(h)} return the same image; one of them shows the wrong brand`);
  else seen.set(h, domain);
  return 'data:image/png;base64,' + buf.toString('base64');
}

const attr = (tag, name) => { const m = tag.match(new RegExp('\\s' + name + '="([^"]*)"')); return m ? m[1] : ''; };

function inject(svg, opts) {
  const key = (opts && 'token' in opts) ? opts.token : token();
  return svg.replace(/<image\b[^>]*\bdata-logo="[^"]*"[^>]*?(?:\/>|>\s*<\/image>)/g, (tag) => {
    const domain = attr(tag, 'data-logo');
    const uri = fetchLogo(domain, key);
    const x = +attr(tag, 'x') || 0, y = +attr(tag, 'y') || 0, w = +attr(tag, 'width') || 28, h = +attr(tag, 'height') || 28;
    // a light tile behind every logo keeps dark marks (GitHub, Next.js) visible in the dark theme
    if (uri) return `<rect class="d-logo-plate" x="${x - 3}" y="${y - 3}" width="${w + 6}" height="${h + 6}" rx="7"/>` + tag.replace(/\s(?:xlink:)?href="[^"]*"/g, '').replace(/^<image\b/, `<image href="${uri}"`);
    const name = attr(tag, 'data-name') || domain;
    const letter = (name.match(/[a-z0-9]/i) || ['?'])[0].toUpperCase();
    const cx = x + w / 2, cy = y + h / 2, r = Math.min(w, h) / 2;
    return `<g class="d-logo-mono"><circle class="d-logo-fb" cx="${cx}" cy="${cy}" r="${r}"/><text class="d-lfb" x="${cx}" y="${cy + 4.5}">${letter}</text></g>`;
  });
}

module.exports = { inject, token };

if (require.main === module) {
  const [, , inp, out] = process.argv;
  if (!inp || !out) { console.error('usage: logos.js in.svg out.svg'); process.exit(1); }
  fs.writeFileSync(out, inject(fs.readFileSync(inp, 'utf8')));
}
