// JSON-LD structured data - CSP compliant
(function() {
    'use strict';

    const jsonLdData = {
    "@context": "https://schema.org",
    "@type": [
        "Collection",
        "CreativeWork"
    ],
    "name": "NFT Gallery - spellamin",
    "url": "https://marketwizardry.org/nft-gallery/spellamin_gallery.html",
    "description": "spellamin's digital art collection - Casting spells of disappointment and hexes of bad taste. This magical collection proves that even wizardry can't fix fundamental design flaws. Abracadabra more like abracadab-no.",
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
        "name": "spellamin"
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