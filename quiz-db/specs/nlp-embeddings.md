# Embeddings & Similarity: coverage spec

**Ladder:** L3 · Text → LLMs › Text Representation   ·   **Prerequisites:** nlp-tokens, np-arrays (dot products, norms, broadcasting)
**Why it matters for AI/ML:** Embeddings turn text into vectors so "similar meaning" becomes "nearby points". They power semantic search, RAG retrieval, recommendation, clustering and deduplication. Most production RAG bugs are embedding bugs: wrong metric, missing normalisation, mixed models in one index, or bad pooling.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `one-hot-dense` | One-hot vs dense vectors | build a one-hot vector, why one-hot has no similarity, what a dense embedding is | one-hot dot products are 0 | distributed representations | — |
| 2 | `bow-tfidf` | Bag-of-words and TF-IDF | CountVectorizer shape, what IDF does | vocabulary order and dropped 1-char tokens, count matrix, word order lost, TF-IDF by hand, IDF = 0 for words in every doc | sklearn smoothed IDF, default L2 norm, unseen words ignored, stop_words='english' removes 'not', lexical vs semantic match | n-gram feature counts |
| 3 | `word2vec` | Distributional hypothesis and word2vec | distributional hypothesis, skip-gram vs CBOW | keep the weights, skip-gram pairs, CBOW averaging | negative sampling, unigram^0.75, CBOW vs skip-gram trade-off, antonyms are close | window size effect, two matrices and the sigmoid score |
| 4 | `glove-fasttext` | GloVe and fastText | fastText handles OOV, GloVe's name | character n-grams with boundary markers, GloVe co-occurrence | `<her>` vs inner 'her', morphologically rich languages, OOV vector from n-grams | — |
| 5 | `analogies` | Vector arithmetic and analogies | king - man + woman | do the arithmetic, set up the analogy expression | analogies are unreliable, why offsets are parallel | input words must be excluded or 'king' wins |
| 6 | `similarity` | Cosine, dot product and Euclidean distance | cosine by hand, cosine range, norm and unit vector | cosine_similarity matrix, normalise with norm | dot vs cosine ranking on raw vectors, equivalence after normalisation, row-wise normalisation with keepdims | ‖a−b‖² = 2 − 2cos, use the metric the model was trained with |
| 7 | `contextual` | Contextual embeddings | static 'bank' has one vector | why BERT is contextual, LLM text is not an embedding | last-token pooling for decoder models | anisotropy and mean-centring, which layer to use |
| 8 | `sentence` | Sentence embeddings, bi- vs cross-encoders | what a sentence embedding is | bi- vs cross-encoder, retrieve then re-rank, argsort top-k trap | masked mean pooling, raw [CLS] is poor, contrastive training | query/passage prefixes for asymmetric models |
| 9 | `dimensions` | Embedding dimension and Matryoshka embeddings | typical sizes | storage maths, dimension trade-off | Matryoshka idea, naive truncation of ordinary models | re-normalise after truncation, quantisation, distance concentration |
| 10 | `vector-search` | Semantic search and vector databases | what semantic search is, vector DB vs SQL index | brute-force top-k, ANN gives up recall | brute-force cost, HNSW idea, efSearch, brute force is fine at small scale | IVF nprobe, filtered search / post-filter trap |
| 11 | `drift-bias` | Embedding drift, mixing models and bias | can't compare vectors across models | re-embed on model upgrade, bias in analogies | rotation demo of mixed spaces, data drift | silent provider updates and version pinning, projection debiasing and its limits |

