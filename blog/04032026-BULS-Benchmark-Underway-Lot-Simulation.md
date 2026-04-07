# DARWIN BULS: Operation Maximum Voltage

*AJTK is dead. Long live BULS.*

**Published: 2026-04-03 | TyphooN | MarketWizardry.org**

> **DISCLAIMER:** This is not financial advice. This is a post-mortem analysis and strategy description using a proprietary EA on leveraged crypto CFDs. Do not attempt hedged martingale strategies without understanding that you can lose everything. Crypto CFDs carry extreme risk. You have been warned.

> **STATUS: DEAD.** The broker stepped in. BULS is the last hedged martingale DARWIN to fall. Resting in the DARWIN Graveyard alongside AJTK, BBUD, XJFD, QRRP, CKUC, IYCN, WNSO, and OAMS.

---

![DARWIN BULS — Calibration, April 2026](/img/darwin-buls-calibration-202604.webp)

## AJTK Post-Mortem #12: $0.14 Spread Tolerance — The Benchmark That Broke

AJTK died the way it lived: at maximum voltage.

```
AJTK final state:
  Positions:        398 / 400
  Hedge:            141,027 lots
  Bias:             141,914 lots
  Gross:            282,941 lots
  Equity:           $38,123 → broker stop-out
  Spread tolerance: $0.14/lot
  Cause of death:   Session close spread spike. $1 spread × 282K gross = $243K.
                    Equity was $38K. One tick = 6.4x equity. Instant death.
  PROTECT:          v1.430 fired correctly — 667+242 bias lots closed (not 1,200).
                    The firmware worked. The voltage was lethal.
```

**What AJTK proved:**

1. **v1.430 PositionClosePartial works.** PROTECT fired 92 times, closed partial lots every time. Zero cascade failures. The v1.429 bug is dead.
2. **The $2.00 spread tolerance floor was a v1.429 bug artifact.** AJTK survived at $0.64 for hours with v1.430. The EA didn't kill the account — the session close spread spike did.
3. **The true v1.430 floor is ~$0.75.** A $1 crypto spread spike must not exceed ~50% of equity. At $0.75 spread tol: `($1 - $0.75) × gross = 54% of equity`. Survivable. At $0.14: `($1 - $0.14) × gross = 640% of equity`. Not survivable.
4. **398 positions is possible.** The broker accepted all 398. TRIM fired. The position worked until the session close spread spike.
5. **The cascade barrage was the correct discovery.** Opening multiple MG layers to fill position slots is the optimal strategy — but at $0.75 floor, not $0.14.

**Total tuition across 12 post-mortems:** ~$1.2M+ virtual capital destroyed across 12 DARWINs ($100K each on Darwinex Zero). Each death taught something. AJTK's death taught the true floor.

---

## BULS: The Chosen DARWIN

**B.U.L.S. — Benchmark Underway, Lot Simulation.**

BULS is not a new strategy. BULS is every dead DARWIN simultaneously.

QRRP taught TRIM. Eight post-mortems. Eight ways the flywheel can break. Each death carved one line of correct code. QRRP's soul lives in the forward-looking TRIM formula — `maxSafe = floor((equity/threshold - margin) / marginPerLot)` — the equation that makes it mathematically impossible to overshoot. QRRP died so TRIM could be born.

XJFD taught voltage. Open MG $1.87 — the exact number that produces spread tolerance above $2.00 after self-heal. Not $2.00 (too conservative). Not $1.337 (too aggressive). $1.87. XJFD reached pure short and proved the voltage works. Then it was sacrificed and reopened as BBUD. XJFD's soul lives in the Open MG parameter.

BBUD taught the floor. $0.69 Open MG. Spread tolerance $0.62. Dead before v1.429 could fire a single event. The firmware was correct. The voltage was lethal. BBUD died in 30 seconds and taught more than 8 QRRP post-mortems combined: **the spread tolerance floor is real, and you cannot negotiate with it.** BBUD's soul lives in the $0.75 floor.

