// JSON-LD structured data for darwinex-radar.html - CSP compliant
(function() {
    'use strict';

    const jsonLdData = {
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "Darwinex RADAR - Symbol Tracker",
    "description": "Real-time tracking of Darwinex symbol additions, delistings, close-only restrictions, and swap rate changes. Know before the notification email hits your spam folder.",
    "url": "https://marketwizardry.org/darwinex-radar.html",
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
