#!/usr/bin/env python3
"""Reference conformance checker for the MRV-P Protocol.

Reads a campaign record (JSON) and reports, clause by clause, which requirements
are met and which conformance level the record supports — at campaign scope and,
under clause 11.1, at the scope of each material stream.

Standard library only. No dependencies, on purpose: a conformance checker that
needs an install is one more reason not to run it.

    python3 tools/check.py schema/examples/P2.json
"""
import json
import sys

E_LAYERS = ("E1", "E2", "E3")
E_WEIGHT = {"E1": 1.00, "E2": 0.60, "E3": 0.30}
TOL = 0.01  # tonnes, for float comparison of declared vs summed mass


class Result:
    def __init__(self):
        self.rows = []          # (clause, requirement, ok|None, note)
        self.failed = set()

    def check(self, clause, req, ok, note=""):
        self.rows.append((clause, req, ok, note))
        if ok is False:
            self.failed.add(clause)
        return ok

    def na(self, clause, req, note=""):
        self.rows.append((clause, req, None, note))


def stream_evidence_ok(s):
    ev = s.get("evidence") or {}
    if not ev:
        return False, "no evidence layers recorded"
    unknown = [k for k in ev if k not in E_LAYERS]
    if unknown:
        return False, f"unknown evidence layer(s): {', '.join(unknown)}"
    total = sum(ev.values())
    if abs(total - s["mass_t"]) > TOL:
        return False, f"layers sum to {total:g} t, mass is {s['mass_t']:g} t"
    return True, ""


def stream_is_measured(s):
    """Clause 2.1 — per-load weighing on certified equipment."""
    return s.get("measurement") == "per_load" and bool(s.get("weighbridge_certified"))


def evaluate(rec):
    r = Result()
    streams = rec.get("streams", [])
    measured = [s for s in streams if stream_is_measured(s)]
    unmeasured = [s for s in streams if not stream_is_measured(s)]

    # ---- clause 2 ----------------------------------------------------------
    r.check("2.1", "Mass measured per load on certified weighbridge (all streams)",
            len(streams) > 0 and not unmeasured,
            "" if not unmeasured else
            "not per-load: " + ", ".join(s["material"] for s in unmeasured))

    # closing against a declared aggregate (clause 2.1 / 1.3)
    declared = rec.get("declared")
    if declared and declared.get("mass_t"):
        total = sum(s["mass_t"] for s in streams)
        gap = declared["mass_t"] - sum(s["mass_t"] for s in measured)
        est = sum(s["mass_t"] for s in unmeasured)
        closes = abs(total - declared["mass_t"]) <= 1.0 and est > 0 and abs(est - gap) <= 1.0
        r.check("2.1b", "Unmeasured streams not sized to close against the declared figure",
                not closes,
                f"streams total {total:g} t vs declared {declared['mass_t']:g} t; "
                f"unmeasured {est:g} t = declared minus measured ({gap:.2f} t)" if closes else "")
    else:
        r.na("2.1b", "Closure against a declared figure", "no declared figure in record")

    # ---- clause 3 ----------------------------------------------------------
    ev_ok, ev_notes = True, []
    for s in streams:
        ok, note = stream_evidence_ok(s)
        if not ok:
            ev_ok = False
            ev_notes.append(f"{s['material']}: {note}")
    r.check("3", "Evidence layer recorded for every measurement", ev_ok, "; ".join(ev_notes))

    # ---- clause 8 / 8.1 / 8.2 ---------------------------------------------
    takeoff = rec.get("takeoff")
    ratio_kind, ratio_val, ratio_basis = None, None, None
    if takeoff and takeoff.get("basis") == "structural" and takeoff.get("mass_t"):
        measured_t = sum(s["mass_t"] for s in measured)
        ratio_kind, ratio_val = "k", measured_t / takeoff["mass_t"]
        ratio_basis = f"structural take-off, {takeoff['mass_t']:g} t"
        r.check("8", "Calibration factor k computed against a structural take-off", True,
                f"k = {ratio_val:.3f}")
        r.check("8.2", "Take-off sealed by a registered engineer",
                bool(takeoff.get("sealed_by_registered_engineer")))
    elif declared and declared.get("mass_t"):
        measured_t = sum(s["mass_t"] for s in measured)
        ratio_kind, ratio_val = "r", measured_t / declared["mass_t"]
        ratio_basis = f"declared {declared.get('basis','?').upper()}, {declared['mass_t']:g} t"
        r.na("8", "Calibration factor k",
             "no structural take-off; clause 8.1 applies — r, not k")
        r.check("8.2", "Ratio published as r, with denominator basis named",
                bool(declared.get("basis")), f"r = {ratio_val:.3f} against {ratio_basis}")
    else:
        r.na("8", "Ratio", "neither a take-off nor a declared figure in record")

    # ---- clause 7 ----------------------------------------------------------
    rc = rec.get("reconciliation") or {}
    delta = rc.get("delta")
    r.check("7", "Reconciliation tolerance declared", delta is not None,
            f"delta = {delta}" if delta is not None else "")
    if delta is not None and delta > 0.15:
        r.check("7b", "Tolerance not looser than 0.15", False,
                f"delta = {delta} is looser than the protocol value; result is not conforming")
    divergences = []
    for c in rc.get("checks", []):
        exp, obs = c["expected_t"], c["observed_t"]
        e_rel = abs(obs - exp) / max(exp, 0.1)
        flag = e_rel > (delta or 0.15)
        divergences.append((c.get("label", "?"), e_rel, flag))
    for label, e_rel, flag in divergences:
        r.check("7.1", f"Reconciliation: {label}", not flag,
                f"e_rel = {e_rel:+.4f} -> " + ("DIVERGENCE, conformance review" if flag
                                               else "within tolerance, recorded"))
    sc = rec.get("scoring") or {}
    r.check("7.1b", "Divergences retained and no estimate revised to match weight",
            bool(sc.get("divergences_retained")) and bool(sc.get("no_estimate_revision")))

    # ---- clauses 4, 5, 6 ---------------------------------------------------
    r.check("4", "Lot compliance score computed for every lot", bool(sc.get("lot_scores_computed")))
    r.check("4b", "Score computed, not hand-entered", bool(sc.get("computed_not_entered")))
    r.check("5", "Confidence tier assigned", bool(sc.get("confidence_tiers")))
    r.check("5.1", "Gating enforced (HIGH for instruments, MEDIUM for carbon)",
            bool(sc.get("gating_enforced")))
    r.check("6.1", "Quality gate run before inference", bool(sc.get("quality_gate")))

    # ---- clause 9 ----------------------------------------------------------
    cb = rec.get("carbon") or {}
    if cb.get("factor_tco2e_per_t") is not None:
        r.check("9.1", "Emission factor published with its denominator",
                bool(cb.get("denominator")))
        r.check("9.1b", "Factor not imported from another campaign",
                not cb.get("imported_from_other_campaign"))
        r.check("9", "Methodology and uncertainty band stated",
                bool(cb.get("methodology")) and cb.get("uncertainty_pct") is not None)
    else:
        r.na("9", "Carbon accounting", "no factor in record")

    # ---- clause 10 ---------------------------------------------------------
    au = rec.get("audit") or {}
    r.check("10", "Record is append-only", bool(au.get("append_only")))
    r.check("10b", "Single source of truth designated", bool(au.get("single_source_of_truth")))
    r.check("10c", "Inconsistency blocks certification",
            bool(au.get("inconsistency_blocks_certification")))

    # ---- clause 11 — level -------------------------------------------------
    L1 = {"2.1", "2.1b", "3", "8.2"}
    L2 = L1 | {"4", "4b", "5", "5.1", "6.1", "7", "7.1", "7.1b", "7b"}
    L3 = L2 | {"9", "9.1", "9.1b", "10", "10b", "10c"}

    level = 0
    if not (r.failed & L1):
        level = 1
        if not (r.failed & L2):
            level = 2
            if not (r.failed & L3) and rec.get("attestation", {}).get("independent_third_party"):
                level = 3
    return r, level, (ratio_kind, ratio_val, ratio_basis), measured, unmeasured


