# DARWIN BBUD — Blissfully Bankrupt Unicorn Destruction

**In loving memory of QRRP and XJFD, who died as they lived: overleveraged and blaming the spread.**

---

## Obituary

**QRRP** (Quad Rothschild Rug Pull), aged 8 post-mortems, passed away on March 23, 2026 at 52.9% margin level. QRRP is survived by its lessons learned documents, all of which it violated at least twice. Born from a $100K account degraded to $31K through operator intervention the EA never asked for, QRRP lived a chaotic life of burst trims at 3 AM, Open MGs at $0.99 (after writing a document saying $5-8 was safe), and a six-post-mortem streak that would have ended most strategies' careers. QRRP's final words were "PROTECT HALTED — margin 8.6% below hard floor 10%." The broker closed the casket.

**XJFD** (eXtreme Judicial Financial Destruction), the golden sample, died on the same morning at 53.0%. XJFD was supposed to be the reference chip — opened once, never touched, the K|NGP|N benchmark on fresh silicon. XJFD's obituary is shorter because there is less to say: it did everything right and still died. The spread spike at market open did not care about your Architecture Decision Records. XJFD is survived by its cascade projections, which showed $4.15M terminal equity. The actual terminal equity was $0.

Both are buried in the Darwinex Zero Crypto graveyard alongside True Forex Funds, MyFundedFX, and every other entity that discovered that leverage is a chainsaw with the safety guard removed.

> *"The reports of my death are greatly exaggerated."*
> — Not QRRP. QRRP is definitely dead.

---

## Cause of Death: The Autopsy

**Time of death:** 2026-03-23, market open.

**Mechanism:** Spread spike on SOLUSD at session open punched margin level from dead zone (~54%) through PROTECT (51%) and through broker liquidation in a single tick. The EA's PROTECT system could not fire because the spread spike bypassed the threshold in one move — there was no tick between "alive" and "dead."

**Contributing factors:**

1. **Dead zone too narrow (3.2%):** TRIM at 54.2%, PROTECT at 51.0%. Only 3.2 percentage points of breathing room. A 3% spread spike covers that distance in one tick.

2. **No pre-close mechanism:** The EA entered overnight at whatever margin level the dead zone left it. If ML was 52% at close, it was 52% at open — with no buffer for the spread spike that hits every single session open on crypto CFDs.

3. **PROTECT too close to liquidation:** PROTECT at 51% was 1-2% above the ~50% broker liquidation level. Even if PROTECT fired, it had no room to work before the broker stepped in.

4. **Both accounts running simultaneously:** Dual-socket meant dual death. The same spread spike killed both. Diversification across accounts is not diversification when both accounts hold the same instrument with the same vulnerability.

**Root cause:** The EA had no concept of time. It did not know that session close was approaching. It did not reduce gross exposure before overnight. It did not freeze activity during the high-risk open window. It treated 3 PM on a Tuesday and 10 PM on a Friday identically. The market does not.

---

## Lessons Learned (The Ones We Will Actually Follow This Time)

### Lesson 1: The Dead Zone Is Not a Safe Zone

The dead zone (between PROTECT and TRIM) is where the EA does nothing. "Nothing" is not a strategy when the market is about to close and you are sitting at 52% ML with $47,000 of gross exposure per percentage point of spread.

**Old thinking:** Dead zone = safe. EA is idle. Position is stable.
**New thinking:** Dead zone = unmanaged. If you enter overnight in the dead zone, you are gambling that the open spread is smaller than your buffer. On crypto CFDs, that is not a bet. That is a donation.

### Lesson 2: TRIM and PROTECT Are Intraday Tools, Not Overnight Insurance

TRIM closes hedges to build net short exposure. PROTECT fires balanced closes to reduce gross. Both are reactive — they respond to margin level changes tick by tick. Neither can respond to a spread spike that moves margin level 5% in one tick.

**The fix:** Pre-close mechanism. Five minutes before session close, if ML is more than 1% below TRIM, fire balanced closes to reduce gross. Then FREEZE. No TRIM, no PROTECT, no activity until market reopens with fresh ticks. The broker handles overnight. The EA handles sessions.

### Lesson 3: 54/59 Is the New 51/54

