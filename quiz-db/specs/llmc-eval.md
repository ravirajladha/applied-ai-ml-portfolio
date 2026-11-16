# Evaluation (M10): coverage spec

**Ladder:** Courses › LLMs for Generative AI (AIMLCZG536)   ·   **Prerequisites:** llmc-foundations (cross-entropy, perplexity idea), llmc-rag (retriever + generator), ml-metrics (precision, recall, F1)
**Why it matters for AI/ML:** Every LLM feature ships with an eval. An AI engineer must pick the right metric for the task (intrinsic vs extrinsic, reference-based vs reference-free), compute BLEU / ROUGE / perplexity / RAGAS by hand in the exam, know that n-gram overlap cannot see hallucinations, and know where benchmarks and LLM judges lie (contamination, position and verbosity bias).

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `framing` | Model vs system evaluation, the three axes | what an eval is, model vs system | intrinsic vs extrinsic, reference-based vs reference-free, automatic vs human | "no single metric" rule, pairing an automatic and a task-level check | classifying a metric on all three axes at once |
| 2 | `perplexity` | Perplexity | lower is better, range 1 to vocabulary | PPL from probabilities (geometric mean) and from mean NLL (exp) | not comparable across tokenizers; not meaningful after SFT/RLHF | bits-per-byte, base-2 vs nats, lower PPL but worse BLEU |
| 3 | `bleu` | BLEU | precision-oriented, made for translation | clipped (modified) n-gram precision, the "the the the" example | brevity penalty e^(1 - r/c), BLEU-2 by hand | zero bigram matches, BP when c > r, BLEU vs paraphrase |
| 4 | `rouge` | ROUGE-1 / ROUGE-2 / ROUGE-L | recall-oriented, made for summarisation | ROUGE-1 and ROUGE-2 recall by hand | ROUGE-L via LCS, P/R/F1 forms | BLEU vs ROUGE on the same short candidate |
| 5 | `semantic-metrics` | METEOR and BERTScore | beyond exact words | METEOR synonyms/stems + recall, BERTScore cosine matching | BERTScore greedy P/R/F1 by hand | why BERTScore still fails RAG faithfulness, embedding-model dependence |
| 6 | `task-metrics` | Task to metric (EM, F1, pass@k, IFEval) | exact match | token F1 for extractive QA, task-to-metric table | pass@k for code, normalisation choices | choosing a primary and a sanity metric |
| 7 | `faithfulness` | Hallucination, faithfulness, FActScore | what a hallucination is | intrinsic vs extrinsic hallucination, faithfulness vs truthfulness | FActScore = supported atomic facts / all facts | cost of LLM-driven decomposition, faithful-but-wrong |
| 8 | `ragas` | RAGAS: faithfulness, answer relevance, context precision, context recall | retrieval vs generation quality | the four metric definitions | computing all three by hand from a scenario, diagnosis table | which metric needs ground truth, fixes per failing metric |
| 9 | `benchmarks` | Benchmarks: static, live, arenas | what a benchmark is, MMLU | static vs live, contamination | Chatbot Arena pairwise votes, Bradley-Terry / Elo | domain benchmarks, why a leaderboard jump can be leakage |
| 10 | `llm-judge` | LLM-as-a-Judge | a model grading a model | single-answer vs pairwise, rubric | position / verbosity / self-preference bias and fixes | calibrating a judge against humans, swap-and-average |
| 11 | `online-offline` | Evaluation in production (offline vs online) | offline vs online | golden set, regression in CI, A/B tests | user feedback signals, drift | gating a release on offline + online evidence |

