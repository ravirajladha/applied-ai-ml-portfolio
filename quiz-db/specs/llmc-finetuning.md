# Fine-tuning & PEFT (M6, course): coverage spec

**Ladder:** Courses › LLMs for Generative AI (AIMLCZG536)   ·   **Prerequisites:** llmc-pretraining (CLM objective, CPT, catastrophic forgetting), llm-finetuning (ladder view of LoRA/QLoRA/SFT)
**Why it matters for AI/ML:** Session 3 of the course and Assignment 1A (CPT then QLoRA) are built on this module. The exam asks "which fine-tuning approach, why, and one example method" scenarios, and the course's own numbers (adapter 49,152 params, LoRA r(d+k), 0.39%, 99.88%, NF4 + double quantization 0.5 -> 0.127 bits/param) are fair game. This subject tests the course's wording and numbers; the ladder subject `llm-finetuning` covers the engineering side (loss masking, memory budgets, hyperparameters).

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `ft-types` | CPT, full FT, PEFT, SFT, IFT | what each term means, examples (BioBERT, Llama 3.1 Instruct) | CPT is self-supervised, IFT is a type of SFT | exam scenario: LM objective on domain text = CPT, not IFT | CPT then IFT ordering (Assignment 1A), what each stage changes |
| 2 | `icl-vs-ft` | In-context learning vs fine-tuning, base vs instruct | zero/one/few-shot, no weight change | three limits of ICL, token cost every call | why a base model rambles (objective, not missing data) | agentic systems and per-call context cost |
| 3 | `ift-data` | Building IFT data | the four methods with their example datasets | match a dataset to a method | Self-Instruct loop: classification check, output-first vs input-first | why the filter step matters, near-duplicate (ROUGE-L) filter |
| 4 | `schema-template` | JSONL schema vs chat template | what JSONL is | instruction/input/output fields, render with a template | switch model = re-render, not rebuild | template mismatch at serve time, task_type/source_dataset metadata |
| 5 | `peft-taxonomy` | PEFT families, prompt/prefix tuning, BitFit | why PEFT ("GPUs don't grow on trees") | classify a method into addition / selective / reparameterisation | hard vs soft prompt, prompt vs prefix tuning trade-offs, BitFit counts | prefix-tuning param counts, BitFit on bias-free Llama layers |
| 6 | `adapters` | Bottleneck adapters | frozen backbone + small module | down -> nonlinearity -> up + residual, 49,152 vs 1,048,576 | per-block counts with biases, extra inference latency | adapter vs LoRA total cost across a model |
| 7 | `lora-math` | LoRA maths | ΔW = BA, W frozen | h = Wx + ΔWx, rank intuition, r(d+k) | B = 0 / A random init, α/r scaling, slide 17's 99.88% example | rank of BA, the slide's swapped A/B notation, why divide by r |
| 8 | `lora-serving` | Merging and multi-tenant LoRA | small adapter file | merge W' = W + (α/r)BA, one base + N adapters | storage maths for N tenants, merged vs unmerged | Assignment 1A adapter counts on Qwen2.5-0.5B (q_proj + v_proj, GQA) |
| 9 | `qlora` | Quantization and QLoRA | 4-bit base + 16-bit LoRA | bytes per param, 7B at 4-bit = 3.5 GB, dequantise on the fly | NF4 quantiles, paged optimizers, fp16 on a T4 | double quantization 0.5 -> 0.127 bits/param, ~3 GB saved on 65B |
| 10 | `merging` | Model merging | one model from many | merging vs ensembling inference cost | Model Soups, same-base requirement | SLERP vs linear averaging (norm shrinkage) |