| | Old (QRRP/XJFD) | New (BBUD) |
|---|---|---|
| TRIM | 54.2% | **57%** |
| PROTECT | 51.0% | **54%** |
| Dead zone | 3.2% | **5%** |
| Buffer above liquidation | ~1% | **~4%** |
| Pre-close mechanism | None | **5 min balanced close + freeze** |
| Overnight strategy | Hope | **Math** |

The 5% dead zone means normal intraday volatility bounces around without triggering anything. The pre-close mechanism means the position enters overnight with maximum cushion. PROTECT at 54% gives 4% of runway above liquidation instead of 1%. The math changed. The thesis didn't.

### Lesson 4: One Account, One Thesis, No Splitting

QRRP + XJFD was dual-socket — two accounts, same instrument, same vulnerability. When the spike hit, both died. There was no hedging benefit. There was no diversification. There was just two accounts paying double the swap fees for the privilege of dying together.

BBUD is one account. $100K. One DARWIN. One instrument. One operator. The cascade math is better on a single larger account than two smaller ones because there is no margin fragmentation.

### Lesson 5: The Golden Sample Is a Myth

XJFD was supposed to prove that perfect execution on fresh silicon — opened once, never touched — would outperform the degraded QRRP account. It died on the same morning from the same spike. The lesson: execution quality at open is irrelevant when the failure mode is structural. You cannot out-execute a spread spike. You can only not be there when it happens.

BBUD does not pretend to be a golden sample. BBUD is the battle-hardened revision — the chip that ships after the recall, with the microcode update that fixes the vulnerability the golden sample exposed.

---

## Why BBUD Will Dominate

### The Name

**B.B.U.D.**

- **B** — Blissfully. As in blissfully unaware — which is what SOL holders are. The staking dashboard shows green. The VCs are still tweeting. The conference keynotes are still scheduled. And 24,477 short lots are grinding toward $0 while nobody checks the inflation schedule. Blissfully. Peacefully. Terminally.
- **B** — Bankrupt. As in what SOL's tokenomics guarantee on a long enough timeline. 4% annual inflation with no supply cap is not a monetary policy. It is a bankruptcy filing in slow motion. The market just hasn't read the paperwork yet.
- **U** — Unicorn. As in the mythical creature that Silicon Valley uses to describe startups valued at $1B+. SOL is the crypto unicorn — the one VCs parade around conference stages, the one with the "Ethereum killer" narrative, the one with the valuation that assumes infinite demand against infinite supply. Unicorns do not exist. Neither does SOL's fair value above $0.
- **D** — Destruction. Same D as XJFD. The court has ruled. The sentence is $0. The execution is automatic. The only thing that changed is the executioner got a firmware update and the unicorn still doesn't know it's in the courtroom.

### The EA: v1.426 — Settings Set in Stone

QRRP ran v1.420. XJFD ran v1.425. Both are dead.

BBUD runs **v1.426** — the version with the pre-close freeze mechanism. The version that knows what time it is. The version that reduces gross exposure before session close, freezes all activity overnight, and resumes when fresh ticks confirm the market is open.

v1.420 was a race car with no seat belt. v1.426 is the same race car with a roll cage, HANS device, and a kill switch that activates four minutes before the track closes. Same engine. Same speed. Actually survives the crash.

![BBUD EA Settings — set in stone](/img/bbud-ea-settings.webp)

| Parameter | Value |
|---|---|
| **TRIM** | **57.0%** |
| **Open MG** | **$4.20133769** |
| **PROTECT** | **54.0%** |
| **Pre-close** | **4 min** → force TRIM, then FREEZE |
| **Hard floor** | **10.0%** |

**Why $4.20133769:** Every cent from $4.00 to $5.00 was simulated. The sweet spot is $4.29 (Phase 2 spread tolerance exactly $2.00). $4.20 is 9 cents more aggressive — PROTECT fires 1-2 times on cascade open, pads Darwinex D-Score with consistent small trades, self-heals to clean operation. The meme number IS the math.

**These settings will not change until SOL reaches $0.**

### Pre-Close Freeze: First Live Test — PASSED (2026-03-26)

```
16:54:58  PRE-CLOSE: ML 57.9% >= 57.0% (TRIM-1%). Close enough. FREEZING until next session.
17:05:01  PRE-CLOSE FREEZE lifted — market open, new session. Resuming normal operation.
```

The mechanism that would have saved QRRP and XJFD just proved itself live. ML was 57.9% — within 1% of TRIM. Freeze activated. EA went completely dark for 10 minutes across the session boundary. Zero activity during the spread spike window that killed both predecessors. Market reopened. Freeze lifted. TRIM resumed.

