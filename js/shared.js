// Shared JavaScript functionality for MarketWizardry.org
// Handles data-action event delegation for all pages

document.addEventListener('DOMContentLoaded', function() {
    // Global event delegation for data-action attributes
    document.addEventListener('click', function(e) {
        // Check if clicked element or any parent has data-action
        let targetElement = e.target.closest('[data-action]');
        const action = targetElement ? targetElement.getAttribute('data-action') : null;

        // Handle modal background clicks
        if (e.target.id === 'analysisModal') {
            closeModal();
            return;
        }

        if (!action) return;

        switch(action) {
            case 'loadContent':
                handleLoadContent(e, targetElement);
                break;
            case 'copyToClipboard':
                handleCopyToClipboard(e);
                break;
            case 'close-modal':
                handleCloseModal(e);
                break;
            case 'previous-image':
                handlePreviousImage(e);
                break;
            case 'next-image':
                handleNextImage(e);
                break;
            case 'download-image':
                handleDownloadImage(e);
                break;
            case 'navigate':
                handleNavigate(e);
                break;
            case 'open-modal':
                handleOpenModal(e);
                break;
            case 'force-download':
                handleForceDownload(e);
                break;
            case 'select-calculator':
                handleSelectCalculator(e, targetElement);
                break;
            case 'open-modal-with-file':
                handleOpenModalWithFile(e, targetElement);
                break;
            case 'close':
                handleCloseModal(e);
                break;
            case 'previous':
                handlePreviousFile(e);
                break;
            case 'next':
                handleNextFile(e);
                break;
            case 'show-symbol-detail':
                handleShowSymbolDetail(e, targetElement);
                break;
            case 'use-in-stop-loss':
                handleUseInStopLoss(e, targetElement);
                break;
            case 'find-similar':
                handleFindSimilar(e, targetElement);
                break;
            case 'add-to-portfolio':
                handleAddToPortfolio(e, targetElement);
                break;
        }
    });
});

// Blog content loading functionality
function handleLoadContent(e, targetElement) {
    e.preventDefault();
    const element = targetElement || e.target.closest('[data-action="loadContent"]');
    const url = element ? element.getAttribute('data-url') : null;
    if (url) {
        window.location.href = url;
    }
}

// AI musings toggle functionality
// Donate page copy to clipboard functionality
function handleCopyToClipboard(e) {
    e.preventDefault();
    const address = e.target.closest('[data-action="copyToClipboard"]').getAttribute('data-address');
    const currency = e.target.closest('[data-action="copyToClipboard"]').getAttribute('data-currency');
    if (address && currency) {
        copyToClipboard(address, currency);
    }
}

function copyToClipboard(address, currency) {
    // Create a temporary textarea to copy the address
    const tempTextArea = document.createElement('textarea');
    tempTextArea.value = address;
    document.body.appendChild(tempTextArea);
    tempTextArea.select();
    tempTextArea.setSelectionRange(0, 99999); // For mobile devices

    try {
        // Copy to clipboard
        document.execCommand('copy');

        // Show notification
        showCopyNotification(currency + ' address copied to clipboard!');
    } catch (err) {
        // Fallback for modern browsers
        if (navigator.clipboard) {
            navigator.clipboard.writeText(address).then(() => {
                showCopyNotification(currency + ' address copied to clipboard!');
            }).catch(() => {
                showCopyNotification('Failed to copy address');
            });
        } else {
            showCopyNotification('Copy not supported');
        }
    }

    // Remove the temporary textarea
    document.body.removeChild(tempTextArea);
}

function showCopyNotification(message) {
    const notification = document.getElementById('copyNotification');
    const messageEl = document.getElementById('copyMessage');

    if (notification && messageEl) {
        messageEl.textContent = message;
        notification.classList.add('show');

        // Hide after 2 seconds with fade out
        setTimeout(() => {
            notification.classList.remove('show');
        }, 2000);
    }
}

// NFT Gallery modal functionality
function handleCloseModal(e) {
    e.preventDefault();
    if (window.closeModal) {
        window.closeModal();
    } else {
        // Fallback for blog post modals
        closeModal();
    }
}

function handlePreviousImage(e) {
    e.preventDefault();
    if (window.previousImage) {
        window.previousImage();
    }
}

function handleNextImage(e) {
    e.preventDefault();
    if (window.nextImage) {
        window.nextImage();
    }
}

function handleDownloadImage(e) {
    e.preventDefault();
    if (window.downloadImage) {
        window.downloadImage();
    } else {
        // Fallback implementation for NFT galleries
        downloadCurrentImage();
    }
}

