// JSON-LD structured data for ai-art.html - CSP compliant
(function() {
    'use strict';

    const jsonLdData = {
    "@context": "https://schema.org",
    "@type": "CreativeWork",
    "name": "AI Art Gallery",
    "description": "AI-generated art collection showcasing the intersection of artificial intelligence and creative expression. Digital art powered by machine learning.",
    "url": "https://marketwizardry.org/ai-art.html",
    "author": {
        "@type": "Person",
        "name": "TyphooN"
    }
};

    // Inject JSON-LD into page
    const script = document.createElement('script');
    script.type = 'application/ld+json';
    script.textContent = JSON.stringify(jsonLdData, null, 2);
    document.head.appendChild(script);
})();
