# frontend/app.py
import streamlit as st
import requests

API = "http://localhost:8000"

st.set_page_config(
    page_title="Aurum Extract",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background: #F0F6FF;
    color: #0A1628;
}

::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #E3EEFF; }
::-webkit-scrollbar-thumb { background: #1565C0; border-radius: 3px; }

/* ── Hero ── */
.hero {
    background: linear-gradient(135deg, #0A1628 0%, #1565C0 60%, #1E88E5 100%);
    border-radius: 16px;
    padding: 3rem 2.5rem 2.5rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -80px; right: -80px;
    width: 300px; height: 300px;
    background: radial-gradient(circle, #FFFFFF0A 0%, transparent 70%);
    border-radius: 50%;
}
.hero::after {
    content: '';
    position: absolute;
    bottom: -60px; left: 30%;
    width: 250px; height: 250px;
    background: radial-gradient(circle, #90CAF918 0%, transparent 70%);
    border-radius: 50%;
}
.hero-tag {
    display: inline-block;
    background: #FFFFFF14;
    border: 1px solid #FFFFFF22;
    color: #90CAF9;
    font-size: 0.68rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    padding: 0.3rem 0.9rem;
    border-radius: 20px;
    margin-bottom: 1.25rem;
    font-family: 'JetBrains Mono', monospace;
}
.hero-title {
    font-size: 3rem;
    font-weight: 700;
    color: #FFFFFF;
    letter-spacing: -0.03em;
    line-height: 1.1;
    margin-bottom: 0.5rem;
}
.hero-title span { color: #90CAF9; }
.hero-sub {
    font-size: 0.9rem;
    color: #FFFFFF88;
    font-weight: 300;
    letter-spacing: 0.02em;
    margin-bottom: 2rem;
}
.hero-chips {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
}
.hero-chip {
    background: #FFFFFF14;
    border: 1px solid #FFFFFF1A;
    color: #FFFFFFCC;
    font-size: 0.7rem;
    letter-spacing: 0.08em;
    padding: 0.3rem 0.8rem;
    border-radius: 6px;
    font-family: 'JetBrains Mono', monospace;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent;
    border-bottom: 2px solid #DBEAFE;
    gap: 0;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Inter', sans-serif;
    font-size: 0.8rem;
    font-weight: 500;
    letter-spacing: 0.03em;
    color: #6B8CC7;
    padding: 0.75rem 1.75rem;
    background: transparent;
    border: none;
    border-bottom: 2px solid transparent;
    margin-bottom: -2px;
}
.stTabs [aria-selected="true"] {
    color: #1565C0 !important;
    border-bottom: 2px solid #1565C0 !important;
    background: transparent !important;
}

/* ── Cards ── */
.card {
    background: #FFFFFF;
    border: 1px solid #DBEAFE;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 1px 3px #1565C008;
}
.card-header {
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #93B4E0;
    margin-bottom: 1rem;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid #EFF6FF;
    font-family: 'JetBrains Mono', monospace;
}

/* ── Field rows ── */
.f-row {
    display: grid;
    grid-template-columns: 150px 1fr auto;
    align-items: center;
    gap: 1rem;
    padding: 0.6rem 0;
    border-bottom: 1px solid #F0F6FF;
}
.f-row:last-child { border-bottom: none; }
.f-key {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.67rem;
    color: #93B4E0;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
.f-val {
    font-size: 0.88rem;
    color: #0A1628;
    font-weight: 500;
}
.f-null {
    font-size: 0.82rem;
    color: #CBD5E1;
    font-style: italic;
}
.f-note {
    font-size: 0.68rem;
    color: #93B4E0;
    font-style: italic;
}

/* ── Confidence badges ── */
.conf {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.08em;
    padding: 0.2rem 0.55rem;
    border-radius: 5px;
    font-weight: 500;
    white-space: nowrap;
}
.conf-high   { background: #DCFCE7; color: #15803D; border: 1px solid #BBF7D0; }
.conf-medium { background: #FEF9C3; color: #A16207; border: 1px solid #FEF08A; }
.conf-low    { background: #F1F5F9; color: #94A3B8; border: 1px solid #E2E8F0; }

/* ── Stats ── */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.75rem;
    margin-bottom: 1.5rem;
}
.stat-card {
    background: #FFFFFF;
    border: 1px solid #DBEAFE;
    border-radius: 10px;
    padding: 1rem;
    text-align: center;
    box-shadow: 0 1px 3px #1565C008;
}
.stat-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.8rem;
    font-weight: 700;
    line-height: 1;
}
.stat-lbl {
    font-size: 0.62rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #93B4E0;
    margin-top: 0.3rem;
}
.s-total  { color: #1565C0; }
.s-found  { color: #0288D1; }
.s-high   { color: #15803D; }
.s-medium { color: #A16207; }

/* ── Type badges ── */
.tbadge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.1em;
    padding: 0.2rem 0.6rem;
    border-radius: 5px;
    font-weight: 500;
}
.tb-invoice  { background: #EFF6FF; color: #1565C0; border: 1px solid #BFDBFE; }
.tb-resume   { background: #F0FDF4; color: #15803D; border: 1px solid #BBF7D0; }
.tb-contract { background: #FFF7ED; color: #C2410C; border: 1px solid #FED7AA; }
.tb-report   { background: #FAF5FF; color: #7E22CE; border: 1px solid #E9D5FF; }

/* ── Skills ── */
.skill-wrap { display: flex; flex-wrap: wrap; gap: 6px; margin: 0.5rem 0; }
.skill-pill {
    font-size: 0.72rem;
    background: #EFF6FF;
    color: #1565C0;
    border: 1px solid #BFDBFE;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-weight: 500;
}

/* ── Finding pills ── */
.finding-item {
    display: flex;
    align-items: flex-start;
    gap: 0.6rem;
    padding: 0.5rem 0;
    border-bottom: 1px solid #F0F6FF;
    font-size: 0.83rem;
    color: #1E3A5F;
    line-height: 1.5;
}
.finding-dot {
    width: 6px; height: 6px;
    background: #1565C0;
    border-radius: 50%;
    margin-top: 7px;
    flex-shrink: 0;
}

/* ── Buttons ── */
.stButton > button {
    font-family: 'Inter', sans-serif;
    font-size: 0.78rem;
    font-weight: 500;
    background: #FFFFFF;
    border: 1px solid #DBEAFE;
    color: #1565C0;
    padding: 0.55rem 1.25rem;
    border-radius: 8px;
    transition: all 0.15s ease;
    width: 100%;
}
.stButton > button:hover {
    background: #EFF6FF;
    border-color: #93C5FD;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #1565C0, #1E88E5);
    border: none;
    color: #FFFFFF;
    font-weight: 600;
    box-shadow: 0 2px 8px #1565C030;
}
.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #0D47A1, #1565C0);
    box-shadow: 0 4px 14px #1565C040;
    transform: translateY(-1px);
}

/* ── Download buttons ── */
.stDownloadButton > button {
    font-family: 'Inter', sans-serif;
    font-size: 0.72rem;
    font-weight: 500;
    background: #FFFFFF;
    border: 1px solid #DBEAFE;
    color: #1565C0;
    border-radius: 8px;
    padding: 0.45rem 1rem;
    width: 100%;
    transition: all 0.15s;
}
.stDownloadButton > button:hover {
    background: #EFF6FF;
    border-color: #93C5FD;
}

/* ── File uploader ── */
.stFileUploader {
    background: #FFFFFF !important;
    border: 2px dashed #BFDBFE !important;
    border-radius: 10px !important;
}
.stFileUploader:hover { border-color: #1565C0 !important; }

/* ── Selectbox ── */
.stSelectbox > div > div {
    background: #FFFFFF !important;
    border: 1px solid #DBEAFE !important;
    border-radius: 8px !important;
    color: #0A1628 !important;
}

/* ── Text inputs ── */
.stTextInput > div > div > input {
    background: #FFFFFF !important;
    border: 1px solid #DBEAFE !important;
    border-radius: 8px !important;
    color: #0A1628 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.8rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: #1565C0 !important;
    box-shadow: 0 0 0 3px #1565C015 !important;
}

/* ── Progress ── */
.stProgress > div > div {
    background: linear-gradient(90deg, #1565C0, #1E88E5) !important;
    border-radius: 4px !important;
}

/* ── Alert ── */
div[data-testid="stAlert"] {
    border-radius: 10px !important;
    border: 1px solid #DBEAFE !important;
    background: #EFF6FF !important;
}

/* ── Expander ── */
.streamlit-expanderHeader {
    background: #FFFFFF !important;
    border: 1px solid #DBEAFE !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    color: #1E3A5F !important;
}

/* ── Success banner ── */
.success-banner {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    background: #F0FDF4;
    border: 1px solid #BBF7D0;
    border-radius: 10px;
    padding: 0.75rem 1.1rem;
    margin-bottom: 1.25rem;
}
.success-icon { font-size: 1rem; }
.success-text { font-size: 0.82rem; color: #15803D; font-weight: 500; flex: 1; }

/* ── History row ── */
.hist-row {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.85rem 1rem;
    background: #FFFFFF;
    border: 1px solid #DBEAFE;
    border-radius: 8px;
    margin-bottom: 6px;
    transition: border-color 0.15s, box-shadow 0.15s;
}
.hist-row:hover {
    border-color: #93C5FD;
    box-shadow: 0 2px 8px #1565C010;
}
.hist-name { flex: 1; font-size: 0.85rem; font-weight: 500; color: #1E3A5F; }
.hist-time {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    color: #93B4E0;
}

/* ── Section divider ── */
.sec-divider {
    height: 1px;
    background: linear-gradient(90deg, #1565C020, #1E88E540, #1565C020);
    margin: 1.5rem 0;
    border: none;
}
</style>
""", unsafe_allow_html=True)

# ── HERO ──────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-tag">◆ AI-Powered Document Intelligence</div>
    <div class="hero-title">Aurum <span>Extract</span></div>
    <div class="hero-sub">Transform unstructured documents into clean, validated, structured data — instantly.</div>
    <div class="hero-chips">
        <span class="hero-chip">Gemini 2.5 Flash</span>
        <span class="hero-chip">Pydantic Validated</span>
        <span class="hero-chip">PDF · DOCX · TXT · Images</span>
        <span class="hero-chip">Invoice · Resume · Contract · Report</span>
        <span class="hero-chip">Confidence Scoring</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── HELPERS ───────────────────────────────────────────────────
CONF_BADGE = {
    "high":   '<span class="conf conf-high">🟢 High</span>',
    "medium": '<span class="conf conf-medium">🟡 Medium</span>',
    "low":    '<span class="conf conf-low">⚪ Low</span>',
}
TYPE_BADGE = {
    "invoice":  '<span class="tbadge tb-invoice">Invoice</span>',
    "resume":   '<span class="tbadge tb-resume">Resume</span>',
    "contract": '<span class="tbadge tb-contract">Contract</span>',
    "report":   '<span class="tbadge tb-report">Report</span>',
}

def render_field_row(key, data):
    if not isinstance(data, dict): return
    val   = data.get("value")
    conf  = data.get("confidence", "low")
    note  = data.get("note", "") or ""
    badge = CONF_BADGE.get(conf, "")
    vhtml = f'<span class="f-val">{val}</span>' if val else f'<span class="f-null">—</span>'
    nhtml = f'<br><span class="f-note">ℹ {note}</span>' if (note and not val) else ""
    st.markdown(f"""
    <div class="f-row">
        <span class="f-key">{key.replace('_',' ')}</span>
        <span>{vhtml}{nhtml}</span>
        {badge}
    </div>""", unsafe_allow_html=True)

def render_editable_fields(result, doc_type, extraction_id, prefix=""):
    uid = f"{prefix}_{extraction_id}"
    corrections = {}
    scalar = {k: v for k, v in result.items() if isinstance(v, dict)}
    lists  = {k: v for k, v in result.items() if isinstance(v, list)}

    # Stats
    total  = len(scalar)
    found  = sum(1 for v in scalar.values() if v.get("value"))
    high   = sum(1 for v in scalar.values() if v.get("confidence") == "high")
    medium = sum(1 for v in scalar.values() if v.get("confidence") == "medium")

    st.markdown(f"""
    <div class="stats-grid">
        <div class="stat-card"><div class="stat-num s-total">{total}</div><div class="stat-lbl">Total Fields</div></div>
        <div class="stat-card"><div class="stat-num s-found">{found}</div><div class="stat-lbl">Extracted</div></div>
        <div class="stat-card"><div class="stat-num s-high">{high}</div><div class="stat-lbl">High Conf</div></div>
        <div class="stat-card"><div class="stat-num s-medium">{medium}</div><div class="stat-lbl">Medium Conf</div></div>
    </div>""", unsafe_allow_html=True)

    # Scalar fields
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-header">Extracted Fields</div>', unsafe_allow_html=True)
    for k, v in scalar.items():
        render_field_row(k, v)
    st.markdown('</div>', unsafe_allow_html=True)

    # Skills
    if lists.get("skills"):
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-header">Skills</div>', unsafe_allow_html=True)
        pills = "".join(f'<span class="skill-pill">{s}</span>' for s in lists["skills"])
        st.markdown(f'<div class="skill-wrap">{pills}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Experience
    if lists.get("experience"):
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-header">Experience</div>', unsafe_allow_html=True)
        for exp in lists["experience"]:
            st.markdown(f"""
            <div class="finding-item" style="flex-direction:column;align-items:flex-start;gap:2px">
                <span style="font-weight:600;color:#0A1628">{exp.get('role','—')}
                  <span style="color:#93B4E0;font-weight:400"> at </span>{exp.get('company','—')}</span>
                <span style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;color:#93B4E0">{exp.get('duration','')}</span>
                <span style="font-size:0.8rem;color:#4A6FA5;margin-top:2px">{exp.get('description','')}</span>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Education
    if lists.get("education"):
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-header">Education</div>', unsafe_allow_html=True)
        for edu in lists["education"]:
            st.markdown(f"""
            <div class="f-row">
                <span class="f-key">{edu.get('year','—')}</span>
                <span class="f-val">{edu.get('degree','—')} — {edu.get('institution','—')}</span>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Parties (contract)
    if lists.get("parties"):
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-header">Parties</div>', unsafe_allow_html=True)
        for p in lists["parties"]:
            st.markdown(f"""
            <div class="f-row">
                <span class="f-key">{p.get('role','—')}</span>
                <span class="f-val">{p.get('name','—')}</span>
                <span style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;color:#93B4E0">{p.get('email','')}</span>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Key findings / recommendations (report)
    for list_key, label in [("key_findings","Key Findings"), ("recommendations","Recommendations")]:
        if lists.get(list_key):
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(f'<div class="card-header">{label}</div>', unsafe_allow_html=True)
            for item in lists[list_key]:
                st.markdown(f'<div class="finding-item"><div class="finding-dot"></div><span>{item}</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # Line items (invoice)
    if lists.get("line_items"):
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-header">Line Items</div>', unsafe_allow_html=True)
        st.table(lists["line_items"])
        st.markdown('</div>', unsafe_allow_html=True)

    # Edit
    st.markdown('<div class="sec-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-header">Edit & Correct Fields</div>', unsafe_allow_html=True)
    for k, v in scalar.items():
        new_val = st.text_input(
            k.replace("_", " ").title(),
            value=v.get("value") or "",
            key=f"{uid}_{k}"
        )
        if new_val != (v.get("value") or ""):
            corrections[k] = new_val
    st.markdown('</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        if corrections:
            if st.button("💾 Save Corrections", key=f"save_{uid}", type="primary"):
                r = requests.patch(f"{API}/extractions/{extraction_id}/correct", json=corrections)
                if r.status_code == 200:
                    st.success("Corrections saved successfully.")
                    st.rerun()
                else:
                    st.error("Failed to save.")
    with c2:
        csv = requests.get(f"{API}/extractions/{extraction_id}/export?format=csv")
        st.download_button("📄 Export CSV", csv.content,
                           file_name=f"{extraction_id}.csv", mime="text/csv",
                           key=f"csv_{uid}")
    with c3:
        xl = requests.get(f"{API}/extractions/{extraction_id}/export?format=excel")
        st.download_button("📊 Export Excel", xl.content,
                           file_name=f"{extraction_id}.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                           key=f"xl_{uid}")

# ── TABS ──────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["Extract Document", "Batch Upload", "History"])

# ── TAB 1 ─────────────────────────────────────────────────────
with tab1:
    left, right = st.columns([1, 1], gap="large")
    with left:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-header">Document Type</div>', unsafe_allow_html=True)
        doc_type = st.selectbox("", ["invoice", "resume", "contract", "report"],
                                key="s_type", label_visibility="collapsed",
                                format_func=lambda x: {
                                    "invoice":"🧾 Invoice",
                                    "resume":"👤 Resume",
                                    "contract":"📋 Contract",
                                    "report":"📊 Report / Custom Doc"
                                }[x])
        st.markdown('<div class="card-header" style="margin-top:1rem">Upload File</div>', unsafe_allow_html=True)
        uploaded = st.file_uploader("",
                                    type=["pdf","txt","docx","png","jpg","jpeg"],
                                    key="s_file", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        extract_clicked = st.button("Extract", type="primary", key="s_btn",
                                    disabled=not uploaded)

    with right:
        if uploaded and extract_clicked:
            with st.spinner("Analysing document with Gemini..."):
                resp = requests.post(f"{API}/extract",
                    files={"file": (uploaded.name, uploaded, uploaded.type)},
                    data={"document_type": doc_type})
            if resp.status_code == 200:
                st.session_state["last"] = resp.json()
            else:
                st.error(resp.json().get("detail", "Extraction failed."))

        if "last" in st.session_state:
            d = st.session_state["last"]
            st.markdown(f"""
            <div class="success-banner">
                <span class="success-icon">✅</span>
                <span class="success-text">{d['filename']} extracted successfully</span>
                {TYPE_BADGE.get(d['document_type'],'')}
            </div>""", unsafe_allow_html=True)
            render_editable_fields(d["result"], d["document_type"], d["id"], prefix="t1")
            with st.expander("View Raw JSON"):
                st.json(d["result"])

# ── TAB 2 ─────────────────────────────────────────────────────
with tab2:
    left, right = st.columns([1, 2], gap="large")
    with left:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-header">Document Type</div>', unsafe_allow_html=True)
        b_type = st.selectbox("", ["invoice","resume","contract","report"],
                              key="b_type", label_visibility="collapsed",
                              format_func=lambda x: {
                                  "invoice":"🧾 Invoice",
                                  "resume":"👤 Resume",
                                  "contract":"📋 Contract",
                                  "report":"📊 Report / Custom Doc"
                              }[x])
        st.markdown('<div class="card-header" style="margin-top:1rem">Upload Files</div>', unsafe_allow_html=True)
        b_files = st.file_uploader("",
                                   type=["pdf","txt","docx","png","jpg","jpeg"],
                                   accept_multiple_files=True,
                                   key="b_files", label_visibility="collapsed")
        if b_files:
            st.markdown(f'<p style="font-size:0.75rem;color:#1565C0;margin-top:0.5rem">📁 {len(b_files)} file(s) queued</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        b_run = st.button("Extract All", type="primary", key="b_btn", disabled=not b_files)

    with right:
        if b_files and b_run:
            prog = st.progress(0)
            log  = st.empty()
            rows = []
            for i, f in enumerate(b_files):
                log.markdown(f'<p style="font-size:0.78rem;color:#1565C0">Processing {f.name} ({i+1}/{len(b_files)})...</p>', unsafe_allow_html=True)
                r = requests.post(f"{API}/extract",
                    files={"file": (f.name, f, f.type)},
                    data={"document_type": b_type})
                ok  = r.status_code == 200
                rid = r.json().get("id","—") if ok else "—"
                rows.append({"file": f.name, "ok": ok, "id": rid,
                             "error": "" if ok else r.json().get("detail","")})
                prog.progress((i+1)/len(b_files))
            log.empty()

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="card-header">Queue Results</div>', unsafe_allow_html=True)
            for row in rows:
                icon  = "✅" if row["ok"] else "❌"
                color = "#15803D" if row["ok"] else "#DC2626"
                st.markdown(f"""
                <div class="hist-row">
                    <span>{icon}</span>
                    <span class="hist-name">{row['file']}</span>
                    <span class="hist-time">{row['id'][:8] if row['ok'] else row['error'][:40]}</span>
                </div>""", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            for row in rows:
                if row["ok"]:
                    with st.expander(f"📄 {row['file']}"):
                        detail = requests.get(f"{API}/extractions/{row['id']}").json()
                        render_editable_fields(detail["result"], b_type, row["id"], prefix="t2")

# ── TAB 3 ─────────────────────────────────────────────────────
with tab3:
    c1, c2 = st.columns([5, 1])
    with c1:
        st.markdown('<p style="font-size:0.78rem;color:#93B4E0;margin-bottom:1rem">All past extractions stored in SQLite — click any record to view, edit, or export.</p>', unsafe_allow_html=True)
    with c2:
        if st.button("Refresh", key="ref"):
            st.rerun()

    records = requests.get(f"{API}/extractions").json()
    if not records:
        st.markdown('<div class="card"><p style="color:#CBD5E1;font-size:0.85rem;text-align:center;padding:2rem 0">No extractions yet. Upload a document to get started.</p></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<p style="font-size:0.72rem;color:#93B4E0;margin-bottom:0.75rem">{len(records)} record(s) found</p>', unsafe_allow_html=True)
        for rec in records:
            with st.expander(f"{rec['filename']}   ·   {rec['timestamp'][:19].replace('T',' ')}"):
                st.markdown(TYPE_BADGE.get(rec["document_type"],""), unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                detail = requests.get(f"{API}/extractions/{rec['id']}").json()
                render_editable_fields(detail["result"], rec["document_type"], rec["id"], prefix="t3")