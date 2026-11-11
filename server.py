"""Stdlib web server. Run: python3 server.py, then open http://localhost:8000"""
import json, os, re, uuid, copy
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import base64
from calc import compute, fuel_tco2, FUELS, DEFAULT_PRECURSOR_SEE
from extract import extract, mode

HERE = os.path.dirname(os.path.abspath(__file__))
YOU = "A"

SEED = {
    "suppliers": {
        "Kaveri Integrated Steel": {"verified": True, "see": 2.1, "report": "Verification report KIS-2026-114 (demo)"},
        "Rayalaseema Steel Rolling": {"verified": False},
        "Godavari Induction Steels": {"verified": False},
    },
    "plants": {
        YOU: {"id": YOU, "name": "Sri Venkateswara Fasteners (your plant)", "steel": [], "fuel": [], "output": [],
              "heats": {}, "checks": [], "log": []},
        "B": {"id": "B", "name": "Chennai Bolt Works", "fuel": [{"fuel": "lpg", "qty": 18, "unit": "t"}],
              "steel": [{"supplier": "Rayalaseema Steel Rolling", "tonnes": 300}, {"supplier": "Kaveri Integrated Steel", "tonnes": 100}],
              "output": [{"tonnes": 390}]},
        "C": {"id": "C", "name": "Hyderabad Wire & Fasteners", "fuel": [{"fuel": "lpg", "qty": 25, "unit": "t"}],
              "steel": [{"supplier": "Rayalaseema Steel Rolling", "tonnes": 500}], "output": [{"tonnes": 480}]},
        "D": {"id": "D", "name": "Nellore Screws", "fuel": [{"fuel": "lpg", "qty": 12, "unit": "t"}],
              "steel": [{"supplier": "Rayalaseema Steel Rolling", "tonnes": 200}, {"supplier": "Godavari Induction Steels", "tonnes": 150}],
              "output": [{"tonnes": 340}]},
    },
}
state, docs = copy.deepcopy(SEED), {}  # shortcut: in memory only, lost on restart. Move to Cloud SQL for pilots.


def add_doc(filename, mime, raw):
    doc_id = uuid.uuid4().hex[:8]
    docs[doc_id] = {"name": filename, "mime": mime, "raw": raw}
    try:
        rec, mode = extract(mime, raw)
    except Exception as e:
        return {"file": filename, "error": f"could not read: {e}"}
    src = {"doc": doc_id, "file": filename, "quote": rec.get("quote")}
    p, t, pos = state["plants"][YOU], rec["doc_type"], lambda v: isinstance(v, (int, float)) and v > 0
    if t in ("mtc", "steel_invoice"):
        rows = [h for h in rec.get("heats") or [] if isinstance(h, dict) and (h.get("heat_no") or pos(h.get("tonnes")))]
        rows = rows or [{"heat_no": rec["heat_no"], "tonnes": rec["steel_tonnes"]}]
        mill = rec["supplier"] if t == "mtc" else None  # an invoice seller may be a trader, never the mill
        if not any(h.get("heat_no") or (mill and pos(h.get("tonnes"))) for h in rows):
            return {"file": filename, "mode": mode, "record": rec, "error": "not used: no heat number"}
        for i, h in enumerate(rows):
            add_heat(p, h.get("heat_no") or f"{doc_id}-{i}", mill, h.get("tonnes") if pos(h.get("tonnes")) else None, src)
        sync_steel(p)
    elif t == "fuel_invoice" and rec["fuel"] in (*FUELS, "natural_gas") and pos(rec["quantity"]) and rec["unit"]:
        p["fuel"].append({"fuel": rec["fuel"], "qty": rec["quantity"], "unit": rec["unit"], "source": src})
    elif t == "production" and pos(rec["output_tonnes"]):
        p["output"].append({"tonnes": rec["output_tonnes"], "cn": rec["cn_code"], "source": src})
    else:
        return {"file": filename, "mode": mode, "record": rec, "error": "not used: missing or invalid fields"}
    return {"file": filename, "mode": mode, "record": rec}


