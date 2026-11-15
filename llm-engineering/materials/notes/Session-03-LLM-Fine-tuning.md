# Session 3 — LLM Fine-tuning (IFT, PEFT, LoRA, QLoRA)

> **Deck:** `CS-3 LLM Fine tuning (1).pptx` (25 slides) · **Lecture:** 14-Nov-2026, 2h08m (transcript in `transcript/…session3.docx`)
>
> **One-line goal:** turn a base model (which only *continues* text) into one that **follows instructions**, cheaply — by training only a tiny add-on (**PEFT**: adapters, **LoRA**, **QLoRA**).
>
> **Taught in class:** the first ~50 min recapped and finished the pre-training deck (case studies → see [Session 2](Session-02-LLM-Pre-training.md), "💬 Session-3 lecture notes" boxes). Then CS-3 slides 3–19. **Quantization & QLoRA (slides 20–22) move to the next class**; model merging got only a short demo. They're summarised below from the deck so you're covered (and they're the core of Assignment 1A).

### Contents
1. [The kinds of "further training"](#1-the-kinds-of-further-training)
2. [In-context learning and its limits](#2-in-context-learning-and-its-limits)
3. [Instruction fine-tuning (IFT)](#3-instruction-fine-tuning-ift)
4. [Building IFT data (4 ways) + the JSON schema](#4-building-ift-data)
5. [Self-Instruct](#5-self-instruct)
6. [Why PEFT + the three PEFT families](#6-why-peft)
7. [Adapters (with worked numbers)](#7-adapters)
8. [Regular fine-tuning maths: the two-path idea](#8-regular-fine-tuning-maths)
9. [Low rank — the intuition](#9-low-rank--the-intuition)
10. [LoRA](#10-lora)
11. [Multi-tenant LoRA serving](#11-multi-tenant-lora-serving)
12. [Quantization & QLoRA *(next class)*](#12-quantization--qlora-next-class)
13. [Model merging *(demo only)*](#13-model-merging-demo-only)
14. [Assignment & logistics notes](#14-assignment--logistics-notes)
15. [Recap + self-check](#-recap)

---

## 1. The kinds of "further training"

```
pre-training data → design architecture → train → BASE model → fine-tuning data (usually labelled) → FINE-TUNED model
```

| Term | What it means | Labelled data? | Weights updated | Example |
|------|---------------|---------------|-----------------|---------|
| **Continued pre-training (CPT)** | Keep training on new *unlabelled* domain text with the **same LM objective** | No (self-supervised) | All | BioBERT; **Assignment 1A** |
| **Full fine-tuning** | Update **all** weights on the new task | Usually yes | All | Qwen/Qwen2.5-0.5B |
| **PEFT** | Update only a **small part** | Yes | Few | Llama-family adapters |
| **SFT** (supervised FT) | Train on input → output pairs | Yes | All or PEFT | Llama 2-Chat |
| **IFT** (instruction FT, a type of SFT) | Train on instruction → response pairs | Yes | All or PEFT | Llama 3.1 Instruct |
| **MLM fine-tuning** (type of SFT) | Adapt BERT-style encoders to a domain | — | — | DistilBERT (rarely used now) |

> 💬 "Nowadays SFT **is** IFT" (Jurafsky & Martin treat them as the same). A student corrected that CPT is **self-supervised**, not "unsupervised" — she agreed.
> 💬 Variants like Qwen2.5-Math / -Coder / -VL come from CPT or fine-tuning the base; the **model card / technical report** says which.

---

## 2. In-context learning and its limits

**In-context learning (ICL)** — put an instruction and maybe a few examples in the prompt; the model does the task. **No weights change** ("hence the name").
- **Zero-shot:** "Translate English to French: cheese →"
- **One-shot / few-shot:** add 1 or more solved examples first ("sea otter → loutre de mer").
- GPT-3 (175B) showed accuracy rises with the number of examples.

**Limits → why we fine-tune:**
1. Examples use context tokens **on every call** (cost + space).
2. **Nothing persists** — next call, the model has learned nothing.
3. Painful in **agentic systems**, which make many LLM calls.

> 🌍 ICL = giving a temp worker a cheat-sheet every morning. Fine-tuning = training them once so they just *know*.

---

## 3. Instruction fine-tuning (IFT)

| | Base model | Instruct model |
|---|---|---|
| Prompt "What is 1+1?" | continues the text (more questions, rambling) | "2" |
| Behaviour | **next-word prediction** | **instruction following** |

**Why does the base model ramble?** (she pushed for the *technical* answer) — the pre-training objective is next-token prediction, and quiz-style lists are common in the corpus. Pre-training flattens everything into running text with no question/answer boundaries. It's **not** a lack of data.

IFT trains on many tasks (QA, summarisation, sentiment…) each written as *instruction / input / output*, so the model learns the general habit of "do what the instruction says" — even for new instructions.

> 💬 IFT is **not** about extending context length; its aim is instruction following. There's no rule-of-thumb dataset size — don't go too small for the model size, and watch for overfitting (one reason PEFT is used).

---

## 4. Building IFT data

| Method | How | Example |
|--------|-----|---------|
| **Human authoring** | Experts write instruction–response pairs from scratch | Databricks **Dolly-15K** |
| **Template conversion** | Rewrite existing labelled NLP datasets (e.g. SQuAD) into instruction format | **FLAN** |
| **Synthetic generation** | A stronger teacher LLM (Llama 3.1 405B, GPT-4) writes instructions/answers | **Alpaca** (52K from text-davinci-003) |
| **Hybrid pipeline** | Small gold set → synthetic expansion → **validate/filter** → final set | **Self-Instruct** (175 seeds → 52K) |

Stored as **JSONL** (one JSON record per line), loaded with `load_dataset("json", ...)`.

> 💬 Synthetic data is cheap now ("pay some money" to a strong LLM). The real bottleneck is **fine-tuning infrastructure** (GPUs).

### Three layers of the same example (slide 9)

**1. Raw data (SQuAD 2.0):**
```
Context : The Eiffel Tower is located in Paris, France. It was constructed between 1887 and 1889. It stands 330 metres tall.
Question: When was the Eiffel Tower built?
Answer  : between 1887 and 1889
```

**2. Stored schema — model-agnostic JSON (never changes whichever model you train):**
```json
{
  "instruction": "Answer the question using only the information in the context. If the answer is not present, say 'The answer is not present in the provided context.'",
  "input": "Context: The Eiffel Tower is located in Paris, France. ...\n\nQuestion: When was the Eiffel Tower built?",
  "output": "The Eiffel Tower was built between 1887 and 1889.",
  "task_type": "question_answering",
  "source_dataset": "squad_v2"
}
```

**3. Template rendering — model-specific (Mistral Instruct):**
```
<s>[INST] Answer the question using only the information in the context. ...
Context: ... Question: When was the Eiffel Tower built? [/INST]
The Eiffel Tower was built between 1887 and 1889.</s>
```

> 🎯 Keep the **stored schema** separate from the **chat template**. Switch models → re-render, don't rebuild the dataset. (The assignment asks you to take raw data, pre-process it, and convert it to JSON like this.)

---

## 5. Self-Instruct

A semi-automated way to instruction-tune using signals **from the model itself** (base = GPT-3).

```
175 human seed tasks (1 instruction + 1 instance each) = task pool
   │
   ├─1. LLM generates a NEW instruction  ("Give me a quote from a famous person on this topic")
   ├─2. Is it a classification task?  (a simple classifier can decide)
   ├─3. LLM generates instances:
   │      • non-classification → input first, then output  (topic "importance of being honest" → quote)
   │      • classification     → class label first, then input  (e.g. stance "favor/against")
   ├─4. Filter / validate (scripts) → drop low-quality and near-duplicates
   └─5. Add survivors back to the task pool → repeat   ⇒ ~52K examples
```

> 🌍 A teacher writes 175 sample questions; a bright student invents thousands more in the same style; a strict checker throws out the bad ones.

---

## 6. Why PEFT

**"GPUs don't grow on trees."**
1. Full fine-tuning a huge model (e.g. GPT-3 175B, all parameters, several epochs) is infeasible on normal hardware.
2. Every fine-tuned copy is as big as the original → one full copy per task is very expensive to store and serve.

> 💬 "Nobody does the full fine-tuning nowadays."

**PEFT** = adapt a big pre-trained model by tuning only a **small subset** of parameters.

| Family | Idea | Methods |
|--------|------|---------|
| **Addition** | Add new trainable modules | Prompt tuning, prefix tuning, **adapters** |
| **Selective** | Tune a chosen subset of existing weights | Layer freezing, BitFit (biases only), diff pruning |
| **Reparameterization** | Learn the update in a cheaper form | **LoRA** |

(Many LoRA variants exist; only the core concept is examinable.)

---

## 7. Adapters

- **Lightweight trainable modules inserted into each Transformer block** (e.g. after multi-head attention and after the FFN). The backbone is **frozen**; only adapters train. They learn task-specific patterns.
- **Bottleneck adapter** = a tiny one-hidden-layer MLP:

```
x (dim d) ──► down-project (d → m) ──► nonlinearity (ReLU…) ──► up-project (m → d) ──► + x   (residual)
```

> 🧪 **Worked numbers (from class).** d = 1024, bottleneck m = 24.
> Adapter = 1024×24 + 24×1024 = **49,152** weights (ignoring biases).
> A full 1024×1024 layer = **1,048,576**. → adapter is **~4.7%** of one layer. (24 is a design choice.)

> 💬 The block's own FC layer is untouched and frozen; the adapter is an *extra* FC → nonlinearity → FC with different dimensions.
> Downside: adapters add layers in the forward path → slightly slower inference (LoRA avoids this — see §10).

---

## 8. Regular fine-tuning maths

> 🎯 She called this "**very important** — simplifies a lot your understanding of LoRA".

A layer computes **h = W x**. A gradient step gives the update:

  **ΔW = α (−∇L_W)**  **W′ = W + ΔW**

Next forward pass: **h = (W + ΔW) x = W x + ΔW x**

So you can think of it as **two paths**: the frozen original **Wx** plus an update path **ΔWx**.

**Problem:** ΔW is the **same size as W** (e.g. 4096 × 4096 ≈ 16.8M numbers per matrix). Training ΔW directly = full fine-tuning.

---

## 9. Low rank — the intuition

```
       ⎡10  20  30⎤
ΔW =   ⎢20  40  60⎥     row 2 = 2 × row 1,  row 3 = 0.5 × row 1
       ⎣ 5  10  15⎦
```

- 9 numbers stored, but only **one unique row** of information (10, 20, 30) → **rank = 1**.
- It can be written as a column × a row: **[1, 2, 0.5]ᵀ × [10, 20, 30]** → 3 + 3 = **6 numbers instead of 9**.
- **Rank** = number of truly independent rows/columns. Related to **PCA / SVD**: approximate a big matrix with a few important directions.

**The LoRA hypothesis (empirically confirmed):** the *update* ΔW during fine-tuning is **low-rank** — the pre-trained model already knows language, and a small fine-tuning set only nudges it in a few directions.

> 🌍 A 4K photo of a clear blue sky has millions of pixels, but you could describe it with "blue, slightly lighter at the top". Lots of numbers, little information.

---

## 10. LoRA

**Low-Rank Adaptation:** don't learn ΔW; learn two thin matrices whose product approximates it.

  **ΔW = B · A**  with  **A ∈ ℝ^(r×k)** (down-projection), **B ∈ ℝ^(d×r)** (up-projection), **r ≪ d, k**

  **h = W x + (α / r) · B A x**

```
          h
          ▲
   ┌──────┴──────┐
   │      +      │
 [ W  frozen ]  [ B  (d×r), init 0 ]
   ▲             ▲
   │          [ A  (r×k), init N(0,σ²) ]
   └──── x ──────┘
```

| Detail | Why |
|--------|-----|
| **W frozen**; only A and B train | Few trainable params, base untouched |
| **B = 0 at start**, A random | BA = 0 → the model starts **exactly** as the pre-trained one |
| **r** (rank) is a hyperparameter, e.g. 8 | Bigger r = more capacity, more params |
| **α** (scaling) | How much weight the LoRA path gets in the output (α/r > 1 amplifies, < 1 dampens — "kind of regularising") |
| Divide by **r** | Mathematical convenience — lets you change r without re-tuning α |
| Backward pass | Gradients flow through both paths, but **only A and B update** (simultaneously) |
| **A + B = the "LoRA adapter"** | You choose which layers get one (commonly the attention Q, K, V, O projections) |

> 🧪 **Parameter saving.** W is 4096 × 4096 = **16,777,216**. With r = 8: A = 8×4096, B = 4096×8 → **65,536** trainable = **0.39%** of W (**99.6% fewer**).
> Formula to memorise: **LoRA params = r × (d + k)** vs full **d × k**.

**Why LoRA beats adapters at inference:** after training you can **merge**: W′ = W + (α/r)·BA → same shape as W → **zero extra latency**. Quality "matches full fine-tuning".

> 💬 Does LoRA *add* parameters? Yes, A and B are new, so the total grows slightly — but only they are trained. It's a **re-parameterisation of ΔW**. (PCA is just intuition; training is still backprop.)

**LoRA fine-tuning process (slide 18):** load base model (frozen) → attach LoRA adapters to chosen layers → train on task data (only A, B update) → save the **small adapter file** (MBs, not GBs) → at inference, load base + adapter, or merge.

---

## 11. Multi-tenant LoRA serving

```
           ┌─ + B₁A₁ → Task 1 (e.g. legal QA)
W₀ (one) ──┼─ + B₂A₂ → Task 2 (e.g. HR chatbot)
           └─ + B₃A₃ → Task 3 …
```

- **One base model in GPU memory + N tiny adapters**, swapped per request, instead of N full fine-tuned copies.
- Huge saving in storage and serving cost.

> 💬 Demo: the Llama 3 8B page on Hugging Face lists community **Adapters** (LoRA/QLoRA), **Finetunes** and **Merges** — "tomorrow you can also publish".

---

## 12. Quantization & QLoRA *(next class)*

**Quantization** = storing weights at lower precision (e.g. 32-bit float → 8-bit int → 4-bit) to cut memory and latency.

> 🧪 Memory per parameter: FP32 = 4 bytes, BF16/FP16 = 2, INT8 = 1, 4-bit = 0.5.
> A 7B model: FP32 ≈ 28 GB, BF16 ≈ 14 GB, **4-bit ≈ 3.5 GB** → fits on a free/student GPU.

**QLoRA = LoRA on a 4-bit quantized base model.**
- Frozen base stored in **4-bit NF4**; LoRA adapters A, B trained in **BF16** (FP16 on GPUs without BF16, e.g. T4).
- **Forward pass:** 4-bit weights are **dequantized to BF16 on the fly** for each matmul, then discarded — only the 4-bit copy stays in memory.
- **Backward pass:** gradients flow through the frozen weights into A and B; only A and B update.
- **Result:** a **65B model fine-tuned on a single 48 GB GPU**, matching 16-bit fine-tuning quality.

**Three tricks that make it work:**

| Trick | What it does |
|-------|-------------|
| **4-bit NormalFloat (NF4)** | Weights are roughly normal (bell-shaped), so the 16 levels sit at normal-distribution quantiles — **more levels near zero**, where most weights are |
| **Double quantization** | Each block of 64 weights needs an FP32 scale constant (32/64 = **0.5 bits/param** overhead). Quantize those constants to 8-bit → **~0.127 bits/param** (~3 GB saved on 65B) |
| **Paged optimizers** | Optimizer states use CUDA unified memory and **spill to CPU RAM** on memory spikes (long sequences) → no out-of-memory crash |

> 🌍 QLoRA = keeping a huge encyclopaedia as a compressed zip (4-bit), unzipping just the page you need when you read it, and writing your notes on sticky notes (LoRA) instead of editing the book.

> 🎯 Assignment 1A = CPT then **QLoRA** fine-tuning — this slide is what you implement.

---

## 13. Model merging *(demo only)*

- **Combine two or more compatible fine-tuned models/adapters into one model.** Works best when they share the **same base architecture** (often the same base checkpoint).
- Unlike **ensembling** (run several models, combine outputs), merging yields **one deployable model** → inference cost doesn't grow with the number of sources.
- Simplest method: **linear weight averaging** of corresponding parameters.
- **Model Soups** paper: averaging several fine-tuned models improves accuracy and robustness **without extra inference time**.
- Other methods exist (e.g. **SLERP**, shown via a LazyMergekit merge of Llama 3 on Hugging Face).

---

## 14. Assignment & logistics notes

- **Assignment preference (1A or 1B) via Google Form by 19-Nov**; otherwise assigned randomly. Start now — don't wait for the Taxila upload.
- **Assignment 1 deadline: 19-Dec.** "Deadlines will not be changed."
- Enterprise use cases/datasets listed are **examples** — you may combine sources or use your own; **state your source**.
- Single-PDF datasets are OK if the rubric allows, but too little data on a billion-parameter model gives "very weird results" and catastrophic forgetting.
- Pipeline: raw source → pre-process → JSON (§4).
- **Webinar 1** (next week): remote lab, Hugging Face, keys, **CPT demo**. **Webinar 2:** LoRA fine-tuning in "a few lines of code" + decoding.
- Classes give concepts, webinars give "80%" of the implementation, you "think and infer" the rest. LFs grade against the rubric.
- **Exam:** the past question paper and problem material will come with the session 8 slides; **session 8 has one hour "from the exam point of view"**.
- **Next class:** QLoRA + quantization, then architecture. Later: distillation, MoE, precision (BF16/FP8), inference.

---

## ✅ Recap

- **CPT** = more pre-training on domain text (no labels). **SFT/IFT** = labelled instruction→response pairs → instruction following.
- **ICL** needs no training but costs context on every call and persists nothing.
- IFT data: human / template / synthetic / **hybrid (Self-Instruct)**; store as **model-agnostic JSONL**, render with the model's chat template.
- **PEFT** families: addition (adapters, prompt/prefix tuning), selective (BitFit), reparameterization (**LoRA**).
- **h = Wx + ΔWx** → LoRA makes ΔW = **B·A** (rank r), **B = 0** at start, scale **α/r**, params **r(d+k)**.
- **QLoRA** = 4-bit **NF4** base + BF16 LoRA + **double quantization** + **paged optimizers**.
- One base + many adapters = **multi-tenant serving**; merging = one model from many.

**Self-check:**
1. Why is B initialised to zero and not A?
2. d = k = 2048, r = 16: how many LoRA params per matrix, and what % of W? *(65,536 · 1.56%)*
3. Why does LoRA add **no** inference latency after merging, while adapters do?
4. What does double quantization quantize?
5. Base vs instruct model — explain the rambling in one technical sentence.
