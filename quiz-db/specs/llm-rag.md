# RAG (Retrieval-Augmented Generation): coverage spec

**Ladder:** L4 · LLM Engineering › Building with LLMs   ·   **Prerequisites:** nlp-embeddings (vectors, cosine similarity), llm-prompting, basic NumPy
**Why it matters for AI/ML:** RAG is the default way to make an LLM answer from *your* data (docs, tickets, policies) without retraining. Most production GenAI features are RAG systems, and most of their bugs are retrieval bugs: wrong chunks, missing chunks, stale data, leaked permissions.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `why-rag` | Why RAG and the pipeline | open-book idea, RAG reduces but doesn't remove hallucination | pipeline order, RAG for changing facts vs fine-tuning for tone | RAG vs long context vs fine-tuning | — |
| 2 | `chunking` | Chunking strategies | why split documents, fixed-size chunks, what overlap is | size/overlap arithmetic, too-small vs too-large chunks, recursive splitting, sentence packing | overlap >= size bug, structural/semantic chunking, chunk-count arithmetic, contextual chunk headers | small-to-big (parent-child) retrieval |
| 3 | `embeddings` | Embedding models and similarity | what an embedding is, cosine similarity, meaning without shared words | normalised dot = cosine, same model for queries and docs | dot vs cosine with unnormalised vectors, index memory, silent truncation at max length, scores are not probabilities | asymmetric query/doc prefixes, binary/int8 quantisation, Matryoshka truncation needs re-normalising, anisotropy |
| 4 | `vector-index` | Vector DBs and ANN search | ANN is approximate, top-k | top-k with NumPy, argsort direction | HNSW recall vs speed (ef), when brute force is fine, IVF nprobe, argpartition top-k | measuring ANN recall, HNSW `M`, PQ memory arithmetic, tombstoned deletes degrade the graph |
| 5 | `hybrid` | Hybrid search (BM25 + dense, RRF) | what keyword (BM25) search is, what hybrid search is | where dense search fails (IDs, codes) | RRF arithmetic, why raw scores can't be added | the RRF k constant, RRF discards score margins, equal-weight fusion can lose to dense alone |
| 6 | `filtering-security` | Metadata filters, permissions, multi-tenancy | filtering by metadata | tenant filters in code, filtering during the search | pre- vs post-filtering, enforce ACLs at retrieval | ACL changes, per-tenant isolation trade-offs, leaks through derived artifacts and shared semantic caches |
| 7 | `rerank` | Reranking with cross-encoders | what a reranker does | bi-encoder vs cross-encoder, relevance thresholds instead of fixed k | retrieve-many, rerank-few latency budget, reranking can't fix first-stage recall, MMR diversity | why cross-encoder scores can't be precomputed |
| 8 | `query-transform` | Query rewriting, multi-query, HyDE | rewriting follow-up questions | multi-query retrieval, query decomposition | HyDE | HyDE / rewrite failure modes, rewrites dropping negations and numbers |
| 9 | `context-citations` | Context assembly and citations | why cite sources, chunks go into the prompt | grounding instructions, "I don't know", labelling chunks with ids | token budget packing, chunk ids for citations and checking them in code, best-at-edges ordering, valid id != supported claim | — |
| 10 | `rag-eval` | Evaluating RAG | evaluate retrieval and generation separately, recall@k | recall@k, faithfulness arithmetic, hit rate, MRR | MRR, precision@k, faithfulness vs answer relevance, mean recall@k over an eval set, context recall | recall ceilings, judge and synthetic-set pitfalls, nDCG by hand, reference-free vs reference metrics, faithful-but-wrong |
| 11 | `failure-modes` | Failure modes and debugging | stale index, abstaining when the docs don't cover it | wrong chunk vs missing info, scanned PDFs without OCR | conflicting/outdated documents, duplicate boilerplate chunks | localising a bug: retrieval or generation |
| 12 | `advanced-rag` | Agentic RAG, GraphRAG, cost/latency | — | — | agentic (iterative) retrieval | GraphRAG for global questions, latency budgets |
| 13 | `sparse-retrieval` | TF-IDF and BM25 from scratch | IDF favours rare words, keyword overlap by code | sklearn TF-IDF retrieval, IDF by hand, vocabulary mismatch | BM25 by hand, k1 saturation, b length normalisation, out-of-vocabulary queries | learned sparse retrieval (SPLADE) |
| 14 | `freshness` | Ingestion, freshness and re-indexing | what re-indexing means | deleting chunks of deleted documents | content-hash incremental indexing, blue-green index swap for a model upgrade | positional chunk ids, read-after-write lag from async indexing |

