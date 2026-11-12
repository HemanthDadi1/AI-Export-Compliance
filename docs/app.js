// The app talks to one router (server.dispatch). With the Python server it uses HTTP.
// On GitHub Pages there is no server, so the same Python files run in the browser with Pyodide.
const $ = id => document.getElementById(id);
const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const f = (x, d = 2) => Number(x).toLocaleString("en-GB", {maximumFractionDigits:d, minimumFractionDigits:d});
const pct = x => f(x * 100, 0) + "%";
const eur = x => "€" + Math.round(x).toLocaleString("en-GB");
const PYODIDE = "https://cdn.jsdelivr.net/pyodide/v0.26.4/full/pyodide.js";
const VIEWS = ["documents", "dashboard", "log", "mills", "report"];
const S = {mode: null, py: null, year: 2027, uploads: [], state: null, ready: null, manifest: {py: [], demo: []}};

// ---------- engine ----------
async function boot() {
  try {
    const r = await fetch("api/readiness");
    if (r.ok && (r.headers.get("content-type") || "").includes("json")) S.mode = "server";
  } catch (e) { /* no server: fall through to the browser engine */ }
  const fresh = url => fetch(url, {cache: "no-cache"});  // never run a stale engine after an update
  S.manifest = await (await fresh("py/manifest.json")).json();
  if (S.mode === "server") return;
  S.mode = "browser";
  $("loading").hidden = false;
  await new Promise((ok, fail) => { const s = document.createElement("script"); s.src = PYODIDE; s.onload = ok; s.onerror = fail; document.head.appendChild(s); });
  const py = await loadPyodide();
  py.FS.mkdirTree("/app/demo");
  for (const name of S.manifest.py) py.FS.writeFile(`/app/${name}`, await (await fresh(`py/${name}`)).text());
  for (const name of S.manifest.demo) py.FS.writeFile(`/app/demo/${name}`, await (await fresh(`demo/${name}`)).text());
  py.runPython(`
import sys, json, base64
sys.path.insert(0, "/app")
import server
def _call(method, path, query, body):
    code, payload, ctype, _ = server.dispatch(method, path, json.loads(query), json.loads(body) if body else None)
    if isinstance(payload, bytes):
        return [code, ctype, base64.b64encode(payload).decode(), True]
    return [code, ctype, payload if isinstance(payload, str) else json.dumps(payload), False]
`);
  S.py = py.globals.get("_call");
  $("loading").hidden = true;
}

async function call(method, path, query = {}, body = null) {
  if (S.mode === "server") {
    const qs = new URLSearchParams(query).toString();
    const r = await fetch(path.slice(1) + (qs ? "?" + qs : ""), method === "POST"
      ? {method, headers: {"Content-Type": "application/json"}, body: JSON.stringify(body || {})} : {});
    const ctype = r.headers.get("content-type") || "";
    if (!ctype.includes("json") && !ctype.startsWith("text/")) return {status: r.status, ctype, data: new Uint8Array(await r.arrayBuffer())};
    return {status: r.status, ctype, data: ctype.includes("json") ? await r.json() : await r.text()};
  }
  const res = S.py(method, path, JSON.stringify(query), body ? JSON.stringify(body) : "");
  const [status, ctype, text, isBytes] = res.toJs(); res.destroy();
  if (isBytes) return {status, ctype, data: Uint8Array.from(atob(text), c => c.charCodeAt(0))};
  return {status, ctype, data: ctype.includes("json") ? JSON.parse(text) : text};
}

function download(name, content, type) {
  const a = document.createElement("a");
  a.href = URL.createObjectURL(new Blob([content], {type}));
  a.download = name; a.click(); setTimeout(() => URL.revokeObjectURL(a.href), 1000);
}

