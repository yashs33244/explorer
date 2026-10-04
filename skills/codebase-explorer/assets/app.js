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
