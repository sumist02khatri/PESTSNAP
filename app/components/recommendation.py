import streamlit as st


def render_recommendation(details):
    st.subheader("Recommendation")
    col1, col2, col3 = st.columns(3, gap="medium")
    col1.info(f"Problem\n\n{details['problem']}")
    col2.success(f"Cure\n\n{details['cure']}")
    col3.warning(f"Prevention\n\n{details['prevention']}")
