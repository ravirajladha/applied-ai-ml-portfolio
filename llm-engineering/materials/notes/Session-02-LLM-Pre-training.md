# Session 2 — LLM Pre-training

> **Deck:** `CS-2 LLM Training.pptx` (28 slides) · **Lecture:** session 2 (no transcript — the file named `…sesion2.docx` is a copy of session 1), then recapped and finished in the first ~50 min of session 3 (slides 4–13 recap, **slides 21–27 taught in detail**). Boxes marked **💬 Session-3 lecture** come from that transcript.
>
> **One-line goal:** how a base model is built: what it learns from (self-supervised next-token prediction), what data it reads and how that data is cleaned, how big to make it (**scaling laws**), how to specialise it for a domain (**continued pre-training**), and what it costs.

### Contents
1. [The 3-stage picture](#1-the-3-stage-picture)
2. [Self-supervised learning](#2-self-supervised-learning)
3. [Pre-training objectives: MLM vs span corruption vs CLM](#3-pre-training-objectives)
4. [How training actually runs (teacher forcing, loss, perplexity)](#4-how-training-actually-runs)
5. [Pre-training data: corpora and the cleaning pipeline](#5-pre-training-data)
6. [Data mixture and curriculum](#6-data-mixture-and-curriculum)
7. [Scaling laws: Kaplan → Chinchilla → today](#7-scaling-laws)
8. [Domain adaptation: three routes](#8-domain-adaptation)
9. [Catastrophic forgetting and the CPT learning-rate recipe](#9-catastrophic-forgetting)
10. [Modern recipes: Llama 3, Qwen3, DeepSeek-V3](#10-modern-recipes)
11. [What it costs](#11-what-it-costs)
12. [Emergent abilities](#12-emergent-abilities)
13. [What you get: the base model](#13-what-you-get-the-base-model)
14. [Recap](#-recap)

---

## 1. The 3-stage picture

From Raschka's *Build an LLM from Scratch* (slide 4):

```
STAGE 1: Build              STAGE 2: Pre-train                 STAGE 3: Fine-tune
data prep + sampling   →    training loop, evaluation,    →    ┌→ classifier (labelled data)
attention mechanism         load pretrained weights            └→ personal assistant (instruction data)
LLM architecture            = FOUNDATION (base) MODEL
```

> 🌍 Pre-training = a child reading the whole library for years (general knowledge). Fine-tuning = a few weeks of job training for one role.

This session = Stage 2. Session 3 = Stage 3.

---

## 2. Self-supervised learning

- The model learns by **predicting hidden parts of text**. No humans label anything: **the label comes from the text itself** (GPT: the next token; BERT: a masked token).
- These made-up prediction games are called **pretext tasks** — not the real goal, but they force the model to learn grammar, facts and meaning.
- **Every token in the corpus is a free training example**, which is why it scales to trillions of tokens.

> 🌍 A fill-in-the-blanks workbook that writes itself: cover a word, guess it, uncover, check.

---

## 3. Pre-training objectives

| Family | Objective | What it does | Models |
|--------|-----------|-------------|--------|
| Encoder-only | **MLM** (masked language modelling) | Hide ~**15%** of tokens; predict them using context **on both sides** | BERT |
| Encoder-decoder | **Span corruption** (denoising) | Replace spans with sentinels `<X>`, `<Y>`; decoder writes the missing spans | T5 |
| Decoder-only | **CLM** (causal language modelling) | Predict the next token from **previous ones only** (left → right) | GPT-2/3, Llama 3, Qwen3, DeepSeek-V3 |

> 🎯 **Modern LLMs use CLM**, because next-token prediction *directly* trains generation; MLM does not.

---

## 4. How training actually runs

- **Teacher forcing** — at each position the input is the **true** previous token, not the model's own guess. (During generation it's the model's own guess.)
  > 🌍 A driving instructor who grabs the wheel after every mistake, so one wrong turn doesn't ruin the rest of the lesson.
- **All positions in parallel** — one forward pass computes the loss at every position at once; the **causal mask** stops each token from peeking at the future.
- **Updates everything** — the loss is backpropagated through all weights, including embeddings.

**Cross-entropy loss** over T tokens:

  **L = −(1/T) Σₜ log P(wₜ₊₁ | w≤ₜ)**   **Perplexity = exp(L)**

- *Cross-entropy* = "how surprised was the model by the true next token", averaged.
- *Perplexity* = "how many tokens was the model effectively choosing between". **Lower = better.**

> 🧪 **Worked example.** The model gives the true next tokens probabilities 0.5, 0.25, 0.5, 0.25.
> log values: −0.693, −1.386, −0.693, −1.386 → mean = −1.04 → **L = 1.04**.
> Perplexity = e^1.04 ≈ **2.83** → on average it was as unsure as picking between ~3 equally likely tokens.

---

## 5. Pre-training data

**Commonly used open corpora (slide 10):** FineWeb (15T tokens), RedPajama-V2 (30T), Dolma (3T, used by OLMo), The Stack v2 (code). Raw sources: Common Crawl, GitHub, arXiv, Wikipedia, books.

**Raw web text is mostly noise.** The cleaning pipeline:

| Step | What it removes | Example |
|------|----------------|---------|
| 1. **Filter** | Low quality, spam, wrong language | `Alice is writing a paper. #$^&` → `#$^&` removed |
| 2. **De-duplicate** | Repeated sentences, near-copy documents | Same paragraph on 50 sites → keep 1 |
| 3. **Remove PII** (personally identifiable info) | Names, emails, phones | `Alice` → `[Somebody]`, `abc@x.com` → `[EMAIL]` |
| 4. **Tokenize + pack** | Wasted padding | `doc1 <eos> doc2 <eos> doc3` fills each context window fully |

**Why de-duplicate?** (likely exam question)
1. Repeated text gets **memorised**.
2. Wastes compute on the same tokens.
3. Prevents **test-set contamination** — if benchmark text is in training data, scores are inflated.
- *How:* n-gram / **MinHash** overlap between documents.

**How filtering is done:**
- **Heuristics** (cheap): language ID, length, block lists.
- **Classifier**: train a small model on known high-quality text; keep what scores well.

---

## 6. Data mixture and curriculum

- **Data mixture** — *what proportion* of each source (web, code, math, books…). E.g. more code → better coding.
- **Data curriculum** — *how the mixture changes over time*: easy/general first, then harder/specialised (math, code, long documents).
- **Annealing** (Llama 3) — in the final stage the learning rate is lowered to **zero** while high-quality data (math, code) is **upsampled** (shown more often).
  - Result: Llama 3 **8B** improved notably on math (GSM8K, MATH); gains on **405B** were negligible — big models already learn well from the general mix.
- **Long context is a curriculum too** — context raised gradually **8K → 128K** in stages.

> 🌍 School: general subjects for years, specialise in the final years, and do the best revision material right before the exam (annealing).

> 💬 **Session-3 lecture — context window ("very important").** Context window = "the maximum sequence of tokens which the LLM can process at a time". BERT/GPT-2: 512 · Llama 2: 4096 · Llama 3: 128K. **The generated output also counts** — the limit is *query + output in one LLM call*. Modern recipes are typically staged: **general knowledge → reasoning → long context**.
> Annealing is a pre-training stage, but the idea can be borrowed in fine-tuning ("anything can be borrowed anywhere").

---

## 7. Scaling laws

### The problem
A big training run costs millions and happens **once**. Before starting you must choose:
- **N** = number of parameters (how big)
- **D** = number of training tokens (how much to read)

Both cost compute: **C ≈ 6 × N × D FLOPs** (dense Transformer, rough). Fixed budget ⇒ bigger model gets less data, and vice versa.

### The solution
**Scaling law** = loss falls in a **smooth, predictable** way (a straight line on a log-log plot) as N, D or C grows. So: run cheap small experiments → fit the curve → extrapolate → lock the recipe before the big run. (Meta used this to pick Llama 3's data mixture.) Predictions are estimates, not guarantees.

### Kaplan et al. (2020)

  **L(N) = (N_c / N)^α_N  L(D) = (D_c / D)^α_D  L(C) = (C_c / C)^α_C**

- Bigger N, D or C → smaller fraction → lower loss.
- **α** (alpha) = how fast loss falls; small here (≈ 0.05–0.1) ⇒ **diminishing returns**, but predictable.
- **Counting parameters:** each layer ≈ **12 d²** weights (attention 4d² + FFN 8d²).
  > 🧪 GPT-3: 96 layers, d = 12,288 → 12 × 96 × 12,288² ≈ **175B** ✔
- **Kaplan's conclusion:** model size matters most; depth vs width barely matters. **10× compute → ~5× bigger model, only ~2× more data.**
- So industry built huge models on little data: **GPT-3 = 175B params, 300B tokens (~1.7 tokens/param).**

### Chinchilla (Hoffmann et al., 2022)

- **Scale model and data equally**: 10× compute → **~3.2× each** (√10 ≈ 3.16).
- Rule of thumb: **~20 training tokens per parameter** is compute-optimal (cheapest route to a given loss — not a minimum).
- Proof: **Chinchilla 70B** (1.4T tokens) used the same compute as **Gopher 280B** and beat it, plus GPT-3 and MT-NLG. Existing big models were **undertrained**.

| Model | Params | Tokens | Tokens/param |
|-------|--------|--------|--------------|
| LaMDA | 137B | 168B | ~1.2 |
| GPT-3 | 175B | 300B | ~1.7 |
| Jurassic | 178B | 300B | ~1.7 |
| Gopher | 280B | 300B | ~1.1 |
| MT-NLG | 530B | 270B | ~0.5 |
| **Chinchilla** | **70B** | **1.4T** | **20** |

> 🧪 **Exam-style numerical.** Budget C = 6 × 10²³ FLOPs, Chinchilla-optimal (D = 20N).
> C = 6·N·D = 6·N·20N = 120 N² → N² = 5 × 10²¹ → **N ≈ 7 × 10¹⁰ (70B)**, **D ≈ 1.4 × 10¹² (1.4T tokens)**. That's Chinchilla itself.

### Scaling laws today (three axes)

| Axis | Spend more of… | What improves | Real example |
|------|---------------|--------------|-------------|
| Pre-training (**overtraining**) | Tokens, far beyond 20/param | Loss keeps falling (diminishing); smaller model is **cheaper to serve** | Llama 3 8B on ~15T tokens ≈ **1,900 tokens/param** |
| **Test-time compute** | Thinking tokens / repeated attempts at inference | Reasoning accuracy ≈ ∝ log(compute) | o1, DeepSeek-R1 improve when allowed to think longer |
| **RL training compute** (emerging) | RL steps on verifiable tasks (math, code) | Reasoning accuracy; responses grow longer | DeepSeek-R1-Zero's response length grew during RL |

> 🎯 Why overtrain past Chinchilla? Chinchilla minimises *training* cost. But a model is trained once and *served* millions of times, so a smaller model trained longer is cheaper overall.

---

## 8. Domain adaptation

D1 = general data, D2 = domain data (finance, medicine, law, code…).

| Route | How | Cost | When |
|------|-----|------|------|
| 1. Regular pre-training | Random weights, D1 only | — | General model, no domain depth |
| 2. **Continued pre-training (CPT)** | Take a D1-trained model, keep pre-training on D2 (+ some D1) | **Low — most common** | Default choice |
| 3. Domain pre-training from scratch | Random weights, D1 + D2 together | Very expensive | Only with a huge domain corpus + budget |

**Finance case studies:**

| | BloombergGPT (from scratch, 2023) | FinLLaMA (CPT, 2024) |
|---|---|---|
| Size | 50B | 8B (starts from Llama 3 8B) |
| Finance tokens | 363B | 52B |
| General tokens | 345B | 18B (finance : general ≈ **3 : 1**) |
| Notes | Size chosen with Chinchilla laws to fit the available data; needs big proprietary corpus | Inherits Llama 3's general knowledge; far fewer tokens |

> 🎯 Both **mix general data with domain data** so general skills aren't lost. CPT is the practical default.

---

## 9. Catastrophic forgetting

**Catastrophic forgetting** = when a network learns new data, weight updates overwrite what it knew. Worst when the new data has a different distribution.
*Example:* CPT Llama 3 only on finance → finance ↑, but general knowledge, coding and instruction-following ↓.

> 🌍 Cramming for a French exam so hard you start forgetting your Spanish.

| Mitigation | Idea | Notes |
|-----------|------|-------|
| **LoRA / PEFT** | Freeze base weights; train small adapters | Forgets less, but **learns less new knowledge**; best for fine-tuning |
| **Learning-rate schedule** | Re-warm to peak LR, then decay | Higher LR learns faster but forgets more; pair with replay |
| **Replay (data mixing)** | Mix some original general data into the new data | **Most effective, standard.** ~5% often enough; FinLLaMA used ~25% |

### LR recipe for CPT
**Repeat the original schedule: re-warm → re-decay → + replay.**
- **Warmup** — start small, ramp up, so first updates (fresh optimizer statistics) don't destabilise training.
- **Cosine decay** — lower the LR gradually so the model settles.
- **Why re-warm?** At the end of pre-training the LR is ~0, so the model can barely learn anything new unless you raise it again.
- Trade-off: higher peak LR = faster domain learning + more forgetting; replay offsets that. Together they can **match retraining from scratch at a fraction of the cost.**

> This is exactly what Assignment 1A uses (CPT on IT-helpdesk text, then QLoRA).

---

## 10. Modern recipes

All use next-token prediction (DeepSeek-V3 adds **multi-token prediction**). Differences are in data, staging and efficiency.

| | Llama 3.1 | Qwen3 | Gemma 2 | DeepSeek-V3 |
|---|---|---|---|---|
| Filtering (heuristics + model-based) | ✓ | ✓ | ✓ | ✓ |
| Synthetic data | ✓ | ✓ | ✗ | post-training |
| Data mixing | ✓ | ✓ | ✓ | ✓ |
| Long-context stage | ✓ | ✓ | ✗ | ✓ |
| High-quality final stage (annealing) | ✓ | ✓ | ✗ | — |
| Knowledge distillation | ✗ | post-training | ✓ | post-training |
| Efficiency (MoE, MTP, FP8) | — | — | — | ✓ |

- **Gemma 2:** 27B trained from scratch; 2B and 9B **distilled** (small student learns from a big teacher).
- **DeepSeek-V3:** MoE 671B (37B active), 14.8T tokens, MTP + FP8 ≈ 2.8M H800 GPU-hours.
- **OLMo 2** (AI2) publishes data, code and checkpoints — a fully open recipe.

### Llama 3 (405B) — three stages
1. **Initial:** ~15.6T tokens at 8K context. Batch grows 4M → 8M → 16M tokens (small early for stability, large later for efficiency).
2. **Long context:** 8K → 128K in six steps, ~800B tokens.
3. **Annealing:** final 40M tokens, LR → 0, upsample math/code. *The last data seen at low LR shapes the final weights.*

**Model-as-judge filtering:** Llama 2 labels a *sample* of documents high/low quality → train cheap classifiers (**fastText** = fast, **DistilRoBERTa** = better) → classifiers score the whole web corpus. Running Llama 2 on trillions of tokens would be too costly.

### Qwen3 — three stages
| Stage | Tokens | Focus |
|-------|--------|-------|
| S1 General | 30T+ | 4K context, **119 languages** |
| S2 Reasoning | ~5T more | more STEM, code, synthetic |
| S3 Long context | — | context → 32K (75% docs 16K–32K, 25% 4K–16K) |

Total **36T** tokens (2× Qwen2.5's 18T; 119 vs 29 languages). Data built by earlier models: Qwen2.5-VL extracts PDFs, Qwen2.5 cleans text, Qwen2.5-Math/Coder write synthetic textbooks/Q&A/code, every document is tagged (domain, educational value, safety) to tune the mix.

> 🎯 Takeaway: **earlier models build the data for the next generation.**

> 💬 **Session-3 lecture.**
> - Gemma 2 terms: the big model is the **teacher**, the distilled small ones are **students** (details in a later module).
> - Distillation is also why some labs are accused of training on rival models' outputs — it makes models cheaper to build. She noted the risk that new models inherit old models' mistakes; labs counter with humans in the loop and scripted checks.
> - Model-as-judge filtering is "a very interesting use of LLM as judge": an expensive model labels a sample, cheap classifiers (fastText first, then DistilRoBERTa) score everything.
> - High-quality data for annealing is scarce, "maybe humans involved".
> - **Read technical reports and model cards** (Llama 3 and Qwen3 have 100+ page reports; she demoed the Gemma 4 model card) — "information you would want to know before you start using any model".

---

## 11. What it costs

Using **C ≈ 6·N·D** (N = *active* parameters):

| Model | Size | Tokens | Compute | Hardware | GPU-hours | Precision |
|-------|------|--------|---------|----------|-----------|-----------|
| Llama 3.1 405B | 405B dense | 15.6T | ~3.8 × 10²⁵ FLOPs | up to 16K H100 | ~30.8M | BF16 |
| DeepSeek-V3 | 671B MoE (37B active) | 14.8T | ~3.3 × 10²⁴ FLOPs | 2,048 H800 | ~2.8M (2,048 × ~57 days) | FP8 mixed |

> 🧪 Check Llama: 6 × 405×10⁹ × 15.6×10¹² ≈ 3.8 × 10²⁵ ✔. DeepSeek: 6 × 37×10⁹ × 14.8×10¹² ≈ 3.3 × 10²⁴ ✔ — **~10× less compute** because MoE activates only 37B of 671B per token.

**Splitting work across GPUs (parallelism types):**
| Type | What's split |
|------|-------------|
| Data parallel | Different batches per GPU group |
| Tensor parallel | Each matrix multiply |
| Pipeline parallel | The layers |
| Context parallel | One long sequence |
| Expert parallel | MoE experts on different GPUs |

Llama 3 used tensor + context + pipeline + data. DeepSeek-V3 used pipeline + expert + data (no tensor).

> 💬 **Session-3 lecture.** Llama 3.1 405B ran ~70–80 days. Beyond GPUs you need whole servers (CPU, RAM, storage) plus cooling — hence the carbon footprint, and why only a few organisations can pre-train. **MoE** (Mixture of Experts) is "related to ensembling, but not ensembling": only some experts (37B of 671B params) run per token — covered later.

---

## 12. Emergent abilities

- **Definition:** "An ability is emergent if it is not present in smaller models but is present in larger models." Random performance until some scale, then well above random.
- Two properties: **sharpness** (appears suddenly) and **unpredictability** (at unforeseeable scales).
- **Counter-view (Schaeffer et al., 2023, "a mirage?"):** alleged emergence **evaporates with different metrics or better statistics** — may not be fundamental.

**Capabilities usually cited:**
1. **In-context learning** (GPT-3, 2020) — instruction / few examples in the prompt; **no weight updates.**
2. **Instruction following** — from instruction tuning; depends on data and post-training, not size alone.
3. **Chain-of-thought reasoning** — gains appeared around 60–100B params in early studies, but not a universal threshold; small models like Qwen3-4B/8B reason well through targeted training, RL and distillation.

> 💬 **Session-3 lecture.** Emergent abilities **don't follow scaling laws** — you can't extrapolate them from small models. The "mirage" paper shows how science works: "somebody comes with some claim and other researchers start validating or invalidating".

---

## 13. What you get: the base model

A **base model** has learned language, facts and patterns, but its default behaviour is to **continue text**, not to act as an assistant (no reliable instruction following or stopping).

| Prompt: "What is the capital of France?" | Output |
|---|---|
| Base model | "What is the capital of Germany? What is the capital of Italy? …" (continues a quiz list) |
| Instruct model | "The capital of France is Paris." |

On Hugging Face these ship separately: `Meta-Llama-3.1-8B` vs `Meta-Llama-3.1-8B-Instruct`; `Qwen3-8B-Base` vs `Qwen3-8B` (the plain name is the post-trained one for Qwen3).

> 💬 **Session-3 lecture.** *Why* does the base model ramble? Not "it mimics" — the **technical** answer: its objective is next-token prediction and quiz-style lists are common in the corpus. Try it yourself on base GPT-2, Llama 3.1 8B or Qwen3-8B-Base (older bases are "purer"). Hence fine-tuning is a "very important post-training step" — a pre-trained model alone "is not so useful". Closed models (GPT, Gemini…) can't be fine-tuned; only open-weight ones.

---

## ✅ Recap

- Pre-training = **self-supervised** next-token prediction (**CLM**) on trillions of tokens, with **teacher forcing**; quality measured by **cross-entropy / perplexity**.
- Data: **filter → de-dup → remove PII → tokenize + pack**; then tune the **mixture** and **curriculum**, end with **annealing**.
- **C ≈ 6ND.** Kaplan: grow model more than data. **Chinchilla: ~20 tokens/param.** Today: **overtrain** small models, plus test-time and RL scaling.
- Domain LLM: **CPT** is the default; fight **catastrophic forgetting** with **replay + re-warm/re-decay LR**.
- Output is a **base model** — it continues text; making it an assistant is Session 3.

**Self-check:**
1. Why does de-duplication protect benchmark scores from being fake?
2. Using C = 6ND, how many FLOPs to train a 1B model on 20B tokens? *(1.2 × 10²⁰)*
3. Why must the LR be re-warmed for continued pre-training?
4. Why is DeepSeek-V3 ~10× cheaper than Llama 3.1 405B despite having more parameters?
