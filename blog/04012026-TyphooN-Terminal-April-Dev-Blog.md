## TyphooN-Terminal: April Dev Blog — Post-Launch Iteration at 40+ Commits/Day

> **Continuation of the [March launch post](03192026-TyphooN-Terminal-Record-Pace.html).** The initial 4.7-day sprint shipped a functional GPU trading terminal. This post tracks April's work: LAN sync parity, drawing tools UX, MQL5→WGSL Phase 2, SEC EDGAR deep integration, multi-broker expansion (tastytrade, Kraken), the cross-language transpiler matrix, the allocation audit (mimalloc + max release profile), the full-repo O(1) sweep, and the end-of-month MT5 sync pipeline rewrite (v3-only demand.txt, cache-wide self-heal, 100K-bar integrity target, 3-part key canonicalization). Updates run chronologically. Monthly format: each month gets its own dev blog going forward.

---

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

**LAN crypto backfill architecture finalized:** the server is the single source of truth for crypto data. Server runs periodic Kraken/CryptoCompare fetches for its active chart. The LAN client sends `FETCH_BARS` to the server (forwarded via LAN protocol), then triggers `LanResyncBars` for fast delivery. Server's `FETCH_BARS` handler detects crypto symbols and routes through `KrakenBackfill` (works on weekends without Alpaca). Client never hits Kraken/CryptoCompare APIs directly.

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

### WASM Web Client Security Hardening (ADR-073)

The WASM web client shipped read-only but still needed hardening before exposing it on a LAN. ADR-073 documents the full security pass:

- **Passphrase authentication** — shared with LAN sync. Login screen on phone before any data flows
- **Rate limiting** — 20 commands/second per client. Prevents abuse from rogue scripts
- **Connection limits** — 10 max clients total, 3 per IP address. No DDoS from a single device
- **64KB message cap** — prevents memory exhaustion from oversized payloads
- **10-second auth timeout** — unauthenticated connections are dropped if they don't send credentials
- **Input validation** — symbol and timeframe allowlists, path traversal blocked. No arbitrary strings reach the backend
- **`deny_unknown_fields`** on all serde types — malformed JSON is rejected at the protocol level
- **Broadcast lag handling** — slow clients get dropped instead of backing up the server's send queue
- **`/health` endpoint** — for monitoring without authentication

**7 new protocol tests** covering auth flow, rate limits, message validation, and connection lifecycle.

### Updated Stats (2026-04-12)

| Metric | 2026-04-08 | 2026-04-12 |
|---|---|---|
| **LOC** | ~66,500 | **~68,900** |

| **Commits** | 848 | **883** |
| **Tests** | 618 | **628** |
| **Crates** | 4 | **7** (+ web, web-protocol, web-server) |
| **Console commands** | 115 | **118+** |

