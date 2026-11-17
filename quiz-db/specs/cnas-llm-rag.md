# Language Models, LLMOps & RAG (S9-S11): coverage spec

**Ladder:** API-driven Cloud Native Solutions (AIMLCZG549) › Module 5 AI and Cognitive Services, Part B   ·   **Prerequisites:** cnas-ai-services (pre-trained vs fine-tuned, Hugging Face), cnas-ml-pipelines (MLflow tracking); llmc-foundations for tokenizer internals
**Why it matters for AI/ML:** Sessions 9-11 turn a language model into an application: pick an LLM or an SLM, call it through a hosted API with the right generation settings, track tokens, latency and cost (LLMOps), and ground it in company documents with a LangChain RAG pipeline. Lab 4 is exactly this: a RAG chatbot that answers questions about an uploaded document. The exam angle is the API and operations view: token cost in ₹, which endpoint family, which hyperparameter, fine-tuning vs RAG, the six RAG stages and the RAG metrics.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `language-models` | Language models and LLMs; training data | what an LM and an LLM are; NLU + NLG | what "large" means; web-scale data (Common Crawl) | what pre-training data implies (cut-off, bias, licence) | when an LLM is the wrong tool |
| 2 | `params-hyperparams` | Parameters vs hyperparameters | learned vs set by you | the decision-tree example (splits, leaves vs max_depth, min_samples_*, criterion) | parameter count -> memory; generation settings are hyperparameters, not parameters | where the slide blurs the line (tree depth) |
| 3 | `tokens-cost` | Tokens, the context limit and token-based cost | token = smallest unit; subwords | limit counts input + output; the 12-token example | ₹ cost per request and per month; input vs output prices | cost levers: shorter prompts, caching, smaller model, max_tokens |
| 4 | `llm-vs-slm` | LLMs vs SLMs, SLM advantages, MMLU | SLM = fewer parameters, cheaper | SLM advantages (fine-tuning to a domain, CPU/hardware limits); DistilBERT, TinyBERT, MiniLM | choosing LLM vs SLM for a use case; MMLU as a general-knowledge benchmark | the slide's size range vs today's ~1-8B SLMs; MMLU scores vs your task |
| 5 | `generation-params` | Generation hyperparameters: stream, temperature, top-p, top-k, max_tokens | what each knob does | temperature for QA vs creative text; top-p as nucleus | compute top-k / top-p candidate sets by hand | interactions (temperature + top-p), truncation by max_tokens, determinism |
| 6 | `llmops` | LLMOps and SLMOps | LLMOps = operating LLMs in production | what to log per call (latency, token counts, cost, model) | the SLMOps MLflow demo log; prompt/version tracking | monitoring drift, cost spikes and quality with logs |
| 7 | `llm-api` | A hosted LLM provider's API: endpoint families, keys, usage | the five endpoint families | access token (API key), usage dashboard, multi-turn chat | which endpoint for a requirement; JSONL fine-tuning data | key handling, rate limits, the legacy prompt/completion vs chat format |
| 8 | `finetune-vs-rag` | Context-based prompting vs fine-tuning vs RAG | three approaches | the slides' comparison table | choose for a scenario (changing data, GBs of docs, tone) | combining them; why fine-tuning is a poor knowledge store |
| 9 | `rag-architecture` | RAG: why, terms, architecture, embedding types, vector stores | RAG = retrieve then generate | prompt, context, retriever, embedding, vector store | embedding types (GloVe vs BERT vs Sentence-BERT vs DPR); vector stores (FAISS, Pinecone, Weaviate, Milvus, Elasticsearch kNN) | managed vs library vector store; same embedding model for docs and queries |
| 10 | `rag-stages` | LangChain and the six RAG stages | LangChain = framework for LLM apps; stage names | what each stage does in the demo (PdfReader -> raw_text, CharacterTextSplitter 1000/300, FAISS docsearch, similarity_search, chain, chat loop) | chunk counts with overlap; top-k choice; the key libraries | design flaws in the demo (re-indexing, no history, summarize chain for QA) |
| 11 | `rag-metrics` | RAG metrics: deflection rate, context precision/relevance/recall, faithfulness, answer relevancy | what each metric asks | compute deflection rate and context precision | read a metric profile and pick the fix | metric gaming and what needs ground truth |