def add_heat(p, key, mill, tonnes, src):
    """One entry per heat. Mill comes from a certificate, tonnes from any document. Conflicts are flagged, never overwritten."""
    e = p["heats"].setdefault(re.sub(r"[^A-Z0-9]", "", key.upper()) or key, {"heat": key})  # "BR-148" == "br 148"
    for field, val in (("mill", mill), ("tonnes", tonnes)):
        if val is None:
            continue
        if field not in e:
            e[field], e[field + "_src"] = val, src
        elif e[field] != val:
            p["checks"].append(f"Heat {key}: {e[field + '_src']['file']} says {e[field]}, "
                               f"{src['file']} says {val}. Kept the first. Check with the supplier.")


def sync_steel(p):
    p["steel"] = [{"supplier": e["mill"], "tonnes": e["tonnes"], "heat": e["heat"], "source": e["tonnes_src"],
                   "mill_source": e["mill_src"]} for e in p["heats"].values() if "mill" in e and "tonnes" in e]
    for s in p["steel"]:
        state["suppliers"].setdefault(s["supplier"], {"verified": False})


def unmatched(p):
    return [{"heat": e["heat"], "missing": "tonnes" if "mill" in e else "mill"}
            for e in p["heats"].values() if not ("mill" in e and "tonnes" in e)]


def add_log(p, e):
    """Monthly capture. Fuel used = opening stock + bought - closing stock, because purchases are not usage."""
    month = str(e.get("month", ""))
    if not re.fullmatch(r"\d{4}-(0[1-9]|1[0-2])", month):
        raise ValueError("month must be YYYY-MM")

    def num(k):
        v = e.get(k)
        if isinstance(v, bool) or not isinstance(v, (int, float)) or v < 0:
            raise ValueError(f"{k} must be a number, 0 or more")
        return v
    if e.get("kind") == "production":
        row = {"kind": "production", "month": month, "output_t": num("output_t")}
    else:
        row = {"kind": "fuel", "month": month, "fuel": e.get("fuel"), "unit": e.get("unit"), "opening": num("opening"),
               "purchased": num("purchased"), "closing": num("closing"), "meter": str(e.get("meter") or "")[:80]}
        row["used"] = row["opening"] + row["purchased"] - row["closing"]
        if row["used"] < 0:
            raise ValueError("closing stock is more than opening stock plus purchases")
        fuel_tco2(row["fuel"], row["used"], row["unit"])  # rejects unknown fuel or unit
    key = lambda r: (r["kind"], r["month"], r.get("fuel"))
    p["log"] = sorted([r for r in p["log"] if key(r) != key(row)] + [row], key=lambda r: r["month"])


def purchase_gap(p, fuel):
    """(logged purchases, invoiced purchases, unit) when they disagree by more than 0.5%, else None."""
    # shortcut: compares only invoices in the log's unit. Convert units when plants mix them.
    rows = [r for r in p.get("log") or [] if r["kind"] == "fuel" and r["fuel"] == fuel]
    unit = rows[0]["unit"]
    inv = sum(f["qty"] for f in p["fuel"] if f["fuel"] == fuel and f["unit"] == unit)
    bought = sum(r["purchased"] for r in rows if r["unit"] == unit)
    return (bought, inv, unit) if inv and abs(bought - inv) > 0.005 * inv else None


