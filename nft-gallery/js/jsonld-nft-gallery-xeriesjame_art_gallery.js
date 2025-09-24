// JSON-LD structured data - CSP compliant
(function() {
    'use strict';

    const jsonLdData = {
    "@context": "https://schema.org",
    "@type": [
        "Collection",
        "CreativeWork"
    ],
    "name": "NFT Gallery - xeriesjame_art",
    "url": "https://marketwizardry.org/nft-gallery/xeriesjame_art_gallery.html",
    "description": "xeriesjame_art's digital art collection - X marks the spot where artistic standards went to die. This collection series-ly challenges the definition of art. James Bond couldn't escape this visual torture.",
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
        "name": "xeriesjame_art"
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