async function openDoc(id) {
  const r = await call("GET", "/api/doc", {id});
  if (r.status !== 200) return;
  window.open(URL.createObjectURL(new Blob([r.data], {type: r.ctype})), "_blank");
}
document.addEventListener("click", e => { const b = e.target.closest("[data-doc]"); if (b) { e.preventDefault(); openDoc(b.dataset.doc); } });

// ---------- shell ----------
function current() { const v = location.hash.replace("#/", ""); return VIEWS.includes(v) ? v : "documents"; }

async function refresh() {
  S.state = (await call("GET", "/api/state", {year: S.year})).data;
  S.ready = (await call("GET", "/api/readiness")).data;
  const r = S.ready;
  $("create").disabled = !r.ready;
  $("create").textContent = r.ready ? "Create carbon compliance report" : `Create report · ${r.done} of ${r.total} documents`;
  $("create").title = r.ready ? "" : "Upload the required documents first";
  $("badge-docs").textContent = `${r.done}/${r.total}`;
  await show();
}

async function show() {
  const v = current();
  VIEWS.forEach(name => { $(`view-${name}`).hidden = name !== v; });
  document.querySelectorAll(".side nav a[data-view]").forEach(a => a.classList.toggle("active", a.dataset.view === v));
  const nav = document.querySelector(".side nav"), on = nav.querySelector("a.active");  // on phones the nav scrolls sideways
  if (on && nav.scrollWidth > nav.clientWidth) nav.scrollLeft = on.offsetLeft - nav.offsetLeft - 16;
  $("title").textContent = $(`view-${v}`).dataset.title;
  $("subtitle").textContent = $(`view-${v}`).dataset.sub;
  document.title = `${$("title").textContent} · Export Compliance`;
  await ({documents, dashboard, log: monthlyLog, mills, report})[v]();
}

window.addEventListener("hashchange", () => { window.scrollTo(0, 0); show(); });
$("create").onclick = () => { location.hash = "#/report"; };
for (let y = 2026; y <= 2034; y++) $("year").add(new Option(`Reporting year ${y}`, y, false, y === S.year));
$("year").onchange = () => { S.year = Number($("year").value); refresh(); };

// ---------- documents ----------
function found(rec) {
  if (!rec) return "";
  if (["mtc", "steel_invoice"].includes(rec.doc_type)) return `${esc(rec.supplier || "")} heat ${esc(rec.heat_no || "?")}, ${rec.steel_tonnes ? esc(rec.steel_tonnes) + " t" : "no tonnes on document"}`;
  if (rec.doc_type === "fuel_invoice") return `${esc(rec.fuel)} ${esc(rec.quantity)} ${esc(rec.unit)}`;
  if (rec.doc_type === "production") return `${esc(rec.output_tonnes)} t, CN ${esc(rec.cn_code || "")}`;
  return "";
}
const KIND = {mtc: "Mill test certificate", steel_invoice: "Steel invoice", fuel_invoice: "Fuel invoice", production: "Production record", other: "Other"};

async function documents() {
  $("browserNote").hidden = S.mode !== "browser";
  const r = S.ready;
  $("readyLine").textContent = r.ready ? "All required documents are in. You can create the report." : `${r.done} of ${r.total} required items are in.`;
  $("checklist").innerHTML = r.items.map(i => `<div class="card check"><span class="tick ${i.done ? "on" : ""}" aria-hidden="true">✓</span>
    <div><b>${esc(i.label)}</b><p>${esc(i.hint)}</p><span class="pill ${i.done ? "ok" : i.required ? "warn" : "info"}">${i.done ? "Done" : i.required ? "Required" : "Recommended"}</span></div></div>`).join("");
  $("uploads").innerHTML = S.uploads.length ? `<table><thead><tr><th>File</th><th>Read as</th><th>What we found</th><th>Status</th></tr></thead><tbody>
    ${S.uploads.map(u => `<tr><td>${esc(u.file)}</td><td>${esc(KIND[u.record?.doc_type] || "—")}</td><td>${found(u.record)}</td>
      <td>${u.error ? `<span class="pill bad">Not used</span><div class="muted">${esc(u.error)}</div>` : `<span class="pill ok">Used</span>`}</td></tr>`).join("")}</tbody></table>`
    : `<p class="muted">No files yet. Drop the plant's documents above, or load the samples.</p>`;
  $("samplePack").onclick = e => { e.preventDefault(); S.manifest.demo.forEach((n, i) => setTimeout(() => { const a = document.createElement("a"); a.href = `demo/${n}`; a.download = n; a.click(); }, i * 150)); };
}

