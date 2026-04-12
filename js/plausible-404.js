(function () {
    'use strict';
    // Queue-based API pattern — works before plausible.js has loaded
    window.plausible = window.plausible || function () {
        (window.plausible.q = window.plausible.q || []).push(arguments);
    };
    window.plausible('404', { props: { path: document.location.pathname } });
})();
