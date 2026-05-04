import streamlit as st
import datetime
from graph.builder import blog_graph

st.set_page_config(
    page_title="AI Blog Generator",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True
if "blog_history" not in st.session_state:
    st.session_state.blog_history = []
if "current_blog" not in st.session_state:
    st.session_state.current_blog = None

st.markdown("""
<style>
    #MainMenu { visibility: hidden !important; }
    footer { visibility: hidden !important; }
    .stDeployButton { display: none !important; }
    div[data-testid="stDecoration"] { display: none !important; }
    div[data-testid="stToolbar"] { display: none !important; }
    [data-testid="stStatusWidget"] { display: none !important; }
    header[data-testid="stHeader"] { display: none !important; }

    .stApp { background-color: #0a0a0f !important; }
    .main .block-container {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        max-width: 100% !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #13131f !important;
        border-right: 1px solid #2a2a3e !important;
    }
    section[data-testid="stSidebar"] > div {
        padding-top: 1rem !important;
    }

    /* Section headings */
    .section-label {
        font-size: 11px;
        font-weight: 700;
        color: #cc44ff !important;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin: 14px 0 6px 0;
        display: block;
    }

    /* Inputs */
    .stTextInput input {
        background-color: #1e1e35 !important;
        color: #ffffff !important;
        border: 1px solid #2a2a3e !important;
        border-radius: 8px !important;
    }
    .stTextInput input::placeholder { color: #555 !important; }
    .stTextInput input:focus { border-color: #cc44ff !important; }

    /* Default buttons */
    .stButton>button {
        background-color: #1e1e35 !important;
        color: #ffffff !important;
        border: 1px solid #2a2a3e !important;
        border-radius: 8px !important;
        transition: all 0.2s !important;
    }
    .stButton>button:hover {
        border-color: #cc44ff !important;
        color: #cc44ff !important;
    }

    /* Glowing generate button */
    .gen-btn .stButton>button {
        background: linear-gradient(135deg, #cc44ff, #7700ff) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        box-shadow: 0 0 20px #cc44ff66 !important;
        transition: all 0.3s !important;
    }
    .gen-btn .stButton>button:hover {
        box-shadow: 0 0 35px #cc44ffaa !important;
        transform: translateY(-2px) !important;
        color: white !important;
    }

    /* Download button */
    .stDownloadButton>button {
        background-color: #1e1e35 !important;
        color: #ffffff !important;
        border: 1px solid #2a2a3e !important;
        border-radius: 8px !important;
    }

    /* Radio */
    .stRadio label { color: #ffffff !important; }

    /* Selectbox */
    .stSelectbox > div > div {
        background-color: #1e1e35 !important;
        color: #ffffff !important;
        border: 1px solid #2a2a3e !important;
        border-radius: 8px !important;
    }
    .stSelectbox svg { fill: #ffffff !important; }
    [data-baseweb="select"] * { color: #ffffff !important; background-color: #1e1e35 !important; }
    [data-baseweb="popover"] * { color: #ffffff !important; background-color: #1e1e35 !important; }
    [role="option"]:hover { background-color: #2a2a3e !important; }

    /* Blog card */
    .blog-card {
        background: #1e1e35;
        border: 1px solid #2a2a3e;
        border-left: 4px solid #cc44ff;
        border-radius: 12px;
        padding: 1.5rem;
        line-height: 1.9;
        color: #ffffff;
        font-size: 15px;
    }
    .stats-bar { color: #888; font-size: 13px; margin: 6px 0 16px 0; }

    /* Expander */
    [data-testid="stExpander"] {
        border: 1px solid #2a2a3e !important;
        border-radius: 8px !important;
        background: #1e1e35 !important;
        margin-bottom: 6px !important;
    }
    .streamlit-expanderHeader p { color: #ffffff !important; font-size: 13px !important; }
</style>
""", unsafe_allow_html=True)

# ── TITLE ─────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:20px 0 10px 0;border-bottom:1px solid #2a2a3e;margin-bottom:8px;">
    <div style="font-size:2.8rem;font-weight:900;color:#cc44ff;
        text-shadow:0 0 10px #ff00ff,0 0 25px #7700ff;
        letter-spacing:-1px;">✍️ AI Blog Generator</div>
    <div style="margin-top:8px;">
        <span style="background:#cc44ff18;border:1px solid #cc44ff33;
            border-radius:20px;padding:3px 16px;font-size:12px;color:#aaa;">
            Generate professional blogs instantly
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── SIDEBAR ───────────────────────────────────────────────
with st.sidebar:
    st.markdown('<span class="section-label">📝 Topic</span>', unsafe_allow_html=True)
    topic = st.text_input("topic", placeholder="eg. Will AI eat jobs?", label_visibility="collapsed")

    st.markdown('<span class="section-label">⚙️ Parameters</span>', unsafe_allow_html=True)
    blog_length = st.radio(
        "length", ["short", "long"], horizontal=True,
        format_func=lambda x: "⚡ Short" if x == "short" else "📖 Long",
        label_visibility="collapsed"
    )
    tone = st.selectbox(
        "tone",
        ["formal", "casual", "sarcastic", "inspirational"],
        format_func=lambda x: {
            "formal": "🎩 Formal",
            "casual": "😊 Casual",
            "sarcastic": "😏 Sarcastic",
            "inspirational": "💪 Inspiring"
        }[x],
        label_visibility="collapsed"
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="gen-btn">', unsafe_allow_html=True)
    generate = st.button("🚀 Generate Blog", use_container_width=True, key="gen_btn")
    st.markdown('</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        share = st.button("🔗 Share", use_container_width=True)
    with c2:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.current_blog = None
            st.rerun()

    if share:
        st.success("✅ Copy:")
        st.code("https://blog-agent-wq4kzbsmq5azaq4gf2axsv.streamlit.app", language=None)

    st.markdown('<span class="section-label">📚 History</span>', unsafe_allow_html=True)

    seen = set()
    unique_history = []
    for item in reversed(st.session_state.blog_history):
        key = item["topic"].lower().strip()
        if key not in seen:
            seen.add(key)
            unique_history.append(item)

    if unique_history:
        if st.button("🗑️ Clear All", use_container_width=True):
            st.session_state.blog_history = []
            st.session_state.current_blog = None
            st.rerun()
        for i, item in enumerate(unique_history):
            with st.expander(f"📄 {item['topic'][:22]}"):
                st.caption(f"{item['length'].capitalize()} · {item.get('tone','formal').capitalize()}")
                if st.button("Load", key=f"load_{i}", use_container_width=True):
                    st.session_state.current_blog = item
                    st.rerun()
    else:
        st.caption("No blogs yet!")

# ── MAIN AREA ─────────────────────────────────────────────
if generate:
    if topic:
        with st.spinner("✍️ Writing your blog..."):
            try:
                result = blog_graph.invoke({
                    "topic": topic,
                    "context": "",
                    "title_candidates": [],
                    "chosen_title": "",
                    "blog_length": blog_length,
                    "tone": tone,
                    "blog_content": "",
                    "final_output": ""
                })
                blog_data = {
                    "title": result["chosen_title"],
                    "blog": result["final_output"],
                    "topic": topic,
                    "length": blog_length,
                    "tone": tone,
                    "time": datetime.datetime.now().strftime("%H:%M %d/%m/%Y")
                }
                st.session_state.current_blog = blog_data
                st.session_state.blog_history.append(blog_data)
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    else:
        st.warning("⚠️ Please enter a topic first!")

if st.session_state.current_blog:
    blog = st.session_state.current_blog
    word_count = len(blog["blog"].split())
    read_time = max(1, word_count // 200)
    st.markdown(f"## {blog['title']}")
    st.markdown(f'<div class="stats-bar">📏 {blog["length"].capitalize()} &nbsp;|&nbsp; 🎭 {blog["tone"].capitalize()} &nbsp;|&nbsp; 📊 {word_count} words &nbsp;|&nbsp; ⏱️ {read_time} min read &nbsp;|&nbsp; 🕐 {blog["time"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="blog-card">{blog["blog"]}</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    blog_text = f"{blog['title']}\n\n{blog['blog']}"
    st.download_button("📥 Download Blog", data=blog_text,
        file_name=f"{blog['topic'][:30]}.txt", mime="text/plain",
        use_container_width=True)
else:
    st.markdown("""
    <div style="display:flex;flex-direction:column;align-items:center;
        justify-content:center;height:65vh;text-align:center;">
        <div style="font-size:60px;margin-bottom:20px;">✍️</div>
        <div style="font-size:1.1rem;font-weight:600;color:#888;">
            Enter a topic and click Generate Blog</div>
        <div style="font-size:0.85rem;margin-top:8px;color:#555;">
            Your blog will appear here</div>
    </div>
    """, unsafe_allow_html=True)