## Must-know facts
- CPT = further training on new unlabelled text with the same LM objective (self-supervised, all weights), e.g. BioBERT. Full FT = all weights. PEFT = a small part. SFT = labelled input-output pairs. IFT is a type of SFT on instruction-response pairs ("nowadays SFT is IFT").
- ICL: instructions/examples in the prompt, no weights change. Limits: examples cost context on every call, nothing persists, painful in agentic systems with many calls.
- A base model continues text because its objective is next-token prediction; it is not missing data. IFT teaches instruction following, not longer context.
- IFT data: human authoring (Dolly-15K), template conversion (FLAN), synthetic generation by a stronger teacher (Alpaca 52K), hybrid pipeline (Self-Instruct: 175 seed tasks -> 52K, filtered).
- Self-Instruct steps: generate instruction -> classify "is it a classification task?" -> generate instances (classification: label first then input; otherwise input first) -> filter -> add to pool.
- Store a model-agnostic JSONL record {instruction, input, output, task_type, source_dataset}; render it with the model's chat template (Mistral `<s>[INST] ... [/INST] ... </s>`). Switching model = re-render.
- PEFT families: addition (prompt tuning, prefix tuning, adapters), selective (layer freezing, BitFit, diff pruning), reparameterisation (LoRA).
- Bottleneck adapter: down-project d -> m, nonlinearity, up-project m -> d, residual. d = 1024, m = 24: 49,152 weights vs 1,048,576 for a full layer (~4.7%). Adapters add layers in the forward path (latency).
- Regular FT: ΔW = α(-∇L), W' = W + ΔW, h = Wx + ΔWx. LoRA: ΔW = BA, B (d x r) = 0, A (r x k) random, h = Wx + (α/r)BAx, params r(d+k).
- 4096 x 4096, r = 8: 65,536 vs 16,777,216 (0.39%). Slide 17: 10000 x 20000, r = 8: 240,000 vs 200M (99.88% fewer).
- Merge after training: W' = W + (α/r)BA, same shape, zero extra latency. Multi-tenant: one base + N adapters instead of N full copies.
- Bytes/param: FP32 4, BF16/FP16 2, INT8 1, 4-bit 0.5. 7B: 28 / 14 / 3.5 GB.
- QLoRA: frozen NF4 base, BF16 LoRA (FP16 on a T4), dequantise per matmul then discard; 65B on one 48 GB GPU. NF4 levels at normal quantiles; double quantization 0.5 -> ~0.127 bits/param; paged optimizers spill optimizer states to CPU RAM on spikes.
- Merging: one deployable model (unlike ensembling); best with the same base checkpoint; linear averaging, Model Soups, SLERP.

## Common traps (each one must have at least one question)
- "CPT is unsupervised" -> the course says self-supervised (the labels come from the text itself).
- "CPT needs instruction-response pairs" -> no, raw domain text with the LM objective.
- "IFT extends the context length" -> no, it teaches instruction following.
- "A base model rambles because it lacks data" -> it is the next-token objective.
- "Few-shot examples teach the model permanently" -> nothing persists; you pay the tokens every call.
- "LoRA params = r x d x k" -> r(d + k).
- "Initialise A to zero (or both)" -> B = 0, A random: BA = 0 but gradients still reach B.
- "LoRA adds no parameters" -> it adds A and B (a reparameterisation of ΔW); only they train.
- "Adapters and merged LoRA both add latency" -> merged LoRA adds none.
- "QLoRA computes matmuls in 4-bit" -> weights are dequantised to BF16 per matmul.
- "Double quantization quantizes the weights twice" -> it quantizes the scale constants.
- "Paged optimizers page the model weights" -> they page the optimizer states.
- "Merging = ensembling" -> merging gives one model; ensembling runs several.
- "Prompt tuning rewrites the prompt text" -> that is hard prompting; soft prompt tuning learns continuous embeddings.
- "BitFit is reparameterisation" -> selective (biases only).
- Slide 16/17 name the factors the other way round (W_A is A x r) -> the count is the same; follow the standard B (d x r), A (r x k) of the notes.