async function upload(files) {
  for (const file of files) {
    S.uploads.unshift({file: file.name, record: null, error: "Reading…"}); documents();
    const data = await new Promise(ok => { const fr = new FileReader(); fr.onload = () => ok(String(fr.result).split(",")[1] || ""); fr.readAsDataURL(file); });
    const r = await call("POST", "/api/upload", {}, {filename: file.name, mime: file.type || "text/plain", data});
    S.uploads[0] = r.status === 200 ? r.data : {file: file.name, error: r.data.error || "could not read"};
  }
  await refresh();
}
$("files").onchange = e => upload([...e.target.files]).then(() => { e.target.value = ""; });
["dragover", "dragenter"].forEach(t => $("drop").addEventListener(t, e => { e.preventDefault(); $("drop").classList.add("over"); }));
["dragleave", "drop"].forEach(t => $("drop").addEventListener(t, e => { e.preventDefault(); $("drop").classList.remove("over"); }));
$("drop").addEventListener("drop", e => upload([...e.dataTransfer.files]));
$("samples").onclick = async () => { const r = await call("POST", "/api/demo"); S.uploads = [...r.data, ...S.uploads]; await refresh(); };
$("reset").onclick = async () => { if (!confirm("Clear all documents, logs and mill data from this session?")) return; await call("POST", "/api/reset"); S.uploads = []; await refresh(); };

// ---------- dashboard ----------
function kpi(label, value, unit, foot) {
  return `<div class="card kpi"><div class="label">${label}</div><div class="value">${value}<span class="unit">${unit}</span></div><div class="foot">${foot}</div></div>`;
}
function niceMax(v) { const step = 10 ** Math.floor(Math.log10(v / 4)); return 4 * step * [1, 2, 2.5, 5, 10].find(m => step * m * 4 >= v); }
function costChart(curve) {
  const W = 720, H = 260, L = 56, R = 12, T = 14, B = 28, top = niceMax(Math.max(...curve.map(c => c.default)));
  const x = i => L + (W - L - R) * i / (curve.length - 1), y = v => H - B - (H - T - B) * v / top;
  let g = [0, .25, .5, .75, 1].map(t => `<line class="gridline" x1="${L}" x2="${W - R}" y1="${y(top * t)}" y2="${y(top * t)}"/><text x="${L - 8}" y="${y(top * t) + 4}" text-anchor="end">€${f(top * t / 1000, 0)}k</text>`).join("");
  g += curve.map((c, i) => `<text x="${x(i)}" y="${H - 8}" text-anchor="middle">${c.year}</text>`).join("");
  const line = k => curve.map((c, i) => `${x(i)},${y(c[k])}`).join(" ");
  return `<svg class="chart" viewBox="0 0 ${W} ${H}" role="img" aria-label="CBAM cost by year, on default values and with your data">${g}
    <polygon class="f-area" points="${x(0)},${y(0)} ${line("yours")} ${x(curve.length - 1)},${y(0)}"/><polyline class="s-bad" points="${line("default")}"/><polyline class="s-acc" points="${line("yours")}"/>
    ${curve.map((c, i) => `<circle class="f-acc" cx="${x(i)}" cy="${y(c.yours)}" r="3.5"><title>${c.year}: ${eur(c.yours)} with your data, ${eur(c.default)} with all steel on defaults</title></circle>`).join("")}</svg>`;
}

