# Quiz bank progress

Read this first in every quiz-creation session. Update it at the end.

## Round 2: deepen every subject (started 15-Nov-2026, finished 16-Nov-2026)

Target: 120-160 questions per subject, with more L3/L4, informative explanations and a real ML-code topic per subject.

| Rung | Subject | Round 1 | Round 2 | Status |
|------|---------|---------|---------|--------|
| Foundations | py-basics | 73 | 148 | done, pushed |
| Foundations | py-variables | 78 | 155 | done, pushed |
| Foundations | py-strings | 87 | 153 | done, pushed |
| Foundations | py-lists | 80 | 158 | done, pushed |
| Foundations | py-dicts | 70 | 146 | done, pushed |
| Foundations | py-conditions | 71 | 151 | done, pushed |
| Foundations | py-loops | 73 | 149 | done, pushed |
| Foundations | py-functions | 67 | 150 | done, pushed |
| Foundations | py-comprehensions | 61 | 136 | done, pushed |
| Foundations | py-errors | 104 | 167 | done, pushed |
| Foundations | py-classes | 108 | 192 | done, pushed |
| Foundations | np-arrays, np-operations | 139, 153 | 203, 215 | done, pushed |
| Foundations | pd-dataframes, pd-cleaning | 151, 163 | 194, 208 | done, pushed |
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

**Next course:** **next** api-driven-cloud-native-solutions (machine-learning-on-the-edge is done) (same approach: extract the material to llm-src-style text, write a brief, add a `courses` section). When the LLM course teaches sessions 4+, top up the subjects from the new notes.

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
| M1 | edge-foundations | 90 | done, pushed |
| M2 | edge-hardware | 90 | done, pushed |
| M3 | edge-data-iot | 95 | done, pushed |
| M4 | edge-deployment | 94 | done, pushed |
| M5 | edge-mlops | 95 | done, pushed |
| M6 | edge-optimization | 95 | done, pushed |
| M7 | edge-security | 94 | done, pushed |
| M8 | edge-benchmarking | 100 | done, pushed |

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

## Known follow-ups
- Writers stall if they write a whole question block in one edit. Tell them to append at most 10 questions per edit.
- New questions in dl-neuron and dl-loss-gd are about 42-45% `out`, and in plotting about 57% `out` (targets 35% / 30%). A later pass can turn some into code mcqs.
- The Python core banks are 55-79% `out` questions (STANDARD.md wants about 35%). Add conceptual mcq/tf questions in a later pass instead of converting existing ones.
- Python 3.12+ `sum()` of floats is compensated: `sum([0.1]*10) == 1.0` is True. Explanations must contrast it with a `+=` loop.
- Course material for cloud-native is not in the bank yet. When edge-ML slides arrive, top up the `edge-*` subjects and replace the reconstructed frameworks.

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
