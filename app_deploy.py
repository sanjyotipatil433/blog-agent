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
if "generate_trigger" not in st.session_state:
    st.session_state.generate_trigger = False

if st.session_state.dark_mode:
    bg = "#0a0a0f"
    sidebar_bg = "#13131f"
    card = "#1a1a2e"
    input_bg = "#1e1e35"
    text = "#ffffff"
    subtext = "#888888"
    border = "#2a2a3e"
    accent = "#cc44ff"
else:
    bg = "#f5f5f5"
    sidebar_bg = "#ffffff"
    card = "#f8f8f8"
    input_bg = "#ffffff"
    text = "#1a1a1a"
    subtext = "#666666"
    border = "#e0e0e0"
    accent = "#f63366"

neon = "text-shadow: 0 0 10px #ff00ff, 0 0 20px #7700ff, 0 0 40px #ff00ff;" if st.session_state.dark_mode else ""
title_color = "#cc44ff" if st.session_state.dark_mode else "#f63366"
title_border = "" if st.session_state.dark_mode else f"border-bottom: 3px solid {accent}; padding-bottom: 4px;"

st.markdown(f"""
<style>
    #MainMenu {{ visibility: hidden !important; }}
    footer {{ visibility: hidden !important; }}
    .stDeployButton {{ display: none !important; }}
    div[data-testid="stDecoration"] {{ display: none !important; }}
    div[data-testid="stToolbar"] {{ display: none !important; }}
    [data-testid="stStatusWidget"] {{ display: none !important; }}
    iframe[title="streamlit_analytics"] {{ display: none !important; }}
    header[data-testid="stHeader"] {{
        background-color: {bg} !important;
        height: 0px !important;
    }}
    .stApp {{ background-color: {bg}; }}
    .main .block-container {{
        padding-top: 0.5rem !important;
        padding-bottom: 0rem !important;
        max-width: 100% !important;
    }}
    section[data-testid="stSidebar"] {{
        background-color: {sidebar_bg} !important;
        border-right: 1px solid {border} !important;
        padding: 1rem !important;
    }}
    section[data-testid="stSidebar"] * {{ color: {text} !important; }}
    p, label, .stMarkdown {{ color: {text}; }}
    h1, h2, h3 {{ color: {text} !important; }}
    .blog-title {{
        {neon}
        {title_border}
        color: {title_color};
        font-size: 1.8rem;
        font-weight: 900;
        text-align: center;
        display: block;
        margin: 0;
    }}
    .subtitle {{
        text-align: center;
        color: {subtext};
        font-size: 0.85rem;
        display: block;
        background: linear-gradient(90deg, {accent}33, {accent}66, {accent}33);
        border-radius: 20px;
        padding: 3px 12px;
        width: fit-content;
        margin: 0.3rem auto 0 auto;
    }}
    .stTextInput input, .stTextArea textarea {{
        background-color: {input_bg} !important;
        color: {text} !important;
        border: 1px solid {border} !important;
        border-radius: 8px !important;
    }}
    .stTextInput input:focus {{
        border-color: {accent} !important;
        box-shadow: 0 0 0 2px {accent}44 !important;
    }}
    /* Normal buttons */
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
    .generate-btn button {{
        background: linear-gradient(135deg, #cc44ff, #7700ff) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        box-shadow: 0 0 15px #cc44ff88 !important;
        transition: all 0.3s !important;
    }}
    .generate-btn button:hover {{
        box-shadow: 0 0 25px #cc44ffcc !important;
        transform: translateY(-1px) !important;
        background: linear-gradient(135deg, #dd55ff, #8811ff) !important;
    }}
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
    .blog-card {{
        background: {card};
        border: 1px solid {border};
        border-left: 4px solid {accent};
        border-radius: 12px;
        padding: 1.5rem;
        line-height: 1.8;
        color: {text};
    }}
    .stats-bar {{
        color: {subtext};
        font-size: 0.82rem;
        margin: 0.3rem 0 1rem 0;
    }}
    [data-testid="stExpander"] {{
        border: 1px solid {border} !important;
        border-radius: 8px !important;
        margin-bottom: 0.4rem !important;
        background: {input_bg} !important;
    }}
    /* Theme toggle small */
    .theme-btn button {{
        padding: 0.2rem 0.5rem !important;
        font-size: 0.8rem !important;
        border-radius: 20px !important;
        min-height: 0px !important;
        height: 32px !important;
        width: 60px !important;
    }}
</style>
""", unsafe_allow_html=True)

