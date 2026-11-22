# Multimodal Information Retrieval (AIMLC ZG543) — Study spec

> Search that works across text, images, audio and video: from BM25 to CLIP to multimodal RAG. · Status: spec only (not built yet)

## 1. What it is and why an AI engineer should care

Information retrieval (IR) is the science of search: given a query, return the most relevant items, ranked. This
course starts with classic text search (inverted index, BM25), moves to modern dense retrieval (embeddings, FAISS,
re-rankers), and then extends the same ideas to images, audio and video. It ends with fusion (combining modalities),
cross-modal search (type text, get images, as CLIP does) and multimodal RAG. Retrieval is the backbone of every RAG
system, product search and recommendation feed, so this is one of the most practical electives for an AI engineer.

**Job relevance: 4/5** — text and image retrieval, vector indexes and evaluation are core RAG and search skills; video and music retrieval are more niche.

## 2. Sources in this folder

| Kind | File (relative path) | Notes |
|---|---|---|
| Handout (current) | `handouts/Handout - MIR - 27-Mar-2026 version 2.docx` | First Semester 2026-2027, course AIMLC ZG543, author Prof. Vimal S P, instructors Prof. Dhruba Adhikary and Prof. V. Maheswari, 16 sessions, 6 labs, exam dates given |
| Handout (older batch) | `handouts/Older batch - Multimodal Information Retrieval (S2-25_AIMLCZG543) COURSE HANDOUT.pdf` | Same content (v2.0, 27/03/2026, AIML ZG543); has per-module hours, used below |
| Book | `books/Multimodality Representation Learning - A Survey on Evolution, Pretraining and Its Applications.pdf` | Handout reference R3 |
| Book | `books/Introduction to audio analysis a MATLAB approach{Theodoros Giannakopoulos _ Aggelos Pikrakis}(2014, Academic Press){115638723} libgen.li.pdf` | Handout reference R5 (Giannakopoulos & Pikrakis) |

Differences (current wins): current handout lists instructors, exam dates (mid-sem 26-12-2026, compre 06-03-2027) and
says "public dataset" for labs 3 and 4, where the older one names ESC-10 and UCF-10 / YouTube-8M small subset; current
EC-1 = "two assignments and two quizzes", older = "either two assignments or three quizzes". Module hours appear only in
the older one.

Gaps: no slides, no past question papers, no lab sheets (only lab objectives).

## 3. Running scenario

**NewsVault** is the archive team of a large Indian news network. It holds 2 million articles, 5 million photos,
80,000 podcast and radio clips, and 300,000 TV video segments. Today journalists search only by headline keywords, so
"flood rescue boat photos from Assam 2022" returns nothing useful. The goal: one search box that takes text (or an
image, or a hummed jingle) and returns ranked articles, photos, audio and video moments, plus an "answer with sources"
mode for quick research. Every module adds one capability to NewsVault search.

## 4. Module map

Hours are per module from the older handout (same modules in the current one). Total 28 h of contact.

### M1 · Foundations of IR, multimodal IR motivation and evaluation basics (≈2 h, session 1)

Topics: classical IR pipeline (documents, queries, ranking, relevance); Boolean, vector space, probabilistic and BM25
models; precision, recall, MAP, nDCG; multimodal objects (text, image, audio, video, point cloud, knowledge graph);
limits of text-only search; application scenarios.

| Concept | One-line definition (≤20 words, no jargon) | Analogy |
|---|---|---|
| Relevance | Whether a returned item actually satisfies the user's need, judged by humans. | The acceptance criteria of a ticket |
| Precision / recall | Share of returned items that are relevant / share of relevant items that were returned. | False alarms vs missed alerts in monitoring |
| MAP | Mean of average precision over queries; rewards putting relevant items early. | Scoring a search page, not one result |
| nDCG | Ranking score with graded relevance, discounting items that appear lower in the list. | Page-one results matter, page five barely |
| Vector space model | Documents and queries as term-weight vectors, ranked by cosine similarity. | Comparing two feature flags arrays |
| Multimodal object | An item whose content is not just text: image, audio, video, 3D, graph. | A row with BLOB columns, not only strings |

