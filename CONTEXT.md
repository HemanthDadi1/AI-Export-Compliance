# CImEx Compliance: project context

Handoff notes for anyone, or any AI session, picking up this project. Updated 20 Nov 2026. Read this first. You should not need earlier chats.

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
- Live site: https://cimex-compliance.vercel.app (Vercel project `cimex-compliance`, team scope `ci-m-ex`, redeploys on every push). Backup: https://hemanthdadi1.github.io/AI-Export-Compliance/
- Pages: `index.html` (homepage), `app.html` (dashboard), `docs.html`, `simulation.html`.
- Buildathon submission PDF: `CImEx-Buildathon-Idea-Submission.pdf` (also in the repo under `pitch/`).

claude.ai artifacts (private unless shared):
- Combined 14-slide pitch deck: https://claude.ai/artifact/L7UfB5x1CPCR7BhLoxSno8 (shared by link). Still shows older numbers (4.40).
- 12-slide CImEx deck: https://claude.ai/artifact/VshfTNwjDQkyLytDiRW6Ha
- Original 14-slide deck: https://claude.ai/artifact/NyLUXV9GUCo6xQ5BAnabv3
- Old combined deck (can be deleted): https://claude.ai/artifact/AbTSKSZMuYx7haamhevizZ
- Product canvas: https://claude.ai/artifact/PdiALZ5EUu13PPQepMXjeF
- Interview kit and exposure check offer: https://claude.ai/artifact/RwT9arJPKRF8SzGzTQLA6w. Brackets still to fill: your name, price, turnaround, where client files are stored.
- Exporter call tracker (Sheet, 25 firms): https://claude.ai/artifact/6CGBES6m6ttYHg2qT2vHem. Not shared with the team yet. Contact names are empty.

## Folder layout

```
CBAM/
  CONTEXT.md                      copy of mvp/CONTEXT.md
  CImEx-Buildathon-Idea-Submission.pdf
  submission-build/               script and images that rebuild the submission PDF
  outreach/target-list.md         25 fastener exporters with sources. Private, not in the repo.
  mvp/                            the code; mirrors the GitHub repo
  real_certs/, ilide.info-*.pdf, "23 039 0 - 20460.signed.pdf"   third-party certificates. Never publish.
  CBAM Exporter-Data Startup Master Document.*   private strategy. Never publish.
  CBAM Exporter-Readiness Startup Launch Plan.pdf private. Never publish.
  Reference Palette/              design references
```

## Code (mvp/)

Python standard library only for the app. The review agent needs `google-adk` (venv at `~/.venvs/cimex`).

- `calc.py` rule engine. `extract.py` Gemini or Vertex reading, else a rule parser for the sample `.txt` format.
- `server.py` one router, `dispatch(method, path, query, body)`. It serves both the HTTP server and the browser build.
- `docs/` the website. The same Python runs in the browser through Pyodide. `docs/py/` holds exact copies made by `make_pages.py`.
- `docs/mark.svg` the C tile from the logo, white, used in every page header.
- `simulate.py` the mill network simulation.
- `agent/` the CImEx Review Agent (Google ADK): `tools.py` (read-only tools over `server.dispatch`), `agent.py`, `skill.md` (review rules; no curly braces, ADK treats them as placeholders), `run.py`. Plan: `AGENT_PLAN.md`.
- Tests: 11 files, `test_*.py`, all passing on 20 Nov. Run: `for t in test_*.py; do python3 $t || break; done`
- After changing the engine or demo files: `python3 make_pages.py`. After changing the simulation: `python3 simulate.py --write`.
- Run locally: `python3 server.py`, then open http://localhost:8000
- Gemini: set `GEMINI_API_KEY`, or `VERTEX_PROJECT` for Vertex AI. Default model `gemini-3.8-flash` (2.5 Flash is closed to new API users). Region `asia-south1`.

Built and tested: upload, Gemini reading, review and confirm with edit log, heat matching, gap checks, monthly fuel log, mill view, rule engine, cost curve to 2034, report, verifier pack, EU CSV, duplicate-file refusal, homepage rule finder, agent tools.

Not built: hosting on Cloud Run, accounts and storage, shipping-bill reading, ICEGATE and DGFT filings.

### Changes pushed to GitHub main (commit 11cd1eb, 20 Nov 2026)

- `calc.py`: Metallurgical mass balance & scrap loss calculation (Annex V), product CN benchmarks (88% bolts, 82% nuts, 90% washers), and sub-installation route allocation (`heat_treated` vs `cold_formed`).
- `server.py`: Real-time carbon depletion ledger preventing heat double-allocation, trader vs melting mill origin verification, verifier ready score (0–100%), and `/api/dossier` ZIP export with streaming `Content-Length`.
- `docs/app.html`, `docs/app.js`: Verifier Readiness score pill, Physical Mass Balance card, Carbon Depletion Ledger table, Alloy/Non-alloy wire rod dropdowns (CN 7213 vs 7227), finished goods CN codes (7318 15/16/22), and hardened ZIP dossier download.
- `docs/py/`: Exact synced engine copies via `make_pages.py`.
- `samples/`: Mock Indian MTC test photo (`sample_mtc_photo.jpg`).
- Tests: All 11 unit test suites passing cleanly (`for t in test_*.py; do python3 $t || break; done`).

## Numbers and their status

Checked against the engine (demo data, reporting year 2027):
- Sample plant: 4.38 tCO2/t (own furnaces 0.20, verified steel 0.80, default steel 3.38). 2.25 after Rayalaseema shares 1.9 verified. Rayalaseema supplies 660 t of 1,040 t (63%).
- Importer cost to 2034: EUR 1,427,628. Saving against the EU default for the goods: EUR 849,075. Open checks: 4 (diesel, lpg, output log, Rayalaseema).
- Other plants: 4.62 to 2.14, 5.49 to 2.13, 5.38 to 3.48.
- The submitted PDF still says 4.40 and Gemini 2.5 Flash. The decks still say 4.40.

