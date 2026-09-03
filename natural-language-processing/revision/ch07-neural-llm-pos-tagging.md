# Ch 7 — Neural, LLM and Agentic Approaches to POS Tagging
**Session 7** (deck: *NLP Session 7 — Neural LLM Agentic approaches to POS tagging*)

**Theory only — no numericals.** This is the "modern methods" companion to
Chapter 6. It is short, and the marks in it are pure recall: know the four
approaches, their accuracy figures, and one pro/con for each.

The story in one line: **HMM → Bi-LSTM-CRF → Transformer/BERT → LLM prompting →
LLM agent**, with accuracy climbing from ~96% to ~99% and the *effort* moving
from feature engineering, to architecture, to prompt writing.

---

## 1. Bi-LSTM-CRF — the go-to neural baseline for sequence tagging

**Concept:** combine a powerful **feature extractor** (Bi-LSTM) with a
**structured prediction layer** (CRF) to ensure **valid tag sequences**.

```
    Input layer   :  Word embeddings (word2vec, GloVe)
                     + CHARACTER embeddings  <- these handle unknown words
                          |
    Bi-LSTM layer :  processes the sentence FORWARD and BACKWARD
                     captures long-range dependencies + bidirectional context
                          |
    CRF layer     :  structured decoder — learns tag-sequence constraints
                          |
    Output        :  the highest-scoring tag sequence for the WHOLE sentence
```

### What each piece contributes

| Layer | Job | Why it matters |
|---|---|---|
| **Character embeddings** | Sub-word representation | **Handles unknown words** — a word ending in *-ing* looks verb-like even if never seen |
| **LSTM** | Gated recurrent unit | Solves the **vanishing gradient** problem of simple RNNs, using **gates: Input, Forget, Output** |
| **Bidirectional** | Reads left→right and right→left | The tag for *bank* in *"I walked to the river bank."* depends on both **river** (left context) and **.** (right context) |
| **CRF** | Structured decoder | Learns constraints such as *"a Verb is unlikely to follow a Determiner"*, and finds the sequence with the highest **overall** probability across the entire sentence |

### Why the CRF layer instead of just picking the best tag per word

> Instead of just picking the highest-probability tag at each word — **which can
> lead to impossible sequences** — the CRF layer scores whole paths:
```
                     exp( score of the true tag path )
    P(y | x)  =  ---------------------------------------
                  Σ_{all possible paths} exp( score )

    Goal: MAXIMISE the numerator (score of the true path)
          relative to ALL possible paths.
```
> This is the same instinct as Viterbi in Chapter 6 — optimise the **whole
> sequence**, not each position greedily.

### Performance

| | |
|---|---|
| **Typical accuracy** | **~97–98% on the Penn Treebank** |
| **Pros** | Highly accurate; **automatically learns features** (no hand-engineering); good for **low-resource languages** with transfer learning |
| **Cons** | **Slower training** than non-recurrent models; **replaced as SOTA by Transformers** |

---

## 2. The Transformer

**Key idea:** **replaces recurrence (RNN/LSTM) with the self-attention
mechanism.**

> **Self-attention** allows the model to weigh the relevance of **every other word
> in the sentence simultaneously, regardless of distance**.
>
> Example: when tagging *"He"*, the model instantly links it to *"ran"* and
> *"ball"* equally well — an LSTM would have to carry that information step by
> step.

**Architecture:** multi-layer **Encoder blocks**, each consisting of
**Multi-Head Attention** + **Feed-Forward Networks**.

> **The one-line contrast to memorise:** an LSTM's path length between two words
> grows with their distance; a Transformer's is **constant (1 hop)** for every
> pair. That is why it beats recurrence on long-range dependencies **and** is far
> more parallelizable.

---

## 3. POS tagging with pre-trained models (BERT, RoBERTa)

**Method: fine-tuning a Pre-trained Language Model (PLM).**

```
    STAGE 1 — PRE-TRAINING (done once, by someone with a data centre)
        The model learns grammar and world knowledge on TRILLIONS of words,
        e.g. by predicting MASKED words.

    STAGE 2 — FINE-TUNING (what you do)
        Add a simple CLASSIFICATION LAYER on top of the PLM's output vectors.
        Train the entire model for a FEW EPOCHS on the specific POS corpus.

    OUTPUT
        A highly CONTEXTUALIZED vector per token, which the final layer maps
        to the appropriate tag.
```