def effective(p):
    """What the calculation uses: logged fuel use beats purchase invoices, logged output beats dispatch records."""
    # shortcut: every logged month counts, whatever the reporting year. Filter by year when plants log more than one.
    log = p.get("log") or []
    flog = [r for r in log if r["kind"] == "fuel"]
    # A log that does not cover the invoices is partial. It must not replace them and lower the number.
    logged = {r["fuel"] for r in flog if not purchase_gap(p, r["fuel"])}
    fuel = [f for f in p["fuel"] if f["fuel"] not in logged] + [
        {"fuel": r["fuel"], "qty": r["used"], "unit": r["unit"], "source": {
            "file": f"monthly log {r['month']}", "quote": f"opening {r['opening']} + bought {r['purchased']} - closing {r['closing']}"}}
        for r in flog if r["fuel"] in logged]
    prod = [{"tonnes": r["output_t"], "source": {"file": f"monthly log {r['month']}", "quote": f"output {r['output_t']} t"}}
            for r in log if r["kind"] == "production"]
    # Same rule for output: a part-year log replaces dispatch records only when there are none.
    output = prod if prod and (len(prod) >= 12 or not p["output"]) else p["output"]
    return {**p, "fuel": fuel, "output": output}


def log_checks(p):
    """Controls a verifier would run on the log. Computed fresh each time."""
    out, flog = [], [r for r in p["log"] if r["kind"] == "fuel"]
    for fuel in sorted({r["fuel"] for r in flog}):
        rows = [r for r in flog if r["fuel"] == fuel]
        for a, b in zip(rows, rows[1:]):
            if a["closing"] != b["opening"]:
                out.append(f"{fuel} {b['month']}: opening stock {b['opening']} does not match {a['month']} closing stock {a['closing']}.")
        gap = purchase_gap(p, fuel)
        if gap:
            out.append(f"{fuel}: log says {gap[0]:g} {gap[2]} bought, invoices say {gap[1]:g} {gap[2]}. "
                       "Using invoices until they match. Check for a missing invoice or month.")
    return out


def plan(p):
    """Rule-based draft of the monitoring plan, plus the gaps a verifier would ask about. No AI."""
    flog = [r for r in p["log"] if r["kind"] == "fuel"]
    logged = {r["fuel"] for r in flog}
    lines = [f"Installation: {p['name']}", "Goods: screws, bolts and nuts (CN 7318)",
             "Route: wire rod, cold heading, heat treatment, plating",
             "Method: calculation-based. Activity data x standard emission factor. Direct emissions only."]
    gaps = []
    for fuel in sorted({f["fuel"] for f in p["fuel"]} | logged):
        if fuel not in logged:
            lines.append(f"{fuel}: purchase invoices only.")
            gaps.append(f"{fuel}: only purchase invoices. Purchases are not usage. Start a monthly stock log.")
            continue
        rows = [r for r in flog if r["fuel"] == fuel]
        meter = next((r["meter"] for r in reversed(rows) if r["meter"]), "")
        lines.append(f"{fuel}: used = opening stock + purchases - closing stock, logged monthly "
                     f"({rows[0]['month']} to {rows[-1]['month']}). Measured by: {meter or 'not recorded'}.")
        if not meter:
            gaps.append(f"{fuel}: no meter or weighing device recorded. Add it with its calibration date.")
        if len(rows) < 12:
            gaps.append(f"{fuel}: {len(rows)} of 12 months logged.")
    months = [r["month"] for r in p["log"] if r["kind"] == "production"]
    if months:
        lines.append(f"Output: production logged monthly ({months[0]} to {months[-1]}).")
        if len(months) < 12:
            gaps.append(f"Output: {len(months)} of 12 months logged.")
    else:
        lines.append("Output: dispatch records." if p["output"] else "Output: none yet.")
        gaps.append("Output: no monthly production log. Log tonnes made each month.")
    for mill in sorted({s["supplier"] for s in p["steel"]}):
        ok = state["suppliers"].get(mill, {}).get("verified")
        lines.append(f"Precursor steel from {mill}: {'verified actual value' if ok else 'EU default value plus penalty'}.")
        if not ok:
            gaps.append(f"{mill}: no verified data. Ask the mill to join.")
    gaps += [f"Heat {u['heat']}: {u['missing']} missing." for u in unmatched(p)]
    return {"lines": lines, "gaps": gaps}


