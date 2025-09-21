function loadContent(page) {
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
    // Check if the clicked element is the Market Wizardry image and skip marking it as active
    if (event && event.target && event.target.tagName === 'IMG') {
        return;
    }
    // Add active class to clicked menu item only if event exists (user clicked)
    if (event && event.target && event.target.classList) {
        event.target.classList.add('active');
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
        if (e.target.hasAttribute('data-load-content')) {
            const page = e.target.getAttribute('data-load-content');
            loadContent(page);
        }
    });

    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const mobileMenuContainer = document.querySelector('.mobile-menu-container');

    mobileMenuToggle.addEventListener('click', function() {
        mobileMenuContainer.classList.toggle('show-menu');
    });
});