async function dashboard() {
  const you = S.state.plants[0];
  $("dashEmpty").hidden = !you.empty; $("dash").hidden = !!you.empty;
  if (you.empty) return;
  const a = (await call("GET", "/api/audit", {year: S.year})).data, steel = a.rows.filter(r => r.kind === "steel");
  const part = rows => rows.reduce((t, r) => t + r.tco2, 0) / you.output_t;
  const ver = part(steel.filter(r => !r.basis.startsWith("default"))), dft = part(steel.filter(r => r.basis.startsWith("default")));
  const yours = you.curve.reduce((t, c) => t + c.yours, 0), all = you.curve.reduce((t, c) => t + c.default, 0);
  const open = [...a.checks.map(c => ["bad", c]), ...a.plan.gaps.map(g => ["warn", g])];
  $("kpis").innerHTML =
    kpi("Embedded emissions", f(you.see_total), "tCO2/t", `<span class="pill ${you.verified_share < 1 ? "warn" : "ok"}">${pct(1 - you.verified_share)}</span> of steel on defaults`) +
    kpi("Steel on verified mill data", pct(you.verified_share), "", `<span class="pill info">${steel.length - steel.filter(r => r.basis.startsWith("default")).length} of ${steel.length}</span> heats on actual values`) +
    kpi("Importer cost, 2026–2034", eur(yours), "", all - yours > 1 ? `<span class="pill ok">−${eur(all - yours)}</span> against all defaults` : "Same as all defaults") +
    kpi("Open checks", open.length, "", open.length ? `<span class="pill warn">To close</span> before a verifier signs` : `<span class="pill ok">None</span>`);
  $("costChart").innerHTML = costChart(you.curve);
  const seg = (cls, v) => `<span class="${cls}" style="width:${Math.max(v, 0) / you.see_total * 100}%"></span>`;
  $("mix").innerHTML = `<h2>What makes up ${f(you.see_total)} tCO2/t</h2><p class="sub">Reporting year ${S.year}, output ${f(you.output_t, 0)} t</p>
    <div class="bar">${seg("c-direct", you.see_direct)}${seg("c-ok", ver)}${seg("c-bad", dft)}</div>
    ${[["c-direct", "Own furnaces (fuel)", you.see_direct], ["c-ok", "Steel, verified mill value", ver], ["c-bad", "Steel, EU default plus penalty", dft]]
      .map(([c, l, v]) => `<div class="rowline"><span><i class="${c}" style="display:inline-block;width:10px;height:10px;border-radius:3px;margin-right:8px"></i>${l}</span><b>${f(v)} <span class="muted">${pct(v / you.see_total)}</span></b></div>`).join("")}
    <p class="muted" style="margin-top:12px">Indirect emissions (electricity) are not counted for iron and steel goods.</p>`;
  $("network").innerHTML = `<table><thead><tr><th>Plant</th><th>Steel on verified data</th><th class="n">tCO2/t</th></tr></thead><tbody>
    ${S.state.plants.filter(p => !p.empty).map((p, i) => `<tr><td>${i ? esc(p.name) : `<b>${esc(p.name)}</b>`}</td>
      <td><div style="display:flex;gap:10px;align-items:center"><div class="progress" style="flex:1"><span style="width:${p.verified_share * 100}%"></span></div><span class="muted">${pct(p.verified_share)}</span></div></td>
      <td class="n">${f(p.see_total)}</td></tr>`).join("")}</tbody></table>`;
  $("checksList").innerHTML = open.length ? `<ul class="list">${open.map(([c, t]) => `<li><span class="dot ${c}"></span><span>${esc(t)}</span></li>`).join("")}</ul>` : `<p class="muted">None found by these rules.</p>`;
}

