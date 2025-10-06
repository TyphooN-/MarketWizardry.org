# Plotly Chart CSP Troubleshooting Guide

## Issue
Plotly-generated charts in explorer pages are not rendering properly.

## Current CSP Configuration

From `.htaccess` line 43:
```apache
Content-Security-Policy: default-src 'self';
  script-src 'self' https://cdn.plotly.com;
  style-src 'self';
  img-src 'self' data:;
  connect-src 'self';
  font-src 'self';
  object-src 'none';
  media-src 'self';
  frame-src 'self' https://*.youtube.com;
  worker-src 'none';
  form-action 'self';
  base-uri 'self';
  manifest-src 'self';
  upgrade-insecure-requests;
  block-all-mixed-content;
```

## How Charts Are Generated

### chart_generator.py Architecture

1. **Chart Creation** (`chart_generator.py` lines 87-194):
   - Generates Plotly figure
   - Converts to JSON (data, layout, config)
   - Escapes JSON for HTML attributes
   - Creates div with `data-plotly-*` attributes (CSP compliant)
   - Loads Plotly from CDN: `https://cdn.plotly.com/plotly-2.35.2.min.js`

2. **Chart Rendering** (`js/chart-navigation.js` lines 8-31):
   - Reads data from `data-plotly-*` attributes
   - Parses JSON
   - Calls `Plotly.newPlot()` to render

## Potential CSP Issues

### Problem 1: Plotly May Need unsafe-eval
**Why:** Plotly might use `eval()` or `new Function()` internally for rendering

**Solution Options:**
1. ❌ Add `'unsafe-eval'` to script-src (reduces security)
2. ✅ Use Plotly's `plotly-strict.min.js` build (no eval)
3. ✅ Generate static images instead of interactive charts

### Problem 2: Plotly May Generate Inline Styles
**Why:** Plotly creates SVG elements with inline style attributes

**Current CSP:** `style-src 'self'` - blocks inline styles

**Solution Options:**
1. ❌ Add `'unsafe-inline'` to style-src (BAD - breaks security model)
2. ✅ Add `'unsafe-hashes'` for specific hash values
3. ✅ Generate CSS classes for all Plotly styles (complex)

### Problem 3: Blob URLs for WebGL
**Why:** Plotly WebGL mode uses blob: URLs for workers

**Current CSP:** `worker-src 'none'` - blocks web workers

**Solution:** Add `blob:` to worker-src if using WebGL mode

## Diagnostic Steps

### Step 1: Check Browser Console
Open Chrome DevTools Console on any chart page:

```javascript
// Check if Plotly is loaded
console.log(typeof Plotly);  // Should be "object"

// Check for CSP violations
// Look for errors like:
// "Refused to execute inline script..."
// "Refused to apply inline style..."
// "Refused to evaluate a string as JavaScript..."
```

### Step 2: Test Minimal Example

Create `test-chart.html` in root:

```html
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.plotly.com/plotly-2.35.2.min.js"></script>
</head>
<body>
    <div id="chart"></div>
    <script>
        const data = [{
            x: [1, 2, 3],
            y: [2, 4, 6],
            type: 'scatter'
        }];
        const layout = {title: 'Test Chart'};
        Plotly.newPlot('chart', data, layout);
    </script>
</body>
</html>
```

Visit: `https://marketwizardry.org/test-chart.html`

**Expected Issues:**
1. Inline script will be blocked by CSP
2. May see Plotly-generated inline styles blocked

### Step 3: Check Specific CSP Violations

```bash
# On server, check Apache error logs
tail -f /var/log/apache2/error.log | grep CSP

# Or check access logs for CSP reports
tail -f /var/log/apache2/access.log | grep csp-report
```

## Recommended Solutions

### Solution 1: Use plotly-strict.min.js (No eval)

**Change in chart_generator.py line 129:**
```python
# OLD
<script src="https://cdn.plotly.com/plotly-2.35.2.min.js" charset="utf-8"></script>

# NEW
<script src="https://cdn.plotly.com/plotly-strict-2.35.2.min.js" charset="utf-8"></script>
```

This version doesn't use `eval()`.

### Solution 2: Allow Specific Hashes for Inline Styles

If Plotly generates consistent inline styles, we can whitelist their hashes:

```apache
# In .htaccess
style-src 'self' 'sha256-<hash1>' 'sha256-<hash2>';
```

**To generate hashes:**
1. Open chart page with CSP violations
2. Console shows: "Refused to apply inline style because... 'sha256-xyz123...'"
3. Copy the hash value
4. Add to CSP