### Advantages and impact

| | |
|---|---|
| **SOTA performance** | **~98.5–99.5% accuracy** |
| **Efficiency** | Highly **parallelizable** — faster training than RNNs |
| **Context** | Captures the deepest contextual meaning, **solving nearly all lexical ambiguity issues** |
| **Impact** | The standard for POS tagging in modern libraries: **spaCy** and **Hugging Face Transformers** |

> Tie this back to Ch 2: these are **contextual embeddings**. *bank* gets a
> different vector in *river bank* and *money bank*, which is exactly why lexical
> ambiguity (Ch 1) largely stops being a problem.

---

## 4. Prompting — POS tagging with an LLM

**Concept:** leverage the vast linguistic knowledge and **zero-shot
capabilities** of Large Language Models (e.g. GPT-4, Llama).

> **Traditional fine-tuning is replaced by prompting**: the POS task is framed as
> a **natural language instruction**.

Example prompt from the slides:
```
    "Tag the following sentence using the Penn Treebank tagset.
     Output only the word/tag pairs.
     Sentence: The concert was great."
```

**Zero-shot / few-shot learning:** the LLM can tag a sentence accurately
**without being explicitly fine-tuned on any POS corpus**, based solely on its
general pre-training.

> **The shift to notice:** with BERT you still needed a *labelled POS corpus* and
> a training run. With prompting you need **neither** — only a well-written
> instruction. That is the whole argument of Chapter 8.

---

## 5. LLM agents and system integration

> **LLM Agent** = an LLM that is given the ability to **use external tools** to
> complete a task.

### The POS agent flow

```
1. INPUT       User gives a complex request:
               "Analyze the sentiment of all nouns in the user reviews."
                        |
2. LLM AGENT   Breaks the task down into sub-tasks.
                        |
3. TOOL USE    For the labelling sub-task, the agent decides to call a
               specialised, FAST POS tagger (e.g. a fine-tuned BERT model)
               as a TOOL.
                        |
4. INTEGRATION The agent feeds the tags back into its context and performs
               the final task — sentiment analysis on the words tagged NN.
```

**Benefit:** combines the LLM's **reasoning / planning ability** with the
**speed and accuracy** of a specialised POS model.

---

## 6. Conclusion — "is modern POS tagging solved?"

The slides' own answer:

- The task has achieved **near-human performance** thanks to deep learning.
- **Current SOTA:** fine-tuned Transformer models (BERT / RoBERTa).
- **Future trend (LLMs):** POS tagging is becoming an **internal utility** inside
  larger LLM agent systems.
- **The focus shifts** from *how to build the best tagger* to **how to use tags to
  power complex downstream AI systems.**

---

## 7. ⭐ The summary table (this is the chapter)

| Approach | Mechanism | Accuracy | Key strength | Key weakness |
|---|---|---|---|---|
| **HMM + Viterbi** (Ch 6) | Generative, transition × emission | ~95–96% | Simple, interpretable, fast | Word identity only; unknown words; left-to-right |
| **MEMM** (Ch 6) | Discriminative logistic regression per position | ~96–97% | Arbitrary features | Still needs feature engineering |
| **Bi-LSTM-CRF** | Bi-LSTM feature extractor + CRF structured decoder | **~97–98%** | Learns features automatically; char embeddings handle OOV | Slow to train; superseded |
| **BERT / RoBERTa fine-tuned** | Self-attention encoder + classification head | **~98.5–99.5%** | Deepest context; parallelizable; **current SOTA** | Needs a labelled corpus + a training run; large model |
| **LLM prompting** | Natural-language instruction, zero/few-shot | — | **No fine-tuning and no labelled corpus at all** | Slower and costlier per sentence; less predictable |
| **LLM agent** | LLM plans; calls a fast tagger as a tool | — | Reasoning + speed combined | Most complex system |

---

## 8. Quick recall table (cover the right column)

