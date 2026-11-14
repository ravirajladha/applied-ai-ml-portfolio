# Assignment 1B: adaptation and production optimization, guide

**Large Language Models for Generative AI · Assignment 1B · 15 marks**

| File | What it is |
|------|------------|
| `explainer.html` | **Open this first.** The production process (9 habits, click to open), a decoding-strategy playground, a speculative-decoding step-through and speed-up calculator, 4-bit and benchmarking pitfalls, a cost-per-1M-tokens calculator, and a 10-question quiz. |
| `practice.ipynb` | **Complete and runnable** top to bottom. Your work is to run it, read the outputs, and write the **✍️ inference cells**. Each has a hidden "what to look for" hint. |
| `guide.md` | This file. |

Source: `../Assignment-1B LLM Adaptation  Production Optimization.pdf` and `../Enterprise_Variants_All_Assignments.pdf`.
For data cleaning and LoRA/QLoRA demos, see the **1A explainer** (`../1A - CPT and QLoRA/explainer.html` §2, §7–§10).

> **Heads-up:** this notebook's Step 1 and B1 code is the answer key to 1A's TODO 1–4 and 15–17.
> If you want 1A to teach you, do 1A first.

---

## The problem statement

Take `Qwen2.5-1.5B` and the IT-helpdesk corpus (Variant 5):

1. **Part A (2):** clean the corpus; record the base model's architecture and 3 "before" answers.
2. **Part B (5):** build ~2,000 grounded Q&A pairs, train QLoRA **Adapter B**, compare with the baseline.
3. **Part C (8):** measure how **decoding strategy**, **speculative decoding** and **4-bit quantization** change quality,
   speed, memory and **cost per 1M tokens**, then recommend what to deploy.

| Choice | Value | Why |
|---|---|---|
| Target model | `Qwen/Qwen2.5-1.5B` | big enough for speculative decoding to make sense, small enough for a T4 |
| Draft model | `Qwen/Qwen2.5-0.5B` | same tokenizer and vocabulary (required), ~3× fewer parameters |
| Adapter | B (r=16, α=32, q_proj + v_proj) | the assignment's "balanced" option |
| Best decoding (default) | Greedy | factual domain; change `BEST` after your C1 analysis if you disagree |

---

## How this was approached: the production process

This is the "production-level" part. The notebook is organised around these habits (explainer §2 explains each):

1. **Contract first.** One `CONFIG` cell holds the models, prompts, seed, `max_new_tokens`, GPU and price. It is saved as `run_config.json`.
2. **Baseline before change.** Save the "before" answers (A2) and the 16-bit numbers (C3) before trying anything.
3. **One change at a time.** C1 varies only decoding, C2 only adds a draft, C3 only changes precision.
4. **Repeatable.** Fixed seeds, a deterministic dataset heuristic, idempotent downloads.
5. **Honest measurement.** Warm-up, `cuda.synchronize()`, tokens actually generated, median of repeats, one model on the GPU at a time.
6. **Verify the optimisation.** Check that speculative output is identical to plain greedy; print the same prompt under every config.
7. **Money and memory.** Turn tok/s into cost per 1M tokens, alongside peak VRAM.
8. **Artifacts.** Every table goes to a CSV in `data/`, plus the adapter, config and library versions.
9. **Decide with evidence.** Each part ends in a decision backed by cited numbers. That is what the ✍️ cells are for.

---

## Notebook map

| Cell / part | Explainer | You do | Marks |
|---|---|---|---|
| 0 Setup | §2 | pick a GPU runtime; it detects Colab vs the institute server | – |
| A1 Corpus | §3 | ✍️ cleaning stats + justification | 1 |
| A2 Baseline | §4 | ✍️ architecture + judge 3 answers | 1 |
| B1 Dataset | §5 | ✍️ method, size, split | 2 |
| B2 QLoRA | §5 | ✍️ adapter choice, hyperparameters, loss | 2 |
| B3 Compare | §5 | ✍️ side-by-side judgement | 1 |
| C1 Decoding | §6 | ✍️ **100-word analysis**, then set `BEST` | 3 |
| C2 Speculative | §7 | ✍️ speed-up, identical output?, why | 2 |
| C3 4-bit + cost | §8, §9 | ✍️ **2–3 sentence deployment recommendation** | 3 |

---

## Schedule: 4 sittings

| Sitting | Do | GPU time (T4) |
|---|---|---|
| 1 | Explainer §1–§5. Run Cell 0 → B3 in one go (training runs while you read). | ~40 min |
| 2 | Write the A1, A2, B1, B2 and B3 inferences while the outputs are fresh. | – |
| 3 | Explainer §6–§9 + quiz. Run C1 → C3. | ~25 min |
| 4 | Write the C1 (100 words), C2 and C3 inferences. Export HTML, zip, submit. | – |

If the session drops between sittings: re-run Cell 0, then the **Part A2 cell** (it defines `tok`, `run` and `fmt`), then continue.
Part C does not need Part B's model in memory.

---

## Skip list

- **The optional extension** (adapter + 4-bit + speculative together): 0 marks.
- **LLM-generated instruction pairs**: just cite the template shown in B1.
- **Tuning the draft's `num_assistant_tokens`**: the default is fine; explain the result instead.
- **vLLM, TensorRT or GGUF**: not asked for. Mention one line under "future work" at most.
- **Re-running C3 many times** to get a "nicer" number: report what you measured and explain it.

---

## What results to expect (so they don't confuse you)

| You may see | That's normal because |
|---|---|
| A base-model answer that keeps writing new "Question:" lines | a base model continues text (CS-2 slide 27) |
| Beam search is the slowest | it tracks 4 sequences |
| Temp 1.2 invents flags | a flatter distribution makes rare tokens likely |
| Speculative speed-up close to 1× | at batch 1 the 0.5B draft step isn't much cheaper than the 1.5B step (explainer §7) |
| 4-bit is **slower** but uses much less VRAM | dequantization overhead at batch 1 on a T4 (explainer §8) |
| A few speculative outputs differ slightly from greedy | 16-bit rounding when several positions are verified at once |

Each of these makes a **good inference** when explained with the reason. None of them is a bug.

---

## Deliverables checklist

- [ ] `practice.ipynb` with outputs
- [ ] HTML export: `jupyter nbconvert --to html practice.ipynb`
- [ ] `data/instruction_dataset.jsonl`
- [ ] `domain_corpus/*.txt` (zip made by the last cell)
- [ ] Final prompts, hyperparameters and benchmark settings: printed in Cell 0 and saved in `data/run_config.json`
- [ ] Every ✍️ cell in your own words

## Progress checklist

- [ ] Explainer read, quiz ≥ 8/10
- [ ] Part A done + 2 inferences
- [ ] Part B done + 3 inferences
- [ ] C1 table + 100-word analysis + `BEST` set
- [ ] C2 speed-up table + inference
- [ ] C3 cost table + recommendation
- [ ] Exported and submitted
