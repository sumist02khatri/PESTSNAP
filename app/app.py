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
        @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Sora:wght@500;600;700;800&display=swap');

        :root {
            --bg-top: #081611;
            --bg-mid: #10261c;
            --bg-bottom: #173826;
            --ink: #0f2019;
            --muted: #64796f;
            --panel: rgba(252, 248, 240, 0.90);
            --line: rgba(22, 58, 42, 0.12);
            --accent: #0f4f37;
            --gold: #d7a44f;
            --shadow: 0 28px 90px rgba(0, 0, 0, 0.26);
            --shadow-soft: 0 14px 34px rgba(0, 0, 0, 0.12);
            --field-pattern: url("data:image/svg+xml,%3Csvg width='420' height='420' viewBox='0 0 420 420' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cg opacity='0.4'%3E%3Cpath d='M0 330C58 306 108 302 168 316C228 330 274 358 334 364C372 368 396 362 420 350' stroke='%23d9f0dd' stroke-opacity='0.22' stroke-width='1.4'/%3E%3Cpath d='M-4 278C48 254 108 248 174 262C240 276 278 308 344 316C374 320 398 316 424 304' stroke='%23d9f0dd' stroke-opacity='0.18' stroke-width='1.2'/%3E%3Cpath d='M0 224C50 200 108 194 170 204C232 214 286 244 346 250C380 254 402 248 420 238' stroke='%23f3d49c' stroke-opacity='0.14' stroke-width='1.1'/%3E%3Cpath d='M44 0V420' stroke='%23ffffff' stroke-opacity='0.05' stroke-width='0.8'/%3E%3Cpath d='M146 0V420' stroke='%23ffffff' stroke-opacity='0.04' stroke-width='0.8'/%3E%3Cpath d='M250 0V420' stroke='%23ffffff' stroke-opacity='0.04' stroke-width='0.8'/%3E%3Cpath d='M354 0V420' stroke='%23ffffff' stroke-opacity='0.05' stroke-width='0.8'/%3E%3C/g%3E%3C/svg%3E");
        }

        html, body, [class*="css"] {
            font-family: "Manrope", sans-serif;
        }

        .stApp {
            background:
                radial-gradient(circle at 12% 8%, rgba(215, 164, 79, 0.32), transparent 18%),
                radial-gradient(circle at 88% 16%, rgba(70, 160, 109, 0.20), transparent 20%),
                radial-gradient(circle at 52% 78%, rgba(255, 244, 214, 0.07), transparent 18%),
                linear-gradient(140deg, rgba(255,255,255,0.06), transparent 34%),
                var(--field-pattern),
                linear-gradient(180deg, var(--bg-top) 0%, var(--bg-mid) 48%, var(--bg-bottom) 100%);
            background-size: auto, auto, auto, auto, 420px 420px, auto;
            background-attachment: scroll, scroll, scroll, scroll, fixed, fixed;
            color: #eaf4ec;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1180px;
        }

        h1, h2, h3 {
            font-family: "Sora", sans-serif;
            color: #eff7f1;
            letter-spacing: -0.02em;
        }

        .hero-shell {
            position: relative;
            overflow: hidden;
            background:
                radial-gradient(circle at 100% 0%, rgba(215, 164, 79, 0.22), transparent 28%),
                radial-gradient(circle at 0% 100%, rgba(70, 160, 109, 0.18), transparent 22%),
                linear-gradient(145deg, rgba(7, 30, 21, 0.94), rgba(18, 54, 37, 0.92));
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 34px;
            padding: 2.2rem 2.2rem 1.8rem;
            box-shadow: var(--shadow);
            backdrop-filter: blur(12px);
            margin-bottom: 1.35rem;
            transition: transform 220ms ease, box-shadow 220ms ease;
        }

        .hero-shell:hover {
            transform: translateY(-2px);
            box-shadow: 0 32px 90px rgba(0, 0, 0, 0.30);
        }

        .hero-shell::before {
            content: "";
            position: absolute;
            inset: 0;
            background:
                linear-gradient(115deg, rgba(255,255,255,0.08), transparent 40%),
                radial-gradient(circle at 82% 20%, rgba(199,146,61,0.16), transparent 22%);
            pointer-events: none;
        }

        .hero-shell::after {
            content: "";
            position: absolute;
            right: -72px;
            top: -72px;
            width: 260px;
            height: 260px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(199,146,61,0.22), transparent 68%);
            pointer-events: none;
        }

        .hero-layout {
            position: relative;
            z-index: 1;
            display: grid;
            grid-template-columns: minmax(0, 1.4fr) minmax(280px, 0.75fr);
            gap: 1.15rem;
            align-items: stretch;
        }

        .hero-topline {
            display: inline-flex;
            align-items: center;
            gap: 0.55rem;
            padding: 0.48rem 0.84rem;
            border-radius: 999px;
            background: rgba(255,255,255,0.08);
            color: #f4f9f5;
            font-size: 0.8rem;
            letter-spacing: 0.03em;
            font-weight: 800;
            text-transform: uppercase;
            margin-bottom: 1rem;
            border: 1px solid rgba(255,255,255,0.08);
        }

        .hero-title {
            font-size: 3.2rem;
            line-height: 0.96;
            font-weight: 800;
            max-width: 700px;
            margin-bottom: 0.95rem;
            color: #f6fbf7;
        }

        .hero-copy {
            max-width: 760px;
            color: rgba(230, 241, 232, 0.86);
            font-size: 1rem;
            line-height: 1.8;
            margin-bottom: 1.4rem;
        }

        .hero-chip-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.7rem;
            margin-bottom: 1.15rem;
        }

        .hero-chip {
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            padding: 0.72rem 0.92rem;
            border-radius: 999px;
            border: 1px solid rgba(255,255,255,0.08);
            background: rgba(255,255,255,0.08);
            color: #eff7f1;
            font-size: 0.86rem;
            font-weight: 700;
            box-shadow: var(--shadow-soft);
            transition: transform 180ms ease, background 180ms ease, border-color 180ms ease;
        }

        .hero-chip:hover {
            transform: translateY(-2px);
            background: rgba(255,255,255,0.14);
            border-color: rgba(255,255,255,0.16);
        }

        .hero-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.9rem;
        }

        .hero-stat {
            background: rgba(255,255,255,0.08);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 20px;
            padding: 1rem 1rem 0.95rem;
            box-shadow: var(--shadow-soft);
            transition: transform 180ms ease, border-color 180ms ease;
        }

        .hero-stat:hover {
            transform: translateY(-3px);
            border-color: rgba(255,255,255,0.16);
        }

        .hero-stat-label {
            color: rgba(228, 240, 230, 0.68);
            font-size: 0.82rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 0.35rem;
        }

        .hero-stat-value {
            color: #f4faf5;
            font-family: "Sora", sans-serif;
            font-size: 1.08rem;
            line-height: 1.35;
            font-weight: 700;
        }

        .hero-spotlight {
            background:
                linear-gradient(180deg, rgba(244, 249, 244, 0.92), rgba(231, 242, 233, 0.84));
            color: rgba(245, 251, 246, 0.96);
            border-radius: 26px;
            padding: 1.2rem 1.15rem;
            box-shadow: 0 24px 60px rgba(0, 0, 0, 0.16);
            position: relative;
            overflow: hidden;
            border: 1px solid rgba(255,255,255,0.18);
        }

        .hero-spotlight::after {
            content: "";
            position: absolute;
            inset: auto -40px -60px auto;
            width: 180px;
            height: 180px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(199,146,61,0.20), transparent 70%);
        }

        .spotlight-kicker {
            font-size: 0.76rem;
            letter-spacing: 0.09em;
            text-transform: uppercase;
            color: #6a7c72;
            margin-bottom: 0.55rem;
            font-weight: 800;
        }

        .spotlight-title {
            font-family: "Sora", sans-serif;
            font-size: 1.2rem;
            line-height: 1.2;
            margin-bottom: 0.7rem;
            font-weight: 700;
            color: #173424;
        }

        .spotlight-copy {
            color: #51675c;
            font-size: 0.93rem;
            line-height: 1.7;
            margin-bottom: 1rem;
        }

        .spotlight-stack {
            display: grid;
            gap: 0.7rem;
        }

        .spotlight-item {
            padding: 0.82rem 0.9rem;
            border-radius: 18px;
            background: rgba(255,255,255,0.58);
            border: 1px solid rgba(22, 58, 42, 0.08);
        }

        .spotlight-item-label {
            color: #688173;
            font-size: 0.74rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 0.25rem;
            font-weight: 700;
        }

        .spotlight-item-value {
            font-size: 0.95rem;
            line-height: 1.5;
            font-weight: 600;
            color: #173424;
        }

        .section-card {
            background: var(--panel);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 26px;
            padding: 1.25rem 1.3rem;
            box-shadow: var(--shadow-soft);
            backdrop-filter: blur(10px);
            margin-bottom: 1rem;
            transition: transform 180ms ease, box-shadow 180ms ease, border-color 180ms ease;
        }

        .section-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 22px 52px rgba(0, 0, 0, 0.18);
            border-color: rgba(255,255,255,0.14);
        }

        .section-kicker {
            color: var(--gold);
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-weight: 700;
            margin-bottom: 0.45rem;
        }

        .section-title {
            font-family: "Sora", sans-serif;
            font-size: 1.3rem;
            font-weight: 700;
            color: var(--ink);
            margin-bottom: 0.32rem;
        }

        .section-copy {
            color: var(--muted);
            font-size: 0.95rem;
            line-height: 1.65;
        }

        .metric-card {
            background: rgba(255,255,255,0.84);
            border: 1px solid rgba(22, 58, 42, 0.08);
            border-radius: 22px;
            padding: 1rem 1.05rem 0.95rem;
            box-shadow: var(--shadow-soft);
            transition: transform 180ms ease, border-color 180ms ease, box-shadow 180ms ease;
            min-height: 138px;
        }

        .metric-card:hover {
            transform: translateY(-3px);
            border-color: rgba(29, 81, 56, 0.16);
            box-shadow: 0 18px 44px rgba(23, 40, 31, 0.10);
        }

        .metric-label {
            color: #6e7f77;
            font-size: 0.8rem;
            font-weight: 800;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            margin-bottom: 0.55rem;
        }

        .metric-value {
            color: #163726;
            font-family: "Sora", sans-serif;
            font-size: 2.25rem;
            line-height: 1.08;
            font-weight: 700;
            letter-spacing: -0.03em;
            word-break: break-word;
        }

        .metric-value.is-small {
            font-size: 2.1rem;
        }

        .stFileUploader > div {
            border-radius: 22px;
            border: 1.5px dashed rgba(255,255,255,0.18);
            background: rgba(255,255,255,0.07);
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.5);
            transition: border-color 180ms ease, box-shadow 180ms ease, transform 180ms ease;
        }

        .stFileUploader > div:hover {
            border-color: rgba(255,255,255,0.28);
            box-shadow: 0 16px 36px rgba(0, 0, 0, 0.16);
            transform: translateY(-1px);
        }

        .stButton > button {
            background: linear-gradient(135deg, #d5a04c, #b8792d);
            color: white;
            border: none;
            border-radius: 999px;
            padding: 0.82rem 1.2rem;
            font-weight: 800;
            letter-spacing: 0.01em;
            box-shadow: 0 14px 28px rgba(0, 0, 0, 0.20);
        }

        .stButton > button:hover {
            background: linear-gradient(135deg, #c99648, #aa6f2b);
            color: white;
        }

        .stTextInput > div > div > input {
            border-radius: 18px;
            border: 1px solid rgba(41, 84, 61, 0.18);
            background: rgba(255,255,255,0.90);
            padding: 0.78rem 0.9rem;
            color: #153325 !important;
            transition: border-color 180ms ease, box-shadow 180ms ease;
        }

        .stTextInput > div > div > input:focus {
            border-color: rgba(41, 84, 61, 0.34);
            box-shadow: 0 0 0 4px rgba(42, 103, 70, 0.10);
        }

        .stTextInput > div > div > input::placeholder {
            color: #809086 !important;
            opacity: 1 !important;
        }

        .stRadio > div {
            background: rgba(255,255,255,0.08);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 20px;
            padding: 0.6rem 0.7rem;
            box-shadow: var(--shadow-soft);
        }

        .stProgress > div > div > div > div {
            background: linear-gradient(90deg, #c4882f, #2e7149);
        }

        hr {
            border-color: rgba(29, 81, 56, 0.10);
        }

        @media (max-width: 900px) {
            .hero-title {
                font-size: 2.25rem;
            }

            .hero-layout {
                grid-template-columns: 1fr;
            }

            .hero-grid {
                grid-template-columns: 1fr;
            }
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
        <div class="hero-shell">
            <div class="hero-layout">
                <div>
                    <div class="hero-topline">{APP_ICON} Intelligent Crop Diagnostics</div>
                    <div class="hero-title">{APP_TITLE}</div>
                    <div class="hero-copy">
                        A more premium crop-health interface for fast pest screening. Upload a field image,
                        verify model confidence, scan management guidance, and continue with AI-assisted next-step recommendations
                        through a cleaner, startup-style workflow.
                    </div>
                    <div class="hero-chip-row">
                        <div class="hero-chip">Top-1 pest classification</div>
                        <div class="hero-chip">Actionable advisory blocks</div>
                        <div class="hero-chip">Fast, local, and cloud support</div>
                    </div>
                    <div class="hero-grid">
                        <div class="hero-stat">
                            <div class="hero-stat-label">Model Type</div>
                            <div class="hero-stat-value">YOLOv8 Classification</div>
                        </div>
                        <div class="hero-stat">
                            <div class="hero-stat-label">Assistant Modes</div>
                            <div class="hero-stat-value">Fast, Local, Cloud</div>
                        </div>
                        <div class="hero-stat">
                            <div class="hero-stat-label">Decision Output</div>
                            <div class="hero-stat-value">Prediction, Confidence, Guidance</div>
                        </div>
                    </div>
                </div>
                <div class="hero-spotlight">
                    <div class="spotlight-kicker">Platform Focus</div>
                    <div class="spotlight-title">Built for practical field-response decisions</div>
                    <div class="spotlight-copy">
                        This layout is optimized for quick review: visual evidence first, advisory second, assistant follow-up third.
                    </div>
                    <div class="spotlight-stack">
                        <div class="spotlight-item">
                            <div class="spotlight-item-label">Best input</div>
                            <div class="spotlight-item-value">One clear crop image with visible pest presence or damage pattern.</div>
                        </div>
                        <div class="spotlight-item">
                            <div class="spotlight-item-label">Best use</div>
                            <div class="spotlight-item-value">Rapid screening before pesticide selection and prevention planning.</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_intro_band():
    left_col, right_col = st.columns([1.2, 0.8], gap="large")
    with left_col:
        st.markdown(
            """
            <div class="section-card">
                <div class="section-kicker">Workflow</div>
                <div class="section-title">Designed for fast operator flow</div>
                <div class="section-copy">
                    Start with the image, move into model-backed prediction, then validate with treatment guidance
                    and assistant support. The interface is intentionally structured like a compact decision product,
                    not a generic demo screen.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with right_col:
        st.markdown(
            """
            <div class="section-card">
                <div class="section-kicker">Positioning</div>
                <div class="section-title">Research prototype with deployable polish</div>
                <div class="section-copy">
                    The current UI keeps the deep-learning workflow approachable while feeling polished enough for showcase,
                    pilot demos, and project presentation.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def main():
    inject_styles()
    render_header()
    render_intro_band()

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
    render_recommendation(pest_details)

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