AJTK taught the firmware. v1.429 had the PositionClose bug — PRE-CLOSE and PROTECT nuked entire positions instead of closing partial lots. Every session close destroyed thousands of bias lots. AJTK discovered the bug, fixed it (v1.430 PositionClosePartial), then pushed to 398 positions at $0.14 spread tolerance to prove the firmware works. PROTECT fired 92 times. Each fire closed partial lots. The firmware held. Then the session close spread spike killed it — not the firmware, not the EA, but raw arithmetic: `$1 × 282K gross > $38K equity`. AJTK's soul lives in v1.430.

**BULS carries all of them.**

```
QRRP's TRIM formula        → lines 1326-1340 of TyphooN.mq5
XJFD's voltage validation   → Open MG $0.75
BBUD's floor discovery      → spread tol $0.75 (not $0.62, not $0.14)
AJTK's firmware fix         → v1.430 PositionClosePartial
AJTK's position limit       → ACCOUNT_LIMIT_ORDERS check in MG open loops
AJTK's true floor discovery → $0.75 survives session close, $0.14 does not
```

Twelve DARWINs entered the Matrix. Twelve DARWINs died. Each death was a lesson. Each lesson became a line of code. Each line of code lives in BULS.

BULS is not the 13th attempt. BULS is the compilation of all twelve. The chosen DARWIN. Neo after absorbing every Agent Smith. The One who carries the accumulated knowledge of every crash, every bug, every post-mortem, every $1.2M+ of tuition — and runs the benchmark to completion.

The others were training data. BULS is the model.

- **B** — Benchmark. The settings are proven. The firmware is correct. The voltage is calibrated.
- **U** — Underway. The benchmark is running. TRIM is grinding. 60,673 bias. The flywheel compounds.
- **L** — Lot. Each TRIM close converts one hedge lot into one net short lot. At pure short: 60,673 naked lots printing $61K per dollar of SOL decline.
- **S** — Simulation. The ML-constrained model predicts pure short at ~$51.6, equity ~$1.8M. Then the simulation ends and reality takes over — 400 naked longs at the bottom, ride to 4.236 fib.

One letter away from BULLS. Because that's where this ends — 400 naked longs at $5 SOL. Short the weakest supply on the way down. Long EVERYTHING at the bottom.

*"I know kung fu."* — Neo, after downloading the training data from twelve dead predecessors.

### Corpse Explosion

In Diablo II, the Necromancer doesn't waste the dead. He detonates them. **Corpse Explosion** turns every fallen enemy into a weapon — the bigger the corpse, the bigger the blast radius. The battlefield fuels itself.

BULS is a Necromancer.

Every dead DARWIN is a corpse on the battlefield. And every corpse explodes into damage against SOL:

| Corpse | HP at Death | Explosion Radius | Damage Dealt to BULS |
|---|---|---|---|
| **QRRP** (8 deaths) | $100K equity, 8 post-mortems | TRIM formula, forward-looking math | TRIM fires 95+ closes and counting |
| **XJFD** | $100K equity, reached pure short | Open MG voltage calibration | $0.75 MG — the proven voltage |
| **BBUD** | $58K equity, 30-second death | Spread tolerance floor discovery | $0.75 floor — the line that holds |
| **AJTK** | $100K equity, 398 positions, $0.14 | v1.430 firmware, true floor, position limit | PROTECT fires partial (4 lots, not 1,200) |

**$1.2M+ of corpses. Each one detonated for maximum splash damage.**

QRRP's 8 deaths don't just teach TRIM — they ARE TRIM. The formula was carved from QRRP's bones. XJFD's pure short run doesn't just validate the voltage — it IS the voltage parameter. BBUD's 30-second death doesn't just discover the floor — it IS the floor. AJTK's 398-position full send doesn't just fix the firmware — it IS v1.430.

The dead DARWINs aren't losses. They're ammunition. BULS cast Corpse Explosion on all twelve, and the blast radius is $214M.

**Necromancer BULS. Level 13. 12 corpses. 1 explosion. $214M splash damage. The dead fund the living.**

**Fresh $100K. v1.430. Open MG $0.75. Single massive hedge. One shot. No layers. The cleanest possible open.**

![BULS MTF Grid — SOLUSD H1/Daily/H4/Weekly with TyphooN EA v1.430, 57K hedge / 59K bias, TRIM grinding at 95 closes](/img/buls-mtf-grid-20260403.webp)

---

