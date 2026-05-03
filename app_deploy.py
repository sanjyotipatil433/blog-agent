import streamlit as st
import datetime
from graph.builder import blog_graph

st.set_page_config(
    page_title="AI Blog Generator",
    page_icon="✍️",
    layout="centered"
)

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True
if "blog_history" not in st.session_state:
    st.session_state.blog_history = []
if "current_blog" not in st.session_state:
    st.session_state.current_blog = None

if st.session_state.dark_mode:
    bg = "#0a0a0f"
    card = "#13131f"
    input_bg = "#1a1a2e"
    text = "#ffffff"
    subtext = "#888888"
    border = "#2a2a3e"
    accent = "#ff66ff"
    neon = "text-shadow: 0 0 10px #ff00ff, 0 0 20px #7700ff, 0 0 40px #ff00ff;"
    title_style = f"color: #ff66ff; {neon}"
else:
    bg = "#ffffff"
    card = "#f8f8f8"
    input_bg = "#ffffff"
    text = "#1a1a1a"
    subtext = "#666666"
    border = "#e0e0e0"
    accent = "#f63366"
    title_style = "color: #f63366; border-bottom: 3px solid #f63366; padding-bottom: 4px;"

st.markdown(f"""
<style>
    #MainMenu {{ visibility: hidden !important; }}
    footer {{ visibility: hidden !important; }}
    .stDeployButton {{ display: none !important; }}
    div[data-testid="stDecoration"] {{ display: none !important; }}
    div[data-testid="stToolbar"] {{ display: none !important; }}
    [data-testid="stStatusWidget"] {{ display: none !important; }}
    header[data-testid="stHeader"] {{
        background-color: {bg} !important;
        height: 0px !important;
        min-height: 0px !important;
    }}
    .stApp {{ background-color: {bg}; }}
    .main .block-container {{
        padding-top: 1.5rem !important;
        padding-bottom: 1rem !important;
        max-width: 750px !important;
    }}
    p, label, .stMarkdown {{ color: {text}; }}
    h1, h2, h3 {{ color: {text} !important; }}
    .blog-title {{
        {title_style}
        font-size: 2.4rem;
        font-weight: 900;
        text-align: center;
        width: 100%;
        display: block;
        margin: 0 0 0.2rem 0;
    }}
    .subtitle {{
        text-align: center;
        color: {subtext};
        font-size: 0.9rem;
        display: block;
        width: 100%;
        margin-bottom: 1.5rem;
    }}
    .stTextInput input {{
        background-color: {input_bg} !important;
        color: {text} !important;
        border: 1px solid {border} !important;
        border-radius: 10px !important;
    }}
    .stTextInput input:focus {{
        border-color: {accent} !important;
    }}
    .stButton>button {{
        background-color: {input_bg} !important;
        color: {text} !important;
        border: 1px solid {border} !important;
        border-radius: 10px !important;
        transition: all 0.2s !important;
    }}
    .stButton>button:hover {{
        border-color: {accent} !important;
        color: {accent} !important;
    }}
    .stDownloadButton>button {{
        background-color: {input_bg} !important;
        color: {text} !important;
        border: 1px solid {border} !important;
        border-radius: 10px !important;
    }}
    .stRadio label {{ color: {text} !important; }}
    .stSelectbox > div > div {{
        background-color: {input_bg} !important;
        color: {text} !important;
        border: 1px solid {border} !important;
        border-radius: 10px !important;
    }}
    .blog-content {{
        background: {card};
        border: 1px solid {border};
        border-left: 4px solid {accent};
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 1rem;
        line-height: 1.8;
        color: {text};
    }}
    .stats-bar {{
        color: {subtext};
        font-size: 0.85rem;
        margin: 0.3rem 0;
    }}
    .footer {{
        text-align: center;
        color: {subtext};
        font-size: 0.8rem;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid {border};
    }}
    .footer a {{ color: {accent}; text-decoration: none; }}
    [data-testid="stExpander"] {{
        border: 1px solid {border} !important;
        border-radius: 10px !important;
    }}
    .streamlit-expanderHeader {{ color: {text} !important; }}
</style>
""", unsafe_allow_html=True)

