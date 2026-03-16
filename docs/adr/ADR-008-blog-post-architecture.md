# ADR-008: Blog Post Architecture - Individual HTML Pages with Modal Content Loading

**Status:** Accepted
**Date:** 2026-03-16
**Decision Makers:** TyphooN

## Context

MarketWizardry.org includes a blog section for trading insights and market analysis. Blog posts need to maintain the terminal CRT aesthetic (ADR-003), comply with CSP (ADR-001), and be individually indexable by search engines with their own canonical URLs and Open Graph tags. A decision was needed on whether to use a single-page blog with dynamic content loading or individual pages per post.

## Decision

Each blog post is a standalone HTML page with:

- Its own meta tags (canonical URL, OG tags, Twitter Cards) generated via `seo_templates.py` for full SEO coverage.
- Schema.org breadcrumb navigation linking back through the blog index.
- A modal that loads post content from `.txt` files via `fetch()` at runtime.
- Content authored as markdown in `.txt` files, parsed client-side by `js/ai-musings.js` using a markdown parser.

The blog index (`blog.html`) links directly to individual post pages. The `ai-musings.js` script handles content fetching, markdown parsing, and rendering into the page.

## Consequences

**Benefits:**
- Full SEO for each post: individual canonical URLs, Open Graph tags, and Twitter Cards enable rich search results and social sharing.
- Content is separated from presentation: blog text lives in `.txt` files as markdown, while the HTML page provides the shell and styling.
- Each post page is a complete, standalone document that can be cached independently (1-hour HTML cache policy).
- The markdown-in-text-file approach makes content authoring simpler than writing full HTML.

**Trade-offs:**
- Two files per post (HTML page + `.txt` content file) must be created and kept in sync.
- Client-side markdown parsing adds a render step after page load; content is not visible until JavaScript executes and the `fetch()` completes.
- Search engine crawlers that do not execute JavaScript will not see the blog post body content (only the meta tags and page shell).
- The `fetch()` call to load `.txt` files requires the content to be on the same origin (enforced by `connect-src 'self'` in the CSP).
