// JSON-LD structured data for ev-explorer.html - CSP compliant
(function() {
    'use strict';

    const jsonLdData = {
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "EV Explorer - Enterprise Value Calculator",
    "description": "Enterprise Value (EV) calculator and analysis platform for fundamental stock analysis. Comprehensive valuation tools for equity research.",
    "url": "https://marketwizardry.org/ev-explorer.html",
    "applicationCategory": "FinanceApplication",
    "operatingSystem": "Web Browser",
    "offers": {
        "@type": "Offer",
        "price": "0",
        "priceCurrency": "USD"
    },
    "author": {
        "@type": "Person",
        "name": "TyphooN",
        "url": "https://twitter.com/MarketW1zardry"
    }
};

    // Inject JSON-LD into page
    const script = document.createElement('script');
    script.type = 'application/ld+json';
    script.textContent = JSON.stringify(jsonLdData, null, 2);
    document.head.appendChild(script);
})();
