// JSON-LD structured data for market-wizardry.html - CSP compliant
(function() {
    'use strict';

    const jsonLdData = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "name": "Market Wizardry - Financial Trading Tools",
    "description": "Professional financial trading tools, market analysis platforms, and quantitative research software. Free tools for traders and investors.",
    "url": "https://marketwizardry.org/market-wizardry.html",
    "author": {
        "@type": "Person",
        "name": "TyphooN"
    }
};

    // Inject JSON-LD into page
    const script = document.createElement('script');
    script.type = 'application/ld+json';
    script.textContent = JSON.stringify(jsonLdData, null, 2);
    document.head.appendChild(script);
})();
