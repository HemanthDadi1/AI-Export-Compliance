"""Rule-based CBAM calculation. No AI here. The final number comes only from this file."""

# India default for non-alloy wire rod (CN 7213), direct emissions, tCO2 per tonne, before the mark-up.
# Source: Implementing Regulation (EU) 2025/2621, Annex I (India), as corrected by 2026/1740. Checked on EUR-Lex, 13 Nov 2026.
# Non-alloy wire rod (CN 7213): 4.27, Alloy wire rod (CN 7227): 7.30
DEFAULT_PRECURSOR_SEE = 4.27
PRECURSOR_DEFAULTS = {"7213": 4.27, "7227": 7.30}
EUA_PRICE = 75.0             # EUR per tCO2, assumed flat


def precursor_see(cn=None):
    code = "".join(ch for ch in str(cn or "") if ch.isdigit())
    if code.startswith("7227"):
        return PRECURSOR_DEFAULTS["7227"]
    return PRECURSOR_DEFAULTS["7213"]

# India defaults for the finished goods (total emissions, before the mark-up), same source as above.
# An importer with no supplier data uses these. Keys are CN codes without spaces.
PRODUCT_DEFAULTS = {"731815": 5.72, "731816": 5.14, "731822": 5.14}
BOLTS = "731815"  # shortcut: goods with no or unknown CN code count as bolts, the demo's product

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


# Typical metallurgical yields for finished fastener goods (Annex V physical mass balance).
# Bolts: ~88% yield (12% scrap), Nuts: ~82% yield (18% scrap), Washers: ~90% yield (10% scrap).
YIELD_BENCHMARKS = {"731815": 0.88, "731816": 0.82, "731822": 0.90}


def product_default(output_lines):
    """EU default per tonne of goods, weighted by output. Matches the longest known CN prefix."""
    tot = sum(o["tonnes"] for o in output_lines)
    def per_t(cn):
        code = "".join(ch for ch in str(cn or "") if ch.isdigit())
        return next((v for k, v in PRODUCT_DEFAULTS.items() if code.startswith(k)), PRODUCT_DEFAULTS[BOLTS])
    return sum(o["tonnes"] * per_t(o.get("cn")) for o in output_lines) / tot


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
            sup = suppliers.get(name)
            for h in heats:
                t = h["tonnes"]
                see = sup["see"] if sup and sup["verified"] else precursor_see(h.get("cn")) * (1 + markup(y))
                tot += t * see
        return tot

    precursors = []
    for name, heats in by_sup.items():
        t = sum(h["tonnes"] for h in heats)
        sup = suppliers.get(name)
        actual = bool(sup and sup["verified"])
        is_alloy = any(str(h.get("cn") or "").startswith("7227") for h in heats)
        base_dft = PRECURSOR_DEFAULTS["7227"] if is_alloy else PRECURSOR_DEFAULTS["7213"]
        see = sup["see"] if actual else base_dft * (1 + markup(year))
        tco2 = sum(h["tonnes"] * (sup["see"] if actual else precursor_see(h.get("cn")) * (1 + markup(year))) for h in heats)
        cn = "7227" if is_alloy else "7213"
        precursors.append({"supplier": name, "tonnes": t, "basis": "actual" if actual else "default",
                           "see": see, "tco2": tco2, "heats": heats, "cn": cn,
                           "report": sup.get("report") if actual else None})

    def see_total(y):
        return (direct + precursor_total(y)) / output

    goods_default = product_default(plant["output"])
    curve = []
    for y in range(2026, 2035):
        curve.append({"year": y, "yours": see_total(y) * PAYABLE[y] * price * 1000,
                      "default": goods_default * (1 + markup(y)) * PAYABLE[y] * price * 1000})  # EUR for 1,000 t

    steel_t = sum(p["tonnes"] for p in precursors)
    yield_ratio = round(output / steel_t, 4) if steel_t > 0 else 1.0
    specific_consumption = round(steel_t / output, 4) if output > 0 else 1.0
    scrap_t = round(max(0.0, steel_t - output), 2)
    scrap_rate = round(scrap_t / steel_t, 4) if steel_t > 0 else 0.0

    # Sub-installation route modeling (Annex V Activity-Based Allocation)
    # Heat-treated products carry the continuous furnace emissions; cold-formed products bypass thermal furnaces.
    ht_lines = [o for o in plant["output"] if o.get("route") != "cold_formed"]
    cf_lines = [o for o in plant["output"] if o.get("route") == "cold_formed"]
    ht_output = sum(o["tonnes"] for o in ht_lines)
    cf_output = sum(o["tonnes"] for o in cf_lines)
    has_routing = cf_output > 0

    routes = {}
    if has_routing:
        see_dir_ht = (direct / ht_output) if ht_output > 0 else 0.0
        routes["heat_treated"] = {"output_t": ht_output, "see_direct": round(see_dir_ht, 4)}
        routes["cold_formed"] = {"output_t": cf_output, "see_direct": 0.0}

    # Primary CN benchmark
    first_cn = "".join(ch for ch in str(plant["output"][0].get("cn") or "") if ch.isdigit())[:6] or BOLTS
    bench = YIELD_BENCHMARKS.get(first_cn, 0.88)

    mass_balance = {
        "valid": steel_t >= (output * 0.95),  # allow 5% tolerance for opening inventory
        "steel_input_t": steel_t,
        "finished_output_t": output,
        "yield_ratio": yield_ratio,
        "benchmark_yield": bench,
        "scrap_t": scrap_t,
        "scrap_rate": scrap_rate,
        "specific_consumption": specific_consumption,
        "status": "healthy" if (0.70 <= yield_ratio <= 1.05) else ("under_input" if yield_ratio > 1.05 else "high_scrap")
    }

    return {"id": plant["id"], "name": plant["name"], "empty": False, "year": year,
            "output_t": output, "direct_tco2": direct, "direct_lines": direct_lines,
            "precursors": precursors, "see_direct": direct / output,
            "see_precursor": precursor_total(year) / output, "see_total": see_total(year),
            "verified_share": sum(p["tonnes"] for p in precursors if p["basis"] == "actual") / steel_t if steel_t else 0,
            "product_default": goods_default, "curve": curve,
            "mass_balance": mass_balance, "routes": routes}
