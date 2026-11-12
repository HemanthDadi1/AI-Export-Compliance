"""Reads one document into one record. Gemini on Vertex AI (VERTEX_PROJECT) or the Gemini API (GEMINI_API_KEY), else a simple rule parser for the demo files."""
import base64, json, os, re, urllib.request

FIELDS = ["doc_type", "supplier", "heat_no", "steel_tonnes", "heats", "fuel", "quantity", "unit",
          "output_tonnes", "cn_code", "quote"]

PROMPT = """You read documents from an Indian fastener plant for EU CBAM reporting.
Return one JSON object with these keys (null when not present):
doc_type: "mtc" (mill or material test certificate), "steel_invoice" (steel purchase invoice), "fuel_invoice", "production", or "other"
supplier: on a certificate, the steel mill that melted the steel (use a "Steel Mill" field if present, not the certificate issuer); otherwise the seller
heat_no: heat number on a mill test certificate
steel_tonnes: total steel quantity in tonnes (convert kg to t; Indian grouping like 1,00,000 kg = 100 t)
heats: list of {"heat_no", "tonnes"}, one per heat row; tonnes is null when only pieces are given
fuel: "lpg", "diesel" or "natural_gas"
quantity: fuel quantity as printed
unit: "t", "kg", "litre" or "m3"
output_tonnes: finished product tonnes on a production or dispatch record
cn_code: CN or HS code if printed
quote: the exact short text the main figure came from
Do not guess numbers that are not on the document."""


def mode():
    if os.environ.get("VERTEX_PROJECT"):
        return "vertex"
    return "gemini" if os.environ.get("GEMINI_API_KEY") else "rules"


def extract(mime, raw):
    m = mode()
    rec = _rules(raw.decode("utf-8", "replace")) if m == "rules" else _gemini(m, mime, raw)
    return {k: rec.get(k) for k in FIELDS}, m


def _vertex_token():
    # Local: VERTEX_TOKEN from `gcloud auth print-access-token`. Cloud Run: the service account via the metadata server.
    if os.environ.get("VERTEX_TOKEN"):
        return os.environ["VERTEX_TOKEN"]
    req = urllib.request.Request("http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token",
                                 headers={"Metadata-Flavor": "Google"})
    with urllib.request.urlopen(req, timeout=5) as r:
        return json.load(r)["access_token"]


def _gemini(m, mime, raw):
    model = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
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
    out = json.loads(text)
    return out[0] if isinstance(out, list) else out


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
