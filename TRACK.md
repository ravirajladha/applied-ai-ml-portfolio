# AI/ML Track — from software engineer to AI engineer

> **The one file to open when you don't know what to do next.** Everything else in this repo is reference material.
> Update the checkboxes and the log at the bottom as you go.

---

## ▶ Start here

**Today's one step:** finish `llm-engineering/materials/notes/Session-01-Intro-to-LLMs.md` (§1–11).

**This week (16–22 Nov), only three things:**
1. LLM Session 1 note + practice topic 02 (Transformer). Follow the 5-day schedule in its `guide.md`.
2. Read §2 of this file (the mindset table) once, slowly.
3. Interview: `interview-preparation/top-100-questions.md` Q1–20, say each answer out loud.

⚠️ **19-Nov:** LLM Assignment 1A/1B preference form.

---

## 1. Where you're heading

You are **not** trying to become an ML researcher. The realistic, well-paid target for a full-stack developer with an
AI/ML M.Tech is:

> **AI Engineer / GenAI Engineer / Applied ML Engineer.** You build products *on top of* models (LLM APIs and open models):
> RAG, agents, fine-tuning with LoRA, evaluation, serving and cost control.

In that job, roughly **80% is software engineering** (APIs, data pipelines, deployment, monitoring) and 20% is ML
judgement. You already have the 80%. What interviews check is the 20%: **can you explain the basics clearly and make
sensible choices?** That's what this track builds.

---

## 2. The mindset shift — SDE → ML translation table

The reason ML feels strange: in normal software **you write the rules**; in ML **you write code that finds the rules from data**.
Everything else follows from that.

| You know this (SDE) | The ML version | One-line meaning |
|---|---|---|
| A function you write by hand | A **model** | A function whose logic is *learned* from examples instead of typed |
| Source code → compile → binary | Data + training code → **train** → **weights** | Training is a very slow, expensive "compile" step (hours on GPU). The weights file is the binary |
| Runtime | **Inference** | Running the trained model on new input |
| Config flags | **Hyperparameters** (learning rate, epochs, LoRA rank) | You set them; the model doesn't learn them |
| Program state | **Parameters / weights** | The numbers the model learns. "8B model" = 8 billion of them |
| Unit tests: pass/fail | **Metrics** on held-out data (accuracy, F1, perplexity) | There is no "correct": only "right 92% of the time" |
| dev / staging / prod | **train / validation / test** split | Never grade the model on data it trained on |
| Hard-coding the test cases to make CI green | **Overfitting** | Memorised the training data, fails on new data |
| Code too simple to handle the cases | **Underfitting** | Model too weak or trained too little |
| Bug in the code | Bug in the **data** (bad labels, leakage, skew) | Most ML bugs are data bugs. Look at the data first |
| Objective / spec | **Loss function** | One number saying how wrong the model is. Training makes it smaller |
| Auto-tuning knobs | **Gradient descent** | Nudge every weight a little in the direction that lowers the loss; repeat millions of times |
| Type errors | **Tensor shape errors** | `(4, 8) @ (4, 4)` fails like a type mismatch. Print `.shape` |
| Deterministic output | **Probabilistic output** | Same input can give different output (sampling). Design for it |
| ID / primary key | **Embedding** | An ID turned into a list of numbers where similar things sit close together |
| Search index lookup | **Vector search / RAG** | Find text by meaning (cosine similarity), then give it to the LLM |
| Function signature + docs | **Prompt** | The LLM's "interface". Small changes change behaviour |
| Loop that calls services | **Agent** | An LLM in a loop that decides which tool/API to call next |
| Test suite | **Evals** | A fixed set of inputs + scoring, rerun on every change |
| Library you import | **Pre-trained model** | Someone else paid for training; you fine-tune or prompt it |
| Patch / plugin | **LoRA adapter** | Small add-on file that changes a big model's behaviour without editing it |

