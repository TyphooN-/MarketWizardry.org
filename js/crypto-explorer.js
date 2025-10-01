// Crypto Explorer functionality

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

    // Handle report link (points to the outlier/analysis file)
    const reportLink = document.getElementById('report-link');
    if (reportLink) {
        reportLink.href = outlierFile;
        reportLink.style.display = outlierFile ? 'inline' : 'none';
    }

    document.getElementById('outlier-modal').style.display = 'block';
    updateNavCounter();

    // Load outlier file content
    fetch(outlierFile)
        .then(response => response.text())
        .then(data => {
            document.getElementById('outlier-content').textContent = data;
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
        openModalWithFile(file.outlier, file.csv, file.title);
    }
}

function nextFile() {
    if (currentFileIndex < filesList.length - 1) {
        currentFileIndex++;
        const file = filesList[currentFileIndex];
        openModalWithFile(file.outlier, file.csv, file.title);
    }
}

function updateNavCounter() {
    document.getElementById('nav-counter').textContent =
        `${currentFileIndex + 1} of ${filesList.length}`;
}

// Initialize files list from grid entries
document.addEventListener('DOMContentLoaded', function() {
    const entries = document.querySelectorAll('.file-entry a');
    filesList = Array.from(entries).map(entry => ({
        outlier: entry.getAttribute('data-outlier-file'),
        csv: entry.getAttribute('data-csv-file'),
        title: entry.textContent.trim()
    }));
});

// Keyboard navigation
document.addEventListener('keydown', function(event) {
    const modal = document.getElementById('outlier-modal');
    if (modal && modal.style.display === 'block') {
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

// Close modal when clicking outside
window.addEventListener('click', function(event) {
    const modal = document.getElementById('outlier-modal');
    if (event.target == modal) {
        closeModal();
    }
});

// Make functions globally accessible for backward compatibility
window.openModalWithFile = openModalWithFile;
window.closeModal = closeModal;
window.previousFile = previousFile;
window.nextFile = nextFile;
