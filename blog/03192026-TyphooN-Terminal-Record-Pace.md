## TyphooN-Terminal: 57K Lines of Pure Rust -- Building a Bloomberg Killer With Zero JavaScript

> **DISCLAIMER:** This is a technical post-mortem of a software development sprint. The author is not affiliated with Bloomberg, Godel Technologies, MetaQuotes, or any terminal vendor mentioned. Opinions on proprietary trading software are exactly that -- opinions formed after years of paying for tools that should have been open source from the start.

## Introduction: What If You Could Replace a $24K/Year Terminal in 5 Days?

Bloomberg Terminal costs **$24,000** per year. Godel Terminal costs **$80-118** per month. MetaTrader 5 is "free" in the same way that a roach motel is free -- you walk in, your data never walks out, and MetaQuotes owns the building.

TyphooN-Terminal started as a sprint -- first functional build in **4.7 days**, March 15 to March 20, 2026. Then the frontend was rebuilt. Twice. The final architecture -- **68,400 lines of pure Rust**, zero JavaScript, native GPU rendering via egui + wgpu -- is the result of **861 commits** and three complete rendering pipeline rewrites. The frontend was gutted and rebuilt because each iteration revealed that the bottleneck was the rendering architecture itself.

This is not a mockup. This is not a demo. This is a fully functional native GPU trading terminal with **60+** indicators (all computed on GPU), **70** drawing tools, **48** floating analytical windows, a complete port of the TyphooN v1.420 risk management engine, direct MT5 SQLite bar sync across multiple Darwinex accounts, and enough research tools to make a sell-side analyst uncomfortable.

**BSL (Business Source License). Open source.** Because proprietary trading terminals are a racket and somebody needed to say it out loud by shipping the alternative.

## The Backstory: Why Build a Terminal at All?

I run DARWINs on Darwinex — including **AJTK** (Automated Judicial Termination of Kapital), an active hedged martingale SOLUSD short managed by **TyphooN v1.429**. The EA handles TRIM, PROTECT, hedged martingale position management, and Monte Carlo simulation. 10 DARWINs died before AJTK. $134K of tuition paid for the correct firmware (v1.429) and correct voltage (Open MG $1.87).

**QRRP** — the Quad Rothschild Rug Pull — was the first step beyond pure discretionary trading into algo-assisted territory. The EA manages the position autonomously. TRIM builds net short exposure. PROTECT handles spread events. The operator's job is to not touch anything and let the flywheel compound.

But QRRP exposed the ceiling. MetaTrader 5 is a proprietary black box. MQL5 is a walled garden. You cannot run MT5 on Linux natively. You cannot integrate with Alpaca Markets. You cannot pull SEC EDGAR fundamentals, options chains with Greeks, congressional trading data, or dark pool volume into the same interface where you manage positions. MT5 does what MetaQuotes allows and nothing more.

The terminal I needed did not exist. Bloomberg has the data but costs more than most retail accounts. Godel has the interface but charges monthly for what should be a local binary. Every open-source alternative is either Electron bloatware burning **500MB** of RAM to render a candlestick chart, or a Python script with a Tkinter GUI that looks like it escaped from 2004.

So I built it.

## The Development Lifecycle: Three Frontends, One Lesson

The backend was always Rust. That decision took ten minutes and never changed. The frontend was rebuilt three times because each iteration revealed that the bottleneck was not the code -- it was the architecture.

### Iteration 1: Tauri + CPU Canvas (Days 1-5)

The first build used **Tauri 2.0** with a vanilla JS frontend rendering charts on HTML5 Canvas. No React. No framework. Just DOM manipulation and `ctx.fillRect()` for every candlestick. It shipped fast and proved the feature set: 288 commands, indicators, order management, risk engine.

**What worked:** Tauri's ~15MB binary vs Electron's 200MB. System webview instead of bundled Chromium. The Rust backend was fast. The IPC bridge was tolerable.

**What broke:** CPU canvas rendering collapsed above 5,000 bars with indicators active. Every pan, every zoom, every new bar required the CPU to repaint thousands of rectangles. The chart stuttered. The UI froze during data loads. Canvas is not a rendering engine -- it is a drawing API pretending to be one.

### Iteration 2: Tauri + WebGL2 GPU Charts + WASM Indicators (Days 5-20)

The canvas was replaced with a custom **WebGL2** rendering pipeline. Candlestick bodies became GPU quads (2 triangles each). Indicator lines became GL_LINE_STRIP calls. Drawing tools became GPU geometry. A **WASM indicator engine** moved the heaviest math off the main thread into Web Workers running compiled Rust at near-native speed.

**The codebase peaked at ~73,000 lines** -- 40,000+ lines of JavaScript, 32KB of WASM indicator modules, and the Rust backend.

**What worked:** GPU rendering was fast. 10,000 bars at 60fps with 39 indicators. The WebGL2 pipeline proved that GPU chart rendering is the correct architecture.

**What broke:** The IPC bridge. Every piece of data -- bar arrays, indicator results, position updates, quotes -- had to be serialized to JSON in Rust, sent over the Tauri IPC bridge, deserialized in JavaScript, and then fed to the WebGL2 renderer. The serialization overhead dominated. A 50,000-bar dataset spent more time in `JSON.parse()` than in the actual rendering. WebKitGTK on Linux added its own overhead -- layout reflows, garbage collection pauses, compositor delays. The webview was the bottleneck, not the chart engine.

### Iteration 3: Native Rust GPU (egui + wgpu) — Zero JavaScript (Days 20+)

The entire JavaScript/WebKit/Tauri frontend was deleted. **40,000 lines of JS, gone.** The WASM chart engine -- gone. The IPC bridge -- gone. Every byte of functionality was rebuilt in pure Rust with **egui** (immediate-mode GUI) and **wgpu** (Vulkan/Metal/DX12).

**The codebase dropped from 73,000 to 38,662 lines** initially -- all Rust, zero JavaScript. The same features in half the code because there is no serialization layer, no bridge, no framework abstraction. Since then, continued development has grown the codebase to **68,400 lines** across **861 commits** and **7 crates**.

**What works:** Everything. Data flows from Rust structs directly to GPU buffers. No JSON. No IPC. No garbage collector. The indicator engine runs on **GPU compute shaders** (WGSL) -- bar data lives in VRAM and never touches the CPU for computation. The UI renders at monitor refresh rate via adaptive vsync and drops to 0fps when idle.

**The current architecture:**

