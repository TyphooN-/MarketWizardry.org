// JSON-LD structured data for atr-explorer.html - CSP compliant
(function() {
    'use strict';

    const jsonLdData = {
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "ATR Explorer - Average True Range Calculator",
    "description": "Advanced Average True Range (ATR) analysis tool for volatility measurement. Professional market analysis for traders and investors.",
    "url": "https://marketwizardry.org/atr-explorer.html",
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
