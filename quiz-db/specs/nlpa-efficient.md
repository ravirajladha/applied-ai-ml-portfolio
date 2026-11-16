# Scalable & Efficient NLP Systems (S15): coverage spec

**Ladder:** NLP Applications (AIMLCZG519) › Session 15 Scalable & Efficient NLP Systems   ·   **Prerequisites:** nlp-tokens, tf-attention, llmc-inference (for LLM serving internals), ops-serving (for general serving)
**Why it matters for AI/ML:** Session 15 argues that efficiency is a product requirement: training and serving cost, latency, energy and access all depend on it. It covers curated data pipelines, the three ways to shrink a model (quantization, pruning, knowledge distillation), efficient architectures (ALBERT sharing, MoE, sparse/linear attention, efficient tokenization) and inference optimisation and deployment. The end-sem papers test it with three-step calculations: training compute and cost (C ≈ 6ND with MFU), latency/throughput/fleet size, and FP16/INT8/INT4 memory and GPU counts.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `need-efficiency` | Why efficiency is a product requirement | latency, cost, energy, access | serving cost over a lifetime vs one-time training | parameter growth BERT -> PaLM, which lever for which goal | choosing the bottleneck to attack |
| 2 | `data-pipelines` | Scalable data pipelines and training cost | dedup, quality filtering | streaming shards, domain mixing (LLaMA / RedPajama) | the 3-step training-cost example (6ND, MFU, $) and dedup savings | GPUs needed for a deadline, budget checks |
| 3 | `quantization` | Quantization of NLP models | lower precision, bytes per param | FP16/INT8/INT4 footprints, dynamic INT8 for BERT Linear layers | LLM.int8() outliers, PTQ vs QAT, GPU counts (round up) | what quantization does not shrink, accuracy traps |
| 4 | `pruning` | Pruning weights and attention heads | remove unneeded weights | magnitude pruning, sparsity %, structured vs unstructured | head pruning (Michel et al.), why unstructured gives no speedup | lottery ticket, movement pruning, prune-then-fine-tune |
| 5 | `distillation` | Knowledge distillation (DistilBERT, TinyBERT) | teacher and student | soft targets, temperature | DistilBERT recipe (6 layers, init from teacher, triple loss) and numbers | TinyBERT layer-wise and two-stage distillation, task-specific vs task-agnostic |
| 6 | `low-rank` | Low-rank factorisation | split one big matrix in two | parameter count m·n vs r(m+n) | truncated SVD of a weight matrix, ALBERT's V×E + E×H embedding | choosing r, when factorisation saves nothing |
| 7 | `efficient-arch` | Efficient architectures | ALBERT, MobileBERT, MoE names | ALBERT cross-layer sharing, MoE total vs active | sharing cuts parameters not FLOPs; MobileBERT bottlenecks; SOP | sparse vs linear attention, efficient tokenization and sequence length |
| 8 | `inference-opt` | Inference optimisation for BERT-style models | batching, caching | dynamic padding, length bucketing, latency vs throughput | ONNX / ONNX Runtime / TensorRT graph optimisation, CPU vs GPU | stacking compressions, sequence-length cost |
| 9 | `deployment-scale` | Deployment and serving at scale | edge vs cloud | the course's L, X, G worked example | decode-speed and batch changes, speculative decoding effect | fleet sizing trade-offs, autoscaling, llama.cpp / vLLM roles |