From EU rules (recheck before quoting):
- Reg (EU) 2025/2621 Annex I (India), as corrected by 2026/1740. Checked on EUR-Lex 13 Nov 2026.
  - Non-alloy wire rod (CN 7213): 4.27. Alloy wire rod (CN 7227): 7.30.
  - Bolts (CN 7318 15): 5.72. Nuts (7318 16) and washers (7318 22): 5.14.
- The dashboard compares against the EU default for the goods, by CN code.
- Payable share 2.5% (2026), 5%, 10%, 22.5%, 48.5%, 61%, 73.5%, 86%, 100% (2034).
- Default mark-up 10% (2026), 20% (2027), 30% from 2028.
- First annual declaration due 30 Sep 2027.
- India sold EUR 5.30 bn of CBAM-covered goods to the EU in 2025 (Eurostat Comext via CBAMGuide).
- EU importers bringing in under 50 t a year are exempt.

Not confirmed:
- Whether Gemini models run on Vertex AI in Mumbai.
- All prices: exposure check Rs 25,000 to 50,000; programme Rs 3 to 6 lakh per plant; annual care Rs 1.5 to 3 lakh. Untested with customers.
- Expert hours saved per plant. Not measured.

Removed from decks because unsourced: Rs 50 to 500 crore plant size, 403 verifiers vs 12,000 applicants, about 180 products from 2028, Isometric funding, "40 days toward 25".

## Google Startup Buildathon India 2026

- The application was due 13 Nov 2026. Confirm it was submitted.
- Team name: CImEx Compliance. Team size: 4.
- The submission puts the CImEx Review Agent at the centre. It checks the file set like a verifier, asks the clerk questions, drafts the mill request, and calls the rule engine as a tool. It never changes a figure.
- Demo goal: on the sample plant, the agent finds the 4 open checks, ranks Rayalaseema first, asks one question (monthly fuel stock records), drafts the mill request, and changes no figure.
- Tools claimed: Gemini API (used). ADK and Agent Skills, Antigravity, AI Studio (planned). The team must actually use them at the Buildathon.
- Open question: whether a team member living in the US is eligible.
- Rebuild the PDF: `submission-build/build_pdf.py` with `/opt/homebrew/bin/python3.11` (needs PyMuPDF; system python3 is 3.9 and too old).

## Outreach (started 14 Nov)

- Plan: interview 15 to 20 exporters and sell three paid exposure checks. Rule set in advance: fewer than 3 yeses in 15 calls means change the offer.
- `outreach/target-list.md`: 25 firms. 17 Tier A (public source says they sell to Europe), 8 Tier B. First 10 calls: mid-size Tier A firms. The large listed firms probably have their own teams (names in the private list).
- Ludhiana has the most Tier A firms (6 of 17). Chennai and Hyderabad have few. Consider starting in Ludhiana.
- Groups that reach many plants: Fasteners Association of India, EEPC India, India Fastener Show (Pune, 16 to 18 Apr 2027), Fastener Fair India (Mumbai, Apr 2027), Fastener Fair Global (Stuttgart, Mar 2027).
- Opening fact: a fastener exporter told The Wire its Danish and German buyers now require CBAM reports.

## Market and competition

- First customers: mid-size Indian metal exporters (fasteners, wire, pipes). Mills join free. EU importers and verifiers are the other sides.
- CleanCarbon.ai runs an India CBAM registry with export council backing. Do not claim nobody does this. Our difference is source-linked, confirmed data and the review trail.
- Others seen: CarbonChain (YC S2020), osapiens, Watershed, Persefoni, GreenSutra, Isometric. None of the six homepages checked show prices.
- YC: the W27 deal is $500k. Non-US companies need a US, Canada, Cayman or Singapore parent. The W27 request for startups includes "The $15-an-Hour Expert".

## How to push

1. Clone `HemanthDadi1/AI-Export-Compliance` to a scratch folder.
2. Sync: `rsync -a --exclude='__pycache__' --exclude='.DS_Store' --exclude='.claude' --exclude='deck' mvp/ <clone>/`
3. Commit with `git -c user.name=HemanthDadi1 -c user.email=HemanthDadi1@users.noreply.github.com commit`.
4. Push. Vercel redeploys on its own.

The Vercel MCP returns 403 for this team. Use the Vercel CLI, which is logged in.

## Rules for this project

- Use plain, short sentences in code, docs, UI and replies.
- Only claim what is built. Mark planned work as planned.
- Never publish private strategy documents, the outreach list or third-party certificates. The repo is public.
- Commit with the GitHub noreply address. Never put personal emails in commits or external requests.
- Never ask for, paste or store the Gemini key. The user sets it in their own terminal: `read -s "GOOGLE_API_KEY?Gemini key: "; export GOOGLE_API_KEY`
- Write tests first for calculation, matching, review and report logic.
- Do not build anything nobody asked for.

## Next steps

1. Outreach: fill the interview kit brackets, add contact names to the tracker, share it with the team, and start the first 10 calls.
2. Review the unpushed 20 Nov changes (above), then push them.
3. Run the review agent live: `cd ~/Downloads/CBAM/mvp && ~/.venvs/cimex/bin/python -m agent.run` after setting `GOOGLE_API_KEY`. Check it against the demo goal. Tune `agent/skill.md` if needed.
4. Update the PDF's models page to the model that worked, and the 4.40 figure to 4.38.
5. Run one real certificate through Gemini and record the result.
6. Check the dashboard and homepage in dark mode, and the dashboard at phone width.
7. Host on Cloud Run with Vertex AI.
