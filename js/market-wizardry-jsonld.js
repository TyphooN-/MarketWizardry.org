// Market Wizardry Main Page JSON-LD structured data injection
(function() {
    'use strict';

    // JSON-LD structured data for Market Wizardry Main Page
    const jsonLdData = {
        "@context": "https://schema.org",
        "@type": ["WebSite", "SoftwareApplication"],
        "name": "Market Wizardry - Professional Financial Analytics Platform",
        "alternateName": "MarketWizardry.org Financial Tools Hub",
        "description": "Professional financial analytics platform providing VaR calculators, ATR analysis, enterprise value tools, and comprehensive risk management solutions for traders and investors.",
        "url": "https://marketwizardry.org/market-wizardry.html",
        "applicationCategory": "FinanceApplication",
        "operatingSystem": "Web",
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
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Financial Analytics Tools",
            "itemListElement": [
                {
                    "@type": "Offer",
                    "itemOffered": {
                        "@type": "SoftwareApplication",
                        "name": "VaR Explorer",
                        "url": "https://marketwizardry.org/var-explorer.html",
                        "description": "Value at Risk analysis tool"
                    }
                },
                {
                    "@type": "Offer",
                    "itemOffered": {
                        "@type": "SoftwareApplication",
                        "name": "ATR Explorer",
                        "url": "https://marketwizardry.org/atr-explorer.html",
                        "description": "Average True Range volatility analysis"
                    }
                },
                {
                    "@type": "Offer",
                    "itemOffered": {
                        "@type": "SoftwareApplication",
                        "name": "EV Explorer",
                        "url": "https://marketwizardry.org/ev-explorer.html",
                        "description": "Enterprise Value analysis tool"
                    }
                },
                {
                    "@type": "Offer",
                    "itemOffered": {
                        "@type": "SoftwareApplication",
                        "name": "Calculator Suite",
                        "url": "https://marketwizardry.org/calculator.html",
                        "description": "Comprehensive financial calculator suite"
                    }
                }
            ]
        },
        "potentialAction": {
            "@type": "SearchAction",
            "target": "https://marketwizardry.org/?page={search_term_string}",
            "query-input": "required name=search_term_string"
        },
        "inLanguage": "en-US",
        "keywords": "financial analytics, VaR calculator, risk management, trading tools, market analysis, volatility analysis, enterprise value, portfolio management"
    };

    // Inject JSON-LD into document head
    function injectJsonLd() {
        const script = document.createElement('script');
        script.type = 'application/ld+json';
        script.textContent = JSON.stringify(jsonLdData);
        document.head.appendChild(script);
        console.log('Market Wizardry main page JSON-LD structured data injected');
    }

    // Execute when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', injectJsonLd);
    } else {
        injectJsonLd();
    }

})();