# ADR-009: Modal UI Standardization

**Status:** Accepted
**Date:** 2026-03-17
**Decision Makers:** TyphooN

## Context

The site has modals on 120+ pages (galleries, explorers, blog posts, AI musings, terms). Over time, different modal structures emerged: some had the close button isolated at the top, navigation at the bottom, and download on a separate row. This caused inconsistent UX and mobile layout issues (buttons wrapping, controls spread across 3+ rows).

## Decision

All modals use a standardized structure:

```html
<div class="modal" id="..." role="dialog" aria-modal="true">
    <div class="modal-content">
        <div class="modal-header">
            <div class="filename-display" id="modalFilename"></div>
            <div class="modal-button-bar">
                <button class="nav-button" data-action="previous-image">← Previous</button>
                <span class="image-counter"></span>
                <button class="nav-button" data-action="next-image">Next →</button>
                <button class="nav-button" data-action="download-image">⬇ Download</button>
                <button class="close-button" data-action="close-modal">✕</button>
            </div>
        </div>
        <img src="" alt="Fullscreen image" class="full-image">
    </div>
</div>
```

Key rules:
- All controls on a **single row** inside `.modal-button-bar`
- Controls appear **above** the content (image or text)
- `.modal-button-bar` uses `flex-wrap: nowrap` on mobile with horizontal scroll
- `role="dialog"` and `aria-modal="true"` for accessibility
- Body gets `modal-open` class when modal opens (prevents background scrolling)
- `dvh` units used for height constraints (accounts for mobile browser chrome)

## Consequences

**Benefits:**
- Consistent UX across all 120+ pages
- Single-row controls work on mobile without wrapping
- Accessibility attributes enable screen reader support
- Body scroll lock prevents touch-scroll-through on mobile

**Trade-offs:**
- All hand-authored HTML files must follow this pattern exactly
- Python generators must produce this structure
- The old `.nav-buttons` and `.download-container` CSS classes are deprecated (dead CSS removed)