## Must-know facts
- Intrinsic = how well the model models language (perplexity). Extrinsic = how well it performs a downstream task.
- Reference-based compares to a gold answer (BLEU, ROUGE, BERTScore). Reference-free scores the output on its own (LLM-as-judge, perplexity, FActScore). Reference-based metrics cannot judge faithfulness to the retrieved source.
- Automatic = cheap, reproducible, imperfect proxy. Human = expensive, slow, still the ground truth for open-ended generation. No single metric captures quality.
- PPL = exp(mean negative log-likelihood) = (1 / prod P(w_i | w_<i))^(1/N). Range 1 (perfect) upward; uniform over V words gives PPL = V.
- PPL is comparable only across models with the identical tokenizer and eval set; it is not meaningful for SFT/RLHF stages; lower PPL does not guarantee downstream gains.
- BLEU = BP * exp(sum w_n ln p_n), with clipped n-gram precision p_n (count clipped at Max_Ref_Count) and BP = 1 if c > r else e^(1 - r/c). Natural log. Typically N = 4.
- ROUGE-N recall = matched n-grams / n-grams in the reference. ROUGE-L uses the longest common subsequence (in order, not necessarily consecutive).
- BLEU asks "how much of the machine output is correct?" (precision). ROUGE asks "how much of the human reference did the machine include?" (recall).
- METEOR adds recall and matches synonyms and word forms (run / ran). BERTScore matches tokens by cosine similarity of contextual embeddings and reports P, R, F1; always report the embedding model.
- Hallucination: intrinsic contradicts the source; extrinsic adds unverifiable information. Faithfulness = entailment by the retrieved context; truthfulness = agreement with real-world facts.
- FActScore = fraction of atomic facts supported by a knowledge source; LLM-driven, so expensive.
- RAGAS: faithfulness = supported claims / total claims; answer relevance = answer addresses the query; context precision = relevant chunks / retrieved chunks; context recall = needed facts retrieved / needed facts total (needs ground truth).
- Static benchmarks (MMLU, GSM8K, ARC, HellaSwag) are cheap and reproducible but leak into training data (contamination). Live benchmarks (LiveCodeBench) use fresh problems after the cutoff.
- Chatbot Arena: anonymous 1-v-1 battles, user votes, Bradley-Terry / Elo rating with confidence intervals.
- LLM-as-judge: single-answer grading or pairwise comparison; good prompts have an explicit rubric, reasoning before the score, a reference when available, and a tie-breaker. Biases: position, verbosity, self-preference.
- Code uses pass@k; classification / extractive QA uses exact match and F1; instruction following uses IFEval / MT-Bench.

## Common traps (each one must have at least one question)
- ROUGE recall divided by candidate length -> it is divided by reference n-grams.
- BLEU precision divided by reference length -> it is divided by candidate n-grams.
- Brevity penalty written as c/r or e^(1 - c/r) -> it is e^(1 - r/c), and 1 when c > r.
- Unclipped precision for "the the the ..." -> clipping caps each n-gram at its max count in one reference.
- p1 = 1.0 means the answer is correct -> it only means every word appears in the reference; a hallucinated claim can still be all-in-vocabulary.
- "Lower perplexity, so it is the better model; the BLEU gap is noise" -> intrinsic is not extrinsic.
- Comparing PPL across different tokenizers -> not comparable; use bits-per-byte.
- "PPL went up after SFT, roll it back" -> PPL is not a progress signal for SFT/RLHF.
- BERTScore as a RAG faithfulness metric -> still reference-based; never sees the retrieved context.
- Context precision vs context recall swapped -> precision = noise in retrieval, recall = missing facts.
- A high MMLU jump is proof of better reasoning -> may be contamination.
- Pairwise judge run once in one order -> position bias; swap A/B and average.

## Interview angle
- "How would you evaluate a RAG chatbot?" -> split retrieval (context precision/recall) from generation (faithfulness, answer relevance); use a golden set offline, then online feedback and A/B.
- "Why is BLEU a poor metric for an LLM answer?" -> lexical overlap, blind to paraphrase and to faithfulness; pair with BERTScore / judge / human.
- "What can go wrong with LLM-as-a-judge?" -> position, verbosity and self-preference bias, variance and cost; fix with rubric, swap order, calibrate on a human-labelled sample.
- "Your model tops a public benchmark but users hate it. Why?" -> contamination, benchmark-task mismatch; use live or domain benchmarks and human preference.

