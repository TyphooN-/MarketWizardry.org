// About Page JSON-LD structured data injection
(function() {
    'use strict';

    // JSON-LD structured data for About Page
    const jsonLdData = {
        "@context": "https://schema.org",
        "@type": ["AboutPage", "WebPage"],
        "name": "About MarketWizardry.org - Financial Analytics Platform",
        "description": "Learn about MarketWizardry.org, a comprehensive financial analytics platform providing VaR calculators, risk management tools, and quantitative analysis for traders and investors.",
        "url": "https://marketwizardry.org/about.html",
        "mainEntity": {
            "@type": "Organization",
            "name": "Market Wizardry",
            "url": "https://marketwizardry.org",
            "description": "Financial analytics platform specializing in Value at Risk calculations, portfolio risk management, and quantitative trading tools",
            "founder": {
                "@type": "Person",
                "name": "TyphooN",
                "identifier": "TyphooN"
            },
            "sameAs": [
                "https://x.com/MarketW1zardry"
            ],
            "knowsAbout": [
                "Value at Risk (VaR) Analysis",
                "Average True Range (ATR) Calculations",
                "Enterprise Value Analysis",
                "Portfolio Risk Management",
                "Quantitative Trading",
                "Financial Risk Assessment",
                "Market Volatility Analysis"
            ],
            "offers": [
                {
                    "@type": "Service",
                    "name": "VaR Calculator Suite",
                    "description": "Comprehensive Value at Risk calculation tools"
                },
                {
                    "@type": "Service",
                    "name": "Risk Management Tools",
                    "description": "Professional portfolio and trading risk analysis"
                },
                {
                    "@type": "Service",
                    "name": "Market Data Analytics",
                    "description": "Real-time financial data analysis and insights"
                }
            ]
        },
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
        "inLanguage": "en-US"
    };

    // Inject JSON-LD into document head
    function injectJsonLd() {
        const script = document.createElement('script');
        script.type = 'application/ld+json';
        script.textContent = JSON.stringify(jsonLdData);
        document.head.appendChild(script);
        console.log('About page JSON-LD structured data injected');
    }

    // Execute when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', injectJsonLd);
    } else {
        injectJsonLd();
    }

})();