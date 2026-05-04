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

# Theme colors
if st.session_state.dark_mode:
    bg = "#0a0a0f"
    sidebar_bg = "#13131f"
    input_bg = "#1e1e35"
    text = "#ffffff"
    subtext = "#aaaaaa"
    border = "#2a2a3e"
    accent = "#cc44ff"
    neon = "text-shadow: 0 0 10px #ff00ff, 0 0 25px #7700ff, 0 0 50px #ff00ff;"
    title_color = "#cc44ff"
    heading_color = "#cc44ff"
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
    heading_color = "#f63366"

st.markdown(f"""
<style>
    /* Hide Streamlit chrome */
    #MainMenu {{ visibility: hidden !important; }}
    footer {{ visibility: hidden !important; }}
    .stDeployButton {{ display: none !important; }}
    div[data-testid="stDecoration"] {{ display: none !important; }}
    div[data-testid="stToolbar"] {{ display: none !important; }}
    [data-testid="stStatusWidget"] {{ display: none !important; }}
    header[data-testid="stHeader"] {{ background-color: {bg} !important; height: 0px !important; }}

    /* Base */
    .stApp {{ background-color: {bg}; }}
    .main .block-container {{
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        max-width: 100% !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }}

    /* Sidebar */
    section[data-testid="stSidebar"] {{
        background-color: {sidebar_bg} !important;
        border-right: 1px solid {border} !important;
    }}
    section[data-testid="stSidebar"] > div {{
        padding-top: 0.5rem !important;
    }}

    /* Text */
    p, span, div {{ color: {text}; }}
    h1, h2, h3, h4 {{ color: {text} !important; }}
    label {{ color: {text} !important; }}

    /* Section headings in sidebar */
    .section-heading {{
        font-size: 13px;
        font-weight: 700;
        color: {heading_color} !important;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin: 16px 0 8px 0;
        display: block;
    }}

    /* Input */
    .stTextInput input {{
        background-color: {input_bg} !important;
        color: {text} !important;
        border: 1px solid {border} !important;
        border-radius: 8px !important;
        font-size: 14px !important;
    }}
    .stTextInput input:focus {{
        border-color: {accent} !important;
        box-shadow: 0 0 0 2px {accent}33 !important;
    }}
    .stTextInput input::placeholder {{ color: {subtext} !important; }}

    /* Default buttons */
    .stButton>button {{
        background-color: {input_bg} !important;
        color: {text} !important;
        border: 1px solid {border} !important;
        border-radius: 8px !important;
        font-size: 14px !important;
        transition: all 0.2s !important;
    }}
    .stButton>button:hover {{
        border-color: {accent} !important;
        color: {accent} !important;
    }}

    /* Download button */
    .stDownloadButton>button {{
        background-color: {input_bg} !important;
        color: {text} !important;
        border: 1px solid {border} !important;
        border-radius: 8px !important;
    }}

    /* Radio */
    .stRadio label {{ color: {text} !important; font-size: 14px !important; }}
    .stRadio > div {{ gap: 8px !important; }}

    /* Selectbox */
    .stSelectbox > div > div {{
        background-color: {input_bg} !important;
        color: {text} !important;
        border: 1px solid {border} !important;
        border-radius: 8px !important;
    }}
    .stSelectbox svg {{ fill: {text} !important; }}
    [data-baseweb="select"] * {{
        color: {text} !important;
        background-color: {input_bg} !important;
    }}
    [data-baseweb="popover"] * {{
        color: {text} !important;
        background-color: {input_bg} !important;
    }}
    [role="option"]:hover {{
        background-color: {border} !important;
    }}

    /* Blog card */
    .blog-card {{
        background: {input_bg};
        border: 1px solid {border};
        border-left: 4px solid {accent};
        border-radius: 12px;
        padding: 1.5rem;
        line-height: 1.9;
        color: {text};
        font-size: 15px;
    }}
    .stats-bar {{
        color: {subtext};
        font-size: 13px;
        margin: 6px 0 16px 0;
    }}

    /* History expander */
    [data-testid="stExpander"] {{
        border: 1px solid {border} !important;
        border-radius: 8px !important;
        background: {input_bg} !important;
        margin-bottom: 6px !important;
    }}
    .streamlit-expanderHeader p {{
        color: {text} !important;
        font-size: 13px !important;
    }}

    /* Fixed title bar */
    .title-bar {{
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        z-index: 998 !important;
        background: {bg} !important;
        border-bottom: 1px solid {border} !important;
        padding: 14px 32px !important;
        text-align: center !important;
    }}
    
    /* Push content down so it doesn't hide under fixed bar */
    .main .block-container {{
        padding-top: 100px !important;
    }}
    
    /* Theme toggle fixed top right */
    .theme-toggle-wrapper .stButton>button {{
        position: fixed !important;
        top: 14px !important;
        right: 16px !important;
        z-index: 999 !important;
        border-radius: 20px !important;
        padding: 4px 12px !important;
        width: auto !important;
        background: {input_bg} !important;
        color: {text} !important;
        border: 1px solid {border} !important;
    }}
    .main-title {{
        {neon}
        color: {title_color};
        font-size: 2.6rem;
        font-weight: 900;
        margin: 0;
        letter-spacing: -1px;
        display: block;
    }}
    .main-subtitle {{
        color: {subtext};
        font-size: 13px;
        margin-top: 6px;
        background: {accent}18;
        border: 1px solid {accent}33;
        border-radius: 20px;
        padding: 3px 14px;
        display: inline-block;
    }}

    /* Glowing generate button */
    .gen-btn .stButton>button {{
        background: linear-gradient(135deg, #cc44ff 0%, #7700ff 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        padding: 0.6rem !important;
        box-shadow: 0 0 20px #cc44ff66, 0 0 40px #cc44ff33 !important;
        transition: all 0.3s !important;
    }}
    .gen-btn .stButton>button:hover {{
        box-shadow: 0 0 30px #cc44ffaa, 0 0 60px #cc44ff55 !important;
        transform: translateY(-2px) !important;
        color: white !important;
    }}

    /* Empty state */
    .empty-state {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 65vh;
        text-align: center;
        color: {subtext};
    }}
    /* Theme toggle fixed top right */
    .theme-toggle-wrapper .stButton>button {{
        background: {input_bg} !important;
        color: {text} !important;
        border: 1px solid {border} !important;
        border-radius: 20px !important;
        padding: 4px 12px !important;
        font-size: 16px !important;
        position: fixed !important;
        top: 12px !important;
        right: 16px !important;
        z-index: 999 !important;
        width: auto !important;
    }}
    /* Always show sidebar toggle */
    button[data-testid="collapsedControl"] {{
        display: flex !important;
        background: {input_bg} !important;
        color: {text} !important;
        border: 1px solid {border} !important;
        border-radius: 8px !important;
    }}
</style>
""", unsafe_allow_html=True)

