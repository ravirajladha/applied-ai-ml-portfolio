# Pre-training & Scaling (M2): coverage spec

**Ladder:** LLMs for Generative AI (AIMLCZG536) › llm4genai   ·   **Prerequisites:** llmc-foundations (tokens, embeddings, decoder-only models), cross-entropy and learning-rate schedules from deep learning basics
**Why it matters for AI/ML:** Module 2 explains how a base model is built and what it costs: the self-supervised objective, the data pipeline that turns the web into a corpus, the scaling laws that fix model size and token budget before a run, and continued pre-training for domain models without catastrophic forgetting. The mid-sem always has a CPT / forgetting question, scaling-law numericals (C ≈ 6ND, 20 tokens per parameter) appear in the practice sets, and Assignment 1 is CPT on IT-helpdesk text.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `objectives` | Self-supervised objectives: MLM, span corruption, CLM | label comes from the text | MLM 15% / span corruption sentinels / CLM, which model uses which | why modern LLMs use CLM, examples per token | number of training signals per sequence under each objective |
| 2 | `training-loop` | Teacher forcing, loss and perplexity | lower perplexity = better | teacher forcing, all positions in parallel, L = −mean log P, PPL = e^L | perplexity by hand, from probabilities or nats | PPL not comparable across tokenizers, bits-per-byte, PPL after SFT/RLHF |
| 3 | `data-pipeline` | Data pipeline: filter, de-dup, PII, packing | raw web is noisy | the four stages in order, why de-duplicate (3 reasons) | MinHash / n-gram overlap, packing arithmetic, heuristic vs classifier filters | model-as-judge filtering (Llama 2 labels → fastText / DistilRoBERTa), contamination |
| 4 | `mixture-curriculum` | Data mixture, curriculum and annealing | — | mixture = proportions, curriculum = order | annealing (LR → 0 + upsample math/code), why 8B gains but 405B doesn't | long context as curriculum, staged recipes |
| 5 | `compute` | Compute and parameter counting | — | C ≈ 6ND | 12·L·d² per model, FLOPs for a run, GPU-hours | active vs total params for MoE (DeepSeek-V3 vs Llama 405B) |
| 6 | `scaling-laws` | Kaplan vs Chinchilla vs overtraining | what a scaling law is | Kaplan 10× → 5× N / 2× D; Chinchilla ~20 tok/param | Chinchilla-optimal N and D from a budget, tokens/param tables | why overtrain (serving cost), test-time and RL scaling, α exponents |
| 7 | `domain-adaptation` | Domain adaptation: CPT vs from scratch | what CPT is | three routes (regular / CPT / from scratch on D1 ∪ D2) | BloombergGPT vs FinLLaMA, choosing a route | mixing ratios, CPT vs instruction fine-tuning |
| 8 | `forgetting` | Catastrophic forgetting and the CPT LR recipe | what forgetting is | replay, LoRA/PEFT, LR schedule | re-warm → re-decay → replay, why re-warm | trade-offs (peak LR vs forgetting), EWC, lower LR, scenario diagnosis |
| 9 | `recipes` | Modern recipes: Llama 3, Qwen3, DeepSeek-V3, Gemma 2 | — | Llama 3 three stages, Qwen3 three stages | batch-size ramp, distillation in Gemma 2, multi-token prediction, FP8 | earlier models build the next generation's data |
| 10 | `parallelism` | Parallelism types | — | data / tensor / pipeline / context / expert | which split for which bottleneck | Llama 3 vs DeepSeek-V3 choices |
| 11 | `emergence-base` | Emergent abilities and base vs instruct | base model continues text | emergence definition, ICL without weight updates | sharpness + unpredictability, the "mirage" critique | why base models ramble (objective), CoT and small models |

