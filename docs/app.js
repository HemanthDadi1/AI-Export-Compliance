// The app talks to one router (server.dispatch). With the Python server it uses HTTP.
// On GitHub Pages there is no server, so the same Python files run in the browser with Pyodide.
const $ = id => document.getElementById(id);
const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const f = (x, d = 2) => Number(x).toLocaleString("en-GB", {maximumFractionDigits:d, minimumFractionDigits:d});
const pct = x => f(x * 100, 0) + "%";
const eur = x => "€" + Math.round(x).toLocaleString("en-GB");
const PYODIDE = "https://cdn.jsdelivr.net/pyodide/v0.26.4/full/pyodide.js";
const VIEWS = ["documents", "dashboard", "log", "mills", "report"];
const S = {mode: null, py: null, year: 2027, notes: [], docs: [], drafts: {}, state: null, ready: null, manifest: {py: [], demo: []}};

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
  S.docs = (await call("GET", "/api/docs")).data;
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
  document.title = `${$("title").textContent} · CBAM · CImEx Compliance`;
  await ({documents, dashboard, log: monthlyLog, mills, report})[v]();
}

window.addEventListener("hashchange", () => { window.scrollTo(0, 0); show(); });
$("create").onclick = () => { location.hash = "#/report"; };
for (let y = 2026; y <= 2034; y++) $("year").add(new Option(`Reporting year ${y}`, y, false, y === S.year));
$("year").onchange = () => { S.year = Number($("year").value); refresh(); };

// ---------- documents: upload, then check what we read ----------
const KIND = {mtc: "Mill test certificate", steel_invoice: "Steel purchase invoice", fuel_invoice: "Fuel invoice", production: "Production record", other: "Other"};
const FUELS = {lpg: "LPG", diesel: "Diesel", natural_gas: "Natural gas"};
const rowsOf = rec => rec.heats && rec.heats.length ? rec.heats.map(h => ({heat_no: h.heat_no ?? "", tonnes: h.tonnes ?? ""}))
  : [{heat_no: rec.heat_no ?? "", tonnes: rec.steel_tonnes ?? ""}];
const draftOf = d => S.drafts[d.id] ||= {...d.record, rows: rowsOf(d.record)};
const opts = (map, cur) => Object.entries(map).map(([k, v]) => `<option value="${k}" ${k === cur ? "selected" : ""}>${v}</option>`).join("");

function fieldsFor(dr) {
  const num = (name, label, v) => `<label>${label}<input type="number" inputmode="decimal" step="any" min="0" data-f="${name}" value="${esc(v ?? "")}"></label>`;
  const txt = (name, label, v, wide) => `<label class="${wide ? "wide" : ""}">${label}<input data-f="${name}" maxlength="120" value="${esc(v ?? "")}"></label>`;
  const t = dr.doc_type;
  if (t === "mtc" || t === "steel_invoice") {
    const heats = dr.rows.map((h, i) => `<label>Heat number<input data-row="${i}" data-k="heat_no" maxlength="60" value="${esc(h.heat_no)}"></label>
      <label>Steel tonnes<input type="number" inputmode="decimal" step="any" min="0" data-row="${i}" data-k="tonnes" value="${esc(h.tonnes)}"></label>`).join("");
    return (t === "mtc" ? txt("supplier", "Steel mill that made it", dr.supplier, true) : "") + heats;
  }
  if (t === "fuel_invoice") return `<label>Fuel<select data-f="fuel"><option value="">Choose</option>${opts(FUELS, dr.fuel)}</select></label>${num("quantity", "Quantity", dr.quantity)}
    <label>Unit<select data-f="unit"><option value="">Choose</option>${opts({t: "t", kg: "kg", litre: "litre", m3: "m3"}, dr.unit)}</select></label>`;
  if (t === "production") return num("output_tonnes", "Output (t)", dr.output_tonnes) + txt("cn_code", "CN code", dr.cn_code);
  return `<p class="muted wide" style="grid-column:1/-1">We could not tell what this is. Pick the right type above.</p>`;
}

