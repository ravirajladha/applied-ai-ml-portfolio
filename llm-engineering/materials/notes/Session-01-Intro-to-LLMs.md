# Session 1 — Introduction to LLMs (building blocks)

> **Deck:** `CS-1 Intro to LLM.pptx` (46 slides) · **Lecture:** 24-Oct-2026, 2h14m (transcript in `transcript/…session1.docx`)
>
> **One-line goal:** what an LLM *is* (a giant next-token predictor), and the first two building blocks of one: **tokenization** (BPE / byte-level BPE) and **embeddings + positional encoding**.
>
> **Taught in class:** slides 1–33 only. Slides 34–46 (LM head, context length, model landscape, encoder/decoder review) were **not lectured** — they're summarised here from the deck so you're covered.

### Contents
0. [Course logistics (what the professor said)](#0-course-logistics)
1. [Language AI: three kinds of application](#1-language-ai)
2. [Probabilistic language models](#2-probabilistic-language-models)
3. [What makes it "Large"](#3-what-makes-it-large)
4. [Every NLP task is next-word prediction](#4-every-nlp-task-is-next-word-prediction)
5. [Generative AI and decoding](#5-generative-ai-and-decoding)
6. [The building blocks](#6-the-building-blocks)
7. [Tokenization: word vs subword vs character vs byte](#7-tokenization)
8. [BPE — worked example](#8-bpe--worked-example)
9. [Byte-level BPE, SentencePiece, which library to use](#9-byte-level-bpe-sentencepiece-libraries)
10. [Token IDs → embeddings](#10-token-ids--embeddings)
11. [Positional encoding](#11-positional-encoding)
12. [LM head, context length *(not lectured)*](#12-lm-head-and-context-length-not-lectured)
13. [Model landscape & architecture families *(not lectured)*](#13-model-landscape--architecture-families-not-lectured)
14. [Recap + self-check](#-recap)

---

## 0. Course logistics

| Component | Weight | Notes |
|-----------|--------|-------|
| Assignments | **35%** | A1 = 15 marks, A2 = 20 marks · groups of 4 · same cleaned dataset carries from A1 → A2 · **no quizzes** |
| Mid-sem | **30%** | **Closed book**, modules 1–5 |
| End-sem | **35%** | **Open book** — only the slides on Taxila are allowed (not her annotated ones) |

**Module plan (11 modules):** 1 Foundations → 2 Pre-training & fine-tuning (moved early because Assignment 1 depends on it) → 3 Architecture (revise attention/Transformer from DNN first!) → 4 Inference fundamentals ("very important") → 5 Inference bottlenecks & optimisation · *(mid-sem = 1–5)* → 6 Preference alignment (RLHF, PPO, DPO) → 7 Prompting & reasoning → 8 RAG (self-RAG, self-correcting RAG) → 9 Agents (memory, hybrid architectures) → 10 Evaluation → 11 Safety & security. Sessions 8 and 16 are buffer/revision.

**Other:**
- **Webinars = labs**, run by LFs. **Webinars 1 & 2 cover what you need for Assignment 1** — attend.
- **Lab:** BITS remote GPU lab (Prayogshala front-end, Kubeflow back-end, Hyderabad). GPUs with ~40/80/96 GB. She advised **avoiding Colab**. No API credits are given.
- **Books:** Alammar *Hands-On LLMs* · Jurafsky & Martin *SLP3* (Jan-2026 draft) · Raschka *Build an LLM from Scratch*. Follow their blogs; the field moves too fast for hard copies.
- Check **Taxila announcements** — deadlines live there.

---

## 1. Language AI

Course scope = **text in, text out.** Three application types:

| Type | Output | "Classic" tool (2019–21) | Today |
|------|--------|-------------------------|-------|
| Generative | text → text | GPT | LLM |
| Embeddings | text → vector | BERT variants | Still BERT-style / embedding APIs |
| Classification | text → label | BERT + classifier head | LLM via prompt, *or* light BERT model |

> 💬 **Professor:** "It's not like you have to use LLM everywhere." Like the early ML hype when people wanted ML "even to calculate 2+2". Choose by budget, infrastructure and objective — "ultimately everything is tied to the cost".

---

## 2. Probabilistic language models

A **language model** gives probabilities to token sequences. Two equivalent views:

1. Probability of a whole sentence: **P(W) = P(w₁, w₂, …, wₙ)**
2. Probability of the next token: **P(wₙ | w₁, …, wₙ₋₁)**

They're linked by the **chain rule**: **P(w₁…wₙ) = ∏ P(wᵢ | w₁…wᵢ₋₁)** → predict the next token well and you can score any sentence.

- P("all of a sudden I notice three guys standing on the sidewalk") **high**
- P("on guys all I of notice sidewalk three a sudden standing the") **low** — order matters.
- In class: "I am teaching ___" → "LLMs". All the previous words = the **context**.

> 🧪 **Chain rule in numbers.** P(I)=0.1, P(am | I)=0.4, P(teaching | I am)=0.05 → P("I am teaching") = 0.1 × 0.4 × 0.05 = **0.002**.

**How LMs evolved:**

```
n-gram  →  Neural LM       →  RNN / LSTM      →  Transformer         →  Hybrid
count      learned            sequential         attention:             attention + Mamba
last n−1   embeddings         memory             GPT, Llama, Qwen       (Jamba)
words
```

- **Why Transformers won:** **parallelization** — self-attention processes all tokens together (RNNs go one by one).
- **Mamba** (not on slides) = a **state space model (SSM)**, RNN-like, no attention. Hybrids exist because Transformers struggle with memory in long agentic tasks.

---

## 3. What makes it "Large"

LLM = deep neural network (**Transformer**) trained with **self-supervised next-token prediction** on huge filtered text (web, code, books, papers). "Large" means three things:

| Dimension | Examples |
|-----------|----------|
| **Parameters** — billions | Llama 3: 8B–405B · DeepSeek-V3: 671B total, ~37B active per token |
| **Training data** — trillions of tokens | Llama 3 ~15T · Qwen3 ~36T |
| **Context window** | 2K (GPT-3) → 128K+ (Llama 3.1, Qwen3) |

> 💬 If it were only about architecture we'd just say "Transformer LM". **"Large" = these three properties.**

---

## 4. Every NLP task is next-word prediction

Almost any NLP task can be phrased as "what word comes next?" (**conditional generation**):

- **Sentiment:** compare P("positive" | "The sentiment of the sentence 'I like Jackie Chan' is:") vs P("negative" | …)
- **QA:** P(w | "Q: Who wrote the book 'The Origin of Species'? A:") — "A:" signals "start answering".

**Then vs now:** one fine-tuned model per task (BERT + classifier) → **one LLM, many tasks, via the prompt.**

---

## 5. Generative AI and decoding

- An LM outputs a **probability distribution over the vocabulary** for the next token. It's just softmax classification where **the classes are the vocabulary tokens** (e.g. 50,000 classes).
- **Sampling** = choosing a word from that distribution. Why not always the top word? Many tokens are near-synonyms; sampling the 2nd/3rd best gives variety. **Sampling is what makes it generative.**
- **Autoregressive LM** = generate → append → repeat.
- **Decoding** = the process of generating text from an LLM (sampling algorithms, temperature… → Module 4).
- Same idea applied to code, images, speech, video = **Generative AI**.

> 🎯 **Flagged:** output is produced **one token at a time** — you can see it streaming in any chatbot. This is the key to understanding inference cost later.

---

## 6. The building blocks

```
"Write an email…" → [Tokenizer] → token IDs → [Embeddings + position]
                  → [Transformer block 1 … N] → [LM head] → next token "Dear"
```

- **Tokenization** (BPE, byte-level BPE) — this session
- **Token embeddings + positional encoding** — this session
- **Attention & Transformer** — Module 3
- **Language-modelling head** — §12 below

Slide 13 one-liners (memorise):
- **Attention = talk between tokens.**
- **FFN = think per token.**
- **Residual stream** = each sub-layer *adds* to X, never replaces it.
- Generative models use **only the decoder** half of the Transformer.

**Corpus** = documents (PDFs, emails, web pages, chats) **after pre-processing**. Raw files are not yet a corpus.

> 🛠️ **Not confident about what happens inside the Transformer blocks?** After this note, do practice topic [02 Transformer — attention to next token](../../practice/02%20Transformer%20-%20Attention%20to%20Next%20Token/guide.md) (explainer + numpy notebook, ~6 h over 5 days), then come back for Session 2.

---

## 7. Tokenization

**Vocabulary building:** corpus → tokenize → unique tokens → each gets a fixed **token ID** (vocab of 50K → IDs 0–49,999). The vocabulary depends on the corpus's language/domain.

**Subwords handle the messy stuff:** common words get their own token; rare words, misspellings and new words are split into pieces.
- `taaaaasty` → `taa## aaa## sty` · `laern` → `la## ern##` · `Transformerify` → `Transformer## ify`
- Worst case: a word splits into as many tokens as it has characters/bytes.
- Notation: `##` = continuation in **WordPiece** (BERT). Byte-level BPE (GPT, Llama, Qwen) instead marks a **leading space**: `Ġtasty`.

### Four token types — `"unhappiness!"`

| Type | Split | Pros | Cons |
|------|-------|------|------|
| Word | `unhappiness` `!` | Short sequences | **OOV** breaks at inference; near-duplicates (apology/apologize/apologist) bloat the vocab |
| **Subword** | `un` `happi` `ness` `!` | New words → known pieces. **Used by every modern LLM** | Splits are learned, not linguistic |
| Character | `u n h a p p i n e s s !` | Tiny vocab | Long sequences; mainly research (CANINE) |
| Byte | "Apple" → `65 112 112 108 101` (5); "क" → `224 164 149` (3) | Vocab = **256**, nothing ever OOV | Much longer sequences (ByT5) |

**Byte-level BPE** = subword merges built on top of bytes → used by Llama, Qwen, DeepSeek, gpt-oss.

### Every tokenizer has two parts

| Part | When | Does |
|------|------|------|
| **Token learner** | Once, at tokenizer-training time | Runs BPE on the corpus → vocabulary + **merge rules** |
| **Token segmenter** | On every input, at inference | Applies the rules: `hugs` → `[hug, s]` → `[12, 5]` |

> 🎯 **Every model publisher trains its own tokenizer; at inference you must use that same tokenizer.** Vocabulary sizes are in the model card. The tokenizer is trained *before* the model.

Three algorithms: **BPE** (Sennrich 2016), **Unigram LM** (Kudo 2018), **WordPiece** (Schuster & Nakajima 2012).

---

## 8. BPE — worked example

> 🎯 **Exam favourite.** She said a full BPE question with answer key is in a past paper she'll upload.

**Steps:**
1. **Pre-tokenize** — split corpus into words (rules: whitespace/regex).
2. **Count word frequencies:** (hug, 10), (pug, 5), (pun, 12), (bun, 4), (hugs, 5)
3. **Start from single characters:** vocab = [b, g, h, n, p, s, u] (7)
4. **Count adjacent pairs (weighted by word frequency) and merge the most frequent.**
5. **Repeat** until target vocab size.

**Iteration 1 pair counts:**

| Pair | Comes from | Count |
|------|-----------|-------|
| **(u, g)** | hug 10 + pug 5 + hugs 5 | **20** ← winner |
| (p, u) | pug 5 + pun 12 | 17 |
| (u, n) | pun 12 + bun 4 | 16 |
| (h, u) | hug 10 + hugs 5 | 15 |

| Iter | Vocab added | Words afterwards |
|------|------------|-----------------|
| 1 | — | `h u g`, `p u g`, `p u n`, `b u n`, `h u g s` |
| 2 | **ug** (20) | `h ug`, `p ug`, `p u n`, `b u n`, `h ug s` |
| 3 | **un** (12+4 = 16) | `h ug`, `p ug`, `p un`, `b un`, `h ug s` |
| 4 | **hug** (h+ug: 10+5 = 15) | `hug`, `p ug`, `p un`, `b un`, `hug s` |

Final toy vocab = 10 tokens: [b, g, h, n, p, s, u, ug, un, hug].

**Segmenter** (apply merges in learned order):
- `bug` → `b u g` → `b ug`
- `hugs` → `h u g s` → `h ug s` → `hug s`
- `mug` → `m` not in vocab → **[UNK]**. Fix: start from **256 bytes**, not characters → **byte-level BPE**.

> 💬 **Not on the slide (asked in class): why wasn't "pu" (17) merged after "ug"?** Real BPE would pick the highest count next — the slide's order is illustrative. She noted **minimum frequency** and **max vocab size** are BPE **hyperparameters** and said she'd add them to the slide. In an exam, **show your pair counts and state any min-freq rule you apply.**
> Also: pair order matters — `ug` ≠ `gu`. Merges build on the previous iteration.

**Advantages:** handles rare words and subword units · smaller vocab → efficient · better generalisation (`apolog` + `y`/`ize`/`ist`).
**Limitations:** purely frequency-based, no linguistics → fragmented tokens for morphologically rich languages (South Indian languages, French) · doesn't capture meaning well.

---

## 9. Byte-level BPE, SentencePiece, libraries

**Byte-level BPE:** characters are decomposed into their UTF-8 bytes. `"u"` = 117, `"g"` = 103 → after the first merge the vocab records "ID 256 = bytes [117 103] = ug". **No unseen characters are possible**, and the base vocabulary is tiny (256).

**SentencePiece** (Google): library implementing BPE + Unigram. **Language-agnostic — no pre-tokenizer needed**, works on raw text (great for Chinese, Japanese, Thai). Marks spaces with `▁`. Used by T5, Gemma, Llama 1 & 2.

**Which tool?**

| Goal | Use | Notes |
|------|-----|-------|
| Train / extend a tokenizer | HF `tokenizers` | Custom BPE/Unigram, normalisation rules, choose vocab size |
| Build on open models | HF `transformers` tokenizers | Loads any Hub model's tokenizer, chat templates, special tokens |
| OpenAI API models | `tiktoken` | Fast exact **token counting** / cost estimation; cannot train |
| Other closed APIs | Vendor's token-count API | No local tokenizer library |

> HF: **you** tokenize, then the model runs. API: the **server** tokenizes; you only count and trim.

---

## 10. Token IDs → embeddings

1. **Text → token IDs** via the tokenizer.
2. **Special context tokens** are added: e.g. `<|unk|>`, `<|endoftext|>`. They differ per model → always use the model's own tokenizer.
3. **IDs → embeddings** by a table lookup.

**Embedding intuition:** a vector whose dimensions loosely capture features (animal? newborn? human? plural?). "cat" scores high on *animal*, "house" low. In 2-D, cat/dog/puppy cluster together; apple/banana cluster elsewhere.

### The embedding layer is just "look up a row"

**E** has shape **\|V\| × d** — one row per vocab token. Values start random and are **learned while training the model** (not the tokenizer).

| ID | token | dim1 | dim2 | dim3 |
|----|-------|------|------|------|
| 0 | brown | 0.34 | −0.18 | −0.17 |
| 1 | dog | 0.92 | 1.58 | 1.30 |
| 2 | fox | 1.28 | −0.20 | −0.16 |
| 3 | jumps | −0.40 | 0.97 | −1.15 |
| 4 | lazy | −1.16 | 0.33 | −0.63 |
| 5 | over | −2.84 | −0.78 | −1.41 |

"fox jumps over dog" → IDs **[2, 3, 5, 1]** → stack those rows → **X is n × d = 4 × 3**.

- Same token → same vector wherever it appears (that's why position must be added separately).
- **Real scale:** Llama 3 8B, E = 128,256 × 4096 ≈ **525M parameters**.

**Types of text embeddings:** token (LLM input) · word (word2vec, static) · sentence (sentence-transformers) · document (doc2vec).

> 💬 **Q&A clarifications:**
> - BPE produces only vocab + IDs. **Embeddings are learned with the model.** "Corpus is never trained. Model is trained."
> - Decoders use causal masking (can't see the future), so **encoder-only models give richer contextual embeddings**.
> - word2vec (skip-gram/CBOW) is static — "nobody uses word2vec now".
> - It's a **token** embedding — "there is nothing called word embedding" in an LLM.

---

## 11. Positional encoding

**Why:** attention has **no built-in sense of order** — "dog bites man" and "man bites dog" would look identical. Position must be injected. (And token ID ≠ position: the ID is a vocab index, position is order in the input.)

**Input to the Transformer = token embedding + positional embedding.**

| Method | How | Used by |
|--------|-----|---------|
| **Sinusoidal** | Fixed sine/cosine at many frequencies, **added** to token embeddings | Original Transformer (2017) |
| **Learned** | Trainable lookup table, one vector per position, **added** | GPT-2, BERT (no longer common) |
| **RoPE** (Rotary) | **Not added to the input** — rotates Q and K inside every attention layer so scores depend on *relative* position | Llama, Qwen, DeepSeek → Module 3 |

> 🌍 Learned/sinusoidal = writing a seat number on each guest's badge. RoPE = turning each guest by an angle so that any two guests can tell how far apart they sit just by comparing their angles.

---

## 12. LM head and context length *(not lectured)*

**Language-modelling head = unembedding layer + softmax.**
- Takes the final hidden state at a position, **h** (1 × d), multiplies by the **unembedding matrix** (d × \|V\|) → **logits u** (1 × \|V\|), one score per vocab token → **softmax** → probabilities **y**.
- Unembedding matrix can be **tied** to the embedding matrix (Eᵀ) to save parameters.
- **Training:** logits at all n positions in parallel (n predictions). **Inference:** only the last position.
- Size: d × \|V\| = 4096 × 128K ≈ **525M params** in Llama 3 8B → bigger vocab = bigger head.
- Probabilities are used to (a) **score** a text, (b) **generate** by sampling.

**Context length** = the maximum number of tokens the model can process. Because generation is autoregressive, the context **grows as tokens are generated**.

> 🎯 Session 3 emphasised: **the context window includes the generated output** — the limit is *prompt + answer* in one call.

---

## 13. Model landscape & architecture families *(not lectured)*

**Timeline:**
- **Early foundation models (late 2010s):** ELMo (LSTM pre-training), BERT (Transformer pre-training + fine-tuning), T5 11B (everything as text-to-text).
- **Scaling, more closed:** GPT-2 1.5B (first zero-shot signs) → Kaplan scaling laws → GPT-3 175B (**in-context learning**) → PaLM 540B (undertrained) → Chinchilla 70B (compute-optimal).
- **Open models:** EleutherAI (The Pile, GPT-J), Meta OPT 175B, BLOOM, Llama, Qwen, DeepSeek, OLMo 2.

**Levels of openness:**

| Level | What you get | Examples |
|-------|-------------|----------|
| Closed | API access only | GPT, Gemini |
| **Open-weight** | Weights + architecture paper, some training details, **no data** | Llama, DeepSeek, Qwen |
| **Open-source** | Weights **and data**, most details | OLMo |

**Recent releases (slide 40):** GPT-6 (deep reasoning, tool use) · Gemini 4 (multimodal problem-solving) · Gemma 4 (open-weight, agentic) · Qwen3.x (open dense + MoE; common fine-tuning base) · DeepSeek V4.1 (open, RL-driven reasoning from R1) · Mistral Large 4 (sparse MoE) · Grok 4.7 (multi-agent research).

### The three Transformer families (review slides)

| | Encoder-only | Decoder-only | Encoder-decoder |
|---|---|---|---|
| Examples | BERT, RoBERTa | GPT, LLaMA | T5, BART |
| Attention | Bidirectional | **Causal mask** (left → right) | Encoder bidirectional + decoder causal + **cross-attention** |
| Objective | **MLM** (mask & predict) | **CLM** (next token, cross-entropy) | Seq2seq / span corruption |
| Strong at | Classification, NER, sentiment | Open-ended generation, dialogue, code | Translation, summarisation, multimodal |
| Weak at | Not naturally generative | Less efficient for classification | Two stacks → more training cost & latency |

---

## ✅ Recap

- LM = probability over token sequences; **chain rule** links "score a sentence" and "predict next token".
- **"Large"** = parameters + training tokens + context window.
- Any NLP task → **prompt + next-word prediction**; **sampling** makes it generative; output is **one token at a time**.
- Pipeline: **tokenizer → embeddings + position → Transformer blocks → LM head**.
- **Subword (BPE)** tokenization beats word/char; **byte-level BPE** means no [UNK].
- **E (\|V\| × d)** is a lookup table learned with the model; position is added (or RoPE rotates Q/K).

**Self-check:**
1. Run BPE on (low, 5), (lower, 2), (newest, 6), (widest, 3) for 3 merges. Show pair counts.
2. Why does a 128K vocab with d = 4096 cost ~525M parameters *twice* (unless tied)?
3. Why can't the token ID double as the position?
4. Why do base vocabularies of 256 guarantee no OOV?
