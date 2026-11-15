# Tokens & Tokenization: coverage spec

**Ladder:** L3 · Text → LLMs › Text Representation   ·   **Prerequisites:** py-strings, py-collections, np-arrays (indexing)
**Why it matters for AI/ML:** Every LLM call is priced, limited and processed in tokens. The tokenizer decides what the model can "see" (letters, numbers, spaces), how much text fits in the context window, and is the source of a whole class of silent bugs (wrong tokenizer, bad padding, chat-template mismatch).

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `preprocessing` | Classic text preprocessing | lowercase + split, what stopwords are, what stemming does | stemming vs lemmatisation, stopword removal flipping 'not good', why LLMs skip it | when classic cleanup still helps (TF-IDF search), stopwords are task-dependent | — |
| 2 | `granularity` | Word vs character vs sub-word tokens | character split, word vocab and `<unk>`, vocab size vs sequence length | why sub-word wins, tokenizer = lexer | sequence length vs attention cost for char-level | — |
| 3 | `bpe` | BPE: the merge algorithm | merge the most frequent pair, the name | one merge by hand, pair counts weighted by word frequency, vocab = base + merges | applying ordered merges to new text, non-overlapping merges, domain shift, tokenizer is trained separately | merge rank order decides the split, why pre-tokenisation stops merges crossing words |
| 4 | `wordpiece-unigram` | WordPiece, SentencePiece and Unigram | the `##` prefix | SentencePiece `▁` and lossless decoding | WordPiece greedy longest-match, WordPiece pair score, Unigram pruning and best segmentation, SentencePiece is BPE or Unigram | whole-word `[UNK]` in WordPiece, subword regularisation |
| 5 | `byte-level` | Byte-level BPE and Unicode | characters vs UTF-8 bytes | 256 base bytes, no `<unk>` | bytes per script, GPT-2's `Ġ` | a token can end mid-character (streaming decode) |
| 6 | `vocab-size` | Vocabulary size trade-offs | bigger vocab = shorter sequences | typical sizes (30k-256k) | embedding memory, costs of a big vocab | why vocabularies grew, embedding rows padded beyond `len(tokenizer)` |
| 7 | `special-tokens` | Special tokens | EOS, [CLS], [PAD] | counting special tokens in the length, segment IDs | special-token injection, pad = eos workaround | masking labels by pad id also masks EOS |
| 8 | `ids-embedding` | Token IDs and the embedding lookup | model receives IDs, lookup = row indexing | (batch, seq) -> (batch, seq, d), IDs carry no meaning | one-hot @ E = lookup, out-of-range ID, embedding param count | weight tying, new tokens' embeddings are untrained |
| 9 | `padding-masks` | Padding, truncation and attention masks | why pad, mask 1 = real | build padded ids + mask, truncation leaves room for special tokens | left padding for decoder generation, dynamic padding / bucketing | mean pooling without the mask |
| 10 | `cost-quirks` | Tokens vs words: cost, limits and quirks | words -> tokens rule of thumb, context counts input + output | cost calculation, letter counting, leading spaces, non-English costs more | number chunking, pre-tokenisation regex, digit splitting | glitch tokens, trailing-space prompts |
| 11 | `templates-mismatch` | Chat templates and tokenizer-model mismatch | what a chat template is | build a ChatML string, generation prompt, missing template, templates differ per family | double BOS, train/serve template skew, wrong tokenizer for the weights | label masking on non-assistant turns, stop-token mismatch, cross-model token counting |