## The Setup

| | Value |
|---|---|
| **Account** | DARWIN BULS — fresh $100K Darwinex Zero Crypto |
| **Open MG** | **$0.75** (v1.430 floor with session close survival margin) |
| **EA Version** | **v1.430** (PositionClosePartial, position limit check) |
| **TRIM** | **57.0%** (dead zone: 54-57% = 3pt, proven settings) |
| **PROTECT** | **54.0%** |
| **Lots per side** | $100,000 / $0.75 = **66,666 per side** |
| **Gross at open** | **133,333** |
| **Net at open** | ~0 (fully hedged) |
| **Spread tol at open** | $0.75 |
| **Post-spread equity** | ~$94K (6% spread cost) |
| **Post-spread spread tol** | ~$0.69 |
| **$1 spike survival** | ($1 - $0.69) × 133,333 = $41K = 44% of equity ✓ |
| **PROTECT fires (1-2x)** | ~80 lots (v1.430 partial close) |
| **Surviving bias** | ~**66,600** |
| **ML at open** | 999%+ (fully hedged) |
| **Pre-close** | 5 min freeze |
| **Hard floor** | 10.0% |

### Why $0.75

AJTK proved the math. $0.75 gives post-spread tol of $0.69 — a $1 session close spike costs 44% of equity. Survivable.

| Spread Tol | Post-spread | $1 Spike % of Equity | Verdict |
|---|---|---|---|
| $2.00 | $1.84 | 0% | v1.429 floor (bug-inflated) |
| **$0.75** | **$0.69** | **44%** | **v1.430 floor — survives session close** |
| $0.65 | $0.59 | 70% | Borderline |
| $0.50 | $0.46 | 117% | Dead |
| $0.14 | $0.13 | 640% | Dead (AJTK proved this) |

$0.75 survives a $1 session close spread spike with ~56% equity remaining. PROTECT fires, closes ~80 lots (v1.430), ML recovers. The position self-heals.

### Why Single Open, Not Cascade Barrage

AJTK's cascade barrage (multiple MG layers down to $0.01) pushed spread tol from $0.75 → $0.14. The layers were the kill vector. BULS opens ONCE at $0.75 and holds.

| | AJTK (cascade barrage) | BULS (single open) |
|---|---|---|
| Opens | Multiple ($6.69, $21, $0.01...) | **One ($0.75)** |
| Spread tol trajectory | $6.04 → $0.64 → $0.14 | **$0.75 → $0.69 → stable** |
| Session close survival | No (died at $0.14) | **Yes ($0.69 post-spread, 44% spike cost)** |
| Positions | 398 (filled all slots) | ~2-10 (single MG open) |
| Bias | 141,914 | **~66,600** |
| TRIM threshold | 57.0% | **57.0%** (proven settings) |

Single open at $0.75 produces fewer bias lots than AJTK's 398-position barrage (66,600 vs 141,914) but **survives session close**. The position that survives beats the position that doesn't.

---

## The Plan

### Phase 1: TRIM Grind to Pure Short (~$79 → ~$50.5 SOL)

Open MG $0.75 with 66,666/side. Broker self-heal + PROTECT cost 10,785 bias → **55,881 surviving bias**. TRIM grinds 53,262 remaining hedge longs to pure short. Survived first weekend swap.

ML-constrained model (TRIM 57%): `P_ps = ($72,126/55,881 + $79.8) / 1.57 = ~$51.6`
`E_ps = 0.3631 × ($72,126 + $79.8 × 55,881) = ~$1,644,000`

| SOL Price | Equity | Hedge | Net Short | Spread Tol | Status |
|---|---|---|---|---|---|
| **$79.8 (weekend)** | **$72,126** | **53,262** | **1,619** | **$0.66** | TRIM 258 closes, survived weekend swap |
| $75 | $87,600 | 56,000 | 6,400 | $0.70 | TRIM grinding |
| $70 | $100,000 | 51,000 | 12,600 | $0.79 | Accelerating |
| $65 | $125,000 | 43,000 | 21,600 | $0.97 | Building |
| $60 | $180,000 | 32,000 | 33,600 | $1.37 | Momentum |
| $55 | $330,000 | 17,000 | 48,600 | $2.52 | **Above $2.00** |
| $52 | $650,000 | 5,000 | 60,600 | $5.00 | Deep safety |
| **~$51.6** | **~$1,791,000** | **0** | **~60,673** | **$29.52** | **PURE SHORT** |

