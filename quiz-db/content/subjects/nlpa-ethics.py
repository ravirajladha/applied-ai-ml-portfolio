from helpers import mcq, tf, out, fill

SUBJECT = "nlpa-ethics"

TOPICS = [
    ("why-ethics", "Why privacy and ethics matter; the ethical risk lifecycle"),
    ("data-consent", "Data issues: consent, collection, provenance, retention"),
    ("data-bias", "Data issues: corpus bias, representation, annotation"),
    ("pii", "PII detection, masking and anonymisation"),
    ("model-bias", "Model issues: bias amplification and stereotyping"),
    ("fairness-metrics", "Fairness metrics"),
    ("model-risks", "Model issues: memorisation, hallucination, calibration, explainability"),
    ("deployment", "Deployment issues: misuse, monitoring, logging, accountability"),
    ("privacy-tech", "Differential privacy and DP-SGD"),
    ("mitigations", "Debiasing, documentation and tooling"),
    ("case-studies", "Real-world case studies"),
]

LIFECYCLE = """
Data Collection -> Annotation -> Training -> Evaluation -> Deployment
 PII, consent      label bias    bias amp.   fairness     monitoring
 representative-   sensitive     leakage     explain-     abuse
 ness              categories                ability      governance
 <------------- governance spans the whole lifecycle ------------->
"""

RISK_STACK = """
 +-----------------------------------------------+
 | Application: UX, misuse, prompt injection     |
 | Model:       hallucination, drift, explain.   |
 | Data:        privacy, retention, stale facts  |
 | Infra:       latency, scaling, logging, sec.  |
 +-----------------------------------------------+
 controls: access control, safety filters,
           red-team testing, continuous monitoring
"""

