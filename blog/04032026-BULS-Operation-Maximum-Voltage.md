# DARWIN BULS — Operation Maximum Voltage

*AJTK is dead. Long live BULS.*

**Published: 2026-04-03 | TyphooN | MarketWizardry.org**

> **DISCLAIMER:** This is not financial advice. This is a post-mortem analysis and strategy description using a proprietary EA on leveraged crypto CFDs. Do not attempt hedged martingale strategies without understanding that you can lose everything. Crypto CFDs carry extreme risk. You have been warned.

---

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

**Total tuition across 12 post-mortems:** ~$234K (QRRP $100K + XJFD→BBUD $34K + AJTK $100K). Each death taught something. AJTK's death taught the true floor.

---

## BULS: The 12th DARWIN

**B.U.L.S. — Benchmark Underway, Lot Simulation.**

- **B** — Benchmark. This is the benchmark run. The settings are proven. The firmware is correct. The voltage is calibrated. $0.75 spread tolerance — the v1.430 floor validated by AJTK's death at $0.14 and survival at $0.64.
- **U** — Underway. The benchmark is running. TRIM is grinding. 66,666 lots per side. The flywheel compounds.
- **L** — Lot. 133,332 gross lots. Each TRIM close converts one hedge lot into one net short lot. At pure short: 66,666 naked lots printing $67K per dollar of SOL decline.
- **S** — Simulation. The ML-constrained model predicts pure short at ~$51.7, equity ~$2.0M. Then the simulation ends and reality takes over — 400 naked longs at the bottom, ride to 4.236 fib.

One letter away from BULLS. Because that's where this ends — 400 naked longs at $5 SOL. Short the weakest supply on the way down. Long EVERYTHING at the bottom.

**Fresh $100K. v1.430. Open MG $0.75. Single massive hedge. One shot. No layers. The cleanest possible open.**

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

Open MG $0.75 with 66,666/side. Broker self-heal cost 5,993 bias → **60,673 surviving bias**. TRIM grinds 58,949 remaining hedge longs to pure short.

ML-constrained model (TRIM 57%): `P_ps = ($79,000/60,673 + $80) / 1.57 = ~$51.6`
`E_ps = 0.3631 × ($79,000 + $80 × 60,673) = ~$1,791,000`

| SOL Price | Equity | Hedge | Net Short | Spread Tol | Status |
|---|---|---|---|---|---|
| **$80 (now)** | **$79,000** | **58,949** | **1,724** | **$0.66** | [DEAD] 56.8%, self-healed |
| $75 | $87,600 | 56,000 | 6,400 | $0.70 | TRIM grinding |
| $70 | $100,000 | 51,000 | 12,600 | $0.79 | Accelerating |
| $65 | $125,000 | 43,000 | 21,600 | $0.97 | Building |
| $60 | $180,000 | 32,000 | 33,600 | $1.37 | Momentum |
| $55 | $330,000 | 17,000 | 48,600 | $2.52 | **Above $2.00** |
| $52 | $650,000 | 5,000 | 60,600 | $5.00 | Deep safety |
| **~$51.6** | **~$1,791,000** | **0** | **~60,673** | **$29.52** | **PURE SHORT** |

### Phase 2: NO CASCADE — Naked Ride to $5

60,673 naked short lots. $60,673 per dollar of SOL decline. Smooth ride for 46.6 dollars. Zero risk.

| SOL Price | Equity | Status |
|---|---|---|
| ~$51.6 (pure short) | $1,791K | **Smooth ride — zero risk** |
| $40 | $2,495K | Autopilot |
| $30 | $3,102K | Cruising |
| $20 | $3,709K | Deep profit |
| $10 | $4,316K | Printing |
| **$5** | **$4,620K** | **CLOSE ALL → DEPLOY LONGS** |

### Phase 3: Deploy 400 Naked Longs at Bottom ($5 SOL)

Close SOL shorts at $5 with ~$4.6M. Deploy into 400 naked long positions across all 7 Darwinex cryptos. Maximum volume per slot.

**Deployment framework (computed at execution with live data):**

1. **Target portfolio VaR: 3.25%** — floor of Darwinex corridor. Maximum VaR multiplier.
2. **Fill iteratively.** Each batch sized based on VaR impact of positions already open.
3. **Fill order:** BTC/ETH first (anchors), XRP/BNB (VaR compressors), SOL/ADA/DOGE (satellites).
4. **After each batch:** TyphooN-Terminal correlation matrix + VaR calculator. Keep portfolio VaR at 3.25%.
5. **Maximum volume per slot.** 400 positions, all max lot size.
6. **Minimum 1 swing per pair.** 7 core swings ride to 4.236+ and beyond.

**Target: ~$214M+ at 4.236 fib targets.**

---

## The Full Plan

| Phase | Action | Equity |
|---|---|---|
| **MG OPEN (DONE)** | SOL SHORT $0.75: 66,666/side, v1.430, TRIM 57/54. Broker self-heal: 60,673 bias | $100K → $79K |
| **TRIM GRIND** | Consume 58,949 hedge longs → pure short ~$51.6 | $79K → $1,791K |
| **Naked Ride** | SOL SHORT: Smooth ride $51.6 → $5, ~$61K/dollar, NO CASCADE | $1,791K → $4,620K |
| **Close SOL** | Extract $4.6M | **$4,620K** |
| **400 NAKED LONGS** | All 7 Darwinex cryptos, VaR-optimized at 3.25%, max volume | $4,620K |
| **Bull Cycle** | 400 naked long positions, 7 symbols, 4.236 fib targets | → **$214M+** |

**$100K → $4.6M (SOL short, single open at v1.430 floor) → $214M (400 naked longs at bottom). 2,140x.**

---

## Lessons Learned: The $234K Education (Updated)

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

$100K → $4.6M → $214M. One DARWIN. One thesis. One EA. One man who killed 11 DARWINs learning how to run one. v1.430 is the final form. The voltage is calibrated. The cooling is proven.

**For BBUD. For AJTK. The court has ruled. The sentence is $0.**

-- TyphooN

---

> **DISCLAIMER:** This post describes a speculative trading strategy using leveraged crypto CFDs. This is NOT financial advice. Past simulation results do not guarantee future performance. Leveraged trading carries substantial risk of loss including loss exceeding your initial deposit. Crypto markets are volatile, illiquid, and manipulated. Do not trade crypto CFDs with money you cannot afford to lose. Do not attempt hedged martingale strategies without understanding that you can lose everything. The author holds active short positions in SOLUSD.
