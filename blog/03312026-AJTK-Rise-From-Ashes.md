# AJTK: Automated Judicial Termination of Kapital

*Rise From the Ashes*

**Published: 2026-03-31 | TyphooN | MarketWizardry.org**

> **DISCLAIMER:** This is not financial advice. This is a post-mortem analysis and strategy description using a proprietary EA on leveraged crypto CFDs. Do not attempt hedged martingale strategies without understanding that you can lose everything. Crypto CFDs carry extreme risk. You have been warned.

---

## BBUD Is Dead

BBUD crashed and burned. The 10th post-mortem. The death was not complicated: $0.69 Open MG on $58K equity produced spread tolerance of $0.62 per lot. Crypto CFD spreads routinely hit $1-2. The broker stopped out the account before v1.429 PROTECT could fire a single event.

The firmware was correct. The voltage was lethal.

```
BBUD final state:
  Open MG:          $1.337 + $0.69 (layered aggression)
  Gross lots:       94,186
  Equity:           $58,420
  Spread tolerance: $0.62/lot
  Cause of death:   Broker stop-out. v1.429 never fired.
```

$0.62 spread tolerance on crypto CFDs is a death sentence. The position could not survive a single normal spread fluctuation. It was dead on arrival.

---

## The Graveyard: 10 DARWINs Died

Three accounts. Ten post-mortems. $134K of tuition.

| Account | Post-Mortems | Open MG | Firmware | Cause of Death |
|---|---|---|---|---|
| **QRRP** | 8 | $2.00 / $0.99 / various | v1.420-1.426 | PROTECT balanced close bug, operator intervention, spread spikes |
| **XJFD** | 1 | $1.87 | v1.426-1.428 | Reached pure short, reopened as BBUD |
| **BBUD** | 1 | $1.337 + $0.69 | v1.428-1.429 | $0.69 spread tol $0.62 = instant death |

Every single Open MG below $1.87 resulted in broker stop-out or catastrophic degradation. The $2.00 spread tolerance floor is not theoretical. It is empirically validated through $134K of destroyed capital.

The bug history is equally instructive:

| Bug | Version | What It Did | Fix |
|---|---|---|---|
| PROTECT balanced close | v1.420-1.428 | Closed equal lots both sides. ML never fixed. All longs consumed. | v1.429: close BIAS to fix ML |
| Pre-close fires PROTECT | v1.426 | ML < PROTECT during close. PROTECT fires into widening spreads. | v1.428: close bias to push ML above TRIM, then freeze |
| Pre-close balanced close | v1.427 | Balanced close LOWERED ML instead of raising it. | v1.428: close bias instead |
| No pre-close mechanism | v1.420 | Position entered overnight with zero protection. | v1.426: pre-close freeze |

Four critical bugs. Each discovered through account destruction. Each fixed in the next version. v1.429 is the first version where ALL three safeguards (TRIM, PROTECT, pre-close) use the correct close direction.

---

## AJTK: Automated Judicial Termination of Kapital

**A.J.T.K.**

- **A** — Automated. TyphooN v1.429. No human intervention. TRIM fires on tick. PROTECT fires on threshold. Pre-close fires on schedule. The EA is the judge, jury, and executioner. The operator's only job is to not touch the BIOS.
- **J** — Judicial. This is not random violence against SOL's market cap. It is a calculated, evidence-based sentence handed down after evaluating the supply dynamics of all 7 Darwinex cryptos. SOL was found guilty of 4% perpetual inflation with no cap. The sentence is $0.
- **T** — Termination. Of SOL's capital. Of every long position that bought the "Solana killer" narrative. Of the $1.65 billion in annual dilution that the market pretends doesn't exist. TRIM terminates hedge longs one at a time. Each close is a verdict. Each net short lot is a sentence served.
- **K** — Kapital. Not "capital" — Kapital. As in Marx. As in the systematic deconstruction of an asset's value through the exploitation of its own structural contradictions. SOL's 4% emission is the internal contradiction. AJTK is the dialectical response. The inflation creates the sell pressure. The sell pressure feeds the short. The short funds the long. The long rebuilds the capital that SOL destroyed. Kapital terminates itself. AJTK just automates the process.