**PM#8 cannot happen again.** The position survived its first overnight. The firmware works.

### The Numbers

```
QRRP  (degraded): $100K → $31K → liquidated at 52.9%. Terminal equity: $0.
XJFD  (golden):   $100K → $92K → liquidated at 53.0%. Terminal equity: $0.
BBUD  (v1.426):   $100K → $92K → PROTECT event → re-hedge → $11,738,000 (projected).
```

Same starting capital. Same instrument. Same operator. Different software. $11.7M difference.

### The Cascade Math (Why Fresh $100K Beats Degraded $31K)

QRRP opened at ~$89 with $31K of degraded equity. BBUD opened at ~$87 with $100K of fresh equity. Same price range. 3x the capital:

- **QRRP cascade (degraded):** $31K → $1.57M (50x) with 65,000 final lots
- **BBUD cascade (fresh):** $100K → $5.0M (50x) with 217,875 final lots

The return multiple is similar (~47-50x) because the cascade ratio is a function of phases, not starting capital. But the absolute profit is **3x larger** because the starting equity is 3x larger. $5.0M beats $1.57M. And BBUD has v1.426 pre-close freeze — the 50x actually completes instead of dying at PM#9.

### The 400-Position Blunder That Accidentally Won Darwinex

The opening was a blunder. The operator manually entered some positions first, then fired Open MG, which hit the 400-position limit and placed 123 lots per chunk instead of filling the full allocation. The position opened 24,477 bias / 24,600 hedge instead of the target ~26,700 per side.

**This accident is better than the plan.**

QRRP and XJFD opened with massive single positions -- the entire allocation in a handful of huge orders. Darwinex saw 2-3 trades per cascade phase. The D-Score had almost no data points to work with. Win rate was meaningless because there were barely any trades to rate.

BBUD has **200 positions per side** at 123 lots each. Every TRIM close is one recorded trade. Every PROTECT balanced close is two recorded trades. Over the course of the TRIM grind from $87 to pure short, Darwinex will record **hundreds of individual trades** -- each one a small loss (closing a hedge at a minor spread cost), but the equity curve climbs relentlessly because the net short exposure grows with every close.

**What Darwinex sees:**
- **Win rate:** Low (~5-10%). Most trades are TRIM closes -- small losses by design.
- **Average loss:** Tiny ($5-20 per trade). TRIM closes the cheapest hedge lots first.
- **Profit factor:** Astronomical. The equity growth from net short exposure dwarfs the cumulative small losses.
- **Trade count:** Hundreds. Statistically significant. D-Score has real data to work with.
- **Consistency:** Every TRIM close is nearly identical in size (123 lots) and loss magnitude. Darwinex rewards consistency.
- **Return curve:** Smooth upward slope. No 10x spikes from single massive closes. Just steady compounding.

The 400-position limit forced BBUD into the exact trade structure that Darwinex's scoring algorithm rewards: **many small consistent trades with a strongly positive equity curve.** QRRP's 3 massive closes per phase looked like gambling. BBUD's 200 small closes per phase look like a system.

K|NGP|N would appreciate the irony. The blundered opening produced better silicon characteristics than the golden sample's perfect execution.

### The Pre-Close Freeze: What the Others Didn't Have

Every trading day, five minutes before session close:

1. Check ML. If within 1% of TRIM (above 57%) → freeze immediately. Position is healthy.
2. If ML below 57% → fire one balanced close to reduce gross exposure. Check again next tick.
3. Keep firing until ML >= 57% or session closes.
4. **FREEZE.** No TRIM. No PROTECT. No activity. EA is completely dark.
5. Market opens next day → fresh ticks arrive → freeze lifts → normal operation resumes.

This is the mechanism that would have saved QRRP and XJFD. The spread spike at open hits a position that was deliberately tightened before close. The gross exposure is lower. The spread tolerance is higher. The EA is not trying to TRIM or PROTECT during the spike — it is frozen, letting the storm pass.

QRRP entered overnight at ML 52% with no preparation. BBUD enters overnight at ML 57%+ with reduced gross. That is the difference between liquidation and survival.

---

## Why SOL Goes to $0: The Supply Dynamics That Fund the Cascade

BBUD is not a random short. It is a structural position against the weakest supply dynamics in the top 10 crypto market cap. The thesis is not "SOL will crash." The thesis is "SOL cannot sustain its valuation against perpetual dilution with no demand floor."