## Must-know facts
- One-hot vectors are as long as the vocabulary and all mutually orthogonal: no similarity information.
- Dense embeddings are short (hundreds to a few thousand floats) and learned so that similar items are close.
- Bag-of-words ignores word order; TF-IDF = term frequency × inverse document frequency.
- Textbook IDF = log(N / df) (0 for a word in every doc); scikit-learn's default IDF = ln((1+N)/(1+df)) + 1 and rows are L2-normalised.
- CountVectorizer lowercases, sorts its vocabulary alphabetically and drops 1-character tokens by default; unseen words at transform time are ignored.
- Distributional hypothesis: words in similar contexts have similar meanings (so antonyms end up close too).
- Skip-gram predicts context from the centre word; CBOW predicts the centre from the averaged context. Negative sampling replaces the full softmax with k binary decisions, sampling negatives from unigram^0.75.
- GloVe fits vectors to global log co-occurrence counts; fastText sums character n-gram vectors, so it handles OOV words.
- Analogy arithmetic (king − man + woman ≈ queen) works for some regular relations and needs the input words excluded.
- Cosine = dot of unit vectors; on unit vectors cosine, dot and Euclidean give the same ranking (‖a−b‖² = 2 − 2cos).
- Contextual models (BERT, LLMs) give a different vector for each occurrence of a word.
- Sentence embeddings: mean pooling must use the attention mask; good models are trained contrastively (sentence-transformers).
- Bi-encoders embed separately (indexable, fast); cross-encoders score pairs jointly (accurate, slow); retrieve then re-rank.
- Storage = N × d × bytes per number (1M × 768 × float32 ≈ 3.07 GB).
- Matryoshka embeddings can be truncated to a prefix and re-normalised; ordinary embeddings cannot.
- ANN indexes (HNSW, IVF) trade a little recall for big speed-ups; HNSW is a layered proximity graph searched greedily.
- Vectors from different models (or model versions) live in different spaces and must never be mixed in one index.
- Embeddings absorb social biases from their training text.

## Common traps (each one must have at least one question)
- Expecting 'I' or 'a' in the CountVectorizer vocabulary -> the default token_pattern drops 1-character tokens.
- Expecting vocabulary in first-seen order -> it is sorted alphabetically.
- Assuming bag-of-words keeps word order -> 'dog bites man' == 'man bites dog'.
- Comparing a hand-computed TF-IDF with sklearn -> sklearn smooths IDF (+1) and L2-normalises rows.
- Assuming a word in every doc gets IDF 0 in sklearn -> it gets 1.0.
- Using stop_words='english' for sentiment -> 'not' is removed.
- Expecting new words at transform time to be added -> they are silently ignored.
- Thinking high cosine means synonym -> antonyms like hot/cold are close too.
- Running analogy search without excluding the input words -> the answer is often 'king' itself.
- Using dot product on un-normalised vectors and calling it cosine -> long vectors win.
- Normalising with the wrong axis or without keepdims -> wrong or broadcasting-error results.
- Using a raw BERT [CLS] vector as a sentence embedding -> poor similarity.
- Mean pooling over padding -> embeddings change with batch composition.
- np.argsort(scores)[:k] for top-k -> returns the k LEAST similar.
- Skipping 'query:' / 'passage:' prefixes on asymmetric models -> recall drops quietly.
- Truncating a Matryoshka vector without re-normalising -> dot product no longer equals cosine.
- Truncating an ordinary embedding -> quality collapses.
- Comparing vectors from two models because shapes match -> meaningless scores.
- Upgrading the embedding model without re-embedding the corpus -> silent search failure.
- Trusting an unversioned embedding API -> silent drift after a provider update.
- Post-filtering a small ANN top-k -> almost no results survive.
- Assuming ANN is exact -> recall is below 100%.
- Believing projection debiasing removes bias -> bias remains recoverable.
- Raw contextual embeddings all look similar (0.8+) -> anisotropy; mean-centre or use a similarity-trained model.

## Interview angle
- **"How does semantic search work end to end?"** Chunk documents, embed each chunk with a bi-encoder, store vectors (plus metadata) in an ANN index such as HNSW. At query time, embed the query with the SAME model, take the top-k by cosine, optionally re-rank with a cross-encoder, and return. SDE analogy: a vector DB is an index for similarity instead of equality.
- **"Cosine vs dot product vs Euclidean?"** Cosine compares direction only; dot also rewards length; Euclidean measures straight-line distance. On L2-normalised vectors all three give the same ranking, so normalise once and use the fast dot product, unless the model was trained for raw dot product.
- **"Explain word2vec in a minute."** A shallow network trained on a fake task: predict neighbours from a word (skip-gram) or a word from its neighbours (CBOW). Negative sampling makes it cheap. The learned weight matrix is the embedding table, and words in similar contexts get similar rows.
- **"Bi-encoder vs cross-encoder?"** Bi-encoder: embed query and document separately, so documents can be pre-computed; fast, used for retrieval. Cross-encoder: reads the pair together; more accurate, but one forward pass per pair, so it is only used to re-rank the top ~100.
- **"What breaks when you change the embedding model?"** Every stored vector is in the old space. You must re-embed the corpus, version the index by model, and switch atomically. Mixing models gives silent garbage, even with the same dimension.

## Source material
To be added.
