# Attention & Transformers: coverage spec

**Ladder:** L3 · Text → LLMs › Transformers   ·   **Prerequisites:** nlp-tokens, nlp-embeddings, dl-neuron, dl-training (matrix multiply, softmax)
**Why it matters for AI/ML:** Every modern LLM (GPT, Llama, BERT, T5) is a stack of transformer blocks. Attention is the one operation that decides how tokens share information, and its O(n²) cost and KV cache drive context-window limits, serving cost and latency. AI-engineer interviews almost always ask you to explain it.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `why-attention` | Why RNNs struggled, the attention idea | RNNs read one token at a time; attention looks at all tokens at once | Vanishing gradients and the fixed-size bottleneck in seq2seq | Path length O(1) vs O(n) between tokens; parallel training | Trade-off: RNN O(1) state per step vs attention's growing cache |
| 2 | `qkv` | Query, Key, Value | What Q, K, V mean (search analogy) | Q, K, V are three learned linear projections of the same input | Why separate K and V projections (match vs content) | Attention as a differentiable soft dictionary lookup / kernel smoother |
| 3 | `sdpa` | Scaled dot-product attention | Formula softmax(QKᵀ/√d_k)V, softmax makes weights sum to 1 | Compute scores and weights for tiny matrices | Why divide by √d_k (dot-product variance grows with d_k, softmax saturates) | Numerical stability, saturated softmax gradients, temperature view |
| 4 | `shapes-masks` | Shapes and causal masking | Attention matrix is seq × seq | Output shape (batch, seq, d_v); building a mask with triu | Mask with -inf before softmax, not 0 after; diagonal=1 | Padding masks + causal masks combined; fully masked rows give NaN |
| 5 | `self-cross` | Self vs cross attention | Self-attention: a sequence attends to itself | Cross-attention: Q from decoder, K/V from encoder | Shapes when query and key lengths differ (n_q × n_k) | Where cross-attention appears (T5, Whisper, multimodal) |
| 6 | `multi-head` | Multi-head attention | Several heads look for different patterns | head_dim = d_model / n_heads; concat + output projection | Reshape/transpose shapes; params same as one big head | Why heads help (subspaces), head pruning, divisibility constraint |
| 7 | `positions` | Positional encodings | Attention has no built-in word order | Sinusoidal vs learned, added to embeddings | Permutation equivariance without positions; extrapolation limits | RoPE rotates Q and K so scores depend on relative offset |
| 8 | `block` | The transformer block | Attention + feed-forward + residual + layer norm | Residual = skip connection; FFN expands to 4·d_model | LayerNorm vs BatchNorm; pre-norm vs post-norm | Why pre-norm trains deeper stacks stably; residual stream view |
| 9 | `architectures` | Encoder-only, decoder-only, encoder-decoder | BERT, GPT, T5 and what each is for | Masked LM vs causal LM vs span corruption | Choosing the architecture for a task | Why decoder-only won for general LLMs |
| 10 | `params-cost` | Parameter counting and O(n²) cost | Bigger sequence = more work | ~12·d² parameters per block | Attention compute/memory grows with n², FFN with n | Where FLOPs go at long vs short contexts; 6·N·D rule |
| 11 | `efficiency` | KV cache, FlashAttention, MQA/GQA | — | KV cache stores past keys and values | Cache size formula; why queries aren't cached | FlashAttention (exact, tiled, IO-aware), MQA/GQA trade-offs, sliding window |

