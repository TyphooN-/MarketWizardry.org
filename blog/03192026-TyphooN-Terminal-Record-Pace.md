## TyphooN-Terminal: 56K Lines of Rust in 6 Days -- Building a Bloomberg Killer on Open Source

> **DISCLAIMER:** This is a technical post-mortem of a software development sprint. The author is not affiliated with Bloomberg, Godel Technologies, MetaQuotes, or any terminal vendor mentioned. Opinions on proprietary trading software are exactly that -- opinions formed after years of paying for tools that should have been open source from the start.

## Introduction: What If You Could Replace a $24K/Year Terminal in 5 Days?

Bloomberg Terminal costs **$24,000** per year. Godel Terminal costs **$80-118** per month. MetaTrader 5 is "free" in the same way that a roach motel is free -- you walk in, your data never walks out, and MetaQuotes owns the building.

TyphooN-Terminal shipped its first functional build in **4.7 days**. March 15 to March 20, 2026. **431 commits**. **73,100+ lines of code**. Approximately **43 commits per day**. A ~**12-15MB GUI binary** and a **6.5MB standalone CLI** that do what Bloomberg charges twenty-four grand a year for.

This is not a mockup. This is not a demo. This is a fully functional trading terminal with **298** Bloomberg-style commands, **39** indicators with exact MT5 visual parity, a complete port of the TyphooN v1.420 risk management engine, direct MT5 SQLite bar sync across multiple Darwinex accounts, and enough research tools to make a sell-side analyst uncomfortable.

**BSL (Business Source License). Open source.** Because proprietary trading terminals are a racket and somebody needed to say it out loud by shipping the alternative.

## The Backstory: Why Build a Terminal at All?

I run six manual high-tilt DARWINs on Darwinex. Six strategies, all discretionary, all managed through a risk management EA (**TyphooN v1.420**) that handles TRIM, PROTECT, hedged martingale position management, and Monte Carlo simulation. The EA has been the equalizer for years -- it does the math so the operator does not have to think about position sizing at 3 AM during a crypto spread spike.

**QRRP** -- the Quad Rothschild Rug Pull, my cascading martingale SOL short strategy -- was the first step beyond pure discretionary trading into algo-assisted territory. The EA manages the position autonomously. TRIM builds net short exposure. PROTECT handles spread events. The operator's job is to not touch anything and let the flywheel compound.

But QRRP exposed the ceiling. MetaTrader 5 is a proprietary black box. MQL5 is a walled garden. You cannot run MT5 on Linux natively. You cannot integrate with Alpaca Markets. You cannot pull SEC EDGAR fundamentals, options chains with Greeks, congressional trading data, or dark pool volume into the same interface where you manage positions. MT5 does what MetaQuotes allows and nothing more.

The terminal I needed did not exist. Bloomberg has the data but costs more than most retail accounts. Godel has the interface but charges monthly for what should be a local binary. Every open-source alternative is either Electron bloatware burning **500MB** of RAM to render a candlestick chart, or a Python script with a Tkinter GUI that looks like it escaped from 2004.

So I built it.

## The Tech Stack: Why Rust and Tauri, Not Electron or Qt

This decision took about ten minutes and the reasoning has not changed since.

### Rust + Tauri 2.0 Backend

- **Binary size:** ~10-15MB. An equivalent Electron app ships at 150-200MB because it bundles an entire Chromium browser.
- **Memory footprint:** ~50-100MB under load. Electron apps routinely consume 200-500MB doing the same work because V8's garbage collector treats RAM like a buffet.
- **No garbage collector.** No runtime. Rust compiles to native machine code that runs at the speed your CPU was designed for, not the speed a JIT compiler feels like generating today.
- Tauri 2.0 uses the system webview (WebKitGTK on Linux, WebView2 on Windows, WKWebView on macOS). Zero bundled browser engines. Your OS already has a renderer -- Tauri uses it.

### JS/HTML/CSS Frontend

- The rendering layer is vanilla JS with **WebGL2** GPU-accelerated charts. No React. No Vue. No framework that adds 400KB of abstraction between your code and the DOM.
- WebGL2 means chart rendering happens on the GPU. Candlesticks, indicators, drawing tools -- all GPU-rendered. Your CPU handles data. Your GPU handles pixels. Division of labor that Electron apps do not understand.

### WASM Indicator Modules

- Performance-critical indicator calculations compile to **WebAssembly**. The same Rust code that runs on the backend can compile to Wasm and execute in the frontend at near-native speed.
- This is not "fast for a web app." This is fast, period.

### The Alternatives and Why They Lost

**Electron:** Ships a 200MB Chromium instance per application. Uses 500MB of RAM to display a chart. This is not engineering. This is negligence.

**Python/Qt:** Python's GIL makes real-time charting a threading nightmare. Qt licensing is a minefield. PyQt5 commercial licenses cost money. PySide6 is LGPL with restrictions. Neither produces binaries under 50MB.

**C++/Qt:** Fast, but C++ memory management in a trading terminal is asking for use-after-free bugs in production where use-after-free means "your order got duplicated and you are now 2x leveraged by accident."

Rust eliminates entire categories of bugs at compile time. Memory safety without garbage collection. Thread safety without runtime overhead. When the code compiles, it works. When it works, it works at native speed. For a trading terminal where correctness is not optional, this is the only sane choice.

## What Was Built: The Numbers

In **6 days**, TyphooN-Terminal shipped with:

### 298 Bloomberg-Style Commands (Ctrl+K Palette)

Every function accessible via keyboard. Type what you want, hit enter. No menu diving. No mouse hunting. Bloomberg proved this UX pattern works for professional traders thirty years ago. Everyone else ignored it.

### 39 Indicators with Exact MT5 Visual Parity

- MultiKAMA, Ehlers Fisher Transform, BetterVolume, Supply/Demand zones, and 35 more.
- "Exact visual parity" means the indicator output matches MT5 pixel-for-pixel. Same colors. Same line weights. Same calculation methodology. If you are migrating from MT5, your charts look identical on day one. 22 of the 39 indicators are compiled to WebAssembly for near-native performance; the rest run in JavaScript with automatic fallback.

### 44 GPU-Rendered Drawing Tools

- Fibonacci retracements, extensions, channels, arcs, and time zones
- Andrew's Pitchfork, Schiff variants
- Elliott Wave markup
- Gann fans and squares
- Linear regression channels
- All rendered on the GPU. Drawing tools on most platforms are canvas-based CPU operations that stutter when you have 15 Fibonacci levels and 30 indicators on a 4K display. GPU rendering does not stutter.

### 7 Order Types with Draggable SL/TP

- Market, limit, stop, stop-limit, trailing stop, bracket, OCO
- Stop-loss and take-profit lines are draggable on the chart. Grab the line, move it, the order updates. This is how order management should have always worked.

### Full Research Suite

- SEC EDGAR fundamentals integration
- Options chains with full Greeks calculation
- Insider trading activity tracking
- Congressional trading disclosure monitoring (because apparently lawmakers trade on information the rest of us do not have, and that data is public if you know where to look)
- Dark pool volume aggregation
- Economic calendar
- Yield curve visualization
- Fear and Greed index
- World indices dashboard
- Forex cross-rate matrix
- Crypto top 50 with real-time data

That is not a terminal. That is a Bloomberg terminal without the **$24K** annual subscription and the proprietary lock-in.

## The Risk Engine Port: MQL5 to Rust

This is the part that matters most for actual trading.

**TyphooN v1.420** has been managing risk on MetaTrader 5 for years. The forward-looking TRIM formula, the PROTECT system, the hedged martingale position management, Monte Carlo simulation -- all of it written in MQL5, all of it trapped inside MetaQuotes' ecosystem.

The port to Rust preserves every feature:

**4 Order Modes:**
The same four modes from the MQL5 EA, mapped to Alpaca Markets order types. Risk percentage calculations, ATR-based stop placement, and position sizing all work identically.

**Hedged Martingale with TRIM/PROTECT:**
- The TRIM formula: `maxSafe = floor((equity / threshold - margin) / marginPerLot)`
- Forward-looking. Proactive. Calculates safe lot capacity before problems occur, not after.
- PROTECT fires balanced closes on spread spikes, maintaining net bias while reducing gross exposure.
- The entire QRRP cascade logic works in Rust exactly as it works in MQL5.

**Monte Carlo Simulation:**
- Run thousands of simulated paths against your current position to estimate drawdown probability, ruin probability, and expected terminal equity.
- In MQL5 this took seconds. In Rust it takes milliseconds. Compiled native code with zero-cost abstractions does that.

The risk engine port is the bridge from Darwinex to Alpaca Markets. Same math. Same logic. Different broker. No more MetaQuotes dependency. No more Windows-only constraint. No more praying that Wine handles MT5 correctly on Linux.

## The Speed: 258 Commits in 6 Days

Let me contextualize what **43 commits per day** means.

A typical professional software team ships maybe **2-5** meaningful commits per developer per day. Senior engineers at FAANG companies might push **3-8**. A focused solo developer on a deadline might hit **10-15**.

Forty-six per day is not normal. It is the result of three factors:

1. **Architectural Clarity from Day One:** 33 Architecture Decision Records were written before and during development. Every major decision -- state management, IPC protocol, chart rendering pipeline, indicator calculation strategy -- was documented and decided before code was written. When you know where everything goes, you do not waste time refactoring.

2. **Rust's Compiler Is the QA Team:** When Rust code compiles, entire categories of bugs are already eliminated. No null pointer dereferences. No data races. No use-after-free. No buffer overflows. The time other languages spend debugging memory corruption, Rust spends at compile time. The result is that committed code actually works.

3. **Years of Domain Knowledge:** The risk management logic, the indicator math, the order management patterns -- none of this was invented during the sprint. It was ported. Porting known-correct logic to a better language is fundamentally faster than designing from scratch. The MQL5 EA has been battle-tested across six DARWINs and seven post-mortems. The math was proven. It just needed a better home.

**431 commits** is not a vanity metric. Every commit represents a testable, working increment. The repository went from zero to functional trading terminal in six days because the architecture was right, the language was right, and the domain knowledge was already paid for in years of live trading.

## Security: 21-Pass Audit, 97 Findings, 91 Fixed

A trading terminal handles API keys, account credentials, and order execution. Security is not a feature. It is a prerequisite.

TyphooN-Terminal underwent a **21-pass** security audit before release:

- **97** total findings identified
- **91** fixed and verified
- **6** accepted as low-risk with documented mitigations

**Key Security Measures:**
- **AES-256-GCM** encryption for all stored credentials and API keys
- Zero `innerHTML` usage anywhere in the frontend (innerHTML is the number one vector for XSS attacks in desktop web apps -- eliminating it entirely removes the attack surface)
- Content Security Policy headers enforced
- IPC command validation on every Tauri bridge call
- No `eval()`. No `Function()`. No dynamic code execution.
- Credential storage uses OS-native keychains where available

