# Quiz bank progress

Read this first in every quiz-creation session. Update it at the end.

## Round 2: deepen every subject (started 15-Nov-2026, finished 16-Nov-2026)

Target: 120-160 questions per subject, with more L3/L4, informative explanations and a real ML-code topic per subject.

| Rung | Subject | Round 1 | Round 2 | Status |
|------|---------|---------|---------|--------|
| Foundations | py-basics | 73 | 148 | done, pushed |
| Foundations | py-variables | 78 | 155 | done, pushed |
| Foundations | py-strings | 87 | 153 → 193 → 233 (round 3) | done, pushed |
| Foundations | py-lists | 80 | 158 → 198 (round 3) | done, pushed |
| Foundations | py-dicts | 70 | 146 → 186 → 226 (round 3) | done, pushed |
| Foundations | py-conditions | 71 | 151 → 191 → 231 (round 3) | done, pushed |
| Foundations | py-loops | 73 | 149 | done, pushed |
| Foundations | py-functions | 67 | 150 | done, pushed |
| Foundations | py-comprehensions | 61 | 136 | done, pushed |
| Foundations | py-errors | 104 | 167 | done, pushed |
| Foundations | py-classes | 108 | 192 → 233 → 273 (round 3) | done, pushed |
| Foundations | np-arrays, np-operations | 139, 153 | 203 → 243, 215 → 255 (round 3) | done, pushed |
| Foundations | pd-dataframes, pd-cleaning | 151, 163 | 194 → 234 → 274, 208 → 248 → 288 (round 3) | done, pushed |
| Foundations | plotting | 99 | 152 | done, pushed |
| L1 | ml-what | 69 | 126 | done, pushed |
| L1 | ml-types | 65 | 122 | done, pushed |
| L1 | ml-data | 72 | 159 | done, pushed |
| L1 | ml-splits | 90 | 160 | done, pushed |
| L1 | ml-overfitting | 76 | 130 | done, pushed |
| L1 | ml-metrics | 94 | 148 | done, pushed |
| L1 | ml-models | 88 | 157 | done, pushed |
| L2 | dl-neuron, dl-loss-gd | 77, 76 | 132, 128 | done, pushed |
| L2 | dl-training | 85 | 144 | done, pushed |
| L3 | nlp-tokens, nlp-embeddings | 98, 95 | 139, 137 | done, pushed |
| L3 | tf-attention, tf-generation | 86, 83 | 131, 131 | done, pushed |
| L4 | llm-prompting, llm-rag | 65, 65 | 130, 130 | done, pushed |
| L4 | llm-finetuning | 63 | 131 | done, pushed |
| L5 | ops-serving, ops-monitoring | 91, 80 | 134, 137 | done, pushed |

Pushed: commit `64243d4` on branch `quiz-db` (7,335 questions). The `aiml_quiz` database is loaded from that commit (16-Nov-2026).

**Round 2 is complete for all 35 ladder subjects.** Next: new subjects from the course material (llm-engineering, nlp-applications, machine-learning-on-the-edge, api-driven-cloud-native-solutions). Each needs a structure.py entry and a spec built from its materials folder.

## Course banks: LLMs for Generative AI (AIMLCZG536), started 16-Nov-2026

Category `courses` (ladder_level 6), section `llm4genai`, 11 subjects in structure.py. Sources: session notes 0-3, current decks, complete old-batch slides and 8 past papers. Text extracts live in `C:/dev/quizdb-tools/llm-src/`, outside the repo; the writer brief is `C:/dev/quizdb-tools/llm-course-brief.md`. Target is 80-100 questions each.

| Module | Subject | Count | Status |
|--------|---------|-------|--------|
| M1 | llmc-foundations | 96 | done, pushed |
| M2 | llmc-pretraining | 98 | done, pushed |
| M3 | llmc-architecture | 92 | done, pushed |
| M4-5 | llmc-inference | 99 | done, pushed |
| M6 | llmc-finetuning | 96 | done, pushed |
| M6 | llmc-alignment | 91 | done, pushed |
| M7 | llmc-prompting | 100 | done, pushed |
| M8 | llmc-rag | 100 | done, pushed |
| M9 | llmc-agents | 105 | done, pushed |
| M10 | llmc-eval | 92 | done, pushed |
| M11 | llmc-safety | 92 | done, pushed |

