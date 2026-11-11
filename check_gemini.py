"""Live check of Gemini extraction. Run: GEMINI_API_KEY=... (or VERTEX_PROJECT=...) python3 check_gemini.py"""
import os, sys
from extract import extract, mode

if mode() == "rules":
    sys.exit("Set GEMINI_API_KEY or VERTEX_PROJECT first.")
rec, mode = extract("application/pdf", open(os.path.join(os.path.dirname(__file__), "samples/mtc_real.pdf"), "rb").read())
print(mode, rec)
# Two heats, 1,00,000 kg in Indian digit grouping.
assert rec["doc_type"] == "mtc", rec["doc_type"]
assert "Rayalaseema" in (rec["supplier"] or ""), rec["supplier"]
assert rec["steel_tonnes"] == 100, rec["steel_tonnes"]
heats = sorted(round(h["tonnes"], 2) for h in rec["heats"] or [])
assert heats == [47.66, 52.34], heats
print("ok")