function docCard(d) {
  const dr = draftOf(d), bad = d.issues.length;
  const state = bad ? ["bad", "Needs a look"] : d.reviewed ? ["ok", "Confirmed"] : ["warn", "To confirm"];
  return `<article class="card doc-card ${bad ? "needs" : d.reviewed ? "done" : ""}" data-id="${esc(d.id)}">
    <div class="doc-head"><b>${esc(d.name)}</b><span class="pill ${state[0]}">${state[1]}</span></div>
    ${d.record.quote ? `<div class="doc-quote">From the file: “${esc(d.record.quote)}” · <button class="linklike" data-doc="${esc(d.id)}">Open original</button></div>` : `<div class="doc-quote"><button class="linklike" data-doc="${esc(d.id)}">Open original</button></div>`}
    <div class="doc-fields"><label class="wide">What is this?<select data-f="doc_type">${opts(KIND, dr.doc_type)}</select></label>${fieldsFor(dr)}</div>
    ${bad ? `<ul class="list">${d.issues.map(i => `<li><span class="dot bad"></span><span>${esc(i)}</span></li>`).join("")}</ul>` : ""}
    ${d.edits.length ? `<p class="muted">Edited: ${d.edits.map(e => `${esc(e.field)} ${esc(e.from ?? "empty")} → ${esc(e.to ?? "empty")}`).join(", ")}</p>` : ""}
    <p class="error" role="alert"></p>
    <div class="doc-foot"><button class="btn small" data-remove type="button">Remove file</button><button class="btn small primary" data-confirm type="button">${d.reviewed ? "Save changes" : "Confirm"}</button></div>
  </article>`;
}

function patchOf(d, dr) {
  const o = d.record, patch = {}, same = (a, b) => (a ?? "") === (b ?? "");
  const n = v => v === "" || v == null ? null : Number(v);
  for (const k of ["doc_type", "supplier", "fuel", "unit", "cn_code"]) if (!same(dr[k], o[k])) patch[k] = dr[k] === "" ? null : dr[k];
  for (const k of ["quantity", "output_tonnes"]) if (n(dr[k]) !== n(o[k])) patch[k] = n(dr[k]);
  const orig = rowsOf(o), changed = dr.rows.some((h, i) => !same(h.heat_no, orig[i].heat_no) || n(h.tonnes) !== n(orig[i].tonnes));
  if (changed) {
    if (o.heats && o.heats.length) patch.heats = dr.rows.map(h => ({heat_no: h.heat_no || null, tonnes: n(h.tonnes)}));
    else Object.assign(patch, {heat_no: dr.rows[0].heat_no || null, steel_tonnes: n(dr.rows[0].tonnes)});
  }
  return patch;
}

async function documents() {
  $("browserNote").hidden = S.mode !== "browser";
  const r = S.ready, total = S.docs.length, ok = S.docs.filter(d => d.reviewed).length;
  $("readyLine").textContent = r.ready ? "Everything required is in and confirmed. You can create the report." : `${r.done} of ${r.total} required items are done.`;
  $("checklist").innerHTML = r.items.map(i => `<div class="card check"><span class="tick ${i.done ? "on" : ""}" aria-hidden="true">✓</span>
    <div><b>${esc(i.label)}</b><p>${esc(i.hint)}</p><span class="pill ${i.done ? "ok" : i.required ? "warn" : "info"}">${i.done ? "Done" : i.required ? "Required" : "Recommended"}</span></div></div>`).join("");
  $("uploadNotes").innerHTML = S.notes.length ? `<div class="notice no-print">${S.notes.map(n => `<div><b>${esc(n.file)}</b>: ${esc(n.error)}</div>`).join("")} <button class="linklike" id="dismissNotes" type="button">Dismiss</button></div>` : "";
  if (S.notes.length) $("dismissNotes").onclick = () => { S.notes = []; documents(); };
  $("reviewLine").textContent = total ? `${ok} of ${total} files confirmed. Values count toward your number only after you confirm them.` : "Upload files above, or load the samples. Each one appears here to check.";
  $("confirmAll").disabled = !total || ok === total;
  $("reviewGrid").innerHTML = total ? [...S.docs].sort((a, b) => (b.issues.length > 0) - (a.issues.length > 0) || a.reviewed - b.reviewed).map(docCard).join("")
    : `<div class="card empty" style="grid-column:1/-1"><b>No files yet</b><p>Drop the plant's documents above, or load the sample documents to see how it works.</p></div>`;
  $("samplePack").onclick = e => { e.preventDefault(); S.manifest.demo.forEach((n, i) => setTimeout(() => { const a = document.createElement("a"); a.href = `demo/${n}`; a.download = n; a.click(); }, i * 150)); };
}

