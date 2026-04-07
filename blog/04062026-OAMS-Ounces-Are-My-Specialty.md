# DARWIN OAMS: Ounces Are My Specialty

*"First there was darkness. Then came the Strangers."*

**Published: 2026-04-06 | TyphooN | MarketWizardry.org**

> **DISCLAIMER:** This is not financial advice. These are real trades on a Darwinex Zero account with virtual capital. Shorting silver after burying four natgas DARWINs in a single day is either evolution or insanity. The Strangers would call it an experiment.

> **TRADING METHOD:** OAMS is managed by TyphooN EA in hedged martingale mode on XAGUSD CFD. Settings: 74/54, micro-lot layers. Discretionary entry by TyphooN, algorithm takes over from there.

---

## O.A.M.S. — Ounces Are My Specialty

*Acronym expanded: **O**unces **A**re **M**y **S**pecialty. Silver is measured in ounces. 5,000 ounces per contract. OAMS measures in precision — micro-lot layers, 20% DEAD zone, and the patience that four dead natgas DARWINs bought. CKUC died at 6%. IYCN died at 10% and 14%. WNSO died at 20%. OAMS doesn't repeat the mistake — different instrument, different margin, different math.*

*"I have become the monster you were looking for."* — John Murdoch learned to tune reality. TyphooN learned to tune margin levels. Four dead DARWINs were the experiment. OAMS is the result — the ability to reshape the position at will, one micro-lot at a time. The Strangers rearranged the city every midnight. OAMS rearranges the hedge at every TRIM tick.

---

## The Instrument — Why Silver, Why Now

Four natgas DARWINs died teaching one lesson: **margin per lot determines hedged martingale viability.** XNGUSD at $2,900/lot made every PROTECT close a 3% ML earthquake. The overcorrection was structural, not configurable.

XAGUSD changes the math:

| Spec | XNGUSD | XAGUSD | SOLUSD (BULS) |
|---|---|---|---|
| **Margin/lot** | $2,900 | $36,065 | $68 |
| **Margin/0.1 lot** | $290 | ~$3,607 | $6.80 |
| **Margin/0.01 lot** | $29 | ~$361 | $0.68 |
| **Swap short** | +$48/lot | +7.6 pts (+$38/lot) | -$2.37/lot |
| **Swap long** | -$78/lot | -10.2 pts (-$51/lot) | +$2.37/lot |
| **Net hedged swap** | -$30/lot | -$13/lot | $0/lot |
| **Bias direction** | Long | **Short** | Long |
| **Bias swap** | **Negative** (-$78) | **Positive** (+$38) | **Positive** (+$2.37) |

**The key difference:** OAMS is short-biased on an instrument where shorts earn positive swap. As TRIM closes hedge longs (which cost swap), the net swap **improves** over time. The exact opposite of XNGUSD where closing hedge shorts reduced swap income.

At micro-lot sizing (0.1 per layer), each PROTECT close swings ML by ~0.36% instead of 3%. The overcorrection problem vanishes.

*"They wanted to find out what makes us tick. So they took us apart, studied us, and put us back together again."* — Dr. Schreber, describing the Strangers' experiments. Four natgas DARWINs were taken apart. OAMS is what was put back together.

---

## The Position — "Tuning"

![DARWIN OAMS — XAGUSD MTF Grid: H1/Weekly/Daily/Monthly (April 2026)](/img/oams-mtf-xagusd-20260406.webp)

*"You have the power to make things happen by will alone."* — Dr. Schreber to John Murdoch. The EA has the power to reshape the position by margin level alone. TRIM tunes the hedge. PROTECT tunes the bias. The DEAD zone is where the city sleeps — nothing moves, nothing changes. The position holds its shape until the next midnight.

```
OAMS deployment (2026-04-06):
  Longs:        62 layers
  Shorts:       65 layers
  Net SHORT:    2.78 lots
  ML:           64.5%
  Equity:       $64,582
  Balance:      $95,440
  Settings:     74/54 (20% DEAD zone)
  TRIM:         Paused (needs 72%)
  PROTECT:      Sleeping (needs 54%)
```

ML 64.5% — deep in the DEAD zone. TRIM won't fire until ML reaches 74%. PROTECT won't wake until 54%. The EA does nothing. The position breathes. The shorts collect swap. The city sleeps.

---

## Why 74/54 on Silver

20% DEAD zone. The widest proven configuration from the natgas graveyard, applied to an instrument that actually supports it:

- **TRIM at 74%:** Patient. Shorts survive longer, collecting +$38/lot/day swap. When silver drops and ML rises above 74%, TRIM grinds hedge longs — closing the positions that cost swap, improving net income
- **PROTECT at 54%:** Below spread-induced ML dips. Silver spreads are tighter than natgas, but off-hours widening still happens. 54% is deep enough that only a real move triggers it — never a spread artifact
- **20% DEAD zone:** Massive buffer. On micro-lots, this is insurmountable by normal price action

**The swap advantage:** Unlike XNGUSD (long-biased, negative bias swap), OAMS is short-biased with **positive bias swap**. As TRIM closes longs, three things happen simultaneously:
1. Swap income improves (fewer negative-swap longs)
2. Directional short bias increases
3. Balance prints from profitable long closes (if silver dropped)

The grind is self-reinforcing. Every TRIM close makes the position healthier.

*"Sleep... now..."* — The Strangers' command when they reshape the city at midnight. Every night at swap rollover, OAMS collects. The shorts earn. The longs bleed. Midnight by midnight, the position tunes itself toward pure short.

---

## Four Headstones, One Evolution

