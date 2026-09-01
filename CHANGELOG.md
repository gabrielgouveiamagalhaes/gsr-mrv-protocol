# Changelog

All notable changes to the MRV-P Protocol are recorded here, with the rationale for each.

## [0.2] — 2026-09-01

Testing the protocol against a second campaign changed the specification. That is the intended
mechanism, and this entry records it working.

### Added
- **Clause 8.1** — `k` (weighed ÷ structural take-off) and `r` (recovered ÷ declared registry
  figure) are distinct quantities and SHALL NOT be reported under the same symbol.
  **Requirement 8.2** forbids computing `k` by substituting a declared figure for a take-off.
- Second reference campaign: [reference/b1-campaign.md](reference/b1-campaign.md) — two passenger
  ferries, 681.765 t of ferrous weighed across 123 expeditions against 962.38 t declared LDT.
- First published `r` = **0.708**.

### Why
B1 was brought in to supply a second calibration factor and test whether `k = 1.167` generalises.
It could not: the campaign has no structural take-off, only a declared LDT. The publisher's
cut-plan engine models prismatic members and cannot honestly produce a take-off for a monocoque
hull; running it anyway would have produced an `E3` estimate occupying the position where the
protocol asks for engineering — the exact substitution clause 3 exists to forbid. The failure to
produce a number was more informative than a number would have been.

B1 also exercised clause 7 on a campaign it was not designed against: an internal steel
inconsistency of **+6.30 %** sits within `δ = 0.15`, is recorded, and correctly does not escalate.

### Changed
- Clause 12 now states that a second `k` remains open, and that `r = 0.708` also rests on a single
  asset type.
- Clause 13 lists both campaigns.

### Still open
- A second `k`, from any asset with an engineering take-off, remains the highest-value
  contribution to this specification.
- B1's non-ferrous, organic and residue streams are round figures summing to exactly the declared
  LDT less the weighed ferrous mass. Under clause 3 they are `E3`, and B1's 962 t total SHALL NOT
  be presented as measured. Recorded rather than corrected: the tickets to correct it do not exist.

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
