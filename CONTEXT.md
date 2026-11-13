# CImEx Compliance: project context

Handoff notes for anyone, or any AI session, picking up this project. Updated 13 Nov 2026.

## What it is

CImEx Compliance (Carbon Import Export) is a carbon compliance platform for Indian exporters. The first product covers the EU carbon border tax (CBAM) for steel goods, starting with fasteners (CN 7318).

One line: AI reads the documents. People confirm. Rules decide the number.

- A clerk uploads mill certificates, invoices, fuel bills and production records.
- Gemini reads each file into fields, each with its source line.
- The clerk confirms or fixes every value. Edits are logged.
- Fixed Python rules calculate embedded emissions. AI never sets the final number.
- Output: a carbon compliance report, an EU supplier CSV and a verifier pack.
- Network effect: verify a mill once, and every plant that buys its steel moves off the penalty default.

Goal framing: "the $15-an-hour expert". A clerk produces expert-grade, verifier-checkable output.

## Links

- Repo (public, MIT): https://github.com/HemanthDadi1/AI-Export-Compliance
- Live site and demo: https://cimex-compliance.vercel.app (Vercel, redeploys on every push). Also on GitHub Pages: https://hemanthdadi1.github.io/AI-Export-Compliance/
- App: `app.html`. Docs: `docs.html`. Simulation: `simulation.html`.
- Buildathon submission PDF: `CImEx-Buildathon-Idea-Submission.pdf` (also in the repo under `pitch/`).

Decks and pages (claude.ai artifacts, private unless shared):
- Combined 14-slide pitch deck: https://claude.ai/artifact/L7UfB5x1CPCR7BhLoxSno8 (shared by link)
- 12-slide CImEx deck: https://claude.ai/artifact/VshfTNwjDQkyLytDiRW6Ha
- Original 14-slide deck: https://claude.ai/artifact/NyLUXV9GUCo6xQ5BAnabv3
- Old combined deck (can be deleted): https://claude.ai/artifact/AbTSKSZMuYx7haamhevizZ
- Product canvas: https://claude.ai/artifact/PdiALZ5EUu13PPQepMXjeF
- Interview kit and exposure check offer: https://claude.ai/artifact/RwT9arJPKRF8SzGzTQLA6w

## Folder layout

```
CBAM/
  CONTEXT.md                      this file
  CImEx-Buildathon-Idea-Submission.pdf
  submission-build/               script and images that rebuild the submission PDF
  mvp/                            the code; mirrors the GitHub repo
  real_certs/, ilide.info-*.pdf   third-party certificates. Never publish.
  CBAM Exporter-Data Startup Master Document.*   private strategy. Never publish.
  CBAM Exporter-Readiness Startup Launch Plan.pdf private. Never publish.
  Reference Palette/              design references
```

## Code (mvp/)

Python standard library only. No packages.

- `calc.py` rule engine. `extract.py` Gemini or Vertex reading, else a rule parser for the sample `.txt` format.
- `server.py` one router, `dispatch(method, path, query, body)`. It serves both the HTTP server and the browser build.
- `docs/` the website (GitHub Pages). The same Python runs in the browser through Pyodide. `docs/py/` holds exact copies made by `make_pages.py`.
- `simulate.py` the mill network simulation.
- Tests: 9 files, `test_*.py`. Run: `for t in test_*.py; do python3 $t || break; done`
- After changing the engine or demo files: `python3 make_pages.py`. After changing the simulation: `python3 simulate.py --write`.
- Run locally: `python3 server.py`, then open http://localhost:8000
- Gemini: set `GEMINI_API_KEY`, or `VERTEX_PROJECT` for Vertex AI. Default model `gemini-2.5-flash`, default region `asia-south1`.

Built and tested: upload, Gemini reading, review and confirm with edit log, heat matching, gap checks, monthly fuel log, mill view, rule engine, cost curve to 2034, report, verifier pack, EU CSV, duplicate-file refusal, homepage rule finder.

Not built: hosting on Cloud Run, accounts and storage, the ADK review agent, shipping-bill reading, ICEGATE and DGFT filings.

