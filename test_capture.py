"""Monthly capture log and monitoring plan draft. Run: python3 test_capture.py"""
import os
for k in ("GEMINI_API_KEY", "VERTEX_PROJECT"): os.environ.pop(k, None)  # rule parser, no network
import server
from calc import compute

doc = lambda *lines: "\n".join(lines).encode()
LPG = lambda month, o, b, c, **kw: {"kind": "fuel", "month": month, "fuel": "lpg", "unit": "t",
                                    "opening": o, "purchased": b, "closing": c, **kw}


def reset():
    server.state.clear(); server.state.update(server.copy.deepcopy(server.SEED)); server.docs.clear()
    p = server.state["plants"][server.YOU]
    server.add_doc("lpg.txt", "text/plain", doc("Document: fuel_invoice", "Fuel: LPG", "Quantity: 30 t"))
    server.add_doc("diesel.txt", "text/plain", doc("Document: fuel_invoice", "Fuel: Diesel", "Quantity: 1000 litre"))
    server.add_doc("prod.txt", "text/plain", doc("Document: production", "Output (t): 100"))
    return p


def fuel_lines(p):
    r = compute(server.effective(p), server.state["suppliers"])
    return sorted((l["fuel"], l["qty"]) for l in r["direct_lines"])


def test_logged_use_beats_purchases():
    p = reset()
    assert fuel_lines(p) == [("diesel", 1000), ("lpg", 30)]
    server.add_log(p, LPG("2026-04", 6, 30, 8))  # used 28, not the 30 bought
    assert fuel_lines(p) == [("diesel", 1000), ("lpg", 28)]  # diesel has no log, invoice still counts
    assert server.log_checks(p) == []


def test_same_month_replaces():
    p = reset()
    server.add_log(p, LPG("2026-04", 6, 30, 8)); server.add_log(p, LPG("2026-04", 6, 30, 10))
    assert fuel_lines(p) == [("diesel", 1000), ("lpg", 26)]


def test_bad_entries_rejected():
    p = reset()
    for bad in (LPG("2026-13", 1, 1, 1), LPG("April", 1, 1, 1), LPG("2026-04", 1, 1, 5),
                LPG("2026-04", -1, 5, 1), {**LPG("2026-04", 1, 1, 1), "fuel": "coal"},
                {**LPG("2026-04", 1, 1, 1), "unit": "gallon"}, {"kind": "production", "month": "2026-04", "output_t": "x"}):
        try: server.add_log(p, bad); assert False, bad
        except ValueError: pass
    assert p["log"] == []


def test_stock_break_and_purchase_mismatch_flagged():
    p = reset()
    server.add_log(p, LPG("2026-04", 6, 30, 8)); server.add_log(p, LPG("2026-05", 9, 5, 4))
    checks = server.log_checks(p)
    assert len(checks) == 2 and "2026-05" in checks[0] and "invoices" in checks[1]  # opening 9 != closing 8; 35 logged vs 30 invoiced
    assert fuel_lines(p) == [("diesel", 1000), ("lpg", 30)]  # log and invoices disagree, so invoices stay


def test_partial_log_never_lowers_the_number():
    p = reset()
    server.add_log(p, {"kind": "fuel", "month": "2026-06", "fuel": "diesel", "unit": "litre",
                       "opening": 100, "purchased": 50, "closing": 40})  # one month against a year of invoices
    assert fuel_lines(p) == [("diesel", 1000), ("lpg", 30)]


def test_full_year_production_log_beats_dispatch_record():
    p = reset()
    server.add_log(p, {"kind": "production", "month": "2026-04", "output_t": 40})
    server.add_log(p, {"kind": "production", "month": "2026-05", "output_t": 45})
    out = lambda: compute(server.effective(p), server.state["suppliers"])["output_t"]
    assert out() == 100  # 2 of 12 months: the dispatch record stays
    for m in range(6, 16):
        server.add_log(p, {"kind": "production", "month": f"{2026 + (m - 1) // 12}-{(m - 1) % 12 + 1:02d}", "output_t": 10})
    assert out() == 185  # 12 months logged: the log wins


def test_plan_lists_gaps_and_closes_them():
    p = reset()
    gaps = " | ".join(server.plan(p)["gaps"])
    assert "lpg: only purchase invoices" in gaps and "diesel: only purchase invoices" in gaps and "Output" in gaps
    server.add_log(p, LPG("2026-04", 6, 30, 8, meter="Weighbridge WB-2, calibrated 2026-01"))
    plan = server.plan(p)
    gaps = " | ".join(plan["gaps"])
    assert "lpg: only purchase invoices" not in gaps and "lpg: 1 of 12 months" in gaps and "lpg: no meter" not in gaps
    assert any("Weighbridge WB-2" in l for l in plan["lines"])


if __name__ == "__main__":
    for n, f in list(globals().items()):
        if n.startswith("test_"): f()
    print("ok")