Diagram ideas:
- IR pipeline: collection → index → query → ranking → results → relevance judgments → metrics.
- Precision-recall curve with the MAP area shaded.
- nDCG worked example table for one query (gains, discounts, ideal order).

Scenario step: label 40 journalist queries with relevant items; measure today's keyword search (baseline MAP).

Notebook idea: implement precision@k, recall@k, AP, MAP and nDCG from scratch in numpy; check against `sklearn.metrics.ndcg_score`. CPU.

Production angle: offline eval sets, click logs, A/B tests. Breaks: the offline metric goes up but users click less,
because the judgment set no longer matches real queries.

### M2 · Textual information retrieval (≈4 h, sessions 2–3)

Topics: tokenisation, normalisation, stopwords, stemming, lemmatisation; inverted and positional indexes; phrase and
proximity queries; query expansion; BM25 ranking; cosine and dot product; dense retrieval (DPR, bi-encoders, ColBERT);
generative retrieval; cross-encoder re-ranking in two-stage pipelines; FAISS, HNSW, product quantisation; MRR,
precision@k, query likelihood.

| Concept | One-line definition (≤20 words, no jargon) | Analogy |
|---|---|---|
| Inverted index | A map from each word to the list of documents (and positions) containing it. | The index at the back of a book |
| BM25 | Keyword score that rewards rare query terms, saturates repeats and normalises for document length. | A tuned `grep` ranking |
| Bi-encoder (dense retrieval) | Encode query and documents separately into vectors; nearest vectors are the results. | Precomputed hash lookups, but by meaning |
| Cross-encoder re-ranker | Reads query and document together to score relevance; accurate but too slow for the whole corpus. | A senior reviewer who only sees the shortlist |
| ColBERT | Keeps one vector per token and matches query tokens to their best document tokens (late interaction). | Matching every field of two records, not one checksum |
| HNSW | A layered graph index that finds approximate nearest vectors in milliseconds. | A skip list for vectors |
| Product quantisation | Compress vectors by splitting them into chunks and storing a short code per chunk. | Dictionary encoding of a column |
| MRR | Average of 1/rank of the first relevant result. | How far down the user must scroll |

Diagram ideas:
- Inverted index with postings lists and positions for a 3-document example.
- Two-stage pipeline: BM25/bi-encoder top-100 → cross-encoder top-10.
- Bi-encoder vs cross-encoder vs ColBERT side by side (where the query and document meet).

Scenario step: articles become searchable by meaning, not only exact headline words.

Notebook idea: lab 1 replica: BM25 (`rank_bm25`) vs `all-MiniLM-L6-v2` bi-encoder on 20 Newsgroups, then a
`cross-encoder/ms-marco-MiniLM-L-6-v2` re-ranker; FAISS Flat vs HNSW vs IVF-PQ speed/recall table. CPU.

Production angle: Elasticsearch/OpenSearch, Vespa, FAISS, Qdrant, Milvus. Breaks: re-ranker latency explodes when top-k
is raised from 50 to 500 under load.

### M3 · Multimodal systems (≈2 h, session 4)

Topics: modality-specific encoders and integration strategies; representations for text, image, audio, video, point
cloud, knowledge graph; representation alignment and the modality gap; challenges: semantic alignment, missing
modalities, noise.

| Concept | One-line definition (≤20 words, no jargon) | Analogy |
|---|---|---|
| Modality encoder | A model that turns one kind of input (image, audio) into a vector. | A per-format parser feeding one data model |
| Alignment | Making vectors of matching items from different modalities land close together. | Mapping two services' user IDs to one ID |
| Modality gap | Image and text vectors cluster in separate regions even after alignment. | Two teams' metrics on different scales |
| Modality incompleteness | Some items lack a modality (a photo with no caption). | Nullable columns |
| Semantic gap | Low-level features (pixels, samples) do not directly say what the content means. | Bytes vs business meaning |

Diagram ideas:
- Encoders per modality feeding an integration box (early, late, shared space).
- 2-D scatter (PCA) of CLIP image and text embeddings showing the modality gap.

Scenario step: design NewsVault's architecture: one encoder per archive type, one shared index.

