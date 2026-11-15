# Fine-tuning & LoRA: coverage spec

**Ladder:** L4 · LLM Engineering › Building with LLMs   ·   **Prerequisites:** dl-training (loss, learning rate, epochs, batches), tf-generation, llm-prompting, llm-rag
**Why it matters for AI/ML:** Fine-tuning changes the weights so a model reliably follows a format, style or domain behaviour. AI engineers must know when it's worth it (vs prompting or RAG), how to do it cheaply (LoRA/QLoRA), how to prepare data, how much GPU memory it needs, and how to prove it helped without breaking general ability.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `when-to-finetune` | Fine-tune vs prompt vs RAG | what fine-tuning changes | behaviour/format vs facts, cost of trying prompting first | combining RAG + fine-tuning | — |
| 2 | `full-vs-peft` | Full fine-tuning vs PEFT | what PEFT means | trainable-parameter counting in PyTorch | when full fine-tuning is worth it | — |
| 3 | `lora` | LoRA | frozen base + small adapter | parameter count r*(d+k), alpha/r scaling | B=0 init, merging, rank of BA, target modules | whole-model counts with GQA shapes, rank choice |
| 4 | `qlora` | QLoRA | 4-bit base + LoRA | — | memory split base vs adapter, paged optimisers | NF4 + double-quantisation overhead, merging into a quantised base |
| 5 | `sft-data` | SFT data format | instruction/response pairs | loss masking with -100, chat templates | `ignore_index` arithmetic, template mismatch | per-token loss averaging across micro-batches |
| 6 | `data-quality` | Dataset quality | duplicates and dirty rows | quality over quantity | train/eval leakage | label noise and style collapse |
| 7 | `cpt` | Continued pre-training vs SFT | — | raw text vs instruction pairs | when CPT is needed | CPT then SFT, losing chat skills |
| 8 | `preference` | Preference tuning (RLHF, DPO) | what preference data looks like | RLHF vs DPO idea | DPO loss at initialisation | DPO loss arithmetic, role of beta and the reference model |
| 9 | `hyperparams` | Learning rate, epochs, batch, accumulation | what an epoch is | effective batch size, steps per epoch | warmup/decay, LoRA vs full lr | — |
| 10 | `eval-forgetting` | Evaluating a fine-tune, catastrophic forgetting | held-out data | before/after task + general evals, catastrophic forgetting | eval loss curves, overfitting | mitigations: replay, LoRA, lower lr |
| 11 | `memory` | GPU memory estimation | bytes per parameter at fp16 | fp16 / int8 / 4-bit weight sizes | full fine-tuning with Adam: ~16 bytes/param | activations, KV, why estimates are lower bounds |
| 12 | `distill-serve` | Distillation and serving adapters | — | what distillation is, merging an adapter | serving many LoRA adapters on one base | soft targets and temperature, merged vs unmerged serving |
| 13 | `lora-pytorch` | LoRA and freezing in PyTorch code | what `requires_grad = False` does | tiny LoRALinear (A, B, zero-init B, trainable count), `named_parameters` filter, `train()` doesn't unfreeze | — | A's gradient is zero at step 0, all-zero init never learns |
| 14 | `special-tokens` | Special tokens, EOS/padding and embeddings | what EOS is for | EOS at the end of every target, resizing embeddings after adding tokens | pad = eos masking bug, embedding + head parameter counts | new-token rows untrained under attention-only LoRA |
| 15 | `train-efficiency` | Mixed precision, checkpointing and packing | why bf16 | gradient checkpointing trade, accumulation doesn't speed up | packing, padding waste, bf16 vs fp16 range, fp16 overflow | packing cross-contamination, sqrt(L) checkpointing |

## Must-know facts
- Order of attack: prompt -> RAG (knowledge) -> fine-tune (behaviour, format, tone, domain style). Fine-tuning is weak at adding fresh, precise facts.
- Full fine-tuning updates every weight; PEFT (parameter-efficient fine-tuning) trains a small set of new or selected parameters and freezes the rest.
- LoRA: W' = W + (alpha / r) * B @ A, with A of shape (r, k) and B of shape (d, r). Trainable params per matrix = r * (d + k). B starts at zero, so the model starts unchanged.
- The update B @ A has rank at most r. Typical r = 8-64, alpha often r or 2r; typical targets: attention projections (q, k, v, o), often MLP too.
- An adapter can be merged into W after training (no extra inference latency) or kept separate (swap adapters per request on one base).
- QLoRA: frozen base quantised to 4-bit NF4, double quantisation of the scale constants, paged optimisers to absorb memory spikes; LoRA adapters train in 16-bit.
- Weight memory: fp32 4 B, fp16/bf16 2 B, int8 1 B, 4-bit 0.5 B per parameter. 7B params at fp16 = 14 GB.
- Full fine-tuning with mixed-precision Adam costs about 16 bytes per parameter before activations (7B -> ~112 GB).
- SFT data = instruction/response (or chat) examples rendered with the model's own chat template. Loss is usually masked on prompt tokens (label -100) so the model learns to answer, not to repeat prompts.
- A small, clean, diverse dataset beats a large noisy one. Dedup, and keep eval data out of training.
- Continued pre-training = next-token training on raw domain text (new vocabulary/knowledge); SFT = learning to respond in a format.
- RLHF trains a reward model on preference pairs then optimises the policy with RL; DPO optimises directly on (chosen, rejected) pairs against a frozen reference model.
- Effective batch = per-device batch * gradient-accumulation steps * number of GPUs.
- LoRA learning rates (~1e-4 to 2e-4) are much higher than full fine-tuning (~1e-5). 1-3 epochs is typical for SFT.
- Catastrophic forgetting: narrow fine-tuning degrades general skills. Always re-run general benchmarks, not just the task eval.
- Distillation: train a small student to imitate a large teacher's outputs (or soft probabilities).
- Causal LMs score logits[t] against token t+1 (shift by one). The answer's EOS must stay unmasked, or the model never learns to stop.
- LoRA gradients at step 0: A's gradient is zero (it flows through B = 0) and B's is not. Zero-init both and nothing ever learns.
- bf16 has fp32's range (no loss scaling) but only 8 mantissa bits; fp16 overflows past 65,504. Small updates merged into bf16 weights can round away.
- QLoRA stores 4-bit NF4 but computes in bf16 (dequantise on the fly), so it is slower per step than bf16 LoRA.
- ZeRO-1/2/3 shard optimizer states / + grads / + weights across N GPUs (7B on 8 GPUs: 38.5 / 26.25 / 14 GB).
- KV cache per sequence = 2 * layers * kv_heads * head_dim * seq_len * bytes.
- DPO is off-policy and only sees the gap between log-ratios: the loss can fall while the chosen answer gets less likely.

