// JSON-LD structured data for crypto-explorer.html - CSP compliant
(function() {
    'use strict';

    const jsonLdData = {
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "Crypto Explorer - Cryptocurrency Analysis",
    "description": "Cryptocurrency market analysis and tracking platform. Real-time crypto data, volatility metrics, and trading insights for digital assets.",
    "url": "https://marketwizardry.org/crypto-explorer.html",
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