**Three rules that replace "make it compile, make the tests pass":**
1. **Start with the data, not the model.** Look at 20 real examples before writing any code.
2. **Always have a baseline** (the simplest thing: a rule, a keyword match, a small model). Only beat it with something bigger.
3. **Measure on data the model never saw.** If you can't measure it, you can't claim it works.

---

## 3. The basics ladder — what "knowing the basics" means

Climb in order. **You're done with a level when you can answer its 5 questions out loud in ~1 minute each**, no notes.

### L1 · ML fundamentals
- What's the difference between supervised, unsupervised and reinforcement learning? One example each.
- What is overfitting, how do you detect it, and three ways to fix it?
- Precision vs recall: when would you prefer each? What is F1?
- Linear vs logistic regression: what does each predict?
- Why train/validation/test splits? What is data leakage?

📂 `interview-preparation/top-100-questions.md` (Q1–50) · `models-explained.md` (linear, logistic, decision tree, random forest, k-means only) · `machine-learning.md` (look things up, don't read it start to finish)

### L2 · Deep learning fundamentals
- What does a single neuron compute? Why do we need a non-linear activation?
- What is a loss function, and what does gradient descent do with it?
- Backpropagation in one sentence (no maths).
- What do learning rate, batch size and epoch mean?
- Dropout and early stopping: what problem do they solve?

📂 `interview-preparation/deep-learning.md` (first sections: neurons, loss, gradient descent, backprop, overfitting) · NLP `revision/ch05-neural-networks-neural-lm.md`

### L3 · Text → LLMs
- What is a token and why do LLMs use sub-word tokens (BPE)?
- What is an embedding? Static (word2vec) vs contextual?
- Cosine similarity: what does it measure, and where is it used?
- Explain self-attention with Query/Key/Value.
- BERT vs GPT: architecture, training objective, what each is good at.

📂 `llm-engineering/materials/notes/Session-00` and `Session-01` · `llm-engineering/practice/02 Transformer …` · NLP `revision/ch02`, `ch03`, `ch04`

### L4 · LLM engineering (where the jobs are)
- Pre-training vs fine-tuning vs prompting: when do you use which?
- What is RAG, and why use it instead of fine-tuning?
- LoRA in one sentence; why QLoRA fits on a small GPU.
- What's a context window, and why does a long answer cost more?
- How would you evaluate an LLM feature before shipping it?

📂 `llm-engineering/materials/notes/Session-02`, `Session-03` · Assignment 1A/1B · upcoming LLM modules (inference, prompting, RAG, agents, evaluation)

### L5 · Shipping it (your SDE edge)
- How do you serve a model behind an API, and what about latency and cost?
- What is data/model drift and how do you monitor it?
- Batch vs real-time inference?
- How is CI/CD different for ML (data + model versions)?
- Design an LLM support chatbot end to end (system design).

📂 `software-engineering-for-machine-learning/materials/notes/` (Sessions 2, 5, 12, 14) · `interview-preparation/application-development/categories/10-ml-ai-integration.html`, `11-system-design.html`

---

## 4. Time budget and the next 5 weeks

**Budget:** ~1.5 h on weekdays + ~3 h on Saturday and Sunday ≈ **13 h/week** for AI/ML. DSA practice and job applications
are **separate blocks**, so don't cut them for this. If a week goes badly, do only the **bold** item for that week.

| Week | LLM course | Interview basics | NLP (selective) |
|---|---|---|---|
| **1 · 16–22 Nov** | **Session 1 note + Transformer topic 02** · 1A/1B form (19-Nov) | top-100 Q1–20 | — |
| **2 · 23–29 Nov** | **Session 2 + 3 notes** · Webinar 1 · start Assignment 1A | L1: top-100 Q21–50, models-explained (4 models) | ch02 cosine/TF-IDF + ch03 word2vec (2 h) |
| **3 · 30 Nov–6 Dec** | **Assignment 1A: CPT + QLoRA runs** · Webinar 2 | L2: deep-learning.md first sections | ch04 n-grams & perplexity (1 h) |
| **4 · 7–13 Dec** | **Assignment 1A: results + write-up** | L3 + L4 questions out loud · write your 2-min pitch (§6) | ch08 prompting/transfer (1 h) |
| **5 · 14–20 Dec** | **Submit 1A (19-Dec)** · start mid-sem revision (modules 1–5, closed book) | L5 + one mock system design | — |

### Checklist
- [ ] W1 — Session 1 note · Transformer topic 02 · top-100 Q1–20 · 1A/1B form
- [ ] W2 — Session 2 & 3 notes · Webinar 1 · L1 questions · NLP ch02–03
- [ ] W3 — 1A training runs · L2 questions · NLP ch04
- [ ] W4 — 1A write-up · L3/L4 out loud · pitch written · NLP ch08
- [ ] W5 — 1A submitted · L5 · mid-sem revision started

---

## 5. NLP: should I revise it? → only ~5 hours, not the handouts

The NLP course is finished, and the two handouts are 234 pages. **Don't re-read them.** Revise only what the LLM course and
interviews reuse, from the revision pack you already built (`natural-language-processing/revision/`):

| Keep (≈5 h total) | Why |
|---|---|
| `ch02` vector semantics, cosine, TF-IDF | Cosine and TF-IDF come up in every RAG/search interview |
| `ch03` word2vec, GloVe | "Static vs contextual embeddings" is a classic question |
| `ch04` n-gram LMs, perplexity | Perplexity = the LLM course's evaluation metric |
| `ch05` neural networks & neural LM | Doubles as L2 deep-learning basics |
| `ch08` prompting, transfer learning, fine-tuning | Direct overlap with LLM modules |
| Your **Assignment 2 project** (review summarizer, T5 + Streamlit) | An interview story, see §6 |

| Skip | Why |
|---|---|
| POS tagging, HMM, **Viterbi**, MEMM, CRF (ch06–07) | Exam numericals; almost never asked for AI-engineer roles |
| Parsing, dependency parsing (post-midsem) | Same |
| NLP `practice/01 Transformers - BERT and GPT` | Covered by LLM `practice/02 Transformer` (newer, linked to your assignment) |
| The handout PDFs | Reference only. Open a page when a note points you there |

---

## 6. Interview kit

**Your 2-minute pitch (fill in during week 4):**
> "I'm a full-stack developer with 4+ years of experience building and shipping web applications. During my M.Tech in AI/ML I've
> built [project 1] and [project 2]. What I bring is the engineering side, APIs, deployment and reliability, combined with
> hands-on LLM work: fine-tuning with LoRA, evaluation, and building apps around models. I'm looking for an AI engineer role
> where I can ship LLM features to production."

**Three stories to be able to tell** (problem → what you did → result → what you'd do differently):
1. **Customer review summarizer** (NLP Assignment 2): LSTM-with-attention baseline vs fine-tuned T5, ROUGE evaluation, Streamlit app.
2. **Domain LLM with CPT + QLoRA** (LLM Assignment 1A): continued pre-training on domain text, QLoRA instruction tuning, before/after evaluation.
3. **An SDE project of yours where you added or could add AI**: how you would integrate an LLM safely (latency, cost, fallbacks, evals).

**Rehearse from:** `interview-preparation/flashcards.html` (phone, 10 min/day) · `top-100-questions.md` · the 5 questions per ladder level above.
**Planned:** `interview-preparation/nlp.md` (LLM/NLP interview set), to build together from the LLM notes in week 4.

---

## 7. Global skip list (for now)

Maths derivations (backprop algebra, SVD proofs, RoPE) · reinforcement learning beyond one-liners · CNN internals beyond
one-liners · writing models from scratch in PyTorch · reading research papers end to end · any new course or
YouTube playlist not linked from this file.

---

## Log

| Date | What I did | Next |
|---|---|---|
| 15-Nov-2026 | Track created. LLM notes (S0–S3) and Transformer topic 02 built. | Session 1 note §1–11 |
