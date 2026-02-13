import asyncio
import streamlit as st

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
st.subheader("Paste text and validate verifiable claims")

st.markdown(
    """
    This tool identifies **verifiable claims** and evaluates them using  
    a hybrid approach: web evidence + LLM reasoning.
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
    st.caption("Hybrid validation using web evidence + Gemini")

st.divider()


# -----------------------------
# Helper: Score Styling
# -----------------------------
def score_badge(score: str) -> str:
    color_map = {
        "Accurate": "#2E7D32",
        "Inaccurate": "#C62828",
        "Disputed": "#EF6C00",
        "Unsupported": "#616161",
        "Cannot Confidently Assess": "#1565C0",
    }

    color = color_map.get(score, "#616161")

    return f"""
    <span style="
        background-color:{color};
        color:white;
        padding:4px 10px;
        border-radius:12px;
        font-size:0.85rem;
        font-weight:600;">
        {score}
    </span>
    """


# -----------------------------
# Results Rendering
# -----------------------------
if analyze_btn:
    if not text_input.strip():
        st.warning("Please enter some text to analyze.")
    elif len(text_input.strip()) < 20:
        st.warning("Text is too short to contain meaningful claims.")
    else:
        with st.spinner("Analyzing and validating claims..."):
            try:
                # Import lazily to avoid startup crashes
                from src.pipelines.claim_pipeline import run_claim_pipeline

                # Run async pipeline safely
                results = asyncio.run(run_claim_pipeline(text_input))

            except RuntimeError:
                # Handles "event loop already running"
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                results = loop.run_until_complete(
                    run_claim_pipeline(text_input)
                )

            except Exception as e:
                st.error(f"Error during processing: {e}")
                st.stop()

        if not results:
            st.info("No strong verifiable claims found.")
        else:
            st.markdown("## 🧾 Validation Results")

            for idx, result in enumerate(results, 1):
                with st.container():
                    st.markdown(f"### 🔹 Claim {idx}")
                    st.write(result.claim.original_sentence)

                    # Score badge
                    st.markdown(score_badge(result.score), unsafe_allow_html=True)

                    # Source
                    if result.source:
                        st.markdown(f"**Source:** [{result.source}]({result.source})")

                    # Evidence snippet
                    if result.evidence_snippet:
                        st.markdown("**Relevant Evidence:**")
                        st.info(result.evidence_snippet)

                    st.divider()


# -----------------------------
# Footer
# -----------------------------
st.divider()
st.caption("⚙️ Assayer v0.2 | Hybrid Claim Validation")