When your terminal can execute market orders, "we'll add security later" is not an acceptable engineering position. The audit happened during development, not after.

## What This Replaces and What It Costs

### The Comparison

**Bloomberg Terminal:**
- **Cost:** $24,000/year
- **Strengths:** Unmatched data depth, institutional credibility
- **Weaknesses:** Proprietary lock-in, obscene pricing, requires dedicated hardware

**Godel Terminal:**
- **Cost:** $80-118/month ($960-1,416/year)
- **Strengths:** Modern UI, good charting
- **Weaknesses:** Subscription model, closed source, no risk engine

**MetaTrader 5:**
- **Cost:** "Free" (your data is the product)
- **Strengths:** Mature platform, large indicator ecosystem
- **Weaknesses:** Windows-only native, proprietary MQL5, no fundamental data, MetaQuotes controls everything

**TyphooN-Terminal:**
- **Cost:** $0 (BSL)
- **Binary:** ~10-15MB
- **Memory:** ~50-100MB
- **Runs on:** Linux, Windows, macOS
- **Risk engine:** Full TyphooN v1.420 port
- **Research:** SEC EDGAR, options, insider, congress, dark pool, economic calendar
- **Source:** Open. Read it. Fork it. Improve it.

The value proposition is not complicated. The same functionality that costs **$24K/year** from Bloomberg or **$80/month** from Godel ships as a **12MB** open-source binary that runs on your existing hardware using **50MB** of RAM.

## What Is Next: The Road to Full Automation

TyphooN-Terminal is not the destination. It is the platform.

The six manual DARWINs on Darwinex taught position management. QRRP taught cascading automation. The v1.420 EA proved that algorithmic risk management outperforms human discretion every single time (seven post-mortems confirm this empirically).

The roadmap:

**Multi-Broker Support:** Alpaca Markets is live. **tastytrade** is the second broker -- login UI with username/password/sandbox mode sits alongside Alpaca in the Connect to Broker window. Interactive Brokers, Tradier, and additional brokers follow. Same risk engine, same interface, different execution venues.

**Fully Automated Algorithm:** The risk management EA handles position sizing, TRIM, PROTECT, and martingale management. The next step is automated signal generation -- entries, exits, and strategy selection without human discretion. The terminal provides the execution layer. The algorithm provides the decisions.

**Strategy Backtesting:** Monte Carlo simulation is already built. Historical backtesting with the same indicators and risk engine follows. Test strategies against the same math that will execute them live.

**Plugin Architecture:** Custom indicators, custom strategies, custom data sources -- all loadable as Wasm modules. Write once in Rust, compile to Wasm, load into the terminal. No MQL5 marketplace gatekeeping.

The progression is clear: manual trading taught the fundamentals, the risk EA automated position management, TyphooN-Terminal ports that automation to open infrastructure, and the fully automated algorithm completes the pipeline. Every step removes one more human failure mode from the process.

## CLI / TUI: 6.5MB Trading Terminal Over SSH

The GUI requires a display server. Algorithmic trading on a VPS doesn't have one. So TyphooN-Terminal now ships a **standalone CLI binary** — a full TUI (Text User Interface) built with `ratatui` + `crossterm` in pure Rust. **6.5MB.** No WebKitGTK. No Node.js. No Wasm. No display server. Works over SSH on any VPS, any terminal emulator, any platform with ANSI escape codes.

**Full trading parity with the GUI:**

| Feature | GUI | CLI |
|---|---|---|
| Account info | Yes | Yes |
| Positions (interactive) | Yes | Yes |
| Orders (interactive) | Yes | Yes |
| Market/Limit/Stop/Bracket orders | Yes | Yes |
| Close/Partial close | Yes | Yes |
| Close all / Cancel all | Yes | Yes |
| Order history | Yes | Yes |
| Watchlist + live quotes | Yes | Yes |
| Market clock | Yes | Yes |
| Risk dashboard (VaR, margin) | Yes | Yes |
| ASCII candlestick chart | N/A | **Yes** |
| Custom timeframes (H2-MN1) | Yes | Yes |
| MT5 CSV import | Yes | Yes |
| Multi-account aggregate | Yes | Yes |

**Trading from the command line:**

```
:buy SMCI 100              # Market buy
:sell SLV 50               # Market sell
:limit buy AAPL 10 150.00  # Limit order
:stop sell SMCI 100 25.00  # Stop order
:bracket buy CC 500 15.00 25.00  # Bracket (OCO)
:close CC                  # Close position
:closeall                  # Close everything
:chart BTC/USD H4          # ASCII candlestick chart
:import DARWIN_EUR /path.csv  # Import MT5 statement
```

The CLI shares **encrypted credentials** with the GUI (AES-256-GCM SQLite). Set up API keys once in the GUI, trade from SSH forever. No re-entry. No plaintext config files. Same encryption, same salt, same security model.

**Why this matters:** A **6.5MB binary** that can execute trades, manage positions, display live quotes, render ASCII charts, and import MT5 history — over SSH, on a $5/month VPS, with no GUI dependencies. This is the headless trading terminal that NinjaTrader ($1,099), Sierra Chart ($54/month), and every other Windows-only desktop terminal cannot offer. The algo doesn't need a monitor. It needs an SSH connection and a thesis.

**The QRRP cascade doesn't need seven monitors and a Tauri window.** It needs TRIM 54.2%, a SOL price feed, and a terminal that can execute. The CLI is that terminal. 6.5MB. Runs anywhere. Trades everything Alpaca offers.

## Performance Optimization Deep Dive

Raw feature count means nothing if the terminal stutters under load. TyphooN-Terminal went through aggressive performance optimization passes that eliminated every bottleneck I could find.

**SQLite Statement Caching:** Every prepared statement is cached after first compilation. Repeated queries -- position lookups, indicator data reads, watchlist refreshes -- hit the statement cache instead of re-parsing SQL. This alone cut database interaction latency by 40-60% on hot paths.

**HTTP Connection Pooling:** Alpaca's API, SEC EDGAR, options data, crypto feeds -- the terminal talks to 21 data sources. Without connection pooling, every request opens a new TCP connection and negotiates a new TLS handshake. With pooling, persistent connections are reused across requests. Latency on sequential API calls dropped from ~200ms to ~30ms per request after the initial handshake.

**DOM Delta Updates:** The frontend never re-renders an entire panel. When a position's P&L changes, only that cell updates. When a quote ticks, only the price element mutates. Full panel re-renders are reserved for structural changes (adding/removing columns, switching views). This is the difference between a UI that feels instant and one that feels like it is "loading."

**Atomic Panel Swap:** Switching between dashboard views (positions, orders, watchlist, research) happens in a single DOM operation. The new panel is constructed off-screen, then swapped in atomically. No flash of empty content. No partial renders. The transition is imperceptible.

**Dashboard Overlap Prevention:** Multiple dashboard panels competing for the same viewport is a classic UI race condition. TyphooN-Terminal enforces a strict panel ownership model -- exactly one panel owns each viewport region at any time. Panel transitions are serialized. No z-index fights. No invisible panels consuming events underneath visible ones.

**Indicator Error Isolation:** A bad indicator calculation (division by zero, NaN propagation, insufficient data) does not crash the chart or poison other indicators. Each indicator runs in an isolated calculation context. If Fisher Transform produces NaN on bar 3 because there are not enough data points yet, the chart renders everything else normally and the indicator picks up cleanly once sufficient data exists.

## Bar Data Chunking Strategy

Fetching historical bar data from Alpaca is the single most time-consuming operation in the terminal. Alpaca's API returns paginated results, rate-limits aggressively, and crypto endpoints have different constraints than equities. The chunking strategy solves all of this.

**Adaptive page_token Pagination:** Alpaca returns a `next_page_token` with each response. The chunker follows these tokens automatically, accumulating bars across pages until the requested range is filled. No fixed page sizes -- the system adapts to whatever Alpaca returns per page.

**Stale Chunk Detection:** Before fetching from the network, the chunker checks if cached data covers the requested range. If the newest cached bar is within one bar-period of the current time, no fetch is needed. If the cache is partially stale, only the gap is fetched and spliced into existing data.

**429 Cooldown with Partial Data Return:** When Alpaca returns HTTP 429 (rate limited), the chunker does not throw an error and lose everything. It returns whatever bars were successfully fetched so far, marks the range as partially filled, and schedules a cooldown retry. The chart renders immediately with partial data rather than showing a loading spinner for minutes.

**Progressive Throttle Detection:** If any API response takes longer than 10 seconds, the chunker increases the interval between subsequent requests. This prevents cascading slowdowns when Alpaca's servers are under load. The system backs off gracefully instead of hammering a slow endpoint.

**Crypto Lookback Caps:** Crypto symbols cap lookback at 90 days for intraday timeframes and 180 days for daily+. Unlike equities with decades of history, crypto bar data on Alpaca has practical limits. Requesting 10 years of 1-minute BTC bars is not useful and would take hours. The caps enforce sanity.

**Early Termination:** If a fetch has been running for more than 60 seconds and has already accumulated more than 100 bars, it terminates and returns what it has. The user sees data now rather than waiting for a theoretically complete dataset that may never arrive due to API constraints.

**Synthetic MN1 from Weekly:** Monthly bars are not available from Alpaca's API. The chunker fetches weekly bars and synthesizes monthly candles by aggregating weeks into calendar months. Open from the first week, close from the last week, high/low from the extremes. This gives the terminal MN1 charts that Alpaca does not natively support.

**The result:** Cold load for a full multi-timeframe grid went from **2.5+ hours** to **30 seconds**. A complete MTF grid across all timeframes loads in **3-5 minutes** instead of **3-4 hours**. The chunking strategy turned bar data loading from the terminal's biggest pain point into a solved problem.

## Incremental Fetch and Live Bar Construction

The chunking strategy handles cold loads. But what about returning users who already have cached data? And what about live candle updates?

**Incremental Cache-Aware Fetch:** On every bar request, the backend checks SQLite for existing cached bars. If data exists, it reads the **second-to-last** bar's timestamp (not the last — the last candle is still forming and needs a fresh API read) and fetches only the gap. A session that previously loaded 2,175 BTC/USD 1-Hour bars now fetches **1-2 chunks** instead of 13. That is an **80-95% reduction** in API calls on warm start.

**Cache Freshness Gate:** Before making any API call, `get_cache_age_secs()` checks when the cache was last updated. If the cache is fresher than the bar's timeframe period (e.g., less than 3,600 seconds old for a 1-Hour chart), cached data is returned immediately with zero network calls. This eliminated a bug where the SLV daily chart was re-fetching every 60 seconds with no new data.

