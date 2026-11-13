"""Rule-based CBAM calculation. No AI here. The final number comes only from this file."""

# India default for non-alloy wire rod (CN 7213), direct emissions, tCO2 per tonne, before the mark-up.
# Source: Implementing Regulation (EU) 2025/2621, Annex I (India), as corrected by 2026/1740. Checked on EUR-Lex, 13 Nov 2026.
# shortcut: one value for all steel. Alloy wire rod (CN 7227) is 7.30, so alloy-steel bolts need a second value.
DEFAULT_PRECURSOR_SEE = 4.27
EUA_PRICE = 75.0             # EUR per tCO2, assumed flat

# Share of the CBAM charge that is payable, by year.
PAYABLE = {2026: .025, 2027: .05, 2028: .10, 2029: .225, 2030: .485,
           2031: .61, 2032: .735, 2033: .86, 2034: 1.0}
MARKUP = {2026: .10, 2027: .20}  # penalty on default values; 30% from 2028

# fuel: (tCO2 per tonne, density kg/litre). Natural gas is per m3 only.
FUELS = {"lpg": (2.985, 0.54), "diesel": (3.186, 0.84)}
NG_PER_M3 = 0.00195


def markup(year):
    return MARKUP.get(year, .30)


def fuel_tco2(fuel, qty, unit):
    if fuel == "natural_gas":
        if unit != "m3":
            raise ValueError("natural gas needs m3")
        return qty * NG_PER_M3
    if fuel not in FUELS:
        raise ValueError(f"unknown fuel {fuel}")
    per_t, dens = FUELS[fuel]
    tonnes = {"t": qty, "kg": qty / 1000, "litre": qty * dens / 1000}.get(unit)
    if tonnes is None:
        raise ValueError(f"unknown unit {unit}")
    return tonnes * per_t


def compute(plant, suppliers, year=2027, price=EUA_PRICE):
    """plant: {id, name, steel[], fuel[], output[]}. suppliers: {name: {verified, see, report}}."""
    output = sum(o["tonnes"] for o in plant["output"])
    if output <= 0:
        return {"id": plant["id"], "name": plant["name"], "empty": True}

    direct_lines = [{**f, "tco2": fuel_tco2(f["fuel"], f["qty"], f["unit"])} for f in plant["fuel"]]
    direct = sum(l["tco2"] for l in direct_lines)

    by_sup = {}
    for s in plant["steel"]:
        by_sup.setdefault(s["supplier"], []).append(s)

    def precursor_total(y):
        tot = 0.0
        for name, heats in by_sup.items():
            t = sum(h["tonnes"] for h in heats)
            sup = suppliers.get(name)
            see = sup["see"] if sup and sup["verified"] else DEFAULT_PRECURSOR_SEE * (1 + markup(y))
            tot += t * see
        return tot

    precursors = []
    for name, heats in by_sup.items():
        t = sum(h["tonnes"] for h in heats)
        sup = suppliers.get(name)
        actual = bool(sup and sup["verified"])
        see = sup["see"] if actual else DEFAULT_PRECURSOR_SEE * (1 + markup(year))
        precursors.append({"supplier": name, "tonnes": t, "basis": "actual" if actual else "default",
                           "see": see, "tco2": t * see, "heats": heats,
                           "report": sup.get("report") if actual else None})

    def see_total(y):
        return (direct + precursor_total(y)) / output

    curve = []
    for y in range(2026, 2035):
        ours = see_total(y)
        dflt = (direct + sum(p["tonnes"] for p in precursors) * DEFAULT_PRECURSOR_SEE * (1 + markup(y))) / output
        curve.append({"year": y, "yours": ours * PAYABLE[y] * price * 1000,
                      "default": dflt * PAYABLE[y] * price * 1000})  # EUR for 1,000 t. "default" = all steel on defaults

    steel_t = sum(p["tonnes"] for p in precursors)
    return {"id": plant["id"], "name": plant["name"], "empty": False, "year": year,
            "output_t": output, "direct_tco2": direct, "direct_lines": direct_lines,
            "precursors": precursors, "see_direct": direct / output,
            "see_precursor": precursor_total(year) / output, "see_total": see_total(year),
            "verified_share": sum(p["tonnes"] for p in precursors if p["basis"] == "actual") / steel_t if steel_t else 0,
            "curve": curve}
