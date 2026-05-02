import streamlit as st

from config.settings import ALLOWED_CHAT_MODES, DEFAULT_CHAT_MODE, DEPLOYMENT_MODE


def render_chat_controls():
    st.markdown(
        """
        <div class="section-card">
            <div class="section-kicker">Assistant</div>
            <div class="section-title">Ask a pest-specific follow-up</div>
            <div class="section-copy">
                Use fast curated guidance, local Ollama inference, or free cloud AI to continue from the predicted pest result.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if DEPLOYMENT_MODE == "cloud":
        st.caption("Hosted mode is enabled, so Local Ollama mode is hidden.")
    mode = st.radio(
        "Assistant Mode",
        options=ALLOWED_CHAT_MODES,
        index=ALLOWED_CHAT_MODES.index(DEFAULT_CHAT_MODE)
        if DEFAULT_CHAT_MODE in ALLOWED_CHAT_MODES
        else 0,
        horizontal=True,
    )
    question = st.text_input(
        "Ask a question about the detected pest",
        placeholder="Example: What should I spray first and how do I reduce the chance of this returning next season?",
    )
    ask = st.button("Generate Advice", use_container_width=True)
    return mode, question, ask


def render_chat_response(answer, source_label):
    st.markdown(
        f"""
        <div class="section-card">
            <div class="section-kicker">Response Source</div>
            <div class="section-title">{source_label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(answer)
