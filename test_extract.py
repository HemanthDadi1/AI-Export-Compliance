"""Checks the Gemini requests offline. Run: python3 test_extract.py"""
import io, json, os
import extract

sent = []
def fake_urlopen(req, timeout):
    sent.append(req)
    if "metadata" in req.full_url:
        return io.BytesIO(b'{"access_token": "tok"}')
    reply = {"candidates": [{"content": {"parts": [{"text": json.dumps({"doc_type": "mtc", "supplier": "RINL"})}]}}]}
    return io.BytesIO(json.dumps(reply).encode())
extract.urllib.request.urlopen = fake_urlopen


def run(env):
    for k in ("GEMINI_API_KEY", "VERTEX_PROJECT", "VERTEX_TOKEN", "VERTEX_LOCATION"): os.environ.pop(k, None)
    os.environ.update(env); sent.clear()
    return extract.extract("application/pdf", b"%PDF")


def test_vertex_on_cloud_run():
    rec, m = run({"VERTEX_PROJECT": "demo-proj"})
    meta, call = sent
    assert m == "vertex" and rec["supplier"] == "RINL"
    assert meta.get_header("Metadata-flavor") == "Google"
    assert call.full_url.startswith("https://asia-south1-aiplatform.googleapis.com/v1/projects/demo-proj/locations/asia-south1/")
    assert call.get_header("Authorization") == "Bearer tok"
    part = json.loads(call.data)["contents"][0]["parts"][1]
    assert part["inlineData"]["mimeType"] == "application/pdf"


def test_vertex_local_token():
    run({"VERTEX_PROJECT": "p", "VERTEX_TOKEN": "local"})
    assert len(sent) == 1 and sent[0].get_header("Authorization") == "Bearer local"


def test_gemini_api_key():
    _, m = run({"GEMINI_API_KEY": "k"})
    assert m == "gemini" and sent[0].get_header("X-goog-api-key") == "k" and "generativelanguage" in sent[0].full_url


def test_rules_without_config():
    rec, m = run({})
    assert m == "rules" and sent == []


if __name__ == "__main__":
    for n, f in list(globals().items()):
        if n.startswith("test_"): f()
    print("ok")
