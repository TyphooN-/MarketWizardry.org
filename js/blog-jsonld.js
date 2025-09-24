// Blog JSON-LD structured data injection
(function() {
    'use strict';

    // JSON-LD structured data for Blog
    const jsonLdData = {
        "@context": "https://schema.org",
        "@type": ["Blog", "WebSite"],
        "name": "MarketWizardry.org Financial Trading Blog",
        "alternateName": "Market Wizardry Blog - Financial Analysis & Trading Insights",
        "description": "Financial autism documented in real-time for your entertainment and education. Market analysis, trading insights, portfolio destruction methodologies with mathematical precision, VaR analysis, and risk management content.",
        "url": "https://marketwizardry.org/blog.html",
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
        "inLanguage": "en-US",
        "keywords": "financial analysis, market data, trading insights, VaR analysis, risk management, market outliers, trading strategy, Darwinex analysis, portfolio management, statistical analysis, financial blog, market research, trading psychology, quantitative trading, volatility analysis, cryptocurrency analysis",
        "about": [
            {
                "@type": "Thing",
                "name": "Financial Analysis",
                "description": "Mathematical analysis of financial markets and instruments"
            },
            {
                "@type": "Thing",
                "name": "Risk Management",
                "description": "Portfolio risk assessment and management strategies"
            },
            {
                "@type": "Thing",
                "name": "Trading Psychology",
                "description": "Behavioral aspects of trading and market participation"
            }
        ],
        "blogPost": [
            {
                "@type": "BlogPosting",
                "headline": "What is Value at Risk (VaR)",
                "url": "https://marketwizardry.org/blog/what-is-value-at-risk-var.html",
                "datePublished": "2024-09-01",
                "description": "Comprehensive guide to understanding Value at Risk calculations"
            },
            {
                "@type": "BlogPosting",
                "headline": "What is Average True Range (ATR)",
                "url": "https://marketwizardry.org/blog/what-is-average-true-range-atr.html",
                "datePublished": "2024-09-01",
                "description": "Understanding ATR for volatility analysis and stop loss optimization"
            },
            {
                "@type": "BlogPosting",
                "headline": "What is Enterprise Value (EV)",
                "url": "https://marketwizardry.org/blog/what-is-enterprise-value-ev.html",
                "datePublished": "2024-09-01",
                "description": "Fundamental analysis using Enterprise Value metrics"
            },
            {
                "@type": "BlogPosting",
                "headline": "GPU Buyers Guide 2025",
                "url": "https://marketwizardry.org/blog/gpu-buyers-guide-2025.html",
                "datePublished": "2024-09-01",
                "description": "Comprehensive guide for GPU selection in 2025"
            }
        ],
        "audience": {
            "@type": "Audience",
            "audienceType": "Professional Traders, Quantitative Analysts, Risk Managers"
        }
    };

    // Inject JSON-LD into document head
    function injectJsonLd() {
        const script = document.createElement('script');
        script.type = 'application/ld+json';
        script.textContent = JSON.stringify(jsonLdData);
        document.head.appendChild(script);
        console.log('Blog JSON-LD structured data injected');
    }

    // Execute when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', injectJsonLd);
    } else {
        injectJsonLd();
    }

})();