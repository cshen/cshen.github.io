/**
 * theme_toggle.js
 * Handles:
 *   1. Dark/light theme toggle with localStorage persistence
 *   2. Immediate theme application (no flash of wrong theme)
 *   3. Mobile hamburger navigation
 */
(function () {
  'use strict';

  var STORAGE_KEY = 'cs-theme';

  /* ----------------------------------------------------------
   * Apply theme: set data-theme on <html> and update button icon
   * ---------------------------------------------------------- */
  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);

    var icon = document.getElementById('theme-icon');
    var btn  = document.getElementById('theme-toggle');
    if (!icon || !btn) { return; }

    if (theme === 'dark') {
      icon.className = 'fa fa-sun-o';
      btn.title = 'Switch to light theme';
      btn.setAttribute('aria-label', 'Switch to light theme');
    } else {
      icon.className = 'fa fa-moon-o';
      btn.title = 'Switch to dark theme';
      btn.setAttribute('aria-label', 'Switch to dark theme');
    }
  }

  function toggleTheme() {
    var current = document.documentElement.getAttribute('data-theme') || 'light';
    var next    = current === 'dark' ? 'light' : 'dark';
    try { localStorage.setItem(STORAGE_KEY, next); } catch (e) {}
    applyTheme(next);
  }

  /* ----------------------------------------------------------
   * Immediately apply saved / preferred theme (before paint)
   * ---------------------------------------------------------- */
  var savedTheme = null;
  try { savedTheme = localStorage.getItem(STORAGE_KEY); } catch (e) {}
  if (!savedTheme && window.matchMedia &&
      window.matchMedia('(prefers-color-scheme: dark)').matches) {
    savedTheme = 'dark';
  }
  if (savedTheme) {
    document.documentElement.setAttribute('data-theme', savedTheme);
  }

  /* ----------------------------------------------------------
   * DOM-ready: wire up buttons
   * ---------------------------------------------------------- */
  document.addEventListener('DOMContentLoaded', function () {

    /* Theme toggle button */
    var btn = document.getElementById('theme-toggle');
    if (btn) {
      btn.addEventListener('click', toggleTheme);
      /* Sync icon with the theme that was applied before DOM was ready */
      var current = document.documentElement.getAttribute('data-theme') || 'light';
      applyTheme(current);
    }

    /* Hamburger / mobile nav */
    var hamburger = document.getElementById('menu-toggle');
    var nav       = document.getElementById('nav');
    if (hamburger && nav) {
      hamburger.addEventListener('click', function () {
        var isOpen = nav.classList.toggle('nav-open');
        hamburger.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
        hamburger.classList.toggle('active', isOpen);
      });

      /* Close nav when any nav link is tapped */
      var links = nav.getElementsByTagName('a');
      for (var i = 0; i < links.length; i++) {
        links[i].addEventListener('click', function () {
          nav.classList.remove('nav-open');
          hamburger.setAttribute('aria-expanded', 'false');
          hamburger.classList.remove('active');
        });
      }
    }
  });
}());