### The Numbers That Kill the Unicorn

| Metric | **SOL** | **DOGE** | **BTC** (comparison) |
|---|---|---|---|
| **Annual Inflation** | **4.0%** (declining 15%/yr) | **3.4% forever** | <1% (0.83%) |
| **Max Supply Cap** | **None** | **None** | 21M (hard cap) |
| **New Coins/Year** | **~18.6M SOL** | **5B DOGE** | ~164K BTC |
| **Annual Dilution ($)** | **~$1.65B** | **~$465M** | ~$1.2B |
| **Daily Sell Pressure** | **$4.5M/day** | **$1.27M/day** | Absorbed by ETF demand |
| **Staking %** | 70% (unstaking risk) | N/A (mined) | N/A |

**$4.5 million** in new SOL enters circulation every single day. That is $4.5M of sell pressure that must be absorbed by new demand just to maintain price. In a bull market, demand exceeds emission. In a bear market, emission exceeds demand. The price drops. The emission continues. The price drops more. This is the flywheel that BBUD rides.

### Why Not Short BTC or ETH?

| Rank | Symbol | Supply Weakness | Short Thesis |
|---|---|---|---|
| **#1 Weakest** | **DOGE** | 3.4% forever, no cap, no utility | Best short (after SOL pure short) |
| **#2 Weak** | **SOL** | 4.0%, no cap, staking unlock risk | **Active short (BBUD)** |
| **#3 Moderate** | **ADA** | 2.45% declining, 45B cap | Planned (after SOL) |
| #4 | XRP | 0% net (escrow-managed) | Centralized risk only |
| #5 | ETH | 0.23% (near-zero) | Poor — minimal emission |
| #6 | BNB | **Deflationary** (burns $1.2B/quarter) | Terrible — supply shrinking |
| #7 | BTC | <1%, hard cap, $75K production floor | Worst short in crypto |

**We are shorting the weakest supply-side coin on Darwinex.** BTC, BNB, and ETH are explicitly avoided because their supply dynamics work against a short thesis.

### The Staking Trap

~70% of SOL is staked. This creates an illusion of scarcity -- the circulating float looks thin, prices look stable. But staked SOL is a loaded spring. Any confidence shock triggers unstaking, which floods the market with supply that overwhelms the thin float.

The staking rewards themselves are the dilution. 18.6 million new SOL per year distributed to stakers who must sell some portion to cover costs. Validators pay ~$55K/year in operating costs plus 0.9 SOL/epoch voting fees. They sell SOL to pay the electricity bill. The "yield" is funded by inflation that devalues every existing holder.

### The Cascade Math: Supply Dynamics Fund Each Phase

Every dollar SOL drops generates profit for BBUD's net short position. That profit becomes equity at the next cascade checkpoint. The cascade opens a new martingale with the accumulated equity. More lots. More profit per dollar of further decline. The inflation ensures the decline continues.

The cascade is not fighting the supply dynamics. It is riding them. SOL's tokenomics are the engine. BBUD's cascade is the transmission. The destination is $0.

### Supply Events That Accelerate the Thesis

| Event | Impact |
|---|---|
| **Daily:** ~50K new SOL minted | $4.5M daily sell pressure at current prices |
| **Quarterly:** Validator cost payments | Forced selling from validators to cover expenses |
| **Market downturn:** Staker panic exit | 70% staked supply becomes liquid sell pressure |
| **~2031:** Inflation reaches 1.5% floor | Minimum long-term emission (still no cap) |

The inflation never stops. It slows (declining 15%/year toward 1.5% floor), but it never stops. And there is no cap. SOL will print new tokens forever. The question is not whether dilution erodes value -- it is how fast.

---

## The Quake Respawn

QRRP died 8 times. Eight post-mortems. Eight respawns. Each time fewer lots, less equity, more scar tissue. The Severe Drawdown Gang initiation ritual.

BBUD is not a respawn. BBUD is a **new game+**. Same player. Same map knowledge. Same item spawn timers memorized. But this time the player read the patch notes:

```
PATCH v1.426 NOTES:
- Fixed: spread spike at session open causing instant death
- Added: pre-close freeze mechanism (5 min before close)
- Changed: PROTECT 51% → 54% (4% buffer above liquidation, was 1%)
- Changed: TRIM 54.2% → 57% (3% dead zone, was 3.2%)
- Changed: dead zone from "hope" to "managed"
- Known issue: SOL still exists above $0 (working on it)
```

