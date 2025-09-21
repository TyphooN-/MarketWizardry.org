// Redirect to market-wizardry.html if accessed directly (not in iframe)
if (window === window.top) {
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
}