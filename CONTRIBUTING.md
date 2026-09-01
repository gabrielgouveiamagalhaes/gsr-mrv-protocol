# Contributing to the MRV-P Protocol

This protocol improves by being attacked, not by being agreed with. The contributions listed
first are the ones most likely to change the specification.

## What is most useful

### 1. A second calibration factor

Clause 8 publishes `k = 1.167` from one ship-to-shore gantry crane. One asset of one type is a
hypothesis. If you run a campaign with an engineering take-off and per-load weighing, the ratio
you obtain is the most valuable thing you can send, whatever it turns out to be — including a
value that contradicts ours.

Open an issue titled `calibration: <asset type>` with: asset type, take-off mass and its basis,
weighed mass, number of loads, evidence layer distribution, and whether the take-off was sealed
by a registered engineer.

### 2. Evidence that the weights are wrong

The weights in clauses 4 and 6 encode a judgement, not a finding. If you have data suggesting a
different set predicts audit outcomes better, that is a specification change, not a comment.

### 3. An argument about δ

`δ = 0.15` is a chosen tolerance. A reasoned case for a different threshold — or for making it a
function of campaign size or asset type — is in scope.

### 4. A conformance report

Implement at any level and report what broke. Ambiguities in the text that forced you to guess
are defects in the text.

## What the protocol will not accept

- Changes that make conformance easier to claim without making measurement better.
- Removal of clause 12. The limits stay.
- A weakening of Requirement 7.1. Closing a divergence by adjusting the estimate to match the
  weight is the specific failure this protocol exists to prevent.

## Process

Version 0.x is a draft. Substantive changes are collected and released together with a rationale
in [CHANGELOG.md](CHANGELOG.md). Every accepted change names its contributor.

Comments to `gabriel@goucap.com` until an issue tracker is public.
