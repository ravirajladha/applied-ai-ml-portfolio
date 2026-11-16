# LLM Foundations (M1): coverage spec

**Ladder:** LLMs for Generative AI (AIMLCZG536) › llm4genai   ·   **Prerequisites:** basic probability (conditional probability, softmax), vectors and dot products; nlp-tokens and nlp-embeddings help but are not required
**Why it matters for AI/ML:** Module 1 is the vocabulary of the whole course: what an LLM is (a next-token probability model), how text becomes token IDs (BPE, byte-level BPE) and vectors (the |V| x d embedding table), how order is injected (sinusoidal, learned, RoPE) and which Transformer family fits which task. Mid-sem questions on architecture choice, BPE by hand and embedding/LM-head shapes come straight from here, and every later module (inference cost, KV cache, RAG) is counted in tokens.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `lm-basics` | Language models as next-token probability | what an LM assigns probabilities to, autoregression | chain rule by hand, softmax over the vocabulary, sampling makes it generative | why order matters, "Large" = params + data + context, n-gram → Transformer (parallelism) | log-space scoring, comparing sentence probabilities of different lengths |
| 2 | `pipeline` | The LLM pipeline and LM head | tokenizer → embeddings → blocks → head | attention = talk, FFN = think, residual adds; corpus = pre-processed documents | LM head = unembedding + softmax, which position's logits are used in training vs inference | head shapes, weight tying saving |V|·d |
| 3 | `token-types` | Word, subword, character and byte tokens | what a token is, OOV / [UNK] | four token types on one word, byte counts in UTF-8 | sequence length vs vocab size trade-off, Indic text costs | worst-case token counts, why vocabulary can't change after training |
| 4 | `bpe` | BPE: token learner and segmenter | merge the most frequent pair | the course hug/pug/pun/bun/hugs example, learner vs segmenter | pair counts recomputed after every merge, hyper-parameters (vocab size, min frequency), [UNK] for unseen chars | segmenter applies merges in learned order, vocab size arithmetic |
| 5 | `markers-libs` | Byte-level BPE, WordPiece, SentencePiece, libraries | — | `##` vs `Ġ` vs `▁`, byte-level BPE has no [UNK] | WordPiece likelihood score vs BPE frequency, SentencePiece needs no pre-tokenizer, tiktoken only counts | GPT-2 vocab 50,257 arithmetic, using the wrong tokenizer |
| 6 | `embeddings` | Token embeddings and the |V| x d table | embedding = dense learned vector | one-hot × E picks a row, X is n × d | parameter counts (Llama 3 8B ≈ 525M), learned with the model not the tokenizer | input table + LM head counts, tying |
| 7 | `similarity` | Static vs contextual embeddings, cosine | cosine range | static (word2vec) vs contextual (hidden states), "bank" | cosine ignores length, semantic similarity for RAG | decoder vs encoder embeddings, the input table is static |
| 8 | `positional` | Positional encoding: sinusoidal, learned, RoPE | why attention needs position | three methods and who uses them | sinusoidal value by hand, RoPE rotates Q/K and gives relative position | RoPE dot product depends only on the offset; extrapolation limits |
| 9 | `context-window` | Context window | max tokens per call | prompt + output share the window | grows during generation, sizes across models | budget arithmetic across a call |
| 10 | `families-tasks` | Encoder vs decoder families, NLU vs NLG | NLU vs NLG | encoder-only / decoder-only / encoder-decoder with examples | exam scenarios (classification, NER, translation, code, fiction), bidirectional vs causal | trade-offs: generation, classification cost, two stacks |

