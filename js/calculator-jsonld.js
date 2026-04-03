// Calculator JSON-LD structured data injection
(function() {
    'use strict';

    // JSON-LD structured data
    const jsonLdData = {
        "@context": "https://schema.org",
        "@type": ["SoftwareApplication", "FinancialProduct", "WebApplication"],
        "name": "Financial Calculator Suite",
        "alternateName": "MarketWizardry Calculator Suite",
        "applicationCategory": "FinanceApplication",
        "applicationSubCategory": "Risk Management Tools",
        "operatingSystem": "Web",
        "browserRequirements": "Requires JavaScript",
        "description": "Financial calculator suite featuring position sizing and compound interest calculators. VaR, ATR, and portfolio tools now available in TyphooN-Terminal.",
        "url": "https://marketwizardry.org/calculator.html",
        "sameAs": [
            "https://marketwizardry.org"
        ],
        "author": {
            "@type": "Person",
            "name": "TyphooN",
            "identifier": "TyphooN"
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
        "offers": {
            "@type": "Offer",
            "price": "0",
            "priceCurrency": "USD",
            "availability": "https://schema.org/InStock",
            "priceValidUntil": "2026-12-31"
        },
        "featureList": [
            "Position Size Calculator with stop loss risk management",
            "Compound Interest Calculator with monthly contributions and timeline",
            "Professional trading risk management"
        ],
        "screenshot": "https://marketwizardry.org/img/xicojam-1924524951521853846-prompt-video1-mod-mod.webp",
        "softwareVersion": "3.0",
        "dateCreated": "2024-01-01",
        "dateModified": "2026-04-02",
        "inLanguage": "en-US",
        "keywords": "financial calculator, position sizing, compound interest, trading tools, risk management",
        "mainEntity": {
            "@type": "ItemList",
            "name": "Financial Calculators",
            "itemListElement": [
                {
                    "@type": "SoftwareApplication",
                    "name": "Position Size Calculator",
                    "description": "Determine position sizes based on account risk and stop loss levels"
                },
                {
                    "@type": "SoftwareApplication",
                    "name": "Compound Interest Calculator",
                    "description": "Long-term investment growth calculations with wealth milestones"
                }
            ]
        }
    };

    // Inject JSON-LD into document head
    function injectJsonLd() {
        const script = document.createElement('script');
        script.type = 'application/ld+json';
        script.textContent = JSON.stringify(jsonLdData);
        document.head.appendChild(script);
    }

    // Execute when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', injectJsonLd);
    } else {
        injectJsonLd();
    }

})();
