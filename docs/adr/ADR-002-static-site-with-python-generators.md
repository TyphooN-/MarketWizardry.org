# ADR-002: Static Site Architecture with Python Generators

**Status:** Accepted
**Date:** 2026-03-16
**Decision Makers:** TyphooN

## Context

MarketWizardry.org hosts financial data explorers (ATR, VAR, EV, Crypto), NFT/AI art galleries, trading calculators, and blog content. The site needs to serve auto-generated pages built from CSV and JSON data files while maintaining fast load times and simple deployment. A decision was needed on whether to use a dynamic server-side framework, a static site generator (Hugo, Jekyll), or a custom approach.

## Decision

Use a static HTML/CSS/JS architecture served by Apache, with custom Python scripts to generate content pages. Key generators include:

- **`generate_gallery.py`** - Scans image directories and produces 106+ gallery HTML pages plus external JS data files.
- **`seo_templates.py`** - Provides an `SEOManager` class that generates meta tags, breadcrumbs, and JSON-LD schema markup for all pages.
- **Explorer pages** - Render financial data from CSV files in the `atr-explorer/`, `var-explorer/`, `ev-explorer/`, and `crypto-explorer/` directories.

All generated output is plain HTML that can be served directly by Apache with no runtime dependencies.

## Consequences

**Benefits:**
- Extremely fast page loads with no server-side processing at request time.
- Aggressive caching strategy (1 year for CSS/JS/images, 1 hour for HTML) since pages are static files.
- No runtime dependency on Python, Node.js, or any application server in production.
- Simple deployment: generated files are committed to the repository and served as-is.
- Full control over output HTML, enabling strict CSP compliance.

**Trade-offs:**
- Manual regeneration required when content changes (running `python3 generate_gallery.py` from the project root).
- No dynamic content at request time; all interactivity is client-side JavaScript.
- Adding a new content type requires writing or modifying Python generator scripts.
- Generated HTML files are checked into version control, increasing repository size.
