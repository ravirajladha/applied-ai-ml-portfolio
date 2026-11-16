# Architecture & MoE (M3): coverage spec

**Ladder:** LLMs for Generative AI (AIMLCZG536) › llm4genai   ·   **Prerequisites:** tf-attention, llmc-foundations
**Why it matters for AI/ML:** Module 3 is the "what is inside a modern decoder" module: why every 2025-26 open model uses RMSNorm + Pre-Norm, RoPE, SwiGLU and GQA/MLA, and why the biggest ones are Mixture-of-Experts. An AI engineer reads model cards in these terms (e.g. "671B total / 37B active, 8 KV heads") and has to turn them into memory and compute estimates.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `attn-review` | Self-attention as the course reviews it | Q/K/V roles in the course's words, causal masking | why the score matrix is built "in one go" in training | — | — |
| 2 | `mha-shapes` | Multi-head attention shape calculations | d_k = d/h | per-head W_Q, Q/K/V shapes, concat, W_O | why h heads cost about the same as one full head | parameter counts of the attention block |
| 3 | `decoder-block` | The decoder block, FFN and residual stream | block contents, FFN is 2 layers, d_ff = 2048 | FFN parameter count, FFN is position-wise | Pre-Norm block order, residual stream view | — |
| 4 | `normalization` | LayerNorm, RMSNorm, Pre/Post-Norm, QK-Norm | what normalization does | LayerNorm vs RMSNorm, formulas of Pre/Post-Norm | deep-model choice (RMSNorm + Pre-Norm), QK-Norm for unstable logits | gradient highway argument, OLMo 2 / Gemma 3 placements |
| 5 | `positional-advances` | RoPE and NoPE | why position is needed | RoPE rotates Q and K, relative distance | RoPE worked numbers, θ_i formula | NoPE layers in hybrids |
| 6 | `activations` | GELU, Swish/SiLU, GLU, SwiGLU | what an activation is | ReLU vs SiLU numbers, GLU = 3 matrices | gating intuition, parameter-matched SwiGLU width | the bilinear layer is still nonlinear |
| 7 | `efficient-attention` | MQA, GQA, MLA, sliding window, sparse, linear | what MQA/GQA share | exact vs approximate variants | MLA latent cache numbers, which variant attacks which cost | MLA up-projection absorption, MHA vs GQA as different models |
| 8 | `moe-basics` | Dense vs sparse layers, experts and the router | what an expert is | the router is an FFNN with softmax, output = gate × expert, sparse vs dense MoE | benefits vs issues listed by the course | one router per MoE layer, per-layer paths |
| 9 | `moe-routing` | Top-k routing and KeepTopK | top-1 vs top-k | KeepTopK sets the rest to -inf, renormalised gate | noisy KeepTopK, token choice | routing arithmetic by hand |
| 10 | `moe-balance` | Load balancing, expert capacity, token overflow | why balance matters | expert capacity, token overflow | capacity factor arithmetic, collapse | trade-offs of capacity, auxiliary loss |
| 11 | `moe-params` | Total vs active parameters and expert parallelism | total vs active | FLOPs follow active, memory follows total | Mixtral / DeepSeek-V3 counts, 6·N_active·D | expert parallelism and all-to-all, serving cost |

