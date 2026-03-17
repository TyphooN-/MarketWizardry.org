// ATR Explorer functionality

// Function to convert URLs in text to clickable links
function linkifyUrls(text) {
    // Escape HTML to prevent XSS
    const escapeHtml = (str) => {
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    };

    // Pattern to match URLs (http, https, ftp)
    const urlPattern = /(https?:\/\/[^\s]+)/g;

    // Split text by URLs, escape non-URL parts, and reconstruct with links
    let lastIndex = 0;
    let result = '';
    let match;

    while ((match = urlPattern.exec(text)) !== null) {
        // Escape text before the URL
        result += escapeHtml(text.substring(lastIndex, match.index));

        // Remove trailing punctuation that shouldn't be part of the URL
        let cleanUrl = match[0].replace(/[.,;:!?)]+$/, '');

        // Add the clickable link
        result += `<a href="${escapeHtml(cleanUrl)}" target="_blank" rel="noopener noreferrer">${escapeHtml(cleanUrl)}</a>`;

        lastIndex = match.index + match[0].length;
    }

    // Escape any remaining text after the last URL
    result += escapeHtml(text.substring(lastIndex));

    return result;
}

// Event delegation handled by shared.js - functions exported to window scope below

let currentFileIndex = 0;
let filesList = [];

function openModalWithFile(outlierFile, csvFile, title) {
    // Find current file index
    for (let i = 0; i < filesList.length; i++) {
        if (filesList[i].outlier === outlierFile) {
            currentFileIndex = i;
            break;
        }
    }

    const modalTitle = document.getElementById('modal-title');
    const csvLink = document.getElementById('csv-link');
    const modal = document.getElementById('outlier-modal');
    const outlierContent = document.getElementById('outlier-content');

    if (modalTitle) modalTitle.innerText = title;
    if (csvLink) {
        csvLink.href = csvFile || '#';
        csvLink.style.display = csvFile ? 'inline' : 'none';
    }
    if (modal) {
        modal.style.display = 'flex';
        document.body.classList.add('modal-open');
    }
    updateNavCounter();

    // Load outlier file content
    fetch(outlierFile)
        .then(response => response.text())
        .then(data => {
            // Convert URLs to clickable links
            const linkifiedData = linkifyUrls(data);
            if (outlierContent) outlierContent.innerHTML = linkifiedData;
        })
        .catch(error => {
            if (outlierContent) outlierContent.textContent = 'Error loading file: ' + error;
        });
}

function closeModal() {
    const modal = document.getElementById('outlier-modal');
    if (modal) {
        modal.style.display = 'none';
        document.body.classList.remove('modal-open');
    }
}

function previousFile() {
    if (currentFileIndex > 0) {
        currentFileIndex--;
        const file = filesList[currentFileIndex];
        openModalWithFile(file.outlier, file.csv, file.display);
    }
}

function nextFile() {
    if (currentFileIndex < filesList.length - 1) {
        currentFileIndex++;
        const file = filesList[currentFileIndex];
        openModalWithFile(file.outlier, file.csv, file.display);
    }
}

function updateNavCounter() {
    const counter = document.getElementById('nav-counter');
    if (counter && filesList.length > 0) {
        counter.textContent = `${currentFileIndex + 1} of ${filesList.length}`;
    }
}

// Keyboard navigation
document.addEventListener('keydown', function(event) {
    const modal = document.getElementById('outlier-modal');
    if (modal && modal.style.display === 'flex') {
        switch(event.key) {
            case 'ArrowLeft':
                previousFile();
                event.preventDefault();
                break;
            case 'ArrowRight':
                nextFile();
                event.preventDefault();
                break;
            case 'Escape':
                closeModal();
                event.preventDefault();
                break;
        }
    }
});

// Window click event to close modal
window.addEventListener('click', function(event) {
    const modal = document.getElementById('outlier-modal');
    if (event.target === modal) {
        closeModal();
    }
});

// Initialize files list on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeFilesList();
});

function initializeFilesList() {
    const entries = document.querySelectorAll('.file-entry a');
    filesList = Array.from(entries).map(entry => ({
        outlier: entry.getAttribute('data-outlier-file'),
        csv: entry.getAttribute('data-csv-file'),
        display: entry.getAttribute('data-display-name')
    }));
}

// Export functions to window scope for shared.js event delegation
window.openModalWithFile = openModalWithFile;
window.closeModal = closeModal;
window.previousFile = previousFile;
window.nextFile = nextFile;