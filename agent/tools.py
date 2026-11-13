"""Read-only tools for the CImEx Review Agent. Each one reads through server.dispatch, the router the website uses.
None of them computes a figure or changes state. The rule engine in calc.py stays the only place numbers come from."""
import server

YEAR = 2027


def _get(path, year=None):
    status, data, _, _ = server.dispatch("GET", path, {"year": str(year)} if year else {}, None)
    if status != 200:
        return {"error": f"{path} returned {status}", "detail": data}
    return data


def _your_plant(year):
    state = _get("/api/state", year)
    return state, state["plants"][0]  # the first plant is always the user's own; the others are peers


def get_readiness():
    """Which documents the report still needs, and whether every file has been confirmed by the clerk."""
    return _get("/api/readiness")


def get_documents():
    """Every uploaded file: what was read from it, its source line, open issues, and whether the clerk confirmed it."""
    return _get("/api/docs")


def get_plant(year: int = YEAR):
    """The plant's emissions per tonne, its steel by mill (most steel on defaults first), and the open checks
    a verifier would raise. Shows only the user's own plant."""
    state, p = _your_plant(year)
    if p.get("empty"):
        return {"plant": p["name"], "empty": True, "open_checks": state["plan"]["gaps"]}
    steel = sum(m["tonnes"] for m in p["precursors"]) or 1
    mills = sorted(({"mill": m["supplier"], "tonnes": m["tonnes"], "basis": m["basis"],
                     "share_of_steel": m["tonnes"] / steel, "heats": [h["heat"] for h in m["heats"]]}
                    for m in p["precursors"]), key=lambda m: (m["basis"] != "default", -m["tonnes"]))
    return {"plant": p["name"], "year": year, "tco2_per_tonne": p["see_total"],
            "own_furnaces_tco2_per_tonne": p["see_direct"], "eu_default_for_goods": p["product_default"],
            "steel_on_verified_data": p["verified_share"], "mills": mills,
            "open_checks": state["plan"]["gaps"], "document_conflicts": state["checks"],
            "heats_without_a_certificate": state["unmatched"]}


def get_audit(year: int = YEAR):
    """Every figure in the report with the file and line it came from, and every edit the clerk made."""
    return _get("/api/audit", year)


def draft_mill_request(mill: str, year: int = YEAR):
    """Draft an email asking a mill for its verified emissions value. Text only: nothing is sent."""
    _, p = _your_plant(year)
    m = next((x for x in p.get("precursors", []) if x["supplier"] == mill), None)
    if m is None:
        return {"error": f"{mill} does not supply this plant."}
    if m["basis"] == "actual":
        return {"error": f"{mill} has already shared verified data."}
    heats = "\n".join(f"  - Heat {h['heat']}: {h['tonnes']:g} t" for h in m["heats"])
    email = (f"Dear {mill} team,\n\n"
             f"Our EU buyers now need the embedded emissions of the steel in our goods under the EU carbon border "
             f"adjustment mechanism (CBAM). In the period we report, we used {m['tonnes']:g} t of your wire rod:\n{heats}\n\n"
             "Without your data, our buyers must use the EU default value plus a penalty mark-up.\n\n"
             "Could you share the embedded emissions of this steel, in tCO2 per tonne, with the verification "
             "report from an accredited verifier? A value for your plant and product route is enough.\n\n"
             "Every customer of yours that uses our system will be able to reuse it.\n\n"
             f"Regards,\n{p['name'].replace(' (your plant)', '')}")
    return {"mill": mill, "subject": f"Request for verified CBAM emissions data: {m['tonnes']:g} t of wire rod",
            "email": email}


ALL = [get_readiness, get_documents, get_plant, get_audit, draft_mill_request]
