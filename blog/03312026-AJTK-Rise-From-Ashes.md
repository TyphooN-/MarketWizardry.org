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
| **Open MG** | $1.87 (validated on XJFD: ~10% degradation, ~18,500 surviving bias) |
| **EA Version** | v1.429 (PROTECT closes bias, pre-close freeze, hard floor 10%) |
| **Position** | 7,725L / 9,600S, net 1,875 SHORT |
| **Equity** | $86,255 \| Balance $89,509 \| Margin $151,309 |
| **SOL Price** | $80.88, ML 57.0% — TRIM actively firing |
| **Spread tol** | $4.98/lot ← SAFE (was $1.77 at open) |
| **TRIM / PROTECT** | 57% / 54% |
| **Pre-close** | 4 min freeze |
| **TRIM closes** | 398 |
| **PROTECT closes** | 0 (EA) |

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

### Phase 1: TRIM Grind to Pure Short — Self-Healed ($83 → ~$40 SOL)

MG $1.87 opened with 26,737/side. Broker forced closures during spread spikes and session boundaries. EA TRIM closed 398 hedge longs. Position now 7,725L / 9,600S. Spread tolerance improved from $1.77 to $4.98 — SAFE. 0 EA PROTECT fires. SOL dropped from $85 to $81 — equity UP from $79K to $86K via net short exposure. ML at 57.0% — TRIM actively firing.

| SOL Price | Equity | Hedge | Net Short | Spread Tol | Status |
|---|---|---|---|---|---|
| **$80.88 (now)** | **$86,255** | **7,725** | **1,875** | **$4.98** | **TRIM firing, ML 57.0%** |
| $70 | $106,000 | 5,000 | 4,700 | $5.45 | Accelerating |
| $60 | $128,000 | 2,500 | 7,700 | $8.39 | Deep safety |
| **~$40** | **~$215,000** | **0** | **~9,600** | **$22.40** | **PURE SHORT → CASCADE** |

Expected pure short at ~$40 SOL. ~9,600 lots. ~$215K equity. **Flywheel confirmed** — SOL dropped $4, equity increased $7K, TRIM fired 216 more closes. Each $1 SOL decline adds ~$1,875 equity from net short exposure.

### Phase 2: Cascade $3.00 at Pure Short (~$40 → ~$24 SOL)

Open MG $3.00 at pure short. ~72K new lots per side. v1.429 PROTECT fires 1-2x, ~73K bias survive.

| SOL Price | Equity | Hedge | Net Short | Status |
|---|---|---|---|---|
| **$40 (cascade)** | **$215K** | **67,000** | **14,600** | **Phase 2 starts** |
| $30 | $570K | 38,000 | 43,000 | Accelerating |
| **~$24** | **~$760K** | **0** | **~73,000** | **PURE SHORT — FINAL** |

### Naked Ride: $24 → $5

~73,000 pure short lots. ~$73K per dollar of SOL decline. Smooth ride for 19 dollars.

| SOL Price | Equity | Status |
|---|---|---|
| $24 | $760K | Smooth ride begins |
| $20 | $1,052K | Cruising |
| $10 | $1,782K | Deep profit |
| **$5** | **$2,147K** | **CLOSE ALL** |

### Deploy Full Crypto Basket

Close SOL shorts at $5 with ~$2.1M. Deploy into all 7 Darwinex cryptos.

| Component | Allocation | Strategy | Target Equity |
|---|---|---|---|
| **ETH** | $1,110K | MG LONG $4.20 | **$49M** |
| **BTC** | $365K | MG LONG $4.20 | **$22M** |
| **DOGE** | $280K | Naked long (6mo) | **$17M** |
| **SOL** | $150K | Naked long | **$6M** |
| **ADA** | $90K | Naked long | **$3M** |
| **XRP** | $85K | Naked long | **$2M** |
| **BNB** | $67K | Naked long | **$1M** |
| **TOTAL** | **$2,147K** | **400 positions** | **~$100M+** |

**$100K → $2.1M (SOL short + cascade) → $100M+ (full crypto basket long). 997x.**

400 positions. 7 symbols. 4.236 fib targets. MG on ETH/BTC. Naked long on everything else. Short the weakest supply on the way down. Long EVERYTHING on the way up.

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

$100K → $2.1M → $100M+. One DARWIN. One thesis. One EA. One man who killed 10 DARWINs learning how to run one.

-- TyphooN

---

> **DISCLAIMER:** This post describes a speculative trading strategy using leveraged crypto CFDs. This is NOT financial advice. Past simulation results do not guarantee future performance. Leveraged trading carries substantial risk of loss including loss exceeding your initial deposit. Crypto markets are volatile, illiquid, and manipulated. Do not trade crypto CFDs with money you cannot afford to lose. Do not attempt cascade martingale strategies without understanding that you can lose everything. The author holds active short positions in SOLUSD.
