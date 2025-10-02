// JSON-LD structured data - CSP compliant
(function() {
    'use strict';

    const jsonLdData = {
    "@context": "https://schema.org",
    "@type": "WebApplication",
    "name": "EV Explorer - Expected Value Analysis",
    "url": "https://marketwizardry.org/ev-explorer.html",
    "description": "Expected Value (EV) calculator and explorer for trading strategy analysis and probability-based decision making.",
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
    "featureList": "Expected Value (EV) calculator and explorer for trading strategy analysis and probability-based decision making."
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