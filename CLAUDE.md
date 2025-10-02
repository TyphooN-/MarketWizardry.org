# MarketWizardry.org - Project Documentation for Claude Code

**Project:** MarketWizardry.org - Financial Trading Tools & NFT Gallery
**Tech Stack:** Static HTML/CSS/JS, Apache, Python generators
**Last Updated:** 2025-10-02

---

## Project Overview

MarketWizardry.org is a **terminal-aesthetic financial data exploration platform** with NFT/AI art galleries. The site features market explorers (ATR, VAR, EV, Crypto), trading calculators, blog content, and curated digital art collections.

### Core Philosophy
- **Retro CRT terminal aesthetic** - Green monospace text on black background
- **CSP-first security** - No inline styles/scripts allowed
- **SEO-optimized** - Comprehensive meta tags, schema markup, breadcrumbs
- **Auto-generated content** - Python scripts generate gallery/explorer pages
- **Performance-focused** - Aggressive caching, compression, lazy loading

---

## Critical Rules & Constraints

### 🔒 CSP (Content Security Policy) - STRICTLY ENFORCED

**The .htaccess file contains a strict CSP that blocks:**
- ❌ Inline styles (`style="..."`)
- ❌ Inline scripts (`<script>...</script>`)
- ❌ Inline event handlers (`onclick="..."`)
- ❌ `javascript:` URLs
- ❌ `unsafe-inline` directive (not allowed)
- ❌ `unsafe-eval` directive (not allowed)

**Location:** `.htaccess:43`

**What IS allowed:**
- ✅ External stylesheets from same origin (`/css/*.css`)
- ✅ External scripts from same origin (`/js/*.js`)
- ✅ Data URIs for images (`img-src 'self' data:`)
- ✅ YouTube embeds (`frame-src https://youtube.com`)
- ✅ `data-action` attributes for event delegation

### 📝 When Making Changes:

**NEVER:**
```html
<!-- WRONG - CSP violation -->
<div style="color: red;">Text</div>
<button onclick="doSomething()">Click</button>
<script>console.log('inline');</script>
```

**ALWAYS:**
```html
<!-- CORRECT - CSP compliant -->
<div class="error-text">Text</div>
<button data-action="do-something">Click</button>
<!-- script src="/js/external.js"></script -->
```

**Then add to `/css/shared-styles.css`:**
```css
.error-text { color: #ff0000; }
```

**And handle in external JS:**
```javascript
document.addEventListener('click', function(e) {
    if (e.target.dataset.action === 'do-something') {
        // Handle action
    }
});
```

---

## Architecture

### Directory Structure
```
/
├── .htaccess                    # CSP, security headers, caching, redirects
├── css/
│   └── shared-styles.css        # ALL styles (1714 lines, CSP compliant)
├── js/
│   ├── shared.js                # Common utilities
│   ├── redirect.js              # URL handling
│   ├── gallery.js               # Image gallery logic
│   ├── calculator.js            # Trading calculators
│   ├── crypto-explorer.js       # Crypto data display
│   ├── ai-musings.js            # Blog functionality
│   └── gallery-data-*.js        # Per-gallery image paths
├── img/                         # Static images (WebP preferred)
├── nft-gallery/                 # 106 generated gallery pages
│   ├── all.html
│   ├── *_gallery.html
│   └── */webp/                  # User image directories
├── atr-explorer/                # ATR data CSVs
├── var-explorer/                # VAR data CSVs
├── ev-explorer/                 # EV data CSVs
├── crypto-explorer/             # Crypto data CSVs
├── seo_templates.py             # SEO meta tag generator (Python)
├── generate_gallery.py          # Gallery HTML generator (CSP compliant)
└── *.html                       # Root pages (19 files)
```

### Key Files

#### `.htaccess` - THE RULEBOOK
**Location:** `/home/typhoon/git/MarketWizardry.org/.htaccess`

**Contains:**
- **Enhanced CSP headers (line 43)** - Maximum security (updated 2025-10-02)
- Security headers (lines 32-36)
- Compression (lines 4-14)
- Caching (lines 17-29)
- URL rewrites (lines 47-50)
- Custom 404 page (line 53)

