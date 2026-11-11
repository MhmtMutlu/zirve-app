/* Zirve · web. Progressive enhancement only: every page works without this file. No cookies, no network requests. */
(function () {
  'use strict';

  // Header border after scrolling.
  var nav = document.querySelector('.nav');
  if (nav) {
    var onScroll = function () { nav.classList.toggle('is-scrolled', window.scrollY > 8); };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  // <details> menus: close on Escape, on an outside click and after following a link inside.
  var menus = [].slice.call(document.querySelectorAll('details.menu, details.langs'));
  var closeAll = function (except) {
    menus.forEach(function (d) { if (d !== except) { d.removeAttribute('open'); } });
  };
  document.addEventListener('click', function (e) {
    var inside = e.target.closest ? e.target.closest('details.menu, details.langs') : null;
    closeAll(inside);
    if (inside && e.target.closest('a')) { inside.removeAttribute('open'); }
  });
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') { return; }
    menus.forEach(function (d) {
      if (d.hasAttribute('open')) { d.removeAttribute('open'); d.querySelector('summary').focus(); }
    });
  });

  // Language hint (plan §4.6): no automatic redirect. When this page exists in a language the visitor prefers more
  // than the current one, show a dismissible strip in that language. Fixed to the bottom, so it never shifts layout.
  var KEY = 'zirve.langhint.dismissed';
  var read = function () { try { return window.sessionStorage.getItem(KEY); } catch (e) { return null; } };
  var dismiss = function () { try { window.sessionStorage.setItem(KEY, '1'); } catch (e) { /* storage unavailable: hide for this view only */ } };
  if (read()) { return; }
  var primary = function (tag) { return (tag || '').toLowerCase().split('-')[0]; };
  var current = (document.documentElement.lang || '').toLowerCase();
  var links = [].slice.call(document.querySelectorAll('.langs a[data-alternate]'));
  var prefs = (navigator.languages && navigator.languages.length) ? navigator.languages : [navigator.language || ''];
  var match = null;
  for (var i = 0; i < prefs.length && !match; i++) {
    var pref = (prefs[i] || '').toLowerCase();
    if (pref === current || primary(pref) === primary(current)) { return; }  // already in a preferred language
    for (var j = 0; j < links.length; j++) {
      var tag = links[j].getAttribute('hreflang').toLowerCase();
      if (tag === pref || primary(tag) === primary(pref)) { match = links[j]; break; }
    }
  }
  if (!match) { return; }
  var strip = document.createElement('div');
  strip.className = 'langhint';
  strip.setAttribute('role', 'region');
  strip.setAttribute('lang', match.getAttribute('lang'));
  strip.setAttribute('aria-label', match.textContent);
  var text = document.createElement('span');
  text.textContent = match.getAttribute('data-hint') + ' ';
  var link = document.createElement('a');
  link.href = match.getAttribute('href');
  link.hreflang = match.getAttribute('hreflang');
  link.textContent = match.textContent;
  text.appendChild(link);
  var close = document.createElement('button');
  close.type = 'button';
  close.setAttribute('aria-label', match.getAttribute('data-close'));
  close.textContent = '✕';
  close.addEventListener('click', function () { dismiss(); strip.remove(); });
  strip.appendChild(text);
  strip.appendChild(close);
  document.body.appendChild(strip);
})();
