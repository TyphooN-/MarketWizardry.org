# DARWIN IYCN: Basin City Natural Gas

*"Walk down the right back alley in Sin City and you can find anything."*

**Published: 2026-04-06 | TyphooN | MarketWizardry.org**

> **DISCLAIMER:** This is not financial advice. These are real trades on a Darwinex Zero account with virtual capital. Going naked long on natural gas after your previous natgas DARWIN died in 36 hours is the kind of decision that separates conviction from insanity. The line is thin. You have been warned.

> **TRADING METHOD:** IYCN is discretionarily traded by TyphooN using the open-source NNFX MQL5 trading system. Stocks/ETF account — cash only, 100% margin, no hedging, no TRIM/PROTECT/martingale. The TyphooN EA serves as **risk management only**. Trade selection is manual: find an extreme outlier, trade it full tilt for a swing, rinse and repeat.

---

## I.Y.C.N. — If You Can, Natgas

*Acronym expanded: **I**f **Y**ou **C**an, **N**atgas. A dare. If you can stomach 432% risk on a single commodity after watching your last DARWIN die in 36 hours, you deserve the supercycle. If you can hold naked long while the death crosses scream at you from every timeframe. If you can watch $18K evaporate and come back the same day with a fresh account and a bigger position. If you can, natgas. Most can't. TyphooN can.*

*"She smells like angels ought to smell."* — Marv, describing Goldie. TyphooN, describing the natgas supercycle thesis. It smells like money. It smells like $134M. It smells like the trade that CKUC died trying to execute the wrong way.

CKUC went in with a hedged martingale. CKUC died in 36 hours. The thesis didn't die — the vehicle did. The $2,900/lot margin made hedged martingale impossible. PROTECT overcorrected. TRIM couldn't grind. The broker pulled the plug.

IYCN is the answer. Same thesis. Same conviction. Same natgas. **No hedge. No martingale. No TRIM. No PROTECT. No dead zone. Just naked directional long with a stop loss and a prayer.**

*"I'll stare the bastard in the face as he screams to God, and I'll laugh harder when he whimpers like a baby. And when his eyes go dead, the hell I send him to will seem like heaven after what I've done to him."* — Marv didn't hedge either. Marv went straight at his target. IYCN goes straight at the supercycle.

---

## The Position — "Worth Dying For"

![DARWIN IYCN — XNGUSD MTF Grid: H4/Weekly/Daily/Monthly (April 2026)](/img/darwin-iycn-mtf-202604.webp)

| Metric | Value |
|---|---|
| **Symbol** | XNGUSD (Natural Gas Spot USD) |
| **Direction** | **LONG** — naked, no hedge |
| **Size** | **32.3 lots** |
| **Entry** | ~$2.904 |
| **Total P/L** | -$6,452 (unrealized) |
| **Risk (notional)** | **$432,489** (432.6%) |
| **TP P/L** | **$134,938,426** |
| **SL P/L** | -$432,489 |
| **R:R Ratio** | **312:1** |
| **VaR %** | 54.24 (net) |
| **ATR D1** | $0.151 |
| **ATR W1** | $0.473 |
| **ATR MN1** | $0.895 |
| **LTF Bull Power** | 70 |
| **HTF Bear Power** | 90 |

32.3 lots naked long. Then TyphooN did what TyphooN does — went back in.

### Update: Single-Layer Hedge (2026-04-06)

```
IYCN current state (Round 2, 69/55 settings):
  Longs:        118 lots
  Shorts:       94 lots (declining — 38 TRIM closes)
  Net LONG:     24.0
  Total P/L:    -$26,975
  Risk:         $320,424 (455.3%)
  ML:           62.9% [DEAD zone]
  Equity:       $43,400
  Balance:      $70,375
  TRIM closes:  38
  PROTECT fires: 0
```

One layer of hedge. Not the multi-layer nightmare that killed CKUC. 32 shorts hedging 61 longs. One short position to TRIM through, not three overlapping positions fighting each other. The lesson from CKUC: if you hedge on XNGUSD, do it once. One layer. One set of shorts. One clean unwind path.

