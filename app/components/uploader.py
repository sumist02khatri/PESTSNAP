import streamlit as st

from config.settings import MAX_IMAGE_SIZE_MB


def render_uploader():
    st.subheader("Upload Field Image")
    st.caption(f"Upload a rice pest image in JPG, JPEG, or PNG format up to {MAX_IMAGE_SIZE_MB} MB.")
    return st.file_uploader(
        "Choose an image",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=False,
        label_visibility="collapsed",
    )