## Source material
- **Framing** (old-batch slides, M10 "Framing: What Are We Actually Measuring?"): intrinsic vs extrinsic, reference-based vs reference-free, automatic vs human; "no single metric captures quality, always pair one automatic + one task-level check". Handout M10: model evaluation vs system evaluation, benchmarks, perplexity, reference-based metrics, LLM-as-Judge, evaluation in production.
- **Perplexity** slides: PPL = exp(mean NLL); worked numericals (P = 0.4, 0.5 gives PPL = sqrt(5) = 2.236; NLL 2.3 gives about 10; NLL 1.5 vs 2.0 gives 4.48 vs 7.39; uniform 0.01 gives 100); caveats: identical tokenizer + eval set, not defined for SFT/RLHF, intrinsic is not extrinsic. Also Session-02 notes (Perplexity = exp(L), "how many tokens the model was choosing between").
- **BLEU** slides: standard vs modified (clipped) n-gram precision with the "the the the the the the the" example (standard 7/7); BLEU = BP * exp(sum w_n ln p_n); BP = e^(1 - r/c) for c <= r; worked example "the cat on mat" vs "the cat is on the mat" gives BP 0.606, p1 = 1, p2 = 1/3, BLEU-2 = 0.35.
- **ROUGE** slides: recall-oriented, ROUGE-N and ROUGE-L (LCS); example "the cat mat" vs "the cat is on the mat" gives ROUGE-1 = 0.50, ROUGE-2 = 0.20; limits of the n-gram family ("quick brown fox" vs "fast tan fox").
- **METEOR & BERTScore** slides: METEOR adds recall and synonym/stem matching; BERTScore uses contextual-embedding cosine, P/R/F1, depends on the embedding model.
- **Faithfulness** slides: intrinsic vs extrinsic hallucination, faithfulness vs truthfulness, FActScore (atomic facts verified against a knowledge source, LLM-driven and expensive).
- **RAGAS** slides: retrieval quality vs generation quality; faithfulness, answer relevance, context precision, context recall; HR-policy example (2/3, 2/4, 2/2) with the diagnosis "over-retrieving + generator not grounded" and fixes (reranker, threshold, hybrid; grounding prompt, claim verifier).
- **Benchmarks** slides: static (MMLU, GSM8K, ARC, HellaSwag) with contamination, live (LiveCodeBench, Big-Bench Hard as listed), arenas (Chatbot Arena, Bradley-Terry / Elo), model-graded (MT-Bench, AlpacaEval, Arena-Hard), domain-specific (MedQA, LegalBench, SWE-bench Verified); HELM in references.
- **LLM-as-a-Judge** slides: single-answer grading vs pairwise; rubric, CoT before score, reference answer, second judge for ties; model-answer note: judge biases are verbosity, self-preference and position.
- **Task-to-metric table** slides: translation/summarisation BLEU, ROUGE; chat LLM-judge, Arena Elo; code pass@k; RAG faithfulness; long-form factuality FActScore; classification / extractive QA exact match, F1; instruction following IFEval, MT-Bench.
- **Online vs offline**: the handout lists "Evaluation in production"; the slides give no detail, so this topic uses standard practice (golden sets in CI, A/B tests, user feedback) and is kept small.
- **Exam patterns** (Endsem Sep 2025 Regular Set 1/2, Sep 2026 Set 1/2, Makeup Set 1/2): "A team is evaluating a summarization model; for one test item..." asks BLEU-2 with BP and uniform weights, ROUGE-1 and ROUGE-2 recall, then the three RAGAS metrics from claim and chunk counts, then "p1 = 1.0 yet the faithfulness check flags a problem: why can't an n-gram metric see it?". The makeup papers compute PPL from per-token probabilities (geometric mean) and from mean NLL, then refute "lower PPL so better, the BLEU gap is noise", "PPLs from 16k and 32k tokenizers are comparable" and "PPL rose after SFT so roll back". A model answer lists the metric on (what it measures, reference-based or free, one weakness) and asks why BERTScore beats BLEU on some hallucinations but still is not a RAG faithfulness metric.
