# Inference & Optimisation (M4-M5): coverage spec

**Ladder:** LLMs for Generative AI (AIMLCZG536) › llm4genai   ·   **Prerequisites:** tf-generation, llmc-architecture
**Why it matters for AI/ML:** Training happens once; inference is paid on every request. Modules 4-5 explain why generation is slow (one token at a time, weights streamed from memory every step), how the KV cache trades memory for compute, and which optimisations (quantization, PagedAttention, FlashAttention, speculative decoding, distillation) attack which bottleneck. Past papers test this module with numbers: memory in GB, weight-streaming passes, top-k/top-p by hand, speculative acceptance.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `autoregressive-loop` | The 4-step autoregressive loop and stop criteria | the four steps | three stop criteria | min(max_new_tokens, context - prompt) | — |
| 2 | `decoding` | Greedy, random sampling and beam search | greedy picks the argmax | tail problem of random sampling, beam scores | beam search by hand, length normalisation | — |
| 3 | `sampling` | Top-k, top-p and temperature | what temperature does | top-k renormalisation, top-p cumulative set | when top-k and top-p diverge, temperature on logits | temperature + top-p interaction |
| 4 | `two-phase` | Prefill vs decode | the two phases | compute-bound vs memory-bound, parallel vs serial | KV-cache state and K/V sets per phase, TTFT vs decode speed | arithmetic intensity and batching |
| 5 | `kv-cache` | KV cache and its memory math | what is cached | why Q is not cached, one cache per layer | KV memory formula, course's Llama 2 / Qwen3 / GPT-3 table | GQA payoff, batch × context limits |
| 6 | `bottleneck` | The inference bottleneck and the optimisation map | why inference is expensive | weights × bytes, weight-streaming passes, best serving stack | optimisation table (what saves which resource), bandwidth-bound tokens/s ceiling | "Set at" column: training-time vs runtime techniques |
| 7 | `paged-batching` | PagedAttention and continuous batching | what vLLM is | internal vs external fragmentation, block table | block arithmetic, preemption (recompute vs swap) | continuous batching + paging together |
| 8 | `flash-attention` | FlashAttention | exact, faster attention | HBM vs SRAM, S and A matrices | tiling, running max/sum/output, O(N²) → O(N) memory | what it does not fix, hardware/backend choice |
| 9 | `quantization` | Quantization (PTQ, QAT, INT8, INT4) | lower-precision weights | symmetric vs asymmetric, memory math | decode gain vs small TTFT gain (past paper), calibration | W4A16 vs W8A8, formats vs methods, when there is no gain |
| 10 | `distill-prune` | Distillation and pruning | teacher and student | response vs logit distillation | when to distil vs fine-tune vs prompt | structured vs unstructured pruning speedups |
| 11 | `speculative` | Speculative decoding | draft and target models | verification in one pass, accept if q ≤ p | rejection rule 1 - p/q, residual norm(max(0, p - q)) | acceptance rate, expected tokens per pass, plateau |

