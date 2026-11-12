"""Review and correct: values count only after the clerk confirms them. Run: python3 test_review.py"""
import base64, os
for k in ("GEMINI_API_KEY", "VERTEX_PROJECT"): os.environ.pop(k, None)  # rule parser, no network
import server

call = lambda method, path, query=None, body=None: server.dispatch(method, path, query or {}, body)
b64 = lambda s: base64.b64encode(s.encode()).decode()
FUEL = lambda qty: f"Document: fuel_invoice\nFuel: LPG\nQuantity: {qty} t"


def reset():
    assert call("POST", "/api/reset")[0] == 200


def up(name, text):
    code, data, _, _ = call("POST", "/api/upload", body={"filename": name, "mime": "text/plain", "data": b64(text)})
    assert code == 200, data
    return data


def docs():
    return call("GET", "/api/docs")[1]


def by_name(name):
    return next(d for d in docs() if d["name"] == name)


def review_item():
    return next(i for i in call("GET", "/api/readiness")[1]["items"] if i["key"] == "review")


def items(year="2027"):
    return [r["item"] for r in call("GET", "/api/audit", {"year": year})[1]["rows"]]


def test_upload_waits_for_review():
    reset()
    r = up("f.txt", FUEL(5))
    d = by_name("f.txt")
    assert r["doc"] == d["id"] and d["reviewed"] is False and d["record"]["quantity"] == 5 and d["edits"] == []
    assert not review_item()["done"] and "1 of 1" in review_item()["hint"]


def test_confirming_changes_no_numbers_and_unlocks_the_report():
    reset()
    call("POST", "/api/demo")
    before = call("GET", "/api/state", {"year": "2027"})[1]["plants"][0]["see_total"]
    assert call("GET", "/api/report", {"year": "2027"})[0] == 409  # documents are in, but nothing is confirmed
    one = docs()[0]["id"]
    assert call("POST", "/api/review", body={"doc": one})[0] == 200 and not review_item()["done"]  # one of eleven
    assert call("POST", "/api/review_all")[0] == 200 and all(d["reviewed"] for d in docs()) and review_item()["done"]
    assert call("GET", "/api/state", {"year": "2027"})[1]["plants"][0]["see_total"] == before
    assert call("GET", "/api/report", {"year": "2027"})[0] == 200


def test_fixing_a_misread_value_changes_the_number_and_is_marked_edited():
    reset()
    call("POST", "/api/demo")
    d = by_name("fuel_1.txt")
    assert "fuel lpg 30.0 t" in items()
    assert call("POST", "/api/review", body={"doc": d["id"], "record": {"quantity": 3}})[0] == 200
    assert "fuel lpg 3 t" in items() and "fuel lpg 30.0 t" not in items()
    fixed = by_name("fuel_1.txt")
    assert fixed["reviewed"] and fixed["edits"] == [{"field": "quantity", "from": 30.0, "to": 3}]
    row = next(r for r in call("GET", "/api/audit", {"year": "2027"})[1]["rows"] if r["item"] == "fuel lpg 3 t")
    assert row["sources"][0]["edited"] is True


def test_correcting_a_heat_number_joins_it_to_its_invoice():
    reset()
    up("cert.txt", "Document: mtc\nSupplier: Kaveri Integrated Steel\nHeat No: BR-1999\nQuantity: 9 coils")
    up("inv.txt", "Document: steel_invoice\nHeat No: BR148\nSteel (t): 12.5")
    assert not next(i for i in call("GET", "/api/readiness")[1]["items"] if i["key"] == "tonnes")["done"]  # both heats are loose
    assert call("POST", "/api/review", body={"doc": by_name("cert.txt")["id"], "record": {"heat_no": "BR148"}})[0] == 200
    tonnes = next(i for i in call("GET", "/api/readiness")[1]["items"] if i["key"] == "tonnes")
    assert tonnes["done"]  # the typo no longer leaves a heat without tonnes


def test_reclassifying_a_document_uses_it():
    reset()
    r = up("odd.txt", "Document: other\nFuel: LPG\nQuantity: 5 t")
    assert "not used" in r["error"]
    assert call("POST", "/api/review", body={"doc": r["doc"], "record": {"doc_type": "fuel_invoice", "fuel": "lpg", "quantity": 5, "unit": "t"}})[0] == 200
    d = by_name("odd.txt")
    assert d["issues"] == [] and d["reviewed"]  # now used, and confirmed by the edit


def test_removing_a_document_removes_its_figures():
    reset()
    call("POST", "/api/demo")
    assert call("GET", "/api/readiness")[1]["items"][3]["done"]
    d = by_name("production.txt")
    assert call("POST", "/api/doc_remove", body={"doc": d["id"]})[0] == 200
    assert not call("GET", "/api/readiness")[1]["items"][3]["done"] and all(x["name"] != "production.txt" for x in docs())
    up("production.txt", "Document: production\nOutput (t): 1000")  # the same file can be added again
    assert call("GET", "/api/readiness")[1]["items"][3]["done"]


def test_certificate_without_tonnes_is_only_flagged_while_its_heat_is_loose():
    reset()
    call("POST", "/api/demo")
    assert by_name("mtc_6.txt")["issues"] == []  # its tonnes come from steel_invoice_1.txt
    up("late.txt", "Document: mtc\nSupplier: Kaveri Integrated Steel\nHeat No: LATE-9\nQuantity: 12 coils")
    issues = by_name("late.txt")["issues"]
    assert len(issues) == 1 and "LATE-9" in issues[0]
    up("late_inv.txt", "Document: steel_invoice\nHeat No: late 9\nSteel (t): 12")
    assert by_name("late.txt")["issues"] == []


def test_bad_edits_are_refused_and_change_nothing():
    reset()
    up("f.txt", FUEL(5))
    d = by_name("f.txt")
    for bad in ({"quantity": -1}, {"quantity": "abc"}, {"quantity": True}, {"unit": "gallon"}, {"fuel": "coal"},
                {"doc_type": "invoice"}, {"heats": "x"}, {"heats": [{"heat_no": "A", "tonnes": -2}]}, {"colour": "red"}, {"supplier": 5}):
        code, data, _, _ = call("POST", "/api/review", body={"doc": d["id"], "record": bad})
        assert code == 400 and "error" in data, bad
    assert by_name("f.txt")["record"] == d["record"] and by_name("f.txt")["edits"] == [] and not by_name("f.txt")["reviewed"]
    assert call("POST", "/api/review", body={"doc": "nope"})[0] == 404
    assert call("POST", "/api/doc_remove", body={"doc": "nope"})[0] == 404


def test_the_report_states_what_was_edited():
    reset()
    call("POST", "/api/demo")
    call("POST", "/api/review", body={"doc": by_name("fuel_1.txt")["id"], "record": {"quantity": 29}})
    call("POST", "/api/review_all")
    rep = call("GET", "/api/report", {"year": "2027"})[1]
    assert rep["review"] == {"documents": 11, "confirmed": 11, "edited": 1,
                             "edits": [{"file": "fuel_1.txt", "field": "quantity", "from": 30.0, "to": 29}]}


if __name__ == "__main__":
    for n, f in list(globals().items()):
        if n.startswith("test_"): f()
    print("ok")
