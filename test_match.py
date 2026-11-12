"""Heat matching: certificates give the mill, invoices give the tonnes. Run: python3 test_match.py"""
import os
for k in ("GEMINI_API_KEY", "VERTEX_PROJECT"): os.environ.pop(k, None)  # rule parser, no network
import server

doc = lambda *lines: "\n".join(lines).encode()
CERT = doc("Document: mtc", "Supplier: RINL", "Heat No: BR148")  # pieces only, no tonnes
INV = lambda t: doc("Document: steel_invoice", "Supplier: Rajkot Steel Traders", "Heat No: BR148", f"Steel (t): {t}")


def reset():
    server.state.clear(); server.state.update(server.copy.deepcopy(server.SEED)); server.docs.clear()
    return server.state["plants"][server.YOU]


def test_cert_then_invoice():
    p = reset()
    assert "error" not in server.add_doc("c.txt", "text/plain", CERT)
    assert p["steel"] == [] and server.unmatched(p) == [{"heat": "BR148", "missing": "tonnes"}]
    server.add_doc("i.txt", "text/plain", INV(12.5))
    assert [(s["supplier"], s["tonnes"], s["heat"]) for s in p["steel"]] == [("RINL", 12.5, "BR148")]
    assert p["steel"][0]["mill_source"]["file"] == "c.txt" and p["steel"][0]["source"]["file"] == "i.txt"
    assert server.unmatched(p) == [] and "RINL" in server.state["suppliers"]


def test_invoice_then_cert():
    p = reset()
    server.add_doc("i.txt", "text/plain", INV(12.5))
    assert p["steel"] == [] and server.unmatched(p) == [{"heat": "BR148", "missing": "mill"}]
    server.add_doc("c.txt", "text/plain", CERT)
    assert len(p["steel"]) == 1  # trader on the invoice is never taken as the mill


def test_conflict_is_flagged_not_added():
    p = reset()
    server.add_doc("c.txt", "text/plain", CERT); server.add_doc("i.txt", "text/plain", INV(12.5))
    server.add_doc("i2.txt", "text/plain", INV(14))
    assert p["steel"][0]["tonnes"] == 12.5 and len(p["checks"]) == 1 and "BR148" in p["checks"][0]


def test_same_tonnes_twice_counts_once():
    p = reset()
    server.add_doc("c.txt", "text/plain", CERT); server.add_doc("i.txt", "text/plain", INV(12.5))
    server.add_doc("i2.txt", "text/plain", INV(12.5))
    assert len(p["steel"]) == 1 and p["checks"] == []


def test_heat_number_spelling():
    p = reset()
    server.add_doc("c.txt", "text/plain", CERT)  # BR148
    server.add_doc("i.txt", "text/plain", doc("Document: steel_invoice", "Heat No: br-148", "Steel (t): 12.5"))
    assert len(p["steel"]) == 1 and p["steel"][0]["heat"] == "BR148"


if __name__ == "__main__":
    for n, f in list(globals().items()):
        if n.startswith("test_"): f()
    print("ok")
