# AI compliance expert for Indian exporters: MVP

Lets a clerk at a metal plant produce EU carbon-border (CBAM) data for fasteners (CN 7318) that a verifier can check. AI reads the documents. Rules do the calculation. The app also drafts the monitoring plan and lists the gaps still open. A mill verified once serves every plant that buys from it.

## Run

```bash
python3 server.py            # open http://localhost:8000
python3 test_calc.py         # calculation tests
python3 test_capture.py      # monthly log and monitoring plan tests
python3 test_verifier.py     # verifier pack: every figure has a source
python3 test_match.py        # heat matching tests
python3 test_extract.py      # Gemini and Vertex requests, offline
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

Without either, the app reads only the demo `.txt` format in `demo/`.

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

1. Click **Load demo files**. That loads 6 mill test certificates, 1 steel invoice, 3 fuel invoices and 1 production record. One certificate gives only coils, not tonnes. The app takes the tonnes from the trader's invoice for the same heat. Both sources show on that heat.
2. Your plant shows 4.40 tCO2/t. Own furnaces add only 0.20. Most of it is Rayalaseema steel on the default value with a penalty.
3. In **Supplier network**, click **Add verified data** for Rayalaseema and enter 1.9.
4. Your plant drops to 2.25. Three other plants that buy from the same mill drop too (by 35% to 61%).
5. Click **Load demo log**. LPG now uses stock-based use (52 t), not purchases (56 t). The number moves to 4.39 (2.24 if step 3 is done). The plan draft lists the gaps left: no diesel log, no production log, 2 of 12 months.
6. Change the year to see the penalty mark-up change. Click **Open the verifier pack**. It lists every figure with its source documents, the open checks and gaps, and the method. Print it or save it as a PDF. The CSV has the same rows.

## Files

- `calc.py`: the rule-based engine. AI never touches the final figure.
- `extract.py`: Gemini extraction, plus a rule parser for the demo files.
- `server.py`: stdlib web server and seed network (3 mills, 4 plants).
- `index.html`: the single page.
- `verifier.html`: the printable verifier pack. It reads `/api/audit`.

## Not real yet

- The steel default (4.3 tCO2/t, India wire rod and bars, before the mark-up) comes from a secondary source citing Regulation (EU) 2025/2621. That annex may have been replaced by 2026/1740. Check the current Official Journal table. CN 7318 itself was not listed, so no fastener default is used. The demo mill values (2.1 and 1.9) are made up.
- Data is kept in memory. A restart clears it.
- No login and no edit step for extracted values.
- Output is one CN code. Direct emissions are not split across products.

## Pitch deck

`deck/` holds the slide source: `deck.json` is the index and `slides/` has one HTML file per slide, in the format of the Claude Slides artifact type. All plants, mills and numbers in the deck and the demo are made up, except where a slide cites a source.

## Demo data

Everything in `demo/` and `samples/` is synthetic. Do not commit real plant documents.
