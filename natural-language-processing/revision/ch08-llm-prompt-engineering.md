# Ch 8 — LLMs, Prompt Engineering, Generative AI and Transfer Learning
**Session 8** (the LLM section of the *Session 5* deck and the closing section of
the pre-midsem handout, *Sessions 1–8*)

**Theory only — no numericals.** Cheap marks, one focused hour. The three things
that get asked: **the traditional-ML vs LLM-development comparison**, **zero-shot
vs few-shot in-context learning**, and **transfer learning vs fine-tuning**.

---

## 1. Large Language Models

An LLM is a language model (Ch 4's task — predict the next word) scaled up to
billions of parameters and trained on a very large corpus, so that it acquires
grammar and a great deal of world knowledge as a side effect.

### ⭐ Traditional ML vs LLM development — the comparison table

| | **Traditional ML** | **LLM development** |
|---|---|---|
| Expertise | Need **ML knowledge** | Use a **pre-trained model / API** |
| Data | **Collect training data** | **No large dataset needed** |
| Model | Choose and **train a model** | **No training from scratch** |
| Resources | More **time + GPU / hardware** | Far less |
| The work | **Minimize a loss function** | **Focus on prompt writing** |

> **The one-line summary:** LLMs move the effort from *training a model* to
> *writing an instruction*.

### Benefits and use cases
Benefits: no training run, no labelled data, fast to prototype, one model serves
many tasks. Typical use cases: summarization, question answering, classification,
translation, code generation, information extraction, conversational assistants.

---

## 2. Prompt engineering

### What is a prompt?

> A **prompt** refers to the **input or query provided to the AI model to generate
> a response**. It can be a sentence, a question, or a combination of multiple
> sentences. **The prompt sets the context and guides the model in understanding
> the desired task or the information it needs to generate its response.**

### Prompts and completions
```
    PROMPT  ---->  [ model ]  ---->  COMPLETION

    prompt     = what you send in
    completion = what the model generates back
```

### What is prompt engineering?
The practice of designing and refining prompts so the model produces the output
you want — choosing the wording, the format, the context supplied, and the
examples included.

---

## 3. ⭐ In-context learning: zero-shot and few-shot

**In-context learning** = the model learns what you want **from the prompt
itself**, without any weight updates. Nothing is trained; the examples simply sit
in the context window.

| | **Zero-shot inference** | **Few-shot inference** |
|---|---|---|
| Examples in the prompt | **None** | **A few** (typically 1–5) |
| What you give | The instruction only | The instruction **plus worked examples** |
| Use when | The task is common and clearly describable | The task is unusual, or you need a **specific output format** |

**Zero-shot:**
```
    Classify the sentiment of this review as positive or negative.
    Review: "The battery lasted two days. Excellent."
    Sentiment:
```

**Few-shot:**
```
    Review: "Screen cracked in a week."      Sentiment: negative
    Review: "Arrived early and works great." Sentiment: positive
    Review: "The battery lasted two days. Excellent."
    Sentiment:
```

> **The key point:** in **neither** case are any model weights updated. This is
> the crucial contrast with **fine-tuning** in §5, and it is exactly the
> distinction the POS-tagging slides in Ch 7 were drawing.

---

## 4. Generative AI

**Generative AI** = models that produce **new content** — text, images, code,
audio — rather than only classifying or scoring existing content.

### Applications named on the slides

**AI assistants, in increasing order of capability:**

| Level | What it does |
|---|---|
| **Notification Assistant** | Pushes information at you |
| **FAQ Assistant** | Answers known questions |
| **Contextual Assistant** | Uses the conversation's context |
| **Personalized Assistant** | **Knows you in much more detail** — e.g. quickly checks a few final things before giving a quote tailored to your actual situation |
| **Autonomous Organization of Assistants** | A **group of AI assistants that know every customer personally**, eventually running large parts of company operations — lead generation, marketing, sales, HR, finance |

Other examples on the slides: **PaintBox** (generative imagery) and **CodeAid**
(code generation).

---

## 5. ⭐ Transfer learning and fine-tuning

### The problem this solves

**Real-life challenges in NLP tasks:**
- Deep learning methods are **data-hungry** — **>50K data items** needed for
  training.
- The **distributions of the source and target data must be the same**.
- **Labelled data in the target domain may be limited.**

> **This problem is typically addressed with transfer learning.**

### Transfer learning

> Using a **pre-trained model as a starting point** for a new task or domain.
> Leverage the knowledge the model acquired on a large dataset and apply it to a
> **related task with a smaller dataset**. We benefit from the general features
> and patterns it already learned, **saving time and computational resources**.
>
> Transfer learning involves **freezing the pre-trained model's weights and only
> training the new layers**.

**Example from the slides:** in image classification, knowledge gained while
learning to recognise **cars** could be applied when trying to recognise
**trucks**.

### Transductive vs inductive transfer

| | **Transductive transfer** | **Inductive transfer** |
|---|---|---|
| Labelled target-domain data | **None available** | **Available** |
| Goal | Adapt to the new domain | **Improve performance on the target task by training on other task(s)** |
| Examples | **Domain adaptation** — the focus of most transfer research in NLP | **Multi-task learning** (jointly training on >1 task); **pre-training** (e.g. word embeddings) |

> **Mnemonic:** trans**D**uctive = **D**omain adaptation, no target labels.
> **In**ductive = labels are **in** hand.

### Fine-tuning — how it differs from transfer learning

> **Fine-tuning takes it a step further by allowing the pre-trained layers to be
> updated.**
>
> Beneficial when the new dataset is **large enough** and **similar** to the
> original dataset the model was pre-trained on.

| | **Transfer learning (feature extraction)** | **Fine-tuning** |
|---|---|---|
| Pre-trained weights | **Frozen** | **Updated** |
| What trains | Only the **new layers** you added | The **whole model** (or its upper layers) |
| Needs | A small dataset is fine | A **large enough**, **similar** dataset |

> **Exam trap.** These two are constantly confused. The single distinguishing
> question is: **are the pre-trained weights allowed to change?**
> Frozen → transfer learning. Updated → fine-tuning.
> And a third option — **neither**, because nothing is trained at all → that is
> **in-context learning / prompting** (§3).

### Applications of transfer learning
Image classification · **Named entity recognition** · **Sentiment analysis** ·
**Cross-lingual learning** · Gaming · Image recognition · Speech recognition.

---

## 6. The three ways to make a model do your task — the mental model

```
            NO WEIGHTS CHANGE            SOME WEIGHTS CHANGE       ALL/MOST CHANGE
    ┌─────────────────────────┐  ┌──────────────────────┐  ┌────────────────────┐
    │  PROMPTING              │  │  TRANSFER LEARNING   │  │  FINE-TUNING       │
    │  (in-context learning)  │  │  (feature extraction)│  │                    │
    │                         │  │                      │  │                    │
    │  zero-shot / few-shot   │  │  freeze the backbone,│  │  unfreeze and      │
    │  examples live in the   │  │  train only the new  │  │  update pre-trained│
    │  prompt                 │  │  head layers         │  │  layers too        │
    │                         │  │                      │  │                    │
    │  data needed: none      │  │  data: small         │  │  data: large AND   │
    │                         │  │                      │  │  similar to source │
    └─────────────────────────┘  └──────────────────────┘  └────────────────────┘
             cheapest  <---------------------------------------->  most capable
```

If you remember only one diagram from this chapter, make it that one — it
organises Ch 7 §3–4 as well.

---

## 7. Quick recall table (cover the right column)

| Question | Answer |
|---|---|
| In traditional ML you minimise a loss function; in LLM development you…? | **Focus on prompt writing** |
| What is a prompt? | The input/query given to the model, which **sets the context and guides** it toward the desired task |
| What is a completion? | What the model generates in response |
| Zero-shot inference? | Instruction only, **no examples** in the prompt |
| Few-shot inference? | Instruction **plus a few worked examples** in the prompt |
| Are weights updated in in-context learning? | **No** |
| How much data do DL methods typically need? | **>50K** data items |
| Transfer learning is? | Using a **pre-trained model as a starting point** for a new task/domain |
| In transfer learning, what happens to the pre-trained weights? | They are **frozen**; only the new layers train |
| Fine-tuning differs how? | It **allows the pre-trained layers to be updated** |
| When is fine-tuning beneficial? | When the new dataset is **large enough** and **similar** to the original |
| Transductive transfer? | **No** labelled target-domain data — e.g. domain adaptation |
| Inductive transfer? | Labelled target data **is** available — e.g. multi-task learning, pre-training |
| Which is the focus of most NLP transfer research? | **Transductive** (domain adaptation) |
| Five applications of transfer learning? | Image classification, NER, sentiment analysis, cross-lingual learning, speech recognition |
| Generative AI is? | Models that produce **new content** rather than only classifying |

---

## 8. You try
*Attempt on paper before scrolling. Answers at the very bottom.*

**Q1.** For each scenario, choose **prompting**, **transfer learning** or
**fine-tuning**, and justify in one line:
(a) You have 200 labelled legal contracts and need a clause classifier.
(b) You have 500,000 labelled medical notes and need the highest possible
accuracy on medical NER.
(c) You need to summarize 30 news articles today and have no labelled data.

**Q2.** State the single question that distinguishes transfer learning from
fine-tuning.

**Q3.** Classify each as **transductive** or **inductive** transfer:
(a) Training a sentiment model on product reviews and applying it to restaurant
reviews, with no restaurant labels.
(b) Jointly training a model on POS tagging and NER to improve NER.
(c) Initialising a model with pre-trained word embeddings.

**Q4.** Write a **zero-shot** and then a **few-shot** prompt for the task
"extract the company name from a news headline". State one reason to prefer the
few-shot version.

**Q5.** In three sentences, contrast traditional ML development with LLM
development along the axes of data, compute and the developer's main activity.

---

## Pre-midsem is now complete
Chapters 1–8 cover the whole pre-midsem syllabus. What is left is not reading,
it is **speed** — the "You try" sections you have not attempted, and one timed
pass over the Viterbi table in [`ch06`](ch06-pos-tagging-hmm-viterbi.md) and the
smoothing table in [`ch04`](ch04-ngram-language-models.md).

Post-midsem picks up at **Session 9 — Parsing**:
[`../notes/parsing/README.md`](../notes/parsing/README.md).

---
---
---

<!-- ANSWERS BELOW - stop scrolling until you have attempted -->

## Answers

**A1.**
(a) **Transfer learning.** 200 examples is far too little to update a large
model's weights without overfitting, so freeze the pre-trained backbone and train
only a small classification head on top.
(b) **Fine-tuning.** The dataset is large (well above the >50K threshold) and
similar in kind to the pre-training text, which is exactly the condition the
slides give for fine-tuning being beneficial — and unfreezing the pre-trained
layers is what buys the last few points of accuracy.
(c) **Prompting.** There is no labelled data and only 30 items, so any training
run would cost more than it saves; a zero-shot instruction to a pre-trained LLM
does the job with no weight updates at all.

**A2.**
**Are the pre-trained weights allowed to change?**
Frozen → transfer learning. Updated → fine-tuning.

**A3.**
(a) **Transductive** — no labelled data in the target domain; this is domain
adaptation, the focus of most NLP transfer research.
(b) **Inductive** — labelled target-task data is available, and the goal is to
improve the target task by training on another task (multi-task learning).
(c) **Inductive** — pre-training is listed explicitly as an inductive-transfer
example.

**A4.**
*Zero-shot:*
```
    Extract the company name from the following news headline.
    Output only the company name.
    Headline: "Acme Corp shares fall 8% after weak guidance"
    Company:
```
*Few-shot:*
```
    Headline: "Globex to acquire rival for $2bn"          Company: Globex
    Headline: "Initech faces antitrust probe in the EU"   Company: Initech
    Headline: "Acme Corp shares fall 8% after weak guidance"
    Company:
```
**Reason to prefer few-shot:** the examples pin down the **output format** — bare
company name, no explanation, no punctuation — which a zero-shot instruction
often fails to enforce consistently across 30 headlines.

**A5.**
*Data:* traditional ML requires you to collect and label a training set (deep
learning typically needs >50K items), whereas LLM development needs no large
dataset because the model is already pre-trained.
*Compute:* traditional ML needs substantial time and GPU hardware for a training
run, while LLM development calls a pre-trained model or API and trains nothing
from scratch.
*Main activity:* the traditional ML developer chooses an architecture and
minimises a loss function; the LLM developer **writes and refines prompts**.
