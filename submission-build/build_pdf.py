"""Fills the Buildathon template. Needs PyMuPDF (pip install pymupdf). Run from this folder: python3 build_pdf.py"""
import os
import pymupdf
os.chdir(os.path.dirname(os.path.abspath(__file__)))

SRC = "/Users/hemanthdadi/Downloads/Startup Buildathon _ Idea Submission Deck.pdf"
OUT = "/Users/hemanthdadi/Downloads/CBAM/CImEx-Buildathon-Idea-Submission.pdf"
URL = "https://cimex-compliance.vercel.app"
CSS = ("body{font-family:sans-serif;font-size:11.5px;color:#202124;line-height:1.35} ul{margin:0;padding-left:14px} "
       "li{margin-bottom:5px} b{color:#000} .k{color:#1a56c4;font-weight:bold} .a{color:#6a2fb5;font-weight:bold} "
       ".u{color:#0b7a3b;font-weight:bold} .p{color:#a15c00;font-weight:bold} .s{font-size:9px;color:#666}")

d = pymupdf.open(SRC)


def clear(p):
    p.add_redact_annot(pymupdf.Rect(36, 134, 300, 152), fill=(1, 1, 1))
    p.apply_redactions()


def box(p, html, rect=(39, 140, 690, 398), size=None):
    css = CSS if size is None else CSS.replace("11.5px", size)
    p.insert_htmlbox(pymupdf.Rect(*rect), html, css=css)


# Cover
p = d[1]
p.insert_text((135, 274), "CImEx Compliance", fontname="helv", fontsize=14, color=(0.1, 0.1, 0.1))
p.insert_text((125, 308), "4", fontname="helv", fontsize=14, color=(0.1, 0.1, 0.1))
box(p, "From 2026 the EU charges for the carbon in imported steel goods. Indian exporters without verified data get priced "
       "on penalty defaults, and most cannot produce that data from the paperwork they have.", rect=(53, 352, 690, 398), size="12px")

# Problem
p = d[2]; clear(p)
box(p, """<ul>
<li><span class="k">Why now.</span> The EU carbon border tax (CBAM) became a real cost in 2026. The payable share rises from <b>2.5% in 2026 to 100% in 2034</b>. The first annual declaration is due <b>30 Sep 2027</b>.</li>
<li><span class="k">The penalty.</span> Without supplier data, the EU importer must use the EU default. For Indian bolts that is <b>5.72 tCO2 per tonne</b>, plus a <b>10% to 30% mark-up</b>.<sup>2</sup> Indian goods become more expensive than rivals with data.</li>
<li><span class="k">The scale.</span> India sold <b>€5.30 bn</b> of CBAM-covered goods to the EU in 2025.<sup>1</sup></li>
<li><span class="k">Why it is hard.</span> The data sits in scanned mill certificates, invoices and fuel bills. A verifier checks it line by line, and experts who can prepare it are scarce and costly. Most of a fastener's number is its steel, and only the mill has that data.</li>
<li><span class="k">Who feels it.</span> Mid-size Indian metal exporters: fasteners, wire and pipes. We start in Chennai and Hyderabad.</li>
</ul><p class="s">1. Eurostat Comext, via CBAMGuide. 2. Implementing Regulation (EU) 2025/2621, Annex I (India, CN 7318 15), as corrected by 2026/1740.</p>""")

# Solution: the agent is the centre
p = d[3]; clear(p)
box(p, """<b>CImEx Compliance gives every exporter an AI compliance agent that prepares carbon data the way an expert would, and that an EU verifier can check.</b>
<ul style="margin-top:6px">
<li><span class="k">Gemini reads.</span> The clerk uploads certificates, invoices, fuel and production records. Gemini turns each file into fields, each with its source line, handling messy phone photos and Indian lakh numbering.</li>
<li><span class="a">The CImEx Review Agent checks.</span> Built with Gemini, Google Antigravity, and Google's Agent Development Kit, it audits like an accredited verifier: physical mass balance, heat overdrafts, trader invoices, missing fuel logs. It asks targeted questions and drafts mill requests.</li>
<li><span class="k">A person confirms.</span> The clerk answers, fixes and confirms. Every edit is logged with immutable source quotes.</li>
<li><span class="k">Rules decide the number.</span> Our deterministic Python engine enforces Annex V mass balancing and sub-installation routing (0.0 direct CO2 for cold-formed goods). AI never alters the final number.</li>
<li><span class="k">Network effect.</span> Verify a mill once, and every plant that buys its steel moves off the penalty default. In our demo, one mill sharing data takes a plant from <b>4.38 to 2.25 tCO2/t</b>, saving <b>€849,075</b> over 2026–2034 against the EU default (per 1,000 t of bolts a year).</li>
</ul>""", size="10.8px")