## Must-know facts
- Self-supervised learning: the label is taken from the text itself (next token or masked token); these pretext tasks need no human labels, so every corpus token is a free training example.
- MLM (BERT): hide ~15% of tokens, predict them using both sides. Span corruption (T5): replace spans with sentinels <X>, <Y>; decoder writes the spans. CLM (GPT-2/3, Llama 3, Qwen3, DeepSeek-V3): predict the next token from the previous ones. Modern LLMs use CLM because it trains generation directly.
- Teacher forcing: the input at every position is the true previous token, not the model's own guess. All positions are trained in one parallel pass under a causal mask; the loss updates all weights including embeddings.
- L = −(1/T) Σ log P(w_{t+1} | w_≤t); perplexity = exp(L) = (1 / Π p)^(1/T). Lower is better. Perplexity is only comparable with the same tokenizer and eval set; it is not meaningful for tracking SFT/RLHF.
- Data pipeline: filter (heuristics or a quality classifier) → de-duplicate (n-gram / MinHash) → remove PII → tokenize + pack (doc1 <eos> doc2 <eos> ... fills each window, no padding).
- De-duplicate because repeated text is memorised, it wastes compute, and it prevents test-set contamination.
- Open corpora: FineWeb 15T, RedPajama-V2 30T, Dolma 3T (OLMo), The Stack v2 (code).
- Mixture = proportions of sources; curriculum = how the mixture changes over time; annealing (Llama 3) = LR lowered to zero while high-quality math/code is upsampled at the end (8B gains on GSM8K/MATH, 405B negligible). Long context is a curriculum (8K → 128K).
- C ≈ 6·N·D FLOPs (dense; N = active parameters for MoE). Params ≈ 12·L·d² (attention 4d² + FFN 8d²); GPT-3 12 × 96 × 12,288² ≈ 175B.
- Kaplan (2020): L(N) = (N_c/N)^α, α ≈ 0.05-0.1 (diminishing but predictable); model size matters most; 10× compute → ~5× model, ~2× data. GPT-3: 175B params, 300B tokens (~1.7 tok/param).
- Chinchilla (2022): scale N and D equally (10× compute → ~3.2× each); ~20 tokens/param is compute-optimal; Chinchilla 70B on 1.4T tokens beat Gopher 280B at the same compute. With D = 20N, C = 120N².
- Today: overtrain small models far past 20 tok/param (Llama 3 8B on ~15T ≈ 1,900 tok/param) because they are cheaper to serve; plus test-time compute scaling (o1, DeepSeek-R1) and RL-compute scaling (R1-Zero).
- Domain routes: regular pre-training (random init, D1), CPT (pre-trained on D1, continue on D2 + some D1; low cost, default), domain pre-training from scratch on D1 ∪ D2 (very expensive). BloombergGPT 50B (363B finance + 345B general, from scratch) vs FinLLaMA 8B (CPT on Llama 3 8B, 52B finance + 18B general ≈ 3:1).
- Catastrophic forgetting: new-distribution updates overwrite old knowledge. Mitigations: replay (most effective; ~5% often enough, FinLLaMA ~25%), LR schedule (re-warm to peak then re-decay), LoRA/PEFT (forgets less, learns less), plus lower LR and EWC (old-batch list).
- CPT LR recipe: repeat the original schedule: re-warm → re-decay (cosine) → + replay. Re-warm because the LR at the end of pre-training is ~0.
- Llama 3 405B: ~15.6T tokens at 8K with batch 4M → 8M → 16M; long-context 8K → 128K in six stages (~800B tokens); annealing on the final 40M tokens. Model-as-judge: Llama 2 labels a sample, fastText and DistilRoBERTa classifiers score the corpus.
- Qwen3: 36T tokens, 119 languages; S1 general 30T+ at 4K, S2 reasoning ~5T, S3 long context to 32K; earlier Qwen models extract, clean and synthesise data.
- DeepSeek-V3: MoE 671B total / 37B active, 14.8T tokens, multi-token prediction + FP8, ~2.8M H800 GPU-hours (~3.3 × 10²⁴ FLOPs vs Llama 3.1 405B's ~3.8 × 10²⁵, ~30.8M H100-hours). Gemma 2: 27B from scratch, 2B and 9B distilled.
- Parallelism: data (batches), tensor (each matmul), pipeline (layers), context (one long sequence), expert (MoE experts). Llama 3: tensor + context + pipeline + data; DeepSeek-V3: pipeline + expert + data.
- Emergent ability: not present in smaller models, present in larger ones; sharp and unpredictable; does not follow scaling laws. Schaeffer et al. (2023): may be a "mirage" of metrics. ICL (GPT-3) uses no weight updates.
- A base model continues text (its objective is next-token prediction); instruct models answer. Llama-3.1-8B vs -8B-Instruct; Qwen3-8B-Base vs Qwen3-8B.

## Common traps (each one must have at least one question)
- "BERT-style MLM is what GPT uses" -> GPT uses CLM; MLM does not train generation.
- "Teacher forcing feeds the model's own predictions back during training" -> it feeds the ground truth; own predictions are used only at generation time.
- Perplexity computed as product of probabilities without the 1/T root, or as e^(sum) instead of e^(mean).
- Comparing perplexities across different tokenizers -> not comparable; use bits-per-byte.
- "Lower perplexity = better on the downstream task" -> intrinsic ≠ extrinsic.
- "De-duplication is only about saving disk space" -> memorisation, wasted compute, contamination.
- Padding short documents instead of packing -> wasted compute.
- Using C = 6ND with total MoE parameters -> use active parameters.
- Using 2ND (inference) for training FLOPs -> training is ~6ND (forward + backward).
- "Chinchilla says 20 tokens/param is the minimum / the best possible model" -> it is the compute-optimal (cheapest-to-a-loss) point.
- "Chinchilla: 10× compute → 10× model" or Kaplan's 5×/2× swapped.
- "Overtraining is a mistake" -> it trades extra training compute for cheaper inference.
- "CPT on domain data only" -> catastrophic forgetting; mix general data (replay).
- Not re-warming the LR for CPT -> LR ~0, model barely learns.
- "LoRA prevents forgetting at no cost" -> it also learns less new knowledge.
- "Annealing helps big models most" -> Llama 3 8B gained, 405B negligible.
- "Emergent abilities can be predicted from scaling-law curves" -> they don't follow them.
- "A base model is broken because it continues the question list" -> it is doing exactly its objective.
- Confusing tensor parallel (split matmuls) with pipeline parallel (split layers).
- "CPT = instruction fine-tuning" -> CPT uses the same LM objective on raw text; IFT uses labelled instruction-response pairs.

## Interview angle
1. **"You have 6 × 10²³ FLOPs. How big a model, how many tokens?"** Chinchilla: C = 6ND with D = 20N → C = 120N² → N ≈ 70B, D ≈ 1.4T. But if the model will be served at scale, train a smaller model on more tokens (overtrain), like Llama 3 8B on 15T.
2. **"Build a finance LLM: from scratch or CPT?"** CPT from a strong base (FinLLaMA: Llama 3 8B + 52B finance + 18B general) unless you have a BloombergGPT-sized corpus and budget. Mix general data (replay), re-warm and re-decay the LR, evaluate both domain and general benchmarks.
3. **"Why de-duplicate pre-training data?"** Memorisation, wasted compute, and benchmark contamination (inflated scores). MinHash / n-gram overlap at scale.
4. **"What is perplexity and when is it misleading?"** exp(mean NLL), effective branching factor; misleading across tokenizers (use bits-per-byte), for downstream task quality (intrinsic vs extrinsic), and after SFT/RLHF.
5. **"Why was DeepSeek-V3 ~10× cheaper than Llama 3.1 405B?"** MoE: only 37B of 671B parameters are active per token, so 6·N_active·D is ~10× smaller; plus FP8 and multi-token prediction.

## Source material
- **Self-supervised learning and objectives (Session-02 §2-3, CS-2 slides 5-6):** label from the text itself, pretext tasks, every token a free example; MLM (BERT, ~15%), span corruption (T5, sentinels <X>, <Y>), CLM (GPT-2/3, Llama 3, Qwen3, DeepSeek-V3); "modern LLMs use CLM".
- **Training (Session-02 §4, CS-2 slide 7):** teacher forcing, all positions in parallel with the causal mask, updates everything incl. embeddings; L = −(1/T) Σ log P(w_{t+1} | w_≤t), PPL = exp(L); worked example 0.5, 0.25, 0.5, 0.25 → L = 1.04, PPL ≈ 2.83.
- **Data (Session-02 §5, CS-2 slides 10-11, old-batch pre-processing slides):** FineWeb 15T, RedPajama-V2 30T, Dolma 3T, The Stack v2; pipeline filter → de-dup → PII → tokenize + pack; why de-dup (memorisation, waste, contamination), MinHash/n-gram overlap; heuristic vs classifier filtering.
- **Mixture/curriculum (Session-02 §6, CS-2 slide 12):** mixture vs curriculum vs annealing (LR → 0, upsample math/code; Llama 3 8B gains, 405B negligible); long context 8K → 128K; Session-3 lecture: context window includes output, recipes are general → reasoning → long context.
- **Scaling laws (Session-02 §7, CS-2 slides 13-16, old-batch Question 3):** C ≈ 6ND; Kaplan L(N) = (N_c/N)^α, α ≈ 0.05-0.1, 12d² per layer, GPT-3 ≈ 175B, 10× → 5× N / 2× D; Chinchilla 3.2× each, ~20 tok/param, table (LaMDA 1.2, GPT-3 1.7, Jurassic 1.7, Gopher 1.1, MT-NLG 0.5, Chinchilla 20); worked example C = 6 × 10²³ → 70B / 1.4T; today: overtraining (Llama 3 8B ≈ 1,900 tok/param), test-time compute, RL compute. Old-batch answer: 8B × 20 = 160B, 15T / 160B ≈ 94×.
- **Domain adaptation and forgetting (Session-02 §8-9, CS-2 slides 17-20, old-batch CPT slides):** three routes, BloombergGPT vs FinLLaMA; forgetting mitigations (LoRA/PEFT, LR schedule, replay ~5%, FinLLaMA ~25%); old-batch list adds lower LR, LR warmup and EWC; CPT LR recipe re-warm → re-decay → replay.
- **Recipes (Session-02 §10, CS-2 slides 21-25):** comparison table (filtering, synthetic data, mixing, long-context stage, annealing, distillation, efficiency); Llama 3 three stages and model-as-judge filtering; Qwen3 three stages, 36T, 119 languages, data built by earlier Qwen models; Gemma 2 distillation; DeepSeek-V3 MoE + MTP + FP8; OLMo 2 fully open.
- **Cost and parallelism (Session-02 §11):** Llama 3.1 405B 15.6T tokens ~3.8 × 10²⁵ FLOPs, ~30.8M H100-hours; DeepSeek-V3 ~3.3 × 10²⁴, ~2.8M H800-hours (2,048 GPUs × ~57 days); data/tensor/pipeline/context/expert parallelism and which models used which.
- **Emergence and base models (Session-02 §12-13):** definition, sharpness and unpredictability, "mirage" (Schaeffer et al. 2023), ICL / instruction following / CoT; base model continues text ("capital of Germany? ..."), instruct answers; Hub naming.
- **Exam patterns:** the June-2026 mid-sem (both sets) has a 5-mark CPT question: define regular pre-training / CPT / retraining on D1 ∪ D2, "why add 18B general tokens to 52B finance tokens, which failure mode does it mitigate", "list three techniques other than replay" and "two LR-based mitigations", and "define self-supervised learning and why no human labels are needed"; the old-batch practice set asks Kaplan vs Chinchilla for a 10× budget, 20 tok/param for an 8B model and the Llama 3 overtraining ratio; the Sep-2025 end-sem papers compute perplexity from three token probabilities and from a mean NLL in nats, then ask why lower PPL ≠ better BLEU, why PPLs from different tokenizers are not comparable, and whether PPL suits RLHF. Bank questions mirror these with new domains (legal, medical, IT helpdesk) and numbers.
