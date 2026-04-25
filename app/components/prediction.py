from io import BytesIO

import streamlit as st
from PIL import Image


def load_uploaded_image(uploaded_file):
    image_bytes = uploaded_file.getvalue()
    return Image.open(BytesIO(image_bytes)).convert("RGB")


def render_prediction_result(image, prediction):
    left_col, right_col = st.columns([1.1, 0.9], gap="large")

    with left_col:
        st.subheader("Uploaded Image")
        st.image(image, use_container_width=True)

    with right_col:
        st.subheader("Prediction Summary")
        st.metric("Predicted Pest", prediction["label"])
        st.metric("Confidence", f"{prediction['confidence']:.2%}")
        st.progress(float(min(max(prediction["confidence"], 0.0), 1.0)))
        st.caption("Confidence bar shows the Top-1 probability from the YOLOv8 classification model.")