$("reviewGrid").addEventListener("input", e => {
  const card = e.target.closest(".doc-card"); if (!card) return;
  const dr = S.drafts[card.dataset.id], t = e.target;
  if (t.dataset.row != null) dr.rows[Number(t.dataset.row)][t.dataset.k] = t.value; else if (t.dataset.f) dr[t.dataset.f] = t.value;
});
$("reviewGrid").addEventListener("change", e => {
  if (e.target.dataset.f !== "doc_type") return;
  const card = e.target.closest(".doc-card"), d = S.docs.find(x => x.id === card.dataset.id);
  card.outerHTML = docCard(d);
});
$("reviewGrid").addEventListener("click", async e => {
  const card = e.target.closest(".doc-card"); if (!card) return;
  const d = S.docs.find(x => x.id === card.dataset.id), err = card.querySelector(".error");
  if (e.target.matches("[data-confirm]")) {
    const r = await call("POST", "/api/review", {}, {doc: d.id, record: patchOf(d, S.drafts[d.id])});
    if (r.status !== 200) { err.textContent = r.data.error; return; }
    delete S.drafts[d.id]; await refresh();
  } else if (e.target.matches("[data-remove]")) {
    if (!confirm(`Remove ${d.name}? Its figures leave your number.`)) return;
    await call("POST", "/api/doc_remove", {}, {doc: d.id}); delete S.drafts[d.id]; await refresh();
  }
});
$("confirmAll").onclick = async () => { S.drafts = {}; await call("POST", "/api/review_all"); await refresh(); };

async function upload(files) {
  for (const file of files) {
    const data = await new Promise(ok => { const fr = new FileReader(); fr.onload = () => ok(String(fr.result).split(",")[1] || ""); fr.readAsDataURL(file); });
    const r = await call("POST", "/api/upload", {}, {filename: file.name, mime: file.type || "text/plain", data});
    if (r.status !== 200) S.notes.push({file: file.name, error: r.data.error || "could not read"});
    else if (r.data.error && !r.data.doc) S.notes.push({file: file.name, error: r.data.error});  // a repeat or an unreadable file is not stored
  }
  await refresh();
}
$("files").onchange = e => upload([...e.target.files]).then(() => { e.target.value = ""; });
["dragover", "dragenter"].forEach(t => $("drop").addEventListener(t, e => { e.preventDefault(); $("drop").classList.add("over"); }));
["dragleave", "drop"].forEach(t => $("drop").addEventListener(t, e => { e.preventDefault(); $("drop").classList.remove("over"); }));
$("drop").addEventListener("drop", e => upload([...e.dataTransfer.files]));
$("samples").onclick = async () => {
  const r = await call("POST", "/api/demo");
  S.notes = r.data.filter(x => x.error && !x.doc).map(x => ({file: x.file, error: x.error}));
  await refresh();
};
$("reset").onclick = async () => { if (!confirm("Clear all documents, logs and mill data from this session?")) return; await call("POST", "/api/reset"); S.notes = []; S.drafts = {}; await refresh(); };

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
    ${curve.map((c, i) => `<circle class="f-acc" cx="${x(i)}" cy="${y(c.yours)}" r="3.5"><title>${c.year}: ${eur(c.yours)} with your data, ${eur(c.default)} on the EU default for your goods</title></circle>`).join("")}</svg>`;
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
  const todo = S.docs.filter(d => !d.reviewed).length;
  $("reviewBanner").innerHTML = todo ? `<div class="notice">${todo} of ${S.docs.length} documents are not confirmed yet, so these numbers are a draft. <a href="#/documents">Check and confirm them</a>.</div>` : "";
  const mills = you.precursors.filter(p => p.basis === "default").sort((x, y) => y.tonnes - x.tonnes), all_t = you.precursors.reduce((t, p) => t + p.tonnes, 0);
  if (mills.length) {
    const m = mills[0], heats = m.heats.map(h => h.heat).join(", ");
    $("attention").innerHTML = `<div class="attention"><span class="icon" aria-hidden="true">!</span><div><b>Attention: ${esc(m.supplier)} is your biggest gap</b>
      <p>It supplied ${f(m.tonnes, 0)} t (${pct(m.tonnes / all_t)} of your steel) and has no verified data, so that steel is on the EU default plus a penalty. Asking this mill for its verified value is the single biggest change you can make.</p>
      <div class="row"><button class="btn small accent" id="copyAsk" type="button">Copy a request to the mill</button><a class="btn small" href="#/mills">Open Mills</a></div></div></div>`;
    $("copyAsk").onclick = async e => {
      const text = `Subject: Verified emissions data for steel you supplied to ${you.name.replace(" (your plant)", "")}

Hello,

Our EU buyers need verified embedded-emissions data for the steel we buy from you (heats ${heats}). Please share your verified value in tCO2 per tonne of steel and the verification report reference. With it we report your actual value instead of the EU default, which lowers the cost for us and for every other customer of yours.

