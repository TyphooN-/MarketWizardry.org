// JSON-LD structured data - CSP compliant
(function() {
    'use strict';

    const jsonLdData = {
    "@context": "https://schema.org",
    "@type": [
        "Collection",
        "CreativeWork"
    ],
    "name": "NFT Gallery - acid_boy__",
    "url": "https://marketwizardry.org/nft-gallery/acid_boy___gallery.html",
    "description": "Chemical burn aesthetics for the digitally damaged. Psychedelic childhood trauma meets blockchain therapy in perfect melting harmony.",
    "author": {
        "@type": "Person",
        "name": "TyphooN"
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
    "collectionSize": "Variable",
    "genre": "Digital Art",
    "artMedium": "Digital",
    "keywords": "AI art, NFT gallery, digital art, generative art, creative technology",
    "creator": {
        "@type": "Person",
        "name": "acid_boy__"
    }
};

    function injectJsonLd() {
        const script = document.createElement('script');
        script.type = 'application/ld+json';
        script.textContent = JSON.stringify(jsonLdData);
        document.head.appendChild(script);
        console.log('JSON-LD structured data injected');
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', injectJsonLd);
    } else {
        injectJsonLd();
    }
})();