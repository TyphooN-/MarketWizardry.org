## TyphooN-Terminal: 44K Lines of Rust in 5 Days -- Building a Bloomberg Killer on Open Source

> **DISCLAIMER:** This is a technical post-mortem of a software development sprint. The author is not affiliated with Bloomberg, Godel Technologies, MetaQuotes, or any terminal vendor mentioned. Opinions on proprietary trading software are exactly that -- opinions formed after years of paying for tools that should have been open source from the start.

## Introduction: What If You Could Replace a $24K/Year Terminal in 5 Days?

Bloomberg Terminal costs **$24,000** per year. Godel Terminal costs **$80-118** per month. MetaTrader 5 is "free" in the same way that a roach motel is free -- you walk in, your data never walks out, and MetaQuotes owns the building.

TyphooN-Terminal shipped in **4.7 days**. March 15 to March 19, 2026. **218 commits**. **45,500 lines of code**. Approximately **46 commits per day**. A ~**12-15MB GUI binary** and a **6.5MB standalone CLI** that do what Bloomberg charges twenty-four grand a year for.

This is not a mockup. This is not a demo. This is a fully functional trading terminal with **288** Bloomberg-style commands, **39** indicators with exact MT5 visual parity, a complete port of the TyphooN v1.420 risk management engine, and enough research tools to make a sell-side analyst uncomfortable.

**Apache 2.0. Open source.** Because proprietary trading terminals are a racket and somebody needed to say it out loud by shipping the alternative.

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

In **4.7 days**, TyphooN-Terminal shipped with:

### 288 Bloomberg-Style Commands (Ctrl+K Palette)

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

## The Speed: 218 Commits in 4.7 Days

Let me contextualize what **46 commits per day** means.

A typical professional software team ships maybe **2-5** meaningful commits per developer per day. Senior engineers at FAANG companies might push **3-8**. A focused solo developer on a deadline might hit **10-15**.

Forty-six per day is not normal. It is the result of three factors:

1. **Architectural Clarity from Day One:** 33 Architecture Decision Records were written before and during development. Every major decision -- state management, IPC protocol, chart rendering pipeline, indicator calculation strategy -- was documented and decided before code was written. When you know where everything goes, you do not waste time refactoring.

2. **Rust's Compiler Is the QA Team:** When Rust code compiles, entire categories of bugs are already eliminated. No null pointer dereferences. No data races. No use-after-free. No buffer overflows. The time other languages spend debugging memory corruption, Rust spends at compile time. The result is that committed code actually works.

3. **Years of Domain Knowledge:** The risk management logic, the indicator math, the order management patterns -- none of this was invented during the sprint. It was ported. Porting known-correct logic to a better language is fundamentally faster than designing from scratch. The MQL5 EA has been battle-tested across six DARWINs and seven post-mortems. The math was proven. It just needed a better home.

**218 commits** is not a vanity metric. Every commit represents a testable, working increment. The repository went from zero to functional trading terminal in under five days because the architecture was right, the language was right, and the domain knowledge was already paid for in years of live trading.

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
- **Cost:** $0 (Apache 2.0)
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

**Multi-Broker Support:** Alpaca Markets is first. Interactive Brokers, Tradier, and additional brokers follow. Same risk engine, same interface, different execution venues.

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

**602/602 smoke tests pass.** The test suite covers command execution, indicator calculation accuracy, order type validation, API response parsing, cache coherence, and UI state transitions. Every commit runs the full suite. No exceptions.

## Open Source: Why This Matters

Proprietary trading terminals are a tax on retail traders. Bloomberg charges institutional prices because institutions will pay. Godel charges subscriptions because traders are conditioned to accept recurring costs for essential tools. MetaTrader is "free" because MetaQuotes monetizes the ecosystem through broker partnerships and marketplace fees.

None of this is necessary. The APIs are public. The math is known. The rendering technology exists in every browser. The only reason trading terminals cost money is because nobody bothered to build the open-source alternative properly.

TyphooN-Terminal is **Apache 2.0**. Use it commercially. Fork it. Modify it. Build your own trading infrastructure on top of it. The only thing you cannot do is close the source and pretend you invented it.

**45,500 lines of Rust. 218 commits. 4.7 days. GUI + CLI + 288 commands + 39 indicators + 602 tests + 21 free APIs.** One developer who got tired of paying rent on tools that should be free.

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
| **TyphooN-Terminal** | **Free** | **Yes (Apache 2.0)** | Stocks, options, crypto | **288 commands** | **Yes** | **~15MB** | **Yes** |
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

**TyphooN-Terminal is the only open-source trading terminal with real brokerage integration, GPU-accelerated charts, and a built-in risk management engine.** Every other free option is either closed-source (Webull, IBKR Lite), web-based (TradingView), research-only (Godel free tier), or locked to Windows (NinjaTrader, Sierra Chart, Quantower).

-- TyphooN

---

> **DISCLAIMER:** TyphooN-Terminal is open-source software provided as-is under the Apache 2.0 license. It is NOT financial advice and NOT a recommendation to trade. Trading involves substantial risk of loss. The software executes orders as instructed -- it does not and cannot guarantee profitable outcomes. Use at your own risk. Test thoroughly in paper trading before risking real capital. The author actively trades using this software and holds positions mentioned in this blog. Prop firm information is current as of March 2026 and may change -- verify directly with each firm before funding an account.
