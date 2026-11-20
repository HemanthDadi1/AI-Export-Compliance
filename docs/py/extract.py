"""Reads one document into one record. Gemini on Vertex AI (VERTEX_PROJECT) or the Gemini API (GEMINI_API_KEY), else a simple rule parser for the demo files."""
import base64, json, os, re, urllib.request

FIELDS = ["doc_type", "supplier", "heat_no", "steel_tonnes", "heats", "fuel", "quantity", "unit",
          "output_tonnes", "cn_code", "quote"]

PROMPT = """You read documents from an Indian fastener plant for EU CBAM reporting.
Return one JSON object with these keys (null when not present):
doc_type: "mtc" (mill or material test certificate), "steel_invoice" (steel purchase invoice), "fuel_invoice", "production", or "other"
supplier: on an MTC certificate, the primary steel mill that melted the steel (look for "Steel Mill", "Producer", "Melted by", or the mill letterhead, e.g. RINL, Tata Steel, JSW, SAIL, Rayalaseema, Kaveri; do NOT use the inspection agency, fabricator, or trader); on an invoice, the seller
heat_no: heat number on a mill test certificate (if multiple heats, use the first heat number or comma-separated)
steel_tonnes: total steel quantity in metric tonnes as a number (convert kg to tonnes: 1 MT = 1 tonne = 1,000 kg. Indian digit grouping: 1,00,000 kg = 100 t, 52,340 kg = 52.34 t)
heats: list of {"heat_no": string, "tonnes": float or null}, one per heat row in table; convert individual heat kg to tonnes. If only piece counts or coil counts are given without weight (e.g. 41 coils, 18500 pcs), set tonnes to null
fuel: "lpg", "diesel" or "natural_gas"
quantity: fuel quantity as a number
unit: "t", "kg", "litre" or "m3"
output_tonnes: finished product tonnes on a production or dispatch record
cn_code: CN or HS code if printed (e.g. 7318 15, 7213)
quote: the exact short text the main figure came from
Do not guess numbers that are not on the document."""


def mode():
    if os.environ.get("VERTEX_PROJECT"):
        return "vertex"
    return "gemini" if os.environ.get("GEMINI_API_KEY") else "rules"


def _normalize_num(v, to_tonnes_if_kg=False):
    if v is None:
        return None
    if isinstance(v, (int, float)):
        val = float(v)
    elif isinstance(v, str):
        s = v.strip().replace(",", "")
        m = re.search(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", s)
        if not m:
            return None
        val = float(m.group(0))
        if "kg" in s.lower() and val > 0:
            val = val / 1000.0
            return val
    else:
        return None
    if to_tonnes_if_kg and val >= 10000.0:
        val = val / 1000.0
    return val


def _normalize_record(rec):
    if not isinstance(rec, dict):
        return {}
    out = dict(rec)

    # Normalization of doc_type
    dt = (out.get("doc_type") or "").strip().lower()
    if "cert" in dt or "mtc" in dt or "mill" in dt:
        out["doc_type"] = "mtc"
    elif "invoice" in dt and "steel" in dt:
        out["doc_type"] = "steel_invoice"
    elif "fuel" in dt:
        out["doc_type"] = "fuel_invoice"
    elif "prod" in dt or "dispatch" in dt:
        out["doc_type"] = "production"

    # Numeric fields
    out["steel_tonnes"] = _normalize_num(out.get("steel_tonnes"), to_tonnes_if_kg=True)
    out["quantity"] = _normalize_num(out.get("quantity"))
    out["output_tonnes"] = _normalize_num(out.get("output_tonnes"), to_tonnes_if_kg=False)

    # Multi-heat table normalization
    heats = out.get("heats")
    if isinstance(heats, list):
        cleaned_heats = []
        for h in heats:
            if isinstance(h, dict):
                h_no = str(h.get("heat_no") or h.get("heat") or "").strip() or None
                t = _normalize_num(h.get("tonnes") or h.get("tonnage") or h.get("weight"), to_tonnes_if_kg=True)
                cleaned_heats.append({"heat_no": h_no, "tonnes": t})
        out["heats"] = cleaned_heats
        if not out["steel_tonnes"]:
            t_sum = sum(h["tonnes"] for h in cleaned_heats if h.get("tonnes"))
            if t_sum > 0:
                out["steel_tonnes"] = round(t_sum, 4)

    # Normalize fuel & unit
    if out.get("fuel"):
        f = str(out["fuel"]).strip().lower().replace(" ", "_")
        out["fuel"] = f if f in ("lpg", "diesel", "natural_gas") else None
    if out.get("unit"):
        u = str(out["unit"]).strip().lower()
        if u in ("mt", "tonne", "tonnes", "t"): out["unit"] = "t"
        elif u in ("kg", "kgs", "kilogram", "kilograms"): out["unit"] = "kg"
        elif u in ("l", "ltr", "litre", "litres", "liter", "liters"): out["unit"] = "litre"
        elif u in ("m3", "cum", "cu.m"): out["unit"] = "m3"

    return out


def extract(mime, raw):
    m = mode()
    rec = _rules(raw.decode("utf-8", "replace")) if m == "rules" else _gemini(m, mime, raw)
    rec = _normalize_record(rec)
    return {k: rec.get(k) for k in FIELDS}, m


def _vertex_token():
    # Local: VERTEX_TOKEN from `gcloud auth print-access-token`. Cloud Run: the service account via the metadata server.
    if os.environ.get("VERTEX_TOKEN"):
        return os.environ["VERTEX_TOKEN"]
    req = urllib.request.Request("http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token",
                                 headers={"Metadata-Flavor": "Google"})
    with urllib.request.urlopen(req, timeout=5) as r:
        return json.load(r)["access_token"]


def _gemini_call_model(model, m, mime, raw):
    part = ({"text": raw.decode("utf-8", "replace")} if mime.startswith("text/")
            else {"inlineData": {"mimeType": mime, "data": base64.b64encode(raw).decode()}})
    body = {"contents": [{"role": "user", "parts": [{"text": PROMPT}, part]}],
            "generationConfig": {"responseMimeType": "application/json", "temperature": 0}}
    if m == "vertex":
        proj, loc = os.environ["VERTEX_PROJECT"], os.environ.get("VERTEX_LOCATION", "asia-south1")
        url = f"https://{loc}-aiplatform.googleapis.com/v1/projects/{proj}/locations/{loc}/publishers/google/models/{model}:generateContent"
        auth = {"Authorization": f"Bearer {_vertex_token()}"}
    else:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
        auth = {"x-goog-api-key": os.environ["GEMINI_API_KEY"]}
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers={"Content-Type": "application/json", **auth})
    with urllib.request.urlopen(req, timeout=60) as r:
        text = json.load(r)["candidates"][0]["content"]["parts"][0]["text"]
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip())
    out = json.loads(text)
    return out[0] if isinstance(out, list) else out