DEMO_LOG = [
    {"kind": "fuel", "month": "2026-04", "fuel": "lpg", "unit": "t", "opening": 6, "purchased": 30, "closing": 8,
     "meter": "Weighbridge WB-2, calibrated 2026-01"},
    {"kind": "fuel", "month": "2026-05", "fuel": "lpg", "unit": "t", "opening": 8, "purchased": 26, "closing": 10},
]


def audit(year):
    """Everything a verifier needs: the result, one row per figure with its sources, the checks and the open gaps."""
    p = state["plants"][YOU]
    r = compute(effective(p), state["suppliers"], year)
    if r["empty"]:
        return {"empty": True}

    def src(role, s):
        return {"role": role, "file": s["file"], "doc": s.get("doc"), "quote": s.get("quote")} if s else None

    def sources(*pairs):
        out = [x for x in (src(*pr) for pr in pairs) if x]
        if len(out) == 2 and out[0]["file"] == out[1]["file"] and out[0]["doc"] == out[1]["doc"]:
            out = [{**out[0], "role": "tonnes and mill"}]  # one document gave both
        return out
    rows = [{"kind": "fuel", "item": f"fuel {l['fuel']} {l['qty']} {l['unit']}", "tco2": round(l["tco2"], 3), "basis": "actual",
             "sources": sources(("quantity", l.get("source")))} for l in r["direct_lines"]]
    for pr in r["precursors"]:
        for h in pr["heats"]:
            rows.append({"kind": "steel", "item": f"steel {pr['supplier']} heat {h.get('heat')} {h['tonnes']} t",
                         "tco2": round(h["tonnes"] * pr["see"], 3),
                         "basis": f"{pr['basis']} {round(pr['see'], 3)} tCO2/t {pr['report'] or ''}".strip(),
                         "sources": sources(("tonnes", h.get("source")), ("mill", h.get("mill_source")))})
    rows += [{"kind": "output", "item": f"output {o['tonnes']} t", "tco2": None, "basis": "",
              "sources": sources(("output", o.get("source")))} for o in effective(p)["output"]]
    keys = ("name", "year", "output_t", "see_total", "see_direct", "see_precursor", "verified_share")
    return {"summary": {k: r[k] for k in keys}, "rows": rows, "plan": plan(p), "method": plan(p)["lines"],
            "checks": p["checks"] + log_checks(p),
            "default_note": f"Steel default used: {DEFAULT_PRECURSOR_SEE} tCO2/t before the mark-up. Secondary source. Check it against the current EU table.",
            "draft": "Draft. Not verified. Indirect emissions are not counted for iron and steel goods."}


def view(year):
    plants = []
    for p in state["plants"].values():
        try:
            plants.append(compute(effective(p), state["suppliers"], year))
        except ValueError as e:
            plants.append({"id": p["id"], "name": p["name"], "empty": True, "error": str(e)})
    you = state["plants"][YOU]
    return {"plants": plants, "suppliers": state["suppliers"], "year": year,
            "unmatched": unmatched(you), "checks": you["checks"] + log_checks(you),
            "log": you["log"], "plan": plan(you),
            "mode": mode()}


