from io import BytesIO

import streamlit as st
from PIL import Image


def load_uploaded_image(uploaded_file):
    image_bytes = uploaded_file.getvalue()
    return Image.open(BytesIO(image_bytes)).convert("RGB")


def render_prediction_result(image, prediction):
    st.markdown(
        """
        <div class="section-card">
            <div class="section-kicker">Detection Result</div>
            <div class="section-title">Visual review and model confidence</div>
            <div class="section-copy">
                Compare the uploaded field image with the classifier output and confidence score before applying any treatment.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left_col, right_col = st.columns([1.18, 0.82], gap="large")

    with left_col:
        st.image(image, use_container_width=True)

    with right_col:
        confidence_pct = prediction["confidence"] * 100
        st.markdown(
            f"""
            <div class="section-card">
                <div class="section-kicker">Primary Label</div>
                <div class="section-title">{prediction["label"]}</div>
                <div class="section-copy">
                    The model selected this class as the strongest match for the uploaded image.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        metric_a, metric_b = st.columns(2, gap="medium")
        with metric_a:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">Confidence</div>
                    <div class="metric-value">{confidence_pct:.2f}%</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with metric_b:
            st.markdown(
                """
                <div class="metric-card">
                    <div class="metric-label">Prediction Rank</div>
                    <div class="metric-value is-small">Top-1</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.progress(float(min(max(prediction["confidence"], 0.0), 1.0)))
        st.caption("Confidence bar reflects the Top-1 classification probability from the YOLOv8 model.")
