# MRV-P Protocol

**An open protocol for auditable measurement of steel recovered in ship and port dismantling.**

Current version: **0.4 — draft for comment** · [Read the spec →](SPEC.md) · [Versão em português →](SPEC.pt-BR.md)

---

## The problem

In current practice, recoverable steel in dismantling is estimated from lightweight displacement
tonnage or from manufacturer data sheets, and rarely measured. Traceability, circular-economy and
carbon claims are then built on top of that single estimate, and inherit its error.

The Hong Kong Convention entered into force in June 2025 and requires chain of custody and audit
of the physical destination of steel. The EU delegated act for iron and steel under the ESPR is
expected in 2026, with enforcement to follow. Both assume a record-keeping capability that most
facilities do not have.

This protocol specifies that capability, in a form a second party can implement.

## What it specifies

1. **Measure per load, not per campaign** — certified weighbridge, one weighing per vehicle
   movement, never a campaign total divided up.
2. **Record an evidence layer per measurement** — an original ticket, a reconstructed record and
   an estimate are three different things and are weighted `1.00 / 0.60 / 0.30`.
3. **Score each lot on six dimensions** and, separately, carry a **confidence tier** that says
   whether the evidence agrees with itself.
4. **Reconcile against official weight** — divergence beyond `δ = 0.15` goes to review and SHALL
   NOT be closed by adjusting the estimate.
5. **Publish your own estimating error** — the ratio of weighed mass to engineering take-off
   (`k`), kept strictly distinct from the recovery ratio against a declared registry figure (`r`).
6. **Establish carbon factors per campaign, with their denominator** — this is where most
   overstatement actually comes from.

## Conformance levels

| Level | Name | Who it is for |
|-------|------|---------------|
| 1 | **Measured** | Any yard with a certified weighbridge. Start here — no software required. |
| 2 | **Scored** | Facilities running a compliance system. |
| 3 | **Attested** | Level 2 plus independent third-party attestation. |

The publisher operates at **Level 2** on its reference campaign, and files a **non-conformance**
on its second one. Both declarations are published in
[conformance/declarations/](conformance/declarations/). Level 3 is unattained by anyone, including
the publisher, because no conformity assessment scheme exists yet.

## Why it is open

A measurement method that only its author can run is not a measurement method; it is a sales
claim. This protocol is free to implement, cite and adapt with attribution — including by
competitors of the publisher. A standard is worth more to its author adopted than owned.

## Check your own record

The reference checker is standard-library Python with no dependencies, on purpose: a conformance
checker that needs an install is one more reason not to run it.

```bash
python3 tools/check.py schema/examples/P2.json   # -> Level 2 Scored
python3 tools/check.py schema/examples/B1.json   # -> NON-CONFORMING (exit 1)
python3 tools/test_check.py                      # asserts both against the filed declarations
```

Describe your campaign in the shape of [schema/examples/P2.json](schema/examples/P2.json) and run
it. The checker reports every clause, computes `k` or `r` and says which it is, applies the
divergence rule, and determines the level — including, under clause 11.1, the level available to
each individual material stream when the campaign as a whole does not conform.

It exits non-zero on non-conformance, so it can sit in a build.

## Regenerate the PDFs

The Markdown files are canonical. The paginated PDFs are generated from them, so there is no second
copy to drift:

```bash
python3 tools/render.py SPEC.md       build/SPEC_EN.html
python3 tools/render.py SPEC.pt-BR.md build/SPEC_PT.html
# then print each to PDF with a headless browser at A4
```

## How to contribute

The most useful contributions are adversarial. See [CONTRIBUTING.md](CONTRIBUTING.md).

- A **second calibration factor** from a different asset type is the single highest-value
  contribution — it is what turns `k = 1.167` from a hypothesis into a model. The publisher tried
  to supply one from its own second campaign and could not; see
  [reference/b1-campaign.md](reference/b1-campaign.md).
- Evidence that the clause 4 or clause 6 weights are wrong.
- An argument that `δ = 0.15` is the wrong tolerance.
- A conformance report from your own implementation.

## Known limits

The weights are expert-assigned, not empirically derived. `δ` is a chosen tolerance. The
calibration factor `k` still comes from one asset of one type, and the second campaign could not
supply another. No conformity assessment scheme exists, so nobody can certify a Level 3 claim —
including the publisher. See [clause 12](SPEC.md#12-known-limits-of-this-version).

## Licence

[CC BY 4.0](LICENSE). Implement it, fork it, argue with it — keep the attribution.

## Contact

GSR Logística Reversa Naval · [gsrcircular.com](https://gsrcircular.com) · gabriel@goucap.com
