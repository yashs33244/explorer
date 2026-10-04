(function () {
  var KEY = window.EXPLORER_KEY || 'explorer-known';
  var known = {};
  try { known = JSON.parse(localStorage.getItem(KEY) || '{}') || {}; } catch (e) { known = {}; }
  function save() { try { localStorage.setItem(KEY, JSON.stringify(known)); } catch (e) {} }
  var boxes = document.querySelectorAll('input[data-k]');
  var total = boxes.length;
  function render() {
    var done = 0, per = {};
    boxes.forEach(function (b) {
      var id = b.getAttribute('data-k');
      var topic = id.split('-')[0];
      per[topic] = per[topic] || { d: 0, t: 0 };
      per[topic].t++;
      b.checked = !!known[id];
      var q = b.closest('.q');
      if (q) q.classList.toggle('done', b.checked);
      if (b.checked) { done++; per[topic].d++; }
    });
    document.getElementById('done').textContent = done;
    document.getElementById('bar').style.width = (total ? (done / total) * 100 : 0) + '%';
    document.querySelectorAll('[data-count]').forEach(function (el) {
      var p = per[el.getAttribute('data-count')];
      el.textContent = p ? p.d + '/' + p.t : '';
    });
  }
  boxes.forEach(function (b) {
    b.addEventListener('click', function (e) { e.stopPropagation(); });
    b.addEventListener('change', function () {
      var id = b.getAttribute('data-k');
      if (b.checked) known[id] = 1; else delete known[id];
      save(); render();
    });
  });
  document.querySelectorAll('.know').forEach(function (l) {
    l.addEventListener('click', function (e) { e.stopPropagation(); });
  });
  render();

  var open = false;
  var tg = document.getElementById('toggleAll');
  tg.addEventListener('click', function () {
    open = !open;
    document.querySelectorAll('details.q').forEach(function (d) { d.open = open; });
    tg.textContent = open ? 'Hide all answers' : 'Open all answers';
  });

  var root = document.documentElement;
  var themeBtn = document.getElementById('theme');
  themeBtn.addEventListener('click', function () {
    var cur = root.getAttribute('data-theme');
    if (!cur) cur = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    root.setAttribute('data-theme', cur === 'dark' ? 'light' : 'dark');
  });

  // diagram style: hand-drawn or clean, remembered per viewer
  var shell = document.getElementById('shell');
  var DS_KEY = KEY + '-dstyle';
  function setStyle(v) {
    shell.setAttribute('data-dstyle', v);
    document.querySelectorAll('[data-ds]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-ds') === v)); });
  }
  var savedDs = null; try { savedDs = localStorage.getItem(DS_KEY); } catch (e) {}
  setStyle(savedDs === 'hand' || savedDs === 'clean' ? savedDs : shell.getAttribute('data-dstyle') || 'hand');
  document.querySelectorAll('[data-ds]').forEach(function (b) {
    b.addEventListener('click', function () { var v = b.getAttribute('data-ds'); setStyle(v); try { localStorage.setItem(DS_KEY, v); } catch (e) {} });
  });

  // full-size view of one diagram
  var dlg = document.getElementById('zoomdlg'), body = document.getElementById('zoombody');
  document.querySelectorAll('.fzoom').forEach(function (b) {
    b.addEventListener('click', function () {
      var svg = b.parentNode.querySelector('svg'); if (!svg || !dlg.showModal) return;
      // the dialog sits in #shell, so it follows the page style; a figure with its own data-dstyle passes it on
      var own = b.parentNode.getAttribute('data-dstyle');
      if (own) dlg.setAttribute('data-dstyle', own); else dlg.removeAttribute('data-dstyle');
      var h = b.parentNode.querySelector('h4');
      dlg.setAttribute('aria-label', (h ? h.textContent : 'Diagram') + ', full size');
      body.innerHTML = ''; body.appendChild(svg.cloneNode(true)); dlg.showModal();
    });
  });
  document.getElementById('zoomclose').addEventListener('click', function () { dlg.close(); });
  dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); });

  var links = {};
  document.querySelectorAll('[data-nav]').forEach(function (a) { links[a.getAttribute('data-nav')] = a; });
  var targets = Object.keys(links).map(function (k) { return document.getElementById(k); }).filter(Boolean);
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          Object.keys(links).forEach(function (k) { links[k].classList.toggle('on', k === en.target.id); });
        }
      });
    }, { rootMargin: '-20% 0px -70% 0px' });
    targets.forEach(function (t) { io.observe(t); });
  }
})();
