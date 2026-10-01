# MRV-P Protocol

**Version 0.4 — draft for comment**
An open protocol for auditable measurement of steel recovered in ship and port dismantling.

Published by GSR Logística Reversa Naval. Free to implement, by anyone, including competitors.

---

## 0. Status of this document

This is a **draft for comment**, not a finished standard. It codifies a method already
implemented and operating in production, derived from one fully instrumented campaign and a
body of peer-reviewed work. It has not been ratified by any standards body, and no conformity
assessment scheme exists for it yet.

It is published openly for a specific reason. A measurement method that only its author can run
is not a measurement method; it is a sales claim. The value of this protocol is that a second
party can implement it, run it on their own yard, and get a comparable number — including a
party competing with the publisher.

**Normative language.** The key words SHALL, SHALL NOT, SHOULD and MAY are used in the
customary sense: SHALL is a requirement for conformance, SHOULD a strong recommendation,
MAY a permitted option.

## 1. Scope

This protocol applies to the dismantling of ships, port equipment and comparable steel-bearing
industrial assets, from the moment an asset is accepted for dismantling to the moment recovered
material is received by a consignee.

It specifies four things: the unit at which mass SHALL be measured; the evidence that SHALL
support each measurement; the arithmetic by which a campaign's material balance is scored and
reconciled; and what an implementer SHALL publish alongside the result.

