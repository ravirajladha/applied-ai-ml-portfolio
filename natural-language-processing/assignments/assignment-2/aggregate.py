"""Task 3.2 - map-reduce aggregation over many reviews.

Owner: Member 3 (Deep Learning Engineer - Transformer).

The model summarises ONE review at a time, but the problem statement asks
for a summary of MANY. That is a classic map-reduce:

    MAP     summarise each review on its own          -> N short summaries
    REDUCE  summarise those summaries together        -> 1 overall summary

Doing it this way, rather than concatenating every review and feeding the
lot to the encoder, matters because the encoder only reads 256 tokens.
Fifty reviews are far longer than that, so a direct pass would silently
throw most of them away. Summarising twice keeps every review represented.
"""

from __future__ import annotations

from collections import Counter

from aspects import AspectReport
from config import MAX_TARGET_TOKENS


def map_summaries(summarizer, reviews: list[str], **kw) -> list[str]:
    """MAP step - one short summary per review."""
    return summarizer.summarize(reviews, **kw)


def reduce_summaries(summarizer, summaries: list[str],
                     max_new_tokens: int = MAX_TARGET_TOKENS * 2) -> str:
    """REDUCE step - one abstractive summary of all the summaries.

    The per-review summaries are joined into a single pseudo-document and
    passed back through the same encoder-decoder.
    """
    kept = [s.strip() for s in summaries if s and s.strip()]
    if not kept:
        return ""
    if len(kept) == 1:
        return kept[0]

    joined = ". ".join(kept)
    out = summarizer.summarize([joined], max_new_tokens=max_new_tokens)
    return out[0] if out else ""


def build_overall_summary(summaries: list[str], report: AspectReport,
                          model_verdict: str = "") -> str:
    """One human-readable paragraph describing the whole review set.

    Combines three signals: how many people were happy, what they praised
    and criticised, and (optionally) the model's own reduce-step verdict.
    """
    if not summaries:
        return "No reviews to summarise."

    share = report.polarity_share
    if share >= 0.65:
        mood = "Most customers are happy with this product"
    elif share >= 0.35:
        mood = "Customer opinion is mixed"
    else:
        mood = "Most customers are unhappy with this product"

    lines = [
        f"{mood} ({report.n_positive} positive, {report.n_negative} negative, "
        f"{report.n_neutral} neutral out of {report.n_reviews} reviews)."
    ]

    if report.positive_aspects:
        praised = ", ".join(a for a, _ in report.positive_aspects[:5])
        lines.append(f"Most praised: {praised}.")
    if report.negative_aspects:
        griped = ", ".join(a for a, _ in report.negative_aspects[:5])
        lines.append(f"Most criticised: {griped}.")

    if model_verdict:
        lines.append(f'Model\'s overall take: "{model_verdict}".')
    else:
        # Fall back to the most repeated headline.
        common = Counter(s.lower() for s in summaries if s).most_common(1)
        if common:
            lines.append(f'Typical review headline: "{common[0][0]}".')

    return " ".join(lines)


def summarize_product(summarizer, reviews: list[str], top_k: int = 8,
                      use_reduce: bool = True, **kw) -> dict:
    """Full pipeline for one product: map, reduce, aspects, verdict."""
    from aspects import analyse_aspects

    summaries = map_summaries(summarizer, reviews, **kw)
    report = analyse_aspects(reviews, top_k=top_k)
    verdict = reduce_summaries(summarizer, summaries) if use_reduce else ""

    return {
        "summaries": summaries,
        "report": report,
        "model_verdict": verdict,
        "overall": build_overall_summary(summaries, report, verdict),
    }
