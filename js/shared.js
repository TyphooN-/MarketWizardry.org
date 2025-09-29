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
            case 'toggle-musing':
                handleToggleMusing(e);
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
                handleOpenModalWithFile(e);
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
            case 'open-image':
                handleOpenImage(e);
                break;
            case 'stop-propagation':
                e.stopPropagation();
                break;
            case 'show-symbol-detail':
                handleShowSymbolDetail(e, targetElement);
                break;
            case 'use-in-stop-loss':
                handleUseInStopLoss(e, targetElement);
                break;
            case 'use-in-portfolio':
                handleUseInPortfolio(e, targetElement);
                break;
            case 'find-similar':
                handleFindSimilar(e, targetElement);
                break;
            case 'add-to-portfolio':
                handleAddToPortfolio(e, targetElement);
                break;
            case 'back-to-list':
                handleBackToList(e, targetElement);
                break;
        }
    });
});

// Blog content loading functionality
function handleLoadContent(e, targetElement) {
    e.preventDefault();
    const element = targetElement || e.target.closest('[data-action="loadContent"]');
    const url = element ? element.getAttribute('data-url') : null;
    if (url && parent.loadContent) {
        parent.loadContent(url);
    }
}

// AI musings toggle functionality
function handleToggleMusing(e) {
    e.preventDefault();
    const filename = e.target.getAttribute('data-filename');
    if (filename) {
        toggleMusing(filename);
    }
}

function toggleMusing(filename) {
    const content = document.getElementById('content-' + filename);
    const btn = document.getElementById('btn-' + filename);

    if (content && btn) {
        if (content.style.display === 'none') {
            content.style.display = 'block';
            btn.textContent = 'Collapse';
        } else {
            content.style.display = 'none';
            btn.textContent = 'Expand';
        }
    }
}

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
function handleOpenModalWithFile(e) {
    e.preventDefault();
    const outlierFile = e.target.getAttribute('data-outlier-file');
    const csvFile = e.target.getAttribute('data-csv-file');
    const displayName = e.target.getAttribute('data-display-name');
    if (outlierFile && displayName && window.openModalWithFile) {
        window.openModalWithFile(outlierFile, csvFile, displayName);
    }
}

function handlePreviousFile(e) {
    e.preventDefault();
    if (window.previousFile) {
        window.previousFile();
    }
}

function handleNextFile(e) {
    e.preventDefault();
    if (window.nextFile) {
        window.nextFile();
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

        modal.style.display = 'block';
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
    }
}

function loadAnalysisContent(contentElement) {
    // Try to find the corresponding .txt file
    const currentPath = window.location.pathname;
    let txtFilename = '';

    // Extract filename from current path and construct .txt filename
    if (currentPath.includes('blog/')) {
        const pathParts = currentPath.split('/');
        const htmlFilename = pathParts[pathParts.length - 1] || 'index.html';
        const baseName = htmlFilename.replace('.html', '');
        txtFilename = baseName + '.txt';
    }

    if (txtFilename) {
        fetch(txtFilename)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to load analysis content');
                }
                return response.text();
            })
            .then(text => {
                contentElement.textContent = text;
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
            window.open(url, '_blank');
        });
}

// NFT Gallery image opening functionality
function handleOpenImage(e) {
    e.preventDefault();
    const index = parseInt(e.target.getAttribute('data-index'));
    if (!isNaN(index) && window.openModal) {
        window.openModal(index);
    } else if (!isNaN(index) && window.openImage) {
        window.openImage(index);
    }
}

// Calculator selection functionality
function handleSelectCalculator(e, targetElement) {
    e.preventDefault();
    const calculatorType = targetElement.getAttribute('data-calculator');

    if (calculatorType && window.selectCalculator) {
        window.selectCalculator(calculatorType, targetElement);
    } else {
        console.error('Calculator type not found or selectCalculator function not available');
    }
}

function handleShowSymbolDetail(e, targetElement) {
    e.preventDefault();
    const symbol = targetElement.getAttribute('data-symbol');
    console.log('🎯 handleShowSymbolDetail called for symbol:', symbol);

    if (symbol && window.showSymbolDetail) {
        window.showSymbolDetail(symbol);
        console.log('✅ showSymbolDetail called successfully from shared.js');
    } else {
        console.error('❌ Symbol or showSymbolDetail function not available:', {
            symbol: symbol,
            showSymbolDetailExists: !!window.showSymbolDetail
        });
        alert('Error: Unable to show symbol details');
    }
}

function handleUseInStopLoss(e, targetElement) {
    e.preventDefault();
    const symbol = targetElement.getAttribute('data-symbol');
    console.log('📊 handleUseInStopLoss called for symbol:', symbol);

    if (symbol && window.useInStopLoss) {
        window.useInStopLoss(symbol);
        console.log('✅ useInStopLoss called successfully from shared.js');
    } else {
        console.error('❌ Symbol or useInStopLoss function not available');
        alert('Error: Stop Loss function not available');
    }
}

function handleUseInPortfolio(e, targetElement) {
    e.preventDefault();
    const symbol = targetElement.getAttribute('data-symbol');
    console.log('💼 handleUseInPortfolio called for symbol:', symbol);

    if (symbol && window.useInPortfolio) {
        window.useInPortfolio(symbol);
        console.log('✅ useInPortfolio called successfully from shared.js');
    } else {
        console.error('❌ Symbol or useInPortfolio function not available');
        alert('Error: Portfolio function not available');
    }
}

function handleFindSimilar(e, targetElement) {
    e.preventDefault();
    const symbol = targetElement.getAttribute('data-symbol');
    console.log('🔍 handleFindSimilar called for symbol:', symbol);

    if (symbol && window.findSimilar) {
        window.findSimilar(symbol);
        console.log('✅ findSimilar called successfully from shared.js');
    } else {
        console.error('❌ Symbol or findSimilar function not available');
        alert('Error: Find Similar function not available');
    }
}

function handleAddToPortfolio(e, targetElement) {
    e.preventDefault();
    const symbol = targetElement.getAttribute('data-symbol');
    console.log('📈 handleAddToPortfolio called for symbol:', symbol);

    if (symbol && window.addSymbolToPortfolio) {
        window.addSymbolToPortfolio(symbol);
        console.log('✅ addSymbolToPortfolio called successfully from shared.js');
    } else {
        console.error('❌ Symbol or addSymbolToPortfolio function not available');
        alert('Error: Add to Portfolio function not available');
    }
}

function handleBackToList(e, targetElement) {
    e.preventDefault();
    console.log('🔙 handleBackToList called');

    if (window.backToSymbolList) {
        window.backToSymbolList();
        console.log('✅ backToSymbolList called successfully from shared.js');
    } else {
        console.error('❌ backToSymbolList function not available');
        alert('Error: Back to List function not available');
    }
}

// Make functions globally accessible for backward compatibility
window.toggleMusing = toggleMusing;
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
window.handleUseInPortfolio = handleUseInPortfolio;
window.handleFindSimilar = handleFindSimilar;
window.handleAddToPortfolio = handleAddToPortfolio;
window.handleBackToList = handleBackToList;