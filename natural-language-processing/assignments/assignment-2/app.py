"""Streamlit web app for Customer Review Summarization (Task 4).

Run:  streamlit run app.py
"""

from __future__ import annotations

import os

import pandas as pd
import streamlit as st

from config import MAX_REVIEWS_DEFAULT, SAMPLE_CSV, TOP_K_ASPECTS
from data_prep import split_reviews
from summarizer_service import (analyse, load_sample_reviews,
                                reviews_from_file)

st.set_page_config(page_title="Customer Review Summarizer",
                   page_icon="📝", layout="wide")

# ---------------------------------------------------------------------
# Model loading - cached so it is read from disk only once per session.
# ---------------------------------------------------------------------

@st.cache_resource(show_spinner="Loading the summarization model...")
def get_model():
    from summarizer_service import get_model as _get
    return _get("t5")


# ---------------------------------------------------------------------
# Input helpers
# ---------------------------------------------------------------------

def reviews_from_upload(upload) -> list[str]:
    """Pull a list of reviews out of an uploaded .txt or .csv file."""
    # getvalue() rather than read() - Streamlit re-runs the whole script on
    # every click, and read() would return empty the second time around.
    return reviews_from_file(upload.name, upload.getvalue())


# ---------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------

# Opening the app as  ?demo=1  loads the sample product and summarises it
# straight away - handy for demonstrating without any clicking.
auto_demo = st.query_params.get("demo") == "1"

st.sidebar.header("Settings")
num_beams = st.sidebar.slider("Beam search width", 1, 6, 4,
                              help="Higher = better wording, slower.")
max_new_tokens = st.sidebar.slider("Max summary length (tokens)", 8, 64, 32)
top_k = st.sidebar.slider("Aspects to show", 3, 15, TOP_K_ASPECTS)
max_reviews = st.sidebar.slider("Max reviews to process", 5, 200,
                                MAX_REVIEWS_DEFAULT,
                                help="Keeps the demo responsive on CPU.")

st.sidebar.divider()
model = get_model()
if model.is_finetuned:
    st.sidebar.success("Using the fine-tuned t5-small model.")
else:
    st.sidebar.warning("No fine-tuned model found - falling back to plain "
                       "t5-small. Run `python train.py` first.")
st.sidebar.caption(f"Model source: `{model.source}`")


# ---------------------------------------------------------------------
# Main page
# ---------------------------------------------------------------------

st.title("📝 Customer Review Summarization")
st.write("Paste or upload many reviews for one product. The app writes a short "
         "summary for each, then reports the aspects customers praise and "
         "complain about most.")

tab_paste, tab_upload, tab_demo = st.tabs(
    ["Paste text", "Upload a file", "Try the sample product"])

reviews: list[str] = []

with tab_paste:
    text = st.text_area("One review per line, or separate them with a blank line.",
                        height=220, placeholder="The coffee tastes great but the "
                                                "box arrived crushed.\nGreat value "
                                                "for the price, will buy again.")
    if text.strip():
        reviews = split_reviews(text)

with tab_upload:
    upload = st.file_uploader("Upload a .txt or .csv file", type=["txt", "csv"])
    if upload is not None:
        reviews = reviews_from_upload(upload)
        st.caption(f"Read {len(reviews)} reviews from `{upload.name}`.")

with tab_demo:
    if os.path.exists(SAMPLE_CSV):
        st.caption("A real product from the Amazon Fine Food Reviews dataset.")
        if st.checkbox("Use the sample reviews", value=auto_demo):
            reviews = load_sample_reviews()
            st.caption(f"Loaded {len(reviews)} sample reviews.")
    else:
        st.info("`data/sample_reviews.csv` not found. Run `python train.py` "
                "to build the data files.")

st.divider()

if st.button("Summarize reviews", type="primary", disabled=not reviews) or (auto_demo and reviews):

    with st.spinner(f"Summarizing {len(reviews)} reviews..."):
        result = analyse(reviews, max_reviews=max_reviews, top_k=top_k,
                         num_beams=num_beams, max_new_tokens=max_new_tokens)
        summaries, report = result["summaries"], result["report"]
        overall, reviews = result["overall"], result["reviews"]

    st.subheader("Overall summary")
    st.success(overall)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Reviews", report.n_reviews)
    c2.metric("Positive", report.n_positive)
    c3.metric("Negative", report.n_negative)
    c4.metric("Positive share", f"{report.positive_share:.0%}")

    st.subheader("What customers talk about most")
    left, right = st.columns(2)

    with left:
        st.markdown("**👍 Praised aspects**")
        if report.positive_aspects:
            df = pd.DataFrame(report.positive_aspects,
                              columns=["aspect", "mentions"]).set_index("aspect")
            st.bar_chart(df, horizontal=True, color="#2e9e5b")
        else:
            st.caption("No clear positive aspects found.")

    with right:
        st.markdown("**👎 Criticised aspects**")
        if report.negative_aspects:
            df = pd.DataFrame(report.negative_aspects,
                              columns=["aspect", "mentions"]).set_index("aspect")
            st.bar_chart(df, horizontal=True, color="#d1495b")
        else:
            st.caption("No clear negative aspects found.")

    st.subheader("Per-review summaries")
    table = pd.DataFrame({
        "Review": [r[:200] + ("..." if len(r) > 200 else "") for r in reviews],
        "Generated summary": summaries,
    })
    st.dataframe(table, use_container_width=True, hide_index=True)
    st.download_button("Download summaries as CSV",
                       table.to_csv(index=False).encode("utf-8"),
                       "review_summaries.csv", "text/csv")

elif not reviews:
    st.info("Add some reviews above to enable the button.")