## Must-know facts
- The course's cost-of-scale numbers: GPT-3 (175B) ~$4.6M and 1,287 MWh to train once; top model size grew ~500x from BERT (2018) to PaLM (2022).
- Efficiency is a product requirement: 400 ms of extra search latency measurably cut usage; lifetime serving compute can exceed one-time training cost; Strubell et al. (2019) put one large NLP training run at about five cars' lifetime CO2; compressed models (DistilBERT, TinyBERT) widen access.
- Scalable data = quality, not just quantity: deduplication (Lee et al. 2022: less compute, same or better quality), quality filtering (CCNet, Gopher rules), streaming sharded batches (WebDataset, MosaicML StreamingDataset), deliberate domain mixing (LLaMA 1.4T tokens; RedPajama 1.2T reproduction, CommonCrawl ~67%).
- Training cost, course style: C = 6 × params × tokens; H = C ÷ (peak FLOP/s × MFU) ÷ 3600; cost = H × $/GPU-hour. Compute is linear in tokens, so halving tokens via dedup halves the bill.
- Three ways to shrink a model: quantization (2-4x smaller, minimal loss), pruning (30-60% fewer parameters at similar accuracy), distillation (40-60% smaller, 95%+ of teacher quality). They stack: quantize a distilled or pruned model.
- Memory = params × bytes/param: FP32 4, FP16 2, INT8 1, INT4 0.5. GPUs to hold weights = ceil(memory ÷ GPU memory).
- LLM.int8() keeps rare high-magnitude outlier features in FP16 and quantizes the rest to INT8: BLOOM-176B 352 GB -> ~180 GB with no measurable quality loss; ships in bitsandbytes.
- Dynamic INT8 quantization of BERT's nn.Linear layers (weights stored INT8, activations quantized on the fly) is the classic CPU speed-up; embeddings and LayerNorm stay in float.
- Unstructured (individual weight) pruning gives sparse matrices that dense GPU kernels do not speed up; structured pruning (heads, neurons, layers) shrinks the dense shapes and gives real speed-ups.
- Michel et al. (2019): many BERT attention heads can be removed at test time with little loss.
- DistilBERT: 6-layer student of 12-layer BERT-base, initialised from every other teacher layer, token-type embeddings and pooler removed, trained during pre-training with a triple loss (soft-target distillation with temperature + MLM + cosine embedding loss); ~66M vs ~110M parameters, 40% smaller, 60% faster, 97% of BERT's GLUE score.
- Soft targets: softmax(z / T) with T > 1 exposes the teacher's "dark knowledge" (relative probabilities of wrong classes).
- TinyBERT distils embeddings, hidden states and attention matrices layer by layer, in two stages: general (pre-training) distillation then task-specific distillation with data augmentation.
- Low-rank factorisation: W (m×n) ≈ A (m×r) B (r×n), parameters m·n -> r(m+n); worthwhile only when r < mn/(m+n).
- ALBERT: factorised embedding (V×E + E×H instead of V×H) plus cross-layer parameter sharing (one transformer block reused at every depth) and sentence-order prediction (SOP) instead of NSP. ALBERT-base ~12M parameters vs BERT-base ~108M, but sharing does not cut compute or latency: every layer still runs.
- MobileBERT: as deep as BERT-large (24 layers) but thin, with bottleneck / inverted-bottleneck blocks, ~25M parameters, distilled layer by layer from an inverted-bottleneck BERT-large teacher (IB-BERT); task-agnostic.
- MoE routes each token to a few experts: Mixtral 8x7B has 46.7B total parameters but ~12.9B active per token (2 of 8 experts), ~28%. Memory follows total parameters; per-token compute follows active.
- Sparse attention (Longformer sliding window + global tokens, BigBird) and linear approximations (Performer, Linformer) replace O(n²) attention; efficient tokenization shortens sequences, which directly lowers attention compute.
- Serving wins named in the course: KV-cache management, continuous batching, speculative decoding, post-training INT8/INT4 quantization at serving time; vLLM (PagedAttention, up to ~24x throughput vs naive HF), llama.cpp (GGUF, 4-bit 7B ≈ 3.9 GB on a laptop).
- Course latency example: L = prefill + output_tokens × decode_time; X = batch_capacity ÷ L; G = ceil(peak_demand ÷ X). Halving decode time nearly doubles X.
- Five deployment pillars on the slide: batching & caching, hardware acceleration, model serving frameworks (TensorRT, ONNX Runtime, Triton), edge/on-device, autoscaling.

## Common traps (each one must have at least one question)
- Rounding a GPU count down (2.75 -> 2) -> the model does not fit; always round up.
- "ALBERT is 9x smaller so it is 9x faster" -> parameter sharing cuts memory, not FLOPs; ALBERT-xxlarge is slower than BERT-large.
- Unstructured 50% sparsity expected to halve GPU latency -> dense kernels still multiply the zeros.
- Training cost assumed proportional to parameters only -> it is 6 × params × tokens; tokens count too.
- Forgetting MFU (using peak FLOP/s) -> underestimates GPU-hours.
- MoE memory sized by active parameters -> all experts must be loaded; memory follows total.
- Quantization assumed to shrink the KV cache or activations automatically -> weight-only quantization shrinks weights only.
- Distillation with T = 1 and hard labels only -> loses the dark knowledge that makes distillation work.
- DistilBERT believed to be fine-tuned from BERT on the task only -> it is distilled during pre-training (task-agnostic), then fine-tuned.
- Low-rank with large r -> r(m+n) can exceed m·n and save nothing.
- Padding every batch to 512 tokens -> wasted compute; dynamic padding / bucketing fixes it.
- Larger batch assumed to cut per-request latency -> it raises throughput, often at a latency cost.
- Deduplication treated as only a quality step -> it also cuts compute linearly.

