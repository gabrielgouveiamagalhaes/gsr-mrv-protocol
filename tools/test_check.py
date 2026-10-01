#!/usr/bin/env python3
"""Tests for the reference checker.

These assert that the checker reproduces the publisher's own filed declarations
in conformance/declarations/. If a specification change makes one of these fail,
either the declaration or the change is wrong — that is the point.

    python3 tools/test_check.py
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check import evaluate, stream_level  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAILS = []


def load(name):
    with open(os.path.join(ROOT, "schema", "examples", f"{name}.json")) as fh:
        return json.load(fh)


def expect(label, got, want):
    ok = got == want
    print(f"  [{'ok  ' if ok else 'FAIL'}] {label}: {got!r}" + ("" if ok else f" (expected {want!r})"))
    if not ok:
        FAILS.append(label)


def test_p2():
    print("P2 — must reproduce conformance/declarations/P2.md")
    rec = load("P2")
    r, level, (kind, val, _), measured, unmeasured = evaluate(rec)
    expect("campaign level", level, 2)
    expect("ratio kind", kind, "k")
    expect("k value (3dp)", round(val, 3), 1.167)
    expect("all streams measured", len(unmeasured), 0)
    expect("no failing clauses", sorted(r.failed), [])
    # Level 3 is blocked by attestation alone
    rec3 = json.loads(json.dumps(rec))
    rec3["attestation"]["independent_third_party"] = True
    _, level3, _, _, _ = evaluate(rec3)
    expect("level 3 once attested", level3, 3)


def test_b1():
    print("\nB1 — must reproduce conformance/declarations/B1.md")
    rec = load("B1")
    r, level, (kind, val, _), measured, unmeasured = evaluate(rec)
    expect("campaign level", level, 0)
    expect("ratio kind", kind, "r")
    expect("r value (3dp)", round(val, 3), 0.753)
    expect("2.1 fails", "2.1" in r.failed, True)
    expect("2.1b closure detected", "2.1b" in r.failed, True)
    expect("unmeasured stream count", len(unmeasured), 7)
    ferrous = [s for s in measured if s["material"] == "steel_ferrous"][0]
    expect("ferrous stream level", stream_level(rec, ferrous), 1)


def test_delta_guard():
    print("\nGuard — a looser delta must not be reported as conforming")
    rec = load("P2")
    rec["reconciliation"]["delta"] = 0.25
    r, level, _, _, _ = evaluate(rec)
    expect("7b fails on loose delta", "7b" in r.failed, True)
    expect("level drops below 2", level < 2, True)


def test_unexplained_difference_guard():
    print("\nGuard — requirement 7.2: a difference with no cause is non-conforming")
    # Era exatamente este o estado do B1 em v0.3: +6,30% dentro de delta, com
    # PASS na clausula 7, e nenhuma clausula pedindo a causa. Era erro de
    # intervalo de planilha, com resposta exata.
    rec = load("B1")
    assert rec["reconciliation"]["checks"][0].get("cause"), "B1 deve trazer a causa"
    del rec["reconciliation"]["checks"][0]["cause"]
    r, level, _, _, _ = evaluate(rec)
    expect("7.2 fails with no cause", "7.2" in r.failed, True)

    print("  — and an explicit 'unexplained' marker is permitted")
    rec["reconciliation"]["checks"][0]["unexplained"] = True
    r, _, _, _, _ = evaluate(rec)
    expect("7.2 passes when explicitly unexplained", "7.2" in r.failed, False)

    print("  — a difference INSIDE delta is not excused from explanation")
    rec = load("B1")
    chk = rec["reconciliation"]["checks"][0]
    del chk["cause"]
    chk["expected_t"], chk["observed_t"] = 100.0, 100.5   # e_rel = +0,005, muito dentro de delta
    r, _, _, _, _ = evaluate(rec)
    expect("7.1 passes (within tolerance)", "7.1" in r.failed, False)
    expect("7.2 still fails (no cause)", "7.2" in r.failed, True)


def test_imported_factor():
    print("\nGuard — an imported carbon factor must fail clause 9.1b")
    rec = load("P2")
    rec["carbon"]["imported_from_other_campaign"] = True
    r, level, _, _, _ = evaluate(rec)
    expect("9.1b fails", "9.1b" in r.failed, True)
    expect("level capped at 2", level, 2)  # 9.1b only gates Level 3


if __name__ == "__main__":
    test_p2()
    test_b1()
    test_delta_guard()
    test_unexplained_difference_guard()
    test_imported_factor()
    print()
    if FAILS:
        print(f"{len(FAILS)} failing assertion(s): {', '.join(FAILS)}")
        sys.exit(1)
    print("all assertions passed")
