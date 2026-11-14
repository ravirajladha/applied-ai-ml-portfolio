# Assignment 1A: CPT and QLoRA, build guide

**Large Language Models for Generative AI · Assignment 1A · 15 marks**

| File | What it is |
|------|------------|
| `explainer.html` | **Open this first.** An interactive lesson with a cleaning-filter demo, a packing demo, a model-layer explorer, a loss/perplexity slider, a forgetting trade-off slider, a chat-template builder, a LoRA rank calculator, a 4-bit rounding demo, and a 10-question quiz. |
| `practice.ipynb` | The assignment notebook (runs on Google Colab). The boilerplate is written; **17 `# TODO` lines** and the **✍️ inference cells** are yours. |
| `guide.md` | This file: the plan, the recap, the schedule and the checklist. |

Source documents: `../Assignment 1A - CPT and SFT.pdf` and `../Enterprise_Variants_All_Assignments.pdf`.
Lecture links: **CS-2** (pre-training, domain adaptation, forgetting, LR schedule) and **CS-3** (IFT, LoRA, QLoRA) in `../../materials/`.

---

## The problem statement

Take a general pretrained LLM and turn it into an **IT helpdesk assistant** (Enterprise Variant 5) in two stages:

1. **Part A, Continual Pre-Training (10 marks).** Let the model *read* Linux admin manuals so it learns the domain's
   language. Prove it with perplexity, and prove it didn't forget general facts.
2. **Part B, QLoRA instruction tuning (5 marks).** Teach it to *answer questions* using a small LoRA adapter trained on
   top of a 4-bit copy of the CPT model.

| Choice | Value | Why |
|---|---|---|
| Domain | Variant 5, IT Helpdesk | Free, clean, well-structured PDFs (RHEL 9 + Ubuntu Server guides); numbered sections make Q&A pairs easy |
| Model | `Qwen/Qwen2.5-0.5B` (base) | Fits a free Colab T4 for *full* CPT; has a chat template for Part B; ungated (no access request) |
| GPU | Colab T4 (16 GB) | Free. An A100 works too and the notebook switches to bf16 automatically |
| Block size | 512 tokens | A T4-friendly memory size; attention cost grows with length² |

---

## Plain-English recap

| Term | In one line |
|------|-------------|
| **CPT** | Keep doing next-token training on *your* domain text, starting from a trained model. |
| **Corpus** | The pile of text you train on, here the cleaned `.txt` manuals. |
| **Length / dedup / language filter** | Drop near-empty pages / exact copies / non-English pages. |
| **Tokenizer** | Cuts text into pieces and maps each to an ID. Always reuse the model's own. |
| **BOS / EOS** | Start and end markers around each document. Qwen uses `<\|endoftext\|>` for both. |
| **Packing** | Join all token IDs, cut into 512-token blocks, so there is zero padding. |
| **Parquet** | A compact table file format, used to save the blocks. |
| **lm_head** | Last layer: one score per vocabulary entry, so its size must equal `vocab_size`. |
| **Loss** | How wrong the next-token guesses are. A pretrained model starts at about 2–4; ~11.9 means random weights. |
| **Perplexity** | e^loss. "Torn between N tokens." CPT should lower it by 10–40% on held-out manuals. |
| **Catastrophic forgetting** | Domain training overwrites general knowledge. Fix: lower the LR, fewer steps, replay. |
| **Instruction tuning (IFT)** | Train on question → answer pairs so the model answers instead of continuing text. |
| **JSONL** | One JSON object per line. |
| **Chat template** | The model's own way of writing a conversation as one string (`<\|im_start\|>user … <\|im_end\|>`). |
| **LoRA** | Freeze W; train two thin matrices B·A (rank r, scale α/r). |
| **QLoRA** | LoRA on a 4-bit NF4 frozen base. On a T4, compute in fp16. |
| **Adapter A / B / C** | r=8 / 16 / 32. We use **B** (r=16, α=32, q_proj + v_proj). |

---

## The build plan, cell by cell

Each code cell ends with `assert` checks. If they pass, move on. If not, the message tells you which TODO broke.

