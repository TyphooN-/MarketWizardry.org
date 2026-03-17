# ADR-006: Dual CSS Strategy - shared-styles.css and Page-Specific Files

**Status:** Accepted
**Date:** 2026-03-16
**Decision Makers:** TyphooN

## Context

The site has diverse page types -- galleries, data explorers, calculators, blog posts -- each with unique layout needs, but all sharing the terminal CRT aesthetic (ADR-003). A decision was needed on whether to consolidate all styles into a single CSS file or split them across multiple files. The strict CSP (ADR-001) requires that all styles live in external CSS files, making this organization particularly important.

## Decision

Use a dual CSS strategy:

- **`css/shared-styles.css`** (2044+ lines) contains all common styles used across multiple pages: base terminal aesthetic, CRT effects (scan lines, flicker), modal styles, gallery grid layouts, breadcrumb navigation, mobile responsive breakpoints, and the modal button bar.
- **Page-specific CSS files** (e.g., `blog.css`, `calculator.css`) contain styles unique to individual page types that are not shared elsewhere.

Every page loads `shared-styles.css`. Pages with unique layouts additionally load their page-specific CSS file.

## Consequences

**Benefits:**
- `shared-styles.css` is cached after the first page visit, making subsequent page loads faster since the common styles are already in the browser cache.
- Common components (modals, grids, breadcrumbs, CRT effects) are defined once and reused everywhere, avoiding duplication.
- Page-specific files keep unique styles isolated, making it clear which styles belong to which feature.
- The 1-year cache policy on CSS files (defined in `.htaccess`) maximizes the caching benefit of the shared file.

**Trade-offs:**
- `shared-styles.css` is large (2044+ lines) and continues to grow, which increases the initial page load cost.
- Risk of CSS selector duplication or conflicts between shared and page-specific files (identified in the 2026-03 audit).
- Contributors must decide whether a new style belongs in the shared file or a page-specific file, which is not always obvious.
- The shared file contains styles for pages a given visitor may never see, resulting in some wasted bytes.