## Must-know facts
- A language model assigns probabilities to token sequences: P(w1..wn) = Π P(wi | w1..wi-1) (chain rule). Predicting the next token well = scoring any sentence.
- The next-token step is softmax classification where the classes are the vocabulary tokens. Sampling from it makes the model generative; generation is autoregressive, one token (one full forward pass) at a time.
- "Large" means three things: parameters (billions), training data (trillions of tokens), context window.
- Transformers beat RNNs mainly through parallelisation: self-attention processes all tokens of a sequence at once.
- Pipeline: tokenizer → token embeddings + positional information → N Transformer blocks → LM head (unembedding + softmax).
- Attention = tokens talk to each other; FFN = each token thinks on its own; the residual stream adds, never replaces.
- Token types: word (OOV, bloated vocab), subword (modern default), character (long sequences), byte (vocab 256, never OOV, longest sequences).
- A tokenizer has a token learner (runs once, builds vocab + ordered merge rules) and a token segmenter (applies the merges to every input). The tokenizer is trained before the model; always use the model's own tokenizer.
- BPE: start from characters, count adjacent pairs weighted by word frequency, merge the most frequent, recompute, repeat until the target vocab size. Hyper-parameters: vocab size, min frequency.
- Course example (hug 10, pug 5, pun 12, bun 4, hugs 5): merges ug (20), un (16), hug (15); `mug` → [UNK] with a character base; fix = byte-level BPE (256 base bytes).
- Markers: WordPiece `##` (continuation, BERT); byte-level BPE `Ġ` (leading space, GPT/Llama/Qwen); SentencePiece `▁` (space, no pre-tokenizer; T5, Gemma, Llama 1/2).
- WordPiece merges by a likelihood score (pair frequency relative to its parts), BPE by raw frequency.
- Embedding table E is |V| × d, learned with the model. one-hot × E = one row. Llama 3 8B: 128,256 × 4096 ≈ 525M parameters; the LM head (d × |V|) is the same size unless tied (Eᵀ).
- Training computes logits at all n positions in parallel; inference uses only the last position's logits.
- Static embeddings (word2vec, GloVe, the LLM input table) give one vector per token; contextual embeddings (hidden states) change with the sentence.
- Cosine similarity = a·b / (|a||b|), range −1 to 1, ignores length.
- Position: sinusoidal (fixed, added; original Transformer), learned (trainable table, added; GPT-2, BERT), RoPE (rotates Q and K in every attention layer, relative position; Llama, Qwen, DeepSeek).
- Context window = max tokens per call and includes the generated output (prompt + answer).
- Encoder-only (BERT; bidirectional; MLM; classification/NER/embeddings), decoder-only (GPT, Llama; causal mask; CLM; generation), encoder-decoder (T5, BART; cross-attention; translation/summarisation).
- NLU extracts meaning (labels, entities); NLG produces text. LLMs do NLU by generating the label word.

## Common traps (each one must have at least one question)
- "The token ID carries meaning / can be used as the position" -> it is just a row index; position must be added or rotated in.
- "Embeddings are produced when the tokenizer is trained" -> BPE gives only vocab + IDs; embeddings are learned with the model.
- "After merging ug, pu (17) should be next" -> pair counts are recomputed; pu drops to 12 because pug is now p+ug.
- Pair order ignored -> (u, g) and (g, u) are different pairs.
- Segmenting by longest match instead of applying merges in learned order.
- "Byte-level BPE never produces long sequences" -> unseen words just cost more tokens.
- "A bigger vocabulary is free" -> it grows both the embedding table and the LM head.
- Forgetting the LM head when counting vocabulary parameters (or counting it twice with tied weights).
- "The context window is for the prompt only" -> the generated output counts too.
- "RoPE is added to the input embeddings" -> it rotates Q and K inside attention.
- "Sinusoidal encodings are learned" -> fixed, no parameters.
- "Decoder-only models give the best sentence embeddings" -> the causal mask means encoder-only embeddings are richer.
- Choosing a decoder-only model for every task -> encoder-only is cheaper and strong for classification/NER.
- "word embedding" in an LLM -> the course stresses it is a token embedding.
- tiktoken used to train a tokenizer -> it only counts/encodes.
- Cosine treated as length-sensitive -> [1,2] and [2,4] have cosine 1.

## Interview angle
1. **"What is an LLM, in one sentence?"** A decoder-only Transformer trained self-supervised to give a probability distribution over the next token; by the chain rule that is the same as scoring whole sequences, and sampling from it repeatedly generates text.
2. **"Walk me through BPE."** Pre-tokenize, start from characters (or 256 bytes), count adjacent pairs weighted by word frequency, merge the top pair, recompute counts, repeat to the target vocab. The learner runs once and saves ordered merges; the segmenter replays them on new text. Byte-level BPE removes [UNK].
3. **"Why does a 128K vocabulary cost about a billion parameters in an 8B model?"** E is |V| × d = 128,256 × 4096 ≈ 525M, and the LM head is d × |V|, another 525M unless tied.
4. **"How does a Transformer know word order?"** It doesn't by itself; we add sinusoidal or learned position vectors, or (modern) rotate Q and K with RoPE so attention scores depend on relative distance.
5. **"Classifier for 12 ticket categories: which architecture?"** Encoder-only (BERT/RoBERTa): bidirectional context, cheap, strong at classification; a decoder LLM works via the prompt but costs more per call.