// ---------- monthly log ----------
async function monthlyLog() {
  const log = S.state.log;
  $("logTable").innerHTML = log.length ? `<table><thead><tr><th>Month</th><th>Item</th><th class="n">Opening</th><th class="n">Bought</th><th class="n">Closing</th><th class="n">Used or made</th></tr></thead><tbody>
    ${log.map(r => r.kind === "fuel"
      ? `<tr><td>${esc(r.month)}</td><td>${esc(r.fuel)}${r.meter ? `<div class="muted">${esc(r.meter)}</div>` : ""}</td><td class="n">${esc(r.opening)}</td><td class="n">${esc(r.purchased)}</td><td class="n">${esc(r.closing)}</td><td class="n"><b>${esc(r.used)} ${esc(r.unit)}</b></td></tr>`
      : `<tr><td>${esc(r.month)}</td><td>Production</td><td></td><td></td><td></td><td class="n"><b>${esc(r.output_t)} t</b></td></tr>`).join("")}</tbody></table>`
    : `<p class="muted">No months logged. Until you log, the number uses fuel bought, from invoices.</p>`;
  $("logChecks").innerHTML = S.state.checks.length ? `<ul class="list" style="margin-top:14px">${S.state.checks.map(c => `<li><span class="dot bad"></span><span>${esc(c)}</span></li>`).join("")}</ul>` : "";
}
async function addLog(e, kind) {
  e.preventDefault();
  const body = {kind};
  for (const el of e.target.elements) if (el.name) body[el.name] = el.type === "number" ? (el.value === "" ? null : Number(el.value)) : el.value;
  const r = await call("POST", "/api/log", {}, body);
  $("logErr").textContent = r.status === 200 ? "" : r.data.error;
  if (r.status === 200) { e.target.reset(); await refresh(); }
}
$("fuelForm").onsubmit = e => addLog(e, "fuel");
$("prodForm").onsubmit = e => addLog(e, "production");
$("sampleLog").onclick = async () => { await call("POST", "/api/demo_log"); $("logErr").textContent = ""; await refresh(); };

// ---------- mills ----------
async function mills() {
  const buyers = {};
  S.state.plants.filter(p => !p.empty).forEach(p => p.precursors.forEach(q => { buyers[q.supplier] = (buyers[q.supplier] || 0) + 1; }));
  const rows = Object.entries(S.state.suppliers);
  $("mills").innerHTML = `<table><thead><tr><th>Mill</th><th>Status</th><th class="n">Plants buying</th><th>Verified value</th></tr></thead><tbody>
    ${rows.map(([name, v], i) => `<tr><td><b>${esc(name)}</b></td>
      <td><span class="pill ${v.verified ? "ok" : "warn"}">${v.verified ? "Verified" : "On EU default"}</span></td>
      <td class="n">${buyers[name] || 0}</td>
      <td>${v.verified ? `${f(v.see)} tCO2/t<div class="muted">${esc(v.report)}</div>`
        : `<form class="form-row" data-mill="${i}" style="margin:0"><label>tCO2 per t <input type="number" inputmode="decimal" name="see" min="0.01" max="9.99" step="any" required></label>
           <label>Verification report <input name="report" maxlength="120" placeholder="Reference"></label><button class="btn small primary">Add verified data</button></form>`}</td></tr>`).join("")}</tbody></table>`;
  document.querySelectorAll("form[data-mill]").forEach(form => form.onsubmit = async e => {
    e.preventDefault();
    const r = await call("POST", "/api/supplier", {}, {name: rows[Number(form.dataset.mill)][0], see: Number(form.see.value), report: form.report.value});
    $("millErr").textContent = r.status === 200 ? "" : r.data.error;
    if (r.status === 200) await refresh();
  });
}