**Cons:** Brittle - hashes change with Plotly updates

### Solution 3: Relaxed CSP for Chart Pages Only

Create separate `.htaccess` in chart directories:

```apache
# var-explorer/.htaccess
# Override main CSP for chart pages only
<FilesMatch "\.html$">
    Header always set Content-Security-Policy "default-src 'self'; script-src 'self' https://cdn.plotly.com; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; font-src 'self';"
</FilesMatch>
```

**Pros:** Charts work without breaking main site security

**Cons:** Allows inline styles on chart pages (minor security reduction)

### Solution 4: Generate Static Images Instead

Use Plotly's static image export:

```python
# In chart_generator.py
import plotly.io as pio

# Generate static PNG/SVG instead of interactive HTML
pio.write_image(fig, 'chart.png', width=1400, height=800)
```

**Pros:**
- No CSP issues
- Faster load times
- Works on all devices

**Cons:**
- No interactivity (zoom, pan, hover)
- Larger file sizes for complex charts

### Solution 5: Pre-render Charts as JSON + External Renderer

Keep current approach but enhance error handling:

```javascript
// In js/chart-navigation.js
function renderChart() {
    const chartDiv = document.getElementById('chart');
    if (!chartDiv) return;

    const data = chartDiv.getAttribute('data-plotly-data');
    const layout = chartDiv.getAttribute('data-plotly-layout');
    const config = chartDiv.getAttribute('data-plotly-config');

    if (!data || !layout || !config) {
        chartDiv.innerHTML = '<p style="color: red;">Error: Missing chart data</p>';
        return;
    }

    if (typeof Plotly === 'undefined') {
        chartDiv.innerHTML = '<p style="color: red;">Error: Plotly library not loaded. Check CSP settings.</p>';
        return;
    }

    try {
        const parsedData = JSON.parse(data);
        const parsedLayout = JSON.parse(layout);
        const parsedConfig = JSON.parse(config);

        // Configure Plotly to avoid CSP violations
        parsedConfig.setBackground = 'transparent';  // Avoid inline background styles

        Plotly.newPlot('chart', parsedData, parsedLayout, parsedConfig);
    } catch (e) {
        console.error('Error rendering Plotly chart:', e);
        chartDiv.innerHTML = `<p style="color: red;">Error rendering chart: ${e.message}</p>`;
    }
}
```

## Immediate Fix (RECOMMENDED)

### Option A: Test with Relaxed CSP First

1. **Backup current .htaccess**
2. **Temporarily relax CSP for testing:**

```apache
# .htaccess line 43
Header always set Content-Security-Policy "default-src 'self'; script-src 'self' https://cdn.plotly.com 'unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; font-src 'self'; object-src 'none'; media-src 'self'; frame-src 'self' https://*.youtube.com; worker-src 'none'; form-action 'self'; base-uri 'self'; manifest-src 'self'; upgrade-insecure-requests; block-all-mixed-content;"
```

3. **Test charts - do they work now?**
4. **If yes:** Narrow down which directive is needed ('unsafe-eval' vs 'unsafe-inline')
5. **If no:** Issue is not CSP-related

### Option B: Chart-Specific .htaccess (Recommended)

Create `/home/typhoon/git/MarketWizardry.org/var-explorer/.htaccess`:

```apache
# Override CSP for chart HTML files only
<FilesMatch "chart.*\.html$">
    Header always set Content-Security-Policy "default-src 'self'; script-src 'self' https://cdn.plotly.com; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; font-src 'self'; object-src 'none'; media-src 'self'; frame-src 'self'; worker-src 'none'; form-action 'self'; base-uri 'self'; manifest-src 'self'; upgrade-insecure-requests; block-all-mixed-content;"
</FilesMatch>
```

Repeat for `atr-explorer/` and `ev-explorer/` directories.

## Testing Checklist

- [ ] Check browser console for CSP violations
- [ ] Verify Plotly CDN loads (check Network tab)
- [ ] Verify `Plotly` object exists in console
- [ ] Check if chart div gets `data-plotly-*` attributes
- [ ] Test with relaxed CSP to isolate issue
- [ ] Implement chart-specific .htaccess if needed
- [ ] Update chart_generator.py to use plotly-strict if eval is the issue
- [ ] Document final solution in this file

## Additional Resources

- Plotly CSP Documentation: https://plotly.com/javascript/configuration-options/
- CSP Reference: https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP
- Plotly Strict Build: https://github.com/plotly/plotly.js/blob/master/dist/README.md

---

**Last Updated:** 2025-10-06
**Status:** Investigation in progress
