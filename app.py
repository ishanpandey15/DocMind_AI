import streamlit as st
from pathlib import Path

# ── Page config (MUST be first Streamlit call) ────────────────────────────────
st.set_page_config(
    page_title="DocMind AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:ital,wght@0,300;0,400;0,500;1,300&display=swap');

:root {
    --bg:         #07090f;
    --bg2:        #0d1017;
    --card:       #121620;
    --border:     #1e2535;
    --border2:    #2a3347;
    --cyan:       #22d3ee;
    --violet:     #818cf8;
    --green:      #34d399;
    --amber:      #fbbf24;
    --red:        #f87171;
    --text:       #e2e8f0;
    --muted:      #64748b;
    --dim:        #334155;
}

*, html, body { box-sizing: border-box; }

[data-testid="stAppViewContainer"],
[data-testid="stApp"] {
    background: var(--bg) !important;
    font-family: 'Space Grotesk', sans-serif;
    color: var(--text);
}

[data-testid="stSidebar"] {
    background: var(--bg2) !important;
    border-right: 1px solid var(--border) !important;
}

[data-testid="stHeader"] { display: none !important; }
.block-container { padding-top: 1.2rem !important; max-width: 900px !important; }

/* ── Top Header Bar ── */
.top-bar {
    display: flex; align-items: center; justify-content: space-between;
    padding-bottom: 1.2rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.4rem;
}
.brand { display: flex; align-items: center; gap: 12px; }
.brand-icon {
    width: 40px; height: 40px; border-radius: 10px;
    background: linear-gradient(135deg, #0ea5e9, #6366f1);
    display: flex; align-items: center; justify-content: center;
    font-size: 20px; flex-shrink: 0;
}
.brand-name {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.45rem; font-weight: 700;
    background: linear-gradient(90deg, var(--cyan), var(--violet));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin: 0; letter-spacing: -0.3px;
}
.brand-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem; color: var(--muted);
    letter-spacing: 2px; text-transform: uppercase; margin: 0;
}
.pills { display: flex; gap: 8px; flex-wrap: wrap; }
.pill {
    background: var(--card); border: 1px solid var(--border2);
    border-radius: 20px; padding: 4px 12px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem; color: var(--muted);
    display: flex; align-items: center; gap: 5px;
}
.pill .v { color: var(--cyan); font-weight: 600; }

/* ── Chat Messages ── */
.msg { display: flex; gap: 10px; margin-bottom: 16px; animation: fadeUp .25s ease; }
@keyframes fadeUp {
    from { opacity:0; transform:translateY(6px); }
    to   { opacity:1; transform:translateY(0); }
}
.msg.user { flex-direction: row-reverse; }

.avatar {
    width: 32px; height: 32px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 15px; flex-shrink: 0; margin-top: 3px;
}
.avatar.ai {
    background: linear-gradient(135deg,#0ea5e920,#6366f130);
    border: 1px solid #6366f150;
}
.avatar.user { background: var(--card); border: 1px solid var(--border2); }

.bubble {
    max-width: 80%; padding: 11px 15px;
    border-radius: 14px; font-size: 0.88rem; line-height: 1.7;
    border: 1px solid var(--border);
    background: var(--card); color: var(--text);
}
.msg.user .bubble {
    background: linear-gradient(135deg,#0c1929,#0f172a);
    border-color: #1e3a5f; border-radius: 14px 4px 14px 14px;
}
.msg.ai .bubble { border-radius: 4px 14px 14px 14px; }

/* Sources */
.src-wrap { margin-top: 10px; }
.src-label {
    font-family: 'JetBrains Mono', monospace; font-size: 0.63rem;
    color: var(--violet); cursor: pointer; letter-spacing: .3px;
}
.src-chip {
    display: inline-block; margin: 3px 3px 0 0;
    background: #160f2e; border: 1px solid #3b2f6e;
    border-radius: 5px; padding: 3px 9px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem; color: #a5b4fc;
}
.src-box {
    background: #0a0a14; border-left: 2px solid var(--violet);
    border-radius: 0 6px 6px 0; padding: 9px 13px; margin: 6px 0;
    font-family: 'JetBrains Mono', monospace; font-size: 0.68rem;
    line-height: 1.6; color: var(--muted); max-height: 110px; overflow-y: auto;
}

/* Welcome card */
.welcome {
    background: var(--card); border: 1px solid var(--border);
    border-radius: 16px; padding: 32px; text-align: center; margin: 8px 0 20px;
}
.welcome h3 {
    font-family: 'Space Grotesk', sans-serif; font-weight: 700;
    font-size: 1.1rem; margin: 12px 0 8px; color: var(--text);
}
.welcome p { font-size: 0.82rem; color: var(--muted); margin: 0 0 18px; line-height: 1.6; }
.eg-chips { display: flex; gap: 8px; flex-wrap: wrap; justify-content: center; }
.eg-chip {
    background: #0c1929; border: 1px solid #1e3a5f;
    border-radius: 7px; padding: 6px 13px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem; color: #60a5fa;
}

/* Input */
.input-wrap {
    position: sticky; bottom: 0;
    background: var(--bg); padding: 12px 0 0;
    border-top: 1px solid var(--border); margin-top: 18px;
}
[data-testid="stTextArea"] textarea {
    background: var(--card) !important;
    border: 1px solid var(--border2) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.88rem !important; resize: none !important;
}
[data-testid="stTextArea"] textarea:focus {
    border-color: var(--cyan) !important;
    box-shadow: 0 0 0 2px #22d3ee18 !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, var(--cyan), #6366f1) !important;
    color: #000 !important; font-weight: 700 !important;
    border: none !important; border-radius: 8px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    transition: all .2s !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 18px #22d3ee30 !important;
}
.clr > button {
    background: var(--card) !important; color: var(--muted) !important;
    border: 1px solid var(--border2) !important;
}
.clr > button:hover {
    border-color: var(--red) !important; color: var(--red) !important;
    box-shadow: none !important; transform: none !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: var(--card) !important;
    border: 1.5px dashed var(--border2) !important;
    border-radius: 10px !important;
}

/* Sidebar labels */
.slabel {
    font-family: 'JetBrains Mono', monospace; font-size: 0.6rem;
    color: var(--dim); letter-spacing: 2px; text-transform: uppercase;
    margin: 1rem 0 .4rem;
}
.status {
    display: inline-flex; align-items: center; gap: 5px;
    font-family: 'JetBrains Mono', monospace; font-size: 0.62rem;
    padding: 3px 10px; border-radius: 20px;
}
.status.on  { background:#052e16; border:1px solid #166534; color:var(--green); }
.status.off { background:#1c0a0a; border:1px solid #7f1d1d; color:var(--red); }

/* Thinking */
.thinking { display:flex; gap:5px; align-items:center; padding:6px 0; }
.dot {
    width:6px; height:6px; border-radius:50%;
    background: var(--cyan); animation: blink 1.1s ease-in-out infinite;
}
.dot:nth-child(2){animation-delay:.18s; background:var(--violet);}
.dot:nth-child(3){animation-delay:.36s; background:#6366f1;}
@keyframes blink {
    0%,80%,100%{transform:scale(.55);opacity:.3;}
    40%{transform:scale(1);opacity:1;}
}

::-webkit-scrollbar{width:4px;height:4px;}
::-webkit-scrollbar-thumb{background:var(--border2);border-radius:2px;}
</style>
""", unsafe_allow_html=True)

# ── Imports ───────────────────────────────────────────────────────────────────
try:
    from src.pipeline import build_index, get_answer_stream
    READY = True
except Exception as e:
    READY = False
    LOAD_ERR = str(e)

# ── Session state ─────────────────────────────────────────────────────────────
for k, v in {
    "messages": [],
    "retriever": None,
    "indexed": False,
    "n_chunks": 0,
    "model_name": "—",
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown('<p class="slabel">📂 Document</p>', unsafe_allow_html=True)
    uploaded = st.file_uploader("Upload PDF or TXT", type=["pdf", "txt", "md"])

    st.markdown('<p class="slabel">🔑 API Key</p>', unsafe_allow_html=True)
    groq_key = st.text_input("Groq API Key", type="password", placeholder="gsk_...")
    st.caption("Get free key → [console.groq.com](https://console.groq.com)")

    st.markdown('<p class="slabel">⚙️ Settings</p>', unsafe_allow_html=True)
    llm_model = st.selectbox(
        "Groq Model",
        ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "gemma2-9b-it", "mixtral-8x7b-32768"],
        index=0,
    )
    embed_model = st.selectbox(
        "Embedding Model",
        ["all-MiniLM-L6-v2", "bge-small-en-v1.5"],
        index=0,
    )
    chunk_size    = st.slider("Chunk Size (chars)", 300, 1500, 800, 100)
    chunk_overlap = st.slider("Chunk Overlap (chars)", 0, 300, 100, 50)
    top_k         = st.slider("Top-K Chunks Retrieved", 1, 8, 3)

    st.markdown('<p class="slabel">🚀 Actions</p>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        build_btn = st.button("🔨 Build Index", use_container_width=True)
    with c2:
        st.markdown('<div class="clr">', unsafe_allow_html=True)
        clear_btn = st.button("🗑 Clear", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<p class="slabel">📊 Status</p>', unsafe_allow_html=True)
    if st.session_state.indexed:
        st.markdown('<span class="status on">● READY</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="status off">● NOT INDEXED</span>', unsafe_allow_html=True)

    st.markdown(f"""
    <div style="font-family:'JetBrains Mono',monospace;font-size:.65rem;
                color:var(--muted);line-height:2.2;margin-top:8px;">
        Model &nbsp;&nbsp;: <span style="color:#a5b4fc">{st.session_state.model_name}</span><br>
        Chunks &nbsp;: <span style="color:var(--cyan)">{st.session_state.n_chunks}</span><br>
        Embed &nbsp;&nbsp;: <span style="color:var(--green)">{embed_model}</span><br>
        VectorDB : <span style="color:var(--amber)">FAISS</span><br>
        Top-K &nbsp;&nbsp;: <span style="color:var(--cyan)">{top_k}</span>
    </div>
    """, unsafe_allow_html=True)

# ── Actions ───────────────────────────────────────────────────────────────────
if clear_btn:
    st.session_state.messages = []
    st.rerun()

if build_btn:
    if not uploaded:
        st.sidebar.error("Pehle document upload karo!")
    elif not groq_key:
        st.sidebar.error("Groq API key daalo!")
    elif not READY:
        st.sidebar.error(f"Import error: {LOAD_ERR}")
    else:
        with st.sidebar:
            with st.spinner("Indexing… please wait ⚙️"):
                try:
                    data_dir = Path("data"); data_dir.mkdir(exist_ok=True)
                    fp = data_dir / uploaded.name
                    fp.write_bytes(uploaded.getvalue())

                    retriever, n_chunks = build_index(
                        file_path=str(fp),
                        embed_model=embed_model,
                        chunk_size=chunk_size,
                        chunk_overlap=chunk_overlap,
                    )
                    st.session_state.retriever  = retriever
                    st.session_state.indexed    = True
                    st.session_state.n_chunks   = n_chunks
                    st.session_state.model_name = llm_model
                    st.success(f"✅ {n_chunks} chunks indexed!")
                except Exception as e:
                    st.error(f"Error: {e}")

# ══════════════════════════════════════════════════════════════════════════════
# MAIN AREA
# ══════════════════════════════════════════════════════════════════════════════

# Header
st.markdown(f"""
<div class="top-bar">
  <div class="brand">
    <div class="brand-icon">🧠</div>
    <div>
      <p class="brand-name">DocMind AI</p>
      <p class="brand-tag">RAG · LangChain · Groq · FAISS</p>
    </div>
  </div>
  <div class="pills">
    <div class="pill">⚡ Groq <span class="v">Streaming</span></div>
    <div class="pill">🗃 FAISS <span class="v">Vector DB</span></div>
    <div class="pill">📦 Chunks <span class="v">{st.session_state.n_chunks}</span></div>
  </div>
</div>
""", unsafe_allow_html=True)

# Welcome screen
if not st.session_state.messages:
    st.markdown("""
    <div class="welcome">
        <div style="font-size:2.4rem">📄</div>
        <h3>Upload a document to get started</h3>
        <p>DocMind reads your document, breaks it into semantic chunks,<br>
        indexes them in FAISS, and answers your questions using Groq LLM.</p>
        <div class="eg-chips">
            <div class="eg-chip">What are the key clauses?</div>
            <div class="eg-chip">Summarise the privacy policy</div>
            <div class="eg-chip">What data is collected?</div>
            <div class="eg-chip">What are user obligations?</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Render chat history
for msg in st.session_state.messages:
    role    = msg["role"]
    content = msg["content"]
    sources = msg.get("sources", [])

    if role == "user":
        st.markdown(f"""
        <div class="msg user">
            <div class="avatar user">👤</div>
            <div class="bubble">{content}</div>
        </div>""", unsafe_allow_html=True)
    else:
        src_html = ""
        if sources:
            chips = "".join(f'<span class="src-chip">Chunk #{s["id"]}</span>' for s in sources)
            boxes = "".join(
                f'<div class="src-box"><b style="color:#a5b4fc">Chunk #{s["id"]}</b> '
                f'(score: {s.get("score","—")})<br>{s["text"][:280]}…</div>'
                for s in sources
            )
            src_html = f"""
            <details class="src-wrap">
                <summary class="src-label">▸ {len(sources)} source chunk(s) used</summary>
                <div style="margin-top:6px">{chips}</div>{boxes}
            </details>"""

        st.markdown(f"""
        <div class="msg ai">
            <div class="avatar ai">🧠</div>
            <div class="bubble">{content}{src_html}</div>
        </div>""", unsafe_allow_html=True)

# ── Input ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="input-wrap">', unsafe_allow_html=True)
col1, col2 = st.columns([9, 1])
with col1:
    query = st.text_area(
        "Ask a question", placeholder="Ask anything about your document…",
        height=70, key="qinput", label_visibility="collapsed"
    )
with col2:
    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
    send = st.button("➤", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── Handle query ──────────────────────────────────────────────────────────────
if send and query.strip():
    q = query.strip()
    st.session_state.messages.append({"role": "user", "content": q})

    if not st.session_state.indexed:
        ans = "⚠️ Please upload a document and click **Build Index** first!"
        sources = []
    elif not groq_key:
        ans = "⚠️ Please enter your Groq API key in the sidebar."
        sources = []
    else:
        # Show thinking animation
        think_ph = st.empty()
        think_ph.markdown("""
        <div class="msg ai">
          <div class="avatar ai">🧠</div>
          <div class="bubble">
            <div class="thinking">
              <div class="dot"></div><div class="dot"></div><div class="dot"></div>
              <span style="font-family:'JetBrains Mono',monospace;font-size:.65rem;
                    color:var(--muted);margin-left:6px;">Retrieving & generating…</span>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

        stream_ph = st.empty()
        full_ans  = ""
        sources   = []

        try:
            for token, src in get_answer_stream(
                query=q,
                retriever=st.session_state.retriever,
                groq_api_key=groq_key,
                model_name=st.session_state.model_name,
                top_k=top_k,
            ):
                full_ans += token
                if src and not sources:
                    sources = src
                stream_ph.markdown(f"""
                <div class="msg ai">
                  <div class="avatar ai">🧠</div>
                  <div class="bubble">{full_ans}<span style="color:var(--cyan);
                    animation:blink 1s infinite;">▋</span></div>
                </div>""", unsafe_allow_html=True)
            ans = full_ans
        except Exception as e:
            ans = f"❌ Generation error: {e}"

        think_ph.empty()
        stream_ph.empty()

    st.session_state.messages.append({
        "role": "assistant", "content": ans, "sources": sources
    })
    st.rerun()
