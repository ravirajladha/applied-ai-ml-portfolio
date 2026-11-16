# Retrieval-Augmented LMs (M8): coverage spec

**Ladder:** LLMs for Generative AI (AIMLCZG536) › M8 Retrieval-Augmented Language Models   ·   **Prerequisites:** llmc-foundations (embeddings), llmc-inference (prefill, TTFT), llmc-prompting (decomposition, routing, ReAct)
**Why it matters for AI/ML:** Module 8 explains why a model's parametric knowledge is not enough, how a retriever-generator pipeline is built (offline index, online query), how chunking, retrievers and rerankers decide what the model sees, how Self-RAG and self-correcting RAG add reflection and verification, and how to diagnose a bad answer from the output backward. The end-sem papers test it with "RAG assistant on API docs / contracts" failure-diagnosis questions, "which retriever for Q1/Q2/Q3 over heterogeneous sources" questions and RAGAS metrics by hand.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `why-rag` | Limits of parametric knowledge and long context | knowledge cutoff, no citations | lost in the middle, needle-in-a-haystack, cost per token | when not to use RAG (fine-tune / long context / tools / agentic) | RAG vs long context trade-offs in numbers |
| 2 | `pipeline` | RAG pipeline: offline index, online query | retrieve then generate | offline vs online stages, same encoder rule, four design questions | prompt cost formula, prefill/TTFT | budget arithmetic for chunk size and top-k |
| 3 | `chunking` | Chunking strategies | why chunk | fixed vs sliding window, overlap | structure-aware, semantic, hierarchical; overlap costs and dedup | choosing chunking from failure patterns |
| 4 | `retrievers` | Sparse, dense, hybrid and tabular retrievers | keyword vs meaning | BM25 vs dense on representation, matching, vocabulary mismatch | course BM25 by hand, hybrid fusion (RRF) | which retriever for heterogeneous sources (tabular / SQL retriever) |
| 5 | `index-rerank` | Vector indexes and reranking | what a vector DB is | exact vs ANN, HNSW vs IVF, bi-encoder vs cross-encoder | two-stage recall vs precision | reranker cost and what it cannot fix |
| 6 | `context` | Context engineering and compression | grounding instruction | anatomy of a RAG prompt, chunk metadata, query last | context budget, conflicts with parametric memory, compression methods | compression trade-offs, position of chunks |
| 7 | `self-rag` | Self-RAG (reflection tokens) | the idea: retrieve on demand and critique | the four reflection tokens | critic vs generator training, segment selection | reflection-token scoring by hand, limits |
| 8 | `self-correcting` | Verification and self-correcting RAG (CRAG, CoVe, agentic RAG) | why check retrieved docs | CRAG's three actions, CoVe steps | retrieve-evaluate-retry loops in the app layer | budgets, fallbacks, Self-RAG vs CRAG |
| 9 | `diagnosis` | RAG failure diagnosis | read what was retrieved | the symptom table | the API-docs P1/P2/P3 pattern and fixes | confident-but-wrong vs ignored-context transcripts |
| 10 | `rag-metrics` | RAG evaluation metrics (RAGAS) | faithfulness vs answer relevance | context precision and recall | metrics by hand, diagnosis from scores | faithfulness vs truthfulness, why BLEU/BERTScore miss it |

