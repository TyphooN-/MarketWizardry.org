# ADR-003: Terminal CRT Aesthetic as Design Language

**Status:** Accepted
**Date:** 2026-03-16
**Decision Makers:** TyphooN

## Context

MarketWizardry.org needed a distinctive visual identity that reflects its focus on financial data exploration and trading tools. The design language needed to be memorable, consistent across all pages (galleries, explorers, calculators, blog), and feasible to maintain with a strict CSP that prohibits inline styles.

## Decision

Adopt a retro terminal CRT aesthetic as the unified design language across the entire site. This includes:

- Green monospace text (`#00ff00`) on a black background as the primary color scheme.
- CRT scan line overlay animations and subtle flicker effects defined in `css/shared-styles.css`.
- Monospace font families throughout all content and UI elements.
- Terminal-inspired UI components: bordered containers, blinking cursors, command-line style navigation.

All CRT effects (scan lines, flicker, glow) are implemented as CSS animations in the shared stylesheet, ensuring CSP compliance.

## Consequences

**Benefits:**
- Strong, immediately recognizable brand identity that differentiates the site from conventional financial platforms.
- Consistent visual language that works across all content types (data tables, image galleries, blog posts, calculators).
- The constrained palette simplifies design decisions and keeps the stylesheet manageable.
- CRT effects are purely decorative CSS animations, so they degrade gracefully on older browsers.

**Trade-offs:**
- Design choices are constrained to what fits the terminal aesthetic (limited color palette, monospace fonts only, minimal use of images for UI).
- Accessibility considerations: green-on-black may need contrast adjustments for some users; CRT flicker effects should respect `prefers-reduced-motion`.
- The aesthetic may not appeal to users expecting a modern, polished financial dashboard look.
- Adding new visual elements requires careful integration to avoid breaking the established theme.
