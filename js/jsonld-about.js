// JSON-LD structured data - CSP compliant
(function() {
    'use strict';

    const jsonLdData = {
    "@context": "https://schema.org",
    "@type": "Person",
    "name": "TyphooN - MarketWizardry.org",
    "url": "https://marketwizardry.org/about.html",
    "description": "Trader and developer specializing in algorithmic trading, risk management, and financial market analysis. Creator of MarketWizardry.org trading tools and explorers.",
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
    "jobTitle": "Trader & Developer",
    "knowsAbout": [
        "Financial Markets",
        "Algorithmic Trading",
        "Risk Management",
        "Market Analysis"
    ],
    "sameAs": [
        "https://twitter.com/MarketW1zardry"
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