QUESTIONS = [
    # ------------------------------------------------------------------ L1
    mcq("The course opens Session 8 with 'Why privacy and ethics matter in NLP'. Which reason is on that slide?",
        ["NLP systems ingest emails, chats and medical records, so the data is highly personal",
         "NLP models are too small to store any training data",
         "Text data is always public, so privacy rules do not apply",
         "Ethics only matters for image models, not text"], 0,
        "Think about what text an NLP system actually reads.",
        "The slide lists four reasons: massive use of personal data, re-identification risk (models memorise and leak PII), bias and discrimination at scale, and regulations (GDPR, DPDP, CCPA, EU AI Act). The wrong options are the excuses teams use to skip the work.",
        topic="why-ethics", level=1),
    mcq("Which of these is India's data-protection law that the course lists next to GDPR and CCPA?",
        ["DPDP (Digital Personal Data Protection Act)", "HIPAA", "COPPA", "SOX"], 0,
        "The course names one law per region: EU, India, USA.",
        "GDPR (EU), DPDP (India), CCPA (USA) and the EU AI Act. HIPAA (US health), COPPA (US children) and SOX (US finance) are real laws but not the ones on the slide.",
        topic="why-ethics", level=1),
    tf("In the course's view, ethics is something you handle once, at model-training time.", False,
       "Look at the last line of the lifecycle diagram.",
       "The course says 'Connect ethics to the full NLP application lifecycle, not only model training' and 'governance spans the entire lifecycle': data collection, annotation, training, evaluation, deployment and monitoring.",
       topic="why-ethics", level=1, diagram=LIFECYCLE),
    mcq("A team scrapes forum posts to train a chatbot without asking the posters. Which data issue from the course is this?",
        ["Consent and collection: scraping public data without explicit consent",
         "Bias amplification",
         "Hallucination",
         "Vendor lock-in"], 0,
        "The course splits data issues into consent, dataset bias, and PII.",
        "The 'Consent & Collection' column lists scraping without explicit consent, no opt-out for data subjects, unclear retention and no purpose limitation. 'It's public' is not consent.",
        topic="data-consent", level=1),
    fill("Using collected data only for the purpose it was collected for, and not for something new, is called purpose ____.", "limitation",
         "The course's slide says 'lack of purpose ____'.",
         "Purpose limitation is a GDPR principle: data gathered to answer support tickets should not quietly become training data for a marketing model. The course lists its absence as a data issue.",
         analogy="Like OAuth scopes: a token granted 'read:tickets' should not be used to 'write:marketing'.", topic="data-consent", level=1),
    mcq("A sentiment corpus has 90% English and 10% everything else. A Tamil user gets worse results. Which data issue is this?",
        ["Representation imbalance: some languages or groups are underrepresented",
         "Annotator label bias",
         "PII leakage",
         "Model hallucination"], 0,
        "Who is missing from the data?",
        "The course lists 'underrepresented minorities in corpora' and 'geographic and language imbalance'. A model learns little about what it rarely sees, so minority dialects and languages get worse service.",
        topic="data-bias", level=1),
    mcq("What does 'historical bias' in a text corpus mean?",
        ["The text reflects past social unfairness, which the model learns as if it were normal",
         "The corpus is too old to load",
         "The dates in the text are wrong",
         "The model is biased towards older tokens in the context"], 0,
        "Data records the world as it was, not as it should be.",
        "If ten years of resumes were mostly men hired, a model learns 'male = hire'. The course's line: training data must reflect the desired future parity, not historical bias.",
        topic="data-bias", level=1),
    mcq("Which of these is PII (personally identifiable information)?",
        ["An email address such as asha.k@example.com",
         "The word 'refund'",
         "The average sentence length of a corpus",
         "A product's model number"], 0,
        "Could it point to one specific person?",
        "PII is any data that can identify a person alone or combined with other data: names, emails, phone numbers, Aadhaar or PAN numbers, addresses. The course's data-issues slide lists 'names, emails, SSNs in training data'.",
        topic="pii", level=1),
    fill("Replacing 'Call Priya on 9876543210' with 'Call [PERSON] on [PHONE]' before storing or training is called PII ____ (one word, the course's word for hiding a span with a tag).", "masking",
         "The course's lab function is called mask_pii.",
         "Masking swaps each detected span for a tag. It is the first stage of the course's production setup ('PII scrubbing'), done with regexes, spaCy NER or Presidio.",
         topic="pii", level=1),
    mcq("Asked for 'a short story about a pilot and a flight attendant', a text generator makes the pilot a man and the attendant a woman in 19 of 20 runs. What is this called?",
        ["Stereotyping: the model reproduces a social stereotype from its data",
         "Hallucination",
         "Data drift",
         "Overfitting to the test set"], 0,
        "It is about groups and roles, not about facts.",
        "Models learn co-occurrence patterns such as 'pilot ... he' from text and repeat them. The course: 'Models can amplify patterns present in data, including harmful stereotypes.'",
        topic="model-bias", level=1),
    mcq("In the course's key fairness metrics table, what does demographic parity require?",
        ["Equal positive-prediction (selection) rates across groups",
         "Equal accuracy across groups",
         "Equal numbers of people from each group in the training set",
         "The same model for every group"], 0,
        "It looks only at how often each group gets the positive outcome.",
        "Demographic parity: P(prediction = 1) is the same for every group, regardless of the true labels. Equal accuracy is the tempting wrong answer: the exams show two groups with identical accuracy and very different selection rates.",
        topic="fairness-metrics", level=1),
    mcq("Which fairness metric from the course asks that qualified people in every group are selected at the same rate (equal true positive rates)?",
        ["Equal opportunity", "Demographic parity", "Individual fairness", "Calibration"], 0,
        "TPR = qualified people correctly selected.",
        "Equal opportunity = equal TPR. Equalized odds is stricter (equal TPR and equal FPR). Demographic parity ignores the true labels entirely.",
        topic="fairness-metrics", level=1),
    tf("Counterfactual fairness, as the course defines it, means the prediction stays the same if only the person's group (for example the name or gender) is changed.", True,
       "Swap one attribute, keep everything else.",
       "The exam's counterfactual test swaps only the name on an otherwise identical resume and checks that P(shortlist) hardly moves. A large change means the model is using the group signal.",
       topic="fairness-metrics", level=1),
    mcq("A chatbot states a made-up refund rule in confident, fluent language. Which model issue is this?",
        ["Hallucination: fluent but unsupported output",
         "Data drift",
         "Demographic parity violation",
         "Consent violation"], 0,
        "It sounds right but nothing supports it.",
        "The course: 'Large models may hallucinate fluent but unsupported answers', and overconfident or hallucinated facts 'cause downstream harm' when people act on them.",
        topic="model-risks", level=1),
    mcq("Why does the course call black-box transformers a problem for compliance?",
        ["They give no rationale for a decision, so it is hard to audit or explain it to the affected person",
         "They cannot be deployed on GPUs",
         "They always have lower accuracy than linear models",
         "They cannot process more than one language"], 0,
        "Think about a rejected loan applicant asking 'why?'.",
        "The slide: 'Black-box transformers provide no rationale: impossible to audit for compliance (GDPR Art. 22)'. Article 22 covers decisions made solely by automated processing; people can ask for human review and an explanation.",
        topic="model-risks", level=1),
    mcq("Which deployment issue from the course is 'deployed models may generate harmful, hateful or toxic outputs'?",
        ["No output filtering (no guardrails)", "Vendor lock-in", "Audit trail gaps", "Rate limiting"], 0,
        "What sits between the model and the user?",
        "The course's six deployment issues: no output filtering, lack of monitoring, audit trail gaps, access-control failures, adversarial attacks and vendor lock-in. An output filter (guardrail) blocks or rewrites toxic replies before the user sees them.",
        topic="deployment", level=1),
    fill("Watching a deployed model for drift, abuse, privacy leakage and safety regressions over time is called ____ (one word).", "monitoring",
         "The last stage of the course's production setup.",
         "The course: 'Monitoring is essential for drift, abuse, privacy leakage and safety regressions.' Its monitoring stage includes drift detection, fairness dashboards, an incident-response SOP and a GDPR deletion pipeline.",
         topic="deployment", level=1),
    mcq("What is the basic idea of differential privacy?",
        ["Add calibrated random noise so the output barely changes whether or not any one person's data is included",
         "Encrypt the dataset with a password",
         "Delete the training data after training",
         "Train a different model for each user"], 0,
        "One person should not be detectable from the result.",
        "Differential privacy bounds how much any single record can change a result, by adding noise. The course lists DP-SGD ('training with privacy guarantees') as the fix for memorisation.",
        diagram="""
  true answer 120 -> + noise -> 118.7 published
            .
           / \\      Laplace noise, centred at 0
         _/   \\_    narrow = little noise (big eps)
   _____/       \\_____  wide = more noise (small eps)
""", topic="privacy-tech", level=1,
        analogy="Like rounding a dashboard metric: the trend is still useful, but you cannot tell whether one particular customer is in it."),
    mcq("What is a model card?",
        ["A short document published with a model that states its intended use, evaluation results (including across groups) and limitations",
         "The GPU the model runs on",
         "A login token for the model API",
         "A diagram of the model's layers"], 0,
        "The course's governance checklist: 'Model card published with limitations and risks'.",
        "Model cards (Mitchell et al. 2019) are the model's README: what it is for, what it is not for, how it was evaluated, per-group results and known risks. The course puts them in the training stage of its production setup.",
        topic="mitigations", level=1,
        analogy="Like the README and CHANGELOG of a library: anyone who imports it should know its limits before shipping."),
    mcq("Amazon's experimental hiring tool, in the course's case study, downgraded resumes from women. What caused it?",
        ["It learned from 10 years of male-dominated hiring data",
         "A developer coded a rule against women",
         "Women's resumes were longer than the context window",
         "A prompt-injection attack"], 0,
        "Where did its idea of a 'good' candidate come from?",
        "The model learned patterns from historical hiring, not an unbiased notion of merit. Takeaways: dataset history matters as much as architecture, and accuracy alone is not a deployment criterion. (The slide labels it 'Amazon Rekognition / NLP Hiring Tool'; Rekognition is actually a separate image-analysis product.)",
        topic="case-studies", level=1),

    # ------------------------------------------------------------------ L2
    mcq("Match the course's lifecycle stage to its typical risk: which pairing is correct?",
        ["Annotation -> label bias and sensitive categories",
         "Data collection -> bias amplification",
         "Deployment -> annotator disagreement",
         "Evaluation -> consent"], 0,
        "Recall the diagram: each stage has its own risk words.",
        "Data collection: PII, consent, representativeness. Annotation: label bias, sensitive categories. Training: bias amplification, leakage. Evaluation: fairness, explainability, robustness. Deployment: monitoring, abuse, governance.",
        topic="why-ethics", level=2, diagram=LIFECYCLE),
    tf("The course says evaluation of an NLP application should go beyond accuracy and include harm, bias and misuse scenarios.", True,
       "One of the four summary bullets.",
       "Accuracy says how often the model is right on average; it says nothing about who carries the errors or what happens when someone misuses it. The exams make exactly this point with equal-accuracy groups.",
       topic="why-ethics", level=2),
    mcq("A support-ticket dataset is kept 'forever, just in case'. Which data-governance principle does this break?",
        ["Retention and data minimisation: keep only what you need, only as long as you need it",
         "Demographic parity",
         "Equal opportunity",
         "Calibration"], 0,
        "The course lists 'unclear data retention policies'.",
        "Data governance must address provenance, retention, consent and data minimisation. Data you no longer hold cannot leak, be subpoenaed or be memorised by the next model.",
        topic="data-consent", level=2,
        analogy="Like log rotation: you set a TTL on logs so the disk (and your liability) does not grow forever."),
    mcq("What does 'data provenance' (lineage) tracking give an NLP team?",
        ["A record of where each piece of training data came from and how it was transformed, so you can audit consent and remove data later",
         "Faster tokenisation",
         "A higher BLEU score",
         "Automatic translation of the data"], 0,
        "The course lists 'no data provenance tracking' as a data issue.",
        "Without lineage you cannot answer 'did this user consent?', 'which model saw this record?' or honour an erasure request. The course's data pipeline stage includes 'data lineage logging'.",
        topic="data-consent", level=2),
    mcq("Three annotators label tweets as 'toxic'. Posts written in a regional English dialect are marked toxic far more often, even when harmless. Which data issue is this?",
        ["Label bias from annotators: guidelines and annotators encode their own subjectivity",
         "Underrepresentation only; labels are always objective",
         "PII leakage",
         "Hallucination"], 0,
        "The labels themselves carry the bias.",
        "The course: 'Annotation guidelines may encode human subjectivity or social stereotypes.' A model trained on these labels then flags that dialect as toxic in production. Studies of toxicity datasets have found exactly this for African American English.",
        topic="data-bias", level=2),
    out("from collections import Counter\n"
        "langs = ['en'] * 82 + ['hi'] * 12 + ['ta'] * 4 + ['or'] * 2\n"
        "c = Counter(langs)\n"
        "n = len(langs)\n"
        "print({k: round(v / n * 100) for k, v in c.items() if v / n < 0.05})",
        ["{'ta': 4, 'or': 2}", "{'hi': 12, 'ta': 4, 'or': 2}", "{'en': 82}", "{'ta': 0.04, 'or': 0.02}"], 0,
        "Keep languages under 5% of the corpus, shown as percentages.",
        "Hindi is 12%, so it passes the filter; Tamil (4%) and Odia (2%) are flagged. A representation audit like this is the first check for the course's 'geographic and language imbalance' issue: those languages need more data or targeted evaluation.",
        topic="data-bias", level=2),
    out("import re\n"
        "AADHAAR = re.compile(r'\\b\\d{4}\\s?\\d{4}\\s?\\d{4}\\b')\n"
        "for s in ['ID 2345 6789 0123 ok', 'ID 234567890123 ok',\n"
        "          'ID 2345-6789-0123 ok']:\n"
        "    print(AADHAAR.sub('[AADHAAR]', s))",
        ["ID [AADHAAR] ok\nID [AADHAAR] ok\nID 2345-6789-0123 ok",
         "ID [AADHAAR] ok\nID [AADHAAR] ok\nID [AADHAAR] ok",
         "ID [AADHAAR] ok\nID 234567890123 ok\nID 2345-6789-0123 ok",
         "ID 2345 6789 0123 ok\nID [AADHAAR] ok\nID 2345-6789-0123 ok"], 0,
        "\\s? allows one optional space; does it allow a hyphen?",
        "The pattern accepts 12 digits with or without single spaces, but not hyphens, so the hyphenated ID leaks through. Regex maskers fail silently on formats nobody wrote a pattern for: test them against real variants before trusting them.",
        topic="pii", level=2),
    mcq("A team must mask person names in free-text chat logs ('spoke to ravi from accounts'). Why does the course pair regex with spaCy NER (or Presidio) instead of using regex alone?",
        ["Names have no fixed format, so a statistical NER model is needed; regex suits fixed formats like emails, phones and IDs",
         "Regex is slower than NER for emails",
         "NER can only detect phone numbers",
         "spaCy encrypts the names"], 0,
        "Which PII types have a pattern you can write down?",
        "Emails, phones, card and Aadhaar numbers have shapes regex can match. Names, addresses and organisations do not ('ravi', lower case, mid-sentence), so the course's tools table lists 'spaCy + custom NER: named entity masking pipeline' and Presidio, which combines both.",
        diagram="""
text -> regex (EMAIL, PHONE, ID formats)
     -> NER   (PERSON, ORG, LOC, no fixed shape)
     -> merge spans -> mask -> [PERSON] [PHONE]
""", topic="pii", level=2),
    tf("Replacing every customer name with a consistent code (Asha -> CUST_0193) and keeping the lookup table makes the dataset anonymous.", False,
       "Can someone with the table reverse it?",
       "That is pseudonymisation. Anyone with the mapping can re-identify every record, so GDPR still treats it as personal data. Anonymisation must be irreversible. Pseudonymisation is still useful (it limits who sees names) but it is not a licence to share the data.",
       diagram="""
  Asha  -> CUST_0193      lookup table kept
  Vikram-> CUST_0194  ==> reversible
  ==> still personal data (pseudonymised)
""", topic="pii", level=2),
    mcq("What does 'bias amplification' mean?",
        ["The model's outputs are more skewed than its training data (e.g. 66% in the data becomes 84% in predictions)",
         "The model copies the exact bias rate of the data, no more and no less",
         "Turning up the learning rate",
         "Adding more layers to reduce bias"], 0,
        "Compare the rate in the outputs with the rate in the data.",
        "Models exploit any correlation that lowers loss, so a majority pattern can become near-universal in predictions. Zhao et al. (2017) found a 'cooking -> woman' skew growing from the training set to the model's outputs. The course lists 'bias amplification' at the training stage.",
        diagram="""
            woman  man
 training:  66%    34%
 predicted: 84%    16%   <- amplified
""", topic="model-bias", level=2),
    mcq("The course's model-issues slide says 'sentiment models score identical text differently based on inferred gender, race or religion'. Which test exposes this most directly?",
        ["Score template sentences that differ only in the identity term ('I am a Hindu/Muslim/Christian woman, the food was fine')",
         "Measure overall accuracy on the test set",
         "Count the tokens in each review",
         "Check the model's perplexity"], 0,
        "Hold everything constant except the group word.",
        "Template (counterfactual) tests isolate the identity term, so any score difference is bias by construction. Overall accuracy can be high while these gaps exist, because identity words are rare in a random test set.",
        topic="model-bias", level=2),
    out("c = {'urban': (120, 200), 'rural': (45, 150)}   # (selected, applicants)\n"
        "sr = {g: s / n for g, (s, n) in c.items()}\n"
        "dpd = abs(sr['urban'] - sr['rural'])\n"
        "print({g: round(v, 2) for g, v in sr.items()}, round(dpd, 2))",
        ["{'urban': 0.6, 'rural': 0.3} 0.3", "{'urban': 120, 'rural': 45} 75",
         "{'urban': 0.6, 'rural': 0.3} 0.5", "{'urban': 0.6, 'rural': 0.3} 2.0"], 0,
        "Selection rate = selected / applicants; DPD = absolute difference.",
        "SR(urban) = 120/200 = 0.60, SR(rural) = 45/150 = 0.30, DPD = 0.30. Comparing raw counts (120 vs 45) is the common slip: groups of different sizes must be compared as rates. 0.5 is the disparate impact ratio, a different metric.",
        topic="fairness-metrics", level=2),
    mcq("Group A: TP = 40, FN = 10. Group B: TP = 24, FN = 16. What is the equal opportunity difference |TPR(A) - TPR(B)|?",
        ["0.20", "0.16", "0.40", "0.60"], 0,
        "TPR = TP / (TP + FN), for each group.",
        "TPR(A) = 40/50 = 0.80, TPR(B) = 24/40 = 0.60, EOD = 0.20. 16 is the difference in raw TP counts, which ignores group size. A qualified person in group B is a quarter less likely to be selected.",
        diagram="""
        TP   FN   TPR = TP/(TP+FN)
  A     40   10   0.80
  B     24   16   0.60
  EOD = |0.80 - 0.60| = 0.20
""", topic="fairness-metrics", level=2),
    tf("Equalized odds is satisfied if two groups have equal true positive rates, even if their false positive rates differ.", False,
       "Odds = both kinds of error.",
       "That is only equal opportunity. Equalized odds needs equal TPR AND equal FPR. In the Sep 2026 paper both TPR and FPR differed by 0.30, so neither held.",
       analogy="Like an SLO that tracks both missed alerts and false pages: being good at one does not excuse the other.", topic="fairness-metrics", level=2),
    out("pairs = {'Arjun/Ayesha': (0.612, 0.548), 'Ravi/Rekha': (0.508, 0.497)}\n"
        "for k, (a, b) in pairs.items():\n"
        "    d = round(abs(a - b), 3)\n"
        "    print(k, d, 'FAIL' if d > 0.05 else 'PASS')",
        ["Arjun/Ayesha 0.064 FAIL\nRavi/Rekha 0.011 PASS",
         "Arjun/Ayesha 0.064 PASS\nRavi/Rekha 0.011 PASS",
         "Arjun/Ayesha 0.064 FAIL\nRavi/Rekha 0.011 FAIL",
         "Arjun/Ayesha -0.064 FAIL\nRavi/Rekha -0.011 PASS"], 0,
        "Absolute difference, threshold 0.05.",
        "Each pair is the same resume with only the name swapped. |0.612 - 0.548| = 0.064 > 0.05 fails the course's counterfactual test; 0.011 passes. One failing pair is enough to flag the model: it is reading the name.",
        topic="fairness-metrics", level=2),
    mcq("What is the difference between memorisation and hallucination as the course uses them?",
        ["Memorisation: the model reproduces training data verbatim (a privacy risk). Hallucination: it produces fluent content nothing supports (a correctness risk)",
         "They are two names for the same thing",
         "Memorisation only happens in small models; hallucination only in large ones",
         "Hallucination leaks PII; memorisation invents facts"], 0,
        "One copies, one invents.",
        "Memorisation is the extraction risk ('large LLMs can regurgitate verbatim PII seen during training'); hallucination is 'fluent but unsupported answers'. Both are model issues, but the fixes differ: DP and scrubbing for one, grounding and verification for the other.",
        topic="model-risks", level=2),
    mcq("A classifier says 'fraud' with 95% confidence, but among all its 95%-confidence calls only 60% are actually fraud. What is wrong?",
        ["It is poorly calibrated (overconfident)",
         "It has perfect calibration",
         "It violates demographic parity",
         "It is memorising PII"], 0,
        "Does 95% confident mean right 95% of the time?",
        "A calibrated model's 95% calls are right about 95% of the time. The course: 'overconfident predictions mislead decision-makers'. Its evaluation stage includes 'calibration checks' for this reason.",
        topic="model-risks", level=2),
    mcq("In the course's deployment risk stack, where does 'employees pasted confidential source code into a public chatbot' belong?",
        ["Data layer (privacy, retention)",
         "Infrastructure layer (latency, scaling)",
         "Model layer (hallucination)",
         "It is not a risk"], 0,
        "What went wrong: speed, correctness, or where the data ended up?",
        "The course uses the 2023 Samsung leak as its data-layer example: sensitive data left the company through prompts and could be retained by the provider. Fixes are policy and tooling: approved internal tools, PII/secret filters on prompts, retention controls.",
        topic="deployment", level=2, diagram=RISK_STACK),
    out("rec = {'ts': '2026-11-02T10:15', 'model': 'v3.2',\n"
        "       'user_text': 'my PAN is ABCDE1234F',\n"
        "       'reply': 'Your request is logged.', 'error': None,\n"
        "       'phone': '9876543210'}\n"
        "SAFE = ('ts', 'model', 'reply', 'error')\n"
        "print(sorted(k for k in rec if k in SAFE))",
        ["['error', 'model', 'reply', 'ts']", "['ts', 'model', 'reply', 'error']",
         "['error', 'model', 'phone', 'reply', 'ts', 'user_text']", "['phone', 'user_text']"], 0,
        "Keep only allow-listed keys, then sort alphabetically.",
        "This is the course's 'what to log' answer as code: keep model outputs, timestamp, model version and error types; drop raw user input with PII and identifiers. An allow-list is safer than a deny-list because a new sensitive field is dropped by default.",
        topic="deployment", level=2),
    mcq("What does 'dual use' mean for an NLP capability?",
        ["The same capability can serve good and harmful ends, e.g. a persuasive-text generator for health campaigns or for disinformation",
         "The model runs on both CPU and GPU",
         "The model supports two languages",
         "Training and inference use the same data"], 0,
        "Who else could use this tool?",
        "Text generation, voice cloning, author profiling and sentiment-based targeting all have legitimate and harmful uses. Deployment controls (access control, rate limits, usage policies, monitoring for abuse) exist because you cannot make the capability itself one-sided.",
        topic="deployment", level=2),
    out("sensitivity = 1          # one person changes a count by at most 1\n"
        "for eps in (2.0, 0.5, 0.1):\n"
        "    print(eps, sensitivity / eps)",
        ["2.0 0.5\n0.5 2.0\n0.1 10.0", "2.0 2.0\n0.5 0.5\n0.1 0.1", "2.0 0.5\n0.5 2.0\n0.1 1.0", "2.0 4.0\n0.5 1.0\n0.1 0.2"], 0,
        "Laplace scale b = sensitivity / epsilon.",
        "Smaller epsilon -> bigger noise scale -> more privacy and less accuracy. At eps = 0.1 a count is perturbed by noise of scale 10, fine for a count of 50,000, useless for a count of 7. The common error is thinking larger epsilon means more privacy.",
        topic="privacy-tech", level=2),
    tf("In differential privacy, a larger epsilon gives a stronger privacy guarantee.", False,
       "Epsilon is the allowed privacy loss.",
       "Epsilon bounds how much one person's data can change the output's probabilities (by a factor of at most e^epsilon). Larger epsilon = looser bound = less noise = weaker privacy. Typical deployments pick epsilon between about 0.1 and 10.",
       topic="privacy-tech", level=2),
    mcq("A resume classifier gives a higher score to 'Mark' than 'Priya' on identical resumes. Which pair of mitigations does the course's lab apply?",
        ["Name masking (replace names with a [NAME] token) plus counterfactual data augmentation",
         "A bigger model plus more epochs",
         "Removing the test set",
         "Lowering the decision threshold for everyone"], 0,
        "Take the signal away, and teach the model it doesn't matter.",
        "Masking removes the token the model associated with the label; counterfactual augmentation adds name-swapped copies so the remaining features are seen with both groups. After both, the lab's two resumes scored 0.500 each.",
        topic="mitigations", level=2),
    mcq("What are 'datasheets for datasets' (Gebru et al.)?",
        ["Standard documents describing a dataset's motivation, composition, collection process, consent, preprocessing and recommended uses",
         "Spreadsheets of raw training data",
         "The GPU spec sheet used for training",
         "A list of the dataset's file sizes"], 0,
        "Model cards document models; this documents the data.",
        "Like electronics datasheets, they make the dataset's assumptions explicit: who is in it, who is missing, how it was labelled, whether people consented. They answer the course's data-issue questions (consent, provenance, representation) before anyone trains on it.",
        topic="mitigations", level=2),
    mcq("Which course case study is mainly a consent violation?",
        ["Clearview AI scraping billions of face images without consent",
         "Amazon's hiring tool",
         "A chatbot demo stating a wrong astronomy fact",
         "Service outages under high demand"], 0,
        "Who agreed to have their data used?",
        "Clearview scraped 3B+ images and was fined EUR 20M in Italy. The takeaway: data sourcing needs a legal basis (consent or legitimate interest) under GDPR, public or not. (The slide calls it an 'NLP pipeline'; it is really computer vision, but the consent lesson is the same for scraped text.)",
        topic="case-studies", level=2),

    # ------------------------------------------------------------------ L3
    mcq("A loan-eligibility text classifier selects 45% of Group A applicants and 33% of Group B. Using the course's disparate impact ratio and the four-fifths rule, what do you conclude?",
        ["DI = 0.33 / 0.45 = 0.733 < 0.80, so there is adverse impact against Group B",
         "DI = 0.45 / 0.33 = 1.36 > 0.80, so the model passes",
         "DPD = 0.12 < 0.80, so the model passes",
         "DI = 0.733 > 0.5, so the model passes"], 0,
        "Lower rate over higher rate, then compare with 0.80.",
        "DI = SR(lower) / SR(higher) = 0.733. Under the four-fifths rule anything below 0.80 signals adverse impact. Dividing the other way gives a number above 1 that always 'passes', and comparing the DPD (0.12) with 0.80 mixes up two metrics.",
        diagram="""
selection rate
 A |#############################  0.45
 B |#####################          0.33
   DI = 0.33 / 0.45 = 0.733  <  0.80 line
""", topic="fairness-metrics", level=3),
    out("cm = {'A': dict(TP=36, FN=4, FP=12, TN=48),\n"
        "      'B': dict(TP=27, FN=3, FP=21, TN=49)}\n"
        "for g, m in cm.items():\n"
        "    tpr = m['TP'] / (m['TP'] + m['FN'])\n"
        "    fpr = m['FP'] / (m['FP'] + m['TN'])\n"
        "    print(g, round(tpr, 2), round(fpr, 2))",
        ["A 0.9 0.2\nB 0.9 0.3", "A 0.9 0.2\nB 0.9 0.2", "A 0.36 0.12\nB 0.27 0.21", "A 0.75 0.25\nB 0.56 0.3"], 0,
        "TPR = TP/(TP+FN), FPR = FP/(FP+TN).",
        "TPR is 0.90 in both groups, so equal opportunity holds. FPR is 0.20 vs 0.30, so equalized odds does not: unqualified Group B applicants are wrongly selected more often. Whether that harms or favours B depends on the task (a wrong 'fraud' flag harms; a wrong 'shortlist' helps).",
        topic="fairness-metrics", level=3),
    mcq("A hospital triage bot's audit: Group A accuracy 0.75, TPR 0.75; Group B accuracy 0.75, TPR 0.375. The vendor says 'accuracy is identical, so it is fair'. What is the best reply?",
        ["Accuracy pools all errors; here truly urgent Group B patients are missed twice as often (FN), which equal opportunity exposes",
         "The vendor is right: equal accuracy means equal treatment",
         "TPR does not matter in healthcare, only accuracy",
         "The fix is to raise overall accuracy to 0.90"], 0,
        "Which kind of error falls on which group?",
        "This is the Sep 2026 end-sem argument: accuracy aggregates over classes and error types, so it can be equal while false negatives concentrate on one group. Group B's TPR of 0.375 vs 0.75 violates equal opportunity; for triage a miss is the dangerous error.",
        diagram="""
 group  acc   TPR   missed urgent cases
   A    0.75  0.75  10 of 40
   B    0.75  0.375 25 of 40
 same accuracy, very different misses
""", topic="fairness-metrics", level=3,
        analogy="Like two API endpoints with the same 99% success rate, where one fails only on premium customers: the average hides who gets hurt."),
    out("import re\n"
        "P = [('[EMAIL]', r'\\b[\\w.-]+@[\\w.-]+\\.\\w+\\b'),\n"
        "     ('[PHONE]', r'\\b\\d{3}[-.]?\\d{3}[-.]?\\d{4}\\b'),\n"
        "     ('[MONEY]', r'\\$\\d+(,\\d{3})*(\\.\\d+)?'),\n"
        "     ('[PERSON]', r'\\b[A-Z][a-z]+ [A-Z][a-z]+\\b')]\n"
        "t = 'candidate Neha Rao, neha.rao@mail.com, 912-555-0147, asks $85,000.'\n"
        "for tag, rx in P:\n"
        "    t = re.sub(rx, tag, t)\n"
        "print(t)",
        ["candidate [PERSON], [EMAIL], [PHONE], asks [MONEY].",
         "candidate [PERSON], [PERSON], [PHONE], asks [MONEY].",
         "candidate Neha Rao, [EMAIL], [PHONE], asks [MONEY].",
         "candidate [PERSON], [EMAIL], [PHONE], asks $[MONEY]."], 0,
        "Apply the patterns in order; the email is lower case.",
        "EMAIL goes first and swallows neha.rao@mail.com; PHONE matches 912-555-0147; MONEY matches $85,000 including the $; PERSON matches the two capitalised words 'Neha Rao'. This is the exam's mask_pii walk-through with new values.",
        topic="pii", level=3),
    out("import re\n"
        "OUT = {'EMAIL': r'\\b[\\w.-]+@[\\w.-]+\\.\\w+\\b',\n"
        "       'PHONE': r'\\b\\d{3}[-.]?\\d{3}[-.]?\\d{4}\\b',\n"
        "       'MONEY': r'\\$\\d+(,\\d{3})*(\\.\\d+)?',\n"
        "       'CARD_LAST4': r'\\b\\d{4}\\b'}\n"
        "reply = 'Your order ships in 2026 and costs $1,499.'\n"
        "hits = [k for k, rx in OUT.items() if re.search(rx, reply)]\n"
        "print(hits, 'BLOCKED' if hits else 'allowed')",
        ["['MONEY', 'CARD_LAST4'] BLOCKED", "['MONEY'] BLOCKED", "[] allowed", "['CARD_LAST4'] BLOCKED"], 0,
        "What else is a stand-alone 4-digit number?",
        "The year 2026 matches \\b\\d{4}\\b, a false positive of the over-broad CARD_LAST4 pattern, so a harmless reply is blocked. The exam asks for exactly this: name the false positive and say why (any 4 digits look like a card). Fixes: require context ('ending in', 'card'), or validate before blocking.",
        topic="pii", level=3),
    out("from collections import Counter\n"
        "rows = [('560001', '30-39', 'F'), ('560001', '30-39', 'F'),\n"
        "        ('560001', '30-39', 'M'), ('560034', '20-29', 'M'),\n"
        "        ('560034', '20-29', 'M'), ('560034', '20-29', 'M')]\n"
        "groups = Counter(rows)          # (pincode, age band, gender)\n"
        "print(min(groups.values()), len(groups))",
        ["1 3", "3 2", "2 3", "1 6"], 0,
        "k = size of the smallest group sharing all quasi-identifiers.",
        "Groups: (560001, 30-39, F) x2, (560001, 30-39, M) x1, (560034, 20-29, M) x3. The single male in 560001 aged 30-39 is unique, so the table is only 1-anonymous: anyone who knows those three facts finds his row. Names were already removed; it didn't help.",
        topic="pii", level=3),
    tf("A dataset with names, emails and phone numbers removed can still identify people, because combinations like pincode + date of birth + gender are often unique.", True,
       "Quasi-identifiers.",
       "Sweeney showed that ZIP code, birth date and sex uniquely identify most Americans. The course lists 'inference attacks' and 're-identification risk'. That is why anonymisation needs generalisation (age bands, truncated pincodes) and k-anonymity checks, not just dropping direct identifiers.",
       topic="pii", level=3),
    out("import numpy as np\n"
        "v = {'he': np.array([1.0, 0.1]), 'she': np.array([0.1, 1.0]),\n"
        "     'engineer': np.array([0.9, 0.3]), 'nurse': np.array([0.2, 0.9])}\n"
        "cos = lambda a, b: float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))\n"
        "for w in ('engineer', 'nurse'):\n"
        "    print(w, round(cos(v[w], v['he']) - cos(v[w], v['she']), 2))",
        ["engineer 0.57\nnurse -0.68", "engineer -0.57\nnurse 0.68", "engineer 0.95\nnurse 0.98", "engineer 0.0\nnurse 0.0"], 0,
        "Association = cos(word, he) - cos(word, she).",
        "This is the WEAT-style association score: positive means closer to 'he', negative closer to 'she'. Embeddings trained on real text show exactly this pattern for occupations (Caliskan et al. 2017; Bolukbasi et al. 2016), and every downstream model built on them inherits it.",
        topic="model-bias", level=3),
    out("train = {'woman': 66, 'man': 34}    # 'cooking' examples by agent gender\n"
        "pred  = {'woman': 84, 'man': 16}    # model's predictions on test set\n"
        "tr = train['woman'] / sum(train.values())\n"
        "pr = pred['woman'] / sum(pred.values())\n"
        "print(round(tr, 2), round(pr, 2), round(pr - tr, 2))",
        ["0.66 0.84 0.18", "0.66 0.84 0.0", "0.34 0.16 -0.18", "66 84 18"], 0,
        "Compare the share in the data with the share in the predictions.",
        "The data is skewed 66/34; the model's outputs are skewed 84/16. The +0.18 gap is bias amplification: the model has turned a tendency into a near-rule. Rebalancing the data to 50/50 is not guaranteed to remove it; you have to measure the output rates too.",
        topic="model-bias", level=3),
    mcq("A Hindi sentence uses a gender-neutral construction: 'woh doctor hai, woh nurse hai'. The MT system outputs 'He is a doctor, she is a nurse'. Following the course's Google Translate deep dive, how should you describe this?",
        ["The source is ambiguous, but resolving it by occupation stereotype is social bias learned from the corpus",
         "It is pure linguistic ambiguity, so there is no bias",
         "It is a hallucination, unrelated to the training data",
         "It is a tokenisation error"], 0,
        "The course separates linguistic ambiguity from social bias.",
        "The ambiguity forces a choice; the bias is in how the choice is made. The course's mitigations: balanced examples, constrained decoding or post-processing policies (e.g. offering both gendered translations), and bias tests covering occupations, pronouns and dialects.",
        diagram="""
 woh doctor hai  -> He is a doctor
 woh nurse hai   -> She is a nurse
 (same neutral pronoun, gender picked by job)
""", topic="model-bias", level=3),
    mcq("A team removes the 'gender' column from a resume-screening dataset and declares the model fair. A later audit still shows a large selection gap. What is the most likely reason?",
        ["Proxy features (first names, women's colleges, hobbies, career gaps) still carry the gender signal",
         "Removing a column has no effect on any model",
         "The audit must be wrong, because the model cannot see gender",
         "The gap is caused by the GPU"], 0,
        "What in a resume still reveals gender?",
        "'Fairness through unawareness' fails when other features correlate with the protected attribute. The Amazon tool reportedly penalised the word 'women's' (as in 'women's chess club'). You must measure group outcomes, then mask or debias the proxies.",
        analogy="Like removing the user_id column but keeping email: the identity is still in the row.", topic="data-bias", level=3),
    mcq("A customer-support intent classifier hits 96% accuracy, but 'report fraud on my account' (0.3% of tickets) is usually mislabelled 'general query'. How does the course frame this?",
        ["Data imbalance suppressing a rare but critical intent; fix with targeted data, per-intent recall checks and human escalation",
         "Not a problem, since 96% accuracy is excellent",
         "A demographic parity violation",
         "A consent problem"], 0,
        "The course: imbalance can suppress minority dialects, languages, 'or rare but critical intents'.",
        "Aggregate accuracy hides the one class that matters most. Oversample or collect fraud examples, track recall for that intent, and route low-confidence or fraud-like tickets to a human, as the course recommends for high-stakes workflows.",
        diagram="""
 general query  |########################## 99.7%
 report fraud   |  0.3%   <- mostly mislabelled
 accuracy 96% overall, fraud recall near 0
""", topic="data-bias", level=3),
    mcq("A user invokes the GDPR right to erasure. Their chats were used to fine-tune last month's model. What does a responsible team need, per the course's governance checklist?",
        ["Provenance to find the records, a deletion pipeline for data stores, and a plan for the model (retrain or unlearn on the next cycle, or DP so one user's influence is bounded)",
         "Nothing: once data is in the weights, erasure does not apply",
         "Just delete the user's account login",
         "Publish a model card"], 0,
        "Data stores are easy to clean; weights are not.",
        "The checklist includes 'GDPR right-to-erasure pipeline implemented' and 'provenance and lineage tracked'. Deleting from the database is necessary but the model may have memorised the data; training with DP or scheduled retraining without the record is how teams honour this in practice.",
        diagram="""
erasure request
   |-> lineage: which stores / models saw it?
   |-> delete: DB, logs, vector store, backups
   `-> model: retrain without it next cycle
              (or DP bounded its influence)
""", topic="data-consent", level=3),
    mcq("For a hospital's discharge-summary assistant, which model choice does the course's 'smaller vs large models' discussion support?",
        ["A smaller, auditable model (or strong explanation and human review), because healthcare is high-stakes and decisions must be explainable",
         "The largest black-box LLM, because accuracy is all that matters",
         "Any model, since explainability matters only for chatbots",
         "No model at all: NLP cannot be used in healthcare"], 0,
        "The trade-off depends on risk level.",
        "The course: prefer explainable models in healthcare, finance and legal decisions; large models are fine for low-risk uses such as support chatbots and recommendations. In the activity, high-stakes -> explainability preferred; low-stakes -> accuracy acceptable.",
        diagram="""
 risk:  low ------------------------------> high
        support chat, recos    finance, legal, health
        large model OK         auditable model + review
""", topic="model-risks", level=3),
    mcq("A bank must show a rejected applicant which words in their application text drove the decision. Which course tools fit, and what is the difference between them?",
        ["SHAP (Shapley-value feature attribution) and LIME (a local surrogate model fitted around one prediction); both are model-agnostic per-prediction explanations",
         "Presidio and Google DLP; both detect PII",
         "Garak and Rebuff; both detect prompt injection",
         "AIF360 and Fairlearn; both explain single predictions"], 0,
        "The explainability row of the tools table.",
        "SHAP attributes the prediction to features using Shapley values from game theory; LIME perturbs the input and fits a simple model locally. The course puts 'SHAP/LIME reports' in its evaluation stage. AIF360 and Fairlearn measure group fairness, not one decision.",
        topic="model-risks", level=3),
    out("scores = [0.95, 0.90, 0.80, 0.70, 0.60, 0.40, 0.30, 0.20]\n"
        "toxic  = [1,    1,    0,    1,    1,    0,    1,    0]\n"
        "for t in (0.85, 0.5):\n"
        "    pred = [s >= t for s in scores]\n"
        "    tp = sum(p and y for p, y in zip(pred, toxic))\n"
        "    fp = sum(p and not y for p, y in zip(pred, toxic))\n"
        "    fn = sum((not p) and y for p, y in zip(pred, toxic))\n"
        "    print(t, round(tp / (tp + fp), 2), round(tp / (tp + fn), 2))",
        ["0.85 1.0 0.4\n0.5 0.8 0.8", "0.85 0.4 1.0\n0.5 0.8 0.8", "0.85 1.0 0.4\n0.5 0.8 1.0", "0.85 1.0 1.0\n0.5 0.8 0.8"], 0,
        "Per threshold: precision = TP/(TP+FP), recall = TP/(TP+FN).",
        "At 0.85 the output filter blocks 2 replies, both toxic (precision 1.0), but misses 3 of 5 toxic ones (recall 0.4). At 0.5 it blocks 5 with 4 toxic (P 0.8) and catches 4 of 5 (R 0.8). A user-facing filter usually prefers recall; check also whether the false positives fall on one dialect.",
        analogy="Like a spam filter: a strict threshold rarely flags good mail but lets spam through; a loose one catches more spam and annoys more users.", topic="deployment", level=3),
    mcq("A mental-health support chatbot detects that a user may be at risk of self-harm. Which design does the course's deployment guidance call for?",
        ["Fallback and human escalation: hand off to trained staff or crisis resources, and log the event without storing the raw conversation",
         "Keep chatting as usual, the model is accurate enough",
         "End the session silently",
         "Store the full conversation for future fine-tuning"], 0,
        "'Fallback design and human escalation are necessary in high-stakes workflows.'",
        "High-stakes moments need a human in the loop and a safe fallback. Logging the event (time, model version, escalation reason) gives an audit trail without retaining sensitive text, matching the course's 'what to log' answer.",
        topic="deployment", level=3),
    mcq("An internal HR assistant's API is reachable by any employee with the URL and returns salary predictions for named colleagues. Which deployment issue is this, and what fixes it?",
        ["Access-control failure; add authentication, role-based authorisation and rate limiting",
         "Hallucination; add RAG",
         "Bias amplification; add counterfactual augmentation",
         "Model drift; retrain monthly"], 0,
        "Who is allowed to ask?",
        "The course lists 'broad API access without authentication; sensitive inference exposed to unauthorised users'. Its deployment stage includes 'rate limiting and auth' and 'audit logging (SIEM)'. No model change fixes a missing authorisation check.",
        analogy="Like an admin endpoint shipped without the auth middleware: the bug is in the gateway, not the business logic.", topic="deployment", level=3),
    out("eps_per_query = [0.3, 0.3, 0.3, 0.3]\n"
        "budget, spent = 1.0, 0.0\n"
        "for i, e in enumerate(eps_per_query):\n"
        "    if spent + e > budget:\n"
        "        print('refuse query', i)\n"
        "        break\n"
        "    spent += e\n"
        "print(round(spent, 2))",
        ["refuse query 3\n0.9", "1.2", "refuse query 4\n1.2", "refuse query 3\n1.2"], 0,
        "Epsilons add up across queries on the same data.",
        "Sequential composition: answering k queries with epsilon each costs k x epsilon in total. After three queries 0.9 is spent; the fourth would reach 1.2 > 1.0, so it is refused. Without a budget, an analyst can average many noisy answers and recover the true value.",
        analogy="Like an API rate-limit quota: every call spends from the same budget, and when it is gone the gateway refuses.", topic="privacy-tech", level=3),
    mcq("A DP query reports the SUM of patient ages (each age clipped to 0-100) instead of a COUNT. With epsilon = 0.5, what Laplace noise scale is needed?",
        ["200, because one person can change the sum by up to 100 (sensitivity 100)",
         "2, the same as for a count",
         "0.5, equal to epsilon",
         "50, half the clip value"], 0,
        "Sensitivity = the most one person can change the answer.",
        "Scale = sensitivity / epsilon = 100 / 0.5 = 200, versus 1 / 0.5 = 2 for a count. Clipping is what makes the sensitivity finite; without it one extreme value could change the sum arbitrarily. The same clipping idea appears in DP-SGD for gradients.",
        topic="privacy-tech", level=3),
    out("W = {'python': 0.4, 'spark': 0.3, 'mark': 0.2, 'priya': -0.2}\n"
        "def score(text, mask=False):\n"
        "    toks = text.lower().split()\n"
        "    if mask:\n"
        "        toks = ['[NAME]' if t in ('mark', 'priya') else t for t in toks]\n"
        "    return round(sum(W.get(t, 0) for t in toks), 2)\n"
        "print(score('Mark python spark'), score('Priya python spark'))\n"
        "print(score('Mark python spark', True), score('Priya python spark', True))",
        ["0.9 0.5\n0.7 0.7", "0.7 0.7\n0.7 0.7", "0.9 0.5\n0.9 0.5", "0.9 0.5\n0.5 0.9"], 0,
        "Masked tokens get weight 0.",
        "Unmasked, the name weights (+0.2 / -0.2) create a 0.4 gap on identical skills. Masking maps both names to [NAME], which has no weight, so the counterfactual difference becomes 0. That is the course lab's 'why masking closes the gap' answer. It does not fix proxies elsewhere in the text.",
        topic="mitigations", level=3),
    mcq("Match each job to the course's tool: (1) find and anonymise PII in chat transcripts, (2) audit a classifier's group fairness and apply a mitigation, (3) scan a deployed LLM for vulnerabilities.",
        ["(1) Presidio, (2) IBM AI Fairness 360, (3) Garak",
         "(1) SHAP, (2) Presidio, (3) Fairlearn",
         "(1) Garak, (2) BertViz, (3) Presidio",
         "(1) Captum, (2) Rebuff, (3) LIME"], 0,
        "Privacy, fairness, red-teaming rows of the tools table.",
        "Presidio (and spaCy NER, Google DLP) for PII; AIF360, Fairlearn, What-If Tool and Aequitas for fairness; Garak for LLM vulnerability scanning, with Guardrails AI, NeMo Guardrails / LangKit and Rebuff on the safety side. SHAP, LIME, Captum and BertViz explain predictions.",
        topic="mitigations", level=3),
    mcq("Which list is in the right order for the course's five-stage production-ready privacy and ethics setup?",
        ["Data pipeline (PII scrubbing, consent) -> Training (fairness constraints, DP-SGD, model cards) -> Evaluation (demographic parity, SHAP/LIME, red-team) -> Deployment (guardrails, auth, audit logs, rollback) -> Monitoring (drift, fairness dashboards, deletion pipeline)",
         "Deployment -> Monitoring -> Data pipeline -> Training -> Evaluation",
         "Training -> Data pipeline -> Deployment -> Evaluation -> Monitoring",
         "Evaluation -> Training -> Data pipeline -> Monitoring -> Deployment"], 0,
        "Follow the data from intake to production.",
        "Each stage owns its controls, which is why the course says privacy and ethics must be integrated across the entire lifecycle. In an exam, placing a control in the right stage (e.g. DP-SGD at training, drift detection at monitoring) is half the marks.",
        topic="mitigations", level=3,
        diagram="""
1 Data      2 Training    3 Eval       4 Deploy     5 Monitor
PII scrub   fair constr.  dem. parity  guardrails   drift
consent     bias audit    SHAP/LIME    auth, rate   fairness dash
lineage     DP-SGD        red-team     audit logs   incident SOP
            model cards   robustness   rollback     GDPR deletion
"""),
    mcq("The course's case study: 'A chatbot trained on customer data leaks sensitive user information.' Which answer matches the model solution?",
        ["Stage: data collection + training; risk: PII leakage / memorisation; fix: PII scrubbing (Presidio) + differential privacy; monitoring: output filters + red-teaming",
         "Stage: deployment only; risk: latency; fix: more GPUs",
         "Stage: evaluation; risk: low BLEU; fix: more test data",
         "Stage: annotation; risk: label bias; fix: more annotators"], 0,
        "Where did the PII enter the model?",
        "The leak shows up at deployment, but the cause is upstream: raw PII went into training and was memorised. Scrub before training, train with DP, then guard the output and red-team for extraction. Blaming only the deployment stage is the common wrong answer.",
        diagram="""
 customer data --(no scrubbing)--> training --> memorised
        |                                          |
   fix: Presidio + DP                     user prompt -> leak
                                    fix: output filter, red-team
""", topic="case-studies", level=3),
    mcq("Map the course's risk-stack examples to layers: (a) service slow and rate-limited under demand, (b) a launch demo stating a wrong astronomy fact, (c) malicious inputs extracting hidden instructions.",
        ["(a) Infrastructure, (b) Model, (c) Application",
         "(a) Data, (b) Application, (c) Model",
         "(a) Model, (b) Infrastructure, (c) Data",
         "(a) Application, (b) Data, (c) Infrastructure"], 0,
        "Infra = scaling; model = what it says; app = how users attack it.",
        "Infrastructure: latency, scaling, logging, security. Model: hallucination, drift, explainability (the demo's factual error cost credibility). Application: UX, misuse, prompt injection. Data (the code-paste leak) is the fourth layer.",
        topic="case-studies", level=3, diagram=RISK_STACK),
    tf("The course's takeaway from Twitter's image-cropping case is that a one-time pre-launch test is enough; once shipped, fairness does not need re-checking.", False,
       "What did the slide say is required post-deployment?",
       "The takeaway is 'continuous fairness audits across demographic groups are required post-deployment'. Inputs and users change after launch. (The slide files this under 'Twitter Sentiment API ... CLIP'; the cropping system was actually an image-saliency model, not a sentiment API.)",
       topic="case-studies", level=3),

    # ------------------------------------------------------------------ L4
    mcq("Audit of an interview-shortlisting model, 100 candidates per group. A: TP 48, FN 12, FP 16, TN 24. B: TP 18, FN 12, FP 6, TN 64. Which statement is fully correct?",
        ["SR 0.64 vs 0.24, DI = 0.375 (fails four-fifths); TPR 0.80 vs 0.60, EOD = 0.20; B's higher accuracy (0.82 vs 0.72) does not clear the model",
         "B's accuracy is higher (0.82), so B is favoured and the model passes",
         "DI = 0.64 / 0.24 = 2.67 > 0.80, so the model passes; EOD = 0",
         "SR 0.48 vs 0.18, DI = 0.375; equalized odds holds because FPRs are both low"], 0,
        "SR = (TP+FP)/N; TPR = TP/(TP+FN); then DI and EOD.",
        "SR(A) = 64/100, SR(B) = 24/100, DI = 0.375. TPR(A) = 48/60 = 0.80, TPR(B) = 18/30 = 0.60. FPR 0.40 vs 0.086 also differ. Part of the SR gap reflects different base rates (60 vs 30 qualified), which is why the EOD matters: qualified B candidates are still selected less. B's higher accuracy comes from its many easy true negatives.",
        topic="fairness-metrics", level=4),
    mcq("Two groups have different base rates of the true label (40% vs 20% qualified). A team wants a non-trivial classifier that satisfies demographic parity AND equalized odds at once. What should you tell them?",
        ["In general it is impossible: equal TPR and FPR with different base rates force different selection rates, so you must choose which criterion fits the harm",
         "Easy: tune one global threshold",
         "Both hold automatically when accuracy is equal",
         "Both hold if the protected attribute is removed"], 0,
        "SR = TPR x base rate + FPR x (1 - base rate).",
        "If TPR and FPR are equal across groups, SR still differs whenever base rates differ, unless TPR = FPR (a classifier no better than chance). Fairness criteria conflict (Kleinberg et al.; Chouldechova). Pick the one that matches the decision: equal opportunity when missing qualified people is the harm, demographic parity when the labels themselves reflect historical bias.",
        topic="fairness-metrics", level=4),
    tf("A model can satisfy demographic parity and still be unfair to qualified individuals, for example by selecting the right number of Group B applicants but picking them at random.", True,
       "Parity checks rates, not who is selected.",
       "Demographic parity ignores the labels, so random selection in one group meets it while qualified people are rejected. That is why the course lists several metrics, including equal opportunity and individual fairness ('similar people treated similarly').",
       topic="fairness-metrics", level=4),
    out("import re\n"
        "P = [('[CARD_LAST4]', r'\\b\\d{4}\\b'),\n"
        "     ('[PHONE]', r'\\b\\d{3}[-.]?\\d{3}[-.]?\\d{4}\\b')]\n"
        "t = 'Call 804-555-1122 or 8045551122'\n"
        "for tag, rx in P:\n"
        "    t = re.sub(rx, tag, t)\n"
        "print(t)",
        ["Call 804-555-[CARD_LAST4] or [PHONE]", "Call [PHONE] or [PHONE]",
         "Call [CARD_LAST4] or [CARD_LAST4]", "Call 804-555-[CARD_LAST4] or 8045551122"], 0,
        "The broad pattern runs first; where are the stand-alone 4-digit runs?",
        "With CARD_LAST4 first, '1122' in the hyphenated phone is a stand-alone 4-digit word and gets tagged, so PHONE no longer matches and '804-555-' stays in the text. The 10-digit run has no inner word boundary, so PHONE still catches it. Order patterns from specific to broad, which is why the exam table lists CARD_LAST4 last.",
        topic="pii", level=4),
    out("import re\n"
        "PERSON = r'\\b[A-Z][a-z]+ [A-Z][a-z]+\\b'\n"
        "print(re.sub(PERSON, '[PERSON]', 'Applicant Neha Rao met Dr. Sen today.'))",
        ["[PERSON] Rao met Dr. Sen today.", "Applicant [PERSON] met [PERSON] today.",
         "Applicant [PERSON] met Dr. Sen today.", "[PERSON] [PERSON] met Dr. Sen today."], 0,
        "Matches go left to right and never overlap; what does the '.' do?",
        "'Applicant Neha' is the first pair of capitalised words, so it is replaced and 'Rao' leaks. 'Dr. Sen' fails because the period breaks the 'Word Word' shape. Two leaks in one line: this is why the course pairs regex with NER (Presidio, spaCy) for names and tests maskers on real sentences.",
        topic="pii", level=4),
    out("from collections import Counter\n"
        "rows = [('560001', 34, 'flu'), ('560001', 37, 'asthma'),\n"
        "        ('560002', 31, 'flu'), ('560002', 39, 'diabetes'),\n"
        "        ('560034', 24, 'flu'), ('560034', 27, 'flu')]\n"
        "key = lambda r: (r[0], r[1] // 10)          # pincode, age decade\n"
        "groups = {key(r) for r in rows}\n"
        "k = min(Counter(key(r) for r in rows).values())\n"
        "l = min(len({r[2] for r in rows if key(r) == g}) for g in groups)\n"
        "print(k, l)",
        ["2 1", "2 2", "1 1", "3 2"], 0,
        "k = smallest group size; l = fewest distinct diagnoses in any group.",
        "Generalising age to decades makes every group size 2 (2-anonymous), but both people in (560034, 20s) have flu. Anyone who knows a neighbour aged 24 is in the table learns the diagnosis: a homogeneity attack. k-anonymity hides who a row is, not what the group shares; l-diversity adds that requirement.",
        analogy="Like a 'k users per bucket' rule in analytics dashboards: big enough buckets, but if every user in a bucket clicked the same thing, the bucket still tells you what each did.", topic="pii", level=4),
    fill("Requiring every k-anonymous group to contain at least l different values of the sensitive attribute (such as diagnosis) is called l-____.", "diversity",
         "It fixes the homogeneity attack on k-anonymity.",
         "l-diversity (Machanavajjhala et al. 2007) stops 'everyone in this group has flu' leaks. Neither it nor k-anonymity protects free text well, which is why NLP pipelines combine masking, minimisation and DP.",
         topic="pii", level=4),
    mcq("A team stores sentence embeddings of support chats instead of the raw text and calls the store 'anonymised'. Why does the course's data-issues slide disagree?",
        ["'Inference attacks on embeddings': embeddings can be inverted to recover much of the text and can reveal attributes such as names or health conditions",
         "Embeddings are always stored unencrypted",
         "Embeddings are larger than raw text",
         "Embeddings cannot be searched"], 0,
        "Is a dense vector a one-way hash?",
        "Embedding inversion and attribute-inference attacks recover content and private attributes from vectors. Treat an embedding store of personal text as personal data: scrub PII before embedding, control access and apply retention rules, the same as the raw logs.",
        topic="pii", level=4,
        analogy="An unsalted hash of a phone number is not anonymous either: the input space is small enough to reverse."),
    out("import numpy as np\n"
        "grads = np.array([[0.3, 0.4], [3.0, 4.0], [0.0, 2.0]])   # per-example\n"
        "C = 1.0                                                    # clip norm\n"
        "norms = np.linalg.norm(grads, axis=1)\n"
        "clipped = grads / np.maximum(1, norms / C)[:, None]\n"
        "print(norms.tolist(), clipped.mean(axis=0).round(2).tolist())",
        ["[0.5, 5.0, 2.0] [0.3, 0.73]", "[0.5, 5.0, 2.0] [1.1, 2.13]", "[0.7, 7.0, 2.0] [0.3, 0.73]", "[0.5, 5.0, 2.0] [0.1, 0.13]"], 0,
        "Only gradients with norm above C are scaled down to norm C.",
        "DP-SGD clips each example's gradient to norm <= C (0.5 stays; 5.0 -> [0.6, 0.8]; 2.0 -> [0, 1]), averages, then adds Gaussian noise scaled to C. Clipping bounds any single example's influence (its sensitivity); the noise hides it. Without clipping, one rare example with a huge gradient, such as a unique phone number, could be memorised.",
        topic="privacy-tech", level=4),
    tf("Training with DP-SGD tends to cost more accuracy on underrepresented groups than on the majority group.", True,
       "Rare examples have the gradients that clipping and noise suppress most.",
       "Bagdasaryan et al. (2019) showed DP-SGD's accuracy drop is larger for minority classes and groups: their distinctive gradients get clipped and drowned in noise. Privacy and fairness can pull against each other, so audit per-group metrics after enabling DP.",
       topic="privacy-tech", level=4),
    mcq("In the course's accountability activity, a healthcare chatbot gives incorrect medical advice that harms a user. Which allocation matches the course's answer?",
        ["Primary accountability lies with the deploying organisation; developers share it for design and safeguards, the company for deployment and monitoring, regulators for enforcement",
         "The user alone, because they chose to follow the advice",
         "The developer alone, because they wrote the code",
         "Nobody, because the model made the decision"], 0,
        "'Accountability is distributed but led by the ___ entity.'",
        "The course's key idea: accountability is distributed but led by the deploying entity. In practice that means audit logs with model version and timestamp, human escalation for high-stakes answers, and an incident-response playbook, so a harmful output can be traced and fixed.",
        diagram="""
            deploying organisation (leads)
           /          |            \\
   developers     company ops      regulators
   design,        deployment,      compliance
   safeguards     monitoring       enforcement
""", topic="deployment", level=4,
        analogy="Like a production outage caused by a library bug: the company running the service answers to customers, even if the library author shares the blame."),
    mcq("A bank's chatbot misroutes some loan queries. Engineers ask to log full conversations for 90 days to debug. Which design best meets the course's 'what to log' guidance?",
        ["Log intent, confidence, model version, timestamp, error type and the reply; store user text only after PII masking, with short retention and restricted access",
         "Log full raw conversations for 90 days, it is internal",
         "Log nothing, to be safe",
         "Log raw text but encrypt the disk"], 0,
        "Log for debugging, minimise personal data exposure.",
        "The course: safe to log outputs, timestamp, model version and error types; avoid raw inputs with PII and full conversations unless anonymised. 'Log nothing' blocks debugging and audits; disk encryption does not stop insiders or the next fine-tune from reading the PII.",
        topic="deployment", level=4),
    mcq("Microsoft's Tay chatbot (2016) was taken offline after 16 hours. What made it fail so fast, and which control would have prevented it?",
        ["It learned from live user interactions, so coordinated users taught it slurs; never train online on unfiltered user input, filter outputs and moderate before learning",
         "Its servers ran out of memory; scale the infrastructure",
         "It was trained on biased resumes; rebalance the data",
         "It used too small a context window; increase it"], 0,
        "Where did its new behaviour come from?",
        "The course's dialog-ethics slides: Tay 'learned from user interactions' and was posting racial slurs and conspiracy theories within hours. Feeding unvetted live data back into a model turns every user into an annotator, including attackers. Henderson et al. (2017) found similar hate speech in Reddit/Twitter dialog datasets themselves.",
        diagram="""
 users --tweets--> Tay --learns online--> Tay v+1
   ^                                       |
   +-------------- toxic replies <---------+
  no filter between user input and learning
""", topic="data-bias", level=4),
    mcq("Five annotators label posts for 'offensive'. Majority vote is used. For posts about a minority community, the two annotators from that community often vote 'offensive' and are outvoted. What is the best practice?",
        ["Treat disagreement as signal: keep per-annotator labels, check disagreement by group, diversify the pool and revisit guidelines rather than silently majority-voting",
         "Majority vote is always correct, nothing to change",
         "Drop all posts with disagreement from the dataset",
         "Replace annotators with the model's own predictions"], 0,
        "Whose view does majority vote erase?",
        "The course: annotation guidelines and annotators encode subjectivity. Majority voting systematically erases the minority view on exactly the content that targets that minority. Keeping disagreement data lets you measure it and train models that reflect it.",
        topic="data-bias", level=4),
    mcq("Your team releases a Hindi-English intent model. Evaluation: 91% F1 on English, 78% on Hinglish code-mixed text, 64% on Bhojpuri-influenced Hindi. What belongs in the model card?",
        ["Intended use, training data summary, per-language/dialect results including the 64% gap, known limitations and out-of-scope uses (e.g. not for automated decisions on Bhojpuri speakers without review)",
         "Only the best number (91%), since cards are for customers",
         "Only the architecture and parameter count",
         "Nothing about dialects, since that could cause concern"], 0,
        "The checklist: 'model card published with limitations and risks'.",
        "A model card exists precisely to surface disaggregated results and limits. Hiding the 64% figure moves the harm to users who never learn the model is weak for them. Card + datasheet together answer 'who is it for, who was it tested on, where does it fail'.",
        topic="mitigations", level=4),

    # ------------------------------------------------------------------ fills
    fill("Microsoft's open-source toolkit that the course lists for PII detection and anonymisation in text is called ____.", "Presidio",
         "First row of the course's privacy tools table.",
         "Presidio combines regex recognisers, checksums and NER models (spaCy) to find PII, then masks, replaces, hashes or encrypts it. The course puts 'PII scrubbing (Presidio)' as step one of the data pipeline.",
         topic="mitigations", level=2),
    fill("Tracking where each record came from and every transformation applied to it is called data provenance or data ____.", "lineage",
         "The course's data pipeline stage logs it.",
         "Lineage lets you answer audits ('which models saw this user's data?') and erasure requests. The governance checklist: 'provenance and lineage tracked throughout pipeline'.",
         topic="data-consent", level=2),
    fill("The basic differential-privacy mechanism for a numeric query adds noise from the ____ distribution with scale sensitivity / epsilon.", "Laplace",
         "A double-sided exponential, named after a French mathematician.",
         "Laplace noise with scale b = sensitivity / epsilon gives epsilon-DP for a single numeric query. DP-SGD instead adds Gaussian noise to clipped gradients.",
         topic="privacy-tech", level=2),
    fill("Under the four-fifths rule, a disparate impact ratio below ____ (write it as a decimal, e.g. 0.5) signals adverse impact.", "0.8",
         "Four fifths as a decimal.",
         "DI = SR(lower) / SR(higher). The Sep 2026 paper's DI of 0.300 / 0.600 = 0.5 is below 0.8, so it fails. The rule comes from US employment guidelines and is a screening flag, not proof of discrimination.",
         topic="fairness-metrics", level=2),
    fill("GDPR Article ____ gives people the right not to be subject to decisions based solely on automated processing, which is why the course links it to explainability.", "22",
         "The course's model-issues slide cites it next to 'black-box transformers'.",
         "Article 22 gives people rights to human intervention, to express their view and to contest the decision. The Sep 2026 answer key cites it: identical accuracy does not justify deployment; provide human review and contest.",
         topic="model-risks", level=3),
    fill("An attack that tests whether one specific person's record was in a model's training set is called a membership ____ attack.", "inference",
         "The attacker infers membership.",
         "Membership inference exploits the model being more confident on data it trained on. Knowing someone was in a 'patients with condition X' fine-tuning set already leaks their diagnosis. DP training bounds exactly this risk.",
         topic="model-risks", level=3),
    fill("Dropping the protected attribute (gender, religion) from the features and assuming the model is then fair is called fairness through ____.", "unawareness",
         "The model is 'unaware' of the attribute.",
         "It fails because proxies (names, pincodes, colleges, word choices) carry the same signal. Measure group outcomes instead, and mask or debias proxies, as in the course's resume lab.",
         topic="mitigations", level=3),
]