## Must-know facts
- Parametric knowledge is frozen at training time, opaque (no sources), expensive to update and has never seen your private data. "Fine-tuning changes how the model behaves. RAG changes what it can know."
- Pasting everything into a long window fails twice: recall degrades (needle-in-a-haystack; worst at 10-50% depth, "lost in the middle"; attention favours start and end) and cost/latency scale with every token on every query.
- RAG pipeline: receive q -> retrieve top-k passages (BM25, vector or hybrid) -> assemble instruction + q + passages -> generate a grounded answer.
- Offline: docs -> chunk -> embed -> index (ANN) -> store. Online: query -> embed (same encoder!) -> search -> rerank -> LLM.
- Four design questions: what to index (offline), how to chunk (offline), how to retrieve (online), how to rank (online).
- Prompt cost ≈ system + query + (chunk_size × top_k) + output; doubling chunk size or top_k doubles retrieval tokens and roughly doubles prefill (TTFT), not decode.
- Chunking: fixed-size (boundaries cut mid-sentence), sliding window (overlap keeps facts whole; ~20-25% more chunks; duplicate hits), structure-aware (headings, code, table rows with headers repeated), semantic, hierarchical, sentence/token splitting.
- Dedup at retrieval time: over-retrieve (top-20), drop same doc_id + large overlap or same content hash, keep top-5 unique.
- Sparse (BM25) = term-frequency vectors, exact lexical match, interpretable, weak on synonyms. Dense (DPR, bi-encoder) = learned embeddings, semantic match, handles paraphrase, needs model + index.
- BM25 as the course computes it: idf = log10(N / df); term score = idf × tf / (tf + k(1 - b + b·|D|/avgdl)); k in [1.2, 2], b = 0.75; k = 0 leaves only idf; b = 0 disables length normalisation. (The textbook version also multiplies the numerator by (k + 1); this rescales scores but not the ranking.)
- Bi-encoder: query and doc encoded separately, doc vectors precomputed, score = dot product, scales to millions via ANN (HNSW graph in RAM; IVF k-means clusters for very large corpora). Cross-encoder: [CLS] q [SEP] d [SEP] jointly, precise, nothing precomputable; used as a reranker.
- Two stages: retriever's job is recall (is the answer somewhere in top-k?), reranker's job is precision (put it at rank 1).
- RAG prompt anatomy: grounding rules (answer only from context, cite chunk ids, exact refusal string), chunks with metadata (id, heading trail, version), query placed last.
- Context budget: window - system/grounding - history - generation headroom = room for chunks; divide by average chunk size for the top-k ceiling. Fitting 7 chunks doesn't mean sending 7.
- Context compression: extractive (keep only relevant sentences), abstractive (summarise), token pruning (LLMLingua-style). Saves tokens and reduces lost-in-the-middle; risks dropping the needed fact.
- Self-RAG trains one LM to emit reflection tokens: Retrieve (retrieve or not), ISREL (passage relevant?), ISSUP (output supported?), ISUSE (overall usefulness 1-5). A critic model labels training data offline; at inference the generator retrieves on demand and ranks candidate segments by reflection-token scores.
- CRAG: a lightweight retrieval evaluator scores retrieved docs -> Correct (refine: decompose-then-recompose into knowledge strips), Incorrect (discard, web search with a rewritten query), Ambiguous (both). Plug-and-play in the application layer.
- CoVe: draft -> plan verification questions -> answer them independently -> final verified answer.
- Agentic RAG: the LLM decides whether to retrieve, which source, how many times, when to stop; self-check-and-retry with a max-retry budget.
- Most "LLM errors" in RAG are retrieval or prompt errors: read what was retrieved first. A grounded, cited, wrong answer is a retrieval bug.
- RAGAS: Faithfulness = supported claims / total claims; Answer relevance; Context precision = relevant chunks / retrieved chunks; Context recall = needed facts retrieved / needed facts total (needs ground truth).
- Faithfulness = entailment by the retrieved context; truthfulness = agreement with real-world facts.

## Common traps (each one must have at least one question)
- "Just use a 1M-token window" -> recall drops mid-context and you pay for every token every query.
- Re-embedding queries with a new model but keeping old document vectors -> incomparable vectors, retrieval collapses.
- "Bigger top-k is always safer" -> more noise, cost, TTFT and lost-in-the-middle.
- Overlap with no dedup -> the same fact fills two of five slots.
- Fixed-size chunks cutting a fact or table in half -> neither chunk matches.
- Using BM25 alone for paraphrased questions; using dense alone for exact IDs and specific phrases.
- Any text retriever (BM25, dense, hybrid) for numeric filters and joins over relational tables -> needs a tabular / SQL retriever.
- "A reranker will fix missing documents" -> it can only reorder what stage 1 returned.
- Cross-encoder over the whole corpus -> one forward pass per pair, impossible at 10M docs.
- A grounded, cited, wrong answer blamed on the LLM -> it's retrieval (stale version won).
- Right chunk retrieved but ignored -> prompt fault (no grounding rules, chunk buried mid-prompt).
- Self-RAG confused with a separate verifier pipeline -> the generator itself emits the reflection tokens.
- CRAG confused with Self-RAG -> CRAG adds an external evaluator and corrective actions, no generator retraining.
- High faithfulness read as "correct" -> faithful to wrong context is still wrong.
- BLEU/ROUGE/BERTScore used as faithfulness -> they compare to a reference, never to the retrieved context.
- Context recall computed without ground truth -> it needs the set of needed facts.

## Interview angle
1. **"Why not just use a long-context model?"** Lost in the middle and needle-in-a-haystack show recall drops at large contexts; every token is paid and prefilled on every query; no citations or freshness control. Retrieval selects what goes in the window.
2. **"Your API-docs bot misses deprecation notes, ranks an old changelog first and cuts multi-paragraph answers. Fix?"** Section/semantic chunking for the note buried in a mixed chunk; a cross-encoder reranker (or dense/hybrid) for the lexical-bias ranking; sliding-window overlap for truncated answers.
3. **"Which retriever for guidelines, patient tables and policy memos?"** Dense (or dense-leaning hybrid) for paraphrased guideline questions; a tabular / text-to-SQL retriever for numeric filters and joins; BM25 (or BM25-leaning hybrid) for short memos with exact institutional phrases.
4. **"Self-RAG vs CRAG?"** Self-RAG trains the generator to emit reflection tokens (retrieve? relevant? supported? useful?). CRAG keeps the generator and adds a retrieval evaluator that triggers refine / web search / both.
5. **"RAGAS shows context precision 0.4, faithfulness 0.6, context recall 1.0. What do you fix?"** Retriever is complete but noisy -> rerank, tighten threshold, hybrid. Generator adds unsupported claims -> stricter grounding prompt, claim verifier, lower temperature.

