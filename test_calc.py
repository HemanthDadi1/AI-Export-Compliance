from calc import *

def plant(steel):
    return {"id": "P", "name": "P", "steel": steel, "fuel": [{"fuel": "lpg", "qty": 100, "unit": "t"}],
            "output": [{"tonnes": 100}]}

def test_fuel():
    assert abs(fuel_tco2("lpg", 1, "t") - 2.985) < 1e-9
    assert abs(fuel_tco2("diesel", 1000, "litre") - 0.84 * 3.186) < 1e-9
    for bad in [("coal", 1, "t"), ("lpg", 1, "gallon"), ("natural_gas", 1, "t")]:
        try: fuel_tco2(*bad); assert False
        except ValueError: pass

def test_default_has_markup():
    r = compute(plant([{"supplier": "X", "tonnes": 100}]), {}, 2027)
    assert abs(r["see_precursor"] - DEFAULT_PRECURSOR_SEE * 1.2) < 1e-9
    assert r["verified_share"] == 0

def test_verified_supplier_lowers_see():
    steel = [{"supplier": "X", "tonnes": 100}]
    a = compute(plant(steel), {}, 2027)["see_total"]
    b = compute(plant(steel), {"X": {"verified": True, "see": 1.9}}, 2027)
    assert abs(b["see_precursor"] - 1.9) < 1e-9 and b["see_total"] < a and b["verified_share"] == 1

def test_curve():
    c = compute(plant([{"supplier": "X", "tonnes": 100}]), {}, 2027)["curve"]
    assert c[0]["year"] == 2026 and c[-1]["year"] == 2034 and c[-1]["yours"] > c[0]["yours"]

def test_curve_default_means_steel_on_defaults():
    steel = [{"supplier": "X", "tonnes": 100}]
    none = compute(plant(steel), {}, 2027)["curve"]
    assert all(abs(c["yours"] - c["default"]) < 1e-6 for c in none)  # no verified mill, so the two lines match
    ver = compute(plant(steel), {"X": {"verified": True, "see": 1.9}}, 2027)["curve"]
    assert all(v["yours"] < v["default"] for v in ver)
    # 2030: (30 t of LPG fuel... direct 298.5 + 100 t steel at default with 30% markup) / 100 t output * 48.5% * EUR 75 * 1000 t
    want = (298.5 + 100 * DEFAULT_PRECURSOR_SEE * 1.3) / 100 * 0.485 * 75 * 1000
    assert abs(none[4]["default"] - want) < 1e-6


def test_empty():
    assert compute({"id": "P", "name": "P", "steel": [], "fuel": [], "output": []}, {})["empty"]

if __name__ == "__main__":
    for n, f in list(globals().items()):
        if n.startswith("test_"): f()
    print("ok")