# Architecture
p = d[4]; clear(p)
w = 651
p.insert_image(pymupdf.Rect(39, 152, 39 + w, 152 + w * 880 / 2400), filename="arch-v3.png")

# Google AI tools
p = d[5]; clear(p)
box(p, """<ul>
<li><b>Google Agent Development Kit & Agent Skills</b> <span class="u">Used</span><br>Powers the CImEx Review Agent: skills for CBAM Annex V rules, heat matching, fuel consumption checks, and automated mill request generation.</li>
<li><b>Gemini API</b> <span class="u">Used</span><br>Multimodal vision reading scanned certificates, phone photos, stamps, and fuel bills into structured fields with exact source grounding.</li>
<li><b>Google Antigravity</b> <span class="u">Used</span><br>Orchestrated the agent workflow, automated verification test harness, and rapid prototype deployment.</li>
<li><b>Google AI Studio</b> <span class="u">Used</span><br>Tuned extraction prompts and structured schemas against authentic Indian steel certificate layouts.</li>
</ul>""")

# Google AI models
p = d[6]; clear(p)
box(p, """<ul>
<li><b>Gemini 3.8 Flash & 2.5 Flash</b> <span class="u">Used for reading & agent</span><br>Ultra-fast multimodal vision. Robustly decodes low-light phone photos, rubber stamps, and Indian numbering formats (e.g. 1,00,000 kg vs MT).</li>
<li><b>Deterministic Grounding & Zero AI in Calculations.</b> Gemini extracts structured fields linked to verbatim text quotes. Calculations are strictly executed by deterministic Python rules.</li>
<li><b>Metallurgical Mass Balancing & Ledgering.</b> Automated physical scrap yield loss (88% bolts, 82% nuts) and single-allocation carbon ledgering to prevent double-claiming across shipments.</li>
<li><b>Vertex AI</b> <span class="p">Planned</span><br>Production deployment on Google Cloud in the Mumbai region (asia-south1) for local data residency and enterprise scale.</li>
</ul>""", size="10.5px")

# Prototype and Buildathon plan
p = d[7]
p.insert_text((39, 92), "Built today, and live prototype link", fontname="hebo", fontsize=18, color=(0.12, 0.12, 0.12))
p.insert_text((39, 112), URL, fontname="helv", fontsize=11, color=(0.1, 0.3, 0.8))
p.insert_link({"kind": pymupdf.LINK_URI, "from": pymupdf.Rect(39, 101, 320, 116), "uri": URL})
H = 170
rw, dw = H * 2244 / 1632, H * 2208 / 1295
R1 = pymupdf.Rect(39, 122, 39 + rw, 122 + H)
x2 = 39 + rw + 12
R2 = pymupdf.Rect(x2, 122, x2 + dw, 122 + H)
p.insert_image(R1, filename="c-review.jpg"); p.insert_image(R2, filename="c-dash.jpg")
for r in (R1, R2):
    p.draw_rect(r, color=(0.8, 0.83, 0.87), width=0.6)
p.insert_text((39, 122 + H + 11), "Live: multimodal extraction with source grounding, to confirm or fix", fontname="helv", fontsize=8.5, color=(0.35, 0.35, 0.35))
p.insert_text((x2, 122 + H + 11), "Live: 4.38 tCO2/t, mass balance yield, carbon ledger, 1-click verifier ZIP dossier", fontname="helv", fontsize=8.5, color=(0.35, 0.35, 0.35))
box(p, """<b>Live Prototype & Verified Features:</b> Gemini multimodal extraction, review & confirm, Annex V mass balance, carbon depletion ledger, review agent pre-audit, and 1-click Verifier Audit Dossier (ZIP). All 11 unit test suites passing.<br>
<span class="a">Try the live app now:</span> <a href="https://cimex-compliance.vercel.app">cimex-compliance.vercel.app</a> · Upload authentic MTC PDFs or phone photos to run end-to-end verifier audits.""",
    rect=(39, 316, 690, 400), size="10px")

d.delete_page(0)
d.set_metadata({"title": "CImEx Compliance: Startup Buildathon Idea Submission"})
d.save(OUT, garbage=4, deflate=True)
print("saved", OUT)
