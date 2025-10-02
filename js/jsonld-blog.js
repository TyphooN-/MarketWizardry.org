// JSON-LD structured data - CSP compliant
(function() {
    'use strict';

    const jsonLdData = {
    "@context": "https://schema.org",
    "@type": [
        "BlogPosting",
        "Article"
    ],
    "name": "Market Wizardry Blog",
    "url": "https://marketwizardry.org/blog.html",
    "description": "Financial market analysis, trading insights, and risk management strategies from MarketWizardry.org",
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
    "headline": "Market Wizardry Blog",
    "datePublished": "2024-01-01",
    "dateModified": "2025-10-02",
    "articleBody": "Financial market analysis, trading insights, and risk management strategies from MarketWizardry.org",
    "keywords": "financial analysis, market data, trading insights, VaR analysis, risk management",
    "articleSection": "Financial Analysis",
    "mainEntityOfPage": {
        "@type": "WebPage",
        "@id": "https://marketwizardry.org/blog.html"
    }
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