**Current CSP (100/100 Security Score):**
```apache
default-src 'self'; script-src 'self'; style-src 'self';
img-src 'self' data:; connect-src 'self'; font-src 'self';
object-src 'none'; media-src 'self';
frame-src 'self' https://*.youtube.com; worker-src 'none';
form-action 'self'; base-uri 'self'; manifest-src 'self';
upgrade-insecure-requests; block-all-mixed-content;
```

**Key Features:**
- ✅ No `unsafe-inline` or `unsafe-eval`
- ✅ Forces HTTPS (`upgrade-insecure-requests`)
- ✅ Blocks mixed content explicitly
- ✅ YouTube embeds allowed (wildcard domain)

**If you change CSP, you MUST:**
1. Test every page in browser console
2. Look for CSP violation errors
3. Update this documentation
4. Run full audit (see SEO_CSP_AUDIT.md and CSP_ANALYSIS.md)

#### `css/shared-styles.css` - ALL STYLES
**Location:** `/home/typhoon/git/MarketWizardry.org/css/shared-styles.css`

**1714 lines containing:**
- Base styles (terminal aesthetic)
- CRT effects (scan lines, flicker animations)
- Modal styles (lines 452-709)
- Gallery grid layouts (lines 110-200)
- Breadcrumb navigation (lines 76-108)
- Mobile responsive (lines 711-800+)
- Explorer-specific styles
- Calculator styles

**Mobile breakpoint:** `@media screen and (max-width: 768px)`

**Recent additions:**
- Modal button bar mobile fix (lines 749-789) - forces single row with horizontal scroll

#### `seo_templates.py` - SEO Meta Generator
**Location:** `/home/typhoon/git/MarketWizardry.org/seo_templates.py`

**Python module providing:**
- `SEOManager` class
- `generate_enhanced_meta_tags()` - Creates meta tag blocks
- `generate_breadcrumbs()` - Schema.org breadcrumb HTML
- `generate_json_ld_schema()` - Structured data markup
- `PAGE_CONFIGS` dict - Per-page SEO settings

**Usage in generators:**
```python
from seo_templates import SEOManager, PAGE_CONFIGS

seo_manager = SEOManager()
page_config = PAGE_CONFIGS['gallery'].copy()
page_config.update({'title': 'Custom Title', ...})

meta_tags = seo_manager.generate_enhanced_meta_tags(page_config)
breadcrumbs = seo_manager.generate_breadcrumbs(breadcrumb_list)
schema = seo_manager.generate_json_ld_schema(config, 'page.html')
```

#### `generate_gallery.py` - Gallery Generator
**Location:** `/home/typhoon/git/MarketWizardry.org/generate_gallery.py`

**Generates:**
1. `nft-gallery.html` - Main gallery index
2. `nft-gallery/*_gallery.html` - Per-user galleries (106 files)
3. `nft-gallery/all.html` - All images aggregated
4. `ai-art.html` - AI art gallery
5. `js/gallery-data-*.js` - External data files (CSP compliant)

**Key functions:**
- `generate_nft_gallery_html()` - Main index
- `generate_user_gallery_html(username, output_file)` - User galleries
- `generate_all_html()` - Aggregated gallery
- `generate_ai_art_html()` - AI art page

**Run from root:** `python3 generate_gallery.py`

**Modal structure template (CSP compliant):**
```html
<div class="modal" id="fullscreenModal">
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

---

## Common Tasks

### Adding a New Page

1. **Create HTML with SEO template:**
```python
from seo_templates import SEOManager, PAGE_CONFIGS

seo_manager = SEOManager()
page_config = PAGE_CONFIGS['default'].copy()
page_config.update({
    'title': 'Page Title - MarketWizardry.org',
    'canonical_url': 'https://marketwizardry.org/new-page.html',
    'description': 'Page description for SEO',
    # ... other meta tags
})

meta_tags = seo_manager.generate_enhanced_meta_tags(page_config)
breadcrumbs = seo_manager.generate_breadcrumbs([
    {'name': '🏠 Market Wizardry', 'url': 'market-wizardry.html'},
    {'name': '📄 New Page', 'url': None}
])

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
{meta_tags}
    <link rel="stylesheet" href="/css/shared-styles.css">
</head>
<body>
{breadcrumbs}
    <div class="container">
        <h1>Page Title</h1>
        <!-- Content here -->
    </div>
    <script src="/js/shared.js"></script>