// ---------- report ----------
async function report() {
  const r = await call("GET", "/api/report", {year: S.year});
  if (r.status !== 200) {
    const missing = r.data.readiness.items.filter(i => i.required && !i.done);
    $("reportOut").innerHTML = `<section class="card empty"><b>The report needs ${missing.length} more ${missing.length === 1 ? "item" : "items"}</b>
      <p>${missing.map(i => esc(i.label)).join(" · ")}</p><a class="btn primary" href="#/documents">Upload documents</a></section>`;
    return;
  }
  const a = r.data, s = a.summary, today = new Date().toISOString().slice(0, 10);
  const chip = c => `<span class="chip"><b>${esc(c.role)}</b> · ${c.doc ? `<button class="linklike" data-doc="${esc(c.doc)}">${esc(c.file)}</button>` : esc(c.file)} “${esc(c.quote)}”</span>`;
  const basis = b => { if (!b) return ""; const [k, ...rest] = b.split(" "); return `<span class="pill ${k === "default" ? "bad" : "ok"}">${esc(k)}</span><div class="muted">${esc(rest.join(" "))}</div>`; };
  $("reportOut").innerHTML = `<div class="controls no-print" style="margin-bottom:16px">
      <button class="btn primary" type="button" onclick="window.print()">Print or save as PDF</button>
      <button class="btn" type="button" id="csv">Download EU supplier template (CSV)</button></div>
    <article class="card report">
      <span class="pill warn">Draft for verifier review</span>
      <h1>Carbon compliance report</h1>
      <p class="muted">${esc(s.name)} · goods CN 7318 (screws, bolts, nuts) · reporting year ${esc(s.year)} · prepared ${today}</p>
      <div class="summary">
        <div><span>Embedded emissions</span><b>${f(s.see_total)}</b> tCO2/t</div><div><span>Direct (own furnaces)</span><b>${f(s.see_direct)}</b></div>
        <div><span>Purchased steel</span><b>${f(s.see_precursor)}</b></div><div><span>Output</span><b>${f(s.output_t, 0)}</b> t</div>
        <div><span>Steel on verified data</span><b>${pct(s.verified_share)}</b></div></div>
      <h3>Method</h3><ul class="list">${a.method.map(l => `<li><span class="dot warn" style="background:var(--mute)"></span><span>${esc(l)}</span></li>`).join("")}</ul>
      <h3>Every figure and its source (${a.rows.length})</h3>
      <div class="table-wrap"><table><thead><tr><th>Figure</th><th class="n">tCO2</th><th>Basis</th><th>Sources</th></tr></thead><tbody>
        ${a.rows.map(x => `<tr><td>${esc(x.item)}</td><td class="n">${x.tco2 == null ? "" : f(x.tco2, 1)}</td><td>${basis(x.basis)}</td><td>${x.sources.map(chip).join("")}</td></tr>`).join("")}</tbody></table></div>
      <h3>Open checks and gaps</h3>${[...a.checks, ...a.plan.gaps].length ? `<ul class="list">${[...a.checks.map(c => ["bad", c]), ...a.plan.gaps.map(g => ["warn", g])].map(([c, t]) => `<li><span class="dot ${c}"></span><span>${esc(t)}</span></li>`).join("")}</ul>` : `<p class="muted">None found by these rules.</p>`}
      <h3>Notes</h3><p class="muted">${esc(a.draft)} ${esc(a.default_note)} The figures were read by software and calculated by fixed rules. An accredited verifier must check and sign before this is used in a CBAM declaration.</p>
      <div class="sign"><div>Prepared by (plant)</div><div>Verified by (accredited verifier) and date</div></div>
    </article>`;
  $("csv").onclick = async () => { const x = await call("GET", "/api/export", {year: S.year}); download(`cbam_report_${S.year}.csv`, x.data, "text/csv"); };
}

// ---------- start ----------
boot().then(() => {
  $("modeNote").textContent = S.mode === "browser" ? "Running in your browser · sample data only" : "Connected to the app server";
  return refresh();
}).catch(e => { $("loading").hidden = true; document.querySelector(".main").insertAdjacentHTML("afterbegin", `<div class="notice">Could not start: ${esc(e.message)}</div>`); });
