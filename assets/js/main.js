/* Small progressive enhancements: theme memory, language switch, scrollspy, footer year. */
(function () {
  'use strict';

  var root = document.documentElement;

  /* ── Theme ───────────────────────────────────────────────── */
  var STORE = 'pc-theme';
  var btn = document.querySelector('.theme');
  var label = btn && btn.querySelector('.theme__label');

  /* The button carries its own wording, so each language page reads right. */
  var wordDark = (btn && btn.getAttribute('data-label-dark')) || 'Dark';
  var wordLight = (btn && btn.getAttribute('data-label-light')) || 'Light';

  function apply(theme) {
    root.setAttribute('data-theme', theme);
    if (label) label.textContent = theme === 'dark' ? wordLight : wordDark;
    if (btn) btn.setAttribute('aria-pressed', String(theme === 'dark'));
  }

  var saved = null;
  try { saved = localStorage.getItem(STORE); } catch (e) { /* private mode */ }
  var prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  apply(saved || (prefersDark ? 'dark' : 'light'));

  if (btn) {
    btn.addEventListener('click', function () {
      var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      apply(next);
      try { localStorage.setItem(STORE, next); } catch (e) { /* ignore */ }
    });
  }

  /* ── Language switch ─────────────────────────────────────── */
  /* Each language is its own page (/ and /pt/). Carry the current
     section anchor across so the reader lands where they were. */
  var langLinks = document.querySelectorAll('.lang a');
  Array.prototype.forEach.call(langLinks, function (a) {
    a.addEventListener('click', function () {
      var hash = window.location.hash;
      if (hash && hash.length > 1) a.setAttribute('href', a.getAttribute('href').split('#')[0] + hash);
    });
  });

  /* ── Scrollspy ───────────────────────────────────────────── */
  var links = Array.prototype.slice.call(document.querySelectorAll('.rail__nav a'));
  var sections = links
    .map(function (a) { return document.querySelector(a.getAttribute('href')); })
    .filter(Boolean);

  if (sections.length && 'IntersectionObserver' in window) {
    var visible = new Set();

    var setActive = function (id) {
      links.forEach(function (a) {
        a.classList.toggle('is-active', a.getAttribute('href') === '#' + id);
      });
    };

    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) visible.add(entry.target.id);
        else visible.delete(entry.target.id);
      });
      // Highlight the topmost section currently in the reading band.
      for (var i = 0; i < sections.length; i++) {
        if (visible.has(sections[i].id)) { setActive(sections[i].id); return; }
      }
    }, { rootMargin: '-12% 0px -70% 0px', threshold: 0 });

    sections.forEach(function (s) { observer.observe(s); });
  }

  /* ── Footer year ─────────────────────────────────────────── */
  var year = document.getElementById('year');
  if (year) year.textContent = String(new Date().getFullYear());
})();
