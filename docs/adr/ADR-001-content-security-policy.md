# ADR-001: Content Security Policy (CSP) - No Inline Styles or Scripts

**Status:** Accepted
**Date:** 2026-03-16
**Decision Makers:** TyphooN

## Context

Web application security requires protection against cross-site scripting (XSS) and code injection attacks. OWASP guidelines recommend strict Content Security Policy headers to mitigate these threats. MarketWizardry.org serves financial data and trading tools, making security a top priority. The site needed a CSP configuration that achieves maximum security scores without relying on `unsafe-inline` or `unsafe-eval` directives.

## Decision

Enforce a strict CSP via `.htaccess` that prohibits all inline styles, inline scripts, and inline event handlers. The policy is:

```
default-src 'self'; script-src 'self'; style-src 'self';
img-src 'self' data:; connect-src 'self'; font-src 'self';
object-src 'none'; media-src 'self';
frame-src 'self' https://*.youtube.com; worker-src 'none';
form-action 'self'; base-uri 'self'; manifest-src 'self';
frame-ancestors 'self'; upgrade-insecure-requests;
```

Additionally, HSTS (`Strict-Transport-Security: max-age=31536000; includeSubDomains`) is enforced to prevent SSL-stripping attacks.

All styles must reside in external CSS files under `/css/`. All scripts must reside in external JS files under `/js/`. Interactive elements use `data-action` attributes with event delegation instead of `onclick` or other inline event handlers.

## Consequences

**Benefits:**
- Achieves a 100/100 security score on CSP evaluators.
- Eliminates entire classes of XSS attacks by blocking inline code execution.
- Forces HTTPS via `upgrade-insecure-requests` and HSTS.
- `frame-ancestors 'self'` prevents clickjacking.
- YouTube embeds remain functional through the `frame-src` whitelist.

**Trade-offs:**
- More files to manage (every style change requires editing `shared-styles.css` or a page-specific CSS file, never the HTML directly).
- Requires discipline from all contributors to never introduce inline styles or scripts.
- JSON-LD structured data must be externalized or use `application/ld+json` script type (which CSP allows for non-executable types).
- Debugging can be harder since styles and behavior are separated from the markup they affect.
