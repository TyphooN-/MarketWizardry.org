// Set viewport immediately for mobile scaling
if (!document.querySelector('meta[name="viewport"]')) {
    const viewport = document.createElement('meta');
    viewport.name = 'viewport';
    viewport.content = 'width=device-width, initial-scale=1.0';
    document.head.insertBefore(viewport, document.head.firstChild);
}