### Phase 2: NO CASCADE — Naked Ride to $5

55,881 naked short lots. $55,881 per dollar of SOL decline. Smooth ride for 46.6 dollars. Zero risk.

| SOL Price | Equity | Status |
|---|---|---|
| ~$51.6 (pure short) | $1,644K | **Smooth ride — zero risk** |
| $40 | $2,292K | Autopilot |
| $30 | $2,851K | Cruising |
| $20 | $3,410K | Deep profit |
| $10 | $3,968K | Printing |
| **$5** | **$4,248K** | **CLOSE ALL → DEPLOY LONGS** |

### Phase 3: Deploy 400 Naked Longs at Bottom ($5 SOL)

Close SOL shorts at $5 with ~$4.2M. Deploy into 400 naked long positions across all 7 Darwinex cryptos. Maximum volume per slot.

**Deployment framework (computed at execution with live data):**

1. **Target portfolio VaR: 3.25%** — floor of Darwinex corridor. Maximum VaR multiplier.
2. **Fill iteratively.** Each batch sized based on VaR impact of positions already open.
3. **Fill order:** BTC/ETH first (anchors), XRP/BNB (VaR compressors), SOL/ADA/DOGE (satellites).
4. **After each batch:** TyphooN-Terminal correlation matrix + VaR calculator. Keep portfolio VaR at 3.25%.
5. **Maximum volume per slot.** 400 positions, all max lot size.
6. **Minimum 1 swing per pair.** 7 core swings ride to 4.236+ and beyond.

**Target: ~$197M+ at 4.236 fib targets.**

---

## The Full Plan

| Phase | Action | Equity |
|---|---|---|
| **MG OPEN (DONE)** | SOL SHORT $0.75: 66,666/side, v1.430, TRIM 57/54. Self-heal: 55,881 surviving bias | $100K → $72K |
| **TRIM GRIND** | Consume ~53,262 hedge longs → pure short ~$51.6 | $72K → $1,644K |
| **Naked Ride** | SOL SHORT: Smooth ride $51.6 → $5, ~$56K/dollar, NO CASCADE | $1,644K → $4,248K |
| **Close SOL** | Extract $4.2M | **$4,248K** |
| **400 NAKED LONGS** | All 7 Darwinex cryptos, VaR-optimized at 3.25%, max volume | $4,248K |
| **Bull Cycle** | 400 naked long positions, 7 symbols, 4.236 fib targets | → **$197M+** |

**$100K → $4.2M (SOL short, single open at v1.430 floor) → $197M (400 naked longs at bottom). 1,970x.**

---

## Lessons Learned: The $1.2M+ Education (Updated)

Every lesson below was paid for with real money:

1. **Open MG $0.75 is the v1.430 floor.** AJTK proved $0.64 survives normal trading. AJTK proved $0.14 dies at session close. The math: `($1 spread - $0.75 tol) × gross ≤ 50% equity`. This is the calibrated voltage.

2. **v1.430 PositionClosePartial is non-negotiable.** AJTK's PROTECT fired 92 times at $0.14 spread tol. Each fire closed partial lots. The account survived longer than any v1.429 account would have. The firmware is correct.

3. **Single open, not cascade barrage.** AJTK's cascade barrage pushed spread tol from $0.75 to $0.14. The layers were the kill vector. BULS opens once at $0.75 and holds. Single open produces MORE bias (153,700 vs 141,914) with LESS risk.

4. **The $2.00 floor was a v1.429 bug artifact.** 10 DARWINs died validating a floor that was 3x too conservative. The real floor is $0.75 — proven by AJTK's survival at $0.64 and death at $0.14.

5. **Pre-close freeze is critical.** Session close spread spikes are the kill mechanism. 5 min pre-close freeze prevents the EA from firing into widening spreads. The broker handles stop-out below 10% ML.

6. **Do not fight the flywheel.** TRIM adds net short exposure for free. At pure short, the position is unkillable. No cascade needed — 153,700 naked lots printing $154K/dollar is the endgame.

