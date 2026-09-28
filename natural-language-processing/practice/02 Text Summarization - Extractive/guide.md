# Extractive text summarization — build guide

**Topic 02 · Natural Language Processing · practice**

| File | What it is |
|------|------------|
| `explainer.html` | **Open this first.** The interactive lesson — a live tf-idf table, a cosine-similarity explorer, TextRank converging round by round, ROUGE computed in front of you, and a self-check quiz. |
| `practice.ipynb` | The template notebook. Boilerplate is filled in; 22 `# TODO` lines are left for you. |
| `guide.md` | This file — the plan, the recap, and the checklist. |

---

## The problem statement

Given a news article, return the **three sentences that best summarize it** — chosen by the computer, not by you.
Then prove with a number that your method beats doing nothing clever.

You will build three summarizers and measure all three against a human-written summary:

1. **Lead-3** — take the first three sentences. No maths. The baseline you must beat.
2. **TF-IDF scoring** — score each sentence by how many *informative* words it contains.
3. **TextRank** — let the sentences vote for each other. PageRank, on sentences instead of web pages.

By the end you will have written, from scratch:

- a sentence splitter using regex lookarounds
- a tokenizer with stopword removal
- a document-term count matrix
- **tf**, **idf**, and **tf-idf**
- **cosine similarity**, all pairs in one matrix multiply
- **PageRank** by power iteration, including the dangling-node fix
- **ROUGE-1** precision / recall / F1, with clipping

---

## On dependencies — why this is numpy only

Nothing to install. Nothing to download. The whole notebook runs in under a second on the Anaconda install you
already have.

| Package | Needed? | Why |
|---|---|---|
| `numpy` | **yes** | already installed |
| `re`, `collections` | **yes** | standard library |
| `scikit-learn` | optional | already installed; used in cell 12 only, to cross-check your work |
| `nltk` | **no** | you are writing the tokenizer and splitter yourself — that is the point |
| `torch` / `transformers` | **no** | that is topic 03 |

The one thing you will *not* get here is fluency — extractive summaries do not flow, because they are stitched from
sentences written to sit somewhere else. Topic 03 fixes that, and costs about 0.7 GB of downloads to do it.

---

## Plain-English recap

Read this table before you start. Every fancy word you need, one line each.

| Term | In one line |
|------|-------------|
| **Extractive** | The summary is *copied* sentences from the source. Cannot invent a false fact. |
| **Abstractive** | The summary is *newly written*. Reads better, can be wrong. (Topic 03.) |
| **Token** | One word, after lowercasing and stripping punctuation. |
| **Stopword** | A word so common (`the`, `of`, `is`) it tells you nothing about which sentence is special. |
| **Vocabulary** | The sorted set of all distinct tokens in the document. |
| **Document-term matrix** | A grid: one row per sentence, one column per vocabulary word, each cell a count. |
| **tf** (term frequency) | How often a word appears in *this* sentence, divided by the sentence length. |
| **df** (document frequency) | In how many sentences does this word appear **at all**. 3 times in 1 sentence still means df = 1. |
| **idf** (inverse document frequency) | `log(N / df)`. High = rare = informative. A word in every sentence gets exactly 0. |
| **tf-idf** | `tf × idf`. Reads as *"frequent here, rare elsewhere"* — the definition of a word worth noticing. |
| **Cosine similarity** | The angle between two sentence vectors. 1 = same direction, 0 = no shared words. Ignores length on purpose. |
| **Dot product** | Multiply two vectors slot by slot, add it all up. Big when both are large in the *same* slots. |
| **Norm** | A vector's length. Dividing by it is what cancels out sentence length. |
| **TextRank** | PageRank on a graph of sentences, where edge weight = cosine similarity. |
| **Power iteration** | Just: apply the same update over and over until the numbers stop moving. |
| **Damping factor** | The `0.85` in PageRank. 15% of all score is redistributed equally each round so no clique can trap it. |
| **Dangling node** | A node with no outgoing edges. Its score leaks out of the system unless you handle it. Cell 8. |
| **MMR** | Maximal Marginal Relevance — pick sentences that are important *and* unlike what you already picked. |
| **ROUGE-1** | Count of overlapping single words between your summary and a human one. |
| **Clipping** | In ROUGE: you only get credit for as many copies of a word as the reference actually has. |
| **Precision / Recall / F1** | *Was what I wrote wanted* / *did I cover what was wanted* / the honest single number. |
| **Compression ratio** | Summary length ÷ original length. |

---

## The build plan, cell by cell

Each cell ends with `assert` checks. If they pass, move on. If they fail, the message tells you what broke.

