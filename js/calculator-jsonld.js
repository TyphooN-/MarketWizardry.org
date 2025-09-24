// Calculator JSON-LD structured data injection
(function() {
    'use strict';

    // JSON-LD structured data
    const jsonLdData = {
        "@context": "https://schema.org",
        "@type": ["SoftwareApplication", "FinancialProduct", "WebApplication"],
        "name": "Professional Financial Calculator Suite",
        "alternateName": "MarketWizardry Calculator Suite",
        "applicationCategory": "FinanceApplication",
        "applicationSubCategory": "Risk Management Tools",
        "operatingSystem": "Web",
        "browserRequirements": "Requires JavaScript",
        "description": "Comprehensive financial calculator suite featuring VaR, stop loss, position sizing, portfolio risk management, and compound interest calculators with real-time data analysis",
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
            "priceValidUntil": "2025-12-31"
        },
        "featureList": [
            "VaR (Value at Risk) Calculator with statistical precision",
            "Stop Loss Calculator with ATR integration and multiple timeframes",
            "Position Size Calculator with risk, VaR, and ATR modes",
            "Portfolio VaR Calculator with correlation adjustments",
            "Compound Interest Calculator with monthly contributions and timeline",
            "Symbol Lookup Tool with 901+ financial instruments",
            "Real-time risk assessment and outlier detection",
            "Enterprise Value data integration",
            "Professional trading risk management"
        ],
        "screenshot": "https://marketwizardry.org/img/xicojam-1924524951521853846-prompt-video1-mod-mod.webp",
        "softwareVersion": "2.0",
        "dateCreated": "2024-01-01",
        "dateModified": "2024-09-17",
        "inLanguage": "en-US",
        "keywords": "financial calculator, VaR calculator, stop loss, position sizing, portfolio risk, compound interest, trading tools, risk management",
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "4.8",
            "ratingCount": "127",
            "bestRating": "5",
            "worstRating": "1"
        },
        "mainEntity": {
            "@type": "ItemList",
            "name": "Financial Calculators",
            "itemListElement": [
                {
                    "@type": "SoftwareApplication",
                    "name": "Stop Loss Calculator",
                    "description": "Calculate optimal stop loss levels with ATR integration"
                },
                {
                    "@type": "SoftwareApplication",
                    "name": "Position Size Calculator",
                    "description": "Determine position sizes based on risk tolerance"
                },
                {
                    "@type": "SoftwareApplication",
                    "name": "Portfolio VaR Calculator",
                    "description": "Calculate portfolio Value at Risk with correlations"
                },
                {
                    "@type": "SoftwareApplication",
                    "name": "Compound Interest Calculator",
                    "description": "Long-term investment growth calculations"
                },
                {
                    "@type": "SoftwareApplication",
                    "name": "Symbol Lookup Tool",
                    "description": "Search comprehensive market data for 901+ symbols"
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
        console.log('JSON-LD structured data injected');
    }

    // Execute when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', injectJsonLd);
    } else {
        injectJsonLd();
    }

})();