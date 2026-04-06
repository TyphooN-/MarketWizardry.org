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
IYCN current state:
  Longs:        61 lots
  Shorts:       32 lots
  Net LONG:     29
  Total P/L:    -$18,521
  Risk:         $816,159 (816.7%)
  VaR %:        55.71 (net)
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

## Post-Mortem: IYCN Is Dead (2026-04-06, evening)

```
IYCN final state:
  Balance:      $72,399 (was $100,000)
  Equity:       $72,399
  Positions:    0 (broker liquidated all)
  Risk:         $0
  VaR:          0%
  Cause of death: Broker stop-out. XNGUSD moved against long bias.
  Lifespan:     ~8 hours
  Total loss:   -$27,601
```

*"Is that the best you can do, you pansies?"* — Marv asked the question one too many times. IYCN lasted 8 hours. Shorter than CKUC's 36. Two natgas DARWINs dead in 12 hours. Same day. Same thesis. Same instrument. Different approaches — both dead.

CKUC died because hedged martingale doesn't work at $2,900/lot. IYCN died because naked long on XNGUSD with 432% risk and no hedge means one adverse daily ATR move ($0.15) wipes the margin. The single-layer hedge bought a few hours. It wasn't enough.

**The scorecard:**

| DARWIN | Strategy | Lifespan | Loss | Cause |
|---|---|---|---|---|
| **CKUC** | Hedged MG (multi-layer) | 36 hours | -$54,686 | PROTECT overcorrection + broker stop-out |
| **IYCN** | Single-layer hedge → naked long | 8 hours | -$27,601 | Broker stop-out on adverse move |
| **Combined** | | 44 hours | **-$82,287** | XNGUSD + leverage + natgas volatility |

$82,287 in tuition across two accounts in one calendar day. The natgas supercycle thesis consumed two DARWINs and spat out the bones.

### The Lesson: XNGUSD CFDs Are Not a Supercycle Vehicle

The thesis isn't wrong. The instrument is wrong. XNGUSD CFDs with 10% margin requirement and $2,900/lot are designed for short-term trading, not multi-month supercycle rides. The margin math doesn't give you enough room to survive the daily volatility while waiting for a thesis that plays out over months or years.

*"Walk down the right back alley in Sin City and you can find anything."* — Marv found what he was looking for. It killed him. IYCN found the supercycle trade. It killed IYCN too. Sometimes the alley leads somewhere you shouldn't go. Not with this much leverage. Not on this instrument.

The supercycle will be traded again. Not today. Not on a CFD account. The thesis deserves a vehicle that can survive the volatility long enough for the thesis to matter.

---

## 🪦 DARWIN Graveyard

IYCN rests in a dark cemetery alongside CKUC — two graves dug on the same day. The fastest double burial in the portfolio's history. They lie next to AJTK, BBUD, XJFD, and QRRP. Six headstones. Six algorithms. Six theses that outlived their vehicles.

IYCN's tombstone reads: *"Here lies IYCN — If You Can, Natgas. Turns out, you can't. Not on CFDs. Not at $2,900/lot. Not with 432% risk. 8 hours. $27,601. The thesis was right. The vehicle was wrong. Again."*

*"Deadly little Miho."* — Miho doesn't talk. She just kills. XNGUSD doesn't talk either. It just stops you out. Two DARWINs in one day. The graveyard is getting crowded.

-- TyphooN

---

> **DISCLAIMER:** This post describes a speculative trading strategy using leveraged commodity CFDs on a virtual (demo) account that was liquidated. This is NOT financial advice. IYCN lost $27,601 of virtual capital in 8 hours. CKUC and IYCN combined lost $82,287 in one calendar day on the same instrument. Do not trade commodity CFDs with money you cannot afford to lose. The natgas supercycle thesis remains the author's personal opinion and is not a recommendation to trade XNGUSD.