function downloadCurrentImage() {
    if (typeof currentImageIndex !== 'undefined' && typeof allImagePaths !== 'undefined') {
        const currentImagePath = allImagePaths[currentImageIndex];
        if (currentImagePath) {
            const link = document.createElement('a');
            link.href = currentImagePath.replace(/'/g, ''); // Remove quotes
            link.download = currentImagePath.split('/').pop().replace(/'/g, '');
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    }
}

function handleNavigate(e) {
    e.preventDefault();
    const targetElement = e.target.closest('[data-action="navigate"]');
    const url = targetElement ? targetElement.getAttribute('data-url') : null;
    if (url) {
        window.location.href = url;
    }
}

// Explorer modal functionality
function handleOpenModalWithFile(e, targetElement) {
    e.preventDefault();
    const element = targetElement || e.target.closest('[data-action="open-modal-with-file"]');
    const outlierFile = element ? element.getAttribute('data-outlier-file') : null;
    const csvFile = element ? element.getAttribute('data-csv-file') : null;
    const displayName = element ? element.getAttribute('data-display-name') : null;
    if (outlierFile && displayName && window.openModalWithFile) {
        window.openModalWithFile(outlierFile, csvFile, displayName);
    }
}

function handlePreviousFile(e) {
    e.preventDefault();
    if (typeof window.previousFile === 'function') {
        window.previousFile();
    } else {
        console.warn('previousFile function not available - page may use custom navigation');
    }
}

function handleNextFile(e) {
    e.preventDefault();
    if (typeof window.nextFile === 'function') {
        window.nextFile();
    } else {
        console.warn('nextFile function not available - page may use custom navigation');
    }
}

// Blog post functionality
function handleOpenModal(e) {
    e.preventDefault();
    openModal();
}

function openModal() {
    const modal = document.getElementById('analysisModal');
    const analysisContent = document.getElementById('analysisContent');

    if (modal && analysisContent) {
        // Check if content is already loaded
        if (analysisContent.textContent.trim() === '') {
            // Load the content from the corresponding .txt file
            loadAnalysisContent(analysisContent);
        }

        modal.style.display = 'flex';
        document.body.classList.add('modal-open');
        modal.focus();

        // Add escape key handler
        const escapeHandler = (event) => {
            if (event.key === 'Escape') {
                closeModal();
                document.removeEventListener('keydown', escapeHandler);
            }
        };
        document.addEventListener('keydown', escapeHandler);
    }
}

function closeModal() {
    const modal = document.getElementById('analysisModal');
    if (modal) {
        modal.style.display = 'none';
        document.body.classList.remove('modal-open');
    }
}

function loadAnalysisContent(contentElement) {
    // Try to find the corresponding .md file (fallback to .txt for legacy)
    const currentPath = window.location.pathname;
    let baseName = '';

    // Extract filename from current path
    if (currentPath.includes('blog/')) {
        const pathParts = currentPath.split('/');
        const htmlFilename = pathParts[pathParts.length - 1] || 'index.html';
        baseName = htmlFilename.replace('.html', '');
    }

    if (baseName) {
        // Try .md first, fall back to .txt
        fetch(baseName + '.md')
            .then(response => {
                if (!response.ok) {
                    return fetch(baseName + '.txt');
                }
                return response;
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to load analysis content');
                }
                return response.text();
            })
            .then(text => {
                // Parse markdown if parser is available, otherwise show plain text
                if (typeof window.parseMarkdown === 'function') {
                    // Replace <pre> with <div> for proper markdown rendering
                    if (contentElement.tagName === 'PRE') {
                        const div = document.createElement('div');
                        div.id = contentElement.id;
                        div.className = contentElement.className;
                        contentElement.parentNode.replaceChild(div, contentElement);
                        contentElement = div;
                    }
                    contentElement.innerHTML = window.parseMarkdown(text);
                } else {
                    contentElement.textContent = text;
                }
            })
            .catch(error => {
                console.error('Error loading analysis content:', error);
                contentElement.textContent = 'Error loading analysis content. Please try again later.';
            });
    } else {
        contentElement.textContent = 'Analysis content not available.';
    }
}

function handleForceDownload(e) {
    e.preventDefault();
    if (window.forceDownload) {
        window.forceDownload(e, e.target);
    } else {
        // Fallback implementation
        forceDownloadFallback(e, e.target);
    }
}

function forceDownloadFallback(event, link) {
    event.preventDefault();
    const url = link.href;
    const filename = link.download || url.split('/').pop();

    fetch(url)
        .then(response => response.blob())
        .then(blob => {
            const downloadUrl = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = downloadUrl;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(downloadUrl);
            document.body.removeChild(a);
        })
        .catch(error => {
            console.error('Download failed:', error);
            // Fallback: Open in new tab
            window.open(url, '_blank', 'noopener,noreferrer');
        });
}

// Calculator selection functionality
function handleSelectCalculator(e, targetElement) {
    e.preventDefault();
    if (!targetElement) return;

    const calculatorType = targetElement.getAttribute('data-calculator');
    if (calculatorType && window.selectCalculator) {
        window.selectCalculator(calculatorType, targetElement);
    }
}

function handleShowSymbolDetail(e, targetElement) {
    e.preventDefault();
    if (!targetElement) return;

    const symbol = targetElement.getAttribute('data-symbol');
    if (symbol && window.showSymbolDetail) {
        window.showSymbolDetail(symbol);
    }
}

function handleUseInStopLoss(e, targetElement) {
    e.preventDefault();
    if (!targetElement) return;

    const symbol = targetElement.getAttribute('data-symbol');
    if (symbol && window.useInStopLoss) {
        window.useInStopLoss(symbol);
    }
}

function handleFindSimilar(e, targetElement) {
    e.preventDefault();
    if (!targetElement) return;

    const symbol = targetElement.getAttribute('data-symbol');
    if (symbol && window.findSimilar) {
        window.findSimilar(symbol);
    }
}

function handleAddToPortfolio(e, targetElement) {
    e.preventDefault();
    if (!targetElement) return;

    const symbol = targetElement.getAttribute('data-symbol');
    if (symbol && window.addSymbolToPortfolio) {
        window.addSymbolToPortfolio(symbol);
    }
}

// Make functions globally accessible for backward compatibility
window.copyToClipboard = copyToClipboard;
window.showCopyNotification = showCopyNotification;
window.downloadCurrentImage = downloadCurrentImage;
window.forceDownloadFallback = forceDownloadFallback;
window.openModal = openModal;
window.closeModal = closeModal;
window.loadAnalysisContent = loadAnalysisContent;
window.handleSelectCalculator = handleSelectCalculator;
window.handleShowSymbolDetail = handleShowSymbolDetail;
window.handleUseInStopLoss = handleUseInStopLoss;
window.handleFindSimilar = handleFindSimilar;
window.handleAddToPortfolio = handleAddToPortfolio;
