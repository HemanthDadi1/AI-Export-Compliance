"""Routing, readiness and the compliance report. Run: python3 test_app.py"""
import base64, json, os
for k in ("GEMINI_API_KEY", "VERTEX_PROJECT"): os.environ.pop(k, None)  # rule parser, no network
import server

call = lambda method, path, query=None, body=None: server.dispatch(method, path, query or {}, body)
b64 = lambda s: base64.b64encode(s.encode()).decode()


def reset():
    assert call("POST", "/api/reset")[0] == 200


def test_state_and_reset():
    reset()
    code, data, ctype, _ = call("GET", "/api/state", {"year": "2027"})
    assert code == 200 and ctype == "application/json" and data["plants"][0]["empty"]


def test_not_ready_until_required_documents_are_in():
    reset()
    r = call("GET", "/api/readiness")[1]
    assert not r["ready"] and [i["key"] for i in r["items"] if i["required"]] == ["certificates", "tonnes", "fuel", "output"]
    code, data, _, _ = call("GET", "/api/report", {"year": "2027"})
    assert code == 409 and not data["readiness"]["ready"]


def test_ready_after_documents_and_report_has_everything():
    reset()
    assert call("POST", "/api/demo")[0] == 200
    r = call("GET", "/api/readiness")[1]
    assert r["ready"] and all(i["done"] for i in r["items"] if i["required"])
    code, rep, _, _ = call("GET", "/api/report", {"year": "2027"})
    assert code == 200 and rep["readiness"]["ready"] and rep["summary"]["see_total"] > 0
    assert rep["rows"] and rep["method"] and "gaps" in rep["plan"] and rep["draft"]


def test_heat_without_tonnes_blocks_the_report():
    reset()
    call("POST", "/api/demo")
    cert = "Document: mtc\nSupplier: Kaveri Integrated Steel\nHeat No: LATE-9\nQuantity: 12 coils"
    assert call("POST", "/api/upload", body={"filename": "late.txt", "mime": "text/plain", "data": b64(cert)})[0] == 200
    tonnes = next(i for i in call("GET", "/api/readiness")[1]["items"] if i["key"] == "tonnes")
    assert not tonnes["done"] and "LATE-9" in tonnes["hint"]
    assert call("GET", "/api/report", {"year": "2027"})[0] == 409


def test_bad_inputs_are_refused():
    reset()
    assert call("POST", "/api/log", body={"kind": "fuel", "month": "2026-13"})[0] == 400
    assert call("POST", "/api/supplier", body={"name": "X", "see": 20})[0] == 400
    assert call("POST", "/api/supplier", body={"name": "X", "see": "abc"})[0] == 400
    assert call("POST", "/api/upload", body={"filename": "x.txt"})[0] == 400
    assert call("GET", "/api/nope")[0] == 404


def test_csv_and_document_download():
    reset()
    call("POST", "/api/demo")
    code, csv, ctype, headers = call("GET", "/api/export", {"year": "2027"})
    assert code == 200 and ctype.startswith("text/csv") and "Specific embedded emissions" in csv
    doc_id = next(iter(server.docs))
    code, raw, ctype, _ = call("GET", "/api/doc", {"id": doc_id})
    assert code == 200 and isinstance(raw, bytes) and ctype.startswith("text/plain")


def test_static_files_stay_inside_docs():
    assert server.static_path("/") .endswith(os.path.join("docs", "index.html"))
    assert server.static_path("/app.html").endswith(os.path.join("docs", "app.html"))
    for bad in ("/../server.py", "/..%2Fserver.py", "/py/../../server.py", "/nope.html"):
        assert server.static_path(bad) is None, bad


if __name__ == "__main__":
    for n, f in list(globals().items()):
        if n.startswith("test_"): f()
    print("ok")
