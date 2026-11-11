"""Network-effect simulation. Run: python3 test_simulation.py"""
import json, os
import simulate as sim
from calc import compute


def committed():
    s = open(os.path.join(sim.HERE, "docs", "simulation.js")).read()
    return json.loads(s[s.index("{"): s.rindex("}") + 1])


def test_fast_path_matches_the_real_engine():
    m = sim.build_market(1, 1.0)
    suppliers = {name: {"verified": True, "see": see} for i, (name, see) in enumerate(sorted(m["mill_see"].items())) if i % 3 == 0}
    for p in m["plants"]:
        want = compute(p, suppliers, 2030)["see_total"]
        assert abs(sim.see_of(p, suppliers, 2030) - want) < 1e-9


def test_verifying_more_mills_never_raises_the_average():
    m = sim.build_market(2, 1.0)
    suppliers, last = {}, None
    for name in sorted(m["mill_see"]):
        suppliers[name] = {"verified": True, "see": m["mill_see"][name]}
        avg = sum(sim.see_of(p, suppliers, 2030) * p["output"][0]["tonnes"] for p in m["plants"])
        assert last is None or avg <= last + 1e-9
        last = avg


def test_same_seed_same_result():
    assert sim.run(3, 1.0, 0.25) == sim.run(3, 1.0, 0.25)


def test_no_mill_joins_means_no_gain():
    r = sim.run(4, 1.0, 0.0)
    assert all(mo["share_verified"] == 0 and mo["drop_pct"] == 0 and mo["mills_verified"] == 0 for mo in r["months"])
    assert r["months"][-1]["plants"] == sim.DEFAULTS["plants"] and r["months"][0]["plants"] == 0


def test_concentrated_mills_are_covered_faster():
    top5 = lambda zipf: sorted(sim.run(s, zipf, 0.25)["coverage"][4] for s in range(1, 11))[5]
    assert top5(1.5) > top5(0.5)


def test_snapshot_is_current():
    # Fails when the engine or the assumptions change. Fix: python3 simulate.py --write
    assert json.loads(json.dumps(sim.build())) == committed()


def test_snapshot_shape():
    d = committed()
    assert len(d["scenarios"]) == 9
    for sc in d["scenarios"].values():
        assert len(sc["months"]) == sim.DEFAULTS["months"] + 1 and len(sc["coverage"]) == sim.DEFAULTS["mills"]


if __name__ == "__main__":
    for n, f in list(globals().items()):
        if n.startswith("test_"): f()
    print("ok")
