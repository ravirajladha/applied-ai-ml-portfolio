from helpers import mcq, tf, out, fill

SUBJECT = "llmc-rag"

TOPICS = [
    ("why-rag", "Limits of parametric knowledge and long context"),
    ("pipeline", "RAG pipeline: offline index, online query"),
    ("chunking", "Chunking strategies"),
    ("retrievers", "Sparse, dense, hybrid and tabular retrievers"),
    ("index-rerank", "Vector indexes and reranking"),
    ("context", "Context engineering and compression"),
    ("self-rag", "Self-RAG (reflection tokens)"),
    ("self-correcting", "Verification and self-correcting RAG (CRAG, CoVe, agentic RAG)"),
    ("diagnosis", "RAG failure diagnosis"),
    ("rag-metrics", "RAG evaluation metrics (RAGAS)"),
]

QUESTIONS = [
    # ------------------------------------------------------------------ L1
    mcq("The course calls what a model learned during training its 'parametric knowledge'. Which is NOT one of the limits the course lists for it?",
        ["It is too small to answer any question",
         "It is frozen at training time (no facts after the cutoff)",
         "It is opaque (no way to cite where an answer came from)",
         "It has never seen your private documents"], 0,
        "Three of these are in the course's table; one is just false.",
        "Parametric knowledge is frozen, opaque, expensive to update (retraining) and has no access to your data. So 'Who won yesterday?' is stale, 'What is our leave policy?' is hallucinated, and no citation is possible. RAG fixes this by fetching text at query time.",
        topic="why-rag", level=1,
        analogy="Weights are like a compiled binary: fast, but to change a constant you rebuild. RAG is reading a config file at runtime."),
    tf("The course's one-line summary: fine-tuning changes how the model behaves; RAG changes what it can know.", True,
       "Behaviour vs knowledge.",
       "Fine-tuning suits style, format and narrow skills. RAG suits large, changing knowledge that needs citations. Many exam answers lose marks by proposing fine-tuning to add fresh facts.",
       topic="why-rag", level=1),
    mcq("'Lost in the middle' describes which effect?",
        ["A fact placed in the middle of a long context is recalled worse than one at the start or end",
         "The model forgets the middle of its own answer",
         "Chunks in the middle of a document are never indexed",
         "The middle layers of the transformer lose information"], 0,
        "Attention favours the edges of the window.",
        "Needle-in-a-haystack tests show retrieval accuracy drops at large context lengths, worst when the fact sits at roughly 10-50% depth. This is why the course says 'do not dump everything' and why important chunks should not be buried mid-prompt.",
        topic="why-rag", level=1,
        diagram="""
recall
 high |*                         *
      | *                      *
      |   *                 *
 low  |      *   *   *   *
      +---------------------------> position in context
       start     middle         end
"""),
    fill("Tests that hide one fact in a long document and ask the model to find it are called needle-in-a-____ tests.", "haystack",
         "A needle hidden somewhere big.",
         "Needle-in-a-Haystack (Kamradt, 2023) pressure-tests long-context recall. Accuracy falls as the context grows, which is the course's first argument for retrieval over 'paste everything'.",
         topic="why-rag", level=1),
    mcq("In the course's RAG design, which pipeline runs when documents change, rather than on every user request?",
        ["The offline pipeline: chunk, embed, build the index, store",
         "The online pipeline: embed the query, search, rerank, generate",
         "The generator's decoding loop",
         "The reranker"], 0,
        "One pipeline builds, the other serves.",
        "Offline builds the index from docs, wikis and PDFs. Online answers each query using that index. The course: 'everything offline exists only to serve the online path'.",
        topic="pipeline", level=1,
        diagram="""
OFFLINE: docs -> chunk -> embed -> index (ANN) -> vector DB
                                                    |
ONLINE:  query -> embed -> search -> rerank -> LLM <-+
                (same encoder!)
"""),
    tf("The online step that embeds the user's query must use the same embedding model as the offline step that embedded the documents.", True,
       "Can you compare vectors from two different models?",
       "Different encoders produce vectors in different spaces, so their similarities are meaningless. Swap the embedding model and you must re-embed the whole corpus.",
       topic="pipeline", level=1,
       analogy="Like hashing passwords: the login check must use the same hash function as the one used at sign-up."),
    mcq("Which is one of the course's reasons to chunk documents at all?",
        ["Retrieved text must fit the context window along with the query, instructions and any examples",
         "Vector databases cannot store more than 100 words",
         "Chunking encrypts the documents",
         "The tokenizer only accepts one paragraph"], 0,
        "Fit, granularity, signal-to-noise, cost.",
        "Four reasons: fit the window; retrieval granularity (smaller = sharper matches, larger = richer context); signal-to-noise (exclude irrelevant sentences but keep a whole answer); and cost/latency, since chunk size directly sets prompt size.",
        analogy='Like paginating an API response: small pages are cheap to send and easy to match, but a page must still hold a complete record.',
        topic="chunking", level=1),
    fill("Sliding-window chunking with chunk_size = 8 words and stride = 5 words makes consecutive chunks overlap by ____ words.", "3",
         "Overlap = chunk size - stride.",
         "Chunk 1 is words 1-8, chunk 2 starts at word 6 (words 6-13), so words 6-8 are shared: 8 - 5 = 3. That overlap keeps a sentence whole in at least one chunk.",
         topic="chunking", level=1),
    mcq("A user asks 'How do I reset my password?' and the doc says 'Steps to recover account credentials'. Which retriever is more likely to match them?",
        ["Dense retrieval (learned embeddings capture meaning)",
         "Sparse retrieval (BM25 needs shared words)",
         "Neither can match without the exact words",
         "Both equally, since they use the same vectors"], 0,
        "No words in common, same meaning.",
        "Dense vectors place paraphrases close together. BM25 scores only shared terms, so 'reset password' vs 'recover credentials' gets nearly zero. That is the vocabulary-mismatch axis in the past papers.",
        diagram="""
query: reset   password
doc:   recover account credentials
BM25:  shared terms = 0          -> score ~ 0
dense: vectors close in meaning  -> high cosine
""",
        topic="retrievers", level=1),
    tf("A sparse (BM25 / TF-IDF) document vector is non-zero only for the terms that appear in the document.", True,
       "Why is it called sparse?",
       "A sparse vector has one dimension per vocabulary term, nearly all zero. Dense embeddings (384-1536 dims) have a value in every dimension.",
       topic="retrievers", level=1),
    mcq("In the course's retrieve-then-rerank design, which stage's job is recall: making sure the right chunk is somewhere in the candidates?",
        ["Stage 1, the fast retriever (bi-encoder / BM25) over the whole corpus",
         "Stage 2, the cross-encoder reranker",
         "The LLM generator",
         "The chunker"], 0,
        "'Rank 47 is fine -- presence is what counts.'",
        "Stage 1 scores millions of chunks fast and returns, say, the top 100: its job is recall. Stage 2 reads each (query, chunk) pair carefully and puts the best at rank 1: precision. No one model does both.",
        topic="index-rerank", level=1,
        diagram="""
corpus (millions) -> [Stage 1 retriever] -> top-100
                     fast, coarse: RECALL
top-100 -> [Stage 2 cross-encoder] -> top-5 -> LLM
           slow, precise: PRECISION
"""),
    mcq("What does a vector database store for each chunk?",
        ["The embedding vector, the original text and metadata (author, date, chapter) for filtering",
         "Only the embedding vector",
         "Only the original text",
         "The LLM's answer for each chunk"], 0,
        "You need to search, show and filter.",
        "The vector is for similarity search, the text goes into the prompt, and metadata supports filters alongside similarity (hybrid SQL-like queries). Libraries like FAISS only index; vector DBs (Pinecone, Milvus, Qdrant, Weaviate, Chroma) add data management.",
        diagram="""
id  | vector (768 dims) | text           | metadata
c12 | [0.12, -0.40 ...] | "Employees..." | doc: leave
    |                   |                | year: 2025
""",
        analogy='Like a table with a full-text index plus a vector index: you can filter on columns and rank by similarity in one query.',
        topic="index-rerank", level=1),
    mcq("The course's RAG prompt says: 'If the answer is not in the context, reply exactly: \"Not in the provided policy.\"' Why define an exact refusal string?",
        ["It makes refusals deterministic and testable, instead of the model guessing from memory",
         "It makes the model answer faster",
         "It hides the context from the user",
         "It stops retrieval from running"], 0,
        "Your eval can check for an exact string.",
        "Grounding rules scope the model to the context, force citations and define the refusal. A fixed string lets tests assert 'unanswerable question -> refusal', and stops polite hallucinations like 'most companies allow about 5 days'.",
        topic="context", level=1),
    mcq("What is the core idea of Self-RAG?",
        ["One model learns to decide when to retrieve and to critique the retrieved passages and its own output using special reflection tokens",
         "The user retrieves documents and pastes them in",
         "The model retrieves from its own previous answers only",
         "A second database stores every answer the model gives"], 0,
        "Self-reflective retrieval.",
        "Self-RAG (Asai et al.) trains the generator to emit tokens such as Retrieve, ISREL, ISSUP and ISUSE, so retrieval is on demand and every passage and segment gets a self-assessment.",
        topic="self-rag", level=1),
    mcq("What does Corrective RAG (CRAG) add to a basic RAG pipeline?",
        ["A retrieval evaluator that scores the retrieved documents and triggers a corrective action (refine them, or search the web) when they look wrong",
         "A larger generator model",
         "A second embedding model for the query",
         "Automatic fine-tuning on every query"], 0,
        "Check the retrieval before trusting it.",
        "CRAG grades retrieved docs as Correct, Incorrect or Ambiguous and acts on it, all in the application layer without retraining the generator. It is self-correction applied to retrieval.",
        topic="self-correcting", level=1),
    tf("The course says that before blaming the model for a bad RAG answer, you should read what was actually retrieved, because most 'LLM errors' in RAG are retrieval or prompt errors.", True,
       "Debug from the output backward.",
       "Every bad answer points upstream: wrong chunk, missing chunk, buried chunk or weak grounding rules. Looking at the retrieved context first tells you which stage to fix.",
       topic="diagnosis", level=1,
       analogy="Like checking the API response payload before blaming the UI for showing the wrong data."),
    mcq("In RAGAS, what does faithfulness measure?",
        ["The fraction of the answer's claims that are supported by the retrieved context",
         "Whether the answer addresses the user's question",
         "The fraction of retrieved chunks that are relevant",
         "How fluent the answer sounds"], 0,
        "Claims vs context.",
        "Faithfulness = supported claims / total claims. It catches hallucination relative to the context. 'Addresses the question' is answer relevance; 'relevant chunks / retrieved' is context precision.",
        diagram="""
answer -> claims: c1  c2  c3
            vs retrieved context
supported:  yes yes no   -> faithfulness = 2/3
""",
        topic="rag-metrics", level=1),
    mcq("In RAGAS, context precision is computed as:",
        ["relevant chunks retrieved / total chunks retrieved",
         "needed facts retrieved / needed facts total",
         "supported claims / total claims",
         "correct answers / total questions"], 0,
        "Precision = how much of what came back is useful.",
        "It measures retriever noise. 5 chunks with 3 relevant -> 0.60. The second option is context recall, the third faithfulness.",
        topic="rag-metrics", level=1),
    out('system, query, output = 300, 40, 400\n'
        'chunk_size, top_k = 512, 5\n'
        'print(system + query + chunk_size * top_k + output)',
        ["3300", "1252", "2560", "3260"], 0,
        "tokens ≈ system + query + (chunk_size x top_k) + output",
        "300 + 40 + 2,560 + 400 = 3,300 tokens. The retrieved slice (2,560) dominates, which is the course's point: once top_k > 3, chunk size and top_k set the cost.",
        topic="pipeline", level=1),
    tf("Pasting all 500 company documents into a 1M-token window is as accurate as retrieving the 5 most relevant chunks, just more expensive.", False,
       "Two ways 'paste everything' fails.",
       "Recall degrades with length (lost in the middle), and every token is paid and prefilled on every query. Selecting what goes in the window, i.e. retrieval, beats a bigger window on both counts.",
       topic="why-rag", level=1),
    # ------------------------------------------------------------------ L2
    mcq("The course lists four design questions for a RAG system. Which two are decided offline?",
        ["What to index (sources, granularity, metadata, freshness) and how to chunk",
         "How to retrieve and how to rank",
         "How to rank and how to generate",
         "How to retrieve and what to index"], 0,
        "Which decisions shape the index before any user arrives?",
        "Offline: what to index and how to chunk build the knowledge base. Online: how to retrieve (sparse, dense, hybrid, multi-vector) and how to rank (first-stage recall vs second-stage precision via reranking).",
        diagram="""
OFFLINE           | ONLINE
1 what to index   | 3 how to retrieve (sparse/dense/hybrid)
2 how to chunk    | 4 how to rank (rerank: precision)
""",
        topic="pipeline", level=2),
    out('for size in (256, 512, 1024):\n'
        '    print(size, "->", size * 5, "tok")',
        ["256 -> 1280 tok\n512 -> 2560 tok\n1024 -> 5120 tok",
         "256 -> 1280 tok\n512 -> 1792 tok\n1024 -> 2816 tok",
         "256 -> 261 tok\n512 -> 517 tok\n1024 -> 1029 tok",
         "1280\n2560\n5120"], 0,
        "top_k = 5 is fixed.",
        "The course's table: with top_k = 5, the retrieved slice is linear in chunk size, so doubling the chunk size doubles the input cost.",
        topic="pipeline", level=2),
    mcq("You double the chunk size in a RAG system. Which part of the response time grows most?",
        ["Time-to-first-token, because prefill must read the whole (now longer) prompt before the first token",
         "Decode time per generated token",
         "Embedding time for the query",
         "Network time to the user"], 0,
        "Prefill reads the prompt; decode writes the answer.",
        "Prompt length drives prefill and therefore TTFT. Decode is not affected by chunk size. The course's order-of-magnitude numbers (70B on 8 A100s): 1k-token prompt ≈ 0.2-0.3 s TTFT, 10k ≈ 2-3 s.",
        diagram="""
[ prefill: read whole prompt ][ decode: t1 t2 t3 ... ]
 ^ grows with chunk size      ^ unchanged per token
 TTFT = end of prefill
""",
        analogy='Like a page that must download its whole payload before the first paint: a bigger payload delays first paint, not the scrolling afterwards.',
        topic="pipeline", level=2),
    mcq("A leave policy says '...Employees may carry forward up to 10 unused leave days into the next calendar year.' Fixed-size chunking puts '...carry forward up to 10 unused' in chunk A and 'leave days into the next calendar year' in chunk B. What happens to 'how many leave days carry forward?'",
        ["Neither chunk holds the full fact, so neither matches the query well and retrieval misses",
         "Both chunks are retrieved and the LLM joins them perfectly",
         "The vector database merges the chunks automatically",
         "Only the embedding of chunk B changes"], 0,
        "The boundary lands mid-sentence.",
        "The course's example: fixed size with no overlap cuts the fact in two. A sliding window (overlap) keeps the whole sentence in at least one chunk; structure-aware or sentence splitting avoids the cut altogether.",
        topic="chunking", level=2,
        diagram="""
fixed:   [..carry forward up to 10 unused][leave days..]
          chunk A: half the fact        chunk B: the rest
sliding: [..carry forward up to 10 unused]
               [carry forward up to 10 unused leave days..]
               chunk B starts earlier: full fact survives
"""),
    out('words = "the transformer architecture was introduced by vaswani et al in 2017 and used self attention".split()\n'
        'size, stride = 8, 5\n'
        'chunks = [words[i:i + size] for i in range(0, len(words) - size + stride, stride)]\n'
        'print(len(words), len(chunks), [c[0] for c in chunks])',
        ["15 3 ['the', 'by', '2017']",
         "15 2 ['the', 'by']",
         "15 4 ['the', 'by', '2017', 'attention']",
         "15 3 ['the', 'introduced', 'and']"], 0,
        "Starts at 0, 5, 10.",
        "15 words, starts at 0, 5, 10: chunk 1 = words 1-8, chunk 2 = words 6-13, chunk 3 = words 11-15 (shorter). Each neighbour shares 3 words, like the course's stride example.",
        topic="chunking", level=2),
    mcq("What does the course say overlap costs you?",
        ["Offline: text in the overlap is stored, embedded and indexed twice (~20-25% more chunks). Online: duplicate hits that waste context slots",
         "Nothing; overlap is free",
         "It makes BM25 unusable",
         "It shrinks the context window of the LLM"], 0,
        "The same sentence lives in two chunks.",
        "A query matching the overlapped sentence scores both chunks highly (0.89 and 0.87 in the course's example), so 2 of 5 slots repeat one fact: 40% of the context budget on redundancy. Fix: over-retrieve (top-20), drop same-doc high-overlap or same-hash chunks, keep the top-5 unique.",
        analogy='Like a CDN caching the same asset under two URLs: you pay twice for storage and the cache fills with duplicates.',
        topic="chunking", level=2),
    mcq("How does the course's structure-aware chunking handle tables and forms?",
        ["Row-level chunks with the column headers repeated, and the table caption included in every chunk",
         "One chunk per cell",
         "Drop tables; they can't be embedded",
         "Concatenate all rows into one long chunk without headers"], 0,
        "A row is meaningless without its column names.",
        "Each row chunk must say what its values mean, so headers repeat. Markdown/HTML split on headings (keep the heading trail as metadata); code splits by function or class, never inside a code fence. 'The document already knows its natural boundaries.'",
        diagram="""
caption: Leave entitlements (2025)
chunk 1: caption + | grade | annual | carry_fwd |
                   | G1    | 18     | 10        |
chunk 2: caption + | grade | annual | carry_fwd |
                   | G2    | 21     | 12        |
""",
        topic="chunking", level=2),
    mcq("A past paper asks you to compare BM25 and dense retrieval on three axes. Which row is correct?",
        ["Representation: sparse term-frequency vector vs fixed-dimension neural embedding. Matching: exact lexical overlap vs semantic similarity. Vocabulary mismatch: fragile vs robust",
         "Representation: both use embeddings. Matching: both use cosine. Vocabulary mismatch: both fragile",
         "Representation: dense is sparse. Matching: BM25 is semantic. Vocabulary mismatch: BM25 is robust",
         "Representation: BM25 uses images. Matching: dense uses regex. Vocabulary mismatch: no difference"], 0,
        "Bag-of-words + IDF vs a neural encoder.",
        "This is the 3-mark answer. BM25 needs shared tokens, so synonyms and paraphrases fail without query expansion; dense maps synonyms to nearby vectors. Dense is weaker on exact IDs and rare phrases, which is why hybrid exists.",
        topic="retrievers", level=2),
    tf("In the course's BM25 formula, setting k = 0 leaves only the idf part of the score.", True,
       "What happens to tf / (tf + 0)?",
       "With k = 0 the term part tf / tf = 1, so each matching term contributes just its idf: term frequency stops mattering. Reasonable values are k in [1.2, 2].",
       topic="retrievers", level=2),
    tf("In BM25, b = 1 switches document-length normalisation off.", False,
       "The course: b ranges from 1 to 0.",
       "b = 1 means full scaling by document length; b = 0 means no length scaling. The usual b = 0.75 partly penalises long documents, which mention any term more often by chance.",
       topic="retrievers", level=2),
    out('import math\n'
        'N, df = 3, 2\n'
        'idf = math.log10(N / df)\n'
        'k, b, avgdl = 1.5, 0.75, 11 / 3\n'
        'def term(tf, dl): return idf * tf / (tf + k * (1 - b + b * dl / avgdl))\n'
        'print(round(idf, 5), round(term(3, 4), 4), round(term(1, 4), 4))',
        ["0.17609 0.1148 0.0677", "0.17609 0.287 0.1692", "0.40547 0.2643 0.1558", "0.17609 0.5283 0.1761"], 0,
        "log10(3/2), then the course's tf / (tf + k(1 - b + b·|D|/avgdl)).",
        "This is the course's worked example: Q = 'apple banana' over 3 docs, D1 = 'apple banana apple apple' (|D| = 4, avgdl = 3.67). apple scores 0.1148, banana 0.0677, total 0.1825. The course's version has no (k + 1) in the numerator, which rescales scores but never changes the ranking.",
        topic="retrievers", level=2),
    mcq("Why can a bi-encoder (DPR-style) search millions of chunks in milliseconds while a cross-encoder cannot?",
        ["Bi-encoder document vectors are computed once offline, so a query needs one forward pass plus dot products via ANN; a cross-encoder must run one full forward pass per (query, document) pair",
         "Bi-encoders use smaller vocabularies",
         "Cross-encoders run only on CPUs",
         "Bi-encoders skip the query entirely"], 0,
        "What can be precomputed?",
        "Bi-encoder: everything precomputable, nothing contextual (query and doc never attend to each other). Cross-encoder: everything contextual, nothing precomputable. So bi-encoders retrieve and cross-encoders rerank tens of candidates.",
        topic="index-rerank", level=2,
        diagram="""
bi-encoder:     f(query) --.            score = f(q) . g(d)
                g(doc)  ---'  (g(doc) stored offline)
cross-encoder:  [CLS] query [SEP] doc [SEP] -> transformer
                -> score h(q, d)   (one pass per pair)
"""),
    mcq("HNSW vs IVF: which description matches the course?",
        ["HNSW: layered neighbour graph, search starts at the top layer and descends; high recall and low latency if the graph fits in RAM. IVF: k-means clusters, search only nearby clusters; suits very large corpora",
         "HNSW: k-means clusters; IVF: a layered graph",
         "Both are exact search methods that scan every vector",
         "HNSW is for sparse vectors, IVF for dense"], 0,
        "Graph vs clusters.",
        "Both are approximate nearest neighbour (ANN) methods: they trade a little accuracy for a massive speed-up. Brute force is exact but O(N) and too slow past ~100K vectors.",
        topic="index-rerank", level=2),
    mcq("In the course's 'Anatomy of a RAG prompt', why is the user's question placed last, after the chunks?",
        ["The model reads the evidence before the question, and recency keeps the question in strong attention",
         "Questions at the start are ignored by the tokenizer",
         "It makes the prompt shorter",
         "The vector DB requires it"], 0,
        "Attention is strongest at the start and end.",
        "Layout: grounding rules first, then chunks with metadata ([chunk 12 | Leave Policy > Carry-forward | 2025]), then the question last. Chunk ids and versions let the model cite and let you audit.",
        diagram="""
[grounding rules: answer only from context, cite ids,
 refusal: "Not in the provided policy."]
[chunk 12 | Leave Policy > Carry-forward | 2025] ...
[chunk 31 | Leave Policy > Encashment | 2025] ...
Question: How many leave days can I carry forward?
""",
        topic="context", level=2),
    mcq("Retrieved context says 'carry forward up to 10 days' (2025 policy) but the model 'remembers' 5 days from training. What do the course's context-engineering tips say to do?",
        ["Instruct the model to treat retrieved chunks as the authoritative, more recent source, and show version/date metadata so the chunk wins",
         "Average the two numbers",
         "Remove the retrieved chunk to avoid confusion",
         "Raise the temperature so the model explores both"], 0,
        "Retrieved context should beat parametric memory.",
        "Conflicts between memory and context are common. A grounding rule plus visible metadata (version 2025, date) tells the model which source wins. Without it, parametric memory can win, the 'context ignored' failure.",
        topic="context", level=2),
    mcq("Which list gives Self-RAG's four reflection tokens and what they judge?",
        ["Retrieve (should I retrieve?), ISREL (is the passage relevant?), ISSUP (is my output supported by it?), ISUSE (is the response useful overall?)",
         "Query, Key, Value, Output",
         "Correct, Incorrect, Ambiguous, Unknown",
         "Thought, Action, Observation, Answer"], 0,
        "One about retrieving, two about the passage/support, one about usefulness.",
        "Retrieve decides on-demand retrieval; ISREL grades each passage; ISSUP checks the segment is supported (fully, partially, not); ISUSE rates usefulness 1-5. Correct/Incorrect/Ambiguous are CRAG's evaluator labels, a common mix-up.",
        diagram="""
segment t: [Retrieve=yes] -> passages p1 p2 p3
  for each p: [ISREL] -> generate -> [ISSUP] [ISUSE]
  keep the best-scoring continuation, go to t+1
""",
        topic="self-rag", level=2),
    mcq("CRAG's retrieval evaluator labels the retrieved set Correct, Incorrect or Ambiguous. Which mapping to actions is right?",
        ["Correct: refine the docs into relevant knowledge strips. Incorrect: discard them and do a web search with a rewritten query. Ambiguous: combine both",
         "Correct: web search. Incorrect: refine. Ambiguous: stop",
         "All three: retrain the generator",
         "Correct: answer from memory. Incorrect: refuse. Ambiguous: ask the user"], 0,
        "Good docs get cleaned; bad docs get replaced.",
        "Refinement uses decompose-then-recompose: split docs into small strips, keep the relevant ones, recompose. When the evaluator distrusts the retrieval, CRAG fetches fresh evidence instead of letting the generator improvise.",
        topic="self-correcting", level=2,
        diagram="""
retrieve -> [evaluator] --Correct----> refine (keep strips)
                       --Incorrect--> discard + web search
                       --Ambiguous--> both, then merge
                                        -> generate
"""),
    mcq("Chain-of-Verification (CoVe), named in the handout's 'Verification and Self-Correction' topic, works in which order?",
        ["Draft an answer -> plan verification questions -> answer them independently -> write the final verified answer",
         "Retrieve -> rerank -> answer -> cite",
         "Answer -> ask the user to verify -> retry",
         "Plan -> act -> observe -> answer"], 0,
        "Check facts with separate questions.",
        "Answering the verification questions independently (not looking at the draft) stops the draft's errors from biasing the checks. In RAG it is a post-generation fact check against retrieved evidence.",
        analogy="Like a reviewer who writes independent test cases for a PR instead of reading the author's own tests.",
        topic="self-correcting", level=2),
    mcq("Which RAGAS metric needs ground truth (the set of facts a correct answer requires)?",
        ["Context recall",
         "Faithfulness",
         "Context precision (in its simplest form)",
         "Answer relevance"], 0,
        "To know what is missing, you must know what was needed.",
        "Context recall = needed facts retrieved / needed facts total, so you need the needed facts. Faithfulness and answer relevance can be judged from question, context and answer alone.",
        analogy='Like test coverage: to know what was missed you need the list of what should have been covered.',
        topic="rag-metrics", level=2),
    mcq("The course separates faithfulness from truthfulness. Which is right?",
        ["Faithfulness: the answer is entailed by the retrieved context. Truthfulness: the answer matches real-world facts, regardless of context",
         "They are the same thing",
         "Faithfulness: matches real-world facts. Truthfulness: entailed by context",
         "Faithfulness is about tone; truthfulness about grammar"], 0,
        "Faithful to what?",
        "An answer can be faithful to an outdated chunk and still untrue today, or true but not supported by the context (an extrinsic hallucination for RAG purposes). RAG metrics check faithfulness; truthfulness needs world knowledge or fact checking.",
        topic="rag-metrics", level=2),
    mcq("In the course's symptom table, the answer states the same fact twice and other needed facts are missing. Likely cause and fix?",
        ["Overlapping chunks retrieved with no dedup; dedup at retrieval time (drop same-doc high-overlap or same-hash chunks)",
         "The generator's temperature is too high",
         "The embedding model is too small",
         "The grounding rules are too strict"], 0,
        "Two slots, one fact.",
        "Sliding-window chunks repeat text, so both copies score high and crowd out other evidence. Over-retrieve, dedup, keep the top unique chunks.",
        topic="diagnosis", level=2),
    mcq("What does context compression do in a RAG pipeline?",
        ["Shrinks the retrieved text before generation: keep only relevant sentences (extractive), summarise (abstractive) or prune low-information tokens",
         "Zips the vector database to save disk",
         "Quantises the generator to 4-bit",
         "Removes the system prompt"], 0,
        "Fewer tokens, same evidence.",
        "Compression cuts prompt tokens, so lower cost and TTFT, and moves the useful sentences out of a sea of filler, which helps lost-in-the-middle. Methods include RECOMP-style extractive/abstractive compressors and LLMLingua-style token pruning. Risk: dropping the sentence you needed.",
        topic="context", level=2,
        analogy="Like sending a reviewer the diff instead of the whole repository."),
    mcq("The course says agentic RAG replaces the fixed pipeline with a decision-maker. What does the LLM decide?",
        ["Whether to retrieve, which source to hit (e.g. SQL vs vector index), how many times, and when to stop",
         "Only the temperature",
         "Which GPU to run on",
         "How to chunk the corpus offline"], 0,
        "The retriever becomes one tool among several.",
        "Example: 'employee count' -> SQL; 'policy wording' -> vector index. For complex questions the agent writes a short plan and executes it. What you tune shifts from chunking and top-k to loop controls: step budgets, stop conditions, tool schemas.",
        diagram="""
query -> [LLM decides] --policy wording--> vector index
              |       --employee count--> SQL
              |       --enough evidence--> answer
              +<----- observe results, retry (budget)
""",
        topic="self-correcting", level=2),
    mcq("The course says 'Advanced RAG = prompt patterns you've already seen'. Which pairing is right?",
        ["Query rewriting = input normalisation; multi-query RAG = decomposition / fan-out; multi-hop RAG = iterative ReAct-style reasoning; routing = query classifier + router",
         "Query rewriting = fine-tuning; multi-hop = quantisation",
         "Multi-query RAG = self-consistency; routing = beam search",
         "Multi-hop RAG = chunk overlap; query rewriting = reranking"], 0,
        "M7's patterns, with the retriever as the tool.",
        "Each advanced technique reuses an M7 system-design pattern: a preprocessing prompt cleans the query, decomposition fans out, a ReAct loop does sequential hops where later steps use earlier results, and a router picks the source (HR docs vs CRM vs web).",
        topic="self-correcting", level=2),
    out('bm25 = ["d3", "d1", "d7", "d2"]\n'
        'dense = ["d1", "d2", "d3", "d9"]\n'
        'k = 60\n'
        'rrf = {}\n'
        'for ranking in (bm25, dense):\n'
        '    for r, d in enumerate(ranking, 1):\n'
        '        rrf[d] = rrf.get(d, 0) + 1 / (k + r)\n'
        'print(sorted(rrf, key=rrf.get, reverse=True)[:3])',
        ["['d1', 'd3', 'd2']", "['d3', 'd1', 'd2']", "['d1', 'd2', 'd3']", "['d3', 'd1', 'd7']"], 0,
        "d1 is rank 2 and rank 1; d3 is rank 1 and rank 3.",
        "Hybrid retrieval fuses BM25 and dense lists with reciprocal rank fusion. d1: 1/62 + 1/61; d3: 1/61 + 1/63; d2: 1/64 + 1/62. Being high in both lists beats being first in one.",
        topic="retrievers", level=2),
    mcq("A user asks 'What is 12% of my invoice total?'. Which tool does the course's 'when not to use RAG' table recommend?",
        ["Tool use / function calling: the answer is computed, not retrieved",
         "RAG over all invoices",
         "Fine-tuning on invoice data",
         "Long-context prompting with every invoice"], 0,
        "Retrieval finds text; it doesn't do arithmetic on live records.",
        "The table: fine-tuning for style/format/narrow stable skill; long context for one document that fits; function calling when the answer is computed; RAG for large changing knowledge needing citations; agentic RAG when the query needs decomposition or several retrieval rounds.",
        analogy='Like computing a total with a SQL SUM instead of searching the docs for a page that happens to contain the number.',
        topic="why-rag", level=2),
    fill("The ANN index that uses a layered neighbour graph, starting at the top layer and descending toward the query, is abbreviated ____.", "HNSW",
         "Hierarchical Navigable Small World.",
         "HNSW gives high recall at low latency for medium-large corpora as long as the graph fits in RAM. IVF (k-means clusters) is the course's choice for very large corpora.",
         topic="index-rerank", level=2),
    out('import numpy as np\n'
        'q = np.array([0.6, 0.8])\n'
        'docs = {"policy": np.array([0.8, 0.6]), "faq": np.array([0.0, 1.0]), "memo": np.array([1.0, 0.0])}\n'
        'scores = {d: round(float(q @ v), 2) for d, v in docs.items()}\n'
        'print(sorted(scores.items(), key=lambda x: -x[1]))',
        ["[('policy', 0.96), ('faq', 0.8), ('memo', 0.6)]",
         "[('faq', 0.8), ('policy', 0.96), ('memo', 0.6)]",
         "[('memo', 0.6), ('faq', 0.8), ('policy', 0.96)]",
         "[('policy', 1.0), ('faq', 0.8), ('memo', 0.6)]"], 0,
        "All vectors are unit length, so dot product = cosine.",
        "Dense retrieval in miniature: score = zq . zd, then take the top-k. 0.6*0.8 + 0.8*0.6 = 0.96 for policy. Real embeddings have 384-1536 dims and the dot products run through an ANN index.",
        topic="retrievers", level=2),
    # ------------------------------------------------------------------ L3
    mcq("A company's RAG assistant over its API docs uses BM25 over fixed 512-token chunks with no overlap. Deprecation notes sit at the end of a section, right after a long code example, and the retriever often misses them even when the right page is relevant. Which failure mode is this?",
        ["Boundary loss / split context: the note sits in a fixed-size chunk dominated by other content, so the chunk's overall score doesn't reflect the note",
         "BM25 lexical-match bias toward old changelogs",
         "Chunk truncation of a multi-paragraph answer",
         "The generator's context window is too small"], 0,
        "What else is in the chunk that holds the note?",
        "This is P1 of the past paper. The fixed boundary puts the note in with unrelated code, so the chunk is 'about' something else. Fix: section/semantic chunking on paragraph and heading boundaries, so the note lands in a chunk whose header names the deprecated API.",
        topic="diagnosis", level=3),
    mcq("Same API-docs bot: for 'How do I authenticate?' the top result is a 2019 changelog that contains the word 'authenticate', not the current auth guide. Diagnosis and the past paper's matched fix?",
        ["BM25 lexical-match bias; add a cross-encoder reranker over the BM25 top-10 so the semantically best passage rises",
         "Boundary loss; switch to semantic chunking",
         "Truncation; add 128-token overlap",
         "Lost in the middle; move the question to the start"], 0,
        "BM25 counts words, it doesn't understand intent.",
        "BM25 rewards term frequency with no notion of meaning or recency, so a changelog that repeats 'authenticate' wins. A cross-encoder reads query and passage together and ranks the guide first. A version/date filter on what is indexed also helps.",
        topic="diagnosis", level=3),
    mcq("A contract-review RAG bot uses fixed 400-token chunks. For multi-step compliance procedures, the retrieved chunk has steps 1-2 but stops before steps 3-5. Which fix from {sliding window with overlap, semantic chunking, cross-encoder reranker} does the past paper's answer key match to this pattern?",
        ["Sliding-window chunking with overlap, so the full procedure appears intact in at least one chunk",
         "A cross-encoder reranker",
         "Raise BM25's k parameter",
         "Use a bigger generator"], 0,
        "The answer is cut off at a token count.",
        "This is P3: truncation across paragraph boundaries. The answer key maps F1 (128-token overlap) to it. A reranker can only reorder chunks; it can't put the missing steps back into the chunk. Semantic chunking could also keep the procedure together, but the key uses it for P1.",
        topic="chunking", level=3),
    mcq("An insurer's v1 RAG embeds claim manuals (long PDFs), policy memos (short), a claims table (15 columns, 3M rows) and FAQs as plain text with one dense retriever. Q: 'What are the recommended steps when water damage is reported late?' returns short FAQ snippets that mention 'water damage' instead of the manual section. Best primary retriever for this question?",
        ["Dense (or a dense-leaning hybrid): the question paraphrases the manual's wording, and BM25 can anchor on 'water damage'",
         "BM25 only, since the exact phrase appears in the FAQ",
         "A tabular / SQL retriever",
         "No retrieval; answer from the model's memory"], 0,
        "Paraphrase of long-form guidance.",
        "Mirrors Q1 of the past paper: the manual says something like 'for delayed notification of water ingress, first...'. Dense captures the paraphrase. The fix also needs the FAQ not to crowd out the manual: source routing or per-source indexes.",
        topic="retrievers", level=3),
    mcq("Same insurer. Q: 'List all claims over ₹5 lakh filed in March that are still open, with the assessor's name.' The generator invents plausible claim IDs. Best retriever?",
        ["A tabular / SQL-style retriever that turns the question into a structured filter (WHERE amount > 500000 AND month = 3 AND status = 'open', JOIN assessors) and executes it",
         "Dense retrieval with a larger top-k",
         "A hybrid of BM25 and dense",
         "BM25 with a lower b"], 0,
        "Can any text-similarity method enforce '> 5 lakh'?",
        "Mirrors Q2: numeric predicates and joins over relational rows. BM25 (lexical) and dense (semantic) both return text about big claims, not the qualifying rows; a text hybrid inherits the same limit. 'Hybrid' is the common wrong answer.",
        topic="retrievers", level=3,
        diagram="""
question -> LLM writes SQL:
    SELECT id, assessor FROM claims JOIN assessors ...
    WHERE amount > 500000 AND status = 'open' ...
-> DB executes -> exact rows -> LLM answers
"""),
    mcq("Same insurer. Q: 'What is our claim-file retention period?' returns a manual passage about 'retention of evidence photos' instead of the 1-page memo that states the period. Best primary retriever?",
        ["BM25 (or a BM25-leaning hybrid): the memo is short and literally contains the specific institutional phrase",
         "Dense only, since it understands meaning",
         "A tabular retriever",
         "A cross-encoder over the whole corpus"], 0,
        "Short document, exact phrase.",
        "Mirrors Q3: 'claim-file retention period' is a specific term that the memo contains verbatim, and BM25 handles short documents with exact terms well. Pure dense blurs it with topically similar 'retention' text.",
        topic="retrievers", level=3),
    mcq("Transcript: User asks the carry-forward limit. Retrieved: [chunk 7 | Leave Policy | 2022] '...up to 5 days...'. Answer: 'You can carry forward 5 days [chunk 7].' The 2025 policy says 10. Where is the fault?",
        ["Retrieval: a superseded version won the similarity contest; remove or down-rank old versions and filter on version/date metadata",
         "The LLM hallucinated",
         "The grounding prompt is too weak",
         "The temperature is too high"], 0,
        "The model did exactly what it was told.",
        "The course: 'A grounded, cited, wrong answer is a retrieval bug, not an LLM bug.' The model was faithful to the context; the context was wrong. Fix at what to index (Q1): drop superseded docs or filter by version.",
        analogy='Like a correct function returning wrong output because the cache served a stale record: fix the data, not the function.',
        topic="diagnosis", level=3),
    mcq("Transcript: the correct 2025 chunk ('up to 10 unused leave days') WAS in the prompt, buried after a long chat history. The answer: 'Carry-forward rules vary, but most companies allow around 5 days.' Where is the fault?",
        ["The prompt: no grounding or conflict rules and the chunk is buried mid-prompt; add grounding rules, move chunks out of the middle, trim history",
         "Retrieval: the chunk was wrong",
         "The embedding model",
         "The chunk size"], 0,
        "Retrieval succeeded.",
        "Same setup, different fault, different fix. Parametric memory won because nothing told the model the context is authoritative and the chunk sat where attention is weakest.",
        diagram="""
[system: be helpful]           <- no grounding rules
[long chat history ........]
[chunk: up to 10 days]         <- buried mid-prompt
[more history .............]
Q: carry-forward?  A: "around 5 days" (from memory)
""",
        topic="diagnosis", level=3),
    out('window = 8000\n'
        'system_grounding, history, headroom = 600, 1400, 1000\n'
        'avg_chunk = 700\n'
        'budget = window - system_grounding - history - headroom\n'
        'print(budget, budget // avg_chunk)',
        ["5000 7", "5000 8", "6000 8", "7400 10"], 0,
        "Subtract everything that isn't retrieved chunks.",
        "The course's 8K example: 8,000 - 600 - 1,400 - 1,000 = 5,000 tokens for chunks; / 700 = 7.1, so at most 7. Generation headroom is the line people forget, and history grows every turn unless you truncate or summarise.",
        topic="context", level=3),
    tf("If the context budget fits 7 chunks, the course recommends always sending all 7 to maximise recall.", False,
       "'Fitting 7 does not mean sending 7.'",
       "Lost in the middle argues for fewer, better-ranked chunks. Prefer high-quality chunks over many mediocre ones, and use the reranker both to select and to place the best chunks at high-attention positions.",
       topic="context", level=3),
    out('claims = {"c1": True, "c2": True, "c3": False, "c4": True}   # supported by context?\n'
        'chunks = [True, False, False, True, False, False]           # relevant?\n'
        'needed, needed_found = 3, 2\n'
        'faith = sum(claims.values()) / len(claims)\n'
        'prec = sum(chunks) / len(chunks)\n'
        'rec = needed_found / needed\n'
        'print(round(faith, 2), round(prec, 2), round(rec, 2))',
        ["0.75 0.33 0.67", "0.75 0.67 0.33", "0.67 0.33 0.75", "0.25 0.33 0.67"], 0,
        "Supported/total claims, relevant/retrieved chunks, found/needed facts.",
        "Faithfulness 3/4 = 0.75, context precision 2/6 = 0.33, context recall 2/3 = 0.67. All three are low in different places: the generator added an unsupported claim, the retriever is noisy and it also missed a fact.",
        topic="rag-metrics", level=3),
    mcq("RAGAS on a pipeline: context recall 1.00, context precision 0.50, faithfulness 0.67. Which plan matches the course's diagnosis?",
        ["Retriever is complete but noisy: add a cross-encoder reranker, tighten the similarity threshold, try hybrid. Generator added an unsupported fact: stricter grounding prompt, claim verifier, lower temperature",
         "Retriever misses facts: increase top-k and chunk size",
         "Everything is fine: 0.67 is a passing score",
         "Retrain the embedding model from scratch"], 0,
        "Recall = nothing missing. Precision = noise. Faithfulness = hallucination.",
        "The course's worked example: 'the retriever isn't missing information, it's over-retrieving, and the generator isn't grounded.' A single accuracy number could not tell you to fix both stages differently, which is why RAGAS matters.",
        topic="rag-metrics", level=3),
    mcq("A candidate answer 'the drug reduces pressure' has unigram precision 1.0 against the reference, but the retrieved context only discusses cholesterol. Why can't BLEU/ROUGE detect the problem?",
        ["They compare surface n-gram overlap with a reference string and never look at the retrieved context, so they can't check entailment",
         "They only work on long answers",
         "They penalise short answers too much",
         "They need a GPU to compute"], 0,
        "What does BLEU compare the candidate against?",
        "The past paper's point: lexical overlap is orthogonal to logical entailment from context. The claim is a hallucination relative to the evidence, which only a context-aware metric (RAGAS faithfulness) can catch.",
        topic="rag-metrics", level=3),
    tf("A cross-encoder reranker over the retriever's top-50 can raise answer quality only if the right chunk is already somewhere in those 50.", True,
       "Can a reranker invent candidates?",
       "The reranker reorders what stage 1 returned. If recall@50 misses the chunk, fix stage 1 (chunking, hybrid, query rewriting), not stage 2. The Qwen2.5-3B example worked because the right chunk was already at rank 4.",
       analogy="Like a sort step: it can reorder the rows the query returned, but it can't add a row the WHERE clause filtered out.",
        topic="index-rerank", level=3),
    out('docs_per_query = {"cross_all": 10_000_000, "rerank_top": 100}\n'
        'ms_per_pair = 5\n'
        'for name, n in docs_per_query.items():\n'
        '    print(name, n * ms_per_pair / 1000 / 3600, "hours")',
        ["cross_all 13.88888888888889 hours\nrerank_top 0.0001388888888888889 hours",
         "cross_all 13.9 hours\nrerank_top 0.0 hours",
         "cross_all 50000.0 hours\nrerank_top 0.5 hours",
         "cross_all 1.3888888888888888 hours\nrerank_top 1.388888888888889e-05 hours"], 0,
        "10M x 5 ms = 50,000 s.",
        "One cross-encoder pass per pair: 10M pairs = 50,000 s ≈ 13.9 hours per query, versus 0.5 s for 100 candidates. That is the course's 'feasible for 100 candidates, impossible for 10 million', and why cross-encoders rerank instead of retrieve.",
        topic="index-rerank", level=3),
    out('hits = [("c12", "leave.md", 0.89), ("c11", "leave.md", 0.87), ("c40", "faq.md", 0.72),\n'
        '        ("c13", "leave.md", 0.70), ("c88", "hr.md", 0.66)]\n'
        'overlaps = {("c12", "c11"), ("c12", "c13")}   # chunk pairs sharing >50% text\n'
        'keep = []\n'
        'for cid, doc, s in hits:\n'
        '    if not any((k, cid) in overlaps or (cid, k) in overlaps for k in keep):\n'
        '        keep.append(cid)\n'
        'print(keep[:3])',
        ["['c12', 'c40', 'c88']", "['c12', 'c11', 'c40']", "['c12', 'c40', 'c13']", "['c11', 'c40', 'c88']"], 0,
        "c11 and c13 each overlap with c12, which is kept first.",
        "Dedup at retrieval time: over-retrieve, walk down by score, drop chunks that heavily overlap one already kept. c11 and c13 are near-copies of c12, so the three slots go to three different facts.",
        topic="chunking", level=3),
    mcq("How is Self-RAG trained, according to the paper?",
        ["A critic model labels training passages and outputs with reflection tokens offline; the generator is then trained on that augmented corpus to predict both text and reflection tokens, so no critic is needed at inference",
         "The generator is trained with RLHF using a reward model that scores retrieval",
         "No training: reflection tokens are added through the prompt only",
         "The retriever is fine-tuned while the generator stays frozen"], 0,
        "Critic offline, generator learns to self-critique.",
        "Self-RAG expands the vocabulary with reflection tokens and trains the LM with ordinary next-token prediction on critic-annotated data. At inference the same model decides to retrieve and grades its own passages and segments.",
        analogy='Like a senior engineer annotating PRs with review comments once, so a junior learns to write those comments on their own code.',
        topic="self-rag", level=3),
    out('p_retrieve_yes = [0.15, 0.62, 0.48, 0.91]   # per output segment\n'
        'delta = 0.5\n'
        'print(["retrieve" if p > delta else "continue" for p in p_retrieve_yes])',
        ["['continue', 'retrieve', 'continue', 'retrieve']",
         "['retrieve', 'retrieve', 'retrieve', 'retrieve']",
         "['continue', 'retrieve', 'retrieve', 'retrieve']",
         "['retrieve', 'continue', 'retrieve', 'continue']"], 0,
        "Retrieve only when p > 0.5.",
        "Self-RAG's adaptive retrieval: the generator predicts the Retrieve token, and retrieval fires only when its probability passes a threshold. Common-knowledge segments skip retrieval; fact-heavy segments trigger it. Raising delta means fewer retrievals.",
        topic="self-rag", level=3),
    mcq("Self-RAG retrieves 3 passages for a segment and generates one candidate continuation per passage. How does it pick which to keep?",
        ["It scores each candidate by its likelihood combined with reflection-token scores (ISREL, ISSUP, ISUSE) and keeps the best (segment-level beam search)",
         "It always keeps the candidate from the top-ranked passage",
         "It concatenates all three",
         "It asks the user to choose"], 0,
        "The critique tokens are the ranking signal.",
        "Candidates whose passage is relevant (ISREL) and which are fully supported (ISSUP) and useful (ISUSE) rank higher. Weights on these terms can be changed at inference, e.g. to favour support for a citation-heavy use case.",
        topic="self-rag", level=3),
    out('def crag(scores, upper=0.7, lower=0.3):\n'
        '    best = max(scores)\n'
        '    if best >= upper: return "Correct: refine strips"\n'
        '    if best < lower: return "Incorrect: web search"\n'
        '    return "Ambiguous: refine + web search"\n'
        'for s in ([0.82, 0.4], [0.12, 0.25], [0.55, 0.31]):\n'
        '    print(crag(s))',
        ["Correct: refine strips\nIncorrect: web search\nAmbiguous: refine + web search",
         "Correct: refine strips\nAmbiguous: refine + web search\nAmbiguous: refine + web search",
         "Incorrect: web search\nIncorrect: web search\nCorrect: refine strips",
         "Correct: refine strips\nIncorrect: web search\nIncorrect: web search"], 0,
        "Use the best score against the two thresholds.",
        "CRAG's evaluator gives a confidence per document. At least one confident doc -> Correct; all below the lower threshold -> Incorrect; otherwise Ambiguous. This is a few lines of application code around an evaluator model.",
        topic="self-correcting", level=3),
    tf("CRAG requires retraining the generator with special tokens, just like Self-RAG.", False,
       "Where does CRAG's evaluator live?",
       "CRAG is plug-and-play: a separate lightweight retrieval evaluator plus corrective actions wrapped around any generator. Self-RAG changes the generator itself. That is why CRAG fits 'self-correcting RAG in the application layer'.",
       topic="self-correcting", level=3),
    out('def answer(q, max_retries=2):\n'
        '    calls, query = 0, q\n'
        '    for attempt in range(max_retries + 1):\n'
        '        calls += 2                      # retrieve+grade, then generate or rewrite\n'
        '        if attempt == 2 or "v2" in query:\n'
        '            return calls, query\n'
        '        query += " v2" if attempt == 1 else ""\n'
        '    return calls, "fallback"\n'
        'print(answer("leave policy"))',
        ["(6, 'leave policy v2')", "(4, 'leave policy v2')", "(6, 'fallback')", "(2, 'leave policy')"], 0,
        "Trace attempts 0, 1, 2.",
        "Attempt 0: no 'v2', no rewrite (calls 2). Attempt 1: still no 'v2', rewrite adds it (calls 4). Attempt 2: returns with calls 6. A self-check-and-retry loop must be bounded by a max-retry budget so it can't loop forever, and every retry costs LLM calls.",
        topic="self-correcting", level=3),
    mcq("Extractive vs abstractive context compression: which trade-off is right?",
        ["Extractive keeps original sentences (safe to cite, less compression); abstractive summarises (more compression, but can drop or distort facts and you can't cite the exact text)",
         "Extractive is always shorter than abstractive",
         "Abstractive keeps the exact wording, extractive paraphrases",
         "Both are identical; only the name differs"], 0,
        "Copying vs rewriting.",
        "Extractive compressors select sentences, so citations still point at real text. Abstractive compressors write a summary, which can introduce an error before the generator even starts. Token pruning (LLMLingua-style) removes low-information tokens and keeps the rest verbatim.",
        analogy='Extractive is quoting the relevant lines of a log; abstractive is paraphrasing the log in your own words.',
        topic="context", level=3),
    out('ranked = ["c1", "c2", "c3", "c4", "c5"]     # best first\n'
        'front, back = [], []\n'
        'for i, c in enumerate(ranked):\n'
        '    (front if i % 2 == 0 else back).append(c)\n'
        'print(front + back[::-1])',
        ["['c1', 'c3', 'c5', 'c4', 'c2']", "['c1', 'c2', 'c3', 'c4', 'c5']", "['c5', 'c4', 'c3', 'c2', 'c1']", "['c1', 'c3', 'c5', 'c2', 'c4']"], 0,
        "Even positions go to the front, odd ones to the back in reverse.",
        "A lost-in-the-middle reordering: the two best chunks (c1, c2) sit at the start and end where attention is strongest, and the weakest (c5) lands in the middle. The course: 'important chunks should never be buried in the middle'.",
        topic="context", level=3),
    out('prefill_tok_per_s = 4000\n'
        'base = 300 + 40                  # system + query\n'
        'for chunk, k in ((512, 5), (512, 10), (1024, 10)):\n'
        '    print(chunk, k, round((base + chunk * k) / prefill_tok_per_s, 2), "s")',
        ["512 5 0.72 s\n512 10 1.36 s\n1024 10 2.65 s",
         "512 5 0.64 s\n512 10 1.28 s\n1024 10 2.56 s",
         "512 5 0.72 s\n512 10 0.72 s\n1024 10 0.72 s",
         "512 5 2.88 s\n512 10 5.44 s\n1024 10 10.56 s"], 0,
        "TTFT ≈ prompt tokens / prefill rate.",
        "(340 + 2,560) / 4,000 = 0.72 s; (340 + 5,120) / 4,000 = 1.365 -> 1.36 and (340 + 10,240) / 4,000 = 2.645 -> 2.65 (float rounding). Doubling top_k or chunk size roughly doubles TTFT, in line with the course's 70B numbers. Decode time is unchanged.",
        topic="pipeline", level=3),
    mcq("A question: 'Who approves expenses for the team that owns the payments service?' needs one fact to find the team, then another to find its approver. Which RAG pattern fits?",
        ["Multi-hop (iterative, ReAct-style) retrieval: retrieve the owning team, then use that answer to retrieve its approver",
         "Multi-query fan-out of independent sub-queries in parallel",
         "A single retrieval with top_k = 50",
         "Long-context prompting with the whole wiki"], 0,
        "Does the second lookup depend on the first answer?",
        "Fan-out works when sub-queries are independent. Here step 2 needs step 1's result, so it is sequential: the same ReAct loop where the tool happens to be the retriever.",
        diagram="""
hop 1: retrieve "owner of payments service" -> Team Atlas
hop 2: retrieve "expense approver Team Atlas" -> R. Iyer
answer uses both hops
""",
        topic="self-correcting", level=3),
    fill("The course's rule: a grounded, cited, wrong answer is a ____ bug, not an LLM bug.", "retrieval",
         "Which stage chose the evidence?",
         "If the model faithfully cites what it was given and the answer is still wrong, the wrong evidence was retrieved (e.g. a superseded version). Fix the index or filters, not the prompt.",
         topic="diagnosis", level=3),
    tf("A team wants to add RAG so their bot always answers in the company's report format. The course's 'when not to use RAG' table suggests fine-tuning (or prompting) instead.", True,
       "Is the problem knowledge or behaviour?",
       "A fixed format is a small, stable, behavioural need: fine-tuning or a good prompt. RAG is for large, changing knowledge that needs citations.",
       topic="why-rag", level=3),
    # ------------------------------------------------------------------ L4
    mcq("In the heterogeneous-sources question, a student answers 'hybrid BM25 + dense' for the patient-table query (HbA1c > 8, with medications). Why does the answer key reject it?",
        ["Both components are text-similarity methods, so a hybrid inherits their limit: neither can evaluate a numeric predicate, join tables or preserve row identity",
         "Hybrid is too slow for 2M rows",
         "BM25 can't index numbers at all",
         "Dense retrieval can't be combined with BM25"], 0,
        "What does combining two text retrievers add?",
        "Hybrid fixes vocabulary mismatch and exact-term issues for text. Structured questions need a different kind of retriever: text-to-SQL or a tabular retriever executing WHERE / JOIN. This is the most common wrong answer on that question.",
        topic="retrievers", level=4),
    mcq("Why does the past paper's key match the cross-encoder reranker (not sliding windows or semantic chunking) to the 'old changelog ranks first' pattern?",
        ["The right chunk is already in BM25's top-10; the problem is ordering by lexical overlap, and only a model that reads query and passage together can rank by meaning",
         "Reranking makes chunks shorter",
         "Overlap would remove the changelog from the index",
         "Semantic chunking deletes old documents"], 0,
        "Is the problem the chunk boundaries or the ranking?",
        "Sliding windows and semantic chunking change what a chunk contains; neither changes the fact that BM25 scores the changelog higher. The reranker fixes precision within the candidate set. A version filter on old docs would be a sensible extra.",
        topic="diagnosis", level=4),
    out('import math\n'
        'idf = math.log10(3 / 2)\n'
        'k, b, avg = 1.5, 0.75, 11 / 3\n'
        'def s(tf, dl, plus1): return idf * tf * ((k + 1) if plus1 else 1) / (tf + k * (1 - b + b * dl / avg))\n'
        'docs = {"D1": [(3, 4), (1, 4)], "D2": [(0, 4), (2, 4)], "D3": [(1, 3), (0, 3)]}\n'
        'for plus1 in (False, True):\n'
        '    tot = {d: sum(s(tf, dl, plus1) for tf, dl in t) for d, t in docs.items()}\n'
        '    print(sorted(tot, key=tot.get, reverse=True), round(tot["D1"], 4))',
        ["['D1', 'D2', 'D3'] 0.1825\n['D1', 'D2', 'D3'] 0.4561",
         "['D1', 'D3', 'D2'] 0.1825\n['D1', 'D3', 'D2'] 0.4561",
         "['D1', 'D2', 'D3'] 0.1825\n['D2', 'D1', 'D3'] 0.4561",
         "['D1', 'D2', 'D3'] 0.1825\n['D1', 'D2', 'D3'] 0.1825"], 0,
        "Multiplying every term by the same (k + 1) can't change the order.",
        "The course's example scores D1 0.1825, D2 0.0978, D3 0.0767, so D1 > D2 > D3 (the slide's text 'D1 > D3 > D2' slips against its own numbers). The textbook (k + 1) numerator multiplies every score by 2.5: same ranking, larger numbers. Watch for this when an exam answer key uses one form.",
        topic="retrievers", level=4),
    out('doc_tokens = 100_000\n'
        'for size, overlap in ((512, 0), (512, 128)):\n'
        '    stride = size - overlap\n'
        '    n = len(range(0, doc_tokens - overlap, stride))\n'
        '    print(size, overlap, n)',
        ["512 0 196\n512 128 261", "512 0 195\n512 128 260", "512 0 196\n512 128 196", "512 0 196\n512 128 781"], 0,
        "Stride 512 vs 384.",
        "Without overlap: ceil(100,000 / 512) = 196 chunks. With 128 overlap, stride 384: 261 chunks, about 33% more to store, embed and index. The course quotes ~20-25% for typical overlap ratios; 25% overlap of the chunk costs a third more chunks, plus duplicate hits online.",
        topic="chunking", level=4),
    mcq("Your team calls a hosted generator through an API: you cannot fine-tune it. Answers must be checked against retrieved docs and recover when retrieval is bad. Self-RAG or CRAG, and why?",
        ["CRAG-style correction: an external retrieval evaluator plus corrective actions wraps any generator; Self-RAG needs a generator trained to emit reflection tokens",
         "Self-RAG, because reflection tokens can be added through the system prompt",
         "Neither; only fine-tuning can verify retrieval",
         "Self-RAG, because it needs no retriever"], 0,
        "Which one changes the model's weights?",
        "Self-RAG is a training recipe: the vocabulary and weights change. With a closed model you can only wrap it: evaluate retrieval, refine, re-retrieve, verify with CoVe. That is 'self-correcting RAG in the application layer'.",
        analogy="Like adding a validation middleware around a third-party service you can't modify.",
        topic="self-correcting", level=4),
    out('w = {"ISREL": 1.0, "ISSUP": 1.0, "ISUSE": 0.5}\n'
        'cands = {"A": {"logp": -1.2, "ISREL": 0.9, "ISSUP": 0.3, "ISUSE": 0.8},\n'
        '         "B": {"logp": -1.6, "ISREL": 0.8, "ISSUP": 0.9, "ISUSE": 0.6},\n'
        '         "C": {"logp": -0.9, "ISREL": 0.2, "ISSUP": 0.2, "ISUSE": 0.9}}\n'
        'score = {c: round(v["logp"] + sum(w[t] * v[t] for t in w), 2) for c, v in cands.items()}\n'
        'print(score, max(score, key=score.get))',
        ["{'A': 0.4, 'B': 0.4, 'C': -0.05} A",
         "{'A': 0.4, 'B': 0.4, 'C': -0.05} B",
         "{'A': 0.4, 'B': 0.5, 'C': -0.05} B",
         "{'A': -1.2, 'B': -1.6, 'C': -0.9} C"], 0,
        "On a tie, max() returns the first key it saw.",
        "Self-RAG's segment score = log-likelihood + weighted reflection scores. A: -1.2 + 0.9 + 0.3 + 0.4 = 0.4; B: -1.6 + 0.8 + 0.9 + 0.3 = 0.4; C: -0.05. C is fluent (highest logp) but irrelevant and unsupported. A and B tie; raising the ISSUP weight would pick B, the well-supported one, which is how users tune Self-RAG at inference.",
        topic="self-rag", level=4),
    tf("Self-RAG's ISSUP token can say a segment is fully supported, partially supported or not supported by the passage, rather than just yes/no.", True,
       "Support comes in degrees.",
       "ISSUP has three values; ISUSE is a 1-5 utility rating; Retrieve has yes/no/continue (reuse evidence). Partial support matters: an answer can be mostly grounded with one added claim, the same thing RAGAS faithfulness measures claim by claim.",
       topic="self-rag", level=4),
    mcq("A RAG answer scores faithfulness 1.0, yet the user's answer is wrong: the retrieved chunk is the 2022 policy, replaced in 2025. Which statement is right?",
        ["Faithfulness only checks entailment by the retrieved context; the answer is faithful but not truthful, so the fault is retrieval/indexing (stale version)",
         "A faithfulness of 1.0 proves the answer is correct",
         "The metric is broken and should be dropped",
         "The generator hallucinated"], 0,
        "Faithful to what?",
        "Faithfulness vs truthfulness: high faithfulness to wrong context is still wrong. Pair RAGAS with correctness checks on a labelled set, and fix freshness: remove superseded versions or filter by date.",
        analogy='Like a perfectly passing unit test written against an outdated spec.',
        topic="rag-metrics", level=4),
    mcq("Why is BERTScore not a good faithfulness metric for RAG, per the course's eval deck?",
        ["It is reference-based: it compares the candidate to a gold answer, never to the retrieved chunks, so a hallucinated claim whose meaning is close to the reference can still score high",
         "It is too slow to compute",
         "It only works for translation",
         "It needs human labels for every answer"], 0,
        "What is in the loop when BERTScore is computed?",
        "The RAG failure is 'claim not entailed by the retrieved chunks', which by definition needs the context in the loop. RAGAS faithfulness decomposes the answer into claims and checks each against the context.",
        topic="rag-metrics", level=4),
    tf("Context recall can be low even when context precision is 1.0.", True,
       "Every chunk relevant, but are all needed facts there?",
       "Precision 1.0: everything retrieved is relevant. Recall: did we get all needed facts? 2 relevant chunks covering 2 of 4 needed facts gives precision 1.0 and recall 0.5. Fix with more top-k, decomposition or better chunking, not a reranker.",
       topic="rag-metrics", level=4),
    fill("A model has a 16,000-token window. System + grounding take 1,000, kept history 3,000, generation headroom 2,000, and chunks average 800 tokens. At most ____ chunks fit.", "12",
         "Budget left for chunks, divided by chunk size, rounded down.",
         "16,000 - 1,000 - 3,000 - 2,000 = 10,000; 10,000 / 800 = 12.5 -> 12. That is a ceiling, not a target: fewer, better-ranked chunks usually answer better.",
         topic="context", level=4),
    tf("Once you pay for a model with a 1M-token window, sending 100K tokens of context per query costs about the same as sending 3K, because the window is already available.", False,
       "Is the window billed or the tokens?",
       "Pricing is per input/output token and every token is prefilled on every query, so 100K tokens cost ~33x the input of 3K and add seconds of TTFT, again and again. The course: '100K tokens of mostly irrelevant text, paid for again and again'.",
       topic="why-rag", level=4),
    tf("The right chunk is ranked #1 but the answer ignores it and answers from memory. Raising top_k from 5 to 15 is the right fix.", False,
       "Retrieval already succeeded.",
       "This is the course's 'context was ignored' transcript: a prompt fault. Add grounding and conflict rules, move the chunk out of the middle, trim history. More chunks would bury it further.",
       topic="diagnosis", level=4),
    mcq("A legal RAG bot's RAGAS scores: faithfulness 0.95, context precision 0.90, context recall 0.40. Users say answers are 'incomplete'. Where do you work first?",
        ["Retrieval coverage: the needed facts are not being retrieved, so look at chunking (facts split or truncated), top-k, hybrid search and query decomposition",
         "The grounding prompt, because faithfulness is not 1.0",
         "The reranker, to improve precision",
         "The generator's temperature"], 0,
        "Which score is the outlier?",
        "High faithfulness and precision mean the generator uses what it gets and what it gets is relevant. Recall 0.40 means most needed facts never arrive. A reranker can't add missing facts; fix what reaches the candidate set.",
        topic="diagnosis", level=4),
    fill("The course's retrieval accuracy in needle-in-a-haystack tests is worst when the fact sits at roughly 10-50% ____ of the document.", "depth",
         "How far into the document the needle is placed.",
         "Needle tests vary context length and the needle's depth. Recall dips in the middle depths: lost in the middle. Attention favours the start and end of the window.",
         topic="why-rag", level=2),
    fill("Prompt cost ≈ system + query + (chunk_size × ____) + output. Fill in the retrieval setting (use the underscore name).", "top_k",
         "How many chunks are retrieved.",
         "The retrieved slice is chunk_size × top_k. With top_k = 5, 512-token chunks add 2,560 tokens; it dominates once top_k > 3.",
         topic="pipeline", level=2),
    fill("Search methods that trade a little accuracy for a massive speed-up by looking only in the query's neighbourhood are called ____ (three-letter abbreviation).", "ANN",
         "Approximate Nearest ____.",
         "Approximate Nearest Neighbours: HNSW and IVF. Brute-force scanning is exact but O(N) and too slow past roughly 100K vectors.",
         topic="index-rerank", level=2),
    fill("Self-RAG's reflection token that judges whether a retrieved passage is relevant to the query is written ____.", "ISREL",
         "IS + RELevant.",
         "ISREL grades the passage; ISSUP grades whether the generated segment is supported by it; ISUSE rates usefulness; Retrieve decides whether to retrieve.",
         topic="self-rag", level=2),
    fill("Compressing retrieved context by deleting low-information tokens (as LLMLingua does with a small LM's perplexity) is called token ____.", "pruning",
         "Like pruning a tree.",
         "Token pruning keeps the remaining text verbatim but drops filler. It cuts prefill cost; aggressive settings can remove a negation or a number the answer needed.",
         topic="context", level=3),
    fill("DPR's bi-encoder score s(q, d) = z_q · z_d is a ____ product.", "dot",
         "The · symbol.",
         "Query and document are encoded independently; the score is a dot product, so document vectors can be precomputed and searched with ANN.",
         topic="retrievers", level=2),
    fill("An answer decomposes into 5 atomic claims, of which 4 are supported by the retrieved context. Its RAGAS faithfulness is ____ (decimal).", "0.8",
         "supported / total",
         "4 / 5 = 0.8. The unsupported claim is a hallucination relative to the context, even if it happens to be true in the world.",
         topic="rag-metrics", level=2),
    tf("IVF indexing clusters vectors with k-means at build time, so a query searches only the nearest clusters instead of the whole dataset.", True,
       "Inverted File Index.",
       "IVF suits very large corpora. Searching too few clusters lowers recall; searching more raises it at a latency cost.",
       topic="index-rerank", level=2),
    mcq("For 'Write a haiku about rain', a Self-RAG model emits Retrieve = no. Why is this a feature?",
        ["Retrieval is on demand: skipping it for tasks that need no facts saves cost and avoids distracting, irrelevant passages",
         "It means the retriever is broken",
         "Self-RAG never retrieves for short prompts",
         "It forces the model to hallucinate"], 0,
        "The course: 'LLM gets distracted by useless information'.",
        "Classic RAG retrieves for every query. Self-RAG's Retrieve token lets the model fetch evidence only when a segment needs facts, which also reduces the noise that hurts creative or general answers.",
        topic="self-rag", level=3),
    mcq("The course says 'reranking matters twice'. What are the two jobs?",
        ["It selects the best chunks and it helps place them at the highest-attention positions in the prompt",
         "It embeds the query and the documents",
         "It chunks the documents and builds the index",
         "It retrieves and generates"], 0,
        "Which chunks, and where.",
        "A good relevance order lets you send fewer chunks and put the strongest at the start or end of the context, away from the weak middle.",
        topic="index-rerank", level=3),
    # -- end --
]
