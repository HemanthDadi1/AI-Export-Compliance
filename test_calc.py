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

def test_steel_default_is_the_official_india_value():
    assert DEFAULT_PRECURSOR_SEE == 4.27  # Reg (EU) 2025/2621 Annex I, India, CN 7213, as corrected by 2026/1740


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

def test_curve_default_is_the_eu_default_for_the_goods():
    # Without supplier data, the importer uses the EU default for the good itself, not for its steel.
    bolts = plant([{"supplier": "X", "tonnes": 100}]); bolts["output"] = [{"tonnes": 100, "cn": "7318 15"}]
    c = compute(bolts, {}, 2027)["curve"]
    assert abs(c[1]["default"] - 5.72 * 1.2 * 0.05 * 75 * 1000) < 1e-6   # 2027: 20% mark-up, 5% payable
    assert abs(c[4]["default"] - 5.72 * 1.3 * 0.485 * 75 * 1000) < 1e-6  # 2030: 30% mark-up


def test_product_default_follows_the_cn_code_and_output_mix():
    p = plant([{"supplier": "X", "tonnes": 100}])
    p["output"] = [{"tonnes": 60, "cn": "731815 90"}, {"tonnes": 40, "cn": "7318 16"}]  # bolts and nuts
    r = compute(p, {}, 2026)
    assert abs(r["product_default"] - (0.6 * 5.72 + 0.4 * 5.14)) < 1e-9
    p["output"] = [{"tonnes": 100, "cn": None}]  # no CN code read: assume bolts
    assert compute(p, {}, 2026)["product_default"] == 5.72


def test_verified_mill_widens_the_gap_to_the_default():
    steel = [{"supplier": "X", "tonnes": 100}]
    a = compute(plant(steel), {}, 2027)["curve"]
    b = compute(plant(steel), {"X": {"verified": True, "see": 1.9}}, 2027)["curve"]
    assert all(y["default"] - y["yours"] > x["default"] - x["yours"] for x, y in zip(a, b))


def test_empty():
    assert compute({"id": "P", "name": "P", "steel": [], "fuel": [], "output": []}, {})["empty"]

if __name__ == "__main__":
    for n, f in list(globals().items()):
        if n.startswith("test_"): f()
    print("ok")
