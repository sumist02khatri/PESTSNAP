import streamlit as st


def render_recommendation(details):
    st.markdown(
        """
        <div class="section-card">
            <div class="section-kicker">Management Guide</div>
            <div class="section-title">Recommended action snapshot</div>
            <div class="section-copy">
                Review the likely field impact, a treatment direction, and prevention guidance tied to the predicted pest.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        st.markdown(
            f"""
            <div class="section-card">
                <div class="section-kicker">Problem</div>
                <div class="section-title">Field impact</div>
                <div class="section-copy">{details["problem"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class="section-card">
                <div class="section-kicker">Cure</div>
                <div class="section-title">Treatment direction</div>
                <div class="section-copy">{details["cure"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
            <div class="section-card">
                <div class="section-kicker">Prevention</div>
                <div class="section-title">Next-season protection</div>
                <div class="section-copy">{details["prevention"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