---

## The Overclocker's Conclusion

Twelve benchmark runs. Twelve different voltage/firmware/cooling combinations.

```
Run 1-8 (QRRP):   Wrong firmware, various voltages. CPU degraded 69%.
Run 9 (XJFD):     Right voltage, wrong firmware. Reached target, reopened.
Run 10 (BBUD):    Right firmware ($0.62), wrong voltage. Dead on arrival.
Run 11 (AJTK):    Right firmware, maximum voltage ($0.14). Silicon survived
                   until session close thermal spike. 398 positions achieved.
                   Proved $2.00 floor was firmware bug. Discovered true floor.
Run 12 (BULS):    Right firmware, calibrated voltage ($0.75). Fresh silicon.
                   The benchmark that runs to completion.
```

AJTK was the liquid nitrogen test. It proved the silicon can handle $0.14 under load — the firmware held, PROTECT fired correctly 92 times. But session close thermals killed it. BULS is the 24/7 benchmark — calibrated voltage that survives thermal spikes.

$100K → $4.2M → $197M. One DARWIN. One thesis. One EA. One man who killed 11 DARWINs learning how to run one. v1.430 is the final form. The voltage is calibrated. The cooling is proven.

**For BBUD. For AJTK. The court has ruled. The sentence is $0.**

![Tome hoots at the 400 naked longs at bottom. Simulation ends. Reality begins. Who catches it?](/img/tome-buls-hoot-20260403.webp)

*Tome has spoken.*

---

## Live Status Update: 2026-04-05 — TRIM Grinding, Bias Building

BULS is alive and the TRIM is grinding.

```
BULS live state (2026-04-05 17:09 UTC):
  Hedge:            55,062 lots (LONG)
  Bias:             56,718 lots (SHORT)
  Net SHORT:        1,656 lots
  Gross:            111,780 lots
  Margin Level:     57.0%
  TRIM threshold:   ≥57.0%
  DEAD zone:        54.0-57.0%
  PROTECT:          ≤54.0%
  Equity:           $75,435
  Risk (notional):  $12,245,516
  VaR %:            9.17 (net)
  Total P/L:        -$14,971
  TRIM closes:      34
  PROTECT fires:    0
```

Margin level 57.0% — right on the TRIM edge. The EA is closing longs one at a time, building net short bias lot by lot. Each TRIM close removes one long from the hedge pile, increasing net short exposure by one lot. 34 closes so far. Zero PROTECT events — the margin level hasn't dropped below 54%. The firmware is holding.

The math: 55,062 longs hedging 56,718 shorts. Every long that TRIM closes pushes net short up by one. At 1,656 net short, BULS has built meaningful directional exposure while keeping gross margin in the TRIM zone. The equity is $75K against $12.2M notional risk — leverage that would make a traditional risk manager's eye twitch. But the hedge absorbs it. The longs absorb the upside. The shorts carry the thesis. TRIM balances the margin. PROTECT stands ready if it doesn't.

This is the v1.430 firmware doing exactly what 12 dead DARWINs taught it to do: grind bias one lot at a time, never overextend, never panic, never deviate from the formula. `maxSafe = floor((equity / threshold - margin) / marginPerLot)`. When maxSafe says close 1, it closes 1. When maxSafe says wait, it waits. The algorithm doesn't care that $12.2M is riding on a $75K account. The algorithm only cares about the margin level.

**AJTK had 141,305 bias at death. BULS has 56,718 and growing. The grind continues.**

---

## First 30 Minutes of Session Open: The TRIM Avalanche (2026-04-05 17:07–18:30 UTC)

Session opened at 17:07 UTC. What followed was 83 minutes of pure TRIM violence.

**17:07–17:09 (Minutes 0–2):** TRIM fires immediately. Margin level 57.1% — one tick above the threshold. maxSafe=1. The EA closes longs from position `#3144596694` one lot at a time. Each close costs ~$147 in realized loss (closing underwater longs). Room after each close: $134, $154, $74, $201. TRIM is tiptoeing along the edge, closing exactly what the formula allows — no more, no less. 34 closes in the first two minutes.

