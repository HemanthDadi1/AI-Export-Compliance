"""Test and harden extraction on real Indian MTC PDFs and edge cases.
Covers:
1. Indian numbering formats (1,00,000 kg vs 100 MT)
2. Multi-heat tables, coil count vs. weight splits
3. Trader invoices vs. direct mill certificates
4. Live PDF inspection when GEMINI_API_KEY / VERTEX_PROJECT is set

Run offline: python3 test_real_certs.py
Run live: GEMINI_API_KEY=... python3 test_real_certs.py
"""
import io, json, os, sys
import extract

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def test_indian_numbering_formats():
    """Verify Indian numbering format parsing (lakhs, commas, kg to tonnes conversion)."""
    # 1,00,000 kg should convert to 100.0 t
    rec1 = extract._normalize_record({
        "doc_type": "mtc",
        "supplier": "Rayalaseema Steel Rolling",
        "heat_no": "RSR-24-0412",
        "steel_tonnes": "1,00,000 kg"
    })
    assert rec1["steel_tonnes"] == 100.0, f"Expected 100.0, got {rec1['steel_tonnes']}"

    # 52,340 kg should convert to 52.34 t
    rec2 = extract._normalize_record({
        "doc_type": "mtc",
        "supplier": "RINL",
        "heat_no": "H-101",
        "steel_tonnes": "52,340"
    })
    assert rec2["steel_tonnes"] == 52.34, f"Expected 52.34, got {rec2['steel_tonnes']}"

    # 100 MT should stay 100.0 t
    rec3 = extract._normalize_record({
        "doc_type": "mtc",
        "supplier": "Kaveri Integrated Steel",
        "steel_tonnes": "100 MT"
    })
    assert rec3["steel_tonnes"] == 100.0, f"Expected 100.0, got {rec3['steel_tonnes']}"

    # 2,50,000 Kgs should convert to 250.0 t
    rec4 = extract._normalize_record({
        "doc_type": "steel_invoice",
        "steel_tonnes": "2,50,000 Kgs"
    })
    assert rec4["steel_tonnes"] == 250.0, f"Expected 250.0, got {rec4['steel_tonnes']}"


def test_multi_heat_tables_and_coil_splits():
    """Verify multi-heat tables with individual heat tonnages or coil count only."""
    # Multi-heat table with weights in kg: 52,340 kg + 47,660 kg = 100 t
    raw_payload = {
        "doc_type": "Inspection Certificate EN 10204 / 3.1",
        "supplier": "Rayalaseema Steel Rolling Pvt Ltd",
        "heat_no": "RSR-26-0877",
        "steel_tonnes": None,
        "heats": [
            {"heat_no": "RSR-26-0877", "tonnes": "52,340 kg"},
            {"heat_no": "RSR-26-0881", "tonnes": "47,660 kg"}
        ]
    }
    rec = extract._normalize_record(raw_payload)
    assert rec["doc_type"] == "mtc"
    assert len(rec["heats"]) == 2
    assert rec["heats"][0]["heat_no"] == "RSR-26-0877"
    assert round(rec["heats"][0]["tonnes"], 2) == 52.34
    assert round(rec["heats"][1]["tonnes"], 2) == 47.66
    # Total steel_tonnes computed from heat sum
    assert round(rec["steel_tonnes"], 2) == 100.0

    # Multi-heat table with coil/piece count only (e.g. 41 coils, 18500 pcs)
    coil_payload = {
        "doc_type": "mtc",
        "supplier": "RINL",
        "heat_no": "BR148",
        "steel_tonnes": None,
        "heats": [
            {"heat_no": "BR148", "tonnes": None},  # only pieces given in document
            {"heat_no": "BR151", "tonnes": None}
        ]
    }
    rec_coil = extract._normalize_record(coil_payload)
    assert rec_coil["steel_tonnes"] is None
    assert all(h["tonnes"] is None for h in rec_coil["heats"])