# ── Header ──────────────────────────────
col_h1, col_h2 = st.columns([5, 1])
with col_h1:
    st.markdown(f'<span class="blog-title">✍️ AI Blog Generator</span>', unsafe_allow_html=True)
    st.markdown(f'<span class="subtitle">Generate professional blogs instantly</span>', unsafe_allow_html=True)
with col_h2:
    if st.button("🌙" if not st.session_state.dark_mode else "☀️", use_container_width=True):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

st.markdown("---")

# ── Input ────────────────────────────────
topic = st.text_input(
    "Enter your topic:",
    placeholder="eg. Benefits of Artificial Intelligence"
)

col_len, col_tone = st.columns([1, 1])
with col_len:
    blog_length = st.radio(
        "Length:",
        ["short", "long"],
        horizontal=True,
        format_func=lambda x: "⚡ Short" if x == "short" else "📖 Long"
    )
with col_tone:
    tone = st.selectbox(
        "Tone:",
        ["formal", "casual", "funny", "inspirational"],
        format_func=lambda x: {
            "formal": "🎩 Formal",
            "casual": "😊 Casual",
            "funny": "😂 Funny",
            "inspirational": "💪 Inspirational"
        }[x]
    )

col_b1, col_b2 = st.columns([3, 1])
with col_b1:
    generate = st.button("🚀 Generate Blog", use_container_width=True)
with col_b2:
    if st.button("🗑️ Clear", use_container_width=True):
        st.session_state.current_blog = None
        st.rerun()

# ── Generate ─────────────────────────────
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

# ── Blog Output ───────────────────────────
if st.session_state.current_blog:
    blog = st.session_state.current_blog
    word_count = len(blog["blog"].split())
    read_time = max(1, word_count // 200)

    st.markdown(f"## {blog['title']}")
    st.markdown(f'<div class="stats-bar">📏 {blog["length"].capitalize()} &nbsp;|&nbsp; 🎭 {blog["tone"].capitalize()} &nbsp;|&nbsp; 📊 {word_count} words &nbsp;|&nbsp; ⏱️ {read_time} min read</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(f'<div class="blog-content">{blog["blog"]}</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Action buttons
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
        twitter_url = f"https://twitter.com/intent/tweet?text=Check out this blog: {blog['title']}"
        st.markdown(f'<a href="{twitter_url}" target="_blank"><button style="width:100%;padding:0.45rem;border-radius:10px;border:1px solid {border};background:{input_bg};color:{text};cursor:pointer;font-size:0.95rem;">🐦 Share on X</button></a>', unsafe_allow_html=True)
    with col_a3:
        st.markdown(f'<a href="https://www.linkedin.com/sharing/share-offsite/?url=https://blog-agent-wq4kzbsmq5azaq4gf2axsv.streamlit.app" target="_blank"><button style="width:100%;padding:0.45rem;border-radius:10px;border:1px solid {border};background:{input_bg};color:{text};cursor:pointer;font-size:0.95rem;">💼 LinkedIn</button></a>', unsafe_allow_html=True)

# ── History ───────────────────────────────
if st.session_state.blog_history:
    st.markdown("---")
    st.subheader("📚 History")
    if st.button("🗑️ Clear History"):
        st.session_state.blog_history = []
        st.rerun()
    for i, item in enumerate(reversed(st.session_state.blog_history)):
        with st.expander(f"📄 {item['topic'][:40]}"):
            st.write(f"**{item['title']}**")
            st.caption(f"{item['length'].capitalize()} · {item.get('tone','formal').capitalize()} · {item['time']}")
            if st.button("Load", key=f"load_{i}", use_container_width=True):
                st.session_state.current_blog = item
                st.rerun()

# ── Footer ────────────────────────────────
st.markdown(f'''
<div class="footer">
    Built with ❤️ using LangGraph · FastAPI · Streamlit · Groq &nbsp;|&nbsp;
    <a href="https://github.com/sanjyotipatil433/blog-agent">GitHub</a>
</div>
''', unsafe_allow_html=True)