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

bg = "#0a0a0f" if st.session_state.dark_mode else "#f5f5f5"
card = "#13131f" if st.session_state.dark_mode else "#ffffff"
input_bg = "#1e1e35" if st.session_state.dark_mode else "#ffffff"
text = "#ffffff" if st.session_state.dark_mode else "#1a1a1a"
subtext = "#888888" if st.session_state.dark_mode else "#666666"
border = "#2a2a3e" if st.session_state.dark_mode else "#e0e0e0"
accent = "#cc44ff" if st.session_state.dark_mode else "#f63366"
neon = "text-shadow:0 0 10px #ff00ff,0 0 25px #7700ff;" if st.session_state.dark_mode else ""

st.markdown(f"""
<style>
    #MainMenu {{visibility:hidden!important;}}
    footer {{visibility:hidden!important;}}
    .stDeployButton {{display:none!important;}}
    div[data-testid="stDecoration"] {{display:none!important;}}
    div[data-testid="stToolbar"] {{display:none!important;}}
    [data-testid="stStatusWidget"] {{display:none!important;}}
    header[data-testid="stHeader"] {{display:none!important;}}
    button[data-testid="collapsedControl"] {{display:none!important;}}
    section[data-testid="stSidebar"] {{display:none!important;}}
    .stApp {{background-color:{bg}!important;}}
    .main .block-container {{
        padding-top:1rem!important;
        max-width:800px!important;
    }}
    p,label,div {{color:{text};}}
    h1,h2,h3 {{color:{text}!important;}}
    .stTextInput input {{
        background-color:{input_bg}!important;
        color:{text}!important;
        border:1px solid {border}!important;
        border-radius:8px!important;
        font-size:15px!important;
    }}
    .stTextInput input::placeholder {{color:{subtext}!important;}}
    .stTextInput input:focus {{border-color:{accent}!important;}}
    .stButton>button {{
        background-color:{input_bg}!important;
        color:{text}!important;
        border:1px solid {border}!important;
        border-radius:8px!important;
        transition:all 0.2s!important;
    }}
    .stButton>button:hover {{
        border-color:{accent}!important;
        color:{accent}!important;
    }}
    .stDownloadButton>button {{
        background-color:{input_bg}!important;
        color:{text}!important;
        border:1px solid {border}!important;
        border-radius:8px!important;
    }}
    .stRadio label {{color:{text}!important;}}
    .stSelectbox>div>div {{
        background-color:{input_bg}!important;
        color:{text}!important;
        border:1px solid {border}!important;
        border-radius:8px!important;
    }}
    .stSelectbox svg {{fill:{text}!important;}}
    [data-baseweb="select"] * {{color:{text}!important;background-color:{input_bg}!important;}}
    [data-baseweb="popover"] * {{color:{text}!important;background-color:{input_bg}!important;}}
    [role="option"]:hover {{background-color:{border}!important;}}
    .gen-btn .stButton>button {{
        background:linear-gradient(135deg,#cc44ff,#7700ff)!important;
        color:white!important;
        border:none!important;
        border-radius:10px!important;
        font-weight:700!important;
        font-size:16px!important;
        box-shadow:0 0 20px #cc44ff66!important;
        padding:0.6rem!important;
    }}
    .gen-btn .stButton>button:hover {{
        box-shadow:0 0 35px #cc44ffaa!important;
        transform:translateY(-2px)!important;
        color:white!important;
    }}
    .blog-card {{
        background:{card};
        border:1px solid {border};
        border-left:4px solid {accent};
        border-radius:12px;
        padding:1.5rem;
        line-height:1.9;
        color:{text};
        font-size:15px;
        margin-top:1rem;
    }}
    .stats {{color:{subtext};font-size:13px;margin:6px 0 16px 0;}}
    [data-testid="stExpander"] {{
        border:1px solid {border}!important;
        border-radius:8px!important;
        background:{input_bg}!important;
        margin-bottom:6px!important;
    }}
    .streamlit-expanderHeader p {{color:{text}!important;font-size:13px!important;}}
    .divider {{
        border:none;
        border-top:1px solid {border};
        margin:1.5rem 0;
    }}
</style>
""", unsafe_allow_html=True)

