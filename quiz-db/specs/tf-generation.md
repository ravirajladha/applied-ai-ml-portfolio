# How LLMs Generate: coverage spec

**Ladder:** L3 · Text → LLMs › Transformers   ·   **Prerequisites:** nlp-tokens, tf-attention (softmax, KV cache)
**Why it matters for AI/ML:** Every LLM feature an AI engineer ships (chat, RAG, agents, structured output) sits on the generation loop. Knowing what temperature, top-p, max tokens and the context window really do, how tokens map to cost and latency, and why models hallucinate is what separates "called an API" from "engineered a reliable product".

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `autoregressive` | Next-token prediction and the loop | Predict one token, append, repeat | Logits -> softmax -> pick -> append; teacher forcing in training | Why generation is sequential even though training is parallel | Exposure bias; cost of each step without/with KV cache |
| 2 | `decoding` | Greedy and beam search | Greedy = always take the top token | argmax code; greedy isn't the best overall sequence | Beam search mechanics, length normalisation | Why beam search gives bland text for open-ended generation |
| 3 | `sampling` | Temperature, top-k, top-p, penalties | Temperature: low = focused, high = random | softmax(logits / T); top-k and top-p filtering | Ranking preserved by T; top-p adapts to the distribution; repetition/frequency/presence penalties | Order of operations in a sampler; min-p; penalty sign bugs |
| 4 | `stopping-context` | Stop sequences, max tokens, context window | The model stops at an end token or a limit | max_tokens caps the output; stop sequences; finish_reason | Prompt + output must fit the window; truncation strategies | Lost-in-the-middle; long-context cost |
| 5 | `tokens-cost` | Tokens and cost | Tokens are word pieces; you pay per token | Prompt vs completion tokens priced separately | Cost arithmetic; ~0.75 words per token in English | Prompt caching; why output tokens cost more |
| 6 | `training-pipeline` | Pre-training -> SFT -> RLHF/DPO; base vs chat | Base models complete text; chat models follow instructions | Pre-training, instruction tuning (SFT), preference tuning | RLHF (reward model + PPO) vs DPO; chat templates | Reward hacking, alignment tax, why RLHF doesn't add knowledge |
| 7 | `hallucination` | Hallucinations | Fluent but false output | Why: the model predicts plausible text, not checked facts | Mitigations: RAG, citations, "I don't know" instructions | Training incentives to guess; calibration after RLHF |
| 8 | `perplexity` | Perplexity | Lower perplexity = less surprised by real text | exp(average negative log-likelihood) | Compute it; uniform model has perplexity = vocab size | Not comparable across tokenizers; doesn't measure helpfulness |
| 9 | `latency` | Latency: TTFT, tokens/sec, prefill vs decode | Time to first token and streaming | Total time ≈ TTFT + tokens / speed | Prefill is compute-bound, decode is memory-bound; KV-cache memory | Batching, continuous batching, KV cache limits concurrency |
| 10 | `inference-opt` | Speculative decoding and quantisation | — | Quantisation stores weights in fewer bits | Memory arithmetic for fp16 / int8 / int4 | Speculative decoding is lossless; acceptance rate maths; quantisation quality trade-offs |
| 11 | `determinism` | Determinism and seeds | Same prompt can give different answers | Temperature 0 = greedy | Seeds make sampling repeatable on one setup | Why temperature 0 still isn't always deterministic (float non-associativity, batching, MoE routing) |
| 12 | `sampler-code` | Building a sampler in code | argmax of logits = argmax of probs | torch.multinomial | top-k renormalise; top-p boundary token; temperature widens the nucleus; sampler order (penalties -> T -> top-k -> top-p -> sample) | No renormalise -> ValueError in NumPy; T = 0 division gives NaN, special-case it |
| 13 | `structured-output` | Constrained decoding and structured output | Use structured-output modes + validate | JSON mode = syntax only; logit bias bans tokens | Masking disallowed logits to -inf; grammar/FSM constrained decoding; valid ≠ correct | Token/grammar boundary mismatch; schema field order (reasoning before answer) |

