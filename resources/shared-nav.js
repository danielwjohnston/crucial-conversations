/*
  ============================================================================
  Shared Navigation Injector — Resource Pages
  ============================================================================
  Dynamically injects a sticky nav bar, breadcrumbs, and footer into any
  resource page. Each page sets window.CC_NAV_CONFIG before loading this
  script to customize the breadcrumb trail and active nav link.

  Usage in any resource page <head>:
    <link rel="stylesheet" href="[path]/shared-nav.css">

  Usage before </body>:
    <script>
      window.CC_NAV_CONFIG = {
        breadcrumbs: [
          { label: 'Home', href: '[path]/index.html' },
          { label: 'Resources', href: '[path]/resources/index.html' },
          { label: 'Current Page' }   // no href = current (last item)
        ],
        activeNav: 'resources'  // 'home', 'chapters', 'resources', 'facilitator'
      };
    </script>
    <script src="[path]/shared-nav.js"></script>
  ============================================================================
*/

(function () {
  'use strict';

  var config = window.CC_NAV_CONFIG || {};
  var breadcrumbs = config.breadcrumbs || [];
  var activeNav = config.activeNav || '';

  // --- Determine relative path to site root ---
  // We figure this out from the first breadcrumb's href if it points to index.html
  var rootPath = '';
  if (breadcrumbs.length > 0 && breadcrumbs[0].href) {
    rootPath = breadcrumbs[0].href.replace(/index\.html$/, '');
  }

  // --- Build nav bar ---
  var navLinks = [
    { id: 'home', label: 'Home', href: rootPath + 'index.html' },
    { id: 'chapters', label: 'Chapters', href: rootPath + 'index.html#chapters' },
    { id: 'resources', label: 'Resources', href: rootPath + 'resources/index.html' },
    { id: 'facilitator', label: 'Facilitator Guide', href: rootPath + 'facilitator_guide/index.html' }
  ];

  var navHtml = '<nav class="site-nav" role="navigation" aria-label="Site navigation">' +
    '<div class="site-nav-inner">' +
    '<a href="' + rootPath + 'index.html" class="site-nav-brand">Crucial Conversations</a>' +
    '<div class="site-nav-links">';

  for (var i = 0; i < navLinks.length; i++) {
    var link = navLinks[i];
    var cls = link.id === activeNav ? ' class="active"' : '';
    navHtml += '<a href="' + link.href + '"' + cls + '>' + link.label + '</a>';
  }

  navHtml += '</div></div></nav>';

  // --- Build breadcrumbs ---
  var bcHtml = '';
  if (breadcrumbs.length > 0) {
    bcHtml = '<div class="site-breadcrumbs" aria-label="Breadcrumb">';
    for (var j = 0; j < breadcrumbs.length; j++) {
      var crumb = breadcrumbs[j];
      if (j > 0) bcHtml += '<span class="sep">›</span>';
      if (crumb.href && j < breadcrumbs.length - 1) {
        bcHtml += '<a href="' + crumb.href + '">' + crumb.label + '</a>';
      } else {
        bcHtml += '<span>' + crumb.label + '</span>';
      }
    }
    bcHtml += '</div>';
  }

  // --- Build footer ---
  var footerHtml = '<footer class="site-footer">' +
    '<a href="' + rootPath + 'index.html">Home</a>' +
    '<a href="' + rootPath + 'resources/index.html">Resources</a>' +
    '<a href="' + rootPath + 'resources/glossary.html">Glossary</a>' +
    '<a href="https://github.com/danielwjohnston/crucial-conversations" target="_blank">GitHub</a>' +
    '<div style="margin-top:8px;">&copy; 2026 Crucial Conversations Leadership Training</div>' +
    '</footer>';

  // --- Inject into page ---
  // Nav + breadcrumbs go at very top of <body>
  var body = document.body;
  var wrapper = document.createElement('div');
  wrapper.innerHTML = navHtml + bcHtml;

  // Insert before first child of body
  if (body.firstChild) {
    body.insertBefore(wrapper, body.firstChild);
  } else {
    body.appendChild(wrapper);
  }

  // Unwrap (move children out of wrapper div)
  while (wrapper.firstChild) {
    body.insertBefore(wrapper.firstChild, wrapper);
  }
  body.removeChild(wrapper);

  // Footer: replace existing site-footer or append
  var existingFooter = document.querySelector('.site-footer, footer:last-of-type');
  if (existingFooter && existingFooter.tagName === 'FOOTER') {
    existingFooter.outerHTML = footerHtml;
  } else {
    body.insertAdjacentHTML('beforeend', footerHtml);
  }

  // --- Add body padding-top to account for sticky nav ---
  // The nav is ~48px, breadcrumbs ~30px
  var navEl = document.querySelector('.site-nav');
  if (navEl) {
    var navHeight = navEl.offsetHeight;
    var bcEl = document.querySelector('.site-breadcrumbs');
    var bcHeight = bcEl ? bcEl.offsetHeight : 0;
    body.style.paddingTop = (navHeight + bcHeight) + 'px';
  }
})();
