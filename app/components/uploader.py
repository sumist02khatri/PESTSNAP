import streamlit as st

from config.settings import MAX_IMAGE_SIZE_MB


def render_uploader():
    st.markdown(
        """
        <div class="section-card">
            <div class="section-kicker">Input</div>
            <div class="section-title">Upload a rice crop image</div>
            <div class="section-copy">
                Drop a JPG, JPEG, or PNG file to start classification. The app will use your trained YOLOv8 model
                to estimate the most likely pest class and attach treatment guidance.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption(f"Accepted formats: JPG, JPEG, PNG up to {MAX_IMAGE_SIZE_MB} MB.")
    return st.file_uploader(
        "Choose an image",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=False,
        label_visibility="collapsed",
    )
