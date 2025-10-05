// Chart Navigation - CSP Compliant
// Handles back button functionality for standalone chart pages

(function() {
    'use strict';

    // Event delegation for chart back button
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('chart-back-link') ||
            e.target.getAttribute('data-action') === 'chart-back') {
            e.preventDefault();
            window.history.back();
        }
    });
})();