## Must-know facts
- Attention(Q, K, V) = softmax(QKᵀ / √d_k) V.
- Q, K, V are produced by three learned weight matrices applied to the token vectors.
- The attention weight matrix has shape (n_queries, n_keys): for self-attention that is seq × seq, independent of d_model.
- Softmax is applied over the key axis (the last axis), so each row of weights sums to 1.
- Dividing by √d_k keeps the score variance near 1; without it softmax saturates and gradients vanish.
- Causal masking sets future scores to -inf before softmax; with `triu(..., diagonal=1)` the diagonal (self) stays visible.
- Cross-attention: queries come from the decoder, keys and values from the encoder output.
- Multi-head: head_dim = d_model / n_heads; heads run in parallel, are concatenated, then mixed by W_O.
- Multi-head attention has the same parameter count (4·d²) as single-head attention of the same d_model.
- Without positional information, self-attention is permutation-equivariant: shuffle the input, the output shuffles the same way.
- Original transformer adds sinusoidal encodings to embeddings; GPT-2/BERT learn them; Llama-class models use RoPE on Q and K.
- A block = attention sublayer + FFN sublayer, each wrapped in a residual connection and LayerNorm.
- FFN (d → 4d → d) holds about 2/3 of a block's parameters; a block is ~12·d² parameters.
- BERT = encoder-only (bidirectional, understanding); GPT = decoder-only (causal, generation); T5 = encoder-decoder (text-to-text).
- Attention cost is O(n²·d) compute and O(n²) memory for the score matrix.
- The KV cache stores each layer's past K and V so a new token only computes its own Q, K, V.
- KV cache size = 2 × layers × kv_heads × head_dim × seq_len × bytes per value (per sequence).
- FlashAttention is exact attention computed in tiles to avoid writing the n×n matrix to GPU memory.
- MQA shares one K/V head across all query heads; GQA shares one K/V head per group; both shrink the KV cache.

## Common traps (each one must have at least one question)
- Dividing by d_k instead of √d_k -> scores are over-shrunk; the paper uses the square root to normalise variance.
- Thinking the attention matrix is d_model × d_model -> it is seq × seq (n_q × n_k).
- Softmax over the wrong axis -> columns sum to 1 instead of rows; each query must get a distribution over keys.
- `triu` with diagonal=0 as the mask -> hides the token from itself; use diagonal=1 for the masked positions.
- Masking by multiplying weights by 0 after softmax -> rows no longer sum to 1; mask scores with -inf before softmax.
- Assuming more heads means more parameters -> heads split d_model; parameter count stays 4·d².
- Assuming attention knows word order -> it is order-blind without positional encodings.
- Thinking positional encodings are concatenated -> in the original transformer they are added.
- Using BERT to generate long text like GPT -> encoder-only models are trained for understanding, not left-to-right generation.
- Swapping cross-attention roles -> Q comes from the decoder; K and V from the encoder.
- Believing the KV cache stores queries too -> past queries are never needed again.
- Believing FlashAttention is an approximation -> it gives the same result; it just moves less memory.
- Thinking most parameters are in attention -> the FFN holds about twice as many as attention.
- Confusing LayerNorm with BatchNorm -> LayerNorm normalises each token across features, no batch statistics.
- Thinking GQA cuts attention FLOPs a lot -> its main win is a smaller KV cache and less memory bandwidth.
- n_heads that doesn't divide d_model -> the reshape fails; PyTorch raises an error.

## Interview angle
1. **Explain self-attention in a minute.** Each token makes a query, key and value. Score every query against every key with a dot product, scale by √d_k, softmax to get weights, take a weighted sum of values. It's a soft, learned key-value lookup that lets every token pull information from every other token in one step.
2. **Why divide by √d_k?** Dot products of random d_k-dim vectors have variance ~d_k. Large scores push softmax into a near one-hot region where gradients are tiny. Scaling keeps variance ~1.
3. **What is the KV cache and why does it matter?** During generation, past tokens' K and V never change, so we store them (memoisation) and only compute the new token's projections. It turns per-step work from re-processing the whole prefix into one token's worth, at the cost of memory that grows with layers × heads × sequence length; that memory is what limits batch size and context in serving.
4. **Why is attention O(n²) and how do people deal with it?** Every token scores every other token: an n×n matrix per head. FlashAttention removes the memory bottleneck (still O(n²) compute); sparse/sliding-window attention, GQA/MQA and KV-cache quantisation reduce cost in practice.
5. **BERT vs GPT vs T5?** BERT: encoder-only, bidirectional, for classification/embeddings. GPT: decoder-only, causal mask, for generation. T5: encoder-decoder, for input→output tasks like translation and summarisation.

SDE analogy: attention is a fuzzy JOIN where every row of Q is matched against every row of K and returns a weighted blend of V; the KV cache is memoisation of that table.

## Source material
To be added
