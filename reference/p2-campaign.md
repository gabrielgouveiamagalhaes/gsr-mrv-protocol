# Reference campaign — P2

The campaign the protocol was derived from, described so that an implementer can judge how far it
generalises. It is one asset of one type; clause 12 states the consequence.

## Asset

Ship-to-shore gantry crane (portainer), dismantled and removed at a Brazilian port terminal.

## Measurement

| Quantity | Value | Basis |
|----------|-------|-------|
| Structural take-off | 692.64 t | Cut plan sealed by an engineer registered with CREA-RJ |
| Weighed mass | 808.0 t | Certified weighbridge |
| Loads | 107 | One weighing per vehicle movement |
| Calibration factor `k` | **1.167** | 808.0 / 692.64 |

The 1.167 divergence between engineering prediction and physical reality was not absorbed. It was
measured, written into the estimating model, and is carried forward as a known correction. Clause
8 exists because of it.

## Cut plan

The cut plan's binding constraint was **transport**, not cutting capacity, at an acceptance of
192.04 t and 88.7 % utilisation. An implementer whose binding constraint is different should
expect a different calibration factor, which is precisely why clause 8 asks for the ratio rather
than for the publisher's number.

## Evidence quality — stated plainly

The campaign's weighing records are **not uniformly E1**. A portion of the physical tickets from
the later period of the campaign is no longer retained, and those records are `E2` —
reconstructed from a primary source. This is the reason clause 3 defines E2 at all, rather than
offering a binary measured/estimated distinction that would have forced the publisher either to
overstate or to discard real data.

Total weighed mass of 808.0 t under official weighing is the claim the publisher makes. A
per-ticket count is deliberately not asserted.

## Carbon

| Quantity | Value |
|----------|-------|
| Avoided emissions | 1,454.4 tCO₂e |
| Factor | 1.80 tCO₂e/t |
| Denominator | Net lot weight, all materials |
| Methodology | `gs_vm0041` |
| Uncertainty | ± 10 % |

This factor is evidence about **this campaign**. Clause 9.1 forbids applying it to another, and
the B1 comparison in that clause shows what happens when the denominator is also swapped: a 69 %
overstatement.

## Economics

| Quantity | Value |
|----------|-------|
| Revenue | R$ 1,768,931 |
| Direct cost | R$ 956,000 |
| Direct operating margin | ≈ 46 % |
| Execution | 30 days against a six-month reference schedule |

Note for readers of the associated papers: the SBPO 2026 paper reports a **segregation premium**
of R$ 556,931 (+45.9 %) measured against a counterfactual of undifferentiated scrap pricing. That
is a different computation from the operating margin above, which happens to land at a similar
percentage. The two SHALL NOT be conflated.