All 11 were pushed together in `4a44ea7` (1,061 questions).

Course-material quirks the explanations point out:
- The BM25 slide drops the (k+1) factor and states the wrong final ranking.
- The slides round the MLA saving of about 57x to 55x.
- The KV-cache table says GB where it means GiB.
- The ShopSmart answer key calls an adversarial suffix "prompt injection".

Topics the slides barely cover use standard practice, flagged in each spec: differential privacy, Self-RAG token names, text-to-SQL safety.

**Next (course banks):** all four course folders now have banks. Remaining: top up course banks when new material arrives (LLM sessions 4+, current-batch cloud-native slides/papers), and the Known follow-ups below. The edge Module 1 top-up is done; **next** is the Module 2+ edge slides when they arrive.

## Course banks: NLP Applications (AIMLCZG519), started 16-Nov-2026

Section `nlpapps` under `courses`, with 9 subjects in structure.py, all marked `ready`. Ship them together, or set unfinished ones to `planned`. Sources: current S1-S2 slides and notebook, two old-batch slide sets, 10 past papers and lecture 1-2 transcripts. Text extracts are in `C:/dev/quizdb-tools/nlp-src/`; the writer brief is `C:/dev/quizdb-tools/nlp-course-brief.md`.

| Sessions | Subject | Count | Status |
|----------|---------|-------|--------|
| S1 | nlpa-overview | 87 | done, pushed |
| S2 | nlpa-spellgrammar | 100 | done, pushed |
| S3-4 | nlpa-rag | 90 | done, pushed |
| S5-6 | nlpa-qa-conv | 90 | done, pushed |
| S7 | nlpa-sentiment | 100 | done, pushed |
| S8 | nlpa-ethics | 93 | done, pushed |
| S10-12 | nlpa-mt | 100 | done, pushed |
| S13-14 | nlpa-ie | 100 | done, pushed |
| S15 | nlpa-efficient | 88 | done, pushed |

All 9 were pushed together in `64243d4` (848 questions). The writers found these course-material errors; each explanation states the correct fact:
- **Spellcheck:** d(speling, spring) is 2, not 3. d(pulp, hello) is 4. d(bok, cake) is 3. The F-score formula is missing its factor of 2. "fone/phone" is not a Soundex match. The Dec 2025 paper's "recieved" case is really a transposition plus a deletion.
- **MT:** the EM slide counts only 1-to-1 alignments, so it is wrong from iteration 2. The BLEU r should be the closest reference length. rivière and fleuve are swapped.
- **Sentiment:** the MCC slide is missing its square root.
- **Ethics:** the slides mislabel Amazon Rekognition, the cropping model and Clearview, and give the GDPR fine in $ instead of EUR.

Thin-slide topics use the textbook (J&M) and say so in each spec: Graph RAG internals, dialogue state tracking, HMM/CRF, DP/model cards, S15 compression.

## Course banks: Machine Learning on the Edge (AIMLCZG535), started 16-Nov-2026

Section `mledge` under `courses`, 8 subjects (one per handout module) in structure.py, all `ready`. Sources: the current handout (16-session plan, 7 labs) and 4 past papers (Jun 2026 midsem sets 1-2, Sep 2026 endsem sets 1-2). **No slides exist yet**, so the material beyond the handout and papers is standard practice or textbook T1, flagged in each spec. Text extracts are in `C:/dev/quizdb-tools/edge-src/` (the .doc papers were converted with antiword); the writer brief is `C:/dev/quizdb-tools/edge-course-brief.md`.

| Module | Subject | Count | Status |
|--------|---------|-------|--------|
| M1 | edge-foundations | 145 | done, pushed (top-up 17-Nov) |
| M2 | edge-hardware | 102 | done, pushed (top-up 17-Nov) |
| M3 | edge-data-iot | 95 | done, pushed |
| M4 | edge-deployment | 114 | done, pushed (webinar top-up 19-Nov) |
| M5 | edge-mlops | 95 | done, pushed |
| M6 | edge-optimization | 115 | done, pushed (webinar top-up 19-Nov) |
| M7 | edge-security | 94 | done, pushed |
| M8 | edge-benchmarking | 120 | done, pushed (webinar top-up 19-Nov) |