**WebSocket Bar Builder:** A new `BarBuilder` module constructs 1-minute OHLCV bars from the live WebSocket trade stream. Trades arrive in real-time via WebSocket. The builder accumulates them into partial bars (tracking open, high, low, close, volume). When the minute rolls over, the bar is "completed" and pushed to the frontend. The frontend polls every 2 seconds, appends completed bars to the chart, and updates the live candle. **Real-time candle updates without a single API call.** Falls back to 10-second API polling when the WebSocket is down.

**Connection Pre-Warming:** `warm_data_connection()` fires a HEAD request to the data API endpoint during the broker connect flow. Since account authentication warms a different endpoint than bar data, this pre-establishes TCP+TLS for the data host ~200ms before the first bar fetch needs it. Shaves the cold-connect latency.

**Fast Compression for Merges:** When merging new bars into existing cache, the system now uses zstd level 3 instead of level 9. Level 3 is **3x faster** with only ~15% larger output. Archival storage (initial writes) still uses level 9 for maximum compression. This reduces CPU overhead on the hot merge path — the one that runs on every incremental update.

**Cache Trim:** `merge_bars()` accepts a `max_bars` limit. After merging and deduplicating, excess bars (oldest first) are trimmed to prevent unbounded SQLite growth. A 2,000-bar prefetch stays at 2,000 bars even after weeks of incremental merges.

**Double-Write Elimination:** The frontend no longer writes to SQLite after receiving data from the backend — the backend already persists during the merge operation. Only the hot in-memory cache is updated in JavaScript. This eliminated duplicate zstd level-9 recompression on every bar fetch.

**Measured result across 3 benchmark runs:**

| Scenario | Before | After | Speedup |
|---|---|---|---|
| BTC/USD 1Hour cold | 2.5+ hours | 33-131s | 70-270x |
| SOL/USD 4Hour cold | 2+ hours | 47-163s | 45-150x |
| Full MTF grid + prefetch | 3-4 hours | ~3 min | 60-80x |
| Warm start (cached) | 30s | **instant** | infinite |

## Four-Tier Cache Architecture

Every piece of market data flows through a four-tier cache before hitting the network. Each tier trades latency for capacity.

**Tier 1 -- Memory LRU (~0ms):** The fastest cache. Recently accessed bar data, quotes, and indicator results live in an in-memory LRU (Least Recently Used) cache. Cache hits are effectively instant. The LRU eviction policy ensures frequently accessed symbols stay hot while rarely viewed symbols get pushed to lower tiers.

**Tier 2 -- IndexedDB (~5-10ms):** Browser-native key-value storage. Larger than the memory LRU and survives page refreshes. Bar data for the current session's symbols lives here. Access time is 5-10ms -- imperceptible to the user but slower than memory.

**Tier 3 -- SQLite + zstd Compression (~20-50ms):** The persistent cache. All bar data eventually lands in SQLite, compressed with Zstandard. This is the cache that survives application restarts. The zstd compression achieves **15-30x** compression ratios on bar data because OHLCV data is highly regular and compresses exceptionally well.

**Tier 4 -- zstd File Cache (~100ms):** Bulk historical data stored as compressed binary files. This is the cold storage tier for data that does not fit efficiently in SQLite (very long historical ranges, exported datasets). Access time is ~100ms due to file I/O and decompression, but this tier handles arbitrarily large datasets.

**Binary Format:** Each bar is stored in a fixed **48-byte** binary format (timestamp + OHLCV as f64). No JSON parsing. No CSV splitting. No string-to-float conversions on read. Raw binary in, raw binary out. This format is what enables the 15-30x compression ratios -- zstd compresses regular binary patterns far better than it compresses text.

**Background Prefetch:** When the user views a chart for AAPL on H4, the terminal silently prefetches M15, H1, D1, and W1 data for AAPL in the background. By the time the user switches timeframes, the data is already cached. This makes timeframe switching feel instant even though the underlying API calls take seconds.

## GPU Chart Engine: Five Phases, All Complete

The chart engine was built in five distinct phases, each adding a layer of capability. All five are complete.

**Phase 1 -- Canvas Foundation:** Basic candlestick rendering on HTML5 Canvas. Price scale, time axis, scrolling. This was the "it works" phase -- functional but CPU-bound and limited to a few hundred bars before frame drops became noticeable.

**Phase 2 -- WebGL2 Migration:** The entire rendering pipeline moved to WebGL2. Candlestick bodies are rendered as **2 triangles** (a quad) per body. Wicks are **2 lines** per candle (high-to-body, body-to-low). Vertex shaders handle the coordinate transforms. The GPU does what GPUs are designed for -- rendering thousands of geometric primitives in parallel.

**Phase 3 -- Indicator Overlays:** All 39 indicators render through the same WebGL2 pipeline. Line-based indicators (SMA, EMA, KAMA) are GL_LINE_STRIP calls. Histogram indicators (MACD, Volume) are instanced quads. Bands (Bollinger, Keltner) are filled polygons with alpha blending. Every indicator renders on the GPU alongside the candlesticks.

**Phase 4 -- Drawing Tools:** All **44 drawing tools** render through WebGL2. Fibonacci levels, pitchforks, Gann fans, regression channels -- all GPU-rendered geometry. Interactive handles for dragging and resizing are hit-tested in JavaScript but rendered in WebGL2. Drawing tools do not degrade chart performance because they are just more vertices in the same render pass.

**Phase 5 -- Polish and Performance:** Crosshair rendering, tooltip overlays, smooth pan/zoom with momentum, price scale auto-ranging, and the final performance pass. The compiled Wasm module for the chart engine is **45KB**. The engine renders **10,000+ bars at 60fps** with multiple indicators and drawing tools active simultaneously.

The GPU chart engine is why TyphooN-Terminal can display a 4K chart with 39 indicators and 15 Fibonacci levels without dropping a frame. CPU-based canvas rendering (TradingView, most Electron apps) cannot do this. The GPU can.

**Draggable Panel Splitter:** The chart and sidebar panels resize by dragging the divider between them. Layout proportions persist across sessions. This sounds like a small thing until you realize NinjaTrader has fixed panel widths and TradingView charges for customizable layouts. In TyphooN-Terminal it is a mousedown/mousemove handler and 19 lines of CSS. Open source means features like this take minutes, not feature request tickets.

## Wasm Indicator Engine

Indicators are the heaviest per-bar computation in any trading terminal. TyphooN-Terminal compiles the indicator math to WebAssembly and runs it off the main thread.

**The compiled Wasm binary is 32KB.** That is the entire indicator engine -- 22 ported indicators, all mathematical kernels, all buffer management. 32KB. For context, a typical npm package for a single charting library starts at 200KB+.

**Performance vs JavaScript:**

| Indicator | JS (ms/10K bars) | Wasm (ms/10K bars) | Speedup |
|---|---|---|---|
| SMA | ~20ms | ~1ms | **20x** |
| KAMA | ~25ms | ~1ms | **25x** |
| Fisher Transform | ~27ms | ~1ms | **27x** |
| Grid Optimizer | ~500ms | ~5-10ms | **50-100x** |

The grid optimizer speedup is the most dramatic because it runs thousands of parameter combinations across the indicator suite. What takes half a second in JavaScript completes in under 10 milliseconds in Wasm. This makes real-time parameter optimization feasible during live trading.

**22 indicators** are fully ported to Wasm. The remaining 17 run in JavaScript with automatic fallback -- if the Wasm module fails to load (older browsers, restricted environments), every indicator still works via the JS implementation. Zero functionality loss. Just slower.

**Web Worker Isolation:** The Wasm indicator engine runs in a dedicated Web Worker, completely off the main thread. Indicator recalculation on a timeframe switch or new bar does not block UI rendering. The chart stays responsive at 60fps while the worker crunches 39 indicators across 10,000 bars in the background.

## Bug Fixes and Reliability

Shipping fast means nothing if the software crashes in production. TyphooN-Terminal has **602 smoke tests** and every single one passes.

**15 NaN Bugs Fixed:** Floating-point NaN (Not a Number) is the silent killer of trading software. A single NaN in an indicator buffer propagates through every downstream calculation, turning charts into empty panels and risk calculations into nonsense. All 15 NaN sources were identified and fixed:
- Division by zero in ATR when bar range is zero (flat candles)
- Log of zero in Fisher Transform on the first few bars
- Square root of negative numbers in standard deviation on single-bar windows
- NaN propagation through indicator chains (e.g., KAMA feeding into Fisher)

**Race Condition Guards (ADR-024):** Architecture Decision Record 024 documents **7 cross-symbol race conditions** that were identified and fixed. These occur when multiple symbols fetch data simultaneously and indicator calculations for Symbol A accidentally read incomplete data from Symbol B's buffer. The fix: each symbol gets its own isolated calculation context with atomic state transitions. No shared mutable state between symbol pipelines.

**429 Rate Limit Stale Data Fix:** When Alpaca returned HTTP 429 during a data fetch, the old code path would silently return stale cached data without marking it as stale. The user would see prices from hours or days ago with no indication that the data was outdated. Fixed: stale data is now visually flagged in the UI, and a background retry ensures fresh data replaces it as soon as the rate limit window expires.

**Arc Cache Lock Contention Fix:** The SQLite cache is now `Arc<SqliteCache>` — the Tauri state lock is dropped immediately after cloning the Arc reference. Heavy operations (API fetch, merge_bars, zstd compression) run outside the lock. Previously, the state lock was held for the entire incremental fetch cycle (seconds to minutes for crypto), which froze the UI. Now the lock is held for microseconds. This is the difference between "the app freezes when loading charts" and "charts load in the background while you trade."

**Dual-Layer Bar Sanitization:** Bad data from APIs is caught at two boundaries. The Rust backend rejects bars with zero/NaN prices, fixes OHLC inconsistency (`true_high = max(o,h,l,c)`), and drops malformed timestamps at parse time. The JavaScript frontend runs `sanitizeBars()` before every chart render — removing duplicates, sorting by time, clamping negative volume. The dual-layer approach means zero chart artifacts even when Alpaca returns malformed crypto bars (which it does, occasionally).

**602/602 smoke tests pass.** The test suite covers command execution, indicator calculation accuracy, order type validation, API response parsing, cache coherence, and UI state transitions. Every commit runs the full suite. No exceptions.

## MT5 Direct SQLite Sync: Zero-Copy Bar Data From Every Darwinex Account

The original MT5 integration used CSV exports. Export from MetaTrader, parse in Rust, store in SQLite. Three steps, file I/O overhead, and manual intervention every time you wanted fresh data. That pipeline is dead.