## Must-know facts
- An LLM outputs one logit per vocabulary token; softmax turns logits into probabilities for the next token.
- Generation is a loop: pick a token, append it to the input, run again, until a stop condition.
- Training uses teacher forcing: all positions are predicted in parallel from the true previous tokens.
- Greedy decoding = argmax every step; it's locally optimal, not the most probable full sequence.
- Temperature divides the logits: T < 1 sharpens, T > 1 flattens, T -> 0 approaches greedy. It never changes the ranking.
- Top-k keeps the k most likely tokens; top-p keeps the smallest set whose probabilities sum to at least p; both then renormalise.
- Repetition penalties lower the logits of tokens that already appeared.
- max_tokens caps completion length; prompt + completion must fit in the context window.
- Generation stops on an end-of-sequence token, a stop sequence, or max_tokens (finish_reason tells you which).
- APIs bill input (prompt) and output (completion) tokens separately; output is usually several times more expensive.
- English averages roughly 0.75 words (about 4 characters) per token.
- The pipeline: pre-training (next token on huge text) -> SFT (instruction/answer pairs) -> preference tuning (RLHF or DPO).
- Base models continue text; instruct/chat models are tuned to follow instructions in a chat template.
- Hallucinations come from predicting plausible continuations without a fact check; low temperature does not remove them.
- Perplexity = exp(mean negative log-likelihood per token); a uniform guess over V tokens has perplexity V.
- TTFT is dominated by prefill (prompt length); tokens/sec by decode, which is memory-bandwidth bound.
- KV-cache memory per token = 2 × layers × kv_heads × head_dim × bytes.
- Speculative decoding: a small draft model proposes tokens, the big model verifies them in one pass; with the right acceptance rule the output distribution is unchanged.
- Quantising weights (fp16 -> int8 -> int4) cuts memory 2x/4x and usually speeds up decoding, at some quality cost.
- Temperature 0 is not guaranteed deterministic: floating-point addition isn't associative, and batch composition changes kernel reduction order.
- Common sampler order: penalties -> temperature -> top-k -> top-p -> softmax -> sample; T = 0 is special-cased to argmax.
- Multiplicative repetition penalty divides positive logits and multiplies negative ones; frequency/presence penalties subtract count·fp and a flat pp.
- Beam search: width 1 = greedy; finished hypotheses go to a separate list; very wide beams can hurt quality (beam search curse); work in log-probs to avoid underflow.
- Constrained decoding masks invalid tokens to -inf each step from a grammar/FSM; it guarantees form, not correct values. Basic JSON mode guarantees only syntax.
- LM training shifts labels: logits[:, :-1] vs tokens[:, 1:]; pads must be excluded from loss and perplexity.
- Chat APIs are stateless: re-sending history makes input tokens grow quadratically with turns; prompt caching discounts only an identical prefix.
- Reasoning tokens are billed as output and count against max tokens.
- Speculative sampling accepts with min(1, p/q) (acceptance rate Σ min(p, q)) and resamples from norm(max(0, p − q)); draft must share the tokenizer; gains shrink at large batch.
- Continuous batching adds/removes sequences at every decode step.