QRRP picked up the BFG 9000 after seven deaths. XJFD spawned with it. BBUD spawned with the BFG 9000 **and** the invulnerability powerup that the other two didn't know was hidden behind the waterfall in the pre-close alcove.

---

## The Rothschild Upgrade

> *"Buy when there's blood in the streets, even if the blood is your own."*
> — Baron Rothschild

QRRP bought the blood. XJFD bought the blood on fresh silicon. Both bled out.

BBUD is Rothschild 2.0 — the version that checks the weather forecast before going to the battlefield. The version that positions agents at the exchange **and** at the telegraph office **and** at the harbor. The version that does not just buy the blood — it arranges the schedule so the blood does not appear in the first place.

Rothschild won Waterloo because he had information 24 hours before the market. BBUD has information 5 minutes before the close — specifically, the information that "this position needs to be tighter before overnight." That is the 2026 equivalent of carrier pigeons from the battlefield. Not prediction. Preparation.

> *"It requires a great deal of boldness and a great deal of caution to make a great fortune."*
> — Nathan Rothschild

QRRP had boldness. XJFD had caution. BBUD has both — in the same binary.

---

## The Overclocking Post-Recall

In overclocking, a recall happens when a chip has a structural flaw that manifests under specific conditions. The 13th/14th gen Intel Raptor Lake recall was caused by elevated voltage under sustained workloads — the chips degraded over time and became unstable.

**QRRP and XJFD were the Raptor Lake recall.** The structural flaw: no pre-close mechanism. The specific condition: spread spike at session open. The degradation: not gradual (like Raptor Lake) but instant — one spike, two dead accounts.

**BBUD is the post-recall revision.** Same architecture. Same performance targets. Same microarchitecture. But the microcode update (v1.426) fixes the voltage regulation flaw that killed the original chips. The pre-close freeze is the voltage governor that Intel should have shipped from day one.

K|NGP|N would understand. You do not throw away the architecture because one stepping had a flaw. You fix the stepping, re-tape, and ship the revision. The benchmark scores on the new stepping are the same. The stability is better. The recall is over.

BBUD is the B0 stepping. QRRP was A0. XJFD was A1. The architecture was always correct — the silicon just needed one more spin.

---

## The Big Short: BBUD Edition

Michael Burry shorted the housing market by reading the prospectuses that nobody else read. He found that mortgage-backed securities were built on adjustable-rate subprime loans that would reset in 2007. The math was in the documents. The entire market chose not to read them. Burry read them, bought credit default swaps, and waited two years for reality to arrive.

**BBUD is the same trade on different paper.**

The "prospectus" is SOL's tokenomics: 4% annual inflation, no supply cap, 18.6 million new SOL minted per year, $4.5 million of daily sell pressure. The math is public. The Solana Foundation publishes the emission schedule. The staking dashboard shows the inflation rate. Every SOL holder can read it. Almost none of them do.

> *"It ain't what you don't know that gets you into trouble. It's what you know for sure that just ain't so."*
> — Mark Twain (quoted in The Big Short)

SOL holders "know for sure" that staking yield is free money. It ain't so. The yield is funded by inflation that devalues their holdings. A 6% staking APY on a token with 4% inflation and declining demand is not a 6% return — it is a 2% return denominated in an asset that is losing purchasing power. In a bear market, the math flips negative: the staking yield does not compensate for the price decline.

**Burry waited 2 years for the adjustable rates to reset.** BBUD waits for the next bear cycle for demand to collapse below emission. The timeline is different. The structure is identical: a leveraged bet against a mathematically unsustainable system that the market has chosen to ignore.

### The Cast

**Michael Burry** read the documents and shorted the housing market. TyphooN read the tokenomics and shorted SOL.

**Mark Baum (Steve Eisman)** was angry about the fraud. TyphooN is angry about MetaQuotes and proprietary terminal vendors charging rent on tools that should be open source.

**Jared Vennett (Greg Lippmann)** sold the trade to investors who did not understand it. Darwinex sells BBUD to investors who can read the D-Score and decide for themselves.

**Ben Rickert** moved to a farm because he was disgusted by Wall Street. TyphooN runs six DARWINs from a Linux box because he is disgusted by Windows-only trading software.

