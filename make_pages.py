"""Copies the Python engine and the sample documents into docs/ so the app runs in the browser on GitHub Pages.
Run after changing calc.py, extract.py, server.py or demo/: python3 make_pages.py"""
import json, os, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
PY = ["calc.py", "extract.py", "server.py"]


def demo_files():
    return sorted(os.listdir(os.path.join(HERE, "demo")))


if __name__ == "__main__":
    for d in ("py", "demo"):
        os.makedirs(os.path.join(HERE, "docs", d), exist_ok=True)
    for f in PY:
        shutil.copy(os.path.join(HERE, f), os.path.join(HERE, "docs", "py", f))
    for f in demo_files():
        shutil.copy(os.path.join(HERE, "demo", f), os.path.join(HERE, "docs", "demo", f))
    json.dump({"py": PY, "demo": demo_files()}, open(os.path.join(HERE, "docs", "py", "manifest.json"), "w"), indent=1)
    print("copied", len(PY), "engine files and", len(demo_files()), "sample documents into docs/")