def stream_level(rec, s):
    """Clause 11.1 — level achievable for one named stream."""
    sub = dict(rec)
    sub["streams"] = [s]
    _, lvl, _, _, _ = evaluate(sub)
    return lvl


def main(path):
    rec = json.load(open(path))
    r, level, (kind, val, basis), measured, unmeasured = evaluate(rec)
    c = rec["campaign"]

    print(f"\nMRV-P conformance check — protocol {rec.get('protocol_version','?')}")
    print(f"Campaign {c['id']} · {c.get('label','')}")
    print(f"Asset type: {c.get('asset_type','?')} · {c.get('period','?')}\n")

    w = max(len(x[1]) for x in r.rows) + 2
    for clause, req, ok, note in r.rows:
        mark = "PASS" if ok else ("FAIL" if ok is False else " n/a")
        print(f"  [{mark}] {clause:<6} {req:<{w}}{note}")

    if kind:
        print(f"\n  Ratio: {kind} = {val:.3f}  ({basis})")
        if kind == "r":
            print("         clause 8.1 — r is NOT k and SHALL NOT be compared with one")

    print(f"\n  Campaign-scope level: ", end="")
    print(f"{level} " + ["NON-CONFORMING", "Measured", "Scored", "Attested"][level])

    if level == 0 and measured:
        print("\n  Clause 11.1 — stream-scoped declarations available:")
        for s in measured:
            lvl = stream_level(rec, s)
            if lvl > 0:
                print(f"    {s['material']:<18} {s['mass_t']:>10.3f} t   Level {lvl}")
        if unmeasured:
            print("    not declarable: " + ", ".join(s["material"] for s in unmeasured))
    print()
    return 0 if level > 0 else 1


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