| Cell | You write | Explainer section |
|------|-----------|------------------|
| 0 | *nothing* — setup and the article | 2 |
| 1 | `split_sentences` — regex with lookbehind + lookahead | 3 |
| 2 | `tokenize` — lowercase, strip punctuation, drop stopwords | 4 |
| 3 | `vocab` and the count matrix | 5 |
| 4 | `tf` — divide each row by its total | 5 |
| 5 | `df`, `idf`, `tf_idf` | 6 |
| 6 | `top_k_indices`, `tfidf_scores` → your first two summarizers | 7 |
| 7 | `cosine_similarity_matrix` — three lines | 8 |
| 8 | `textrank` — power iteration | 9 |
| 9 | *nothing* — read all three summaries and form an opinion | 10 |
| 10 | `rouge_1` — with clipping | 11 |
| 11 | *nothing* — the result, stated in words | — |
| 12 | *nothing* — cross-check against scikit-learn | — |
| 13 | `mmr` — optional, the redundancy fix | 10 |
| 14 | paste your own text and run the whole pipeline | — |

### Where people get stuck

- **Cell 1** — the regex is `r"(?<=[.!?])\s+(?=[A-Z])"`. Lookarounds *check* without *consuming*, which is what
  keeps the full stop attached to its sentence.
- **Cell 3** — `counts` is indexed `[sentence_number, vocab_index[word]]`. If the total-tokens assert fails, you are
  probably overwriting with `=` instead of adding with `+=`.
- **Cell 5** — df counts **non-zeros**, not sums. `(counts > 0).sum(axis=0)`, not `counts.sum(axis=0)`.
- **Cell 6** — `np.argsort` sorts *ascending*, so negate the scores to rank best-first. Then `sorted()` the chosen
  indices so the summary reads in document order.
- **Cell 8** — the `P.T` catches everyone. `P[j, i]` is the share flowing *from j to i*; to collect what arrives *at
  i* you need column `i`, which is row `i` of `P.T`. If your scores stop summing to 1, that is the bug.
- **Cell 10** — clipping. Walk your own tokens and *spend down* a budget taken from the reference's word counts.
  Without it, repeating one word inflates your score forever.

---

## What you should expect to see

Do not read this until you have run cell 10. It spoils the punchline.

<details>
<summary>The result (click to expand)</summary>

ROUGE-1 F1 comes out at roughly:

| method | F1 |
|---|---|
| lead-3 | 0.44 |
| tf-idf | **0.08** |
| textrank | **0.84** |

**TF-IDF loses badly — to the do-nothing baseline.** That is not a bug in your code, and it is the most useful
thing in this notebook. It happens because tf-idf scores each sentence *in isolation*, so it rewards unusual
vocabulary. It picked the three sentences whose words appear nowhere else in the article (cell 11 prints the
evidence: 9 of 9 tokens unique, 7 of 9, 6 of 8) and skipped the sentence saying who approved what.

TextRank asks a different question — *is this sentence connected to the rest of the article?* — and gets it right.

Also expect **s2 to be flagged as a dangling node**. It shares no words with any other sentence, so it has nobody
to pass its score to. Cell 8 handles it; the markdown above that cell explains why it matters.

</details>

---

## Progress checklist

Tick as you go.

- [ ] Read `explainer.html` end to end
- [ ] Scored 4+ on the section 12 quiz
- [ ] Can say out loud what **idf** is for, why **cosine** and not distance, and what **damping** prevents
- [ ] Cell 1 — sentence splitter, 8 sentences
- [ ] Cell 2 — tokenizer, stopwords gone
- [ ] Cell 3 — vocabulary and count matrix
- [ ] Cell 4 — tf, rows sum to 1
- [ ] Cell 5 — df, idf, tf-idf
- [ ] Cell 6 — lead-3 and tf-idf summaries printed
- [ ] **Wrote down a guess** about what went wrong with the tf-idf summary
- [ ] Cell 7 — cosine similarity matrix, symmetric with a diagonal of 1
- [ ] Cell 8 — TextRank converges, scores sum to 1
- [ ] Cell 10 — ROUGE-1 with clipping, all three methods scored
- [ ] Cell 11 — read the explanation, checked it against my guess
- [ ] Cell 12 — cross-checked against sklearn, understood why they differ
- [ ] Cell 13 *(optional)* — MMR
- [ ] Cell 14 — ran it on my own text

### Then answer these in your own words

Worth doing — these are the questions an exam or an interview would ask.

1. Why does a word appearing in every sentence get an idf of exactly 0, and why is that the right behaviour?
2. Why divide by both norms in cosine similarity instead of just taking the dot product?
3. What would happen to TextRank if you *didn't* zero the diagonal?
4. Lead-3 beat tf-idf here. Give one reason lead-3 is such a strong baseline on news, and one kind of document
   where it would fail badly.
5. Your summary scores ROUGE-1 F1 = 0.9 but reads terribly. How is that possible?

---

## Where this goes next

- **Topic 03 — abstractive summarization.** A pretrained model writes the summary in its own words. Bring these
  ROUGE numbers; they are the baseline it has to beat.
- **tf-idf is the reusable part.** It is still the backbone of search ranking, spam filtering and document
  clustering.
- **Cosine similarity is how RAG works.** Vector databases compare embeddings with exactly this formula. Swap
  tf-idf vectors for neural embeddings and the retrieval half of a RAG system is the code in cell 7.
