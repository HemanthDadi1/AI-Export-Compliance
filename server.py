"""Stdlib web server and the one router the app uses. Run: python3 server.py, then open http://localhost:8000
The same router runs in the browser on GitHub Pages (Pyodide), so there is one copy of every rule."""
import base64, copy, json, os, re, uuid
from urllib.parse import urlparse, parse_qs, unquote
try:
    from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
except ImportError:  # the browser build has no sockets; only dispatch() is used there
    ThreadingHTTPServer, BaseHTTPRequestHandler = None, object
from calc import compute, fuel_tco2, FUELS, DEFAULT_PRECURSOR_SEE
from extract import extract, mode

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(HERE, "docs")
CTYPES = {".html": "text/html; charset=utf-8", ".css": "text/css", ".js": "text/javascript", ".json": "application/json",
          ".txt": "text/plain; charset=utf-8", ".py": "text/plain; charset=utf-8", ".svg": "image/svg+xml", ".png": "image/png"}
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
    same = next((d["name"] for d in docs.values() if d["raw"] == raw), None)
    if same:  # a second copy would count its fuel or output twice
        return {"file": filename, "error": f"already uploaded as {same}"}
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


def readiness(p):
    """Which required documents are in. The report unlocks when every required item is done."""
    eff, missing = effective(p), unmatched(p)
    no_mill = [u["heat"] for u in missing if u["missing"] == "mill"]
    no_tonnes = [u["heat"] for u in missing if u["missing"] == "tonnes"]
    items = [
        {"key": "certificates", "label": "Mill test certificates", "required": True,
         "done": any("mill" in e for e in p["heats"].values()) and not no_mill,
         "hint": f"Missing for heat {', '.join(no_mill)}. Upload its mill test certificate." if no_mill
         else "One for each steel heat. It names the mill that made the steel."},
        {"key": "tonnes", "label": "Steel tonnes for every heat", "required": True,
         "done": bool(p["steel"]) and not no_tonnes,
         "hint": f"No tonnes yet for heat {', '.join(no_tonnes)}. Upload its purchase invoice." if no_tonnes
         else "From the certificates or the steel purchase invoices."},
        {"key": "fuel", "label": "Fuel records", "required": True, "done": bool(eff["fuel"]),
         "hint": "Fuel invoices for furnaces and boilers, or the monthly fuel log."},
        {"key": "output", "label": "Production record", "required": True, "done": bool(eff["output"]),
         "hint": "A production or dispatch record, or the monthly output log."},
        {"key": "log", "label": "Monthly fuel and output log", "required": False, "done": bool(p.get("log")),
         "hint": "Recommended. A verifier asks for fuel used, not fuel bought."},
    ]
    req = [i for i in items if i["required"]]
    return {"items": items, "ready": all(i["done"] for i in req), "done": sum(i["done"] for i in req), "total": len(req)}


def static_path(path):
    """A file under docs/ for this URL path, or None. Never anything outside docs/."""
    rel = unquote(path).lstrip("/") or "index.html"
    if ".." in rel.replace("\\", "/").split("/"):
        return None
    full = os.path.realpath(os.path.join(DOCS, rel))
    return full if full.startswith(os.path.realpath(DOCS) + os.sep) and os.path.isfile(full) else None


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


def dispatch(method, path, query, body):
    """The one router. Returns (status, payload, content type, extra headers)."""
    js = lambda code, data: (code, data, "application/json", [])
    you = state["plants"][YOU]
    try:
        year = int(query.get("year") or 2027)
        if method == "GET":
            if path == "/api/state":
                return js(200, view(year))
            if path == "/api/audit":
                return js(200, audit(year))
            if path == "/api/readiness":
                return js(200, readiness(you))
            if path == "/api/report":
                r = readiness(you)
                if not r["ready"]:
                    return js(409, {"error": "required documents are missing", "readiness": r})
                return js(200, {**audit(year), "readiness": r})
            if path == "/api/export":
                return 200, export_csv(year), "text/csv; charset=utf-8", [
                    ("Content-Disposition", "attachment; filename=cbam_supplier_communication.csv")]
            if path == "/api/doc" and query.get("id") in docs:
                d = docs[query["id"]]
                safe = d["mime"] if d["mime"] == "application/pdf" or d["mime"].startswith("image/") else "text/plain; charset=utf-8"
                return 200, d["raw"], safe, []
        if method == "POST":
            body = body or {}
            if path == "/api/upload":
                if not body.get("filename") or not body.get("data"):
                    return js(400, {"error": "filename and data are required"})
                return js(200, add_doc(str(body["filename"])[:200], body.get("mime") or "text/plain", base64.b64decode(body["data"])))
            if path == "/api/demo":
                return js(200, [add_doc(f, "text/plain", open(os.path.join(HERE, "demo", f), "rb").read())
                                for f in sorted(os.listdir(os.path.join(HERE, "demo")))])
            if path in ("/api/log", "/api/demo_log"):
                for e in (DEMO_LOG if path == "/api/demo_log" else [body]):
                    add_log(you, e)
                return js(200, {"ok": True})
            if path == "/api/supplier":
                see = float(body.get("see"))
                if not body.get("name") or not 0 < see < 10:
                    return js(400, {"error": "a mill name and a value between 0 and 10 tCO2/t are required"})
                state["suppliers"][str(body["name"])] = {"verified": True, "see": see,
                                                         "report": str(body.get("report") or "Verification report (demo)")[:120]}
                return js(200, {"ok": True})
            if path == "/api/reset":
                state.clear(); state.update(copy.deepcopy(SEED)); docs.clear()
                return js(200, {"ok": True})
    except (TypeError, ValueError) as e:  # bad number, month, unit or base64 from the client
        return js(400, {"error": str(e)})
    return js(404, {"error": "not found"})


class H(BaseHTTPRequestHandler):
    def send(self, code, body, ctype="application/json", extra=()):
        data = body if isinstance(body, bytes) else body.encode() if isinstance(body, str) else json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("X-Content-Type-Options", "nosniff")
        for k, v in extra:
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(data)

    def route(self, method, body):
        u = urlparse(self.path)
        q = {k: v[0] for k, v in parse_qs(u.query).items()}
        self.send(*dispatch(method, u.path, q, body))

    def do_GET(self):
        u = urlparse(self.path)
        if u.path.startswith("/api/"):
            return self.route("GET", None)
        f = static_path(u.path)
        if not f:
            return self.send(404, {"error": "not found"})
        self.send(200, open(f, "rb").read(), CTYPES.get(os.path.splitext(f)[1], "application/octet-stream"))

    def do_POST(self):
        n = int(self.headers.get("Content-Length") or 0)
        if n > 15_000_000:
            return self.send(413, {"error": "file too large"})
        try:
            body = json.loads(self.rfile.read(n) or b"{}")
        except ValueError:
            return self.send(400, {"error": "body must be JSON"})
        self.route("POST", body)

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
