# CImEx Compliance: carbon compliance for exporters (CBAM first)

CImEx stands for Carbon Import Export.

A carbon compliance platform. The first product, CBAM, lets a clerk at a metal plant produce EU carbon-border data for fasteners (CN 7318) that a verifier can check. The homepage has a Products menu; CBAM opens the dashboard, and other rules (Scope 1–3, India CCTS, California SB 253) are planned on the same document layer. AI reads the documents. Rules do the calculation. The app drafts the monitoring plan, lists the gaps still open, and creates a carbon compliance report once the required documents are in. A mill verified once serves every plant that buys from it.

**Website:** https://cimex-compliance.vercel.app (also on GitHub Pages: https://hemanthdadi1.github.io/AI-Export-Compliance/) (homepage, [app](https://hemanthdadi1.github.io/AI-Export-Compliance/app.html), [docs](https://hemanthdadi1.github.io/AI-Export-Compliance/docs.html), [simulation](https://hemanthdadi1.github.io/AI-Export-Compliance/simulation.html)). On the website the app runs the same Python engine in your browser with Pyodide, using made-up sample data.

**Pitch:** [Startup Buildathon idea submission (PDF)](pitch/CImEx-Buildathon-Idea-Submission.pdf) and the [architecture diagram](pitch/architecture.png). The Buildathon build is planned in [AGENT_PLAN.md](AGENT_PLAN.md).

## Run

```bash
python3 server.py            # open http://localhost:8000 (homepage) and /app.html (the app)
```

No packages needed. Python 3.10+.

To read real PDFs and photos with Gemini:

```bash
GEMINI_API_KEY=your-key python3 server.py
```

Or with Gemini on Vertex AI in Mumbai (`asia-south1`), so files stay in India:

```bash
VERTEX_PROJECT=your-project VERTEX_TOKEN=$(gcloud auth print-access-token) python3 server.py
```

Without either, the app reads only the sample `.txt` format in `demo/`.

## Test

```bash
for t in test_*.py; do python3 $t || break; done
```

- `test_app.py`: the router, the required-documents check and the report
- `test_review.py`: check and confirm, corrections, removal, and the edit trail
- `test_calc.py`, `test_match.py`, `test_capture.py`: calculation, heat matching, monthly log and plan
- `test_verifier.py`: every figure in the report has a source
- `test_extract.py`: Gemini and Vertex requests, offline
- `test_pages.py`: the website uses exact copies of the engine
- `test_simulation.py`: the simulation matches the engine

After changing `calc.py`, `extract.py`, `server.py` or `demo/`, run `python3 make_pages.py` to update the website copies. After changing `simulate.py`, run `python3 simulate.py --write`.

## Deploy to Cloud Run

```bash
gcloud services enable run.googleapis.com aiplatform.googleapis.com cloudbuild.googleapis.com
gcloud run deploy cbam --source . --region asia-south1 --max-instances 1 \
  --set-env-vars VERTEX_PROJECT=$(gcloud config get-value project) --allow-unauthenticated
```

Give the service's runtime service account the Vertex AI User role (`roles/aiplatform.user`).
Keep `--max-instances 1`. Data is in memory, so a second instance would show different data.
The URL is public and has no login. Anyone with it can upload or reset. Share it only for the demo.

## Demo flow (about 3 minutes)

1. Open the app. **Documents** shows four required items, all missing. **Create carbon compliance report** is locked.
2. Click **Load sample documents**: 6 mill test certificates, 1 steel invoice, 3 fuel invoices and 1 production record. One certificate gives only coils, so its tonnes come from the trader's invoice for the same heat. Four items turn green. The fifth, **Extracted values confirmed**, stays open, and the report stays locked.
3. Under **Check what we read**, each file is a card with its values and source line. Change a value (say LPG 30 t to 29), then **Confirm**, or press **Confirm all as read**. The report unlocks. Corrections are listed in it.
4. **Dashboard**: an Attention card names the biggest gap and copies a request email to the mill. The plant shows 4.38 tCO2/t. Own furnaces add only 0.20. Most of it is Rayalaseema steel on the default value with a penalty.
5. **Mills**: add verified data for Rayalaseema, 1.9. The plant drops to 2.25, and three other plants that buy from the same mill drop too.
6. **Monthly log**: click **Load sample log**. LPG now counts fuel used (52 t), not fuel bought (56 t).
7. **Create carbon compliance report**: summary, method, every figure with its source document and line, who checked it and what they changed, open gaps, and signature lines. Print it or save it as a PDF, or download the EU supplier template as a CSV.

## Files

- `calc.py`: the rule-based engine. AI never touches the final figure.
- `extract.py`: Gemini extraction, plus a rule parser for the sample files.
- `server.py`: the one router (`dispatch`) used by the HTTP server and by the browser build, plus the seed network (3 mills, 4 plants).
- `docs/`: the website. `index.html` homepage, `app.html` and `app.js` the app, `docs.html` documentation, `simulation.html`, shared `app.css`. `docs/py/` holds copies of the engine made by `make_pages.py`.
- `simulate.py`: the network-effect simulation behind `docs/simulation.html`.
- `deck/`: the pitch deck source (in the repository only).

## Not real yet

- The steel default is 4.27 tCO2/t for Indian non-alloy wire rod (CN 7213), before the mark-up. It comes from Implementing Regulation (EU) 2025/2621, Annex I, as corrected by 2026/1740 (checked on EUR-Lex, 13 Nov 2026). Alloy wire rod (CN 7227) is 7.30, and the engine does not handle it yet. The EU also lists product defaults for fasteners, for example 5.72 for threaded screws and bolts (CN 7318 15) and 5.14 for nuts (CN 7318 16). The demo mill values (2.1 and 1.9) are made up.
- Data is kept in memory. A restart clears it. On the website it lives in the browser tab.
- No login, and no edit step for extracted values.
- The homepage sign-up form needs a team inbox: set `CONTACT_EMAIL` in `docs/index.html`.
- Output is one CN code. Direct emissions are not split across products.

## Demo data

Everything in `demo/` and `samples/` is synthetic. Do not commit real plant documents.

## License

MIT. See [LICENSE](LICENSE).
