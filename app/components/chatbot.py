import streamlit as st

from config.settings import ALLOWED_CHAT_MODES, DEFAULT_CHAT_MODE


def render_chat_controls():
    st.subheader("Pest Assistant")
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
        placeholder="Example: What pesticide should I use and how can I prevent this next season?",
    )
    ask = st.button("Ask Assistant", use_container_width=True)
    return mode, question, ask


def render_chat_response(answer, source_label):
    st.caption(source_label)
    st.markdown(answer)
