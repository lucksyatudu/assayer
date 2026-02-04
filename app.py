import streamlit as st

from src.pipelines.claim_pipeline import run_claim_pipeline

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Assayer - Claim Validator",
    page_icon="🧾",
    layout="wide",
)

# -----------------------------
# Header
# -----------------------------
st.title("🧾 Assayer - Claim Validator")
st.subheader("Paste text and extract verifiable claims")

st.markdown(
    """
    This tool identifies **claims** in a given text and (later) finds
    **relevant sources from the web** to support or refute them.
    """
)

st.divider()

# -----------------------------
# Input section
# -----------------------------
st.markdown("### 📥 Input Text")

text_input = st.text_area(
    label="Paste your text here",
    height=280,
    placeholder=(
        "Example:\n"
        "India became the world's most populous country in 2023. "
        "The GDP growth rate exceeded 7% that year."
    ),
)

# -----------------------------
# Controls
# -----------------------------
col1, col2 = st.columns([1, 4])

with col1:
    analyze_btn = st.button(
        "🔍 Analyze Claims",
        type="primary",
        use_container_width=True,
    )

with col2:
    st.caption("Analysis will extract factual, checkable claims.")

# -----------------------------
# Validation feedback
# -----------------------------
if analyze_btn:
    if not text_input.strip():
        st.warning("Please enter some text to analyze.")
    elif len(text_input.strip()) < 20:
        st.warning("Text is too short to contain meaningful claims.")
    else:
        claims = run_claim_pipeline(text_input)
        for claim in claims:
            st.write(f"🔹 {claim.original_sentence}")

# -----------------------------
# Footer
# -----------------------------
st.divider()
st.caption("⚙️ Version 0.1")