# ── Top header ─────────────────────────────
col_space, col_title, col_toggle = st.columns([0.3, 8, 0.8])
with col_title:
    st.markdown(f'<span class="blog-title">✍️ AI Blog Generator</span>', unsafe_allow_html=True)
    st.markdown(f'<span class="subtitle">Generate professional blogs instantly</span>', unsafe_allow_html=True)
with col_toggle:
    st.markdown('<div class="theme-btn">', unsafe_allow_html=True)
    if st.button("🌙" if not st.session_state.dark_mode else "☀️"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ── Sidebar ─────────────────────────────────
with st.sidebar:
    st.markdown(f"### 📝 Blog Content")

    topic = st.text_input(
        "Enter your topic:",
        placeholder="eg. Will AI eat jobs?",
        key="topic_input"
    )

    st.markdown(f"### ⚙️ Parameters")

    col_l, col_t = st.columns([1, 1])
    with col_l:
        blog_length = st.radio(
            "Length",
            ["short", "long"],
            format_func=lambda x: "⚡ Short" if x == "short" else "📖 Long"
        )
    with col_t:
        tone = st.selectbox(
            "Tone",
            ["formal", "casual", "sarcastic", "inspirational"],
            format_func=lambda x: {
                "formal": "🎩 Formal",
                "casual": "😊 Casual",
                "sarcastic": "😏 Sarcastic",
                "inspirational": "💪 Inspiring"
            }[x]
        )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="generate-btn">', unsafe_allow_html=True)
    generate = st.button("🚀 Generate Blog", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Enter key trigger
    if topic and st.session_state.get("topic_input") and st.session_state.generate_trigger:
        st.session_state.generate_trigger = False
        generate = True

    st.markdown("---")
    st.markdown("### 📚 History")

    # Unique history only
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
            with st.expander(f"📄 {item['topic'][:28]}"):
                st.caption(f"{item['length'].capitalize()} · {item.get('tone','formal').capitalize()}")
                if st.button("Load", key=f"load_{i}", use_container_width=True):
                    st.session_state.current_blog = item
                    st.rerun()
    else:
        st.caption("No blogs yet!")

# ── Main area ────────────────────────────────
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

    col_a1, col_a2, col_a3 = st.columns([1, 1, 1])
    with col_a1:
        blog_text = f"{blog['title']}\n\n{blog['blog']}"
        st.download_button(
            "📥 Download",
            data=blog_text,
            file_name=f"{blog['topic'][:30]}.txt",
            mime="text/plain",
            use_container_width=True
        )
    with col_a2:
        if st.button("🗑️ Clear Blog", use_container_width=True):
            st.session_state.current_blog = None
            st.rerun()
    with col_a3:
        if st.button("🔗 Copy Link", use_container_width=True):
            st.code("https://blog-agent-wq4kzbsmq5azaq4gf2axsv.streamlit.app")
            st.success("✅ Copy the link above!")
else:
    st.markdown(f"""
    <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:60vh;color:{subtext};text-align:center;">
        <div style="font-size:4rem;">✍️</div>
        <div style="font-size:1.2rem;margin-top:1rem;color:{subtext};">Enter a topic and click Generate Blog</div>
        <div style="font-size:0.9rem;margin-top:0.5rem;color:{subtext};">Your blog will appear here</div>
    </div>
    """, unsafe_allow_html=True)