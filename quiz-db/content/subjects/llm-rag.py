from helpers import mcq, tf, out, fill

SUBJECT = "llm-rag"

TOPICS = [
    ("why-rag", "Why RAG and the pipeline"),
    ("chunking", "Chunking strategies"),
    ("embeddings", "Embedding models and similarity"),
    ("vector-index", "Vector DBs and ANN search"),
    ("hybrid", "Hybrid search (BM25 + dense, RRF)"),
    ("filtering-security", "Metadata filters, permissions, multi-tenancy"),
    ("rerank", "Reranking with cross-encoders"),
    ("query-transform", "Query rewriting, multi-query, HyDE"),
    ("context-citations", "Context assembly and citations"),
    ("rag-eval", "Evaluating RAG"),
    ("failure-modes", "Failure modes and debugging"),
    ("advanced-rag", "Agentic RAG, GraphRAG, cost/latency"),
    ("sparse-retrieval", "TF-IDF and BM25 from scratch"),
    ("freshness", "Ingestion, freshness and re-indexing"),
]

QUESTIONS = [
    # ------------------------------------------------------------------ L1
    tf("Once you add RAG, the model can no longer hallucinate.", False,
       "Can a student with an open book still misread it?",
       "RAG reduces hallucination by giving the model the right text, but it can still ignore the context, mix chunks up, or answer when nothing relevant was retrieved.",
       topic="why-rag", level=1),
    mcq("A model was trained on data up to last year. Your company changed its leave policy last week. Without retraining, how does RAG let the bot answer correctly?",
        ["It looks up the new policy text at question time and puts it in the prompt",
         "It updates the model's weights every night",
         "It asks the user to paste the policy",
         "It can't; only fine-tuning can"], 0,
        "Where does the fresh knowledge live in RAG?",
        "In RAG the knowledge lives in an index you control. Update the document, re-index it, and the next question retrieves the new text.",
        topic="why-rag", level=1,
        analogy="Cache-aside: look up the source of truth instead of trusting a stale copy baked into the binary."),
    out('words = "the quick brown fox jumps over the lazy dog".split()\nsize = 4\n'
        'chunks = [words[i:i + size] for i in range(0, len(words), size)]\nprint(len(chunks), chunks[-1])',
        ["3 ['dog']", "2 ['over', 'the', 'lazy', 'dog']", "3 ['lazy', 'dog']", "9 ['dog']"], 0,
        "9 words, 4 per chunk.",
        "Chunks start at words 0, 4 and 8, so there are 3 chunks and the last holds just 'dog'. Fixed-size chunking often leaves a small tail.",
        topic="chunking", level=1),
    mcq("Why not embed a whole 200-page manual as a single vector?",
        ["One vector would blur 200 pages of topics together, so no single question would match it well, and it wouldn't fit in the prompt anyway",
         "Vector databases ban long documents",
         "Embedding models only accept English",
         "It would make the model forget its training"], 0,
        "Think of averaging every topic into one point.",
        "An embedding is one point in meaning-space. Small focused chunks give sharp points that match specific questions, and only the relevant pieces go into the prompt.",
        topic="chunking", level=1),
    mcq("What is an embedding, in one line?",
        ["A list of numbers that represents the meaning of a piece of text, so similar meanings get nearby vectors",
         "A compressed zip of the text",
         "The text translated into code",
         "A hash that changes completely if one letter changes"], 0,
        "Meaning as coordinates.",
        "Embedding models map text to vectors (e.g. 768 numbers). 'refund policy' and 'money back rules' land close together.",
        topic="embeddings", level=1),
    out('import numpy as np\na = np.array([1.0, 0.0])\nb = np.array([1.0, 1.0])\n'
        'cos = a @ b / (np.linalg.norm(a) * np.linalg.norm(b))\nprint(round(float(cos), 3))',
        ["0.707", "1.0", "0.5", "1.414"], 0,
        "The angle between them is 45 degrees.",
        "cos = 1 / (1 * sqrt(2)) = 0.707. Cosine similarity measures direction: 1 = same direction, 0 = unrelated.",
        topic="embeddings", level=1,
        diagram="""
   y
   |    b (1,1)
   |   /
   |  /  45 deg
   | /
   +--------- a (1,0)  x
"""),
    tf("An approximate nearest neighbour (ANN) index can occasionally miss the true closest vector in exchange for much faster search.", True,
       "What does the A in ANN stand for?",
       "ANN indexes (HNSW, IVF) skip most of the data to be fast, so recall is high but not guaranteed 100%. That trade-off is tunable.",
       topic="vector-index", level=1),
    mcq("What does keyword search like BM25 rank documents by?",
        ["How often the query's words appear in the document, weighted so rare words count more",
         "How similar the embeddings are",
         "The document's file size",
         "The date the document was added"], 0,
        "It's the classic search-engine method.",
        "BM25 scores exact term matches, boosting rare terms and normalising for document length. No neural network involved.",
        topic="hybrid", level=1),
    mcq("Each chunk is stored with metadata like `{\"dept\": \"hr\", \"year\": 2026}`. What can you do with it at query time?",
        ["Restrict the search, e.g. only HR chunks from 2026",
         "Make the embedding more accurate",
         "Train the LLM",
         "Nothing; metadata is only for display"], 0,
        "Think WHERE clause.",
        "Metadata filters narrow the candidate set before or during similarity search, like a SQL WHERE plus ORDER BY similarity.",
        topic="filtering-security", level=1),
    mcq("In a RAG pipeline, what does a reranker do?",
        ["Re-scores the top retrieved chunks with a more accurate (slower) model and reorders them",
         "Re-embeds the whole corpus",
         "Ranks the final answers by length",
         "Decides which LLM to call"], 0,
        "Cheap first pass, careful second pass.",
        "Retrieval quickly finds ~50 candidates; a reranker reads each with the query and keeps the best few for the prompt.",
        topic="rerank", level=1,
        analogy="A recruiter's quick CV filter, then a proper interview for the shortlist."),
    mcq("A user asks \"What's the refund window?\" and then \"And for electronics?\". Why might the second question retrieve badly on its own?",
        ["Alone, \"And for electronics?\" doesn't mention refunds, so the search has little to match; rewrite it into a standalone question first",
         "Short questions can't be embedded",
         "Electronics is a banned word",
         "The vector DB caches the first answer"], 0,
        "What does the search engine see?",
        "Follow-ups depend on chat history. Query rewriting turns them into standalone queries like 'refund window for electronics' before retrieval.",
        topic="query-transform", level=1),
    mcq("Why should a RAG answer include citations (which chunk or document it used)?",
        ["So users and reviewers can check the answer against the source",
         "Citations make the model faster",
         "The API requires them",
         "They reduce token cost"], 0,
        "Trust, but verify.",
        "Citations make answers checkable, help debugging, and build user trust. They also let you measure whether the model used the right sources.",
        topic="context-citations", level=1),
    mcq("Why evaluate the retrieval step separately from the final answer?",
        ["So when an answer is wrong you know whether search failed or the model failed",
         "Retrieval is never wrong",
         "Only the final answer matters to users, so retrieval needs no tests",
         "Because LLMs can't be evaluated"], 0,
        "Two components, two sets of tests.",
        "Retrieval metrics (recall@k) and generation metrics (faithfulness) point to different fixes. Without both, you can't tell which half broke.",
        topic="rag-eval", level=1,
        analogy="Unit tests per service instead of only an end-to-end test."),
    tf("If a document is updated but never re-indexed, the RAG bot can keep answering from the old version.", True,
       "The index is a copy of the data.",
       "A stale index is a classic RAG bug. Re-index on change (or on a schedule) and store document versions/dates in metadata.",
       topic="failure-modes", level=1),
    fill("RAG stands for Retrieval-Augmented ____.", "Generation",
         "The last step is the LLM writing the answer.",
         "Retrieval-Augmented Generation: retrieve relevant text, then generate an answer with it in the prompt.",
         topic="why-rag", level=1),

    # ------------------------------------------------------------------ L2
    mcq("Put the offline (indexing) part of a RAG pipeline in order.",
        ["ingest -> chunk -> embed -> store in index",
         "embed -> ingest -> chunk -> store in index",
         "chunk -> store in index -> embed -> ingest",
         "ingest -> embed -> store in index -> chunk"], 0,
        "You can't embed a chunk that doesn't exist yet.",
        "Load and clean documents, split into chunks, embed each chunk, store vectors + text + metadata. Online: embed the query, retrieve, (rerank), generate.",
        topic="why-rag", level=2,
        diagram="""
 OFFLINE: docs -> clean -> chunk -> embed -> [index]
 ONLINE:  query -> embed -> search [index] -> top-k
          -> rerank -> prompt(query + chunks) -> LLM
"""),
    out('text = "x" * 100\nsize, overlap = 40, 10\nstep = size - overlap\n'
        'chunks = [text[i:i + size] for i in range(0, len(text), step)]\n'
        'print(len(chunks), [len(c) for c in chunks])',
        ["4 [40, 40, 40, 10]", "3 [40, 40, 20]", "4 [40, 40, 40, 40]", "3 [40, 40, 40]"], 0,
        "Each new chunk starts 30 characters after the last.",
        "Starts at 0, 30, 60, 90: four chunks, the last only 10 characters long. Overlap means more chunks than len/size.",
        topic="chunking", level=2),
    mcq("You use 50-token chunks and answers often miss key details; with 2,000-token chunks the right section is found but answers get vague and costly. What's the usual fix?",
        ["A middle size (a few hundred tokens) with some overlap, then tune on your eval set",
         "Always use the smallest possible chunk",
         "Always use the biggest chunk that fits the context window",
         "Chunk size doesn't affect retrieval"], 0,
        "Both extremes failed.",
        "Tiny chunks lose context; huge chunks blur the embedding and waste tokens. Pick a middle size per document type and measure recall@k.",
        topic="chunking", level=2),
    out('import numpy as np\na = np.array([3.0, 4.0]); b = np.array([4.0, 3.0])\n'
        'an, bn = a / np.linalg.norm(a), b / np.linalg.norm(b)\n'
        'print(round(float(an @ bn), 2), round(float(a @ b), 2))',
        ["0.96 24.0", "0.96 0.96", "24.0 0.96", "1.0 24.0"], 0,
        "Both vectors have length 5.",
        "After dividing by length 5, the dot product is the cosine (0.96). The raw dot product (24) also depends on vector length.",
        topic="embeddings", level=2),
    mcq("You upgrade to a better embedding model for incoming queries, but leave the stored document vectors as they were. What happens?",
        ["Retrieval breaks: vectors from two different models live in unrelated spaces, so similarities are meaningless",
         "Retrieval improves immediately",
         "Nothing changes",
         "The vector DB converts the old vectors automatically"], 0,
        "Are coordinates from two different maps comparable?",
        "Queries and documents must come from the same model and version. Changing the model means re-embedding the whole corpus (store the model name in metadata).",
        topic="embeddings", level=2),
    out('import numpy as np\ndocs = ["refund policy", "shipping times", "reset password", "refund timeline"]\n'
        'D = np.array([[0.9, 0.1], [0.1, 0.9], [0.3, 0.7], [0.8, 0.3]])\n'
        'D = D / np.linalg.norm(D, axis=1, keepdims=True)\n'
        'q = np.array([1.0, 0.2]); q = q / np.linalg.norm(q)\n'
        'top = np.argsort(-D @ q)[:2]\nprint([docs[i] for i in top])',
        ["['refund policy', 'refund timeline']", "['refund timeline', 'refund policy']",
         "['shipping times', 'reset password']", "['refund policy', 'reset password']"], 0,
        "The query points mostly along the first axis.",
        "With normalised vectors, D @ q is cosine similarity. argsort(-scores) sorts high to low; the two 'refund' chunks point closest to the query.",
        topic="vector-index", level=2),
    out('import numpy as np\nscores = np.array([0.91, 0.12, 0.55, 0.87])\nprint(np.argsort(scores)[:2])',
        ["[1 2]", "[0 3]", "[3 0]", "[0 1]"], 0,
        "Which way does argsort sort?",
        "argsort is ascending, so [:2] gives the two WORST matches. Use np.argsort(-scores)[:k] or [::-1] for top-k.",
        question="You want the indices of the top-2 matches. What does this print?",
        topic="vector-index", level=2),
    mcq("Users search for error code `ERR-4031`. Dense (embedding) search returns chunks about other errors. Why, and what helps?",
        ["Embeddings capture general meaning and blur exact tokens; add keyword (BM25) search alongside it",
         "The embedding model is broken; replace it",
         "Error codes can't be indexed",
         "Raise the LLM temperature"], 0,
        "'Similar meaning' vs 'exact string'.",
        "Codes, SKUs, names and acronyms are where dense retrieval is weak and BM25 shines. Hybrid search gets both.",
        topic="hybrid", level=2),
    out('chunks = [{"id": 1, "tenant": "acme", "text": "acme pricing"},\n'
        '          {"id": 2, "tenant": "globex", "text": "globex pricing"},\n'
        '          {"id": 3, "tenant": "acme", "text": "acme roadmap"}]\n'
        'def search(query, tenant):\n'
        '    return [c["id"] for c in chunks if c["tenant"] == tenant and query in c["text"]]\n'
        'print(search("pricing", "acme"))',
        ["[1]", "[1, 2]", "[1, 3]", "[2]"], 0,
        "Both conditions must hold.",
        "The tenant filter is part of the search itself, so Globex's pricing chunk can never be returned to Acme.",
        topic="filtering-security", level=2),
    mcq("Bi-encoder (embedding) retrieval vs a cross-encoder reranker: what's the key difference?",
        ["A bi-encoder embeds query and doc separately (doc vectors precomputed); a cross-encoder reads query + doc together and outputs one relevance score",
         "They are the same model with different names",
         "A cross-encoder is used at indexing time, a bi-encoder at query time",
         "A bi-encoder is always more accurate"], 0,
        "Which one can do its work before the query arrives?",
        "Bi-encoders are fast because documents are embedded once. Cross-encoders see both texts at once, which is more accurate but must run per (query, doc) pair.",
        topic="rerank", level=2,
        diagram="""
 bi-encoder:    q -> [enc] -> vq      d -> [enc] -> vd
                score = cos(vq, vd)   (vd precomputed)
 cross-encoder: [q + d] -> [model] -> score   (per pair)
"""),
    mcq("What is multi-query retrieval?",
        ["Ask the LLM for several rephrasings of the question, retrieve for each, and merge the results",
         "Send the same query to the vector DB several times for reliability",
         "Let multiple users share one query",
         "Split a document into multiple chunks"], 0,
        "Different wordings find different chunks.",
        "Rephrasings widen recall when the user's words don't match the document's words. Merge with dedup or RRF.",
        topic="query-transform", level=2),
    mcq("Which instruction best reduces made-up answers in a RAG prompt?",
        ["\"Answer only from the context below. If the answer isn't there, say you don't know. Cite chunk ids.\"",
         "\"Be as helpful as possible.\"",
         "\"Use your knowledge and the context.\"",
         "\"Never say you don't know.\""], 0,
        "Give the model a permitted way out.",
        "Grounding instructions plus an explicit 'I don't know' option cut hallucination; citations make it checkable.",
        topic="context-citations", level=2),
    out('retrieved = ["d7", "d2", "d9", "d4", "d1"]\nrelevant = {"d2", "d4", "d8"}\nk = 3\n'
        'hits = sum(d in relevant for d in retrieved[:k])\nprint(hits, round(hits / len(relevant), 2))',
        ["1 0.33", "2 0.67", "1 0.2", "2 0.4"], 0,
        "Only look at the first 3 results; divide by the number of relevant docs.",
        "Top 3 = d7, d2, d9: one relevant (d2). recall@3 = 1 / 3 relevant = 0.33.",
        topic="rag-eval", level=2),
    out('claims = {"refunds take 5 days": True,\n          "refunds need a receipt": True,\n'
        '          "refunds are free": False}   # supported by the retrieved context?\n'
        'print(round(sum(claims.values()) / len(claims), 2))',
        ["0.67", "0.33", "1.0", "2"], 0,
        "True counts as 1.",
        "Faithfulness (groundedness) = supported claims / total claims = 2/3. The unsupported claim is a hallucination even if it happens to be true.",
        topic="rag-eval", level=2),
    mcq("The right document exists, but it was never ingested (the PDF parser failed silently). Your eval shows the right chunk is missing from the top-k for these questions. Which failure is this?",
        ["Missing information: the content is not in the index at all",
         "Wrong chunk ranked first",
         "The LLM ignored the context",
         "Temperature too high"], 0,
        "Could any retriever have found it?",
        "Check that the answer exists in the index before tuning retrieval. Ingestion bugs (bad PDF parsing, skipped tables) are common and invisible without checks.",
        topic="failure-modes", level=2),
    mcq("Retrieval returns 20 chunks, so you put all 20 into the prompt \"to be safe\". What's the likely downside?",
        ["More cost and latency, and relevant facts get buried among distractors (lost in the middle)",
         "None: more context always improves answers",
         "The model will refuse prompts with more than 10 chunks",
         "Embedding quality drops"], 0,
        "Is more always better for the reader?",
        "Irrelevant chunks distract the model and cost tokens. Rerank and keep the best few, ordered with the strongest first.",
        topic="context-citations", level=2),

    # ------------------------------------------------------------------ L3
    mcq("Your docs are 30 pages each and the model has a 200k-token context window. A teammate says: \"Skip RAG, just paste the whole knowledge base (5,000 docs) into every prompt.\" Best response?",
        ["5,000 docs won't fit, and even for what fits, per-call cost, latency and lost-in-the-middle make retrieval of a few relevant chunks better",
         "Agree: long context makes RAG obsolete",
         "Agree, if temperature is 0",
         "Fine-tune instead; RAG and long context are both wrong"], 0,
        "Multiply tokens by calls per day.",
        "Long context helps for one or a few big documents. For a large corpus, RAG is cheaper, faster, updateable per document, and easier to cite.",
        topic="why-rag", level=3),
    out('text = "x" * 100\nsize, overlap = 20, 20\nchunks = [text[i:i + size] for i in range(0, len(text), size - overlap)]\nprint(len(chunks))',
        ["ValueError", "5", "0", "ZeroDivisionError"], 0,
        "What is the step of the range?",
        "step = size - overlap = 0, and range() with step 0 raises ValueError. In a while-loop chunker the same bug is an infinite loop. Validate overlap < size.",
        topic="chunking", level=3),
    mcq("You're chunking API docs full of headings, code blocks and tables. Fixed 500-token chunks split tables in half. Better approach?",
        ["Structure-aware chunking: split on headings/sections, keep tables and code blocks whole, and prefix each chunk with its section title",
         "Smaller fixed chunks of 50 tokens",
         "Remove tables and code before indexing",
         "Embed each sentence separately"], 0,
        "Use the document's own structure.",
        "Splitting by structure keeps self-contained units. Adding the heading path ('Billing > Refunds') to each chunk gives the embedding missing context.",
        topic="chunking", level=3),
    out('import numpy as np\nq = np.array([1.0, 0.0])\nsame_dir = np.array([0.9, 0.1])\nother_dir = np.array([3.0, 3.0])\n'
        'cos = lambda a, b: a @ b / (np.linalg.norm(a) * np.linalg.norm(b))\n'
        'print(q @ same_dir < q @ other_dir, cos(q, same_dir) > cos(q, other_dir))',
        ["True True", "False True", "True False", "False False"], 0,
        "Dot product grows with vector length; cosine doesn't.",
        "By raw dot product the long off-direction vector wins (3.0 > 0.9); by cosine the same-direction one wins. Normalise vectors or use the metric the model was trained for.",
        topic="embeddings", level=3),
    out('n, dim = 1_000_000, 768\nprint(round(n * dim * 4 / 1e9, 2))',
        ["3.07", "0.77", "768.0", "30.72"], 0,
        "float32 = 4 bytes per number.",
        "1M x 768 x 4 bytes = 3.07 GB for raw fp32 vectors, before index overhead (HNSW graph links add more). This drives instance size and cost.",
        question="How many GB does a flat fp32 index of 1M chunks with 768-dim embeddings need? What does this print?",
        topic="embeddings", level=3),
    mcq("In an HNSW index you raise the search-time parameter `ef` (candidate list size) from 16 to 256. What happens?",
        ["Recall goes up and queries get slower",
         "Recall goes down and queries get faster",
         "Index build time doubles but queries are unchanged",
         "Nothing; ef only matters at build time"], 0,
        "A bigger candidate list explores more of the graph.",
        "ef_search controls how many candidates are explored per query: the main recall-vs-latency knob. Tune it against an exact-search baseline.",
        topic="vector-index", level=3,
        diagram="""
 recall  ^          ______
         |      ___/
         |   __/
         |  /
         +----------------> latency
          ef=16  64   256
"""),
    mcq("You have 20,000 chunks of 384 dims. Is a full ANN vector database needed?",
        ["Not necessarily: exact brute-force search over 20k vectors is a fast matrix multiply and gives perfect recall",
         "Yes, brute force is impossible above 1,000 vectors",
         "Yes, because ANN is more accurate than exact search",
         "No, but only if you use BM25 instead"], 0,
        "20,000 x 384 is about 7.7 million multiply-adds.",
        "Brute force is O(n*d) per query; for tens of thousands of vectors that's milliseconds. ANN pays off at millions. Choose for ops needs (filters, updates), not hype.",
        topic="vector-index", level=3),
    out('bm25 = ["d1", "d2", "d3"]\ndense = ["d3", "d1", "d4"]\nk = 60\nscores = {}\n'
        'for ranking in (bm25, dense):\n    for rank, doc in enumerate(ranking, start=1):\n'
        '        scores[doc] = scores.get(doc, 0) + 1 / (k + rank)\n'
        'print(sorted(scores, key=scores.get, reverse=True))',
        ["['d1', 'd3', 'd2', 'd4']", "['d3', 'd1', 'd2', 'd4']", "['d1', 'd2', 'd3', 'd4']", "['d1', 'd3', 'd4', 'd2']"], 0,
        "d1 is ranks 1 and 2; d3 is ranks 3 and 1.",
        "RRF: d1 = 1/61 + 1/62, d3 = 1/63 + 1/61, so d1 edges out d3. Docs found by both lists beat docs found by one.",
        topic="hybrid", level=3),
    out('bm25 = {"d1": 12.0, "d2": 9.5}      # unbounded keyword scores\n'
        'cosine = {"d1": 0.31, "d2": 0.89}   # 0..1 similarity\n'
        'combined = {d: bm25[d] + cosine[d] for d in bm25}\nprint(max(combined, key=combined.get))',
        ["d1", "d2", "KeyError", "d1 d2"], 0,
        "Compare the size of the two scores.",
        "BM25 scores are on a much larger scale, so a plain sum is just BM25 ranking; d2's far better semantic match is ignored. Use RRF (ranks) or normalise scores.",
        topic="hybrid", level=3),
    out('docs = [("d1", "hr", 0.95), ("d2", "eng", 0.93), ("d3", "eng", 0.90),\n'
        '        ("d4", "hr", 0.60), ("d5", "hr", 0.55)]\nk = 3\n'
        'ranked = sorted(docs, key=lambda d: -d[2])\n'
        'post = [d[0] for d in ranked[:k] if d[1] == "hr"]\n'
        'pre = [d[0] for d in ranked if d[1] == "hr"][:k]\nprint(post, pre)',
        ["['d1'] ['d1', 'd4', 'd5']", "['d1', 'd4', 'd5'] ['d1']", "['d1', 'd4', 'd5'] ['d1', 'd4', 'd5']", "['d1'] ['d1']"], 0,
        "Post-filter cuts to top-k first, then removes non-HR.",
        "Post-filtering returns 1 result instead of 3 (and zero for a small tenant). Filter before/during the vector search so you still get k matches.",
        topic="filtering-security", level=3),
    tf("It's acceptable to index all departments' documents together and add \"Do not reveal HR documents to non-HR employees\" to the system prompt.", False,
       "Would you secure a database with a comment in the query?",
       "Access control must happen in retrieval (ACL filters, separate indexes). Anything placed in the prompt can be leaked via injection or simple model error.",
       topic="filtering-security", level=3,
       analogy="Like returning every row and asking the frontend to hide the ones the user can't see."),
    mcq("You retrieve 50 candidates and rerank them with a cross-encoder. Each pair takes ~4 ms on your GPU (batched together ~60 ms). P95 latency budget for retrieval is 150 ms. What's a sensible design?",
        ["Retrieve ~50 with ANN, rerank all 50 in one batch, keep the top 5 for the prompt",
         "Rerank the entire corpus with the cross-encoder",
         "Skip retrieval and use only the cross-encoder",
         "Rerank only the top 1"], 0,
        "Fast wide net, slow precise filter.",
        "Two-stage retrieval: cheap ANN recall over millions, expensive cross-encoder precision over tens. Tune the candidate count against recall and latency.",
        topic="rerank", level=3),
    mcq("What is HyDE (Hypothetical Document Embeddings)?",
        ["Have the LLM write a hypothetical answer to the question, embed that, and search with it",
         "Hide document embeddings from users",
         "Embed documents at lower precision",
         "A reranker model"], 0,
        "Answers look more like documents than questions do.",
        "A short question and a long document chunk are phrased differently. A fake answer is phrased like a document, so its embedding often lands nearer the real one.",
        topic="query-transform", level=3),
    out('chunks = [("c1", 300), ("c2", 500), ("c3", 250), ("c4", 400)]  # ranked, (id, tokens)\n'
        'budget = 800\npicked, used = [], 0\nfor cid, toks in chunks:\n'
        '    if used + toks <= budget:\n        picked.append(cid); used += toks\nprint(picked, used)',
        ["['c1', 'c2'] 800", "['c1', 'c3'] 550", "['c1', 'c2', 'c3'] 1050", "['c1'] 300"], 0,
        "c1 + c2 fills the budget exactly.",
        "Greedy packing in rank order: 300 + 500 = 800 fits; c3 and c4 would exceed. Reserve budget for instructions and the answer too.",
        topic="context-citations", level=3),
    mcq("How do you make citations reliable in a RAG answer?",
        ["Label each chunk with an id in the prompt (e.g. [doc3#p2]), ask the model to cite ids, and check in code that cited ids were actually provided",
         "Ask the model to recall the URL of its source from memory",
         "Add 'cite your sources' and trust the output",
         "Put citations in the system prompt"], 0,
        "The model can only cite what it was shown, if you can verify it.",
        "Ids in the context make citations checkable: drop or flag answers citing ids that weren't in the prompt.",
        topic="context-citations", level=3),
    out('results = [["d3", "d1", "d2"], ["d5", "d6", "d4"], ["d9", "d8", "d7"]]\ngold = ["d1", "d4", "d0"]\n'
        'rr = [1 / (r.index(g) + 1) if g in r else 0.0 for r, g in zip(results, gold)]\n'
        'print(round(sum(rr) / len(rr), 3))',
        ["0.278", "0.417", "0.833", "0.333"], 0,
        "Reciprocal ranks: 1/2, 1/3 and 0.",
        "MRR = mean of 1/rank of the first relevant hit = (0.5 + 0.333 + 0) / 3 = 0.278. Misses count as 0.",
        topic="rag-eval", level=3),
    out('retrieved = ["d1", "d5", "d2", "d6", "d7"]\nrelevant = {"d1", "d2", "d3"}\nk = 5\n'
        'hits = sum(d in relevant for d in retrieved[:k])\n'
        'print(round(hits / len(relevant), 2), round(hits / k, 2))',
        ["0.67 0.4", "0.4 0.67", "0.67 0.67", "1.0 0.4"], 0,
        "recall divides by relevant docs, precision by k.",
        "2 hits: recall@5 = 2/3 = 0.67, precision@5 = 2/5 = 0.4. Raising k usually raises recall and lowers precision.",
        topic="rag-eval", level=3),
    mcq("An answer is fully supported by the retrieved chunks but doesn't address what the user asked. Which metric catches it?",
        ["Answer relevance (it scores high on faithfulness)",
         "Faithfulness",
         "recall@k",
         "Embedding cosine similarity"], 0,
        "Grounded and on-topic are different properties.",
        "Faithfulness checks claims vs context; answer relevance checks answer vs question. RAGAS-style evals score both, plus context precision/recall.",
        topic="rag-eval", level=3),
    mcq("The index has both the 2024 and 2026 versions of the travel policy. The bot answers with a mix of both. Best fix?",
        ["Store version/effective dates in metadata, filter or prefer the latest, and retire superseded documents from the index",
         "Raise the temperature",
         "Increase chunk size",
         "Tell users to ask about 2026 explicitly"], 0,
        "The retriever can't tell old from new by meaning alone.",
        "Conflicting versions look equally relevant. Version metadata plus dedup/retirement in ingestion resolves conflicts before the LLM sees them.",
        topic="failure-modes", level=3),
    mcq("When does agentic (iterative) RAG beat a single retrieve-then-answer pass?",
        ["Multi-hop questions, e.g. \"Which team owns the service that caused last week's outage?\" needs one lookup to feed the next",
         "Simple FAQ questions",
         "Whenever latency must be under 200 ms",
         "When the corpus is tiny"], 0,
        "Does the second search depend on the first result?",
        "An agent can search, read, and decide a follow-up query. It costs more calls and latency, so use it only when single-shot retrieval can't answer.",
        topic="advanced-rag", level=3),

    # ------------------------------------------------------------------ L4
    mcq("Small chunks retrieve precisely but give the LLM too little context. What does \"small-to-big\" (parent-child) retrieval do?",
        ["Search over small child chunks, then send the larger parent section they belong to into the prompt",
         "Start with big chunks and split them at query time",
         "Use a small embedding model, then a big LLM",
         "Retrieve small chunks first and big chunks only if nothing is found"], 0,
        "Match on the sentence, read the section.",
        "Decouple the unit you search from the unit you read: precise matching on child chunks, coherent context from parents (dedup parents that share children).",
        topic="chunking", level=4),
    mcq("Some embedding models expect a prefix like `query: ...` for searches and `passage: ...` for documents. You embed everything without prefixes. What is the likely effect?",
        ["Silently worse retrieval: the model was trained on asymmetric inputs, so unprefixed vectors sit in a slightly wrong region",
         "An error from the model",
         "No effect; prefixes are cosmetic",
         "Better retrieval, since prefixes add noise"], 0,
        "Training-time format vs inference-time format.",
        "Asymmetric models learn different roles for short queries and long passages. Missing prefixes don't crash, they just lower recall; read the model card and test.",
        topic="embeddings", level=4),
    out('n, dim = 1_000_000, 1024\nfp32_bytes = n * dim * 4\nbinary_bytes = n * dim // 8\n'
        'print(fp32_bytes / 1e9, binary_bytes / 1e6, fp32_bytes // binary_bytes)',
        ["4.096 128.0 32", "4.096 512.0 8", "1.024 128.0 8", "4.096 128.0 4"], 0,
        "Binary quantisation keeps 1 bit per dimension.",
        "fp32 = 32 bits per dim, binary = 1 bit: 32x smaller (4.1 GB -> 128 MB). Recall drops, so systems often search binary, then rescore the top candidates with full vectors.",
        topic="embeddings", level=4),
    mcq("How do you measure whether your ANN index settings are costing you retrieval quality?",
        ["Run the same queries through exact brute-force search and compute the ANN's recall@k against those exact neighbours",
         "Check that the vector DB reports no errors",
         "Compare query latency only",
         "Ask the LLM if the results look good"], 0,
        "You need a ground truth for 'nearest'.",
        "ANN recall is measured against exact kNN on a sample of queries. That isolates index loss from embedding-model loss.",
        topic="vector-index", level=4),
    mcq("In RRF, score = sum of 1 / (k + rank). What happens if you lower k from 60 to 1?",
        ["Top ranks dominate much more: rank 1 vs rank 2 becomes 1/2 vs 1/3 instead of nearly equal",
         "Nothing; k cancels out",
         "Lower-ranked documents gain more weight",
         "Scores become negative"], 0,
        "Compare 1/61 vs 1/62 with 1/2 vs 1/3.",
        "A large k flattens differences between ranks (fusion rewards appearing in many lists); a small k rewards being first in any one list.",
        topic="hybrid", level=4),
    mcq("A user's access to a confidential project is revoked. A day later they still get answers quoting its docs. The vector DB filters on an `allowed_users` list copied into each chunk at ingestion. What is the root cause?",
        ["ACLs were snapshotted at ingestion and never updated; permissions should be resolved at query time (or re-synced on change)",
         "The embedding model memorised the documents",
         "The LLM is fine-tuned on the project docs",
         "Cosine similarity ignores metadata"], 0,
        "Where is the source of truth for permissions?",
        "Copied ACLs go stale. Filter by group ids resolved live from the identity system, propagate ACL changes, and test revocation as a security case.",
        topic="filtering-security", level=4),
    mcq("You serve 2,000 tenants, most with a few hundred chunks. Shared index with a tenant filter, or one index per tenant?",
        ["Shared index with a pre-filter or namespace is cheaper to run, but filtered ANN on tiny tenants can hurt recall; separate namespaces give stronger isolation. Choose based on isolation needs and test small-tenant recall",
         "Always one index per tenant, it's free",
         "Always shared with post-filtering",
         "Tenancy doesn't matter in vector search"], 0,
        "Isolation, cost and filtered-search recall pull in different directions.",
        "Thousands of tiny indexes are an ops burden; a shared index risks leaks if a filter is missed and can degrade HNSW recall under very selective filters.",
        topic="filtering-security", level=4),
    mcq("Why can't a cross-encoder reranker's work be precomputed at indexing time the way embeddings are?",
        ["Its score depends on the query and document together, so it must run once per (query, doc) pair at query time",
         "Cross-encoders are too large to store",
         "Precomputing is possible but forbidden by licences",
         "Cross-encoders don't output numbers"], 0,
        "What does the model take as input?",
        "Joint attention across query and document is why it's accurate and also why it's expensive: no per-document vector exists to cache.",
        topic="rerank", level=4),
    mcq("HyDE improved retrieval for general questions but made it worse for questions about your company's internal product codenames. Why?",
        ["The LLM knows nothing about the codenames, so its hypothetical answer is confidently wrong and pulls retrieval toward the wrong documents",
         "HyDE only works in English",
         "The codenames are too short to embed",
         "HyDE requires a reranker"], 0,
        "HyDE's fake answer is only as good as the model's prior knowledge.",
        "HyDE helps when the model can guess the shape of the answer. On private or niche topics, combine it with the raw query (or skip it) and measure.",
        topic="query-transform", level=4),
    mcq("Your eval set was generated by asking an LLM to write one question per chunk. Retrieval scores recall@5 = 0.97, but real users are unhappy. What's the likely flaw?",
        ["Synthetic questions reuse the chunk's own wording and target one chunk each, so they're far easier than real, vague, multi-chunk user questions",
         "recall@5 is the wrong formula",
         "The LLM that wrote the questions is too small",
         "0.97 is too high to be possible"], 0,
        "Who wrote the questions, and from what?",
        "Synthetic sets overstate quality via lexical overlap. Mix in real user queries (from logs), multi-hop and unanswerable questions, and label them.",
        topic="rag-eval", level=4),
    mcq("A question has 3 relevant chunks, and you evaluate recall@2. What is the best possible score, and why does it matter?",
        ["0.67: with k=2 you can't fetch all 3, so k must be at least the number of chunks an answer needs",
         "1.0, recall is always reachable",
         "0.5, because k=2",
         "0.33, only one chunk counts"], 0,
        "Two slots, three needed items.",
        "Recall@k is capped at k / relevant. If answers need several chunks, a small k guarantees incomplete context no matter how good the retriever is.",
        topic="rag-eval", level=4),
    mcq("Retrieval logs show the correct chunk ranked #1 for a question, yet the answer is wrong. Where do you look next?",
        ["Generation: context packing (was it truncated or buried?), the prompt's grounding instructions, and whether the model contradicted the chunk",
         "Re-embed the corpus with a new model",
         "Increase k to 50",
         "Switch to BM25"], 0,
        "Retrieval did its job.",
        "Localise the fault: if retrieval succeeded, the bug is downstream: truncation, ordering, conflicting chunks, or the model ignoring context. Measure faithfulness.",
        topic="failure-modes", level=4,
        diagram="""
 index has it? -> retrieved top-k? -> survived rerank?
      -> in final prompt? -> model used it? -> answer
 (find the first 'no'; that's the stage to fix)
"""),
    mcq("A user asks: \"What are the main themes across all 10,000 customer interviews?\" Why does standard top-k RAG do poorly, and what helps?",
        ["It's a global question: no top-5 chunks contain the answer. GraphRAG-style approaches (entity graph + community summaries) or map-reduce summarisation fit better",
         "Increase k to 10,000",
         "Use a bigger embedding model",
         "Lower the temperature"], 0,
        "Is the answer in any single chunk?",
        "Top-k RAG answers local questions. Corpus-wide questions need pre-built structure (graphs, cluster summaries) or summarising everything, at much higher indexing cost.",
        topic="advanced-rag", level=4),
    mcq("Your RAG endpoint's P95 latency is 4 s: query rewrite LLM call 0.8 s, retrieval 0.1 s, rerank 0.2 s, generation 2.9 s. Which change cuts latency most without hurting quality much?",
        ["Stream the answer tokens and cap/shorten output; consider skipping the rewrite call for first-turn (standalone) questions",
         "Remove the reranker",
         "Switch to a faster vector DB",
         "Retrieve fewer chunks (k=3 instead of 5)"], 0,
        "Where is the time actually spent?",
        "Generation and extra LLM calls dominate; retrieval is rarely the bottleneck. Streaming improves time-to-first-token; conditional rewrites remove a whole LLM round trip.",
        topic="advanced-rag", level=4),

    # ------------------------------------------------------------------ Round 2: L1
    mcq("In a RAG system, what does \"re-indexing\" a document mean?",
        ["Re-chunking and re-embedding it and replacing its old entries in the index",
         "Retraining the LLM on it",
         "Renaming the file",
         "Sorting the index alphabetically"], 0,
        "The index is a derived copy of your documents.",
        "When a source document changes, its chunks and vectors must be rebuilt and the old ones removed, or the bot keeps quoting "
        "the old text. No model weights change.",
        topic="freshness", level=1),
    tf("TF-IDF gives a word more weight when it appears in fewer documents in the corpus.", True,
       "IDF = inverse document frequency.",
       "Words like 'the' appear everywhere and tell you nothing; a rare word like 'chargeback' is a strong signal. IDF scales a "
       "term's weight up as the number of documents containing it goes down.",
       topic="sparse-retrieval", level=1),
    fill("The number of results you ask the retriever to return (e.g. the best 5 chunks) is written top-____.",
         "k",
         "A single letter, also used in kNN.",
         "top-k: the k highest-scoring chunks. k too small misses needed facts; k too large adds noise and tokens.",
         topic="vector-index", level=1),
    mcq("What is chunk overlap?",
        ["Repeating the last few tokens of one chunk at the start of the next, so text on a boundary isn't cut off from its context",
         "Storing the same chunk in two indexes",
         "Two documents that cover the same topic",
         "Chunks that are longer than the context window"], 0,
        "Think about a sentence that straddles the cut.",
        "Without overlap a sentence split across two chunks is half-meaningful in both. A small overlap (often 10-20%) keeps it "
        "whole in at least one chunk, at the cost of a few more chunks.",
        topic="chunking", level=1,
        diagram="""
 text:    [..........................................]
 chunk 1: [==============]
 chunk 2:             [==============]
 chunk 3:                         [==============]
                      ^^^ overlap  ^^^
"""),
    tf("Two sentences with no words in common can still get a high cosine similarity between their embeddings.", True,
       "\"How do I get my money back?\" vs \"refund process\".",
       "Embeddings capture meaning, not shared words, which is exactly what keyword search can't do. The flip side: they can blur "
       "exact tokens like error codes.",
       topic="embeddings", level=1),
    mcq("In RAG, where do the retrieved chunks go?",
        ["Into the prompt, next to the instructions and the user's question",
         "Into the model's weights",
         "Into the user's browser cache",
         "Into a separate model that answers instead of the LLM"], 0,
        "The model can only use what it reads in this call.",
        "Retrieval just fetches text; the LLM sees it as part of the prompt and answers from it. That's why context size, ordering "
        "and labelling matter.",
        topic="context-citations", level=1),
    out('docs = {"d1": "reset your password", "d2": "refund your order", "d3": "password rules"}\n'
        'q = set("forgot password".split())\nscores = {d: len(q & set(t.split())) for d, t in docs.items()}\nprint(scores)',
        ["{'d1': 1, 'd2': 0, 'd3': 1}", "{'d1': 2, 'd2': 0, 'd3': 1}", "{'d1': 1, 'd2': 1, 'd3': 1}", "{'d1': 0, 'd2': 0, 'd3': 1}"], 0,
        "& is set intersection: shared words.",
        "Only 'password' is shared with d1 and d3. This is the crudest keyword search; TF-IDF and BM25 add weighting so rare words "
        "count more and long documents don't win by size.",
        topic="sparse-retrieval", level=1),
    mcq("What is hybrid search?",
        ["Running keyword (BM25) and vector (dense) search together and merging their results",
         "Searching two vector databases",
         "Using a GPU and a CPU at the same time",
         "Letting the LLM search the web"], 0,
        "Two kinds of retrievers, one result list.",
        "Keyword search nails exact terms (codes, names); dense search finds paraphrases. Merging both, usually with RRF, beats "
        "either alone on most real corpora.",
        topic="hybrid", level=1),
    fill("The fraction of the relevant documents that show up in the top k results is called ____@k.",
         "recall",
         "Did we recall everything we needed?",
         "recall@k = relevant found in top k / all relevant. If the needed chunk isn't retrieved, no prompt can save the answer.",
         topic="rag-eval", level=1),
    mcq("A user asks something your documents don't cover at all. What should a well-built RAG bot do?",
        ["Say it couldn't find the answer in the sources (and offer a hand-off), rather than guess",
         "Make up a plausible answer",
         "Return the closest chunk as if it were the answer",
         "Crash, so the developer notices"], 0,
        "Retrieval always returns something, even if it's irrelevant.",
        "Top-k always returns k chunks, related or not. The prompt (and ideally a relevance threshold) must allow 'I don't know'; "
        "a confident answer from unrelated chunks is worse than none.",
        topic="failure-modes", level=1),

    # ------------------------------------------------------------------ Round 2: L2
    out('from sklearn.feature_extraction.text import TfidfVectorizer\n'
        'from sklearn.metrics.pairwise import cosine_similarity\n'
        'docs = ["refund takes five days", "reset password via email", "refund needs a receipt"]\n'
        'vec = TfidfVectorizer()\nX = vec.fit_transform(docs)\nq = vec.transform(["how to reset my password"])\n'
        'print(int(cosine_similarity(q, X).argmax()))',
        ["1", "0", "2", "3"], 0,
        "Which document shares the query's words?",
        "Only doc 1 contains 'reset' and 'password'; 'how', 'to', 'my' aren't in the vocabulary and are dropped. Fit the vectoriser on "
        "the corpus, transform the query with the same vectoriser: the same rule as one embedding model for both sides.",
        topic="sparse-retrieval", level=2),
    out('import math\ndocs = [{"refund", "policy"}, {"refund", "days"}, {"password", "reset"}]\nN = len(docs)\n'
        'for term in ("refund", "password"):\n    df = sum(term in d for d in docs)\n    print(term, round(math.log(N / df), 3))',
        ["refund 0.405\npassword 1.099", "refund 1.099\npassword 0.405", "refund 2\npassword 1", "refund 0.667\npassword 0.333"], 0,
        "df = number of documents containing the term; idf = log(N / df).",
        "'refund' is in 2 of 3 docs: log(1.5) = 0.405. 'password' is in 1 of 3: log(3) = 1.099. The rarer term carries more weight. "
        "BM25 uses a smoothed version of the same idea.",
        topic="sparse-retrieval", level=2),
    mcq("The query is \"car insurance\" and a document talks only about \"automobile cover\". Why does TF-IDF score it zero?",
        ["TF-IDF only matches exact terms; it has no idea that car and automobile mean the same thing",
         "The document is too short",
         "TF-IDF ignores nouns",
         "Its IDF weights are negative"], 0,
        "What does a sparse vector have one slot for?",
        "Sparse methods have one dimension per word, so synonyms are different dimensions with zero overlap: the vocabulary mismatch "
        "problem. Dense embeddings fix it, which is why hybrid search uses both.",
        topic="sparse-retrieval", level=2,
        analogy="Like a SQL LIKE '%car%' search: it will never return a row that only says automobile."),
    mcq("A \"recursive\" text splitter tries separators in order: paragraph breaks, then line breaks, then sentences, then words. Why that order?",
        ["It keeps the largest natural units that still fit the size limit, and only cuts finer when it has to",
         "It is the fastest order to compute",
         "Embedding models require it",
         "It guarantees every chunk is exactly the same size"], 0,
        "Prefer cutting between paragraphs over cutting mid-sentence.",
        "Splitting on the coarsest boundary first keeps ideas whole; a mid-sentence cut only happens for a giant paragraph. Chunk "
        "sizes vary, which is fine: coherent beats uniform.",
        topic="chunking", level=2),
    out('text = "Refunds take 5 days. Keep the receipt. Electronics have 15 days. Sale items are final."\n'
        'sents = [s.strip() + "." for s in text.split(".") if s.strip()]\nchunks, cur = [], ""\nfor s in sents:\n'
        '    if cur and len(cur) + 1 + len(s) > 40:\n        chunks.append(cur); cur = s\n'
        '    else:\n        cur = (cur + " " + s).strip()\nchunks.append(cur)\nprint(len(chunks), chunks[0])',
        ["3 Refunds take 5 days. Keep the receipt.", "4 Refunds take 5 days.", "2 Refunds take 5 days. Keep the receipt.",
         "3 Refunds take 5 days."], 0,
        "Sentence lengths: 20, 17, 25, 21. The cap is 40 characters.",
        "20 + 1 + 17 = 38 fits; adding 25 would not, so the third sentence starts chunk 2, and 25 + 1 + 21 > 40 starts chunk 3. "
        "Packing whole sentences never cuts one in half. Real chunkers count tokens and handle 'e.g.' and '3.5'.",
        topic="chunking", level=2),
    tf("If all stored vectors and the query vector are L2-normalised, ranking by dot product gives the same order as ranking by cosine similarity.", True,
       "cos(a, b) = a.b / (|a| |b|).",
       "With |a| = |b| = 1 the denominator is 1, so dot = cosine. That's why indexes normalise once at write time and then use the "
       "cheaper inner product.",
       topic="embeddings", level=2),
    mcq("Your reranker scores the top candidates: 0.92, 0.88, 0.15, 0.07, 0.03. What should go into the prompt?",
        ["The high-scoring ones; drop chunks below a relevance threshold tuned on your eval set (and say 'I don't know' if none pass)",
         "Always exactly 5, whatever the scores",
         "Only the lowest-scoring ones, for diversity",
         "All candidates, since the LLM will sort it out"], 0,
        "Do 0.07-relevance chunks help the model?",
        "A fixed k pads the context with junk when only two chunks are relevant, and junk invites wrong answers. A score floor plus "
        "a max k adapts to each query.",
        topic="rerank", level=2),
    mcq("A user asks: \"Compare the refund rules for the Basic and Pro plans.\" Why can a single retrieval pass do poorly, and what helps?",
        ["One embedding mixes both topics, so the top-k may favour one plan; split it into sub-queries (Basic refunds, Pro refunds) and retrieve for each",
         "Comparisons can't be answered with RAG",
         "Use a longer query",
         "Raise the LLM temperature"], 0,
        "The answer needs two different chunks.",
        "Query decomposition turns a multi-part question into focused searches, so each part gets its own top-k. Merge the results "
        "(with dedup) before generation.",
        topic="query-transform", level=2),
    tf("Metadata filters such as `year >= 2025` can be applied by the vector database during the similarity search, not only on the results afterwards.", True,
       "Think of a WHERE clause the engine uses while it searches.",
       "Most vector DBs support filtered search: only matching vectors are candidates, so you still get k results. Filtering the "
       "top-k afterwards can leave you with few or none.",
       topic="filtering-security", level=2),
    out('chunks = [("kb12", "Refunds take 5 days."), ("kb40", "Keep your receipt.")]\n'
        'context = "\\n".join(f"[{cid}] {text}" for cid, text in chunks)\n'
        'prompt = f"Answer only from the sources below. Cite ids.\\n{context}\\nQ: How long do refunds take?"\n'
        'print(prompt.splitlines()[1])',
        ["[kb12] Refunds take 5 days.", "Answer only from the sources below. Cite ids.", "[kb40] Keep your receipt.", "Q: How long do refunds take?"], 0,
        "Line 0 is the instruction.",
        "Each chunk gets its id inline, so the model can cite [kb12] and your code can check the citation against the ids it sent. "
        "Without ids, 'citations' are free text you can't verify.",
        topic="context-citations", level=2),
    out('results = {"q1": ["d3", "d1"], "q2": ["d5", "d6"], "q3": ["d2", "d9"]}\n'
        'gold = {"q1": "d1", "q2": "d4", "q3": "d2"}\nhits = [gold[q] in r for q, r in results.items()]\n'
        'print(sum(hits), round(sum(hits) / len(hits), 2))',
        ["2 0.67", "1 0.33", "3 1.0", "2 0.5"], 0,
        "Is each query's gold doc anywhere in its top 2?",
        "q1 and q3 found their gold doc, q2 didn't: hit rate@2 = 2/3. Hit rate ignores the position inside the top k; MRR rewards "
        "ranking it first.",
        topic="rag-eval", level=2),
    mcq("A page is deleted from the wiki. What must the indexing pipeline also do?",
        ["Delete that page's chunks from the index, or the bot keeps citing a page that no longer exists",
         "Nothing; the vector DB notices on its own",
         "Re-train the embedding model",
         "Lower the page's similarity scores"], 0,
        "The index is a copy, and copies don't hear about deletes.",
        "Pipelines that only handle 'new' and 'changed' leak ghost content forever. Track source ids per chunk and sync deletions; "
        "for compliance (e.g. a right-to-erasure request) this is mandatory.",
        topic="freshness", level=2),
    mcq("Many of your PDFs are scanned images. After ingestion, questions about them never retrieve anything. Most likely cause?",
        ["The parser extracted no text (there's no text layer), so empty or junk chunks were indexed; you need OCR",
         "Scanned PDFs are too large to embed",
         "The embedding model can't read English",
         "The LLM refuses PDFs"], 0,
        "What does a text extractor find in a photo of a page?",
        "No text layer means empty strings. Add checks at ingestion: chunk counts per doc, empty-text alerts, sample reviews. "
        "Silent ingestion failures look like 'retrieval is bad'.",
        topic="failure-modes", level=2),
    mcq("You need the bot to (a) write in your brand's tone and (b) quote this week's prices. Which tools fit?",
        ["Tone: prompt instructions or fine-tuning. Prices: RAG (or a live tool), since they change weekly and must be exact",
         "Fine-tune weekly on the price list",
         "RAG for the tone, fine-tuning for the prices",
         "Neither; put both in a longer system prompt once"], 0,
        "Behaviour vs facts that change.",
        "Fine-tuning shapes style and format but bakes facts in at training time and can't cite them. Fresh, exact facts belong in "
        "retrieval or an API call made at question time.",
        topic="why-rag", level=2),
    fill("A reranker that reads the query and a document together in one forward pass and outputs a relevance score is called a ____-encoder.",
         "cross",
         "As opposed to bi-encoder.",
         "Cross-encoders let query and document tokens attend to each other, which makes them more accurate but impossible to "
         "precompute per document.",
         topic="rerank", level=2),
    fill("The mean over queries of 1 / (rank of the first relevant result) is the metric called ____ (three-letter abbreviation).",
         "MRR",
         "Mean Reciprocal ...",
         "Mean Reciprocal Rank: 1.0 if the first hit is always at rank 1, 0.5 if at rank 2. It suits tasks where one good chunk is "
         "enough; recall@k suits answers that need several.",
         topic="rag-eval", level=2),

    # ------------------------------------------------------------------ Round 2: L3
    out('import math\nN, df = 1000, 10            # docs in corpus, docs containing the term\n'
        'tf, dl, avgdl = 3, 100, 100  # term count in this doc, doc length, average length\nk1, b = 1.2, 0.75\n'
        'idf = math.log((N - df + 0.5) / (df + 0.5) + 1)\n'
        'score = idf * tf * (k1 + 1) / (tf + k1 * (1 - b + b * dl / avgdl))\nprint(round(idf, 2), round(score, 2))',
        ["4.56 7.16", "4.61 13.68", "4.56 13.68", "2.0 7.16"], 0,
        "With dl = avgdl the length term is 1, so the tf part is 3 * 2.2 / (3 + 1.2).",
        "idf = ln(990.5 / 10.5 + 1) = 4.56; the tf part is 6.6 / 4.2 = 1.57, so 7.16. Not 3 x idf: BM25 grows with term frequency "
        "but saturates. A document's score is this summed over the query terms.",
        topic="sparse-retrieval", level=3),
    out('k1 = 1.2\nfor tf in (1, 2, 10, 100):\n    print(tf, round(tf * (k1 + 1) / (tf + k1), 2))',
        ["1 1.0\n2 1.38\n10 1.96\n100 2.17", "1 1.0\n2 2.0\n10 10.0\n100 100.0", "1 2.2\n2 4.4\n10 22.0\n100 220.0", "1 1.0\n2 1.38\n10 2.2\n100 2.2"], 0,
        "As tf grows, the fraction approaches k1 + 1.",
        "BM25's term-frequency part saturates toward k1 + 1 = 2.2: the 2nd mention adds a lot, the 100th almost nothing. So keyword "
        "stuffing barely helps, unlike raw TF-IDF, where the score grows linearly with counts.",
        topic="sparse-retrieval", level=3,
        diagram="""
 tf part
 2.2 |            .  .  .  .  .   (ceiling = k1 + 1)
     |      .  '
 1.0 |  .'
     +-------------------------> term count
       1  2     10           100
"""),
    mcq("In BM25, what does the parameter `b` (usually 0.75) control?",
        ["Document-length normalisation: b = 1 fully penalises long documents, b = 0 ignores length",
         "The weight given to rare terms",
         "How many results are returned",
         "The term-frequency saturation point"], 0,
        "A long document mentions everything a few times.",
        "Long docs contain more words, so they match more terms by chance; b scales tf by dl / avgdl to compensate. Saturation is "
        "k1's job. Lower b for corpora where long docs really are richer (e.g. full manuals).",
        topic="sparse-retrieval", level=3,
        diagram="""
 effective tf = tf / (1 - b + b * dl/avgdl)
 b = 0    : length ignored
 b = 0.75 : a doc 4x the average length counts tf at ~1/3.25
 b = 1    : fully proportional to length
"""),
    tf("In BM25, a term that appears 100 times in a document scores about 100 times more than a term that appears once.", False,
       "Look at the k1 + 1 ceiling.",
       "Term frequency saturates: with k1 = 1.2, 100 mentions score about 2.2x one mention, not 100x. This is a deliberate guard "
       "against long, repetitive or keyword-stuffed pages.",
       topic="sparse-retrieval", level=3),
    out('from sklearn.feature_extraction.text import TfidfVectorizer\n'
        'vec = TfidfVectorizer().fit(["refund policy", "shipping policy"])\n'
        'q = vec.transform(["reimbursement rules"])\nprint(q.nnz)',
        ["0", "2", "1", "KeyError"], 0,
        "nnz = number of non-zero entries. Are the query words in the fitted vocabulary?",
        "Neither 'reimbursement' nor 'rules' was seen at fit time, so the query vector is all zeros and every similarity is 0, with "
        "no error. Out-of-vocabulary queries silently return nothing (or arbitrary ties), so log zero-score queries.",
        topic="sparse-retrieval", level=3),
    fill("A 10,000-token document is chunked with size 512 and overlap 64 (`range(0, 10000, 512 - 64)`). The number of chunks is ____.",
         "23",
         "The step is 448; count the start positions below 10,000.",
         "ceil(10000 / 448) = 23 starts, and the last chunk holds only 144 tokens. Overlap costs ~14% more chunks than no overlap "
         "(20): more vectors, more storage, more near-duplicate hits.",
         topic="chunking", level=3),
    mcq("A chunk from ACME's Q3 report reads: \"It increased 12% over the prior quarter.\" The query \"ACME Q3 revenue growth\" never retrieves it. Best fix?",
        ["Prepend context to each chunk before embedding, e.g. document title, company, period and section heading (\"ACME Q3 2026 report > Revenue\")",
         "Use smaller chunks",
         "Raise k to 100",
         "Switch to a bigger LLM"], 0,
        "What does the chunk itself not say?",
        "Pronouns and implied subjects make chunks meaningless out of context. Contextual chunk headers (or an LLM-written one-line "
        "context per chunk) put the missing entities into both the embedding and the BM25 text.",
        topic="chunking", level=3),
    mcq("Your embedding model's max input is 512 tokens, but your chunks are 1,500 tokens. What happens?",
        ["Usually the text is silently truncated: only the first ~512 tokens are embedded, so facts in the rest can never be found",
         "The model raises an error on every chunk",
         "The model compresses the whole chunk into the vector",
         "The vector becomes three times longer"], 0,
        "Many libraries truncate by default.",
        "Truncation is silent, so two-thirds of each chunk is invisible to search while still being sent to the LLM. Match chunk size "
        "to the embedder's limit, and check the model card.",
        topic="embeddings", level=3,
        diagram="""
 chunk:  [=====512 embedded=====][~~~~~~988 ignored~~~~~~]
 vector: only knows the first part
"""),
    tf("Cosine similarity scores from an embedding model are calibrated probabilities, so 0.8 means an 80% chance the chunk is relevant.", False,
       "Would the same 0.8 mean the same thing under a different model?",
       "Similarity scales are model-specific: one model's 'relevant' band is 0.8+, another's is 0.3+. Any threshold must be tuned on "
       "your labelled queries, and re-tuned when you change the model.",
       topic="embeddings", level=3),
    mcq("An IVF index clusters 10M vectors into 4,096 cells. With `nprobe = 1`, recall is poor. Why, and what is the knob?",
        ["Only the single closest cell is searched, so true neighbours just across a cell boundary are missed; raise nprobe (more cells, slower)",
         "The clusters are too small; reduce them to 4",
         "IVF can't search more than one cell",
         "nprobe controls vector precision"], 0,
        "The query sits near the edge of its cell.",
        "IVF trades recall for speed by searching a few cells. nprobe is its ef-like knob: scan more cells to recover neighbours near "
        "boundaries. Tune it against exact search on sample queries.",
        topic="vector-index", level=3,
        diagram="""
  cell A        | cell B
     x  x   q   |  *  x       q = query, * = true nearest
     x      x   |     x       nprobe=1 scans A only -> misses *
"""),
    out('import numpy as np\nrng = np.random.default_rng(0)\nD = rng.normal(size=(1000, 8))\n'
        'D /= np.linalg.norm(D, axis=1, keepdims=True)\nq = D[42] + 0.01\nscores = D @ (q / np.linalg.norm(q))\n'
        'top = np.argpartition(-scores, 3)[:3]      # 3 best, in no particular order\n'
        'top = top[np.argsort(-scores[top])]        # sort just those 3\nprint(int(top[0]), len(top))',
        ["42 3", "0 3", "42 1000", "3 42"], 0,
        "q is a tiny nudge away from row 42.",
        "argpartition finds the top 3 in O(n) without sorting all 1,000; sorting only those 3 gives the ranked top-k. Row 42 is the "
        "best match. This is brute-force exact search: for a corpus this size it beats running an ANN service.",
        topic="vector-index", level=3),
    mcq("You add a strong cross-encoder reranker, but answers barely improve. Logs show the right chunk is in the first stage's top 50 only 60% of the time. What do you fix?",
        ["The first stage (hybrid search, better embeddings or chunking, more candidates): a reranker can only reorder what it is given",
         "Use a bigger reranker",
         "Rerank only the top 5",
         "Lower the LLM temperature"], 0,
        "Can a reranker find a chunk that wasn't retrieved?",
        "Reranking raises precision at the top, but recall is capped by stage one. Measure recall@50 of the candidates before "
        "spending on rerankers.",
        topic="rerank", level=3,
        analogy="A great interviewer can't hire someone the CV filter already rejected.",
        diagram="""
 corpus 1M --[stage 1: ANN/BM25]--> top 50  (recall@50 = 0.6)
 top 50 --[stage 2: reranker]--> top 5
 missing from the 50? stage 2 never sees it
"""),
    tf("A reranker can raise recall@5 of the final context, but it cannot raise recall@50 of the candidate set it was given.", True,
       "Reordering moves items inside the list; it can't add new ones.",
       "Pushing relevant candidates from rank 30 into the top 5 raises recall@5. The set of 50 is fixed, so recall@50 doesn't move. "
       "That's why you track both.",
       topic="rerank", level=3),
    out('ranked = ["c1", "c2", "c3", "c4", "c5"]   # best first\nfront, back = ranked[0::2], ranked[1::2]\nprint(front + back[::-1])',
        ["['c1', 'c3', 'c5', 'c4', 'c2']", "['c1', 'c2', 'c3', 'c4', 'c5']", "['c5', 'c4', 'c3', 'c2', 'c1']", "['c1', 'c3', 'c5', 'c2', 'c4']"], 0,
        "Odd positions go forward, even positions come back reversed.",
        "The best chunk opens the context and the second-best closes it, with the weakest in the middle. This counters lost-in-the-"
        "middle without dropping chunks; measure it, since the gain varies by model.",
        topic="context-citations", level=3),
    out('import re\nprovided = {"kb12", "kb40"}\nanswer = "Refunds take 5 days [kb12]. Receipts are optional [kb99]."\n'
        'cited = re.findall(r"\\[(\\w+)\\]", answer)\nprint([c for c in cited if c not in provided])',
        ["['kb99']", "[]", "['kb12', 'kb99']", "['kb12']"], 0,
        "Which cited id was never in the prompt?",
        "kb99 was never sent, so that claim's citation is invented: flag it, drop the sentence, or regenerate. This check is cheap "
        "and catches fabricated sources, but it can't tell whether kb12 really supports its sentence.",
        topic="context-citations", level=3),
    tf("If every citation id in an answer refers to a chunk you actually provided, the answer is grounded.", False,
       "Valid id vs supporting text.",
       "A real id can sit next to a claim the chunk doesn't make. Grounding needs a per-claim support check (quote matching, an NLI "
       "model or an LLM judge), not just an id lookup.",
       topic="context-citations", level=3),
    out('evalset = [({"d1", "d2"}, ["d1", "d7", "d2"]),\n           ({"d3"}, ["d8", "d9", "d4"]),\n'
        '           ({"d5", "d6"}, ["d6", "d5", "d1"])]   # (relevant, retrieved)\nk = 2\n'
        'r = [len(rel & set(ret[:k])) / len(rel) for rel, ret in evalset]\n'
        'print([round(x, 2) for x in r], round(sum(r) / len(r), 2))',
        ["[0.5, 0.0, 1.0] 0.5", "[1.0, 0.0, 1.0] 0.67", "[0.5, 0.0, 1.0] 0.67", "[0.5, 0.33, 1.0] 0.61"], 0,
        "Per query: relevant found in the first 2 / number relevant.",
        "q1 finds d1 but d2 is at rank 3 (0.5); q2 finds nothing (0.0); q3 finds both (1.0). Mean recall@2 = 0.5. Always look at the "
        "per-query list too: an average hides the queries that totally fail.",
        topic="rag-eval", level=3,
        analogy="Like a p50 latency that hides the requests timing out."),
    out('import numpy as np\nsim_q = np.array([0.9, 0.89, 0.7])                 # relevance to the query\n'
        'sim_dd = np.array([[1, 0.99, 0.2], [0.99, 1, 0.2], [0.2, 0.2, 1]])  # chunk-chunk similarity\n'
        'lam, picked = 0.5, [0]                             # chunk 0 is already chosen\n'
        'mmr = {c: lam * sim_q[c] - (1 - lam) * max(sim_dd[c][p] for p in picked) for c in [1, 2]}\n'
        'print(max(mmr, key=mmr.get))',
        ["2", "1", "0", "[1, 2]"], 0,
        "Chunk 1 is almost a copy of chunk 0.",
        "MMR = relevance minus redundancy. Chunk 1: 0.445 - 0.495 < 0; chunk 2: 0.35 - 0.1 = 0.25, so the less relevant but new chunk 2 "
        "wins. MMR stops top-k filling up with near-duplicates (the same FAQ in five places).",
        topic="rerank", level=3),
    out('import hashlib\ndef h(t): return hashlib.sha256(t.encode()).hexdigest()[:8]\n'
        'old = {"c1": h("Refunds take 5 days."), "c2": h("Keep receipt.")}\n'
        'new = {"c1": "Refunds take 7 days.", "c2": "Keep receipt.", "c3": "Sale items are final."}\n'
        'to_embed = [c for c, t in new.items() if old.get(c) != h(t)]\nto_delete = [c for c in old if c not in new]\n'
        'print(to_embed, to_delete)',
        ["['c1', 'c3'] []", "['c1', 'c2', 'c3'] []", "['c3'] []", "['c1', 'c3'] ['c2']"], 0,
        "c1's text changed, c2's didn't, c3 is new.",
        "Content hashes let an incremental indexer re-embed only changed or new chunks (c1, c3) and skip c2, which saves most of the "
        "embedding cost on a big corpus. to_delete catches removed chunks; skipping that step leaves ghost content.",
        topic="freshness", level=3,
        analogy="Like an incremental build (make) or ETags: only redo work whose content hash changed."),
    mcq("You are upgrading the embedding model for a 50M-chunk index used in production. What is a safe procedure?",
        ["Build a new index with the new model alongside the old one, backfill it, compare them on the eval set, switch reads via an alias, keep the old one for rollback",
         "Re-embed in place, chunk by chunk, while serving traffic",
         "Switch the query model now and re-embed documents over the next month",
         "Only embed new documents with the new model"], 0,
        "Two vector spaces must never mix in one index.",
        "During an in-place or partial migration, queries compare vectors from two models, which is meaningless. A parallel index "
        "plus an atomic alias swap gives zero-downtime and instant rollback, at the price of double storage for a while.",
        topic="freshness", level=3,
        analogy="Blue-green deployment, for an index."),
    fill("The BM25 parameter (usually around 1.2) that controls how quickly term-frequency gains saturate is called ____.",
         "k1",
         "Its partner b handles document length.",
         "Higher k1 lets repeated terms keep adding score for longer; k1 = 0 turns BM25 into a pure presence/absence (binary) model.",
         topic="sparse-retrieval", level=3),
    mcq("In RAGAS-style evaluation, what does context recall measure?",
        ["How much of the reference (ground-truth) answer is supported by the retrieved context",
         "How many chunks were retrieved",
         "How much of the generated answer is supported by the context",
         "How fast retrieval ran"], 0,
        "It compares the retrieved context with the reference answer.",
        "Context recall asks 'did retrieval bring everything a correct answer needs?' and needs a reference answer. The tempting "
        "option, answer claims supported by context, is faithfulness, which grades the generator.",
        topic="rag-eval", level=3),
    mcq("Top-5 results are often five copies of the same boilerplate (a legal footer repeated on every page). What fixes it?",
        ["Strip boilerplate and deduplicate near-identical chunks at ingestion (hashes, MinHash), and diversify results (e.g. MMR)",
         "Raise k to 50",
         "Use a bigger embedding model",
         "Add 'ignore footers' to the prompt"], 0,
        "Fix the data before the ranking.",
        "Duplicates eat retrieval slots and context tokens without adding facts. Clean them out of the index; MMR at query time "
        "catches what slips through.",
        topic="failure-modes", level=3),

    # ------------------------------------------------------------------ Round 2: L4
    mcq("You raise HNSW's build parameter `M` (links per node) from 16 to 64. What changes?",
        ["Higher recall at the same ef, but more memory per vector and slower index builds and inserts",
         "Lower memory and faster builds",
         "Nothing at query time; M only affects disk layout",
         "Recall drops because the graph gets noisy"], 0,
        "More edges per node: better routes, bigger graph.",
        "M sets graph degree: denser graphs find neighbours more reliably, especially in high dimensions, but each link costs "
        "memory (often several hundred bytes per vector at large M) and build time. ef is the query-time knob, M the build-time one.",
        topic="vector-index", level=4),
    out('n, dim = 100_000_000, 768\nm_subvectors, bits = 96, 8          # product quantisation: 96 codes of 8 bits\n'
        'fp32_gb = n * dim * 4 / 1e9\npq_gb = n * m_subvectors * bits / 8 / 1e9\n'
        'print(fp32_gb, pq_gb, int(fp32_gb / pq_gb))',
        ["307.2 9.6 32", "307.2 76.8 4", "30.72 9.6 3", "307.2 9.6 8"], 0,
        "PQ stores one byte per sub-vector instead of 4 bytes per dimension.",
        "Raw fp32 is 307 GB (RAM for many machines); PQ with 96 one-byte codes is 9.6 GB, 32x smaller. Distances become approximate, "
        "so IVF-PQ systems re-rank a shortlist with full vectors. This is why IVF-PQ, not HNSW, wins at billion scale on tight RAM.",
        topic="vector-index", level=4,
        diagram="""
 fp32: [768 floats x 4 bytes]        = 3072 bytes/vector
 PQ:   [96 sub-vectors -> 1-byte id] =   96 bytes/vector
"""),
    mcq("Your HNSW index takes heavy deletes and updates every day. After a few months, latency rises and recall falls. Why?",
        ["Deletes are usually tombstones: dead nodes stay in the graph and are still traversed, and repairs weaken its links; periodic rebuilds or compaction fix it",
         "HNSW indexes age like disks",
         "The embedding model drifted",
         "Too many queries wear out the index"], 0,
        "What does 'delete' mean inside a graph that others route through?",
        "Removing a node breaks paths through it, so engines mark it deleted and skip it in results. The graph fills with dead "
        "weight. Plan rebuilds (or use engines with compaction) and monitor recall against exact search over time.",
        topic="vector-index", level=4,
        analogy="Soft deletes in a database, or tombstones in an LSM tree: cheap now, compaction later."),
    tf("RRF ignores how much better the top document scored than the second one, so it can throw away useful score information.", True,
       "RRF only looks at positions.",
       "A huge BM25 score gap (an exact error-code match) and a near-tie look identical to RRF. That robustness is why it is the "
       "default, but a tuned, normalised score fusion can beat it when score margins carry signal.",
       topic="hybrid", level=4),
    mcq("On your eval set, dense recall@20 = 0.80, BM25 = 0.55, and hybrid with plain RRF = 0.76: worse than dense alone. How is that possible, and what next?",
        ["Equal-weight RRF lets the much weaker BM25 list push dense hits out of the top 20; weight the lists, tune per query type, or let a reranker decide",
         "It isn't possible; hybrid is always better",
         "RRF has a bug; use plain score addition",
         "Recall@20 can't be compared across retrievers"], 0,
        "RRF gives every list the same vote.",
        "Fusion helps when retrievers have complementary strengths of similar quality. When one is much weaker on your traffic, its "
        "junk takes slots. Measure per query slice (codes vs natural language) and use weighted RRF or routing.",
        topic="hybrid", level=4,
        diagram="""
 dense : d1 d2 d3 ... d20   (good)
 bm25  : x1 x2 x3 ...       (mostly noise here)
 RRF   : d1 x1 d2 x2 ...    (noise takes top-20 slots)
"""),
    mcq("What does a learned sparse retriever (e.g. SPLADE) add over BM25?",
        ["A model assigns weights to terms and adds related terms that never appeared (expansion), but the result is still a sparse vector served from an inverted index",
         "It is BM25 with a bigger vocabulary file",
         "It produces dense vectors like a bi-encoder",
         "It removes the need for any index"], 0,
        "Sparse format, learned weights.",
        "Expansion attacks vocabulary mismatch ('car' can light up 'automobile') while keeping exact-term matching and inverted-index "
        "speed. Costs: an encoder pass at indexing and query time, and domain shift like any learned model.",
        topic="sparse-retrieval", level=4),
    mcq("Retrieval enforces ACL filters correctly, but a confidential project still leaks into answers for unauthorised users. Which component most likely leaked it?",
        ["A derived artifact built across all documents without ACLs, e.g. GraphRAG community summaries, a shared answer cache, or a cross-document FAQ",
         "The embedding model's weights",
         "The BM25 index statistics",
         "The LLM's temperature"], 0,
        "What else gets indexed besides the raw chunks?",
        "Summaries, graphs and caches mix content from many docs, and each needs the strictest ACL of its inputs (or per-group "
        "versions). Security reviews often check the chunk filter and forget the derived stores.",
        topic="filtering-security", level=4),
    tf("A semantic answer cache (reuse an answer if a new question's embedding is close to a past one) shared across all users is safe as long as retrieval enforces ACLs.", False,
       "Does a cache hit even reach the retrieval step?",
       "A cache hit skips retrieval, so the ACL filter never runs and user B gets an answer built from user A's documents. Key caches "
       "by permission scope (tenant/group), and invalidate them when the index changes.",
       topic="filtering-security", level=4,
       analogy="A CDN cache keyed on the URL but not the auth header: user B gets user A's private page.",
       diagram="""
 user A: q -> cache miss -> ACL filter -> answer(A docs) -> cache
 user B: q2 ~ q -> cache HIT -> answer(A docs)  (filter skipped)
"""),
    mcq("Your query rewriter turns \"flights to Goa not on Sunday, under 5k\" into \"flights to Goa\". Retrieval looks fine but answers ignore the constraints. What is the lesson?",
        ["Rewrites can drop negations, numbers and entities; evaluate the rewrite step itself and keep the original query in the retrieval mix",
         "Never use query rewriting",
         "Constraints should go in the system prompt",
         "Use HyDE instead"], 0,
        "Which words did the rewriter treat as noise?",
        "An LLM rewriter is another model that can fail silently. Test it on queries with negations, numbers and filters, pass "
        "structured constraints to metadata filters, and fuse original + rewritten queries.",
        topic="query-transform", level=4),
    out('import numpy as np\nrels = [3, 0, 2]                  # graded relevance, in ranked order\n'
        'dcg = sum(r / np.log2(i + 2) for i, r in enumerate(rels))\nideal = sorted(rels, reverse=True)\n'
        'idcg = sum(r / np.log2(i + 2) for i, r in enumerate(ideal))\nprint(round(float(dcg / idcg), 3))',
        ["0.939", "0.833", "1.0", "0.667"], 0,
        "Ideal order is [3, 2, 0]; rank 2 is discounted by log2(3).",
        "DCG = 3 + 0 + 2/2 = 4; ideal = 3 + 2/1.585 = 4.26; nDCG = 0.939. Unlike recall@k, nDCG uses graded relevance and punishes "
        "putting the best chunk low. Use it when 'somewhat relevant' differs from 'the answer'.",
        topic="rag-eval", level=4),
    mcq("You have real user questions but no reference answers. Which RAG metrics can you still compute?",
        ["Faithfulness (answer vs retrieved context) and answer relevance (answer vs question); context recall needs a reference answer",
         "Only context recall",
         "None; every RAG metric needs ground truth",
         "recall@k, using the LLM's answer as the label"], 0,
        "Which metrics compare only things you already have?",
        "Reference-free metrics judge consistency between question, context and answer. Anything about completeness (context recall, "
        "answer correctness) needs labels. Start reference-free on logs, then label a smaller set.",
        topic="rag-eval", level=4),
    tf("A higher faithfulness score always means a more correct answer for the user.", False,
       "Faithful to what?",
       "Faithfulness measures agreement with the retrieved context. If retrieval brought last year's policy, a perfectly faithful "
       "answer is perfectly wrong. Pair it with context relevance and correctness checks.",
       topic="rag-eval", level=4),
    mcq("Your incremental indexer gives chunks ids like `handbook#0`, `handbook#1` by position. An editor adds one paragraph at the top of the handbook. What happens?",
        ["Every chunk after it shifts position, so all ids map to different text: the whole document is re-embedded and old citations point to the wrong text",
         "Only the new paragraph is embedded",
         "Nothing; ids are cosmetic",
         "The index rejects the update"], 0,
        "What does id #1 refer to after the insert?",
        "Positional ids make a one-line edit look like a full rewrite, and stored citations or feedback now point to other text. "
        "Use stable ids (section anchors) plus content hashes to detect real changes.",
        topic="freshness", level=4,
        diagram="""
 before: #0 intro   #1 refunds  #2 shipping
 insert a new paragraph at the top:
 after:  #0 NEW     #1 intro    #2 refunds   #3 shipping
 every id now points at different text
"""),
    mcq("A user edits a wiki page and asks the bot about it a few seconds later. The bot quotes the old text. Indexing runs through an async queue. Best design response?",
        ["It's eventual consistency: surface the index's freshness, speed up the path for edits, or fetch the live document for chunks whose source changed after indexing",
         "Re-index the whole corpus on every edit",
         "Tell users to wait a day",
         "It's a hallucination; lower the temperature"], 0,
        "Write path vs read path, with a queue in between.",
        "Retrieval reads a replica that lags the source. Options: store source updated_at and re-fetch stale hits, prioritise "
        "interactive edits in the queue, or show 'last indexed at'. Full re-indexes don't scale.",
        topic="freshness", level=4,
        analogy="Read-after-write on a lagging read replica."),
    out('import numpy as np\nv = np.array([0.6, 0.0, 0.8, 0.0])   # a unit-length embedding\nt = v[:2]                            # keep the first 2 dims\n'
        'print(round(float(np.linalg.norm(t)), 2))',
        ["0.6", "1.0", "0.8", "0.5"], 0,
        "Length of [0.6, 0.0].",
        "Truncating a vector (as Matryoshka models allow) breaks unit length, so dot product is no longer cosine until you re-"
        "normalise. Only truncate models trained for it, and re-check recall at the smaller size.",
        topic="embeddings", level=4),
    tf("With many embedding models, cosine similarities for almost all text pairs fall in a narrow band (e.g. 0.70 to 0.90), so a fixed rule like 'relevant if > 0.5' is meaningless.", True,
       "Anisotropy: the vectors crowd into a narrow cone.",
       "Embedding spaces are often anisotropic, so even unrelated texts score high. Relative rank matters more than the raw value; "
       "thresholds need calibrating per model on labelled pairs, or use a reranker's score.",
       topic="embeddings", level=4),
]
