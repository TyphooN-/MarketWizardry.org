// JSON-LD structured data for 404.html - CSP compliant
(function() {
    'use strict';

    const jsonLdData = {
    "@context": "https://schema.org",
    "@type": "WebPage",
    "name": "404 - Page Not Found",
    "description": "Page not found on MarketWizardry.org. Navigate back to trading tools and market analysis platforms.",
    "url": "https://marketwizardry.org/404.html"
};

    // Inject JSON-LD into page
    const script = document.createElement('script');
    script.type = 'application/ld+json';
    script.textContent = JSON.stringify(jsonLdData, null, 2);
    document.head.appendChild(script);
})();