# ── TITLE BAR ─────────────────────────────────────────────
st.markdown(f"""
<div class="title-bar">
    <span class="main-title">✍️ AI Blog Generator</span>
    <div><span class="main-subtitle">Generate professional blogs instantly</span></div>
</div>
""", unsafe_allow_html=True)

# Fixed theme toggle top right
st.markdown('<div class="theme-toggle-wrapper">', unsafe_allow_html=True)
if st.button("🌙" if not st.session_state.dark_mode else "☀️", key="theme_btn"):
    st.session_state.dark_mode = not st.session_state.dark_mode
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# ── SIDEBAR ───────────────────────────────────────────────
with st.sidebar:
    # Topic
    st.markdown(f'<span class="section-heading">📝 Topic</span>', unsafe_allow_html=True)
    topic = st.text_input("topic", placeholder="eg. Will AI eat jobs?", label_visibility="collapsed")

    # Parameters
    st.markdown(f'<span class="section-heading">⚙️ Parameters</span>', unsafe_allow_html=True)
    blog_length = st.radio(
        "length",
        ["short", "long"],
        horizontal=True,
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

    # Glowing Generate button
    st.markdown('<div class="gen-btn">', unsafe_allow_html=True)
    generate = st.button("🚀 Generate Blog", use_container_width=True, key="gen_btn")
    st.markdown('</div>', unsafe_allow_html=True)

    # Share + Clear
    col_s, col_c = st.columns([1, 1])
    with col_s:
        share = st.button("🔗 Share", use_container_width=True)
    with col_c:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.current_blog = None
            st.rerun()

    if share:
        st.success("✅ Copy this link:")
        st.code("https://blog-agent-wq4kzbsmq5azaq4gf2axsv.streamlit.app", language=None)

    # History
    st.markdown(f'<span class="section-heading">📚 History</span>', unsafe_allow_html=True)

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
                st.caption(f"{item['length'].capitalize()} · {item.get('tone','formal').capitalize()} · {item['time']}")
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
    st.download_button(
        "📥 Download Blog",
        data=blog_text,
        file_name=f"{blog['topic'][:30]}.txt",
        mime="text/plain",
        use_container_width=True
    )
else:
    st.markdown(f"""
    <div class="empty-state">
        <div style="font-size:60px;margin-bottom:20px;">✍️</div>
        <div style="font-size:1.1rem;font-weight:600;">Enter a topic and click Generate Blog</div>
        <div style="font-size:0.85rem;margin-top:8px;opacity:0.6;">Your blog will appear here</div>
    </div>
    """, unsafe_allow_html=True)