| Crate | Purpose | Lines of Rust |
|---|---|---|
| **engine/** | Broker APIs, SQLite cache, indicators, DARWIN analytics, SEC scraper, risk engine | ~25,800 |
| **native/** | egui + wgpu native GPU application, all UI, GPU compute shaders, 110+ floating windows | ~35,300 |
| **cli/** | Standalone TUI (ratatui, SSH-ready, 6.5MB binary) | ~2,300 |
| **mql5-compiler/** | pest parser → AST → IR → WGSL codegen for custom MQL5/PineScript indicators | ~4,500 |
| **web/** | eframe + glow WASM thin client for phone/browser access | ~500 |
| **web-protocol/** | Shared WebCmd/WebMsg serializable types with auth + validation | ~220 |
| **web-server/** | axum HTTPS + WebSocket relay with TLS, rate limiting, passphrase auth | ~290 |
| **Total** | **100% Rust. Zero JavaScript. Phone access via WASM.** | **~68,900** |

### Price Scale Drag Fix + DARWIN Delete UX (2026-04-12, late)

**Price scale drag regression fixed:** price axis Y-drag was blocked by a `pointer_over_window` guard that prevented drag initiation on price axis clicks. Fix: price axis drags bypass the window check while chart panning still respects it. Release condition no longer cancels active drags when `pointer_over_window` is true.

**DARWIN delete with KV blacklist:** X button added per row in the DARWIN Accounts grid. Deletion writes a `darwin:deleted:TICKER` KV blacklist entry so LAN sync's `import_darwin_data` skips re-importing deleted tickers. Previously, deleted DARWINs would reappear on the next LAN sync cycle.

**DARWIN delete UI freeze eliminated:** the SQL DELETE ran on the UI thread and blocked when LAN sync held the DB write lock. Now uses a three-step non-blocking pattern: 1) immediately remove from in-memory state (instant UI update), 2) write KV blacklist (fast), 3) spawn SQL DELETE on a background thread. Both the console `DELETE_DARWIN` command and the grid X button use the same pattern.

### Fundamentals Scraping Improvements + SEC Fix (2026-04-13)

**Per-broker scrape buttons:** the Scrape Status Dashboard now has MT5 Only, Alpaca Only, TastyTrade Only, and All Sources buttons. No more scraping 12K Alpaca symbols when you only want Darwinex data.

**Yahoo 404 permanent caching:** symbols that return 404 from Yahoo Finance are permanently recorded in the `scrape_failures` table and skipped on all future runs. Rate limit (429) detection with 60-second cooldown and auto-retry.

**SEC scrape fix:** was querying `kv_cache` (wrong table) for MT5 symbols — now queries `bar_cache` with correct key parsing (`mt5:CC:SYMBOL:tf`, index 2). SEC filings now correctly resolve to Darwinex stock symbols.

**DARWIN delete blacklist hardened:** blacklist now filters the background thread account list AND LAN client KV-loaded `account_details`, preventing deleted DARWINs from reappearing via any sync path.

### Win Rate Double-Multiply Bug Fix (2026-04-13)

The engine stores `win_rate` as 0–100 (percentage), but every analytics UI was multiplying by 100 again — showing 3,281% instead of 32.8%. Fixed in: DARWIN Accounts grid, P&L Attribution, Backtest Results, Backtest log message, and Optimization Results grid. Thresholds corrected from 0.5 to 50.0. Only `oos_win_rate` (0–1 format) correctly keeps the `* 100` multiplier.

### Analytics Calculation Bug Fixes (2026-04-13, cont.)

Six analytics formulas corrected after audit:

- **Tail ratio:** use `abs()` on both numerator and denominator (p95 could be negative)
- **Kurtosis:** apply sample-corrected excess kurtosis formula (Fisher adjustment) instead of population kurtosis
- **Profit factor:** cap at 999.0 instead of `f64::INFINITY` (prevents JSON/DB serialization issues)
- **D-Score:** clamp all 6 components to [0,10] and total to [0,100]
- **Sortino:** return 99.0 for perfect records (positive returns, zero downside deviation) instead of 0
- **Calmar:** return 99.0 for zero-drawdown strategies instead of 0

### Security Hardening + DARWIN AuM Input + ADRs 074–077 (2026-04-13, late)

**Zeroize Kraken API secret:** the API secret now uses `Zeroizing<String>` — memory is overwritten with zeros when dropped. Prevents secrets from lingering in memory after use.

**Input validation hardened:** ticker format validated before Yahoo Finance URL construction (prevents injection). CIK validated as numeric-only before SEC EDGAR URL construction. Both prevent SSRF via malformed user input.

**DARWIN AuM input:** editable per-DARWIN AuM (Assets under Management) field in the Accounts grid. Values persist to KV cache (`darwin:aum:TICKER`) and auto-sync to LAN clients. Enables accurate portfolio-level AuM tracking without manual spreadsheets.

**Four new ADRs:**
- **ADR-074:** Notification System architecture
- **ADR-075:** SwapHarvester automated strategy
- **ADR-076:** DarwinexRadar symbol lifecycle tracking
- **ADR-077:** Screener Framework for multi-factor filtering

### Performance Optimizations (2026-04-13, final)

Three hot-path optimizations:

- **Correlation matrix:** pre-compute per-series mean/variance in a single pass, then single-pass covariance per pair (was 5 passes). Self-correlation short-circuits to 1.0. Pre-allocate result `Vec`. Significant speedup on 6-DARWIN correlation computations.
- **DARWIN import:** wrap all DELETE+INSERT in a single transaction (`BEGIN IMMEDIATE`/`COMMIT`) for ~20–40x speedup on 46K deals. Use `prepare_cached()` for deal/position statements (eliminates per-row query planning). `HashSet` for O(1) blacklist lookups (was O(n) per row).
- **GPU indicator upload:** single-loop bar extraction with pre-allocated `Vec`s (was 4 separate `collect()` passes). Reduces allocations on every chart render.

### LAN Client Watchlist Fix + SEC Scrape Key Parsing (2026-04-14)

**LAN client watchlist overwrite fix:** the server was syncing its `broker:watchlist` rows to the client, overwriting client-side edits. Now the LAN client filters server-synced watchlist rows to only show symbols that exist in the local `user_watchlist`. Server data supplements but never replaces client edits.

**SEC scrape 0 results fix:** `bar_cache` keys have two formats — 3-part (`mt5:SYMBOL:TF`) and 4-part (`mt5:CC:SYMBOL:TF`). The previous fix assumed 4-part keys (`parts[2]`), which returned the timeframe instead of the symbol for 3-part keys. Now handles both formats correctly.

**Hardcoded path removed:** darwin radar export path replaced `/home/typhoon/` with `$HOME`-based resolution. Portable across machines.

**ADR updates:** ADR-054 (scrape_failures blocklist, 429 cooldown, per-broker buttons), ADR-057 (cross-references to ADR-075/076), ADR-064 (security hardening, performance optimizations, analytics fixes from 2026-04-07/08).

### Extended Hours Quotes — Yahoo Finance + SIP Feed (2026-04-14+)

**Pre-market and after-hours quotes now match TradingView.** Alpaca's snapshot endpoint was using the IEX feed, which only reports regular session trades — pre-market and after-hours prices showed stale closing data. The fix evolved through three iterations:

1. **Switched Alpaca snapshot to SIP feed** — gets real extended hours trade data from the consolidated tape
2. **Finnhub enrichment (attempted)** — Finnhub's `/quote` endpoint returns regular session close as current price, making it useless for pre/post market. Removed.
3. **Yahoo Finance v7 batch quotes (final)** — `v7/finance/quote` returns explicit `preMarketPrice` and `postMarketPrice` fields. All equity symbols in one HTTP call (no per-symbol rate limiting). During pre-market: Last/Chg/Chg% show pre-market price, Ext% shows change from regular close to extended price. During regular hours: uses Yahoo `regularMarketPrice` as fallback if fresher than Alpaca.

The watchlist now shows a dedicated **Ext%** column with extended hours change percentage. Last/Chg/Chg% columns switch to extended hours data when available. Positions panel reflects the same pricing.

**Collapsible Recent Fills:** defaults to collapsed with trade count in header. Moved from nested inside Positions to sibling level — aligns with Positions/Orders/Watchlist collapsible headers.

### Yahoo Finance Session + Watchlist Hardening (2026-04-08)

**Yahoo Finance authenticated session:** bare `reqwest` client was getting 401/empty responses from Yahoo. Now creates a `YahooSession` with consent-bypass cookies + crumb token — same auth flow as the fundamentals scraper. Session cached across poll cycles and recreated every 30 minutes (was creating 2 auth HTTP calls per poll).

**Watchlist poll interval: 15s** (was 1s). Combined with session caching, Yahoo API calls dropped from ~180/min to ~4/min.

**LAN client watchlist skip:** clients no longer fire Alpaca/Yahoo API calls for watchlist data — it arrives via KV sync (`broker:watchlist`) from the server. Zero wasted calls on machines with no broker connection.

**Volume column fixed:** `regularMarketVolume` added to Yahoo fields param. Handles both integer and nested JSON formats.

**Correlation matrix fix:** values were exceeding [-1, 1] (e.g. -1.1478). The previous optimization pre-computed variance over all dates per series, but covariance was computed over common dates only — mismatched denominators. Now computes mean, variance, and covariance all over the same common-date pairs in a single pass. Result clamped to [-1, 1].

### Extended Hours Magenta Candle + Active Only Filters (2026-04-08)

**Extended hours magenta candle on chart.** When pre/post market data is available from Yahoo Finance, the terminal draws a magenta candlestick after the last regular bar — open is the regular session close, high/low/close tracked from extended price updates. A magenta dashed price line sits at the extended close price with a labeled price tag on the Y-axis. During regular hours, falls back to a ghost candle placeholder. Matches TradingView extended hours visualization.

**Active Only filter on all research windows.** Every informational window that displays per-symbol data now has an **Active Only** checkbox that filters to symbols currently in charts, positions, or watchlist. Applied to: Earnings Calendar, Dividend Calendar, EV Scanner, Congressional Trades, Unusual Volume Scanner, SEC Filing Scanner. All use a shared `active_symbols()` helper that returns the unique set of chart symbols + position symbols (ticked brokers) + watchlist.

**Fundamentals window shows all MTF grid charts + open positions.** When MTF grid is enabled, the Fundamentals window displays data for ALL chart symbols (not just the active tab). Also includes position symbols from ticked brokers (Alpaca, TastyTrade). Scrape All button for batch refresh. Each symbol gets its own collapsible section with company info, valuation, ratios, earnings/dividends, quarterly financials, and institutional holders.

### LAN Sync Bandwidth Optimization (2026-04-08)

**Forced reconnect interval: 2 hours** (was 15 minutes). The previous 15-minute interval was doing a full initial sync — 45K deals, 30K positions, 10-30MB — every cycle, when the incremental 30-second re-sync already handles updates. Re-sync interval also relaxed to 30s (was 15s). Massive bandwidth reduction for multi-machine setups.

**launch.sh improvements:** auto-installs `wasm32-unknown-unknown` target before WASM build (survives `rustup toolchain` updates). Auto-builds WASM web client if sources changed — checks if `web/src/*.rs` or `web-protocol/src/lib.rs` are newer than `target/web-dist/index.html`. Skips if trunk not installed or already up-to-date. `./launch.sh web` for force rebuild.

### Options Pricing Engine + Greeks (2026-04-08)

**Black-Scholes options pricing engine.** New `engine/src/core/options.rs`: full Black-Scholes pricing, Greeks (Delta, Gamma, Theta, Vega, Rho), Newton-Raphson implied volatility solver, put-call parity verified. The Option Chain window expanded from 3 columns (Strike/Call/Put) to 7 columns with Delta, Gamma, Theta, Vega per strike. Uses spot price from watchlist and days to expiry from the chain date. 8 new tests (BS pricing, Greeks call/put, put-call parity, IV roundtrip, edge cases).

### Drawing Tools Complete + Zero Unwrap Policy (2026-04-08)

**ADR-068 complete — all drawing tool items done.** Hit-testing added for Pitchfork (3-point segment distance), Ellipse (normalized elliptical distance), GannFan (origin point), FibCircle/FibSpiral (circle border distance), FibWedge (3-point segment distance). Drag handles: control points now draggable — click near handle to resize a single point, click elsewhere for whole-drawing drag. Cross-timeframe drawings: TF toggle button in toolbar syncs HLines (price-based, TF-independent) across all charts with the same symbol.

**Zero unwrap/expect policy enforced across production code (ADR-082).** Replaced all `.expect()` in broker init (Alpaca, Kraken, notifications) with `.unwrap_or_else` fallbacks. Fixed `darwin.rs` `returns.last().unwrap()` → `.map().unwrap_or()`. Fixed `fundamentals.rs` `enterprise_value.unwrap()` → `if let Some(ev)`. Timezone `.expect()` → `.unwrap_or(UTC)`. Tokio runtime `.expect()` → `process::exit(1)` on fatal. All remaining `unwrap/expect` are exclusively in `#[test]` functions.

### Analytics Expansion — ADR-083 (2026-04-08)

**Relative Strength Ranking:** `compute_relative_strength()` ranks symbols by price performance over a configurable lookback period. Sorted by return%, ranked 1=strongest.

**Portfolio Metrics:** Treynor Ratio `(return-rfr)/beta` and Jensen Alpha (CAPM excess return) added to `BenchmarkComparison` struct using 4% risk-free rate.

**Symbol Correlation Matrix:** `compute_symbol_correlation_matrix()` — N×N Pearson correlation from close price series, configurable window, single-pass mean/var/cov, clamped [-1,1].

**Volume Profile — Initial Balance (IB):** detects session start, computes first-hour high/low/range.

**GPU Monte Carlo VaR dispatch:** `run_monte_carlo_gpu()` uploads historical daily returns, runs N parallel simulations (256 threads/workgroup) via PCG hash RNG on GPU, returns sorted final equity values. Uses the existing `MONTE_CARLO_SHADER` (PCG random walk, days_forward horizon, starting_equity). GPU backtester `evaluate()` and `evaluate_nnfx()` already fully implemented — no changes needed. ADR-083 complete: only Market Breadth + Put/Call Ratio remain (blocked on external data feeds).

### Dependency Audit + Optimization (2026-04-08)

**Dependency unification: 45→19 duplicate crates.** Force-unified `tokio-tungstenite` 0.29→0.28 (match axum), `zip` 8→7 (match calamine), `rand` 0.10→0.9 (match tungstenite). Remaining 19 duplicates are deep transitive (Wayland toolkit, prometheus→protobuf→thiserror, crypto stack transition) — unfixable without replacing upstream crates. `cargo audit`: 0 vulnerabilities.

**UX improvements:** watchlist right-click context menu with Chart/Remove options. Trading button tooltips on Destroy Lines, Open MG, Close Partial. MACD periods configurable via UI DragValue. GPU health status in Help window. Indicator Vec reuse (clear+reserve+push instead of new Vec per compute).

### 7 New Analytics Modules (2026-04-08)

**HV Cone:** Historical Volatility Cone with percentile rank at 10/20/60/252-day windows — shows where current IV sits relative to historical distribution.

**Sector Heatmap:** aggregates symbols by sector for visual performance overview.

**Earnings Surprise:** actual vs estimate percentage — flags beats and misses.

**Dividend Yield Screener:** filters and ranks by yield.

**MTF Confluence Score:** multi-timeframe signal agreement scored from -1 (full bearish) to +1 (full bullish).

**Stat Arb Pairs:** z-score + half-life for mean-reversion pair identification.

**Risk Budget:** marginal VaR decomposition — shows each position's contribution to total portfolio risk.

8 new tests across all modules.

**All 7 analytics wired into UI windows with console commands:** `HV_CONE` (volatility cone with percentile rank grid), `SECTOR_HEATMAP` (sector aggregates from fundamentals data), `DIVSCREEN` (dividend yield screener ranked by yield), `CONFLUENCE` (MTF RSI/MACD/SMA200/KAMA signals per chart), `STAT_ARB` (correlated pairs with z-score signals), `RISK_BUDGET` (marginal VaR contribution per DARWIN). All accessible from the terminal console.

### Test Gap Fill — 499→682 Tests (2026-04-09)

**Test coverage hardened across core engine modules:** VaR (5→12 tests), risk (5→10), margin (8→12), options (10→18). New tests cover: VaR edge cases (insufficient data, 99%>95% ordering), `std_dev` edge cases, inverse normal at 50th/99th percentile, risk lots with zero SL/equity/VaR, lot normalization, margin urgency at threshold, deep ITM/OTM Greeks, IV put roundtrip, vega always positive, gamma highest ATM. Paranoia over assumptions — every edge case that could silently corrupt a live trade gets its own test.

### Ext-Hours Candle Fix + Event Calendar + DARWINVAR/EVOUTLIERS (2026-04-09)

**Magenta candle finally renders.** Two bugs: `next_x = chart_rect.right() + 0.5*bar_w` placed the candle past the right edge so the bounds guard always failed — clamp flush to right edge instead. Second bug: `ext_price = prev_close * (1 + ext_change_pct/100)` used the wrong base — `ext_change_pct` is measured against intraday `reg_price`, not `prev_close`. Use `row.last` directly (already set to ext price by Yahoo enrichment).

**New single-dimension outlier scanners:** `DARWINVAR` runs IQR detection on `per_darwin_var.var_95` and flags Darwinex corridor violations (3.25%–6.5%). `EVOUTLIERS` runs IQR on `fundamentals.enterprise_value` grouped by sector. **Event Calendar** aggregates upcoming earnings / ex-div / div-pay dates from fundamentals, tagged per-broker (Alpaca/Darwinex/Tasty) with source + type filters in a new egui window. `DIVEXPLORER` is a preset entry point (Darwinex + dividends only). ADR-084 documents.

### Broker Scope Filter + ForexFactory Calendar + GPU Buffer Reuse (2026-04-09)

**New `SCOPE [ALL|ALPACA|DARWINEX|TASTY]` command** with `broker_scope_symbols` / `scoped_fundamentals` helpers threaded through OUTLIERS / EVOUTLIERS / SectorHeatmap / DivScreener. Per-command overrides on `ALPACAOUTLIERS` / `TASTYOUTLIERS` / `DARWINEXOUTLIERS`.

**ForexFactory XML parser** (`engine/core/econ_calendar.rs`, 7 tests) — keyless fallback when no Finnhub API key. Delivers impact / forecast / previous / currency. Dedup: `OUTLIERS` absorbs `DARWINEXOUTLIERS`, `EVENTS` absorbs `DIVEXPLORER` (handler aliases preserved).

**GPU:** Hoist `ind_out` / `ind_params` buffers to `GpuContext`, reuse across 31 indicator dispatches per frame instead of realloc. **Cache:** align `read_conn` `PRAGMA cache_size` to `-64000` (was `-32000`). **Unwrap cleanup (ADR-082):** web-server auth JSON, native main tokio init, cli chunk.last, web/src/lib DOM init, metrics.rs registry init now returns Result. ADR-085 documents.

### Perf Pass — O(1) LAN Remote Queue, Indexed Key Search (2026-04-09)

**`append_to_queue` + `drain_queue` replace the `lan:remote_queue` read-decompress-append-recompress-write pattern** which was O(n²) under burst load (9 FETCH_BARS arriving together). Now O(1) insert + single-transaction drain.

**`search_keys` uses SQL `LIKE` + timestamp index;** replaces 3 `detailed_stats` full-table scans in `app.rs` (symbol fallback lookup, HTF MA fallback, HTF KAMA fallback, Monday Kraken cleanup). Prevents the ADR-064 full-DB-scan frame stall regression. Log buffer cap 500→200 steady-state. `get_kv_raw` helper returns compressed blob without zstd decode — ready for future LAN pass-through paths. 5 new tests.

### UX Pass — Calendar UI, Staleness Badges, Alert Notifications (2026-04-09)

**Economic calendar:** impact + currency filters, actual/forecast/previous parsed columns, staleness badge, ForexFactory/Finnhub source tag, Majors preset.

**Live panel staleness:** `positions_last_update_ts` / `orders_last_update_ts` / `watchlist_last_update_ts`, `staleness_badge` helper, inline badges on right-panel collapsing headers with color escalation (fresh/stale/STALE).

**Alert breach badge:** top-bar red counter when indicator alerts fire, latest message as tooltip, click opens alert builder + clears. **Help window overhauled:** searchable filter, 3 sections (chart nav, app/window, command palette), 31 top commands documented, resize 720x560. **Order entry:** prefix-match autocomplete from `all_broker_assets` + watchlist, live validation (green=known, red=unknown w/hint), monospace font. ADR-086 documents.

### ADR-084/085/086 Follow-Ups — Help Auto-Gen, Session Persistence, ICS Export (2026-04-09)

**Help window now iterates `COMMANDS` registry directly** — no drift. `DRAW_*` commands moved to a collapsible sub-section. **Persistent broker scope button** in top bar — click to cycle ALL/ALPACA/DARWINEX/TASTY, color-coded. **`save/load_session` round-trip** `broker_scope` + `econ_filter_high/medium/low/holiday` + `econ_filter_currencies`. EV Scanner respects `broker_scope`; `EVSCRAPE` overrides `use_mt5/use_alpaca/use_tastytrade` flags based on active scope.

**Alert badge uses `ViewportCommand::RequestUserAttention(Critical)`** — no new crate dep, taskbar flash / dock bounce / titlebar flash cross-platform. **Event Calendar ICS export** via new `build_events_ics` helper (RFC 5545, all-day VEVENTs, proper escaping, stable UIDs). Export `.ics` button writes `~/typhoon_events.ics`. 6 new unit tests.

### ADR-069 Feature Gap Closure — Tasty Close, MT5 Auto-Sync, CP Drag Expansion (2026-04-09)

**Tastytrade `close_equity_position`** — looks up position, picks Sell/Buy to Close from `quantity_direction`, submits market order. `BrokerCmd::TastytradeClosePosition` dispatches. Close X button on each tasty position row with hover tooltip.

**`mt5_auto_sync` setting** (opt-in, persisted) fires `Mt5Sync` every ~5 min silently. Settings checkbox next to manual "Sync MT5 Data Now" button. **Watchlist context menu:** Move Up / Move Down / Move to Top.

**Drawing control point drag expanded:** FibChannel + all Vec-of-points patterns (Polyline, PathDraw, Brush, ElliottWave/Double/Triangle/TripleCombo, HeadShoulders, XabcdPattern, AbcCorrection, AbcdPattern, TrianglePattern, ThreeDrives, CypherPattern). Each point editable individually.

**Compound interest calc:** "Use My Equity Curve" button pre-fills principal + annual return from DARWIN portfolio CAGR when ≥30 days data. ADR-088 documents. Closes ADR-069 actionable items.

### EasyLanguage + thinkScript Compilers + Phone Order Entry (ADR-073 Phase 2) (2026-04-09)

**Third and fourth indicator-language compilers land.** `mql5-compiler/src/easylang.rs` — line scanner for TradeStation/MultiCharts PowerLanguage. `inputs`/`variables` blocks, case-insensitive keywords, `Plot1..N` with labels, built-ins mapped to common IR (`Average`→`ta_sma`, `XAverage`→`ta_ema`, `RSI`/`ATR`/`Highest`/`Lowest`/`StdDev`, `math_abs`/`sqrt`/`log`/`max`/`min`), arithmetic + comparison ops, `{}` brace + `//` line comments. 11 tests.

`mql5-compiler/src/thinkscript.rs` — line scanner for thinkScript. `input`/`def`/`plot` statements, `declare lower`/`upper` for `separate_window`, case-sensitive built-ins (`Average`/`ExpAverage`/`RSI`/`ATR`), `#` line comments, bool/int/float input classification. 12 tests. **Indicator Compiler dropdown now offers 4 languages.** Auto-detection by extension (`.el`/`.els` → EL, `.ts`/`.tos` → TS).

**Phone order entry (ADR-073 Phase 2):** 3 new `WebCmd` variants (`PlaceOrder`, `CancelOrder`, `ClosePosition`) + `WebMsg::OrderResult` + `is_valid_order_side`/`type`/`qty` helpers + `MAX_ORDER_QTY` constant. 8 new web-protocol tests. Per-variant validation in web-server dispatch loop — symbol/qty/side/type/price/broker whitelists, invalid commands dropped with `tracing::warn!`. Native `WebCmd` drain relays `PlaceOrder` to `AlpacaMarketOrder`/`LimitOrder`/`StopOrder` or `TastytradeEquityOrder`, `CancelOrder` → `AlpacaCancelOrder`, `ClosePosition` → `ClosePosition` or `TastytradeClosePosition`. `OrderResult` reply broadcast back. Local log mirror so operator sees every web-originated order. **728 total tests pass** (131 compiler + 497 engine + 78 native + 22 web-protocol). ADR-089 documents. Closes the last two explicitly-deferred items from ADR-069/073.

### Phone WASM Trade Tab — Place/Cancel/Close from Any LAN Browser (2026-04-09)

**ADR-089 follow-up — phone can now trade.** `web/src/app.rs` Trade tab wires the `PlaceOrder`/`CancelOrder`/`ClosePosition` protocol commands into the WASM client. Broker dropdown (alpaca/tastytrade), symbol, side, type (market/limit/stop), qty, conditional limit/stop price fields. **Inline validation mirrors the server whitelist** — client-side rejection before bytes hit the websocket, so typos never reach the dispatch loop. **Two-step review-then-send confirm** — stray tap can't fire an order; review screen shows every field before the final send button activates. `OrderResult` toast banner pinned to bottom of viewport so every submission gets a visible success/failure acknowledgement.

**Positions tab:** per-row `Close` button using the currently selected Trade tab broker. **Orders tab:** per-row `Cancel` button, same broker context. Closes the last deferred item in ADR-089 — protocol + server + native relay + phone UI all shipped. Phone can now place, cancel, and close orders from any browser on the LAN.

### Six New Indicator Frontends + Cross-Language Transpiler (ADR-090, 2026-04-09)

**Indicator compiler expands from 4 languages to 9.** Every new frontend lowers into the same `IrModule` the MQL5/Pine/EL/TS pipelines already consume, which is what makes the headline transpiler feature trivial.

**MQL4** (`mql5-compiler/src/mql4.rs`) — textual rewrite pass runs before the existing MQL5 pest parser. Converts `extern`→`input`, `init`/`start`/`deinit`→`OnInit`/`OnCalculate`/`OnDeinit`, `Close[i]`→`iClose(...)`, `Bid`/`Ask` barewords→`SymbolInfoDouble(...)`, `Bars` bareword→`iBars(...)`. **String and comment aware** — user string literals are preserved verbatim instead of corrupted by the find-replace. Warns on `OrderSend`/`OrderSelect` calls since there is no textual port path for the MQL4 trading API.

**AFL (AmiBroker)** — line scanner. `_SECTION_BEGIN`/`_SECTION_END` parsed, `Param()` calls lowered to `input`, `EMA`/`SMA`/`RSI`/`ATR`/`HHV`/`LLV`/`StdDev` built-ins mapped to common IR, `Plot()` lowered to plot statements. Case-insensitive keyword matching (AFL is case-insensitive by spec).

**Pine v4** — extension to the existing `pine.rs` frontend. Auto-detects `//@version=4` header and normalises bareword calls (`sma` → `ta.sma`, `study` → `indicator`) — **only when not already namespaced**, so mixed-version files parse correctly. v5 files go through the normal v5 path untouched.

**ProBuilder (ProRealTime)** — bracketed-length syntax (`ExponentialAverage[20](close)`), `RETURN expr AS "label"` multi-return statements, `CROSSES OVER`/`CROSSES UNDER` operators, `REM` + `//` comments.

**NinjaScript (NinjaTrader)** — indicator subset. `[NinjaScriptProperty]` attribute scan to discover parameters, `AddPlot()` declarations, `Value[0]`/`Values[N][0]` assignments, SMA/EMA/RSI/ATR built-ins, `Math.*` utilities.

**cAlgo (cTrader)** — indicator subset. `[Indicator]`/`[Parameter]`/`[Output]` attributes, `Indicators.SimpleMovingAverage(...).Result[index]` long-form calls, `Bars.ClosePrices` + `MarketSeries.Close` long and short forms, `#region` blocks stripped.

**Cross-language transpiler** (`mql5-compiler/src/transpile.rs`) — **the exclusive headline feature.** Because every frontend lowers into the same `IrModule`, `transpile(source, from, to)` is just `parse_X → IR → emit_Y`. Phase 1 covers EL / TS / AFL / ProBuilder / Pine as sources and **MQL5 / Pine v5 / EL / TS as targets**. Each backend emits idiomatic source: full `#property` header and vectorised `OnCalculate` loop for MQL5, `//@version=5` + `ta.*`/`math.*` for PineScript, `inputs:`/`variables:`/`Plot1..N` for EasyLanguage, `input`/`def`/`plot` for thinkScript. Identifier case conventions preserved per-language (camel_case for EL/MQL5, snake_case for Pine/TS).

**Native UI:** Indicator Compiler window now has a **9-entry language dropdown** (MQL5/MQL4/PineScript/EasyLanguage/thinkScript/AFL/ProBuilder/NinjaScript/cAlgo). File-extension auto-detection expanded (`.mq4`, `.afl`, `.itf`, `.cs` — `.cs` disambiguated by scanning for the `NinjaScriptProperty` keyword to distinguish NinjaScript from unrelated C# files). Beneath the Compile button: **`Transpile to: [dropdown] [Transpile] [Use as Source] [Copy]` row**. Successful transpiles render in a green "Transpiled Output" panel below the metadata summary, and the "Use as Source" button feeds the transpiled text back into the source editor for chained conversions.

**65 new tests** — 11 MQL4, 10 AFL, 9 ProBuilder, 10 NinjaScript, 11 cAlgo, 2 Pine v4, 10 transpile, plus a cAlgo indicator-name regression fix. **Total workspace 793 tests** (from 728 in ADR-089). ADR-090 documents the full design.

### Complete 9×9 Cross-Language Transpiler Matrix (ADR-091, 2026-04-10)

**Phase 2 closes the transpiler: every language is now both a source AND a target.** The full 9×9 = 81 directional matrix is live — any of the 9 indicator languages can transpile to any other in a single click.

**Source-to-IR for the remaining 4 languages:** MQL5 gets a new `build_mql5_ir()` helper wrapping pest parser → AST → `ir::lower` into one call (`compile_mql5` becomes a thin wrapper). MQL4 gets source-to-IR for free via its textual rewrite pass + `build_mql5_ir`. NinjaScript and cAlgo each get `build_ir()` extracted from their parse functions.

**Five new IR → source backends:**

- **MQL4** — `#property strict`, `extern` inputs, `init()`/`start()` entry points, `Close[i]`/`Open[i]` series, `iMA(NULL,0,...)`/`iRSI`/`iATR`/`iStdDev` built-in calls.
- **AFL** — `_SECTION_BEGIN`/`_SECTION_END`, `Param()` inputs, `EMA`/`MA`/`RSI`/`ATR`/`HHV`/`LLV`/`StDev` built-ins, `Plot(value, "label", color, style)`.
- **ProBuilder** — bracketed-length form (`ExponentialAverage[N]`/`Average[N]`/`RSI[N]`/`ATR[N]`/`Highest[N]`/`Lowest[N]`/`StdDev[N]`), multi-return `RETURN ... AS "label"`.
- **NinjaScript** — full C# class skeleton: `using` directives, namespace, `OnStateChange` with `AddPlot`, `OnBarUpdate` with `Values[N][0]` assignments, `[NinjaScriptProperty]`/`[Display]` attributes. PascalCase input references.
- **cAlgo** — full C# class skeleton: `[Indicator]`/`[Parameter]`/`[Output]` attributes, `IndicatorDataSeries` outputs, `Calculate(int index)` with `Bars.ClosePrices[index]` and `Indicators.SimpleMovingAverage(...).Result` long-form built-ins. PascalCase input references.

**C# identifier handling:** both NinjaScript and cAlgo backends collect IR input names and promote `GetLocal` references to PascalCase when matching an input, keeping `public int Period { get; set; }` and body references consistent. New `pascal_case` helper handles word splits, digit-prefix safety, and non-alphanumeric drops.

**Native UI:** transpile target dropdown expanded from 4 to 9 entries — the full matrix is exposed.

**10 new transpile tests** including a `full_matrix_smoke_test` (EL source → all 9 targets, asserts non-empty output for each). **803 total tests** (from 793). ADR-091 documents the full design.

### Command Palette Consolidation — 230 → 226 Entries (2026-04-10)

**Four redundant commands removed from the palette**, their functionality merged into the primary command:

- **`ECON_CALENDAR` absorbed into `CALENDAR`** — one command now opens the calendar window AND fetches econ events (FOMC/NFP/CPI/PMI). Updated description, LAN remote handler, and `BrokerCmd` result routing.
- **`OPTION_CHAIN` absorbed into `OPTIONS`** — one command now fetches from both Alpaca (equity options) and tastytrade simultaneously.
- **`PRICE_TARGET` absorbed into `ANALYST`** — one command now opens the analyst window AND auto-fetches Finnhub price targets for the current symbol.
- **`POPOUT` removed** — `NEW_WINDOW` is the only entry.

Old command names still work in the handler (match arms kept for backwards compat) but no longer appear in the palette. UI hint text updated throughout (`"run OPTION_CHAIN"` → `"run OPTIONS"`, `"run DARWINEXOUTLIERS"` → `"run OUTLIERS"`).

### Zero Alias Cruft — One Name Per Feature (2026-04-10)

**Follow-up to the palette consolidation: all legacy alias match arms stripped from the handler.** `ECON_CALENDAR`, `OPTION_CHAIN`, `PRICE_TARGET`, `POPOUT` — removed from handler (were already removed from palette). `DIVEXPLORER`, `EVENTCALENDAR` removed from `EVENTS` handler. `DARWINEXOUTLIERS`, `ALPACAOUTLIERS`, `TASTYOUTLIERS` removed from `OUTLIERS` handler — the `SCOPE` command already controls broker filtering globally. `DIVEXPLORER` preset logic (forced Darwinex + dividends filter) removed. Typing a removed name now falls to the default no-op. No backward-compat shims, no aliases, no cruft.

### Sierra Chart ACSIL — 10th Language, 10×10 Transpiler (ADR-092, 2026-04-10)

**Tenth indicator language: Sierra Chart ACSIL** (`mql5-compiler/src/acsil.rs`). ACSIL uses C/C++ with Sierra Chart's proprietary API. The frontend scans for:

- `SCDLLName("...")`/`sc.GraphName` → short name
- `sc.GraphRegion = N` → separate window detection
- `SCSubgraphRef`/`SCInputRef` alias declarations
- `sc.SetDefaults` block: `Subgraph.Name`, `.DrawStyle`, `Input.Name`, `.SetInt`/`.SetFloat`
- Built-in study functions: `sc.SimpleMovAvg`/`ExponentialMovAvg`/`RSI`/`ATR`/`Highest`/`Lowest`/`StdDev` (both 3-arg write-to-subgraph and 2-arg forms)
- `sc.BaseDataIn[SC_LAST/OPEN/HIGH/LOW/VOLUME]` price series
- `Subgraph[sc.Index] = expr` direct buffer assignments
- Standard C arithmetic and comparison operators

**Transpiler expanded to full 10×10 = 100 directional matrix.** IR → ACSIL backend emits a complete study skeleton: `#include`, `SCDLLName`, `SCSFExport`, `SCSubgraphRef`/`SCInputRef` declarations, `SetDefaults` block, and `sc.*` built-in calls. Input references emit `RefName.GetInt()`.

**Native UI:** language dropdown 9 → 10, transpile target 9 → 10. File loader accepts `.cpp`/`.h` with content-sniffing (`SierraChart.h`/`SCSFExport`/`SCStudyInterfaceRef` → ACSIL, else MQL5 C++ fallback).

**10 new ACSIL tests** + 1 `ema_mapping` regression fix (`starts_with` vs `contains` for `sc.BaseDataIn` prefix). **813 total tests** (from 803).

### Codebase Audit — Zero GPU Unwraps + O(1) Darwin Analytics (2026-04-10)

**All 10 `.as_ref().unwrap()` calls in `gpu_compute.rs` eliminated** (ADR-082 compliance). Pattern was: create buffer into `Some()`, immediately unwrap to write. Fix: capture buffer in local variable, write to `&local`, then move into `self.field = Some(local)`. Zero unwraps remain in `gpu_compute.rs`. Affected methods: `upload_darwin_batched` (2 sites × 2 buffers = 4), `BacktestContext::upload` (3 buffers), `evaluate_nnfx` (3 buffers).

**4 production unwraps eliminated:** `backtest.rs` — 2× `bars.last().unwrap()` → if-let pattern. `darwin.rs` — `regimes.iter().max_by().unwrap()`/`min_by().unwrap()` → `.unwrap_or(&default_regime)` with `MEDIUM_VOL` fallback.

**O(n²) → O(1) HashMap lookups in `darwin.rs`:** `darwin_var_list.iter().find()` in correlation pair loop → pre-built `sharpe_map: HashMap<&str, f64>`. `all_open.iter().find()` → pre-built `open_pos_map: HashMap<(&str, &str), &tuple>`. `returns.iter().find()` in drawdown analysis (dates × darwins × returns) → pre-built `balance_maps: Vec<HashMap<&str, f64>>` per darwin. `Vec::with_capacity()` added for portfolio balance allocations.

**Security audit: CLEAN** — all SQL parameterized, no path traversal, no command injection, no unsafe blocks, AES-256-GCM + PBKDF2 crypto, rate limiting in place.

ADR-090/091 accuracy updated: ACSIL marked implemented (was "permanently out of scope"), test counts corrected 803→813, language count 9→10. Pest parser unwraps (58 in `parser.rs`) retained — standard pest idiom where grammar validates structure before Rust runs.

### Zero Non-Pest Production Unwraps (2026-04-10)

**Final unwrap pass: 7 `.unwrap()` calls in `ir.rs` converted to `.expect()` with guard documentation.** `iOpen`/`iHigh`/`iLow`/`iClose`/`iVolume` — `.into_iter().last().unwrap()` → `.last().expect("guarded by !is_empty")` (5 sites). `MathMax`/`MathMin` — `it.next().unwrap()` → `it.next().expect("guarded by len==2")` (4 sites across 2 match arms).

**Production unwrap audit: 41 remain, ALL in `parser.rs`** — standard pest idiom where the grammar validates structure before Rust code runs. **Zero `.unwrap()` in engine, native, web-server, web-protocol, web, or cli production code.** ADR-082 fully satisfied.

## ADR-092/093/094: Darwinex Web Scraping, GPU Parity, UX Analytics Overhaul

**5,339 lines added across 20 files** in a single commit spanning three ADRs. This is the largest single commit in TyphooN-Terminal history.

**ADR-093 — Darwinex Zero Web Scraping** (`engine/src/core/darwin_web.rs`, 934 lines): Full web scraping engine for Darwinex Zero portfolio data. Scrapes investor allocation, DARWIN performance metrics, and portfolio analytics directly from the Darwinex web interface — eliminating manual XML export workflows. The engine handles authentication, session management, and data extraction with proper error handling throughout.

**ADR-092/094 — GPU Parity & UX Analytics Overhaul**: Massive expansion of GPU compute capabilities (`native/src/gpu_compute.rs`, +818 lines) and native app UX (`native/src/app.rs`, +1,127 lines). The web client received a parallel overhaul (`web/src/app.rs`, +852 lines) and protocol layer (`web-protocol/src/lib.rs`, +595 lines) to maintain full GPU/CPU and native/web feature parity. CLI broker interface extended, cache layer updated, LAN sync protocol expanded.

**MQL5 compiler improvements**: `parser.rs` gained 99 lines of new parsing logic, `ir.rs` refined with 25 lines of IR lowering improvements — continuing the transpiler expansion from ADR-090/091.

## ADR Follow-Up Closures: tastytrade Cancel, GPU MACD, ADR Accuracy

**Closing open follow-ups across multiple ADRs** — 99 lines added, 53 removed across 10 files. Focused refinement pass tying off loose ends.

**tastytrade order cancellation** (`engine/src/broker/tastytrade.rs`, +16 lines): Cancel order support added to the tastytrade broker integration — completing the order lifecycle (place, modify, cancel).

**GPU MACD dynamic parameters** (`native/src/gpu_compute.rs`, +33/-6 lines): MACD GPU shader updated with dynamic parameter support, replacing hardcoded values. Ensures GPU/CPU parity for MACD rendering with user-configurable fast/slow/signal periods.

**Native app UX refinements** (`native/src/app.rs`, +27/-5 lines): UI polish pass on the native desktop client.

**ADR documentation updates**: 7 ADR docs updated with accuracy corrections and status changes — ADR-058 (GPU strategy optimizer), ADR-069 (feature status), ADR-072 (Kraken broker), ADR-081 (optimization roadmap), ADR-085 (broker scope), ADR-088 (gap closure), ADR-089 (EasyLang/ThinkScript/phone orders).

## ADR-038 Phase 2: Pluggable DataSourceManager with Priority Routing

**+385 lines, -34 lines across 5 files.** The data layer gets its routing brain.

New `engine/src/core/data_source.rs` introduces the **DataSourceManager** — a pluggable priority-based routing engine for market data. Five default sources ranked by priority: MT5 (1) > Alpaca (2) > tastytrade (3) > CryptoCompare (4) > Kraken (5). The manager handles `resolve_candidates()` for priority-ordered cache key lookup, `mark_success()`/`mark_failure()` for health tracking, and `update_health()` with automatic timeout detection (15 minutes without data → unhealthy). Unhealthy sources get demoted to end of candidate list but are still tried as last resort.

**Per-symbol wildcard overrides** allow routing specific instruments to preferred sources — e.g., `BTC*` → Kraken first. The `find_cache_key()` function now uses `DataSourceManager::resolve_candidates()` instead of hardcoded source lists.

**SOURCES console command** displays a health dashboard as a Summary result card — live visibility into which sources are healthy, unhealthy, or overridden.

**11 new tests** covering source resolution, health transitions, wildcard overrides, and priority ordering. 865 total, 0 failures, 0 warnings.

## Alpaca OCO Orders, ICS Calendar Export, Kraken Margin Trading

**+132 lines, -22 lines across 13 files.** Two commits expanding broker capabilities and calendar tooling.

**Alpaca OCO orders** (`engine/src/broker/alpaca.rs`): New `AlpacaBroker::oco_order()` sends order_class "oco" with take-profit limit and stop-loss stop in a single API call. Wired to `OCO` console command — `OCO SELL AAPL 10 200 180` places a bracket exit in one shot.

**ICS calendar export** (`native/src/app.rs`): `EXPORT_CALENDAR` command writes the event calendar to a `.ics` file via `build_events_ics()` with source, impact, and event type filters. Import your economic calendar into any calendar app.

**Kraken margin trading** (`engine/src/broker/kraken_broker.rs`): `KrakenBroker::place_order_with_leverage()` adds optional leverage parameter (e.g. "2:1", "5:1") passed to the Kraken AddOrder API. `KrakenBroker::cancel_all_orders()` implements POST `/0/private/CancelAll` for one-command position cleanup.

**ADR accuracy sweep**: 6 ADR docs updated — compiler tests 82→216 with 8 transpiler backends (067), data sources 19→21 with tastytrade/Kraken added (069), OCO + CancelAll + leverage marked implemented (072), ICS export done (084), broker scope sites resolved + ForexFactory filters implemented (085).

## SCOPE System, Scrollbar Fixes, Test Coverage, Cache Repair

**+390 lines, -92 lines across 10 files in 6 commits.** Symbol scoping gets a proper UI and the test suite fills gaps.

**SCOPE POSITIONS** (`native/src/app.rs`): New scope filter shows only symbols with open positions across Alpaca + tastytrade. Useful for focused outlier/fundamental analysis on actively held positions instead of 5,000+ symbols. Scope cycle: All → Alpaca → Darwinex → Tasty → Positions → All.

**Unified SCOPE system**: SCOPE command and fundamentals source toggles (MT5/Alpaca/tastytrade) now drive the same state — changing one syncs the other. No more divergence between what OUTLIERS sees and what EVSCRAPE scrapes. New SCOPE popup window with checkboxes and quick presets (ALL, Alpaca Only, Darwinex Only, Positions). Status bar shows source toggles (MT5:ON Alpaca:off Tasty:off). All 8 checkbox combinations have explicit mappings — no more stale same-frame values.

**Scrollbar fix** across all 26 floating windows: `auto_shrink(false)` on every `ScrollArea` instance so scrollbars appear at the window edge instead of mid-content. Outlier scanner switched to `ScrollArea::both` for horizontal overflow on wide grids.

**Cache repair fix** (`engine/src/core/cache.rs`): `repair_bar_counts` now skips `__SPECS__`, `__SYMBOLS__`, `__SERVER__` metadata entries before attempting zstd decompression — eliminates warning spam on every startup.

**+16 tests** filling gaps across 5 files: OCO body construction, Kraken credentials, data source wildcards/health, FRED series roundtrip, web-protocol OCO/DARWIN commands. **881 total, 0 failures, 0 warnings.**

## Matrix Community Chat, Claude Code Integration, UX Polish

**13 commits, +525 lines, -117 lines.** The terminal gets a community chat, AI assistant integration, and a full UX audit.

**Matrix community chat** (`native/src/app.rs`): Full Matrix protocol integration — guest auto-join, send messages, auto-refresh every 10 seconds, stick-to-bottom auto-scroll, connection status indicator. Evolved through 6 iterations: guest auth → user login (matrix.org disabled guests) → credentials in Settings panel alongside Alpaca/Finnhub/Kraken → keyring persistence across restarts. `CHAT` command (aliases: `MATRIX`) opens the community chat window. `MATRIX_LOGIN` removed — credentials now live in the Settings panel where they belong.

**CLAUDE command** (`native/src/app.rs`, +107 lines): Claude Code CLI integration that detects the local `claude` binary in PATH and opens a chat window piping to `claude --print` on a background thread. Uses the user's existing Claude Code subscription — no API key required. Separate from the `AI` command which uses API-based Claude/GPT.

**Screenshot performance fix** (`native/src/app.rs`): PNG encode moved to background thread. On 4K displays, `image::save_buffer()` compresses ~33MB RGBA → PNG (100-500ms) — was blocking the UI thread. Now shows "Saving screenshot..." immediately while encoding happens in the background. Full audit confirmed all `block_on()`, `thread::sleep()`, and `Mutex::lock()` calls are already in background threads.

**UX combover**: All 239 commands verified to have handlers with zero silent failures. Broker-dependent commands (`FILLS`, `MOVERS`, `HISTORY`, `MOST_ACTIVE`, `WATCHLISTS`, `PORTFOLIO_HIST`) now check `broker_connected` first and show a clear error instead of silently failing.

**CLI parity** (`cli/src/broker.rs`, `cli/src/main.rs`): Added `oco` and `cancel` commands. CLI now has full order type parity with native: market, limit, stop, bracket, trailing, oco, cancel, cancelall, closeall.

**SEC EDGAR rate limiting** (`engine/src/core/sec_filing.rs`): Rate limit increased from 200ms to 250ms (4 req/sec). Form 4 fetch retries up to 3 times on HTTP 429 with exponential backoff (1s, 2s, 4s) instead of immediately moving to the next filing.

## AI Multi-Provider: 7 Providers + Gemini CLI + Local Models

**+164 lines, -11 lines across 2 files.** The AI command becomes a universal LLM gateway.

**7 AI providers** via radio selector in the AI chat window: Claude (Anthropic native API), GPT (OpenAI), Gemini (Google AI Studio), Grok (xAI), Mistral, Perplexity, and Local (Ollama at localhost:11434 / LM Studio at localhost:1234). All OpenAI-compatible providers share the same code path with different base URLs and model names — no new dependencies beyond reqwest.

**GEMINI command**: Local Gemini CLI binary integration, same pattern as the CLAUDE command. Each CLI tool gets its own chat window with independent history.

**Settings panel**: 4 new API key fields (Gemini, Grok, Mistral, Perplexity) alongside existing keys. All persisted in system keyring.

## Lossless WebP Screenshots + SHARE to Matrix

**+94 lines, -6 lines.** Screenshots upgrade and community sharing in one commit.

**Lossless WebP**: Screenshots switched from PNG to lossless WebP — smaller files with no quality loss. Uses `image::DynamicImage::save()` with auto-format detection from the `.webp` extension.

**SHARE command**: Uploads the last screenshot to the Matrix community chat room via `/_matrix/media/r0/upload`, sent as an `m.image` message. Requires Matrix login (credentials in Settings). Flow: `SCREENSHOT` → saves WebP locally → `SHARE` → uploads to community chat. Last screenshot path tracked for instant sharing.

## O(1) Performance Audit + ADR-094 Comprehensive Update

**Last Vec::remove(0) eliminated.** The deferred chart loads queue was the final `Vec::remove(0)` in the codebase — replaced with `VecDeque::pop_front()` for O(1) queue operations. Zero `Vec::remove(0)` remaining anywhere in the project.

**ADR-094 updated** with a comprehensive session summary covering all recent work: 881 tests, scrollbar fix, SCOPE popup, Matrix chat, Claude/Gemini CLI, AI multi-provider, WebP screenshots, SEC 429 fix, CLI OCO, broker guards, and the O(1) audit itself.

**Full security audit**: 0 production `unwrap`, 0 `unsafe`, 0 `panic`, 0 SQL injection. **O(1) audit**: 0 `Vec::remove(0)`, all queues use `VecDeque`. 881 tests, 0 failures, 0 warnings.

## Matrix Auth: Access Token Migration

**Username/password login replaced with access token authentication.** The entire `MatrixLogin` flow has been removed — no more interactive username/password prompts. Matrix authentication now uses a direct access token stored in the system keyring (`MATRIX_ACCESS_TOKEN` + `MATRIX_USER_ID`). The Settings UI gains a token field instead of credential inputs. Simpler, more secure, no login state machine.

## Matrix Send + Broker Scope Filtering Fixes

**Matrix room IDs now URL-encoded in all API URLs**, fixing send failures caused by unencoded `!`, `/`, and `:` characters. A new `MatrixJoinRoom` command auto-joins the configured room on connect and session restore — no more silent message drops to unjoined rooms.

**Broker scope default changed from All to Darwinex** to match fund_source defaults. The `broker_scope` now syncs automatically from fund_source checkboxes in both Settings and scrape panels. The SCOPE popup displays the scoped symbol count instead of the total — what you see is what you're trading.

## Darwinex Web Scraping Expansion

**Expanded Darwinex web scraping to all DARWIN profile tabs and portfolio pages.** The scraper now clicks through Return/Performance, Risk, Investable Attributes, and Investor tabs per DARWIN, extracting the full data surface. Portfolio-level performance, risk, and allocation pages are scraped alongside individual DARWINs. Snapshot validation with retry on partial failures ensures complete data capture — 11 new data types, 50 new tests.

## EVSCRAPE FORCE + Darwinex Scope Regression Fix

**+101 lines, -70 lines.** Cache bypass and scope filtering made reliable.

**EVSCRAPE FORCE**: `EVSCRAPE FORCE` now bypasses the 24-hour fundamentals cache, forcing a fresh scrape regardless of when data was last fetched. LAN forwarding propagates the force flag to the server — remote clients get the same cache-bypass behavior as local.

**Darwinex scope regression fix**: The background thread now loads `darwinex_specs` via `load_all_specs_parsed()` every cycle, auto-populating `darwinex_radar_data` so Darwinex scope filtering works without manually running `DARWINEXRADAR` first. `broker_scope_symbols()` returns `None` (no filter) when radar data is empty instead of `Some(empty_set)` — which was silently filtering everything to zero symbols. `EVSCRAPE FORCE` also bypasses the `scrape_failures` blocklist, not just the 24h cache.

## O(1) Hot-Path Optimizations (ADR-095)

**All remaining O(n²) and O(n) hot paths converted to O(1).** The live quote ingestion loop was rebuilt around a pre-built symbol→chart-indices `HashMap` per message batch, collapsing the old `O(quotes × charts)` nested iteration into a single `HashMap` lookup per tick. Watchlist quote routing uses the same pattern.

**Static HashSets for routing**: Indices and forex classification uses `LazyLock<HashSet>` instead of per-tick `.iter().any()` calls with `Vec` allocations. LAN watchlist filter switched to `HashSet` for O(1) exact-match lookup. MTF grid sort uses a match-based ordinal rather than `.position()` linear search.

**ADRs 084 through 094 moved from Accepted to Implemented.** Every pluggable data source, every audit recommendation, every deferred perf pass — closed out and documented. 904 tests pass.

## SEC Filing Database: FTS5 + Indefinite Storage + Insider Aggregation

**Complete rearchitecture of SEC EDGAR filing storage.** New schema: `sec_filing_content` stores full plain-text filing content with no retention limit, `sec_fts` is a FTS5 virtual table with porter stemming and Unicode tokenization, and `sec_keyword_watchlist` holds proactive alert keywords. The background thread now loads ALL filings and ALL insider trades (previously capped at 100/90-day windows).

**New engine functions**: `get_all_filings()`, `get_all_insider_trades()` (no limits), `strip_html_to_text()`, `store_filing_content()` with automatic FTS5 indexing, `search_filings_fts()`, `filing_content_stats()`, keyword watchlist CRUD, and `get_unfetched_filings()` for backfill prioritization.

**SEC window UI**: `broker_scope` filtering replaces the old "Active Only" checkbox, a text search box provides instant client-side filter over the loaded filings, "X/Y indexed" status shows full-text search coverage, and a new **Insiders tab** aggregates Form 4 trades across symbols with cluster detection — 3+ trades within a 14-day window get flagged as a high-confidence cluster signal. Filing content auto-stores to the DB and FTS5 index on first View Document.

## SEC Phase 2: Content Backfill, Chart Overlays, Filing Diff, Timeline Heatmap

**+1,400 lines across BG thread, chart rendering, and SEC window.** The background thread now runs a continuous content backfill: every ~30 seconds it fetches 5 unfetched filings in a spawned thread with 250ms rate limiting. Every filing gets indexed into FTS5 without user intervention.

**Keyword watchlist UI**: the Alerts tab lets you add/remove keywords as removable badges. During backfill, each new filing's text is scanned against the watchlist — matches fire `KEYWORD_MATCH` alerts. Proactive SEC intelligence with zero manual work.

**Insider trade chart overlay**: `build_trade_overlay()` renders Form 4 buy/sell markers directly on the price chart, labeled with the insider's name (e.g., `SEC:John Smith`). See every insider transaction contextualized against price action without leaving the chart.

**Filing diff viewer**: `diff_filing_content()` runs an LCS-based paragraph diff between the current filing and its previous revision via `find_previous_filing()`. Compare 10-Q to 10-Q, see what changed in management's risk disclosures. Nobody else in retail tooling does this.

**Timeline tab**: monthly filing activity heatmap with proportional bars, color intensity scaled to density, and a form type breakdown per month. At a glance you see whether a company is quiet or slammed with activity.

## GPU→CPU Indicator Fallback: Thirteen Boundary Regressions Fixed

**Every GPU-accelerated indicator has a CPU fallback for when the shader path fails or is unavailable.** The CPU and GPU paths must produce identical results — and they weren't. Two commits fix thirteen off-by-one and warmup-period bugs that were silently discarding valid indicator bars.

**RSI**: `i<=period` → `i<period`. First valid RSI bar was being blanked. **ADX**: split warmup into separate DI+/- (period) and ADX (period*2-1) windows — was blanking 14 valid DI bars, and ADX warmup had an off-by-one. **CCI**: hardcoded `i<20` corrected to `i<19` (period-1). **Fisher**: added explicit index boundary alongside the 0.0 sentinel check (0.0 is a legitimate Fisher value and was being treated as "not yet valid").

**Williams %R**: `i<14` → `i<13`. **Ehlers EBSW**: `i<40` → `i<2` — 38 valid bars were being discarded. **Ehlers Cyber Cycle**: `i<7` → `i<4`. **Ehlers Center of Gravity**: replaced 0.0 sentinel with `i<9` index boundary (0.0 is a valid oscillator reading). **Ehlers Roofing Filter**: `i<10` → `i<2`. **MAMA/FAMA**: added `i<6` index boundary alongside 0.0 sentinel.

**Bonus**: `sec_filing.rs` symbol dedup switched from `Vec::contains()` O(n²) to `HashSet` O(n). Zero production `unwrap()` confirmed (ADR-082 compliant). 904 tests pass, zero warnings.

## VAROUTLIER + ATROUTLIER: MarketWizardry.org Methodology Ported to Rust

**Three commits build out VaR-based and ATR-based IQR outlier detection commands**, matching the methodology used in the MarketWizardry.org VaR Explorer and ATR Explorer.

**VAROUTLIER** computes `VaR_1_Lot` from D1 daily returns (95% confidence, `z × σ × price`) for every scoped symbol, then runs three-level IQR detection (sector → industry → global) with 1.5× IQR multiplier. Reports Q1, Q3, IQR, and bounds in the log. New engine function: `compute_var_from_closes()`. Then upgraded to the **full DWEX Portfolio Risk Man formula**: `VaR_1_Lot` now uses `tickValue`/`tickSize` from the `__SPECS__` CSV — the same formula as the MQL5 `CPortfolioRiskMan` class. New engine: `compute_var_from_closes_with_tick()` accepts a tick scaling factor, `load_tick_specs()` extracts per-symbol tick specs from bar cache. The VaR/Ask ratio used for IQR analysis is tick-scale-invariant (`z × σ × scale × price / price = z × σ × scale`), so the comparison remains fair across instruments with wildly different tick structures.

**ATROUTLIER** computes ATR(14)/Close ratio from D1 bars, runs IQR per sector, matching the MarketWizardry.org ATR Explorer methodology. Both commands scope-filtered, both read directly from the bar cache.

**Cruft removal**: `IMPORT_DARWIN` and `EXPORT_DARWIN` commands deleted. XLSX import via `DarwinImportAll` is the real path — the JSON import/export path was dead code. Command palette shrinks from 264 to 262 commands. **69 BrokerCmd variants sent, 27 BrokerMsg variants handled**. Zero dead code wired into the UI.

## Performance/UX/Memory Pass (ADR-097)

**Audit of 18 items across UX, performance, and memory. Twelve implemented, six deferred with rationale.**

**UX**: the command palette gains `fuzzy_score()` subsequence matching with positional bonus, replacing the old contains-only filter — type `vrout` and VAROUTLIER matches. The filing detail viewer gains a sticky pin button with accession-tracked content, so scrolling the filing list doesn't blow away your current view.

**Performance**: explicit `PRAGMA wal_checkpoint(TRUNCATE)` on quit — the WAL no longer balloons across crashes.

**Memory — the big wins**: `sec_filing_content` now stores content with **zstd-3 compression** for ~10× size reduction. Insider trades are SQL-filtered to the last 5 years on load. The bar cache gained **LRU eviction** with a 500MB soft limit — eviction skips entries newer than 7 days (hot data always retained) and runs every 30 minutes alongside the existing vacuum cycle.

**Deferred with rationale**: `Arc<str>` symbol interning, GPU buffer pool, scope cache, workspace presets, sparklines, chart auto-scroll. All documented in ADR-097 so future-me (or any contributor) understands why the knob wasn't turned.

## ADR-098/099/100: Every Deferred Item Implemented, Every Table Wired

**Three ADRs in one sprint. Every item deferred in ADR-097 is now implemented, every new piece of infrastructure is wired into every table that can use it, and the allocation profile has been halved again.**

### ADR-098 — The Deferred Seven

Every item the perf pass deferred with rationale gets built:

- **PERF2: Per-frame scope HashSet cache** — `cached_scope_syms` invalidated each `update()`. `scoped_fundamentals*()` and the SEC/EV scanner now read from the cache instead of recomputing the scope set on every callsite.
- **PERF4: GPU buffer pool** — `pooled_bar_count` tracks the last upload size per chart. Forming-bar updates skip **8 buffer reallocations per chart per tick** by reusing the existing GPU buffer when the bar count hasn't grown.
- **PERF5: Sector interning** — `sector_interner: HashMap<String, Arc<str>>` plus `intern_sector()` helper. Infrastructure in place for the migration pass in ADR-099.
- **UX3: Symbol action pattern** — `SymbolAction` enum, `symbol_label_with_menu()` free function, `apply_symbol_action()` helper. Right-click any symbol, get chart/fundamentals/SEC/insider actions in a context menu. Wired first into the Outlier Scanner.
- **UX4: Workspaces** — `WORKSPACE_SAVE`, `WORKSPACE_LOAD`, `WORKSPACES` commands. `capture_workspace_snapshot()` serializes ~20 `show_*` flags; `apply_workspace_snapshot()` restores them. Name a layout, switch to it with one command.
- **UX6: Auto-scroll to extremes** — `outlier_scroll_pending` flag. On first EXTREME tier outlier, the table scrolls to the row so you see the thing that matters without hunting.
- **UX7: Sparklines** — `sparkline_cache` with lazy fetch via `get_sparkline()`. `draw_inline_sparkline()` renders a 60×14px inline chart inside grid cells. First deployment in the EV Scanner.

### ADR-099 — Wire It Everywhere

With the symbol action + sparkline infrastructure in place, ADR-099 runs the wiring pass across every table that can use it.

**Symbol context menus in nine grids**: `outliers_grid`, `multi_outlier_grid`, `ev_scanner_grid`, `sec_filings_grid`, `insider_agg_grid`, `swap_harvest_grid`, `radar_grid`, `div_screen_grid`, `unusual_vol_grid`. Every table that shows a symbol now lets you right-click for actions. The Watchlist context menu gains View fundamentals / View SEC / View insider entries.

**Sparklines in three more tables**: EV Scanner, Multi-Outlier, Single-Dim Outlier. Sparklines are pre-fetched outside the rendering closure to avoid egui borrow conflicts.

**PERF5 migration — the 20× allocation reduction**: `detect_outliers()` now uses `HashMap<Arc<str>, Vec<(&str, f64)>>` internally for sector grouping. Every symbol in every sector group used to clone a `String` for the sector key — now it's an `Arc::clone()` refcount bump. `tier` changed from `String::from("EXTREME")` to `&'static str` literals. `sector_str` is materialized once per group instead of once per symbol. For a 1000-symbol scan across 50 sectors, that's roughly **20× fewer `String` allocations**.

### ADR-100 — Deeper Still

The wiring pass continues. Sparklines land in two more tables (`div_screen_grid` and `unusual_vol_grid` — **five tables total** now). Live Alpaca and tastytrade positions gain right-click context menus via a new `deferred_symbol_action` field applied at the end of `update()` (deferred because the positions loop can't mutably borrow `self` while iterating).

**Built-in workspace presets** — four curated layouts shipped out of the box:
- **TRADING** — focus mode, charts + order panel only.
- **RESEARCH** — full data surface, every fundamentals/SEC/EV window open.
- **DARWIN** — analytics-first: portfolio VaR, correlation, DARWIN allocation.
- **COMPACT** — everything closed except the command palette.

`Self::builtin_workspace()` returns the snapshot; `WORKSPACE_LOAD` falls back to a builtin if no user-saved workspace matches the name. Type `WORKSPACE_LOAD TRADING` and the terminal rearranges itself.

**Sparkline cache bounds**: 2000-entry soft cap (~480KB), drops the 500 oldest entries on overflow. No LRU bookkeeping cost — a simple truncation beats tracking access time for this workload.

## ADR-101/102: Every Surface, Every Table, Every Window

**Two more wiring passes.** ADR-098/099/100 got context menus into 11 tables and sparklines into 5. ADR-101 and ADR-102 push those numbers to **17 surfaces for context menus** and **7 for sparklines** — effectively every grid and window that shows a symbol.

**ADR-101 (wiring pass 2)**: Context menus land in `live_orders` and `congress_grid` (13 tables total). Sparklines reach 6 tables with the Fundamentals window gaining an 80×18 inline chart next to the ticker name. **OUTLIERS handler clone reduction**: the per-row handler was cloning `f.symbol` **four times per row**; now it clones once and reuses. On a 1000-symbol scan that's **~3000 String allocations eliminated**. VAROUTLIER gets the same pattern — another ~1000 saved.

**ADR-102 (wiring pass 3)**: Context menus extend to `earnings_cal_grid`, `div_cal_grid`, `event_cal_grid`, and the insider trades window header — **17 surfaces total**. Sparklines reach the insider trades window (100×18 next to the active symbol) — **7 surfaces total**.

**The inner-loop fix**: `active_symbols()` was deduping with `Vec::contains()`, which is `O(n²)` — a quadratic cost quietly running on every "Active Only" filter check across the app. Replaced with `HashSet::insert()` — `O(n)`. A `cached_active_symbols` field now recomputes once per frame, and **six callsites** read from the cache instead of rebuilding the set each time. Non-trivial win: this used to be one of the hot spots on large watchlists.

## ADR-103: Scoped Fundamentals Cache + Stat Arb Menus

**One more pass. The `cached_scoped_fundamentals` field is recomputed once per frame**, and three callsites — the sector heatmap, dividend screener, and outlier scanner — now read from the cache instead of re-running the scope filter each time.

**The `.to_uppercase()` bug**: the EV Scanner was calling `.to_uppercase()` on every symbol **three times per frame** (once per callsite that needed an uppercase key for the scope filter). That's **~600 String allocations eliminated per render** on a 200-symbol scanner just by hoisting the uppercase conversion and caching the result.

**Stat arb pairs get context menus too**: the stat arb window displays pairs as `SYM_A / SYM_B`, and both symbols in each pair now have independent right-click menus — **18 surfaces with context menus total**. Full symbol interactivity across every grid, window, and pair display in the app.

## ADR-104/105: Active Filter HashSet, Filing Truncation, BG Blacklist

**Two more wiring passes and a real inner-loop fix.** ADR-104 introduces `cached_active_symbols_set` — a HashSet field built once per frame — and converts **five windows** (Unusual Volume, Congress, EV Scanner, Earnings Calendar, Dividend Calendar) from `O(N×M)` `iter().any()` calls to `O(1)` HashSet lookups. On a 100-row watchlist with 30 active symbols, that's **3,000 string comparisons per frame replaced by 100 hash lookups** — a quiet but significant win on the active-filter hot path.

**Filing truncation cap**: `store_filing_content()` now caps at **500KB of plain text** with UTF-8 boundary-safe truncation (no mid-codepoint splits, marker appended). The FTS5 index gets the same truncation. A single 8-MB 10-K filing was enough to bloat the cache — capped now.

**Backfill grid context menu**: another surface joins the family. **19 surfaces with context menus total.**

**ADR-105 (wiring pass 6)**: the BG thread's darwin:deleted blacklist was a `Vec` with an `O(n²)` `retain` — flipped to `HashSet` for `O(n)` retain. Cache capacities pre-allocated at startup so the sparkline cache (256), sector interner (64), and cached active-symbols set (64) do not reallocate during the first few frames. Also investigated a suspicious `build_trade_overlay` call — `entry.2.contains(...)` turned out to be `String::contains` (substring check), not `Vec::contains`, and was correct as written. 904 tests still pass.

## ADR-106: mimalloc + Max Release Profile

**The allocator gets replaced.** `mimalloc` (Microsoft Research's small-object-optimized allocator) is now the global allocator for the entire terminal. For a workload like this — thousands of small `String` and `Vec<f32>` allocations per frame as grids re-render and indicator pipelines feed GPU buffers — a small-object-tuned allocator is the right call. **Expected 5–15% frame latency reduction** on render-heavy operations.

**Release profile maxed out**:
- `opt-level` **2 → 3** (max optimizations + auto-vectorization)
- `lto` **thin → fat** (cross-crate inlining across all 8 crates)
- `codegen-units` → **1** (single-pass compilation, lets LLVM see the whole program)
- `panic = abort` (no unwind tables, smaller binary)
- `debug = false` (strip debug info)

Build time goes from **3 minutes to 8 minutes** on release. For a production trading binary that runs 8+ hours a day at monitor refresh rate, that tradeoff is obvious. 904 tests pass, 0 warnings.

## Outlier Tables: Industry Column + Sortable Headers

**The multi-dim OUTLIERS window gets an industry breakout.** `OutlierResult` / `MultiOutlierResult` now carry an `industry` field; `detect_outliers` and `detect_multi_outliers` take `(symbol, sector, industry, ...)` tuples. IQR grouping stays **by sector** — industry has too few peers per bucket for stable IQR — but it's carried as a display/sort column so you can finally see which *industry* within a sector an outlier is drifting from.

**VAROUTLIER / EVOUTLIER / ATROUTLIER single-metric tables**: converted from static egui Grid to **clickable sortable headers** — Symbol / Sector / Industry / Value / Median / Tier / Z-Score / Dir. Default sort is `|z-score|` descending. VAROUTLIER lost its redundant second IQR-by-industry pass in the process — same information now rides along as a column on the sector-grouped result. One pass instead of two.

## Yahoo Fundamentals: ETF / Fund / Crypto Fallback

**Every ETF used to show up as "Unknown" in the outlier tables.** Yahoo Finance returns an empty `summaryProfile` for ETFs and mutual funds — they populate `fundProfile` + `quoteType` instead. Previously every ETF fell through with an empty sector/industry and got bucketed as Unknown, obscuring the actual sector distribution in the scanner.

- Added `fundProfile,quoteType` to `YAHOO_MODULES`.
- When `summaryProfile` is empty, `parse_yahoo_data` now reads `categoryName` / `family` / `legalType` from `fundProfile` and `quoteType` from `quoteType`:
  - **ETF** → sector='ETF', industry=categoryName (e.g. 'Large Blend')
  - **MUTUALFUND** → sector='Mutual Fund', industry=categoryName
  - **CRYPTOCURRENCY / CURRENCY / INDEX / FUTURE** → corresponding sector bucket (last-resort fallback when `fundProfile` is absent)

Equities with populated `summaryProfile` are untouched. 4 new tests cover ETF, mutual fund, crypto last-resort, and the equity-unchanged case.

## ASKAI / ASKCLAUDE / ASKGEMINI: Research Packet Commands

**The palette's bare AI/CLAUDE/GEMINI commands are dead. Long live ASKAI/ASKCLAUDE/ASKGEMINI.** These new commands open the corresponding chat window **AND** — when given symbol arguments — pre-load a full Markdown research packet assembled from every local data source the terminal has:

- `symbol_fundamentals` row: sector, industry, mcap, EV, debt, cash, P/E, fwd P/E, PEG, P/B, P/S, EV/EBITDA, margins, ROE, ROA, beta, short interest, dividend yield, next earnings date, description
- **Last 4 quarterly financials** from the SQLite cache: revenue, net income, FCF, gross/operating profit, EPS
- **Top 5 institutional holders**: org, shares, pct, value
- **Recent SEC filings**: form, category, summary
- **Insider activity summary**: buy/sell counts, aggregate values, last 5 transactions
- **Price & volatility**: last close, 20/60/252d returns, ATR(14) %, VaR 95% per 1 lot
- **Sector peer comparison**: this symbol's ratios vs sector median across 9 metrics (P/E, P/B, P/S, EV/EBITDA, margins, ROE, beta, short % float, dividend yield), minimum 3 peers required

**Three backends, one contract**:
- `ASKAI` → `BrokerCmd::AiChat` (Claude / GPT / Gemini / Grok / Mistral / Perplexity / Local)
- `ASKCLAUDE` → `claude --print` subprocess
- `ASKGEMINI` → `gemini` subprocess

Type `ASKGEMINI AAPL,MSFT what's their debt burden vs the sector?` and you get a chat window already populated with 10+ KB of structured fundamentals for both symbols plus the question verbatim. No re-querying Yahoo at chat-time, no copy-paste — it's already there.

**Also in the same commit**: Claude Code CLI chat intercepts interactive-only slash commands (`/status`, `/help`, `/clear`, `/model`, `/cost`, `/config`, `/login`, ...) **locally** before shelling out. Previously `/status` returned "Unknown skill: status" because `claude --print` treats `/foo` as a skill invocation. `/clear` clears history, `/help` and `/status` return a local explanation, other interactive-only commands return a note. Regular user-invocable skills (`/commit` etc.) still pass through. **908 tests pass.**

### Palette Plumbing: Argument Honour + Parser Fix

Two follow-up commits fixed subtle bugs exposed by the new ASKAI commands:

**Palette honours typed arguments on Enter.** The command palette was always executing `cmd.name` from the selected row, so typing `ASKGEMINI AAPL,MSFT what's their debt?` fuzzy-matched to `ASKGEMINI` and then dropped everything after the command name — the chat window opened empty with no research packet. Fix: on Enter, if the input contains whitespace the **raw input** is passed to `handle_command` verbatim; otherwise the palette selection is used as before (fuzzy-match stays intact for short typing). Click-to-execute still runs `cmd.name` with no args. MRU dedupes on the leading token now so `ASKAI AAPL` and `ASKAI MSFT` collapse to one entry.

**Argument parser: stop swallowing question words.** `handle_command()` upper-cases the entire command string before `parse_ask_args()` runs, so my original `is_tickerish` check based on `is_ascii_uppercase` treated every word in a user question as a ticker. Typing `ASKGEMINI AAPL,MSFT what is your opinion...` ended up pushing a packet for symbols `[AAPL, MSFT, WHAT, IS, YOUR, OPINION, ...]` which was obviously wrong. New contract: **the first whitespace-separated token is the comma-separated symbol list; everything after the first whitespace is the question, preserved verbatim.** Space-separated symbol lists are no longer accepted — use commas. Added 7 regression tests: single-symbol, comma-separated, single+question, multi+question (the original bug), dedupe, empty input, and special-character tickers (BRK.B, RDS-A, BTC-USD).

## MT5 Parity: MTF_MA and MultiKAMA Plot Every Timeframe

**A subtle parity bug fixed.** `compute_mtf_sma` and `compute_multi_kama` previously skipped any timeframe `<=` the current chart TF, which meant a W1 chart only rendered the MN1 line from MTF_MA (1/6 of the buffers) and only the MN1 KAMA from MultiKAMA (1/5 of the buffers). **MT5's `MTF_MA.mqh` declares all 6 plotted buffers (H1/200, H4/200, D1/200, W1/200, W1/100, MN1/100) as `INDICATOR_DATA` with no chart-period guard.** `MultiKAMA.mqh` does the same for its 5 KAMA buffers. Both indicators draw every line on every host timeframe.

Guard removed in both functions. Lower-TF lines projected onto higher-TF bars are informationally thin — but they match MT5 1:1, which is the mandate. **GPU/CPU parity is non-negotiable** (see CLAUDE.md: GPU/CPU parity mandatory, no disabling).

## Alpaca FetchBars: Incremental Delta via `get_incremental_start`

**99% reduction in API load on scheduled syncs.** `FetchBars` has always called `get_bars(.., limit=1000)` with no `after_timestamp`, which meant every scheduled sync re-fetched the full lookback window — **hundreds to thousands of bars** even when only a handful of new bars had formed since the last call.

Fix: look up the second-to-last bar timestamp from the existing cache entry via `cache.get_incremental_start()` and pass it to `broker.get_bars_after()`. When the delta is empty we preserve the existing cache untouched; when there are new bars we read the existing entry, merge-dedupe by timestamp, and write the combined series back. **First-ever fetch** of a symbol still does a full lookback (no cache yet). For true full history the `BARDATA` command still exists and calls `get_all_bars()`, which ignores the lookback caps entirely.

**Net effect** on a typical daily sync with cached D1 bars: **1-2 bars returned instead of 1000, ~99% reduction in API load** and ~99% less bandwidth + parse work on each cycle. Rate-limiter pressure drops proportionally. The scheduler already runs hourly on every cached symbol — this is the kind of quiet win that only shows up when you look at the outbound request log and realise it shrunk by two orders of magnitude.

## Matrix Client: `server_name` Hint on Join

**A federation bug hiding in plain sight.** The Matrix client-server spec for `POST /_matrix/client/v3/join/{roomId}` recommends passing `?server_name=<host>` to tell your homeserver which federation peer to ask about the room. When the hint is missing and your homeserver hasn't resolved the room before, it returns `M_UNKNOWN: "No known servers"` — even if the target homeserver is your own.

Fix: derive `server_name` from the suffix of the room id/alias so it works regardless of which homeserver hosts the room. Also `%23`-encode `#` for alias support, and surface "already joined" as a positive result instead of a silent no-op. The terminal's SHARE-to-Matrix feature (see last update) was occasionally failing on first-run for users who hadn't previously seen the room — this makes the first join succeed.

## The Full Repo O(1) Pass

**Six commits in one sweep. One obsession: kill the N+1, kill the per-frame allocation, kill the redundant SQL parse.** After ADR-106's mimalloc + max-release-profile landing, the natural next question was "where is the terminal still doing N work that could be O(1)?" Turns out: a lot of places. What follows is five batches of a **full-repo O(1) pass** plus the opening batch of round 2.

### bg_rev: Derived Caches Only Rebuild When BG Moves

**The biggest single win.** The BG thread replaces `self.bg` atomically every cycle; the render thread reads from it every frame at monitor refresh rate. Multiple derived caches in the render path — `cached_scope_syms`, `cached_scoped_fundamentals`, `cached_mt5_symbols` — were being **rebuilt from scratch every frame**, even when the BG data hadn't changed. That's:

- **~500 Fundamentals struct clones per frame** (~1 MB of allocation churn) for the scoped fundamentals cache
- **A fresh HashSet rebuild** from `detailed_stats` with N `split+upper` per frame for the MT5 symbols cache
- **Per-frame rescoping** of symbol lists that only change when the user switches broker scope or BG refreshes

Fix: introduce a `bg_rev` monotonic counter that bumps whenever the BG thread swaps `self.bg`. Derived caches key on `(bg_rev, broker_scope)` and only rebuild when the key changes. A cache that used to fire **60 times a second** now fires **once per BG cycle** (every few seconds). That's ~3 orders of magnitude fewer rebuilds.

`get_sparkline` now returns `Arc<Vec<f64>>`. The 6 local sparkline maps (unusual volume, EV scanner, fundamentals window, dividend calendar, outlier table, etc.) store the Arc so per-row clones become **O(1) refcount bumps** instead of copying 30 f64s × N rows per frame. For a 100-row scanner open, that's 6,000 f64 copies per frame replaced by 6,000 integer increments.

Four other things in the same commit:
- **`fuzzy_score` palette search**: precomputed `COMMANDS_LOWER` table + caller lowercases query once. Was doing `2 × N .to_lowercase()` allocations per frame while the palette is open. Replaced with constant-string slice lookups.
- **darwin_breakdown positions join**: `.map(|d| d.clone()).collect::<Vec<String>>()` → `.map(|d| d.as_str()).collect::<Vec<&str>>()`. No more per-frame String clone per DARWIN per position.
- **Pre-normalize to uppercase at load time**: `sec_filings.ticker`, `insider_trades` keys, `congress_trades.ticker`, `unusual_volume_results` symbols. Per-frame scope filters can now use `contains(s.as_str())` directly — no fresh `to_uppercase()` allocation per record per frame.
- **`evict_lru` in the bar cache**: N per-row `DELETE` calls replaced with a single chunked `DELETE ... WHERE key IN (?, ?, ...)`. **~100× faster** on large eviction batches.
- **`get_sector_exposure`**: `sector_map` value was `(Vec<String>, ...)` with `Vec::contains` O(N) dedup in the hot loop. Swapped to `HashSet<String>` for O(1) insert + dedup, materialized to sorted `Vec` at output.
- **SEC scraper N+1**: replaced N per-symbol `SELECT last_scrape_date` round-trips (each in its own `spawn_blocking` with its own DB connection) with a **single upfront batch** `SELECT ticker, last_scrape_date FROM sec_scrape_index` into a HashMap. One query instead of N.

**557 engine + 85 native tests still pass. Zero warnings.**

### Batch 2: LAN Sync Buffer Reuse, Bulk KV Drain, Chart Bare Hoist

**Every batch finds something.** `lan_sync::import_table_json` was allocating both a `Vec<Value>` and a `Vec<&dyn ToSql>` for every row during multi-thousand-row imports — millions of heap allocations when importing a full LAN sync snapshot. Rewrote to reuse one `Vec<Value>` buffer across rows and feed rusqlite via `params_from_iter(buf.iter())`. One allocation instead of N.

`cache::drain_queue` got the same treatment as `evict_lru`: N per-row `DELETE ... WHERE key = ?` inside the transaction replaced with chunked `DELETE ... WHERE key IN (?, ?, ...)` at CHUNK=512. Same IN-list pattern, same ~100× speedup on large batches.

`list_kv_entries_since` (polled by LAN sync on every tick) now uses `prepare_cached` to skip the SQL re-parse.

**The MT5 live bid/ask refresh** (fires every 30 frames at 60Hz = twice a second) was computing `chart.symbol.replace('/', '').to_uppercase() + split(':').collect()` **once per quote per chart** inside the inner quote × chart loop. With 50 quotes × 20 charts that's 1,000 redundant allocations per refresh. Hoisted `chart_bare` out of the inner loop — now computed once per chart per cycle. 20 allocations instead of 1,000.

**`draw_chart` sub-panes**: `Vec::with_capacity(bars.len())` for the 6 per-frame `points: Vec<Pos2>` buffers in supertrend, MACD (line + signal), stochastic (%K + %D), ADX (triple-series), plus Bollinger upper/lower fill vecs. Skips the geometric reallocation sequence egui normally does as points are pushed — fewer `memcpy` calls during the chart render.

### Batch 3: Trade Marker Binary Search + Sparkline Uppercase Drop

**`draw_chart` trade markers**: the marker list is already sorted by `bar_idx` in `build_trade_overlay()`. Use `partition_point` to binary-search the first marker `>= start_idx`, then `take_while` until `end_idx`. **Skips the O(N) full-list scan every frame** when the account has thousands of historical markers. On a DARWIN with 5,000 trade markers and a 200-bar visible window, this is 5,000 comparisons per frame replaced with ~log₂(5000) ≈ 13 comparisons plus 200 takes.

**Sparkline HashMap lookups**: `uv_sparklines` (unusual volume), `sparklines` (EV scanner), `fw_sparklines` (fundamentals window) all had `.get(&sym.to_uppercase())` calls. But `sym` is **already normalized uppercase at creation** in all three cases (checked via tracing back through `parse_yahoo_data` and the scanner constructors). Swapped to `.get(sym.as_str())` to drop **N String allocations per row per frame** when the scanner is open.

**Supertrend points** Vec pre-sized to `bars.len()` to skip the geometric realloc.

### Batch 4: `prepare_cached` for Bar Cache Hot Reads

**SQLite reparses every `prepare` call.** That's the SQL parse + query-plan cost. `prepare_cached` keeps the parsed statement in the connection's statement cache and reuses it across calls — the parse cost is paid once per connection lifetime and amortised across every call for the life of the worker thread. No behavioural change, just the parse overhead removed.

Converted on the hot bar-cache read paths:
- `cache::detailed_stats` — called every BG cycle by the background thread
- `cache::all_keys` — called by LAN sync, symbol search, scanners
- `cache::get_raw_blob` — called in LAN sync migration and BG jobs
- `cache::read_bid_ask` — called every 30s from the UI to refresh forming bars
- `cache::get_bar_timestamp_range_with_conn` — called for every crypto entry on every BG cycle (was reparsing the same SQL N times per phase)
- `app.rs` BG Phase 1c `detailed_stats` direct query — same treatment

Each saves the SQL parse + plan cost; the win scales with the number of calls inside a hot loop. Multiply by the BG cycle rate and it adds up.

### Batch 5: `prepare_cached` for DARWIN BG Queries

**Same pattern, different hot loop.** The BG thread iterates ~10-20 DARWIN accounts every cycle and calls into `darwin::get_daily_returns`, `get_darwin_open_positions`, `get_darwin_summary`, and `list_darwin_accounts` — each was re-parsing the same SQL text on every call. All converted to `prepare_cached`:

- `get_daily_returns` (called N times inside `get_darwin_correlations` + `get_portfolio_daily_returns` + several other aggregators)
- `get_darwin_open_positions` (called N times inside `get_portfolio_open_positions`)
- `get_darwin_summary` — its `darwin_positions WHERE account = ?` and `darwin_deals ORDER BY time` queries
- `list_darwin_accounts` (called at the top of every BG phase entry point)

On a portfolio with 15 DARWINs, a single BG cycle used to do ~60 redundant SQL parses across these four entry points. Now: 4 parses, amortised across every subsequent call.

### Round 2 Batch 1: SEC N+1 Drop, Log Pre-Format, Bound Drain

**Round 1 was the obvious stuff. Round 2 finds the hidden N+1s.** `sec_filing::scrape_filings_for_ticker` was doing **3 per-filing SQL round-trips** on every filing: exists check, insert, alert-dedup `COUNT`. For a 100-filing batch that's **~300 round-trips**. Replaced with two bulk preloads into HashSets before the loop, plus **one transaction** that batches the INSERTs via prepared statements. DB work drops from ~300 round-trips to **2 + 100 prepared inserts** — all inside one tx.

`fundamentals::scrape_batch` was doing **two per-ticker SELECTs** before every Yahoo call (`scrape_failures WHERE symbol=?` and `fundamentals WHERE symbol=?`). A 500-ticker scrape was **1000 DB round-trips just for bookkeeping** before any Yahoo request fired. Swapped for two upfront `SELECT symbol [, last_updated]` scans into a HashSet + HashMap. **1000 round-trips → 2.**

**Log bottom panel rendering**: pre-format `display: String` at `LogEntry::new`, drop the per-frame `format!("[{}] {} {}", ...)` over all 200 log entries every render. **~12,000 allocs/sec → 0** on the log render path. Removed the now-unused `icon()` helper and the `timestamp` field (folded into `display`).

**`broker_rx` drain**: cap at **128 messages per frame** and call `ctx.request_repaint()` when the cap is hit. A flood of broker messages can no longer stall the render thread — leftover messages pick up on the next frame. Bounded work per frame is non-negotiable for a 60Hz UI.

**Symbol Explorer `parse_cache_key`** was returning `(&str, String, &str)` and collecting `Vec<&str>` via `split(':').collect()` per cache-key. Rewrote with `splitn` + byte-count prefix check — **no heap Vec, same semantics**. Replaced `symbol.replace('/', "").to_uppercase()` (two allocs) with `replace(..)` + in-place `make_ascii_uppercase` (one alloc).

**Symbol Explorer `fund_map`** now keys on `&str` (since `f.symbol` is uppercase via `parse_yahoo_data`) — dropped N `to_uppercase` allocations per frame.

**`compute_all_indicators` pivot-previous-close**: hoisted `last_day` out of the reverse-find closure. Was being recomputed on every bar in the scan — classic hoisting miss. One bind outside the loop, done.

**Command palette recent-command check**: per-row `recent_commands.iter().take(10).any()` → `HashSet<&str>` built once outside the render loop. Quadratic palette render killed.

### Round 2 Batch 2: Fused Math Passes, DARWIN prepare_cached Sweep

**The analytics layer had compounding math waste.** `darwin::get_darwin_correlations` was doing a **3-pass Pearson**: one pass for `mean_a`, one for `mean_b`, then a deviation pass across an intermediate `Vec<(f64, f64)>` pair buffer. Replaced with a single-pass running-sums formula that iterates the smaller of the two date maps. Zero allocation inside the inner loop. On a 20-DARWIN correlation matrix that's **N²/2 fewer 3-pass setups per BG cycle**.

`screener::find_stat_arb_pairs` was doing **3 separate passes over the spread series** (mean, variance, std) before the AR(1) half-life **4-pass regression** fired. Fused to: one pass builds spreads and accumulates sum + sum_sq simultaneously, then a single-pass AR(1) coefficient computation via running sums of x, y, xy, x².

`backtest::TradeReport::from_trades` was building a `wins: Vec<f64>`, a `losses: Vec<f64>`, and then summing them for `total_pnl` — three passes plus two intermediate Vecs. Replaced with a single branchless loop accumulating `gross_profit / gross_loss / total_pnl / n_wins / n_losses` in one traversal. Zero intermediate allocation, zero branch mispredicts on the inner path.

**DARWIN `prepare_cached` sweep** hit **15 more per-account analytics queries**: `get_darwin_equity_curve`, `get_darwin_pnl_by_symbol`, `get_streak_analysis`, `get_hourly_pnl`, `get_day_of_week_pnl`, `get_hold_time_stats`, `get_symbol_rotation`, `get_sizing_efficiency`, `get_cost_analysis` (both inner queries), `analyze_slippage`, `compute_tax_lots`, `get_equity_history`, `get_portfolio_equity_curve`, and the per-account deals query inside `get_timing_divergences`. Every one of these is called N times per BG cycle across every DARWIN on the account list — parse + plan cost is now amortised.

`darwin::get_hourly_pnl` was also doing `dt.format("%H").to_string().parse::<usize>()` — **allocating a String on every row just to read one integer**. Replaced with `dt.hour() as usize` via chrono's `Timelike` trait. Zero allocation on the hour-bucket loop.

**`native/src/app.rs` fine-grain wins**: hoisted `last_day` out of the pivot-points reverse-find closure (was being recomputed on every scanned bar). Right-panel active symbol display swapped `split + Vec<&str>::collect` for `rsplit` + `next`. Three more broker-message handlers (MTF Live Quote, Watchlist Quote, 30s bid/ask refresh) got the same `rsplit` treatment when deriving the chart-bare symbol. Symbol-autocomplete fundamentals scan dropped the redundant `.to_uppercase()` on the already-uppercase `f.symbol` field.

### Round 2 Batch 3: prepare_cached Sweep on sec_filing + fundamentals Hot Reads

Same treatment, different module. `sec_filing::get_filing_alerts` (drives the alerts panel), `get_all_filings` and `get_all_insider_trades` (run once per BG phase to refresh the cache), and `get_unfetched_filings` (backs the content backfill worker) all switched from `conn.prepare` to `conn.prepare_cached`. Each is called every BG cycle — the parse + plan cost is now paid **once per connection lifetime**, not per call.

Added `check_keywords_in(&keywords, content)` taking a **pre-loaded slice**. Batch callers used to hit `SELECT keyword FROM sec_keyword_watchlist` **once per filing** they were scanning; now the keywords are loaded once at the top of the batch and the check is pure in-memory.

`fundamentals.rs` got the same sweep: `get_fundamentals` (per-symbol research panel reads), `get_all_fundamentals` (BG fundamentals cache refresh), `get_upcoming_earnings` + `get_upcoming_dividends` (BG calendar refresh), `get_quarterly_financials` + `get_institutional_holders` (research panel per-symbol reads) — six functions, all on hot paths, all now `prepare_cached`.

### Round 2 Batch 4: Single-Pass Statistics Across Engine Analytics

This is the batch where the **raw-moments formula** pays off at scale. The canonical textbook way to compute variance is to take a mean pass, then a deviation pass: `Σ(xᵢ - μ)²`. The raw-moments form is `Σxᵢ² - n·μ²` — same result, **one pass instead of two**, numerically stable at the data scales this engine operates on.

**`var::detect_outliers`** (sector IQR) was doing **3 passes**: sum to get mean, a `.iter().map().collect::<Vec<_>>()` of deviations, then `std_dev` calling a Welford pass on the collected Vec. Fused to one pass using raw-moments. Zero intermediate allocation.

**`var::detect_multi_outliers::z_scores`**: same treatment. The closure now folds mean + variance into a single pass over the per-dimension values.

**`screener::compute_symbol_correlation_matrix`**: single-pass running-sums Pearson replaces two intermediate `ret_a` / `ret_b` Vecs and three passes (mean_a, mean_b, deviation accumulators). The correlation loop walks the aligned close slices **once per pair** and accumulates sums directly into `cov / var_a / var_b` formulas. For an N × M matrix that's **N²/2 fewer 2-allocation pair setups** per BG invocation of the screener.

**`screener::compute_hv_cone`**: two wins here. First, build the log-returns series **ONCE** and share it across all lookbacks — the old code was recomputing it per lookback. Second, replace the O(lookback · window) rolling-HV loop with an O(N + lookback) sliding sum + sum_sq update: each window advance is **one add and one subtract** instead of re-scanning the whole window. For `252 × [10,30,60,90,120,180,252]` that's **~120k inner ops → ~1.7k**. Also swapped the post-sort `filter(<= current).count()` rank for `partition_point`.

**`darwin::get_rolling_var`**: reuse the `pnls` buffer across sliding windows instead of allocating a new `Vec<f64>` per iteration. On a 500-day series that's **~500 allocations eliminated** per call. Fused mean + variance over `return_pct` into a single loop via raw-moments.

**`darwin::compute_var_full`** was the worst offender: **five separate loops** — build `pnls`, build `returns`, sum pnl, sum returns, variance pass, downside_sq + downside_count, max_dd — all fused into **ONE loop over `daily_returns`**. Also eliminates an intermediate `Vec<f64>` (was building both `pnls` and `returns`). Still sorts `pnls` for the percentile VaR computation, but sorts the buffer we just built rather than a clone.

### Round 2 Batch 5: put_kv_dedup Static Keys, Trade Autocorrelation Single-Pass

**Small but hot-path**. `native/src/app.rs::put_kv_dedup` had all five call sites passing `&'static str` literals — `"broker:positions"`, `"broker:watchlist"`, etc. Changed `kv_write_hashes` and `kv_write_times` from `HashMap<String, ...>` to `HashMap<&'static str, ...>` and took the key as `&'static str`. Drops **one `key.to_string()` allocation per call** on the hot BrokerMsg handler path — ~5 allocs × every broker tick.

`engine/src/core/darwin::compute_trade_autocorrelation`: switched the `darwin_positions WHERE account = ?` profit query to `prepare_cached`, and fused the mean + variance computation into a single pass over `profits` via the raw-moments formula (was two traversals).

### Round 2 Batch 6: Sliding-Window Volatility on Remaining DARWIN BG Paths

**The last of the O(N·window) offenders.** `darwin::compute_conditional_var` and `detect_market_regime` were both computing a 20-day rolling volatility via **O(N·20) double-pass per window**. Replaced with a sliding sum + sum_sq: on each advance, subtract the outgoing element and add the incoming one, then derive variance from raw moments. Total work drops from **O(N·20) → O(N)**.

`darwin::compute_signal_decay` was the big one. The rolling Sharpe window was **building a fresh `Vec<f64>` of returns per iteration** and then doing mean + variance in two traversals. Switched to the same sliding-sums pattern. Was **O(N · window · 2)** — for a 500-day series × 90-day window × ~10 accounts per BG cycle that's **~900,000 ops**. Now **O(N) → ~5,000 ops per account**. That's a **180× reduction on a single function**, compounding across every BG phase tick.

`darwin::simulate_margin_call`: build the `returns` buffer **AND** accumulate sum + sum_sq **in one pass** instead of collect-then-two-traversal. The Monte Carlo loop below still needs the `Vec` for random indexing, so the allocation stays — but the stats fold is free now.

`darwin::compute_trade_autocorrelation`: confirmed that the single-pass raw-moments variance (`sum_sq − n·mean²`) is **numerically stable** for the trade-count scales this function runs on. It always gates on `profits.len() > 10` before proceeding, and at that scale the catastrophic-cancellation risk of raw-moments variance vs. Welford is negligible.

---

**The meta-point — Round 2 edition**: eleven commits across two rounds, **+438 Rust insertions against 196 deletions** over the whole surface. This is **not a rewrite** — it is what happens when you stop treating "fast" as a binary and start asking where the compounding waste lives. Round 1 killed per-frame cache rebuilds and N+1 SQL patterns. Round 2 proved the analytics layer itself had **compounding math waste**: triple-pass Pearson correlations, nested window scans for rolling volatility, fresh `Vec<f64>` allocations inside sliding-window loops, and `String` allocations just to read an integer hour field. The common thread: **single-pass raw-moments** (`sum, sum_sq → mean, variance`) replaces the two-traversal formulas that textbooks teach and every implementation ships. Numerically stable at the scales these functions operate on, and cuts both the traversals and the allocations in half. `compute_signal_decay` alone went from ~900k ops per BG cycle to ~5k — **180× on a single function**, compounding across every BG phase tick.

## SEC Window: Hash-Keyed Cache Rebuild + DB-Cached Filing Viewer

**Two commits, one obsession: stop re-deriving SEC window state every frame.** The SEC window was doing **per-frame dedup** (`format!()` per row building a `"{ticker}:{form}:{date}"` key), multi-field `.to_lowercase()` search across ticker+form+title+accession, a fresh `HashSet` allocation per frame, and a full `sort_by` over every filing in the database. On a 5,000-filing scope that's thousands of allocations and string comparisons **every frame the window is open**, even when nothing has changed.

Fix: hoist **all four tab datasets** — filings indices, insider rows + 14-day clusters, timeline monthly grouping, per-tab filing counts — into a single `rebuild_sec_caches()` function keyed by a **`u64` hash** (DefaultHasher over `bg_rev + broker_scope + filters + query + sort_mode`). Steady state is now **zero O(N) work**; caches rebuild only when the hash key actually changes. Filings dedup switched from `format!("{}:{}:{}")` to a tuple `HashSet<(String, String, String)>` key — no intermediate allocation. Search reduced to symbol-only uppercase compare (ticker is stored upper at ingest, so no case-folding needed).

**Chart "+" buttons across every table.** Added an inline "open new chart tab" button next to symbol cells in: Watchlist (custom painter — new `col_plus` at `avail_w - 28`, relative-x hit-test), Outlier Scanner (both multi-outlier and single-metric tables), SEC Filings + Insiders tabs (wrapped in `ui.horizontal` to stay one Grid column), Fundamentals, Holders, and Dividend Screener headers. Unified UX across every surface that shows a ticker — click the symbol for context menu, click "+" for instant chart.

**MT5 auto-sync cadence fixed.** The auto-sync interval was 5 minutes but BarCacheWriter writes at `UpdateIntervalSec=30`. Dropped the UI sync to **30 seconds** (120 frames × 250ms idle) so fresh bars propagate from MT5 to the terminal at the same cadence they land in the cache.

**DB-cached filing viewer + heuristic summarizer.** The SEC viewer now serves filing text from the `sec_filing_content` DB cache **before** re-fetching from EDGAR — no more waiting for a network round-trip to re-read a filing you've already downloaded. Summary cache invalidated on fresh content. New `sec_filing::summarize_filing()` is a **deterministic, form-type-aware heuristic**: 8-K extracts numbered Items, 10-K/Q extracts Risk Factors + MD&A sections, DEF 14A extracts proposals, S-1 extracts Use of Proceeds, 13F reports row count, Form 4 falls back to a generic insider summary. GUI renders a headline + collapsible bullets/sections above the raw filing text.

**LAN sync whitelist extended**: `sec_filing_content` added with `fetched_at` as the incremental sync column, so LAN peers replicate cached filing bodies instead of each peer re-fetching independently from EDGAR. **Gemini CLI window** got a dynamic `ScrollArea` height that fills available space instead of a hard-coded 340px, constrained to viewport.

---

## News Pipeline: 6-Source Aggregator with FTS5 Search

**Finnhub was sparse for MT5/Darwinex symbols.** The commit-1003 snapshot above still relied on Finnhub as the single news feed, which meant CC, NCLH, CAR, and most of the Darwinex equity universe returned empty result sets on news lookup. A dedicated `engine/src/core/news.rs` now aggregates **six sources**:

- **Keyless sources:** GDELT (global news graph), Yahoo RSS (per-symbol feeds), SEC EDGAR (official filings)
- **Free-tier keyed sources:** Marketaux, Alpha Vantage, Financial Modeling Prep

Dedup runs on `SHA-256(url)` with field-merge `ON CONFLICT` — syndicated stories from multiple sources collapse to one row, but each source contributes whatever fields the others left blank. The merged result is a single `research_news` row with summary + headline + publisher + source attribution.

**FTS5 virtual table** mirrors `headline + summary` for **O(log n)** cache search. Type a keyword, get hits across every ingested source in milliseconds without walking the backing table. `research_news` joined the LAN sync whitelist — the cache server scrapes once, and every client pulls incrementally by `updated_at` timestamp.

**SEC-viewer-style two-pane reader.** The NEWS window got a full rewrite matching the SEC filing viewer pattern: clickable list on the left, lazy-loaded body on the right. Buttons: **Load Cached** (from SQLite), **Fetch All Sources** (6-source sweep), **Scrape All** (MT5 + Alpaca + tastytrade symbol universes), **FTS search**. The "(0)" empty-state bug from the launch window is gone — AI-ingested articles appear in the panel on the next tick.

## ADR-130: AI Web Research Ingest — Closing the Round-Trip Gap

**Problem:** Packets flow out to Claude/Gemini; the web-search articles those agents fetch get lost on every turn. The research context the AI just built is thrown away the moment the chat window closes.

**Fix:** Every outbound packet now ships with a **Return Path footer** instructing the agent to echo its articles back in a `===TYPHOON_INGEST===` block. The `INGEST_RESEARCH` console command parses that block — **lenient: json fences, alias fields, tolerant of wrapper text** — and appends each article to a per-symbol bag (FIFO, 50 cap, URL-deduped, timestamp-wins).

- **New table:** `research_web_articles` (schema v23), `WebArticle` struct, LAN sync replication
- **BrokerMsg::IngestResearchArticles** handler upserts each `WebArticle` as a `NewsArticle` into `research_news` too (source tag `"Ingested/<agent>"`) — so the NEWS panel displays them immediately without a round-trip through `LoadCachedNews`
- **Auto-refresh:** after a successful ingest, auto-dispatch `LoadCachedNews` for the active filter or first ingested symbol. No more "Claude ingested news but NEWS shows (0)"
- **LAN fan-out:** client-mode terminals forward ingest packets to the LAN server so peers converge on the same research view

The AI's web research is now **first-class terminal data**. What Claude read about CC's debt load yesterday is available to Gemini today, cached across every machine on the LAN.

## ADR-157: AI Session Persistence + RESUME Slash Commands

**Transcripts died on restart.** `engine/src/core/ai_sessions.rs` adds **zstd-compressed `kv_cache` storage** for every chat turn across all four AI surfaces (Claude Code, Gemini CLI, Codex CLI, generic AI Chat). Persists at reply-receipt sites so transcripts survive `File → Quit`.

- **Claude's `--session-id` UUID** is saved on the first turn. `/RESUMECLAUDE` rejoins the original thread — Anthropic's server still has it, and now so do you
- **Gemini / Codex / AI:** transcript replays as prompt context on the next turn (those CLIs don't expose session handles, so replay is the next-best thing)
- **Four palette-bound slash commands:** `/RESUMECLAUDE`, `/RESUMEGEMINI`, `/RESUMECODEX`, `/RESUMEAI`
- **AISESSIONS history-browser window** lists every prior session with model picker, turn count, last-message preview, and a one-click resume button

## ADR-162: Cross-Client AI Response Cache (LAN-Shared)

**One peer pays, the rest hit cache.** A `SHA256`-keyed `ai_response_cache` table intercepts every AI call in the native broker. Hash input is `(model, prompt, whitespace-normalised)`. Hit → return cached reply, bump `hit_count`, update `last_hit_at`. Miss → call the model, store, return. `updated_at` is the LAN sync delta column, so cache hits and hit-count bumps propagate to every peer on the next sync window.

**11 engine tests ship with the cache:** hash determinism, whitespace normalisation, hit-count increment, stats aggregation, recent ordering, prune TTL, etc. **Stats window** shows top queries by hit count, recent queries, total hit ratio — the cache's own dashboard.

The economics are straightforward: if four terminals on the LAN ask Claude the same question in one day, three of those calls resolve locally at zero marginal cost. For a terminal whose primary AI use case is repeated symbol research across a fixed watchlist, the hit ratio is high.

## Codex CLI Integration (ASKCODEX)

**Third AI surface lands.** `ASKCODEX SYM [question]` mirrors `ASKGEMINI`: packet-preloaded dispatch, standalone chat window with model picker (`gpt-5-codex` / `gpt-5` / `o4-mini`), one-shot `codex exec` per turn with `--skip-git-repo-check` so it runs outside a git repo.

The terminal is now **model-agnostic across four AI integrations** — Claude Code (`claude`), Gemini CLI (`gemini`), Codex CLI (`codex`), and the generic AI Chat that speaks to whichever HTTP-backed provider is configured. Every one of them receives the same research packet, the same session persistence, the same cached-response lookup. The differentiator between them is the model, not the terminal.

## ADR-148: MT5 BarCacheWriter Health-Check Protocol

**Cold-start and silent-drift holes closed.** The MT5 bar sync path had two failure modes: (1) EA running but not yet writing → client gap-requests never answered, (2) EA silently stopped writing → client thinks bars are fresh indefinitely. Both now self-heal via heartbeat.

**Engine side:**
- `SqliteCache::read_mt5_heartbeat(account_tag)` — reads the EA's heartbeat row from `bar_cache`, returns `(json, row_ts)`

**Native side:**
- `BrokerMsg::Mt5Heartbeat(Vec<(path, json, row_ts)>)` emitted from the `Mt5Sync` worker after scanning each source DB
- **Gap-fill demand** triggered when `heartbeat.row_ts` is older than `2 × UpdateIntervalSec` — forces the EA to rotate through the symbol queue even if it thinks it's idle

## ADR-166: Options Expiration Calendar (Tier 1 + Tier 2)

**Two-tier expiration intelligence.** Tier 1 is a **market-wide** calendar: weekly expirations, monthly expirations, quarterly expirations (index options), LEAPS expirations, VIX expirations. Tier 2 is **per-symbol**: the underlying's own options chain with expirations ranked by OI, volume, and days-to-expiration.

Both tiers materialize as RESEARCH_PACKET fields so the AI sees expiration context alongside the rest of the symbol's data. The Tier 2 view answers questions like "what's the nearest high-OI monthly on NVDA" without a separate options-chain query.

## Godel Parity Sweep: 65 Rounds of Indicator/Analytics Expansion

**The headline item of April.** The RESEARCH_PACKET — the markdown payload sent to every AI backend — ballooned from ~40 research surfaces in March to **320+ surfaces** by April 17. Each "godel parity round" adds 4-5 new surfaces following the same **ADR-107/108 fetcher → BrokerCmd/Msg → SQLite → LAN sync** pattern:

1. **Fetcher function** pulls data (TA-Lib derivation from bars, FMP API, SEC, Yahoo, etc.)
2. **BrokerCmd/Msg** plumbing carries the fetch request and response across the broker worker boundary
3. **SQLite cache table** persists the result for incremental LAN sync
4. **Label heuristic** converts the raw number into a bucket string (e.g., `BULL_STRONG / BULL / NEUTRAL / BEAR / BEAR_STRONG / INSUFFICIENT_DATA`) so the packet gives the AI both the raw value and a human-readable classification
5. **RESEARCH_PACKET.md docs** document the field, the source, the edge cases, and the label thresholds
6. **Tests** — 5-12 per round — covering fetch, cache round-trip, label logic, LAN sync delta column

**Cumulative surfaces by round range** (rounds 1-65, cumulative):

| Category | Examples | Surfaces |
|---|---|---|
| Fundamentals | FA, MGMT, COT, DVD, EEB, UPDG, GY, FCFY, MARGINS, REGIME, RELVOL | 60+ |
| Market structure | HRA, DCF, SVM, OMON, IVOL, WCR, BETA, DDM, WEI, MOV, INDU | 40+ |
| Factor models | RRK, QRK, VRK, VAL, QUAL, RISK, MOMF, SIZEF, PEADRANK | 25+ |
| Risk / VaR analytics | CVAR, RACHEV, UPR, LEVEREFF, DRAWDAR, VARHALF, GINI, ULCER | 35+ |
| Volatility / distribution | PARKINSON, GKVOL, RSVOL, ENTROPY, PERMEN, RECFACT, KPSS, SPECENT, SAMPEN | 40+ |
| Statistical tests | ADF, PSR, MNKENDALL, BIPOWER, DDDUR, LJUNGB, RUNSTEST, ARCHLM, JBNORM, KSNORM | 30+ |
| TA-Lib canonical | MACD, RSI, ADX, CCI, CMF, MFI, PSAR, SUPERTREND, KELTNER, FISHER, AROON, ICHIMOKU, STOCH, VWAP, WILLR, ULTOSC, KST, DPO, PPO, TRIX, VORTEX, HMA, OBV, MOM, ROC, APO, SAREXT, MIDPRICE | 100+ |
| Adaptive / advanced filters | MAMA, FRAMA, KAMA, ZLEMA, ALMA, T3, TRIMA, VIDYA, SMI, PVT, HT_TRENDLINE, HT_DCPHASE, HT_SINE, HT_PHASOR, LINEARREG, LINEARREG_SLOPE, LINEARREG_ANGLE | 45+ |
| Pattern / structure | FRACTALS, ZIGZAG, PIVOTS, HEIKIN, DONCHIAN, ALLIGATOR, GATOR, DEMARKER, BBSQUEEZE, SQUEEZERANK | 25+ |

**File-level impact** (as of round 65):

- `engine/src/core/research.rs` — **52,559 lines** (from ~6,000 at blog-1003 snapshot)
- `docs/RESEARCH_PACKET.md` — **6,211 lines** covering 323 `####` field entries
- `native/src/app.rs` — each round adds ~500 lines of window + UI wiring
- `engine/src/core/lan_sync.rs` — incremental sync columns for every new table

**Per-round ADR cadence.** Every round ships its own ADR documenting the label thresholds, edge-case handling (insufficient-data gates, n<window fallback), mathematical formulation, and the rationale for picking that indicator (why MOM distinct from ROC, why MIDPRICE distinct from MIDPOINT, why SAREXT distinct from SAR). The ADR corpus grew from ~107 entries in March to **156 entries** by mid-April — roughly one per round plus the infrastructure ADRs (130, 148, 157, 162, 166).

**What this buys you.** The AI no longer needs to compute these itself. When you `ASKCLAUDE NVDA write me a technical read`, the packet already contains ADX current value + label, MACD histogram + crossover state + label, ICHIMOKU cloud position + Tenkan/Kijun state + label, a 65-wide Hurst exponent + tail-risk + KPSS stationarity + GARCH(1,1) volatility forecast, and ~300 more fields. Claude spends its tokens on **interpretation**, not recomputation.

## MT5 Bar Sync: 4-Part Key Collation (ADR-056 Regression Fix)

**CC and CAR stuck out-of-sync across every timeframe.** `detect_mt5_gaps()`, `write_mt5_demand_txt()`, and `save_session()` were looking up cache timestamps using 3-part keys `mt5:{sym}:{tf}` while BarCacheWriter stores **4-part keys** `mt5:{broker}:{sym}:{tf}` per ADR-056. Every lookup returned 0, gap detector marked all symbols "empty", and every heartbeat fired max-bars demand requests that saturated the EA rotation queue.

Fix: unify every lookup to the 4-part key by threading the broker tag through the call chain. Gap-detect loops now correctly see the cached bars and only demand what's actually missing.

## MT5 Self-Heal: DARWIN Positions + Right-Sized Gap-Fill

**Open positions weren't being chart-refreshed.** `detect_mt5_gaps()` previously only scanned **open charts** — held positions not currently charted were excluded from gap detection. Positions on CC / CAR held but never charted stayed stale until a user clicked them open. Fix: mirror the DARWIN loop from `write_mt5_demand_txt()` so position symbols also trigger `demand.txt` fill requests.

**Right-sized gap-fill.** Switched from **always-max_bars** to **gap-sized** requests. When stale (vs. empty), compute the actual missing bar count from `period_ms` with 10% headroom, cap at `max_bars`. Avoids wasting EA rotation asking for 1,500 H1 bars when ~50 were missing.

## Alpaca Bar Data: adjustment=all + Split-Cache Purge

**Symptom:** Charts for split-affected symbols rendered as a long flat region followed by a vertical hockey-stick, while TradingView showed a clean trend. **Root cause:** Alpaca bar fetches never passed the `adjustment` parameter — every cached stock series was **raw (pre-split)** for old history and **post-split** for fresh bars, the two glued together in the same chart.

**Fix across three surfaces:**
- `alpaca::get_bars_after`: request `adjustment=all` for stock bars (skip for crypto endpoint which does not accept the field)
- `cache::open`: one-shot migration purges existing `alpaca:*:*` stock bar cache entries on first launch of the fixed build so the next fetch re-pulls with adjustment applied
- Harden `pack / merge / try_load` paths to survive partial-purge state transitions

## Update (2026-04-18): MT5 Sync Pipeline Rewrite, Self-Heal, 100K-Bar Integrity Target

45 commits in ~24 hours. The MT5 bar pipeline — the data plumbing that feeds every chart, every DARWIN analytic, every RESEARCH_PACKET surface — got rewritten end-to-end. The surface changes are small; the engineering underneath is a reset.

### demand.txt v3-Only + Common/Files Delivery

**The entire MT5 demand signal was being dropped at the EA's front door.** Two bugs compounded into a null data pipeline:

1. `write_mt5_demand_txt` and `save_session` built a full v3 payload (`SYMBOL:TF:LAST_TS_MS:MAX_BARS` per row), then wrote a *different* bare-symbol-only variable to the actual demand.txt files. The EA only ever saw v1 bare symbols. Timestamped gap-fill semantics never activated — every rotation cycle re-exported every symbol from scratch.
2. BarCacheWriter reads `demand.txt` with the `FILE_COMMON` flag, which resolves to `<install>/Common/Files` or the Wine AppData/Roaming path. Terminal was only writing to `MQL5/Files` next to the DB — **a directory the EA never reads**.

Refactored into four shared helpers: `collect_mt5_demand_local`, `parse_mt5_demand_txt`, `render_mt5_demand_txt`, `flush_mt5_demand_txt`. Format is v3-only now: `MAX_BARS=0` for passive demand (normal rotation), `MAX_BARS>0` for gap-fill requests that force-export N recent bars. v1 and v2 paths deleted. New `mt5_common_files_dirs()` helper enumerates candidate `Common/Files` directories under each configured MT5 db path — writes fan out to every candidate that exists. Ramdisk-symlink layouts (deploy_ramdisk.sh) now resolve correctly via the instance name embedded in the tmpfs filename.

1 Hz flush cadence with content-hash dedup means fresh-tab-open latency is sub-second without flooding /dev/shm. Idle-tick flush now includes gap requests — previously, the heartbeat path would stage gap-fill demand and the idle flush one second later would overwrite demand.txt with the non-gap set, silently erasing the request before BCW's ~60 s reload window ever saw it.

### Self-Heal: Pass-2 Cache-Wide Scan + Repair/Steady-State Modes

**detect_mt5_gaps previously only scanned pairs the user had open.** Anything else in the cache that fell behind — rotation lag, BarCacheWriter restart, /dev/shm wipe, Wine hibernate, transient broker dropout — stayed stale until the user happened to open its chart.

New pass-2 self-healing sweeps the entire local cache. Any `mt5:{sym}:{tf}` with `bars>0` lagged more than **5×TF** behind now queues a gap-fill request automatically. Pass-1 (watched pairs) keeps the aggressive 2×TF threshold. Queue caps at 256 most-stale entries sorted by `lag ÷ period`, so demand.txt stays bounded (~25 KB at cap) and the EA's linear gap-fill scan stays cheap. Empty pairs (`bars==0`) are skipped — baseline rotation handles cold-start warm-up.

Mode tracking: `mt5_repair_mode` flag flips to false after 3 consecutive pass-2 runs find no staleness (~90 s at 30 s cadence). Log line reports the transition. Periodic self-heal (`frame_count % 120 == 90`) runs unconditionally when any MT5 db path exists, regardless of auto-sync toggle — matches the user-intent phrasing: *"run gap fill / self healing until all timeframes/symbols are repaired, then only normal predictive sync."*

### 100K-Bar Integrity Target + Coverage-Gap Flag

Per-TF integrity target declared in `mt5_tf_spec()`: D1/W1/MN1 get full-history (100K covers 274 years of D1), M1–H4 get last 100K bars matching BCW's `MAX_BARS_PER_KEY`. Pass-2 self-heal gains a **second trigger** alongside staleness: any `(sym, TF)` whose bar count is <95% of the integrity target flags as a **coverage gap** even when the newest bar is fresh. Scoring combines lag-in-periods with coverage-deficit-permille so both metrics compete for queue slots on a common scale — a severely-shallow 1Day cache ranks above a modestly-lagging 1Min.

**Broker-saturation memory** prevents the coverage-gap flag from firing forever on symbols the broker genuinely can't backfill past (new listings, short-history tickers). Per-`(sym, tf)` tracker holds `(last_flagged_count, consecutive_noops)`. After 2 consecutive cycles where the count hasn't grown, the shallow flag is suppressed as "broker saturated." Any growth resets the counter; reaching ≥95% forgets the memory entirely so subsequent regressions flag cleanly. Memory is bounded by cache key count (~225 KB ceiling).

### Alpaca + tastytrade: MT5 Priority + Full-History First Fetch

Two long-standing limitations on non-MT5 bar fetches removed:

- **MT5/Darwinex priority check.** Before dispatching any HTTP request, the handler probes `mt5:{BARE_UPPER}:{TF}` — if MT5 has bars, skip the broker fetch entirely. Saves free-tier rate-limit quota for symbols Darwinex carries anyway. Crypto naturally falls through since MT5 has no crypto keys.
- **Full-history first fetch.** `FetchAllBars` was defined but dispatched nowhere — dead code. First fetch (when `after_ts` is None) now routes through `get_all_bars`, paginating from 2000-01-01 (stocks) / 2015-01-01 (crypto) with no total cap. A tokio forwarder bridges chunk-by-chunk progress strings to `BrokerMsg::OrderResult` so users see live updates during multi-minute full-history fetches. tastytrade's 365-day lookback clamp extended to 2000-01-01 — DXLink returns whatever the instrument actually has.

Symptom before the fix: fresh installs only ever saw the last ~1000 bars for Alpaca-only symbols, even though the underlying broker method supported the full paginated history.

### Crypto Backfill: CC + Kraken Union with Shared Rate-Limit Back-Off

Two tightly-coupled fixes triggered by rate-limit logs recurring every ~15 s — each `(symbol, TF)` pair was re-hitting the API to re-learn the same 429 state:

- **Process-wide `RATE_LIMITED_UNTIL_SECS` clock.** On HTTP 429 or in-body "rate limit"/"upgrade" message, CryptoCompare arms a 10 min back-off. Subsequent `fetch_ohlcv` calls short-circuit with `Err(...)` before the HTTP round-trip. Callers drop out immediately and can route to Kraken instead. `rate_limited_for_secs()` lets callers probe the back-off state *before* dispatching.
- **Per-source 6 h freshness + union merge.** Per TF, CC and Kraken fetch independently; a fresh Kraken entry no longer short-circuits the whole TF. Chart-side merge dedups both keys, so the union gives CC's longer history plus Kraken's recent 720-bar window. Status messages differentiate fresh / back-off / unavailable / empty per source.

### Storage Manager: First/Last Bar + FROZEN Status

Storage Manager window gained per-row bar-range visibility: **First Bar** (oldest timestamp), **Last Bar** (newest), **Status**. Status is `ok` if last bar is within 24× the TF period, `FROZEN` (red) if older, `empty` if the blob has no bars, `…` while the BG thread backfills the range cache, `?` for unknown TF suffixes. The FROZEN multiplier is deliberately loose (24×) so weekend/holiday gaps don't trip M1/M5. A FROZEN D1 entry means "no new daily bar for 24 days" — strong signal that the source lost the symbol. At-a-glance distinction between real current data and orphans from retired brokers.

Backing store change: `crypto_ts_cache` → `bar_ts_cache`, now covers every key rather than just `cryptocompare:`/`kraken:` prefixes. Decompression rate-limited to 500 keys/cycle so cold-startup scans of ~7500 keys complete in ~15 BG cycles (~45 s) without stalling the 3 s loop.

### Settings: MT5 Heartbeat Freshness Tri-State

`App::mt5_heartbeats` has been populated on every Mt5Sync pass since the ADR-148 heartbeat protocol landed — and nothing ever read it. Users had no way to distinguish "BarCacheWriter is actively writing" from "EA crashed but the .db file is still there." Fixed with a tri-state label next to each configured MT5 source:

- **≤45 s** → green `beat Ns ago` (fresh)
- **45–90 s** → yellow `beat Ns ago (lagging)`
- **>90 s** → red `STALE (Ns)` — EA likely dead (BCW cadence is 30 s, so 90 s = three missed cycles)
- **no beat** → dim `no heartbeat yet`

Thresholds match the EA's 30 s write cadence with 50% jitter allowance. Also fixed two underlying read-path bugs: heartbeats were being stored as SQLite TEXT (not BLOB) so rusqlite refused the implicit coercion; Common/Files resolution now recovers the instance name from the ramdisk symlink's filename suffix so ancestor-walking finds `drive_c` even when the configured path is the /dev/shm target.

### 3-Part Key Canonicalization — Drop the Never-Shipped 4-Part Form

ADR-056 speculated on a 4-part `mt5:{broker}:{sym}:{tf}` cache key. **BarCacheWriter has always written 3-part `mt5:{SYM}:{TF}`** — the 4-part form never shipped from any writer. Every consumer site was carrying a dead `parts.len() >= 4` fallback that pulled a broker tag out of a slot that didn't exist. Symptom: 4 MT5 symbols were intermittently returning empty bars because `detect_mt5_gaps`, `write_mt5_demand_txt`, and `save_session` were looking up cache timestamps using 3-part keys while reading from code paths that assumed 4-part. Every lookup returned 0. Gap detector marked all symbols empty. Every heartbeat fired max-bars demand that saturated the EA rotation queue.

Fix: unify every lookup to the 3-part key. Drop dead `mt5:CC:...` fallbacks from five consumer sites (insider-panel, VaR, ATR, sparkline, web `GetBars`). Metadata rows (`mt5:__SYMBOLS__`, `mt5:__HEARTBEAT__:acct`, `mt5:__SPECS__:...`) filtered via single `starts_with("mt5:__")` guard instead of substring probes. Hide `mt5:__` rows from symbol autocomplete, Symbol Screener, Cache Statistics grid, and Symbol Explorer cache tree. ADR-054 + ADR-056 text updated to match reality. 1396 engine tests pass.

### RAII Guards + Observability

Introduced `Mt5SyncGuard` with a `Drop` impl so `MT5_SYNC_IN_FLIGHT` releases on normal completion, early return, **and panic unwind**. Previously the target-cache open-failure early return or any unexpected thread panic would silently leak the flag, permanently disabling all future 30 s trigger cycles until terminal restart. Same RAII pattern applied to the `importing_flag` in XLSX import + compact threads — without it, a panic in the openpyxl row decoder would leak the flag stuck `true` and the background stats worker would silently skip every 3 s cycle forever.

Six previously-silent failure paths in the demand pipeline now log via `tracing`: heartbeat read errors, Mt5Sync per-cycle summaries, empty-heartbeat states, client-KV forward failures, Common/Files write failures, and malformed demand.txt row rejection (was `unwrap_or(0)` silently coercing to full-history gap-fill).

### Godel Parity Rounds 54–66 Complete + ADR-178

Thirteen more parity rounds landed since the commit-1003 snapshot, taking the RESEARCH_PACKET through:

- **R54 (AC/CHVOL/BBWIDTH/ELDERIMP/RMI)** — accelerator oscillator, Chaikin volatility, Bollinger width, Elder impulse, Relative Momentum Index
- **R55–R60 adaptive/structural** — SMMA, ALLIGATOR, CRSI, SEB, IMI, GMMA, MAENV, ADL, VHF, VROC, KDJ, QQE, PMO, CFO, TMF, FRACTALS, IFT_RSI, MAMA, COG, DIDI, DEMARKER, GATOR, BW_MFI, VWMA, STDDEV, WMA, RAINBOW, MESA_SINE, FRAMA, IBS
- **R61–R65 cycle/linear/pattern** — LAGUERRE_RSI, ZIGZAG, PGO, HT_TRENDLINE, MIDPOINT, MASSINDEX, NATR, TTM_SQUEEZE, FORCE_INDEX, TRANGE, LINEARREG_SLOPE/ANGLE, HT_DCPERIOD/DCPHASE/SINE/PHASOR/TRENDMODE, ACCBANDS, STOCHF, MIDPRICE, APO, MOM, SAREXT, ADXR
- **R66 price transforms + variance (ADR-178)** — AVGPRICE ((O+H+L+C)/4), MEDPRICE ((H+L)/2), TYPPRICE ((H+L+C)/3), WCLPRICE ((H+L+2C)/4), VARIANCE (flat-window population σ² over close). Schema v67→v68, 5 BrokerCmd + 5 BrokerMsg variants, per-snapshot App fields, tokio-spawned handlers, palette alias blocks, packet emitters 2.318–2.322. `VAR` alias collided with ADR-045 `show_var_mult` so `VARWIN` is used instead.

**Options Expiration Calendar (ADR-166)** also shipped: Tier 1 market-wide (weekly/monthly/quarterly/LEAPS/VIX expirations) + Tier 2 per-symbol (underlying's own chain ranked by OI, volume, DTE). Both tiers materialize as RESEARCH_PACKET fields.

### Sync Status: Per-Broker % Healthy + Storage Manager Triage

Closing the month: a dedicated **Sync Status window** aggregates `bar_ts_cache` into `(broker, TF)` health buckets via `SyncStatsRow` + `compute_bar_sync_stats / _broker_totals`. Every configured broker always emits a row — a newly-configured-but-not-yet-synced broker shows `0%` instead of being invisible. Per-broker chips at the top, per-TF grid below. Opened via the **SYNC** palette command (aliases: `SYNC_STATUS`, `SYNC_PCT`, `BARSYNC`, `BAR_SYNC`).

Storage Manager now carries a one-line Sync banner with a `[Details]` button that jumps into the same window. The FROZEN column also got triage-aware: entries with outstanding `mt5_gap_requests` render as **pending** (not frozen), and entries where `mt5_shallow_saturation ≥ 2` render as **capped** — so shallow pre-v1.463 caches the broker genuinely can't backfill past aren't mislabelled as dead.

Single commit but it's the operator-visible closing piece of the MT5 pipeline rewrite: every bar in the cache now has a provenance label and a health score visible from one window.

---

**1127 total commits. ~197,200 LOC. 1,753 tests (1,395 engine + 216 compiler + 85 native + 57 web). 8 crates. 157 ADRs. Zero warnings. 66 godel parity rounds + ADR-130/148/157/162/166/178 infrastructure.**

The March post framed the launch as "4.7 days to Bloomberg-class." April's framing is different: **the terminal is done shipping features and is now shipping a research surface.** The AI integrations are the product. Every godel parity round makes the packet denser, every LAN sync table makes the packet cheaper to materialize across peers, every cache layer makes the packet cheaper to re-serve. The terminal is, at this point, a **context compiler for AI-assisted trading research** that happens to also execute orders and render charts.

Feature velocity on the base terminal has slowed — not because the pace dropped (the commit rate is unchanged at ~40+/day), but because the commits are now **additive research surfaces** rather than foundational infrastructure. The foundation is done. The building on top of it is what April was.

-- TyphooN

---

> **DISCLAIMER:** TyphooN-Terminal is open-source software provided as-is under the BSL (Business Source License) license. It is NOT financial advice and NOT a recommendation to trade. Trading involves substantial risk of loss. The software executes orders as instructed -- it does not and cannot guarantee profitable outcomes. Use at your own risk. Test thoroughly in paper trading before risking real capital. The author actively trades using this software and holds positions mentioned in this blog. Prop firm information is current as of March 2026 and may change -- verify directly with each firm before funding an account.
