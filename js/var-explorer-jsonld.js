// VaR Explorer JSON-LD structured data injection
(function() {
    'use strict';

    // JSON-LD structured data for VaR Explorer
    const jsonLdData = {
        "@context": "https://schema.org",
        "@type": ["SoftwareApplication", "FinancialProduct", "WebApplication"],
        "name": "VaR Explorer - Value at Risk Analysis Tool",
        "alternateName": "MarketWizardry VaR Calculator",
        "applicationCategory": "FinanceApplication",
        "applicationSubCategory": "Risk Analysis Tools",
        "operatingSystem": "Web",
        "browserRequirements": "Requires JavaScript",
        "description": "Advanced Value at Risk (VaR) analysis tool with 901+ financial instruments, real-time outlier detection, and comprehensive risk metrics for professional traders and portfolio managers",
        "url": "https://marketwizardry.org/var-explorer.html",
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
            "Value at Risk calculations with statistical precision",
            "901+ financial instruments database",
            "Real-time outlier detection algorithms",
            "Multi-asset class coverage (stocks, CFDs, futures)",
            "Sector and industry filtering capabilities",
            "Risk metrics and volatility analysis",
            "Portfolio risk assessment tools",
            "Enterprise Value integration",
            "Advanced search and filtering"
        ],
        "screenshot": "https://marketwizardry.org/img/xicojam-1924524951521853846-prompt-video1-mod-mod.webp",
        "softwareVersion": "2.0",
        "dateCreated": "2024-01-01",
        "dateModified": "2024-09-24",
        "inLanguage": "en-US",
        "keywords": "VaR calculator, Value at Risk, risk analysis, financial risk tools, portfolio risk, volatility analysis, outlier detection, market risk, trading tools",
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "4.7",
            "ratingCount": "89",
            "bestRating": "5",
            "worstRating": "1"
        },
        "mainEntity": {
            "@type": "Dataset",
            "name": "VaR Financial Instruments Database",
            "description": "Comprehensive database of 901+ financial instruments with VaR calculations",
            "keywords": "financial data, VaR, risk metrics, market data",
            "distribution": [
                {
                    "@type": "DataDownload",
                    "encodingFormat": "application/json",
                    "contentUrl": "https://marketwizardry.org/var-explorer.html"
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
        console.log('VaR Explorer JSON-LD structured data injected');
    }

    // Execute when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', injectJsonLd);
    } else {
        injectJsonLd();
    }

})();