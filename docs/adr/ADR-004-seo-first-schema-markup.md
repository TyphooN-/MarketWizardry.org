# ADR-004: SEO-First Approach with Schema.org Markup

**Status:** Accepted
**Date:** 2026-03-16
**Decision Makers:** TyphooN

## Context

MarketWizardry.org provides financial trading tools (ATR, VAR, EV explorers), calculators, and blog content that users discover primarily through search engines. Discoverability is critical for the site's reach. The site needed a systematic approach to SEO that could be applied consistently across 19+ root pages and 106+ generated gallery pages without manual per-page effort.

## Decision

Adopt an SEO-first approach where every page receives comprehensive meta tags and structured data, generated automatically via `seo_templates.py`. Specifically:

- **Every page** includes: canonical URL, meta description, keywords, robots directive, Open Graph tags (title, description, URL, type, image), and Twitter Card tags.
- **Major pages** include Schema.org breadcrumb navigation with `BreadcrumbList` microdata.
- **Content pages** include JSON-LD structured data (`application/ld+json` script blocks) describing the page type, name, description, and URL.
- **`seo_templates.py`** provides the `SEOManager` class with `generate_enhanced_meta_tags()`, `generate_breadcrumbs()`, and `generate_json_ld_schema()` methods. The `PAGE_CONFIGS` dictionary stores per-page SEO settings.
- All Python generators (`generate_gallery.py`, blog generators) use `SEOManager` to produce consistent SEO markup.

## Consequences

**Benefits:**
- Excellent search engine visibility with rich snippets, breadcrumb trails, and social sharing previews.
- Consistent meta tags across all pages, including auto-generated gallery pages.
- Centralized SEO configuration in `PAGE_CONFIGS` makes bulk updates straightforward.
- JSON-LD blocks use `application/ld+json` type, which is CSP-compliant (not executed as scripts).

**Trade-offs:**
- Adds complexity to page generation: every new page or generator must integrate with `seo_templates.py`.
- Meta descriptions and keywords must be maintained and kept under character limits (160 chars for descriptions).
- Changes to SEO strategy require updating both the `SEOManager` class and re-running all generators.
- Risk of stale meta tags if pages are manually edited without updating the corresponding `PAGE_CONFIGS` entry.