## Must-know facts
- RAG = retrieve relevant chunks, put them in the prompt, generate an answer grounded in them. Knowledge lives outside the weights, so updating = re-indexing.
- Pipeline: ingest -> clean -> chunk -> embed -> index (offline); embed query -> retrieve top-k -> (rerank) -> assemble context -> generate with citations (online).
- Chunk size is a trade-off: too small loses context, too large dilutes the embedding and wastes tokens. Overlap keeps sentences that straddle a boundary; step = size - overlap must be > 0.
- Queries and documents must be embedded with the same model (and version). Changing the model means re-embedding the whole corpus.
- For unit-length vectors, dot product = cosine similarity. With unnormalised vectors, dot product favours long vectors.
- Memory of a flat fp32 index = n * dim * 4 bytes (1M x 768 = ~3.1 GB), before index overhead.
- ANN (e.g. HNSW) trades a little recall for big speed-ups; higher search effort (ef) = higher recall, slower. Brute force is fine for small corpora.
- Dense search misses exact tokens (error codes, SKUs, names); BM25 catches them. Hybrid + Reciprocal Rank Fusion: score = sum 1/(k + rank), k usually 60.
- BM25 and cosine scores are on different scales; never just add them. RRF uses ranks only.
- Filter before (or during) the ANN search; filtering after top-k can return fewer than k results, or none.
- Permissions must be enforced in retrieval (filters/separate indexes), never by asking the LLM not to reveal things.
- Cross-encoder rerankers read query + chunk together: more accurate, but must run per pair at query time, so rerank only the top 20-100.
- recall@k = relevant found in top k / total relevant. MRR = mean of 1/rank of the first relevant hit. Faithfulness = fraction of answer claims supported by the context.
- Evaluate retrieval and generation separately so you know which half to fix.
- Common failures: right info not in index, info chunked badly, wrong chunk ranked first, stale index, conflicting versions, model ignoring context.
- TF-IDF / BM25 weight rare terms up (IDF). BM25's tf part saturates toward k1 + 1 (k1 ~ 1.2); b (~0.75) normalises for document length. Query words outside a fitted TF-IDF vocabulary score zero, silently.
- IVF searches `nprobe` clusters (more = higher recall, slower); HNSW's `M` sets graph degree (recall vs memory and build time); PQ compresses vectors ~32x at some recall cost, so re-rank a shortlist with full vectors.
- HNSW deletes are usually tombstones; heavy churn degrades recall and latency until a rebuild.
- RRF uses ranks only: robust, but it discards score margins, and equal weighting can let a weak retriever drag down a strong one.
- A reranker can only reorder its candidates: it can raise recall@5, never recall@50 of stage one.
- Embedding models truncate input past their max length, often silently. Similarity scores are model-specific, not probabilities, and often crowd into a narrow band.
- Context recall needs a reference answer; faithfulness and answer relevance don't. A faithful answer to stale context is still wrong.
- Incremental indexing: stable chunk ids + content hashes; re-embed only changed chunks, delete removed ones; swap indexes blue-green for model upgrades.
- Derived stores (semantic caches, summaries, graphs) need ACLs too, because a cache hit skips the retrieval filter.

