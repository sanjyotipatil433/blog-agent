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
if "copied" not in st.session_state:
    st.session_state.copied = False

if st.session_state.dark_mode:
    bg = "#0a0a0f"
    sidebar_bg = "#13131f"
    input_bg = "#1e1e35"
    text = "#ffffff"
    subtext = "#888888"
    border = "#2a2a3e"
    accent = "#cc44ff"
    neon = "text-shadow: 0 0 10px #ff00ff, 0 0 20px #7700ff;"
    title_color = "#cc44ff"
    dropdown_bg = "#1e1e35"
    dropdown_text = "#ffffff"
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
    dropdown_bg = "#ffffff"
    dropdown_text = "#1a1a1a"

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
    .main .block-container {{
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        max-width: 100% !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
    }}
    section[data-testid="stSidebar"] {{
        background-color: {sidebar_bg} !important;
        border-right: 1px solid {border} !important;
    }}
    section[data-testid="stSidebar"] > div {{ padding-top: 1rem !important; }}
    p, label {{ color: {text} !important; }}
    h1, h2, h3 {{ color: {text} !important; }}

    /* Input */
    .stTextInput input {{
        background-color: {input_bg} !important;
        color: {text} !important;
        border: 1px solid {border} !important;
        border-radius: 8px !important;
    }}
    .stTextInput input:focus {{ border-color: {accent} !important; }}

    /* All buttons default */
    .stButton>button {{
        background-color: {input_bg} !important;
        color: {text} !important;
        border: 1px solid {border} !important;
        border-radius: 8px !important;
        transition: all 0.2s !important;
    }}
    .stButton>button:hover {{
        border-color: {accent} !important;
        color: {accent} !important;
    }}

    /* Generate button */
    div[data-testid="stButton"].generate-btn > button,
    .generate-btn .stButton>button {{
        background: linear-gradient(135deg, #cc44ff, #7700ff) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        box-shadow: 0 0 20px #cc44ff77 !important;
    }}

    /* Download */
    .stDownloadButton>button {{
        background-color: {input_bg} !important;
        color: {text} !important;
        border: 1px solid {border} !important;
        border-radius: 8px !important;
    }}

    /* Radio */
    .stRadio label {{ color: {text} !important; }}
    .stRadio div {{ color: {text} !important; }}

    /* Selectbox — fix dark mode */
    .stSelectbox > div > div {{
        background-color: {input_bg} !important;
        color: {text} !important;
        border: 1px solid {border} !important;
        border-radius: 8px !important;
    }}
    .stSelectbox svg {{ fill: {text} !important; }}
    [data-baseweb="select"] * {{ color: {text} !important; background-color: {input_bg} !important; }}
    [data-baseweb="popover"] * {{ color: {text} !important; background-color: {input_bg} !important; }}
    [role="option"] {{ color: {text} !important; background-color: {input_bg} !important; }}
    [role="option"]:hover {{ background-color: {border} !important; }}

    /* Blog card */
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

    /* Expander */
    [data-testid="stExpander"] {{
        border: 1px solid {border} !important;
        border-radius: 8px !important;
        background: {input_bg} !important;
        margin-bottom: 4px !important;
    }}
    .streamlit-expanderHeader {{ color: {text} !important; }}
    .streamlit-expanderHeader p {{ color: {text} !important; }}

    /* Full width header */
    .top-bar {{
        width: 100%;
        background: {bg};
        border-bottom: 1px solid {border};
        padding: 16px 32px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-sizing: border-box;
    }}
    .blog-title {{
        {neon}
        color: {title_color};
        font-size: 2rem;
        font-weight: 900;
        margin: 0;
        letter-spacing: -0.5px;
    }}
    .subtitle-pill {{
        background: {accent}22;
        color: {accent};
        font-size: 0.78rem;
        border-radius: 20px;
        padding: 2px 12px;
        display: inline-block;
        margin-top: 4px;
        border: 1px solid {accent}44;
    }}
    .theme-toggle {{
        background: {input_bg};
        border: 1px solid {border};
        border-radius: 20px;
        padding: 6px 14px;
        cursor: pointer;
        font-size: 14px;
        color: {text};
        position: absolute;
        right: 24px;
        top: 16px;
    }}
</style>
""", unsafe_allow_html=True)

# ── TOP BAR (full width) ──────────────────────────────
top_col1, top_col2, top_col3 = st.columns([1, 6, 1])
with top_col1:
    st.markdown(f'<div style="height:70px;background:{bg};border-bottom:1px solid {border};"></div>', unsafe_allow_html=True)
with top_col2:
    st.markdown(f"""
    <div style="background:{bg};border-bottom:1px solid {border};padding:12px 0;text-align:center;">
        <div class="blog-title">✍️ AI Blog Generator</div>
        <div class="subtitle-pill">Generate professional blogs instantly</div>
    </div>
    """, unsafe_allow_html=True)
with top_col3:
    st.markdown(f'<div style="height:10px;background:{bg};border-bottom:1px solid {border};"></div>', unsafe_allow_html=True)
    if st.button("🌙" if not st.session_state.dark_mode else "☀️", key="theme_btn"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

# ── SIDEBAR ───────────────────────────────────────────
with st.sidebar:
    st.markdown(f'<div style="font-size:10px;color:{subtext};letter-spacing:1px;margin-bottom:4px;">📝 TOPIC</div>', unsafe_allow_html=True)
    topic = st.text_input("topic", placeholder="eg. Will AI eat jobs?", label_visibility="collapsed")

    st.markdown(f'<div style="font-size:10px;color:{subtext};letter-spacing:1px;margin:12px 0 4px;">⚙️ PARAMETERS</div>', unsafe_allow_html=True)

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

    # Glowing generate button
    st.markdown(f"""
    <style>
    div[data-testid="stButton"]:has(button[kind="secondary"]) {{ display: none; }}
    .gen-wrap .stButton>button {{
        background: linear-gradient(135deg, #cc44ff, #7700ff) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        box-shadow: 0 0 20px #cc44ff77 !important;
        padding: 0.6rem !important;
    }}
    .gen-wrap .stButton>button:hover {{
        box-shadow: 0 0 30px #cc44ffcc !important;
        transform: translateY(-1px) !important;
    }}
    </style>
    <div class="gen-wrap">
    """, unsafe_allow_html=True)
    generate = st.button("🚀 Generate Blog", use_container_width=True, key="gen_btn")
    st.markdown('</div>', unsafe_allow_html=True)

    col_s, col_c = st.columns([1, 1])
    with col_s:
        share_clicked = st.button("🔗 Share", use_container_width=True)
    with col_c:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.current_blog = None
            st.rerun()

    if share_clicked:
        st.markdown(f"""
        <div style="background:{input_bg};border:1px solid {border};border-radius:8px;padding:8px 12px;margin-top:8px;">
            <div style="font-size:10px;color:{subtext};margin-bottom:4px;">App link:</div>
            <div style="font-size:11px;color:{accent};word-break:break-all;">https://blog-agent-wq4kzbsmq5azaq4gf2axsv.streamlit.app</div>
        </div>
        <script>
        navigator.clipboard.writeText('https://blog-agent-wq4kzbsmq5azaq4gf2axsv.streamlit.app');
        </script>
        """, unsafe_allow_html=True)
        st.success("✅ Link copied!")

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

# ── MAIN AREA ─────────────────────────────────────────
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
        st.warning("⚠️ Please enter a topic!")

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