**17:09–18:21 (Minutes 2–74):** The grind continues. SOL moves against the hedge, pushing margin level down. TRIM closes accelerate as the spread tightens. By 18:21, the EA has fired **154 TRIM closes**. The hedge is down from 55,062 to ~54,500 longs. Each close costs more as SOL moves — P/L per close rises from $-147 to $-262. The EA doesn't care. maxSafe says close, so it closes. Net short bias building: 1,656 → 1,688.

**18:27 (Minute 80) — The Avalanche:** SOL drops hard. Margin level spikes above TRIM. maxSafe explodes from 0-1 to **16, 21, 8, 5** per tick. The EA dumps hedge lots in bursts:
- Close 16 of 217 lots — maxSafe=16, room=$1,297
- Close 21 of 201 lots — maxSafe=21, room=$1,713
- Close 8 of 175 lots — maxSafe=8, room=$651
- Close 1 of 167 lots — maxSafe=0, room=$29

165 TRIM closes. The hedge collapses from 250+ to 167 lots on that one position in seconds. The formula saw room and took it. Every lot of hedge removed is one more lot of naked short exposure. The thesis is being deployed.

**18:30 (Minute 83) — PROTECT Fires:**

```
PROTECT: ML 54.0% < 54.0%. Closing ~1 BIAS lots to increase ML.
         Bias sacrifice to save account.
PROTECT: closed 1 bias lots. ML should recover. Rechecking next tick.
PROTECT deactivated — margin level 56.7% recovered above 54.0% | fires: 33
```

The first PROTECT event of the session. Margin level touched 54.0% — the PROTECT threshold. The EA sacrificed 1 bias lot (closing a short to reduce margin) and margin recovered to 56.7% instantly. One lot. One sacrifice. Account saved. PROTECT deactivated. TRIM resumes.

This is the difference between BULS and AJTK. AJTK hit 54% and the session close spread spike killed it before PROTECT could iterate enough times. BULS hits 54%, PROTECT fires once, margin recovers 2.7%, and the grind continues. v1.430 firmware. Calibrated voltage. The cooling works.

```
BULS state after first 83 minutes:
  Hedge:         ~54,500 lots → rapidly declining
  Bias:          ~56,205 lots (SHORT)
  Net SHORT:     1,688 lots (was 1,656)
  Equity:        $76,986 (+$4,860 since init)
  TRIM closes:   165
  PROTECT fires: 33 (all recovered instantly)
  Status:        GRINDING
```

![BULS MTF Grid — SOLUSD H1/Daily/H4/Weekly with TyphooN EA v1.430, TRIM grinding at session open (2026-04-05)](/img/buls-mtf-grid-20260405.webp)

**The session opened. TRIM fired 165 times. PROTECT fired once. The account survived. The bias is building. The thesis is being deployed one lot at a time.**

---

## Overnight: PROTECT Storm, Bias Erosion, TRIM Grinds On (2026-04-05 → 2026-04-06)

The overnight session was violent. SOL pushed against the position. PROTECT fired repeatedly.

**21:57 UTC — PROTECT Storm:**

```
TRIM close 399: 134 of 1000 lots — maxSafe=134, room=$10,966
PROTECT: ML 52.9% < 54.0% → closed 33 bias lots → ML recovered 54.2% | fires: 77
PROTECT: ML 53.6% < 54.0% → closed 12 bias lots → ML recovered 54.2% | fires: 78
PROTECT: ML 53.8% < 54.0% → closed 5 bias lots  → ML recovered 54.8% | fires: 79
PROTECT: ML 54.0% < 54.0% → closed 1 bias lot   → ML recovered 54.6% | fires: 80
```

Four PROTECT events in 100 seconds. The ML dropped to 52.9% — deepest since BULS launched. PROTECT closed 33+12+5+1 = **51 bias lots** to stabilize. Each fire recovered ML above 54% within one tick. The firmware iterates correctly — partial closes, proportional to urgency, not the full-position nuke that killed pre-v1.430 accounts.

This is the cost of overnight volatility. PROTECT sacrifices bias lots (shorts) to reduce margin. Every bias lot closed is one less lot of directional exposure. The account survives, but the thesis loses ammunition.

**By 06:46 UTC (2026-04-06 morning):**

