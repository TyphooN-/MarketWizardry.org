// EV Explorer functionality

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

// Event delegation for data-action attributes
document.addEventListener('click', function(e) {
    const action = e.target.getAttribute('data-action');
    if (action) {
        switch(action) {
            case 'open-modal-with-file':
                e.preventDefault();
                const outlierFile = e.target.getAttribute('data-outlier-file');
                const csvFile = e.target.getAttribute('data-csv-file');
                const displayName = e.target.getAttribute('data-display-name');
                if (outlierFile && displayName) {
                    openModalWithFile(outlierFile, csvFile, displayName);
                }
                break;
            case 'close-modal':
                closeModal();
                break;
            case 'previous':
                previousFile();
                break;
            case 'next':
                nextFile();
                break;
        }
    }
});

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

    document.getElementById('modal-title').innerText = title;
    document.getElementById('csv-link').href = csvFile;
    document.getElementById('csv-link').style.display = csvFile ? 'inline' : 'none';
    document.getElementById('outlier-modal').style.display = 'flex';
    updateNavCounter();

    // Load outlier file content
    fetch(outlierFile)
        .then(response => response.text())
        .then(data => {
            // Convert URLs to clickable links
            const linkifiedData = linkifyUrls(data);
            document.getElementById('outlier-content').innerHTML = linkifiedData;
        })
        .catch(error => {
            document.getElementById('outlier-content').textContent = 'Error loading file: ' + error;
        });
}

function closeModal() {
    document.getElementById('outlier-modal').style.display = 'none';
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