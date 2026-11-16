from helpers import mcq, tf, out, fill

SUBJECT = "llmc-eval"

TOPICS = [
    ("framing", "Model vs system evaluation, the three axes"),
    ("perplexity", "Perplexity"),
    ("bleu", "BLEU"),
    ("rouge", "ROUGE-1 / ROUGE-2 / ROUGE-L"),
    ("semantic-metrics", "METEOR and BERTScore"),
    ("task-metrics", "Task to metric (EM, F1, pass@k, IFEval)"),
    ("faithfulness", "Hallucination, faithfulness, FActScore"),
    ("ragas", "RAGAS: faithfulness, answer relevance, context precision, context recall"),
    ("benchmarks", "Benchmarks: static, live, arenas"),
    ("llm-judge", "LLM-as-a-Judge"),
    ("online-offline", "Evaluation in production (offline vs online)"),
]

AXES = """
  intrinsic  <---->  extrinsic        (LM fit vs task)
  ref-based  <---->  ref-free         (gold answer or not)
  automatic  <---->  human            (cheap proxy vs truth)
"""

QUESTIONS = [
    # ------------------------------------------------------------------ L1
    mcq("The course separates 'model evaluation' from 'system evaluation'. What does system evaluation look at?",
        ["The whole application: retriever, prompts, tools and model together, judged on the end task",
         "Only the raw model's next-token probabilities",
         "Only the GPU hardware the model runs on",
         "Only the size of the training set"], 0,
        "Think of the product, not the network.",
        "Model evaluation scores the LLM on its own (perplexity, benchmarks). System evaluation scores the full pipeline a user touches, e.g. a RAG bot: did retrieval find the right chunks and is the final answer faithful and relevant?",
        topic="framing", level=1,
        analogy="Unit test of one function (model eval) vs end-to-end test of the deployed app (system eval)."),
    mcq("Which of these is an INTRINSIC evaluation of a language model?",
        ["Perplexity on held-out text",
         "Accuracy on a customer-ticket classification task",
         "BLEU on a translation test set",
         "Pass rate on code unit tests"], 0,
        "Intrinsic = how well it models language itself.",
        "Intrinsic metrics measure how well the model predicts text (perplexity). The other three measure a downstream task, which the course calls extrinsic.",
        topic="framing", level=1),
    tf("A lower perplexity means the model assigned higher probability to the true next tokens.", True,
       "Perplexity is a measure of surprise.",
       "PPL = exp(mean negative log-likelihood). Higher probability on the true tokens gives lower NLL and so lower PPL. 1.0 is perfect.",
       topic="perplexity", level=1),
    fill("A model has perplexity 10 on a test set. It is as unsure as if it were choosing uniformly between about ____ equally likely words at each step.", "10",
         "That is the intuition the slides give.",
         "PPL is the effective branching factor. A model with PPL 10 is as confused as one picking uniformly among 10 words at each step.",
         topic="perplexity", level=1),
    mcq("BLEU was designed for which task, and which side of the precision/recall pair does it lean on?",
        ["Machine translation; precision",
         "Summarisation; recall",
         "Question answering; recall",
         "Code generation; precision"], 0,
        "The 'BiLingual' in its name is a clue.",
        "BLEU (BiLingual Evaluation Understudy) asks how much of the machine's output appears in the reference: precision. ROUGE is the recall-oriented one, made for summaries.",
        topic="bleu", level=1),
    mcq("ROUGE asks which question about a machine summary?",
        ["How much of the human reference did the machine manage to include?",
         "How much of the machine output is grammatical?",
         "How many words of the machine output are synonyms?",
         "How fast was the summary generated?"], 0,
        "R is for Recall.",
        "ROUGE = Recall-Oriented Understudy for Gisting Evaluation. If a human summary has 5 key points, ROUGE checks how many of them show up in the machine summary.",
        topic="rouge", level=1),
    tf("BERTScore can give credit when the candidate says 'started' and the reference says 'began'.", True,
       "It compares meanings, not spellings.",
       "BERTScore embeds tokens with a pretrained model and matches them by cosine similarity, so paraphrases like began/started score high. BLEU and ROUGE give them zero.",
       topic="semantic-metrics", level=1),
    mcq("A QA system answers 'Paris' and the gold answer is 'Paris'. Another answers 'Paris, France'. Under strict exact match (EM), what are the two scores?",
        ["1 and 0",
         "1 and 1",
         "1 and 0.5",
         "0.5 and 0.5"], 0,
        "Exact means exact (after normalisation).",
        "EM gives 1 only when the normalised strings are identical. 'Paris, France' is not identical, so it gets 0, even though a human would accept it. Token F1 would give partial credit.",
        analogy="Exact match is a strict string == after normalising; token F1 is a fuzzy match.",
        topic="task-metrics", level=1),
    mcq("What is a hallucination in an LLM output?",
        ["Content that is unfaithful to the provided source or nonsensical relative to real-world facts",
         "Any answer longer than the reference",
         "An answer written in a different language",
         "An output that is cut off by the token limit"], 0,
        "It sounds right but is not supported.",
        "The course defines hallucination as generated content that is unfaithful to the source documents or nonsensical relative to real-world facts. It is often fluent and confident, which is why it is dangerous.",
        topic="faithfulness", level=1),
    mcq("The RAGAS framework splits the evaluation of a RAG pipeline into which two layers?",
        ["Retrieval quality and generation quality",
         "Training loss and validation loss",
         "Latency and cost",
         "Tokenizer quality and embedding quality"], 0,
        "A RAG bot has two halves.",
        "RAGAS asks two separate questions: did the retriever fetch the right context, and did the LLM use that context accurately without hallucinating? Splitting them tells you which half to fix.",
        topic="ragas", level=1,
        diagram="""
 query -> [retriever] -> chunks -> [generator] -> answer
              |                         |
     context precision/recall   faithfulness, relevance
"""),
    tf("A static benchmark like MMLU uses a fixed, public set of questions that every model is tested on.", True,
       "Static = the questions never change.",
       "MMLU, GSM8K, ARC and HellaSwag are released once as CSV/JSON and every model faces the exact same items. That makes them cheap and reproducible, and also easy to leak into training data.",
       topic="benchmarks", level=1),
    mcq("What does 'LLM-as-a-Judge' mean?",
        ["Using a strong LLM to score or compare another model's outputs, usually against a rubric",
         "Training an LLM on legal judgements",
         "Letting users vote on answers in an app",
         "Measuring the model's perplexity on court documents"], 0,
        "Who is doing the grading?",
        "A strong model reads the question and the candidate answer (and optionally a reference) and returns a score or a winner. It scales far beyond human review, but it brings its own biases.",
        topic="llm-judge", level=1,
        analogy="A senior engineer doing code review with a checklist, except the reviewer is a model."),
    mcq("What is the difference between offline and online evaluation of an LLM feature?",
        ["Offline runs on a fixed test set before release; online measures real users' traffic after release",
         "Offline needs no GPU; online needs a GPU",
         "Offline uses humans; online uses metrics",
         "There is no difference; the names are interchangeable"], 0,
        "Before vs after shipping.",
        "Offline eval = your golden set, run in CI before you deploy. Online eval = A/B tests, thumbs-up rates, escalations and other signals from live traffic. You need both: offline catches regressions early, online tells you what users actually experience.",
        topic="online-offline", level=1,
        analogy="Unit/integration tests in CI (offline) vs production monitoring and A/B experiments (online)."),
    tf("According to the course, automatic metrics like BLEU are cheap and reproducible, but human evaluation is still the ground truth for open-ended generation.", True,
       "Which one is expensive but trusted?",
       "The slides put it as: automatic = cheap, reproducible, imperfect proxy; human = expensive, slow, still the ground truth for open-ended text.",
       topic="framing", level=1),
    fill("BLEU multiplies the n-gram precision score by a factor that punishes candidates that are too short. This factor is called the ____ penalty.", "brevity",
         "Brevity = shortness.",
         "Without the brevity penalty (BP), a one-word candidate that matches could score perfect precision. BP = e^(1 - r/c) when the candidate is shorter than the reference.",
         topic="bleu", level=1),
    tf("ROUGE-L is based on the longest common subsequence: words in the same order in both texts, but not necessarily next to each other.", True,
       "Subsequence, not substring.",
       "'The cat is on the mat' and 'The cat mat' share the LCS 'the cat mat' (length 3) even though 'cat mat' is not consecutive in the reference.",
       topic="rouge", level=1),
    mcq("A coding assistant model is evaluated by running its generated functions against unit tests. Which metric family does the course list as primary for code generation?",
        ["pass@k (functional correctness)",
         "BLEU",
         "ROUGE-L",
         "Perplexity"], 0,
        "For code, does it run and pass?",
        "Code can look textually different from the reference and still be correct, or look similar and fail. pass@k checks whether at least one of k samples passes the tests.",
        topic="task-metrics", level=1),
    mcq("In RAGAS, the faithfulness score of an answer is:",
        ["supported claims / total claims in the answer",
         "relevant chunks / retrieved chunks",
         "matched words / reference words",
         "the cosine similarity between answer and question"], 0,
        "Faithful to the retrieved context, claim by claim.",
        "The answer is split into atomic claims, each claim is checked against the retrieved context, and faithfulness is the supported fraction. Relevant chunks / retrieved chunks is context precision.",
        topic="ragas", level=1),
    tf("Chatbot Arena ranks models by asking users to vote between two anonymous answers to the same prompt.", True,
       "Blind 1-v-1 battles.",
       "Users see two anonymous responses, vote for the better one, and only then see the model names. The pairwise votes are turned into Bradley-Terry / Elo ratings with confidence intervals.",
       topic="benchmarks", level=1),
    # ------------------------------------------------------------------ L2
    out("import math\n"
        "p = [0.5, 0.2, 0.4, 0.25]          # P(true token | context) at each step\n"
        "ppl = (1 / math.prod(p)) ** (1 / len(p))\n"
        "print(round(ppl, 3))",
        ["3.162", "2.963", "0.316", "10.0"], 0,
        "Nth root of 1 / (product of probabilities).",
        "prod = 0.5 * 0.2 * 0.4 * 0.25 = 0.01, 1/0.01 = 100, and the 4th root of 100 is 3.162. This is the same as exp(mean NLL). 0.316 is the geometric mean of p itself (forgot the 1/), 10.0 is a square root instead of a 4th root.",
        diagram="""
 PPL = ( 1 / (p1 * p2 * ... * pN) ) ^ (1/N)
     = exp( -(1/N) * sum ln p_i )
 p = 1 every step  -> PPL = 1  (perfect)
 p = 1/V every step -> PPL = V  (guessing)
""",
        topic="perplexity", level=2),
    out("import math\n"
        "mean_nll = 1.2        # validation cross-entropy, natural log (nats)\n"
        "print(round(math.exp(mean_nll), 2))",
        ["3.32", "2.3", "1.2", "0.3"], 0,
        "Cross-entropy is log-perplexity.",
        "With natural-log loss, PPL = e^loss = e^1.2 = 3.32. 2.3 is 2^1.2 (the base-2 formula, which only applies when the loss is in bits).",
        topic="perplexity", level=2),
    out("from collections import Counter\n"
        "cand = 'the the the the'.split()\n"
        "ref = 'the cat sat on the mat'.split()\n"
        "rc = Counter(ref)\n"
        "standard = sum(w in rc for w in cand) / len(cand)\n"
        "clipped = sum(min(n, rc[w]) for w, n in Counter(cand).items()) / len(cand)\n"
        "print(standard, clipped)",
        ["1.0 0.5", "1.0 1.0", "0.5 0.5", "0.25 0.5"], 0,
        "Clipping caps each word at its count in the reference.",
        "Standard precision gives 4/4 because every 'the' exists in the reference. Modified (clipped) precision caps 'the' at its max reference count, 2, so 2/4 = 0.5. This is exactly why BLEU clips.",
        diagram="""
 cand: the the the the        ref: the cat sat on the mat
 count(the) in cand = 4
 max count in ref   = 2   -> clip to min(4, 2) = 2
 clipped p1 = 2 / 4
""", analogy="A coupon limited to 2 per customer: buying 4 items still gets only 2 discounts.",
        topic="bleu", level=2),
    mcq("In BLEU's modified n-gram precision, what is the denominator for p1?",
        ["The total number of unigrams in the CANDIDATE",
         "The total number of unigrams in the reference",
         "The length of the longest reference",
         "The number of distinct words in both texts"], 0,
        "Precision = how much of what the machine said.",
        "p_n = clipped matched n-grams / all n-grams in the candidate. Dividing by the reference length is the ROUGE (recall) formula, and is the classic mix-up in exam answers.",
        diagram="""
            matched n-grams
 BLEU p_n = -------------------------  (precision)
            n-grams in CANDIDATE

            matched n-grams
 ROUGE-N = -------------------------  (recall)
            n-grams in REFERENCE
""",
        topic="bleu", level=2),
    tf("In BLEU, if the candidate is LONGER than the reference (c > r), the brevity penalty is 1.", True,
       "The penalty only punishes being short.",
       "BP = 1 if c > r, else e^(1 - r/c). Long candidates are already punished by lower precision (extra words don't match), so BP doesn't touch them.",
       topic="bleu", level=2),
    out("import math\n"
        "c, r = 5, 8          # candidate and reference lengths\n"
        "bp = 1.0 if c > r else math.exp(1 - r / c)\n"
        "print(round(bp, 3))",
        ["0.549", "1.455", "0.625", "1.0"], 0,
        "r/c, not c/r.",
        "e^(1 - 8/5) = e^(-0.6) = 0.549. 1.455 is the flipped form e^(1 - c/r), which would REWARD a short answer. 0.625 is just c/r, and 1.0 is the value for c > r.",
        analogy="Like a minimum word count on an essay: a three-line answer can't score full marks however accurate it is.",
        topic="bleu", level=2),
    out("from collections import Counter\n"
        "def ngrams(t, n): return [tuple(t[i:i+n]) for i in range(len(t)-n+1)]\n"
        "ref = 'the high court rejected the appeal on monday'.split()\n"
        "cand = 'the court rejected the appeal'.split()\n"
        "for n in (1, 2):\n"
        "    rc, cc = Counter(ngrams(ref, n)), Counter(ngrams(cand, n))\n"
        "    hit = sum(min(v, rc[g]) for g, v in cc.items())\n"
        "    print(f'ROUGE-{n} recall = {hit}/{sum(rc.values())}')",
        ["ROUGE-1 recall = 5/8\nROUGE-2 recall = 3/7",
         "ROUGE-1 recall = 5/5\nROUGE-2 recall = 3/4",
         "ROUGE-1 recall = 5/8\nROUGE-2 recall = 4/7",
         "ROUGE-1 recall = 4/8\nROUGE-2 recall = 3/7"], 0,
        "Recall divides by the REFERENCE n-gram count.",
        "All 5 candidate words are in the 8-word reference: 5/8. Candidate bigrams: 'the court' (not in ref, ref has 'the high'), 'court rejected', 'rejected the', 'the appeal' all match: 3 of the reference's 7 bigrams. 5/5 and 3/4 are the precision versions.",
        topic="rouge", level=2),
    out("def lcs(a, b):\n"
        "    d = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]\n"
        "    for i, x in enumerate(a):\n"
        "        for j, y in enumerate(b):\n"
        "            d[i+1][j+1] = d[i][j] + 1 if x == y else max(d[i][j+1], d[i+1][j])\n"
        "    return d[-1][-1]\n"
        "ref = 'in march the sales of laptops rose'.split()\n"
        "cand = 'sales rose in march'.split()\n"
        "print(lcs(ref, cand), round(lcs(ref, cand) / len(ref), 3))",
        ["2 0.286", "4 0.571", "3 0.429", "2 0.5"], 0,
        "All four words appear, but in what order?",
        "Every candidate word is in the reference, so ROUGE-1 recall would be 4/7. But LCS keeps order: 'sales ... rose' or 'in march' gives length 2, so ROUGE-L recall = 2/7 = 0.286. ROUGE-L punishes the scrambled order that ROUGE-1 ignores.",
        diagram="""
 ref : in march the SALES of laptops ROSE
 cand: SALES ROSE in march
 LCS keeps order: 'sales rose' (or 'in march') = 2
""",
        topic="rouge", level=2),
    mcq("What does METEOR add that BLEU lacks, according to the course?",
        ["A recall component and matching of synonyms and word forms (e.g. 'run' and 'ran')",
         "A brevity penalty",
         "Contextual embeddings from BERT",
         "An LLM judge that reads the source"], 0,
        "It was designed to fix BLEU's weak spots.",
        "METEOR uses generalised unigram matching (exact, stem, synonym) and includes recall, so it correlates better with human judgement on short outputs. Contextual embeddings are BERTScore; BLEU already has a brevity penalty.",
        topic="semantic-metrics", level=2),
    mcq("A summary says a drug 'cures' a disease when the source document says it 'manages symptoms of' it. What type of hallucination is this, in the course's terms?",
        ["Intrinsic: the output directly contradicts the source",
         "Extrinsic: the output adds information not in the source",
         "Neither: it is a paraphrase",
         "A retrieval failure"], 0,
        "Does it contradict, or merely add?",
        "Intrinsic hallucination contradicts facts in the source context. Extrinsic hallucination fabricates information that the source neither supports nor contradicts (e.g. adding a dosage the document never mentions).",
        topic="faithfulness", level=2),
    out("def token_f1(pred, gold):\n"
        "    p, g = pred.lower().split(), gold.lower().split()\n"
        "    common = sum(min(p.count(w), g.count(w)) for w in set(p))\n"
        "    if common == 0:\n"
        "        return 0.0\n"
        "    prec, rec = common / len(p), common / len(g)\n"
        "    return round(2 * prec * rec / (prec + rec), 3)\n"
        "print(token_f1('the Eiffel Tower in Paris', 'Eiffel Tower'))",
        ["0.571", "1.0", "0.4", "0.0"], 0,
        "Precision 2/5, recall 2/2.",
        "Two tokens overlap. Precision = 2/5 = 0.4, recall = 2/2 = 1.0, F1 = 2*0.4*1/(1.4) = 0.571. Exact match would give 0 here; token F1 gives partial credit, which is why the course pairs EM with F1 for extractive QA.",
        topic="task-metrics", level=2),
    mcq("The course's 'faithfulness vs truthfulness' distinction: a RAG answer repeats exactly what an outdated retrieved document says, and that is no longer true in the world. How does it score?",
        ["Faithful (entailed by the context) but not truthful",
         "Truthful but not faithful",
         "Both faithful and truthful",
         "Neither, because it was retrieved"], 0,
        "Faithfulness is measured only against the retrieved context.",
        "Faithfulness = strict entailment from the retrieved context. Truthfulness = agreement with real-world facts regardless of the context. A stale document gives a faithful but untruthful answer: the fix is in the corpus (freshness), not the generator.",
        diagram="""
                 matches context   contradicts context
 true in world    faithful+true     unfaithful+true
 false in world   faithful+false    unfaithful+false
 stale doc -> bottom-left: fix the corpus
""", analogy="Faithful = the code matches the spec; truthful = the spec matches reality.",
        topic="faithfulness", level=2),
    mcq("Which RAGAS metric needs ground-truth annotations (the list of facts the answer should have used)?",
        ["Context recall",
         "Faithfulness",
         "Answer relevance",
         "Context precision judged by an LLM against the query"], 0,
        "To know what is MISSING you must know what was needed.",
        "Context recall = needed facts retrieved / needed facts total, so you must know the needed facts. Faithfulness only needs the answer and the retrieved context, and answer relevance only needs the answer and the query.",
        analogy="You can only report missing items from a delivery if you have the packing list.",
        topic="ragas", level=2),
    mcq("A RAG bot's answer is fully supported by its retrieved chunks, but it talks about the refund window when the user asked how to change a delivery address. Which RAGAS metric flags this?",
        ["Answer relevance",
         "Faithfulness",
         "Context recall",
         "BLEU"], 0,
        "Supported is not the same as on-topic.",
        "Answer relevance checks that the answer addresses the query (catches off-topic answers). Faithfulness would be high here because every claim is in the context.",
        topic="ragas", level=2),
    mcq("What is 'data contamination' in the context of static benchmarks?",
        ["The public test questions leak into a new model's training data, so it can score high by memorisation rather than reasoning",
         "The benchmark contains spelling mistakes",
         "Two benchmarks share the same metric",
         "The model's outputs are toxic"], 0,
        "Public questions, web-scale training data.",
        "Because static benchmarks are public, their items often end up in web crawls used for pre-training. The model then looks smarter than it is. Live benchmarks such as LiveCodeBench use problems created after the model's cutoff to avoid this.",
        topic="benchmarks", level=2,
        analogy="Like an interview candidate who has seen the exact question on a forum the night before."),
    mcq("LiveCodeBench pulls problems from recent coding contests held after a model's training cutoff. Which weakness of static benchmarks does that address, and at what cost?",
        ["It prevents contamination, but it is harder to maintain and to compare across time",
         "It removes the need for unit tests, but it is slower",
         "It removes judge bias, but it needs humans",
         "It lowers cost, but it is less realistic"], 0,
        "Fresh questions cannot have been memorised.",
        "Live / dynamic benchmarks test true generalisation because the model cannot have seen the items. The trade-off in the course table: resists contamination / harder to compare and maintain.",
        diagram="""
 |---- training data ----| cutoff |-- new contests --|
   static benchmark items          live benchmark items
   (may have leaked)               (cannot have leaked)
""",
        topic="benchmarks", level=2),
    mcq("What are the two dominant prompt patterns for LLM-as-a-Judge listed in the course?",
        ["Single-answer grading on a rubric, and pairwise comparison of A vs B",
         "Zero-shot and few-shot",
         "Chain-of-thought and tree-of-thought",
         "Greedy and beam search"], 0,
        "One answer at a time, or two side by side.",
        "Single-answer grading scores one output (1-10 or pass/fail). Pairwise comparison picks the better of two; it is the basis of MT-Bench and Arena-Hard.",
        topic="llm-judge", level=2),
    mcq("Which judge prompt design does the course recommend?",
        ["An explicit rubric with criteria scored separately, reasoning before the final score, and a reference answer when available",
         "Just 'Rate this answer 1-10', so the judge is not biased by instructions",
         "Ask for the score first, then the reasoning",
         "Use the same model that produced the answer, so it understands its own style"], 0,
        "Make the judge think and give it a yardstick.",
        "Rubric (helpfulness, factuality, formatting, safety separately) + chain-of-thought before the score + a reference answer raise agreement with humans. Using the same model invites self-preference bias.",
        topic="llm-judge", level=2),
    tf("Before every release, re-running a fixed 'golden set' of prompts with expected behaviour and failing the build on a score drop is a form of offline evaluation.", True,
       "It runs before users see the change.",
       "A golden set in CI is the LLM version of a regression test suite: a prompt, model or retriever change that drops the score blocks the deploy.",
       analogy="The LLM version of a regression test suite that blocks a merge.",
        topic="online-offline", level=2),
    fill("The course's metric that breaks a long answer into atomic facts and reports the fraction supported by a knowledge source is called ____.", "FActScore",
         "Fact + Score.",
         "FActScore = supported atomic facts / total atomic facts. Higher means fewer hallucinations in long-form text. The decomposition and verification are LLM-driven, so it is expensive.",
         topic="faithfulness", level=2),
    mcq("Place BERTScore on the course's three framing axes.",
        ["Extrinsic, reference-based, automatic",
         "Intrinsic, reference-free, automatic",
         "Extrinsic, reference-free, human",
         "Intrinsic, reference-based, human"], 0,
        "It needs a gold answer and no person.",
        "BERTScore scores a task output (extrinsic) by comparing it to a gold reference (reference-based), computed by a model with no human in the loop (automatic). Being reference-based is exactly why it cannot judge faithfulness to retrieved context.",
        topic="framing", level=2, diagram=AXES),
    tf("If a model assigns probability 1/V to every token of a vocabulary of size V (pure guessing), its perplexity is V.", True,
       "PPL = 1 / (geometric mean probability).",
       "Every step has P = 1/V, so PPL = (V^N)^(1/N) = V. The slides' example: P = 0.01 everywhere gives PPL = 100, a 'highly surprised' model. PPL = 1 is the other extreme (P = 1 every step).",
       topic="perplexity", level=2),
    mcq("Your team must check that a model follows formatting instructions like 'answer in exactly 3 bullet points, no more than 50 words'. Which benchmark/metric family does the course map to instruction following?",
        ["IFEval / MT-Bench, with human pairwise as a check",
         "BLEU",
         "Perplexity",
         "Exact match against one reference"], 0,
        "The instructions themselves are checkable rules.",
        "IFEval uses verifiable instructions (word counts, bullet counts, keywords) that a script can check; MT-Bench uses a judge on multi-turn prompts. BLEU against a reference cannot tell whether a constraint was obeyed.",
        topic="task-metrics", level=2),
    tf("BERTScore values depend on which embedding model computed them, so a paper should state the model (e.g. roberta-large) when it reports BERTScore.", True,
       "Different encoder, different cosines.",
       "Cosine similarities, and so P/R/F1, change with the encoder and layer. Comparing BERTScores computed with different models is like comparing perplexities across tokenizers.",
       topic="semantic-metrics", level=2),
    mcq("You ship a new prompt to 10% of users and compare thumbs-up rate and escalation rate against the old prompt on the other 90%. What is this?",
        ["An online A/B test",
         "An offline golden-set evaluation",
         "A static benchmark",
         "Red teaming"], 0,
        "Real users, split traffic.",
        "Online evaluation measures behaviour on live traffic. A/B testing splits users between variants and compares business and quality signals, which an offline test set cannot capture.",
        topic="online-offline", level=2),
    # ------------------------------------------------------------------ L3
    mcq("A team evaluates a release-notes summariser. Reference R: 'the patch fixes the login timeout bug on mobile' (9 words). Candidate C: 'the patch fixes the login bug' (6 words). Compute BLEU-2 with brevity penalty and uniform weights w1 = w2 = 0.5.",
        ["About 0.542 (BP = 0.607, p1 = 1.0, p2 = 4/5)",
         "About 0.894 (BP ignored)",
         "About 0.405 (BP = 0.607, p2 = 4/8)",
         "About 0.667 (6/9, the length ratio)"], 0,
        "BP = e^(1 - r/c); p2 divides by candidate bigrams.",
        "BP = e^(1 - 9/6) = e^(-0.5) = 0.607. p1: all 6 candidate words appear in R ('the' twice, R also has it twice) so 6/6. Candidate bigrams: the patch, patch fixes, fixes the, the login match; 'login bug' doesn't: p2 = 4/5. BLEU-2 = 0.607 * exp(0.5 ln 1 + 0.5 ln 0.8) = 0.607 * 0.894 = 0.542. Dividing p2 by the reference's 8 bigrams is the ROUGE-2 formula.",
        topic="bleu", level=3),
    mcq("Same item: R = 'the patch fixes the login timeout bug on mobile', C = 'the patch fixes the login bug'. What are ROUGE-1 recall and ROUGE-2 recall?",
        ["ROUGE-1 = 6/9 = 0.667, ROUGE-2 = 4/8 = 0.500",
         "ROUGE-1 = 6/6 = 1.0, ROUGE-2 = 4/5 = 0.800",
         "ROUGE-1 = 6/9 = 0.667, ROUGE-2 = 4/5 = 0.800",
         "ROUGE-1 = 5/9 = 0.556, ROUGE-2 = 4/8 = 0.500"], 0,
        "Recall: divide by the reference's n-gram counts.",
        "All 6 candidate unigrams are in R (9 unigrams): 6/9. R has 8 bigrams; the candidate matches 4 of them: 4/8. 1.0 and 0.8 are the precision values (BLEU's p1 and p2). 5/9 comes from wrongly counting the repeated 'the' once.",
        topic="rouge", level=3,
        diagram="""
R: the patch fixes the login timeout bug on mobile
C: the patch fixes the login bug
   [=======================]  4 bigrams match
                       login bug -> no match
"""),
    out("import math\n"
        "from collections import Counter\n"
        "def ng(t, n): return [tuple(t[i:i+n]) for i in range(len(t)-n+1)]\n"
        "def bleu2(c, r):\n"
        "    c, r = c.split(), r.split()\n"
        "    bp = 1.0 if len(c) > len(r) else math.exp(1 - len(r) / len(c))\n"
        "    ps = []\n"
        "    for n in (1, 2):\n"
        "        cc, rc = Counter(ng(c, n)), Counter(ng(r, n))\n"
        "        ps.append(sum(min(v, rc[g]) for g, v in cc.items()) / sum(cc.values()))\n"
        "    return round(bp * math.exp(0.5 * math.log(ps[0]) + 0.5 * math.log(ps[1])), 3)\n"
        "print(bleu2('the battery lasts two days', 'the new battery lasts nearly two full days'))",
        ["0.274", "0.5", "0.549", "0.198"], 0,
        "Count the bigrams carefully: the reference has 'the new battery', not 'the battery'.",
        "BP = e^(1 - 8/5) = 0.549. p1 = 5/5 = 1. Candidate bigrams: 'the battery' (no), 'battery lasts' (yes), 'lasts two' (no), 'two days' (no): p2 = 1/4. BLEU-2 = 0.549 * sqrt(0.25) = 0.274. Every word matched, yet the score is low: BLEU's bigrams reward word order and fluency.",
        topic="bleu", level=3),
    out("from collections import Counter\n"
        "ref = 'the update improves battery life'.split()\n"
        "cand = ('the update improves battery life and also improves speed '\n"
        "        'and also fixes many bugs in the app').split()\n"
        "hit = sum(min(v, Counter(ref)[w]) for w, v in Counter(cand).items())\n"
        "print(round(hit / len(ref), 2), round(hit / len(cand), 2))",
        ["1.0 0.29", "0.29 1.0", "1.0 1.0", "0.29 0.29"], 0,
        "Which denominator is the long one?",
        "ROUGE-1 recall = 5/5 = 1.0: every reference word appears. Precision = 5/17 = 0.29. A padded, rambling summary maximises recall-only ROUGE, which is why you report ROUGE precision/F1 too, or a length limit.",
        topic="rouge", level=3,
        question="This prints ROUGE-1 recall then ROUGE-1 precision for a long candidate. What does it print?"),
    mcq("An insurance-FAQ RAG bot is checked on one item. The answer splits into 4 atomic claims; 3 are supported by the retrieved context. The retriever returned 8 chunks, of which 2 are relevant. The answer needed 3 facts; 2 of them were in the retrieved chunks. What are faithfulness, context precision and context recall?",
        ["0.75, 0.25, 0.67",
         "0.75, 0.67, 0.25",
         "0.25, 0.75, 0.67",
         "0.75, 0.25, 1.00"], 0,
        "claims for faithfulness, chunks for precision, facts for recall.",
        "Faithfulness = 3/4 = 0.75. Context precision = relevant / retrieved chunks = 2/8 = 0.25. Context recall = needed facts retrieved / needed facts = 2/3 = 0.67. Swapping precision and recall is the usual slip: precision is about noise in what was fetched, recall about what is missing.",
        diagram="""
 claims : 3 supported / 4      -> faithfulness
 chunks : 2 relevant  / 8      -> context precision
 facts  : 2 retrieved / 3 need -> context recall
""",
        topic="ragas", level=3),
    mcq("For the same item (faithfulness 0.75, context precision 0.25, context recall 0.67), which pair of fixes follows the course's RAGAS diagnosis?",
        ["Add a cross-encoder reranker / tighter threshold for the noisy retrieval, and a grounding instruction or claim verifier for the unsupported claim",
         "Fine-tune the generator on more data; nothing to do on retrieval",
         "Increase top-k to 16 so recall rises; precision does not matter",
         "Switch the metric to BLEU, which is cheaper"], 0,
        "Each low metric points at a different component.",
        "Low context precision = over-retrieval: rerank, tighten the similarity threshold, use hybrid dense + BM25. Low faithfulness = generator not grounded: 'only use the provided context, say if it is missing', a post-hoc claim verifier, lower temperature. Context recall below 1 also means a needed fact is missing, so check chunking/coverage. Raising top-k would make precision even worse.",
        topic="ragas", level=3),
    mcq("A candidate summary has unigram precision p1 = 1.0 against the reference, yet the RAG faithfulness check marks one of its claims unsupported. What is the right reading?",
        ["Every candidate word appears in the reference, but n-gram metrics only check surface overlap with a gold string; they never look at the retrieved context, so they cannot see that the claim is not entailed",
         "p1 = 1.0 proves the answer is correct, so the faithfulness check must be wrong",
         "The faithfulness check is reference-based and so is unreliable",
         "BLEU-2 would detect it if you used 4-grams instead"], 0,
        "What does each metric compare the candidate against?",
        "This is the exam's favourite twist. p1 = 1.0 says the word choice is lexically 'perfect' relative to the reference. But lexical overlap is orthogonal to logical entailment: BLEU/ROUGE compare to a reference string, not to what the evidence supports. Faithfulness checks claims against the retrieved context. Higher-order n-grams are still lexical.",
        topic="faithfulness", level=3),
    mcq("A team member says: 'Model P has lower perplexity than model Q on our probe text, so P is the better model; the BLEU result showing Q ahead on summarisation must be noise.' Using the course's framing, what is wrong?",
        ["Perplexity is intrinsic (next-token likelihood); summarisation quality is extrinsic. Lower PPL does not guarantee downstream gains, so the BLEU gap is real evidence",
         "Nothing: lower perplexity always means better summaries",
         "BLEU is intrinsic and perplexity extrinsic, so they cannot be compared",
         "Perplexity must be multiplied by BLEU to get the true score"], 0,
        "Two different questions are being measured.",
        "The makeup papers ask exactly this. PPL measures how well a model predicts text; summarisation tests content selection, faithfulness and format. The course: 'Lower PPL does not guarantee downstream gains (intrinsic != extrinsic)'.",
        topic="perplexity", level=3),
    mcq("After a supervised fine-tuning round on support dialogues, a model's validation perplexity on the general pre-training validation set goes up. A colleague wants to roll back the SFT because 'PPL went up, so the model got worse'. What does the course say?",
        ["The reasoning is wrong: perplexity is not a meaningful progress signal for SFT/RLHF stages, so judge the SFT with task metrics (ROUGE, judge, human preference)",
         "Roll back: any PPL increase means the model is worse",
         "Roll back only if PPL more than doubled",
         "Recompute PPL with a different tokenizer to see if it falls"], 0,
        "SFT deliberately shifts the distribution.",
        "SFT moves the output distribution from 'continue web text' to 'complete the task', so next-token likelihood on the old distribution can rise while the model gets better at its job. The slides: perplexity is not defined for SFT/RLHF stages; use task metrics there. (Do keep an eye on general skills, but with general benchmarks, not raw PPL.)",
        topic="perplexity", level=3),
    out("import numpy as np\n"
        "# cosine similarities: rows = candidate tokens, cols = reference tokens\n"
        "S = np.array([[0.9, 0.2, 0.1],\n"
        "              [0.3, 0.8, 0.4]])\n"
        "P = S.max(axis=1).mean()      # each candidate token -> best reference token\n"
        "R = S.max(axis=0).mean()      # each reference token -> best candidate token\n"
        "F = 2 * P * R / (P + R)\n"
        "print(round(float(P), 3), round(float(R), 3), round(float(F), 3))",
        ["0.85 0.7 0.768", "0.7 0.85 0.768", "0.85 0.85 0.85", "0.45 0.35 0.394"], 0,
        "Precision walks the candidate side, recall the reference side.",
        "BERTScore greedy matching: P = mean of row maxima = (0.9 + 0.8)/2 = 0.85; R = mean of column maxima = (0.9 + 0.8 + 0.4)/3 = 0.7; F1 = 0.768. The third reference token has no good match, which pulls recall down: the candidate missed some reference meaning.",
        diagram="""
            ref1  ref2  ref3
 cand1  [   0.9   0.2   0.1 ]   row max -> precision
 cand2  [   0.3   0.8   0.4 ]
 col max:   0.9   0.8   0.4      -> recall
""",
        topic="semantic-metrics", level=3),
    mcq("Why can BERTScore catch some errors that BLEU misses, yet still not be a good faithfulness metric for a RAG system?",
        ["It compares contextual embeddings, so semantically mismatched matches score lower than in BLEU; but it is still reference-based and never looks at the retrieved context the answer must be faithful to",
         "It uses an LLM judge internally, which is biased",
         "It only works for translation",
         "It ignores word meaning and only checks order"], 0,
        "What is BERTScore compared against?",
        "This is a past-paper model answer. Contextual embeddings make BERTScore sensitive to meaning, not just spelling. But in RAG the failure is 'claim not entailed by the retrieved chunks', and a metric that compares to a gold string cannot measure that. Entailment/grounding metrics (RAGAS faithfulness, FActScore, AlignScore) fill the gap.",
        topic="semantic-metrics", level=3),
    out("ratings = {'A': 1200.0, 'B': 1000.0}\n"
        "K = 32\n"
        "def expected(ra, rb): return 1 / (1 + 10 ** ((rb - ra) / 400))\n"
        "ea = expected(ratings['A'], ratings['B'])\n"
        "# one arena battle: users vote for B\n"
        "ratings['A'] += K * (0 - ea)\n"
        "ratings['B'] += K * (1 - (1 - ea))\n"
        "print(round(ea, 2), round(ratings['A'], 1), round(ratings['B'], 1))",
        ["0.76 1175.7 1024.3", "0.5 1184.0 1016.0", "0.76 1224.3 975.7", "0.24 1192.3 1007.7"], 0,
        "A was expected to win; an upset moves ratings a lot.",
        "A's expected score vs a 200-point weaker model is 0.76. B wins, so A loses 32 * 0.76 = 24.3 points and B gains the same. Arena-style leaderboards aggregate many such pairwise votes (the course: Bradley-Terry / Elo with 95% CI).",
        topic="benchmarks", level=3),
    out("# judge verdicts on the same 4 answer pairs, shown in both orders\n"
        "ab = ['A', 'A', 'A', 'B']      # first slot = answer A\n"
        "ba = ['B', 'A', 'B', 'B']      # first slot = answer B\n"
        "first_slot_wins = sum(v == 'A' for v in ab) + sum(v == 'B' for v in ba)\n"
        "consistent = sum(x == y for x, y in zip(ab, ba))\n"
        "print(first_slot_wins, 'of 8 |', consistent, 'of 4 consistent')",
        ["6 of 8 | 2 of 4 consistent", "4 of 8 | 4 of 4 consistent", "6 of 8 | 4 of 4 consistent", "5 of 8 | 2 of 4 consistent"], 0,
        "Consistent means the same winner whichever order it was shown in.",
        "The first-shown answer wins 3 + 3 = 6 of 8 times, and only pairs 2 and 4 keep the same winner after swapping. That is position bias. The fix is to judge both orders and count a win only when they agree (or average), treating disagreements as ties.",
        diagram="""
 order 1: [A][B] -> judge -> winner
 order 2: [B][A] -> judge -> winner
 same winner both times? count it; else tie
""", analogy="Like a reviewer who tends to approve whichever pull request is first in the queue.",
        topic="llm-judge", level=3,
        question="This checks a pairwise LLM judge for position bias. What does it print?"),
    mcq("A judge model consistently prefers the longer of two answers, even when the shorter one is correct and the longer one pads with generic advice. Which bias is this, and what is one mitigation?",
        ["Verbosity bias; add a rubric that scores correctness and concision separately and tell the judge length is not a criterion (or length-control the comparison)",
         "Position bias; swap the order",
         "Self-preference bias; use a different judge family",
         "Contamination; switch to a live benchmark"], 0,
        "Longer looks more helpful.",
        "Verbosity bias: judges (and humans) reward length. The course notes human arenas share the same position, verbosity and style biases. Mitigate with explicit rubrics, length-controlled win rates, and calibration against human labels.",
        topic="llm-judge", level=3),
    mcq("A vendor's model scores near the top of MMLU. Your HR-policy RAG bot built on it gives wrong leave balances half the time. What does the course's model-vs-system split tell you to do?",
        ["Run a system evaluation of the whole pipeline (retrieval metrics, faithfulness, task accuracy on your own questions); a model benchmark says little about your system",
         "Trust MMLU and look for a bug in the UI",
         "Switch to a model with an even higher MMLU score",
         "Measure the model's perplexity on HR documents"], 0,
        "MMLU tests the model in isolation on general knowledge.",
        "Model evaluation (benchmarks, perplexity) tells you about the raw LLM. Your bot's failures can come from chunking, retrieval, prompts or stale data, none of which MMLU sees. System evaluation scores the end-to-end behaviour on your task.",
        diagram="""
 model eval : [ LLM ]  -> MMLU, perplexity
 system eval: query -> [chunker][retriever][prompt][LLM]
                       -> answer judged on YOUR task
""",
        topic="framing", level=3),
    out("facts = {\n"
        "    'born in 1950': True,\n"
        "    'studied physics': True,\n"
        "    'won a Nobel prize': False,\n"
        "    'taught at a university': True,\n"
        "    'wrote three novels': False,\n"
        "}\n"
        "print(round(sum(facts.values()) / len(facts), 2))",
        ["0.6", "0.4", "3", "1.5"], 0,
        "Supported atomic facts / all atomic facts.",
        "A FActScore-style check splits a generated biography into atomic facts, verifies each against a knowledge source, and reports the supported fraction: 3/5 = 0.6. The two unsupported facts are hallucinations that a fluent paragraph would hide.",
        topic="faithfulness", level=3,
        question="A FActScore-style checker has verified each atomic fact of a generated bio. What does this print?"),
    mcq("The reference says 'the quick brown fox jumped' and the candidate says 'the fast tan fox leapt'. A human calls them equivalent. Which metric is most likely to agree with the human?",
        ["BERTScore (or METEOR with synonym matching), since it rewards paraphrases",
         "BLEU-4",
         "ROUGE-2",
         "Exact match"], 0,
        "The slides' own example of n-gram failure.",
        "N-gram metrics are surface-level: 'quick brown fox' vs 'fast tan fox' share almost nothing, so BLEU/ROUGE punish a correct paraphrase. Embedding-based BERTScore and synonym-aware METEOR give credit for meaning.",
        topic="semantic-metrics", level=3),
    mcq("A team uses model family X as the judge to compare their own fine-tune of X against a competitor model Y. X wins 70% of comparisons. What should make you suspicious?",
        ["Self-preference bias: judges tend to favour outputs that resemble their own style; use a judge from a different family or human spot checks",
         "Position bias, which only affects single-answer grading",
         "Contamination of the judge's rubric",
         "Nothing: a stronger judge is always unbiased"], 0,
        "The judge is grading its own relative.",
        "The past-paper answer lists judge biases as verbosity, self-preference and position. A judge from the same family shares style and phrasing with one contestant. Cross-family judges, multiple judges, or a human-labelled calibration set reduce this.",
        topic="llm-judge", level=3),
    mcq("Your golden-set score is unchanged after a release, but online the thumbs-down rate doubles, mostly on questions about a product launched last week. What is the best next step?",
        ["Treat it as a distribution shift: sample and label the new failing traffic, add those cases to the golden set, and fix retrieval/data for the new product",
         "Ignore it; the offline score is the ground truth",
         "Raise the temperature to make answers more varied",
         "Delete the thumbs-down button, it is noisy"], 0,
        "The offline set no longer represents what users ask.",
        "Offline sets go stale. Online signals reveal new query types the golden set doesn't cover. The loop is: monitor online -> mine failures -> add them to the offline set -> fix -> regression-test before the next deploy.",
        topic="online-offline", level=3,
        diagram="""
 offline golden set --CI--> deploy --> online signals
        ^                                  |
        +---- add mined failures ----------+
"""),
    out("def ngrams(text, n):\n"
        "    t = text.split()\n"
        "    return {' '.join(t[i:i+n]) for i in range(len(t) - n + 1)}\n"
        "bench_q = 'a train leaves the station at noon travelling at sixty km per hour'\n"
        "crawl = 'forum post: a train leaves the station at noon travelling at sixty km per hour, find'\n"
        "overlap = ngrams(bench_q, 8) & ngrams(crawl, 8)\n"
        "print(len(overlap) > 0, len(overlap))",
        ["True 5", "True 1", "False 0", "True 6"], 0,
        "The crawl has 'hour,' with a comma, so the last 8-gram doesn't match.",
        "The 13-word question has 6 eight-grams; the last one ends in 'hour' but the crawl has 'hour,' so 5 match. Any long n-gram overlap between a benchmark item and the training crawl is a contamination red flag. This is how labs screen for leaked GSM8K/MMLU items.",
        topic="benchmarks", level=3,
        question="A simple contamination check looks for shared 8-grams between a benchmark item and a training document. What does it print?"),
    mcq("For a code-generation feature, why does the course prefer pass@k over BLEU against a reference solution?",
        ["Two correct programs can share few tokens and a near-identical one can fail; pass@k measures functional correctness by running tests",
         "pass@k is cheaper because it needs no execution",
         "BLEU cannot handle programming-language tokens",
         "pass@k is reference-based like BLEU but uses 4-grams"], 0,
        "Correctness for code means it runs.",
        "Code has many correct forms. A variable rename tanks BLEU but not correctness, while one wrong operator keeps BLEU high and breaks the program. pass@k runs the code against unit tests (it needs a sandbox, so it is not cheaper).",
        analogy="Judge a pull request by running CI, not by diffing it against the senior engineer's solution.",
        topic="task-metrics", level=3),
    tf("The course notes that human preference arenas are not bias-free: human voters show the same position, verbosity and style biases as LLM judges.", True,
       "Humans are the ground truth, but not perfect.",
       "Arenas capture helpfulness and tone that reference metrics miss, but they are expensive, slow, and humans also prefer longer, nicely formatted answers. That is why arenas report confidence intervals and some add style control.",
       topic="benchmarks", level=3),
    tf("In the course's model answer, perplexity is described as 'reference-free in the sense of no gold string', but its weakness is that low perplexity does not mean an answer is correct or faithful.", True,
       "It needs text, but not a gold answer.",
       "Perplexity scores how surprised the model is by some text, with no reference answer to compare to. It measures fluency relative to the model itself; a confident hallucination can have very low perplexity.",
       topic="perplexity", level=3),
    # ------------------------------------------------------------------ L4
    out("import math\n"
        "text_bytes = 40\n"
        "# same 40-byte text, two tokenizers\n"
        "A = {'tokens': 10, 'mean_nll': 2.0}     # 32k vocab\n"
        "B = {'tokens': 8,  'mean_nll': 2.4}     # 64k vocab\n"
        "for name, m in (('A', A), ('B', B)):\n"
        "    ppl = math.exp(m['mean_nll'])\n"
        "    bpb = m['tokens'] * m['mean_nll'] / (text_bytes * math.log(2))\n"
        "    print(name, round(ppl, 2), round(bpb, 3))",
        ["A 7.39 0.721\nB 11.02 0.692", "A 7.39 0.692\nB 11.02 0.721", "A 7.39 0.5\nB 11.02 0.6", "A 2.0 0.721\nB 2.4 0.693"], 0,
        "Total nats = tokens * mean NLL; divide by bytes and by ln 2.",
        "Per-token PPL says A is better (7.39 < 11.02), but B splits the text into fewer, harder tokens. Normalised to the same unit, bits per byte, B is better (0.692 < 0.721). This is why the course says PPL is only comparable with an identical tokenizer and eval set, and the model answer suggests bits-per-byte for cross-tokenizer comparison.",
        analogy="Like comparing two storage systems per GB rather than per 'block' when each uses a different block size.",
        topic="perplexity", level=4),
    mcq("Two models are compared on the same text. Model A uses a 16k-vocabulary tokenizer, model B a 32k one. Exactly why are their perplexities not comparable?",
        ["The same text is split into different numbers of tokens N with different per-token distributions, so each PPL is a geometric mean over a different unit; compare in bits-per-byte or bits-per-character instead",
         "Bigger vocabularies always give higher perplexity, so you can just rescale by 32k/16k",
         "They are comparable as long as both use natural log",
         "Perplexity depends on the GPU type, not the tokenizer"], 0,
        "What is the 'N' in the Nth root?",
        "The 16k tokenizer usually produces more, easier sub-tokens; the 32k one fewer, harder tokens. PPL averages per token, so the two numbers measure surprise per different unit. There is no simple vocab-ratio rescale; a tokenizer-invariant unit (bits per byte) fixes it.",
        topic="perplexity", level=4),
    out("import math\n"
        "from collections import Counter\n"
        "def ng(t, n): return [tuple(t[i:i+n]) for i in range(len(t)-n+1)]\n"
        "c = 'the parcel was delivered to the wrong flat'.split()\n"
        "r = 'the parcel was delivered to a wrong address'.split()\n"
        "ps = []\n"
        "for n in range(1, 5):\n"
        "    cc, rc = Counter(ng(c, n)), Counter(ng(r, n))\n"
        "    ps.append(sum(min(v, rc[g]) for g, v in cc.items()) / sum(cc.values()))\n"
        "bleu4 = 0.0 if min(ps) == 0 else math.exp(sum(math.log(p) for p in ps) / 4)\n"
        "print([round(p, 2) for p in ps], round(bleu4, 3))",
        ["[0.75, 0.57, 0.5, 0.4] 0.541","[0.75, 0.57, 0.5, 0.4] 0.0", "[0.75, 0.57, 0.33, 0.2] 0.0", "[0.75, 0.57, 0.5, 0.4] 0.555"], 0,
        "Equal lengths, so BP = 1. Count 4-grams: 'the parcel was delivered', ...",
        "c = r = 8, so BP = 1. Matches: 6/8 unigrams, 4/7 bigrams, 3/6 trigrams ('the parcel was', 'parcel was delivered', 'was delivered to'), 2/5 four-grams. BLEU-4 = geometric mean = exp(mean ln p) = 0.541 (0.555 is the arithmetic mean, the wrong combiner). If any p_n were 0 the geometric mean would collapse to 0, which is why sentence-level BLEU-4 on short outputs needs smoothing.",
        topic="bleu", level=4),
    tf("Because BLEU combines the n-gram precisions with a geometric mean, a single short candidate with zero matching 4-grams gets BLEU-4 = 0, even if its unigram and bigram precision are high.", True,
       "What is ln(0)?",
       "exp(sum w_n ln p_n) with p_4 = 0 is exp(-infinity) = 0. That is why BLEU is meant as a corpus-level metric (counts pooled over many sentences) and why sentence-level BLEU uses smoothing.",
       topic="bleu", level=4),
    mcq("A grader marks this exam answer wrong: 'BLEU-2 = BP x (p1 + p2)/2 with BP = e^(1 - c/r)'. Which TWO errors does it contain?",
        ["The precisions are combined by a weighted GEOMETRIC mean exp(sum w_n ln p_n), not an arithmetic mean; and BP = e^(1 - r/c) for c <= r",
         "Only the BP is wrong; the arithmetic mean is the standard form",
         "Only the mean is wrong; e^(1 - c/r) is the standard BP",
         "BLEU-2 has no brevity penalty at all"], 0,
        "Check both the combiner and the exponent.",
        "BLEU = BP * exp(w1 ln p1 + w2 ln p2) = BP * sqrt(p1 * p2) for uniform weights. The flipped BP e^(1 - c/r) is greater than 1 for short candidates, rewarding exactly what BP is meant to punish.",
        topic="bleu", level=4),
    out("def lcs(a, b):\n"
        "    d = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]\n"
        "    for i, x in enumerate(a):\n"
        "        for j, y in enumerate(b):\n"
        "            d[i+1][j+1] = d[i][j] + 1 if x == y else max(d[i][j+1], d[i+1][j])\n"
        "    return d[-1][-1]\n"
        "r = 'police arrested the suspect after a long chase'.split()\n"
        "c = 'after a chase the police arrested the suspect'.split()\n"
        "L = lcs(r, c); P, R = L / len(c), L / len(r)\n"
        "print(L, round(2 * P * R / (P + R), 3))",
        ["4 0.5", "8 1.0", "3 0.375", "7 0.875"], 0,
        "The LCS must keep the order of both sentences.",
        "Both have 8 words and share 7 of them, so ROUGE-1 F1 would be 7/8 = 0.875. But the clauses are swapped. The longest in-order common subsequence is 'police arrested the suspect' (4; 'after a chase' is only 3). P = R = 4/8, so ROUGE-L F1 = 0.5. ROUGE-L exposes the reordering that ROUGE-1 misses.",
        topic="rouge", level=4),
    mcq("A short candidate scores BLEU-2 = 0.45 and ROUGE-2 recall = 0.20 on the same item. A student writes: 'contradiction, one of them is miscomputed'. What is the better explanation?",
        ["No contradiction: BLEU's precision divides by the few candidate n-grams (most of which match), ROUGE recall divides by the many reference n-grams (most of which are missing)",
         "BLEU must be wrong because it should always be lower than ROUGE",
         "ROUGE must be wrong because recall cannot be below precision",
         "They use different tokenizers"], 0,
        "Same matches, different denominators.",
        "The course's own example ('the cat mat' vs 'the cat is on the mat') makes this point: the machine was precise but its recall is low. BLEU asks 'how much of the output is correct?', ROUGE 'how much of the reference did it include?'.",
        diagram="""
 candidate bigrams:  4   (3 match) -> precision 3/4
 reference bigrams: 15   (3 match) -> recall    3/15
 same 3 matches, different denominators
""",
        topic="rouge", level=4),
    out("def context_precision(rel):        # rel[k] = 1 if chunk at rank k+1 is relevant\n"
        "    hits, s = 0, 0.0\n"
        "    for k, r in enumerate(rel, 1):\n"
        "        if r:\n"
        "            hits += 1\n"
        "            s += hits / k            # precision@k at each relevant rank\n"
        "    return round(s / max(1, sum(rel)), 3)\n"
        "for order in ([1, 1, 0, 0], [0, 0, 1, 1]):\n"
        "    print(order, sum(order) / len(order), context_precision(order))",
        ["[1, 1, 0, 0] 0.5 1.0\n[0, 0, 1, 1] 0.5 0.417",
         "[1, 1, 0, 0] 0.5 0.5\n[0, 0, 1, 1] 0.5 0.5",
         "[1, 1, 0, 0] 0.5 1.0\n[0, 0, 1, 1] 0.5 0.5",
         "[1, 1, 0, 0] 1.0 1.0\n[0, 0, 1, 1] 0.0 0.417"], 0,
        "One formula ignores rank, the other averages precision@k at the relevant ranks.",
        "The course formula (relevant / retrieved) gives 0.5 for both orders. The RAGAS library's context precision is rank-aware: relevant chunks at the top score 1.0, at the bottom (1/3 + 2/4)/2 = 0.417. For the exam use the course formula; in a real project know that ranking matters because LLMs attend best to the top of the context.",
        diagram="""
 rank:      1   2   3   4
 order A:   R   R   .   .   -> rank-aware 1.0
 order B:   .   .   R   R   -> rank-aware 0.417
 course formula: 2/4 for both
""",
        topic="ragas", level=4),
    mcq("A RAG answer contains a claim that is true in the real world (the model knew it from pre-training) but is not in any retrieved chunk. The product shows citations for every sentence. How should the eval treat it?",
        ["As unfaithful: faithfulness only counts claims entailed by the retrieved context, and an uncited claim breaks the citation contract even if it happens to be true",
         "As faithful, because it is true",
         "As a context-recall failure only",
         "Ignore it; true claims cannot hurt"], 0,
        "Faithfulness vs truthfulness again, from the other side.",
        "Truthful but unfaithful. In a grounded product, parametric claims cannot be audited and are where outdated or invented facts slip in. It may also hint at a context-recall gap (the fact should have been retrieved), so check both.",
        topic="faithfulness", level=4),
    mcq("Your judge agrees with human labels on 90% of a 200-item calibration set. 90% of the items are 'good' answers. What is the key concern before you gate releases on it?",
        ["A judge that labels everything 'good' would also score 90%; check agreement on the 'bad' class (or a chance-corrected statistic like Cohen's kappa) before trusting it",
         "None: 90% agreement is excellent",
         "200 items is too many, it will overfit",
         "The judge must be fine-tuned on the 200 items first"], 0,
        "What would a lazy judge score?",
        "Raw agreement on an imbalanced set hides a judge that never flags bad answers, which are the ones a release gate exists to catch. Measure per-class agreement, kappa, and look at the disagreements before replacing human review.",
        topic="llm-judge", level=4),
    out("import math\n"
        "c = 8                       # candidate length\n"
        "refs = [6, 9]               # two human references\n"
        "r = min(refs, key=lambda L: (abs(L - c), L))   # best-match length\n"
        "bp = 1.0 if c > r else math.exp(1 - r / c)\n"
        "print(r, round(bp, 3))",
        ["9 0.882", "6 1.0", "15 0.325", "7.5 1.0"], 0,
        "With several references, r is the reference length closest to the candidate.",
        "The course defines r as the effective reference length: the best-match (closest) reference length. |8 - 9| = 1 beats |8 - 6| = 2, so r = 9 and BP = e^(1 - 9/8) = 0.882. Using the shorter reference would give BP = 1; summing (15) or averaging (7.5) the lengths is not the BLEU rule.",
        diagram="""
 candidate length c = 8
 ref A: 6  (|8-6| = 2)
 ref B: 9  (|8-9| = 1)  <- closest, r = 9
 BP = e^(1 - 9/8)
""",
        topic="bleu", level=4,
        question="BLEU with two references: which reference length is used, and what is the BP?"),
    mcq("Arena-style leaderboards fit a Bradley-Terry model over all pairwise votes rather than simply replaying online Elo updates. Why?",
        ["Online Elo depends on the order of the battles and the K-factor; Bradley-Terry estimates one strength per model from all votes at once and gives stable ratings with confidence intervals",
         "Bradley-Terry needs no human votes",
         "Elo cannot handle more than two models",
         "Bradley-Terry ignores ties, which makes it faster"], 0,
        "Replay the same votes in a different order with Elo: do you get the same ratings?",
        "Sequential Elo is path-dependent: the same set of votes in a different order gives different ratings. Bradley-Terry is a maximum-likelihood fit of P(i beats j) = s_i / (s_i + s_j) over all votes, and bootstrapping gives the 95% CIs the course mentions.",
        topic="benchmarks", level=4),
    mcq("A team optimises its prompts and fine-tune until the in-house LLM judge's score rises from 7.1 to 9.3. Human raters see no improvement. What most likely happened?",
        ["Goodhart's law: the system learned the judge's preferences (length, format, confident tone) rather than better answers; the judge must be re-calibrated against humans and kept separate from the optimisation loop",
         "Human raters are always wrong when they disagree with a judge",
         "The judge's temperature was too low",
         "The benchmark is contaminated"], 0,
        "When a measure becomes a target...",
        "Any automatic proxy that you optimise against can be gamed, LLM judges especially (verbosity, style). Hold out a human-labelled set, rotate or ensemble judges, and score criteria separately so padding cannot buy points.",
        analogy="Like chasing a test-coverage percentage: you get many asserts that test nothing.",
        topic="llm-judge", level=4),
    mcq("A model jumps 12 points on a public static benchmark after a new pre-training data mix. Which check best separates real gains from contamination?",
        ["Re-test on freshly written or perturbed versions of the items (new numbers, reworded questions) and on a live benchmark created after the cutoff; a big drop means memorisation",
         "Re-run the same benchmark with a different random seed",
         "Check the model's perplexity on the benchmark answers; low perplexity proves reasoning",
         "Compute BLEU between answers and the gold labels"], 0,
        "Memorised items break when you change their surface.",
        "Contamination shows up as a gap between the original items and equivalent unseen ones. Very low perplexity on benchmark text is itself a contamination SIGNAL, not proof of reasoning. Live benchmarks like LiveCodeBench exist for this reason.",
        topic="benchmarks", level=4),
    mcq("You must decide whether a new RAG prompt can replace the old one in production. Which evidence plan is strongest?",
        ["Offline: golden set with RAGAS faithfulness and context metrics plus judge scores calibrated on human labels, as a CI gate; then online: a small A/B with task-success, escalation and complaint rates, ramping only if guardrail metrics hold",
         "Offline BLEU against last month's answers, then full rollout",
         "Online only: ship to everyone and watch thumbs-up",
         "Offline only: if MMLU is unchanged, ship"], 0,
        "One automatic + one task-level check, offline then online.",
        "The course rule is 'no single metric captures quality, always pair one automatic and one task-level check'. Offline catches regressions cheaply; online confirms on real traffic with a safe ramp. BLEU against old answers rewards copying the old prompt's wording.",
        topic="online-offline", level=4),
    tf("On the course's three axes, FActScore is an extrinsic, automatic metric that is reference-free in the sense of needing no gold answer string, though it does need a knowledge source to verify facts against.", True,
       "What does FActScore compare each atomic fact against?",
       "The slides list FActScore under reference-free (with LLM-as-judge and perplexity). It checks each atomic fact against a knowledge source C, not against a gold summary, which is exactly why it can measure factual precision when BLEU cannot.",
       topic="framing", level=4),
    fill("To compare language models with different tokenizers fairly, you report total negative log-likelihood (in bits) divided by the number of UTF-8 bytes. This unit is called bits per ____.", "byte",
         "Not per token.",
         "Bits-per-byte (or bits-per-character) normalises by the text itself, which is the same for both tokenizers, so the numbers become comparable.",
         topic="perplexity", level=4),
    fill("BLEU is designed as a ____-level metric: n-gram counts are pooled over all test sentences before the precisions and brevity penalty are computed.", "corpus",
         "Opposite of sentence-level.",
         "Pooling counts over a corpus avoids the zero-4-gram collapse of single short sentences. Averaging sentence BLEUs gives a different, usually lower, number.",
         topic="bleu", level=4),
    # ------------------------------------------------------------------ fills (mixed levels)
    fill("A metric that compares a model output to a gold human answer (like BLEU or ROUGE) is called reference-____.", "based",
         "The opposite is reference-free.",
         "Reference-based metrics need a gold answer; reference-free ones (LLM-as-judge, perplexity, FActScore) score the output on its own or against a source.",
         topic="framing", level=1),
    fill("In BLEU's modified n-gram precision, each n-gram's count is capped at the maximum number of times it appears in any single reference. This capping is called ____.", "clipping",
         "Count_clip.",
         "Clipping stops 'the the the the the the the' from scoring 7/7: 'the' is credited at most as many times as it appears in one reference.",
         topic="bleu", level=2),
    fill("ROUGE-L is computed from the longest common ____ of the candidate and the reference.", "subsequence",
         "In order, gaps allowed.",
         "Longest common subsequence (LCS), not substring: the words keep their relative order but need not be adjacent.",
         topic="rouge", level=2),
    fill("In RAGAS, relevant chunks / retrieved chunks is the metric called context ____.", "precision",
         "How much of what was fetched is useful?",
         "Context precision measures noise in retrieval. Context recall (needed facts retrieved / needed facts total) measures what is missing.",
         topic="ragas", level=2),
    fill("Pairwise arena votes are usually turned into a ranking with an Elo-style rating fitted by the ____-Terry model.", "Bradley",
         "Two surnames.",
         "The Bradley-Terry model gives each model a strength s and models P(i beats j) = s_i / (s_i + s_j); the course slide names it for Chatbot Arena.",
         topic="benchmarks", level=3),
    fill("A judge prefers whichever answer it is shown first, regardless of quality. This is called ____ bias.", "position",
         "Where the answer sits in the prompt.",
         "Position bias. The standard fix is to run each pair in both orders and only count a win when both orders agree.",
         topic="llm-judge", level=2),
    tf("Using several human references per test item usually makes BLEU and ROUGE more reliable than a single reference.", True,
       "More than one valid way to say it.",
       "The slides list it under the n-gram family's limits: a single reference is often too narrow, so valid paraphrases get punished. Multiple references widen what counts as a match.",
       topic="rouge", level=3),
    # END
]