**Top-up, 17-Nov-2026, pushed `50aea96`.** New material: the CS1 slides (Module 1, 39 slides), transcripts for S1-3 and the learner's S1-3 notes (extracts in `C:/dev/quizdb-tools/edge-src/new/`). edge-foundations went 90 → 145 (+55, 21 edited), edge-hardware 90 → 102 (+12).
- **Framework resolved:** the paper's "five-question deployment framework" is BLERP (bandwidth, latency, economics, reliability, privacy) applied letter by letter; connectivity sits under Reliability. The decision questions now use BLERP.
- **Still unconfirmed:** the five pipeline stages (acquisition → preprocessing → inference → post-processing → action) appear in no slide or transcript. The course teaches sensing → inference → actuation plus a five-step development lifecycle. The bank keeps the five stages as a refinement because the papers ask for five.
- **Material slips:** the S2 recording is dated 31-Oct-2026 (notes say ~8-Nov). The professor said "activation" for actuation, "transmitting signal" for transforming signals, and "LoRa, low range". Optimisation was announced for S13-14 (the handout says S11-12). The slide framework list includes the retired Google Cloud IoT Core, and Azure Data Box Edge is now Azure Stack Edge.
- When the Module 2+ slides arrive, top up the other `edge-*` subjects the same way.

**Webinar top-up, 19/20-Nov-2026, pushed `c5fa429`.** Source: Webinar Experiment 1, edge vs cloud inference (`machine-learning-on-the-edge/webinars/01 Edge AI Experiment 1/`, guide + notebook). +20 each to edge-deployment (TFLite/LiteRT interpreter, FastAPI serving), edge-optimization (param counts, dynamic-range quant, the 11.39x ratio) and edge-benchmarking (warm-up, median/P95 vs mean, RTT vs server time, payload bytes, localhost bias). Material slips stated in the explanations and specs:
  - The 11.39x .keras → .tflite ratio is file-to-file: 3.15x from dropping the Adam state and metadata times 3.62x from int8. It is not the quantization gain.
  - The 67x edge speedup is a lower bound, since the "cloud" was localhost with no real network or TLS.
  - `tf.lite.Interpreter` is deprecated in favour of `ai_edge_litert`.
  - Accuracy after quantization was never measured.
  - Guide rounding: the HTTP+JSON overhead is 97.6% and the JSON overhead 81.3%. Mean > P95 means at most 5 outlier runs, not fewer than 5.

All 8 were pushed together in `14015da` (753 questions, 8,088 total). The DB is reloaded from that commit. Issues in the course material that the explanations point out:
- **No slides.** Both frameworks below were rebuilt from the papers, and the questions test the reasoning, not one exact wording. Replace them when the slides arrive.
  - Five pipeline stages: acquisition, preprocessing, inference, post-processing, action.
  - Five deployment questions: latency, connectivity, bandwidth/cost, privacy, power/autonomy.
- **Papers:**
  - "6 hours every 4 hours" overlaps and sends 1.5x the data.
  - The fleet costs come to only a few rupees a day, so the rebuttal must rest on latency, connectivity and privacy.
  - Option C's extra chip is an accelerator in Set 1 but a BLE radio in Set 2.
  - The 3.5 to 0.7 MB pruning shrink needs compressed or sparse storage.
  - The papers assume an ONNX Runtime CPU fallback that isn't guaranteed in every version.
- **Handout:** PyTorch Mobile is deprecated in favour of ExecuTorch. OpenVINO dropped Movidius (MYRIAD) after 2022.3 LTS.
- **Conventions:**
  - PSI uses the natural log, with bands at 0.1 and 0.25.
  - 1 MB = 10^6 bytes.
  - The Krum guarantee needs n > 2f + 2, which no attacker count meets with only 4 banks. One question covers this.

## Course banks: API-driven Cloud Native Solutions (AIMLCZG549), started 17-Nov-2026

