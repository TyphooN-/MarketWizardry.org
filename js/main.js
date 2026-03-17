function updateMobileBreadcrumb(page) {
    const mobileBreadcrumb = document.getElementById('mobileBreadcrumb');
    if (!mobileBreadcrumb) return;

    const breadcrumbText = mobileBreadcrumb.querySelector('.mobile-breadcrumb-text');
    if (!breadcrumbText) return;

    // Map pages to breadcrumb text
    const pageMap = {
        'market-wizardry': '🏠 Home',
        'about': '📖 About',
        'code': '💻 Code',
        'calculator': '🧮 Calculator',
        'var-cult': '📈 VaR Cult',
        'blog': '📊 Blog',
        'var-explorer': '📊 VaR Explorer',
        'ev-explorer': '💰 EV Explorer',
        'atr-explorer': '📈 ATR Explorer',
        'crypto-explorer': '₿ Crypto Explorer',
        'ai-art': '🎨 AI Art',
        'ai-musings': '🤖 AI Musings',
        'nft-gallery': '🖼️ NFT Gallery',
        'affiliates': '🤝 Affiliates',
        'donate': '💝 Donate',
        'terms': '📋 Terms'
    };

    // Handle blog posts and gallery pages
    if (page.includes('blog/')) {
        breadcrumbText.textContent = '📊 Blog → Article';
    } else if (page.includes('nft-gallery/')) {
        breadcrumbText.textContent = '🖼️ Gallery → Artist';
    } else {
        breadcrumbText.textContent = pageMap[page] || '🏠 Home';
    }
}

function loadContent(page, clickedElement) {
    const iframe = document.getElementById('contentIframe');
    // Handle full paths (like blog/post.html or nft-gallery/artist.html) vs simple page names
    if (page.includes('/') || page.endsWith('.html')) {
        iframe.src = page;
    } else {
        iframe.src = `${page}.html`;
    }

    // Update mobile breadcrumb
    updateMobileBreadcrumb(page);

    // Remove active class from all menu items
    const menuItems = document.querySelectorAll('.menu-item, .image-item');
    menuItems.forEach(item => item.classList.remove('active'));

    // Add active class to clicked menu item if provided and it's not the Market Wizardry image
    if (clickedElement && clickedElement.classList && !clickedElement.classList.contains('image-item')) {
        clickedElement.classList.add('active');
    }
}

// Load content based on URL parameter or default to "market-wizardry"
document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    const pageParam = urlParams.get('page');
    // Validate page parameter to prevent open redirect / iframe injection
    const targetPage = pageParam && /^[a-zA-Z0-9\-_\/\.]+$/.test(pageParam) && !pageParam.includes('..')
        ? pageParam : 'market-wizardry';
    loadContent(targetPage);

    // Set up hamburger menu event listener
    const hamburger = document.getElementById('hamburgerToggle');
    if (hamburger) {
        hamburger.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            toggleMenu();
        });
    }

    // Set up event delegation for loadContent
    document.addEventListener('click', function(e) {
        let targetElement = e.target;

        // If clicked element doesn't have data-load-content, check its parent
        if (!targetElement.hasAttribute('data-load-content') && targetElement.parentElement) {
            targetElement = targetElement.parentElement;
        }

        if (targetElement.hasAttribute('data-load-content')) {
            const page = targetElement.getAttribute('data-load-content');
            loadContent(page, targetElement);

            // Close mobile menu after clicking a menu item
            const menu = document.getElementById('sideMenu');
            const contentFrame = document.querySelector('.content-frame');
            const mobileHeader = document.getElementById('mobileHeader');
            if (menu && contentFrame && menu.classList.contains('show')) {
                menu.classList.remove('show');
                contentFrame.classList.remove('menu-open');
                if (mobileHeader) {
                    mobileHeader.classList.remove('menu-open');
                }
            }
        }
    });

    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const mobileMenuContainer = document.querySelector('.mobile-menu-container');

    // Only add event listener if mobile menu elements exist
    if (mobileMenuToggle && mobileMenuContainer) {
        mobileMenuToggle.addEventListener('click', function() {
            mobileMenuContainer.classList.toggle('show-menu');
        });
    }
});

// Hamburger menu toggle function
function toggleMenu() {
    const menu = document.getElementById('sideMenu');
    const contentFrame = document.querySelector('.content-frame');
    const mobileHeader = document.getElementById('mobileHeader');

    if (menu && contentFrame) {
        menu.classList.toggle('show');
        contentFrame.classList.toggle('menu-open');

        // Toggle mobile header class to hide/show logo
        if (mobileHeader) {
            mobileHeader.classList.toggle('menu-open');
        }
    }
}