Notebook idea: embed 200 images and their captions with CLIP (`sentence-transformers/clip-ViT-B-32`), PCA plot, measure
the gap between modality centroids. CPU (slow but fine).

Production angle: multi-vector stores with per-modality fields. Breaks: missing captions silently drop items from
text-only queries.

### M4 · Visual information retrieval (≈4 h, sessions 5–6)

Topics: image as a 2-D grid, encodings, semantic gap; colour histograms and texture features; CNN and ViT embeddings;
object-aware and region-level descriptors; content-based image retrieval (CBIR); image indexing, ANN search, ranking;
region-based and semantic retrieval; P@K, mAP, MRR.

| Concept | One-line definition (≤20 words, no jargon) | Analogy |
|---|---|---|
| Colour histogram | Counts of pixels per colour bin; a cheap global description of an image. | A word-count vector for pictures |
| CNN / ViT embedding | The vector from a pretrained vision model's last layers, capturing what is in the image. | A learned fingerprint |
| CBIR | Search images by an example image instead of words. | "Find similar" on a product page |
| Region-level descriptor | Embeddings of detected objects or patches, so small objects can be matched. | Indexing each field, not the whole document |
| ANN for images | Approximate nearest-neighbour index over image embeddings for fast lookup. | Same HNSW, different vectors |

Diagram ideas:
- Feature ladder: pixels → histogram → CNN features → ViT patch tokens.
- CBIR flow: query image → encoder → FAISS → top-k grid.

Scenario step: "find more photos like this one" for the photo desk.

Notebook idea: lab 2 replica: ResNet-18 and ViT embeddings (`torchvision`, `timm` or HF) on a 5,000-image CIFAR-10 subset,
FAISS index, P@10 and mAP, compared with colour histograms. CPU, about 10–15 min.

Production angle: FAISS/Milvus, near-duplicate detection, perceptual hashes. Breaks: crops and watermarks make
near-duplicates look different to global embeddings.

### M5 · Audio information retrieval (≈4 h, sessions 7, 9)

Topics: audio as a 1-D time series, sampling, encoding, semantic gap; mel spectrogram and MFCC; chroma and rhythm
features; deep audio embeddings; audio similarity and indexing; spoken term search; music and melody retrieval;
environmental sound tagging; audio retrieval pipeline; MAP, P@K, accuracy.

| Concept | One-line definition (≤20 words, no jargon) | Analogy |
|---|---|---|
| Sampling rate | How many amplitude readings per second are stored (16 kHz = 16,000). | Frame rate for sound |
| Mel spectrogram | Energy per frequency band over time, with bands spaced the way human hearing works. | A heat map of sound |
| MFCC | A compact summary of the mel spectrogram's shape per frame, ~13 numbers. | A compressed audio fingerprint per frame |
| Chroma | Energy per musical note (12 pitch classes), ignoring octave. | Grouping by key, not exact value |
| Spoken term search | Finding where a word is spoken in audio, usually via speech-to-text then text search. | Full-text search over transcripts |
| Audio embedding | A vector for a clip from a pretrained audio model (e.g. PANNs, CLAP). | Image embedding, for sound |

Diagram ideas:
- Waveform → frames → FFT → mel filter bank → log → DCT = MFCC.
- Two retrieval paths: speech (ASR → text index) vs sound/music (embedding → ANN).

Scenario step: find every radio clip where "Brahmaputra" is spoken; find the network jingle by sound.

Notebook idea: lab 3 replica: `librosa` MFCC + mel features on ESC-10 (small, public), mean-pooled vectors, cosine top-k,
MAP. CPU.

Production angle: Whisper transcripts into a text index, audio fingerprinting (Chromaprint). Breaks: different sample
rates between index and query silently shift features.

### M6 · Video information retrieval (≈4 h, sessions 10–11)

Topics: frames, shots, clips, temporal organisation; transformer video embeddings (VideoMAE, InternVideo, VideoCLIP);
clip- and video-level embeddings; action and event representations; cosine and temporal distance; shot boundary
detection and key-shot selection; video retrieval pipeline; mAP, recall@k, temporal IoU.

