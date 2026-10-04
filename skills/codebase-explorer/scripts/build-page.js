#!/usr/bin/env node
/*
 * build-page.js - turn topic JSON files + hand-drawn SVG diagrams into one self-contained explorer page.
 *
 *   node build-page.js --config explorer.config.json --topics topics/ --diagrams diagrams/ --out page.html
 *
 * No dependencies. The output is a fragment (a <title>, <style>, markup and <script>) that the Artifact tool
 * wraps in a document skeleton, and that also opens fine inside a plain HTML wrapper (see render.sh).
 */
const fs = require('fs');
const path = require('path');

const args = {};
for (let i = 2; i < process.argv.length; i += 2) args[process.argv[i].replace(/^--/, '')] = process.argv[i + 1];
for (const need of ['config', 'topics', 'out']) if (!args[need]) { console.error('usage: build-page.js --config c.json --topics dir [--diagrams dir] --out file.html'); process.exit(1); }

const HERE = __dirname;
const ASSETS = args.assets || path.join(HERE, '..', 'assets');
const CFG_DIR = path.dirname(path.resolve(args.config));
const cfg = JSON.parse(fs.readFileSync(args.config, 'utf8'));
const TOPICS = path.resolve(args.topics);
const DIAGRAMS = args.diagrams ? path.resolve(args.diagrams) : null;