class H(BaseHTTPRequestHandler):
    def send(self, code, body, ctype="application/json", extra=()):
        data = body if isinstance(body, bytes) else json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("X-Content-Type-Options", "nosniff")
        for k, v in extra:
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        u = urlparse(self.path); q = parse_qs(u.query)
        if u.path == "/":
            return self.send(200, open(os.path.join(HERE, "index.html"), "rb").read(), "text/html; charset=utf-8")
        if u.path == "/verifier":
            return self.send(200, open(os.path.join(HERE, "verifier.html"), "rb").read(), "text/html; charset=utf-8")
        if u.path == "/api/audit":
            return self.send(200, audit(int(q.get("year", ["2027"])[0])))
        if u.path == "/api/state":
            return self.send(200, view(int(q.get("year", ["2027"])[0])))
        if u.path == "/api/doc" and q.get("id", [""])[0] in docs:
            d = docs[q["id"][0]]
            safe = d["mime"] if d["mime"] == "application/pdf" or d["mime"].startswith("image/") else "text/plain; charset=utf-8"
            return self.send(200, d["raw"], safe)
        if u.path == "/api/export":
            return self.send(200, export_csv(int(q.get("year", ["2027"])[0])).encode(), "text/csv",
                             [("Content-Disposition", "attachment; filename=cbam_supplier_communication.csv")])
        self.send(404, {"error": "not found"})

    def do_POST(self):
        n = int(self.headers.get("Content-Length") or 0)
        if n > 15_000_000:
            return self.send(413, {"error": "file too large"})
        body = json.loads(self.rfile.read(n) or b"{}")
        path = urlparse(self.path).path
        if path == "/api/upload":
            return self.send(200, add_doc(body["filename"], body.get("mime") or "text/plain", base64.b64decode(body["data"])))
        if path == "/api/demo":
            out = [add_doc(f, "text/plain", open(os.path.join(HERE, "demo", f), "rb").read())
                   for f in sorted(os.listdir(os.path.join(HERE, "demo")))]
            return self.send(200, out)
        if path in ("/api/log", "/api/demo_log"):
            try:
                for e in (DEMO_LOG if path == "/api/demo_log" else [body]):
                    add_log(state["plants"][YOU], e)
            except ValueError as e:
                return self.send(400, {"error": str(e)})
            return self.send(200, {"ok": True})
        if path == "/api/supplier":
            see = float(body["see"])
            if not 0 < see < 10:
                return self.send(400, {"error": "value must be between 0 and 10 tCO2/t"})
            state["suppliers"][body["name"]] = {"verified": True, "see": see, "report": body.get("report") or "Verification report (demo)"}
            return self.send(200, {"ok": True})
        if path == "/api/reset":
            state.clear(); state.update(copy.deepcopy(SEED)); docs.clear()
            return self.send(200, {"ok": True})
        self.send(404, {"error": "not found"})

    def log_message(self, *a):
        pass


def export_csv(year):
    import csv, io
    a = audit(year)
    if a.get("empty"):
        return "No data yet. Upload documents first.\n"
    sm = a["summary"]
    out = io.StringIO(); w = csv.writer(out)
    w.writerow(["CBAM supplier communication (draft, not verified)", f"reporting year {year}"])
    w.writerow(["Installation", sm["name"]]); w.writerow(["CN code", "7318"])
    w.writerow(["Output (t)", sm["output_t"]])
    w.writerow(["Specific direct emissions (tCO2/t)", round(sm["see_direct"], 4)])
    w.writerow(["Precursor emissions (tCO2/t)", round(sm["see_precursor"], 4)])
    w.writerow(["Specific embedded emissions (tCO2/t)", round(sm["see_total"], 4)])
    w.writerow(["Indirect emissions", "not counted for iron and steel goods"])
    w.writerow([]); w.writerow(["Audit trail: item", "value", "basis", "source file", "source text"])
    for r in a["rows"]:
        files = " + ".join(dict.fromkeys(x["file"] for x in r["sources"]))
        w.writerow([r["item"], "" if r["tco2"] is None else r["tco2"], r["basis"], files, r["sources"][0].get("quote")])
    w.writerow([]); w.writerow(["Monitoring plan (draft)"])
    for l in a["method"]:
        w.writerow([l])
    w.writerow(["Open gaps"])
    for g in a["plan"]["gaps"]:
        w.writerow([g])
    return out.getvalue()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"Open http://localhost:{port}  (extraction: {mode()})")
    ThreadingHTTPServer((os.environ.get("HOST", "127.0.0.1"), port), H).serve_forever()
