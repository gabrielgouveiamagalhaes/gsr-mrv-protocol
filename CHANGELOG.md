# Changelog

All notable changes to the MRV-P Protocol are recorded here, with the rationale for each.

## [0.4] — 2026-10-01

A tolerance that excuses investigation converts a bug into a conformance. The publisher's own
declaration proved it.

### Added
- **Requirement 7.2:** every reconciliation check SHALL carry the cause of its difference, or SHALL
  be marked explicitly as unexplained. A difference within `δ` is **not** excused from explanation.
  Enforced by the reference checker; guarded by `test_unexplained_difference_guard`.

### Changed
- **B1 reference data corrected.** The ferrous stream moves from 681.765 t to **724.695 t**, and the
  seven residual streams from a round 280 t to **237.685 t**. The ratio moves from `r = 0.708` to
  **`r = 0.753`**. `schema/examples/B1.json` and `conformance/declarations/B1.md` both updated.

### Why
For three filings, B1's steel reconciliation showed +6.30% — comfortably inside `δ = 0.15` — and
clause 7 passed it. Correctly, under v0.3: `δ` is the threshold at which a difference becomes a
divergence requiring review, and 6.3% was below it.

The cause turned out to be arithmetic and exact. The source spreadsheet's TOTAL cell summed
`B1:B118` while the load records ran to row 125; the seven omitted expeditions (2020-09-30 to
2020-10-08) are exactly 42,930 kg. The traceability matrix had carried it for months as a "physical ε
of +6.3%" — a label, not an explanation — and no clause obliged anyone to ask why.

So the specification was answering only half the question. `δ` decides when a difference becomes a
*divergence requiring review*. It was never meant to decide whether a difference deserves an
*explanation*. v0.4 separates the two.

The correction propagates in the direction that costs the publisher something: with the ferrous mass
right, the seven residual streams close against declared LDT **exactly** (962.38 − 724.695 =
237.685) instead of approximately, so the campaign's non-conformance under clause 2.1 is now more
evident than it was. That is the correct direction for a correction to move.

### Known limit this exposes
Requirement 7.2 obliges an explanation or an explicit admission of its absence. It does not and
cannot adjudicate whether a stated cause is *true*. A false cause passes 7.2 and is a matter for
audit, not for a checker.

## [0.3] — 2026-09-01

Filing the publisher's own conformance declarations changed the specification. Again.

### Added
- **Clause 11.1 — declaration scope**, and **Requirement 11.2**: a declaration may be scoped to a
  named material stream, provided the campaign-scoped result is also filed, including a
  non-conformance.
- The publisher's own declarations: [P2](conformance/declarations/P2.md) — Level 2, and
  [B1](conformance/declarations/B1.md) — **non-conforming**, with its ferrous stream at Level 1.

### Why
Filling in the checklist for B1 produced a failure with no way to report it usefully. The campaign
fails 2.1 because seven of eight material streams were sized against declared LDT rather than
weighed. But one stream — 681.765 t of ferrous across 123 expeditions — fully satisfies Level 1.
Without stream scoping, the honest options were to declare nothing or to overstate, and a protocol
that leaves those as the only two choices will be ignored.

### Translated
- [`SPEC.pt-BR.md`](SPEC.pt-BR.md) — normative Portuguese version, using the ABNT/ISO modal
  convention (DEVE / NÃO DEVE / CONVÉM QUE / PODE) rather than a literal rendering of
  SHALL/SHOULD/MAY. Brazil is where the yards, the mills and the regulator are; a protocol that
  reaches an implementer only in English cannot be filed by most of the parties able to file it.
  The English version prevails on divergence until one is designated canonical.

### Tooling
- [`tools/check.py`](tools/check.py) — dependency-free reference checker. Reads a campaign record,
  reports every clause, computes `k` or `r` and names which, applies the divergence rule, and
  determines campaign-scope and stream-scope levels. Exits non-zero on non-conformance.
- [`tools/test_check.py`](tools/test_check.py) — asserts that the checker independently reproduces
  both filed declarations (P2 → Level 2, B1 → non-conforming with its ferrous stream at Level 1),
  and that a loosened `δ` and an imported carbon factor are both caught.
- Machine-readable records for both campaigns in [`schema/examples/`](schema/examples/).

The checker was written after the declarations, and reproduced them without adjustment. It also
detected the LDT-closure pattern in B1 on its own: unmeasured streams of 280 t against a declared
figure less measured mass of 280.62 t.

### Note
P2's declaration records an evidence distribution of E1 56.8 % / E2 43.2 %, and fails Level 3 on
requirement 3.10 alone — no independent attestation — with the other nine met. It is declared at
Level 2, because partial conformance is reported by declaring the lower level.

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
