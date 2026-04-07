# DARWIN OAMS: Ounces Are My Specialty

*"Walk down the right back alley in Sin City and you can find anything."* Including 5,000 ounces of silver per lot and the conviction to short it.

**Published: 2026-04-06 | TyphooN | MarketWizardry.org**

> **DISCLAIMER:** This is not financial advice. These are real trades on a Darwinex Zero account with virtual capital. Shorting silver after burying four natgas DARWINs in a single day is either evolution or insanity. The line is thinner than a Miho blade.

> **TRADING METHOD:** OAMS is managed by TyphooN EA in hedged martingale mode on XAGUSD CFD. Settings: 72/54, micro-lot layers. Discretionary entry by TyphooN, algorithm takes over from there.

---

## O.A.M.S. — Ounces Are My Specialty

*Acronym expanded: **O**unces **A**re **M**y **S**pecialty. Silver is measured in ounces. 5,000 ounces per contract. OAMS measures in precision — micro-lot layers, 18% DEAD zone, and the patience that four dead natgas DARWINs bought. CKUC died at 6%. IYCN died at 10% and 14%. WNSO died at 20%. OAMS doesn't repeat the mistake — different instrument, different margin, different math.*

*"Deadly little Miho."* — Dwight, describing the deadliest woman in Basin City. She doesn't talk. She doesn't negotiate. She just cuts. OAMS is the Miho of the DARWIN portfolio — micro-lot precision, silent execution, no wasted motion. Every 0.1 lot is a blade. Every TRIM close is a cut. The shorts accumulate. The longs die quietly.

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

---

## The Position — "The Big Fat Kill"

![DARWIN OAMS — XAGUSD MTF Grid: H1/Weekly/Daily/Monthly (April 2026)](/img/oams-mtf-xagusd-20260406.webp)

*"It's time to prove to your friends that you're worth a damn. Sometimes that means dying. Sometimes it means killing a whole lot of people."* — Dwight, before the alley fight. OAMS deploys into Basin City's silver alley with precision:

```
OAMS deployment (2026-04-06):
  Longs:        62 layers
  Shorts:       65 layers
  Net SHORT:    2.78 lots
  ML:           64.5%
  Equity:       $64,582
  Balance:      $95,440
  Settings:     72/54 (18% DEAD zone)
  TRIM:         Paused (needs 72%)
  PROTECT:      Sleeping (needs 54%)
```

ML 64.5% — deep in the DEAD zone. TRIM won't fire until ML reaches 72%. PROTECT won't wake until 54%. The EA does nothing. The position breathes. The shorts collect swap.

---

## Why 72/54 on Silver

18% DEAD zone. The widest proven configuration from the natgas graveyard, applied to an instrument that actually supports it:

- **TRIM at 72%:** Patient. Shorts survive longer, collecting +$38/lot/day swap. When silver drops and ML rises above 72%, TRIM grinds hedge longs — closing the positions that cost swap, improving net income
- **PROTECT at 54%:** Below spread-induced ML dips. Silver spreads are tighter than natgas, but off-hours widening still happens. 54% is deep enough that only a real move triggers it — never a spread artifact
- **18% DEAD zone:** Massive buffer. On micro-lots, this is insurmountable by normal price action

**The swap advantage:** Unlike XNGUSD (long-biased, negative bias swap), OAMS is short-biased with **positive bias swap**. As TRIM closes longs, three things happen simultaneously:
1. Swap income improves (fewer negative-swap longs)
2. Directional short bias increases
3. Balance prints from profitable long closes (if silver dropped)

The grind is self-reinforcing. Every TRIM close makes the position healthier.

---

## Four Headstones, One Evolution

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

*"She doesn't quite chop his head off. She makes a Pez dispenser out of him."* — Dwight, watching Miho work. OAMS doesn't need to be dramatic. It just needs to cut 0.1 lots at a time until the position is pure short and the thesis prints.

---

## Swap Profile at 62L/65S

| Period | Short Swap (+$38/lot) | Long Swap (-$51/lot) | Net Swap | As TRIM grinds longs... |
|---|---|---|---|---|
| **Daily** | +$2,470 (65 lots equiv) | -$3,162 (62 lots equiv) | -$692 | Improves toward positive |
| **Wednesday 3x** | +$7,410 | -$9,486 | -$2,076 | — |
| **Weekly** | +$17,290 | -$22,134 | -$4,844 | Improves weekly |

Net swap starts slightly negative but **improves as TRIM closes longs**. Once TRIM has closed enough longs, net swap flips positive. The position starts paying you to hold it. This is the dream scenario that XNGUSD could never achieve.

---

*"Walk down the right back alley in Sin City and you can find anything."* OAMS found the right alley. Different metal. Different math. Same conviction. Micro-lot Miho, cutting silver ounces one blade at a time.

*Ounces Are My Specialty.*

-- TyphooN

---

> **DISCLAIMER:** This post describes a speculative trading strategy using leveraged commodity CFDs on a virtual (demo) account. This is NOT financial advice. Four previous natgas DARWINs sustained total account losses before OAMS was created on XAGUSD. Hedged martingale carries inherent risk regardless of instrument. Do not trade commodity CFDs with money you cannot afford to lose. The silver short thesis is the author's personal opinion and is not a recommendation to trade XAGUSD.