## Numbers and their status

Checked against the engine (demo data, reporting year 2027):
- Sample plant: 4.38 tCO2/t (0.20 own furnaces, 4.18 steel). 2.25 after Rayalaseema shares 1.9 verified. Other plants: 4.62 to 2.14, 5.49 to 2.13, 5.38 to 3.48. (Before 13 Nov the default was 4.3 and the plant showed 4.40; the submitted PDF still says 4.40.)

From EU rules, as researched (recheck before quoting):
- Steel default 4.27 tCO2/t for India non-alloy wire rod (CN 7213), before mark-up. Reg (EU) 2025/2621 Annex I, as corrected by 2026/1740. Checked on EUR-Lex 13 Nov 2026. Alloy wire rod (CN 7227): 7.30. Product defaults: bolts (CN 7318 15) 5.72, nuts (CN 7318 16) 5.14.
- Payable share 2.5% (2026), 5%, 10%, 22.5%, 48.5%, 61%, 73.5%, 86%, 100% (2034).
- Default mark-up 10% (2026), 20% (2027), 30% from 2028.
- First annual declaration due 30 Sep 2027.
- India sold EUR 5.30 bn of CBAM-covered goods to the EU in 2025 (Eurostat Comext via CBAMGuide).

Not confirmed:
- Whether Gemini models run on Vertex AI in Mumbai.
- All prices: exposure check Rs 25,000 to 50,000; programme Rs 3 to 6 lakh per plant; annual care Rs 1.5 to 3 lakh. Untested with customers.
- Expert hours saved per plant. Not measured.

Removed from decks because unsourced: Rs 50 to 500 crore plant size, 403 verifiers vs 12,000 applicants, about 180 products from 2028, Isometric funding, "40 days toward 25".

## Google Startup Buildathon India 2026

- Application due 13 Nov 2026. Submit the official template as PDF, 5 MB or less.
- Team name: CImEx Compliance. Team size: 4.
- The submission puts the CImEx Review Agent at the centre. It is built with Gemini and the Agent Development Kit at the Buildathon. It checks the file set like a verifier, asks the clerk questions, drafts the mill request, and calls the rule engine as a tool. It never changes a figure.
- Demo goal at the city round: on the sample plant, the agent finds the 4 open checks, asks only what it cannot resolve, drafts the mill request, and the report unlocks after the clerk approves.
- Tools claimed: Gemini API (used). ADK and Agent Skills, Antigravity, AI Studio (planned). The team must actually use them at the Buildathon.
- Open question: whether a team member living in the US is eligible. Check the official rules.
- Rebuild the PDF from the template: `submission-build/build_pdf.py` (needs PyMuPDF). That folder holds the screenshots and architecture image it uses.

## Market and competition

- First customers: mid-size Indian metal exporters (fasteners, wire, pipes), Chennai and Hyderabad first. Mills join free. EU importers and verifiers are the other sides.
- CleanCarbon.ai runs an India CBAM registry with export council backing. Do not claim nobody does this. Our difference is source-linked, confirmed data and the review trail.
- Others seen: CarbonChain (YC S2020), osapiens, Watershed, Persefoni, GreenSutra, Isometric. None of the six homepages checked show prices.
- YC: W27 deal is $500k. Non-US companies need a US, Canada, Cayman or Singapore parent. The W27 request for startups includes "The $15-an-Hour Expert".

## Rules for this project

- Use plain, short sentences in code, docs, UI and replies.
- Only claim what is built. Mark planned work as planned.
- Never publish private strategy documents or third-party certificates. The repo is public.
- Commit with the GitHub noreply address. Never put personal emails in commits or external requests.
- Write tests first for calculation, matching, review and report logic.

## Next steps

1. Submit the Buildathon PDF.
2. Run one real certificate through Gemini and record the result.
3. Run the interview kit with 15 to 20 exporters. Sell three paid exposure checks.
4. Confirm the EU default values and replace the working steel figure.
5. Plan the ADK review agent build for the city round.
6. Host on Cloud Run with Vertex AI.