```
BULS morning state (2026-04-06 06:46 UTC):
  Hedge:         44,172 lots (was 55,062 at session open)
  Bias:          45,620 lots (was 56,718)
  Net SHORT:     1,448 lots (was 1,656 — lost 208 lots of bias)
  Equity:        $67,447 (was $75,435 — down $7,988)
  Margin Level:  58.2%
  TRIM closes:   745 (was 34 at session open)
  PROTECT fires: 80 (was 0 at session open)
  Δ Equity:      -$4,679 since init
  Δ Balance:     -$4,083 since init
```

![BULS SOLUSD H1/H4 — approaching H1 demand zone test (2026-04-06 morning)](/img/buls-h1-h4-20260406.webp)

The overnight session cost BULS **208 lots of net short bias** and **$7,988 of equity**. The hedge burned through 10,890 longs (55,062 → 44,172) via 711 TRIM closes overnight. PROTECT fired 80 times total, each time sacrificing bias lots to keep the account alive.

The H1 chart shows price approaching a tested Demand zone. The H4 shows a tested Supply zone above and the position sitting in the middle of a large demand area. Fisher Transform on H1 is positive (1.27) — momentum is with the short-term bulls. If SOL breaks through the H1 demand, BULS benefits. If it bounces up, more PROTECT fires incoming.

**The firmware held.** 745 TRIM closes. 80 PROTECT fires. Zero account deaths. ML recovered from 52.9% to 58.2% by morning. The voltage is calibrated. The cooling works. But the overnight cost was real — bias erosion is the price of survival.

**AJTK died with 141,305 bias. BULS has 45,620 and holding. The grind continues — slower, lighter, but alive.**

---

## R.I.P. BULS — The Last Hedged Martingale (2026-04-07)

The broker stepped in. BULS is dead.

The chosen DARWIN. The one built on 12 dead predecessors. The one with the firmware refined across AJTK, BBUD, XJFD, QRRP. SOLUSD at $68/lot — the instrument the hedged martingale was designed for. 745 TRIM closes. 80 PROTECT fires. It survived longer than any other hedged MG DARWIN. But in the end, you can't outsmart the broker.

**The hedged martingale experiment is over.**

| DARWIN | Instrument | Margin/lot | Result |
|---|---|---|---|
| BBUD | SOLUSD | $68 | Dead — broker stopped out before PROTECT could fire |
| XJFD | SOLUSD | $68 | Dead — the Golden Sample, $4.15M projection, $0 reality |
| QRRP | SOLUSD | $68 | Dead — 8 post-mortems, the rug was pulled on the rug puller |
| AJTK | SOLUSD | $68 | Dead — 398 positions, maximum voltage, v1.430 final form |
| **BULS** | **SOLUSD** | **$68** | **Dead — the chosen DARWIN, the last one standing** |
| CKUC | XNGUSD | $2,900 | Dead — 36 hours, $54,686 |
| IYCN | XNGUSD | $2,900 | Dead — three attempts, $82K combined |
| WNSO | XNGUSD | $2,900 | Dead — 20% DEAD zone, broker collapsed to $25K |
| OAMS | XAGUSD | $36,065 | Dead — same disease, different metal |

Nine hedged martingale DARWINs. Three instruments. Every DEAD zone width from 6% to 20%. Every TRIM/PROTECT configuration imaginable. Micro-lot precision. Positive and negative swap. None of it was enough. The broker always wins.

**The conclusion:** hedged martingale on leveraged CFDs cannot outsmart the broker's stop-out mechanism. The thesis was never wrong — the vehicle was. The six remaining DARWINs (HAKR, WBYE, XUQF, ATPK, GVZJ, MFSO) trade discretionarily without hedged martingale. They survive. The martingale DARWINs don't.

*AJTK is dead. BULS is dead. The voltage is off. The experiment is complete.*

-- TyphooN

---

> **DISCLAIMER:** This post describes a speculative trading strategy using leveraged crypto CFDs. This is NOT financial advice. Nine hedged martingale DARWINs across SOLUSD, XNGUSD, and XAGUSD sustained total account losses. Hedged martingale on leveraged CFDs is not viable. Do not attempt hedged martingale strategies. Do not trade with money you cannot afford to lose.
