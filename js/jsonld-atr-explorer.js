// JSON-LD structured data - CSP compliant
(function() {
    'use strict';

    const jsonLdData = {
    "@context": "https://schema.org",
    "@type": "WebApplication",
    "name": "ATR Explorer - Average True Range Analysis",
    "url": "https://marketwizardry.org/atr-explorer.html",
    "description": "Interactive ATR (Average True Range) explorer for volatility analysis across 900+ financial instruments. Real-time market data and risk metrics.",
    "author": {
        "@type": "Person",
        "name": "TyphooN"
    },
    "publisher": {
        "@type": "Organization",
        "name": "Market Wizardry",
        "url": "https://marketwizardry.org",
        "logo": {
            "@type": "ImageObject",
            "url": "https://marketwizardry.org/img/apple-touch-icon.png"
        }
    },
    "inLanguage": "en-US",
    "applicationCategory": "FinanceApplication",
    "operatingSystem": "Any",
    "browserRequirements": "Requires JavaScript",
    "offers": {
        "@type": "Offer",
        "price": "0",
        "priceCurrency": "USD"
    },
    "featureList": "Interactive ATR (Average True Range) explorer for volatility analysis across 900+ financial instruments. Real-time market data and risk metrics."
};

    function injectJsonLd() {
        const script = document.createElement('script');
        script.type = 'application/ld+json';
        script.textContent = JSON.stringify(jsonLdData);
        document.head.appendChild(script);
        console.log('JSON-LD structured data injected');
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', injectJsonLd);
    } else {
        injectJsonLd();
    }
})();