_AVAILABLE_MODELS = None


def _get_api_models():
    """Discover which Gemini models are available and enabled for the current API key."""
    global _AVAILABLE_MODELS
    if _AVAILABLE_MODELS is not None:
        return _AVAILABLE_MODELS
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        return []
    try:
        url = "https://generativelanguage.googleapis.com/v1beta/models"
        req = urllib.request.Request(url, headers={"x-goog-api-key": key})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.load(r)
        models = [m["name"].replace("models/", "") for m in data.get("models", [])
                  if "generateContent" in m.get("supportedGenerationMethods", [])]
        flash = [m for m in models if "flash" in m]
        pro = [m for m in models if "pro" in m]
        other = [m for m in models if m not in flash and m not in pro]
        _AVAILABLE_MODELS = flash + pro + other
        return _AVAILABLE_MODELS
    except Exception:
        return []


def _gemini(m, mime, raw):
    import time
    primary_model = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
    candidates = [primary_model]
    for alt in ("gemini-2.0-flash", "gemini-1.5-flash-latest", "gemini-1.5-flash-002", "gemini-1.5-flash", "gemini-1.5-pro"):
        if alt not in candidates:
            candidates.append(alt)

    last_err = None
    discovered = False
    idx = 0
    while idx < len(candidates):
        model = candidates[idx]
        idx += 1
        for attempt in range(2):
            try:
                return _gemini_call_model(model, m, mime, raw)
            except urllib.error.HTTPError as e:
                last_err = e
                # If 503 (overloaded) or 429 (rate limited), sleep briefly and retry
                if e.code in (429, 503):
                    time.sleep(1.5 * (attempt + 1))
                    continue
                # If 404 (model not found) and haven't discovered yet, query enabled models
                if e.code == 404 and not discovered and m != "vertex":
                    discovered = True
                    for discovered_model in _get_api_models():
                        if discovered_model not in candidates:
                            candidates.append(discovered_model)
                break
            except Exception as e:
                last_err = e
                break

    msg = str(last_err)
    if hasattr(last_err, "read"):
        try:
            msg = json.loads(last_err.read().decode("utf-8", "replace"))["error"]["message"]
        except Exception:
            pass
    code = getattr(last_err, "code", "Error")
    raise RuntimeError(f"Gemini extraction failed ({code}): {msg}. Tried models: {', '.join(candidates[:5])}")


def _rules(text):
    # shortcut: only reads the "Key: value" demo format. Real files need Gemini.
    kv = dict((k.strip().lower(), v.strip()) for k, v in re.findall(r"^([^:\n]+):(.+)$", text, re.M))
    num = lambda s: float(re.sub(r"[^\d.]", "", s)) if s and re.search(r"\d", s) else None
    qty = kv.get("quantity", "")
    unit = qty.split()[-1].lower() if qty else None
    return {"doc_type": kv.get("document"), "supplier": kv.get("supplier"), "heat_no": kv.get("heat no"),
            "steel_tonnes": num(kv.get("steel (t)")), "fuel": (kv.get("fuel") or "").lower().replace(" ", "_") or None,
            "quantity": num(qty), "unit": unit, "output_tonnes": num(kv.get("output (t)")),
            "cn_code": kv.get("cn code"),
            "quote": next((l for l in text.splitlines() if re.search(r"\(t\)|quantity", l, re.I)), None)}
