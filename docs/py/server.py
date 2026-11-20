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


DOC_TYPES = ("mtc", "steel_invoice", "fuel_invoice", "production", "other")
FUEL_NAMES, UNIT_NAMES = ("lpg", "diesel", "natural_gas"), ("t", "kg", "litre", "m3")
pos = lambda v: isinstance(v, (int, float)) and not isinstance(v, bool) and v > 0


def apply_record(p, doc_id, d):
    """Put one document's values into the plant. Returns why it was not used, or None."""
    rec, t = d["record"], d["record"]["doc_type"]
    src = {"doc": doc_id, "file": d["name"], "quote": rec.get("quote"), "edited": bool(d["edits"])}
    if t in ("mtc", "steel_invoice"):
        rows = [h for h in rec.get("heats") or [] if isinstance(h, dict) and (h.get("heat_no") or pos(h.get("tonnes")))]
        rows = rows or [{"heat_no": rec.get("heat_no"), "tonnes": rec.get("steel_tonnes")}]
        mill = rec.get("supplier") if t == "mtc" else None  # an invoice seller may be a trader, never the mill
        if not any(h.get("heat_no") or (mill and pos(h.get("tonnes"))) for h in rows):
            return "not used: no heat number"
        for i, h in enumerate(rows):
            add_heat(p, h.get("heat_no") or f"{doc_id}-{i}", mill, h.get("tonnes") if pos(h.get("tonnes")) else None, src, cn=h.get("cn") or rec.get("cn_code"))
    elif t == "fuel_invoice" and rec.get("fuel") in FUEL_NAMES and pos(rec.get("quantity")) and rec.get("unit") in UNIT_NAMES:
        p["fuel"].append({"fuel": rec["fuel"], "qty": rec["quantity"], "unit": rec["unit"], "source": src})
    elif t == "production" and pos(rec.get("output_tonnes")):
        p["output"].append({"tonnes": rec["output_tonnes"], "cn": rec.get("cn_code"), "source": src})
    else:
        return "not used: missing or invalid fields"
    return None


def rebuild():
    """The plant's document figures are always derived from the stored records, so a correction or a removal just replays them."""
    p = state["plants"][YOU]
    p.update(steel=[], fuel=[], output=[], heats={}, checks=[])
    for doc_id, d in docs.items():
        d["error"] = apply_record(p, doc_id, d)
    sync_steel(p)


def doc_result(doc_id):
    d = docs[doc_id]
    out = {"file": d["name"], "doc": doc_id, "mode": d["mode"], "record": d["record"]}
    return {**out, "error": d["error"]} if d["error"] else out


def add_doc(filename, mime, raw):
    same = next((d["name"] for d in docs.values() if d["raw"] == raw), None)
    if same:  # a second copy would count its fuel or output twice
        return {"file": filename, "error": f"already uploaded as {same}"}
    try:
        rec, how = extract(mime, raw)
    except Exception as e:
        return {"file": filename, "error": f"could not read: {e}"}
    doc_id = uuid.uuid4().hex[:8]
    docs[doc_id] = {"name": filename, "mime": mime, "raw": raw, "record": rec, "mode": how, "reviewed": False, "edits": [], "error": None}
    rebuild()
    return doc_result(doc_id)


def clean_record(patch):
    """Check a clerk's corrections. Raises ValueError on anything unsafe, so nothing is half-applied."""
    if not isinstance(patch, dict):
        raise ValueError("record must be an object")
    out = {}

    def text(k, n):
        if patch[k] is not None and not isinstance(patch[k], str):
            raise ValueError(f"{k} must be text")
        return (patch[k] or "")[:n] or None

    def num(v, k):
        if v is not None and not pos(v):
            raise ValueError(f"{k} must be a number above 0")
        return v
    for k in patch:
        if k == "doc_type":
            if patch[k] not in DOC_TYPES:
                raise ValueError("unknown document type")
            out[k] = patch[k]
        elif k in ("supplier", "heat_no", "cn_code"):
            out[k] = text(k, 120)
        elif k in ("steel_tonnes", "quantity", "output_tonnes"):
            out[k] = num(patch[k], k)
        elif k == "fuel":
            if patch[k] is not None and patch[k] not in FUEL_NAMES:
                raise ValueError("unknown fuel")
            out[k] = patch[k]
        elif k == "unit":
            if patch[k] is not None and patch[k] not in UNIT_NAMES:
                raise ValueError("unknown unit")
            out[k] = patch[k]
        elif k == "heats":
            if not isinstance(patch[k], list) or len(patch[k]) > 50 or not all(isinstance(h, dict) for h in patch[k]):
                raise ValueError("heats must be a list of heats")
            out[k] = [{"heat_no": (str(h.get("heat_no") or "")[:60] or None), "tonnes": num(h.get("tonnes"), "tonnes")} for h in patch[k]]
        else:
            raise ValueError(f"unknown field {k}")
    return out


