# SEO Automation for MarketWizardry.org

**Automated SEO maintenance with JSON-LD structured data generation**

## Overview

This suite of Python scripts automatically generates and maintains SEO metadata and JSON-LD structured data for all pages on MarketWizardry.org. All generated content is **CSP-compliant** using external JavaScript files.

## Quick Start

To regenerate all SEO components across the entire site:

```bash
cd /home/typhoon/git/MarketWizardry.org
python3 generate_all_seo.py
```

This master script runs all individual generators in sequence.

---

## Individual Generators

### 1. `generate_gallery.py`
**Purpose:** Generate NFT gallery pages with ImageGallery JSON-LD schema

**Generates:**
- Main gallery index: `nft-gallery.html`
- Individual artist galleries: `nft-gallery/*_gallery.html` (106+ pages)
- Aggregated gallery: `nft-gallery/all.html`
- AI art gallery: `ai-art.html`
- External JSON-LD scripts: `js/jsonld-nft-gallery-*.js`
- External gallery data: `js/gallery-data-*.js`

**Usage:**
```bash
python3 generate_gallery.py
```

**Schema Type:** ImageGallery, Collection, CreativeWork

---

### 2. `generate_root_pages_seo.py`
**Purpose:** Add JSON-LD to root pages (explorer tools, main pages)

**Targets:**
- `var-explorer.html` - SoftwareApplication schema
- `atr-explorer.html` - SoftwareApplication schema
- `ev-explorer.html` - SoftwareApplication schema
- `crypto-explorer.html` - SoftwareApplication schema
- `darwinex-radar.html` - SoftwareApplication schema
- `blog.html` - Blog schema
- `ai-musings.html` - Blog schema
- `market-wizardry.html` - WebSite schema
- `var-cult.html` - WebPage schema
- `code.html` - SoftwareSourceCode schema
- `about.html` - AboutPage schema
- `404.html` - WebPage schema
- `ai-art.html` - CreativeWork schema

**Generates:**
- External JSON-LD scripts: `js/jsonld-*.js`
- Adds `<script src="/js/jsonld-*.js"></script>` to HTML

**Usage:**
```bash
python3 generate_root_pages_seo.py
```

**Features:**
- Detects existing JSON-LD and skips pages that already have it
- Uses appropriate schema types for each page
- Maintains CSP compliance

---

### 3. `generate_blog_seo.py`
**Purpose:** Add Article JSON-LD schema to blog posts

**Targets:**
- All HTML files in `blog/` directory (46+ posts)

**Generates:**
- External JSON-LD scripts: `js/jsonld-blog-*.js`
- Adds Article schema with:
  - Headline, description, URL
  - Published/modified dates
  - Author information (TyphooN)
  - Publisher information (MarketWizardry.org)
  - Article section and keywords

**Usage:**
```bash
python3 generate_blog_seo.py
```

**Features:**
- Automatically extracts metadata from existing HTML
- Pulls published dates from `article:published_time` meta tag
- Extracts title, description, keywords from existing meta tags
- Uses BeautifulSoup for robust HTML parsing

---

## Master Generator Script

### `generate_all_seo.py`
**Purpose:** Run all SEO generators in sequence

**Executes:**
1. `generate_gallery.py` → 106+ gallery pages
2. `generate_root_pages_seo.py` → 13 root pages
3. `generate_blog_seo.py` → 46+ blog posts

**Usage:**
```bash
python3 generate_all_seo.py
```

**Output:**
- Progress for each generator
- Summary of successes/failures
- Exit code 0 if all succeed, 1 if any fail

---

## CSP Compliance

All generated JSON-LD uses **external JavaScript files** to comply with the strict Content Security Policy in `.htaccess`:

```apache
Content-Security-Policy: default-src 'self'; script-src 'self';
```

**Pattern:**
```html
<!-- In HTML -->
<script src="/js/jsonld-page-name.js"></script>
```

```javascript
// In external JS file
(function() {
    'use strict';

    const jsonLdData = {
        "@context": "https://schema.org",
        "@type": "Article",
        ...
    };

    const script = document.createElement('script');
    script.type = 'application/ld+json';
    script.textContent = JSON.stringify(jsonLdData, null, 2);
    document.head.appendChild(script);
})();
```

This pattern:
- ✅ Complies with CSP (no inline scripts)
- ✅ Validates with Google's Rich Results Test
- ✅ Allows easy updating without editing HTML
- ✅ Maintains separation of concerns

