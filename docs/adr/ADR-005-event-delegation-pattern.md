# ADR-005: Event Delegation Pattern for Interactive Elements

**Status:** Accepted
**Date:** 2026-03-16
**Decision Makers:** TyphooN

## Context

The strict Content Security Policy (see ADR-001) prohibits inline event handlers such as `onclick`, `onchange`, `onsubmit`, and `javascript:` URLs. All interactive elements -- modal navigation buttons, gallery image clicks, calculator inputs, explorer controls -- need a CSP-compliant mechanism for binding behavior to DOM elements.

## Decision

All interactivity uses `data-action` attributes on HTML elements, with centralized event delegation handlers in external JavaScript files. The pattern is:

**HTML (in generated pages or templates):**
```html
<button data-action="next-image">Next</button>
<button data-action="close-modal">Close</button>
```

**JavaScript (in `/js/shared.js` or feature-specific JS files):**
```javascript
document.addEventListener('click', function(e) {
    if (e.target.dataset.action === 'next-image') {
        handleNextImage();
    }
    if (e.target.dataset.action === 'close-modal') {
        handleCloseModal();
    }
});
```

This pattern is used consistently across `shared.js`, `gallery.js`, `calculator.js`, `crypto-explorer.js`, and `ai-musings.js`.

## Consequences

**Benefits:**
- Fully CSP compliant: no inline handlers means no `unsafe-inline` requirement.
- Centralized event handling reduces the number of event listeners attached to the DOM.
- Works with dynamically generated content (event delegation catches events from elements added after page load).
- `data-action` attributes serve as self-documenting markers of interactive elements in the HTML.

**Trade-offs:**
- More indirection: reading the HTML alone does not reveal which function handles a given action. Developers must search the JS files for the corresponding `data-action` string.
- All click handlers flow through a single delegation point, which can become long if many actions are registered in one file.
- Requires naming discipline to avoid `data-action` collisions across different JS modules.
- Slightly more verbose than inline handlers for simple one-off interactions.
