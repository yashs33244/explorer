// top-to-bottom layered diagram, returns inline SVG string + legend
module.exports = function makeDiagram(clean, esc) {
  return function diagram(spec, idp) {
    const nodes = spec.nodes.map((n, i) => ({ ...n, i }));
    const id2 = Object.fromEntries(nodes.map((n) => [n.id, n]));
    const edges = spec.edges.filter((e) => id2[e.from] && id2[e.to]);
    const color = {}; const back = new Set();
    const out = {}; nodes.forEach((n) => (out[n.id] = []));
    edges.forEach((e, k) => out[e.from].push([e.to, k]));
    const dfs = (u) => { color[u] = 1; for (const [v, k] of out[u]) { if (color[v] === 1) back.add(k); else if (!color[v]) dfs(v); } color[u] = 2; };
    const indeg = {}; nodes.forEach((n) => (indeg[n.id] = 0)); edges.forEach((e) => indeg[e.to]++);
    nodes.filter((n) => indeg[n.id] === 0).forEach((n) => !color[n.id] && dfs(n.id));
    nodes.forEach((n) => !color[n.id] && dfs(n.id));
    const preds = {}; nodes.forEach((n) => (preds[n.id] = []));
    edges.forEach((e, k) => { if (!back.has(k) && e.from !== e.to) preds[e.to].push(e.from); });
    const layer = {};
    const L = (id, stack = []) => { if (layer[id] != null) return layer[id]; if (stack.includes(id)) return 0; layer[id] = 0; let m = 0; for (const p of preds[id]) m = Math.max(m, L(p, [...stack, id]) + 1); layer[id] = m; return m; };
    nodes.forEach((n) => L(n.id));
    const nl = Math.max(...nodes.map((n) => layer[n.id])) + 1;
    const rows = Array.from({ length: nl }, () => []);
    nodes.forEach((n) => rows[layer[n.id]].push(n));
    const pos = {};
    rows.forEach((c) => c.forEach((n, i) => (pos[n.id] = i)));
    for (let pass = 0; pass < 3; pass++) {
      for (let l = 1; l < nl; l++) {
        rows[l].forEach((n) => { const ps = preds[n.id]; n._b = ps.length ? ps.reduce((a, p) => a + pos[p], 0) / ps.length : pos[n.id]; });
        rows[l].sort((a, b) => a._b - b._b || a.i - b.i);
        rows[l].forEach((n, i) => (pos[n.id] = i));
      }
    }
    const W = 158, H = 44, GX = 46, GYL = 62, PX = 16, PY = 14, PADR = 110;
    const maxCols = Math.max(...rows.map((c) => c.length));
    const fullW = maxCols * W + (maxCols - 1) * GX;
    const rowW = (c) => c.length * W + (c.length - 1) * GX;
    nodes.forEach((n) => {
      const c = rows[layer[n.id]];
      n.x = PX + (fullW - rowW(c)) / 2 + pos[n.id] * (W + GX);
      n.y = PY + layer[n.id] * (H + GYL);
    });
    const width = PX + fullW + PADR;
    const height = PY * 2 + nl * H + (nl - 1) * GYL;
    const groups = []; nodes.forEach((n) => { const g = n.group || 'Other'; if (!groups.includes(g)) groups.push(g); });
    const gi = (n) => groups.indexOf(n.group || 'Other') % 6;
    let svg = `<svg viewBox="0 0 ${width} ${height}" role="img" aria-label="${esc(spec.claim)}" xmlns="http://www.w3.org/2000/svg"><defs><marker id="ar-${idp}" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,1 L9,5 L0,9 z" fill="currentColor"/></marker></defs>`;
    const labels = [];
    let loop = 0;
    edges.forEach((e, k) => {
      const a = id2[e.from], b = id2[e.to];
      let d, lx, ly, anchor = 'middle';
      if (layer[a.id] < layer[b.id]) {
        const x1 = a.x + W / 2, y1 = a.y + H, x2 = b.x + W / 2, y2 = b.y;
        const dy = (y2 - y1) * 0.5;
        d = `M${x1},${y1} C${x1},${y1 + dy} ${x2},${y2 - dy} ${x2},${y2}`;
        const t = layer[b.id] - layer[a.id] > 1 ? 0.2 : 0.5;
        const mt = 1 - t;
        lx = mt ** 3 * x1 + 3 * mt * mt * t * x1 + 3 * mt * t * t * x2 + t ** 3 * x2;
        ly = mt ** 3 * y1 + 3 * mt * mt * t * (y1 + dy) + 3 * mt * t * t * (y2 - dy) + t ** 3 * y2;
        if (Math.abs(x2 - x1) > 8) { lx = lx; }
      } else {
        const x1 = a.x + W, y1 = a.y + H / 2, x2 = b.x + W, y2 = b.y + H / 2;
        const bx = PX + fullW + 22 + (loop++ % 3) * 6;
        d = `M${x1},${y1} C${bx + 30},${y1} ${bx + 30},${y2} ${x2},${y2}`;
        lx = bx + 12; ly = (y1 + y2) / 2 - 4; anchor = 'start';
        if (a.id === b.id) { ly = y1; }
      }
      svg += `<path d="${d}" class="edge" fill="none" marker-end="url(#ar-${idp})"/>`;
      labels.push(`<text x="${lx.toFixed(1)}" y="${(ly + 4).toFixed(1)}" text-anchor="${anchor}" class="elabel">${esc(e.label)}</text>`);
    });
    nodes.forEach((n) => {
      const words = clean(n.label).split(' '); let l1 = '', l2 = '';
      words.forEach((w) => { if (!l2 && (l1 + ' ' + w).trim().length <= 21) l1 = (l1 + ' ' + w).trim(); else l2 = (l2 + ' ' + w).trim(); });
      svg += `<g class="node g${gi(n)}"><rect x="${n.x}" y="${n.y}" width="${W}" height="${H}" rx="14"/>`;
      if (l2) svg += `<text x="${n.x + W / 2}" y="${n.y + H / 2 - 3}" text-anchor="middle">${esc(l1)}</text><text x="${n.x + W / 2}" y="${n.y + H / 2 + 11}" text-anchor="middle">${esc(l2)}</text>`;
      else svg += `<text x="${n.x + W / 2}" y="${n.y + H / 2 + 4.5}" text-anchor="middle">${esc(l1)}</text>`;
      svg += `</g>`;
    });
    svg += labels.join('') + '</svg>';
    const legend = groups.map((g, i) => `<span class="chip g${i % 6}"><i></i>${esc(g)}</span>`).join('');
    return { svg, legend, width, height };
  };
};
