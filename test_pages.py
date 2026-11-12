"""The browser build uses exact copies of the engine. Run: python3 test_pages.py (fix: python3 make_pages.py)"""
import filecmp, json, os
import make_pages as m

D = os.path.join(m.HERE, "docs")


def test_engine_copies_are_identical():
    for f in m.PY:
        assert filecmp.cmp(os.path.join(m.HERE, f), os.path.join(D, "py", f), shallow=False), f


def test_sample_documents_are_identical():
    for f in m.demo_files():
        assert filecmp.cmp(os.path.join(m.HERE, "demo", f), os.path.join(D, "demo", f), shallow=False), f


def test_manifest_lists_everything():
    man = json.load(open(os.path.join(D, "py", "manifest.json")))
    assert man == {"py": m.PY, "demo": m.demo_files()}


def test_pages_exist_and_link_up():
    for page in ("index.html", "app.html", "docs.html", "simulation.html"):
        assert os.path.isfile(os.path.join(D, page)), page
    home = open(os.path.join(D, "index.html")).read()
    assert "app.html" in home and "docs.html" in home


if __name__ == "__main__":
    for n, f in list(globals().items()):
        if n.startswith("test_"): f()
    print("ok")