## Interview angle
1. **"Your BERT classifier is too slow on CPU. What do you do?"** Distil to DistilBERT or TinyBERT, dynamically quantize Linear layers to INT8, export to ONNX Runtime, use dynamic padding and batching; measure accuracy after each step.
2. **"ALBERT has 12M parameters. Why is it not faster than BERT-base?"** Cross-layer sharing reuses one block's weights at all 12 depths; each layer still runs, so FLOPs and latency are similar. It saves memory and download size.
3. **"Pruning vs distillation vs quantization?"** Pruning removes weights/heads; distillation trains a smaller student; quantization lowers precision. They are complementary: distil, prune heads, then quantize.
4. **"How many GPUs for 50 req/s?"** L = prefill + tokens × decode; X = batch ÷ L; G = ceil(50 ÷ X). Halving decode time roughly halves the fleet.
5. **"What does an MoE save?"** Per-token compute (only active experts run), not memory (all experts are stored).

## Source material
- Handout (`nlp-src/handout.txt`), session 15: Scalable & Efficient NLP Systems: Need for Efficiency & Scalable Data; Model Compression & Efficient Architectures; Inference Optimisation & Deployment.
- Session 15 deck (`nlp-applications-slides.txt` ~lines 7120-7500; identical copy in `old-batch-slides.txt` ~6856+): cost of scale ($4.6M, 1,287 MWh, 500x parameter growth BERT -> PaLM); "efficiency is a product requirement" (400 ms latency, serving vs training cost, Strubell CO2, access & equity via DistilBERT/TinyBERT).
- Same deck: scalable data is about quality (dedup Lee et al. 2022, quality filtering CCNet/Gopher, streaming WebDataset/MosaicML, curriculum and mixing); RedPajama reproduction of LLaMA's 1.2T-token recipe (CommonCrawl 67%, C4 15%, GitHub/Wikipedia/Books/arXiv ~4.5% each).
- Same deck: "Three core ways to shrink a model" table (quantization 2-4x smaller; pruning 30-60% fewer parameters; distillation 40-60% smaller, 95%+ quality; techniques stack).
- Same deck: DistilBERT slide (6-layer student of 12-layer BERT-base trained during pre-training; 40% smaller, 60% faster, 97% GLUE); LLM.int8() slide (outliers in FP16, BLOOM-176B 352 -> 180 GB, "49% memory reduction"; bitsandbytes).
- Same deck: "Designing models to be efficient by default" (MoE / Switch Transformer 1.6T; sparse and linear attention: Longformer, Performer, RWKV; ALBERT parameter sharing; efficient tokenization); Mixtral 8x7B (46.7B total, 12.9B active, ~28%).
- Same deck: serving wins (KV-cache, continuous batching, speculative decoding, PTQ with GPTQ/AWQ); vLLM PagedAttention (~24x vs HF); llama.cpp GGUF (7B: FP16 ~13.5 GB, INT8 ~7.2 GB, Q4 ~3.9 GB); five deployment pillars (batching & caching, hardware acceleration, serving frameworks TensorRT/ONNX Runtime/Triton, edge, autoscaling).
- Same deck: three worked examples: training cost (175B, 300B tokens, 312 TFLOP/s, 40% MFU, $2/hr -> 3.15e23 FLOPs, ~700k GPU-hr, ~$1.4M); quantization memory (70B: FP16 140 GB = 2 GPUs, INT4 35 GB = 1 GPU); production inference (L = 200 + 256 × 20 = 5,320 ms; X = 32 / 5.32 = 6.0 req/s; G = 40 / 6.0 -> 7 GPUs; halving decode -> ~4 GPUs).
- **Gap flagged:** the slides only name the techniques. Pruning details (magnitude, structured vs unstructured, Michel et al. 2019 head pruning, Frankle & Carbin 2019 lottery ticket, movement pruning), DistilBERT internals (triple loss, initialisation; Sanh et al. 2019), TinyBERT (Jiao et al. 2020), MobileBERT (Sun et al. 2020), ALBERT internals (factorised embedding, SOP; Lan et al. 2019), low-rank factorisation, dynamic INT8 quantization of BERT and ONNX/TensorRT export come from the papers and standard textbook material, not the slides.
- **Course slip noted:** the LLM.int8() slide says "49% memory reduction" for 352 -> 180 GB; that is (352 - 180) / 352 ≈ 48.9%, so the label is right, but INT8 alone would be 50% (176 GB); the extra ~4 GB is the FP16 outlier columns and overhead.
- Exam patterns: Sep 2026 Regular (Set 1/2) and 2026 Makeup end-sem Q5. (1) Training: C = 6 × params × tokens; effective throughput = peak × MFU; H = C ÷ throughput ÷ 3600; cost = H × rate; dedup cuts tokens by x% -> cost falls by x%; GPUs in parallel for a deadline = H ÷ (days × 24); budget yes/no. (2) Serving: L = prefill + tokens × decode (ms and s); X = batch ÷ L; G = ceil(demand ÷ X); speculative decoding halves decode -> recompute G and % fleet reduction. (3) Memory: params × 2 / 1 / 0.5 bytes and ceil(÷ GPU memory) GPUs per precision. GPU counts are always rounded up.