Thank you,
${you.name.replace(" (your plant)", "")}`;
      try { await navigator.clipboard.writeText(text); e.target.textContent = "Copied. Paste it into an email"; } catch (x) { e.target.textContent = "Could not copy"; }
    };
  } else $("attention").innerHTML = `<div class="attention calm"><span class="icon" aria-hidden="true">✓</span><div><b>All your steel is on verified mill data</b><p>Nothing to chase. Close the open checks below and create the report.</p></div></div>`;
  $("kpis").innerHTML =
    kpi("Embedded emissions", f(you.see_total), "tCO2/t", `<span class="pill ${you.verified_share < 1 ? "warn" : "ok"}">${pct(1 - you.verified_share)}</span> of steel on defaults`) +
    kpi("Steel on verified mill data", pct(you.verified_share), "", `<span class="pill info">${steel.length - steel.filter(r => r.basis.startsWith("default")).length} of ${steel.length}</span> heats on actual values`) +
    kpi("Importer cost, 2026–2034", eur(yours), "", all - yours > 1 ? `<span class="pill ok">−${eur(all - yours)}</span> against the EU default` : "No saving against the EU default") +
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
  const buyers = {}, mine = {}, you = S.state.plants[0], total = you.empty ? 0 : you.precursors.reduce((t, p) => t + p.tonnes, 0);
  S.state.plants.filter(p => !p.empty).forEach(p => p.precursors.forEach(q => { buyers[q.supplier] = (buyers[q.supplier] || 0) + 1; }));
  if (!you.empty) you.precursors.forEach(p => { mine[p.supplier] = p.tonnes; });
  const rows = Object.entries(S.state.suppliers).sort((a, b) => (mine[b[0]] || 0) - (mine[a[0]] || 0));
  $("mills").innerHTML = `<table><thead><tr><th>Mill</th><th>Status</th><th class="n">Your steel</th><th class="n">Plants buying</th><th>Verified value</th></tr></thead><tbody>
    ${rows.map(([name, v], i) => `<tr><td><b>${esc(name)}</b></td>
      <td><span class="pill ${v.verified ? "ok" : "warn"}">${v.verified ? "Verified" : "On EU default"}</span></td>
      <td class="n">${mine[name] ? `${f(mine[name], 0)} t <span class="muted">${pct(mine[name] / total)}</span>` : `<span class="muted">none</span>`}</td>
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
  const chip = c => `<span class="chip"><b>${esc(c.role)}</b> · ${c.doc ? `<button class="linklike" data-doc="${esc(c.doc)}">${esc(c.file)}</button>` : esc(c.file)} “${esc(c.quote)}”${c.edited ? ` <span class="pill warn">edited by clerk</span>` : ""}</span>`;
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
      <h3>Review by the plant</h3><p class="muted">${a.review.confirmed} of ${a.review.documents} documents were checked and confirmed by the plant. ${a.review.edited ? `${a.review.edited} had values corrected:` : "No values were changed."}</p>
      ${a.review.edits.length ? `<ul class="list">${a.review.edits.map(e => `<li><span class="dot warn"></span><span>${esc(e.file)}: ${esc(e.field)} was ${esc(e.from ?? "empty")}, now ${esc(e.to ?? "empty")}</span></li>`).join("")}</ul>` : ""}
      <h3>Open checks and gaps</h3>${[...a.checks, ...a.plan.gaps].length ? `<ul class="list">${[...a.checks.map(c => ["bad", c]), ...a.plan.gaps.map(g => ["warn", g])].map(([c, t]) => `<li><span class="dot ${c}"></span><span>${esc(t)}</span></li>`).join("")}</ul>` : `<p class="muted">None found by these rules.</p>`}
      <h3>Notes</h3><p class="muted">${esc(a.draft)} ${esc(a.default_note)} The figures were read by software and calculated by fixed rules. An accredited verifier must check and sign before this is used in a CBAM declaration.</p>
      <div class="sign"><div>Prepared by (plant)</div><div>Verified by (accredited verifier) and date</div></div>
    </article>`;
  $("csv").onclick = async () => { const x = await call("GET", "/api/export", {year: S.year}); download(`cbam_report_${S.year}.csv`, x.data, "text/csv"); };
}

// ---------- product menu ----------
document.addEventListener("click", e => { const m = $("productMenu"); if (m.open && !m.contains(e.target)) m.open = false; });
document.addEventListener("keydown", e => { if (e.key === "Escape") $("productMenu").open = false; });

// ---------- start ----------
boot().then(() => {
  $("modeNote").textContent = S.mode === "browser" ? "Running in your browser · sample data only" : "Connected to the app server";
  return refresh();
}).catch(e => { $("loading").hidden = true; document.querySelector(".main").insertAdjacentHTML("afterbegin", `<div class="notice">Could not start: ${esc(e.message)}</div>`); });
