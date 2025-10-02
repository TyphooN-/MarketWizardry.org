// JSON-LD structured data - CSP compliant
(function() {
    'use strict';

    const jsonLdData = {
    "@context": "https://schema.org",
    "@type": "ItemList",
    "name": "Support MarketWizardry.org",
    "url": "https://marketwizardry.org/donate.html",
    "description": "Support the development of free trading tools and market analysis resources.",
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
    "numberOfItems": 2,
    "itemListElement": [
        {
            "@type": "ListItem",
            "position": 1,
            "name": "Bitcoin Donation",
            "url": "https://marketwizardry.org/donate.html"
        },
        {
            "@type": "ListItem",
            "position": 2,
            "name": "Ethereum Donation",
            "url": "https://marketwizardry.org/donate.html"
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