## Must-know facts
- A language model understands and generates human language (NLU + NLG). An LLM is a deep learning model trained on very large text datasets (books, articles, web pages) to recognise, extract, summarise, predict and generate text.
- Parameters are learned from data (weights; in a decision tree the splits and leaf values); hyperparameters are set by you before or at run time (max_depth, min_samples_split, min_samples_leaf, criterion; for generation: temperature, top_p, max_tokens).
- Common Crawl is a free, open web corpus (since 2007, 250+ billion pages) used to build LLMs.
- Tokens are the smallest units the model processes, usually subwords ("unbelievable" -> "un", "believ", "able"). The context limit (e.g. 4,096) counts input and output tokens together, and providers bill per token, often with output tokens priced higher.
- SLMs have far fewer parameters than LLMs, need less compute, run on CPUs or small GPUs and are easy to fine-tune for a domain; LLMs are general-purpose.
- MMLU (Massive Multitask Language Understanding) is a benchmark of multiple-choice questions across 57 subjects used to compare models' general knowledge and reasoning.
- stream=True sends tokens as they are generated; temperature scales randomness (low = deterministic, high = diverse); top_p keeps the smallest set of tokens whose cumulative probability reaches p (nucleus sampling); top_k keeps the k most likely tokens; max_tokens caps the output length.
- LLMOps: the practices, techniques and tools for operating LLMs in production (data, prompts, fine-tuning, deployment, monitoring); the SLMOps demo logs model, question, latency, token counts, response length and estimated cost per call to MLflow.
- A hosted LLM provider's API has five endpoint families: chat/completion, embeddings, image generation, speech-to-text, fine-tuning. Calls need an API key; usage is tracked on a dashboard.
- Fine-tuning data is JSONL, one example per line (the slides use {"prompt", "completion"}; current chat fine-tuning uses a list of messages).
- Context-based prompting pastes a document into each prompt (limited to that document); fine-tuning bakes knowledge and style into weights (needs retraining when data changes); RAG retrieves relevant chunks on demand from a large corpus.
- RAG terms: prompt, context, LLM, retriever, embedding, vector store. Same embedding model for documents and queries.
- The six RAG stages: document loading, document splitting, vector stores and embedding, retrieval, question answering, chat.
- The demo: PdfReader extracts text into raw_text; CharacterTextSplitter makes 1,000-character chunks with 300 overlap; embeddings go into a FAISS index (docsearch) built once; similarity_search returns the top 10 chunks; a chain produces the answer; a loop keeps chatting until the user types "exit".
- Key libraries: LangChain (chaining), FAISS (similarity search), PyPDF2 (PDF text), the provider SDK (embeddings and LLM); Gradio for a web UI.
- Deflection rate = queries resolved by the bot without a human / total queries. Context precision = are the relevant chunks ranked at the top; context recall = did the retrieved context contain everything the reference answer needs; faithfulness = share of answer claims supported by the context; answer relevancy = does the answer address the question.

## Common traps (each one must have at least one question)
- Counting only the prompt against the context limit -> input + output share it.
- Pricing input and output tokens the same -> output tokens usually cost more.
- Calling temperature a model parameter -> it is a generation hyperparameter; weights do not change.
- Thinking temperature 0.5 restricts answers to the corpus -> temperature changes randomness, not knowledge; grounding comes from retrieval and the prompt.
- top_p = 0.7 read as "70% of the tokens" -> it is the smallest set whose probabilities sum to 0.7.
- max_tokens treated as a target length -> it is a hard cap that can cut an answer mid-sentence.
- Using fine-tuning to teach facts that change monthly -> use RAG; fine-tune for style and format.
- Embedding the documents with one model and queries with another -> similarities become meaningless.
- Chunk count computed as length / chunk_size when there is overlap -> the step is size - overlap.
- Rebuilding the FAISS index on every question -> build once (docsearch), reuse per query.
- High deflection rate taken as success -> the bot may be deflecting with wrong answers; pair it with faithfulness and CSAT.
- High faithfulness taken as a correct answer -> faithful to wrong or stale context is still wrong.
- GloVe treated as contextual -> one static vector per word.
- SLM size taken from the slide ("thousands to a few million parameters") -> today's SLMs are hundreds of millions to a few billion parameters.