**The court has ruled. The sentence is $0. The execution is automatic. TyphooN v1.429 carries it out one TRIM at a time.**

AJTK is fresh $100K with the correct firmware and the proven voltage. For the first time in this strategy's history, both variables are right simultaneously.

| | Value |
|---|---|
| **Account** | DARWIN AJTK — fresh $100K Darwinex Zero Crypto |
| **Open MG** | $1.87 (initial) + **$7.00 (early cascade, planned at market open)** |
| **EA Version** | **v1.430** (CRITICAL FIX: PositionClosePartial in PRE-CLOSE/PROTECT) |
| **Position (pre-cascade)** | 6,442L / 8,400S, net 1,958 SHORT |
| **Post-cascade** | 19,299L / 21,257S, net 1,958 SHORT, spread tol $2.07 |
| **Equity** | $89,691 \| ML 56.8% [DEAD] |
| **SOL Price** | $79 |
| **TRIM / PROTECT** | 57% / 54% |
| **Pre-close** | 5 min freeze |
| **TRIM closes** | 539 |
| **PROTECT closes** | 0 (EA) |

**v1.430 Critical Fix:** PRE-CLOSE and PROTECT were using `PositionClose()` (closes entire position) instead of `PositionClosePartial()`. The "broker forced 1,200 bias closures" was the EA's own PRE-CLOSE nuking a full sell position when ~40 lots were needed. **Bug #5 in the series. Every session close since AJTK opened destroyed an entire position.** Fixed — partial close costs ~40 lots per fire, not 1,200. This makes early cascade viable.

### Why $1.87 Is Not Random

$1.87 was the Open MG used on XJFD. The results are documented:

- **Starting equity:** $100K
- **Spread cost on open:** ~$8.8K (8.8%)
- **Post-open equity:** ~$91K
- **PROTECT fires:** 1-2 (self-heal)
- **Post-heal equity:** ~$87K (~10% total degradation)
- **Surviving bias:** ~18,500 lots
- **Spread tolerance after heal:** ~$2.18 (above $2.00 minimum)

Compare to $1.337:

- **Post-heal equity:** ~$75K (25% degradation)
- **Surviving bias:** ~15,000 lots
- **Spread tolerance after heal:** ~$2.64

$1.87 preserves 3,500 more bias lots and $12K more equity than $1.337 for the same strategy. The extra aggression of $1.337 buys nothing — the EA trims the excess via PROTECT anyway, and each PROTECT fire costs equity. You are paying $12K for the privilege of having lots that get immediately destroyed.

$0.69 does not even reach the self-heal phase. The account dies before PROTECT can fire.

### Why v1.429 Is Not Random

v1.429 is four bug fixes deep. Each fix was discovered through account destruction:

