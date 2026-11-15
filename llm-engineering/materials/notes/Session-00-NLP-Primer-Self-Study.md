# Session 0 — NLP Primer (self-study)

> **Deck:** `NLP_Primer_SelfStudy_llm.pptx` (13 slides; `NLP_Primer_SelfStudy (1).pptx` is the same deck) · No lecture, read on your own.
>
> **One-line goal:** learn the 20 or so words the rest of the course uses without explaining: how text becomes numbers, what a language model is, and which NLP tasks LLMs do.

### Contents
1. [Text → numbers](#1-text--numbers)
2. [Tokens → vectors](#2-tokens--vectors)
3. [Measuring similarity](#3-measuring-similarity)
4. [Language models and autoregression](#4-language-models-and-autoregression)
5. [The three Transformer families](#5-the-three-transformer-families)
6. [What LLMs are used for (NLU vs NLG)](#6-what-llms-are-used-for-nlu-vs-nlg)
7. [Recap](#-recap)

---

## 1. Text → numbers

A computer can't read words; it only does arithmetic. So step one is always: **chop the text into pieces and give each piece a number.**

| Term | Plain meaning | Example | Why an LLM cares |
|------|---------------|---------|------------------|
| **Corpus** | The big pile of text a model learns from (web, books, code, papers), cleaned and de-duplicated | Llama 3 read ≈ **15 trillion tokens** | A model rarely knows what its corpus lacked |
| **Token** | The unit a model reads and writes: a word, a piece of a word, punctuation or one byte | `"unhappiness!"` → `un | happi | ness | !` (4 tokens) | Context length, API price and speed are all counted in tokens, not words |
| **Tokenization** | Splitting text into tokens and mapping each to an integer ID | `"hug"` → bytes `[104,117,103]` → after merges `[257]` | The same sentence costs different token counts on different models, especially Hindi or code |
| **Vocabulary \|V\|** | The fixed list of every token the model knows. Set when the tokenizer is trained; can't change later without retraining | Llama 3: 128,256 · Qwen3: ≈151,669 · Gemma 3: 262,144 | \|V\| sets the size of the embedding table and the output layer. Bigger \|V\| = fewer tokens per sentence but more parameters |
| **OOV** (out-of-vocabulary) | A word not in the vocabulary. Old word-level models replaced it with `[UNK]` and lost its meaning | word-level: `Transformerify` → `[UNK]`; subword: `Transformer | ify`; byte-level: never `[UNK]` | Byte-level BPE removes OOV completely; new words just cost more tokens |

> 🌍 **Analogy — LEGO.** The vocabulary is your box of LEGO brick types. Common words are big pre-made pieces; rare words get built from small bricks. With byte-level bricks (only 256 tiny types) you can build *anything*, it just takes more bricks.

---

## 2. Tokens → vectors

A token ID like `2` is just a label; the number itself carries no meaning (token 3 isn't "more" than token 2). We need a **vector** (a list of numbers) that captures meaning.

**One-hot vector** — length \|V\|, all zeros except a 1 at the token's ID.
- vocab `[brown, dog, fox, jumps]` → `"fox"` = `[0, 0, 1, 0]`
- Problem: huge (128K long) and meaningless: every pair of words is equally far apart. It is only a conceptual step: one-hot × E simply *picks one row* of the embedding matrix.

**Embedding** — a short, dense vector of learned numbers (length *d*).
- `"fox"` → `[1.28, −0.20, −0.16, …]`; Llama 3 8B uses *d* = 4096.
- The embedding table **E** has shape \|V\| × *d* → 128,256 × 4096 ≈ **525M parameters** in Llama 3 8B.
- Values start random and are trained so that words used in similar ways end up with similar vectors.

### Static vs contextual

| | Static embedding | Contextual embedding |
|---|---|---|
| Idea | One fixed vector per word, whatever the sentence | Vector depends on the surrounding words |
| Learned by | word2vec, GloVe | Every Transformer layer, via attention |
| "bank" in *river bank* vs *bank loan* | **same** vector | **different** vectors (v1 ≠ v2) |
| In an LLM | The **input embedding table** is static | The **hidden states** inside are contextual |

> 🌍 Static = a dictionary entry (one definition, printed once). Contextual = a friend who hears the whole sentence and tells you which meaning was intended.

---

## 3. Measuring similarity

Once text is a vector, "how close in meaning?" becomes "how close in direction?"

**Cosine similarity:**  cos θ = (a · b) / (|a| |b|)
- **1** = same direction, **0** = unrelated, **−1** = opposite. It ignores vector length.
- sim(king, queen) high; sim(king, banana) low.

**Semantic similarity** — closeness of *meaning* even with no shared words.
- "How do I reset my password?" vs "I forgot my login details" → high similarity, almost no shared words.
- This is the basis of **RAG** (Retrieval-Augmented Generation: find the documents most similar to the question and hand them to the LLM).

> 🧪 **Tiny worked example.** a = [1, 2], b = [2, 4]. a·b = 2 + 8 = 10. |a| = √5, |b| = √20. cos = 10 / √100 = **1.0**, same direction even though b is twice as long. That's why cosine is used: length (e.g. document length) shouldn't change "meaning".

---

## 4. Language models and autoregression

**Language model (LM)** — a model that gives probabilities to sequences of tokens, or, equivalently, a probability for each possible *next* token.
- P("sidewalk" | "…standing on the") = high; P("banana" | "…standing on the") = low.
- An LLM is exactly this, just huge and trained on trillions of tokens.

**Autoregressive** — generate one token at a time; append it to the input; predict the next.
- "So long and thanks for" → "all" → "the" → "fish".
- Explains why chat output streams word by word, and why long answers are slow: **one full model pass per generated token.**

> 🌍 Autocomplete on your phone, run in a loop, fed its own suggestions.

---

## 5. The three Transformer families

| Family | How it reads | Generates? | Examples | Good for |
|--------|-------------|-----------|----------|----------|
| **Encoder-decoder** (seq2seq) | Encoder reads all input; decoder writes output while looking back at encoder | Yes | Original Transformer (2017), T5, BART | Translation (English → Hindi), summarization |
| **Encoder-only** | Whole text, both directions at once | No, produces embeddings | BERT, RoBERTa | Classification, NER, embedding models for RAG search |
| **Decoder-only** | Left to right; each token sees only earlier tokens | Yes, autoregressively | GPT, Llama 3, Qwen3, DeepSeek-V3 | Almost all modern LLMs, **the focus of this course** |

---

## 6. What LLMs are used for (NLU vs NLG)

- **NLU** (Natural Language Understanding) — extract meaning: labels, entities, intent. *"Is this review positive?"*
- **NLG** (Natural Language Generation) — produce new text. *"Write a reply to this review."*
- LLMs are generators, but they do NLU **by generating the answer word** (e.g. "positive").

| Task | Type | Example | How an LLM does it |
|------|------|---------|-------------------|
| Text classification | NLU, whole text | sentiment, spam, ticket = billing/technical | Compare P("positive" \| prompt) vs P("negative" \| prompt), no task-specific model |
| NER (named entity recognition) | NLU, per span | [Charles Darwin]PERSON published in [London]LOCATION in [1859]DATE | Prompt + JSON (structured) output, e.g. invoices, contracts |
| POS tagging (part of speech) | NLU, per word | "book a flight" → VERB; "read a book" → NOUN | Learned implicitly |
| Machine translation | NLG | "Where is the station?" → "स्टेशन कहाँ है?" | General LLM; quality depends on how much of that language was in the corpus |
| Summarization | NLG | 10-page report → 5 bullets | Limited by context window; check faithfulness |
| Question answering | NLG | "Who wrote *The Origin of Species*?" → Darwin | RAG = QA over your own documents, reduces hallucination |

---

## ✅ Recap

- Text → **tokens** → **IDs** → **embeddings** (vectors). Everything is counted in tokens.
- **Byte-level BPE** means no word is ever unknown (no `[UNK]`), just more tokens.
- **Embedding table** is static; **hidden states** are contextual.
- **Cosine similarity** compares meaning; it powers search and RAG.
- An **LLM = next-token probability model**, generating **autoregressively**.
- **Decoder-only** is the modern LLM design; encoder-only still powers classifiers and embedding search.

**Self-check (answer without looking):**
1. Why does a bigger vocabulary make a model bigger? *(Hint: two layers depend on \|V\|.)*
2. Give one sentence where "bank" needs a contextual embedding.
3. Why is a 1,000-token answer slower than a 100-token one?