## Must-know facts
- The course's loop: 1 Input tokens → 2 Compute probabilities → 3 Select token → 4 Stop or continue. Stop on the end-of-turn token, on max_new_tokens, or when prompt + generated tokens reach the context window; the binding limit is min(max_new_tokens, context - prompt).
- Greedy = argmax each step (= top-k with k = 1), not globally optimal. Random sampling picks odd tail tokens. Beam search keeps k hypotheses, scores by sum of log-probs (product of probs), length-normalised.
- Top-k keeps exactly k tokens and renormalises; top-p keeps the smallest set whose cumulative probability ≥ p (variable size). Temperature divides logits before softmax: T > 1 flatter, T < 1 sharper; it is not a decoding algorithm.
- Prefill: whole prompt in one parallel pass, KV cache starts empty, computes N K/V sets, compute-bound, sets TTFT. Decode: one token per step, cache partly built, one new K/V set per step, memory-bandwidth-bound, sets tokens/s.
- KV cache stores K and V (not Q) for every past token, one cache per layer. Memory = batch × seq × 2 × layers × kv_heads × head_dim × bytes. Course table: Llama 2 7B (4,096 ctx) ≈ 2 GB, Qwen3-8B (32,768 ctx, 8 KV heads) ≈ 4.5 GB, GPT-3 175B (2,048 ctx) ≈ 9 GB (these are GiB).
- Weights = params × bytes: FP32 4, FP16/BF16 2, INT8 1, INT4 0.5. 70B FP32 = 280 GB; 70B FP16 = 140 GB; 70B INT4 = 35 GB. A 500-token reply streams the weights ~500 times.
- Optimisation map: model-level (quantization, pruning, distillation), cheaper attention math (FlashAttention, sliding window, sparse), smarter KV storage (GQA/MQA, PagedAttention, quantized KV), faster decode (speculative decoding, fused kernels), avoid repeat work (continuous batching, prefix caching). Best real-world stack: quantization + PagedAttention + continuous batching (vLLM, TGI).
- Static contiguous KV allocation causes internal fragmentation (reserved but unused within a request) and external fragmentation (free memory scattered in gaps). PagedAttention stores KV in fixed-size non-contiguous blocks with a per-request block table; under pressure vLLM prefers recomputation over CPU swapping.
- FlashAttention is exact and IO-aware: it tiles Q/K/V into SRAM, keeps a running max, running sum of exp and a running output, never writes the N×N S or A matrices to HBM. Same FLOPs, far less memory traffic, attention memory O(N²) → O(N). It does not shrink the KV cache.
- Symmetric quantization: s = (2^(b-1) - 1)/α with α = max|x|; x_q = round(s·x). Asymmetric (zero-point): s = (2^b - 1)/(β - α), z = round(-s·α) - 2^(b-1). PTQ = after training (calibration on ~128-512 samples; RTN has none; GPTQ/AWQ/SmoothQuant use calibration); QAT = during training. W4A16 (GPTQ, AWQ) vs W8A8 (SmoothQuant); GGUF, NF4, FP8 are formats/dtypes, not methods.
- Weight quantization speeds decode about in proportion to the byte reduction (FP16 → INT4 ≈ 4×, → INT8 ≈ 2×, minus dequantisation overhead) but barely improves TTFT for long prompts, because prefill is compute-bound.
- Distillation: response distillation (fine-tune the student on teacher outputs with cross-entropy, no logits needed) vs logit distillation (match the teacher distribution with KL). Pruning: unstructured (individual weights, irregular sparsity) vs structured (neurons, heads, layers).
- Speculative decoding: a draft proposes K tokens; the target verifies all K in one forward pass. Keep x if q(x) ≤ p(x); else reject with probability 1 - p(x)/q(x); on rejection resample from norm(max(0, p - q)) and discard the rest. Output distribution equals the target's. Expected tokens per target pass with acceptance rate α and K drafts: (1 - α^(K+1))/(1 - α).

## Common traps (each one must have at least one question)
- Top-k renormalisation forgotten (using raw probabilities).
- Top-p "keep tokens with p ≥ threshold" instead of the cumulative set.
- "Temperature is a decoding strategy" -> it reshapes the distribution used by any strategy.
- Beam scores multiplied as log-probs, or no length normalisation.
- Prefill called memory-bound and decode compute-bound (swapped).
- "Q is cached too" -> past queries are never reused.
- KV cache forgotten in memory estimates, or computed with query heads instead of KV heads.
- "Quantization speeds up TTFT 4×" -> prefill is compute-bound; the gain is in decode.
- "FlashAttention is approximate / reduces FLOPs" -> exact; it reduces memory traffic.
- "FlashAttention fixes KV-cache growth" -> no; that is GQA/MLA/PagedAttention.
- "PagedAttention speeds up the attention math" -> it is memory management.
- "More draft tokens always means more speed" -> acceptance falls geometrically; speedup plateaus or drops.
- "Speculative decoding changes the output quality" -> the rejection rule keeps the target distribution.
- Confusing quantization formats (GGUF, NF4) with methods (GPTQ, AWQ).