Section `cloudnative` under `courses`, with 9 subjects in structure.py, all `ready`. Sources: the older-batch handout (S2-25) and the complete old-batch deck (430 slides). **No past papers and no current-batch slides.** Text extracts are in `C:/dev/quizdb-tools/cloud-src/` (one file per subject, split by slide page); the writer brief is `C:/dev/quizdb-tools/cloud-course-brief.md`.

| Sessions | Subject | Count | Status |
|----------|---------|-------|--------|
| S1 | cnas-apis | 90 | done, pushed |
| S1 | cnas-api-styles | 88 | done, pushed |
| S2-3 | cnas-cloudnative | 85 | done, pushed |
| S4-5 | cnas-data-pipelines | 100 | done, pushed |
| S6-7 | cnas-ml-pipelines | 92 | done, pushed |
| S8 | cnas-ai-services | 98 | done, pushed |
| S9-11 | cnas-llm-rag | 96 | done, pushed |
| S12 | cnas-containers-k8s | 85 | done, pushed |
| S13-15 | cnas-iot-analytics | 100 | done, pushed |

All 9 were pushed together in `ba42aa3` (834 questions, 8,922 total; the commit message says 830 by mistake). The DB is reloaded from that commit (student row kept). The writers found these slide errors; each explanation states the correct fact:
- **APIs:** "synchronous" is defined as waiting for the previous request (it means the caller blocks on its own reply). PUT is described as update only (it replaces; partial is PATCH). Semver PATCH is said to add features (it is fixes only). The movies example puts full versions in URIs (MAJOR only). gRPC uses HTTP/2 "instead of HTTP" (instead of HTTP/1.1).
- **Cloud-native/K8s:** blue = staging, green = production clashes with the usual convention, so questions test the mechanism. The Deployment YAML lacks the required `spec.selector`. The app and MySQL share one container.
- **Data/ML pipelines:** the Covid SEMMA slide puts feature engineering under Model (it belongs in Modify). The Covid MLflow summary's metrics don't add up (accuracy 194/243 = 0.798; positive-class recall 0.04) and it reads whole-machine system metrics as the model's. "768 hidden layers" means hidden size 768. GitHub-hosted jobs run on a VM, not a container. `--workspace-key` is not a Prefect CLI option. MLflow stages are deprecated in favour of aliases (both taught).
- **AI services/LLM-RAG:** the SLM size range is outdated (the course's own demo SLM is ~3.8B). Temperature 0.5 "for grounding" confuses randomness with grounding. The QA stage uses a summarize chain. Fine-tuning is said to improve interpretability.
- **IoT/analytics:** prescriptive analytics is captioned "what might happen?" (it is "what should we do?"). The box-plot whisker slides contradict each other (Tukey convention used). Woebot is listed as prescriptive (it is cognitive).

Image-only slides (technologies pyramid, DevOps dimensions, DataOps architectures, Bedrock, IoT stacks) and handout-only topics (MMLU, RAG metrics, speech APIs, device APIs) were written from standard practice; each spec says which.

## Known follow-ups
- Writers stall if they write a whole question block in one edit. Tell them to append at most 10 questions per edit.
- New questions in dl-neuron and dl-loss-gd are about 42-45% `out`, and in plotting about 57% `out` (targets 35% / 30%). A later pass can turn some into code mcqs.
- The Python core banks are too `out`-heavy (STANDARD.md wants about 35%). Round 3 appends conceptual mcq/tf/fill, never converts. Pass 1 (18-Nov-2026, `f1056e8`): +40 each to py-conditions (now 62% out), py-dicts (56%), py-strings (54%), py-lists (52%). Pass 2 (18-Nov-2026, `fc57c1c`): +40-41 each to py-classes (233, 51% out), py-variables (195, 48%), py-functions (190, 46%), py-loops (189, 44%), py-errors (208, 42%), py-basics (188, 42%), py-comprehensions (176, 41%). Pass 3 (18-Nov-2026, `2745db9`): +40 each to np-arrays (243, 37% out), np-operations (255, 35%), pd-dataframes (234, 50%), pd-cleaning (248, 52%). Pass 4 (19/20-Nov-2026, `c5fa429`): +40 each to py-conditions (231, 52% out), py-dicts (226, 46%), py-strings (233, 45%), py-classes (273, 43%), pd-cleaning (288, 45%), pd-dataframes (274, 42%). **Next:** only py-conditions is still clearly above 45%; one more +30 pass there would finish the type-mix work. Unrun facts to spot-check: PyTorch `state_dict` aliasing, `model.eval()` vs `no_grad()`, forward-hook `handle.remove()` (py-loops/py-functions L4), TabError and stale .pyc answers (py-basics L4).
- Python 3.12+ `sum()` of floats is compensated: `sum([0.1]*10) == 1.0` is True. Explanations must contrast it with a `+=` loop.
- Cloud-native banks use old-batch slides only (no papers). When current slides or papers arrive, top up the `cnas-*` subjects. Edge Module 1 slides are in (17-Nov); top up the other `edge-*` subjects as the Module 2+ slides arrive.

## Log
| Date | What happened |
|------|---------------|
| 15-Nov-2026 | Round 1 (earlier): 35 subjects, 3,238 questions, pushed. |
| 15-Nov-2026 | Round 2: Python core and six ML fundamentals subjects deepened, 4,450 questions, pushed `f941be6`. Stopped early to save tokens. ml-models is half-reviewed on disk. |
| 16-Nov-2026 | Round 2: ml-models committed, and all L2-L5 subjects deepened to 128-144 each (5,159 questions). Vendor names removed from tf-generation and nlp-embeddings. Pushed `779e5dd`, DB reloaded. |
| 16-Nov-2026 | NumPy and Pandas subjects deepened with L3/L4 and ML topics (`ml-arrays`, `ml-numpy`, `ml-features`, `windows`). 5,373 questions, pushed `71dcb2e`, DB reloaded. Plotting is next; then course-material subjects. |
| 16-Nov-2026 | plotting deepened to 152 (new topics scales-ticks, color-images, ml-plots, reading-charts). Round 2 done: 5,426 questions, pushed `59b790a`, DB reloaded. |
| 16-Nov-2026 | Added the `courses` category and 11 llmc-* subjects from the LLMs for GenAI course (notes, decks, old-batch slides, 8 past papers): 1,061 questions, 6,487 total. Pushed `4a44ea7`, DB reloaded. |
| 16-Nov-2026 | Added the NLP Applications course: 9 nlpa-* subjects, 848 questions, 7,335 total. Pushed `64243d4`, DB reloaded. |
| 17-Nov-2026 | Added the Machine Learning on the Edge course: 8 edge-* subjects (handout + 4 past papers, no slides), 753 questions, 8,088 total. Pushed `14015da`, DB reloaded (student row kept). |
| 17-Nov-2026 | Added the API-driven Cloud Native Solutions course: 9 cnas-* subjects (old-batch handout + 430-slide deck, no papers), 834 questions, 8,922 total. Pushed `ba42aa3`, DB reloaded (student row kept). |
| 17-Nov-2026 | Edge top-up from the CS1 slides, S1-3 transcripts and notes: edge-foundations 145, edge-hardware 102, BLERP replaces the reconstructed framework. 8,989 total. Pushed `50aea96`, DB reloaded (student row kept). |
| 18-Nov-2026 | Round 3 (type mix): +40 conceptual mcq/tf/fill each to py-conditions, py-dicts, py-strings, py-lists. 9,149 total. Pushed `f1056e8`, DB reloaded (student row kept). Fixed stale cnas pipeline rows. |
| 18-Nov-2026 | Round 3 pass 2: +282 conceptual mcq/tf/fill across py-classes, py-errors, py-variables, py-basics, py-functions, py-comprehensions, py-loops. 9,431 total. Pushed `fc57c1c`, DB reloaded (student row kept). |
| 18-Nov-2026 | Round 3 pass 3: +160 conceptual mcq/tf/fill across np-arrays, np-operations, pd-dataframes, pd-cleaning. 9,591 total. Pushed `2745db9`, DB reloaded (student row kept). |
| 20-Nov-2026 | Edge webinar 1 top-up (+60 across edge-deployment/optimization/benchmarking) and round 3 pass 4 (+240 conceptual mcq/tf/fill across py-conditions, py-dicts, py-strings, py-classes, pd-cleaning, pd-dataframes). 9,891 total. Pushed `c5fa429`, DB reloaded (student row kept). |
