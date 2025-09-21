// Event delegation for data-action attributes
document.addEventListener('click', function(e) {
    if (e.target.hasAttribute('data-action')) {
        const action = e.target.getAttribute('data-action');

        switch(action) {
            case 'loadContent':
                const url = e.target.getAttribute('data-url');
                if (url && parent.loadContent) {
                    parent.loadContent(url);
                }
                e.preventDefault();
                break;
        }
    }
});