## Interview angle
1. **"Why is decode memory-bound but prefill compute-bound?"** Prefill multiplies the weights by N prompt tokens at once (high arithmetic per byte); decode multiplies them by one token, so the GPU waits on HBM to stream weights and the KV cache.
2. **"How much memory to serve a 70B model?"** Weights 140 GB in FP16 (35 GB INT4) plus KV cache = batch × seq × 2 × layers × kv_heads × head_dim × bytes. Quantization, GQA and PagedAttention attack the two terms.
3. **"Explain PagedAttention."** OS-style paging for the KV cache: fixed-size blocks, a block table per request, allocate on demand. Removes internal/external fragmentation so more requests fit; pairs with continuous batching.
4. **"Explain speculative decoding and when it fails."** Cheap draft guesses K tokens, the target checks them in one pass; accepted tokens are free. Fails with low acceptance (domain mismatch, high temperature), a draft that is not much cheaper, or when decoding is not the bottleneck.

## Source material
- Handout: Module 4 (autoregressive generation, decoding and sampling, two-phase inference, KV caching) and Module 5 (inference bottleneck, speculative decoding, PagedAttention, FlashAttention, efficient attention variants, model compression: quantization, distillation); Lab 4 is decoding strategies and speculative decoding.
- Old-batch slides, M4 decoding deck (lines ~1760-1890): the 4-step loop with "Stop or continue?" (<|im_end|>, max new tokens, max context), greedy, random sampling's tail problem, top-k (k = 1 is greedy) and renormalisation, top-p (p = 1 means no truncation), temperature (T = 1 unchanged, T > 1 flatter, T < 1 sharper; gold 40% → 20% and magic 3% → 15% at T = 1.5), beam search with summed log-probs and length normalisation, "The cat sat" beam example.
- Old-batch slides, M5 optimisation deck (lines ~1890-2360): two-phase table, QKV caching ("past KVs don't change", "what about Q?"), one KV cache per layer, KV memory formula and the Llama 2 7B / Qwen3-8B / GPT-3 table, weights table (14 / 16.4 / 350 GB), "70B model, 500 tokens = 500 loops", optimisation table (saves / phase / set at), best stack = quantization + PagedAttention + continuous batching; speculative decoding with p(x)/q(x), "The cat sat on" worked example (mat rejected at 0.40, floor resampled 85.7%), Gemma 4 drafter / MTP; PagedAttention, internal/external fragmentation (200 of 2,048; gaps 600 + 400 + 300), block table, recomputation preferred over swapping.
- Old-batch slides, M5 deck 2 (lines ~2450-2870): quadratic attention costs; HBM ↔ SRAM data flow of S and A; FlashAttention tiling and running values; exact, same FLOPs; Ampere/Hopper, FA3 not on A100; sample questions (rare-disease exact attention; 12k-token OOM fixed by FlashAttention); symmetric/asymmetric quantization worked examples (α = 10.8, s = 11.76, -1.95 → -23; zero-point → -50); PTQ/QAT, calibration, RTN/GPTQ/AWQ/SmoothQuant, W4A16 vs W8A8, GGUF/NF4/FP8; distillation (response vs logit, Llama-3.2-1B/3B, DeepSeek-R1-Distill), distilling step-by-step, pruning.
- Old-batch revision questions (lines ~3050-3105): prefill vs decode "why", fragmentation definitions, top-k vs top-p divergence, the 4-step loop and stop-criteria arithmetic (4,096 ctx, 2,400 prompt, 1,800 max_new → 1,696).
- Exam patterns: midsem papers ask the two phases with (i) KV-cache state at start, (ii) number of K/V sets computed for N prompt and M generated tokens, (iii) compute- vs memory-bound with reason; "a 70B FP32 / 13B FP16 model generating a 500 / 250-token response: weight size and number of weight-streaming passes, and why quantization, KV caching and speculative decoding exist"; greedy / top-k (with renormalised probabilities) / top-p (cumulative sums) by hand on an 8-token distribution; FlashAttention bottleneck, exact or approximate, FLOPs or memory access; GQA vs MLA. Endsem papers ask "a 70B model in FP16 switched to 4-bit (or INT8): why decode speeds up ~4× (~2×) but TTFT barely improves, and one condition with no gain", and "speculative decoding: why speedup plateaus as draft length grows (acceptance, verification cost, wasted work), why it helps, and conditions where it helps least / most".
