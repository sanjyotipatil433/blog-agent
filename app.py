import streamlit as st
import requests
import datetime

st.set_page_config(
    page_title="AI Blog Generator",
    page_icon="✍️",
    layout="wide"
)

# Theme toggle
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

if "blog_history" not in st.session_state:
    st.session_state.blog_history = []

if "current_blog" not in st.session_state:
    st.session_state.current_blog = None

# Dynamic CSS based on theme
if st.session_state.dark_mode:
    bg = "#0f0f1a"
    card_bg = "#1a1a2e"
    text = "#ffffff"
    subtext = "#aaaaaa"
    input_bg = "#1e1e2e"
    neon = "text-shadow: 0 0 10px #ff00ff, 0 0 20px #7700ff, 0 0 40px #ff00ff;"
    title_style = f"color: #ff66ff; {neon}"
else:
    bg = "#f5f5f5"
    card_bg = "#ffffff"
    text = "#1a1a1a"
    subtext = "#555555"
    input_bg = "#ffffff"
    title_style = "color: #f63366; border-bottom: 3px solid #f63366; display: inline-block; padding-bottom: 4px;"

st.markdown(f"""
<style>
    .stApp {{ background-color: {bg}; }}
    .main {{ background-color: {bg}; }}
    p, label, .stMarkdown, .stCaption {{ color: {text} !important; }}
    h1, h2, h3 {{ color: {text} !important; }}
    
    /* Input box */
    .stTextInput input {{
        background-color: {input_bg} !important;
        color: {text} !important;
        border: 1px solid #444 !important;
        border-radius: 8px !important;
    }}
    
    /* Buttons */
    .stButton>button {{
        background-color: {input_bg} !important;
        color: {text} !important;
        border: 1px solid #555 !important;
        border-radius: 8px !important;
    }}
    
    /* Radio */
    .stRadio label {{ color: {text} !important; }}
    
    /* Expander */
    .streamlit-expanderHeader {{ color: {text} !important; }}

    .blog-title {{
        {title_style}
        font-size: 2.5rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.5rem;
    }}
    .subtitle {{
        text-align: center;
        color: {subtext};
        margin-bottom: 2rem;
        font-size: 0.95rem;
    }}
    
    header[data-testid="stHeader"] {{
        background-color: {bg} !important;
    }}
    
    div[data-testid="stDecoration"] {{
        display: none !important;
    }}
</style>
""", unsafe_allow_html=True)

# Header
col_title, col_toggle = st.columns([5, 1])
with col_title:
    st.markdown(f'<div class="blog-title">✍️ AI Blog Generator</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="subtitle">Powered by LangGraph + Groq</div>', unsafe_allow_html=True)

with col_toggle:
    st.write("")
    st.write("")
    if st.button("🌙 Dark" if not st.session_state.dark_mode else "☀️ Light"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

# Main layout
col1, col2 = st.columns([2, 1])

with col1:
    topic = st.text_input(
        "Enter your topic:",
        placeholder="eg. Benefits of Artificial Intelligence",
        key="topic_input"
    )

    blog_length = st.radio(
        "Blog length:",
        ["short", "long"],
        horizontal=True,
        format_func=lambda x: "⚡ Short (200-300 words)" if x == "short" else "📖 Long (500-800 words)"
    )

    col_btn1, col_btn2 = st.columns([1, 1])
    with col_btn1:
        generate = st.button("🚀 Generate Blog", use_container_width=True)
    with col_btn2:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.current_blog = None
            st.rerun()

    if generate or (topic and st.session_state.get("enter_pressed")):
        if topic:
            with st.spinner("✍️ Writing your blog..."):
                response = requests.post(
                    "http://127.0.0.1:8000/generate",
                    json={"topic": topic, "blog_length": blog_length}
                )
                result = response.json()
                blog_data = {
                    "title": result["title"],
                    "blog": result["blog"],
                    "topic": topic,
                    "length": blog_length,
                    "time": datetime.datetime.now().strftime("%H:%M %d/%m/%Y")
                }
                st.session_state.current_blog = blog_data
                st.session_state.blog_history.append(blog_data)
        else:
            st.warning("Please enter a topic first!")

    if st.session_state.current_blog:
        blog = st.session_state.current_blog
        st.markdown(f"## {blog['title']}")
        st.markdown(f"*{blog['length'].capitalize()} blog • {blog['time']}*")
        st.markdown("---")
        st.markdown(blog["blog"])

        blog_text = f"{blog['title']}\n\n{blog['blog']}"
        st.download_button(
            label="📥 Download as Text",
            data=blog_text,
            file_name=f"{blog['topic']}.txt",
            mime="text/plain"
        )

with col2:
    st.subheader("📚 History")
    if st.session_state.blog_history:
        if st.button("🗑️ Clear History"):
            st.session_state.blog_history = []
            st.rerun()
        for i, item in enumerate(reversed(st.session_state.blog_history)):
            with st.expander(f"📄 {item['topic']} — {item['time']}"):
                st.write(f"**{item['title']}**")
                st.caption(f"Length: {item['length']}")
                if st.button("Load", key=f"load_{i}"):
                    st.session_state.current_blog = item
                    st.rerun()
    else:
        st.info("No blogs generated yet!")