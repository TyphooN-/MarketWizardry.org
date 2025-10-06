// JSON-LD structured data for var-cult.html - CSP compliant
(function() {
    'use strict';

    const jsonLdData = {
    "@context": "https://schema.org",
    "@type": "WebPage",
    "name": "VaR Cult - Value at Risk Community",
    "description": "Value at Risk (VaR) methodology, research, and community resources for quantitative risk management.",
    "url": "https://marketwizardry.org/var-cult.html"
};

    // Inject JSON-LD into page
    const script = document.createElement('script');
    script.type = 'application/ld+json';
    script.textContent = JSON.stringify(jsonLdData, null, 2);
    document.head.appendChild(script);
})();