---

## Maintenance Workflow

### When to Run Generators

**Run `generate_gallery.py` when:**
- New artists are added to nft-gallery/
- Gallery flavor text is updated
- Gallery images change

**Run `generate_root_pages_seo.py` when:**
- New root pages are created
- Page descriptions change
- Schema types need updating

**Run `generate_blog_seo.py` when:**
- New blog posts are published
- Blog metadata changes

**Run `generate_all_seo.py`:**
- After major site updates
- Before deployment
- Weekly/monthly maintenance

### Quick Regeneration

```bash
# One command to update everything
cd /home/typhoon/git/MarketWizardry.org && python3 generate_all_seo.py
```

---

## Testing SEO Output

### Validate JSON-LD

**Google Rich Results Test:**
```
https://search.google.com/test/rich-results
```

**Schema.org Validator:**
```
https://validator.schema.org/
```

### Check CSP Compliance

```bash
# Search for inline styles (should return 0)
grep -r 'style=' *.html | wc -l

# Search for inline scripts (should only show src= references)
grep -r '<script>' *.html | grep -v 'src='

# Verify JSON-LD files exist
ls -l js/jsonld-*.js | wc -l
```

### Browser Console Check

1. Open any page in Chrome/Firefox
2. Open Developer Tools (F12)
3. Check Console for CSP violations
4. Should see: **No errors** ✅

---

## Dependencies

All generators use standard library modules:
- `os` - File system operations
- `re` - Regular expressions
- `json` - JSON formatting
- `subprocess` - Running generators
- `BeautifulSoup4` - HTML parsing (blog generator only)

**Install BeautifulSoup if needed:**
```bash
pip install beautifulsoup4
```

---

## File Structure

```
MarketWizardry.org/
├── generate_all_seo.py           # Master generator script
├── generate_gallery.py           # NFT gallery generator
├── generate_root_pages_seo.py    # Root pages JSON-LD
├── generate_blog_seo.py          # Blog Article schema
├── seo_templates.py              # SEO helper library
├── js/
│   ├── jsonld-*.js              # Generated JSON-LD scripts
│   ├── jsonld-blog-*.js         # Blog Article schemas
│   ├── jsonld-nft-gallery-*.js  # Gallery schemas
│   └── gallery-data-*.js        # Gallery image data
├── nft-gallery/
│   ├── *.html                   # Individual gallery pages
│   └── js/
│       └── jsonld-*.js          # Gallery-specific JSON-LD
└── blog/
    └── *.html                   # Blog posts with Article schema
```

---

## Audit Results

### Before Automation (SEO_CSP_AUDIT_2025.md)
- ❌ JSON-LD: 2/20 root pages (10%)
- ❌ NFT Gallery: 0/106 pages had SEO
- ❌ Blog Posts: 0/46 had Article schema

### After Automation
- ✅ JSON-LD: 13/13 root pages (100%)
- ✅ NFT Gallery: 106/106 pages have ImageGallery schema (100%)
- ✅ Blog Posts: 46/46 have Article schema (100%)
- ✅ CSP Compliance: 100% (zero inline violations)

**SEO Grade Improvement:** B+ → A

---

## Troubleshooting

### Generator fails with "File not found"
**Solution:** Ensure you're in the root directory:
```bash
cd /home/typhoon/git/MarketWizardry.org
```

### "Already has JSON-LD" but page looks wrong
**Solution:** Delete the JSON-LD script reference from HTML and regenerate:
```bash
# Remove reference from HTML
sed -i '/<script src="\/js\/jsonld-/d' page.html

# Regenerate
python3 generate_root_pages_seo.py
```

### CSP violations after regeneration
**Solution:** Check for inline styles/scripts:
```bash
grep 'style=' page.html
grep '<script>' page.html | grep -v 'src='
```

All content should be in external files.

---

## Future Enhancements

**Potential additions:**
- [ ] Sitemap.xml generator
- [ ] Robots.txt updater
- [ ] Meta description optimizer
- [ ] Image alt text generator
- [ ] Breadcrumb schema validator
- [ ] Automated Google Search Console submission

---

## Related Documentation

- `SEO_CSP_AUDIT_2025.md` - Comprehensive SEO/CSP audit results
- `CLAUDE.md` - Project documentation
- `seo_templates.py` - SEO helper library documentation

---

## Maintainer

**TyphooN** (@MarketW1zardry)

**Last Updated:** 2025-10-06

**Version:** 1.0.0
