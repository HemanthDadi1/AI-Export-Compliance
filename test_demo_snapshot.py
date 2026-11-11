"""The GitHub Pages demo is built from the real engine. Run: python3 test_demo_snapshot.py"""
import json, os
import make_demo_snapshot as m


def committed():
    s = open(os.path.join(m.HERE, "docs", "demo.js")).read()
    return json.loads(s[s.index("{"): s.rindex("}") + 1])


def test_snapshot_is_current():
    # Fails when the engine, the demo files or the seed data change. Fix: python3 make_demo_snapshot.py
    assert json.loads(json.dumps(m.build())) == committed()


def test_story_numbers():
    d = committed()
    before, after = (d["states"][k]["years"]["2027"]["plants"] for k in ("before", "after"))
    assert [round(p["see_total"], 2) for p in before] == [4.39, 4.65, 5.53, 5.42]
    assert [round(p["see_total"], 2) for p in after] == [2.24, 2.14, 2.13, 3.50]


def test_every_row_has_a_source_file_that_ships():
    d = committed()
    for state in d["states"].values():
        for y in state["years"].values():
            for r in y["audit"]["rows"]:
                assert r["sources"]
                for s in r["sources"]:
                    assert s["file"] and "doc" not in s  # random upload ids must not leak into the page
                    if s["file"].endswith(".txt"):
                        assert os.path.exists(os.path.join(m.HERE, "docs", "demo", s["file"]))


if __name__ == "__main__":
    for n, f in list(globals().items()):
        if n.startswith("test_"): f()
    print("ok")
