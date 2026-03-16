# ADR-007: Gallery Image Generation Pipeline

**Status:** Accepted
**Date:** 2026-03-16
**Decision Makers:** TyphooN

## Context

MarketWizardry.org hosts 106+ NFT gallery pages, each displaying a user-specific collection of images stored in `nft-gallery/*/webp/` directories. Manually creating and maintaining HTML pages for each gallery is impractical. The gallery pages must also comply with the strict CSP (ADR-001), which prohibits inline scripts -- meaning image path data cannot be embedded directly in HTML script tags.

## Decision

Use `generate_gallery.py` as the single entry point for all gallery generation. The script:

1. Scans `nft-gallery/*/webp/` directories to discover user image collections.
2. Generates per-user gallery HTML pages (`nft-gallery/*_gallery.html`) with full SEO markup via `seo_templates.py`.
3. Generates external JavaScript data files (`js/gallery-data-*.js`) containing image path arrays, keeping data out of inline scripts for CSP compliance.
4. Generates aggregate pages: `nft-gallery/all.html` (all images) and `ai-art.html` (AI art collection).
5. Generates the main gallery index at `nft-gallery.html`.

The modal viewer structure uses `data-action` attributes (ADR-005) for navigation (previous, next, download, close).

Run from the project root: `python3 generate_gallery.py`.

## Consequences

**Benefits:**
- Fully automated: adding new images to a user's `webp/` directory and re-running the generator is all that is needed.
- CSP compliant: image data is loaded from external JS files, not inline scripts.
- Consistent SEO markup across all 106+ gallery pages via `seo_templates.py` integration.
- Modal navigation and lazy loading are applied uniformly to all generated galleries.

**Trade-offs:**
- Requires manual execution of the generator script when images change; there is no file watcher or CI trigger.
- Generated HTML files are committed to version control, adding to repository size.
- All gallery pages share the same template structure; per-gallery customization requires modifying the generator.
- The generator must be kept in sync with any changes to `shared-styles.css` modal classes or `gallery.js` data format expectations.
