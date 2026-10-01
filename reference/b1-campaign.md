# Reference campaign — B1

The second campaign, added in v0.2. It was brought in to test whether the calibration factor of
clause 8 generalises. **It did not settle that question, and the reason it could not is itself a
specification change** — see clause 8.1.

## Asset

Two historic passenger ferries from the Rio–Niterói crossing, dismantled at the publisher's own
yard between February and October 2020.

| | Vital Brazil | Itapuca |
|---|---|---|
| Builder | Arsenal de Marinha do RJ | EMAQ |
| Year | 1962 | — |
| LOA × beam × depth | 57.0 × 10.6 × 3.7 m | 57.0 × 10.6 × 3.7 m |
| Gross tonnage | 1,006 | 608 |
| **Declared LDT** | **482.38 t** | **480.00 t** |
| Registry | Tribunal Marítimo 05636 DVA-S | Tribunal Marítimo 05637 DVA-I |

Total declared LDT: **962.38 t**.

## Why no calibration factor `k`

Clause 8 defines `k = P_weighed / P_take-off`, where the take-off is a **structural take-off**:
a member-by-member sum produced by an engineer. P2 had one, sealed.

B1 has no structural take-off, and one cannot honestly be reconstructed. The publisher's cut-plan
engine models *prismatic members* — box girders, tubes, trusses, each with a linear mass and a
length. That is a gantry crane. A monocoque steel hull is plate structure with frames; its steel
weight comes from a shipyard weight breakdown, not from a member list. Running the crane model
over a hull would have produced a number, and that number would have been an `E3` estimate
presented in the position where the protocol asks for engineering. Clause 3 exists to forbid
exactly that substitution, including by the publisher.

What B1 has instead is **declared LDT** — a registry figure, not an engineering take-off. Dividing
by it produces a different quantity, and conflating the two is a common field error. Hence
clause 8.1.

## Recovery ratio `r`

| Quantity | Value | Basis |
|----------|-------|-------|
| Declared LDT | 962.38 t | Tribunal Marítimo registration (evidence tier A) |
| Ferrous steel weighed | 724.695 t | Homologated weighbridge, 123 expeditions |
| **`r` = ferrous / LDT** | **0.753** | — |

`r = 0.753` is the first published number quantifying how far a declared LDT sits from recovered
ferrous mass. It is not an error ratio and SHALL NOT be compared with P2's `k = 1.167`. It is
evidence for clause 2: an estimate built on LDT is estimating a different quantity from the one
that leaves the site on a truck.

## A live test of clause 7

The campaign record carries an internal inconsistency, already flagged in the publisher's own
audit notes before this protocol existed:

```
Declared steel mass       681,765 kg   (source document)
Sum of line items         724,695 kg   (authoritative)
Relative difference          +6.30 %
Against δ = 0.15          within tolerance — record, do not escalate
Cause (req. 7.2)          range error: TOTAL summed B1:B118, records run to row 125;
                          the seven omitted expeditions are exactly 42,930 kg
```

This is the reconciliation rule of clause 7 exercised on a campaign it was not designed against,
and it behaves correctly: the difference is recorded and retained, and it does not trigger a
conformance review. It has not been closed by adjusting either figure.

## An open reconciliation, stated because the protocol requires it

The eight material streams sum to **962.00 t** against a declared LDT of **962.38 t** — a
difference of 0.04 %.

| Stream | Mass | Class |
|--------|------|-------|
| Ferrous steel | 724.695 t | weighed, 123 expeditions |
| Equipment | 42.444 t | residual against LDT |
| Wire / copper | 8.489 t | residual against LDT |
| Electric motors | 4.244 t | residual against LDT |
| Bronze | 4.244 t | residual against LDT |
| Valves | 8.489 t | residual against LDT |
| Wood (donated) | 101.865 t | residual against LDT |
| Waste / residue | 67.910 t | residual against LDT |

*Revised in v0.4.* The seven unmeasured streams were previously filed as round figures totalling
280 t. They are a residual against declared LDT, so correcting the ferrous mass rescales all seven
by the same factor: the residual falls from 280 t to 237.685 t. The rule that built them did not
change — only its input did. They were round because they were *sized*, and the revision keeps that
visible: the class column now names what they are instead of describing their typography.

One stream is weighed. The other seven total exactly 237.685 t, which is exactly the declared LDT
less the weighed ferrous mass. That pattern is
consistent with those seven streams having been **sized to close against LDT** rather than
weighed independently.

Under clause 3 they are therefore `E3`, and under clause 2 the campaign total of 962.38 t SHALL NOT
be presented as a measured mass. Only the 724.695 t of ferrous carries per-load weighing.

This is recorded here rather than corrected, because the publisher does not yet have the tickets
to correct it with. It is the clearest available illustration of why the protocol was written.

## Carbon

| Quantity | Value |
|----------|-------|
| Avoided emissions | 1,023 tCO₂e |
| Factor | 1.50 tCO₂e/t |
| **Denominator** | **Recovered ferrous only (682 t)** |
| Uncertainty | ± 10 % |

The denominator is the sound part of this campaign, and it is the reason clause 9.1 requires the
denominator to travel with the factor. Applying P2's 1.80 tCO₂e/t to B1's 962 t of declared LDT
would report 1,731.6 tCO₂e against the 1,023 recorded — a **69 % overstatement**, of which only
20 points come from the factor. The rest is the denominator swap.

## Economics

| Quantity | Value |
|----------|-------|
| Operating revenue | R$ 643,993 |
| Acquisition | R$ 255,000 |
| Opex | R$ 270,744 |
| Operating result | R$ 118,249 |
| Operating margin | 18.4 % |
| Diversion from landfill | 91.7 % |

Note the contrast with P2's ≈ 46 % direct operating margin. Two campaigns, two asset types, two
very different economics — which is a further argument against any single headline figure for a
facility, of margin or of carbon.
