"""Network-effect simulation: how fast does verifying mills put plants' steel on actual values?

Run: python3 simulate.py          prints a summary
     python3 simulate.py --write  rebuilds docs/simulation.js for the GitHub Pages page
Every input below is our assumption, not data. Change DEFAULTS and rerun.
"""
import json, math, os, random, sys
from calc import DEFAULT_PRECURSOR_SEE, EUA_PRICE, PAYABLE, fuel_tco2, markup

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULTS = {
    "plants": 150,        # plants on the platform after 24 months (the base case in the business plan)
    "mills": 40,          # steel mills they buy from
    "months": 24,
    "median_t": 500,      # steel a plant buys in a year, tonnes (median)
    "sigma": 0.6,         # spread of plant size (lognormal)
    "yield": 0.96,        # tonnes of bolts made per tonne of steel
    "lpg_per_t": 0.056,   # tonnes of LPG per tonne of bolts, like the demo plant
    "pull": 2,            # a mill is approached once this many of our plants buy from it
    "see_lo": 1.6, "see_hi": 2.6,  # verified mill value, tCO2 per t of steel, drawn per mill
    "year": 2030,         # reporting year used for default values and the payable share
    "seeds": 40,
}
ZIPF = {"spread": 0.5, "typical": 1.0, "concentrated": 1.5}   # how unevenly plants cluster on a few mills
JOIN = {"slow": 0.10, "medium": 0.25, "fast": 0.50}           # chance per month that an approached mill joins


def build_market(seed, zipf, d=DEFAULTS):
    rng = random.Random(seed)
    names = [f"Mill {i + 1}" for i in range(d["mills"])]
    weights = [1 / (i + 1) ** zipf for i in range(d["mills"])]
    mill_see = {n: rng.uniform(d["see_lo"], d["see_hi"]) for n in names}
    plants = []
    for i in range(d["plants"]):
        picked = []
        for _ in range(rng.choice([1, 2, 2, 3])):
            m = rng.choices(names, weights)[0]
            if m not in picked:
                picked.append(m)
        steel_t = rng.lognormvariate(math.log(d["median_t"]), d["sigma"])
        parts = [rng.random() + 0.2 for _ in picked]
        out = steel_t * d["yield"]
        plants.append({"id": f"P{i + 1}", "name": f"Plant {i + 1}",
                       "steel": [{"supplier": m, "tonnes": steel_t * p / sum(parts)} for m, p in zip(picked, parts)],
                       "fuel": [{"fuel": "lpg", "qty": out * d["lpg_per_t"], "unit": "t"}], "output": [{"tonnes": out}]})
    return {"plants": plants, "mill_see": mill_see}


def see_of(plant, suppliers, year):
    """Same arithmetic as calc.compute, without the cost curve, so a run stays fast. A test keeps them equal."""
    direct = sum(fuel_tco2(f["fuel"], f["qty"], f["unit"]) for f in plant["fuel"])
    default = DEFAULT_PRECURSOR_SEE * (1 + markup(year))
    prec = sum(s["tonnes"] * (suppliers[s["supplier"]]["see"] if s["supplier"] in suppliers else default) for s in plant["steel"])
    return (direct + prec) / plant["output"][0]["tonnes"]


def run(seed, zipf, p_join, d=DEFAULTS):
    m = build_market(seed, zipf, d)
    plants, y = m["plants"], d["year"]
    rng = random.Random(seed * 1000 + 7)
    outs = [p["output"][0]["tonnes"] for p in plants]
    base = [see_of(p, {}, y) for p in plants]
    suppliers, buyers, onboarded, months = {}, {}, 0, []
    for mo in range(d["months"] + 1):
        while onboarded < round(d["plants"] * mo / d["months"]):
            for s in plants[onboarded]["steel"]:
                buyers[s["supplier"]] = buyers.get(s["supplier"], 0) + 1
            onboarded += 1
        if mo:
            for name in sorted(buyers):
                if name not in suppliers and buyers[name] >= d["pull"] and rng.random() < p_join:
                    suppliers[name] = {"verified": True, "see": m["mill_see"][name]}
        tot = ver = w_now = w_base = saved = 0.0
        for i in range(onboarded):
            now = see_of(plants[i], suppliers, y)
            w_now += now * outs[i]; w_base += base[i] * outs[i]; saved += (base[i] - now) * outs[i]
            for s in plants[i]["steel"]:
                tot += s["tonnes"]; ver += s["tonnes"] if s["supplier"] in suppliers else 0
        months.append({"month": mo, "plants": onboarded, "mills_verified": len(suppliers),
                       "share_verified": round(ver / tot, 4) if tot else 0,
                       "drop_pct": round(100 * (1 - w_now / w_base), 2) if onboarded else 0,
                       "saving_per_plant_eur": round(saved * PAYABLE[y] * EUA_PRICE / onboarded) if onboarded else 0})
    by_mill = {}
    for p in plants:
        for s in p["steel"]:
            by_mill[s["supplier"]] = by_mill.get(s["supplier"], 0) + s["tonnes"]
    total, run_sum, cov = sum(by_mill.values()), 0.0, []
    for t in sorted(by_mill.values(), reverse=True) + [0.0] * (d["mills"] - len(by_mill)):
        run_sum += t; cov.append(round(run_sum / total, 4))
    return {"months": months, "coverage": cov}


def band(values):
    v = sorted(values); at = lambda f: v[round(f * (len(v) - 1))]
    return {"p10": at(0.1), "p50": at(0.5), "p90": at(0.9)}


def build(d=DEFAULTS):
    out = {"assumptions": {**d, "zipf": ZIPF, "join": JOIN, "default_see": DEFAULT_PRECURSOR_SEE, "eua_price": EUA_PRICE,
                           "payable_share": PAYABLE[d["year"]]}, "scenarios": {}}
    for zn, z in ZIPF.items():
        for jn, p in JOIN.items():
            runs = [run(s, z, p, d) for s in range(1, d["seeds"] + 1)]
            months = []
            for mo in range(d["months"] + 1):
                at = [r["months"][mo] for r in runs]
                months.append({"month": mo, "plants": at[0]["plants"], "mills_verified": band([a["mills_verified"] for a in at])["p50"],
                               "share": band([a["share_verified"] for a in at]), "drop_pct": band([a["drop_pct"] for a in at]),
                               "saving": band([a["saving_per_plant_eur"] for a in at])})
            cov = [band([r["coverage"][k] for r in runs])["p50"] for k in range(d["mills"])]
            out["scenarios"][f"{zn}_{jn}"] = {"zipf": zn, "join": jn, "months": months, "coverage": cov}
    return out


if __name__ == "__main__":
    data = json.loads(json.dumps(build()))
    if "--write" in sys.argv:
        open(os.path.join(HERE, "docs", "simulation.js"), "w").write("window.SIM = " + json.dumps(data, sort_keys=True, indent=1) + ";\n")
        print("wrote docs/simulation.js")
    print(f"{'mills cluster':14}{'mills join':11}{'mills verified':>15}{'steel on verified data':>25}{'emissions drop':>16}   (median, month 12 / 24)")
    for sc in data["scenarios"].values():
        a, b = sc["months"][12], sc["months"][24]
        print(f"{sc['zipf']:14}{sc['join']:11}{a['mills_verified']:>7} /{b['mills_verified']:>3}{a['share']['p50']*100:>14.0f}% /{b['share']['p50']*100:>4.0f}%{a['drop_pct']['p50']:>10.0f}% /{b['drop_pct']['p50']:>4.0f}%")