## Interview angle
1. **"A SaaS company serves 30 enterprise clients from one LLM but cannot store 30 full copies. What do you do?"** PEFT, specifically LoRA: one frozen base in GPU memory plus 30 small adapters swapped per request (multi-tenant serving). Storage drops from 30 full models to one model plus a few MB per client.
2. **"Derive LoRA from regular fine-tuning."** h = Wx + ΔWx; ΔW is as big as W; the update is low-rank, so write ΔW = BA with r << d, k; params r(d+k); B = 0 so training starts at the base model; scale α/r; merge after training.
3. **"Why does QLoRA fit a 65B model on one 48 GB GPU?"** 4-bit NF4 base (65B x 0.5 B ≈ 32.5 GB), 16-bit LoRA only, double quantization of the scale constants (~3 GB saved) and paged optimizers absorbing spikes.
4. **"How would you build an instruction dataset for an IT helpdesk?"** Raw manuals -> pre-process -> model-agnostic JSONL (instruction/input/output) from human, template, synthetic or hybrid (Self-Instruct style) generation with filtering; render with the target model's chat template at training time.
5. **"CPT vs IFT?"** CPT: unlabelled domain text, LM objective, learns the domain's language. IFT: labelled instruction-response pairs, learns to follow instructions. Assignment 1A does CPT first, then QLoRA IFT.

## Source material
- Notes `materials/notes/Session-03-LLM-Fine-tuning.md` (lecture 14-Nov-2026) and `Quick-Revision-Sheet.md` (S3 section): the fine-tuning taxonomy table, ICL limits, base vs instruct rambling (💬 "not a lack of data"), the four IFT data methods, Self-Instruct loop, three-layer example (SQuAD raw -> JSON schema -> Mistral template, 🎯 keep schema separate), PEFT families, adapter worked numbers (49,152 vs 1,048,576, ~4.7%), "two-path" regular FT maths (🎯 "very important"), rank-1 matrix intuition, LoRA table (B = 0, α/r, divide by r), 65,536 = 0.39%, multi-tenant serving, QLoRA tricks, merging.
- Deck `CS-3 LLM Fine tuning` slides 4-23: definitions with examples (BioBERT, Qwen2.5-0.5B, Llama 2-Chat, Llama 3.1 Instruct, DistilBERT), slide 8 data methods, slide 9 schema, slide 10 Self-Instruct, slides 11-13 PEFT and adapters, slide 14 ΔW = α(-∇L), slides 15-18 LoRA (slide 16 uses W_A ∈ R^(A x r), W_B ∈ R^(r x B); slide 17: 10000 x 20000, r = 8 -> 240,000, 99.88%), slide 19 multi-tenant h = x(W0 + (α/r)B_iA_i), slides 20-22 quantization and QLoRA (NF4, double quantization 0.5 -> 0.127 bits/param, ~3 GB on 65B, paged optimizers, BF16 or FP16 on T4), slide 23 merging and Model Soups.
- Old-batch slides (`old-batch-slides.txt` ~1375-1545): hard vs soft prompt tuning, prefix tuning (trainable prefix vectors in all layers; more capacity, more compute, may overfit), the same PEFT/QLoRA/merging content.
- Assignment guides `assignments/1A - CPT and QLoRA/guide.md` (+ explainer): CPT then QLoRA on Qwen2.5-0.5B; Adapter A/B/C = r 8/16/32, α 16/32/32, targets q,v / q,v / q,v,o; q_proj 896 -> 896, v_proj 896 -> 128 (GQA), 24 layers; NF4 + double quant config; fp16 on a T4. `1B .../guide.md`: Adapter B on Qwen2.5-1.5B, 4-bit can be slower at batch 1.
- Exam patterns: the June-2026 midsems ask a 4-part scenario: "a team with a small GPU budget / a SaaS provider with 30 client tasks: (a) which fine-tuning approach (PEFT), (b) why better than full fine-tuning (memory, storage, one base + adapters), (c) one example method (LoRA, adapters, prefix tuning), (d) training on raw text with the LM objective is what (CPT) and how it differs from IFT / SFT". Answers are short justifications with the course's terms; the L3/L4 questions here mirror that with new scenarios, plus course-number calculations (adapter, LoRA, QLoRA bits/param) and "spot the wrong answer" traps.