## Common traps (each one must have at least one question)
- "Temperature 0 means identical output every time" -> usually, but GPU reduction order, batching and MoE routing can change it.
- "Higher temperature makes the model more accurate/creative-smarter" -> it only flattens the distribution; errors increase.
- "Temperature changes which token is most likely" -> the ranking stays the same; only the gaps change.
- "Greedy gives the best overall sentence" -> it can miss a higher-probability sequence that starts with a less likely token.
- "Beam search is best for chat" -> it tends to produce bland, repetitive text; sampling is used for open-ended generation.
- "top_p = 1.0 filters tokens" -> it keeps the full distribution (no filtering).
- "Top-k and top-p are the same thing" -> top-k keeps a fixed count, top-p a variable count based on cumulative probability.
- "max_tokens includes the prompt" -> in chat APIs it caps the completion; the prompt still uses up context.
- "The model remembers what fell out of the context window" -> anything not in the window is invisible.
- "Tokens = words" -> a word can be several tokens; numbers and non-English text often take more.
- "Input and output tokens cost the same" -> output tokens are usually priced higher.
- "A base model will follow my instructions" -> it continues text; it may just write more questions.
- "RLHF teaches the model new facts" -> it mainly shapes behaviour and preferences; knowledge comes from pre-training.
- "Low temperature cures hallucinations" -> a confidently wrong answer is still produced greedily.
- "Perplexity can compare any two models" -> only with the same tokenizer and test set.
- "Long answers mainly slow down time-to-first-token" -> TTFT depends on prompt length (prefill); output length affects total time.
- "Speculative decoding trades quality for speed" -> with proper verification it is exactly the big model's distribution.
- "Repetition penalty = divide the logit by the penalty" -> dividing a negative logit makes it more likely; negatives must be multiplied.
- "Stop sequences appear in the returned text" -> most APIs cut the text before the stop sequence.
- "Zero out filtered probs and sample" -> without renormalising, NumPy raises ValueError (PyTorch silently accepts).
- "Temperature 0 is just logits / 0" -> inf/nan; implementations switch to argmax.
- "Wider beam is always better" -> very wide beams give short/degenerate outputs.
- "Multiply probabilities to score a sequence" -> underflows to 0.0; sum log-probs.
- "JSON mode / schema constraints make the answer correct" -> they constrain form only.
- "Put the answer field first in the schema" -> the model commits before reasoning.
- "Strong repetition penalty is harmless" -> it punishes needed repeats (identifiers, quotes) in RAG/code.
- "Including pads in the perplexity mean is fine" -> it fakes a lower perplexity.
- "Speculative decoding speeds up any batch size" -> at high batch the GPU is compute-bound and gains vanish.
- "Hand-written 'User:/Assistant:' prompt is fine for a chat model" -> must match the chat template.
- "A stop string is detected per streamed chunk" -> it can span chunks; match on accumulated text.

## Interview angle
1. **Walk me through how an LLM generates a reply.** Tokenise the prompt, run a forward pass (prefill) to get logits for the next token, apply temperature/top-p, sample a token, append it, and repeat with the KV cache until an end token, stop sequence or max_tokens. Stream tokens as they're produced.
2. **Temperature vs top-p?** Temperature rescales the whole distribution (sharper or flatter). Top-p truncates the long tail to the smallest set covering probability p, then renormalises. Typically tune one, not both.
3. **Why do LLMs hallucinate and what do you do about it?** They are trained to produce plausible continuations, and evaluation/RLHF often rewards confident answers over "I don't know". Mitigate with retrieval (RAG), asking for citations, allowing abstention, constrained outputs, and evals that check groundedness.
4. **Explain TTFT vs tokens/sec and how to improve each.** TTFT = prefill of the whole prompt (compute-bound): shorten prompts, use prompt caching. Tokens/sec = decode (memory-bandwidth bound, one token at a time): quantisation, speculative decoding, GQA, smaller models, batching.
5. **Why isn't temperature 0 deterministic?** Floating-point sums give slightly different results in different orders; server-side batching changes the reduction order, so near-tied logits can flip and the outputs diverge from that token onward.

6. **How do you get reliable JSON out of an LLM?** Use schema-constrained decoding (logits of tokens that would break the grammar are masked to -inf each step), validate with a schema anyway, put reasoning fields before answer fields, and handle truncation by max_tokens.
7. **Why does speculative decoding not change the output distribution?** Accept a drafted token with min(1, p/q); on rejection resample from norm(max(0, p − q)). The combined distribution equals p exactly; the speed-up depends on acceptance rate (Σ min(p, q)) and on decode being memory-bound.

SDE analogy: the generation loop is a `while` loop calling a pure function `next_token(context)`; the KV cache is memoisation; the context window is a fixed-size buffer; max_tokens is a loop guard.

## Source material
To be added
