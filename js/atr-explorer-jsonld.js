// ATR Explorer JSON-LD structured data injection
(function() {
    'use strict';

    // JSON-LD structured data for ATR Explorer
    const jsonLdData = {
        "@context": "https://schema.org",
        "@type": ["SoftwareApplication", "FinancialProduct", "WebApplication"],
        "name": "ATR Explorer - Average True Range Analysis Tool",
        "alternateName": "MarketWizardry ATR Calculator",
        "applicationCategory": "FinanceApplication",
        "applicationSubCategory": "Volatility Analysis Tools",
        "operatingSystem": "Web",
        "browserRequirements": "Requires JavaScript",
        "description": "Advanced Average True Range (ATR) analysis tool for measuring market volatility across 901+ financial instruments with real-time data and professional trading insights",
        "url": "https://marketwizardry.org/atr-explorer.html",
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
            "Average True Range calculations with precision",
            "901+ financial instruments volatility data",
            "Multi-timeframe ATR analysis",
            "Real-time volatility measurements",
            "Stop loss optimization using ATR",
            "Position sizing recommendations",
            "Sector and industry volatility comparison",
            "Asset class volatility analysis",
            "Historical ATR trends and patterns"
        ],
        "screenshot": "https://marketwizardry.org/img/xicojam-1924524951521853846-prompt-video1-mod-mod.webp",
        "softwareVersion": "2.0",
        "dateCreated": "2024-01-01",
        "dateModified": "2024-09-24",
        "inLanguage": "en-US",
        "keywords": "ATR calculator, Average True Range, volatility analysis, market volatility, trading volatility, stop loss calculation, position sizing, technical analysis",
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "4.6",
            "ratingCount": "76",
            "bestRating": "5",
            "worstRating": "1"
        },
        "mainEntity": {
            "@type": "Dataset",
            "name": "ATR Financial Volatility Database",
            "description": "Comprehensive database of 901+ financial instruments with Average True Range calculations",
            "keywords": "ATR data, volatility metrics, market volatility, trading data",
            "distribution": [
                {
                    "@type": "DataDownload",
                    "encodingFormat": "application/json",
                    "contentUrl": "https://marketwizardry.org/atr-explorer.html"
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
        console.log('ATR Explorer JSON-LD structured data injected');
    }

    // Execute when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', injectJsonLd);
    } else {
        injectJsonLd();
    }

})();