// JSON-LD structured data - CSP compliant
(function() {
    'use strict';

    const jsonLdData = {
    "@context": "https://schema.org",
    "@type": "ItemList",
    "name": "MarketWizardry.org Affiliates & Partners",
    "url": "https://marketwizardry.org/affiliates.html",
    "description": "Curated list of trading platforms, services, and tools recommended by MarketWizardry.org",
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
    "numberOfItems": 4,
    "itemListElement": [
        {
            "@type": "ListItem",
            "position": 1,
            "name": "Darwinex Zero",
            "url": "https://www.darwinexzero.com"
        },
        {
            "@type": "ListItem",
            "position": 2,
            "name": "FXVPS",
            "url": "https://fxvps.biz"
        },
        {
            "@type": "ListItem",
            "position": 3,
            "name": "Godly Trading",
            "url": "https://www.godlytrading.com"
        },
        {
            "@type": "ListItem",
            "position": 4,
            "name": "FuckTrader",
            "url": "https://fucktrader.com"
        }
    ]
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