"""Builds the GitHub Pages demo (docs/demo.js) from the real engine. Run: python3 make_demo_snapshot.py"""
import copy, json, os, shutil
for k in ("GEMINI_API_KEY", "VERTEX_PROJECT"): os.environ.pop(k, None)  # rule parser, no network
import server
from calc import compute

HERE = os.path.dirname(os.path.abspath(__file__))
MILL, MILL_SEE = "Rayalaseema Steel Rolling", 1.9


def load_demo(verified):
    server.state.clear(); server.state.update(copy.deepcopy(server.SEED)); server.docs.clear()
    for f in sorted(os.listdir(os.path.join(HERE, "demo"))):
        server.add_doc(f, "text/plain", open(os.path.join(HERE, "demo", f), "rb").read())
    for e in server.DEMO_LOG:
        server.add_log(server.state["plants"][server.YOU], e)
    if verified:
        server.state["suppliers"][MILL] = {"verified": True, "see": MILL_SEE, "report": "Verification report RSR-2026-031 (demo)"}


def build():
    out = {"mill": MILL, "see": MILL_SEE, "states": {}}
    for name in ("before", "after"):
        load_demo(name == "after")
        years = {}
        for y in range(2026, 2035):
            plants = []
            for p in server.state["plants"].values():
                r = compute(server.effective(p), server.state["suppliers"], y)
                plants.append({k: r[k] for k in ("id", "name", "see_total", "see_direct", "see_precursor", "verified_share")})
            a = server.audit(y)
            for row in a["rows"]:
                for s in row["sources"]:
                    s.pop("doc", None)  # upload ids are random per run
            years[str(y)] = {"plants": plants, "audit": a}
        you = compute(server.effective(server.state["plants"][server.YOU]), server.state["suppliers"], 2027)
        out["states"][name] = {"years": years, "curve": you["curve"]}
    return out


if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "docs", "demo"), exist_ok=True)
    for f in os.listdir(os.path.join(HERE, "demo")):
        shutil.copy(os.path.join(HERE, "demo", f), os.path.join(HERE, "docs", "demo", f))
    data = json.loads(json.dumps(build()))
    open(os.path.join(HERE, "docs", "demo.js"), "w").write("window.DEMO = " + json.dumps(data, sort_keys=True, indent=1) + ";\n")
    print("wrote docs/demo.js")
