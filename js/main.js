function loadContent(page, clickedElement) {
    const iframe = document.getElementById('contentIframe');
    // Handle full paths (like blog/post.html or nft-gallery/artist.html) vs simple page names
    if (page.includes('/') || page.endsWith('.html')) {
        iframe.src = page;
    } else {
        iframe.src = `${page}.html`;
    }
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
    const targetPage = pageParam || 'market-wizardry';
    loadContent(targetPage);

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
    menu.classList.toggle('show');
    contentFrame.classList.toggle('menu-open');
}