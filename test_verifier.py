"""Verifier hand-off: every figure in the number has a source. Run: python3 test_verifier.py"""
import os
for k in ("GEMINI_API_KEY", "VERTEX_PROJECT"): os.environ.pop(k, None)  # rule parser, no network
import server


def demo():
    server.state.clear(); server.state.update(server.copy.deepcopy(server.SEED)); server.docs.clear()
    for f in sorted(os.listdir(os.path.join(server.HERE, "demo"))):
        server.add_doc(f, "text/plain", open(os.path.join(server.HERE, "demo", f), "rb").read())
    for e in server.DEMO_LOG:
        server.add_log(server.state["plants"][server.YOU], e)
    return server.audit(2027)


def test_every_figure_has_a_source():
    a = demo()
    kinds = [r["kind"] for r in a["rows"]]
    assert kinds.count("fuel") == 3 and kinds.count("steel") == 6 and kinds.count("output") == 1
    assert all(r["sources"] and all(s["file"] for s in r["sources"]) for r in a["rows"])


def test_rows_add_up_to_the_number():
    a = demo()
    total = sum(r["tco2"] for r in a["rows"] if r["tco2"] is not None)
    out = next(r for r in a["rows"] if r["kind"] == "output")["item"].split()[1]
    assert abs(total / float(out) - a["summary"]["see_total"]) < 0.002


def test_heat_shows_certificate_and_invoice():
    a = demo()
    row = next(r for r in a["rows"] if "KIS-H88457" in r["item"])
    files = {s["file"]: s for s in row["sources"]}
    assert set(files) == {"mtc_6.txt", "steel_invoice_1.txt"}
    assert {s["role"] for s in row["sources"]} == {"tonnes", "mill"} and all(s["doc"] for s in row["sources"])


def test_log_rows_name_the_month_and_have_no_file_link():
    a = demo()
    row = next(r for r in a["rows"] if r["kind"] == "fuel" and "lpg" in r["item"])
    assert row["sources"][0]["file"].startswith("monthly log 2026-0") and row["sources"][0]["doc"] is None
    assert "opening" in row["sources"][0]["quote"]


def test_open_gaps_travel_with_the_pack():
    a = demo()
    assert any("diesel: only purchase invoices" in g for g in a["plan"]["gaps"])
    assert a["summary"]["name"] and a["summary"]["year"] == 2027 and a["method"]


def test_csv_matches_rows():
    a = demo()
    csv = server.export_csv(2027)
    for r in a["rows"]:
        assert r["item"] in csv
    assert "mtc_6.txt + steel_invoice_1.txt" in csv or "steel_invoice_1.txt + mtc_6.txt" in csv


def test_empty_plant():
    server.state.clear(); server.state.update(server.copy.deepcopy(server.SEED))
    assert server.audit(2027) == {"empty": True}


if __name__ == "__main__":
    for n, f in list(globals().items()):
        if n.startswith("test_"): f()
    print("ok")
