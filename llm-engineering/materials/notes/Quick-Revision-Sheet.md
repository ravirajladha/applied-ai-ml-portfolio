# Quick Revision Sheet — Sessions 0–3

> One page for exam eve. Details in the session notes.

## Foundations (S0–S1)
- **LM:** P(w₁…wₙ) = ∏ P(wᵢ | w<ᵢ) — scoring a sentence ⇔ predicting the next token.
- **LLM** = decoder-only Transformer, self-supervised next-token prediction. **"Large"** = params (B) + data (T tokens) + context window.
- Any NLP task = prompt + next-word prediction. **Sampling** → generative. Output **one token at a time**.
- Pipeline: **tokenizer → embedding + position → N Transformer blocks → LM head (unembedding + softmax)**.
- Attention = tokens talk · FFN = each token thinks · residual = add, never replace.

## Tokenization
| Word | Subword | Char | Byte |
|------|---------|------|------|
| OOV, bloated vocab | **modern default** | long seqs | vocab 256, never OOV, long seqs |
- **BPE:** chars → count adjacent pairs (× word freq) → merge most frequent → repeat to target vocab. Hyperparams: **vocab size, min frequency**.
  `hug10 pug5 pun12 bun4 hugs5` → **ug(20)** → un(16) → hug(15). `mug` → [UNK] (no "m") → fix = **byte-level BPE**.
- Learner (once, builds vocab + merges) vs segmenter (every input). **Use the model's own tokenizer.**
- WordPiece `##` (BERT) · byte-level BPE `Ġ` (GPT/Llama/Qwen) · SentencePiece `▁`, no pre-tokenizer (T5, Gemma, Llama 1/2).
- tiktoken = count only. HF tokenizers = train/load.

## Embeddings & position
- **E = \|V\| × d**, row lookup, learned with the model. Llama 3 8B: 128,256 × 4096 ≈ **525M** (LM head same size unless tied).
- Static (word2vec) vs contextual (hidden states). Cosine = a·b / (|a||b|).
- Position: sinusoidal (added) · learned (added; GPT-2/BERT) · **RoPE** (rotates Q, K; Llama/Qwen/DeepSeek).
- Context window counts **prompt + output**.

## Pre-training (S2)
- Objectives: **MLM** (BERT, 15% masked) · **span corruption** (T5) · **CLM** (GPT/Llama — modern).
- **Teacher forcing**, all positions in parallel with causal mask. **L = −(1/T) Σ log P(next)**, **PPL = e^L** (lower = better).
- Data: **filter → de-dup (MinHash; avoids memorisation, waste, test contamination) → PII removal → tokenize + pack**.
- Mixture (proportions) · curriculum (order) · **annealing** (LR → 0 + upsample math/code at the end).
- **C ≈ 6ND.** Params/layer ≈ 12d² (GPT-3: 12·96·12288² ≈ 175B).
- **Kaplan:** 10× C → 5× N, 2× D (GPT-3: 1.7 tok/param). **Chinchilla:** scale equally, **~20 tok/param** (70B, 1.4T beat Gopher 280B). **Today:** overtrain (Llama 3 8B ≈ 1,900 tok/param), test-time compute, RL compute.
- Domain: from scratch (BloombergGPT 50B) vs **CPT** (FinLLaMA, 8B, 3:1 finance:general) — CPT default.
- **Catastrophic forgetting** fixes: **replay** (~5–25% general data) + **re-warm & re-decay LR** (+ LoRA).
- Llama 3: 15.6T @8K → long-context 8K→128K (800B) → anneal (40M). Model-as-judge: Llama 2 labels sample → fastText/DistilRoBERTa score all.
- Qwen3: 36T, 119 languages; general → reasoning → long (32K); earlier Qwen models make the data.
- DeepSeek-V3: MoE 671B/37B active, FP8, MTP, ~2.8M H800-h (~10× less compute than Llama 405B).
- Parallelism: data · tensor (matmul) · pipeline (layers) · context (sequence) · expert (MoE).
- Emergence: sharp + unpredictable; "mirage" = metric artefact. Base model **continues** text; instruct model answers.

## Fine-tuning (S3)
- CPT (unlabelled, same objective) · full FT · PEFT · SFT ⊃ **IFT** · MLM-FT.
- **ICL:** no weight change; costs context every call, nothing persists → fine-tune.
- IFT data: human (Dolly) · template (FLAN) · synthetic (Alpaca) · hybrid (**Self-Instruct**: 175 seeds → 52K, classify task → generate instances → filter).
- Store model-agnostic **JSONL** {instruction, input, output}; render with model's chat template (`[INST]…[/INST]`).
- PEFT: **addition** (adapters, prompt/prefix) · **selective** (BitFit, freezing) · **reparam** (LoRA).
- Adapter: down → nonlinearity → up + residual. d=1024, m=24 → 49,152 vs 1,048,576.
- **h = Wx + ΔWx.** LoRA: **ΔW = BA**, B = 0 init, A ~ N(0,σ²), **h = Wx + (α/r)BAx**, params **r(d+k)**. Merge after training → no latency.
- Multi-tenant: one base + many adapters.
- **QLoRA:** 4-bit **NF4** frozen base + BF16 LoRA, dequantize on the fly; **double quantization** (0.5 → 0.127 bits/param); **paged optimizers**. 65B on one 48 GB GPU.
- Merging: one model from many (weight averaging, Model Soups, SLERP) — not ensembling.
