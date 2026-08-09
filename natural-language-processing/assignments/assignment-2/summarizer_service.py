"""Task 4 - the service layer shared by every front end.

Owner: Member 4 (Application & DevOps Engineer).

Streamlit, Flask and the notebook all call this, so they cannot drift
apart. The model is loaded once and reused - loading t5-small takes a few
seconds, which would be unbearable on every request.
"""

from __future__ import annotations

import os

from aggregate import summarize_product
from config import MAX_REVIEWS_DEFAULT, SAMPLE_CSV, TOP_K_ASPECTS
from data_prep import split_reviews

_MODEL = None


def get_model(kind: str = "t5"):
    """Load the summarizer once and keep it.

    kind="t5"   the fine-tuned Transformer (default)
    kind="lstm" the Seq2Seq baseline, if it has been trained
    """
    global _MODEL
    if _MODEL is None or getattr(_MODEL, "_kind", None) != kind:
        if kind == "lstm":
            from infer_lstm import LSTMSummarizer
            _MODEL = LSTMSummarizer()
        else:
            from model_t5 import ReviewSummarizer
            _MODEL = ReviewSummarizer()
        _MODEL._kind = kind
    return _MODEL


def load_sample_reviews() -> list[str]:
    """The bundled product used by the demo."""
    if not os.path.exists(SAMPLE_CSV):
        return []
    import pandas as pd
    return [str(v) for v in pd.read_csv(SAMPLE_CSV)["Text"].dropna()]


def reviews_from_file(name: str, raw: bytes) -> list[str]:
    """Pull reviews out of an uploaded .txt or .csv file."""
    if name.lower().endswith(".csv"):
        import io

        import pandas as pd
        df = pd.read_csv(io.BytesIO(raw))
        for col in ["Text", "text", "review", "Review", "document", "body"]:
            if col in df.columns:
                return [str(v) for v in df[col].dropna()]
        return [str(v) for v in df.iloc[:, -1].dropna()]

    return split_reviews(raw.decode("utf-8", errors="ignore"))


def analyse(reviews: list[str], kind: str = "t5",
            max_reviews: int = MAX_REVIEWS_DEFAULT,
            top_k: int = TOP_K_ASPECTS, **kw) -> dict:
    """Run the whole pipeline over a set of reviews.

    Returns per-review summaries, the aspect report, the model's own
    overall verdict, and a readable paragraph combining them.
    """
    reviews = [r for r in reviews if r and str(r).strip()][:max_reviews]
    if not reviews:
        return {"error": "No usable reviews were given."}

    model = get_model(kind)
    result = summarize_product(model, reviews, top_k=top_k, **kw)
    result["reviews"] = reviews
    result["model_source"] = model.source
    result["is_finetuned"] = getattr(model, "is_finetuned", False)
    return result


def to_plain_dict(result: dict) -> dict:
    """Flatten the result so it can be returned as JSON."""
    if "error" in result:
        return result
    rep = result["report"]
    return {
        "n_reviews": rep.n_reviews,
        "sentiment": {"positive": rep.n_positive,
                      "negative": rep.n_negative,
                      "neutral": rep.n_neutral,
                      "positive_share": round(rep.positive_share, 3)},
        "praised_aspects": [{"aspect": a, "mentions": c}
                            for a, c in rep.positive_aspects],
        "criticised_aspects": [{"aspect": a, "mentions": c}
                               for a, c in rep.negative_aspects],
        "overall_summary": result["overall"],
        "model_verdict": result["model_verdict"],
        "summaries": [{"review": r[:300], "summary": s}
                      for r, s in zip(result["reviews"], result["summaries"])],
        "model_source": result["model_source"],
    }