## Source material
- **LM definition (Session-01 §2, CS-1 slides 5-8):** P(W) = P(w1..wn) and P(wn | w1..wn-1), linked by the chain rule; worked number P(I am teaching) = 0.1 × 0.4 × 0.05 = 0.002. Evolution n-gram → neural LM → RNN/LSTM → Transformer → hybrids (Mamba); Transformers won by parallelisation.
- **"Large" (Session-01 §3):** parameters (Llama 3 8B-405B, DeepSeek-V3 671B / 37B active), data (Llama 3 ~15T, Qwen3 ~36T tokens), context window (2K GPT-3 → 128K+).
- **Generative AI (Session-01 §4-5):** every NLP task as conditional next-word prediction; softmax over vocabulary classes; sampling makes it generative; output one token at a time (flagged for exam).
- **Building blocks (Session-01 §6, CS-1 slide 13):** tokenizer → embeddings + position → blocks → LM head; attention = talk, FFN = think, residual adds; corpus = documents after pre-processing.
- **Tokenization (Session-00 §1, Session-01 §7-9, CS-1, NLP primer deck):** word/subword/char/byte with "unhappiness!"; byte examples "Apple" = 5 bytes, "क" = 3 bytes; token learner vs token segmenter; BPE (Sennrich 2016), Unigram (Kudo 2018), WordPiece (Schuster & Nakajima 2012); markers `##`, `Ġ`, `▁`; library table (HF tokenizers / transformers / tiktoken count-only).
- **BPE worked example (Session-01 §8, flagged "exam favourite"):** (hug 10, pug 5, pun 12, bun 4, hugs 5) → ug (20), un (16), hug (15); segmenter bug → b ug, hugs → hug s, mug → [UNK]; hyper-parameters vocab size and min frequency.
- **Old-batch slides (lines 440-500):** GPT-2 byte-level BPE vocab 50,257 = 256 bytes + 50,000 merges + 1 end-of-text; WordPiece scores pairs by likelihood, not raw frequency; byte-level example "The sun is" with space glued to the word.
- **Embeddings (Session-00 §2, Session-01 §10):** one-hot × E selects a row; E = |V| × d; "fox jumps over dog" → IDs [2, 3, 5, 1] → X is 4 × 3; Llama 3 8B 128,256 × 4096 ≈ 525M; embeddings learned with the model ("corpus is never trained, model is trained"); "there is nothing called word embedding" in an LLM.
- **Similarity (Session-00 §3):** cosine = a·b/(|a||b|), [1,2] vs [2,4] = 1.0; static vs contextual ("bank"); input table static, hidden states contextual; encoder-only embeddings richer than decoder ones.
- **Positional encoding (Session-01 §11, old-batch lines 205-225 and 1250-1290):** sinusoidal PE(pos,2i) = sin(pos/10000^(2i/d)), PE(pos,2i+1) = cos(...), sample "pos = 2, d = 4" → sin 2 ≈ 0.91, cos 2 ≈ −0.42; learned (GPT-2, BERT); RoPE rotates Q/K (Llama, Qwen, DeepSeek); sinusoidal has no parameters, unseen positions beyond training length.
- **LM head and context (Session-01 §12, old-batch Question 1):** u = h · Eᵀ, [1 × d] × [d × |V|]; weight tying saves |V| × d (205M for |V| = 50,000, d = 4,096); inference uses the last position because of the causal mask; context window includes generated output.
- **Families (Session-00 §5-6, Session-01 §13):** encoder-only / decoder-only / encoder-decoder table (attention, objective, strengths, weaknesses); NLU vs NLG task table.
- **Exam patterns:** the June-2026 mid-sem (both sets) opens with "choose encoder-only / decoder-only / encoder-decoder for each scenario and name a model" (ticket sentiment, fiction, manual translation, biomedical/contract NER, IDE code completion) plus "explain MLM vs CLM / bidirectional vs causal in 2-3 points"; the old-batch practice set asks for E and Eᵀ shapes, one-hot × E, logits u = h·Eᵀ, weight-tying savings and "which position's logits at inference"; the professor promised a full BPE-by-hand question (show pair counts, state min-frequency rules). Bank questions reuse these shapes with new scenarios and numbers.