## Interview angle
1. **"Our support bot must answer from 40 GB of manuals that change weekly. Fine-tune or RAG?"** RAG: retrieve the relevant chunks at query time; re-index when manuals change; fine-tune only for tone or format.
2. **"Estimate the monthly LLM bill."** Requests x (input tokens x input price + output tokens x output price); cut it with shorter prompts, fewer retrieved chunks, a max_tokens cap, caching and a smaller model where quality allows.
3. **"What settings for a factual QA bot?"** Low temperature (0-0.2), moderate top_p, a max_tokens cap, stream=True for UX, and a grounded prompt.
4. **"How do you know the RAG bot works?"** Retrieval metrics (context precision and recall), generation metrics (faithfulness, answer relevancy) on a labelled set, and business metrics (deflection rate, CSAT) in production.
5. **"LLM or SLM?"** SLM for narrow, high-volume, latency- or privacy-sensitive tasks on modest hardware; LLM for broad reasoning and open-ended tasks.

## Source material
- Old-batch slides p234-288 (`cloud-src/cnas-llm-rag.txt`), sessions 9-11, Module 5 Part B "Language Models".
- Language models and LLMs (definitions adapted from an NVIDIA beginner's guide); "what is large"; model parameters (with the decision-tree example) vs hyperparameters (max_depth, min_samples_split, min_samples_leaf, criterion); Common Crawl.
- Tokens and subword tokenization ("unbelievable"), the 4,096-token limit covering input and output, and the 12-token "capital of India" example.
- SLMs (scale, advantages: domain fine-tuning and efficient resource use), LLM vs SLM differences, popular SLMs (DistilBERT, TinyBERT, MiniLM and others), and the demo with a ~3.8B-parameter instruct SLM via Hugging Face APIs (token creation, chat interface, a Word-document chatbot compared with a distilled SQuAD QA model).
- SLM generation hyperparameters: stream=True, temperature=0.5 (QA 0.5 vs poem 0.8), max_tokens=1024, top_p=0.7 with the dragon example.
- LLMOps (definition from the Databricks glossary) and the SLMOps demo logging latency, token counts, response length and estimated cost to MLflow as JSON.
- A hosted LLM provider's API: five endpoint families (chat/completion, embeddings, image generation, speech-to-text, fine-tuning), access tokens, the usage dashboard, the base client setup, fine-tuning steps and the JSONL prompt/completion format with the dissertation example.
- Context-based approach vs fine-tuned model vs RAG model comparison tables; Rivet (visual prompt-graph environment).
- RAG: definition, why RAG, terms (prompt, context, LLM, retriever, embedding, vector store), simple and detailed architecture, embedding types (hosted-API embeddings, BERT, Sentence-BERT, DPR, GloVe), vector stores (Pinecone, FAISS, Weaviate, Milvus, Elasticsearch with kNN).
- LangChain; the six stages and Demo 1 (PDF upload, PdfReader -> raw_text, CharacterTextSplitter 1,000/300, embeddings into FAISS "docsearch", similarity_search top 10, load_summarize_chain, chat loop until "exit"); key libraries (LangChain, FAISS, PyPDF2, the provider SDK); Demo 2 with Gradio.
- Handout only: MMLU; RAG metrics deflection rate, context precision, context relevance. Recall, faithfulness and answer relevancy use the RAGAS definitions.
- No past papers; scenario style modelled on BITS WILP papers (Bengaluru food-delivery support bot, a Pune smart-city citizen helpdesk, a university dissertation FAQ bot, ₹ token costs).
- **Standard practice (slides thin):** MMLU details (57 subjects, multiple choice), top-k sampling (not on the slides), input vs output token pricing, RAGAS metric definitions and deflection rate, LLMOps monitoring practice, the modern chat-messages fine-tuning format, LangChain chain types.
- **Slide issues handled:** the SLM size range "thousands to a few million parameters" is outdated (current SLMs, including the ~3.8B demo model, are hundreds of millions to a few billion); "LLMs are general purpose [all tasks such as NLP, CV]" overstates (text LLMs handle language; vision needs multimodal models); temperature 0.5 for QA "since we want the answer from the corpus only" conflates randomness with grounding (factual QA usually uses 0-0.2, and grounding comes from retrieval); listing "tree depth" as a learned parameter is loose (depth results from training, max_depth is the hyperparameter); the {"prompt","completion"} fine-tuning format is the legacy completion format; the QA stage uses a summarize chain rather than a QA chain. Questions follow the standard facts and say so.
