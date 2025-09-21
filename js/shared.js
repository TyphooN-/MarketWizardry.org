// Shared JavaScript functionality for MarketWizardry.org
// Handles data-action event delegation for all pages

document.addEventListener('DOMContentLoaded', function() {
    // Global event delegation for data-action attributes
    document.addEventListener('click', function(e) {
        const action = e.target.getAttribute('data-action');
        if (!action) return;

        switch(action) {
            case 'loadContent':
                handleLoadContent(e);
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
        }
    });
});

// Blog content loading functionality
function handleLoadContent(e) {
    e.preventDefault();
    const url = e.target.getAttribute('data-url');
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
    const url = e.target.getAttribute('data-url');
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
    if (window.openModal) {
        window.openModal();
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

// Make functions globally accessible for backward compatibility
window.toggleMusing = toggleMusing;
window.copyToClipboard = copyToClipboard;
window.showCopyNotification = showCopyNotification;
window.downloadCurrentImage = downloadCurrentImage;
window.forceDownloadFallback = forceDownloadFallback;