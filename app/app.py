import re
import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from components.chatbot import render_chat_controls, render_chat_response
from components.prediction import load_uploaded_image, render_prediction_result
from components.recommendation import render_recommendation
from components.uploader import render_uploader
from config.settings import APP_ICON, APP_LAYOUT, APP_TITLE, CLASSES_PATH
from utils.llm_handler import get_chat_response
from utils.model_loader import load_model
from utils.pest_info import get_pest_details, normalize_pest_name


st.set_page_config(page_title=APP_TITLE, page_icon=APP_ICON, layout=APP_LAYOUT)


def inject_styles():
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(180deg, #f6f1e7 0%, #eef7ea 100%);
        }
        .hero-card {
            background: rgba(255, 255, 255, 0.9);
            border: 1px solid rgba(98, 126, 87, 0.15);
            border-radius: 20px;
            padding: 1.4rem 1.5rem;
            box-shadow: 0 12px 40px rgba(63, 78, 58, 0.08);
            margin-bottom: 1rem;
        }
        .hero-title {
            font-size: 2.1rem;
            font-weight: 700;
            color: #24361f;
        }
        .hero-copy {
            color: #4a5d45;
            font-size: 1rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def parse_classes_file():
    classes = []
    if not CLASSES_PATH.exists():
        return classes

    with CLASSES_PATH.open("r", encoding="utf-8") as file_handle:
        for raw_line in file_handle:
            line = raw_line.strip()
            if not line:
                continue
            cleaned = re.sub(r"^\d+\s+", "", line)
            cleaned = re.sub(r"\s+", " ", cleaned).strip()
            if cleaned:
                classes.append(cleaned)
    return classes


def get_label_from_model(model, top1_index):
    names = getattr(model, "names", {})

    if isinstance(names, dict):
        label = names.get(top1_index)
        if label:
            return label

    if isinstance(names, list) and 0 <= top1_index < len(names):
        return names[top1_index]

    parsed_classes = parse_classes_file()
    if 0 <= top1_index < len(parsed_classes):
        return parsed_classes[top1_index]

    return f"class_{top1_index}"


def predict_image(model, image):
    results = model(image)
    top1_index = int(results[0].probs.top1)
    confidence = float(results[0].probs.top1conf)
    label = get_label_from_model(model, top1_index)
    return {
        "label": label,
        "normalized_label": normalize_pest_name(label),
        "confidence": confidence,
    }


def render_header():
    st.markdown(
        f"""
        <div class="hero-card">
            <div class="hero-title">{APP_ICON} {APP_TITLE}</div>
            <div class="hero-copy">
                Upload a rice crop image to classify the likely pest, review treatment guidance,
                and ask follow-up questions in fast, local, or free-cloud assistant modes.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def main():
    inject_styles()
    render_header()

    try:
        model = load_model()
    except Exception as exc:
        st.error(f"Unable to load model: {exc}")
        st.stop()

    uploaded_file = render_uploader()
    if not uploaded_file:
        st.info("Upload an image to begin prediction.")
        return

    image = load_uploaded_image(uploaded_file)
    prediction = predict_image(model, image)
    pest_details = get_pest_details(prediction["normalized_label"])

    render_prediction_result(image, prediction)
    st.divider()
    render_recommendation(pest_details)
    st.divider()

    chat_mode, question, ask_clicked = render_chat_controls()
    if ask_clicked:
        if not question.strip():
            st.warning("Enter a question for the assistant.")
        else:
            answer, source_label = get_chat_response(
                chat_mode,
                question.strip(),
                prediction["label"],
                prediction["confidence"],
                pest_details,
            )
            render_chat_response(answer, source_label)


if __name__ == "__main__":
    main()