With 61L/32S, TRIM has 32 shorts to grind through. At $2,900/lot, that's a manageable hedge — not the 88-short bloated mess that caused the overcorrection cascade on CKUC. PROTECT has less to overcorrect because there's less gross. The margin math is tighter but cleaner.

**EA settings: 64/54** — the widest DEAD zone yet. 10% buffer between TRIM and PROTECT. CKUC ran 60/54 (6%) and died. Then 62/54 (8%) and died. IYCN runs 64/54 (10%). Each dead DARWIN buys 2% more cushion.

```
IYCN EA Configuration:
  EnableMartingale           = true
  MartingaleUnwindMarginPct  = 64      // TRIM — widest yet
  MartingaleDangerMarginPct  = 54      // PROTECT
  MartingaleMarginFloor      = 10      // Hard floor
  PreCloseMinutes            = 5       // Pre-close TRIM
  MartingaleSpreadTolerance  = 0       // No Open MG
  Bias:                      MG: LONG (auto-detected)
```

**First TRIM fire (09:42 UTC):** ML 95.2% — way above 64%. maxSafe=14. The EA closed 14 of 32.3 shorts in one tick. That's 43% of the hedge in one fire — but this time it's TRIM (building thesis), not PROTECT (destroying thesis). The single-layer hedge means TRIM can unwind the entire short side in 2-3 fires instead of grinding 0.1 lots for hours.

*"An old man dies. A young woman lives. A fair trade."* — Hartigan, Sin City. An old DARWIN (CKUC) dies. A new DARWIN (IYCN) lives. A fair trade.

---

## The Thesis — Same Story, Different Driver

The natgas supercycle thesis hasn't changed. Not one word:

1. **Global LNG demand is structural** — Europe's regasification terminals need feeding. Forever.
2. **AI datacenters burn gas** — 40% of US electricity is natgas. Every GPU cluster is a natgas demand center.
3. **Supply is constrained** — shale decline rates 60-70% year one. Rig counts at multi-year lows.
4. **Below marginal cost** — $2.90 is below production cost for most US shale. Unsustainable.
5. **New LNG export terminals** — Golden Pass, Plaquemines, Rio Grande coming online 2025-2026.

What changed is the execution. CKUC tried to grind a hedged martingale on an instrument that charges $2,900 per lot of margin. IYCN goes naked. One direction. One thesis. One stop loss at $1.484. If natgas goes down, the SL takes the loss. If natgas goes up, the TP prints $134M. No PROTECT to overcorrect. No TRIM to grind. No bias inversion. No overnight DEAD zone anxiety.

*"I've been framed for murder and the cops are in on it. But the real enemy, the one who killed the angel lying next to me — that enemy I will find."* — Marv's entire plot in Sin City is a straight line. No hedging. No diversification. One target. One direction. All the way to the end. That's IYCN.

---

## Why Naked Works Where Hedged Failed

CKUC's autopsy revealed the truth: hedged martingale requires cheap lots.

| Factor | CKUC (Hedged MG) | IYCN (Naked Long) |
|---|---|---|
| **Lots** | 113L + 88S = 201 gross | 32.3L = 32.3 gross |
| **Margin used** | ~$116K (both sides) | ~$94K (one side) |
| **PROTECT risk** | Overcorrection destroys bias | None — no PROTECT, no hedge |
| **TRIM dependency** | Must grind shorts to build thesis | Already at full thesis from entry |
| **Spread risk** | $0.014 × 201 lots = $2.81 | $0.014 × 32.3 lots = $0.45 |
| **Complexity** | 5 moving parts (TRIM/PROTECT/DEAD/ML/bias) | 1 moving part (price goes up or down) |
| **Time to thesis** | Weeks of TRIM grinding | **Immediate** — 100% long from tick one |

IYCN is at full thesis exposure from the first tick. No grind period. No hedge to unwind. No weeks of waiting for TRIM to build bias. 32.3 lots long, 312:1 R:R, and the supercycle either happens or it doesn't.

*"That there is one damn fine coat you're wearing."* — Marv appreciated simplicity. One coat. One mission. One target. IYCN has one position, one direction, one thesis. No accessories. No hedge. No complications.