## Must-know facts
- Course Q/K/V roles: Query = the current element being compared to preceding inputs; Key = a preceding input being compared to determine a similarity weight; Value = what gets weighted and summed into the output.
- Original Transformer: d = 512, h = 8, d_k = d_v = d/h = 64, d_ff = 2048. Each head has W_Q_i, W_K_i in R^(d×d_k), W_V_i in R^(d×d_v); concat is [N × h·d_v]; W_O is [h·d_v × d]; output [N × d].
- h heads cost h · N² · (d/h) = N² · d: about the same as one full-width head.
- FFN = 2 linear layers with an activation between; d_ff > d. FFN params ≈ 2·d·d_ff = 8d² (twice the attention block's 4d²).
- LayerNorm forces zero mean and unit variance (gain γ and bias β). RMSNorm only divides by the root-mean-square and keeps the gain: fewer parameters, no mean, ~7-15% faster.
- PostNorm(x) = LayerNorm(x + Sublayer(x)); PreNorm(x) = x + Sublayer(LayerNorm(x)). Pre-Norm keeps a "gradient highway" through the residual, trains stably at 100+ layers and needs less warm-up.
- QK-Norm normalises Q and K (per head) before the dot product (and before RoPE) to stop softmax saturation.
- RoPE rotates Q and K pairwise by position-dependent angles θ_i = 10000^(-2(i-1)/d); the score depends on relative distance m - n. NoPE drops positional info in some layers (SmolLM3: every fourth layer).
- GLU FFNs use 3 matrices instead of 2: SwiGLU(x) = Swish(W_a x) ⊙ (W_b x), then a down projection.
- MQA: one shared K,V; GQA: G groups of K,V; both are exact attention and cut KV-cache memory and bandwidth. MLA (DeepSeek-V2) caches a compressed latent (576 numbers per token per layer vs 32,768 for MHA, ~55× smaller).
- Sliding window and sparse attention (NSA, DSA) are approximate; linear attention (e.g. KDA) replaces the growing cache with a fixed state.
- MoE replaces the dense FFN with many expert FFNs plus a router (gate network, H(x) = Wx, softmax). Output = Σ gate_i × expert_i(x) over the selected experts.
- KeepTopK sets all but the top-k router logits to -inf so their softmax weight is 0; trainable Gaussian noise stops the same experts always winning.
- Expert capacity caps tokens per expert; overflow goes to the next expert or, if all are full, skips the expert layer through the residual (token overflow).
- Total parameters set memory; active parameters set compute per token. DeepSeek-V3 671B total / 37B active; Llama 4 Maverick 128 experts, 17B active; Mixtral 8x7B ≈ 46.7B total / 12.9B active (top-2).
- Expert parallelism puts different experts on different GPUs and needs all-to-all token exchange.

## Common traps (each one must have at least one question)
- "More heads = more compute" -> per-head width shrinks; total cost stays ~N²·d.
- "RMSNorm centres the activations" -> it only rescales; no mean is subtracted.
- Writing Post-Norm and Pre-Norm the wrong way round.
- "The FFN mixes information across tokens" -> it is applied per token; attention mixes tokens.
- "RoPE adds a position vector to the embedding" -> it rotates Q and K inside attention.
- "GQA approximates MHA at inference" -> a GQA model is its own model; its attention is exact.
- "Sliding window is exact like FlashAttention" -> it drops far tokens; it is approximate.
- "MoE 8x7B = 56B and all of it runs per token" -> shared attention; only top-k experts run.
- "MoE needs less GPU memory" -> all experts must be resident; memory follows total params.
- "Top-k picks experts, then the outputs are simply averaged" -> they are weighted by the gate values.
- "Overflowed tokens are dropped from the sequence" -> they skip the expert and pass through the residual.
- "The router is a fixed hash" -> it is a learned FFN trained with the model.

## Interview angle
1. **"Why RMSNorm + Pre-Norm?"** Cheaper (no mean, fewer params) and stable at depth: the residual is an untouched gradient path, so 100+ layers train without fragile warm-up.
2. **"Explain MoE in one minute."** Swap the FFN for N expert FFNs and a learned router; each token runs only its top-k experts weighted by the gate. Capacity grows with total params while per-token FLOPs follow active params. Costs: load balancing, routing overhead, instability, and memory for all experts.
3. **"How do GQA and MLA differ?"** Both shrink the KV cache. GQA shares K/V heads across query groups; MLA caches one compressed latent per token and rebuilds (or absorbs) K/V through learned up-projections, keeping per-head K/V.
4. **"What is expert capacity and token overflow?"** A per-expert token limit; tokens over it go to the next choice or skip the layer through the residual, trading a little quality for predictable compute.

## Source material
- Handout, Module 3 (session 4): classical attention & Transformer review; normalization (LayerNorm, RMSNorm, norm placement); positional encoding advances (RoPE); advanced activations (GELU, Swish, GLU); Mixture of Experts; emerging architectures. Session 7 adds GQA, MQA, MLA; session 13 adds sub-quadratic, sparse and hybrid attention.
- Old-batch slides, "Attention and Transformers Review" (lines ~80-200): Q/K/V roles; the matrix "comparing each token with every token that came before", created "in one go" in training; MHA shape worked example (N = 4, d = 512, h = 8 → d_k = 64, W_O 512×512); FFN d = 512, d_ff = 2048.
- Old-batch slides, M3 deck (lines ~945-1245): RMSNorm (no mean, ~7-15% faster), PostNorm/PreNorm formulas, gradient highway, OLMo 2 and Gemma 3 placements; QK-Norm; RoPE intuition, θ_i = 10000^(-2(i-1)/d) and the q = [1, 0, 0, 1] worked example; NoPE (SmolLM3 every 4th layer); GELU, SiLU/Swish, GLU (3 FC layers), SwiGLU.
- Old-batch slides, MoE: dense vs sparse layers, router H(x) = Wx + softmax, output × gate value, KeepTopK (with trainable Gaussian noise, -inf), token choice (top-1 / top-k), expert capacity, token overflow, sparse vs dense MoE, Llama 4 Maverick (128 experts, 17B active), dynamic sparsity (Qwen3-Next), benefits and issues; sample questions on deep-model normalization, QK-Norm and expert capacity.
- Old-batch slides, M5 efficient attention (lines ~2450-2480, 2730-2960): which method attacks which cost; MQA/GQA exact, "different models"; MLA (DeepSeek-V2, latent 512 + 64 = 576 vs 2·128·128 = 32,768, ~55×); sliding window, NSA/DSA, linear attention (KDA).
- Learner notes (Session-02, Quick-Revision-Sheet): DeepSeek-V3 MoE 671B / 37B active; expert parallelism listed with data/tensor/pipeline/context parallelism; 6·N·D uses active params for MoE.
- Exam patterns: midsem papers ask shape calculations for MHA (d_k, W_Q_i, concat, W_O, "why per-head reduction keeps compute similar"), "which normalization for a 100+ layer model and why", QK-Norm for unstable attention, "explain expert capacity and token overflow", "why SwiGLU/GELU over ReLU", and "GQA and MLA target the same bottleneck: name it and explain each". Answers are marked on naming the course term plus a one-line reason.