## Common traps (each one must have at least one question)
- "Fine-tune the model on our docs so it knows the facts" -> unreliable, can't cite, needs retraining; use RAG.
- LoRA param count computed as r * d * k -> it's r * (d + k).
- Thinking LoRA changes the model's output at step 0 -> B = 0, so it doesn't.
- Forgetting the alpha / r scale when merging -> merged model behaves differently.
- Computing the memory of fine-tuning from weights only -> gradients, optimizer states and activations dominate.
- "QLoRA trains a 4-bit model" -> the base is frozen in 4-bit; adapters train in 16-bit.
- Training without masking prompt tokens -> the model spends capacity learning to reproduce prompts.
- Training with one chat template and serving with another -> degraded, weird outputs.
- `ignore_index` thought to lower the loss by counting ignored tokens as zero -> they're excluded from the mean.
- More data at any quality -> duplicates and noise teach the wrong thing.
- Eval examples leaking into the training set -> inflated scores.
- Judging the fine-tune by training loss alone -> overfitting; watch held-out eval loss and task evals.
- Only testing the target task -> catastrophic forgetting goes unnoticed.
- Effective batch size forgetting accumulation or GPU count -> wrong learning-rate scaling and step counts.
- Using a full-fine-tuning learning rate for LoRA (or vice versa) -> no learning, or divergence.
- Merging an adapter into a 4-bit quantised base directly -> precision loss; merge into a higher-precision copy.
- DPO without a reference model -> nothing anchors the policy; it drifts.
- pad_token = eos_token and masking labels by pad id -> the real EOS is masked too; the model never stops.
- Adding special tokens but training LoRA only on attention -> new embedding/head rows stay random.
- All labels -100 (answer truncated away) -> cross-entropy returns NaN.
- Packing with a plain causal mask -> examples attend to unrelated earlier examples.
- Step-based warmup copied to a run with fewer steps (more GPUs) -> lr never reaches peak.
- Thinking gradient accumulation speeds training up -> it only saves memory.
- Comparing eval loss across different tokenizers -> not comparable; use task metrics.
- LLM-judge comparisons in a fixed order -> position bias inflates the win rate.
- Fine-tuning on facts the model doesn't know -> teaches confident hallucination.
- Random row split with in-split dedup -> same-source near-copies leak across splits.

## Interview angle
1. **"When would you fine-tune instead of using RAG or prompting?"** When the problem is behaviour, not knowledge: a strict output format, a tone, a domain style, a classification task at scale, or making a small model match a big one (distillation) to cut cost/latency. Facts that change go in RAG. Try prompting first; it's the cheapest experiment.
2. **"Explain LoRA."** Freeze W; learn a low-rank update B @ A (rank r) scaled by alpha/r. Parameters per matrix drop from d*k to r*(d+k), e.g. 16.8M to 65k for 4096x4096 at r=8. B starts at zero, so training starts from the base model. Merge after training for zero latency, or keep adapters separate to serve many tasks on one base. SDE analogy: a patch/diff applied on top of a frozen binary.
3. **"How much GPU memory to fine-tune a 7B model?"** Full fine-tune with Adam: ~16 bytes/param -> ~112 GB plus activations (multi-GPU). LoRA in bf16: 14 GB of frozen weights + small adapter states + activations (~a 24 GB GPU). QLoRA: ~3.5-4 GB of 4-bit weights + adapters + activations (fits a 16 GB card).
4. **"How do you evaluate a fine-tune?"** Held-out eval loss during training, a task-specific eval set (exact match / rubric) before vs after, general-ability regression benchmarks for forgetting, and side-by-side comparisons vs the prompted base model.
5. **"What is DPO and why use it over RLHF?"** It trains directly on preferred vs rejected answers with a simple classification-style loss against a frozen reference model, skipping the separate reward model and RL loop; simpler and more stable.
6. **"Your fine-tune never stops generating. Debug it."** Check that EOS ends every target and its label isn't -100 (the pad = eos masking bug), that train and serve use the same chat template, and that the end-of-turn token is a stop token at inference.
7. **"Full fine-tuning a 7B model on 8 GPUs: memory per GPU?"** 16 bytes/param = 112 GB total; ZeRO-1 38.5 GB, ZeRO-2 26.25 GB, ZeRO-3/FSDP 14 GB per GPU, plus activations (cut with gradient checkpointing; use packing with per-example masks for throughput).

## Source material
To be added.