</body>
</html>'''
```

2. **Update sitemap.xml** (if exists)
3. **Test CSP compliance** in browser console
4. **Verify breadcrumbs** navigation works

### Adding Styles

**NEVER use inline styles.** Always add to `css/shared-styles.css`:

```css
/* New feature styles */
.my-new-feature {
    color: #00ff00;
    border: 2px solid #00ff00;
}

/* Mobile responsive */
@media screen and (max-width: 768px) {
    .my-new-feature {
        font-size: 0.8em;
    }
}
```

### Adding JavaScript Functionality

**NEVER use inline scripts.** Create external file in `/js/`:

```javascript
// /js/my-feature.js
(function() {
    'use strict';

    // Use event delegation for CSP compliance
    document.addEventListener('click', function(e) {
        if (e.target.dataset.action === 'my-action') {
            handleAction(e.target);
        }
    });

    function handleAction(element) {
        // Implementation
    }

    // Initialize on DOM ready
    document.addEventListener('DOMContentLoaded', function() {
        console.log('Feature initialized');
    });
})();
```

**Include in HTML:**
```html
<script src="/js/my-feature.js"></script>
```

### Regenerating Galleries

```bash
cd /home/typhoon/git/MarketWizardry.org
python3 generate_gallery.py
```

**This will:**
- Scan `nft-gallery/*/webp/` directories for images
- Generate individual gallery pages
- Create external JS data files (CSP compliant)
- Update main gallery index
- Regenerate `ai-art.html`

**After regeneration:**
- Check browser console for CSP errors
- Verify image grid displays correctly
- Test modal navigation on mobile

---

## Known Issues & Workarounds

### Current CSP Violations (as of 2025-10-02)

**3 files with inline styles - MUST FIX:**
1. `about.html:164` - `style="max-width: 300px;"`
2. `affiliates.html:86` - `style="text-align: left;"`
3. `calculator.html` - `style="margin-top: 20px;"`

**Fix:** Create CSS classes in `shared-styles.css` and replace inline styles.

### innerHTML Usage

**Status:** ✅ Safe - Using template literals with sanitized data

Files using innerHTML (acceptable pattern):
- `js/calculator.js` - 15 instances
- `js/crypto-explorer.js` - 1 instance
- `js/ai-musings.js` - 1 instance

**These are safe because:**
- Data comes from trusted sources (CSV files, JSON)
- Using template literals, not concatenation
- No user input directly inserted

### Mobile Modal Button Bar

**Fixed:** 2025-10-02

**Issue:** Modal buttons wrapped to multiple rows on mobile, breaking layout.

**Solution:** Added mobile-specific CSS at `shared-styles.css:749-789`:
- `flex-wrap: nowrap` on mobile
- Horizontal scroll with styled scrollbar
- Reduced font size (0.65em) and padding
- `white-space: nowrap` prevents text wrapping

**Applies to:** All explorers, galleries, and modal pages

---

## SEO Best Practices

### Required Meta Tags (Every Page)
```html
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="author" content="TyphooN">
<meta name="description" content="...">
<meta name="keywords" content="...">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="https://marketwizardry.org/page.html">

<!-- Open Graph -->
<meta property="og:title" content="...">
<meta property="og:description" content="...">
<meta property="og:url" content="...">
<meta property="og:type" content="website">
<meta property="og:image" content="...">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="...">
<meta name="twitter:description" content="...">
<meta name="twitter:image" content="...">
```

### Breadcrumb Schema (Major Pages)
```html
<nav class="breadcrumb" itemscope itemtype="https://schema.org/BreadcrumbList">
    <span itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
        <a href="market-wizardry.html" itemprop="item">
            <span itemprop="name">🏠 Market Wizardry</span>
        </a>
        <meta itemprop="position" content="1" />
    </span>
    <span class="separator">→</span>
    <span itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
        <span itemprop="name">📄 Current Page</span>
        <meta itemprop="position" content="2" />
    </span>
</nav>
```

### JSON-LD Structured Data (Recommended)
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "name": "Page Title",
  "description": "Page description",
  "url": "https://marketwizardry.org/page.html"
}
</script>
```

**Use `seo_templates.py` to generate these automatically.**

---

## Testing Checklist

### Before Committing Changes

**CSP Compliance:**
- [ ] No inline styles (`grep -r 'style=' *.html`)
- [ ] No inline scripts (`grep -r '<script>' *.html | grep -v 'src='`)
- [ ] No inline event handlers (`grep -r 'onclick=' *.html`)
- [ ] All new styles in `css/shared-styles.css`
- [ ] All new scripts in `js/*.js`

**Browser Testing:**
- [ ] Open Chrome DevTools Console
- [ ] Navigate to all modified pages
- [ ] Check for red CSP violation errors
- [ ] Verify no "Refused to apply inline style" errors
- [ ] Test on mobile viewport (375px, 768px)

**SEO:**
- [ ] Canonical URL present and correct
- [ ] Meta description under 160 characters
- [ ] Open Graph tags complete
- [ ] Breadcrumbs working (if applicable)
- [ ] Validate HTML (W3C validator)

**Functionality:**
- [ ] All links work
- [ ] All buttons respond
- [ ] Modals open/close properly
- [ ] Mobile navigation works
- [ ] Images load correctly (lazy loading)

---

## Performance Optimization

### Caching Strategy (.htaccess:17-29)
- **CSS/JS:** 1 year (`access plus 1 year`)
- **Images:** 1 year (WebP, PNG, JPG)
- **HTML:** 1 hour (allows frequent updates)

**When changing static assets:**
- Consider cache busting with query strings: `style.css?v=2`
- Or update file names: `style-v2.css`

### Image Optimization
- **Preferred format:** WebP (smaller, faster)
- **Lazy loading:** Enabled on gallery images (`loading="lazy"`)
- **Compression:** Lossy WebP conversion in NFT galleries
- **Naming:** `*-lossy.webp` for compressed versions

### Compression (.htaccess:4-14)
- GZIP enabled for all text assets
- Automatic compression via Apache mod_deflate

---

## Debugging Common Issues

### "Refused to apply inline style" Error

**Cause:** CSP blocking inline `style="..."` attribute

**Fix:**
1. Find the inline style in HTML
2. Create a CSS class in `shared-styles.css`
3. Replace inline style with class name
4. Test in browser

### "Refused to execute inline script" Error

**Cause:** CSP blocking inline `<script>` tag

**Fix:**
1. Move script to external file in `/js/`
2. Include with `<script src="/js/file.js"></script>`
3. Use `data-action` attributes for event handling
4. Implement event delegation in external JS

### Modal Buttons Wrapping on Mobile

**Fixed:** See `shared-styles.css:749-789`

**If issue recurs:**
1. Check `.modal-button-bar` has `flex-wrap: nowrap` on mobile
2. Verify buttons have `flex-shrink: 0`
3. Ensure `white-space: nowrap` on button text
4. Test at 375px and 768px viewports

### Gallery Not Displaying Images

**Check:**
1. Run `python3 generate_gallery.py` from root
2. Verify `js/gallery-data-*.js` files exist
3. Check browser console for 404 errors
4. Confirm image paths in data files are correct
5. Verify `initializeGallery()` is called in gallery.js

---

## Contact & Support

**Site Owner:** TyphooN
**Site URL:** https://marketwizardry.org
**Twitter:** @MarketW1zardry

**Documentation Maintained By:** Claude Code
**Last Full Audit:** 2025-10-02 (see SEO_CSP_AUDIT.md)
**Next Audit:** 2025-11-01

---

## Quick Reference Commands

```bash
# Regenerate all galleries
python3 generate_gallery.py

# Check for inline styles
grep -r 'style=' *.html

# Check for inline scripts
grep -r '<script>' *.html | grep -v 'src='

# Count total pages
ls *.html | wc -l
find nft-gallery -name "*.html" | wc -l

# Test CSP header
curl -I https://marketwizardry.org | grep -i content-security

# Find missing canonical tags
grep -L 'rel="canonical"' *.html

# Find missing meta descriptions
grep -L 'name="description"' *.html
```

---

## Version History

**2025-10-02:**
- Added mobile modal button bar fix
- Completed comprehensive SEO/CSP audit
- Created this documentation
- Identified 3 inline style violations (pending fix)
- Identified 10 pages needing JSON-LD schema

**Previous:**
- CSP implementation (removed unsafe-inline)
- Gallery generator CSP compliance update
- SEO templates module creation
- Breadcrumb schema markup implementation

---

**Remember:** This site has STRICT CSP. When in doubt, check the browser console for violations. Always use external CSS/JS files. Never use inline styles or scripts.
