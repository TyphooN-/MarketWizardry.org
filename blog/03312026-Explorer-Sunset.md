# Explorer Sunset: VaR, ATR, EV, and Crypto Explorers Retired

*All Explorers Have Been Absorbed Into TyphooN-Terminal*

**Published: 2026-03-31 | TyphooN | MarketWizardry.org**

---

## The Explorers Are Dead. Long Live the Terminal.

The MarketWizardry.org sidebar just got lighter. Four explorers have been removed from navigation:

- **VaR Explorer** — Value at Risk analysis across 895 Darwinex symbols
- **ATR Explorer** — Average True Range outlier detection
- **EV Explorer** — Enterprise Value screening
- **Crypto Explorer** — Crypto-specific metrics and analysis

These tools served their purpose as standalone web pages. That purpose is over. Everything they did — and more — now lives natively inside TyphooN-Terminal.

---

## Why Now?

TyphooN-Terminal v1.429 has 288 console commands, 39 indicators, and a full risk engine ported from the MQL5 EA. The explorers were built when the terminal didn't exist. They were Python scripts generating static HTML with CSV data that was already stale by the time you loaded the page.

The terminal renders the same data live. From the broker. On GPU. With charts.

| Explorer | Terminal Equivalent | Improvement |
|---|---|---|
| **VaR Explorer** | `VAR` command + VaR panel | Live VaR from position data, not static CSV |
| **ATR Explorer** | ATR indicator + `ATR` command | Real-time ATR on any timeframe, any symbol |
| **EV Explorer** | SEC Filing Scanner + Finnhub | Live fundamentals, not quarterly snapshots |
| **Crypto Explorer** | Crypto supply analysis + live data | CryptoCompare deep history, Kraken weekend fill |

Static HTML pages with day-old data cannot compete with a native GPU application pulling live feeds. The explorers were training wheels. The terminal is the bike.

---

## What's Still Accessible

The explorer pages still exist at their original URLs for anyone who bookmarked them. They just aren't in the sidebar anymore. The data is frozen — no further updates will be generated.

**Darwinex RADAR remains in the sidebar.** RADAR is low-maintenance and useful as-is. A replacement feature is in the works for TyphooN-Terminal.

**Blog stays.** Obviously.

---

## The Broader Pattern

MarketWizardry.org started as a collection of Python-generated analysis pages. Over time, each page's functionality was absorbed into TyphooN-Terminal:

1. **VaR analysis** → Terminal VaR engine (var.rs)
2. **ATR screening** → Terminal indicators (GPU compute shaders)
3. **Enterprise Value** → SEC Filing Scanner (engine/src/core/sec.rs)
4. **Crypto metrics** → CryptoCompare + Kraken data sources
5. **Risk calculator** → Terminal risk panel (risk.rs + margin.rs)
6. **Blog** → Still here. Terminal doesn't write blog posts. Yet.

The website is now what it should be: a blog, a calculator, DARWIN RADAR, and the VaR Cult manifesto. The analytical heavy lifting happens in 45,500 lines of Rust, not in static HTML.

---

## What This Means for the Terminal

Nothing changes for TyphooN-Terminal. The explorer functionality has been in the terminal for months. This is just cleaning up the website to reflect reality.

The terminal roadmap continues:
- 56 drawing tools + 10 harmonic patterns
- 29 floating windows
- Multi-window support (NEW_WINDOW/POPOUT)
- LAN sync between instances
- Full DARWIN analytics (80 engine functions)

The explorers were version 0. The terminal is version 1. There won't be a version 2 of the explorers.

---

## Update (2026-04-02): Calculator Tools Follow the Explorers

The cleanup continues. Three calculator tools have been removed from the [Calculator Suite](/calculator.html):

- **Stop Loss Calculator** — removed (broken: JS referenced non-existent HTML fields)
- **Portfolio VaR Calculator** — removed (required `window.varData` from frozen explorer data)
- **Symbol Lookup Tool** — removed (850-symbol database permanently stale)

All three depended on `calculator_complete_data.js`, a consolidated dataset generated from the same explorer CSVs that are no longer updated. A VaR calculator showing October 2025 data in April 2026 is worse than no calculator at all.

**What remains on the calculator page:**

| Calculator | Status | Why It Stays |
|---|---|---|
| **Position Size Calculator** | ✅ Active | Pure math — account size, risk %, entry, stop loss → position size. No data dependencies. |
| **Compound Interest Calculator** | ✅ Active | Standalone — principal, rate, time → growth projections. No market data needed. |

**Where the removed tools live now:**

| Removed Web Tool | TyphooN-Terminal Equivalent |
|---|---|
| Stop Loss Calculator | Risk panel with VaR-based and ATR-based SL across 4 order modes |
| Portfolio VaR Calculator | `VAR` command + DARWIN analytics (80 functions) + correlation matrix |
| Symbol Lookup Tool | `SEARCH` command + anomaly scanner (VaR+EV+ATR+SEC) + stock screener |

Same pattern as the explorers: static web tools with frozen data replaced by a native GPU application with live broker feeds. The website keeps what works standalone. Everything else is in the terminal.

-- TyphooN
