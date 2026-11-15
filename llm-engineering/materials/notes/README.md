# LLMs for Generative AI — Study Notes

> Course **AIMLCZG536** (S1-26) · Instructor: Dr. Monali Mavani (BITS-Pilani WILP)
> Books — Alammar & Grootendorst, *Hands-On Large Language Models* · Jurafsky & Martin, *Speech and Language Processing* (3rd ed. draft) · Raschka, *Build a Large Language Model (From Scratch)*

Each note merges two sources:
1. **The slide deck** (`../CS-N ….pptx`) — definitions and structure.
2. **The lecture transcript** (`../../transcript/`) — the professor's explanations, examples, Q&A and exam hints (marked 💬).

Legend: 🌍 analogy · 🧪 worked numbers · 🎯 likely exam point · 💬 said in class.

---

## 📚 Session index

| # | Note | Topic in one line | Deck | Transcript |
|---|------|-------------------|------|:----------:|
| 0 | [NLP Primer (self-study)](Session-00-NLP-Primer-Self-Study.md) | Token, vocabulary, embedding, cosine, LM, encoder vs decoder, NLU vs NLG | `NLP_Primer_SelfStudy_llm.pptx` | — |
| 1 | [Intro to LLMs](Session-01-Intro-to-LLMs.md) | LM = next-token probability · **BPE / byte-level BPE** · embeddings · positional encoding | `CS-1 Intro to LLM.pptx` | ✅ 24-Oct |
| 2 | [LLM Pre-training](Session-02-LLM-Pre-training.md) | CLM · data pipeline · **Kaplan vs Chinchilla** · CPT & forgetting · Llama 3 / Qwen3 recipes | `CS-2 LLM Training.pptx` | ❌ (part in S3) |
| 3 | [LLM Fine-tuning](Session-03-LLM-Fine-tuning.md) | ICL vs IFT · Self-Instruct · PEFT · adapters · **LoRA** · **QLoRA** · merging | `CS-3 LLM Fine tuning (1).pptx` | ✅ 14-Nov |

**Extras:** [Quick Revision Sheet](Quick-Revision-Sheet.md) — everything so far on one page.

### Source notes
- `transcript/…sesion2.docx` is a **byte-for-byte copy of session 1** — there is no session 2 transcript. If you get the real one, the Session 2 note can be topped up.
- `NLP_Primer_SelfStudy (1).pptx` and `NLP_Primer_SelfStudy_llm.pptx` are the same deck.
- Session 1 covered CS-1 slides 1–33 only; Session 3 covered CS-3 up to multi-tenant LoRA (QLoRA moves to the next class). The untaught slides are still summarised in each note.

---

## 🗺️ How it fits together

```
S0 Primer          S1 Building blocks              S2 Pre-training                    S3 Fine-tuning
text→tokens→   →   tokenizer (BPE) →          →    self-supervised CLM on        →    base model → IFT (instructions)
vectors, LM        embeddings + position →         trillions of tokens; scaling       cheaply via PEFT: adapters,
                   Transformer → LM head           laws; CPT for a domain             LoRA, QLoRA
                                                   ⇒ BASE model                       ⇒ INSTRUCT / domain model
```

**Coming next (per the course plan):** architecture (attention, RoPE, MoE) → inference fundamentals → inference optimisation *(mid-sem = modules 1–5, closed book)* → alignment (RLHF/DPO) → prompting & reasoning → RAG → agents → evaluation → safety.

## 📝 Evaluation

| Component | Weight | Notes |
|-----------|--------|-------|
| Assignments | 35% | A1 (15) + A2 (20), groups of 4. **A1 deadline 19-Dec**; 1A/1B preference form by 19-Nov |
| Mid-sem | 30% | Closed book, modules 1–5 |
| End-sem | 35% | Open book (Taxila slides only) |