- **$8K** bought the discovery that PROTECT balanced close does not fix ML (PM#7-9)
- **$12K** bought the discovery that pre-close needs to fire before PROTECT (overnight wipes)
- **$6K** bought the discovery that balanced close LOWERS ML, not raises it
- **$8K** bought the validation that TRIM 57/54 is the optimal setting

**Total tuition: $134K across 3 accounts.** The return on that tuition is the correct EA configuration for every trade from this point forward.

v1.429 PROTECT closes BIAS (shorts) to increase ML. This is the opposite of what v1.420-1.428 did (balanced close). The balanced close bug caused 3x full dehedge on previous accounts — consuming all longs without ever fixing ML. v1.429 sacrifices a few bias lots to keep ML above 54% and PRESERVE the hedge. The hedge is the position. Without the hedge, there is no TRIM. Without TRIM, there is no flywheel.

---

## The Plan

### Phase 1: Early Cascade $7.00 at $79 SOL

v1.430 fixes the PositionClose bug. Early cascade is now viable — PRE-CLOSE costs ~40 lots per session, not 1,200. Maximum intensity while maintaining $2.00 spread tol floor.

MG $7.00 on $90K equity adds 12,857 lots per side → total 19,299 hedge / 21,257 bias. Spread tol $2.07 post-spread. PROTECT fires 1-2x at ~40 lots each (v1.430 partial close).

| SOL Price | Equity | Hedge | Net Short | Spread Tol | Status |
|---|---|---|---|---|---|
| **$79 (cascade)** | **$84,000** | **19,299** | **1,958** | **$2.07** | Post-spread, self-healing |
| $70 | $110,000 | 14,000 | 9,200 | $2.75 | TRIM grinding |
| $60 | $200,000 | 8,000 | 15,200 | $4.65 | Accelerating |
| $50 | $340,000 | 3,000 | 20,200 | $7.10 | Deep safety |
| **~$40** | **~$530,000** | **0** | **~21,257** | **$24.93** | **PURE SHORT → CASCADE #2** |

Expected pure short at ~$40 SOL. ~21,257 lots. ~$530K equity. The early cascade at $7.00 more than doubles the bias (8,400 → 21,257) and triples the equity at pure short ($205K → $530K).

### Phase 2: Cascade $3.00 at Pure Short (~$40 → ~$24 SOL)

Open MG $3.00 at pure short on $530K equity. ~176,667 new lots per side. v1.430 PROTECT fires 1-2x (~80 lots), ~197,800 bias survive.

| SOL Price | Equity | Hedge | Net Short | Status |
|---|---|---|---|---|
| **$40 (cascade #2)** | **$530K** | **170,000** | **27,000** | **Phase 2 starts** |
| $30 | $1,300K | 90,000 | 107,000 | Accelerating |
| **~$24** | **~$2,100K** | **0** | **~197,800** | **PURE SHORT — FINAL** |

### Naked Ride: $24 → $5

~197,800 pure short lots. ~$198K per dollar of SOL decline. Smooth ride for 19 dollars.

| SOL Price | Equity | Status |
|---|---|---|
| $24 | $2,100K | Smooth ride begins |
| $20 | $2,891K | Cruising |
| $10 | $4,869K | Deep profit |
| **$5** | **$5,858K** | **CLOSE ALL** |

### Deploy Full Crypto Basket

Close SOL shorts at $5 with ~$5.9M. Deploy into all 7 Darwinex cryptos.

| Component | Allocation | Strategy | Target Equity |
|---|---|---|---|
| **ETH** | $3,030K | MG LONG $4.20 | **$132M** |
| **BTC** | $995K | MG LONG $4.20 | **$60M** |
| **DOGE** | $760K | Naked long (6mo) | **$46M** |
| **SOL** | $410K | Naked long | **$17M** |
| **ADA** | $245K | Naked long | **$7M** |
| **XRP** | $230K | Naked long | **$6M** |
| **BNB** | $188K | Naked long | **$4M** |
| **TOTAL** | **$5,858K** | **400 positions** | **~$272M+** |

**$100K → $5.9M (SOL short + early cascade $7 + cascade $3 at pure short) → $272M+ (full crypto basket long). 2,720x.**

400 positions. 7 symbols. 4.236 fib targets. MG on ETH/BTC. Naked long on everything else. Short the weakest supply on the way down. Long EVERYTHING on the way up. **4 Martingale 4 Furious.**

---

## Why Not Just Short Naked? — Single Swing vs 2x Cascade

The obvious question: if the thesis is "SOL goes to $0," why not just open a naked short with everything and ride it down? Why the hedged martingale? Why the cascade? Why 10 dead DARWINs of complexity?

Because the math isn't close.

### Option A: Single Naked Short — Full Tilt Swing to $0

Take the entire $90K equity. Open one massive short at $79.

**Darwinex crypto CFDs are 1:1 leverage.** Margin = position size. So:

| | Value |
|---|---|
| Equity | $90,000 |
| SOL price | $79 |
| Max lots (1:1) | $90,000 / $79 = **1,139 lots** |
| Margin used | $89,981 (99.98%) |
| ML at entry | ~100% |
| Profit per $1 SOL drop | **$1,139** |
| Equity at SOL $0 | $90,000 + (1,139 × $79) = **$179,981** |
| **Return** | **1.8x** |

Problems:
- **ML starts at 100%.** Any price move UP eats margin. SOL goes to $90 (+$11) → loss $12,529 → ML 86% → PROTECT territory. SOL goes to $120 (+$41) → loss $46,699 → ML ~52% → dead.
- **No spread tolerance buffer.** The position IS the equity. One spread spike can trigger stop-out.
- **Darwinex VaR corridor (3.25%-6.5%).** A naked 1,139-lot short has VaR well above the corridor ceiling. D-Score gets crushed. Investor allocation goes to zero. The DARWIN becomes uninvestable.
- **No recovery from drawdown.** If SOL bounces 50% before going to $0, the account is dead. No PROTECT. No hedge. No self-healing.

**$90K → $180K. 1.8x. One shot. No second chance.**

### Option B: Hedged Martingale with 2x Cascade (AJTK Plan)

Same $100K starting equity. Open MG $1.87 — 26,737 lots per side. Net exposure: ~0. Margin: ~$0.

| | Value |
|---|---|
| Open equity | $100,000 |
| MG $1.87 | 26,737 lots per side |
| Net at open | ~0 (fully hedged) |
| Margin at open | ~$0 (net-based) |
| ML at open | 999%+ |
| Spread tolerance at open | $1.87/lot (self-heals to $6+) |

**Phase 1:** TRIM grinds hedge longs. Net short builds from 0 → 1,958 → eventually ~8,400 at pure short. Equity grows from $100K → $205K as SOL drops to $40. The position SURVIVES bounces because the hedge absorbs adverse moves while TRIM only fires when ML is above threshold.

**Phase 2:** Cascade $3.00 at pure short ($40). Fresh 68K lots per side on $205K equity. v1.429 PROTECT fires 1-2x, ~69K bias survive. TRIM grinds again to pure short #2 at ~$24.

**Naked Ride:** 69,000 pure short lots from $24 → $5. **$69K per dollar of SOL decline.** That's 60x the profit rate of the single naked short ($1,139/dollar).

| | Single Swing | 2x Cascade |
|---|---|---|
| Lots at pure short | 1,139 | **69,000** |
| Profit per $1 drop | $1,139 | **$69,000** |
| Equity at SOL $5 | $180K | **$2,031K** |
| Equity at SOL $0 | $180K | **$2,375K** |
| Return | 1.8x | **20.3x** |
| Survives 50% bounce | No | **Yes** |
| Survives spread spikes | No | **Yes** |
| Darwinex VaR compliant | No | **Yes** (hedged = low VaR) |

**Then deploy the $2.0M into the full crypto basket long:**

| | Single Swing | 3x Cascade + Basket |
|---|---|---|
| Equity at SOL $5 | $180K | $5,858K |
| Deploy into basket | N/A (too small) | MG LONG ETH/BTC + naked longs |
| Equity at 4.236 fib targets | ~$180K (already extracted) | **$272M+** |
| **Total return** | **1.8x** | **2,720x** |

### Why the Cascade Works and the Swing Doesn't

1. **Net-based margin is the exploit.** Darwinex charges margin on NET exposure, not gross. A hedged position with 26,737 lots per side uses ~$0 margin. A naked 1,139-lot short uses $90K margin. The hedge lets you carry 23x more gross exposure on the same equity.

2. **TRIM converts hedge into direction for free.** Every closed hedge long adds one net short lot without opening a new position. No additional margin. No additional spread cost. The flywheel compounds because TRIM fires on every tick where ML exceeds threshold.

3. **The cascade multiplies the base.** At pure short ($40), equity is $205K — not because of trading gains, but because TRIM built net short exposure that profited as SOL dropped. That $205K becomes the base for cascade #2, which produces 69,000 bias lots. The single swing can never access this multiplication because it started and stays at 1,139 lots.

4. **Darwinex VaR compliance.** A hedged position starts with near-zero VaR (net exposure ≈ 0). As TRIM builds net, VaR grows gradually. The DARWIN stays within the 3.25%-6.5% corridor. A naked 1,139-lot short has VaR spiking from day one — D-Score gets hammered, investors flee, the DARWIN becomes a pariah. AJTK can attract investor capital while building the position. The single swing cannot.

5. **Survival.** SOL bounces. Crypto bounces violently. A 40% bounce from $79 takes SOL to $111. The naked short loses $36K → account at $54K → ML ~48% → broker stop-out. The hedged position? ML barely moves because the hedge absorbs the bounce. TRIM pauses, PROTECT might fire 1-2 balanced closes. The position survives and resumes when SOL drops again.

**The single swing is a bet. The cascade is a machine.** The bet returns 1.8x and dies on the first serious bounce. The machine returns 943x and self-heals through broker forced closures, spread spikes, and overnight gaps.

---

## Lessons Learned: The $134K Education

Every lesson below was paid for with real money:

1. **Open MG $1.87 is the proven floor.** Every Open MG below $1.87 has resulted in broker stop-out or catastrophic degradation. $1.87 produces spread tolerance of $1.77 at open, which self-heals to ~$2.18 after 1-2 PROTECT fires. The ~10% equity loss is the cost of business. $1.337 loses 25%. $0.69 loses everything.

2. **The $2.00 spread tolerance floor is real.** Crypto CFD spreads spike to $1-2 routinely. A spread tolerance below $2.00 will trigger PROTECT events that erode the position. Below $1.00, the account dies before PROTECT can help.

3. **PROTECT is insurance, not a strategy.** The position should survive WITHOUT PROTECT firing. PROTECT handles edge cases — spread spikes, overnight gaps, session boundaries. If your position design REQUIRES PROTECT to survive normal operation, the Open MG is too aggressive.

4. **v1.429 PROTECT closes bias to fix ML.** Previous versions used balanced close, which does not fix ML because it preserves net exposure. The balanced close bug destroyed three full positions on BBUD's predecessor accounts. v1.429 is the first version that handles PROTECT correctly.

5. **Do not fight the flywheel.** TRIM adds net short exposure for free. Every closed hedge long is a bias lot gained without opening a new position. The flywheel is the strategy. Fighting it — overriding TRIM, panic closing, manual intervention — is how you turn $100K into $47K.

6. **The firmware must be correct before the voltage matters.** XJFD had the right voltage ($1.87) but wrong firmware (v1.426-1.428). BBUD had the right firmware (v1.429) but wrong voltage ($0.69). Both failed. AJTK has both right.

---

## The Overclocker's Conclusion

The K|NGP|N analogy holds. Ten benchmark runs. Ten different voltage/firmware combinations. Ten crashes.

```
Run 1-8 (QRRP):   Wrong firmware, various voltages. CPU degraded 69%.
Run 9 (XJFD):     Right voltage, wrong firmware. Reached target, reopened.
Run 10 (BBUD):    Right firmware, wrong voltage. Dead on arrival.
Run 11 (AJTK):    Right firmware, right voltage. Fresh silicon.
```

The firmware is correct. The voltage is validated. The silicon is fresh. AJTK is the final form.

$100K → $5.9M → $272M+. One DARWIN. One thesis. One EA. One man who killed 10 DARWINs learning how to run one. v1.430 is the final form.

-- TyphooN

---

> **DISCLAIMER:** This post describes a speculative trading strategy using leveraged crypto CFDs. This is NOT financial advice. Past simulation results do not guarantee future performance. Leveraged trading carries substantial risk of loss including loss exceeding your initial deposit. Crypto markets are volatile, illiquid, and manipulated. Do not trade crypto CFDs with money you cannot afford to lose. Do not attempt cascade martingale strategies without understanding that you can lose everything. The author holds active short positions in SOLUSD.
