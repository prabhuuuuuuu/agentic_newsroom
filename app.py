# app.py
import streamlit as st
import uuid
import time

# ============ PAGE CONFIGURATION ============
st.set_page_config(
    page_title="Agentic Newsroom",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============ CUSTOM CSS — ChatGPT-style ============
st.markdown("""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

/* ── Root / Body ── */
html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background-color: #212121 !important;
    color: #ececec !important;
    font-family: 'Inter', sans-serif !important;
}

/* hide default header / footer / hamburger */
#MainMenu, header, footer { visibility: hidden; }
[data-testid="collapsedControl"] { display: none; }

/* ── Remove default padding from main block ── */
[data-testid="stAppViewContainer"] > .main > .block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* ── HERO / EMPTY STATE ── */
.hero-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 92vh;
    padding: 2rem;
    gap: 1.5rem;
}
.hero-logo {
    font-size: 2.8rem;
    font-weight: 600;
    color: #ececec;
    letter-spacing: -0.5px;
    margin-bottom: 0.25rem;
}
.hero-sub {
    font-size: 1rem;
    color: #8e8ea0;
    margin-bottom: 1.5rem;
}

/* ── INPUT BOX (chat-style) ── */
.input-bar-wrapper {
    width: 100%;
    max-width: 720px;
    background: #2f2f2f;
    border: 1px solid #444;
    border-radius: 16px;
    padding: 12px 16px;
    display: flex;
    align-items: center;
    gap: 10px;
    box-shadow: 0 0 30px rgba(0,0,0,0.4);
    transition: border-color 0.2s;
}
.input-bar-wrapper:focus-within {
    border-color: #10a37f;
    box-shadow: 0 0 0 2px rgba(16,163,127,0.2);
}

/* Override Streamlit's text_input inside the bar */
.input-bar-wrapper .stTextInput > div > div > input {
    background: transparent !important;
    border: none !important;
    color: #ececec !important;
    font-size: 1rem !important;
    font-family: 'Inter', sans-serif !important;
    box-shadow: none !important;
    padding: 4px 0 !important;
}
.input-bar-wrapper .stTextInput > div > div {
    border: none !important;
    background: transparent !important;
}
.input-bar-wrapper .stTextInput { flex: 1 !important; }

/* ── SEND BUTTON ── */
.stButton > button {
    background: #10a37f !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 8px 18px !important;
    font-size: 0.95rem !important;
    font-weight: 500 !important;
    cursor: pointer !important;
    transition: background 0.2s, transform 0.1s !important;
    white-space: nowrap !important;
}
.stButton > button:hover { background: #0d8a6b !important; transform: scale(1.02); }
.stButton > button:active { transform: scale(0.98); }

/* ── CONTENT AREA ── */
.content-wrapper {
    max-width: 900px;
    margin: 0 auto;
    padding: 2rem 1.5rem 6rem;
}

/* ── CHAT INPUT (shown at bottom when content exists) ── */
.bottom-bar {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: linear-gradient(to top, #212121 70%, transparent);
    padding: 1.5rem 2rem 1.5rem;
    display: flex;
    justify-content: center;
    z-index: 100;
}
.bottom-bar-inner {
    width: 100%;
    max-width: 720px;
    background: #2f2f2f;
    border: 1px solid #444;
    border-radius: 16px;
    padding: 10px 14px;
    display: flex;
    align-items: center;
    gap: 10px;
    box-shadow: 0 0 30px rgba(0,0,0,0.5);
}

/* ── STEP CARDS (log) ── */
.step-card {
    background: #2a2a2a;
    border-left: 3px solid #10a37f;
    border-radius: 8px;
    padding: 10px 16px;
    margin: 6px 0;
    font-size: 0.9rem;
    color: #c5c5d2;
}

/* ── ARTICLE CARD ── */
.article-card {
    background: #2a2a2a;
    border-radius: 14px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    border: 1px solid #3a3a3a;
}
.article-card h1, .article-card h2, .article-card h3 {
    color: #ececec !important;
}
.article-card p, .article-card li { color: #c5c5d2 !important; line-height: 1.75; }
.article-card code { background: #1a1a2e; border-radius: 4px; padding: 2px 6px; color: #7ec8e3; }
.article-card pre { background: #1a1a2e !important; border-radius: 10px; padding: 1rem; }

/* ── REVIEW CARD ── */
.review-card {
    background: #2a2a2a;
    border: 1px solid #10a37f44;
    border-radius: 14px;
    padding: 1.5rem 2rem;
    margin: 1.5rem 0;
}

/* ── PILL BADGE ── */
.status-badge {
    display: inline-block;
    background: #10a37f22;
    color: #10a37f;
    border: 1px solid #10a37f44;
    padding: 3px 12px;
    border-radius: 999px;
    font-size: 0.8rem;
    font-weight: 500;
    margin-bottom: 1rem;
}

/* tweak streamlit radio / textarea in dark bg */
[data-testid="stRadio"] label { color: #c5c5d2 !important; }
[data-testid="stTextArea"] textarea {
    background: #1e1e1e !important;
    color: #ececec !important;
    border-color: #444 !important;
    border-radius: 10px !important;
}
[data-testid="stAlert"] { border-radius: 10px !important; }
</style>
""", unsafe_allow_html=True)

# ============ SESSION STATE ============
if "thread_id"        not in st.session_state: st.session_state.thread_id        = None
if "awaiting_review"  not in st.session_state: st.session_state.awaiting_review  = False
if "generation_done"  not in st.session_state: st.session_state.generation_done  = False
if "final_draft"      not in st.session_state: st.session_state.final_draft      = ""
if "final_image"      not in st.session_state: st.session_state.final_image      = ""
if "log_messages"     not in st.session_state: st.session_state.log_messages     = []
if "topic"            not in st.session_state: st.session_state.topic            = ""
if "generating"       not in st.session_state: st.session_state.generating       = False

has_content = bool(st.session_state.final_draft or st.session_state.generating)

# ============================================================
# HERO — shown when no generation has started yet
# ============================================================
if not has_content:
    st.markdown('<div class="hero-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="hero-logo">📰 Agentic Newsroom</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">AI-powered blog generator · Human-in-the-loop editing</div>', unsafe_allow_html=True)

    # Centered input bar using a form (Enter submits)
    with st.form("hero_form", clear_on_submit=False):
        st.markdown('<div class="input-bar-wrapper">', unsafe_allow_html=True)
        col_input, col_btn = st.columns([10, 1])
        with col_input:
            topic_input = st.text_input(
                "topic", label_visibility="collapsed",
                placeholder="What should I write about today?",
                key="hero_topic"
            )
        with col_btn:
            submitted = st.form_submit_button("➤", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # close hero-wrapper

    if submitted and topic_input.strip():
        st.session_state.topic = topic_input.strip()
        st.session_state.generating = True
        st.session_state.log_messages = []
        st.session_state.final_draft = ""
        st.session_state.final_image = ""
        st.session_state.awaiting_review = False
        st.session_state.generation_done = False
        st.session_state.thread_id = str(uuid.uuid4())
        st.rerun()
    elif submitted:
        st.warning("Please type a topic first!")

# ============================================================
# CONTENT AREA — shown during / after generation
# ============================================================
else:
    st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)

    # ── Header ──
    st.markdown(f"<h2 style='color:#ececec; margin-bottom:0.25rem;'>📰 Agentic Newsroom</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:#8e8ea0; margin-top:0;'>Topic: <strong style='color:#c5c5d2;'>{st.session_state.topic}</strong></p>", unsafe_allow_html=True)

    # ── Progress Log ──
    if st.session_state.log_messages:
        for msg in st.session_state.log_messages:
            st.markdown(f'<div class="step-card">{msg}</div>', unsafe_allow_html=True)

    # ── Image ──
    if st.session_state.final_image and "error" not in st.session_state.final_image:
        st.image(st.session_state.final_image, use_container_width=True)

    # ── Article ──
    if st.session_state.final_draft:
        st.markdown('<div class="article-card">', unsafe_allow_html=True)
        st.markdown(st.session_state.final_draft)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Review Card ──
    if st.session_state.awaiting_review and st.session_state.final_draft:
        from graph import graph
        st.markdown('<div class="review-card">', unsafe_allow_html=True)
        st.markdown('<div class="status-badge">⏸ Awaiting your review</div>', unsafe_allow_html=True)
        st.markdown("**What would you like to do with this draft?**")

        approval_choice = st.radio(
            "", ["✅ Approve & Publish", "🔄 Request Revisions"],
            horizontal=True, key="approval_radio", label_visibility="collapsed"
        )

        if approval_choice == "✅ Approve & Publish":
            if st.button("📤 Publish Article", key="publish_btn"):
                config = {"configurable": {"thread_id": st.session_state.thread_id}}
                with st.spinner("Publishing..."):
                    for event in graph.stream(None, config, stream_mode="values"):
                        if event.get("messages"):
                            st.session_state.log_messages = event["messages"]
                st.session_state.awaiting_review = False
                st.session_state.generation_done = True
                st.rerun()
        else:
            feedback = st.text_area(
                "Your feedback", placeholder="e.g. Add more code examples, make the intro shorter...",
                key="feedback_text"
            )
            if st.button("🔄 Revise", key="revise_btn"):
                if feedback.strip():
                    config = {"configurable": {"thread_id": st.session_state.thread_id}}
                    with st.spinner("Revising..."):
                        for event in graph.stream(
                            {"human_feedback": feedback, "approval_status": "needs_revision"},
                            config, stream_mode="values"
                        ):
                            if event.get("messages"):
                                st.session_state.log_messages = event["messages"]
                            if event.get("draft"):
                                st.session_state.final_draft = event["draft"]
                            img = event.get("image_path", "")
                            if img and "error" not in img:
                                st.session_state.final_image = img
                    st.session_state.awaiting_review = True
                    st.rerun()
                else:
                    st.warning("Please write your feedback first.")

        st.markdown('</div>', unsafe_allow_html=True)

    # ── Done banner ──
    if st.session_state.generation_done:
        st.success("🎉 Article published! Check the **output/** folder.")

    st.markdown('</div>', unsafe_allow_html=True)  # close content-wrapper

    # ─── Run agents (happens on the rerun triggered above) ───
    if st.session_state.generating:
        from graph import graph

        initial_state = {
            "topic": st.session_state.topic,
            "research_notes": [], "draft": "", "critique": "",
            "revision_count": 0, "human_feedback": "",
            "approval_status": "pending", "image_prompt": "",
            "image_path": "", "messages": []
        }
        config = {"configurable": {"thread_id": st.session_state.thread_id}}

        with st.spinner("🤖 Agents working… (LLM calls may take 1-2 mins)"):
            try:
                for event in graph.stream(initial_state, config, stream_mode="values"):
                    if event.get("messages"):
                        st.session_state.log_messages = event["messages"]
                    if event.get("draft"):
                        st.session_state.final_draft = event["draft"]
                    img = event.get("image_path", "")
                    if img and "error" not in img:
                        st.session_state.final_image = img

                # Graph paused at interrupt_before=["publisher"]
                st.session_state.generating = False
                st.session_state.awaiting_review = True
            except Exception as e:
                st.error(f"❌ {e}")
                import traceback; st.code(traceback.format_exc())
                st.session_state.generating = False

        st.rerun()