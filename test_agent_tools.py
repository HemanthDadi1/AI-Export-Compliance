"""Review agent tools: right facts on the sample plant, and no tool changes anything. No model or key. Run: python3 test_agent_tools.py"""
import json, os
for k in ("GEMINI_API_KEY", "VERTEX_PROJECT"): os.environ.pop(k, None)  # rule parser, no network
import server
from agent import tools

call = lambda method, path, query=None, body=None: server.dispatch(method, path, query or {}, body)
RAYALASEEMA = "Rayalaseema Steel Rolling"


def sample_plant():
    assert call("POST", "/api/reset")[0] == 200
    call("POST", "/api/demo")
    call("POST", "/api/review_all")


def snapshot():
    return json.dumps([call("GET", p, {"year": "2027"})[1] for p in ("/api/state", "/api/docs", "/api/readiness", "/api/audit")], sort_keys=True)


def test_finds_the_four_open_checks():
    sample_plant()
    checks = tools.get_plant(2027)["open_checks"]
    assert len(checks) == 4
    for word in ("diesel", "lpg", "Output", RAYALASEEMA):
        assert sum(word in c for c in checks) == 1, word


def test_ranks_the_mill_with_most_steel_on_defaults_first():
    sample_plant()
    mills = tools.get_plant(2027)["mills"]
    top = mills[0]
    assert top["mill"] == RAYALASEEMA and top["basis"] == "default" and top["tonnes"] == 660
    assert abs(top["share_of_steel"] - 660 / 1040) < 1e-9
    assert all(m["basis"] == "actual" for m in mills[1:])


def test_plant_tool_shows_only_your_plant():
    sample_plant()
    p = tools.get_plant(2027)
    assert p["plant"].endswith("(your plant)") and round(p["tco2_per_tonne"], 2) == 4.38
    assert "Chennai Bolt Works" not in json.dumps(p)


def test_mill_request_names_the_mill_heats_and_tonnes():
    sample_plant()
    r = tools.draft_mill_request(RAYALASEEMA, 2027)
    for text in (RAYALASEEMA, "RSR-24-0412", "180", "660", "tCO2 per tonne", "verif"):
        assert text in r["email"], text
    assert r["subject"] and r["mill"] == RAYALASEEMA


def test_mill_request_refuses_unknown_or_verified_mills():
    sample_plant()
    assert "error" in tools.draft_mill_request("No Such Mill", 2027)
    assert "error" in tools.draft_mill_request("Kaveri Integrated Steel", 2027)  # already verified


def test_no_tool_changes_anything():
    sample_plant()
    before = snapshot()
    tools.get_readiness(); tools.get_documents(); tools.get_plant(2027); tools.get_audit(2027)
    tools.draft_mill_request(RAYALASEEMA, 2027); tools.draft_mill_request("No Such Mill", 2027)
    assert snapshot() == before


def test_every_tool_returns_json():
    sample_plant()
    for out in (tools.get_readiness(), tools.get_documents(), tools.get_plant(2027), tools.get_audit(2027),
                tools.draft_mill_request(RAYALASEEMA, 2027)):
        json.dumps(out)


if __name__ == "__main__":
    for n, f in list(globals().items()):
        if n.startswith("test_"): f()
    print("ok")
