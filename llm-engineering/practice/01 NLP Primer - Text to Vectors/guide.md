# NLP primer: text to vectors to next word — build guide

**Topic 01 · Large Language Models for Generative AI · practice**

| File | What it is |
|------|------------|
| `explainer.html` | **Open this first.** Interactive lesson: a live tokenizer, an OOV tester, one-hot vs embedding, "bank" in two sentences, a cosine-angle slider, a click-to-generate next-word model, and a 5-question quiz. |
| `practice.ipynb` | The template notebook. Boilerplate is filled in; 14 `# TODO` lines are left for you. |
| `guide.md` | This file — the plan, the recap, and the checklist. |

Source: the course's *NLP primer for this course (self-study)* slides, in `../../materials/`.

---

## The problem statement

A model can only do arithmetic, so text must become numbers first. Starting from a tiny story about a cat and a dog,
build the whole chain an LLM uses:

`text → tokens → IDs → vectors → probability of the next token → generated text`

By the end you will have written, from scratch:

- a tokenizer (regex)
- a vocabulary with IDs, and OOV handling via `<unk>`
- one-hot vectors, and proof that an embedding lookup is just a row pick
- cosine similarity
- a co-occurrence "static embedding" where `cat` and `dog` land close together
- a next-word probability table and an autoregressive generator

Only `numpy` and `re` — nothing to install.

---

## Plain-English recap

| Term | In one line |
|------|-------------|
| **Corpus** | The pile of text a model learns from. |
| **Token** | One piece the model reads: a word, part of a word, punctuation, or a byte. |
| **Tokenization** | Cutting text into tokens and giving each an integer ID. |
| **Vocabulary (\|V\|)** | The fixed list of all tokens a model knows. Llama 3: 128,256. |
| **OOV** | Out-of-vocabulary: a word not in the list. Old models wrote `[UNK]`; byte-level BPE never needs to. |
| **One-hot vector** | Length \|V\|, all zeros except one 1. Names a word, carries no meaning. |
| **Embedding** | A short learned vector (length `d`) per token. Looking it up = picking a row of a \|V\|×d table. |
| **Static embedding** | One vector per word, whatever the sentence (word2vec, GloVe). |
| **Contextual embedding** | A vector recomputed from the surrounding words (inside a Transformer). |
| **Cosine similarity** | Angle between two vectors, ignoring length. 1 same, 0 unrelated, −1 opposite. |
| **Semantic similarity** | Closeness in meaning even with no shared words; the engine of RAG. |
| **Language model** | Gives a probability for the next token. |
| **Autoregressive** | Generate one token, append it, predict the next. One model pass per token. |
| **Encoder-only / Decoder-only / Encoder-decoder** | Reader (BERT) / writer (GPT, Llama) / interpreter (T5, BART). |
| **NLU vs NLG** | Understanding (labels, entities) vs generating (answers, summaries, code). |
| **NER / POS** | Tag names of real things / tag each word's grammar role. |

---

## The build plan, cell by cell

Each cell ends with `assert` checks. If they pass, move on; if not, the message says what broke.

| Cell | You write | Explainer section |
|------|-----------|-------------------|
| 0 | *nothing* — setup and the corpus | 2 |
| 1 | `tokenize` — lowercase + one `re.findall` | 2 |
| 2 | `word_to_id` and `encode` with `<unk>` | 3 |
| 3 | `one_hot` | 4 |
| 4 | embedding lookup two ways, and the parameter count | 4 |
| 5 | `cosine` | 6 |
| 6 | co-occurrence matrix; then find the word most like `sat` | 5 |
| 7 | bigram `counts` and probabilities `P` | 7 |
| 8 | greedy `generate` loop | 7 |
| 9 | *optional* — sampling with `rng.choice` | 7 |
| 10 | *nothing* — answer the questions below | — |

### Where people get stuck

- **Cell 2** — `dict.get(word, default)` is the whole OOV story. Add `<unk>` *after* building the dict, so it does not shift real IDs.
- **Cell 3** — `np.zeros(size)` then `v[word_id] = 1`.
- **Cell 4** — `one_hot(i, V) @ E` and `E[i]` must match exactly; if not, check `i` is the same in both.
- **Cell 5** — the denominator is `norm(a) * norm(b)`, a product, not a sum.
- **Cell 6** — `co[word_to_id[word], word_to_id[tokens[nb]]] += 1`. The assert counts every neighbouring pair twice.
- **Cell 7** — `counts / counts.sum(axis=1, keepdims=True)`. `keepdims` is what makes the shapes line up.
- **Cell 8** — `np.argmax(P[word_to_id[out[-1]]])` gives an ID; convert back with `id_to_word` before appending.

---

## What you should expect to see

Do not read this until you have finished cell 7.

<details>
<summary>The result (click to expand)</summary>

| check | value |
|---|---|
| tokens in the corpus | 38 |
| \|V\| (11 words + `<unk>`) | 12 |
| `cos(cat, dog)` and `cos(mat, rug)` | 1.000 — identical neighbours |
| `cos(cat, mat)` | 0.866 |
| `cos(cat, the)` | 0.292 |
| after `the` | cat 40%, dog 40%, mat 10%, rug 10% |
| greedy `generate("the")` | `the cat .` |

**Why greedy ends so fast:** after `cat` the top choice is the full stop, so the sentence ends after two words. Sampling
(cell 9) gives longer, varied sentences. Also note the model only sees *one* previous word — it has no idea what the
whole sentence was about. Real LLMs look at thousands of tokens of context.

</details>

---

## Progress checklist

- [ ] Read `explainer.html` end to end
- [ ] Scored 4+ on the section 10 quiz
- [ ] Can say out loud: token vs word, static vs contextual, why cosine ignores length
- [ ] Cell 1 — tokenizer, 38 tokens
- [ ] Cell 2 — vocabulary, `<unk>` for unseen words
- [ ] Cell 3 — one-hot
- [ ] Cell 4 — embedding lookup equals one-hot × E
- [ ] Cell 5 — cosine passes all three asserts
- [ ] Cell 6 — co-occurrence matrix, `cat`/`dog` score 1.0
- [ ] Cell 7 — next-word probabilities, rows sum to 1
- [ ] Cell 8 — greedy generation
- [ ] Cell 9 *(optional)* — sampled generation
- [ ] Cell 10 — answered the questions below

### Then answer these in your own words

1. Why is a one-hot vector useless for finding that `cat` and `dog` are related?
2. What is the difference between a token and a word, and why does \|V\| matter for cost?
3. Why does `generate("the")` always give the same sentence, and what does sampling change?
4. Our model looks at one previous word only. Give one sentence it would get wrong.
5. Why can a decoder-only model write text but an encoder-only model (BERT) cannot?

---

## Where this goes next

- **Next topics for this subject:** attention and the Transformer block, then prompting and RAG.
- **Cosine similarity is RAG's search step.** Swap the co-occurrence vectors for neural embeddings and cell 5 is the retrieval half of a RAG system.
- **Topic NLP 02 (extractive summarization)** used tf-idf vectors with the same cosine. Same idea, older vectors.