## Must-know facts
- A token is a chunk of text from a fixed vocabulary; the model only ever sees integer token IDs.
- Rule of thumb for English: 1 token ≈ 0.75 words (≈ 4 characters). Other languages and code differ.
- Context windows and API prices are counted in tokens, and the window holds prompt + reply.
- BPE: start from characters (or bytes), repeatedly merge the most frequent adjacent pair; vocab size = base symbols + number of merges.
- Encoding new text replays the learned merges in rank order; order changes the result.
- The tokenizer is trained separately, before the model, by counting; it is frozen afterwards.
- WordPiece (BERT): `##` marks continuation pieces, greedy longest-match encoding, merge score freq(ab)/(freq(a)·freq(b)).
- SentencePiece treats spaces as the symbol `▁` and can train BPE or Unigram; Unigram prunes a big vocabulary by likelihood.
- Byte-level BPE (GPT-2 onward) starts from 256 bytes, so there is no unknown token; `Ġ` is GPT-2's space marker.
- Typical vocab sizes: BERT 30,522; GPT-2 50,257; Llama 3 ≈128k. Bigger vocab = shorter sequences but bigger embedding/softmax.
- The embedding layer is a lookup table (vocab × d_model); lookup = one-hot × matrix = row indexing.
- Special tokens: BOS/EOS (start/end), PAD (filler), UNK (unknown), CLS/SEP (BERT classification/separator), MASK.
- Attention mask: 1 = real token, 0 = padding. Decoder-only batch generation needs left padding.
- Leading spaces are part of tokens (' hello' ≠ 'hello'); numbers split oddly; letters are hidden inside tokens.
- Chat models expect their own chat template; always use the tokenizer from the same checkpoint as the model.

## Common traps (each one must have at least one question)
- Removing stopwords "because they mean nothing" -> 'not good' becomes 'good', sentiment flips.
- Thinking stemming returns real words -> 'studies' becomes 'studi' / 'stud'.
- Thinking unknown words become `<unk>` in GPT-style tokenizers -> byte-level BPE never produces an unknown token.
- Thinking 'low' must become one token because it "looks like a word" -> only learned merges apply, in rank order.
- Thinking merges overlap -> 'aaa' with merge (a, a) gives ['aa', 'a'].
- Thinking the tokenizer is learned with the model by backprop -> it is trained separately and frozen.
- Thinking a bigger vocabulary makes sequences longer -> it makes them shorter; the cost is memory and rare tokens.
- Thinking token IDs carry meaning (500 is close to 501) -> IDs are arbitrary row numbers.
- Adding tokens without resizing embeddings -> IndexError / device-side assert.
- Assuming `len(tokenizer)` must equal the embedding row count -> rows are often padded to a multiple of 64.
- Setting pad = eos and masking labels by token id -> the real EOS is never learned, the model never stops.
- Right padding for decoder-only batch generation -> the model continues after pad tokens.
- Mean pooling without the attention mask -> embeddings depend on how much padding the batch had.
- Forgetting special tokens count towards max length -> truncation must leave room for [CLS]/[SEP].
- Counting len(str) as bytes -> 'é' is 1 character but 2 UTF-8 bytes.
- Decoding a byte-level token alone in streaming output -> a split character shows as U+FFFD.
- Assuming the same text costs the same tokens in every language -> non-English often costs much more.
- Ending a prompt with a trailing space -> unusual token split, worse output.
- Double BOS from template + add_special_tokens -> silent quality drop.
- Using another model's tokenizer with the same vocab size -> no crash, garbage output.
- Training on the whole templated chat as labels -> the model learns to write user turns.
- Stop token not matching the template's turn-end token -> generation never stops.
- Using one model's tokenizer to estimate another provider's cost -> counts differ.

## Interview angle
- **"Explain BPE."** Start from characters (or bytes). Count adjacent pairs across the corpus weighted by word frequency, merge the most frequent pair into a new token, repeat until the vocabulary hits the target size. To encode new text, split it into characters and replay the merges in learned order. It is like a compression dictionary built from the data. SDE analogy: a lexer whose token set was learned from logs.
- **"Why sub-words and not words or characters?"** Words give unbounded vocabularies and unknown words; characters give tiny vocabularies but very long sequences, and attention cost grows quadratically. Sub-words keep frequent words whole and split rare ones into known pieces, so nothing is out of vocabulary.
- **"Why can't an LLM count the r's in 'strawberry'?"** It sees 2-3 sub-word tokens, not letters. Spelling is only known if memorised per token. Fix: ask it to spell first, or use a tool.
- **"What vocabulary size would you choose?"** Trade-off: bigger means shorter sequences (cheaper, more context) but a bigger embedding/softmax and more under-trained rare tokens. Modern LLMs use about 32k-256k; multilingual and code-heavy models go larger.
- **"Name a tokenizer bug you have seen."** Wrong tokenizer for the checkpoint (silent garbage), pad = eos masking the real EOS, right padding in batch generation, double BOS from the chat template, or stop tokens not matching the template.

## Source material
To be added.
