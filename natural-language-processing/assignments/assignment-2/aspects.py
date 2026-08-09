"""Task 3.3 - aspect mining.

Owner: Member 3 (Deep Learning Engineer - Transformer).

Answers the half of the problem statement a per-review summarizer cannot:
across ALL the reviews, which topics are praised and which are criticised?

Method: split into sentences, score each with VADER, then rank phrases by
how *distinctive* they are to one side. Ranking by raw frequency fails -
for a cat toy, "cat" and "toy" top both lists, which tells a buyer nothing.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from functools import lru_cache

from config import (ASPECT_SKEW, MIN_ASPECT_MENTIONS, NEG_REVIEW_THRESHOLD,
                    NEG_SENTENCE_THRESHOLD, POS_REVIEW_THRESHOLD,
                    POS_SENTENCE_THRESHOLD, TOP_K_ASPECTS)
from data_prep import clean_text, split_sentences


# Sentiment words describe the opinion, not the aspect, so they are noise
# when we ask "which feature is being discussed?".
_OPINION_WORDS = {
    # verdict words - they carry the opinion, not the topic
    "good", "great", "bad", "nice", "best", "worst", "awesome", "terrible",
    "awful", "excellent", "poor", "amazing", "wonderful", "fantastic",
    "perfect", "decent", "ok", "okay", "fine", "favorite", "favourite",
    "happy", "disappointed", "disappointing", "disappointment", "recommend",
    "love", "loves", "loved", "loving", "like", "likes", "liked",
    "hate", "hates", "hated", "enjoy", "enjoys", "enjoyed",
    # transaction filler - true of every review, so never a useful aspect
    "product", "item", "thing", "things", "buy", "buying", "bought",
    "purchase", "purchased", "order", "ordered", "amazon", "star", "stars",
    "review", "reviews",
    # generic verbs and intensifiers
    "would", "will", "get", "gets", "got", "one", "use", "uses", "used",
    "make", "makes", "made", "much", "very", "also", "even", "really",
    "just", "think", "thought", "know", "say", "said", "want", "wanted",
    "try", "tried", "going", "goes", "come", "comes", "back", "still",
    "way", "little", "lot", "bit", "pretty", "quite", "definitely",
    "absolutely", "highly", "super", "ve", "don", "doesn", "didn", "isn",
    "wasn", "couldn", "won", "does", "did", "doing", "done", "give",
    "gives", "gave", "seems", "seem", "looks", "look", "need", "needs",
}

_POS_FALLBACK = {"good", "great", "love", "excellent", "perfect", "best",
                 "nice", "happy", "delicious", "fast", "works", "recommend"}
_NEG_FALLBACK = {"bad", "poor", "terrible", "awful", "worst", "broken",
                 "waste", "disappointed", "slow", "expensive", "returned"}


@lru_cache(maxsize=1)
def _sentiment_scorer():
    """Return a function text -> score in [-1, 1].

    Cached: the app calls this on every click, and rebuilding VADER re-reads
    its whole lexicon from disk each time.

    Uses NLTK's VADER when available (downloading the lexicon once), and a
    small word-list otherwise so the app never hard-fails offline.
    """
    try:
        import nltk
        from nltk.sentiment.vader import SentimentIntensityAnalyzer
        try:
            nltk.data.find("sentiment/vader_lexicon.zip")
        except LookupError:
            nltk.download("vader_lexicon", quiet=True)
        vader = SentimentIntensityAnalyzer()
        return lambda t: vader.polarity_scores(t)["compound"]
    except Exception:
        def simple(t: str) -> float:
            words = set(re.findall(r"[a-z']+", t.lower()))
            pos = len(words & _POS_FALLBACK)
            neg = len(words & _NEG_FALLBACK)
            if pos == neg:
                return 0.0
            return (pos - neg) / max(pos + neg, 1)
        return simple


def _singular(term: str) -> str:
    """Crude plural key so 'cat' and 'cats' are treated as one aspect."""
    return " ".join(w[:-1] if len(w) > 3 and w.endswith("s") and
                    not w.endswith("ss") else w
                    for w in term.split())


def _rank(candidates: list[tuple[str, int]], top_k: int) -> list[tuple[str, int]]:
    """Drop redundant wordings, then take the most-mentioned survivors."""
    counted = dict(candidates)

    # Best count of any 2-word phrase containing a given single word.
    in_phrase: dict[str, int] = {}
    for term, c in counted.items():
        if " " in term:
            for word in term.split():
                in_phrase[word] = max(in_phrase.get(word, 0), c)

    # Keep a single word only when it beats every phrase it sits inside,
    # so "battery life" wins but a standalone "flavor" survives.
    kept = [(t, c) for t, c in counted.items()
            if " " in t or in_phrase.get(t, 0) < c]

    # Collapse singular/plural duplicates, keeping the commoner spelling.
    best: dict[str, tuple[str, int]] = {}
    for term, c in kept:
        key = _singular(term)
        if key not in best or c > best[key][1]:
            best[key] = (term, c)

    out = sorted(best.values(), key=lambda x: (-x[1], x[0]))
    return out[:top_k]


def _contrastive_terms(pos_sents: list[str], neg_sents: list[str],
                       top_k: int, min_count: int = MIN_ASPECT_MENTIONS, skew: float = ASPECT_SKEW):
    """Find the aspects that are *distinctive* to each side.

    Ranking purely by frequency fails: for a cat toy, "cat" and "toy" top
    both lists, so praise and criticism look identical. Instead a term is
    only listed on a side if it is disproportionately common there.

    `min_count` drops one-off noise; `skew` is the share of a term's usage
    that must fall on a side (0.6 = mentioned 1.5x more often there).
    """
    from sklearn.feature_extraction.text import (ENGLISH_STOP_WORDS,
                                                 CountVectorizer)

    docs = pos_sents + neg_sents
    if not docs:
        return [], []

    stop = list(ENGLISH_STOP_WORDS | _OPINION_WORDS)
    try:
        vec = CountVectorizer(
            ngram_range=(1, 2), stop_words=stop, min_df=1,
            # Must start with a letter, so "25" and "3rd" are ignored.
            token_pattern=r"(?u)\b[a-z][a-z-]+\b",
        )
        matrix = vec.fit_transform(docs)
    except ValueError:      # every word was a stop word
        return [], []

    terms = vec.get_feature_names_out()
    split = len(pos_sents)
    pos_counts = matrix[:split].sum(axis=0).A1
    neg_counts = matrix[split:].sum(axis=0).A1

    # Rates, not raw counts - the two piles are rarely the same size.
    pos_total = max(pos_counts.sum(), 1)
    neg_total = max(neg_counts.sum(), 1)

    def pick(mine, theirs, my_total, their_total):
        out = []
        for term, m, t in zip(terms, mine, theirs):
            if m < min_count:
                continue
            my_rate = m / my_total
            their_rate = t / their_total
            if my_rate / (my_rate + their_rate + 1e-12) >= skew:
                out.append((term, int(m)))
        return _rank(out, top_k)

    return (pick(pos_counts, neg_counts, pos_total, neg_total),
            pick(neg_counts, pos_counts, neg_total, pos_total))


@dataclass
class AspectReport:
    """What the aggregate analysis found across all reviews."""
    n_reviews: int = 0
    positive_aspects: list = field(default_factory=list)
    negative_aspects: list = field(default_factory=list)
    n_positive: int = 0
    n_negative: int = 0
    n_neutral: int = 0

    @property
    def positive_share(self) -> float:
        """Positive reviews as a share of ALL reviews - shown as a metric."""
        total = self.n_positive + self.n_negative + self.n_neutral
        return self.n_positive / total if total else 0.0

    @property
    def polarity_share(self) -> float:
        """Positive as a share of reviews that took a side at all.

        The verdict must use this, not positive_share. With 3 positive,
        3 negative and 2 neutral reviews, positive_share is 0.375, which
        would wrongly read as "mostly unhappy" - the neutrals drag it down.
        Ignoring them gives 0.5, which is correctly "mixed".
        """
        decided = self.n_positive + self.n_negative
        return self.n_positive / decided if decided else 0.5


def analyse_aspects(reviews: list[str], top_k: int = TOP_K_ASPECTS) -> AspectReport:
    """Split reviews into sentences, judge each one's sentiment, then count
    which topics show up most often on the positive and negative sides."""
    score = _sentiment_scorer()
    report = AspectReport(n_reviews=len(reviews))

    pos_sents: list[str] = []
    neg_sents: list[str] = []

    for review in reviews:
        cleaned = clean_text(review)
        if not cleaned:
            continue

        # Overall verdict for this review, used for the share bar.
        overall = score(cleaned)
        if overall >= POS_REVIEW_THRESHOLD:
            report.n_positive += 1
        elif overall <= NEG_REVIEW_THRESHOLD:
            report.n_negative += 1
        else:
            report.n_neutral += 1

        # Sentence level, used for the aspect lists.
        for sent in split_sentences(cleaned) or [cleaned]:
            s = score(sent)
            if s >= POS_SENTENCE_THRESHOLD:
                pos_sents.append(sent)
            elif s <= NEG_SENTENCE_THRESHOLD:
                neg_sents.append(sent)

    report.positive_aspects, report.negative_aspects = _contrastive_terms(
        pos_sents, neg_sents, top_k)
    return report
