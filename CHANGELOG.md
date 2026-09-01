# Changelog

All notable changes to the MRV-P Protocol are recorded here, with the rationale for each.

## [0.1] — 2026-09-01

First public draft, for comment.

### Specified
- Per-load measurement as the unit of record (clause 2), replacing aggregate estimation from LDT
  or manufacturer data sheets.
- Evidence layers `E1` / `E2` / `E3` at weights `1.00` / `0.60` / `0.30` (clause 3).
- Six-dimension lot compliance score and grade bands (clause 4).
- Confidence tier as a dimension independent of score, with gating rules for transferable
  instruments and carbon certification (clause 5).
- Five-step campaign governance flow, with the quality gate and reconciliation mandatory for
  conformance (clause 6).
- The divergence rule at `δ = 0.15`, and the prohibition on resolving divergence by revising the
  estimate (clause 7).
- Publication of the calibration factor `k` (clause 8).
- Per-campaign emission factors published with their denominator (clause 9).
- Append-only audit trail requirements (clause 10).
- Three conformance levels (clause 11).

### Notes on provenance
Clauses 4, 5 and 10 codify behaviour already implemented in the publisher's production system.
Clauses 6 and 7 follow Algorithm 1 of the MRV-P governance flow documented at PUC-Rio.
Clause 9 was written after an internal review found that applying one campaign's emission factor
across a different denominator overstated a result by 69 %.

### Open
- No conformity assessment scheme. Level 3 is unattainable by anyone at this version.
- Weights and `δ` are expert-assigned; no empirical study yet supports them over alternatives.
- One calibration factor, from one asset type.
