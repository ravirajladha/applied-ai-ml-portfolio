# Sentiment Analysis (S7): coverage spec

**Ladder:** Courses › NLP Applications (AIMLCZG519) › Session 7 Sentiment Analysis   ·   **Prerequisites:** nlpa-overview (tokenisation, NLTK/spaCy pipelines), ml-models (Naive Bayes, logistic regression), ml-metrics (precision, recall, F1)
**Why it matters for AI/ML:** Sentiment is the most common text-classification job in industry (reviews, tweets, support tickets, call-centre turns). Session 7 walks the whole ladder: lexicon rules (VADER), lexicon induction (seed words, PMI), supervised Naive Bayes / logistic regression / SVM, neural and transformer models, aspect-based sentiment, production problems (sarcasm, domain shift, drift, code-switching, imbalance) and LLM zero/few-shot and agentic approaches. Past papers test it with "which level of sentiment fits this chatbot", VADER-style rule scoring, aspect scoring with a lexicon, Naive Bayes with given smoothed probabilities, and F1 by hand.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `basics` | Opinions, polarity and use cases | fact vs opinion, polarity labels, other names (opinion mining) | types: polarity, emotion, intention; use cases per industry | opinion search vs fact search; text-driven forecasting | which output a business actually needs |
| 2 | `levels` | Document, sentence and aspect level | what each level classifies | pick the level for a review / tweet / chatbot turn | why document level fails on mixed reviews and chat | exam pattern: per-turn sentence level in a conversational agent |
| 3 | `lexicon` | Lexicon (rule) based methods and VADER | tokenize, look up, shift, aggregate; VADER, SentiWordNet, AFINN, Hu-Liu | negation and intensifier rules by hand | VADER heuristics (caps, "!", "but", compound normalisation) | where rules break; lexicon vs ML trade-off |
| 4 | `lexicon-induction` | Building lexicons: seeds, conjunctions, PMI, WordNet | what a seed list is | "and" vs "but" conjunction rule | Turney phrase patterns, PMI polarity by hand | WordNet expansion drift, domain-specific lexicons |
| 5 | `naive-bayes` | Naive Bayes for sentiment (add-1, binary NB) | prior and likelihood | add-1 smoothing by hand, equal priors | binary NB, NOT_ negation trick, log space | unknown words, double-counted evidence, NB vs LR |
| 6 | `features-lr` | Features and discriminative models (BoW, TF-IDF, n-grams, LR, SVM) | bag of words | n-grams for "not good", TF-IDF | logistic regression score by hand, coefficient reading | why LR/SVM beat NB with more data; feature leakage |
| 7 | `neural` | Neural and transformer sentiment models | embeddings as learned features | feedforward over pooled embeddings, CNN/RNN/LSTM | BERT [CLS] fine-tuning, accuracy ladder | cost vs accuracy choice, distillation and quantisation |
| 8 | `absa` | Aspect-based sentiment analysis | aspect and target | opinion quintuple (e, a, s, h, t) | frequency-based aspect extraction, aspect scoring by hand | ABSA pipeline design and aggregation pitfalls |
| 9 | `challenges` | Sarcasm, domain shift, drift, code-switching, imbalance | why sarcasm is hard | domain mismatch ("positive biopsy") | drift monitoring, code-mixed text, imbalance fixes | latency arithmetic at scale |
| 10 | `evaluation` | Evaluating sentiment classifiers | accuracy, confusion matrix | precision, recall, F1 by hand | macro vs weighted F1, Cohen's kappa | MCC, cross-entropy, accuracy paradox |
| 11 | `genai-agentic` | LLM and agentic approaches | zero-shot prompt classification | few-shot, structured JSON output | LLM labelling to train a cheap model | agentic sentiment pipelines, cost/latency/consistency trade-offs |