# ── HEADER ────────────────────────────────────────────────
h1, h2 = st.columns([9, 1])
with h1:
    st.markdown(f"""
    <div style="text-align:center;padding:10px 0 16px 0;">
        <div style="{neon}color:{accent};font-size:2.8rem;font-weight:900;letter-spacing:-1px;">
            ✍️ AI Blog Generator
        </div>
        <div style="margin-top:8px;">
            <span style="background:{accent}18;border:1px solid {accent}33;
                border-radius:20px;padding:3px 16px;font-size:12px;color:{subtext};">
                Generate professional blogs instantly
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
with h2:
    st.write("")
    if st.button("🌙" if not st.session_state.dark_mode else "☀️", key="theme"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

st.markdown(f'<hr class="divider">', unsafe_allow_html=True)

# ── INPUT ─────────────────────────────────────────────────
topic = st.text_input("", placeholder="✏️  Enter your topic — eg. Will AI replace jobs?", label_visibility="collapsed")

c1, c2 = st.columns([1, 1])
with c1:
    blog_length = st.radio(
        "Length", ["short", "long"], horizontal=True,
        format_func=lambda x: "⚡ Short (200-300 words)" if x == "short" else "📖 Long (500-800 words)"
    )
with c2:
    tone = st.selectbox(
        "Tone",
        ["formal", "casual", "sarcastic", "inspirational"],
        format_func=lambda x: {
            "formal": "🎩 Professional — high level English",
            "casual": "😊 Casual — simple everyday language",
            "sarcastic": "😏 Sarcastic — funny but hits reality",
            "inspirational": "💪 Inspirational — motivating"
        }[x]
    )

# ── BUTTONS ───────────────────────────────────────────────
b1, b2, b3 = st.columns([3, 1, 1])
with b1:
    st.markdown('<div class="gen-btn">', unsafe_allow_html=True)
    generate = st.button("🚀 Generate Blog", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
with b2:
    if st.button("🗑️ Clear", use_container_width=True):
        st.session_state.current_blog = None
        st.rerun()
with b3:
    share = st.button("🔗 Share", use_container_width=True)

if share:
    st.info("🔗 https://blog-agent-wq4kzbsmq5azaq4gf2axsv.streamlit.app")

# ── GENERATE ──────────────────────────────────────────────
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

# ── BLOG OUTPUT ───────────────────────────────────────────
if st.session_state.current_blog:
    blog = st.session_state.current_blog
    word_count = len(blog["blog"].split())
    read_time = max(1, word_count // 200)

    st.markdown(f"## {blog['title']}")
    st.markdown(f'<div class="stats">📏 {blog["length"].capitalize()} &nbsp;|&nbsp; 🎭 {blog["tone"].capitalize()} &nbsp;|&nbsp; 📊 {word_count} words &nbsp;|&nbsp; ⏱️ {read_time} min read &nbsp;|&nbsp; 🕐 {blog["time"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="blog-card">{blog["blog"]}</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    blog_text = f"{blog['title']}\n\n{blog['blog']}"
    st.download_button(
        "📥 Save Blog",
        data=blog_text,
        file_name=f"{blog['topic'][:30]}.txt",
        mime="text/plain",
        use_container_width=True
    )

else:
    st.markdown(f"""
    <div style="text-align:center;padding:60px 0;color:{subtext};">
        <div style="font-size:50px;margin-bottom:16px;">✍️</div>
        <div style="font-size:1rem;">Enter a topic above and click Generate Blog</div>
    </div>
    """, unsafe_allow_html=True)

# ── HISTORY ───────────────────────────────────────────────
if st.session_state.blog_history:
    st.markdown(f'<hr class="divider">', unsafe_allow_html=True)
    st.markdown(f'<div style="font-size:11px;font-weight:700;color:{accent};letter-spacing:1.5px;margin-bottom:8px;">📚 HISTORY</div>', unsafe_allow_html=True)

    seen = set()
    unique_history = []
    for item in reversed(st.session_state.blog_history):
        key = item["topic"].lower().strip()
        if key not in seen:
            seen.add(key)
            unique_history.append(item)

    hc1, hc2 = st.columns([4, 1])
    with hc2:
        if st.button("🗑️ Clear All", use_container_width=True):
            st.session_state.blog_history = []
            st.session_state.current_blog = None
            st.rerun()

    for i, item in enumerate(unique_history):
        with st.expander(f"📄 {item['topic']} — {item['time']}"):
            st.write(f"**{item['title']}**")
            st.caption(f"{item['length'].capitalize()} · {item.get('tone','formal').capitalize()}")
            if st.button("Load this blog", key=f"load_{i}", use_container_width=True):
                st.session_state.current_blog = item
                st.rerun()