TyphooN-Terminal now reads MT5's SQLite database **directly**. A custom MQL5 Expert Advisor (**BarCacheWriter.mq5**) writes OHLCV bars to a shared SQLite database in WAL mode. The Rust backend reads the same database file -- zero CSV parsing, zero file I/O intermediary, zero manual export steps. BarCacheWriter writes. TyphooN-Terminal reads. Same database. Different processes. WAL mode handles the concurrency.

**Multi-Instance Sync Across All Darwinex Accounts**

Running six DARWINs means running multiple MT5 instances -- Futures, Crypto, CFD, Stocks/ETFs. Each instance has its own BarCacheWriter database. `find_all_mt5_sqlite_dbs()` discovers every `typhoon_mt5_cache.db` across all `.mt5_*` instance directories and merges them into the terminal's unified cache. Each Darwinex account type contributes unique symbols. No conflicts. No duplicates. One sync command pulls **895 symbols** across all accounts simultaneously.

**Symbol Normalization:** MT5 names like `SOLUSD`, `EURUSD`, `XAUUSD` are normalized at every import boundary -- `SOL/USD`, `EUR/USD`, `XAU/USD`. Crypto, forex, metals all get slash-separated pairs. Indices like `US30` and `DE40` stay as-is. The terminal speaks the same symbol language as Alpaca regardless of where the data originated.

**Live Sync Progress UI:** The sync window shows real-time progress with per-category status bars -- Forex, Crypto, Commodities, Indices, Healthcare, Technology, and more. Each category displays complete, partial, and pending counts. The sync runs continuously with live updates instead of one-shot import. Green bars fill as symbols sync. The UI never freezes because all heavy operations run on `spawn_blocking` threads outside the Tauri state lock.

Full sync across all 3 Darwinex instances: **895 symbols**, **8,447 bar entries** synced. Every sector fully populated -- Basic Materials (35), Commodities (44), Communication Services (28), Consumer Cyclical (103), Consumer Defensive (42), Crypto Currency (7), Financial (194+1 partial), Forex (41+1 partial+6 pending), Healthcare (97), Indices (11), Industrials (112), Other (11), Real Estate (8), Technology (124), Utilities (30). The sync idles at **"Waiting for BarCacheWriter"** when all databases are current, consuming zero resources until fresh bars arrive.

![MT5 SQLite Sync -- 895 symbols, 8447 bar entries synced across all 3 Darwinex instances with full per-category and per-symbol breakdown](/img/mt5-sync-895-symbols.webp)

**OOM Guards and Sync Safety:**
- **Sync mutex** via `AtomicBool` prevents concurrent background + foreground syncs from doubling memory usage
- **100-entry cap** per sync cycle -- excess entries are deferred to the next cycle, preventing memory spikes on initial sync of large databases
- **Mtime fast-path:** Before scanning metadata, the sync checks filesystem modification times on all MT5 databases. If nothing changed since last cycle, it skips the entire metadata scan -- zero allocations, zero database reads. The UI shows "idle (no changes)" during fast-path skips
- **Rayon threshold:** Parallel compression via rayon only kicks in at 32+ entries per cycle. For typical incremental syncs (~9 entries/cycle), sequential compression is faster because rayon's thread pool overhead exceeds the parallelism benefit
- **Progress event throttling:** `mt5-sync-progress` IPC events fire every 10th entry instead of every entry -- **~90% reduction** in frontend IPC traffic during large syncs
- **Cached symbol normalization:** `normalize_mt5_symbol()` results are cached in a static `HashMap`. Repeated normalization of the same MT5 symbol (which happens every 30-second sync cycle) hits the cache instead of re-running string comparisons
- **Covering index:** `idx_bar_meta` index on the SQLite cache enables metadata-only scans without touching bar data pages. Metadata queries (cache age checks, symbol enumeration) run faster because the index covers the query entirely

**BarCacheWriter Optimizations (v1.200):**
- CSV format instead of JSON -- **60% smaller** payloads, O(n) string construction
- Incremental writes -- tracks last bar time per symbol:TF, skips unchanged data (**90% less I/O**)
- Full export only on initialization, incremental 100 bars/TF after
- 30-second update interval (was 10s), configurable

**The pipeline reduction:** What was CSV export → file discovery → parse → validate → store is now SQLite read → validate → store. Two fewer steps. No human intervention. The sync runs in the background while you trade.

**MT5 as Master Data Source (ADR-037):** MT5 is now the authoritative data source for every symbol it covers. No more merge complexity between MT5 and Alpaca -- if MT5 has the symbol, MT5 wins. The deepest history always takes priority. Alpaca is the fallback for symbols MT5 does not have. The frontend's `cachedGetBars` uses a 5-second rapid dedup window instead of per-timeframe staleness checks (which could defer up to 7 days), ensuring the backend's MT5-first logic always runs. When background MT5 sync imports new bars, the in-memory cache is invalidated and the chart reloads automatically -- no manual refresh needed.

**UI State Persistence:** Every panel toggle -- news, indicators, log, watchlist, positions, orders -- saves session state immediately. Indicator checkbox changes, article opens, and watchlist collapse state all persist. Close the terminal and reopen it: everything is exactly where you left it.

**Auto-Fib Labels:** Fibonacci retracement levels now display text labels with both the ratio and the computed price level (e.g., "61.8% (25.30)"). No more eyeballing where a fib level lands on the price axis.

**Live Bid/Ask Sync from MT5:** BarCacheWriter now writes a `bid_ask` table alongside bar data. The MT5 sync pipeline reads these quotes and caches them as a JSON array via the `__MT5_QUOTES__` KV key. The frontend falls back to MT5 bid/ask when Alpaca quotes are unavailable -- displayed with a blue indicator to show the MT5 source. This means live quotes for **every symbol MT5 covers**, even when the Alpaca WebSocket has no subscription for that instrument. 895 symbols with live pricing without 895 WebSocket subscriptions.

## Kraken Crypto Data Source: Full History From 2013

Alpaca's crypto history is shallow. MT5's crypto coverage depends on your broker. Kraken has **every major crypto pair back to 2013** (BTC genesis on Kraken) and a public API that requires no API key.

New module `core/kraken.rs` adds Kraken as the third data source in a three-tier hierarchy:

1. **MT5 (Darwinex)** -- weekday authority, deepest history for CFDs
2. **Kraken** -- fills weekend gaps, extends history from 2013, covers Kraken-only symbols
3. **Alpaca** -- live trading execution and US equities

**Weekend Gap-Fill:** MT5 crypto CFDs don't trade on weekends. Kraken does. The Kraken fetcher fills those weekend gaps automatically. Your BTC/USD chart no longer has holes every Saturday and Sunday.

**Any-Symbol Support:** Kraken covers symbols that neither Darwinex nor Alpaca list. The `list_kraken_pairs` command fetches all USD pairs from Kraken's AssetPairs API. Click any pair to fetch its full history.

**SOURCES Command:** A unified data source manager with 5 views -- Overview (card-style display of all 4 data providers with status), MT5 (cached symbols with TF count, cache size, sync age), Alpaca (account status and portfolio info), Kraken Crypto (cached crypto with bar counts and one-click backfill), and Add from Kraken (live pair listing, click to fetch any symbol). One command to see every data source, its status, and what it covers.

**Smart Incremental Sync:** First run does a full 2013→now fetch in a single pass, filling every weekend gap. Subsequent runs only do incremental forward fill from the latest cached bar. Two tracking keys (`kraken_full` and `kraken_sync`) ensure the full backfill only runs once per symbol:timeframe. Rate limit handling (4s between requests, 15s backoff + retry on 429) ensures the backfill completes without hammering Kraken. Reset Tracking button forces a full re-sync when needed. The frontend shows color-coded status per pair: green (new data), blue (already synced), amber (pending), red (error).

**All 9 Timeframes Backfilled:** 1Min, 5Min, 15Min, 30Min, 1Hour, 4Hour, Daily, Weekly, Monthly -- all gap-filled from Kraken with smart depth limits per timeframe. 1Min goes back 30 days (avoids millions of bars), 5Min 90 days, 15Min 1 year, 30Min 2 years, 1Hour+ full history from 2013.

**Live Backfill Grid:** Real-time status grid showing per-symbol per-timeframe completion. Each cell updates live as Tauri events fire for every completed fetch -- `✓` synced, `+` new data, `⟳` fetching, `⏳` pending, `✗` error. Hover tooltips show bar count and estimated percentage (e.g., "19,732 bars (99% est)"). Auto-retry loops until all combos are synced (max 10 passes), with 15s backoff on rate limits and a stop button to cancel mid-backfill.

