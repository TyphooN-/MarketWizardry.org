// Redirect to market-wizardry.html if accessed directly (not in iframe)
if (window === window.top) {
    // Load main.css for standalone access before redirect
    const mainCssLink = document.createElement('link');
    mainCssLink.rel = 'stylesheet';
    mainCssLink.href = '/css/main.css';
    document.head.appendChild(mainCssLink);

    // Small delay to ensure viewport takes effect on mobile
    setTimeout(() => {
        const currentPath = window.location.pathname;
        if (currentPath.includes('/blog/') || currentPath.includes('/nft-gallery/')) {
            // For blog posts and NFT galleries, pass full path
            const fullPath = currentPath.startsWith('/') ? currentPath.substring(1) : currentPath;
            window.location.href = `/?page=${encodeURIComponent(fullPath)}`;
        } else {
            // For main pages, redirect with page parameter
            const currentPage = currentPath.split('/').pop().replace('.html', '');
            window.location.href = `/?page=${currentPage}`;
        }
    }, 100);
} else {
    // When in iframe, do NOT load main.css to avoid layout conflicts
    // Only shared-styles.css should be loaded for iframe content
}