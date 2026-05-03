import streamlit as st
import datetime
from graph.builder import blog_graph

st.set_page_config(
    page_title="AI Blog Generator",
    page_icon="✍️",
    layout="wide"
)

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True
if "blog_history" not in st.session_state:
    st.session_state.blog_history = []
if "current_blog" not in st.session_state:
    st.session_state.current_blog = None

if st.session_state.dark_mode:
    bg = "#0a0a0f"
    sidebar_bg = "#13131f"
    input_bg = "#1e1e35"
    text = "#ffffff"
    subtext = "#666666"
    border = "#2a2a3e"
    accent = "#cc44ff"
    neon = "text-shadow: 0 0 8px #ff00ff, 0 0 16px #7700ff;"
    title_color = "#cc44ff"
else:
    bg = "#f5f5f5"
    sidebar_bg = "#ffffff"
    input_bg = "#ffffff"
    text = "#1a1a1a"
    subtext = "#666666"
    border = "#e0e0e0"
    accent = "#f63366"
    neon = ""
    title_color = "#f63366"

st.markdown(f"""
<style>
    #MainMenu {{ visibility: hidden !important; }}
    footer {{ visibility: hidden !important; }}
    .stDeployButton {{ display: none !important; }}
    div[data-testid="stDecoration"] {{ display: none !important; }}
    div[data-testid="stToolbar"] {{ display: none !important; }}
    [data-testid="stStatusWidget"] {{ display: none !important; }}
    header[data-testid="stHeader"] {{ background-color: {bg} !important; height: 0px !important; }}
    .stApp {{ background-color: {bg}; }}
    .main .block-container {{ padding-top: 0 !important; padding-bottom: 0 !important; max-width: 100% !important; }}
    section[data-testid="stSidebar"] {{ background-color: {sidebar_bg} !important; border-right: 1px solid {border} !important; }}
    section[data-testid="stSidebar"] > div {{ padding-top: 1rem !important; }}
    p, label, div {{ color: {text}; }}
    h1, h2, h3 {{ color: {text} !important; }}
    .stTextInput input {{
        background-color: {input_bg} !important;
        color: {text} !important;
        border: 1px solid {border} !important;
        border-radius: 8px !important;
    }}
    .stTextInput input:focus {{ border-color: {accent} !important; }}
    .stButton>button {{
        background-color: {input_bg} !important;
        color: {text} !important;
        border: 1px solid {border} !important;
        border-radius: 8px !important;
        transition: all 0.2s !important;
    }}
    .stButton>button:hover {{ border-color: {accent} !important; color: {accent} !important; }}
    .stDownloadButton>button {{
        background-color: {input_bg} !important;
        color: {text} !important;
        border: 1px solid {border} !important;
        border-radius: 8px !important;
    }}
    .stRadio label {{ color: {text} !important; }}
    .stSelectbox > div > div {{
        background-color: {input_bg} !important;
        color: {text} !important;
        border: 1px solid {border} !important;
        border-radius: 8px !important;
    }}
    .generate-btn > div > button {{
        background: linear-gradient(135deg, #cc44ff, #7700ff) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        box-shadow: 0 0 15px #cc44ff66 !important;
        transition: all 0.3s !important;
    }}
    .generate-btn > div > button:hover {{
        box-shadow: 0 0 25px #cc44ffcc !important;
        transform: translateY(-1px) !important;
    }}
    .blog-card {{
        background: {input_bg};
        border: 1px solid {border};
        border-left: 4px solid {accent};
        border-radius: 12px;
        padding: 1.5rem;
        line-height: 1.8;
        color: {text};
    }}
    .stats-bar {{ color: {subtext}; font-size: 0.82rem; margin: 0.3rem 0 1rem 0; }}
    [data-testid="stExpander"] {{
        border: 1px solid {border} !important;
        border-radius: 8px !important;
        background: {input_bg} !important;
        margin-bottom: 4px !important;
    }}
    .top-header {{
        background: {bg};
        border-bottom: 1px solid {border};
        padding: 10px 24px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }}
    .blog-title {{
        {neon}
        color: {title_color};
        font-size: 1.6rem;
        font-weight: 900;
        margin: 0;
    }}
    .subtitle-pill {{
        background: {accent}22;
        color: {subtext};
        font-size: 0.78rem;
        border-radius: 20px;
        padding: 2px 12px;
        display: inline-block;
        margin-top: 2px;
    }}
</style>
""", unsafe_allow_html=True)

# ── Full width header ─────────────────────────
st.markdown(f"""
<div class="top-header">
    <div style="width:60px"></div>
    <div style="text-align:center;">
        <div class="blog-title">✍️ AI Blog Generator</div>
        <div class="subtitle-pill">Generate professional blogs instantly</div>
    </div>
    <div style="width:60px"></div>
</div>
""", unsafe_allow_html=True)

# Theme toggle — float top right using columns trick
col_space, col_toggle = st.columns([11, 1])
with col_toggle:
    if st.button("🌙" if not st.session_state.dark_mode else "☀️"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

# ── Sidebar ───────────────────────────────────
with st.sidebar:
    st.markdown(f'<div style="font-size:10px;color:{subtext};letter-spacing:1px;margin-bottom:6px;">📝 TOPIC</div>', unsafe_allow_html=True)
    topic = st.text_input("", placeholder="eg. Will AI eat jobs?", label_visibility="collapsed")

    st.markdown(f'<div style="font-size:10px;color:{subtext};letter-spacing:1px;margin:12px 0 6px;">⚙️ PARAMETERS</div>', unsafe_allow_html=True)

    blog_length = st.radio(
        "Length",
        ["short", "long"],
        horizontal=True,
        format_func=lambda x: "⚡ Short" if x == "short" else "📖 Long",
        label_visibility="collapsed"
    )

    tone = st.selectbox(
        "Tone",
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
    st.markdown('<div class="generate-btn">', unsafe_allow_html=True)
    generate = st.button("🚀 Generate Blog", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    col_s, col_c = st.columns([1, 1])
    with col_s:
        if st.button("🔗 Share", use_container_width=True):
            st.code("https://blog-agent-wq4kzbsmq5azaq4gf2axsv.streamlit.app")
    with col_c:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.current_blog = None
            st.rerun()

    st.markdown("---")
    st.markdown(f'<div style="font-size:10px;color:{subtext};letter-spacing:1px;margin-bottom:8px;">📚 HISTORY</div>', unsafe_allow_html=True)

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
            with st.expander(f"📄 {item['topic'][:25]}"):
                st.caption(f"{item['length'].capitalize()} · {item.get('tone','formal').capitalize()}")
                if st.button("Load", key=f"load_{i}", use_container_width=True):
                    st.session_state.current_blog = item
                    st.rerun()
    else:
        st.caption("No blogs yet!")

# ── Main area ──────────────────────────────────
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
    st.download_button(
        "📥 Download Blog",
        data=blog_text,
        file_name=f"{blog['topic'][:30]}.txt",
        mime="text/plain",
        use_container_width=True
    )
else:
    st.markdown(f"""
    <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:65vh;text-align:center;">
        <div style="font-size:56px;margin-bottom:16px;">✍️</div>
        <div style="font-size:1.1rem;color:{subtext};">Enter a topic and click Generate Blog</div>
        <div style="font-size:0.85rem;color:{subtext};margin-top:6px;opacity:0.6;">Your blog will appear here</div>
    </div>
    """, unsafe_allow_html=True)