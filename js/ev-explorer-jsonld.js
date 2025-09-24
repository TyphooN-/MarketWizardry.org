// EV Explorer JSON-LD structured data injection
(function() {
    'use strict';

    // JSON-LD structured data for EV Explorer
    const jsonLdData = {
        "@context": "https://schema.org",
        "@type": ["SoftwareApplication", "FinancialProduct", "WebApplication"],
        "name": "EV Explorer - Enterprise Value Analysis Tool",
        "alternateName": "MarketWizardry Enterprise Value Calculator",
        "applicationCategory": "FinanceApplication",
        "applicationSubCategory": "Valuation Analysis Tools",
        "operatingSystem": "Web",
        "browserRequirements": "Requires JavaScript",
        "description": "Advanced Enterprise Value (EV) analysis tool for fundamental analysis and company valuation across 901+ financial instruments with comprehensive market metrics",
        "url": "https://marketwizardry.org/ev-explorer.html",
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
            "Enterprise Value calculations and analysis",
            "901+ financial instruments valuation data",
            "Fundamental analysis metrics",
            "Market capitalization calculations",
            "Debt-to-equity analysis",
            "Valuation ratio comparisons",
            "Sector and industry EV analysis",
            "Real-time market data integration",
            "Investment screening capabilities"
        ],
        "screenshot": "https://marketwizardry.org/img/xicojam-1924524951521853846-prompt-video1-mod-mod.webp",
        "softwareVersion": "2.0",
        "dateCreated": "2024-01-01",
        "dateModified": "2024-09-24",
        "inLanguage": "en-US",
        "keywords": "enterprise value, EV calculator, valuation analysis, fundamental analysis, market cap, company valuation, investment analysis, financial metrics",
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "4.5",
            "ratingCount": "67",
            "bestRating": "5",
            "worstRating": "1"
        },
        "mainEntity": {
            "@type": "Dataset",
            "name": "Enterprise Value Financial Database",
            "description": "Comprehensive database of 901+ financial instruments with Enterprise Value calculations",
            "keywords": "enterprise value data, valuation metrics, fundamental data, market data",
            "distribution": [
                {
                    "@type": "DataDownload",
                    "encodingFormat": "application/json",
                    "contentUrl": "https://marketwizardry.org/ev-explorer.html"
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
        console.log('EV Explorer JSON-LD structured data injected');
    }

    // Execute when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', injectJsonLd);
    } else {
        injectJsonLd();
    }

})();