## Source material
- Handout (`llm-src/handout.txt`), Module 8 (2 hrs, session 12): Limits of Long-Context Models (lost in the middle, needle-in-a-haystack); RAG Pipeline Overview and Context Compression; Self-Reflective RAG (Self-RAG); Verification and Self-Correction (Chain-of-Verification, CoVe); Self-Correcting RAG in the Application Layer. Texts T1 ch 11, T2 ch 8, R2 (Kimothi, *A Simple Guide to RAG*) ch 6.
- Old-batch M8 deck (`old-batch-slides.txt` ~lines 3660-4105): "Why LLMs need external knowledge" (parametric knowledge limits table; "fine-tuning changes how it behaves, RAG changes what it can know"); NIAH and lost in the middle (10-50% depth); "do not dump everything".
- Same deck: RAG pipeline steps; offline (chunk, embed, index, store) vs online (embed with the same encoder, search, rerank, LLM); four design questions; prompt cost formula tokens ≈ system + query + chunk_size × top_k + output (256 -> 1,280, 512 -> 2,560, 1024 -> 5,120 at top_k = 5); prefill/TTFT numbers (Llama-3-70B: 1k tokens ≈ 0.2-0.3 s, 10k ≈ 2-3 s).
- Same deck: chunking (fixed-size vs sliding window with stride, leave-policy carry-forward example, overlap costs ~20-25% more chunks and duplicate hits, dedup fix; structure-aware for Markdown/code/tables; sentence, token, semantic, hierarchical).
- Same deck: sparse vs dense; BM25 worked example (Q = "apple banana", k = 1.5, b = 0.75, idf = log10(3/2) = 0.17609; D1 = 0.1825, D2 = 0.0978, D3 = 0.0767, so D1 > D2 > D3 by the slide's own numbers; its text "D1 > D3 > D2" is a slip); DPR bi-encoder vs cross-encoder; ANN (HNSW, IVF); vector DB categories (FAISS / Pinecone, Milvus, Qdrant, Weaviate, Chroma / pgvector / Elasticsearch); retrieve-then-rerank (top-100 -> top-5; recall vs precision; Qwen2.5-3B context-length reranking example).
- Same deck: context engineering (RAG prompt anatomy with grounding rules, chunk metadata, query last; conflict tips; 8K budget: 8,000 - 600 - 1,400 - 1,000 = 5,000 / 700 ≈ 7 chunks); failure transcripts (confident but wrong = retrieval; context ignored = prompt); symptom -> cause -> fix table; advanced RAG = prompt patterns (query rewriting, multi-query, multi-hop, routing); agentic RAG (self-check and retry = "the Self-RAG idea", ReAct, memory); when not to use RAG. References: Self-RAG, RAFT, REALM, ATLAS.
- Eval deck (~lines 5040-5100): hallucination intrinsic vs extrinsic; faithfulness vs truthfulness; RAGAS four metrics and the worked example (faithfulness 2/3, context precision 2/4, context recall 2/2) with the diagnosis "retriever over-retrieves, generator added a fact".
- Self-RAG reflection tokens (Asai et al. 2023), CRAG (Yan et al. 2024), CoVe (Dhuliawala et al. 2023) and context compression (RECOMP-style extractive/abstractive, LLMLingua token pruning) come from the handout topic list and R2/papers; the old slides only name them, so questions on them use the papers' own terms.
- Exam patterns: Sep 2025 / Sep 2026 Regular end-sems: "RAG assistant on internal API documentation (or contract review)" with BM25 + fixed 512/400-token chunks + 4K generator; diagnose P1 (note at end of section missed: boundary loss), P2 (old changelog/brochure ranks first: BM25 lexical bias), P3 (multi-paragraph answer cut off: truncation), then match F1 sliding window -> P3, F2 semantic chunking -> P1, F3 cross-encoder reranker -> P2. Sep 2025 Makeup: heterogeneous sources (guideline PDFs, policy memos, relational tables, FAQs) with one dense retriever; compare BM25 vs dense on representation / matching / vocabulary mismatch and pick dense for Q1, tabular retriever for Q2, BM25 for Q3. Regular papers also compute RAGAS faithfulness / context precision / context recall by hand and ask why BLEU cannot see the hallucination.