const DASHES = new RegExp('[' + String.fromCharCode(0x2014, 0x2013) + ']', 'g'); // keep the page free of em and en dashes
const clean = (s) => String(s == null ? '' : s).replace(DASHES, '-');
const esc = (s) => clean(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const rel = (p) => path.resolve(CFG_DIR, p);
const readJson = (p) => JSON.parse(fs.readFileSync(p, 'utf8'));

/* ---------- topics ---------- */
const groups = cfg.groups || [];
const ORDER = groups.flatMap((g) => g.topics);
const topics = {};
ORDER.concat(cfg.overviewKey ? [cfg.overviewKey] : []).forEach((k) => {
  const f = path.join(TOPICS, k + '.json');
  if (!fs.existsSync(f)) { console.error('missing topic file ' + f); process.exit(1); }
  topics[k] = readJson(f);
});
const short = (k) => (cfg.navLabels && cfg.navLabels[k]) || topics[k].short || topics[k].title;

/* ---------- tables: columns sized by content ---------- */
function percentile(arr, p) { if (!arr.length) return 0; const s = arr.slice().sort((a, b) => a - b); return s[Math.min(s.length - 1, Math.floor(p * s.length))]; }
function table(columns, rows, opts) {
  opts = opts || {};
  const text = (v) => clean(Array.isArray(v) ? v.join(" ") : v);
  // Fixed layout with computed widths: narrow columns (numbers, pills, short words) get just enough ch,
  // and the rest of the width is shared by how much text each column really holds, so long sentences get more room.
  const meta = columns.map((c) => {
    const kind = c.kind || "text";
    const shown = (r) => { const s = text(r[c.key]); return kind === "link" ? s.replace(/^https?:\/\/(www\.)?/, "").slice(0, 44) : s; };
    const lens = rows.map((r) => shown(r).length);
    const max = Math.max(0, ...lens);
    const p90 = percentile(lens, 0.9);
    const avg = lens.length ? lens.reduce((a, b) => a + b, 0) / lens.length : 0;
    const narrow = kind === "num" || kind === "pill" || kind === "nowrap" || (max <= 10 && kind !== "link");
    const weight = narrow ? 0 : Math.max(10, Math.min(100, 0.2 * avg + 0.5 * p90 + 0.3 * max));
    const ch = narrow ? Math.min(20, Math.max(max, c.label.length) + 4) : 0;
    return { c, kind, narrow, weight, ch, shown };
  });
  const totalW = meta.reduce((a, m) => a + m.weight, 0) || 1;
  const narrowCh = meta.reduce((a, m) => a + m.ch, 0);
  const textCols = meta.filter((m) => !m.narrow).length;
  const minPx = Math.round(Math.max(600, narrowCh * 7.5 + textCols * 150));
  const T = Math.max(minPx, 1000);
  const narrowPct = meta.reduce((a, m) => a + (m.narrow ? (m.ch * 8) / T * 100 : 0), 0);
  const head = meta.map((m) => {
    const base = (13 * 8) / T * 100; // every text column keeps at least about 13 characters
    const pct = m.narrow ? (m.ch * 8) / T * 100 : base + Math.max(0, 100 - narrowPct - base * textCols) * (m.weight / totalW);
    return "<th class=\"" + (m.kind === "num" ? "num" : "") + "\" style=\"width:" + pct.toFixed(2) + "%\">" + esc(m.c.label) + "</th>";
  }).join("");
  const cell = (m, r) => {
    const raw = text(r[m.c.key]);
    switch (m.kind) {
      case "code": return "<td class=\"mono\"><code>" + esc(raw) + "</code></td>";
      case "link": return raw ? "<td><a href=\"" + esc(raw) + "\" target=\"_blank\" rel=\"noopener\">" + esc(m.shown(r)) + "</a></td>" : "<td></td>";
      case "pill": return "<td class=\"nowrap\"><span class=\"pill\">" + esc(raw) + "</span></td>";
      case "num": return "<td class=\"num\">" + esc(raw) + "</td>";
      case "muted": return "<td class=\"muted\">" + esc(raw) + "</td>";
      case "nowrap": return "<td class=\"nowrap\">" + esc(raw) + "</td>";
      default: return "<td>" + esc(raw) + "</td>";
    }
  };
  const body = rows.map((r) => "<tr>" + meta.map((m) => cell(m, r)).join("") + "</tr>").join("");
  const tall = rows.length > (opts.tallAfter || 8) ? " tall" : "";
  return "<div class=\"tbl" + tall + "\"><div class=\"tbl-scroll\" tabindex=\"0\" role=\"region\" aria-label=\"" + esc(opts.label || "table") + "\"><table style=\"min-width:" + minPx + "px\"><thead><tr>" + head + "</tr></thead><tbody>" + body + "</tbody></table></div></div>" + (opts.caption ? "<p class=\"tblcap\">" + esc(opts.caption) + "</p>" : "");
}

/* ---------- pieces ---------- */
const li = (arr) => '<ul>' + arr.map((x) => `<li>${esc(x)}</li>`).join('') + '</ul>';
const codeify = (s) => esc(s).replace(/((?:[A-Za-z0-9_.\-]+\/)+[A-Za-z0-9_.\-]+|[A-Za-z0-9_]+\.(?:c|h|y|l|js|ts|tsx|py|go|rs|java|md|json|sql|sgml|yml|yaml|toml|sh))/g, '<code>$1</code>');
const ROLE = { architecture: 'How the parts connect', lifecycle: 'Follow it step by step', structure: 'Anatomy' };
const { inject: injectLogos } = require('./logos.js');
// optional: diagram-types/catalog.json gives each meta "type" slug a readable name for the chip on the figure
const CATALOG = (() => { const f = path.join(HERE, '..', '..', '..', 'diagram-types', 'catalog.json'); try { return Object.fromEntries(readJson(f).map((t) => [t.slug, t.name])); } catch (e) { return {}; } })();

let autoDiagram = null;
function fallbackFigure(key, spec) {
  if (!autoDiagram) autoDiagram = require('./layout.js')(clean, esc);
  const d = autoDiagram(spec, key);
  return `<figure class="fig"><div class="figscroll">${d.svg}</div><div class="legend">${d.legend}</div><figcaption>${esc(spec.claim)}</figcaption></figure>`;
}
function figures(key) {
  const dir = DIAGRAMS && path.join(DIAGRAMS, key);
  const metaFile = dir && path.join(dir, 'meta.json');
  if (metaFile && fs.existsSync(metaFile)) {
    const meta = readJson(metaFile);
    return '<div class="figs">' + meta.map((d) => {
      const f = path.join(dir, d.file);
      if (!fs.existsSync(f)) return '';
      const svg = injectLogos(fs.readFileSync(f, 'utf8').replace(/<\?xml[^>]*\?>/, '').trim());
      const slug = d.type ? d.type.split('/').pop() : ''; // accept "layered-architecture" or "software/layered-architecture"
      const chip = slug ? `<span class="ftype">${esc(CATALOG[slug] || slug.replace(/-/g, ' '))}</span>` : '';
      const badges = d.badges && d.badges.length ? `<ol class="badges">${d.badges.map((b) => `<li value="${b.n}">${esc(b.meaning)}</li>`).join('')}</ol>` : '';
      return `<figure class="fig">${chip}<h4>${esc(ROLE[d.role] || d.role)}: ${esc(d.title)}</h4><button class="fzoom" type="button" aria-label="Open full size: ${esc(d.title)}">Full size</button><div class="figscroll">${svg}</div>${badges}<figcaption>${esc(d.caption)}</figcaption></figure>`;
    }).join('') + '</div>';
  }
  const t = topics[key];
  return t.diagram && t.diagram.nodes && t.diagram.nodes.length ? `<div class="figs">${fallbackFigure(key, t.diagram)}</div>` : '';
}

function section(key, idx) {
  const r = topics[key];
  let h = `<section class="topic" id="${esc(key)}"><header class="th"><p class="kicker">Part ${idx + 1} of ${ORDER.length}</p><h2>${esc(r.title)}</h2><p class="lede">${esc(r.one_liner)}</p>${r.analogy ? `<p class="analogy"><b>Think of it like this.</b> ${esc(r.analogy)}</p>` : ''}</header>`;
  h += `<div class="cols"><div class="card"><h3>The idea in plain words</h3>${li(r.big_picture || [])}</div>`;
  if (r.glossary && r.glossary.length) h += `<div class="card soft"><h3>Words you will hear</h3><dl class="gl">${r.glossary.map((g) => `<dt>${esc(g.term)}</dt><dd>${esc(g.meaning)}</dd>`).join('')}</dl></div>`;
  h += '</div>' + figures(key);
  if (r.flow && r.flow.length) h += `<h3 class="sub">Step by step through the code</h3><ol class="flow">${r.flow.map((f) => `<li><div class="st">${esc(f.step)}</div><p>${esc(f.detail)}</p><div class="wh">${codeify(f.where)}</div></li>`).join('')}</ol>`;
  if (r.file_tree && r.file_tree.length) h += `<h3 class="sub">What you will actually see on disk</h3>` + table([{ key: 'path', label: 'Path', kind: 'code' }, { key: 'what', label: 'What it is' }], r.file_tree, { label: 'files on disk' });
  if (r.try_it && r.try_it.length) h += `<h3 class="sub">Try it yourself</h3>` + table([{ key: 'cmd', label: 'Command', kind: 'code' }, { key: 'shows', label: 'What it shows' }], r.try_it, { label: 'commands to try', caption: cfg.tryItNote || '' });
  if (r.interview && r.interview.length) {
    h += `<h3 class="sub">Interview me on this</h3><p class="hint">Try to answer out loud first, then open the question. Tick it when you could explain it to a friend.</p><div class="qa">`;
    r.interview.forEach((q, i) => {
      const qid = `${key}-${i}`;
      h += `<details class="q" data-qid="${esc(qid)}"><summary><span class="qn">Q${i + 1}</span><span class="qt">${esc(q.q)}</span><label class="know" title="I can explain this"><input type="checkbox" id="k-${esc(qid)}" data-k="${esc(qid)}"><span>Got it</span></label></summary><div class="ans">${li(q.answer)}${q.trap ? `<p class="trap"><b>Common trap.</b> ${esc(q.trap)}</p>` : ''}</div></details>`;
    });
    h += '</div>';
  }
  if (r.more && r.more.length) h += `<div class="card more"><h3>Be ready for these follow-ups too</h3>${li(r.more)}</div>`;
  if (r.key_files && r.key_files.length) h += `<h3 class="sub">Files to open first</h3>` + table([{ key: 'path', label: 'File', kind: 'code' }, { key: 'what', label: 'What to look for' }], r.key_files, { label: 'key files' });
  if (r.contributor_tips && r.contributor_tips.length) h += `<div class="card tips"><h3>If you want to contribute here</h3>${li(r.contributor_tips)}</div>`;
  return h + '</section>';
}

function extraSection(s) {
  let h = `<section class="topic" id="${esc(s.id)}"><header class="th">${s.kicker ? `<p class="kicker">${esc(s.kicker)}</p>` : ''}<h2>${esc(s.title)}</h2>${s.lede ? `<p class="lede">${esc(s.lede)}</p>` : ''}</header>`;
  if (s.table) {
    const rows = readJson(rel(s.table.file));
    h += table(s.table.columns, rows, { label: s.title, tallAfter: s.table.tallAfter || 8, caption: s.table.caption });
  }
  if (s.htmlFile) h += fs.readFileSync(rel(s.htmlFile), 'utf8');
  return h + '</section>';
}

/* ---------- assemble ---------- */
const extras = cfg.extraSections || [];
let nav = '<a href="#top" data-nav="top"><span>0</span>Start here</a>'; let n = 0;
groups.forEach((g) => { nav += `<p class="ng">${esc(g.name)}</p>`; g.topics.forEach((k) => { n++; nav += `<a href="#${esc(k)}" data-nav="${esc(k)}"><span>${n}</span>${esc(short(k))}<em data-count="${esc(k)}"></em></a>`; }); });
if (extras.length) { nav += '<p class="ng">Next</p>'; extras.forEach((s) => { nav += `<a href="#${esc(s.id)}" data-nav="${esc(s.id)}"><span>+</span>${esc(s.navLabel || s.title)}</a>`; }); }
const total = ORDER.reduce((a, k) => a + ((topics[k].interview || []).length), 0);

const how = (cfg.how || []).length ? `<div class="how">${cfg.how.map((x) => `<div><b>${esc(x.title)}</b><p>${esc(x.text)}</p></div>`).join('')}</div>` : '';
const life = cfg.lifecycle ? `<h2 class="mini">${esc(cfg.lifecycle.title)}</h2><ol class="life">${cfg.lifecycle.steps.map((l) => `<li><a href="#${esc(l.topic)}"><b>${esc(l.name)}</b><p>${esc(l.text)}</p></a></li>`).join('')}</ol>` : '';
const callouts = (cfg.callouts || []).map((c) => `<div class="card ${c.style === 'more' ? 'more' : 'soft'} rules"><h3>${esc(c.title)}</h3><ul>${c.items.map((i) => `<li>${i.bold ? `<b>${esc(i.bold)}</b> ` : ''}${esc(i.text)}</li>`).join('')}</ul></div>`).join('');
const hero = `<section class="hero"><p class="kicker">${esc(cfg.kicker || '')}</p><h1>${esc(cfg.heroTitle || cfg.title)}</h1><p class="lede wide">${esc(cfg.heroLede || '')}</p>${how}${cfg.overviewKey ? figures(cfg.overviewKey) : ''}${life}${callouts}</section>`;

const css = fs.readFileSync(path.join(ASSETS, 'style.css'), 'utf8');
const js = fs.readFileSync(path.join(ASSETS, 'app.js'), 'utf8');
const brand = `<div class="brand"><svg viewBox="0 0 40 40" width="30" height="30" aria-hidden="true"><path d="M20 4 L34 12 V28 L20 36 L6 28 V12 Z" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"/><path d="M6 12 L20 20 L34 12 M20 20 V36" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg><div><b>${esc(cfg.title)}</b><small>${esc(cfg.brandSub || '')}</small></div></div>`;
const side = `<aside class="side" id="side">${brand}<nav aria-label="Sections">${nav}</nav><div class="prog"><div class="bar"><i id="bar"></i></div><small><b id="done">0</b> of ${total} interview questions ticked</small></div><button class="btn" id="toggleAll" type="button">Open all answers</button><div class="dsw" role="group" aria-label="Diagram style"><button type="button" data-ds="hand" aria-pressed="false">Hand-drawn</button><button type="button" data-ds="clean" aria-pressed="false">Clean</button></div><button class="btn ghost" id="theme" type="button">Switch theme</button></aside>`;
const DSTYLE = cfg.diagramStyle === 'clean' ? 'clean' : 'hand';
const filters = fs.readFileSync(path.join(ASSETS, 'filters.svg'), 'utf8').trim();

const html = `<title>${esc(cfg.title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700&family=Figtree:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap">
<style>${css}</style>
${filters}
<div class="shell" id="shell" data-dstyle="${DSTYLE}">
${side}
<main class="main" id="top">
${hero}
${ORDER.map((k, i) => section(k, i)).join('\n')}
${extras.map(extraSection).join('\n')}
<footer class="foot"><p>${esc(cfg.footer || '')}</p></footer>
</main>
<dialog class="zoomdlg" id="zoomdlg" aria-label="Diagram, full size"><button class="btn ghost" type="button" id="zoomclose">Close</button><div class="zoombody" id="zoombody"></div></dialog>
</div>
<script>window.EXPLORER_KEY=${JSON.stringify(cfg.storageKey || 'explorer-known')};</script>
<script>${js}</script>`;

fs.writeFileSync(args.out, clean(html));
const svgs = (html.match(/<svg /g) || []).length;
const problems = [/="NaN"/, /NaN(%|ch|px)/, /="undefined"/, />undefined</].filter((re) => re.test(html)).map(String);
if (html.length > 4 * 1024 * 1024) console.warn(`warning: ${args.out} is ${Math.round(html.length / 1048576)} MB; logo-heavy diagrams inline every logo, so trim logo slots or split the guide`);
console.log(`wrote ${args.out}: ${Math.round(html.length / 1024)} KB, ${ORDER.length} topics, ${svgs} svgs, ${total} questions${problems.length ? ', PROBLEMS: ' + problems.join(',') : ''}`);