---

## The Chart — Basin City at Night

**H4:** Price sitting between Supply Untested above and Demand Proven below. The range is compressing. Fisher deeply negative (-0.97). BetterVolume showing buy climax. The coiled spring.

**Daily:** Supply Proven overhead, Demand Tested below. SL set at $1.484 — below the SL line visible on the monthly. The daily shows the pullback from $3.45 into the $2.90 zone. This is the buy zone.

**Weekly:** Demand Proven holding at the bottom. The weekly structure shows the multi-year base. This is where supercycles start — boring, compressed, ignored by everyone chasing tech stocks.

**Monthly:** Demand Proven at generational lows. Fisher just turned positive (0.15). The monthly candle is forming inside a proven demand zone with the SL below structure. This is the trade. Right here. Right now.

LTF Bull Power: 70. HTF Bear Power: 90. The lower timeframes are turning while the higher timeframes are still bearish. This is exactly where CKUC entered too — the difference is IYCN doesn't need the higher timeframes to confirm before the position is at full thesis. CKUC needed weeks of TRIM to get here. IYCN arrived on entry.

---

## CKUC Died So IYCN Could Live

*"Deadly little Miho. She won't let you feel a thing unless she wants you to."* — CKUC felt everything. Every PROTECT fire. Every TRIM close. Every overnight ML swing. $54,686 of pain across 36 hours. Every single lesson burned into the firmware.

IYCN feels nothing. No PROTECT. No TRIM. No margin level anxiety. No DEAD zone. Price goes up → IYCN prints. Price goes down → SL takes the loss at $1.484. Clean. Simple. Lethal.

CKUC is the sixth headstone in the DARWIN Graveyard. But its corpse isn't wasted. Every lesson from CKUC's 36-hour life is baked into the decision to go naked:
- Don't hedge what you can't grind ($2,900/lot = no grind)
- Don't let PROTECT touch a position where one lot = 3% of margin
- Don't spend weeks building thesis exposure when you can have it immediately
- The thesis is the thesis. The vehicle is the variable.

**IYCN is CKUC reborn. Same thesis. Same conviction. Same natgas. No hedge. No martingale. No complications. Just Marv walking into a room full of people who need to die, with nothing but his fists and his faith.**

*"Walk down the right back alley in Sin City and you can find anything."*

IYCN found the supercycle. No hedge required.

---

## The Tuition: $28K Balance Damage, Position Rebuilt (2026-04-06)

```
IYCN damage report (before Round 2):
  Balance:      $72,399 (was $100,000)
  Damage:       -$27,601 (naked long stop-out + single-layer hedge stop-out)
  Decision:     Ignore the damage. Rebuild deeper. Wider settings.
```

Two stop-outs in one day. $27,601 in tuition. The first attempt (naked long, 32.3 lots) lasted 8 hours. The single-layer hedge (61L/32S at 64/54) lasted even less. CKUC had already died the same day with $54,686 in losses. Combined tuition: **$82,287 in one calendar day** learning how to trade XNGUSD with the TyphooN EA.

*"Walk down the right back alley in Sin City and you can find anything."* — IYCN walked down the alley, got mugged twice, and came back a third time with better armor. The alley is still there. The supercycle is still there. The thesis didn't change. The settings did.

**The scorecard:**

| Attempt | Strategy | Settings | Loss | Lesson |
|---|---|---|---|---|
| **CKUC** | Multi-layer hedged MG | 60/54 → 62/54 | -$54,686 | PROTECT overcorrects at $2,900/lot |
| **IYCN Round 1** | Naked → single-layer hedge | 64/54 | -$27,601 | DEAD zone too narrow |
| **IYCN Round 2** | Full hedge, wide settings | **69/55** | **Active** | 14% DEAD zone holds |

### Could Hedged Martingale Work on XNGUSD? The Math Says Maybe — With Extreme Settings

Three attempts. Three deaths. Three different TRIM/PROTECT configurations:

| DARWIN | Settings | DEAD Zone | Result |
|---|---|---|---|
| CKUC (attempt 1) | 60/54 | 6% | PROTECT overcorrection, bias inverted, dead |
| CKUC (attempt 2) | 62/54 | 8% | Still died — ML swings too fast at $2,900/lot |
| IYCN | 64/54 | 10% | TRIM unwound hedge too fast, left naked, dead |

The settings got wider each time. Each dead DARWIN bought 2% more DEAD zone. The pattern suggests the DEAD zone needs to be **much** wider for XNGUSD.

**The theoretical minimum: 55/69 (14% DEAD zone)**

```
$100K account, XNGUSD at $2.90, $2,900/lot margin

Max safe gross: ~34 lots (17L/17S)
  Margin: 34 × $2,900 = $98,600
  ML at entry: $100K / $98.6K = 101.4%

TRIM at 69%:
  ML must drop from 101% to 69% before TRIM fires
  That's a 32% ML drop — requires significant price move against hedge
  Gives massive room to absorb volatility without touching the hedge
  When TRIM fires, it's because there's genuine room to build bias

PROTECT at 55%:
  ML must drop from 69% to 55% (14% DEAD zone)
  At 34 lots gross, each lot closed = ~3% ML swing
  PROTECT closing 5 lots = 15% ML swing → still overcorrects
  BUT 14% DEAD zone means price must move much further to trigger PROTECT

Key insight: 69% TRIM means TRIM barely fires
  The hedge sits for weeks/months, collecting +$48/lot/day short swap
  When natgas drops (thesis direction), ML rises, TRIM fires, bias builds
  When natgas rises (against thesis), ML drops into 14% DEAD zone buffer
```

**The problem remains:** even at 55/69, PROTECT closing 5 lots still causes a 15% ML swing. The overcorrection is inherent to the $2,900/lot margin. The only real fix is account size — **$500K+ where each lot is <1% of margin** and PROTECT can close in small increments without overshooting.

**On $100K:** the safest XNGUSD approach is naked directional (what IYCN reverted to). No hedge. No PROTECT to overcorrect. Price goes your way → thesis prints. Price goes against → SL takes the hit. Clean. Simple. The $82K in CKUC/IYCN tuition proves this empirically.

**On $500K+:** hedged martingale at 55/69 might work. Each lot = 0.6% of margin instead of 3%. PROTECT closing 5 lots = 3% ML swing instead of 15%. The grind is slow (swap-funded, collecting +$48/lot/day on shorts) and the DEAD zone is enormous. But this requires 5x the capital that was available.

**The verdict from the first two deaths:** XNGUSD hedged martingale on $100K was not viable at 60/54, 62/54, or 64/54. The DEAD zone was too narrow for $2,900/lot margin swings.

**But we paid tuition to fly closer to the sun.** Every dead DARWIN bought 2% more DEAD zone. $82,287 of tuition across two accounts. The question became: is there a setting wide enough?

---

## IYCN Round 2: 69/55 — The Widest Configuration (2026-04-06, late)

IYCN came back. Same account ($72K remaining). Same thesis. New approach: **hedged martingale at 69/55 — 14% DEAD zone.**

![IYCN EA Settings: TRIM 69%, PROTECT 55%, Open MG $2.00, Pre-close 5min, Floor 10%](/img/iycn-settings-69-55-20260406.webp)

```
IYCN Round 2 state (2026-04-06 10:20 UTC):
  Longs:        118 lots
  Shorts:       103.7 lots (declining — TRIM active)
  Net LONG:     14.3 lots
  ML:           99.0% at init → 71.4% mid-session
  Equity:       $40,711
  Balance:      $71,320
  TRIM closes:  8 (grinding 0.1 lots at ML edge)
  PROTECT fires: 0
  Settings:     69/55 (14% DEAD zone)
```

Open MG at $2.00 filled the account with hedge pairs. 118L / 104S. ML started at 99% and immediately began dropping as natgas moved. TRIM fired at 69% — 6 lots in the first close, then grinding 0.1 at a time.

**Why 69/55 might survive where 60/54, 62/54, 64/54 died:**