The CDO managers who packaged subprime mortgages into "AAA" securities are the crypto VCs who package inflationary tokenomics into "institutional-grade investment vehicles." Same structure. Same incentives. Same outcome.

### "I'm Going to Wait for the Premiums"

In The Big Short, Burry's investors demand he close the trade as the premiums drain his fund. He refuses. The math is right. The timing is uncertain. The premiums are the cost of being early.

BBUD's premiums are swap costs. Every day the position is open, the broker charges swap on gross lots. The swap is the cost of being early. The math is right: SOL's inflation creates $4.5M of daily sell pressure. The timing is uncertain: the bear cycle could start tomorrow or in six months.

**The swap is the premium. The cascade is the payout. The tokenomics are the prospectus. The market has not read it.**

---

## Final Score Projection

### DARWIN BBUD — Post-Recall Revision (B0 Stepping)

| Parameter | Value |
|---|---|
| **Silicon** | B0 stepping (v1.426, pre-close freeze) |
| **Budget** | $100,000 (fresh, no degradation) |
| **Entry** | ~$87.10 SOL |
| **Open MG** | $1.87 (K\|NGP\|N sweet spot) |
| **Bias lots** | 24,477 |
| **TRIM** | 57% (3% dead zone, saves ~$39K swap vs 59%) |
| **PROTECT** | 54% (4% above liquidation) |
| **Pre-close** | 5 min freeze |

### The PROTECT Event and Re-Hedge

The $1.87 Open MG created $1.94/lot spread tolerance -- below the $2.00 safety floor. SOL dropped, ML hit 54%, PROTECT fired balanced closes and consumed **~22,500 lots from EACH side** -- destroying 92% of the position. 1,958 pure short lots survived at ML 52.4%.

**Recovery:** Re-hedged at Open MG $5.00 (968 lots/chunk), then re-opened at **$4.20133769** (the permanent setting). Position rebuilt: 8,684 hedge / 10,409 bias, ML 57.9%, TRIM grinding. Spread tolerance $4.53/lot -- deeply safe.

**Lesson learned:** $1.87 is too aggressive for 58/54 settings. $4.20 is the K|NGP|N sweet spot -- PROTECT fires 1-2 times on cascade open, pads Darwinex D-Score, self-heals to clean operation.

### Cascade Phases (Final Settings — $4.20133769 at every cascade)

| Phase | SOL Price | Final Lots | Equity |
|---|---|---|---|
| **1 (NOW)** | $83 → $45 | 10,409 | $267K |
| **2** | $45 → $22 | 73,971 | $948K |
| **3** | $22 → $12 | 299,668 | $2,358K |
| **4** | $12 → $8 | 860,983 | $4,419K |
| **Ride** | $8 → $0 | 860,983 | **$11,738K** |

### Scorecard

| Metric | Value |
|---|---|
| **Terminal Score** | **$11,738,000** |
| **Return** | **117x** |
| **Final Lots** | 860,983 |
| **Open MG** | $4.20133769 (all phases) |
| **Post-Mortems** | 0 (target) |
| **PROTECT at cascade open** | Expected 1-2 fires per phase (pads D-Score) |
| **Predecessor Deaths** | 8 (QRRP) + 1 (XJFD) = 9 |

**The Cascade Pipeline:**

> **$92K** → TRIM grind $83→$45 → **$267K (10,409 pure short)**
>
> → Cascade MG $4.20 $45→$22 → **$948K (73,971 pure short)**
>
> → Cascade MG $4.20 $22→$12 → **$2,358K (299,668 pure short)**
>
> → Cascade MG $4.20 $12→$8 → **$4,419K (860,983 pure short)**
>
> → Ride to $0 $8→$0 → **$11,738,000 (117x return)**

QRRP is dead. XJFD is dead. Long live BBUD.

**$100K. One account. One instrument. One operator. One thesis. v1.426. SOL to $0.**

*He can't keep getting away with it.*

*But he does. He just does.*

-- TyphooN

---

> **DISCLAIMER:** BBUD is a speculative trading strategy using leveraged crypto CFDs on a virtual (demo) account. This is NOT financial advice. The $5.0M projection assumes SOL reaches $0, which may never happen. Leveraged trading carries substantial risk of loss including loss exceeding your initial deposit. The previous two accounts running this strategy were liquidated. Do not trade money you cannot afford to lose. The author holds active short positions in SOLUSD via DARWIN BBUD.