def review(doc_id, patch):
    d = docs[doc_id]
    new = clean_record(patch or {})
    for k, v in new.items():
        if d["record"].get(k) != v:
            d["edits"].append({"field": k, "from": d["record"].get(k), "to": v})
            d["record"][k] = v
    d["reviewed"] = True
    rebuild()


def issues(d):
    out = [d["error"]] if d["error"] else []
    r = d["record"]
    if r["doc_type"] in ("mtc", "steel_invoice"):
        rows = [h for h in r.get("heats") or [] if isinstance(h, dict)] or [{"heat_no": r.get("heat_no"), "tonnes": r.get("steel_tonnes")}]
        heats = state["plants"][YOU]["heats"]
        loose = [h["heat_no"] for h in rows if h.get("heat_no") and not pos(h.get("tonnes"))
                 and "tonnes" not in heats.get(re.sub(r"[^A-Z0-9]", "", h["heat_no"].upper()), {})]
        if loose:
            out.append(f"No tonnes for heat {', '.join(loose)}. Type them here, or upload the invoice for it.")
    return out


def add_heat(p, key, mill, tonnes, src, cn=None):
    """One entry per heat. Mill comes from a certificate, tonnes from any document. Conflicts are flagged, never overwritten."""
    e = p["heats"].setdefault(re.sub(r"[^A-Z0-9]", "", key.upper()) or key, {"heat": key})  # "BR-148" == "br 148"
    if cn and "cn" not in e:
        e["cn"] = str(cn).strip()
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
                   "mill_source": e["mill_src"], "cn": e.get("cn")} for e in p["heats"].values() if "mill" in e and "tonnes" in e]
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
        return {"role": role, "file": s["file"], "doc": s.get("doc"), "quote": s.get("quote"), "edited": bool(s.get("edited"))} if s else None

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
    edits = [{"file": d["name"], **e} for d in docs.values() for e in d["edits"]]
    keys = ("name", "year", "output_t", "see_total", "see_direct", "see_precursor", "verified_share")
    return {"summary": {k: r[k] for k in keys}, "rows": rows,
            "review": {"documents": len(docs), "confirmed": sum(d["reviewed"] for d in docs.values()),
                       "edited": sum(bool(d["edits"]) for d in docs.values()), "edits": edits}, "plan": plan(p), "method": plan(p)["lines"],
            "checks": p["checks"] + log_checks(p),
            "default_note": f"Steel default used: {DEFAULT_PRECURSOR_SEE} tCO2/t before the mark-up, India wire rod (CN 7213), Implementing Regulation (EU) 2025/2621 as corrected by 2026/1740.",
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
        {"key": "review", "label": "Extracted values confirmed", "required": True,
         "done": bool(docs) and all(d["reviewed"] for d in docs.values()),
         "hint": f"{sum(not d['reviewed'] for d in docs.values())} of {len(docs)} documents still to confirm. Check each value against its file."
         if docs and not all(d["reviewed"] for d in docs.values()) else "Check what we read from each file, fix anything wrong, then confirm."},
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


def draft_mill_request(mill, year=2027):
    p = view(year)["plants"][0]
    m = next((x for x in p.get("precursors", []) if x["supplier"] == mill), None)
    if m is None:
        return {"error": f"{mill} does not supply this plant."}
    if m.get("basis") == "actual":
        return {"error": f"{mill} has already shared verified data."}
    heats = "\n".join(f"  - Heat {h['heat']}: {h['tonnes']:g} t" for h in m.get("heats", []))
    email = (f"Dear {mill} team,\n\n"
             f"Our EU buyers now need the embedded emissions of the steel in our goods under the EU carbon border "
             f"adjustment mechanism (CBAM). In the period we report, we used {m['tonnes']:g} t of your wire rod:\n{heats}\n\n"
             "Without your data, our buyers must use the EU default value plus a penalty mark-up.\n\n"
             "Could you share the embedded emissions of this steel, in tCO2 per tonne, with the verification "
             "report from an accredited verifier? A value for your plant and product route is enough.\n\n"
             "Every customer of yours that uses our system will be able to reuse it.\n\n"
             f"Regards,\n{p['name'].replace(' (your plant)', '')}")
    return {"mill": mill, "subject": f"Request for verified CBAM emissions data: {m['tonnes']:g} t of wire rod",
            "email": email}


def agent_review(year=2027):
    you = state["plants"][YOU]
    v = view(year)
    p_info = v["plants"][0]
    if p_info.get("empty"):
        return {
            "empty": True,
            "status": "No documents uploaded yet",
            "tco2_per_tonne": 0.0,
            "product_default": 5.72,
            "summary": "No plant documents have been uploaded yet. Upload mill test certificates, fuel invoices, and production records to begin the verifier audit.",
            "fixes": [],
            "questions": ["Please upload the plant's mill test certificates, fuel invoices, and annual production records."],
            "draft_email": None,
            "ready": False
        }

    total = p_info["see_total"]
    prod_dft = p_info["product_default"]
    open_gaps = v["plan"]["gaps"]
    doc_conflicts = v["checks"]
    unconfirmed = [d["name"] for d in docs.values() if not d.get("reviewed")]
    all_steel = sum(m["tonnes"] for m in p_info["precursors"]) or 1.0

    summary = (f"Plant emissions are currently {total:.2f} tCO2/t (EU goods default is {prod_dft:.2f} tCO2/t). "
               f"{(1 - p_info['verified_share'])*100:.0f}% of steel is on penalty default values.")

    fixes = []
    default_mills = [m for m in p_info["precursors"] if m["basis"] == "default"]
    default_mills.sort(key=lambda x: -x["tonnes"])
    top_mill_draft = None

    if default_mills:
        top_m = default_mills[0]
        share = (top_m["tonnes"] / all_steel) * 100
        fixes.append({
            "rank": 1,
            "category": "mill_data",
            "title": f"Chasing verified data from {top_m['supplier']}",
            "detail": f"{top_m['supplier']} supplies {top_m['tonnes']:g} t ({share:.0f}% of your steel) with no verified emissions data, triggering the EU default penalty. Moving this mill to actual data is your single biggest cost reduction.",
            "action": f"Send the pre-drafted data request email below to {top_m['supplier']}."
        })
        top_mill_draft = draft_mill_request(top_m["supplier"], year)

    rank = len(fixes) + 1
    fuel_gaps = [g for g in open_gaps if "purchase invoices" in g.lower()]
    if fuel_gaps:
        fuels = []
        if any("lpg" in g.lower() for g in fuel_gaps): fuels.append("LPG")
        if any("diesel" in g.lower() for g in fuel_gaps): fuels.append("diesel")
        fuel_names = " and ".join(fuels) if fuels else "fuel"
        fixes.append({
            "rank": rank,
            "category": "fuel_log",
            "title": f"Missing monthly stock logs for {fuel_names}",
            "detail": "Fuel purchase invoices show what was bought, but CBAM verifiers require physical consumption (opening stock + bought − closing stock).",
            "action": "Add monthly fuel tank/meter stock logs in the Monthly Log tab."
        })
        rank += 1

    prod_gaps = [g for g in open_gaps if "production log" in g.lower()]
    if prod_gaps:
        fixes.append({
            "rank": rank,
            "category": "production_log",
            "title": "Missing monthly production logs",
            "detail": "An annual dispatch summary was provided, but CBAM verifiers require monthly gross production tonnes.",
            "action": "Log monthly finished goods output in the Monthly Log tab."
        })
        rank += 1

    if unconfirmed:
        fixes.append({
            "rank": rank,
            "category": "unconfirmed_docs",
            "title": f"{len(unconfirmed)} document(s) pending clerk confirmation",
            "detail": f"Files like {', '.join(unconfirmed[:2])} have not been confirmed by a person. Verifiers require human sign-off on OCR values.",
            "action": "Confirm or edit all extracted fields in the Documents tab."
        })
        rank += 1

    if doc_conflicts:
        fixes.append({
            "rank": rank,
            "category": "document_conflict",
            "title": "Document conflicts detected",
            "detail": "; ".join(doc_conflicts),
            "action": "Resolve mismatched heat numbers or weights between mill certs and invoices."
        })

    question = None
    if fuel_gaps:
        question = "Do you maintain monthly fuel stock logs or only purchase invoices?"
    elif prod_gaps:
        question = "Do you keep monthly physical production logs for finished goods (nuts/bolts) or only annual dispatch records?"
    elif unconfirmed:
        question = "Have you verified the highlighted OCR values against the original paper certificates?"

    questions = [question] if question else []

    return {
        "empty": False,
        "plant": p_info["name"],
        "year": year,
        "tco2_per_tonne": total,
        "product_default": prod_dft,
        "verified_share": p_info["verified_share"],
        "summary": summary,
        "fixes": fixes,
        "question": question,
        "questions": questions,
        "draft_email": top_mill_draft,
        "tools_used": ["get_readiness", "get_documents", "get_plant", "draft_mill_request"],
        "ready": readiness(you)["ready"]
    }


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
            if path == "/api/agent/review":
                return js(200, agent_review(year))
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
            if path == "/api/dossier":
                return 200, export_dossier(year), "application/zip", [
                    ("Content-Disposition", f"attachment; filename=cbam_verifier_dossier_{year}.zip")]
            if path == "/api/docs":
                return js(200, [{"id": i, "name": d["name"], "mime": d["mime"], "mode": d["mode"], "record": d["record"],
                                 "reviewed": d["reviewed"], "edits": d["edits"], "issues": issues(d)} for i, d in docs.items()])
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
            if path in ("/api/review", "/api/doc_remove"):
                if body.get("doc") not in docs:
                    return js(404, {"error": "no such document"})
                if path == "/api/doc_remove":
                    del docs[body["doc"]]
                    rebuild()
                else:
                    review(body["doc"], body.get("record"))
                return js(200, {"ok": True})
            if path == "/api/review_all":
                for d in docs.values():
                    d["reviewed"] = True
                return js(200, {"ok": True})
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
        files = " + ".join(dict.fromkeys(x["file"] + (" (edited by clerk)" if x.get("edited") else "") for x in r["sources"]))
        w.writerow([r["item"], "" if r["tco2"] is None else r["tco2"], r["basis"], files, r["sources"][0].get("quote")])
    w.writerow([]); w.writerow(["Monitoring plan (draft)"])
    for l in a["method"]:
        w.writerow([l])
    w.writerow(["Open gaps"])
    for g in a["plan"]["gaps"]:
        w.writerow([g])
    return out.getvalue()


def export_dossier(year):
    import io, zipfile
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        rep = audit(year)
        ag = agent_review(year)
        you = state["plants"][YOU]
        dossier_data = {
            "dossier_type": "CBAM_ACCREDITED_VERIFIER_AUDIT_DOSSIER",
            "regulatory_framework": "Regulation (EU) 2023/956 & Implementing Regulation (EU) 2025/2621",
            "installation": you["name"],
            "reporting_year": year,
            "report_summary": rep.get("summary"),
            "audit_rows": rep.get("rows"),
            "plant_review": rep.get("review"),
            "open_checks": rep.get("checks"),
            "monitoring_plan_gaps": rep.get("plan", {}).get("gaps"),
            "review_agent_audit": ag
        }
        z.writestr("cbam_audit_trail.json", json.dumps(dossier_data, indent=2))
        z.writestr("cbam_supplier_communication.csv", export_csv(year))

        meth = [
            "CBAM INSTALLATION MONITORING METHODOLOGY",
            f"Installation: {you['name']}",
            f"Reporting Year: {year}",
            "Applicable Goods: Fasteners (CN 7318: Screws, Bolts, Nuts)",
            "",
            "1. Calculation Standard:",
            "  Specific Embedded Emissions (SEE) = Direct Emissions (Furnaces) + Precursor Emissions (Wire Rod)",
            "  LPG Direct Emission Factor: 2.985 tCO2/t",
            "  Diesel Direct Emission Factor: 3.186 tCO2/t (Density: 0.84 kg/L)",
            "  Non-Alloy Steel Wire Rod Default (CN 7213): 4.27 tCO2/t",
            "  Alloy Steel Wire Rod Default (CN 7227): 7.30 tCO2/t",
            "",
            "2. Specific Rules & Boundaries Applied:"
        ]
        meth += [f"  - {line}" for line in rep.get("method", [])]
        z.writestr("monitoring_methodology.txt", "\n".join(meth) + "\n")

        # Primary Evidence Documents
        for doc_id, d in docs.items():
            raw_bytes = d["raw"] if isinstance(d["raw"], bytes) else d["raw"].encode("utf-8", "replace")
            z.writestr(f"evidence_documents/{d['name']}", raw_bytes)

    return buf.getvalue()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"Open http://localhost:{port}  (extraction: {mode()})")
    ThreadingHTTPServer((os.environ.get("HOST", "127.0.0.1"), port), H).serve_forever()