| Question | Answer |
|---|---|
| What does the Bi-LSTM contribute? | Bidirectional context + long-range dependencies |
| What does the CRF layer contribute? | Valid tag **sequences** — learns constraints, scores whole paths |
| Why character embeddings? | To **handle unknown words** |
| What problem do LSTM gates solve, and what are they? | **Vanishing gradients**; Input, Forget, Output |
| Bi-LSTM-CRF accuracy on Penn Treebank? | ~97–98% |
| Two cons of Bi-LSTM-CRF? | Slower training; replaced as SOTA by Transformers |
| Transformer's key idea? | Replaces recurrence with **self-attention** |
| What does self-attention let you do? | Weigh every other word **simultaneously, regardless of distance** |
| Transformer encoder block contains? | Multi-Head Attention + Feed-Forward Networks |
| BERT POS accuracy? | ~98.5–99.5% |
| Two stages of the BERT approach? | Pre-training (masked word prediction on trillions of words) + fine-tuning (add a classification layer, few epochs) |
| Which libraries use this as standard? | spaCy, Hugging Face Transformers |
| What replaces fine-tuning in the LLM approach? | **Prompting** |
| What is an LLM agent? | An LLM given the ability to **use external tools** |
| Benefit of the agent approach? | LLM's reasoning/planning + the speed/accuracy of a specialised model |
| Where is POS tagging heading? | Becoming an **internal utility** inside larger LLM agent systems |

---

## 9. You try
*Attempt on paper before scrolling. Answers at the very bottom.*

**Q1.** Explain in two sentences why a Bi-LSTM alone is not enough and the CRF
layer is added on top.

**Q2.** *"I walked to the river bank."* Explain which context each direction of
the Bi-LSTM supplies for tagging *bank*, and why a unidirectional model would
struggle.

**Q3.** Put these in order of typical POS accuracy, lowest first, and give the
approximate figure for each: BERT fine-tuned, HMM+Viterbi, Bi-LSTM-CRF.

**Q4.** You must build a POS tagger for a low-resource language with only 2,000
labelled sentences and no pre-trained model. Which approach from this chapter
would you choose, and why?

**Q5.** In one sentence each, state what the *user* has to supply in the
BERT-fine-tuning approach versus the LLM-prompting approach.

---

## Next
**Chapter 8 — LLM and Prompt Engineering.** The last pre-midsem chapter, and the
one this one's §4–5 leads into.
→ [`ch08-llm-prompt-engineering.md`](ch08-llm-prompt-engineering.md)

---
---
---

<!-- ANSWERS BELOW - stop scrolling until you have attempted -->

## Answers

**A1.**
A Bi-LSTM produces an excellent contextual score for each word **independently**,
so if you simply take the highest-scoring tag at each position you can end up
with an **impossible sequence** — for example a Verb immediately following a
Determiner. The CRF layer adds transition scores between adjacent tags and
selects the tag path with the highest score **over the whole sentence**, so the
learned constraints between neighbouring tags are respected.

**A2.**
The **forward** pass supplies the left context — *I walked to the **river***,
which strongly suggests the geographic sense; the **backward** pass supplies the
right context — the sentence-final **.**, confirming *bank* ends the noun phrase
rather than starting a verb phrase. A unidirectional left-to-right model would
have the *river* cue but no evidence about what follows, and a right-to-left
model would have the opposite problem — either one is deciding on half the
available evidence.

**A3.**
```
1. HMM + Viterbi      ~95–96%
2. Bi-LSTM-CRF        ~97–98%
3. BERT fine-tuned    ~98.5–99.5%   (SOTA)
```

**A4.**
**Bi-LSTM-CRF.** It is explicitly listed as *"good for low-resource languages
(with transfer learning)"*; its **character embeddings** handle the many unknown
words you will hit with only 2,000 labelled sentences, and it **learns features
automatically**, so you do not have to hand-engineer an MEMM feature set for a
language you may not know well. Fine-tuning BERT is ruled out by the premise (no
pre-trained model available), and an HMM would be weak on unknown words.

**A5.**
**BERT fine-tuning:** the user must supply a **labelled POS corpus** plus compute
for a training run of a few epochs, and must add a classification layer on top of
the pre-trained model.
**LLM prompting:** the user must supply only a **well-written natural-language
instruction** (optionally a few examples for few-shot), with no labelled corpus
and no training at all.