def test_trader_invoice_vs_direct_mill_certificates():
    """Verify distinction between direct mill certificate, trader-issued MTC, and purchase invoice."""
    # 1. Trader-issued MTC specifying primary melting mill
    trader_mtc = {
        "doc_type": "MATERIAL TEST CERTIFICATE BS EN 10204 - 3.1",
        "supplier": "RINL",  # Melted by primary mill RINL, though issued by Real Engineering
        "heat_no": "BR148",
        "quote": "Melting Process: EAF, Steel Mill: RINL"
    }
    rec1 = extract._normalize_record(trader_mtc)
    assert rec1["doc_type"] == "mtc"
    assert rec1["supplier"] == "RINL"

    # 2. Steel purchase invoice from a trader/stockist
    trader_inv = {
        "doc_type": "steel_invoice",
        "supplier": "Sri Balaji Steel Traders, Chennai",
        "heat_no": "RSR-24-0412",
        "steel_tonnes": 180.0,
        "quote": "Tax Invoice 4471: Sri Balaji Steel Traders to Sri Venkateswara Fasteners"
    }
    rec2 = extract._normalize_record(trader_inv)
    assert rec2["doc_type"] == "steel_invoice"
    assert "Sri Balaji" in rec2["supplier"]
    assert rec2["steel_tonnes"] == 180.0


def test_markdown_fence_sanitization():
    """Verify Gemini markdown output fences (```json ... ```) are cleanly stripped."""
    fence = '```json\n{"doc_type": "mtc", "supplier": "Jindal Steel", "heat_no": "JSP-88", "steel_tonnes": 45.5}\n```'
    # Mocking urlopen response
    orig_open = extract.urllib.request.urlopen
    orig_key = os.environ.get("GEMINI_API_KEY")
    try:
        os.environ["GEMINI_API_KEY"] = "test-key"
        reply = {"candidates": [{"content": {"parts": [{"text": fence}]}}]}
        extract.urllib.request.urlopen = lambda req, timeout: io.BytesIO(json.dumps(reply).encode())
        res, m = extract.extract("application/pdf", b"%PDF-1.4 mock")
        assert m == "gemini"
        assert res["doc_type"] == "mtc"
        assert res["supplier"] == "Jindal Steel"
        assert res["steel_tonnes"] == 45.5
    finally:
        extract.urllib.request.urlopen = orig_open
        if orig_key: os.environ["GEMINI_API_KEY"] = orig_key
        else: os.environ.pop("GEMINI_API_KEY", None)


def run_live_gemini_if_configured():
    """If GEMINI_API_KEY or VERTEX_PROJECT is available, test against real PDFs in the directory."""
    m = extract.mode()
    if m == "rules":
        print("[info] Skipping live Gemini extraction (GEMINI_API_KEY/VERTEX_PROJECT unset).")
        print("       Mock edge case suite passed 100%.")
        return

    print(f"[live] Running live Gemini extraction using mode '{m}'...")
    if m == "gemini":
        available = extract._get_api_models()
        if available:
            print(f"       Discovered {len(available)} model(s) enabled for this key: {', '.join(available[:4])}...")
    targets = [
        os.path.join(HERE, "samples/mtc_real.pdf"),
        os.path.join(ROOT, "ilide.info-fastners-mtc-pr_440008252c5a37ecf87173c7279e48d0.pdf"),
        os.path.join(ROOT, "23 039 0 - 20460.signed.pdf")
    ]
    for path in targets:
        if not os.path.isfile(path):
            continue
        name = os.path.basename(path)
        print(f" -> Testing {name} ({os.path.getsize(path)/1024:.1f} KB)...")
        try:
            raw = open(path, "rb").read()
            res, mode_used = extract.extract("application/pdf", raw)
            print(f"    Extracted: doc_type={res['doc_type']}, supplier={res['supplier']}, steel_tonnes={res.get('steel_tonnes')}, heats={res.get('heats')}")
            assert res["doc_type"] in ("mtc", "steel_invoice", "production", "other"), res["doc_type"]
        except Exception as e:
            print(f"    [error] {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and not sys.argv[1].startswith("-"):
        os.environ["GEMINI_API_KEY"] = sys.argv[1]
    test_indian_numbering_formats()
    test_multi_heat_tables_and_coil_splits()
    test_trader_invoice_vs_direct_mill_certificates()
    test_markdown_fence_sanitization()
    run_live_gemini_if_configured()
    print("ok")