## Must-know facts
- Sentiment analysis (opinion mining) is the computational process of identifying and extracting subjective information from text: Positive, Negative or Neutral. Facts are objective ("iPhone is an Apple product"), opinions are subjective ("iPhone is good").
- Types: polarity (pos/neu/neg), emotion, and intention (to buy, to sell, to complain).
- Levels: document (whole review), sentence (each sentence or chat turn), aspect (sentiment per entity/attribute: "camera amazing, battery terrible" -> [camera: +] [battery: -]).
- Lexicon pipeline: tokenize -> look up each token -> apply valence shifters (negation, intensifiers) -> aggregate -> classify polarity. VADER (social media, slang, emojis), SentiWordNet (WordNet, ~117k synsets), AFINN (2,477 words, -5..+5), Hu & Liu Opinion Lexicon (~6,800 words).
- VADER outputs neg/neu/pos proportions plus a compound score in [-1, 1]; compound = x / sqrt(x^2 + 15) on the summed valence x. Usual thresholds: >= 0.05 positive, <= -0.05 negative.
- Corpus-based lexicon induction: start from seed adjectives; adjectives joined by "and" share polarity, joined by "but" have opposite polarity; build a graph and cluster.
- Turney: extract two-word phrases by POS pattern (JJ+NN, RB+JJ, JJ+JJ, NN+JJ, RB+VB), polarity(phrase) = PMI(phrase, "excellent") - PMI(phrase, "poor"), review = average phrase polarity. PMI(x, y) = log2 P(x, y) / (P(x)P(y)); 0 when independent.
- Multinomial NB: c* = argmax P(c) * prod P(w|c); with add-1 smoothing P(w|c) = (count(w, c) + 1) / (sum count(., c) + |V|). Compute in log space. Unknown test words are dropped.
- Binary NB: clip each word count to 1 per document before counting (presence matters more than frequency for sentiment).
- Negation trick: prefix NOT_ to every word after a negation token until the next punctuation ("didn't like this" -> didn't NOT_like NOT_this).
- Features: bag of words, TF-IDF, n-grams (bigram "not good"), embeddings, POS tags. Classic models: NB (fast baseline), logistic regression (probabilistic, works well with TF-IDF), SVM (high-dimensional margin), random forest, gradient boosting.
- Neural: learned embeddings as input instead of hand-built features; RNN/LSTM -> BiLSTM + attention -> BERT -> RoBERTa -> LLMs. BERT fine-tuning puts a classifier on the [CLS] vector.
- Slide accuracy ladder (SST-2 style): VADER 79%, NB 83%, SVM + TF-IDF 88%, fine-tuned BERT ~96%; LLM zero-shot ~91% with no labelled data.
- ABSA: opinion = quintuple (e, a, s, h, t): entity, aspect, sentiment, holder, time. Aspect extraction by frequent noun phrases (frequency-based) or a classifier; extract phrases -> classify -> assign aspect -> aggregate per aspect.
- Production issues: data/concept drift (retraining, monitoring), domain mismatch ("positive biopsy"; fix: domain fine-tuning, DAPT), sarcasm ("Great, another system outage"; contextual models), code-switching (mBERT, XLM-R, language routing), latency (50 ms x 1M = 13.9 h on one GPU; INT8, DistilBERT, batching), class imbalance (65/25/10; class weights, SMOTE, per-class thresholds).
- Metrics: accuracy, precision, recall, F1, macro F1 (imbalanced data), weighted F1, confusion matrix, AUC, MCC, Cohen's kappa for annotator agreement, cross-entropy loss.

## Common traps (each one must have at least one question)
- Document-level sentiment for a chatbot -> you need the per-turn (sentence-level) signal to adapt the dialogue.
- Summing lexicon scores and forgetting the negation flips the NEXT word only -> "not good" = -2, not +2.
- Applying the intensifier to the wrong word or adding instead of multiplying.
- Treating "but" as neutral -> the clause after "but" dominates (VADER weights it up).
- Forgetting the +|V| in the add-1 denominator.
- Keeping unknown test words in NB with a made-up probability -> the standard move is to drop them.
- Binary NB clips counts per document, not across the corpus.
- Equal priors still require multiplying all word likelihoods: the prior cancels, the words do not.
- Bag of words loses "not good" -> add bigrams or the NOT_ trick.
- Domain shift: "unpredictable plot" (+) vs "unpredictable steering" (-); "positive biopsy".
- Sarcasm read literally by lexicons.
- Accuracy on a 65% neutral dataset -> a majority-class model looks good; use macro F1.
- MCC computed without the square root in the denominator (the old slide's formula omits it).
- LLM zero-shot labels treated as ground truth -> sample-check against humans, measure agreement.
- Averaging aspect scores into one review score hides the actionable signal.

## Interview angle
1. **"Lexicon or ML?"** Lexicon: no training data, transparent, fast, but brittle (domain, sarcasm, unseen slang). ML/transformers: need labels, adapt to domain, much more accurate. Hybrid is common.
2. **"Walk me through Naive Bayes for sentiment."** Count words per class, add-1 smooth with |V|, sum log prior + log likelihoods, take the max; binary NB and NOT_ negation help.
3. **"Our model trained on movie reviews does badly on hospital feedback. Why and what do you do?"** Domain shift: words change polarity; label a small in-domain set and fine-tune, or domain-adaptive pretraining; monitor drift.
4. **"Why aspect-based sentiment?"** One star rating hides that camera is loved and battery hated; ABSA gives per-aspect actionable scores.
5. **"When would you use an LLM instead of fine-tuned BERT?"** Little labelled data, many changing labels, need explanations; but cost, latency and consistency at millions of posts favour a fine-tuned small model, possibly trained on LLM labels.

## Source material
- Handout (`nlp-src/handout.txt`): Session 7 "Sentiment Analysis Methods", "Neural Networks for Sentiment Analysis", "Gen AI and Agentic AI approaches for Sentiment Analysis"; reference T1 (Jurafsky & Martin) chapter 4; Lab 10 Sentiment Analysis.
- Old-batch slides (`old-batch-slides.txt` ~lines 2505-3040, same content in `nlp-applications-slides.txt` ~2587-3140): motivation, facts vs opinions, types (polarity, emotion, intention), definition, document/sentence/aspect levels with the camera/battery example, industry use-case table (e-commerce ABSA, finance transformers, healthcare rule + ML, support tickets LLM-based, social buzz hybrid).
- Same deck: lexicon methods (4 steps, VADER/SentiWordNet/AFINN/Hu-Liu, VADER output example "ABSOLUTELY FANTASTIC! Not bad at all" -> compound 0.87); corpus-based lexicon generation (seed adjectives, "and"/"but" conjunctions, graph); Turney's POS patterns and PMI polarity; WordNet synonym/antonym expansion.
- Same deck: ML methods (BoW, TF-IDF, n-grams, embeddings, POS; NB, LR, SVM, RF, gradient boosting), deep learning evolution (RNN/LSTM -> BiLSTM+attention -> BERT -> RoBERTa -> LLMs), BERT [CLS] fine-tuning, accuracy comparison table, LLM zero-shot JSON prompt (91%), feedforward nets over embeddings, Twitter product case study (2.4M tweets, RoBERTa on TweetEval, Kafka, TorchServe).
- Same deck: ABSA (iPhone review, quintuple (e, a, s, h, t), frequency-based aspect extraction, aspects per entity, the Blair-Goldensohn extract -> classify -> aspect -> aggregate architecture); production issues table (drift, domain mismatch, sarcasm, code-switching, latency, imbalance) with solutions.
- Same deck: evaluation slide (confusion matrix TP 850, FN 50, FP 30, TN 520: accuracy 94.5%, precision 96.6%, recall 94.4%, F1 95.5%; AUC; MCC; Cohen's kappa (0.87 - 0.52)/(1 - 0.52) = 0.73; cross-entropy -log 0.85 = 0.163) and "sentiment: macro F1, accuracy; challenge sarcasm, domain shift".
- **Course error flagged:** the old MCC slide writes the denominator without the square root; the correct MCC = (TP*TN - FP*FN) / sqrt((TP+FP)(TP+FN)(TN+FP)(TN+FN)). Its printed 0.883 is (approximately) the correct square-root result; the product it shows is also slightly off (248,292,000,000).
- **Gaps (textbook material used):** the slides do not work Naive Bayes by hand for sentiment, binary NB, the NOT_ negation trick, logistic regression scoring or the VADER compound formula; those questions follow Jurafsky & Martin ch. 4 (which the handout cites) and the VADER paper (Hutto & Gilbert 2014). "GenAI and agentic approaches" is covered on the slides by a single zero-shot line; questions on few-shot prompting, LLM labelling and agentic pipelines use standard practice.
- Exam patterns: Sep 2026 end-sem Sets 1-2 Q1: banking / healthcare assistant, "what level of sentiment analysis suits and why other levels won't work" (answer: sentence level per user turn, feeding the NLU and the dialogue manager), then Naive Bayes on a patient turn with given Laplace-smoothed word probabilities and equal priors. Jun 2026 mid-sem Set 2 Q5: VADER-style scoring with a given lexicon, intensifier x1.5, negation flips the next word, thresholds > 1 / [-1, 1] / < -1. Jun 2026 mid-sem Q5: extract aspects from 8 phone reviews, rank by count, score with a lexicon, top positive/negative aspect. Jun 2026 mid-sem makeup Q5: tweet percentages, dominant sentiment, approach for millions of posts (fine-tuned RoBERTa/BERT or LLM), two challenges (sarcasm, code-switching). 2026 end-sem makeup Q1c: F1 of a sentiment analyser from TP/FP/FN counts.