**Quake Console Toggle:** Backtick (`` ` ``) and tilde (`~`) toggle the command bar -- tap to focus and select all, tap again to dismiss. The same muscle memory as opening the Quake console. Capture phase handler prevents the character from typing into the input.

**Weekend Auto-Poll:** The terminal detects when you are viewing a crypto symbol on a weekend (Friday 22:00 – Sunday 22:00 UTC) and automatically polls Kraken every 30 seconds. The chart cache invalidates and reloads with fresh data. Crypto charts stay live on weekends without manual intervention. Weekend candles render with a **blue tint** to visually distinguish Kraken-sourced bars from MT5 weekday bars -- you always know which data source painted each candle. A "Kraken (weekend)" badge appears in the chart header during off-hours.

**Bid/Ask Price Lines:** Green dashed line for bid, red dashed for ask, updated every 10 seconds from MT5 quotes. Works on all chart types including the MTF Grid. The spread is visible at a glance on every chart.

**DARWIN Quote Charting:** Type any DARWIN ticker (e.g., `HAKR`) in the symbol bar to chart it. The terminal fetches synthetic OHLC from FTP RETURN data and renders it as a standard candlestick chart. Transparent fallthrough to normal chart loading if the ticker is not a DARWIN.

**Auto-Reimport DARWIN XLSX:** A file watcher monitors `~/mt5xml/` for modified XLSX files and reimports them automatically every 60 seconds. Drop a fresh Darwinex trade history export into the folder and the terminal picks it up without any manual import step.

The crypto data gap is closed. Thirteen years of continuous crypto history across all 9 timeframes, weekends included. Binance was the original implementation but was replaced with Kraken due to US geo-blocking restrictions.

## DARWIN Import Pipeline: XLSX Trade History to Portfolio Analytics

Six DARWINs means six separate Darwinex accounts, each with its own trade history. Darwinex exports trade history as XLSX spreadsheets. TyphooN-Terminal now ingests those spreadsheets directly.

**core/darwin.rs** (1,178 lines of new Rust) parses XLSX files via the `calamine` crate, extracts every deal, stores them in SQLite, and reconstructs open positions using volume-balance detection. The entire deal history for all six DARWINs lives in the terminal's database with dedicated SQLite connections -- no contention with the MT5 sync pipeline.

**Per-DARWIN Commands (9):** The `DARWIN` command opens a per-account viewer -- account summary, open positions, equity curve, P&L breakdown by symbol, and full deal history. Every DARWIN gets its own analysis dashboard.

**Portfolio-Level Commands (13):** The `DARWINS` command launches a combined portfolio dashboard across all imported DARWINs. Cross-DARWIN position exposure, aggregate equity curves, and combined analytics in one view.

**DARWINS Risk Analytics Dashboard:**

The `DARWINS` command is a full risk analytics dashboard with six tabbed views:

- **Portfolio VaR:** VaR 95%/99%, CVaR, Sharpe, Sortino, Calmar ratios with a per-DARWIN comparison table. See which DARWINs contribute the most risk at a glance.
- **Drawdown Chart:** Portfolio drawdown over time with per-DARWIN current/max drawdown and recovery factor. Canvas-rendered area chart shows exactly when and how deep each drawdown went.
- **Rolling VaR:** 60-day rolling VaR 95%/99% and rolling Sharpe ratio plotted over time. Spot regime changes in portfolio risk before they become problems.
- **Monthly Heatmap:** Color-coded monthly returns grid -- combined portfolio and per-DARWIN breakdown. Green months, red months, the full picture at a glance.
- **P&L Distribution:** Histogram with VaR lines overlaid, plus skew, kurtosis, and win/loss day statistics. Know whether your returns distribution has fat tails.
- **Correlation Matrix:** Cross-DARWIN correlation with color coding -- green means diversified, red means redundant. If two DARWINs are 0.9 correlated, one of them is not adding value.

All charts use a reusable `drawChart()` canvas helper for consistent line/area rendering across the dashboard.

This is the complete Darwinex analytics pipeline: XLSX import → deal parsing → open position reconstruction → per-account analysis → portfolio-level risk dashboard. What previously required a spreadsheet and manual calculation now runs as two Ctrl+K commands.

## Trade Pattern Analytics

Seven new per-DARWIN analytical views that answer the questions every trader asks but never quantifies:

**Win/Loss Streaks:** Distribution chart of consecutive wins and losses. How long do your winning streaks run? How deep do your losing streaks go? The streak analysis exposes whether your strategy clusters wins or distributes them evenly.

**Hourly P&L Heatmap:** P&L and win rate broken down by hour (0-23 UTC). Reveals which hours of the trading day are profitable and which are hemorrhaging money. If your win rate drops to 30% between 14:00-16:00 UTC, the heatmap makes it obvious.

**Day-of-Week Breakdown:** Average P&L and win rate by day. Monday winners, Friday losers -- or the reverse. Pattern detection across the weekly cycle.

**Hold Time Distribution:** Seven buckets from <1 hour to >4 weeks, with median, average, min, and max hold times. Are your best trades the quick scalps or the multi-week holds? The distribution answers empirically.

**Position Sizing Efficiency:** Quartile analysis -- do larger positions perform better than smaller ones? If your top-quartile position sizes underperform your bottom quartile, your sizing model is backwards.

**Commission & Swap Cost Analysis:** Cumulative costs, per-symbol breakdown, and costs as percentage of equity. The drag that nobody tracks until it has eaten 15% of their returns.

**Cross-DARWIN Trade Overlaps:** Symbols held in multiple accounts simultaneously, with concentration risk warnings. If three DARWINs are all long EURUSD, that is not diversification -- it is concentrated exposure with extra commissions.

## DARWIN RADAR: FTP Screener for 50K+ DARWINs

The `RADAR` command scans Darwinex's FTP server to screen **all 50,000+ DARWINs** with configurable filters: minimum trading days, minimum return percentage, maximum drawdown percentage. Results are ranked by a composite score.

The screener does not trust Darwinex's published metrics. It parses raw RETURN files for equity curves and independently computes Sharpe ratios and drawdown. It reads POSITIONS files to identify which symbols each DARWIN trades. The analysis is from primary data, not derived ratings.

**Radar Snapshot Export:** Dumps MT5 specs to `~/mt5xml/radar/` for MarketWizardry.org compatibility. Symbol lifecycle tracking shows first/last trade dates, active months, and P&L per symbol for every DARWIN in the scan.

This replaces manually browsing Darwinex's platform to find DARWINs worth following. One command. Configurable filters. 50K+ DARWINs scanned. Ranked by math, not marketing.

## Advanced Risk Analytics: Monte Carlo, Stress Tests, Kelly Criterion

The analytics suite went from "useful" to "institutional-grade" with six new analytical modules backed by **32 unit tests** and **2,900+ lines** of Rust in `darwin.rs`:

**Monte Carlo VaR:** 10,000 simulated portfolio paths using historical return distributions. Instead of a single VaR number, you get a percentile distribution -- the 1st, 5th, 10th, 25th, 50th percentile outcomes across all simulated paths. This is how hedge funds estimate tail risk. Now it runs as a Ctrl+K view.

**Stress Testing:** Six historical crash scenarios applied to your portfolio: **COVID crash** (March 2020), **Global Financial Crisis** (2008), **Rate Hike Shock** (2022), **Flash Crash** (May 2010), **Tech Wreck** (2000-2002), and **Crypto Winter** (2022). Each scenario shows projected portfolio impact based on your current positions and correlations. Know how your portfolio would have performed during every major crisis of the last 25 years.

**Kelly Criterion:** Optimal position sizing computed from your actual win rate and payoff ratio. Kelly tells you the mathematically optimal percentage of capital to risk per trade. Overbetting degrades returns. Underbetting leaves money on the table. Kelly finds the edge.

**Sector Exposure:** GICS-classified portfolio breakdown -- Technology, Healthcare, Financials, Energy, and every other sector. Visualizes concentration risk. If 60% of your portfolio is in Technology, the sector exposure chart makes it impossible to ignore.

**VaR Forecast:** Linear trend projection of rolling VaR with threshold crossing estimates. If your VaR has been trending upward for 30 days, the forecast tells you when it will breach your risk limit at the current trajectory.

**Trade Autocorrelation:** Lag-1, lag-2, lag-3, and lag-5 serial dependence tests on your trade returns. If your wins cluster (positive autocorrelation), your strategy has momentum. If your trades are serially independent, each trade is a fresh coin flip. The autocorrelation analysis tells you which one you are running.

**DARWIN Price Series:** Synthetic OHLC candles constructed from FTP RETURN data at daily, weekly, and monthly resolution. View any DARWIN's equity curve as a candlestick chart -- the same way you view a stock. Spot trends, reversals, and consolidation patterns in DARWIN performance.

All **73 unit tests** pass (32 + 41 new) against an in-memory SQLite test database covering table creation, account CRUD, open position reconstruction, VaR computation, daily/monthly returns, rolling VaR, equity curves, and every analytical module listed above.

## Complete Analytics Expansion: 50+ Functions, 4,200 Lines of Rust

The analytics engine expanded again with 12 more modules, bringing `darwin.rs` to **4,200+ lines** with **50+ analytics functions**:

**Seasonal Analysis:** Monthly return patterns across years with bar chart data. Average and median returns per month, plus best/worst year for each month. Reveals whether January is consistently your best month or if August is consistently deadly.

**MAE/MFE Estimation:** Maximum Adverse Excursion and Maximum Favorable Excursion estimated from daily volatility and hold time. How far do your trades go against you before recovering? How far do they run in your favor before reversing? MAE/MFE separates good entries from bad ones.

**What-If Simulator:** Portfolio VaR impact of closing a specific symbol. Before you exit a position, see how the portfolio's risk profile changes. If closing EURUSD increases your VaR because it was hedging other positions, the what-if tells you before you click.

**Liquidity Risk:** Days-to-exit estimation by volume tier with risk classifications. If your position would take 15 days to unwind at normal volume, the liquidity risk module flags it. Concentration warnings included.

**Tail Risk Dashboard:** Skewness, kurtosis, Ulcer Index, Omega ratio, gain-to-pain ratio, and fat tail warnings. Know whether your return distribution has the kind of tails that blow up accounts.

**Trading Burst Detection:** Weekly trade clustering with intensity classification. Identifies periods of excessive trading activity -- the kind that usually correlates with emotional decision-making rather than strategy execution.

**Position Pyramiding Analysis:** Detects scaling-in versus averaging-down behavior per symbol. Scaling into winners is a valid strategy. Averaging down into losers is a different thing entirely. The pyramiding analysis distinguishes the two.

**Low-Correlation DARWIN Finder:** Scans the FTP for DARWINs that are uncorrelated with your current portfolio. The diversification tool that finds what you are missing.

**Investor Flow Reader:** AuM (Assets under Management) and investor count from FTP INVESTMENT_CHART data. Track capital inflows and outflows over time.

**D-Score Components:** Reads all 8 Darwinex investability scores from FTP. Experience, risk management, consistency, and more -- decomposed into individual components instead of a single opaque rating.

**Alert System:** VaR breach, drawdown threshold, concentration risk, trade overlap, and correlation spike detection. Alerts fire with severity badges and color-coded thresholds. Risk monitoring that does not require staring at dashboards.

**Benchmark Comparison:** Alpha, beta, information ratio, and tracking error against benchmark indices. How much of your return is skill versus market exposure?

The DARWIN command now has **18 views**. The DARWINS command has **33 views**. Combined with the per-account analysis and **5,400+ lines** of Rust in `darwin.rs`, the terminal provides deeper analytics than most institutional risk platforms charge five figures a year for.

## Daily Report, Tax Lots, and Cross-Account Intelligence

The final analytics push completes every remaining view:

**Daily Risk Report:** One-screen portfolio snapshot -- current regime badge, total equity, P&L, VaR, drawdown, top gainers/losers, active alerts. The morning briefing that replaces checking six separate account dashboards.

**Tax Lot Tracking:** FIFO cost basis calculation with short-term versus long-term capital gains classification. Interactive account and year selector with gain/loss summary. Tax season solved by a Ctrl+K command.

**Cross-Account Timing Divergence:** Detects when multiple DARWINs entered the same symbol at different times and prices. If two accounts opened EURUSD three hours apart at different prices, the divergence analysis quantifies the spread and flags concentration risk.

**Regime Performance:** Per-DARWIN Sharpe ratio comparison across LOW, MEDIUM, and HIGH volatility regimes. Know which DARWINs thrive in crisis and which ones only perform in calm markets.

**Investor Flow:** AuM and investor count charts from FTP data, per-DARWIN and portfolio-level. Track when capital enters and exits each strategy over time.

**D-Score Components:** All 8 Darwinex investability scores color-coded -- experience, risk management, consistency, and more. Per-DARWIN and portfolio aggregate views.

**Low-Correlation Finder:** Scans the FTP for DARWINs that are uncorrelated with your current portfolio, ranked by correlation and Sharpe. The diversification discovery tool.

**Benchmark Comparison:** Alpha, beta, tracking error, and information ratio against benchmark indices. Decompose your returns into skill and market exposure.

## Risk Simulation and Portfolio Optimization

The final analytics expansion pushes `darwin.rs` past **4,900 lines** with **120 unit tests** (602 smoke + 47 + 41 + 32 new):

**Margin Call Simulator:** Monte Carlo simulation estimating the probability of margin call at 30 and 90 days. Uses historical return distributions to project thousands of equity paths forward. If the 30-day margin call probability exceeds 5%, you are overleveraged and the simulator tells you before the broker does.

**Slippage Analysis:** Entry price versus deal execution price comparison, broken down by symbol and hour of day. Reveals systematic slippage -- are your fills consistently worse at certain times? Which symbols have the worst execution quality?

**Optimal DARWIN Allocation:** Inverse-volatility weighting with Sharpe contribution analysis. Compares your current equal-weight allocation against the mathematically optimal allocation. Shows exactly how much each DARWIN contributes to portfolio Sharpe and which ones are dragging performance.

**Conditional VaR:** VaR computed separately for LOW, MEDIUM, and HIGH volatility regimes. Standard VaR blends all market conditions together. Conditional VaR tells you your risk in calm markets versus your risk in crisis markets -- two very different numbers.

**Market Regime Detection:** 20-day rolling volatility with automatic regime classification and regime history tracking. Know whether you are currently in a low-vol grind, a normal environment, or a high-vol crisis. The regime history timeline shows how long each regime lasted and when transitions occurred.

**Exposure Treemap:** Hierarchical sector-to-symbol breakdown for treemap visualization. Sector-colored blocks with proportional sizing show portfolio concentration at a glance. Technology taking up half the treemap is impossible to miss.

**What-If Simulator:** Interactive symbol input with real-time VaR impact calculation. Type a symbol, see how adding or removing it changes your portfolio's risk profile. Make allocation decisions with immediate feedback on their risk consequences.

## Indicator Parity Fixes, Multi-Symbol MTF Grid, and Performance

Twelve indicator fixes across JS, WASM, Web Worker, and fallback paths: EMA SMA bootstrap, KAMA seed, Fisher median+window, MACD signal, DEMA, Bollinger NaN handling, ATR initial value, minBars enforcement, Ichimoku Chikou, BetterVolume 2-bar, Alligator shift, ForceIndex. Every indicator now produces identical output regardless of which execution path handles it.

**Multi-Symbol MTF Grid:** The grid now supports multiple symbols simultaneously. View CC+SLV across H4+D1+MN1 in a single grid. GPU-first rendering with full `addLineSeries` wrapper. Sequential grid cell loading with `requestAnimationFrame` yields keeps the UI responsive during heavy multi-symbol loads.

**get_bars_tail: 34x Faster MT5 Bar Serving.** The old path serialized entire bar arrays to JSON, round-tripped through IPC, and deserialized. The new path does a binary tail read from the SQLite cache -- direct binary slice, zero JSON overhead. MT5 sync no longer triggers a full chart reload either (was freezing the UI every 30 seconds).

**Indicator Bar Cap:** Indicators compute on the most recent 1,000 bars. Full data is preserved for scrolling. This eliminates the case where a 10,000-bar chart causes 39 indicators to recompute on every pan, turning the GPU chart into a slideshow.

## Backup, LAN Sync, and Credential Management

**BACKUP-CREDS / RESTORE-CREDS:** AES-256-GCM encrypted credential backup to `.ttbackup` files. Export your API keys and broker credentials as a single encrypted file. Move between machines without re-entering keys.

**BACKUP-DATA / RESTORE-DATA:** Full SQLite database and DARWIN data backup to `.ttfull` files. The complete terminal state -- bar cache, DARWIN analytics, settings -- in one portable archive.

**LAN-SERVER / LAN-CLIENT / LAN-STATUS:** WebSocket-based LAN sync with HMAC authentication. Run the terminal on two machines and keep their data synchronized over the local network. The server pushes updates, the client receives them, HMAC prevents unauthorized connections.

## Extended DARWIN Analytics

Seven new DARWIN dashboard views:

**DRAWDOWN:** Combined drawdown dashboard with SVG bar charts. Portfolio and per-DARWIN drawdown visualized side by side.

**FLOATING:** Mark-to-market equity using live Alpaca quotes. Real-time portfolio valuation, not end-of-day snapshots.

**REBALANCE:** Profit-only portfolio rebalancer with 45-day correlation window and 0.95 correlation threshold. Suggests allocation changes using only realized profits -- never touches principal.

**VAR-MULTIPLIER:** Darwinex VaR corridor prediction (3.25-6.5% target range) using a blended 45-day + 6-month model. Predicts when your VaR will breach Darwinex's investability thresholds.

**SYMBOL-OVERLAP:** Cross-DARWIN correlation heatmap. Visual heat grid showing which DARWINs are trading the same symbols with correlated timing.

**DARWIN-TRADES:** Buy/sell arrows from deal history rendered directly on the chart. See exactly where every entry and exit occurred on the price action.

**MT5-Style Margin Bar:** Balance, Equity, Margin, Free Margin, and Margin Level percentage displayed in a familiar MT5-format status bar at the bottom of the dashboard.

## SEC Filing System: 27 Form Types, Insider Tracking, Auto-Alerts

New module `sec_filing.rs` turns the terminal into an SEC EDGAR research platform:

**27 form types tracked:** 10-K, 10-Q, 8-K, Form 3/4/5, SC 13D/G, 13F-HR, S-1/S-3/S-4, 424B, PREM14A, DEF14A, SC TO, 15-12B/G, CORRESP, 11-K, and amended/late filing variants. Each form type has an importance score (10-85) and category classification.

**Form 4 XML Parser:** Extracts insider name, title, transaction type, shares, and price from Form 4 filings. The raw data that insider trading trackers charge subscriptions for, parsed locally from primary SEC data.

**Auto-Alerts:** Activist accumulation (SC 13D), financial restatement (10-K/A), dilution risk (S-3/424B), delisting warning (15-12B), tender offers (SC TO), late filings, and SEC inquiry detection. Alerts fire automatically with severity classification.

**SEC-SCANNER:** Filing dashboard with form type filters, importance bars, and one-click "Scrape Now." **INSIDER-TRACKER:** Insider trade aggregation with BUY/SELL color coding across all tracked symbols. **SEC-ALERTS:** Alert cards with dismiss and reason dropdown. **SEC-OVERLAY:** Filing event markers rendered directly on the price chart -- see exactly when an 8-K dropped relative to the price move.

**EV-OUTLIER:** Market cap to enterprise value IQR outlier detection by industry -- the MarketWizardry.org EV Explorer, ported to Rust and running on live data.

**Daily auto-scrape** runs on startup if more than 24 hours since the last run. Rate limited at 200ms between SEC requests. CIK lookups cached in SQLite.

## Full Indicator Data and MTF Grid Improvements

The 1,000-bar indicator cap is gone. Indicators now compute on **all bars** -- matching MT5 behavior exactly. WASM handles the heavy lifting (SMA, EMA, KAMA, RSI, ATR) while the backend serves up to 50,000 bars per request. Grid cells increased from 250 to 500 bars.

**MTF Grid: Current Symbol vs All Tabs.** A radio toggle switches the grid between showing all timeframes for the current symbol or displaying all open tabs simultaneously. Live rebuild on toggle -- no page reload needed.

## Performance Phase 2: Async Pipeline, GPU Rendering, Adaptive Vsync

The rendering and computation pipeline was rebuilt from the ground up:

**Async Indicator Pipeline:** Every indicator and HTF projection yields between computations. The UI never freezes during a 39-indicator recalculation across 10,000 bars. A 200-entry indicator memoization cache prevents recomputation when scrolling back to previously viewed ranges.

**GPU Histogram and Fill Rendering:** The WASM chart engine gained `add_histogram`, `add_fill`, and `add_pane_histogram` — volume bars, MACD histograms, and Bollinger Band fills are now GPU-rendered geometry instead of CPU canvas operations.

**10x Timestamp Parser:** The bar timestamp parser was rewritten for direct integer parsing instead of Date object construction. On a 50,000-bar dataset, this alone saves hundreds of milliseconds per load.

**Adaptive Vsync Render Loop:** The chart renders at monitor refresh rate when the viewport is changing (scroll, zoom, new data) and drops to 0fps when idle. No wasted GPU cycles on a static chart.

**Web Worker Grid Computation:** MTF Grid cells compute indicators in a dedicated Web Worker, completely off the main thread. Parallel prefetch loads adjacent cells while the current one renders.

**Binary Search Data Clipping, O(1) Crosshair Lookup:** Visible bar range is found via binary search instead of linear scan. Crosshair price lookup uses a Map instead of array iteration.

**localStorage Write Batching, Tab Visibility Pausing, DOM Ref Caching:** Session state writes are batched to prevent per-keystroke disk I/O. Background tabs pause their update intervals. Frequently accessed DOM elements are cached as references.

## MQL5 Compiler: Parse MQL5, Generate WASM

A new `mql5_compiler` crate parses MQL5 source code and compiles it to WebAssembly. The pipeline: **pest parser → AST → IR → WASM codegen**. The `COMPILE` command in the Ctrl+K palette triggers compilation from within the terminal. This is the foundation for running custom MQL5 indicators natively in the terminal without MetaTrader — write once in MQL5, compile to WASM, execute at near-native speed alongside the existing 39 indicators.

## Native Rust GPU Renderer: Zero JavaScript, Zero WebKit

The entire JavaScript/WebKit frontend has been eliminated. **40,000 lines of JS deleted.** The WASM chart engine (WebGL2) and WASM indicator worker -- gone. Every byte of functionality is being rebuilt in pure Rust with **egui + wgpu** for native GPU rendering.

The architecture shift:
- `src-tauri/` (Tauri backend) → `engine/` (pure Rust library, zero framework dependency)
- New `native/` crate: egui + wgpu native GPU application
- Cargo workspace: `engine` + `native` + `mql5_compiler`
- **Zero JSON serialization.** Data flows from Rust structs directly to GPU buffers. No IPC. No string parsing. No garbage collection.
- **Zero WebKit.** No system webview. No Chromium. No DOM. The terminal is a native window with GPU-rendered pixels.

This is the final architecture. The Tauri/WebKit version proved the feature set. The native version delivers it without the overhead. Direct memory → GPU -- rendered by the GPU instead of a browser engine pretending to be a desktop application.

**Full feature parity achieved in 5,147 lines of native Rust:**

- **21 indicators:** SMA, EMA, KAMA, Bollinger Bands, RSI, Fisher Transform, ATR, MACD, Stochastic, ADX, Ichimoku, WMA, HMA, CCI, Williams %R, OBV, Momentum, Parabolic SAR, ATR Projection, Better Volume
- **7 drawing tools:** HLine, TrendLine, Fibonacci, VLine, Rectangle, Ray, Channel
- **5 chart types:** Candlestick, Heikin Ashi, Line, OHLC Bars, Renko
- **29 panels** wired to the engine: Symbol Overlap, Correlation Matrix, Seasonals, Monte Carlo VaR, Stress Test, Volume Profile (POC/VA), Screener, Optimizer, VaR Multiplier, Margin Monitor, and more
- **DARWIN engine:** accounts, portfolio, VaR, correlations, exposure, streaks, hourly P&L, monthly returns, open positions, XLSX import via native file dialog
- **Backtest engine:** SMA Cross + NNFX strategies, grid search optimizer, trade reports, equity curves
- **Risk/margin engine:** risk lot calculator, margin monitor, max safe lots, PROTECT urgency
- Session persistence, CSV export, OLED `#000000` theme, Quake console (`~`)
- **Order Entry panel:** symbol, side, quantity, type (market/limit/stop/bracket), limit/stop/TP prices, risk preview with notional + ATR calculation
- **Data Window:** floating panel showing all indicator values at cursor position, color-coded and auto-updating as the crosshair moves
- **Price Alerts:** set alerts at any price with labels, triggered within 0.1% tolerance, managed from a dedicated Alerts panel
- **Previous Candle Levels:** daily and weekly high/low rendered as dotted lines (white=daily, magenta=weekly)
- **NNFX preset:** one command enables SMA200 + KAMA + Fisher + ATR Projection + Better Volume + Previous Levels -- the complete NNFX indicator suite in one click
- **Per-DARWIN equity curves** rendered with egui_plot in each account detail section
- **Pivot Points:** classic P/R1/R2/S1/S2 from previous daily high/low/close, color-coded (white=pivot, red=resistance, green=support)
- **Bill Williams Fractals:** 5-bar swing high/low arrows (green up, red down)
- **Scott Carney Harmonic Patterns:** automatic detection of all 7 patterns -- Gartley, Butterfly, Bat, Crab, Shark, Cypher, and 5-0 -- rendered on the chart
- **Supply/Demand Zones:** automatic detection and rendering of institutional supply and demand zones
- **Drawing Color Picker:** customize drawing tool colors per object
- **8 Ehlers indicators:** Super Smoother, Decycler, Instantaneous Trendline, MAMA/FAMA, Even Better Sinewave, Cyber Cycle, Center of Gravity, Roofing Filter
- **S/D Zone Labels:** zones classified as Untested, Tested, or Proven based on price interaction history
- **Right Panel:** tabbed layout (Trade/Positions/Orders/Watchlist/Risk), colored trading buttons, SL/TP inputs, MTF moving average dot grid, position P&L, colored watchlist
- **Chart Overlay:** ATR, close, volume, SL/TP, risk-reward displayed in the chart's top-right corner
- **GPU Compute Shaders:** wgpu compute pipeline for indicator computation -- bar data in VRAM, SMA fully parallel (256 threads/workgroup), EMA sequential
- **MultiKAMA + FakeCandle:** 10/10 MT5 custom indicator parity achieved in the native renderer
- **MTF_MA Overlay:** 200 SMA status, KAMA, Bull/Bear Power text overlay matching MTF_MA.mqh
- **44 unit tests** for all indicator computations
- **93 commands**, **32 windows**, **32+ indicators**

## Explorer Migration: VaR/ATR/EV/Crypto Scanners Built Into the Terminal

The MarketWizardry.org web explorers (ATR Explorer, VaR Explorer, EV Explorer, Crypto Explorer) served their purpose -- browser-based outlier analysis from static CSV data. But static CSVs go stale the moment they are generated. The terminal has live data. The explorers belong in the terminal.

**6 new Ctrl+K commands replace the web explorers entirely:**

**VAROUT** -- VaR Outlier Scanner. Scans all available symbols, groups by sector, runs IQR (1.5x interquartile range) outlier detection on VaR/Price ratios. Results display as a ranked table with clickable symbols and Z-scores. The symbols with statistically extreme risk profiles surface instantly.

**ATROUT** -- ATR Volatility Outlier Scanner. Same IQR methodology applied to ATR/Price ratios. Identifies symbols with abnormal volatility relative to their sector peers.

**EVOUT** -- Enterprise Value Scanner. Market cap to enterprise value ratios, balance sheet scoring. Finds companies where the market's valuation diverges significantly from the underlying asset value.

**CRYPTORISK** -- Crypto Risk Analysis. Multi-metric analysis including ATR volatility tiers, VaR levels, and advanced ratios across all available crypto symbols. Pulls from both Alpaca crypto data and MT5 crypto CFDs when available.

**OUTLIERS** -- Combined tabbed report. Launches any scanner from a tabbed interface. Switch between VaR, ATR, EV, and crypto outliers without re-running the analysis.

**SCREEN** -- Multi-Factor Screener. Cross-references VaR and ATR to find dual outliers -- symbols that are extreme on multiple risk dimensions simultaneously. These are the symbols that deserve attention because they are anomalous on more than one axis.

**The Rust backend does the math:** `calculate_atr()` computes Average True Range from OHLC bars. `detect_outliers()` runs IQR-based outlier detection with sector grouping and Z-score classification. `OutlierResult` and `SectorStats` structs provide structured output. All computation happens in compiled Rust -- no JavaScript number crunching, no CSV parsing in the browser.

**DARWINEX Command:** Runs a full analysis pipeline across ALL imported MT5 symbols. Sector classification (Forex/Crypto/Indices/Commodities/Stocks), dual-metric outliers (VaR x ATR), per-sector IQR statistics, top 20 most extreme outliers by Z-score, and crypto risk tiers. One command gives you the complete risk landscape of your Darwinex universe.

`gatherScanSymbols()` unifies symbol collection from positions + watchlist + MT5 cache. All 6 scanner commands automatically include Darwinex data when available. The web explorers are legacy. The terminal scanners are live.

## Open Source: Why This Matters

Proprietary trading terminals are a tax on retail traders. Bloomberg charges institutional prices because institutions will pay. Godel charges subscriptions because traders are conditioned to accept recurring costs for essential tools. MetaTrader is "free" because MetaQuotes monetizes the ecosystem through broker partnerships and marketplace fees.

None of this is necessary. The APIs are public. The math is known. The rendering technology exists in every browser. The only reason trading terminals cost money is because nobody bothered to build the open-source alternative properly.

TyphooN-Terminal is **BSL (Business Source License)**. Use it commercially. Fork it. Modify it. Build your own trading infrastructure on top of it. The only thing you cannot do is close the source and pretend you invented it.

**73,100+ lines of Rust. 319 commits. 9 days. GUI + CLI + 298 commands + 39 indicators + 722 tests + 21 free APIs + 895-symbol MT5 sync + LAN sync + SEC EDGAR scraper + 50+ DARWIN analytics functions + Monte Carlo VaR + margin call simulator + 50K DARWIN radar screener.** One developer who got tired of paying rent on tools that should be free.

The terminal is open. The code is public. The Bloomberg tax is optional.

## The Competition: Every Trading Terminal for US Retail Traders (2026)

No terminal exists in a vacuum. Here is every serious option available to US retail traders and prop firm traders, what they cost, what they do, and where they fall short.

### MetaTrader 4 / MetaTrader 5

**Cost:** Free (broker-provided) | **Assets:** Forex, CFDs, futures, stocks (MT5) | **Algo:** MQL4/MQL5 Expert Advisors | **Platform:** Desktop (Windows), Web, Mobile

The industry standard for forex. MT5 adds multi-threaded backtesting and stock support. Both are proprietary (MetaQuotes), and US availability is severely restricted -- only OANDA and Forex.com offer MT4/MT5 to NFA-regulated accounts. MetaQuotes actively pushes brokers from MT4 to MT5. The MQL marketplace takes a cut of every indicator and EA sale. Your data lives on their servers.

**vs TyphooN-Terminal:** MT5 has a 20-year ecosystem. TyphooN-Terminal has open source, GPU charts, and no MetaQuotes gatekeeping. MT5 can't run on Linux without Wine. TyphooN-Terminal is native.

### TradingView

**Cost:** Free (limited) to $59.95/month (Premium) | **Assets:** Charts for everything; trading via broker integration | **Algo:** Pine Script indicators/alerts only -- no native execution | **Platform:** Web-based, Mobile, Desktop (Electron)

The most popular charting platform. Beautiful UI, massive community, 100M+ users. But it is NOT a trading terminal -- it is a charting platform with broker integrations bolted on. No native algo execution. Pine Script cannot place orders. Alerts can trigger webhooks to external bots, but that is a Rube Goldberg machine, not a trading system. The desktop app is an Electron wrapper (~200MB).

**vs TyphooN-Terminal:** TradingView has better social features and a larger indicator library. TyphooN-Terminal has native algo execution, GPU rendering (not a web canvas), and costs $0 forever. TradingView Premium costs $720/year for what should be free.

### Thinkorswim (Charles Schwab)

**Cost:** Free with Schwab account | **Assets:** Stocks, options, futures, forex, ETFs | **Algo:** thinkScript custom studies; limited automation (conditional orders) | **Platform:** Desktop (Java), Web, Mobile

Excellent options analysis. Inherited the TD Ameritrade platform, which was best-in-class for options Greeks and probability analysis. The desktop client is Java-based and can eat **2GB+ of RAM**. thinkScript is a custom language with no community outside Schwab. Automation is limited to conditional orders -- no true algo trading.

**vs TyphooN-Terminal:** Thinkorswim wins on options analysis depth and futures access. TyphooN-Terminal wins on resource usage (~50-100MB vs 2GB+), algo execution, and not being written in Java. Both are free.

### Interactive Brokers (TWS / IBKR)

**Cost:** Free platform; $0 stocks (Lite), $0.0035/share (Pro) | **Assets:** Everything -- 150+ markets, 200+ countries | **Algo:** Full API (Java, C++, C#, Python, REST). Built-in VWAP, TWAP | **Platform:** Desktop (Java), Web, Mobile

The gold standard for US retail traders who want global market access. Lowest margin rates in the industry. 120+ indicators. FIX protocol support. But the TWS desktop client is a Java application that looks like it was designed in 2005 and has not been significantly updated since. The learning curve is brutal. **$10/month inactivity fee** on accounts under $2K (Lite exempt).

**vs TyphooN-Terminal:** IBKR wins on market access (150+ markets vs Alpaca's US stocks/options/crypto). TyphooN-Terminal wins on UI/UX, GPU rendering, binary size (~15MB vs ~500MB+), and open source. If IBKR adds a broker trait to TyphooN-Terminal, the comparison changes entirely.

### TradeStation

**Cost:** $0 stocks/ETFs (up to 10K shares); $0.60/contract options; $1.50/contract futures | **Assets:** Stocks, options, futures, ETFs, crypto | **Algo:** EasyLanguage scripting -- the original retail algo language. 294 built-in indicators | **Platform:** Desktop, Web, Mobile

The largest indicator library of any retail platform (294). EasyLanguage has been the standard for retail algo development for 30+ years. Radar Screen for multi-symbol scanning. Matrix for futures ladder trading. 30+ years of historical data. **$10/month inactivity fee** (balance <$5K).

**vs TyphooN-Terminal:** TradeStation wins on historical data depth and EasyLanguage ecosystem maturity. TyphooN-Terminal wins on cost (no inactivity fee, no commissions via Alpaca), open source, and modern tech stack. TradeStation is the veteran; TyphooN-Terminal is the new challenger.

### NinjaTrader

**Cost:** Free (limited, $0.39/micro); Lease $720/year; Lifetime $1,099 | **Assets:** Futures, forex | **Algo:** NinjaScript (C#). Full automation. SuperDOM | **Platform:** Desktop only (Windows)

The industry standard for futures day trading. SuperDOM is unmatched for order flow. ATM (Advanced Trade Management) handles complex position management. Widely supported by prop firms (Topstep, Apex). Acquired by Kraken in 2025 -- crypto integration expected. **Windows only.** Free plan has a **$35/month inactivity fee** if you do not trade.

**vs TyphooN-Terminal:** NinjaTrader wins on futures execution and prop firm compatibility. TyphooN-Terminal wins on cost ($0 vs $720+/year), cross-platform potential (Rust/Tauri), and not being locked to Windows. NinjaTrader's C# ecosystem is mature; TyphooN-Terminal's Rust codebase is faster.

### Sierra Chart

**Cost:** $26-54/month | **Assets:** Futures, forex, crypto, commodities, stocks | **Algo:** C++ custom scripting. 300+ technical studies. DTC Protocol | **Platform:** Desktop only (Windows)

Lowest latency of any retail terminal. Best unfiltered historical data. Extremely lightweight. Preferred by professional order flow traders. The UI looks like Windows 98. The documentation reads like a PhD thesis. The C++ API is powerful but unforgiving. **Windows only.**

**vs TyphooN-Terminal:** Sierra Chart wins on raw latency and data quality. TyphooN-Terminal wins on UI/UX, cost ($0 vs $26-54/month), open source, and not looking like it was designed before Y2K.

### Quantower

**Cost:** Free tier; Full $70/month or $1,590 lifetime | **Assets:** Multi-broker (stocks, futures, forex, crypto) | **Algo:** C# API | **Platform:** Desktop (Windows)

Modern UI with strong footprint/delta tools. Multi-broker connectivity is the killer feature -- connect to Rithmic, CQG, Interactive Brokers, Binance, and more from one platform. Good order flow analysis. **Windows only.** Premium features are expensive.

**vs TyphooN-Terminal:** Quantower wins on multi-broker support. TyphooN-Terminal wins on cost and open source. Both have modern UIs. Quantower's C# API vs TyphooN-Terminal's Rust backend.

### cTrader

**Cost:** Free (broker-provided) | **Assets:** Forex, indices, commodities, crypto, stock CFDs | **Algo:** cBots in C#, free cloud hosting | **Platform:** Desktop, Web, Mobile

Modern forex platform with free cloud bot hosting (no VPS needed). 70+ indicators, 28 timeframes. Supported by 300+ brokers globally. **NOT available to US retail traders** due to CFD regulatory restrictions. Used by some prop firms (FTMO, FundedNext) but not for US-based traders.

**vs TyphooN-Terminal:** cTrader wins on forex ecosystem and free cloud hosting. TyphooN-Terminal wins on US availability and open source. cTrader is irrelevant for US retail traders.

### Godel Terminal

**Cost:** Free tier; $118/month standard (+$30 FINRA surcharge) | **Assets:** Stocks, options, forex, commodities, crypto | **Algo:** None -- research/data terminal only | **Platform:** Desktop (Mac, Windows)

Bloomberg-style CLI interface at 1/20th the price. 6-panel layout. 2x more news per ticker than competitors. Nasdaq data with unlimited history. **NOT a trading platform** -- no order execution. Research and data only. Still **$148/month** with FINRA surcharge.

**vs TyphooN-Terminal:** Godel wins on data depth (Nasdaq feed, institutional-grade news). TyphooN-Terminal wins on everything else -- trading execution, algo support, risk management, cost ($0 vs $148/month), and open source. TyphooN-Terminal's 288 commands directly target Godel's use case.

### Bloomberg Terminal

**Cost:** $31,980/year (single seat) | **Assets:** Everything | **Algo:** BLPAPI (C++, Java, .NET, Python) | **Platform:** Proprietary hardware + software

The gold standard for institutions. Unmatched data, analytics, news, messaging. **Effectively unavailable to retail traders.** $32K/year requires a sales relationship. Designed for hedge funds, banks, and asset managers. 6.5% annual price increases.

**vs TyphooN-Terminal:** Bloomberg wins on data comprehensiveness. TyphooN-Terminal wins on accessibility ($0 vs $32K), open source, and being usable by humans who do not work at Goldman Sachs.

### Webull

**Cost:** $0 commission stocks/ETFs/options | **Assets:** Stocks, options, ETFs, futures (micros), crypto | **Algo:** OpenAPI (REST, gRPC, MQTT) | **Platform:** Desktop, Web, Mobile

Commission-free with a modern mobile-first design. OpenAPI supports algo trading across all asset classes. AI assistant (Vega). Good for casual/mobile traders. Charting is limited compared to pro platforms.

**vs TyphooN-Terminal:** Webull wins on mobile experience and crypto variety. TyphooN-Terminal wins on desktop charting, indicator depth (39 NNFX indicators), risk management, and open source.

### tastytrade

**Cost:** $0 stocks; $1/contract options (to open), $0 to close (capped $10/leg) | **Assets:** Stocks, options, futures, futures options | **Algo:** REST API, Python SDK | **Platform:** Desktop, Web, Mobile

Options-focused platform with excellent Greeks/probability tools. Low options commissions. Clean modern UI. Full API access with typed Python SDK. No forex, no crypto.

**vs TyphooN-Terminal:** tastytrade wins on options analysis and futures options. TyphooN-Terminal wins on crypto support, risk management depth, and open source.

## US Prop Firms: Platform Requirements (2026)

If you trade with a prop firm, your terminal choice is dictated by the firm. Here is what is available to US traders:

| Firm | Status | US Platforms | Assets | Max Account | EA/Algo |
|---|---|---|---|---|---|
| **FTMO** | Active | DXtrade only (US) | Forex, indices, crypto | $200K | Yes (with limits) |
| **E8 Markets** | Active | TradeLocker, E8 Futures | Forex, crypto, futures | $500K | Yes |
| **Topstep** | Active | TopstepX, NinjaTrader, TradingView | Futures only | $150K | Yes |
| **Apex Trader Funding** | Active | NinjaTrader, Sierra Chart, Quantower, TradingView | Futures only | $300K | Yes |
| **FundedNext** | Active | MT4, MT5, cTrader (limited US) | Forex, futures | $300K+ | Yes |
| **MyFundedFX** | **DEAD** | Shut down Feb 2026 | N/A | N/A | N/A |
| **The Funded Trader** | **DEAD** | Delisted, declined payouts | N/A | N/A | N/A |
| **True Forex Funds** | **DEAD** | Shut down May 2024, owed $1.2M | N/A | N/A | N/A |

**Key insight for US prop firm traders:** Futures firms (Topstep, Apex) offer the most platform flexibility. Forex firms force US traders onto restricted platforms (DXtrade, TradeLocker) because MT4/MT5/cTrader are not available due to CFD regulations. Three major prop firms have died in the past 2 years -- do your due diligence.

## The Full Comparison Matrix

| Terminal | Cost | Open Source | Assets | Algo | GPU Charts | Binary Size | US Available |
|---|---|---|---|---|---|---|---|
| **TyphooN-Terminal** | **Free** | **Yes (BSL)** | Stocks, options, crypto + MT5 sync | **298 commands** | **Yes** | **~15MB** | **Yes** |
| MetaTrader 5 | Free | No | Forex, CFDs, stocks | MQL5 | No | ~50MB | Limited |
| TradingView | $0-60/mo | No | Charts only | Pine Script (no exec) | No (canvas) | ~200MB | Yes |
| Thinkorswim | Free | No | Stocks, options, futures | thinkScript (limited) | No | ~1GB+ | Yes |
| IBKR TWS | Free | No | Everything | Full API | No | ~500MB+ | Yes |
| TradeStation | $0+ fees | No | Stocks, options, futures | EasyLanguage | No | ~200MB | Yes |
| NinjaTrader | $0-1,099 | No | Futures, forex | NinjaScript (C#) | No | ~200MB | Yes (Win only) |
| Sierra Chart | $26-54/mo | No | Futures, forex | C++ | No | ~20MB | Yes (Win only) |
| Quantower | $0-70/mo | No | Multi-broker | C# API | No | ~100MB | Yes (Win only) |
| cTrader | Free | No | Forex, CFDs | cBots (C#) | No | ~100MB | **No (US blocked)** |
| Godel Terminal | $118+/mo | No | Research only | None | No | ~100MB | Yes |
| Bloomberg | $32K/yr | No | Everything | BLPAPI | No | Proprietary | Institutional |
| Webull | Free | No | Stocks, options, crypto | OpenAPI | No | ~150MB | Yes |
| tastytrade | Free | No | Stocks, options, futures | REST API | No | ~100MB | Yes |

**TyphooN-Terminal is the only open-source trading terminal with real brokerage integration, GPU-accelerated charts, direct MT5 database sync, built-in outlier scanners, and a built-in risk management engine.** Every other free option is either closed-source (Webull, IBKR Lite), web-based (TradingView), research-only (Godel free tier), or locked to Windows (NinjaTrader, Sierra Chart, Quantower).

-- TyphooN

---

> **DISCLAIMER:** TyphooN-Terminal is open-source software provided as-is under the BSL (Business Source License) license. It is NOT financial advice and NOT a recommendation to trade. Trading involves substantial risk of loss. The software executes orders as instructed -- it does not and cannot guarantee profitable outcomes. Use at your own risk. Test thoroughly in paper trading before risking real capital. The author actively trades using this software and holds positions mentioned in this blog. Prop firm information is current as of March 2026 and may change -- verify directly with each firm before funding an account.
