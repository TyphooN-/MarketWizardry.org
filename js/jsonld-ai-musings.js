// JSON-LD structured data for ai-musings.html - CSP compliant
(function() {
    'use strict';

    const jsonLdData = {
    "@context": "https://schema.org",
    "@type": "Blog",
    "name": "AI Musings - Artificial Intelligence Articles",
    "description": "AI-generated market commentary and trading insights. Exploring the intersection of artificial intelligence and financial markets.",
    "url": "https://marketwizardry.org/ai-musings.html",
    "author": {
        "@type": "Person",
        "name": "TyphooN",
        "url": "https://twitter.com/MarketW1zardry"
    },
    "publisher": {
        "@type": "Organization",
        "name": "MarketWizardry.org",
        "url": "https://marketwizardry.org"
    }
};

    // Inject JSON-LD into page
    const script = document.createElement('script');
    script.type = 'application/ld+json';
    script.textContent = JSON.stringify(jsonLdData, null, 2);
    document.head.appendChild(script);
})();