| Concept | One-line definition (≤20 words, no jargon) | Analogy |
|---|---|---|
| Shot | A continuous run of frames from one camera take, between two cuts. | A paragraph in a document |
| Shot boundary detection | Finding cuts by large frame-to-frame changes (e.g. histogram difference). | Detecting log session boundaries |
| Key frame / key shot | Representative frames chosen to index a shot cheaply. | A thumbnail per chapter |
| Clip embedding | One vector for a short segment, from a video model or averaged frame embeddings. | A summary row per time window |
| Temporal IoU | Overlap of predicted and true time ranges divided by their union. | Overlap of two calendar meetings |

Diagram ideas:
- Video → shots → key frames → embeddings → index, with timestamps kept.
- Temporal IoU drawn as two overlapping bars on a timeline.

Scenario step: return the exact 20-second segment of a TV bulletin showing the rescue boat.

Notebook idea: lab 4 style: detect shots in a short public video with OpenCV histogram differences, CLIP-embed one key
frame per shot, text query → segment with timestamps, compute temporal IoU on 5 hand labels. CPU.

Production angle: FFmpeg, PySceneDetect, Twelve Labs-style video search. Breaks: indexing every frame blows up storage
and cost; sample key frames instead.

### M7 · Multimodal retrieval — early and late fusion (≈2 h, session 12)

Topics: early fusion (feature-level, joint representation); late fusion (score-level and rank-level); learned fusion
(attention, MLP); modality weighting, normalisation, calibration.

| Concept | One-line definition (≤20 words, no jargon) | Analogy |
|---|---|---|
| Early fusion | Concatenate features from modalities into one vector before retrieval. | Denormalising into one wide table |
| Late fusion | Retrieve per modality, then combine the scores or ranks. | Merging results from several microservices |
| Score normalisation | Rescale each modality's scores (min-max, z-score) so they are comparable. | Converting currencies before summing |
| Rank fusion (RRF) | Combine by rank positions, avoiding score-scale problems. | Merging leaderboards by position |
| Learned fusion | A small network learns how much to trust each modality per query. | A learned load-balancer weight |

Diagram ideas:
- Early vs late fusion block diagrams side by side.
- Worked table: raw scores, min-max normalised, weighted sum, RRF.

Scenario step: one query searches article text and photo embeddings and merges the results.

Notebook idea: lab 5 replica with precomputed 20 Newsgroups text and CIFAR-10 image embeddings; compare early, late
(weighted sum) and RRF by MAP. CPU.

Production angle: hybrid search with weighted or RRF fusion in Elasticsearch/Vespa. Breaks: one modality's scores are
on a larger scale and silently dominate the fused ranking.

### M8 · Cross-modal retrieval and deep architectures (≈4 h, sessions 13–14)

Topics: text-image, text-audio, text-video retrieval; shared embedding spaces, metric learning, contrastive learning;
dual encoders and CLIP-style alignment; bridging the modality gap; multimodal transformers and vision-language
pretraining; multimodal LLMs (MLLMs) for retrieval; prompt-based and zero-shot retrieval; multimodal RAG.

| Concept | One-line definition (≤20 words, no jargon) | Analogy |
|---|---|---|
| Shared embedding space | One vector space where text and images about the same thing are close. | One schema all services write to |
| Contrastive learning | Train by pulling matching pairs together and pushing non-matching pairs apart. | Learning faces by "same person / different person" |
| CLIP | A dual encoder trained on image-caption pairs with contrastive loss; enables zero-shot search. | A translator between pictures and words |
| Zero-shot retrieval | Searching for categories the model was never explicitly trained on. | A generic API that needs no per-client code |
| MLLM | A language model that also accepts images (or audio) as input. | An LLM with extra input ports |
| Multimodal RAG | Retrieve images, tables or clips as context, then let an MLLM answer with them. | RAG whose documents include screenshots |

Diagram ideas:
- CLIP training matrix: N images x N captions, diagonal = positives.
- Multimodal RAG flow: query → retrieve text + images → MLLM → cited answer.

Scenario step: type "flood rescue boat" and get photos and video moments with no captions needed; then "answer with sources".