| Notebook cell | Explainer | What you write | Marks |
|---|---|---|---|
| 0 Setup | – | nothing (pick a GPU runtime; the cell detects Colab vs the institute server) | – |
| 1a Download PDFs | §2 | nothing: 25 PDFs download automatically | |
| 1b Extract pages | §2 | **TODO 1**: list of `page.get_text()` | |
| 1c Clean | §2 | **TODO 2** length check · **TODO 3** md5 fingerprint · **TODO 4** `detect(...) == 'en'` | **2** |
| 2 Tokenize + pack | §3 | **TODO 5** `[BOS]+ids+[EOS]` · **TODO 6** flatten · **TODO 7** slice into blocks | **2** |
| 3 Model + architecture | §4 | **TODO 8** parameter count · **TODO 9** lm_head output size | **2** |
| 4 CPT training | §5 | **TODO 10** dataset item (labels = input_ids) · **TODO 11** loss callback | **2** |
| 5A Perplexity | §5 | **TODO 12** `exp(mean loss)` · **TODO 13** % drop | |
| 5B Forgetting | §6 | **TODO 14** your Retained/Degraded verdicts | **2** |
| B1 Instruction data | §7, §8 | **TODO 15** write JSONL · **TODO 16** 80/20 split | **2** |
| B2 QLoRA | §9, §10 | **TODO 17** Adapter B config | **2** |
| B3 Evaluation | §7 | nothing new to code; inference only | **1** |

**Every step ends with a ✍️ inference cell.** The assignment says inferences are mandatory. Each cell lists the exact
questions to answer, so you never face a blank page.

---

## Schedule: 6 sittings, about 60–90 minutes each

| Sitting | Do | GPU time |
|---|---|---|
| 1 | Explainer §1–§3 + quiz Q1–Q2. Notebook Cell 0 → Step 1 (TODO 1–4) + inference. | ~0 (CPU work; a GPU runtime is fine) |
| 2 | Step 2 (TODO 5–7) + explainer §4 + Step 3 (TODO 8–9) + inferences. | ~5 min |
| 3 | Explainer §5 + quiz Q3–Q5. Step 4: first run with `MAX_STEPS = 30` to check that loss starts at ~2–4, then a full run. | ~30–45 min |
| 4 | Explainer §6 + quiz Q6. Step 5 (TODO 12–14) + inferences. **Part A done (10 marks).** | ~10 min |
| 5 | Explainer §7–§10 + quiz Q7–Q10. B1 (TODO 15–16) + B2 (TODO 17). | ~15–25 min |
| 6 | B3 + every remaining inference. Export HTML, zip the corpus, submit. | ~5 min |

Colab disconnects when idle. Because everything is saved to Drive (or your home folder off Colab), after a disconnect you re-run Cell 0 and
continue from your step. Re-run the cells of your current step from its first cell.

---

## Skip list (do NOT spend time on these)

- **The optional extension** (multi-adapter routing): 0 marks.
- **The LLM-generated dataset**: the heuristic is enough. Only read the prompt template so you can mention it.
- **Training all three adapters**: the assignment says *any one*. Do B.
- **Tuning many hyperparameters**: one clean run with a justified LR beats five runs with no explanation.
- **Reading Transformer source code**: the config table in Step 3 is all you need.
- **Near-duplicate detection (MinHash)**: only *mention* it in the Step 1 inference.

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| First CPT loss ≈ 11–12 | Model didn't load its pretrained weights | Check `MODEL_ID` and `from_pretrained` |
| `CUDA out of memory` in Step 4 | Batch too big for a T4 | `BATCH, ACCUM = 1, 16` |
| Loss goes up or spikes | LR too high | `learning_rate=1e-5`, or a longer warmup |
| PPL drop < 10% | Too few steps / small corpus | One full epoch (`MAX_STEPS=-1`) |
| General prompts degraded | Over-training | LR ÷10 or halve the steps (assignment tip) |
| `bf16` error on a T4 | T4 has no bf16 | Already handled by `BF16_OK`; don't force it on |
| A PDF download fails | URL moved | Skip it; 20+ PDFs are plenty. Note it in the inference |
| `TypeError` on `dtype=` / `max_length=` | Old library versions | Re-run the `pip install -U` cell, then *Runtime → Restart* |

---

## Deliverables checklist

- [ ] `practice.ipynb` **with outputs** (download from Colab)
- [ ] HTML export: `jupyter nbconvert --to html practice.ipynb`
- [ ] `instruction_dataset.jsonl` (in `WORKDIR/data/` on Drive)
- [ ] `domain_corpus/*.txt` (zipped by the last cell)
- [ ] Every ✍️ inference cell filled in, in your own words

## Progress checklist

- [ ] Explainer read, quiz ≥ 8/10
- [ ] Step 1: cleaning stats table + which step removed most
- [ ] Step 2: token count, average doc length, number of packed sequences
- [ ] Step 3: parameter count, architecture table, lm_head check, 3 baseline outputs
- [ ] Step 4: loss curve, plateau step, checkpoint saved
- [ ] Step 5A: base PPL, CPT PPL, % drop
- [ ] Step 5B: forgetting table with verdicts
- [ ] B1: JSONL, 5 samples, train/eval counts
- [ ] B2: Adapter B trained, trainable %, hyperparameters reported
- [ ] B3: base vs CPT vs adapter comparison + observations
- [ ] Exported and submitted
