from helpers import mcq, tf, out, fill

SUBJECT = "nlpa-ie"

TOPICS = [
    ("ie-overview", "What IE is and the IE pipeline"),
    ("ner-basics", "Named entities: types, variation, ambiguity"),
    ("bio-tagging", "BIO / IOB and BIOES tagging"),
    ("ner-rules", "Rule-based and gazetteer NER"),
    ("sequence-models", "HMM, MEMM and CRF sequence labelling"),
    ("neural-ner", "BiLSTM-CRF, transformers and LLM-based NER"),
    ("ner-eval", "Span-level NER evaluation"),
    ("re-patterns", "Relations and pattern-based extraction"),
    ("re-supervised", "Supervised relation extraction and RE evaluation"),
    ("re-semi", "Bootstrapping, distant supervision, Open IE and LLM RE"),
    ("events", "Event extraction"),
    ("temporal", "Temporal expressions, TIMEX3 normalisation and temporal relations"),
]

QUESTIONS = [
    # ------------------------------------------------------------------ L1
    mcq("What does information extraction (IE) do, in the course's definition?",
        ["Turns unstructured or semi-structured text into structured data, such as database rows or filled templates",
         "Translates text from one language into another",
         "Generates a fluent summary of a document",
         "Compresses documents so they take less disk space"], 0,
        "Think 'text in, table out'.",
        "IE identifies specific pieces of information (names, titles, organisations, dates) in text and fills slots in a database. The course's example turns a news story about Bill Gates, Bill Veghte and Richard Stallman into a NAME / TITLE / ORGANIZATION table. Summarisation produces more text, not structured rows.",
        topic="ie-overview", level=1,
        diagram="""
"...said Bill Veghte, a Microsoft VP..."
                 |  IE
                 v
NAME          | TITLE   | ORGANIZATION
Bill Gates    | CEO     | Microsoft
Bill Veghte   | VP      | Microsoft
R. Stallman   | founder | Free Software Fdn.
""",
        analogy="Like a scraper that reads an HTML page and writes rows into a SQL table, except the 'page' is free English text with no tags."),
    fill("The course sums up IE as a family of techniques: segmentation + classification + ____.", "association",
         "After finding and labelling the pieces, you link them.",
         "Segmentation finds the spans (Bill Gates, CEO, Microsoft), classification gives each a type (PERSON, TITLE, ORG), and association links them into one record (Bill Gates is CEO of Microsoft).",
         topic="ie-overview", level=1),
    fill("A standard NER system tags '20 March 2026' with the entity type ____ (capitals).", "DATE",
        "It names a day on the calendar.",
        "Common NER types are PERSON, ORGANIZATION, LOCATION (or GPE), DATE, TIME, MONEY and PERCENT. Dates and money amounts are 'numeric' entities that the course's exam excerpts always include.",
        topic="ner-basics", level=1),
    tf("In the sentence 'Tata announced record profits', the word 'Tata' could be a person or an organisation, which is why NER must look at context.", True,
       "The course lists Tata among its ambiguity examples.",
       "The course's ambiguity list: 1945 (date vs time), Washington (location vs person), May (person vs month), Tata (person vs organisation). Here 'announced record profits' points to the company. A plain dictionary lookup cannot decide.",
       analogy="Like an overloaded function name in code: you only know which one is meant from the arguments around it.",
       topic="ner-basics", level=1),
    mcq("In BIO (IOB) tagging, what does the tag B-ORG on a token mean?",
        ["The token is the first token of an organisation name",
         "The token is inside an organisation name but not first",
         "The token is outside any entity",
         "The token is a word that is both an organisation and a person"], 0,
        "B is for 'begin'.",
        "B-X marks the first token of an entity of type X, I-X marks the following tokens of the same entity, and O marks tokens that belong to no entity. So 'Reserve Bank of India' is B-ORG I-ORG I-ORG I-ORG.",
        topic="bio-tagging", level=1,
        diagram="""
Rohan   Mehta   joined  FinEdge  Capital
B-PER   I-PER   O       B-ORG    I-ORG
"""),
    fill("In BIO tagging, a token that is not part of any entity gets the tag ____.", "O",
         "Outside.",
         "O means outside. Most tokens in a sentence are O; only entity tokens get B- or I- tags.",
         topic="bio-tagging", level=1),
    mcq("Which rule is an example of the course's rule-based NER?",
        ["'Dr.' followed by a capitalised word -> PERSON",
         "Train a BiLSTM on CoNLL-2003",
         "Ask a large language model to list the entities",
         "Cluster all words by their embeddings"], 0,
        "Hand-written, no training data.",
        "Rule-based NER uses hand-written linguistic rules and regular expressions: titles such as Mr. / Dr. / Prof. before a capitalised word give PERSON, DD/MM/YYYY gives DATE, a currency sign followed by numbers gives MONEY. 'Dr. Abdul Kalam' -> PERSON.",
        topic="ner-rules", level=1),
    tf("One advantage the course gives for rule-based NER is that it needs no training data.", True,
       "What do you need before you can write a regex?",
       "The course lists: no training data required, easy for small domains, highly interpretable. The cost comes later: rules miss unseen patterns (low recall) and must be maintained by hand.",
       topic="ner-rules", level=1,
       analogy="Like hard-coding validation rules in a form: quick to ship and easy to read, but every new edge case is another if-statement."),
    mcq("Why is NER called a 'sequence labelling' task?",
        ["It gives every token in the sentence a label, and each label depends on the neighbouring words and labels",
         "It labels the whole document with one category",
         "It sorts the words of a sentence into alphabetical order",
         "It predicts the next word in the sequence"], 0,
        "One label per token, in order.",
        "Text classification gives one label per document. Sequence labelling (POS tagging, NER with BIO tags) gives one label per token, and the labels are not independent: I-PER can only follow B-PER or I-PER. That dependency is what HMMs, CRFs and BiLSTM-CRFs model.",
        topic="sequence-models", level=1),
    mcq("In a Hidden Markov Model (HMM) tagger, what is 'hidden'?",
        ["The tags (states); only the words are observed",
         "The words; only the tags are observed",
         "The training data",
         "The probabilities, which are never estimated"], 0,
        "What do you see in raw text, and what must you infer?",
        "You observe the words. The tag sequence that produced them (B-PER, O, B-LOC...) is hidden and must be inferred. The HMM uses transition probabilities P(tag | previous tag) and emission probabilities P(word | tag).",
        topic="sequence-models", level=1),
    mcq("When a BERT model is fine-tuned for NER, what does it predict?",
        ["A tag (such as B-PER, I-PER or O) for every token, from that token's contextual vector",
         "One label for the whole sentence from the [CLS] vector",
         "The next word after the sentence",
         "A translation of every entity"], 0,
        "This setup is called token classification.",
        "BERT gives a contextual vector per (sub)word token; a small linear layer on top maps each vector to a tag. That is 'token classification' in Hugging Face terms. Sentence classification would use only [CLS].",
        topic="neural-ner", level=1),
    tf("The course lists hallucination and higher inference cost among the limitations of using a large language model for NER.", True,
       "Advantages: zero/few-shot, no retraining. Limitations?",
       "LLM NER needs no labelled data and no retraining, but it can invent entities, costs far more per document than a small tagger, and is less consistent than fine-tuned models on benchmark datasets.",
       topic="neural-ner", level=1),
    mcq("In NER evaluation, what is a false negative (FN)?",
        ["A gold (human-annotated) entity that the system did not output correctly",
         "An entity the system output that is not in the gold standard",
         "A token correctly tagged O",
         "An entity that is correct but appears twice"], 0,
        "'Negative' = the system said nothing (correct) about it.",
        "TP: predicted entity matches a gold entity in span and type. FP: predicted entity with no matching gold entity. FN: gold entity the system missed. Recall = TP / (TP + FN) measures how many gold entities you found.",
        topic="ner-eval", level=1,
        diagram="""
         gold entities      system entities
        +-----------+   +-------------+
        |    FN     | TP|     FP      |
        |  (missed) |   |  (spurious) |
        +-----------+   +-------------+
"""),
    fill("NER F1 is the ____ mean of precision and recall.", "harmonic",
         "Not arithmetic, not geometric.",
         "F1 = 2PR / (P + R). The harmonic mean is pulled towards the smaller value, so a system cannot hide poor recall behind high precision.",
         topic="ner-eval", level=1),
    mcq("Which is a relation triple, as the course writes them?",
        ["Founding-year(IBM, 1911)",
         "IBM (ORGANIZATION)",
         "B-ORG I-ORG O",
         "1911 (DATE)"], 0,
        "A relation links two arguments.",
        "A binary relation is Relation(Arg1, Arg2). The course's IBM example gives Founding-year(IBM, 1911) and Founding-location(IBM, New York). 'IBM (ORGANIZATION)' is an entity, not a relation.",
        topic="re-patterns", level=1),
    mcq("The Hearst pattern 'Y such as X' extracts which relation from 'red algae, such as Gelidium'?",
        ["IS-A (hyponym): Gelidium is a kind of red algae",
         "Part-of: Gelidium is part of red algae",
         "Located-in: Gelidium is in red algae",
         "Founded-by: red algae founded Gelidium"], 0,
        "Hearst (1992) was learning hyponyms.",
        "Hearst's patterns find IS-A (hypernym/hyponym) pairs: 'Y such as X', 'such Y as X', 'X or other Y', 'X and other Y', 'Y including X', 'Y, especially X'. Even without knowing the word Gelidium, the pattern tells you it is a kind of red algae.",
        analogy="Like spotting a type hierarchy from code comments: 'handlers such as LoginHandler' tells you LoginHandler is a handler even if you have never seen it.",
        topic="re-patterns", level=1),
    tf("Supervised relation extraction needs a corpus in which humans have labelled the entities and the relations between them.", True,
       "What does 'supervised' always need?",
       "The course's steps: choose relations and entity types, choose a representative corpus, label the named entities, hand-label the relations, split into train / dev / test, train a classifier. The labelling is the expensive part, which motivates bootstrapping and distant supervision.",
       topic="re-supervised", level=1),
    mcq("What do you start bootstrapping relation extraction with?",
        ["A few seed tuples, such as <Mark Twain, Elmira> for buried-in",
         "A fully labelled training corpus",
         "A trained BERT model",
         "A list of all verbs in English"], 0,
        "It pulls itself up from a tiny start.",
        "Bootstrapping: take seed tuples, find sentences that contain them ('Mark Twain is buried in Elmira, NY'), turn those contexts into patterns ('X is buried in Y'), use the patterns to find new tuples, and iterate.",
        diagram="""
seeds <Mark Twain, Elmira>
   -> find sentences  -> "X is buried in Y"
   -> apply patterns  -> new tuples
   -> repeat (seed set grows each round)
""",
        topic="re-semi", level=1),
    mcq("Event extraction answers which question about a sentence?",
        ["Who did what to whom, where and when",
         "Which words are nouns",
         "Whether the sentence is positive or negative",
         "Which language the sentence is in"], 0,
        "The course quotes this phrase directly.",
        "Event extraction finds an event (usually signalled by a trigger word such as 'acquired' or 'outbreak') and its participants, place and time. Relation extraction only links two entities; events carry richer role information.",
        topic="events", level=1),
    mcq("Which temporal expression is a DURATION?",
        ["six weeks", "5 January 2026", "next Monday", "yesterday"], 0,
        "A span of time, not a point.",
        "Durations denote spans of time (seconds, days, weeks, centuries). '5 January 2026' is absolute (maps straight to a calendar date); 'next Monday' and 'yesterday' are relative (need a reference point such as the article date).",
        diagram="""
ABSOLUTE : 5 January 2026     (calendar point)
RELATIVE : next Monday        (needs anchor date)
DURATION : six weeks          (length of time)
""",
        topic="temporal", level=1),
    tf("'5 January 2026' is an absolute temporal expression because it maps directly to a calendar date.", True,
       "Do you need to know when the article was written?",
       "Absolute expressions can be placed on the calendar without any reference point. Relative ones ('next Monday', 'last Tuesday', 'within six months') need an anchor such as the document date.",
       topic="temporal", level=1),
    fill("The event trigger word in 'Pharmaco Ltd. acquired BioNext for $12 million on 3 May 2026' is ____.", "acquired",
        "The word that names what happened.",
        "The trigger is the word (usually a verb or event noun) that most clearly expresses the event: 'acquired'. The other items are arguments: Acquirer = Pharmaco Ltd., Acquired = BioNext, Price = $12 million, Time = 3 May 2026.",
        topic="events", level=1),
    # ------------------------------------------------------------------ L2
    mcq("The course's typical IE pipeline runs these stages. Which order is right?",
        ["NER and shallow parsing -> reference resolution -> relation detection -> event detection -> template filling",
         "Template filling -> NER -> relation detection -> event detection -> reference resolution",
         "Relation detection -> NER -> template filling -> event detection -> reference resolution",
         "Event detection -> template filling -> NER -> reference resolution -> relation detection"], 0,
        "You can't relate entities you haven't found yet.",
        "Entities come first, then coreference links 'the company' and 'it' to the right entity, then relations between entities, then events with their arguments, and finally the template (database row) is filled. Each stage consumes the previous stage's output.",
        topic="ie-overview", level=2,
        diagram="""
text -> [NER + shallow parse] -> [reference resolution]
     -> [relation detection] -> [event detection]
     -> [template filling] -> DB rows
"""),
    mcq("'Manmohan Singh', 'Manmohan' and 'Dr. Manmohan Singh' in one article all refer to one person. What NER problem is this?",
        ["Variation: one entity appears in several surface forms",
         "Type ambiguity: one string could be several types",
         "Metonymy: a place name used for an organisation",
         "Boundary error: the span is cut short"], 0,
        "Same referent, different strings.",
        "The course separates variation (many names for one entity) from ambiguity (one name, several types, like 'May' the person vs the month). Variation is why IE needs reference resolution after NER, so all three mentions map to one database entity.",
        topic="ner-basics", level=2),
    fill("In 'Washington imposed new tariffs', annotators tag 'Washington' as an organisation (the US government), not a location. The course blames such grey areas on ____ (one word).", "metonymy",
        "A related thing names the thing.",
        "Metonymy uses one entity to refer to another closely related one ('Washington' for the US government, 'Wall Street' for the finance industry). The course lists Organisation vs Location and Company vs Artefact as typical metonymy grey areas, which is why guidelines must state a rule.",
        topic="ner-basics", level=2),
    mcq("Tag 'He joined the Reserve Bank of India' with BIO (types PER, ORG, LOC). Which sequence is right?",
        ["O O O B-ORG I-ORG I-ORG I-ORG",
         "O O B-ORG I-ORG I-ORG I-ORG I-ORG",
         "O O O I-ORG I-ORG I-ORG I-ORG",
         "B-PER O O B-ORG I-ORG I-ORG B-LOC"], 0,
        "Is 'the' part of the name? Does 'India' start a new entity here?",
        "'the' is a determiner outside the name, so it is O. The whole name 'Reserve Bank of India' is one ORG starting with B-ORG; 'India' is inside it, not a separate LOC. 'He' is a pronoun, not a named entity. Exam papers plant exactly these two traps.",
        topic="bio-tagging", level=2),
    out('tags = ["B-PER", "I-PER", "O", "B-ORG", "I-ORG", "I-ORG", "O", "B-LOC"]\n'
        'toks = ["Meera", "Nair", "joined", "Cloud", "Nova", "Labs", "in", "Pune"]\n'
        'spans, cur = [], None\n'
        'for w, t in zip(toks, tags):\n'
        '    if t.startswith("B-"):\n'
        '        if cur: spans.append(cur)\n'
        '        cur = [t[2:], w]\n'
        '    elif t.startswith("I-") and cur and cur[0] == t[2:]:\n'
        '        cur[1] += " " + w\n'
        '    else:\n'
        '        if cur: spans.append(cur)\n'
        '        cur = None\n'
        'if cur: spans.append(cur)\n'
        'print(len(spans), spans[1])',
        ["3 ['ORG', 'Cloud Nova Labs']",
         "3 ['ORG', 'Cloud']",
         "4 ['ORG', 'Cloud Nova Labs']",
         "2 ['LOC', 'Pune']"], 0,
        "Each B- opens a span, I- of the same type extends it, O closes it.",
        "Decoding BIO gives spans PER 'Meera Nair', ORG 'Cloud Nova Labs', LOC 'Pune': 3 spans, and index 1 is the ORG. Span-level evaluation works on exactly these decoded spans, not on the raw tags.",
        topic="bio-tagging", level=2),
    mcq("What is a gazetteer in NER?",
        ["A list of known names of one type (cities, companies, drugs) used to look up or feature-tag tokens",
         "A neural network layer that predicts tags",
         "A newspaper corpus used for pre-training",
         "A scoring script for CoNLL"], 0,
        "Originally, a geographical dictionary.",
        "Gazetteers are name lists: country lists, company registries, drug lexicons. A pure lookup tags exact matches; better, 'token is in the city list' becomes a feature for a CRF or a hint for a neural tagger. The course also uses gazetteers as features for relation extraction.",
        topic="ner-rules", level=2,
        analogy="Like an allow-list in a config file: a fast exact-match check, but useless for names that aren't on the list yet."),
    out('import re\n'
        'text = "Paid Rs. 4,500 on 12/03/2026 to Dr. Asha Rao; refund of Rs. 300 on 15/03/2026."\n'
        'dates = re.findall(r"\\b\\d{2}/\\d{2}/\\d{4}\\b", text)\n'
        'money = re.findall(r"Rs\\. ?[\\d,]+", text)\n'
        'person = re.findall(r"Dr\\. [A-Z][a-z]+(?: [A-Z][a-z]+)*", text)\n'
        'print(len(dates), money, person)',
        ["2 ['Rs. 4,500', 'Rs. 300'] ['Dr. Asha Rao']",
         "2 ['Rs. 4,500', 'Rs. 300'] ['Dr. Asha']",
         "1 ['Rs. 4,500'] ['Dr. Asha Rao']",
         "2 ['4,500', '300'] ['Asha Rao']"], 0,
        "findall returns the whole match when the pattern has no capturing groups.",
        "The DD/MM/YYYY rule finds both dates, the 'Rs.' + digits rule finds both amounts, and 'Dr.' + one or more capitalised words gives 'Dr. Asha Rao' (the (?: ...) group is non-capturing, so findall still returns full matches). This is the course's rule-based NER in three regexes.",
        topic="ner-rules", level=2),
    out('# HMM: P(tags, words) = product of transition * emission\n'
        'trans = {("<s>", "PER"): 0.3, ("PER", "O"): 0.6}\n'
        'emit = {("PER", "Ravi"): 0.01, ("O", "spoke"): 0.02}\n'
        'p = trans[("<s>", "PER")] * emit[("PER", "Ravi")]\n'
        'p *= trans[("PER", "O")] * emit[("O", "spoke")]\n'
        'print(f"{p:.1e}")',
        ["3.6e-05", "1.8e-03", "9.3e-01", "6.0e-03"], 0,
        "Multiply all four numbers.",
        "0.3 × 0.01 × 0.6 × 0.02 = 3.6 × 10^-5. An HMM scores a tag sequence as the product of P(tag | previous tag) and P(word | tag) at every position. Real taggers add log-probabilities instead to avoid underflow.",
        topic="sequence-models", level=2),
    mcq("How does a MEMM (maximum entropy Markov model) differ from an HMM tagger?",
        ["It is discriminative: it directly models P(tag | word features, previous tag) with a logistic-regression-style classifier",
         "It is generative and models P(word | tag) like an HMM, just with more states",
         "It ignores the previous tag entirely",
         "It needs no training data"], 0,
        "Generative vs discriminative.",
        "An HMM generates words from tags, so adding rich overlapping features (suffix, capitalisation, gazetteer hit) is awkward. A MEMM is a per-token classifier that can use any features of the input plus the previous tag. The course shows greedy MEMM inference: pick the best tag left to right.",
        topic="sequence-models", level=2),
    mcq("What does each layer of a BiLSTM-CRF NER model contribute?",
        ["Embeddings represent words, the BiLSTM adds left and right context to each word, the CRF picks the best whole tag sequence using tag-transition scores",
         "The BiLSTM picks the tag sequence and the CRF produces word embeddings",
         "The CRF reads the sentence in both directions and the BiLSTM normalises the tags",
         "The embeddings choose the tags directly; the other layers only speed up training"], 0,
        "Representation, context, structured output.",
        "The BiLSTM gives each token a context-aware score for every tag. The CRF layer adds learned transition scores (I-PER after B-PER is good, I-PER after O is bad) and Viterbi decoding finds the best valid sequence. Without the CRF, each token's tag would be chosen independently.",
        topic="neural-ner", level=2,
        diagram="""
words:   Dr.    Asha   Rao    spoke
          |      |      |      |
        [embedding per word]
        [BiLSTM: -> and <- context]
        [CRF: transition scores + Viterbi]
tags:   B-PER  I-PER  I-PER   O
"""),
    mcq("A WordPiece tokenizer splits 'Bengaluru' into 'Ben', '##gal', '##uru'. The word's gold tag is B-LOC. What is the usual way to train a BERT token classifier on it?",
        ["Put B-LOC on the first subword and give the other subwords a label that the loss ignores (e.g. -100)",
         "Put B-LOC on all three subwords",
         "Put B-LOC, I-LOC, I-LOC on the three subwords and count all three in the F1",
         "Drop the word from the training data"], 0,
        "Labels belong to words; the model sees subwords.",
        "Word-level gold tags must be aligned to subwords. The common recipe labels only the first subword and masks the rest out of the loss (label -100 in PyTorch / Hugging Face), then predicts the word's tag from its first subword. Labelling every subword B-LOC would create three B- tags, i.e. three entities, when decoded.",
        topic="neural-ner", level=2,
        diagram="""
word:     Bengaluru
subwords: Ben     ##gal   ##uru
labels:   B-LOC   -100    -100   (-100 = ignored)
"""),
    out('gold = {("Mumbai", "LOC"), ("Acme Corp", "ORG"), ("Ravi Kumar", "PER"),\n'
        '        ("2024", "DATE"), ("Delhi", "LOC"), ("Rs. 50 lakh", "MONEY")}\n'
        'pred = {("Mumbai", "LOC"), ("Acme", "ORG"), ("Ravi Kumar", "PER"),\n'
        '        ("2024", "DATE"), ("Delhi", "ORG")}\n'
        'tp = len(gold & pred)\n'
        'p, r = tp / len(pred), tp / len(gold)\n'
        'f1 = 2 * p * r / (p + r)\n'
        'print(tp, round(p, 3), round(r, 3), round(f1, 3))',
        ["3 0.6 0.5 0.545", "4 0.8 0.667 0.727", "3 0.5 0.6 0.545", "3 0.6 0.5 0.55"], 0,
        "A pair only matches if both span and type are identical.",
        "Exact match needs span AND type: 'Acme' is a partial span and 'Delhi' has the wrong type, so only Mumbai, Ravi Kumar and 2024 match. P = 3/5 = 0.6, R = 3/6 = 0.5, F1 = 2(0.6)(0.5)/1.1 = 0.545. Using sets of (span, type) pairs is exactly the course's exact-match rule.",
        topic="ner-eval", level=2),
    mcq("Gold: 'New York City' (LOC). System: 'New York' (LOC). How is this scored under the CoNLL exact-match scheme?",
        ["Zero credit: one FP (the predicted span) and one FN (the gold span)",
         "One TP, because the type is right",
         "Half a TP, because two of three tokens overlap",
         "Nothing at all: it is neither FP nor FN"], 0,
        "Exact match needs identical boundaries.",
        "The course's boundary-mismatch slide: 'New York' vs 'New York City' fails. Exact-match scoring gives no partial credit; relaxed schemes such as MUC or SemEval's partial match would give some credit for the overlap.",
        topic="ner-eval", level=2),
    fill("____-F1 pools every entity of every type before computing P and R, so frequent types dominate the score.", "Micro",
         "The other option averages per-type F1.",
         "Micro-F1 pools TP/FP/FN over all entities. Macro-F1 computes F1 per type and averages them equally, so a rare type like MONEY counts as much as PERSON. Report both when rare types matter.",
         topic="ner-eval", level=2),
    mcq("'Steve Jobs, co-founder of Apple' expresses which ACE relation type, with which argument types?",
        ["Org-AFF-Founder, PER-ORG",
         "Part-Whole-Subsidiary, ORG-ORG",
         "Person-Social-Family, PER-PER",
         "Physical-Located, PER-GPE"], 0,
        "A person and the organisation they founded.",
        "The course's ACE examples: Physical-Located (PER-GPE) 'He was in Tennessee'; Part-Whole-Subsidiary (ORG-ORG) 'XYZ, the parent company of ABC'; Person-Social-Family (PER-PER) 'John's wife Yoko'; Org-AFF-Founder (PER-ORG) 'Steve Jobs, co-founder of Apple'. Fixing the argument types is what lets NE tags guide relation extraction.",
        topic="re-patterns", level=2),
    out('import re\n'
        's = "The shop sells instruments such as sitar, tabla and veena."\n'
        'm = re.search(r"(\\w+) such as ((?:\\w+, )*\\w+ (?:and|or) \\w+)", s)\n'
        'hyper = m.group(1)\n'
        'hypos = re.split(r", | and | or ", m.group(2))\n'
        'print([(h, "IS-A", hyper) for h in hypos][-1], len(hypos))',
        ["('veena', 'IS-A', 'instruments') 3",
         "('veena', 'IS-A', 'sitar') 3",
         "('instruments', 'IS-A', 'veena') 3",
         "('veena', 'IS-A', 'instruments') 2"], 0,
        "Y such as X1, X2 and X3: each X is a kind of Y.",
        "Group 1 is the hypernym 'instruments'; group 2 'sitar, tabla and veena' splits into three hyponyms. Each gives a triple hyponym IS-A hypernym. This is Hearst's 'Y such as X ((, X)* (, and|or) X)' pattern as a regex.",
        topic="re-patterns", level=2),
    tf("According to the course, hand-built relation patterns tend to be high-precision but low-recall.", True,
       "Rules rarely fire wrongly, but how many phrasings do they cover?",
       "A rule like '[PERSON], CEO of [ORG]' is usually right when it fires, but people express the same relation in hundreds of ways, so it misses most instances. The course also notes it is 'a lot of work to think of all possible patterns' for every relation.",
       topic="re-patterns", level=2),
    mcq("The course's supervised relation extraction classifies entity pairs in which steps?",
        ["Find all pairs of named entities (usually in one sentence) -> decide whether the two are related -> if yes, classify the relation",
         "Classify every word in the sentence -> find pairs -> decide if related",
         "Classify the relation first -> then find the entities that fit",
         "Cluster all sentences -> label each cluster with a relation"], 0,
        "There is a yes/no filter before the multi-class step.",
        "Most entity pairs in a sentence are unrelated, so a binary 'related?' classifier first removes them. That makes training the relation-type classifier faster and lets each step use its own feature set, which is the course's answer to 'why the extra step?'.",
        diagram="""
all entity pairs in sentence
   -> [related? yes/no]  (drops most pairs)
   -> [which relation?]  e.g. Org-AFF, Located-in
""",
        topic="re-supervised", level=2),
    mcq("For 'American Airlines, a unit of AMR, immediately matched the move, spokesman Tim Wagner said', which is a named-entity-type feature from the course?",
        ["The concatenation of the two mention types: ORG-PERSON",
         "The bag of words between the mentions: {a, unit, of, AMR, ...}",
         "The dependency path Airlines <- matched -> said -> Wagner",
         "The word before mention 2: spokesman"], 0,
        "All four are course features; only one uses NE types.",
        "The course groups features into word features (headwords, bags of words, positional words, words between), NE-type and mention-level features (M1 ORG, M2 PERSON, their concatenation ORG-PERSON, entity level NAME / NOMINAL / PRONOUN) and parse features (chunk sequence, constituent path, dependency path).",
        topic="re-supervised", level=2),
    mcq("Distant supervision (Mintz et al., 2009) gets its training labels from where?",
        ["A large existing knowledge base: every sentence that mentions both entities of a known tuple is treated as a (noisy) positive example",
         "Crowd workers who label each sentence by hand",
         "Five hand-picked seed tuples, as in DIPRE",
         "The model's own predictions on a test set"], 0,
        "Instead of five seeds, use a whole database.",
        "Course steps: for each relation (Born-In), for each tuple in a big database (<Edwin Hubble, Marshfield>), find sentences with both entities, extract frequent features ('PER was born in LOC'), and train a supervised classifier over thousands of patterns. It combines bootstrapping's idea with supervised learning.",
        topic="re-semi", level=2,
        diagram="""
KB: Born-In(Hubble, Marshfield), Born-In(Einstein, Ulm)
          | match both entities in text
"Hubble was born in Marshfield"   -> PER was born in LOC
"Einstein, born (1879), Ulm"      -> PER, born (XXXX), LOC
          | features from 1000s of matches
train classifier P(born-in | f1 ... fn)
"""),
    mcq("Snowball improved on DIPRE's bootstrapping in which two ways, according to the course?",
        ["It requires X and Y to be named entities of the right types, and it computes a confidence for each pattern",
         "It uses a neural network and needs no seeds",
         "It uses a knowledge base instead of seeds and computes recall",
         "It only works on tables, not on plain text"], 0,
        "ORGANIZATION {'s, in, headquarters} LOCATION  .69",
        "Snowball (Agichtein & Gravano 2000) extracts <Organization, Headquarters location> pairs. Requiring NE types stops patterns matching random noun phrases, and pattern confidences (.69, .75 in the course's slide) let it keep only reliable patterns and tuples.",
        topic="re-semi", level=2),
    tf("Open Information Extraction extracts relations from the web with no training data and no predefined list of relations.", True,
       "(Tesla, invented, coil transformer)",
       "Open IE (Banko et al. 2007, TextRunner) trains a 'trustworthy tuple' classifier, extracts all relations between noun phrases in one pass, and ranks them by redundancy. The relation name is just the connecting phrase, such as 'specializes in'.",
       topic="re-semi", level=2),
    mcq("'IBM purchased Microsoft' and 'IBM was purchased by Microsoft' contain the same two entities. What does event extraction add that NER cannot?",
        ["The roles: who is the buyer and who is acquired, which are reversed in the two sentences",
         "The entity types, which differ between the sentences",
         "Nothing; both give the same output",
         "The sentiment of each sentence"], 0,
        "Same entities, opposite meaning.",
        "The course: NER identifies types of entities; event extraction identifies role relationships associated with events. An NER system outputs IBM (ORG), Microsoft (ORG) for both sentences; an event extractor must output Acquirer = IBM in one and Acquirer = Microsoft in the other, which means handling passive voice.",
        diagram="""
IBM purchased Microsoft        Acquirer=IBM  Acquired=MS
IBM was purchased by Microsoft Acquirer=MS   Acquired=IBM
NER output for both: IBM (ORG), Microsoft (ORG)
""",
        topic="events", level=2),
    tf("In the course, relation extraction and event extraction differ only in name: both link exactly two entities.", False,
        "Binary link vs 'who did what to whom, where and when'.",
        "Employment(Meera Nair, CloudNova) is a binary relation. An acquisition event has a trigger ('acquired') and several role-filled arguments (Acquirer, Acquired, Price, Time), giving 'a richer picture' than relation extraction.",
        topic="events", level=2),
    mcq("Sequence-labelling temporal expression recognition tags 'the meeting moved to next Friday' how, in the course's IOB-with-TIMEX3 scheme?",
        ["the/O meeting/O moved/O to/O next/B Friday/I",
         "the/O meeting/O moved/O to/B next/I Friday/I",
         "the/O meeting/O moved/O to/O next/O Friday/B",
         "the/B meeting/I moved/O to/O next/B Friday/I"], 0,
        "Mark only the tokens of the time expression.",
        "The span 'next Friday' is the TIMEX3: 'next' begins it (B) and 'Friday' is inside (I); everything else is O. It is the same IOB idea used for named entities, with one expression type. 'to' is a preposition before the expression, not part of it.",
        topic="temporal", level=2),
    tf("The course describes rule-based temporal expression recognisers as cascades of automata: tokens are POS-tagged, then larger chunks are recognised stage by stage using trigger words (February) and classes (MONTH).", True,
        "Small patterns first, bigger ones built on top.",
        "Stage 1 recognises 'February' as a MONTH, stage 2 combines a number + MONTH into a date, stage 3 attaches modifiers such as 'early' or 'next'. Each stage works on the previous stage's output, like a pipeline of regex passes.",
        topic="temporal", level=2,
        analogy="Like a compiler front end: a lexer finds tokens, then a parser builds larger structures from them."),
    fill("In TimeML, temporal expressions are marked up with the ____ tag (letters and a digit).", "TIMEX3",
         "TIMEX, version 3.",
         "TIMEX3 marks a temporal expression's span and records its type (DATE, TIME, DURATION, SET) and its normalised value, e.g. value=\"2026-01-05\" or value=\"P6W\". The course's IOB labelling slide labels the span of each TIMEX3.",
         topic="temporal", level=2),
    # ------------------------------------------------------------------ L3
    mcq("An agritech news IE system is scored with exact match (span AND type). Gold has 10 entities: Hyderabad (LOC), 2 August 2026 (DATE), AgriSense Labs (ORG, 1st mention), KisanNet (ORG), ₹120 crore (MONEY), Kavya Reddy (PER), Telangana (LOC), AgriSense Labs (ORG, 2nd mention), NABARD (ORG), 2019 (DATE). The system outputs 9: Hyderabad (LOC), 2 August 2026 (DATE), AgriSense Labs (ORG, 1st), KisanNet (PER), ₹120 (MONEY), Kavya Reddy (PER), Telangana (LOC), Founder (PER), 2019 (DATE). What are P, R and F1?",
        ["TP 6, FP 3, FN 4: P 0.667, R 0.600, F1 0.632",
         "TP 7, FP 2, FN 3: P 0.778, R 0.700, F1 0.737",
         "TP 6, FP 3, FN 3: P 0.667, R 0.667, F1 0.667",
         "TP 6, FP 2, FN 4: P 0.750, R 0.600, F1 0.667"], 0,
        "Wrong type and partial span each cost an FP AND an FN; count the 2nd mention.",
        "TP = Hyderabad, the date, AgriSense (1st), Kavya Reddy, Telangana, 2019 = 6. FP = KisanNet (PER, wrong type), '₹120' (partial span), 'Founder' (spurious) = 3. FN = KisanNet (ORG), ₹120 crore, AgriSense (2nd mention), NABARD = 4. P = 6/9, R = 6/10, F1 = 12/19 = 0.632. Counting the partial span as a TP is the classic lost mark.",
        topic="ner-eval", level=3),
    out('gold = [(0, 3, "ORG"), (5, 6, "PER"), (8, 10, "MONEY")]   # [start, end) tokens\n'
        'pred = [(0, 2, "ORG"), (5, 6, "PER"), (8, 10, "DATE")]\n'
        'def f1(match):\n'
        '    tp = sum(any(match(p, g) for g in gold) for p in pred)\n'
        '    p, r = tp / len(pred), tp / len(gold)\n'
        '    return round(2 * p * r / (p + r), 3) if tp else 0.0\n'
        'exact = lambda p, g: p == g\n'
        'partial = lambda p, g: p[2] == g[2] and p[0] < g[1] and g[0] < p[1]\n'
        'print(f1(exact), f1(partial))',
        ["0.333 0.667", "0.333 1.0", "0.667 0.667", "0.333 0.333"], 0,
        "Partial = same type and overlapping spans. Does MONEY vs DATE count?",
        "Exact: only PER matches, so P = R = 1/3. Partial (overlap with the same type): the truncated ORG also counts, so P = R = 2/3. MONEY vs DATE still fails because the type differs. Relaxed schemes (MUC, SemEval partial) reward boundary-near misses; the course's exams use exact match unless told otherwise.",
        topic="ner-eval", level=3),
    out('gold = ["B-ORG", "I-ORG", "I-ORG", "O", "O", "B-PER", "I-PER", "O"]\n'
        'pred = ["B-ORG", "I-ORG", "O",     "O", "O", "B-PER", "I-PER", "O"]\n'
        'acc = sum(g == p for g, p in zip(gold, pred)) / len(gold)\n'
        '# spans: gold ORG(0-3), PER(5-7); pred ORG(0-2), PER(5-7)\n'
        'tp, n_pred, n_gold = 1, 2, 2\n'
        'p, r = tp / n_pred, tp / n_gold\n'
        'print(acc, 2 * p * r / (p + r))',
        ["0.875 0.5", "0.875 0.875", "0.5 0.875", "1.0 0.5"], 0,
        "One wrong token; how many wrong entities?",
        "Token accuracy is 7/8 = 0.875 because O tokens are easy and plentiful. At span level the truncated ORG is a miss, so only PER matches: F1 = 0.5. This is why the course says to score NER at the entity level, not per token.",
        topic="ner-eval", level=3),
    out('states = ["PER", "O"]\n'
        'start = {"PER": 0.4, "O": 0.6}\n'
        'A = {("PER", "PER"): 0.5, ("PER", "O"): 0.5, ("O", "PER"): 0.2, ("O", "O"): 0.8}\n'
        'B = {"PER": {"Asha": 0.5, "Rao": 0.4, "spoke": 0.01},\n'
        '     "O":   {"Asha": 0.05, "Rao": 0.05, "spoke": 0.3}}\n'
        'words = ["Asha", "Rao", "spoke"]\n'
        'v = [{s: (start[s] * B[s][words[0]], [s]) for s in states}]\n'
        'for w in words[1:]:\n'
        '    v.append({s: max((v[-1][q][0] * A[(q, s)] * B[s][w], v[-1][q][1] + [s])\n'
        '                     for q in states) for s in states})\n'
        'best = max(v[-1].values())\n'
        'print(round(v[1]["PER"][0], 4), round(best[0], 4), best[1])',
        ["0.04 0.006 ['PER', 'PER', 'O']",
         "0.1 0.006 ['PER', 'PER', 'O']",
         "0.04 0.0002 ['PER', 'PER', 'PER']",
         "0.04 0.006 ['PER', 'O', 'O']"], 0,
        "v2(PER) = max over previous tag of v1 · transition, then times the emission.",
        "v1: PER = 0.4 × 0.5 = 0.2, O = 0.6 × 0.05 = 0.03. v2(PER) = max(0.2 × 0.5, 0.03 × 0.2) × 0.4 = 0.04; v2(O) = max(0.1, 0.024) × 0.05 = 0.005. v3(O) = max(0.04 × 0.5, 0.005 × 0.8) × 0.3 = 0.006 beats v3(PER) = 0.0002. Backtrace: PER PER O. This is the exam's 'Viterbi step by hand'.",
        topic="sequence-models", level=3,
        diagram="""
        Asha      Rao       spoke
PER     0.2  ->   0.04  ->  0.0002
O       0.03      0.005     0.006  <- best (from PER 0.04)
backtrace: O <- PER <- PER   =>  PER PER O
"""),
    mcq("Using the Viterbi recurrence v_t(j) = max_i v_{t-1}(i) · a_ij · b_j(o_t): v1(LOC) = 0.12, v1(O) = 0.30, a(LOC->LOC) = 0.3, a(O->LOC) = 0.1, b_LOC('Pune') = 0.5. What is v2(LOC), and which back-pointer is stored?",
        ["0.018, back-pointer to LOC", "0.015, back-pointer to O", "0.033, back-pointers to both", "0.036, back-pointer to LOC"], 0,
        "Compute both incoming paths, keep the max, then multiply by the emission.",
        "From LOC: 0.12 × 0.3 = 0.036. From O: 0.30 × 0.1 = 0.030. Max = 0.036 from LOC; × 0.5 = 0.018. Viterbi keeps only the best incoming path (max, not sum) and remembers where it came from for the backtrace. Summing both (0.066 × 0.5 = 0.033) would be the Forward algorithm, which gives a probability, not a best path.",
        analogy="Viterbi is memoised dynamic programming, like a shortest-path algorithm: keep only the best way to reach each state at each step, plus a back-pointer.",
        topic="sequence-models", level=3),
    out('start = {"A": 0.6, "B": 0.4}\n'
        'trans = {("A", "A"): 0.5, ("A", "B"): 0.5, ("B", "A"): 0.1, ("B", "B"): 0.9}\n'
        'emit = {"A": [0.5, 0.1], "B": [0.6, 0.5]}     # P(w1|tag), P(w2|tag)\n'
        '# greedy: pick the best tag at each step, never revisit\n'
        't1 = max("AB", key=lambda s: start[s] * emit[s][0])\n'
        't2 = max("AB", key=lambda s: trans[(t1, s)] * emit[s][1])\n'
        'g = start[t1] * emit[t1][0] * trans[(t1, t2)] * emit[t2][1]\n'
        '# exhaustive search = what Viterbi finds\n'
        'best = max((start[a] * emit[a][0] * trans[(a, b)] * emit[b][1], a + b)\n'
        '           for a in "AB" for b in "AB")\n'
        'print(t1 + t2, round(g, 3), best[1], round(best[0], 3))',
        ["AB 0.075 BB 0.108", "BB 0.108 BB 0.108", "AB 0.075 AB 0.075", "AA 0.015 BB 0.108"], 0,
        "Greedy commits to A at step 1 because 0.30 > 0.24.",
        "Greedy picks A first (0.6 × 0.5 = 0.30 vs 0.24), then B: path AB = 0.075. But B -> B has transition 0.9, so BB = 0.24 × 0.9 × 0.5 = 0.108 is better. Greedy MEMM-style decoding can lock in a locally best tag; Viterbi keeps every state's best path and finds BB.",
        topic="sequence-models", level=3),
    out('def to_bioes(tags):\n'
        '    res = []\n'
        '    for i, t in enumerate(tags):\n'
        '        nxt = tags[i + 1] if i + 1 < len(tags) else "O"\n'
        '        if t == "O":\n'
        '            res.append(t); continue\n'
        '        pre, typ = t.split("-")\n'
        '        cont = nxt == "I-" + typ\n'
        '        res.append(("B-" if cont else "S-") + typ if pre == "B" else ("I-" if cont else "E-") + typ)\n'
        '    return res\n'
        'print(" ".join(to_bioes(["B-PER", "I-PER", "I-PER", "O", "B-LOC", "O", "B-ORG", "I-ORG"])))',
        ["B-PER I-PER E-PER O S-LOC O B-ORG E-ORG",
         "B-PER I-PER I-PER O B-LOC O B-ORG I-ORG",
         "B-PER I-PER E-PER O B-LOC O B-ORG E-ORG",
         "S-PER I-PER E-PER O S-LOC O S-ORG E-ORG"], 0,
        "E- ends a multi-token entity; S- is a single-token entity.",
        "BIOES (also called BILOU) marks the last token with E- and one-token entities with S-. 'Pune'-style single tokens become S-LOC. The extra tags give a CRF explicit boundary information, which often helps on long names (biomedical NER).",
        topic="bio-tagging", level=3),
    mcq("A softmax-per-token NER model outputs 'O I-PER I-PER O' for 'the Asha Rao said'. What is wrong, and what in the architecture prevents it?",
        ["An entity cannot start with I-; a CRF layer with learned transition scores (O -> I-PER is heavily penalised) plus Viterbi decoding avoids such sequences",
         "Nothing is wrong; I- may start an entity in BIO",
         "The tokenizer is wrong; use a bigger vocabulary",
         "The sentence needs BIOES, which allows I- at the start"], 0,
        "Each token's tag was chosen independently.",
        "In the BIO scheme the course uses, every mention begins with B-. Independent per-token softmax can't see that O -> I-PER is invalid. A CRF scores the whole tag sequence including transitions, so the best-scoring sequence is 'O B-PER I-PER O'. A quick fix without a CRF is a decoding rule that converts a stray I-X to B-X.",
        topic="bio-tagging", level=3),
    fill("Tag 'Dr. Asha Rao of the Indian Institute of Science spoke in Bengaluru .' with BIO (PER, ORG, LOC; 'Dr.' is part of the person, 'the' is not part of the ORG). How many tokens get a B- tag? ____", "3",
         "Count the entities, not the tokens.",
         "Each entity has exactly one B- tag: Dr. Asha Rao (B-PER I-PER I-PER), Indian Institute of Science (B-ORG I-ORG I-ORG I-ORG), Bengaluru (B-LOC). So 3 B- tags, 5 I- tags and the other 5 tokens (of, the, spoke, in, .) are O.",
         analogy="Like counting rows by counting primary keys: one B- tag per entity, however many tokens it spans.",
         topic="bio-tagging", level=3),
    mcq("A biomedical NER system keeps failing on gene names such as 'breast cancer associated 1' and 'ether a go-go'. Which course reason explains this best?",
        ["Biomedical names are long multi-token spans that look like ordinary words, with spelling variants and abbreviations, so boundary detection and ambiguity are hard",
         "Gene names are always single tokens, so BIO tagging cannot represent them",
         "Biomedical text has no capital letters",
         "CRFs cannot be trained on scientific articles"], 0,
        "Where does 'breast cancer associated 1' start and end, and is 'breast cancer' a disease?",
        "The course lists long names (multi-token boundary detection), spelling and typographical variants, abbreviations and symbols, and ambiguity with common meanings. Extracted names are then mapped to ontologies such as Gene Ontology or UMLS. Domain gazetteers and BIOES-style boundary tags help.",
        topic="ner-basics", level=3),
    out('# EE/RE tuples: a match needs the type AND every argument exact\n'
        'gold = [("Acquisition", "Zentro", "Paylite", "2025"), ("HQ", "Zentro", "Pune"),\n'
        '        ("CEO_of", "Neha Iyer", "Zentro"), ("Funding", "Paylite", "$5M")]\n'
        'pred = [("Acquisition", "Zentro", "Paylite", "2025"), ("HQ", "Zentro", "Mumbai"),\n'
        '        ("CEO_of", "Neha Iyer", "Zentro")]\n'
        'tp = sum(t in gold for t in pred)\n'
        'p, r = tp / len(pred), tp / len(gold)\n'
        'print(tp, round(p, 3), r, round(2 * p * r / (p + r), 3))',
        ["2 0.667 0.5 0.571", "3 1.0 0.75 0.857", "2 0.5 0.667 0.571", "2 0.667 0.5 0.583"], 0,
        "The HQ tuple has the right type but a wrong argument.",
        "Acquisition and CEO_of match exactly. HQ(Zentro, Mumbai) has one wrong argument, so it is an FP and the gold HQ(Zentro, Pune) is an FN; the Funding tuple is missed. P = 2/3, R = 2/4, F1 = 0.571. The Mar 2026 end-sem scores EE/RE exactly this way: type and all arguments must match.",
        topic="re-supervised", level=3),
    mcq("Bootstrapping for Headquartered-In(ORG, LOC): the seed <Zomato, Gurugram> returns 'Zomato, headquartered in Gurugram, reported...' and 'Gurugram's Zomato expanded...'. Which patterns and new tuple from 'Bengaluru's Flipkart announced a sale' are right?",
        ["Patterns 'X, headquartered in Y' and 'Y's X'; new tuple Headquartered-In(Flipkart, Bengaluru)",
         "Patterns 'X, headquartered in Y' and 'Y's X'; new tuple Headquartered-In(Bengaluru, Flipkart)",
         "Pattern 'Zomato, headquartered in Gurugram'; no new tuple",
         "Patterns 'X reported' and 'X expanded'; new tuple Headquartered-In(Flipkart, sale)"], 0,
        "Replace the seed entities with X (ORG) and Y (LOC), keep the context words.",
        "Generalise each context by replacing the seed ORG with X and LOC with Y. 'Y's X' then matches 'Bengaluru's Flipkart', giving Headquartered-In(Flipkart, Bengaluru) with the ORG first. Getting the argument order backwards is the common slip; the 2026 makeup end-sem asks exactly this kind of step.",
        topic="re-semi", level=3,
        diagram="""
seed <Zomato, Gurugram>
 "Zomato, headquartered in Gurugram" => X, headquartered in Y
 "Gurugram's Zomato"                 => Y's X
"Bengaluru's Flipkart" matches Y's X
 -> new tuple <Flipkart, Bengaluru> -> next iteration
"""),
    mcq("A distant-supervision system uses the KB fact Founder(Steve Jobs, Apple). Which training sentence shows the method's main weakness?",
        ["'Steve Jobs unveiled the iPhone at an Apple event' is labelled as a Founder example",
         "'Steve Jobs co-founded Apple in 1976' is labelled as a Founder example",
         "'Apple was started by Steve Jobs and Steve Wozniak' is labelled as a Founder example",
         "A sentence without Steve Jobs is ignored"], 0,
        "Two entities in one sentence don't guarantee the relation is stated.",
        "Distant supervision assumes any sentence mentioning both entities expresses the KB relation. 'Unveiled the iPhone at an Apple event' doesn't, so it becomes a noisy positive. The course: weak supervision costs no annotation but is 'often noisy'. Fixes: many features over thousands of sentences, multi-instance learning, de-noising.",
        analogy="Like auto-labelling support tickets by joining them with the CRM on customer ID: cheap and large, but the join says nothing about what each ticket is really about.",
        topic="re-semi", level=3),
    out('extracted = 40_000          # new tuples from a bootstrapped extractor\n'
        'sample = 200                # randomly sampled and checked by hand\n'
        'correct_in_sample = 150\n'
        'p_hat = correct_in_sample / sample\n'
        'print(p_hat, int(p_hat * extracted))',
        ["0.75 30000", "0.75 150", "0.005 200", "0.75 40000"], 0,
        "Estimate precision on the sample, then scale.",
        "With no gold set, the course estimates precision from a random sample: P^ = 150/200 = 0.75, so about 30,000 of the 40,000 tuples are probably correct. Recall can't be estimated: you don't know how many true tuples exist on the web. Precision at top-N (top 1,000, top 10,000...) repeats this on ranked subsets.",
        topic="re-semi", level=3),
    tf("For an Open IE or bootstrapped relation extractor run over the web, the course says you can compute precision exactly but recall only approximately.", False,
       "What would you need to know to compute recall at all?",
       "Neither is exact: there is no gold set. Precision is approximated from a hand-checked random sample (also precision at top-N); recall cannot be evaluated because the set of all true relations on the web is unknown.",
       topic="re-semi", level=3),
    mcq("A team asks a large language model to output relation triples as JSON from contract clauses. Spot checks find well-formed triples such as Indemnifies(VendorX, ClientY) that no clause states. Which course-recommended fix fits best?",
        ["Validate triples against the source text and use schema-constrained decoding so only allowed relation types and argument spans can be produced",
         "Raise the temperature so the model explores more triples",
         "Remove the schema from the prompt so the model is less constrained",
         "Switch to token-level evaluation, which ignores the extra triples"], 0,
        "The course: 'hallucinated triples need validation and constrained decoding'.",
        "LLM RE gives strong zero/few-shot results, but it can invent triples. Constrained decoding restricts outputs to the ontology; a validation step checks each argument appears in the text (and can use a verifier or rules). The course also notes LLMs can still trail fully fine-tuned supervised models in-domain.",
        topic="re-semi", level=3),
    mcq("'Patna - Health officials reported on 14 July 2026 that a cholera outbreak in Gaya district had affected 340 people.' Fill {Trigger, Disease, Place, Affected-Count, Report-Date}.",
        ["outbreak; cholera; Gaya district; 340; 14 July 2026",
         "reported; cholera; Patna; 340; 14 July 2026",
         "outbreak; cholera; Patna; 340 people; 14 July",
         "affected; Gaya district; cholera; 340; 2026"], 0,
        "The dateline place is where the news was filed, not where the event happened.",
        "The trigger is the event noun 'outbreak'. The outbreak is in Gaya district (Patna is the dateline), 340 is the count, and the report date is 14 July 2026. 'reported' is the reporting event, not the outbreak event: a frequent exam slip, as is copying the dateline into the Place slot.",
        topic="events", level=3),
    mcq("In a pipeline NER -> relation extraction, NER misses 'DataSprint' in 'DataSprint was founded in Pune in 2018'. What happens downstream, and what does the course propose?",
        ["Founded-in(DataSprint, Pune) and Founding-year(DataSprint, 2018) can never be extracted: errors propagate; joint models such as OneIE decode entities, relations and events together",
         "Relation extraction recovers the entity automatically, so nothing is lost",
         "Only precision drops, because missing entities create false positives",
         "Nothing; relation extraction runs on the raw text, not on NER output"], 0,
        "A relation's arguments must be entities.",
        "The course's motivation slide: 'pipeline models suffer from the error propagation problem and disallow interactions among components'. One NER miss costs every relation and event argument that needed it (recall loss). OneIE identifies mentions and triggers with CRF taggers, classifies nodes and edges, and uses beam search for the globally best information graph.",
        analogy="Like a chain of microservices with no retries: if the first service drops a record, every downstream service silently never sees it.",
        topic="ie-overview", level=3),
    mcq("Classify 'within ten days', 'every Monday' and '17 October 2026' in TimeML terms.",
        ["Relative (anchored to a reference date); SET (a recurring time); absolute DATE",
         "Duration; relative; absolute",
         "Absolute; duration; relative",
         "Duration; duration; absolute"], 0,
        "The course mentions 'sets of these' too.",
        "'within ten days' is a deadline anchored to the document time, which the course's exams class as RELATIVE (a duration-based reading is accepted only if justified). 'every Monday' is a recurring set of times (TIMEX3 type SET). '17 October 2026' is absolute. 'for two months' alone would be a DURATION.",
        topic="temporal", level=3),
    out('from datetime import date, timedelta\n'
        'dct = date(2026, 1, 5)                  # document creation time (a Monday)\n'
        'days = (0 - dct.weekday()) % 7 or 7     # Monday = 0; "next" never means today\n'
        'next_monday = dct + timedelta(days=days)\n'
        'in_six_weeks = dct + timedelta(weeks=6)\n'
        'print(next_monday.isoformat(), in_six_weeks.isoformat(), "P6W")',
        ["2026-01-12 2026-02-16 P6W", "2026-01-05 2026-02-16 P6W", "2026-01-12 2026-02-12 P6W", "2026-01-12 2026-02-16 6W"], 0,
        "If today is Monday, 'next Monday' is 7 days away.",
        "Normalisation anchors relative expressions to the document creation time: next Monday = 2026-01-12, six weeks later = 2026-02-16. A pure duration 'six weeks' normalises to the ISO 8601 value P6W in TIMEX3. Systems store the normalised value, not the raw text.",
        topic="temporal", level=3),
    mcq("A hospital wants to tag rare diseases, drugs and procedures in discharge notes. It has almost no labelled notes but a large curated medical knowledge base. Which course NER approach fits best?",
        ["Retrieval-augmented (RAG) NER: retrieve matching knowledge-base entries and let an LLM extract entities grounded in them",
         "A rule-based tagger with 'Dr.' + capitalised word rules",
         "A BiLSTM-CRF trained from scratch on the few labelled notes",
         "Plain zero-shot LLM prompting with no external knowledge"], 0,
        "Specialised domain + external knowledge + little labelled data.",
        "The course's RAG NER workflow is Input -> Retriever -> Knowledge Base -> LLM -> Entity Extraction, with exactly this hospital example (rare diseases, drugs, procedures). Training a BiLSTM-CRF needs far more labels; zero-shot alone misses rare domain terms and hallucinates; title rules only find people.",
        diagram="""
note -> retriever -> medical KB entries
     -> LLM (note + KB context) -> entities
""",
        topic="neural-ner", level=3),
    mcq("A bank must extract IFSC codes, account numbers and dates in DD/MM/YYYY from fixed-format statements, and every extraction must be auditable. What is the most sensible first choice?",
        ["Rule-based extraction with regular expressions: the formats are fixed, precision matters and every match is explainable",
         "A large language model prompted per statement",
         "A BiLSTM-CRF trained on news text",
         "Distant supervision from Wikipedia"], 0,
        "Controlled domain, explicit formats, audit trail.",
        "The course's RE/NER tables say rules suit 'controlled domains where relationships are explicit and predictable' and are highly interpretable. An LLM adds cost, inconsistency and hallucination risk to a problem a regex solves. Rules also make a cheap first labelled set for training a model later.",
        topic="ner-rules", level=3,
        analogy="Like validating a PAN or IFSC in a form with a regex instead of calling an ML service: deterministic, cheap and easy to audit."),
    tf("A CRF normalises over whole tag sequences, while a MEMM normalises each token's tag distribution separately, which is why MEMMs can suffer from the label bias problem.", True,
       "Local vs global normalisation.",
       "In a MEMM each state's outgoing probabilities must sum to 1, so a state with few successors passes its probability on almost regardless of the word (label bias). A CRF scores the full sequence and normalises once over all sequences, so evidence anywhere can override a locally confident choice.",
       topic="sequence-models", level=3),
    tf("The course starts relation extraction from named-entity tags (located-in(ORGANIZATION, LOCATION), cures(DRUG, DISEASE)) because typed arguments filter out most wrong candidate pairs and make patterns more precise.", True,
        "What can 'X cures Y' match if X and Y can be any noun phrase?",
        "'X cures Y' with untyped X and Y matches 'Time cures sorrow'. Requiring X = DRUG and Y = DISEASE removes such matches. The same idea is why Snowball requires X and Y to be named entities and why supervised RE uses NE-type features such as ORG-PERSON.",
        topic="re-patterns", level=3),
    mcq("In the course's generative event extraction example ('On Tuesday, IBM acquired Red Hat for $34 billion'), what does constrained decoding guarantee?",
        ["The output record only uses event types and roles from the schema in the prompt, e.g. Merge-Org with Acquirer, Acquired, Price, Time",
         "The extracted values are factually true in the real world",
         "Every token in the sentence is tagged with BIO labels",
         "The trigger word gets its own separate classifier"], 0,
        "It restricts the form, not the truth.",
        "Generative EE (Text2Event, DEGREE, GTEE) writes the whole record in one pass; constrained decoding stops it inventing a role such as 'BuyerCompany' or an event type outside the ontology. It does not verify that IBM really paid $34 billion; argument values still need checking against the text.",
        topic="events", level=3,
        diagram="""
text + schema(Merge-Org: Acquirer, Acquired, Price, Time)
        -> seq2seq / LLM -> constrained decoding
        -> Merge-Org{Acquirer: IBM, Acquired: Red Hat,
                     Price: $34 billion, Time: Tuesday}
"""),
    mcq("A team has 50,000 labelled sentences for 6 relation types in its own domain, and the production system needs the best in-domain accuracy at low cost per document. What does the course's material suggest?",
        ["Fine-tune a supervised model (e.g. BERT-based) on the labelled data; LLM prompting can still trail fully fine-tuned models in-domain and costs more per call",
         "Use only hand-written patterns because supervised models need no data",
         "Use Open IE, since it needs no relation list",
         "Use bootstrapping from 5 seeds and ignore the labels"], 0,
        "Plenty of labels, fixed schema, cost matters.",
        "The course: LLMs win on new schemas and low-resource domains, but 'LLMs can still trail fully fine-tuned supervised models' and cost, latency and reproducibility are concerns. With 50k labels and a fixed schema, a fine-tuned encoder is the strong, cheap choice; an LLM can help label edge cases.",
        topic="re-supervised", level=3),
    out('# template-level IE accuracy (course slide): N gold slots, E extracted, C correct\n'
        'N, E, C = 12, 10, 8\n'
        'R, P = C / N, C / E\n'
        'F = 2 * P * R / (P + R)\n'
        'print(round(R, 3), P, round(F, 3))',
        ["0.667 0.8 0.727", "0.8 0.667 0.727", "0.667 0.8 0.733", "0.833 0.8 0.816"], 0,
        "Recall divides by what should have been found; precision by what was extracted.",
        "The course's IE accuracy slide: Recall = C/N = 8/12, Precision = C/E = 8/10, F = harmonic mean = 0.727. It is the same P/R/F1 idea as NER, applied to slot/value pairs in the solution template.",
        topic="ie-overview", level=3),
    # ------------------------------------------------------------------ L4
    out('# gold and predicted entities as (text, type, start_offset)\n'
        'gold = [("FinEdge", "ORG", 0), ("Mumbai", "LOC", 30), ("FinEdge", "ORG", 88)]\n'
        'pred = [("FinEdge", "ORG", 0), ("Mumbai", "LOC", 30)]\n'
        'drop = lambda xs: {(t, y) for t, y, _ in xs}        # buggy: ignores offsets\n'
        'r_bug = len(drop(gold) & drop(pred)) / len(drop(gold))\n'
        'r_ok = len(set(gold) & set(pred)) / len(gold)\n'
        'print(r_bug, round(r_ok, 3))',
        ["1.0 0.667", "0.667 0.667", "1.0 1.0", "0.667 1.0"], 0,
        "How many gold entities does the buggy set think there are?",
        "Keying entities by (text, type) collapses the two FinEdge mentions into one, so the missed 2nd mention vanishes and recall reads 1.0. Keyed by offsets, there are 3 gold mentions and recall is 2/3. Every mention is a separate gold entity, which is exactly the '2nd mention' FN the end-sem papers plant.",
        topic="ner-eval", level=4),
    out('# per-type counts: (tp, fp, fn)\n'
        'counts = {"PER": (90, 10, 10), "MONEY": (1, 4, 4)}\n'
        'def f1(tp, fp, fn):\n'
        '    p, r = tp / (tp + fp), tp / (tp + fn)\n'
        '    return 2 * p * r / (p + r)\n'
        'tp, fp, fn = (sum(c[i] for c in counts.values()) for i in range(3))\n'
        'micro = f1(tp, fp, fn)\n'
        'macro = sum(f1(*c) for c in counts.values()) / len(counts)\n'
        'print(round(micro, 3), round(macro, 3))',
        ["0.867 0.55", "0.55 0.867", "0.9 0.2", "0.867 0.867"], 0,
        "Micro pools counts; macro averages the per-type F1s (0.9 and 0.2).",
        "Micro: 91 TP, 14 FP, 14 FN -> 0.867, dominated by the frequent PER class. Macro: (0.9 + 0.2) / 2 = 0.55, exposing that MONEY extraction is nearly useless. For a fintech pipeline where amounts matter, reporting only micro-F1 would hide the real problem.",
        analogy="Like averaging API latency: weighted by traffic (micro) the busy endpoint dominates; per endpoint (macro) the slow rare endpoint shows up.",
        topic="ner-eval", level=4),
    fill("With 4 entity types (PER, ORG, LOC, DATE), BIO uses 9 tags (B- and I- per type, plus O). How many tags does BIOES use? ____", "17",
         "B, I, E, S for each type, plus O.",
         "4 types × 4 prefixes (B, I, E, S) + O = 17. Viterbi costs O(T × N²) for T tokens and N tags, so moving from 9 to 17 tags makes decoding about 3.6× more expensive per token, still tiny compared with the 17^T brute-force sequences it avoids.",
         topic="bio-tagging", level=4),
    mcq("'The Bank of India branch in Delhi': annotators want 'Bank of India' as ORG AND 'India' inside it as LOC. Why can't a standard BIO tagger output both?",
        ["BIO gives each token exactly one tag, so it encodes only flat, non-overlapping spans; nested entities need span-based or layered models",
         "BIO cannot represent multi-token entities",
         "BIO has no tag for locations",
         "A CRF layer forbids LOC tags after ORG tags"], 0,
        "How many tags can 'India' carry?",
        "'India' would need I-ORG and B-LOC at once. Flat sequence labelling cannot express nesting; options are span classification (score every candidate span, as many transformer IE models do), multiple tag layers, or a guideline that keeps only the outermost entity, which is what CoNLL-style datasets do.",
        topic="bio-tagging", level=4,
        diagram="""
The  Bank   of     India  branch
O    B-ORG  I-ORG  I-ORG  O      <- outer ORG
                   B-LOC         <- nested LOC: 2nd layer
"""),
    mcq("Why can a CRF use a feature like 'current word is capitalised AND previous word is Dr.' easily, when an HMM tagger cannot?",
        ["The CRF is discriminative: it conditions on the whole observed sentence, so overlapping, non-independent features are fine; the HMM must generate each word from its tag alone",
         "HMMs have no transition probabilities",
         "CRFs do not use the previous tag",
         "HMMs can only be used for POS tagging, not NER"], 0,
        "What does each model have to explain: the words, or the tags given the words?",
        "An HMM models P(words, tags) with emissions P(word | tag), so every feature must be a property of the word generated by one tag, and correlated features break its independence assumptions. A CRF models P(tags | words) directly, so any function of the input (prefixes, gazetteer hits, neighbouring words) can be a feature with its own weight.",
        topic="sequence-models", level=4),
    mcq("A BERT NER model scores 0.91 F1 on the validation set during training, but the same checkpoint scores 0.74 when the team evaluates it with a script that decodes a tag for every subword. What is the most likely cause?",
        ["Subwords after the first get their own (untrained) tags; '##gal' tagged B-LOC splits one entity into several spans, adding FPs and FNs",
         "BERT overfits more when evaluated on subwords",
         "The CRF layer is missing, which always costs 17 F1 points",
         "Validation sets always score higher than test sets"], 0,
        "During training, which subwords had labels?",
        "Training used labels only on the first subword (others -100), so predictions on continuation subwords are meaningless. Decoding them produces fragments such as [Ben]LOC [##uru]LOC, which break exact span matches. Evaluate on word-level predictions taken from the first subword.",
        topic="neural-ner", level=4),
    mcq("Bootstrapping Headquartered-In with the pattern 'Y's X' starts extracting <Prime Minister, India> from 'India's Prime Minister said...'. What is this, and which course fix addresses it?",
        ["Semantic drift from an over-general pattern; require typed arguments (X = ORG, Y = LOC) and keep only patterns and tuples with high confidence, as Snowball does",
         "Distant supervision noise; add more KB facts",
         "Label bias; switch to a CRF",
         "A temporal normalisation error; anchor to the document date"], 0,
        "Each iteration trusts the previous one's output.",
        "A loose pattern brings in wrong tuples, which create new wrong patterns on the next iteration: drift. Snowball requires X and Y to be named entities of the right types ('Prime Minister' is not an ORG) and scores each pattern's confidence so weak ones are dropped. Periodic human review of samples also helps.",
        topic="re-semi", level=4),
    out('# Snowball-style tuple confidence: 1 - product of (1 - pattern confidence)\n'
        'patterns = {"ORG \'s headquarters in LOC": 0.69, "LOC-based ORG": 0.75}\n'
        'miss = 1.0\n'
        'for conf in patterns.values():\n'
        '    miss *= 1 - conf\n'
        'print(round(1 - miss, 4))',
        ["0.9225", "0.72", "0.5175", "1.44"], 0,
        "The tuple is wrong only if every pattern that found it was wrong.",
        "1 - (0.31 × 0.25) = 1 - 0.0775 = 0.9225. A tuple found by two independent decent patterns is more trustworthy than one found by either alone. 0.5175 multiplies the confidences (both right), 0.72 averages them, 1.44 adds them.",
        topic="re-semi", level=4),
    mcq("A relation extractor's micro-F1 is 0.88, but the legal team says it is useless. Per-relation results: Located-in F1 0.93 (5,000 instances), Indemnifies F1 0.21 (60 instances). Which metric should the report lead with, and why?",
        ["Macro-F1 (or per-relation F1): it gives each relation equal weight and exposes the rare relation the legal team needs",
         "Micro-F1, because it is always the more honest metric",
         "Token accuracy, because relations are made of tokens",
         "Precision only, because recall cannot be computed for supervised RE"], 0,
        "The course: macro = equal weight per relation; micro = frequency-weighted.",
        "Micro-F1 is dominated by the 5,000 Located-in instances. Macro-F1 averages per-relation F1, so Indemnifies drags it down to about 0.57 and shows the real problem. Supervised RE has a gold set, so recall is computable; it is semi-/unsupervised RE where recall is not.",
        topic="re-supervised", level=4),
    mcq("A surface pattern 'X purchased Y' -> Acquisition(Acquirer = X, Acquired = Y) runs on 'IBM was purchased on Tuesday by Microsoft'. What goes wrong, and what representation fixes it?",
        ["The pattern doesn't match the passive (or, loosened, swaps the roles); dependency paths or semantic roles (agent of 'purchased' = Microsoft) give the right Acquirer regardless of voice",
         "Nothing goes wrong; the pattern matches and IBM is the acquirer",
         "The NER step fails because 'Tuesday' is not an entity",
         "BIO tagging cannot represent passive sentences"], 0,
        "The course's NER-vs-EE slide uses exactly these sentences.",
        "Word-order patterns encode active voice. In the passive, the object comes first and the agent sits in a 'by' phrase. Parse features (the course's dependency-path feature) or semantic role labels identify Microsoft as the agent and IBM as the theme, so Acquirer = Microsoft, Acquired = IBM, Time = Tuesday.",
        topic="events", level=4),
    mcq("A security team must extract a new 'Ransomware-Attack' event type (Attacker, Victim, Ransom, Date) starting next week, with no labelled data. In six months they expect 20,000 labelled examples. Which plan matches the course's view?",
        ["Start with LLM-based extraction, supplying the schema in the prompt with structured (JSON / constrained) output; once labels exist, train a supervised extractor, which still leads in-domain",
         "Wait six months, since nothing can be done without labels",
         "Use the supervised model trained for Merge-Org events unchanged",
         "Use Open IE and rename its relation phrases"], 0,
        "'Supervised models still lead in-domain; LLMs win on new schemas.'",
        "With generative / LLM extraction the schema moves into the prompt, so a new event type needs no architectural change. JSON schemas, tool calling and constrained decoding keep records well-formed, and retrieval-augmented prompting helps argument roles on new domains. With enough labels, a fine-tuned model is usually more accurate and cheaper per document.",
        topic="events", level=4),
    mcq("'Regulators approved the deal on 2 March; the merger was announced on 20 March and will close by June.' Which TimeML-style temporal relations (TLINKs) are right?",
        ["approval BEFORE announcement; announcement BEFORE closing; closing is anchored by the relative deadline 'by June'",
         "announcement BEFORE approval; closing SIMULTANEOUS with announcement",
         "approval AFTER announcement; closing BEFORE approval",
         "No temporal relation can be extracted without exact times of day"], 0,
        "Order events on a timeline using the dates and tense.",
        "Temporal relation extraction links events and times with relations such as BEFORE, AFTER, INCLUDES, SIMULTANEOUS (Allen-style interval relations in TimeML TLINKs). 2 March < 20 March gives approval BEFORE announcement; 'will close by June' places closing after the announcement, bounded by June. Such links let a system answer 'what happened before the merger was announced?'.",
        topic="temporal", level=4,
        diagram="""
2 Mar          20 Mar               June
  |--approved----|--announced--------|--closes (by)
  approval BEFORE announcement BEFORE closing
"""),
    mcq("An archive of 2019 news articles is re-processed in 2027. The normaliser maps 'next Monday' in every article to a date in 2027. What is the bug?",
        ["Relative expressions were anchored to the processing date instead of each article's document creation time (DCT)",
         "'next Monday' is absolute and should not be normalised",
         "The recogniser should have tagged 'next Monday' as a DURATION",
         "TIMEX3 cannot store dates before 2020"], 0,
        "A reference point is needed; which one?",
        "Relative expressions 'map to particular times through some other reference point'. For news that point is the article's publication date (the DCT in TimeML), or sometimes a time mentioned earlier in the text. Using 'now' is a classic production bug when IE jobs are re-run on old data.",
        topic="temporal", level=4,
        analogy="Like resolving a relative URL against the wrong base URL: the path is fine, but every link points into the wrong site."),
    mcq("OneIE learns global features with weights, e.g. 'A Transport event has only one Destination argument' (+2.61) and 'An event has two Place arguments' (-2.47). Why do these help over a pipeline?",
        ["They score the whole information graph, so beam-search decoding prefers globally consistent graphs and can reject locally likely but jointly impossible combinations",
         "They replace the CRF taggers for entity mentions",
         "They make the model run faster than a pipeline",
         "They are hand-written rules that the model cannot change"], 0,
        "Cross-subtask and cross-instance interactions.",
        "A pipeline decides each argument independently, so it can assign two Places to one event. OneIE adds learned global feature scores to the local scores and uses beam search to find the graph with the highest global score. The features are explainable because each has a readable meaning and a learned weight.",
        topic="ie-overview", level=4),
    mcq("Applying 'X and other Y' to '...temples, treasuries, and other important civic buildings' should yield which IS-A pairs, and what is the pitfall?",
        ["temple IS-A building and treasury IS-A building; the pitfall is taking the whole phrase 'important civic buildings' (or only the last X) instead of NP heads over the full list",
         "buildings IS-A temple; Hearst patterns run right to left",
         "Only 'treasuries IS-A important'; Hearst patterns match single words",
         "No pair; 'and other' is not a Hearst pattern"], 0,
        "Y is the noun phrase after 'other'; X can be a list.",
        "'X and other Y' says each listed X is a kind of Y. Good extractors chunk noun phrases, take heads ('buildings', lemmatised to 'building'), and expand the coordinated list so both temples and treasuries are kept. Without NP chunking, a regex often grabs one word too many or too few.",
        topic="re-patterns", level=4),
    mcq("In an exam excerpt, a system outputs 'CEO (PERSON)' and 'Reserve Bank of India (LOCATION)'. How should each be scored under exact match, and why?",
        ["'CEO' is a spurious FP (a job title is not a named entity); 'Reserve Bank of India' as LOCATION is an FP and the gold ORG is an FN",
         "Both are TPs because the strings appear in the text",
         "'CEO' is an FN; 'Reserve Bank of India' is a TP with a type warning",
         "'CEO' is ignored; 'Reserve Bank of India' is half a TP"], 0,
        "Spurious vs wrong type.",
        "Titles such as CEO or Founder are not proper names, so there is no gold entity to match: one FP. The RBI is an organisation; tagging it LOCATION (a metonymy-style confusion with 'India') gives an FP for the prediction and leaves the gold ORG unmatched, an FN. Each wrong-type error therefore costs both precision and recall.",
        topic="ner-basics", level=4),
    tf("Adding more hand-written NER rules to a mature rule-based system usually raises recall without any effect on precision.", False,
       "Rules interact.",
       "New rules catch new cases but also fire on text they weren't meant for, and they start conflicting with older rules (which one wins?). Mature rule sets become hard to maintain; teams then use the rules to auto-label data and train a statistical model, keeping rules only for high-precision formats.",
       topic="ner-rules", level=4),
    mcq("An exam asks why the course's Google / YouTube / 2006 example (YouTube tagged PRODUCT instead of ORG) gives F1 = 0.667. Which accounting is right?",
        ["TP 2 (Google, 2006), FP 1 (YouTube: PRODUCT), FN 1 (YouTube: ORG): P = R = 2/3, F1 = 0.667",
         "TP 2, FP 1, FN 0: P = 0.667, R = 1.0, F1 = 0.8",
         "TP 3, FP 0, FN 0 with a type warning: F1 = 1.0",
         "TP 2, FP 0, FN 1: P = 1.0, R = 0.667, F1 = 0.8"], 0,
        "One type mismatch is one full error on each side.",
        "The span 'YouTube' is right but the type is wrong, so under strict span match it counts as an FP and the gold ORG becomes an FN. P = 2/3, R = 2/3, F1 = 0.667. Counting it only on one side gives 0.8, the tempting wrong answer.",
        topic="ner-eval", level=4),
    # ------------------------------------------------------------------ more L2/L3
    out('toks = "book a cab for Priya Kapoor to Pune Airport on 15th June at 2:00 pm".split()\n'
        'slots = {"NAME": (4, 6), "DEST": (7, 9), "DATE": (10, 12), "TIME": (13, 15)}\n'
        'tags = ["O"] * len(toks)\n'
        'for name, (s, e) in slots.items():\n'
        '    tags[s] = "B-" + name\n'
        '    for i in range(s + 1, e):\n'
        '        tags[i] = "I-" + name\n'
        'print(len(toks), [sum(t.startswith(p) for t in tags) for p in "BIO"])',
        ["15 [4, 4, 7]", "15 [4, 8, 3]", "15 [8, 0, 7]", "14 [4, 4, 6]"], 0,
        "Each slot is two tokens: one B-, one I-.",
        "15 tokens; four two-token slots give 4 B- tags and 4 I- tags; the remaining 7 tokens are O. Slot filling in conversational AI uses the same BIO scheme as NER, and the Dec 2025 midsem asks for exactly this kind of tag count.",
        topic="bio-tagging", level=2,
        diagram="""
book a cab for Priya  Kapoor to Pune   Airport ...
O    O O   O   B-NAME I-NAME O  B-DEST I-DEST  ...
"""),
    out('toks = ("American Airlines , a unit of AMR , immediately matched "\n'
        '        "the move , spokesman Tim Wagner said").split()\n'
        'm1, m2 = (0, 2), (14, 16)          # [start, end) token spans\n'
        'between = [w for w in toks[m1[1]:m2[0]] if w != ","]\n'
        'head = lambda s: toks[s[1] - 1]\n'
        'print(head(m1) + "-" + head(m2), len(between), toks[m2[0] - 1], toks[m2[1]])',
        ["Airlines-Wagner 9 spokesman said",
         "American-Tim 9 spokesman said",
         "Airlines-Wagner 12 spokesman said",
         "Airlines-Wagner 9 Tim said"], 0,
        "The headword of an English name is usually its last token.",
        "These are the course's word features for this sentence: headwords Airlines-Wagner, the 9 words between the mentions {a, unit, of, AMR, immediately, matched, the, move, spokesman}, and M2's neighbours -1 'spokesman' and +1 'said'. A supervised RE classifier gets them as features.",
        topic="re-supervised", level=2),
    fill("In the course's mention-level features, the entity level of 'the company' is ____ (NAME, NOMINAL or PRONOUN).", "NOMINAL",
         "It is a common noun phrase, not a name or a pronoun.",
         "'American Airlines' is NAME, 'the company' is NOMINAL, 'it' is PRONOUN. Relations expressed through nominal or pronoun mentions need coreference to connect them back to the named entity.",
         topic="re-supervised", level=2),
    out('import re\n'
        'def kind(e):\n'
        '    if re.match(r"(next|last|this|within|by)\\b", e) or e.endswith("ago"):\n'
        '        return "REL"\n'
        '    if re.search(r"\\b(days?|weeks?|months?|years?)$", e):\n'
        '        return "DUR"\n'
        '    return "ABS" if re.search(r"\\d{4}", e) else "?"\n'
        'exprs = ["5 January 2026", "six weeks", "next Monday", "within three weeks", "2018"]\n'
        'print([kind(e) for e in exprs])',
        ["['ABS', 'DUR', 'REL', 'REL', 'ABS']",
         "['ABS', 'DUR', 'REL', 'DUR', 'ABS']",
         "['ABS', 'DUR', 'REL', 'REL', '?']",
         "['ABS', 'REL', 'REL', 'REL', 'ABS']"], 0,
        "Rule order matters: the relative check runs first.",
        "'within three weeks' ends in 'weeks' but the REL rule fires first because it starts with 'within', matching how the course's papers classify it (a deadline anchored to the document date). '2018' contains four digits, so ABS. Swapping the rule order would make it DUR: rule cascades are order-sensitive.",
        topic="temporal", level=3),
    tf("Under the IO scheme (only I-X and O tags, no B-), two adjacent entities of the same type, such as two company names listed with no separator, can't be told apart from one long entity.", True,
       "What marks where one entity ends and the next begins?",
       "'I-ORG I-ORG I-ORG I-ORG' decodes to one span. BIO's B- tag marks the start of the second entity, 'B-ORG I-ORG B-ORG I-ORG', which is exactly why the course's exam rule says every mention begins with B-.",
       topic="bio-tagging", level=3,
       analogy="Like a CSV file without delimiters: the fields are all there, but you can't tell where one ends and the next starts."),
    fill("Hearst's 1992 paper was titled 'Automatic Acquisition of ____ from Large Text Corpora' (one word, plural).", "Hyponyms",
         "The 'kind of' words below a category.",
         "Hyponyms are the more specific terms (Gelidium is a hyponym of red algae); hypernyms are the more general ones. Hearst patterns find hyponym-hypernym (IS-A) pairs with high precision.",
         topic="re-patterns", level=1),
]