| Config | DEAD Zone | Result | Why It Failed |
|---|---|---|---|
| 60/54 (CKUC) | 6% | Dead in 36h | PROTECT overcorrection, too narrow |
| 62/54 (CKUC) | 8% | Dead | Still too narrow for $2,900/lot swings |
| 64/54 (IYCN) | 10% | Dead in 8h | TRIM unwound hedge too fast, left naked |
| **69/55** | **14%** | **Active** | TRIM fires high (69%), massive buffer to PROTECT |

The 69% TRIM threshold means TRIM only fires when ML is comfortably high — plenty of margin room. The 14% DEAD zone means price has to move dramatically before PROTECT territory. On previous attempts, PROTECT fired within hours. At 69/55, PROTECT needs ML to drop from 69% to 55% — a 14-point slide that requires much more adverse price action.

### Swap Income Projection (94 shorts remaining)

| Period | Short Swap (+$48/lot/day) | Long Swap (-$78/lot/day) | Net Swap | Cumulative |
|---|---|---|---|---|
| **Daily** | +$4,512 (94 shorts) | -$9,204 (118 longs) | -$4,692 | -$4,692 |
| **Wednesday 3x** | +$13,536 | -$27,612 | -$14,076 | — |
| **Weekly (7 days)** | +$31,584 | -$64,428 | -$32,844 | -$32,844 |
| **Monthly (30 days)** | +$135,360 | -$276,120 | -$140,760 | -$140,760 |

Net swap is negative — longs cost more than shorts earn. But the short swap partially offsets: without it, the carry cost would be -$9,204/day instead of -$4,692. The shorts cut the daily carry cost in half. As TRIM closes shorts, the swap benefit decreases and the carry cost rises toward the full -$9,204.

### Hedge Unwind Projection (94 shorts, avg entry ~$2.87)

| Scenario | Price Move | Target | Short P/L per Lot | Total | TRIM Speed | Timeline |
|---|---|---|---|---|---|---|
| **Range-bound** | ±$0.03 | $2.83–$2.89 | -$100 to +$200 | -$9.4K to +$18.8K | 0.1 lots/tick at ML edge | **6-10 weeks** |
| **1 ATR D1 drop** | -$0.151 | **$2.71** | +$1,600/lot | **+$150K total** | Fast (ML spikes above 69%) | **1-2 weeks** |
| **1 ATR W1 drop** | -$0.473 | **$2.39** | +$4,800/lot | **+$451K total** | Very fast | **2-3 days** |
| **Price rises $0.10** | +$0.10 | $2.96 | -$1,300/lot | -$122K | DEAD zone holds | **Stalled** |
| **Price rises $0.20** | +$0.20 | $3.06 | -$2,300/lot | -$216K | **PROTECT fires** | **Account at risk** |

**Current state:** ML 62.9% in the DEAD zone. TRIM paused (needs 69%). 94 shorts surviving, collecting swap. If natgas drops $0.05, ML rises above 69% and TRIM resumes grinding. If natgas rises $0.15+, ML approaches 55% PROTECT territory.

The 14% DEAD zone is doing its job — IYCN has survived longer than CKUC's 36 hours or IYCN Round 1's 8 hours. The position breathes. The swap accumulates. The thesis waits.

The account has $72K left. Two natgas DARWINs already dead. $82K of tuition already paid. This is the third attempt — same thesis, third vehicle, widest settings yet. Each death refined the calibration. Each headstone bought 2% more cushion.

*"Is that the best you can do, you pansies?"* — Marv gets hit. Gets up. Gets hit again. Gets up again. IYCN took $28K of damage, ignored it, and came back with 69/55 — the widest DEAD zone yet. The damage is tuition. The position is alive. The thesis continues.

-- TyphooN

---

> **DISCLAIMER:** This post describes a speculative trading strategy using leveraged commodity CFDs on a virtual (demo) account. This is NOT financial advice. IYCN sustained significant losses during initial calibration but continues trading with wider settings (69/55). Do not trade commodity CFDs with money you cannot afford to lose. The natgas supercycle thesis remains the author's personal opinion and is not a recommendation to trade XNGUSD.
