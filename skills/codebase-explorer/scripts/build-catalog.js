#!/usr/bin/env node
/*
 * build-catalog.js - regenerate the diagram-type gallery and the skill's chooser from diagram-types/catalog.json.
 *
 *   node build-catalog.js            (run from anywhere inside the explorer repo)
 *
 * Writes diagram-types/README.md (a gallery with thumbnails) and skills/codebase-explorer/references/diagram-types.md
 * (a compact "to explain X, use Y" table the skill reads when picking a diagram). Fails if a listed folder is
 * missing its example.svg, hand.jpg, clean.jpg or README.md, or if a README's "Not for" line names a slug that is
 * not in the catalog. Warns when a jpg is older than its example.svg, style.css or filters.svg (re-render with
 * scripts/render.sh --catalog).
 */
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..', '..');
const DT = path.join(ROOT, 'diagram-types');
const cat = JSON.parse(fs.readFileSync(path.join(DT, 'catalog.json'), 'utf8'));
const CATS = {
  software: 'Software and systems', technical: 'Technical and architecture', mapping: 'Diagramming and mapping',
  'process-workflow': 'Process and workflow', 'data-visualization': 'Data visualization', analysis: 'Analysis and comparison',
  planning: 'Planning and management', 'customer-ux': 'Customer and user experience', 'design-content': 'Design and content',
  'org-hierarchy': 'Organization and hierarchy', 'business-strategy': 'Business and strategy', education: 'Education',
  creative: 'Creative', admin: 'Admin and reference',
};
const order = Object.keys(CATS);
const DASH = new RegExp('[' + String.fromCharCode(0x2014, 0x2013) + ']', 'g');
const clean = (s) => String(s || '').replace(DASH, '-').replace(/\|/g, '/');

const missing = [];
for (const t of cat) for (const f of ['example.svg', 'hand.jpg', 'clean.jpg', 'README.md']) {
  if (!fs.existsSync(path.join(DT, t.category, t.slug, f))) missing.push(`${t.category}/${t.slug}/${f}`);
}
if (missing.length) { console.error('missing files:\n  ' + missing.join('\n  ')); process.exit(1); }

const slugs = new Set(cat.map((t) => t.slug));
const dangling = [];
for (const t of cat) {
  const notFor = fs.readFileSync(path.join(DT, t.category, t.slug, 'README.md'), 'utf8').split('\n').filter((l) => /^Not for/.test(l)).join(' ');
  for (const m of notFor.matchAll(/`([a-z0-9-]+)`/g)) if (!slugs.has(m[1])) dangling.push(`${t.category}/${t.slug}/README.md names \`${m[1]}\``);
}
if (dangling.length) { console.error('"Not for" lines point at slugs not in catalog.json:\n  ' + dangling.join('\n  ')); process.exit(1); }

const ASSETS = path.join(__dirname, '..', 'assets');
const kitTime = Math.max(...['style.css', 'filters.svg'].map((f) => fs.statSync(path.join(ASSETS, f)).mtimeMs));
const stale = [];
for (const t of cat) {
  const dir = path.join(DT, t.category, t.slug);
  const src = Math.max(kitTime, fs.statSync(path.join(dir, 'example.svg')).mtimeMs);
  for (const f of ['hand.jpg', 'clean.jpg']) if (fs.statSync(path.join(dir, f)).mtimeMs < src) stale.push(`${t.category}/${t.slug}/${f}`);
}
if (stale.length) console.warn(`warning: ${stale.length} renders are older than their example.svg or the kit CSS (run scripts/render.sh --catalog):\n  ` + stale.slice(0, 10).join('\n  ') + (stale.length > 10 ? '\n  ...' : ''));

const byCat = order.map((c) => [c, cat.filter((t) => t.category === c)]).filter(([, ts]) => ts.length);
const unknown = cat.filter((t) => !CATS[t.category]);
if (unknown.length) { console.error('unknown categories: ' + unknown.map((t) => t.category).join(', ')); process.exit(1); }

let g = `# Diagram types\n\n${cat.length} diagram types, each drawn once and rendered in both styles the explorer page offers: **hand-drawn** and **clean**. Every folder has the source \`example.svg\`, \`hand.jpg\`, \`clean.jpg\` and a README with when to use it and its anatomy.\n\nThe skill picks a type with [\`references/diagram-types.md\`](../skills/codebase-explorer/references/diagram-types.md). The class kit is in [\`references/diagram-kit.md\`](../skills/codebase-explorer/references/diagram-kit.md). Regenerate this page with \`node skills/codebase-explorer/scripts/build-catalog.js\`.\n\nRows marked (logos) show product logos provided by [Logo.dev](https://logo.dev). The logos are trademarks of their owners and are not covered by this repo's MIT license.\n\n`;
g += byCat.map(([c, ts]) => `- [${CATS[c]}](#${CATS[c].toLowerCase().replace(/[^a-z0-9]+/g, '-')}) (${ts.length})`).join('\n') + '\n';
for (const [c, ts] of byCat) {
  g += `\n## ${CATS[c]}\n\n| Type | Use it to explain | Clean | Hand-drawn |\n|---|---|---|---|\n`;
  for (const t of ts) {
    const d = `${t.category}/${t.slug}`;
    g += `| [**${clean(t.name)}**](${d}/)${t.uses_logos ? ' (logos)' : ''} | ${clean(t.use_for)} | <img src="${d}/clean.jpg" width="220" alt="${clean(t.name)}, clean"> | <img src="${d}/hand.jpg" width="220" alt="${clean(t.name)}, hand-drawn"> |\n`;
  }
}
fs.writeFileSync(path.join(DT, 'README.md'), g);

let r = `# Choosing a diagram type\n\nPick the type whose shape matches what you are explaining, then start from its example: \`diagram-types/<category>/<slug>/example.svg\` in the explorer repo (its README lists the anatomy). Put the bare slug (the first column, for example \`layered-architecture\`) in \`meta.json\` as \`"type"\`. Generated from \`diagram-types/catalog.json\`.\n\n`;
for (const [c, ts] of byCat) {
  r += `## ${CATS[c]}\n\n| Slug | Folder | Use it to explain | Match on |\n|---|---|---|---|\n`;
  for (const t of ts) r += `| \`${t.slug}\` | \`${t.category}/${t.slug}\` | ${clean(t.use_for)} | ${clean((t.keywords || []).join(', '))} |\n`;
  r += '\n';
}
fs.writeFileSync(path.join(__dirname, '..', 'references', 'diagram-types.md'), r);
console.log(`catalog: ${cat.length} types in ${byCat.length} categories`);
