// Event delegation for data-action attributes
document.addEventListener('click', function(e) {
    // Check if clicked element or any parent has data-action
    let targetElement = e.target.closest('[data-action]');

    if (targetElement) {
        const action = targetElement.getAttribute('data-action');

        switch(action) {
            case 'loadContent':
                const url = targetElement.getAttribute('data-url');
                if (url && parent.loadContent) {
                    parent.loadContent(url);
                }
                e.preventDefault();
                break;
        }
    }
});