**Out of scope.** Hazardous-material inventory of the asset before dismantling (covered by the
Hong Kong Convention's IHM regime), occupational safety, environmental licensing, and downstream
metallurgical certification. This protocol is designed to sit *between* the IHM and the mill
certificate, and to interoperate with both.

## 2. The unit of measurement is the load, not the campaign

The failure this protocol exists to correct is aggregate estimation. In current practice,
recoverable steel is estimated from lightweight displacement tonnage (LDT) or from manufacturer
data sheets, and rarely measured. Every downstream claim — traceability, circularity, carbon —
inherits the error of that single estimate.

> **Requirement 2.1.** Recovered mass SHALL be measured per load leaving the site, on a
> weighbridge with valid legal-metrology certification, and SHALL NOT be derived by dividing a
> campaign total.

**Definitions.** A **lot** is the smallest unit carrying an independent material balance. A
**load** is one weighed vehicle movement. A **campaign** is the dismantling of one asset.
Every load SHALL map to exactly one lot; every lot SHALL map to exactly one campaign.

## 3. Evidence layers

Not all records are equal, and a protocol that treats them as equal cannot be audited. Each
measurement SHALL carry an evidence layer, and the layer SHALL be recorded, not inferred.

| Layer | Definition | Weight |
|-------|------------|--------|
| `E1` | Original, contemporaneous certified weighbridge ticket, retained | 1.00 |
| `E2` | Record reconstructed from a primary source, where the original ticket is no longer retained | 0.60 |
| `E3` | Estimated, modelled or simulated value with no document of record | 0.30 |

An implementer MAY extend the scale with further layers; the three above SHALL retain these
weights, so that scores remain comparable between implementations.

**Why E2 exists, and why it is not hidden.** A reconstructed record is not a forgery and is not
a certified ticket. It is a third thing, and the honest move is to name it and discount it. The
publisher's own reference campaign contains both E1 and E2 records, and the protocol was
designed that way because of it.

## 4. Lot compliance score

Each lot SHALL carry a score on six dimensions, each expressed 0–100, combined by fixed weights.

```
S_MRV = 0.30·W + 0.20·D + 0.15·L + 0.15·C + 0.10·G + 0.10·A
```

| Symbol | Dimension | Weight | Meaning |
|--------|-----------|--------|---------|
| `W` | Weight certainty | 0.30 | Instrument class, calibration validity, ticket retention |
| `D` | Documentation | 0.20 | Waste manifest, invoice, receipt certificate, weighing report |
| `L` | Logistics traceability | 0.15 | Unbroken custody from site to consignee |
| `C` | Compliance | 0.15 | Environmental licence, contract, hazardous-material record |
| `G` | Geolocation | 0.10 | Origin and destination coordinates on record |
| `A` | Auditability | 0.10 | Completeness and immutability of the trail |

The score SHALL be computed, never entered by hand. In the reference implementation it is a
generated database column, so no operator can write a score directly.

### 4.1 Grade bands

| Grade | Score | Reading |
|-------|-------|---------|
| `A+` | ≥ 90 | Fully evidenced; suitable for third-party assertion |
| `A`  | ≥ 80 | Evidenced with minor gaps |
| `B`  | ≥ 70 | Traceable; documentation incomplete |
| `C`  | ≥ 60 | Partial; not suitable for external claims |
| `D`  | ≥ 50 | Weak |
| `F`  | < 50 | Unevidenced |

## 5. Confidence tier — a second, independent dimension

A score says how much evidence exists. It does not say whether that evidence agrees with itself.
These are different questions and SHALL NOT be collapsed into one number.

Each lot SHALL therefore also carry a confidence tier, derived from document presence *and* from
machine extraction of the documents' contents reconciled against the recorded values.

| Tier | Condition |
|------|-----------|
| `HIGH` | Invoice, weighing report and waste manifest all present, and at least two independent document extractions match the recorded values |
| `MEDIUM` | Invoice or weighing report present, and at least one extraction matches |
| `LOW` | Photographic evidence only |
| `UNVERIFIED` | None of the above |

> **Requirement 5.1 — gating.** A lot SHALL NOT be used to issue a transferable instrument — a
> token, a certificate, a tradable claim — below `HIGH`. A lot SHALL NOT be used for carbon
> certification below `MEDIUM`.

A high score with a low tier is a well-documented claim that nothing has checked.

## 6. Campaign governance flow

At campaign level the protocol defines a five-step flow. Steps 1 and 5 are the load-bearing
ones; a conforming implementation SHALL implement both.

```
1. Quality gate  →  2. Context  →  3. Prediction  →  4. Score  →  5. Reconcile vs official weight
   integrity +        cycle          ŷ with           S = .4C       e/P > 0.15 ⇒ divergence
   outliers           features       interval         + .3K + .3E            │
        ▲                                                                   │
        └───────────── divergence ⇒ conformance review, ────────────────────┘
                       not silent adjustment
```

### 6.1 Step 1 — data quality gate

Operational records SHALL be screened before any inference.

- Negative values SHALL be logged as errors.
- Univariate outliers SHALL be flagged by a robust z-score using median and median absolute
  deviation (MAD), at a threshold of `3.5`.
- Payload per trip outside `3–20 t` SHALL be flagged as a logistical inconsistency.

### 6.2 Step 4 — campaign score

```
S = 0.40·Completeness + 0.30·Consistency + 0.30·Evidence

Completeness = fraction of required operational fields populated
Consistency  = 0.60 · payload-in-range + 0.40 · free-of-outliers
Evidence     = layer weight from clause 3 (E1 = 1.00, E2 = 0.60, E3 = 0.30)
```

## 7. Reconciliation and the divergence rule

This is the clause the rest of the protocol exists to support.

```
e = | P_official − ŷ |          e / P_official > δ  ⇒  divergence          (δ = 0.15)
```

> **Requirement 7.1.** Where a divergence is raised, the implementer SHALL record it, SHALL route
> it to conformance review, and SHALL NOT resolve it by revising the estimate to match the
> weight. The divergence SHALL remain visible in the published campaign record after resolution.

> **Requirement 7.2.** Every reconciliation check SHALL carry the cause of its difference, or SHALL
> be marked explicitly as unexplained. A difference within `δ` is **not** thereby excused from
> explanation: `δ` bounds when a divergence is *raised*, not when a difference may go
> *uninvestigated*. A check carrying neither a cause nor an explicit unexplained marker is
> non-conforming.

Requirement 7.2 was added in v0.4 because the publisher's own B1 declaration passed clause 7 on a
difference of +6.30% — comfortably inside `δ` — that turned out to be a range error in the source
spreadsheet, with an exact and discoverable cause: a TOTAL cell summing to row 118 while the load
records ran to row 125, omitting seven expeditions worth 42,930 kg. The traceability matrix had
recorded it for months as a "physical ε of +6.3%" and no clause obliged anyone to ask why.

A tolerance that excuses investigation converts a bug into a conformance. `δ` exists to decide when
a difference becomes a *divergence requiring review*; it was never meant to decide when a difference
deserves an *explanation*. Those are different questions, and v0.3 answered only the first.

`δ = 0.15` is a chosen tolerance, not a derived one. It is stated here so that implementers use
the same threshold and so that anyone may argue it is wrong. An implementer MAY apply a tighter
δ; one applying a looser δ SHALL declare it, and the result SHALL NOT be described as conforming.

## 8. Calibration factor — publish the error

Where an engineering take-off precedes the campaign, the implementer SHALL publish the ratio of
weighed mass to predicted mass, and SHALL carry it forward as a correction to subsequent
estimates.

```
k = P_weighed / P_take-off

Reference campaign:  808.0 t weighed ÷ 692.64 t structural take-off  ⇒  k = 1.167
```

A facility that cannot state its own estimating error cannot produce an auditable material
balance. Publishing `k` is the cheapest available demonstration that an implementer is measuring
rather than asserting.

### 8.1 `k` and `r` are different quantities

A structural take-off and a declared registry figure — lightweight displacement tonnage, a
manufacturer's mass, a customs declaration — are not the same basis, and the ratios computed
against them SHALL NOT be reported under the same symbol.

```
k = P_weighed / P_take-off        take-off = engineer's member-by-member sum
r = P_recovered / P_declared      declared = registry or manufacturer figure
```

> **Requirement 8.2.** An implementer publishing a ratio SHALL state which of `k` or `r` it is,
> and SHALL name the basis of the denominator. An implementer SHALL NOT compute `k` by
> substituting a declared figure for a structural take-off.

`r` and `k` answer different questions. `k` measures **how wrong the engineering was**. `r`
measures **how much of a declared mass actually leaves the site as a given material**. A facility
with an excellent `k` may have a low `r` simply because the registry figure counts machinery,
outfitting and non-ferrous mass that was never in scope.

| Campaign | Ratio | Value | Denominator basis |
|----------|-------|-------|-------------------|
| `P2` | `k` | **1.167** | Sealed structural take-off, 692.64 t |
| `B1` | `r` | **0.753** | Declared LDT, 962.38 t (ferrous recovered 724.695 t) |

These two numbers SHALL NOT be compared with each other. They are published together to make the
distinction concrete. See [reference/b1-campaign.md](reference/b1-campaign.md) for why B1 cannot
yield a `k`.

## 9. Carbon accounting

> **Requirement 9.1.** An emission factor SHALL be established per campaign, and SHALL be
> published together with **the denominator it was computed over**. A factor derived from one
> campaign SHALL NOT be applied to another.

The denominator half of that requirement is the one usually missed, and it is where the larger
error lives. Two campaigns in the publisher's own record illustrate it:

| Campaign | Factor | Denominator | Provenance |
|----------|--------|-------------|------------|
| `P2` | 1.80 tCO₂e/t | Net lot weight, all materials | 107 weighed lots · 808.0 t → 1,454.4 tCO₂e |
| `B1` | 1.50 tCO₂e/t | Recovered ferrous only | 682 t ferrous → 1,023 tCO₂e |

The factors differ by 20 %. But applying P2's factor to B1's *declared lightweight displacement*
of 962 t would report **1,731.6 tCO₂e against the 1,023 actually recorded — a 69 % overstatement**,
on a figure sold as auditable. Most of that error is not the factor; it is the silent
substitution of one denominator for another.

Where no campaign factor exists for an asset, an implementer MAY apply a modelled default, and
SHALL label the result as modelled rather than measured, at the point of display.

Every published factor SHALL carry a stated methodology and an uncertainty band. Carbon results
SHALL be reported with the confidence tier of the underlying lots, and SHALL NOT be reported for
lots below `MEDIUM`.

**A rule that costs the publisher something.** Under 9.1 the publisher cannot state a single
headline carbon number for the company. Every figure is attached to one campaign and one
denominator. That is a worse marketing position and a better evidentiary one, and the trade is
the entire point of the protocol.

## 10. Audit trail

- The record SHALL be append-only: entries may be added and read, never rewritten or deleted.
- Where a value is denormalised for performance, one copy SHALL be designated the source of
  truth, and any inconsistency between copies SHALL block certification until resolved.
- Each lot SHOULD carry a resolvable public identifier permitting a third party to retrieve its
  passport without access to the implementer's systems.

## 11. Conformance levels

An implementer SHALL declare a level. Levels exist so that a yard with a weighbridge and no
software can begin.

| Level | Name | Requirements |
|-------|------|--------------|
| **1** | Measured | Per-load weighing on certified equipment (2.1), evidence layer recorded per load (3), calibration factor published (8). No scoring required. |
| **2** | Scored | Level 1, plus lot compliance score (4) and confidence tier (5) computed, plus the reconciliation rule (7) applied and divergences retained. |
| **3** | Attested | Level 2, plus an append-only trail (10), per-campaign carbon factors (9), and independent third-party attestation of the campaign record. |

The publisher currently operates at **Level 2**, with Level 3 unattained: no independent
attestation of a campaign record has yet been obtained. Its own declarations are published in
[conformance/declarations/](conformance/declarations/) — one Level 2, and one non-conformance.

### 11.1 Declaration scope

A declaration SHALL name its scope. The scope MAY be a whole campaign, or a **named material
stream** within a campaign.

> **Requirement 11.2.** Where a stream-scoped declaration is made, the implementer SHALL also file
> the campaign-scoped result, including a non-conformance, and SHALL NOT present a stream-scoped
> level as though it applied to the campaign.

Without stream scoping, an implementer holding one well-measured stream inside a poorly-measured
campaign has no way to report the part that is sound, and the rational response is to report
nothing. The publisher's own B1 declaration is exactly this case: non-conforming as a campaign,
Level 1 for its ferrous stream.

## 12. Known limits of this version

Read this before citing the protocol.

- The weights in clauses 4 and 6 are **expert-assigned, not empirically derived**. They encode a
  judgement about what matters, and no study yet demonstrates that these particular coefficients
  outperform alternatives.
- `δ = 0.15` is likewise a chosen tolerance.
- The calibration factor `k = 1.167` still comes from **one asset of one type**. Testing it
  against a second campaign (B1, two passenger ferries) did not settle it: that campaign has no
  structural take-off, only a declared LDT, and so yields `r`, not `k`. A second `k` remains the
  single highest-value open contribution — see [CONTRIBUTING.md](CONTRIBUTING.md).
- `r = 0.753` likewise rests on one campaign of one asset type.
- No conformity assessment scheme exists. Nobody can currently certify a Level 3 claim,
  including the publisher.
- The protocol has not been tested against an asset containing significant composite fractions.
  B1 contained non-ferrous and organic streams, but only its ferrous stream was weighed per load;
  the remainder is `E3`.
- Clause 5's confidence tier has not yet been exercised against a campaign whose documents were
  machine-extracted at scale.

These limits are stated because a protocol that hides them is worth less than one that does not.
Each is an invitation: an implementer who tests the weights against their own data, or who
supplies a second calibration factor, materially improves version 0.2.

## 13. Provenance

Two campaigns are published as references.

**P2** — a ship-to-shore gantry crane at a Brazilian port terminal: 808.0 t recovered across 107
weighed loads against a 692.64 t structural take-off, under a cut plan sealed by a registered
engineer. See [reference/p2-campaign.md](reference/p2-campaign.md).

**B1** — two historic passenger ferries, 2020: 724.695 t of ferrous steel weighed across 123
expeditions against a declared LDT of 962.38 t. Added in v0.2 to test clause 8, which it did not
confirm; it produced clause 8.1 instead. See [reference/b1-campaign.md](reference/b1-campaign.md).

The method is documented in three papers co-authored with Prof. Fernanda Baião at PUC-Rio — two
presented at the II Symposium on Decommissioning (CONIDS, UFRJ) on the data-science framework and
on multi-case transferability, and one accepted at SBPO 2026 on physical–financial measurement
and the MRV proposal itself. The campaign-level flow follows Algorithm 1 of that work.
