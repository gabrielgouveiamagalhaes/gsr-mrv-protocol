# Conformance checklist

Copy this file, fill it in, publish it alongside your campaign record. A declaration without a
completed checklist is not a conformance claim.

```
Implementer: ____________________________________
Facility:    ____________________________________
Campaign:    ____________________________________
Asset type:  ____________________________________
Period:      ____________________________________
Level declared:  [ ] 1 Measured   [ ] 2 Scored   [ ] 3 Attested
```

## Level 1 — Measured

| # | Requirement | Clause | Y/N | Evidence |
|---|-------------|--------|-----|----------|
| 1.1 | Mass measured per load leaving site | 2.1 | | |
| 1.2 | Weighbridge holds valid legal-metrology certification | 2.1 | | |
| 1.3 | No load mass derived by dividing a campaign total | 2.1 | | |
| 1.4 | Every load maps to exactly one lot; every lot to one campaign | 2 | | |
| 1.5 | Evidence layer (E1/E2/E3) recorded for every measurement | 3 | | |
| 1.6 | Calibration factor `k` computed and published | 8 | | |

```
k = P_weighed / P_take-off  =  __________ / __________  =  __________
Take-off basis: ______________________  Sealed by registered engineer? [ ] Y [ ] N
Evidence layer distribution:  E1 ____ %   E2 ____ %   E3 ____ %
```

## Level 2 — Scored

| # | Requirement | Clause | Y/N | Evidence |
|---|-------------|--------|-----|----------|
| 2.1 | All Level 1 requirements met | 11 | | |
| 2.2 | Lot compliance score computed for every lot | 4 | | |
| 2.3 | Score is computed, not hand-entered | 4 | | |
| 2.4 | Confidence tier assigned to every lot | 5 | | |
| 2.5 | Gating enforced: no transferable instrument below HIGH | 5.1 | | |
| 2.6 | Gating enforced: no carbon certification below MEDIUM | 5.1 | | |
| 2.7 | Quality gate run before any inference | 6.1 | | |
| 2.8 | Reconciliation against official weight performed | 7 | | |
| 2.9 | δ used (declare if not 0.15) | 7 | | δ = ______ |
| 2.10 | Divergences recorded, routed to review, and retained in the record | 7.1 | | |
| 2.11 | No divergence closed by revising the estimate | 7.1 | | |

```
Lots: ______   Grade distribution: A+ ___  A ___  B ___  C ___  D ___  F ___
Confidence tiers: HIGH ___  MEDIUM ___  LOW ___  UNVERIFIED ___
Divergences raised: ______   resolved: ______   open: ______
```

## Level 3 — Attested

| # | Requirement | Clause | Y/N | Evidence |
|---|-------------|--------|-----|----------|
| 3.1 | All Level 2 requirements met | 11 | | |
| 3.2 | Record is append-only | 10 | | |
| 3.3 | Single source of truth designated for denormalised values | 10 | | |
| 3.4 | Inconsistency between copies blocks certification | 10 | | |
| 3.5 | Emission factor established for this campaign | 9.1 | | |
| 3.6 | Factor published together with its denominator | 9.1 | | |
| 3.7 | No factor imported from another campaign | 9.1 | | |
| 3.8 | Modelled defaults labelled as modelled at point of display | 9 | | |
| 3.9 | Methodology and uncertainty band stated for the factor | 9 | | |
| 3.10 | Independent third-party attestation of the campaign record obtained | 11 | | |

```
Emission factor: ________ tCO₂e/t
Denominator:     ____________________________________
Methodology:     ______________  Uncertainty: ± ____ %
Attested by:     ____________________________________  Date: __________
```

## Declaration

Any requirement answered `N` means the level is **not** met. Partial conformance is reported by
declaring the lower level, not by qualifying the higher one.

```
Signed: ____________________________  Role: ______________  Date: __________
```