| Crate | Purpose | Lines of Rust |
|---|---|---|
| **engine/** | Broker APIs (Alpaca, tastytrade, Kraken), SQLite cache, indicators, DARWIN analytics, SEC scraper, risk engine | ~25,800 |
| **native/** | egui + wgpu native GPU application, all UI, GPU compute shaders, 110+ floating windows | ~35,300 |
| **cli/** | Standalone TUI (ratatui, SSH-ready, 6.5MB binary) | ~2,300 |
| **mql5-compiler/** | pest parser → AST → IR → WGSL codegen for custom MQL5/PineScript indicators | ~4,500 |
| **web/** | eframe + glow WASM thin client for phone/browser access | ~400 |
| **web-protocol/** | Shared WebCmd/WebMsg serializable types | ~90 |
| **web-server/** | axum HTTPS + WebSocket relay with self-signed TLS | ~110 |
| **Total** | **100% Rust. Zero JavaScript. Phone access via WASM.** | **~68,400** |

### Why Rust Won (And Why Everything Else Still Loses)

**Electron:** Ships a 200MB Chromium instance per application. Uses 500MB of RAM to display a chart. TyphooN-Terminal tried the Tauri variant of this approach -- system webview instead of bundled Chromium -- and even that was too much overhead. If the lightest possible webview (Tauri) is the bottleneck, Electron never had a chance.

**Python/Qt:** Python's GIL makes real-time charting a threading nightmare. Qt licensing is a minefield. Neither produces binaries under 50MB.

**C++/Qt:** Fast, but C++ memory management in a trading terminal is asking for use-after-free bugs in production where use-after-free means "your order got duplicated and you are now 2x leveraged by accident."

**The lesson from three rebuilds:** The only architecture that works for a real-time trading terminal is compiled native code rendering directly to the GPU with zero intermediary layers. No webview. No bridge. No serialization. Rust + egui + wgpu is that architecture. Everything else adds overhead that compounds under load until the terminal stutters at exactly the moment you need it most.

## What Was Built: The Numbers

In **6 days**, TyphooN-Terminal shipped with:

### 298 Bloomberg-Style Commands (Ctrl+K Palette)

Every function accessible via keyboard. Type what you want, hit enter. No menu diving. No mouse hunting. Bloomberg proved this UX pattern works for professional traders thirty years ago. Everyone else ignored it.

### 60+ Indicators with Exact MT5 Visual Parity

- Moving averages (SMA, EMA, KAMA, WMA, HMA), Bollinger Bands, Keltner Channels, Donchian Channels, ATR, RSI, MACD, Stochastic, Ichimoku, ADX, Supertrend, Fisher Transform, Squeeze Momentum, VWAP with deviation bands, OBV, BetterVolume, Supply/Demand zones, pivot points, fractals, auto-Fibonacci levels, and 5+ Ehlers indicators (Super Smoother, Decycler, MAMA/FAMA, Cyber Cycle, Roofing Filter).
- All computed on GPU via the native Rust engine. No WebAssembly. No JavaScript fallback. Direct GPU compute.

### 70 GPU-Rendered Drawing Tools

- Fibonacci retracements, extensions, channels, arcs, time zones, wedge, circle, spiral
- Andrew's Pitchfork, Schiff, Modified Schiff, Inside Pitchfork
- Elliott Wave markup, XABCD Harmonic patterns, Head & Shoulders
- Gann fans and boxes
- Linear regression channels, trend channels, speed resistance fan/arc
- Measurement tools: ruler, date range, price range, risk/reward box
- Annotations: text labels, price labels, callouts, anchor notes, signposts
- Freehand drawing: brush, polyline, arc, Bezier curve, path
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

3. **Years of Domain Knowledge:** The risk management logic, the indicator math, the order management patterns -- none of this was invented during the sprint. It was ported. Porting known-correct logic to a better language is fundamentally faster than designing from scratch. The MQL5 EA has been battle-tested across multiple DARWINs and ten post-mortems. The math was proven. It just needed a better home.

**861 commits** is not a vanity metric. Every commit represents a testable, working increment. The repository went from zero to functional trading terminal in six days because the architecture was right, the language was right, and the domain knowledge was already paid for in years of live trading.

## Security: 21-Pass Audit, 97 Findings, 91 Fixed

A trading terminal handles API keys, account credentials, and order execution. Security is not a feature. It is a prerequisite.

TyphooN-Terminal underwent a **21-pass** security audit before release:

- **97** total findings identified
- **91** fixed and verified
- **6** accepted as low-risk with documented mitigations

**Key Security Measures:**
- **AES-256-GCM** encryption for all stored credentials and API keys
- Credential storage uses OS-native keychains (system keyring)
- Zero bare `unwrap()` in production code — all fallible calls use safe alternatives
- Constant-time HMAC comparison in LAN sync authentication
- Discord webhook URL validation (SSRF prevention)
- Bounded log buffer (500 entries, prevents memory leak)
- No dynamic code execution — pure compiled Rust, no eval, no scripting engine

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

The six manual DARWINs on Darwinex taught position management. QRRP taught cascading automation. The v1.420 EA proved that algorithmic risk management outperforms human discretion every single time (ten post-mortems confirm this empirically).

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

**The QRRP cascade doesn't need seven monitors and a GUI.** It needs TRIM 54.2%, a SOL price feed, and a terminal that can execute. The CLI is that terminal. 6.5MB. Runs anywhere. Trades everything Alpaca offers.

## Performance Optimization Deep Dive

Raw feature count means nothing if the terminal stutters under load. TyphooN-Terminal went through aggressive performance optimization passes that eliminated every bottleneck I could find.

**SQLite Statement Caching:** Every prepared statement is cached after first compilation. Repeated queries -- position lookups, indicator data reads, watchlist refreshes -- hit the statement cache instead of re-parsing SQL. This alone cut database interaction latency by 40-60% on hot paths.

**HTTP Connection Pooling:** Alpaca's API, SEC EDGAR, options data, crypto feeds -- the terminal talks to 21 data sources. Without connection pooling, every request opens a new TCP connection and negotiates a new TLS handshake. With pooling, persistent connections are reused across requests. Latency on sequential API calls dropped from ~200ms to ~30ms per request after the initial handshake.

**Immediate-Mode Rendering:** egui rebuilds the UI from scratch every frame — there is no retained widget tree, no stale state, no "update propagation" bugs. When a position's P&L changes, the next frame reflects it automatically. No explicit invalidation. No delta tracking. The data IS the UI.

**Background Thread Isolation:** Heavy operations (DARWIN analytics, SEC scraping, broker API calls, bar fetches) run on background threads via `tokio`. The UI thread never blocks. A `try_lock` pattern on shared data means the UI renders the last known state while the background computes the next. Zero freezes. Zero spinners.

**Dashboard Panel Management:** Multiple floating windows coexist without fighting for viewport space. egui handles z-ordering natively. Panel state (open/closed/position/size) persists across sessions.

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

**Double-Write Elimination:** Bar data is persisted during the merge operation in the engine. The in-memory cache is updated directly from the same Rust structs — no redundant serialization or recompression. This eliminated duplicate zstd level-9 recompression on every bar fetch.

**Measured result across 3 benchmark runs:**

| Scenario | Before | After | Speedup |
|---|---|---|---|
| BTC/USD 1Hour cold | 2.5+ hours | 33-131s | 70-270x |
| SOL/USD 4Hour cold | 2+ hours | 47-163s | 45-150x |
| Full MTF grid + prefetch | 3-4 hours | ~3 min | 60-80x |
| Warm start (cached) | 30s | **instant** | infinite |

## Four-Tier Cache Architecture

Every piece of market data flows through a four-tier cache before hitting the network. Each tier trades latency for capacity.

**Tier 1 -- Memory LRU (~0ms):** The fastest cache. Recently accessed bar data, quotes, and indicator results live in an in-memory LRU (Least Recently Used) cache backed by `HashMap`. Cache hits are effectively instant. The LRU eviction policy ensures frequently accessed symbols stay hot while rarely viewed symbols get pushed to lower tiers.

**Tier 2 -- KV Cache (~1-5ms):** A key-value store in SQLite for session state, DARWIN analytics, LAN sync data, and frequently accessed metadata. Faster than full bar queries because values are pre-computed and stored as simple key-value pairs.

**Tier 3 -- SQLite + zstd Compression (~20-50ms):** The persistent cache. All bar data lands in SQLite, compressed with Zstandard. Dual-connection architecture (separate read + write connections) eliminates "database is locked" errors. The zstd compression achieves **15-30x** compression ratios on bar data because OHLCV data is highly regular and compresses exceptionally well.

**Tier 4 -- External APIs (~100-500ms):** Alpaca, Kraken, CryptoCompare, tastytrade, MT5 SQLite sync. Data fetched from external sources flows through the sanity filter (reject negative/zero/NaN/high<low bars), gets merged into Tier 3, and populates Tier 1 on access.

**Binary Format:** Each bar is stored in a fixed **48-byte** binary format (timestamp + OHLCV as f64). No JSON parsing. No CSV splitting. No string-to-float conversions on read. Raw binary in, raw binary out. This format is what enables the 15-30x compression ratios -- zstd compresses regular binary patterns far better than it compresses text.

**Background Prefetch:** When the user views a chart for AAPL on H4, the terminal silently prefetches M15, H1, D1, and W1 data for AAPL in the background. By the time the user switches timeframes, the data is already cached. This makes timeframe switching feel instant even though the underlying API calls take seconds.

## GPU Chart Engine: Five Phases, All Complete

The chart engine was built in five distinct phases, each adding a layer of capability. All five are complete.

**Phase 1 -- Canvas Foundation:** Basic candlestick rendering on HTML5 Canvas. Price scale, time axis, scrolling. This was the "it works" phase -- functional but CPU-bound and limited to a few hundred bars before frame drops became noticeable.

**Phase 2 -- WebGL2 Migration:** The entire rendering pipeline moved to WebGL2. Candlestick bodies are rendered as **2 triangles** (a quad) per body. Wicks are **2 lines** per candle (high-to-body, body-to-low). Vertex shaders handle the coordinate transforms. The GPU does what GPUs are designed for -- rendering thousands of geometric primitives in parallel.

**Phase 3 -- Indicator Overlays:** All 60+ indicators render through the native GPU pipeline via egui + wgpu. Line-based indicators (SMA, EMA, KAMA) are GPU draw calls. Histogram indicators (MACD, Volume) are instanced quads. Bands (Bollinger, Keltner) are filled polygons with alpha blending. Every indicator renders on the GPU alongside the candlesticks.

**Phase 4 -- Drawing Tools:** All **70 drawing tools** render through the native GPU pipeline. Fibonacci levels, pitchforks, harmonic patterns, Gann fans, regression channels -- all GPU-rendered geometry. Interactive handles for dragging and resizing are hit-tested in Rust. Drawing tools do not degrade chart performance because they are just more vertices in the same render pass.

**Phase 5 -- Polish and Performance:** Crosshair rendering, tooltip overlays, smooth pan/zoom with momentum, price scale auto-ranging, and the final performance pass. The engine renders **10,000+ bars at 60fps** with multiple indicators and drawing tools active simultaneously.

The GPU chart engine is why TyphooN-Terminal can display a 4K chart with 60+ indicators and 15 Fibonacci levels without dropping a frame. CPU-based canvas rendering (TradingView, most Electron apps) cannot do this. The GPU can.

**Draggable Panel Splitter:** The chart and sidebar panels resize by dragging the divider between them. Layout proportions persist across sessions. This sounds like a small thing until you realize NinjaTrader has fixed panel widths and TradingView charges for customizable layouts. In TyphooN-Terminal it is a drag handler in egui. Open source means features like this take minutes, not feature request tickets.

## GPU Indicator Engine (Replaced WASM)

The Tauri-era WASM indicator engine (32KB binary, Web Workers, JS fallback) was deleted alongside the entire JavaScript frontend. Every indicator now runs on **GPU compute shaders** via wgpu.

All 60+ indicators are compiled to WGSL (WebGPU Shading Language) and dispatched on the GPU with 256 threads per workgroup. Bar data lives in VRAM. Indicator computation happens in parallel on the GPU — SMA, EMA, RSI, KAMA, Bollinger, ATR, MACD, Fisher, Stochastic, ADX, Ichimoku, and the full Ehlers DSP suite all run as GPU compute pipelines. Zero CPU indicator computation remaining.

**Performance:** GPU compute makes the old WASM vs JavaScript comparison irrelevant. The bottleneck is now the GPU upload (microseconds for typical datasets), not the computation. 10,000 bars with 39 indicators renders in a single frame. The GPU Strategy Optimizer performs parameter grid search across hundreds of combinations in parallel — what took 500ms in JavaScript and 5-10ms in WASM takes under 1ms on the GPU.

**10 adjustable parameters** (SMA, EMA, RSI, ATR, BB, Stochastic, ADX, Fisher, Momentum periods) are configurable per-chart via DragValue sliders. Changes trigger immediate GPU recompute. No restart needed.

## Bug Fixes and Reliability

Shipping fast means nothing if the software crashes in production. TyphooN-Terminal has **602 smoke tests** and every single one passes.

**15 NaN Bugs Fixed:** Floating-point NaN (Not a Number) is the silent killer of trading software. A single NaN in an indicator buffer propagates through every downstream calculation, turning charts into empty panels and risk calculations into nonsense. All 15 NaN sources were identified and fixed:
- Division by zero in ATR when bar range is zero (flat candles)
- Log of zero in Fisher Transform on the first few bars
- Square root of negative numbers in standard deviation on single-bar windows
- NaN propagation through indicator chains (e.g., KAMA feeding into Fisher)

**Race Condition Guards (ADR-024):** Architecture Decision Record 024 documents **7 cross-symbol race conditions** that were identified and fixed. These occur when multiple symbols fetch data simultaneously and indicator calculations for Symbol A accidentally read incomplete data from Symbol B's buffer. The fix: each symbol gets its own isolated calculation context with atomic state transitions. No shared mutable state between symbol pipelines.

**429 Rate Limit Stale Data Fix:** When Alpaca returned HTTP 429 during a data fetch, the old code path would silently return stale cached data without marking it as stale. The user would see prices from hours or days ago with no indication that the data was outdated. Fixed: stale data is now visually flagged in the UI, and a background retry ensures fresh data replaces it as soon as the rate limit window expires.

**Arc Cache Lock Contention Fix:** The SQLite cache uses `Arc<SqliteCache>` with dual read/write connections. Heavy operations (API fetch, merge_bars, zstd compression) run on background threads with `try_lock`. The UI thread never waits for a database operation. This is the difference between "the app freezes when loading charts" and "charts load in the background while you trade."

**Dual-Layer Bar Sanitization:** Bad data from APIs is caught at two boundaries. The Rust backend rejects bars with zero/NaN prices, fixes OHLC inconsistency (`true_high = max(o,h,l,c)`), and drops malformed timestamps at parse time. The JavaScript frontend runs `sanitizeBars()` before every chart render — removing duplicates, sorting by time, clamping negative volume. The dual-layer approach means zero chart artifacts even when Alpaca returns malformed crypto bars (which it does, occasionally).

**602/602 smoke tests pass.** The test suite covers command execution, indicator calculation accuracy, order type validation, API response parsing, cache coherence, and UI state transitions. Every commit runs the full suite. No exceptions.

## MT5 Direct SQLite Sync: Zero-Copy Bar Data From Every Darwinex Account

The original MT5 integration used CSV exports. Export from MetaTrader, parse in Rust, store in SQLite. Three steps, file I/O overhead, and manual intervention every time you wanted fresh data. That pipeline is dead.

TyphooN-Terminal now reads MT5's SQLite database **directly**. A custom MQL5 Expert Advisor (**BarCacheWriter.mq5**) writes OHLCV bars to a shared SQLite database in WAL mode. The Rust backend reads the same database file -- zero CSV parsing, zero file I/O intermediary, zero manual export steps. BarCacheWriter writes. TyphooN-Terminal reads. Same database. Different processes. WAL mode handles the concurrency.

**Multi-Instance Sync Across All Darwinex Accounts**

Running multiple DARWINs means running multiple MT5 instances -- Futures, Crypto, CFD, Stocks/ETFs. Each instance has its own BarCacheWriter database. `find_all_mt5_sqlite_dbs()` discovers every `typhoon_mt5_cache.db` across all `.mt5_*` instance directories and merges them into the terminal's unified cache. Each Darwinex account type contributes unique symbols. No conflicts. No duplicates. One sync command pulls **895 symbols** across all accounts simultaneously.

**Symbol Normalization:** MT5 names like `SOLUSD`, `EURUSD`, `XAUUSD` are normalized at every import boundary -- `SOL/USD`, `EUR/USD`, `XAU/USD`. Crypto, forex, metals all get slash-separated pairs. Indices like `US30` and `DE40` stay as-is. The terminal speaks the same symbol language as Alpaca regardless of where the data originated.

**Live Sync Progress UI:** The sync window shows real-time progress with per-category status bars -- Forex, Crypto, Commodities, Indices, Healthcare, Technology, and more. Each category displays complete, partial, and pending counts. The sync runs continuously with live updates instead of one-shot import. Green bars fill as symbols sync. The UI never freezes because all heavy operations run on `spawn_blocking` threads with `try_lock` patterns on shared state.

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

**MT5 as Master Data Source (ADR-037):** MT5 is now the authoritative data source for every symbol it covers. No more merge complexity between MT5 and Alpaca -- if MT5 has the symbol, MT5 wins. The deepest history always takes priority. Alpaca is the fallback for symbols MT5 does not have. The bar loader uses a 5-second rapid dedup window instead of per-timeframe staleness checks (which could defer up to 7 days), ensuring the MT5-first logic always runs. When background MT5 sync imports new bars, the in-memory cache is invalidated and the chart reloads automatically — no manual refresh needed.

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

**Live Backfill Grid:** Real-time status grid showing per-symbol per-timeframe completion. Each cell updates live as progress events fire for every completed fetch -- `✓` synced, `+` new data, `⟳` fetching, `⏳` pending, `✗` error. Hover tooltips show bar count and estimated percentage (e.g., "19,732 bars (99% est)"). Auto-retry loops until all combos are synced (max 10 passes), with 15s backoff on rate limits and a stop button to cancel mid-backfill.

**Quake Console Toggle:** Backtick (`` ` ``) and tilde (`~`) toggle the command bar -- tap to focus and select all, tap again to dismiss. The same muscle memory as opening the Quake console. Capture phase handler prevents the character from typing into the input.

**Weekend Auto-Poll:** The terminal detects when you are viewing a crypto symbol on a weekend (Friday 22:00 – Sunday 22:00 UTC) and automatically polls Kraken every 30 seconds. The chart cache invalidates and reloads with fresh data. Crypto charts stay live on weekends without manual intervention. Weekend candles render with a **blue tint** to visually distinguish Kraken-sourced bars from MT5 weekday bars -- you always know which data source painted each candle. A "Kraken (weekend)" badge appears in the chart header during off-hours.

**Bid/Ask Price Lines:** Green dashed line for bid, red dashed for ask, updated every 10 seconds from MT5 quotes. Works on all chart types including the MTF Grid. The spread is visible at a glance on every chart.

**DARWIN Quote Charting:** Type any DARWIN ticker (e.g., `HAKR`) in the symbol bar to chart it. The terminal fetches synthetic OHLC from FTP RETURN data and renders it as a standard candlestick chart. Transparent fallthrough to normal chart loading if the ticker is not a DARWIN.

**Auto-Reimport DARWIN XLSX:** A file watcher monitors `~/mt5xml/` for modified XLSX files and reimports them automatically every 60 seconds. Drop a fresh Darwinex trade history export into the folder and the terminal picks it up without any manual import step.

The crypto data gap is closed. Thirteen years of continuous crypto history across all 9 timeframes, weekends included. Binance was the original implementation but was replaced with Kraken due to US geo-blocking restrictions.

## DARWIN Import Pipeline: XLSX Trade History to Portfolio Analytics

Six DARWINs means six separate Darwinex accounts, each with its own trade history. Darwinex exports trade history as XLSX spreadsheets. TyphooN-Terminal now ingests those spreadsheets directly.

**core/darwin.rs** (1,178 lines of new Rust) parses XLSX files via the `calamine` crate, extracts every deal, stores them in SQLite, and reconstructs open positions using volume-balance detection. The entire deal history for all multiple DARWINs lives in the terminal's database with dedicated SQLite connections -- no contention with the MT5 sync pipeline.

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

All charts render natively via egui_plot for consistent line/area visualization across the dashboard.

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

Twelve indicator fixes across GPU and CPU fallback paths: EMA SMA bootstrap, KAMA seed, Fisher median+window, MACD signal, DEMA, Bollinger NaN handling, ATR initial value, minBars enforcement, Ichimoku Chikou, BetterVolume 2-bar, Alligator shift, ForceIndex. Every indicator produces identical output between GPU and CPU paths.

**Multi-Symbol MTF Grid:** The grid supports multiple symbols simultaneously. View CC+SLV across H4+D1+MN1 in a single grid. GPU-first rendering. Sequential grid cell loading keeps the UI responsive during heavy multi-symbol loads.

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

**GPU Histogram and Fill Rendering:** Volume bars, MACD histograms, and Bollinger Band fills are GPU-rendered geometry — instanced quads and filled polygons with alpha blending.

**10x Timestamp Parser:** The bar timestamp parser was rewritten for direct integer parsing instead of Date object construction. On a 50,000-bar dataset, this alone saves hundreds of milliseconds per load.

**Adaptive Vsync Render Loop:** The chart renders at monitor refresh rate when the viewport is changing (scroll, zoom, new data) and drops to 0fps when idle. No wasted GPU cycles on a static chart.

**Background Thread Grid Computation:** MTF Grid cells compute indicators on background threads via `tokio::spawn_blocking`. Parallel prefetch loads adjacent cells while the current one renders.

**Binary Search Data Clipping, O(1) Crosshair Lookup:** Visible bar range is found via binary search instead of linear scan. Crosshair price lookup uses a `HashMap` instead of array iteration.

**Session State Batching, Adaptive Vsync:** Session state writes are batched to prevent per-keystroke disk I/O. The render loop runs at monitor refresh rate when the UI is changing and drops to **0fps when idle** — zero GPU cycles on a static chart.

## MQL5 Compiler: Parse MQL5, Generate WASM

A new `mql5_compiler` crate parses MQL5 source code and compiles it to WebAssembly. The pipeline: **pest parser → AST → IR → WASM codegen**. The `COMPILE` command in the Ctrl+K palette triggers compilation from within the terminal. This is the foundation for running custom MQL5 indicators natively in the terminal without MetaTrader — write once in MQL5, compile to WASM, execute at near-native speed alongside the existing 39 indicators.

## Native Rust GPU Renderer: The Architecture Every Other Terminal Got Wrong

Every trading terminal on the market makes the same mistake. TradingView is an Electron wrapper around lightweight-charts -- a JavaScript canvas library running inside Chromium. NinjaTrader is C# with GDI+ software rendering. Thinkorswim is Java Swing. Sierra Chart is Win32 GDI. Even the "modern" terminals like Quantower and Godel are CPU-rendered desktop apps with web-tech charting layers bolted on.

The rendering pipeline in every one of these terminals:

```
Market Data → JSON/String parsing → CPU indicator math → CPU canvas drawing → compositor → pixels
```

Every step is CPU-bound. Every step contends with the UI thread. Every step adds latency between data arrival and pixel output. This is why TradingView stutters with 10 indicators on a 4K display. This is why Thinkorswim eats 2GB of RAM. This is why NinjaTrader freezes during data replay.

**TyphooN-Terminal v2 eliminated the entire legacy pipeline.** The JavaScript/WebKit/Tauri frontend was deleted -- **40,000 lines of JS, gone.** The WebGL2 WASM chart engine -- gone. lightweight-charts -- never used it, but the point stands: every library that renders charts through a browser engine is doing it wrong.

The new pipeline:

```
Market Data → Rust structs (zero-copy) → GPU compute shaders → wgpu render pipeline → pixels
```

**Zero JavaScript.** No V8. No garbage collector. No JSON serialization between backend and frontend because there is no frontend -- it is all one Rust binary.

**Zero WebKit.** No system webview. No Chromium. No DOM. No CSS layout engine computing where a candlestick body should appear. The terminal is a native window with GPU-rendered pixels via **wgpu** (Vulkan/Metal/DX12).

**Zero IPC.** Tauri's architecture required serializing every piece of data to JSON, sending it over an IPC bridge, deserializing it in JavaScript, then rendering it in a webview. That entire serialization layer is eliminated. Rust structs flow directly from the SQLite cache to GPU buffers.

**Zero canvas.** No HTML5 Canvas. No `ctx.fillRect()` called 10,000 times per frame. Candlestick bodies are GPU quads. Indicator lines are GPU line strips. The GPU does what GPUs are designed for -- rendering thousands of geometric primitives in parallel -- while the CPU handles data and computation.

**GPU Compute Shaders:** **100% GPU indicator coverage.** Every indicator runs on the GPU via WGSL compute shaders -- SMA, EMA, RSI, KAMA, Bollinger Bands, ATR, MACD, Fisher Transform, Stochastic, ADX, WMA, CCI, Williams %R, OBV, Momentum, Parabolic SAR, Ichimoku, Fractals, and the complete Ehlers DSP suite (Super Smoother, Decycler, ITL, MAMA/FAMA, EBSW, Cyber Cycle, CG, Roofing Filter). Full OHLC data uploads to VRAM. Parallel indicators use 256 threads per workgroup. Zero CPU indicator computation remaining.

**GPU Backtest Engine:** The strategy backtester runs entirely on GPU compute shaders. Monte Carlo VaR simulation with robustness scoring evaluates strategy performance across thousands of randomized paths. The GPU Strategy Optimizer performs parameter grid search with results visualization -- testing hundreds of parameter combinations in parallel instead of sequentially on the CPU.

The architecture:
- `engine/` -- pure Rust library, zero framework dependency. Broker APIs, data cache, indicators, DARWIN analytics, SEC scraper, risk engine. Reusable by any frontend.
- `native/` -- egui + wgpu native GPU application. The entire UI rendered at monitor refresh rate via adaptive vsync. 0fps when idle.
- `mql5_compiler/` -- pest parser → AST → IR → WASM codegen for custom MQL5 indicators.

### Why egui: Immediate Mode GUI on the GPU

**egui** is an immediate-mode GUI library written in pure Rust. "Immediate mode" means the UI is rebuilt from scratch every frame -- there is no retained widget tree, no layout cache, no stale state. Every frame, the code says "draw a button here, a chart there, a table here" and the GPU renders it. If the data changed, the next frame reflects it automatically. There is no `setState()`, no `invalidate()`, no "why isn't my widget updating" debugging.

This is the opposite of how every traditional GUI works. Qt, GTK, WinForms, Swing, Electron/React -- they all maintain a retained widget tree. You create widgets, attach them to a hierarchy, bind data to them, and then pray that the update propagation works correctly. Retained mode GUIs are complex because state synchronization between data and widgets is an unsolved problem. React exists because the DOM's retained model is so painful that Facebook built an entire abstraction layer to pretend it is immediate mode (virtual DOM diffing).

egui skips all of that. The widget IS the render call. The data IS the frame. No virtual DOM. No diffing. No reconciliation. No stale widget pointing at deallocated data. The entire UI is a function: `fn ui(data) → pixels`. Every frame. At 60fps. On the GPU.

**Why this matters for a trading terminal:**

- **Real-time data is immediate by nature.** Prices tick every millisecond. Positions change. Indicators recalculate. A retained GUI fights this -- you update the data, then chase down every widget that needs to know. An immediate GUI renders the current truth every frame. The data IS the UI. There is nothing to synchronize.

- **No layout engine overhead.** CSS Flexbox computation, DOM reflow, paint invalidation rectangles -- all of that is CPU work that happens before a single pixel is drawn. egui computes layout inline during the render pass. The layout IS the rendering. One pass. Zero reflow.

- **GPU-native from the ground up.** egui outputs a mesh of textured triangles. wgpu uploads that mesh to the GPU and renders it in a single draw call. Panels, buttons, text, charts -- everything is triangles on the GPU. The same GPU that renders Cyberpunk 2077 is rendering your candlestick chart. It is not even trying.

- **Adaptive vsync.** The render loop runs at monitor refresh rate (60/120/144hz) when the UI is changing and drops to **0fps when idle**. A static chart with no interaction consumes zero GPU cycles. TradingView's requestAnimationFrame loop runs at 60fps whether anything changed or not.

- **Background thread isolation.** Heavy operations (DARWIN analytics queries, SEC scraping, broker API calls) run on background threads via `tokio`. The UI thread never blocks. A `try_lock` pattern on shared data means the UI renders the last known state while the background thread computes the next state. Zero freezes. Zero spinners. The terminal never says "loading" -- it shows what it has and updates when more arrives.

### wgpu: Vulkan/Metal/DX12 Without the Pain

**wgpu** is Rust's GPU abstraction layer -- the same API used by Firefox's WebGPU implementation. It compiles to Vulkan on Linux, Metal on macOS, and DX12 on Windows. One codebase. Three GPU backends. Native performance on every platform.

The chart rendering pipeline:
1. Bar data arrives from SQLite (binary, zero-copy)
2. Indicator computation runs on 10 GPU compute shaders (SMA, EMA, RSI, KAMA, BB, ATR, MACD, Fisher, Stoch, ADX in VRAM)
3. egui builds the UI mesh (panels, text, widgets)
4. Custom chart rendering adds candlesticks, indicators, drawings as GPU geometry
5. wgpu submits one render pass to the GPU
6. Pixels appear on screen

**Total CPU involvement: data loading and egui layout.** Everything else is GPU. This is why the terminal can render a 4K chart with 32+ indicators, 7 harmonic patterns, supply/demand zones, pivot points, fractals, and Fibonacci levels simultaneously without dropping a frame. The GPU does not care. It was built for this.

This is what TradingView would be if it were built by someone who understood that a browser is not a rendering engine. This is what Bloomberg Terminal would be if it were built in 2026 instead of 1982. **The rendering pipeline that every other terminal got wrong, done right.**

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
- **10 GPU Compute Shaders:** SMA, EMA, RSI, KAMA, Bollinger, ATR, MACD, Fisher, Stochastic, ADX -- all in VRAM via wgpu compute pipelines
- **Bookmap Depth Heatmap:** volume-at-price visualization constructed from bar data -- institutional order flow analysis without a Level 2 subscription
- **Order Flow Visualization:** trade flow analysis rendered natively in the GPU pipeline
- **Trade Journal:** persistent trade journal window with session save/restore
- **37 GPU Compute Shaders (~98% coverage):** ATR Projection, BetterVolume, and S/D Zones added to the GPU pipeline. Nearly every indicator now runs on WGSL compute shaders
- **Indicator Alert Engine:** configurable alerts when indicators cross thresholds -- fires notifications without watching the chart
- **Optimization Heatmap:** 2D parameter surface visualization (OMS-style) for the GPU strategy optimizer -- see which parameter combinations produce the best Sharpe at a glance
- **Risk-of-Ruin Calculator:** Monte Carlo ruin probability estimation from your actual trade history
- **Replay Mode:** step through historical bar data tick by tick for strategy development and review
- **Multi-Window Support:** `NEW_WINDOW` / `POPOUT` spawns a separate terminal process -- run multiple charts on multiple monitors natively
- **Multi-Signal Anomaly Scanner:** combined VaR + EV + ATR + SEC outlier detection -- surfaces symbols that are anomalous across multiple risk dimensions simultaneously
- **FRED Economic Data Dashboard:** yield curve visualization with automatic inversion detection -- see when the 2Y/10Y spread flips negative
- **Economic Calendar:** upcoming events with impact ratings
- **Congressional Trade Tracker:** monitor disclosed trades by US lawmakers
- **Supply/Demand Zones:** fractal-based 1:1 port of SupplyDemand.mqh (GPU+CPU hybrid rendering)
- **BetterVolume:** full rewrite with buy/sell pressure estimation (1:1 MQL5 port)
- **DARWIN Trade Overlay:** buy/sell arrows + open position SL/TP lines rendered on chart
- **Broker Selector:** dropdown for Alpaca / tastytrade / Both with per-broker connection status
- **LAN Sync TLS:** encrypted WebSocket sync (wss:// with ephemeral self-signed certs)
- **GPU/CPU Indicator Audit:** 28 indicator pairs verified, 3 mismatches fixed between GPU and CPU paths
- **5 New Indicators:** Supertrend (ATR-based trend bands with direction flip), Donchian Channels (N-bar high/low), Keltner Channels (EMA ± ATR), Regression Channel (rolling linear regression ± std error), Squeeze Momentum (BB-inside-KC detection with momentum histogram)
- **Session Highlighting:** Asian/London/NY timezone shading on charts
- **MA Ribbon Fill:** KAMA vs SMA200 green/red gradient fill
- **Volume Heatmap Candles:** color-coded by relative volume (blue→green→yellow→red)
- **VWAP with Deviation Bands:** daily-anchored VWAP with 1σ/2σ/3σ bands
- **Price Distribution Histogram:** time-at-level displayed on chart right side
- **Drawing Toolbar:** left-side floating toolbar, TradingView-style
- **O(n) Performance Optimizations:** Bollinger, KAMA, Fisher, Stochastic, Williams %R, CCI all rewritten from O(n²) to O(n) with rolling sums and monotonic deques
- **112 tests pass**
- **MultiKAMA + FakeCandle:** 10/10 MT5 custom indicator parity achieved in the native renderer
- **MTF_MA Overlay:** 200 SMA status, KAMA, Bull/Bear Power text overlay matching MTF_MA.mqh
- **44 unit tests** for all indicator computations
- **110 commands**, **110 windows**, **60+ indicators**, **70 drawing tools**

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

Symbol collection unifies positions + watchlist + MT5 cache. All 6 scanner commands automatically include Darwinex data when available. The web explorers are legacy. The terminal scanners are live.

## Post-Launch: 56 Commits, LAN Parity, Drawing Tools UX, MQL5→WGSL Phase 2

Since the initial sprint, 56 more commits have landed. The terminal is now **59,769 lines** across **734 commits**. The major post-launch themes:

### LAN Sync: Full Client/Server Parity

LAN sync evolved from a basic WebSocket bridge to a zero-gap replication system. The server broadcasts all data — bar cache, DARWIN analytics, broker positions, account details — via KV sync. The client receives everything and never needs to recompute locally.

- **Auto-start:** LAN server launches on startup
- **15-second periodic resync** (down from 60s)
- **try_lock instead of lock.await** — eliminates UI freezes on the client when FetchBars runs
- **FetchBars forwarding** — client sends bar requests to the server instead of erroring with "Broker not connected"
- **Multi-source bar lookup** with dedup — eliminates FetchBars spam
- **Alpaca 429 fix** — GetPositions no longer fires on every OrderResult, preventing rate limit cascades
- **Crypto weekend bar merge** — CryptoCompare+Kraken data merged in `try_load()` for seamless weekend gap-fill
- **Broader LIVE detection** — status bar shows LIVE when MT5, API keys, or cached data available (not just broker connection)
- **LAN client data source display** — client shows server's connected data sources; reduced BG thread log spam
- **LAN remote FETCH_BARS** — server executes Alpaca bar fetches on behalf of the client (client needs zero API keys for chart data)
- **LAN concurrent remote commands** — multiple requests can execute in parallel without blocking
- **LAN client read-only mode** — trading buttons disabled with read-only overlay (prevents accidental trades from non-primary machines)
- **DARWIN trade markers** — ticker labels on buy/sell arrows with aggregation for overlapping trades
- **Full LAN remote command wiring** — server executes every forwarded client request (not just FETCH_BARS — all commands)
- **Crypto bar dedup fix** — snap timestamps to TF boundary for timezone parity across data sources
- **Supply/demand GPU fix** — apply BACK_LIMIT=1000 matching MT5 behavior for zone detection accuracy
- **KV-based analytics:** all 31 DARWIN analytics functions are computed on the server and synced as KV pairs. Client reads computed results — zero local deal queries
- **TLS encryption:** wss:// with ephemeral self-signed certificates
- **Status bar:** shows "ONLINE [LAN x.x.x.x]" when connected

### Drawing Tools: 70 Tools with Professional UX

Drawing tools went from 44 to **70** with major UX improvements:

- **Undo/redo** (Ctrl+Z / Ctrl+Y) for all drawing operations
- **Color picker** per drawing object
- **Live preview** during placement — see the tool before committing
- **OHLC snapping** — drawing points align to candlestick open/high/low/close levels
- **Trashcan button** for quick deletion
- **Status text** showing active tool name and instructions
- New tools: FibWedge, FibSpiral, RotatedRectangle, AnchoredVwapLine, TrendChannel, InsidePitchfork, PriceNote, MeasureTool, and more

### MQL5→WGSL Phase 2: Compile MQL5 Indicators to GPU

The MQL5 compiler now targets **WGSL (WebGPU Shading Language)** instead of WASM. Custom MQL5 indicators compile directly to GPU compute shaders. Write your indicator in MQL5 → the compiler generates WGSL → wgpu dispatches it on the GPU. No JavaScript. No WASM. No CPU. The indicator runs alongside the 31 built-in GPU shaders in the same compute pipeline.

Parser improvements: function call arguments in variable declaration initializers now parse correctly.

### PineScript Parser: Weekend Bars Finally Behave

The compiler crate gained a **PineScript parser** — TradingView's Pine Script indicators can now be parsed alongside MQL5. Weekend crypto bars (sourced from Kraken/CryptoCompare) that previously caused timestamp misalignment now align correctly across all data sources. The bar merging logic snaps timestamps to timeframe boundaries, eliminating duplicate and phantom bars at weekend/weekday transitions.

![Tome hoots: PineScript parser lives. Weekend bars finally behave.](/img/tome-pinescript-parser-20260403.webp)

### Crypto Backfill: CryptoCompare + Kraken

Sub-hourly crypto timeframes now backfill from **CryptoCompare** with **Kraken** as fallback. Skip-if-cached logic prevents redundant fetches. The three-tier hierarchy (MT5 → Kraken → CryptoCompare → Alpaca) covers every crypto gap.

### Dual-Connection SQLiteCache

The "Cache busy" error is permanently eliminated. The SQLite cache now uses **two connections** — a dedicated read connection and a dedicated write connection. Background operations (MT5 sync, bar merges, DARWIN imports) use the write connection. UI reads use the read connection. Zero contention. Zero "database is locked" errors. Zero UI freezes during data operations.

### Security Hardening

A security audit pass eliminated all panic risks:
- All `unwrap()` calls on fallible operations replaced with proper error handling
- Safe integer conversions (no truncation panics)
- Graceful fallbacks for missing data instead of crashes
- BarCacheWriter raw blob handling (no zstd assumption)

### BarCacheWriter v1.435: Ramdisk via /dev/shm

The biggest I/O bottleneck in the terminal pipeline was BarCacheWriter's SQLite database — 851 symbols × 9 timeframes = 7,659 keys written every 30 seconds. On spinning disk or even NVMe, the write amplification from SQLite journaling and fsync made each cycle slow enough to notice.

**The fix: move the database to `/dev/shm` (Linux tmpfs ramdisk) via symlink.**

`deploy_ramdisk.sh` symlinks each MT5 instance's `typhoon_mt5_cache.db` from the Wine filesystem to `/dev/shm/`. MQL5 code is completely unaware — `DatabaseOpen("typhoon_mt5_cache.db")` follows the symlink transparently. Zero EA code changes needed.

**Performance gains:**

| Metric | Before (NVMe) | After (ramdisk) | Speedup |
|---|---|---|---|
| Metadata queries | ~12 seconds | <100ms | **>120x** |
| Statement execution | baseline | ~10x faster (pre-prepared reset+rebind) | **10x** |
| CopyRates calls | 7,659/cycle | ~766/cycle (TF gating) | **90% eliminated** |
| Lock overhead | 7,659 individual | ~85 batch transactions | **90x fewer locks** |

**Key optimizations baked into v1.435:**

- **Covering index** on `bar_cache(key, timestamp, bar_count)` — readers get metadata from index alone without scanning multi-MB blob rows
- **Batch transactions** — 10 symbols per `BEGIN/COMMIT` = ~85 transactions per cycle instead of 7,659
- **TF gating** — only calls `CopyRates` near bar boundaries (H4 only updates every 4 hours, not every tick)
- **Pre-prepared statements** — `reset+rebind` is ~10x faster than `prepare+finalize` per call
- **SQLite pragmas tuned for ramdisk:** `journal_mode=DELETE` (WAL shared memory doesn't work across Wine/Linux boundary), `synchronous=NORMAL`, `cache_size=16MB`, `temp_store=MEMORY`

**Operational notes:**
- `/dev/shm` is tmpfs — data does NOT survive reboot. BarCacheWriter re-exports all 851 symbols on startup (~5-10 min)
- Steady-state: ~2GB per MT5 instance (3 instances = ~6GB in /dev/shm)
- TyphooN-Terminal's Mt5Sync reads directly from ramdisk paths — configure in Settings → MT5 BarCacheWriter Sources
- v1.434 attempted Wine Z: drive mapping to `/dev/shm` directly — abandoned in favor of symlinks (more reliable, zero EA code changes)

### Symbol Explorer: Full Broker Universe + Fundamentals

New **Symbol Explorer** floating window displays the complete broker symbol universe with fundamentals-based categorization. Browse every available instrument, sorted by sector, with live data. No more guessing what symbols your broker offers.

### tastytrade Integration

tastytrade positions now wire to chart overlay and positions panel. All symbol matching normalized across Alpaca, tastytrade, and DARWIN sources. Position visibility toggles: show/hide DARWIN, Alpaca, or tastytrade positions independently.

### POSITION_CHARTS Command

Type `POSITION_CHARTS` and the terminal opens weekly chart tabs for every open position simultaneously. One command, all positions visible.

### Backfill Candle Coloring

Bars from non-primary sources now render in distinct colors:
- **Magenta** — backfill/weekend bars (Kraken, CryptoCompare)
- Weekly and monthly timeframes exempt (weekend coloring disabled for W1/MN1)

Visual distinction so you always know which data source painted each candle.

### Supply/Demand GPU→CPU Fallback

When GPU compute produces zero supply/demand zones (edge cases with insufficient data), the engine falls back to CPU computation automatically. Zero missing zones.

### Performance & Stability

- **480 tests passing, 0 vulnerabilities** (cargo update bumped all compatible crates)
- **UI freeze fix** during fundamentals scrape — per-ticker lock release prevents blocking
- **Session saves on window close** — no more lost state
- **LAN sync auto-reconnect** with session IP persistence
- **NNFX preset cleanup** — disables volume heatmap + 10 non-NNFX indicators for clean NNFX charts

### Updated Stats (2026-04-03)

| Metric | Launch (Mar 20) | Current |
|---|---|---|
| **LOC** | 43,739 | **59,769** |
| **Commits** | 594 | **734** |
| **Indicators** | 32+ | **60+** (31 GPU compute) |
| **Drawing tools** | 44 | **70** |
| **Floating windows** | 29 | **110** |
| **Console commands** | 103 | **110** |
| **DARWIN analytics** | 69 | **31 public functions** |
| **Crates** | 4 | 4 (engine, native, cli, mql5-compiler) |

## Open Source: Why This Matters

Proprietary trading terminals are a tax on retail traders. Bloomberg charges institutional prices because institutions will pay. Godel charges subscriptions because traders are conditioned to accept recurring costs for essential tools. MetaTrader is "free" because MetaQuotes monetizes the ecosystem through broker partnerships and marketplace fees.

None of this is necessary. The APIs are public. The math is known. The rendering technology exists in every browser. The only reason trading terminals cost money is because nobody bothered to build the open-source alternative properly.

TyphooN-Terminal is **BSL (Business Source License)**. Use it commercially. Fork it. Modify it. Build your own trading infrastructure on top of it. The only thing you cannot do is close the source and pretend you invented it.

**68,400 lines of pure Rust. 861 commits. Three frontend rebuilds. Zero JavaScript remaining.** GUI (egui + wgpu) + CLI (ratatui) + WASM web client + 118+ commands + 60+ indicators (all GPU compute) + 89 drawing tools + 110 floating windows + 31 DARWIN analytics functions + SEC EDGAR scraper + MQL5→WGSL compiler + risk-of-ruin + replay mode + GPU strategy optimizer + LAN sync + phone access over LAN. One developer who gutted 40,000 lines of JavaScript because the webview was the bottleneck.

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
| **TyphooN-Terminal** | **Free** | **Yes (BSL)** | Stocks, options, crypto + MT5 sync | **118+ commands** | **Yes (wgpu)** | **~15MB** | **Yes** |
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

**TyphooN-Terminal is the only trading terminal with a native GPU rendering pipeline (wgpu/Vulkan), zero JavaScript, zero WebKit, real brokerage integration, direct MT5 database sync, GPU compute shaders for indicators, LAN sync with TLS, WASM web client for phone access, built-in outlier scanners, MQL5→WGSL compiler, and a built-in risk management engine.** Every other option is either CPU-rendered (NinjaTrader, Sierra Chart, Thinkorswim), browser-based (TradingView), Electron bloatware, closed-source (Webull, IBKR), research-only (Godel), or locked to Windows (NinjaTrader, Sierra Chart, Quantower). TyphooN-Terminal is the only one that got the rendering pipeline right.

## Update (2026-04-02): Calculator Suite Sunset — VaR, ATR, and Portfolio Tools Retired

The calculator page just lost three tools:

- **Stop Loss Calculator** — removed (was non-functional: JS referenced HTML fields that didn't exist)
- **Portfolio VaR Calculator** — removed (100% dependent on explorer data that no longer updates)
- **Symbol Lookup Tool** — removed (850-symbol database from `calculator_complete_data.js` is now stale)

**What remains:** The **Position Size Calculator** (account size, risk %, entry price, stop loss → position size) and the **Compound Interest Calculator** (standalone, no market data needed). These two tools work without any external data dependencies.

### Why These Specific Calculators?

The removed tools all shared one fatal dependency: `window.varData` — a consolidated dataset of 850 symbols generated from the explorer CSVs. With the explorers frozen (see [Explorer Sunset](03312026-Explorer-Sunset.html)), that data is permanently stale. A VaR calculator showing October 2025 volatility data in April 2026 isn't a calculator — it's a liability.

The Stop Loss Calculator had an additional problem: the JavaScript referenced `sl-account-size` and `sl-risk-percent`, but the HTML form contained `sl-risk-value` and `sl-risk-mode`. It was never functional in its current state.

### Where These Features Live Now

| Removed Web Calculator | TyphooN-Terminal Equivalent |
|---|---|
| **Stop Loss Calculator** | Risk panel: VaR-based SL, ATR-based SL, 4 order modes |
| **Portfolio VaR Calculator** | `VAR` command, DARWIN analytics (80 functions), correlation matrix |
| **Symbol Lookup Tool** | `SEARCH` command, anomaly scanner (4D: VaR+EV+ATR+SEC), stock screener |

The terminal computes VaR live from broker position data. It calculates ATR on GPU compute shaders across any timeframe. It pulls SEC EDGAR fundamentals, options chains, insider trading data, and dark pool volume. A static HTML page with a frozen JSON dataset cannot compete with a native GPU application pulling live feeds.

### The Remaining Calculators

The **Position Size Calculator** is pure math: you enter four numbers, it tells you how many shares to buy. No market data needed. No API calls. No staleness risk. It stays because it works.

The **Compound Interest Calculator** is the same story — standalone math with wealth milestones, yearly breakdowns, and timeline visualization. Zero external dependencies. It stays.

The website calculator page is now two tools that do two things correctly, rather than five tools where three are broken or stale. That's the right trade.

## Update (2026-04-04): 765 Commits, 537 Tests, Drawing Tools Complete

31 more commits since the last update. **765 total commits.** The codebase crossed **61,900 lines of pure Rust** across all four crates. 537 tests. Every major drawing tool category is now fully wired, draggable, and selectable.

### Updated Stats (2026-04-04)

| Metric | 2026-04-03 | 2026-04-05 |
|---|---|---|
| **LOC** | 59,769 | **~62,900** |
| **Commits** | 734 | **782** |
| **Tests** | 480 | **618** |
| **Drawing tools** | 70 | **89** (82 TV parity + 7 bonus) |
| **Console commands** | 110 | **115** |
| **BrokerCmd variants** | — | **57** |
| **Crates** | 4 | 4 |

### MQL5 Compiler UI: Load, Compile, Inspect

The MQL5 compiler crate got a full UI. The `COMPILE` command now opens a dedicated compiler window: select an MQL5 or PineScript file, compile it, and get structured diagnostics with line numbers, error categories, and metadata. Compilation results include function signatures, variable types, and detected indicator outputs. The compiler targets WGSL — custom indicators go straight to the GPU pipeline, not WASM, not a CPU fallback.

**7 new tests** cover the compiler's output and AST pipeline.

### BarBuilder: Real-Time Bar Streaming

`BarBuilder` is the new live data engine for chart candles. The `StartStream` command initiates a streaming session. `StreamTick` and `StreamQuoteTick` messages feed individual tick data into the builder. The builder accumulates ticks into OHLCV bars, completes them at bar boundaries, and pushes them to the chart in real time.

This is the headless path for algo deployment — no polling, no API calls on a timer. The stream feeds bars as they form. Charts update continuously without a refresh cycle.

**7 new BarBuilder tests.**

### Notifications Wired to Indicator Alerts

Discord, Pushover, and ntfy notifications are now wired to the indicator alert engine. Configure an alert threshold on any indicator — when it fires, the notification goes out on all enabled channels. The terminal becomes an alert system that works whether you are watching it or not.

**13 new notification tests.**

### Drawing Tools: 73 Types, All Selectable, All Draggable

Drawing tools hit **73 types** with complete professional UX:

- **Hit-test selection** on all 73 drawing types — click any drawing object on the chart to select it
- **Move/drag** for all 73 types — grab any drawing and reposition it on the chart
- **Width and style** controls wired across all types — line weight, dash style, and selection tint
- **Undo/redo sync** across tab drag-drop and drawing operations
- **Tab drag-drop** — reorder chart tabs by dragging

Previously, selection worked on roughly 20 drawing types. Now it works on all of them. The drawing toolkit is at TradingView parity for selection and manipulation UX.

### Analyst/Holders/Orderbook DOM/Option Chain Windows

Four floating windows that previously logged raw data are now fully wired with structured rendering:

- **Analyst Window** — analyst ratings, price targets, buy/hold/sell consensus
- **Institutional Holders** — top holder names, share counts, percentage ownership, change quarter-over-quarter
- **Orderbook DOM** — depth of market ladder with bid/ask stacks, volume visualization
- **Option Chain** — strikes, expiry, Greeks (delta/gamma/theta/vega), OI, volume, IV — the full options analysis panel that tastytrade and Thinkorswim charge for

All four render structured data grids instead of raw log output.

### Screener: Filter, Sort, 5-Column Grid

The stock screener got a UX pass:
- **Filter bar** — type to filter results in real time
- **Sort by bars** — order results by bar count (most data first)
- **Colored source column** — visual distinction between MT5, Alpaca, Kraken, and other data sources
- **5-column grid layout** — more results visible per screen without scrolling

### Replay Mode: Actually Masks Future Bars

Replay mode's chart now correctly hides future bars during playback. Previously the full bar history was visible while the replay cursor stepped through it — defeating the entire purpose of replay. Fixed: bars beyond the playback cursor are masked from the chart. Historical strategy review now works as intended.

### 32 Custom Timeframes Restored

The timeframe selector was rebuilt as a **ComboBox dropdown**, replacing the row of buttons that ran out of space above M5. All **32 custom timeframes via bar aggregation** are available: M2 through Y10. Right-click on any timeframe to switch context. `Alt+TF` keyboard shortcut. Every aggregated timeframe that MT5 offers, available in the terminal.

### UX Polish

- **Middle-click close** — close any chart tab with middle mouse button
- **P&L%** — positions panel shows P&L as both dollar amount and percentage simultaneously
- **MTF grid focus fix** — multi-timeframe grid correctly tracks focused symbol
- **Weekend crypto auto-poll** — Kraken poll fires automatically on weekends without manual trigger

### Smart MT5SYNC + Live Forming Bars

The MT5 sync pipeline was overhauled:

- **Smart skip** — MT5SYNC detects unchanged symbols and skips them, eliminating redundant database reads and bar merges on every sync cycle
- **Regression detection** — if new bar data has fewer bars than the cache for a symbol, it is flagged as a regression instead of silently overwriting good data with bad data
- **Detailed sync stats** — the sync window shows per-symbol counts: synced, skipped, regressed, errors
- **Live bid/ask every 30s** — MT5 bid/ask prices update on a 30-second cycle and feed the chart's price lines
- **Bar sync every 60s** — incremental bar sync on a 60-second cycle with auto-reload when new bars arrive
- **Live forming bars** — the currently-forming bar updates in real time from MT5 bid/ask, Alpaca quotes, and watchlist prices without waiting for the bar to close

### LAN Server Reliability

The LAN server had a persistent auto-start regression where the KV client recovery path was overriding server mode on startup. Fixed via KV cache persistence — `server_enabled` survives restarts. IP address also persists across sessions. The LAN server now starts reliably on primary machines and stays off on client machines without manual configuration every session.

Periodic resync added on the client side — the client resyncs on a schedule rather than waiting for server pushes, eliminating staleness on reconnect.

### MQL5 Export Tests

**7 new tests** for the MQL5 export pipeline covering round-trip accuracy from MQL5 source → AST → IR → WGSL output.

**9 new LAN sync tests** covering the server/client state machine, KV propagation, and reconnect behavior.

Total: **537 tests across all crates.** All pass.

### 5 Missing Alpaca API Endpoints + FRED Full 10-Series (2026-04-04, late)

Five new commands wired to previously untapped Alpaca API endpoints:

- **PRICE_TARGET** — analyst price target consensus (mean, median, high, low) from Alpaca's corporate actions API
- **SHORT_INTEREST** — short interest data for any symbol, showing shares short, days to cover, and short ratio
- **CORPORATE** — corporate actions feed (dividends, splits, spinoffs, mergers) with date ranges
- **MOST_ACTIVE** — most active symbols by volume from Alpaca's market movers endpoint
- **PORTFOLIO_HIST** — historical portfolio equity curve from the broker, rendered as a time series

The FRED economic data dashboard expanded from a partial implementation to the **full 10-series suite**: Federal Funds Rate, 2Y/10Y/30Y Treasury Yields, CPI YoY, Core PCE, Unemployment Rate, Initial Jobless Claims, GDP Growth, and Consumer Sentiment. All 10 time series display with proper date ranges and auto-refresh.

ADR counts updated: **46 BrokerCmd** variants, **29 BrokerMsg** variants.

### DARWIN Analytics Wiring + 551 Tests (2026-04-04, cont.)

Three DARWIN analytics functions wired to the per-account display:

- **Performance Attribution** — decomposes per-DARWIN returns into symbol-level contributions. See exactly which symbols drove profits and which dragged performance for each account.
- **D-Score Components** — all 8 Darwinex investability scores rendered per-account with color-coded thresholds (experience, risk management, consistency, etc.)
- **Investment Velocity** — AuM growth rate and investor flow momentum per DARWIN over time.

**Price target** data now displays in the Analyst window alongside ratings consensus — mean, median, high, low targets visible at a glance next to buy/hold/sell counts.

**14 new tests:** 4 FRED endpoint tests + 10 screener tests covering filter logic, sort ordering, and source column rendering. Test distribution: **82 compiler + 383 engine + 86 native = 551 total.**

Code cleanup: `FISHER_SIG` constant replaces hardcoded `Color32` for the Fisher Transform signal line — consistent theming across indicator rendering.

### 19 New Drawing Tools (70→89), Eraser, Cross-TF, DXLink Streaming (2026-04-04, final)

The drawing toolkit jumped from **70 to 89 tools** in a single commit. The 19 new tools:

Circle, PitchFan, TrendFibTime, GannSquare, GannSquareFixed, BarsPattern, Projection, DoubleCurve, AnchoredText, Comment, ArrowMarkerLeft, ArrowMarkerRight, TrianglePattern, ThreeDrives, ElliottDouble, AbcdPattern, CypherPattern, ElliottTriangle, ElliottTripleCombo.

That's every harmonic pattern, every Elliott Wave variant, Gann squares, projection tools, and annotation types. The drawing toolkit now covers the full TradingView drawing palette.

**Eraser cursor mode** (`DRAW_ERASER`): click near any drawing to delete it instantly. No more right-click → delete menu diving. Click. Gone.

**Cross-timeframe drawings** (`CROSS_TF`): toggle to share drawings across all timeframes for the same symbol. Draw a Fibonacci on H4, see it on D1 and W1 automatically. Previously, drawings were timeframe-locked.

**DXLink real-time streaming**: `subscribe_quotes()` wires tastytrade's DXLink WebSocket for live quote streaming. Real-time bid/ask/last from tastytrade alongside Alpaca's feed.

**Watchlist CRUD + Alpaca options chain** wired to the API layer. DARWIN export/import pattern warnings cleaned up — zero compiler warnings across the entire codebase.

**BrokerCmd count: 57** (was 46). **Drawing tools: 89** (was 70).

### Dead Code Purge + Security Hardening (2026-04-05)

**515 lines of dead code removed** in a single commit. Deleted: 8 unused CSS color constants, the `DrawingEntry` struct, `ATR_PROJ_COL`, `KEEPALIVE_SECS`, `confirm_close_all`, `watchlist_symbols`, `screenshot_path`, `created_at`, `should_query_db()`, standalone `OrderBlock`/`FVG`/`MarketStructure` detection helpers (inline versions in `draw_chart` remain). Removed all stale `#[allow(dead_code)]` annotations from 50+ Drawing variants and used structs. LOC went from ~63,200 to ~62,700 — the codebase got smaller while gaining features.

**Three security fixes:**

- **Constant-time HMAC comparison** in LAN sync authentication — the previous byte-by-byte comparison was vulnerable to timing attacks. An attacker on the LAN could theoretically measure response time differences to reconstruct the HMAC key byte by byte. Fixed with constant-time comparison.
- **Discord webhook URL validation** hardened against path traversal and hostname spoofing. Webhook URLs are now validated for correct hostname (`discord.com` / `discordapp.com`) and path structure before any request fires. Prevents SSRF via malicious webhook URLs.
- **Log VecDeque bounded to 500 entries** — the log buffer was unbounded, growing without limit. On long-running sessions, this was a slow memory leak. Capped at 500 entries with oldest-first eviction.

**Zero bare `unwrap()` in production code.** Every fallible call in hot paths replaced with `unwrap_or`, `match`, early return, or `unwrap_or_default()`. `VecDeque::front()` uses `unwrap_or(&0)`. `bars.last()` returns early. Background connection and summary paths use `match`-continue. The tokio runtime init uses `expect()` (unrecoverable — acceptable). Chrono conversions use `unwrap_or_default()`. A trading terminal that panics during order execution is not a trading terminal — it's a liability. Zero panicking unwraps remain in any path that handles live data.

### Full TradingView Drawing UX Parity (2026-04-05, cont.)

The drawing toolkit now matches TradingView's UX feature-for-feature, plus 7 bonus tools TradingView doesn't have:

**TradingView-standard keyboard shortcuts:**
- `Alt+H` — Horizontal Line
- `Alt+V` — Vertical Line
- `Alt+T` — Trend Line
- `Alt+F` — Fibonacci Retracement
- `Alt+R` — Rectangle
- `Alt+E` — Eraser
- `Alt+C` — Cycle chart type (Candlestick → Heikin Ashi → Line → OHLC → Renko)

**Pre-placement color picker:** 8-color toolbar palette. Select the color before placing the drawing — no more draw-first-edit-later workflow.

**Per-drawing right-click property editor:** right-click any selected drawing to change its color, line width, and line style inline. No modal dialog. No settings panel. Right-click → pick → done.

**Control point handles on selected drawings** — drag individual anchor points (Gap #3 from ADR-068, now complete). Select a Fibonacci, grab an endpoint, reposition it. Same interaction model as TradingView.

**Follow-latest toggle** — lock the chart to auto-scroll with new bars, or unlock to freely scroll history. Toggle in the toolbar.

All 71 unique drawing colors now use the per-drawing `draw_color` field instead of hardcoded constants. Removed unused `HLINE_COL`. **89 drawing tools = 82 TradingView tools + 7 bonus** (ElliottTripleCombo, CypherPattern, ThreeDrives, BarsPattern, DoubleCurve, AnchoredText, Comment).

### Logarithmic Price Scale + Fit All Bars (2026-04-05, late)

**Logarithmic price scale** — `Alt+L`, `LOG_SCALE` command, or right-click menu. Uses `ln()` mapping so that a move from $10→$20 (100%) takes the same vertical space as $100→$200 (100%). Essential for volatile assets like crypto and small-caps where linear scale compresses the early price history into a flat line. Session-persisted per chart — switch to log on BTC/USD and it stays log when you reopen.

**Fit All Bars** — `FIT` command or right-click menu. Zooms the chart to show the entire bar history in the viewport. One click to see the full picture.

### Adjustable Indicator Parameters + Multi-Symbol Chart Overlay (2026-04-05, final)

**Adjustable indicator parameters:** 10 key indicator periods are now configurable per-chart via DragValue sliders in the Indicators panel — SMA slow/fast, EMA, RSI, ATR, Bollinger Bands, Stochastic, ADX, Fisher Transform, and Momentum. Drag a slider, the GPU recomputes immediately. No restart. No config file. No reloading the chart. Every parameter change triggers a GPU compute shader dispatch with the new period. Session-persisted per chart — set RSI to 21 on your BTC chart and it stays 21 next session.

**Multi-symbol chart overlay** (`COMPARE` command): load a second symbol from cache and render it as a purple percentage-change line normalized to the primary chart's price axis. Compare AAPL vs SPY on the same chart. The overlay scales the second symbol's price history to percentage change from its first visible bar, so both symbols share the same Y-axis regardless of absolute price difference. Session-persisted.

### Bid/Ask Spread Lines + 575 Tests (2026-04-06)

**Live bid/ask spread lines on chart** — green dashed line for bid, red dashed for ask, fed from real-time streaming quotes. The spread is visible at a glance on every chart without checking a separate panel. All TradingView/MT5 UX gaps now filled.

**Undo/redo toast feedback** — undo (`Ctrl+Z`) and redo (`Ctrl+Y`) actions now show confirmation messages in the log panel so you know what was undone.

**38 new tests** covering two previously untested broker integrations:
- **DXLink (16 tests):** token struct, candle struct, quote struct, `parse_f64` edge cases (NaN, Infinity, null, bool coercion)
- **tastytrade (22 tests):** session/account/position/expiration/strike/Greeks struct tests, Greeks defaults, empty strikes handling

Test distribution: **575 total** (up from 537). All pass.

### Graphical Upgrades: 6 Analytics Windows (2026-04-06, cont.)

Six stats windows upgraded from plain text/tables to native egui charts and color-coded visualizations:

- **Monte Carlo VaR** — bar chart rendering of VaR/CVaR levels instead of raw numbers
- **Correlation Matrix** — colored heatmap cells: green (low) → yellow → orange → red (high correlation). Spot redundant DARWINs at a glance
- **Seasonal Patterns** — monthly return bar chart with green (positive) / red (negative) bars. Visual seasonality detection
- **Margin Monitor** — horizontal gauge with color zones (red/yellow/green) showing current margin utilization against thresholds
- **Trade Journal** — cumulative P&L line chart tracking equity curve over journal entries
- **Data Window** — color-coded indicator values: RSI overbought (red) / oversold (green), Fisher positive (green) / negative (red), ATR dimmed for context

These windows previously showed raw numbers in tables. Now they render native egui charts — bar charts, heatmaps, gauges, and line plots — all GPU-rendered in the same frame as the rest of the UI.

### Graphical Upgrades Batch 2: 5 More Windows + Color Pass (2026-04-06, final)

Five more analytics windows upgraded to native charts:

- **Stress Test** — impact bar chart showing projected portfolio loss under each historical crash scenario (COVID, GFC, Rate Hike, Flash Crash, Tech Wreck, Crypto Winter)
- **VaR Multiplier** — corridor gauge showing current VaR position within the Darwinex 3.25%–6.5% target range with color zones
- **Risk Calculator** — risk/reward visualization bar for the current trade setup
- **Cache Statistics** — data distribution bar chart showing cache utilization across tiers
- **News** — sentiment coloring on headlines (positive/negative/neutral)

**Color consistency pass across 12+ uncolored percentages:** drawdowns always render red, win rates use green/yellow/red thresholds, VaR corridor values color-coded to zone, contribution percentages green (positive) / red (negative). No more raw white numbers for metrics that have inherent good/bad semantics.

### Order Entry Wired: Real Trades From the GUI (2026-04-06)

The Order Entry panel's Submit button was logging instead of sending real orders — a migration regression from the frontend rewrite. Fixed: all five Alpaca order types (market, limit, stop, bracket, cancel) and tastytrade equity orders now fire real `BrokerCmd` messages to the broker backend. The button does what it says.

Order placement integrates with the full **TyphooN v1.420 risk engine** already ported to Rust — all 4 order modes from the MQL5 EA are supported. The `RISK_CALC` command opens the position sizing calculator: enter equity, risk %, entry, stop loss, take profit, tick value/size → get lot sizing via `risk_lots()`, dollar risk, SL distance, R:R ratio, and usable margin. The margin monitor (`MARGIN` command) computes `max_safe_lots()` from the forward-looking TRIM formula and PROTECT urgency — the same math that manages live DARWINs on Darwinex. 100% of the TyphooN MQL5 EA's risk management features are available natively in Rust.

**Order cancel buttons** added to the Orders panel — click to cancel any open order directly. No more command-line-only cancellation.

**`warm_data_connection`** fires on Alpaca connect — pre-establishes the TCP+TLS handshake to the data API endpoint so the first bar fetch doesn't eat a cold-connect penalty.

### Compound Interest Calculator + Crypto Auto-Refresh (2026-04-06, late)

**`COMPOUND` command** — compound interest calculator with growth chart. Enter principal, monthly contribution, annual rate, and time horizon. The calculator renders a line chart showing principal growth vs total contributions over time, with final balance and total interest earned. The same calculator from MarketWizardry.org's web tools, now native in the terminal with an egui line chart instead of a static HTML page.

**Periodic crypto bar refresh** — crypto symbols auto-fetch fresh bars approximately every 60 seconds. Charts stay current without manual refresh or switching timeframes.

### Fear & Greed Index, Trailing Stop, Per-Position Close (2026-04-07)

**Fear & Greed Index window** — pulls live data from the alternative.me API and renders a colored gauge visualization (extreme fear → fear → neutral → greed → extreme greed). Auto-fetches on window open. One more data point for regime detection without leaving the terminal.

**Order entry expanded to 6 order types** — added **trailing stop** and **stop-limit** to the existing market, limit, stop, and bracket types. Trailing stop follows price movement by a specified trail amount. Stop-limit converts to a limit order when the stop price is hit. Both wired to Alpaca's API.

**Per-position close button** — each Alpaca position in the right panel now has an `(x)` button for one-click close. Sends `ClosePosition` command directly. Disabled for LAN clients (read-only mode prevents accidental trades from non-primary machines).

### Draggable SL/TP, World Indices, Crypto50, Forex, HTF Forming Bars (2026-04-07, cont.)

**Draggable SL/TP lines — full MT5 EA parity.** The complete TyphooN.mq5 `OrderLines` workflow is now native in the terminal:
1. **Buy Lines** places SL at visible low + TP at visible high (Sell Lines inverted) — matching TyphooN.mq5 exactly
2. **Drag** SL or TP line on the chart — click within 8px to start dragging, release to set new price. Blocks chart pan during drag.
3. **Set SL / Set TP** buttons place real GTC stop/limit orders at the line price, opposite to position direction. `AlpacaModifyOrder` handles modifying existing bracket legs.
4. **Destroy Lines** clears both.

All buttons appear in both the right panel and Trading menu. This is the exact SL/TP management workflow from the MQL5 EA, running natively on Alpaca instead of MT5.

**World Indices dashboard** (`INDICES` command) — 16 major global indices via ETF proxies (SPY, QQQ, IWM, DIA, EFA, EEM, VGK, EWJ, FXI, EWZ, etc.). Live quotes in a single dashboard.

**Crypto Top 50** (`CRYPTO50` command) — top 50 cryptocurrencies by market cap from CoinGecko API with live prices, 24h change, market cap, and volume.

**Forex major pairs** (`FOREX` command) — 10 major forex pairs with proper decimal precision (5 decimals for most, 3 for JPY crosses).

**HTF forming bar synthesis** — when the last bar on H1/H4/D1/W1/MN1 is stale (common on weekends for crypto), the engine aggregates M5/M1 bars newer than the last HTF period boundary into a single forming bar. Tries M5 first, then M1, from MT5/Kraken/CryptoCompare sources. Fixes the weekend gap where HTF charts showed stale data while lower-timeframe data was available.

**BarBuilder hardened** — validates NaN/Infinity/negative size/empty symbol/invalid timestamps (rejects instead of silently accepting). Added `ingest_quote()` for bid/ask mid-price updates, `flush_stale()` for timed bar completion, 10K completed buffer limit, and `active_count()`/`pending_count()` metrics. **18 tests** (was 7).

**586 total tests.** Only 2 remaining feature gaps are external constraints (SqueezMetrics paid API, Alpaca OCO limitation). Every blog-claimed feature now exists.

### LAN Client/Server Crypto Weekend Parity (2026-04-07, late)

Crypto charts on weekends were broken on the LAN client — the periodic fetch required `broker_connected` which is false on client machines. Fixed: Kraken and CryptoCompare fetches now run locally on both server and client without broker dependency. The periodic crypto refresh fetches M1 + M5 + the chart's active timeframe, so forming bar synthesis always has lower-timeframe data to aggregate from.

**Server→client live quote sync:** the server stores live quotes to KV as `quote:SYMBOL` keys. The LAN client reads them every ~5 seconds and uses them to update forming bars. Bid/ask lines now work on both server and client — previously the client showed stale bid/ask because it had no direct quote feed.

**Forming bar synthesis priority:** `kraken:M1` is tried first for the freshest granularity, then falls back to other sources. Kraken fetch triggers `Mt5SyncDone` → chart reload → forming bar synthesis from M5 data. The full pipeline works end-to-end on weekends without manual intervention on either machine.

**Forming bar cascade fix:** synthesis now tries ALL lower timeframes from ALL sources (kraken/mt5/cryptocompare/alpaca × M1/M5/M15/M30/H1/H4/D1/W1) instead of just M5/M1. MN1 crypto backfill fixed — was sending `'MN1'` label instead of `'1Month'` cache suffix to Kraken. Periodic fetch uses next-lower TF for forming bar data. FetchBars handler now accepts both MT5 labels (`M1`/`H1`/`D1`/`W1`/`MN1`) and Alpaca format (`1Min`/`1Hour`/`1Day`/`1Week`/`1Month`) transparently — no cache key rename needed.

### Demand-Based BarCacheWriter Sync (2026-04-07, final)

BarCacheWriter exports all 851 symbols × 9 timeframes on every reboot — a 5-10 minute cold start that re-exports data the terminal may never use. The new **demand.txt** system fixes this.

On session save, the terminal writes `demand.txt` to persistent `~/.typhoon/cache/` (survives `/dev/shm` reboot). **Smart filtering:** only MT5-sourced symbols are included — crypto (Kraken/CryptoCompare) and ETFs/indices (Alpaca) are excluded since neither needs BarCacheWriter. DARWIN open position symbols are added automatically. The filter checks chart source prefix (`mt5`/`default`/`paper_`) to determine what actually comes from MT5.

When BarCacheWriter reads `demand.txt` on startup, it only re-exports the listed symbols instead of the full 851. Cold start drops from 5-10 minutes to seconds.

### LAN Crypto Fix + Workspace Freeze Fix (2026-04-08)

Three fixes in one commit:

1. **Periodic crypto fetch is now server-only** — LAN clients get crypto data via KV sync, no direct API calls. Reverts the earlier "local execution on both" approach which caused duplicate Kraken/CryptoCompare requests. The server fetches once, syncs to all clients.

2. **CryptoCompare for D1+ backfill** — daily and higher timeframe crypto bars now fetch from CryptoCompare instead of Alpaca `FetchBars`. CryptoCompare has deeper crypto history and doesn't require broker authentication.

3. **Workspace UI freeze eliminated** — the `WORKSPACE` command was calling 11 `keyring::store` operations synchronously on the main thread, each hitting DBUS on Linux (~100-200ms per call). Total: 1-2 seconds of frozen UI. All 11 keyring calls moved to a background thread. The workspace saves instantly and the keyring writes happen asynchronously.

### 26 Compiler Tests — Zero Test Gaps (2026-04-08, cont.)

**26 new tests** across 4 previously untested MQL5 compiler modules:
- **lib.rs (5):** `compile_mql5`/`compile_pine` integration tests — end-to-end compilation pipeline
- **ast.rs (9):** AST node construction, all variants, clone/debug trait verification
- **ir.rs (6):** IrModule construction, `extract_metadata` with properties/inputs, lower empty program
- **runtime.rs (6):** JS template content validation

Test distribution: **108 compiler + 383 engine + 86 native + 35 other = 612 total.** Every compiler module now has test coverage. Zero gaps.

### AI Chat, Matrix Chat, Reddit WSB Viewer (2026-04-08, final)

**AI Chat window** — built-in Claude and GPT chat. Provider selector toggles between Anthropic Messages API and OpenAI Chat Completions. Chat history persists per session. Ask Claude about your positions, paste chart data, get analysis — without leaving the terminal. API keys stored in the system keyring, configurable in Settings.

**Matrix Chat window** — public Matrix room message viewer via the client-server API. Read VaR Cult Matrix Space messages directly inside the terminal. No browser tab. No separate client. Trading discussion and chart analysis in the same window.

**Reddit r/WallStreetBets viewer** (`WSB` command) — hot posts with score and comment counts. No Reddit authentication required. Sentiment gauge for the degenerates. **20 out of 22 data sources** now integrated — only whale-alert (needs API key) and QuiverQuant (paid) remain.

**ADR-070: LAN-Lite client mode** — proposed architecture for lightweight clients that only download bars for viewed symbols instead of syncing the full 851-symbol cache. Reuses existing `RequestEntries`/`EntryData` protocol with a full vs lite toggle in Settings.

### Generalized MT5 XLSX Import — Any Server (2026-04-08, late)

The XLSX trade history import is no longer Darwinex-only. The import pipeline now accepts XLSX exports from **any MT5 server** — OANDA, Forex.com, IC Markets, Pepperstone, any broker running MetaTrader 5. Core analytics (equity curves, P&L, streaks, correlation, monthly returns, hold time, position sizing) work for any server's export. Darwinex-specific features (VaR multiplier, FTP scanner, D-Score components, investor flow) remain labeled as Darwinex.

### Crypto Bar Merge + LAN Backfill Architecture Fix (2026-04-09)

**W1/MN1 bar merge fix:** weekly bars now snap to Monday 00:00 UTC (was dividing by `7*86400000` which misaligned week boundaries). Monthly bars snap to 1st-of-month 00:00 UTC (was dividing by `30*86400000` which doesn't match real months). This caused duplicate bars from different sources appearing at slightly different timestamps within the same week/month — Kraken and CryptoCompare would each produce a bar for the same period but with timestamps a few hours apart. Both duplicates are now eliminated.

**Bar sanity filter:** reject bars with negative, zero, or NaN prices, and bars where high < low. Catches malformed data from APIs before it enters the cache.

**LAN crypto backfill architecture finalized:** the server is the single source of truth for crypto data. Server runs periodic Kraken/CryptoCompare fetches for its active chart. The LAN client sends `FETCH_BARS` to the server (forwarded via LAN protocol), then triggers `LanResyncBars` for fast delivery. Server's `FETCH_BARS` handler detects crypto symbols and routes through `KrakenBackfill` (works on weekends without Alpaca). Client never hits Kraken/CC APIs directly.

**LAN client demand forwarding:** clients no longer write a local `demand.txt`. Instead, the client's symbol list is forwarded to the server via KV (`client:demand`). On session save, the server reads `client:demand` from its KV cache and merges those symbols into its own `demand.txt` for BarCacheWriter. Result: BarCacheWriter re-exports symbols that ANY machine in the LAN is actively viewing — not just the server's charts.

### BARDATA: Full History Download + Multi-Broker Fetch (2026-04-09, cont.)

**`BARDATA` command** — download ALL available bars from every connected broker in one command. `get_all_bars()` paginates from 2015 (equities) or 2000 (crypto) to present with progress reporting. Handles Alpaca rate limiting, monthly aggregation from weekly, crypto symbol normalization. Stores in cache, triggers chart reload. ADR-071 documents the feature.

The command also pulls from **tastytrade** — DXLink historical bars plus the option chain for the symbol. One command, all brokers, all available data.

**tastytrade sandbox fix:** sandbox URL updated from `api.cert.tastyworks.com` to `api.cert.tastytrade.com` (rebrand). Session saves on Settings close so `tt_sandbox` persists immediately. UI labels renamed TT → Tasty.

**Negative price elimination (two passes):** bar sanity filter moved outside crypto-only block — now runs on ALL bars unconditionally. Added filter at cache read time (primary + gap-fill sources) to reject bad bars before merge. Also fixed the source: `aggregate_to_monthly` in both Kraken and CryptoCompare now skips zero/negative price daily bars during aggregation. Combined with load-time filtering, negative prices can never appear on any chart.

**BARDATA expanded: ALL symbols × ALL timeframes × ALL brokers.** One command now collects symbols from chart tabs, watchlist, DARWIN positions, Alpaca positions, and tastytrade positions. For each symbol: Alpaca full history (D1/W1/H1/H4/MN1), Kraken + CryptoCompare for crypto, tastytrade DXLink bars + option chains. Builds the complete cache in a single invocation.

**Symbol Explorer LAN client:** shows `cached (local)` label on LAN clients. Per-symbol sync button (📥) requests all 9 timeframes from the server and triggers `LanResyncBars` for fast delivery. Tooltips on all buttons (Load chart, Add to watchlist, Sync from server).

**Smart BARDATA:** skips fully-cached symbols (>100 bars = sufficiently cached), prioritizes uncached first. Checks cache for existing symbol:TF combos before fetching. Crypto routes through Kraken + CryptoCompare only (not Alpaca). Stocks/forex use Alpaca. Only fetches missing TFs per symbol. Reports queued vs skipped counts — no redundant API calls on repeat runs.

**Zero API calls on LAN clients and before cache loads.** Every periodic fetch path now has two guards: `is_lan_client` (server/standalone only) and `cache_loaded` (no calls until cache is ready). Periodic crypto fetch, weekend crypto sync, watchlist quotes — all gated. LAN clients get all data from the server via KV sync. No rogue API calls on startup, no rate limit hits before the terminal is ready, no duplicate fetches from client machines.

### Symbol Explorer: 8,000+ Crypto Universe + Kraken Broker ADR (2026-04-10)

**Symbol Explorer crypto expansion:** fetches the full CryptoCompare universe on open — **8,000+ coins** with full names (e.g. "Solana", "Monero", "Monero"). Dynamic list with filter search, `[cached]` tag for already-downloaded symbols. Top 200 shown by default, filter narrows to 500 max. Replaces the hardcoded 48-coin list. Click to load chart, +WL to add to watchlist, sync button for LAN clients. Works on both server and client.

**Expanded crypto detection:** XMR, ZEC, DASH added to crypto detection + Kraken pair mapping (`XXMRZUSD`, `XZECZUSD`). SHIB, APE, ARB, OP, HBAR, VET, THETA, AXS added to Kraken pairs. XMR data available from CryptoCompare (2014+) and Kraken.

**ADR-072: Kraken as full broker** — proposed 3-phase integration: authentication + account info, order placement, WebSocket streaming. US-friendly, real-time, 200+ crypto pairs. Would make Kraken the third trading broker alongside Alpaca and tastytrade.

**Multi-broker symbol search:** autocomplete now queries Alpaca (12K+ symbols), tastytrade (via `search_symbols` API), and CryptoCompare (48 popular coins) in parallel. Results show source tag `[Alpaca]`/`[tastytrade]`/`[CryptoCompare]`. Deduplicates across brokers. Type any ticker and see every broker that offers it — one search bar, three data sources.

### Kraken Broker: Live Trading From the Terminal (2026-04-10, cont.)

**Kraken is now the third trading broker** alongside Alpaca and tastytrade. ADR-072 Phase 1+2 complete:

- **Full REST API with HMAC-SHA512 authentication** — balance, open orders, open positions, place order (market/limit/stop), cancel order, tradeable pairs (public endpoint)
- **Native UI wired** — Settings panel with API key/secret + connect button, Kraken option in broker selector dropdown, auto-connect on startup, keyring persistence
- **Order placement functional** — market and limit orders from the Order Entry panel, cancel from the Orders panel
- **Symbol search integration** — Kraken tradeable pairs merged into multi-broker autocomplete
- **6 new tests** for the Kraken API module. **618 total tests.**

Three brokers. One terminal. Alpaca for US equities/options/crypto. tastytrade for options/futures. Kraken for 200+ crypto pairs with real-time trading. All three share the same risk engine, the same chart, the same order entry panel.

### BARDATA Progress Window + Rate Limiting (2026-04-10, final)

**BARDATA progress window:** green progress bar, stats grid (total/queued/completed/skipped), scrollable activity log. Opens automatically on `BARDATA` command. FetchAllBars now runs sequentially (not parallel spawned) to respect Alpaca rate limits.

**CryptoCompare rate limiting fixed:** retry with exponential backoff (10s/20s/30s) instead of immediate abort. Body-level rate limit returns partial data instead of error. BARDATA includes full Alpaca universe + Kraken tradeable pairs.

**Cleanup pass:** dead LAN client code path removed from periodic fetch (outer guard already blocks). Crypto symbol normalization in BARDATA (strip slashes). CryptoCompare limited to H1+ timeframes in BARDATA (sub-hourly has 7-day history limit). Forming bar synthesis cache key slash-stripping fixed.

### BARDATA Optimization, DELETE_DARWIN, MT5 Sync Fix (2026-04-06+)

**BARDATA v2:** cache threshold dropped from 100→0 bars (any cached data = skip). Uses incremental `FetchBars` (1,000 bars) instead of `FetchAllBars` (full history from 2000). **Stop button** in the BARDATA progress window to cancel mid-run. `demand.txt` v2 format with timestamps for cache freshness tracking.

**DELETE_DARWIN command:** delete a single DARWIN/MT5 account and all its data — deals, positions, equity snapshots. Usage: `DELETE_DARWIN CKUC`. Also available via delete button in the account detail panel. Returns row count for confirmation.

**Yahoo scrape failures blocklist:** `scrape_failures` SQLite table records symbols that return 404/Not Found from Yahoo Finance. On subsequent `EVSCRAPE` runs, failed symbols are silently skipped — no wasted API calls. Persists across sessions.

**MT5 sync regression check removed:** the check was blocking new bars after reboot. BarCacheWriter caps at 10K bars per export, but the terminal cache had 100K from pre-reboot exports. The regression check saw 10K < 50K (100K/2) and refused ALL updates. Now accepts any source with newer timestamps. BarCacheWriter handles its own integrity.

**The terminal now manages all 6 active DARWINs simultaneously** — TyphooN uses the cross-DARWIN correlation matrix, symbol overlap heatmap, and portfolio VaR tools to juggle correlation and optimize profits across all accounts in real-time. The DARWINS command shows combined portfolio analytics. The DARWIN command shows per-account detail. One terminal, six accounts, zero spreadsheets.

**SwapHarvest — Positive Swap Scanner:** Scans every symbol on the broker and identifies instruments with positive swap in either direction. 890 symbols scanned, 827 with positive swap found — 807 on the short side. Filters by direction (Long/Short/Both), sorts by best swap rate, shows spread, min lot, margin, and full description. Export to CSV for analysis. The Short King's shopping list, generated in seconds.

![SwapHarvest — TyphooN-Terminal Positive Swap Scanner: 827 symbols with positive swap across 890 scanned](/img/swapharvest-scanner-20260407.webp)

**848 total commits. ~66,500 LOC. 618 tests. Zero warnings.**

### WASM Web Client: Phone Access Over LAN (2026-04-12)

Three new crates bring TyphooN-Terminal to your phone:

- **web-protocol** — shared serializable `WebCmd`/`WebMsg` types between server and client
- **web-server** — axum HTTPS + WebSocket relay with self-signed TLS
- **web** — eframe 0.34 + glow WebGL2 thin client compiled to WASM

The `WEBSERVER` console command starts an HTTPS server on port 9848, serves the WASM bundle, and bridges WebSocket connections to `BrokerCmd`/`BrokerMsg` channels. Open `https://your-ip:9848` on your phone and get:

- **Account tab** — balance, equity, margin, buying power
- **Positions tab** — all open positions with P&L
- **Orders tab** — pending orders with status
- **Chart tab** — basic chart with auto-refresh

Read-only Phase 1 — no order placement from the phone. The server bridges all data from the native terminal's broker connections. No API keys needed on the phone. No app install. Just a browser and a LAN connection.

The crate count goes from 4 to **7** (engine, native, cli, mql5-compiler, web, web-protocol, web-server).

### Rich UI: SwapHarvest + DarwinexRadar Windows (2026-04-10+)

**SwapHarvest UI** — the positive swap scanner got a full floating window:
- Sortable grid with direction filters (Long/Short/Both)
- Symbol search with instant filtering
- Color-coded swap values (green positive, red negative)
- Gold-highlighted best-swap column
- Export CSV button

**DarwinexRadar UI** — full symbol browser for all 851 Darwinex instruments:
- Sector/industry columns
- Trade mode indicators (close-only detection)
- Swap rates and margin data
- Export to MarketWizardry.org as semicolon-delimited CSVs

Both open via console command or Darwin panel button.

**DARWINEXRADAR Changelog:** compares current MT5 specs against a previous snapshot stored in KV — detects new/removed symbols, swap changes, spread changes, and trade mode changes (close-only). Exports changelog to `/home/typhoon/git/MarketWizardry.org/darwinex-radar/` for web publishing. Displayed as a collapsible section with color-coded change types.

### Fundamentals Scrape: Source Settings + Status Dashboard (2026-04-10+)

**Symbol source settings:** MT5/Alpaca/TastyTrade checkboxes control which broker's symbols are scraped for fundamentals. Previously it was scraping all 12K Alpaca symbols even when only MT5 was selected — the fix filters to `mt5:` prefixed keys only, reducing Darwinex scrapes from 12K to ~800 symbols.

**Scrape Status dashboard** (`SCRAPESTATUS` command): unified view with live progress bars, color-coded status indicators (idle/running/done/error), and action buttons for Fundamentals, SEC Filings, DarwinIA FTP, and Crypto Backfill. Tracks OK/fail/cached counts with progress percentage. Inline source selection in the dashboard.

### CRYPTOCOMPARE Console Command (2026-04-10+)

`CRYPTOCOMPARE DOGEUSD` — downloads all timeframes (1Min→1Month) at full depth from CryptoCompare with Kraken gap-fill. One command, one symbol, all timeframes backfilled. Handles rate limits and partial data gracefully.

### LAN Sync Audit: 7 Bug Fixes (2026-04-11)

A comprehensive audit of the LAN sync pipeline fixed 7 bugs:

1. **Dead `total_received` counter** — now tracks entries and validates against server batch count
2. **`bytes_sent` tracked actual bytes** — was counting entry count, not byte count
3. **KV batch uses `mem::replace`** — eliminates unnecessary clone on hot path
4. **Client IP cleanup on all early-exit paths** — WS/auth/send failures now properly clean up
5. **No-progress + zero-key guards** — all 5 binary parsing loops protected against infinite loops
6. **30s TLS handshake timeout** — prevents hung connections from blocking the sync pipeline

**KV log noise reduction:** 0-entry re-sync messages downgraded from info to debug level. Only logs info when entries are actually received.

### SWAPHARVEST Fix: 10→851 Symbols (2026-04-10)

The `__SPECS__` query used `LIMIT 1` which grabbed the smallest MT5 account (10 symbols) instead of the CFD account (851 symbols). Fixed: now merges ALL `__SPECS__` entries across all MT5 accounts, deduplicating by symbol. The same bug affected `export_radar_txt`.

### Updated Stats (2026-04-12)

| Metric | 2026-04-08 | 2026-04-12 |
|---|---|---|
| **LOC** | ~66,500 | **~68,400** |
| **Commits** | 848 | **861** |
| **Tests** | 618 | **621** |
| **Crates** | 4 | **7** (+ web, web-protocol, web-server) |
| **Console commands** | 115 | **118+** |

| Crate | Purpose | Lines of Rust |
|---|---|---|
| **engine/** | Broker APIs, SQLite cache, indicators, DARWIN analytics, SEC scraper, risk engine | ~25,800 |
| **native/** | egui + wgpu native GPU application, all UI, GPU compute shaders, 110+ floating windows | ~35,300 |
| **cli/** | Standalone TUI (ratatui, SSH-ready, 6.5MB binary) | ~2,300 |
| **mql5-compiler/** | pest parser → AST → IR → WGSL codegen for custom MQL5/PineScript indicators | ~4,500 |
| **web/** | eframe + glow WASM thin client for phone/browser access | ~400 |
| **web-protocol/** | Shared WebCmd/WebMsg serializable types | ~90 |
| **web-server/** | axum HTTPS + WebSocket relay with self-signed TLS | ~110 |
| **Total** | **100% Rust. Zero JavaScript. Phone access via WASM.** | **~68,400** |

**861 total commits. ~68,400 LOC. 621 tests. 7 crates. Zero warnings.**

![Tome approves: lossless webp across the entire site. Peak efficiency.](/img/tome-approves-webp-20260406.webp)

*Tome has inspected the webp metadata. Lossless compression for a grin. Peak efficiency. All PNG content images across MarketWizardry.org have been converted to lossless webp via `cwebp -lossless`. Apple-touch-icons remain PNG (browser requirement). Every screenshot, every chart, every Tome hoot — webp. The owl has spoken.*

-- TyphooN

---

> **DISCLAIMER:** TyphooN-Terminal is open-source software provided as-is under the BSL (Business Source License) license. It is NOT financial advice and NOT a recommendation to trade. Trading involves substantial risk of loss. The software executes orders as instructed -- it does not and cannot guarantee profitable outcomes. Use at your own risk. Test thoroughly in paper trading before risking real capital. The author actively trades using this software and holds positions mentioned in this blog. Prop firm information is current as of March 2026 and may change -- verify directly with each firm before funding an account.