## Common traps (each one must have at least one question)
- "RAG eliminates hallucination" -> it reduces it; the model can still ignore or misread context.
- Overlap >= chunk size -> step of 0 (ValueError) or an infinite loop.
- Swapping the embedding model for queries only -> query and doc vectors no longer comparable.
- `np.argsort(scores)[:k]` -> gives the *lowest* scores; sort descending.
- Dot product on unnormalised vectors -> long vectors win regardless of direction.
- Adding BM25 and cosine scores directly -> BM25's larger scale dominates.
- Post-filtering after top-k -> fewer than k results, often none for small tenants.
- "Tell the LLM not to show HR docs to non-HR users" -> permissions in the prompt are not security.
- "More chunks in context = better answers" -> lost in the middle, distraction, cost.
- Stale index -> answers from last quarter's policy after the doc was updated.
- Conflicting versions of a document -> model mixes old and new; needs dates/versions in metadata.
- High recall@k with wrong answers -> the problem is generation/context assembly, not retrieval.
- HyDE on a topic the model knows nothing about -> the hypothetical answer is confidently wrong and retrieves the wrong neighbourhood.
- Synthetic eval questions generated from chunks -> too easy, overstate retrieval quality.
- "BM25 score grows with every repetition" -> it saturates; 100 mentions is about 2.2x one mention.
- Chunks longer than the embedder's max length -> the tail is silently not embedded.
- "Cosine 0.8 = 80% relevant" / a fixed 0.5 threshold -> scores are model-specific and bunched.
- IVF with nprobe = 1 -> neighbours across cluster boundaries are missed.
- Adding a reranker to fix poor first-stage recall -> it can't add what wasn't retrieved.
- "Every citation id is valid, so the answer is grounded" -> the cited chunk may not support the claim.
- Positional chunk ids (`doc#3`) -> one insert at the top re-embeds everything and breaks citations.
- Re-embedding in place / only new docs during a model upgrade -> two vector spaces mixed in one index.
- Forgetting deletes in the indexer -> ghost content cited forever.
- Shared semantic cache across users -> bypasses ACL filters.
- Truncating Matryoshka embeddings without re-normalising -> dot product is no longer cosine.
- Query rewriter dropping "not" or numbers -> constraints silently lost.

## Interview angle
1. **"Design a RAG system for our internal docs."** Ingest with metadata (source, date, ACL), structure-aware chunking with overlap, embed with one versioned model, hybrid index (BM25 + vectors), permission filters at query time, retrieve ~50, rerank to ~5, pack context with chunk ids, prompt to answer only from context and cite, eval set for retrieval (recall@k) and generation (faithfulness), re-index on document change. SDE analogy: cache-aside lookup plus an open-book exam.
2. **"Your RAG bot gives a wrong answer. How do you debug it?"** Check whether the right chunk exists in the index; whether it was retrieved in top-k; whether it survived reranking and context packing; then whether the model used it. Each step has its own metric.
3. **"Why hybrid search?"** Dense embeddings capture meaning but blur exact tokens like `ERR-4031` or product codes; BM25 matches them exactly. Fuse ranks with RRF because the score scales differ.
4. **"How do you handle multi-tenant data?"** Enforce tenant/ACL filters inside the retrieval query (or separate namespaces/indexes), never in the prompt; filter before the top-k cut; test for cross-tenant leakage.
5. **"RAG or fine-tuning?"** RAG for facts that change and need citations; fine-tuning for behaviour, format and style. Often both.
6. **"HNSW or IVF-PQ?"** HNSW: high recall and low latency, but memory-heavy (vectors + links) and awkward with heavy deletes. IVF-PQ: compressed codes (~32x), needs k-means training on representative data, recall tuned via nprobe plus re-ranking with full vectors. Under ~100k vectors, brute force with NumPy is fine.
7. **"How do you keep the index fresh?"** Event-driven ingestion with stable ids and content hashes, re-embed only changed chunks, sync deletes, store updated_at/version metadata, show index freshness, and do model upgrades as a blue-green index swap. SDE analogy: a read replica with lag; design for eventual consistency.

## Source material
To be added.
