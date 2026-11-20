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
    assert not r["ready"] and [i["key"] for i in r["items"] if i["required"]] == ["certificates", "tonnes", "fuel", "output", "review"]
    code, data, _, _ = call("GET", "/api/report", {"year": "2027"})
    assert code == 409 and not data["readiness"]["ready"]


def test_ready_after_documents_and_report_has_everything():
    reset()
    assert call("POST", "/api/demo")[0] == 200
    assert not call("GET", "/api/readiness")[1]["ready"]  # read, but not yet confirmed by the clerk
    assert call("POST", "/api/review_all")[0] == 200
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


def test_same_document_twice_is_counted_once():
    reset()
    call("POST", "/api/demo")
    once = call("GET", "/api/state", {"year": "2027"})[1]["plants"][0]
    again = call("POST", "/api/demo")[1]
    assert all("already uploaded" in r["error"] for r in again)
    twice = call("GET", "/api/state", {"year": "2027"})[1]["plants"][0]
    assert twice["output_t"] == once["output_t"] == 1000 and twice["see_total"] == once["see_total"]
    fuel = "Document: fuel_invoice\nFuel: LPG\nQuantity: 5 t"
    first = call("POST", "/api/upload", body={"filename": "a.txt", "mime": "text/plain", "data": b64(fuel)})[1]
    second = call("POST", "/api/upload", body={"filename": "copy of a.txt", "mime": "text/plain", "data": b64(fuel)})[1]
    assert "error" not in first and "a.txt" in second["error"]


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


def test_verifier_dossier_zip_export():
    import io, zipfile
    reset()
    call("POST", "/api/demo")
    code, data, ctype, headers = call("GET", "/api/dossier", {"year": "2027"})
    assert code == 200 and ctype == "application/zip"
    assert isinstance(data, bytes) and data.startswith(b"PK")
    with zipfile.ZipFile(io.BytesIO(data), "r") as z:
        names = z.namelist()
        assert "cbam_audit_trail.json" in names
        assert "cbam_supplier_communication.csv" in names
        assert "monitoring_methodology.txt" in names
        assert any(n.startswith("evidence_documents/") for n in names)


def test_agent_review_endpoint():
    reset()
    # Empty plant
    code, data, _, _ = call("GET", "/api/agent/review", {"year": "2027"})
    assert code == 200 and data["empty"] and len(data["questions"]) > 0

    # Populated plant
    call("POST", "/api/demo")
    call("POST", "/api/review_all")
    code, data, _, _ = call("GET", "/api/agent/review", {"year": "2027"})
    assert code == 200 and not data["empty"]
    assert round(data["tco2_per_tonne"], 2) == 4.38
    assert len(data["fixes"]) >= 2
    top = data["fixes"][0]
    assert "Rayalaseema" in top["title"] and top["rank"] == 1
    assert "660" in top["detail"] and "63%" in top["detail"]
    assert data["question"] == "Do you maintain monthly fuel stock logs or only purchase invoices?"
    assert data["tools_used"] == ["get_readiness", "get_documents", "get_plant", "draft_mill_request"]
    assert data["draft_email"] and data["draft_email"]["mill"] == "Rayalaseema Steel Rolling"
    assert "RSR-24-0412" in data["draft_email"]["email"]


def test_dossier_zip_export():
    import zipfile, io
    call("POST", "/api/reset")
    call("POST", "/api/demo")
    code, payload, ctype, hdrs = call("GET", "/api/dossier", {"year": "2027"})
    assert code == 200, f"Expected 200, got {code}"
    assert ctype == "application/zip", f"Expected application/zip, got {ctype}"
    assert isinstance(payload, bytes), "Payload must be binary bytes"
    assert len(payload) > 1000, "ZIP dossier is unexpectedly small"
    zf = zipfile.ZipFile(io.BytesIO(payload))
    assert zf.testzip() is None, "ZIP file integrity check failed"
    names = zf.namelist()
    assert "cbam_audit_trail.json" in names
    assert "cbam_supplier_communication.csv" in names
    assert "monitoring_methodology.txt" in names
    assert any(n.startswith("evidence_documents/") for n in names)


def test_carbon_ledger_and_trader_detection():
    call("POST", "/api/reset")
    # Upload an MTC with a trader name to test origin detection
    doc = call("POST", "/api/upload", {}, {
        "filename": "trader_cert.txt",
        "mime": "text/plain",
        "data": base64.b64encode(b"Document: mtc\nSupplier: Aggarwal Steel Traders\nHeat No: AGG-991\nSteel (t): 45\n").decode()
    })[1]
    issues = [d["issues"] for d in call("GET", "/api/docs")[1] if d["name"] == "trader_cert.txt"][0]
    assert any("distributor/trader" in iss for iss in issues)

    # Load demo and verify carbon ledger
    call("POST", "/api/reset")
    call("POST", "/api/demo")
    state = call("GET", "/api/state", {"year": "2027"})[1]
    ledger = state.get("carbon_ledger", [])
    assert len(ledger) > 0
    item = next((x for x in ledger if "RSR" in x["heat_no"]), None)
    assert item is not None
    assert item["purchased_t"] > 0
    assert item["status"] in ("active", "depleted", "fully_allocated")

    # Readiness score
    call("POST", "/api/review_all")
    ready = call("GET", "/api/readiness")[1]
    assert ready["score"] == 100
    assert ready["verifier_ready"] is True


def test_static_files_stay_inside_docs():
    assert server.static_path("/") .endswith(os.path.join("docs", "index.html"))
    assert server.static_path("/app.html").endswith(os.path.join("docs", "app.html"))
    for bad in ("/../server.py", "/..%2Fserver.py", "/py/../../server.py", "/nope.html"):
        assert server.static_path(bad) is None, bad


if __name__ == "__main__":
    for n, f in list(globals().items()):
        if n.startswith("test_"): f()
    print("ok")