*"There used to be a way out of this city. I've seen it in my memories."* — Everyone in Dark City remembers Shell Beach. No one can find it. Four natgas DARWINs remembered profitability. None could find it. OAMS stopped looking in the same place.

OAMS stands on the graves of four natgas DARWINs — but it's not another XNGUSD attempt. It's the answer to what they died asking:

| DARWIN | Instrument | Margin/lot | Bias Swap | DEAD Zone | Result |
|---|---|---|---|---|---|
| CKUC | XNGUSD | $2,900 | -$78 (negative) | 6-8% | Dead |
| IYCN R1 | XNGUSD | $2,900 | -$78 (negative) | 10% | Dead |
| IYCN R2 | XNGUSD | $2,900 | -$78 (negative) | 14% | Dead |
| WNSO | XNGUSD | $2,900 | -$78 (negative) | 20% | Dead |
| **OAMS** | **XAGUSD** | **$3,607/0.1** | **+$38 (positive)** | **18%** | **Active** |

The natgas DARWINs died because the math was wrong: high margin per lot + negative bias swap + wide spreads = guaranteed overcorrection. OAMS flips every variable:
- Micro-lot sizing eliminates overcorrection
- Positive bias swap means the grind is self-funding
- Silver spreads are tighter than natgas
- Short conviction backed by technical setup

*"I was just thinking, what you do seems kind of like brain surgery."* — Inspector Bumstead to Dr. Schreber. What OAMS does to the XAGUSD order book seems kind of like brain surgery. Micro-lot precision. Every layer placed deliberately. Every TRIM close calculated. No wasted margin.

---

## Swap Profile at 62L/65S

| Period | Short Swap (+$38/lot) | Long Swap (-$51/lot) | Net Swap | As TRIM grinds longs... |
|---|---|---|---|---|
| **Daily** | +$2,470 (65 lots equiv) | -$3,162 (62 lots equiv) | -$692 | Improves toward positive |
| **Wednesday 3x** | +$7,410 | -$9,486 | -$2,076 | — |
| **Weekly** | +$17,290 | -$22,134 | -$4,844 | Improves weekly |

Net swap starts slightly negative but **improves as TRIM closes longs**. Once TRIM has closed enough longs, net swap flips positive. The position starts paying you to hold it. This is the dream scenario that XNGUSD could never achieve.

*"Shut it down. Shut it down forever."* — John Murdoch, after defeating the Strangers. Once the longs are shut down, only shorts remain. Pure directional. Positive swap. The city belongs to Murdoch. The silver belongs to OAMS.

---

## Hedge Unwind Status (2026-04-06 22:13 UTC)

```
TRIM grinding at ML edge:
  Hedge (longs):  61.72 lots remaining
  Bias (shorts):  64.58 lots
  Net SHORT:      2.86 lots
  TRIM closes:    99
  PROTECT fires:  0
  ML:             72.3%
  Equity:         $74,390
  Settings:       74/54 (20% DEAD zone)
  TRIM speed:     0.01 lots/tick at ML edge
```

99 TRIM closes. Zero PROTECT fires. The EA is grinding 0.01 lots at the 74% edge — micro-lot precision that XNGUSD could never achieve. Each close releases ~$360 of margin. No overcorrection. No panic. Just the steady pulse of the algorithm tuning the position.

### Hedge Unwind Price Projections

6,172 more closes needed (61.72 lots × 100) to reach pure short. Timeline depends on silver price action:

| Scenario | Silver Price | ML Effect | TRIM Speed | Timeline to Pure Short |
|---|---|---|---|---|
| **Range-bound** | ~$72 ±$0.50 | Hovers at 74% edge | 0.01/tick, intermittent | **3-5 trading days** |
| **Drop $1** | ~$71 | ML spikes above 74% | Accelerated, continuous | **1-2 days** |
| **Drop $2** | ~$70 | ML well above 74% | Very fast, multi-lot | **6-12 hours** |
| **Drop $5** | ~$67 | ML extremely high | Maximum speed | **1-3 hours** |
| **Rise $1** | ~$73 | ML drops below 74% | **TRIM paused** | **Indefinite** |
| **Rise $2** | ~$74 | ML approaches 54% | **PROTECT territory** | **Danger zone** |

### Swap Evolution as Longs Close

As TRIM closes longs, net swap improves. The position evolves from net-negative to net-positive carry:

| Longs Remaining | Net Swap/Day | Status |
|---|---|---|
| 61.72 (now) | -$694 | Slightly negative |
| ~48 lots | ~$0 | **Breakeven** — net swap flips positive |
| 30 lots | +$916 | Position pays you to hold |
| 10 lots | +$1,944 | Strong positive carry |
| 0 (pure short) | +$2,454 | **Maximum swap income** |

Once longs drop below ~48 lots, the position flips to positive net swap. From there, every midnight the market pays OAMS to hold the short. The Strangers reshape the city at midnight — and every midnight, they pay tribute.

*"You have the power to make things happen by will alone."* — 99 TRIM closes. Zero PROTECT fires. The will is working.

---

*"First there was darkness. Then came the Strangers."* First there was CKUC. Then IYCN. Then WNSO. Darkness, all of them. Then came OAMS — and OAMS learned to tune.

*Ounces Are My Specialty.*

-- TyphooN

---

> **DISCLAIMER:** This post describes a speculative trading strategy using leveraged commodity CFDs on a virtual (demo) account. This is NOT financial advice. Four previous natgas DARWINs sustained total account losses before OAMS was created on XAGUSD. Hedged martingale carries inherent risk regardless of instrument. Do not trade commodity CFDs with money you cannot afford to lose. The silver short thesis is the author's personal opinion and is not a recommendation to trade XAGUSD.