Notebook idea: lab 6 replica: zero-shot CLIP text→image retrieval on CIFAR-10, precision@10 per class; tiny InfoNCE loss
written in torch on random vectors. CPU. MLLM answering step optional via a small local model or read only.

Production angle: CLIP/SigLIP, ColPali for document images, vector DBs with multimodal fields. Breaks: CLIP fails on
domain-specific terms (local place names, Indian-language text in images).

### M9 · Evaluation, challenges, ethics and future directions (≈2 h, session 15)

Topics: benchmark datasets and experimental protocol; human evaluation and annotation for multimodal relevance; bias,
domain shift, scalability, robustness, interpretability; privacy and ethics (reverse image search, audio
fingerprinting, copyright); future: multimodal foundation models, conversational search, multimodal RAG.

| Concept | One-line definition (≤20 words, no jargon) | Analogy |
|---|---|---|
| Experimental protocol | Fixed queries, judged relevance and metrics so systems are compared fairly. | A benchmark harness with pinned versions |
| Inter-annotator agreement | How often human judges agree on relevance (e.g. Cohen's kappa). | Two reviewers approving the same PR |
| Domain shift | Real queries or content differ from what the model was trained or tested on. | Prod traffic unlike staging |
| Retrieval bias | Some groups or sources are systematically ranked lower or higher. | A load balancer that always favours one node |
| Reverse image search risk | Finding a person from a photo can enable stalking or privacy harm. | Data that should be access-controlled but is public |

Diagram ideas:
- Evaluation protocol flow: sample queries → pool results → annotate → compute metrics → significance test.
- Risk map: privacy, copyright, bias vs mitigations.

Scenario step: sign-off report for NewsVault: metrics per modality, failure cases, a face-search policy.

Notebook idea: compute Cohen's kappa for two simulated annotators; bootstrap confidence intervals for MAP difference between
two systems. CPU.

Production angle: annotation tools (Label Studio), online metrics. Breaks: no one re-judges queries after the content
mix changes, so the eval set goes stale.

## 5. Codebase plan

`newsvault-search`: a local multimodal search service over a small sample archive.

```
codebase/
├── README.md                    how to run; which module added which file           (M1)
├── data/fetch_samples.py        20NG text, CIFAR-10 subset, ESC-10 clips, one video  (M1)
├── src/newsvault/
│   ├── metrics.py               P@k, recall@k, AP, MAP, nDCG, MRR, temporal IoU      (M1, M6)
│   ├── text_index.py            BM25 + bi-encoder + cross-encoder re-rank            (M2)
│   ├── vector_store.py          FAISS wrapper (Flat, HNSW, IVF-PQ)                   (M2)
│   ├── image_index.py           CNN / CLIP image embeddings                          (M4, M8)
│   ├── audio_index.py           MFCC / mel features + embeddings                     (M5)
│   ├── video_index.py           shot detection + key-frame embeddings                (M6)
│   ├── fusion.py                early, late, RRF fusion                              (M7)
│   └── api.py                   FastAPI /search?q=&modality=                         (M7, M8)
└── tests/
    ├── test_metrics.py          metric values on hand-made examples                 (M1)
    ├── test_text_index.py       BM25 finds exact codes; dense finds paraphrases     (M2)
    ├── test_fusion.py           normalisation stops one modality dominating         (M7)
    └── test_cross_modal.py      CLIP P@10 above threshold                           (M8)
```

## 6. Practice topics plan

1. 01 IR evaluation metrics — M1 — 3 h
2. 02 Sparse retrieval: inverted index and BM25 — M2 — 4 h
3. 03 Dense retrieval, re-ranking and vector indexes — M2 — 5 h
4. 04 Image retrieval (CBIR) — M3, M4 — 4 h
5. 05 Audio retrieval: MFCC to similarity search — M5 — 4 h
6. 06 Video retrieval: shots, key frames, temporal IoU — M6 — 4 h
7. 07 Fusion: early, late, RRF — M7 — 3 h
8. 08 CLIP and cross-modal search — M3, M8 — 4 h
9. 09 Multimodal RAG and evaluation protocol — M8, M9 — 4 h

## 7. Exam signal

No past question papers in this folder. Evaluation scheme (current handout):

| Component | Type | Weight | When |
|---|---|---|---|
| EC-1 Quizzes | Online | 10% | Nov 23 – Dec 02, 2026 |
| EC-1 Assignments | Online | 20% | Jan 18 – Jan 27, 2027 |
| EC-2 Mid-Semester Test | Closed book, 2 h | 30% | 26-12-2026 (EN) |
| EC-3 Comprehensive Exam | Open book, 2.5 h | 40% | 06-03-2027 (EN) |

Mid-sem covers sessions 1–8 (M1–M5 feature extraction), closed book: memorise metric formulas (P@k, AP, nDCG, MRR) and
BM25. Open book compre allows publisher copies of text/reference books only.

## 8. Interview angle

1. **Bi-encoder vs cross-encoder?** Bi-encoder embeds separately and is fast for search; cross-encoder reads both together, accurate, used to re-rank.
2. **Why keep BM25 in a RAG stack?** It catches exact names, codes and rare terms that embeddings blur.
3. **What does HNSW trade?** A little recall and extra memory for millisecond search on millions of vectors.
4. **Explain nDCG.** Graded relevance summed with a log discount by rank, divided by the ideal ordering's score.
5. **How does CLIP work?** Image and text encoders trained contrastively on pairs, so matching pairs share a space.
6. **Early vs late fusion?** Early merges features before retrieval; late merges per-modality scores or ranks after.
7. **How would you search video?** Split into shots, embed key frames or clips with timestamps, index, return segments.
8. **What is product quantisation for?** Compressing vectors many times over so billions fit in memory, at some accuracy cost.
9. **How do you evaluate a new retriever before launch?** Fixed judged query set, offline metrics with confidence intervals, then an online A/B test.
10. **What is the modality gap?** Image and text embeddings occupy separate regions even in a shared space, hurting mixed ranking.

## 9. Repetition plan

| Concept | First met (module) | Revisited in (modules) |
|---|---|---|
| Precision@k / MAP | M1 | M2, M4, M5, M6, M9 (each modality's evaluation) |
| Embedding + cosine | M2 | M3, M4, M5, M6, M8 |
| ANN index (HNSW, PQ) | M2 | M4 (images), M5 (audio), M6 (video) |
| Two-stage retrieve then re-rank | M2 | M8 (multimodal RAG) |
| Semantic gap | M3 | M4, M5, M6 |
| Alignment / modality gap | M3 | M7 (fusion), M8 (CLIP) |
| Score normalisation / RRF | M7 | M8, M9 |
| Domain shift | M8 (CLIP failures) | M9 |

## 10. Overlap with my other courses

- [../../natural-language-processing/](../../natural-language-processing/) — TF-IDF, cosine, embeddings (revision ch02–ch03) underpin M2.
- [../../llm-engineering/](../../llm-engineering/) — RAG and embedding use in LLM apps builds on M2 and M8.
- [../../nlp-applications/](../../nlp-applications/) — QA and text processing pipelines (tokenisation, stemming) in M2.
- [../conversational-ai/](../conversational-ai/) — its M1 hybrid search and M2 RAG reuse BM25, HNSW, PQ and re-ranking from here.
- [../audio-analytics/](../audio-analytics/) — MFCC, mel spectrograms and audio features for M5, with labware.

## 11. Build checklist

- [ ] SPEC reviewed
- [ ] cards.json (M1…M9, 5–10 cards each)
- [ ] practice/01 IR evaluation metrics
- [ ] practice/02 Sparse retrieval
- [ ] practice/03 Dense retrieval, re-ranking and vector indexes
- [ ] practice/04 Image retrieval
- [ ] practice/05 Audio retrieval
- [ ] practice/06 Video retrieval
- [ ] practice/07 Fusion
- [ ] practice/08 CLIP and cross-modal search
- [ ] practice/09 Multimodal RAG and evaluation protocol
- [ ] codebase/ runs + tests

Total estimated study hours: ≈ 35 h practice + ≈ 12 h codebase + ≈ 5 h cards/revision = **≈ 52 h**.
