from helpers import mcq, tf, out, fill

SUBJECT = "nlpa-mt"

TOPICS = [
    ("mt-hard", "The MT problem and why it is hard"),
    ("rbmt", "Rule-based MT, transfer and interlingua (Vauquois triangle)"),
    ("smt-noisy", "Statistical MT and the noisy channel"),
    ("ibm-em", "Word alignment, IBM models and EM"),
    ("phrase-decode", "Phrase-based SMT, decoding and beam search"),
    ("nmt", "Neural MT: encoder-decoder, attention, Transformer"),
    ("subword-data", "Subword vocabularies, back-translation and multilingual models"),
    ("bleu-mt", "BLEU by hand (multi-reference, brevity penalty)"),
    ("mt-eval", "Human and neural MT evaluation (adequacy, fluency, chrF, TER, COMET)"),
    ("indic-mt", "Indic-language MT"),
    ("mt-risks", "MT failure modes, bias and deployment"),
]

QUESTIONS = [
    # ------------------------------------------------------------------ L1
    mcq("The course names one core trade-off every MT system has to balance. What is it?",
        ["Adequacy (faithful meaning) vs fluency (natural target text)",
         "Speed vs memory",
         "Precision vs recall of named entities",
         "Vocabulary size vs sentence length"], 0,
        "One side looks at the source, the other at the output alone.",
        "Adequacy (also called fidelity or faithfulness) asks 'is the meaning of the source preserved?'. Fluency asks 'does it read like natural target language?'. A word-by-word gloss can be adequate but clumsy; a smooth sentence can be fluent but wrong. The course writes the goal as Tbest = argmax faithfulness(T, S) x fluency(T).",
        topic="mt-hard", level=1,
        analogy="Like a code port from Java to Python: it must behave the same (adequacy) and also look like idiomatic Python, not Java written in Python syntax (fluency)."),
    mcq("English is SVO ('Ravi reads books'). Hindi is SOV ('Ravi kitaabein padhta hai'). What does this mean for a translator?",
        ["The verb has to move from the middle of the sentence to the end",
         "Hindi has no verbs, so they are dropped",
         "The words can be translated one by one in the same order",
         "Only the subject needs to change position"], 0,
        "S = subject, V = verb, O = object. Compare the positions of V.",
        "SVO puts the verb between subject and object; SOV puts it last. A word-for-word system that keeps English order produces 'Ravi padhta hai kitaabein', which is wrong. The course adds that SVO languages tend to use prepositions ('in the house') and SOV languages postpositions ('ghar mein').",
        topic="mt-hard", level=1,
        diagram="""
English (SVO):  Ravi   reads        books
                 S       V            O
Hindi   (SOV):  Ravi   kitaabein    padhta hai
                 S       O            V
"""),
    tf("A 'pro-drop' language is one where the subject pronoun is often left out, so the translator must infer it from context.", True,
       "Pro = pronoun.",
       "The course's example: 'Did you give the food to Nadya?' answered with just 'gave' in a pro-drop language means '(I) gave (her the food)'. Translating into English, which requires a subject, means guessing 'I' from the conversation. Japanese, Hindi and Spanish all drop subjects regularly.",
       topic="mt-hard", level=1),
    mcq("Which system is the course's example of rule-based MT (RBMT)?",
        ["SYSTRAN (1968), used for Cold War Russian-English documents",
         "Google Neural Machine Translation (2016)",
         "Meta's NLLB-200 (2022)",
         "IndicTrans2 (2023)"], 0,
        "The oldest system in the list.",
        "RBMT translates with hand-written bilingual dictionaries, morphological analysers and transfer rules. SYSTRAN is the classic example; it later powered AltaVista's Babel Fish. The other three are neural systems learnt from data.",
        topic="rbmt", level=1),
    fill("In the Vauquois triangle, the apex, where the source is analysed into a language-independent meaning representation, is called the ____.", "interlingua",
         "Latin-flavoured: 'between languages'.",
         "The triangle goes from direct translation (words to words) at the bottom, through syntactic and semantic transfer, to the interlingua at the top. At the apex there is no transfer step at all: analyse into meaning, then generate the target from it.",
         topic="rbmt", level=1),
    mcq("What does a statistical MT (SMT) system learn its translation knowledge from?",
        ["A parallel corpus (bitext): the same sentences in two languages",
         "Hand-written grammar rules from linguists",
         "A bilingual dictionary only",
         "Monolingual text in the target language only"], 0,
        "The course's example is the Canadian Hansards.",
        "SMT replaced hand-coded rules with probabilities estimated from bitext, e.g. the Canadian parliamentary proceedings published in French and English. The sentences are first paired up (sentence alignment, using cues like length), then word alignments are learnt. Monolingual text is used too, but only for the language model.",
        topic="smt-noisy", level=1),
    mcq("In the noisy-channel formula for SMT, ê = argmax P(f | e) P(e), what job does P(e) do?",
        ["It is the language model: it scores how fluent the target sentence e is",
         "It is the translation model: it scores how faithful e is to f",
         "It is the probability of the foreign sentence",
         "It is the alignment between e and f"], 0,
        "It mentions only the output sentence.",
        "P(e) looks at the English candidate alone, so it can only judge whether it is good English: the language model (fluency), trained on monolingual text. P(f | e) is the translation model (fidelity), trained on parallel text.",
        diagram="""
 e (English) --> [ noisy channel P(f|e) ] --> f (French)
                                              |
 decoder: e^ = argmax  P(f|e)  x  P(e)  <-----+
                       TM         LM
                    (fidelity) (fluency)
""",
        topic="smt-noisy", level=1),
    mcq("What is a word alignment in SMT?",
        ["The mapping that says which source word produced each target word in a sentence pair",
         "Sorting the words of a sentence alphabetically",
         "Matching each sentence of a document to its translation",
         "Padding sentences to the same length"], 0,
        "Think of lines drawn between the words of two sentences.",
        "For 'green house / casa verde' the alignment links green-verde and house-casa. It is never written in the data, so the IBM models treat it as a hidden (latent) variable and learn it with EM. Sentence alignment, the third option, is the earlier step that pairs whole sentences.",
        topic="ibm-em", level=1,
        diagram="""
  green    house
      \\    /
       \\  /
        \\/
        /\\
       /  \\
   casa    verde
"""),
    tf("In the IBM models, a target word that has no counterpart in the source sentence can be aligned to a special NULL word at position 0.", True,
       "Some words have no partner.",
       "Function words such as 'do' in 'I do not know' or a Spanish article often have no source partner. NULL gives them somewhere to go, so EM does not have to force them onto a random content word.",
       topic="ibm-em", level=1),
    fill("Neural MT models are built from two halves: an ____ that reads the source sentence into vectors and a decoder that writes the target sentence word by word.", "encoder",
         "It encodes.",
         "The encoder turns 'Le chat dort' into contextual vectors; the decoder generates 'The cat sleeps' one token at a time, each step conditioned on the encoder output and the tokens it already produced.",
         topic="nmt", level=1),
    mcq("Which paper introduced attention for neural MT, letting the decoder 'look back' at the source words at every step?",
        ["Bahdanau et al. (2014/2015)",
         "Brown et al. (1993)",
         "Vaswani et al. (2017)",
         "Papineni et al. (2002)"], 0,
        "Brown is the IBM models, Papineni is BLEU.",
        "Bahdanau, Cho and Bengio added attention to the RNN encoder-decoder. Brown et al. wrote the IBM alignment models, Vaswani et al. the Transformer ('Attention Is All You Need'), Papineni et al. BLEU. Expect the course to mix these names in an MCQ.",
        topic="nmt", level=1),
    mcq("Why do modern MT systems split rare words into subword pieces (BPE) instead of using a fixed word vocabulary?",
        ["So that unseen or rare words can still be built from known pieces instead of becoming <unk>",
         "So that sentences become shorter",
         "Because GPUs cannot store whole words",
         "To remove punctuation"], 0,
        "What happens to a word that was never in the training vocabulary?",
        "With a word vocabulary, 'unbookable' or a new place name becomes the out-of-vocabulary token <unk> and is lost. Byte Pair Encoding builds a vocabulary of frequent pieces ('un', 'book', 'able'), so any word can be spelled out. This matters most for morphologically rich languages like Tamil or Finnish.",
        topic="subword-data", level=1,
        analogy="Like a Lego set: you don't need a special brick for every model, you combine standard bricks."),
    tf("BLEU scores a machine translation by comparing its n-grams with one or more human reference translations.", True,
       "BLEU = Bilingual Evaluation Understudy.",
       "BLEU is an 'understudy' for a human judge: the closer the candidate's n-grams are to professional translations, the higher the score. It needs references; it never looks at the source sentence.",
       topic="bleu-mt", level=1),
    fill("In BLEU, the human translation the output is compared against is called the reference; the machine output is called the ____.", "candidate",
         "The course writes C for it.",
         "The course's examples label references R1, R2, R3 and the machine output C (candidate). Every count in BLEU is taken over the candidate's n-grams.",
         topic="bleu-mt", level=1),
    mcq("A human judge reads only the machine output (no source) and rates 'is this grammatical, readable target-language text?'. Which dimension is being judged?",
        ["Fluency",
         "Adequacy",
         "Informativeness",
         "Fidelity"], 0,
        "Without the source you cannot judge meaning.",
        "Fluency needs only the output. Adequacy/fidelity asks whether the meaning matches the source, so it needs either the source (bilingual judge) or a reference (monolingual judge). Informativeness is the task-based check: can a reader answer questions about the source from the translation?",
        topic="mt-eval", level=1),
    mcq("The course describes chrF as a 'character-level F-score'. For which languages does it say this metric works especially well?",
        ["Morphologically rich languages, where one word carries many suffixes",
         "Languages with no written script",
         "Only English",
         "Languages that use the Latin alphabet only"], 0,
        "A wrong suffix should not cost the whole word.",
        "In Hindi, Tamil or Finnish a word like 'ladkiyon' vs 'ladkiyan' differs only in a suffix. Word-level BLEU counts that as a total miss; character n-grams give partial credit for the shared stem.",
        topic="mt-eval", level=1),
    fill("The Eighth Schedule of the Indian Constitution lists ____ languages, the coverage target of IndicTrans2 and Bhashini (answer as a number).", "22",
         "The course slide says 'NLP for ... constitutional languages'.",
         "India has 22 scheduled languages written in more than a dozen scripts. IndicTrans2 was the first open model to cover all 22. Eleven was the count in the earlier parallel-corpus collection effort, and 200 is NLLB's coverage.",
         topic="indic-mt", level=1),
    tf("Many Indian languages are low-resource: they have far less parallel text available than pairs like English-French.", True,
       "Compare the Hansards with, say, Santali.",
       "Low-resource pairs are one of the course's listed MT challenges. Hindi is relatively well served; Kashmiri, Manipuri, Sindhi or Santali have very little parallel data, which is why the course stresses mining, back-translation, transfer from related languages and script unification.",
       topic="indic-mt", level=1),
    mcq("A product listing says 'Ships in 3 days from Pune, Rs 1,499'. An MT system outputs 'Ships in a few days from Mumbai, Rs 1,500'. Which challenge from the course has it failed?",
        ["Named entities and numbers must be preserved exactly",
         "Pro-drop",
         "Lexical gaps",
         "Word-order divergence"], 0,
        "The sentence is fluent; look at what changed.",
        "The course lists 'Named Entities & Numbers: proper nouns, dates and units must be preserved exactly, not creatively translated'. The output is fluent, so a fluency check would pass it; this is why production systems add placeholder/copy mechanisms and entity checks for prices and places.",
        topic="mt-risks", level=1),
    fill("When a fluent translation states something that is not in the source at all, this failure (a new risk the course flags for LLM-based MT) is called ____.", "hallucination",
         "Same word as for LLM chatbots.",
         "The course: LLM translation is strong on fluency, context and idioms, but 'new risk: hallucination, fluent output that is unfaithful to the source'. Fluency hides it, so it needs adequacy checks.",
         topic="mt-risks", level=1),
    mcq("According to the course's history slide, which order did MT approaches follow?",
        ["Rule-based -> statistical -> neural seq2seq with attention -> Transformer -> LLM-based",
         "Statistical -> rule-based -> Transformer -> neural seq2seq -> LLM-based",
         "Neural -> statistical -> rule-based",
         "Transformer -> rule-based -> statistical -> LLM-based"], 0,
        "Rules first, data later.",
        "1950s-80s RBMT, 1990s-2010s SMT, 2014-2017 seq2seq + attention, 2017-2020 Transformer, 2020 onwards LLM-based MT. Google Translate itself moved from phrase-based SMT (2006) to GNMT (2016).",
        topic="mt-hard", level=1),
    mcq("In the course's 'decoding' slides, what does beam search keep at each step?",
        ["The k best partial translations so far (k = beam size)",
         "Only the single best next word",
         "Every possible partial translation",
         "Only the translations that end with a full stop"], 0,
        "Somewhere between greedy and exhaustive.",
        "Greedy decoding keeps 1 hypothesis; exhaustive search keeps all (impossible: vocabulary^length). Beam search keeps the top k, extends each with candidate next words, and prunes back to k. k = 4 to 10 is typical in NMT.",
        topic="phrase-decode", level=1),

    # ------------------------------------------------------------------ L2
    mcq("'John plays the guitar' -> 'John toca la guitarra', but 'John plays soccer' -> 'John juega el fútbol'. Which MT difficulty does the course use this pair to show?",
        ["Ambiguity: the right translation of 'plays' depends on its object",
         "Pro-drop",
         "A lexical gap: Spanish has no word for 'plays'",
         "SOV word order"], 0,
        "Spanish has words for both senses; the problem is choosing.",
        "'Play' an instrument is tocar, 'play' a sport is jugar. Spanish has both words, so it is not a lexical gap; the system must resolve the sense from context (word-sense disambiguation). The course puts it under 'ambiguity resolution is required for translation'.",
        topic="mt-hard", level=2),
    mcq("French distinguishes 'rivière' (a river flowing into another river) from 'fleuve' (a river flowing into the sea). English has only 'river'. What kind of problem does this create?",
        ["A lexical gap: one language makes a distinction the other has no single word for",
         "A word-order divergence",
         "A pro-drop problem",
         "A named-entity problem"], 0,
        "The course also lists Schadenfreude.",
        "Lexical gaps: some words have no corresponding term in the other language (Schadenfreude in German, oyakoko 'filial piety' in Japanese). English -> French must pick rivière or fleuve using knowledge that is not in the English word, so information has to be added. (The slide swaps the two definitions; in French usage the fleuve is the one that reaches the sea.)",
        topic="mt-hard", level=2),
    mcq("Translating 'I saw the movie and it is good' into German, why must 'it' become the masculine pronoun 'er'?",
        ["'it' refers to the movie, the German word Film is masculine, so the pronoun must agree with Film",
         "German pronouns are always masculine",
         "Because the subject 'I' is masculine",
         "'it' is dropped in German, so 'er' is a placeholder"], 0,
        "Follow the chain: it -> movie -> Film -> gender.",
        "Pronominal anaphora: the system must resolve 'it' to 'movie', translate 'movie' to 'Film', look up Film's grammatical gender (masculine) and only then choose 'er'. A sentence-by-sentence system that loses the antecedent picks the wrong pronoun, which is why the course lists discourse and context as an open challenge.",
        topic="mt-hard", level=2),
    mcq("In the course's Vauquois triangle, what is the main difference between moving UP one level (syntactic -> semantic) and staying at the bottom (direct translation)?",
        ["More source analysis, less (simpler) transfer: the higher you go, the smaller the gap between the two languages' representations",
         "More transfer rules are needed at the top than at the bottom",
         "Higher levels need no target-language generation",
         "Higher levels only work for related languages"], 0,
        "The two sides of the triangle get closer as you climb.",
        "Width of the triangle = how different the two representations are. Words differ a lot (wide gap, many direct rules); semantic structures differ less; at the apex the interlingua is shared, so transfer disappears. The cost moves into deeper analysis (parsing, SRL, WSD) and generation.",
        topic="rbmt", level=2,
        diagram="""
               Interlingua
              /           \\
      Semantic --transfer-- Semantic
          /                     \\
   Syntactic ----transfer---- Syntactic
        /                         \\
   Words ------- direct -------- Words
  Source                          Target
"""),
    fill("In the course's direct-transfer example, '... a la verde bruja' becomes '... a la bruja verde'. This step of direct transfer is called lexical ____.", "reordering",
         "Only the order of two words changed.",
         "The four steps: morphological analysis (didn't -> DO:PAST not), lexical transfer (word-for-word into Spanish with features), lexical reordering (adjective after noun: verde bruja -> bruja verde), morphological generation (dar:PAST -> dio).",
         topic="rbmt", level=2,
         diagram="""
Mary didn't slap the green witch
  | morphological analysis
Mary DO:PAST not slap the green witch
  | lexical transfer
Maria no dar:PAST una bofetada a la verde bruja
  | lexical reordering
Maria no dar:PAST una bofetada a la bruja verde
  | morphological generation
Maria no dio una bofetada a la bruja verde
"""),
    tf("In the noisy-channel model, P(f) can be dropped from argmax_e P(f | e) P(e) / P(f) because the foreign sentence f is fixed for the whole search.", True,
       "What varies across the candidates?",
       "The decoder compares many English candidates e for one input f. P(f) is the same number for every candidate, so dividing by it does not change which e wins. Same trick as in the spelling-correction noisy channel from session 2.",
       topic="smt-noisy", level=2),
    out("cands = {\"the house is small\": (0.020, 0.0010),\n"
        "         \"the house is little\": (0.030, 0.0002),\n"
        "         \"small is the house\": (0.025, 0.00005)}\n"
        "# value = (P(f|e) translation model, P(e) language model)\n"
        "best_tm = max(cands, key=lambda e: cands[e][0])\n"
        "best = max(cands, key=lambda e: cands[e][0] * cands[e][1])\n"
        "print(best_tm)\n"
        "print(best)",
        ["the house is little\nthe house is small",
         "the house is little\nthe house is little",
         "the house is small\nthe house is small",
         "small is the house\nthe house is small"], 0,
        "Multiply the two columns before choosing.",
        "TM alone prefers 'little' (0.030). Products: small 0.020 x 0.0010 = 2.0e-5, little 0.030 x 0.0002 = 6.0e-6, 'small is the house' 1.25e-6. The LM knows 'the house is small' is far more natural English, and it wins. This is the course's TM-for-fidelity, LM-for-fluency split.",
        topic="smt-noisy", level=2),
    mcq("The course says the SMT translation model is 'learnt from parallel data' and the language model is 'learnt from monolingual data'. Why is that split useful in practice?",
        ["Monolingual target text is far more plentiful than bitext, so fluency can be learnt from much more data",
         "Parallel data cannot be used to train n-gram models",
         "Monolingual data contains the alignments",
         "It halves the training time"], 0,
        "Compare how much English web text exists with how much English-Hindi bitext.",
        "Terabytes of web English trained 5-gram LMs; bitext is scarcer and expensive. Splitting the model lets the scarce resource handle only fidelity and the abundant one handle fluency. NMT later recovered this advantage through back-translation.",
        analogy='Like a code reviewer and a linter: the reviewer (TM) checks the change does what the ticket says, the linter (LM) checks it reads like house style. The linter can be trained on every repo you own.',
        topic="smt-noisy", level=2),
    fill("IBM Model 3 adds ____ n(phi | e): how many target words one source word produces, e.g. 'slap' -> 'dar una bofetada'.", "fertility",
         "1 = lexical, 2 = absolute position, 3 = ?",
         "Model 1: lexical translation t(f | e) with uniform alignment. Model 2: absolute alignment a(i | j, l, m). Model 3: fertility n(phi | e). Model 4: relative distortion. Model 5: fixes deficiency (no probability wasted on impossible, overlapping positions).",
         topic="ibm-em", level=2,
         diagram="""
Model 1  t(f|e)          lexical, uniform alignment
Model 2  + a(i|j,l,m)    absolute position
Model 3  + n(phi|e)      fertility
Model 4  + distortion    relative reordering
Model 5  non-deficient   only valid positions
"""),
    out("from fractions import Fraction as F\n"
        "E = [\"small\", \"cat\"]; Fs = [\"katze\", \"klein\"]\n"
        "t = {(f, e): F(1, 2) for f in Fs for e in E}   # uniform start\n"
        "for f in Fs:                                    # IBM Model 1 E-step\n"
        "    z = sum(t[(f, e)] for e in E)\n"
        "    print(f, [str(t[(f, e)] / z) for e in E])",
        ["katze ['1/2', '1/2']\nklein ['1/2', '1/2']",
         "katze ['1', '0']\nklein ['0', '1']",
         "katze ['0', '1']\nklein ['1', '0']",
         "katze ['1/4', '1/4']\nklein ['1/4', '1/4']"], 0,
        "Posterior = t(f | e) divided by the sum over the source words.",
        "P(a_j = i | e, f) = t(f_j | e_i) / sum_i' t(f_j | e_i') = 0.5 / (0.5 + 0.5) = 1/2 for every cell. With one symmetric sentence and a uniform start, EM has no evidence to prefer katze-cat over katze-small. This is the end-sem's E-step answer; the tempting '1 and 0' is the alignment you know is right, not what EM computes.",
        topic="ibm-em", level=2),
    mcq("Why did phrase-based SMT replace word-based (IBM-model) translation in production systems like the 2006 Google Translate?",
        ["Translating multi-word chunks captures local reordering, idioms and one-to-many mappings that word-by-word models get wrong",
         "Phrases need no parallel data",
         "Phrase-based systems do not need a language model",
         "Word-based models cannot be trained with EM"], 0,
        "Think of 'dió una bofetada' for 'slapped'.",
        "A phrase table stores pairs such as 'bruja verde' <-> 'green witch' or 'dió una bofetada' <-> 'slapped', learnt from word alignments. Reordering inside the phrase and many-to-many mappings come for free. A language model and a reordering model are still combined with it, and a beam decoder searches.",
        topic="phrase-decode", level=2),
    tf("Greedy decoding (always pick the single most probable next word) is guaranteed to find the most probable whole translation.", False,
       "A good first word can lead to a bad sentence.",
       "The best first word can force poor continuations, so the product of probabilities ends lower than a path that started with the second-best word. Beam search keeps several hypotheses to reduce such search errors; it still does not guarantee the optimum.",
       analogy='Like choosing the fastest-looking road at every junction: you can end up in a jam that a slightly slower first turn would have avoided.',
       topic="phrase-decode", level=2),
    mcq("The course's 'Issues with encoder-decoder' slide says performance 'deteriorates rapidly as input length increases'. What causes this?",
        ["The encoder must squeeze the whole source sentence into one fixed-length vector",
         "The decoder vocabulary is too small",
         "RNNs cannot process more than 10 words",
         "Long sentences have more rare words"], 0,
        "The bottleneck.",
        "A 50-word sentence and a 5-word sentence get the same size context vector, so details of long sentences are lost. Attention fixes it by giving the decoder access to every encoder hidden state at every step.",
        topic="nmt", level=2,
        diagram="""
 x1 .. x50 -> [ENCODER] -> c -> [DECODER] -> y1 .. yn
                            ^
            one fixed-length vector = bottleneck
"""),
    mcq("The course calls Bahdanau attention weights a 'soft alignment'. What does that mean?",
        ["Each target word gets a probability distribution over all source words instead of one hard link",
         "Attention aligns sentences, not words",
         "The alignment is learnt with EM like IBM Model 1",
         "Attention only links words with the same spelling"], 0,
        "Hard = one link. Soft = weights summing to 1.",
        "IBM alignments are hard: f_j comes from exactly one e_i. Attention gives, at each decoder step, weights over all encoder states (e.g. 0.73 / 0.16 / 0.11), learnt end to end by backprop rather than EM. Plotting them as a matrix looks like an alignment grid.",
        diagram="""
            Le    chat   dort     (source)
 The       0.85   0.10   0.05
 cat       0.08   0.88   0.04
 sleeps    0.03   0.07   0.90
 (target)  each row sums to 1 = soft alignment
""",
        topic="nmt", level=2),
    out("import numpy as np\n"
        "scores = np.array([2.0, 0.5, 0.1])   # decoder state vs 3 source words\n"
        "w = np.exp(scores) / np.exp(scores).sum()\n"
        "print(w.round(2).tolist(), int(w.argmax()))",
        ["[0.73, 0.16, 0.11] 0",
         "[0.77, 0.19, 0.04] 0",
         "[0.2, 0.5, 0.3] 1",
         "[2.0, 0.5, 0.1] 0"], 0,
        "Softmax: exponentiate, then divide by the sum.",
        "e^2 = 7.39, e^0.5 = 1.65, e^0.1 = 1.11; sum 10.15. Weights 0.73, 0.16, 0.11. The context vector is 0.73 h1 + 0.16 h2 + 0.11 h3, and the argmax (source word 0) is what you would draw as the alignment link. [0.77, 0.19, 0.04] is the scores divided by their sum, not softmax.",
        topic="nmt", level=2),
    out("from collections import Counter\n"
        "words = {\"l o w\": 5, \"l o w e r\": 2, \"n e w e r\": 6, \"w i d e r\": 3}\n"
        "pairs = Counter()\n"
        "for w, f in words.items():\n"
        "    s = w.split()\n"
        "    for a, b in zip(s, s[1:]):\n"
        "        pairs[(a, b)] += f\n"
        "print(pairs.most_common(2))",
        ["[(('e', 'r'), 11), (('w', 'e'), 8)]",
         "[(('l', 'o'), 7), (('o', 'w'), 7)]",
         "[(('e', 'r'), 3), (('w', 'e'), 2)]",
         "[(('n', 'e'), 6), (('e', 'w'), 6)]"], 0,
        "Each pair counts once per word occurrence, weighted by word frequency.",
        "BPE's first step counts adjacent symbol pairs weighted by word frequency: 'e r' appears in lower (2), newer (6), wider (3) = 11; 'w e' in lower (2) and newer (6) = 8. BPE merges 'e r' -> 'er' first, then recounts. Counting each word once (the third option) ignores frequency.",
        topic="subword-data", level=2),
    mcq("What does back-translation do to create extra training data for an English -> Hindi system?",
        ["Translate monolingual HINDI text into English with a reverse model, then train on (synthetic English, real Hindi) pairs",
         "Translate monolingual ENGLISH text into Hindi, then train on (real English, synthetic Hindi) pairs",
         "Translate the test set back and forth until it stops changing",
         "Ask human translators to check the output in reverse"], 0,
        "Which side should be real, human-written text?",
        "The decoder learns to write whatever is on the target side, so that side must be real fluent Hindi. Noisy synthetic English on the source side does little harm. NLLB used this to cover low-resource languages. Putting synthetic Hindi on the target side teaches the model to copy its own mistakes.",
        diagram="""
 real Hindi (mono) --[hi->en model]--> synthetic English
                                            |
 train en->hi on (synthetic English, real Hindi)
""",
        analogy='Like generating test inputs from known-good expected outputs: the expected side must be trustworthy; the inputs can be a bit synthetic.',
        topic="subword-data", level=2),
    out("from collections import Counter\n"
        "cand = \"train train leaves at at noon\".split()\n"
        "refs = [\"the train leaves at noon\".split(),\n"
        "        \"the train departs at twelve noon\".split()]\n"
        "c = Counter(cand)\n"
        "clip = sum(min(n, max(Counter(r)[w] for r in refs)) for w, n in c.items())\n"
        "print(clip, len(cand))",
        ["4 6", "6 6", "5 6", "4 11"], 0,
        "Each word is capped at its count in the single reference where it appears most.",
        "train: 2 in C, max 1 in any reference -> 1. leaves 1 -> 1. at: 2 in C, max 1 -> 1. noon 1 -> 1. Clipped total 4 out of 6 candidate words, p1 = 4/6. This is the course's Step 2-3 (R(w) = largest count in any one reference, clip = min). Unclipped precision gives 6/6 for a stuttering candidate.",
        diagram="""
 word    C(w)  max over refs R(w)  clip=min
 train    2          1               1
 leaves   1          1               1
 at       2          1               1
 noon     1          1               1
 total    6                          4
""",
        analogy="Like rate limiting: each n-gram can claim at most as many matches as the most generous single reference allows; repeating it doesn't buy more.",
        topic="bleu-mt", level=2),
    mcq("In the course's BLEU example 1, the candidate 'but love other love friend for love yourself' has 'love' 3 times; R3 'but love your neighbors as you love yourself' has it twice and R1, R2 once each. What clipped count does 'love' get?",
        ["2: the maximum count in any single reference",
         "3: its count in the candidate",
         "4: the sum over all three references",
         "1: the minimum over the references"], 0,
        "Course Step 2: R(w) = the largest number of times it appears in any of the references.",
        "R(love) = max(1, 1, 2) = 2 and clip = min(C, R) = min(3, 2) = 2. Summing across references (4) would let a candidate repeat a word as often as all references combined. The course example ends at 5/8.",
        topic="bleu-mt", level=2),
    mcq("A bilingual judge is shown the source and the MT output; a monolingual judge is shown a reference translation and the MT output. What are both rating?",
        ["Adequacy (fidelity): whether the meaning is conveyed",
         "Fluency only",
         "BLEU",
         "Informativeness via a quiz"], 0,
        "They need something that carries the source meaning.",
        "The course: adequacy is judged on a fixed scale either by bilingual judges given source + target, or by monolingual judges given reference + MT result. Fluency needs only the output. Informativeness is the task-based variant (answer questions about the source using only the translation).",
        topic="mt-eval", level=2),
    mcq("The course's Indic slide translates 'He is going to Delhi' and 'She is going to Delhi' into Hindi. Both start 'vaha dilli jaa ...'. Where does the gender show up in Hindi?",
        ["In the verb: 'jaa rahaa hai' (masculine) vs 'jaa rahii hai' (feminine)",
         "In the pronoun vaha, which has two forms",
         "In the word for Delhi",
         "Nowhere: Hindi cannot express gender"], 0,
        "vaha covers he, she and it.",
        "Hindi's pronoun vaha is gender-neutral, but the verb agrees with the subject's gender. So English -> Hindi must find the gender of 'he/she' and move it onto the verb, and Hindi -> English must recover he or she from the verb ending. 'Information does not always map fully from one language into another.'",
        diagram="""
 He  is going to Delhi -> vaha dilli jaa rahaa hai  (masc.)
 She is going to Delhi -> vaha dilli jaa rahii hai  (fem.)
       pronoun 'vaha' is the same; the verb carries gender
""",
        topic="indic-mt", level=2),
    mcq("The course says Hindi and Marathi are 'related languages'. Which three similarities does it list as the reason transfer learning works well between them?",
        ["Lexical (shared cognates and loanwords), morphological (corresponding suffixes/postpositions), syntactic (same basic word order)",
         "Same script, same speakers, same newspapers",
         "Same phonology, same tones, same alphabet size",
         "Identical vocabularies and grammar"], 0,
        "Words, word endings, word order.",
        "The slide aligns a Marathi sentence with its Hindi translation (bhAratAcyA ... / bhArata ke ...) to show shared vocabulary, suffix-postposition correspondences and the same SOV order. It also notes related languages may not share a family: they can be related by contact (the Indian subcontinent as a linguistic area), e.g. Dravidian and Indo-Aryan languages.",
        topic="indic-mt", level=2),
    tf("According to the course, IndicTrans2 (AI4Bharat, 2023) was the first open-source Transformer NMT model to cover all 22 scheduled Indian languages.", True,
       "It also powers Bhashini's translation APIs.",
       "IndicTrans2: about 1.1B parameters, MIT-licensed, trained on BPCC (built on Samanantar), state of the art on the IN22 and FLORES benchmarks, with script unification to help low-resource languages like Kashmiri, Manipuri, Sindhi and Santali.",
       topic="indic-mt", level=2),
    mcq("An English -> French system translates 'The nurse is here' with the feminine 'L'infirmière' and 'The doctor is here' with the masculine 'Le médecin', though English gives no gender. What is this called?",
        ["Gender bias learnt from the training data",
         "A lexical gap",
         "Hallucination",
         "Pro-drop"], 0,
        "The model copied a stereotype from its data.",
        "English 'nurse' and 'doctor' are gender-neutral; the model fills the missing gender from statistical associations in its corpus. The course: 'NMT picks up biases in training data'. Fixes include offering both forms, gender tags in the input and counterfactual data augmentation.",
        analogy="Like autocomplete trained on old commit logs suggesting yesterday's conventions: it reproduces the statistics of its data, not the intent of the user.",
        topic="mt-risks", level=2),
    mcq("A hospital bot's MT turns 'Do not stop the medicine' into the target-language equivalent of 'Stop the medicine'. What kind of error is this?",
        ["Negation deletion: the meaning is reversed while the sentence stays fluent",
         "A fluency error",
         "A brevity-penalty error",
         "A tokenisation error in the reference"], 0,
        "The output reads perfectly well.",
        "Dropping 'do not' flips the instruction. Fluency checks pass it and BLEU barely drops (most n-grams still match), yet it is dangerous in healthcare. Safety-critical deployments need adequacy checks, negation test suites and human review of instructions.",
        topic="mt-risks", level=2),
    out("lengths = [5, 30, 6, 28, 7, 29]     # sentence lengths in tokens\n"
        "def pad_waste(ls, bs=2):\n"
        "    waste = 0\n"
        "    for i in range(0, len(ls), bs):\n"
        "        b = ls[i:i+bs]\n"
        "        waste += max(b) * len(b) - sum(b)\n"
        "    return waste\n"
        "print(pad_waste(lengths), pad_waste(sorted(lengths)))",
        ["69 23", "23 69", "69 69", "0 0"], 0,
        "Each mini-batch is padded to its longest sentence.",
        "Unsorted batches (5,30), (6,28), (7,29) waste 25 + 22 + 22 = 69 pad tokens; sorted (5,6), (7,28), (29,30) waste 1 + 21 + 1 = 23. That is why the course (after Koehn) sorts a maxi-batch (e.g. 1,600 pairs) by length before cutting mini-batches of 80: less compute spent on padding.",
        topic="nmt", level=2),
    fill("In a Transformer MT decoder, self-attention is ____ so that position t cannot look at the target words after it.", "masked",
         "The course's diagram labels it 'Masked Attn + FFN'.",
         "During training the whole reference target is fed in at once (teacher forcing). The causal mask hides future positions so the model learns to predict each word from only the words before it, just like at inference time.",
         topic="nmt", level=2),
    mcq("A single multilingual NMT model is trained on English<->Hindi and English<->Tamil only. How does it know which language to output?",
        ["A target-language tag token (e.g. <2ta>) is added to the input",
         "It always outputs English",
         "It detects the language of the reference at inference",
         "Each language has its own separate decoder chosen at random"], 0,
        "Google's zero-shot paper used a token at the start of the source.",
        "Prepending a tag like <2ta> tells the shared decoder which language to write. Because the encoder learns a shared, interlingua-like space, the model can then try Hindi -> Tamil with <2ta>, a direction never seen in training (zero-shot translation).",
        diagram="""
 "<2ta> How are you?"  -> [shared model] -> Tamil
 "<2hi> How are you?"  -> [shared model] -> Hindi
 "<2ta> (Hindi text)"  -> [shared model] -> Tamil, zero-shot
""",
        topic="subword-data", level=2),

    # ------------------------------------------------------------------ L3
    mcq("A parallel corpus has three pairs: 'the cat sleeps' -> 'le chat dort', 'the dog sleeps' -> 'le chien dort', 'cat eats' -> 'chat mange'. IBM Model 1, no NULL, uniform start t(f | e) = 1/5 (five French words). What is t(chat | cat) after the first M-step?",
        ["5/12",
         "1/3",
         "1/2",
         "5/6"], 0,
        "Collect fractional counts from EVERY sentence that contains 'cat', then normalise by cat's total.",
        "E-step: in sentence 1 each French word splits over 3 English words (1/3 each); in sentence 3 over 2 (1/2 each). c(chat, cat) = 1/3 + 1/2 = 5/6. c(cat) = 3 x 1/3 + 2 x 1/2 = 2. t = (5/6) / 2 = 5/12. Using only sentence 1 gives 1/3; 5/6 forgets to normalise. This is the end-sem's 'collect counts from all relevant sentences' trap.",
        diagram="""
 sentence          French words   share per word for 'cat'
 the cat sleeps    le chat dort        1/3 each
 cat eats          chat mange          1/2 each
 c(chat,cat) = 1/3 + 1/2 = 5/6     c(cat) = 1 + 1 = 2
 t(chat|cat) = (5/6) / 2 = 5/12
""",
        analogy='Like splitting credit for pair-programmed commits: start by giving each author an equal share, then reweight by who usually touches those files, and repeat until the shares settle.',
        topic="ibm-em", level=3),
    out("from collections import defaultdict\n"
        "corpus = [(\"green house\", \"casa verde\"), (\"the house\", \"la casa\")]\n"
        "t = defaultdict(lambda: 1 / 3)            # 3 Spanish words, uniform\n"
        "c, tot = defaultdict(float), defaultdict(float)\n"
        "for es, fs in corpus:                     # one EM iteration\n"
        "    E = es.split()\n"
        "    for f in fs.split():\n"
        "        z = sum(t[(f, e)] for e in E)\n"
        "        for e in E:\n"
        "            c[(f, e)] += t[(f, e)] / z; tot[e] += t[(f, e)] / z\n"
        "print(c[(\"casa\", \"house\")] / tot[\"house\"], c[(\"la\", \"house\")] / tot[\"house\"])",
        ["0.5 0.25", "0.3333333333333333 0.3333333333333333", "1.0 0.5", "0.5 0.5"], 0,
        "'house' is in both sentences, and 'casa' is in both too.",
        "c(casa, house) = 1/2 + 1/2 = 1, c(la, house) = 1/2, c(verde, house) = 1/2, so house's total is 2. t(casa | house) = 1/2, t(la | house) = t(verde | house) = 1/4: exactly the course's 'Example cont.' table. Co-occurrence across sentences is what breaks the symmetry; casa keeps gaining in later iterations.",
        topic="ibm-em", level=3),
    mcq("An exam asks: 'English \"big dog\" -> German \"hund groß\". Does IBM Model 1 penalise the swapped adjective-noun order?' Which answer earns the mark?",
        ["No: Model 1's alignment probability is uniform (1/l per source position), so it ignores where words sit; position-dependence only arrives in Model 2's a(i | j, l, m)",
         "Yes: crossing alignment links get a lower probability",
         "Yes: the language model penalises it",
         "No, because German and English have the same word order"], 0,
        "What does Model 1 assume about P(a_j = i)?",
        "Model 1 is a 'bag of words' alignment model: every source position is equally likely for every target position. 'hund groß' scores exactly as 'groß hund' would. Model 2 adds absolute position, Models 3-5 fertility and distortion. (In a full SMT system the target LM would handle fluency, but the question is about Model 1's alignment term.)",
        diagram="""
   big     dog          P(a_j = i) = 1/2 for every link,
     \\     /            crossed or not
      \\   /
       \\ /
       / \\
      /   \\
   hund    gross
""",
        topic="ibm-em", level=3),
    mcq("In IBM Model 1 with a NULL token, the Spanish word 'se' appears in many sentences but never consistently with any one English word. After many EM iterations, where does most of its alignment mass go?",
        ["To NULL: NULL is in every sentence, so it is the one 'source word' that always co-occurs with 'se'",
         "To the most frequent English word, 'the'",
         "Evenly to every English word in the vocabulary",
         "It stays uniform forever"], 0,
        "Which source token is present in every single sentence pair?",
        "EM rewards consistent co-occurrence. Each English content word appears with 'se' only sometimes, but NULL appears in all pairs, so t(se | NULL) grows. This is how Model 1 learns that some target words have no source partner. The makeup paper asks the same idea with 'NULL I am hungry' -> 'Tengo hambre'.",
        diagram="""
 NULL   the   house   is   ...     <- NULL is in EVERY pair
   |
   +-----> se   (no consistent English partner)
""",
        topic="ibm-em", level=3),
    out("import math\n"
        "# (log P(f|e), log P(e)) for two candidate translations\n"
        "cands = {\"A\": (math.log(0.04), math.log(1e-6)),\n"
        "         \"B\": (math.log(0.01), math.log(8e-6))}\n"
        "for k, (tm, lm) in cands.items():\n"
        "    print(k, round(tm + lm, 2))",
        ["A -17.03\nB -16.34", "A -16.34\nB -17.03", "A -3.22\nB -4.61", "A 4e-08\nB 8e-08"], 0,
        "log(a x b) = log a + log b; the larger (less negative) total wins.",
        "A: 0.04 x 1e-6 = 4e-8, ln = -17.03. B: 0.01 x 8e-6 = 8e-8, ln = -16.34. B wins although its TM score is 4 times worse, because its LM score is 8 times better. Real decoders add log probabilities (often with weights) to avoid underflow on long sentences.",
        topic="smt-noisy", level=3),
    mcq("A student writes the noisy channel as ê = argmax_e P(e | f) x P(e). What is wrong with it?",
        ["It should be P(f | e) x P(e): Bayes turns P(e | f) into P(f | e) P(e) / P(f); multiplying P(e | f) by P(e) counts fluency twice",
         "Nothing; it is the course's formula",
         "It should be P(e | f) x P(f)",
         "It should be P(f | e) / P(e)"], 0,
        "Apply Bayes' rule to P(e | f).",
        "argmax P(e | f) = argmax P(f | e) P(e) / P(f) = argmax P(f | e) P(e). The 'reversed' translation model P(f | e) need not produce fluent English; P(e) does that. The course slide labels P(f | e) the translation model and P(e) the language model.",
        topic="smt-noisy", level=3),
    mcq("Before learning word alignments, SMT pipelines align the sentences of the bitext. What cue does the course say simple sentence-alignment methods use?",
        ["Sentence length: a long sentence usually translates to a long sentence",
         "Word alignments from IBM Model 1",
         "BLEU between candidate pairs",
         "The language model score"], 0,
        "Gale-Church style methods use a very coarse cue.",
        "Coarse length-based alignment (in characters or words) pairs sentences of a document and its translation cheaply, allowing 1-1, 1-2 and 2-1 merges. Only after that does EM learn word alignments inside each pair.",
        topic="smt-noisy", level=3),
    out("P = {(): {\"a\": 0.5, \"the\": 0.4},\n"
        "     (\"a\",): {\"cat\": 0.3, \"dog\": 0.2},\n"
        "     (\"the\",): {\"cat\": 0.9, \"dog\": 0.1}}\n"
        "greedy = max(P[()], key=P[()].get)\n"
        "g2 = max(P[(greedy,)], key=P[(greedy,)].get)\n"
        "print(greedy, g2, round(P[()][greedy] * P[(greedy,)][g2], 2))\n"
        "paths = [((w1, w2), P[()][w1] * p2) for w1 in P[()] for w2, p2 in P[(w1,)].items()]\n"
        "best = max(paths, key=lambda x: x[1])\n"
        "print(\" \".join(best[0]), round(best[1], 2))",
        ["a cat 0.15\nthe cat 0.36", "a cat 0.15\na cat 0.15", "the cat 0.36\nthe cat 0.36", "a cat 0.5\nthe cat 0.9"], 0,
        "Greedy commits to the best first word; the second line scores whole paths.",
        "Greedy picks 'a' (0.5) and ends with 0.5 x 0.3 = 0.15. 'the' (0.4) is followed by a very confident 'cat' (0.9): 0.36. A beam of size 2 keeps both first words and finds 'the cat'. This is the course's 'select second and third best' step in the beam-search walkthrough.",
        topic="phrase-decode", level=3,
        diagram="""
start --0.5--> a   --0.3--> cat   = 0.15  (greedy)
      \\              \\-0.2--> dog   = 0.10
       \\-0.4--> the --0.9--> cat   = 0.36  (best)
                     \\-0.1--> dog   = 0.04
"""),
    out("import math\n"
        "short = [0.6, 0.5]                      # 'Good.' then </s>\n"
        "long_ = [0.6, 0.7, 0.8, 0.8, 0.7]       # 'Good morning to you.' then </s>\n"
        "for name, ps in ((\"short\", short), (\"long\", long_)):\n"
        "    lp = sum(math.log(p) for p in ps)\n"
        "    print(name, round(lp, 2), round(lp / len(ps), 2))",
        ["short -1.2 -0.6\nlong -1.67 -0.33", "short -0.6 -1.2\nlong -0.33 -1.67", "short -1.2 -0.6\nlong -1.67 -1.67", "short 0.3 0.15\nlong 0.19 0.04"], 0,
        "Every token adds a negative log probability; the last column divides by length.",
        "Raw sum: the short hypothesis wins (-1.2 > -1.67) although every word of the long one is fairly confident, because it pays for fewer tokens. Per-token average (length normalisation): long wins (-0.33 > -0.6). Without normalisation beam search drifts to short outputs, which BLEU's brevity penalty then punishes.",
        topic="phrase-decode", level=3),
    mcq("Following Koehn, the course reranks with a right-to-left (R2L) model. Why can the R2L model not be used during the left-to-right beam search itself?",
        ["It needs the complete sentence to score from the right end, so it can only score finished candidates from the n-best list",
         "R2L models are too slow to load",
         "R2L models are trained on different languages",
         "Beam search does not use model scores"], 0,
        "The course: 'Only possible once full sentence produced'.",
        "Steps: generate an n-best list with the L2R model, score each candidate with the R2L model, choose the best average. The R2L model brings right context (e.g. agreement with a word that comes later) but has nothing to say about a half-built prefix.",
        topic="phrase-decode", level=3),
    mcq("A bank's English -> Hindi bot is scored on one test item. Reference: 'Transfer money to savings account' (5 words). Candidate: 'Transfer the money to account' (5 words). What is BLEU-2 (uniform weights, geometric mean)?",
        ["0.447",
         "0.525",
         "0.8",
         "0.2"], 0,
        "p1 counts matching words, p2 matching adjacent pairs; c = r so BP = 1.",
        "p1: Transfer, money, to, account match, 'the' doesn't: 4/5. Bigrams: 'Transfer the' no, 'the money' no, 'money to' yes, 'to account' no: 1/4. BP = 1 (c = r = 5). BLEU-2 = sqrt(0.8 x 0.25) = sqrt(0.2) = 0.447. 0.525 is the arithmetic mean (0.8 + 0.25) / 2; 0.2 forgets the square root.",
        diagram="""
 unigrams:  Transfer  the  money  to  account   -> 4/5
              ok      x     ok    ok    ok
 bigrams:   Transfer-the  the-money  money-to  to-account
                x            x          ok        x   -> 1/4
 BLEU-2 = 1 x sqrt(0.8 x 0.25) = 0.447
""",
        topic="bleu-mt", level=3),
    out("import math\n"
        "c = \"your order has shipped\".split()\n"
        "r = \"your order has shipped today\".split()\n"
        "p1 = sum(w in r for w in c) / len(c)\n"
        "bi = lambda s: list(zip(s, s[1:]))\n"
        "p2 = sum(b in bi(r) for b in bi(c)) / len(bi(c))\n"
        "bp = 1.0 if len(c) > len(r) else math.exp(1 - len(r) / len(c))\n"
        "print(p1, p2, round(bp, 3), round(bp * math.sqrt(p1 * p2), 3))",
        ["1.0 1.0 0.779 0.779", "1.0 1.0 1.0 1.0", "1.0 1.0 0.8 0.8", "0.8 0.75 0.779 0.603"], 0,
        "A truncated candidate has perfect precision; only BP can punish it.",
        "Every candidate word and bigram is in the reference, so p1 = p2 = 1. c = 4 < r = 5, so BP = e^(1 - 5/4) = e^(-0.25) = 0.779 and BLEU-2 = 0.779. This is the end-sem pattern ('Machine learning improves' -> e^(-1/3) = 0.717). 0.8 is c/r, which is not the BP formula.",
        topic="bleu-mt", level=3),
    mcq("The course's Cand 1 'Mary no slap the witch green' against Ref 'Mary did not slap the green witch' has p1 = 5/6 and p2 = 1/5. What is its BLEU (N = 2), and what does each factor contribute?",
        ["sqrt(5/6 x 1/5) = 0.408 times BP e^(1 - 7/6) = 0.846, so BLEU = 0.345",
         "(5/6 + 1/5) / 2 = 0.517 times BP 0.846 = 0.437",
         "0.408 with BP = 1 because c > r",
         "5/6 x 1/5 = 0.167 times BP 0.846 = 0.141"], 0,
        "c = 6, r = 7.",
        "Geometric mean of 5/6 and 1/5 is sqrt(1/6) = 0.408. The candidate (6 words) is shorter than the best reference (7), so BP = e^(1 - 7/6) = e^(-1/6) = 0.846. 0.846 x 0.408 = 0.345. The low bigram precision exposes the bad word order (witch green), which unigrams alone would miss.",
        topic="bleu-mt", level=3),
    tf("The course's Cand 2 'Mary did not give a smack to a green witch' (10 words) gets brevity penalty 1, even though it is longer than every reference (7 words each), so BLEU does not punish it for being too long.", True,
       "BP only looks one way.",
       "BP = 1 whenever c > r. Over-long candidates are punished only indirectly: their extra n-grams don't match and lower the precisions (p1 = 7/10, p2 = 4/9, BLEU 0.558). That is why BLEU needs BP at all: precision alone can't see missing words, but it does see extra ones.",
       topic="bleu-mt", level=3),
    mcq("An English -> Hindi system scores BLEU 0.21 but BERTScore 0.79 against the references. Human raters say most outputs are correct. What is the most likely explanation?",
        ["The outputs are valid paraphrases: different word choices and inflections share few exact n-grams with the reference but are close in meaning",
         "The system hallucinates content",
         "BERTScore is broken for Hindi",
         "The references are in the wrong language"], 0,
        "BLEU rewards the exact surface form; BERTScore compares embeddings.",
        "Hindi allows free-ish word order and many inflected forms, so a correct translation can share few exact n-grams with one reference. BERTScore matches tokens by contextual-embedding cosine similarity (the course's cat/mat vs cat/rug example), so it gives credit. A gap like this argues for chrF/COMET and multiple references, not for distrusting the system.",
        topic="mt-eval", level=3),
    out("from collections import Counter\n"
        "def char_ngrams(s, n=2):\n"
        "    s = s.replace(\" \", \"\")\n"
        "    return Counter(s[i:i+n] for i in range(len(s) - n + 1))\n"
        "hyp, ref = \"ladkiyan ko\", \"ladkiyon ko\"\n"
        "h, r = char_ngrams(hyp), char_ngrams(ref)\n"
        "m = sum((h & r).values())\n"
        "p, rc = m / sum(h.values()), m / sum(r.values())\n"
        "word_p = sum((Counter(hyp.split()) & Counter(ref.split())).values()) / len(hyp.split())\n"
        "print(round(word_p, 2), round(2 * p * rc / (p + rc), 2))",
        ["0.5 0.78", "0.5 0.5", "1.0 0.78", "0.5 1.0"], 0,
        "The two forms share every character bigram except those around the changed vowel.",
        "At word level 'ladkiyan' vs 'ladkiyon' is a total miss: 1/2. Character bigrams (spaces removed): 9 each, 7 shared (la ad dk ki iy nk ko), F = 7/9 = 0.78. This is the course's point that chrF suits morphologically rich languages. Real chrF averages n = 1..6 and weights recall twice as much (beta = 2).",
        topic="mt-eval", level=3),
    mcq("During NMT training the decoder is fed the reference word y_(t-1) at step t, not its own prediction. What is this called, and what problem does it create at inference?",
        ["Teacher forcing; at inference the model sees its own (possibly wrong) outputs, which it never saw in training (exposure bias)",
         "Beam search; it makes training slower",
         "Back-translation; it creates synthetic data",
         "Attention; it removes the bottleneck"], 0,
        "The course's 'Training phase: comparing predicted word with actual'.",
        "Teacher forcing makes training fast and stable (with a Transformer every position is computed in parallel). But at test time one early mistake feeds into later steps, a mismatch called exposure bias. Beam search and ensembles reduce its impact.",
        diagram="""
 training : <s>  The  cat     (gold words fed in)
              |    |    |
 predict  :  The  cat  sleeps
 inference: <s> -> own guess -> own guess (errors carry)
""",
        analogy="Like a junior dev who always gets the senior's correct previous commit to build on in training, then in production has to build on their own possibly buggy commits.",
        topic="nmt", level=3),
    mcq("Why does the course say the Transformer trains 'dramatically faster than RNNs' on the same parallel corpus?",
        ["Self-attention processes all positions of a sentence in parallel; an RNN must step through tokens one after another",
         "Transformers have fewer parameters",
         "Transformers need no positional information",
         "Transformers do not use a decoder"], 0,
        "What forces an RNN to be sequential?",
        "An RNN's hidden state h_t needs h_(t-1), so a 40-token sentence is 40 sequential steps. Self-attention computes every position's representation at once with matrix multiplies, which GPUs love. Positional encodings put back the order information that recurrence used to carry.",
        analogy='An RNN is a for-loop where each iteration needs the previous result; self-attention is a vectorised map over all positions at once.',
        topic="nmt", level=3),
    mcq("A Transformer English-Hindi banking bot uses BPE with 30k merges. A customer types the Hinglish 'Meri EMI-wali date kab hai?'. 'EMI-wali' never occurred in training. What does BPE most likely do?",
        ["Split it into known pieces such as 'EMI', '-', 'wali', each of which the model has seen and can translate",
         "Map the whole token to <unk> and drop it",
         "Translate it letter by letter",
         "Refuse to tokenize mixed-script input"], 0,
        "BPE never needs a dictionary entry for the whole word.",
        "BPE greedily applies its learnt merges, so the unseen compound falls back to frequent subwords: the English root 'EMI' and the Hindi suffix 'wali' (as with 'loan-ka' -> 'loan' + '-ka' in the end-sem). A dictionary-based English tokenizer fails on the Hindi suffix and the hyphenated compound.",
        topic="subword-data", level=3),
    mcq("The course shows two ways to train a multilingual NMT model for a low-resource pair C1 given a high-resource pair C2. Which describes Method 2?",
        ["Train a model on C2, then fine-tune it on C1",
         "Sample from C1 and C2 and combine them into one training corpus",
         "Train on C1 only and discard C2",
         "Translate C1 into C2 with back-translation"], 0,
        "Method 1 mixes the data; Method 2 is sequential.",
        "Method 1: sample from both corpora (often oversampling the small one) and train one joint model. Method 2: transfer learning, train on C2 (e.g. Hindi-English) and fine-tune on C1 (e.g. Marathi-English). Transfer works best when C1 and C2 are related languages.",
        diagram="""
 Method 1: sample(C1) + sample(C2) -> one corpus -> train
 Method 2: train on C2 -> fine-tune on C1 -> model for C1
""",
        topic="subword-data", level=3),
    tf("In 'Since you brought it up, I do not agree' and 'Since you brought it up, we have been working on it', 'since' needs different translations (causal vs temporal), and choosing correctly needs discourse analysis beyond the words themselves.", True,
       "Because ... or from the time that ...?",
       "The course's discourse slide: 'How to translate since? Temporal or conditional?' Many languages use different words for the two senses (French 'puisque' vs 'depuis que'). The clue is in how the clauses relate, which is why discourse is listed among the open challenges.",
       topic="mt-hard", level=3),
    fill("The course's English -> Chinese transfer rule VP -> V PP[+benefactor] => VP -> PP[+benefactor] V says that in Chinese a benefactor phrase goes ____ the verb (one word).", "before",
         "Read the right-hand side of the rule left to right.",
         "English 'bought a gift for her' has the benefactor PP after the verb; the rule moves it in front for Chinese. A recipient PP, by contrast, stays after the verb, so the rule needs the semantic role, not just syntax: that is why the course files it under semantic transfer.",
         topic="rbmt", level=3,
         analogy="Like a code-mod rule in a compiler pass: match a syntax pattern, check a type annotation (+benefactor), rewrite the tree."),
    out("n = 22                       # languages to support\n"
        "transfer = n * (n - 1)       # one transfer module per direction\n"
        "interlingua = 2 * n          # one analyser + one generator per language\n"
        "print(transfer, interlingua)",
        ["462 44", "231 22", "484 44", "462 22"], 0,
        "Directions are ordered pairs; Hindi->Tamil differs from Tamil->Hindi.",
        "22 x 21 = 462 directed transfer modules vs 2 x 22 = 44 components for an interlingua. That is the classic argument for the top of the Vauquois triangle, and the same argument (one shared model instead of 462 pairwise ones) drives multilingual NMT for Indian languages. 231 counts unordered pairs.",
        topic="rbmt", level=3,
        analogy="Point-to-point integrations between n services need n(n-1) adapters; a canonical data model (hub and spoke) needs 2n mappers.",
        diagram="""
pairwise transfer        interlingua (hub)
  HI <----> TA             HI    TA
   ^ \\    / ^               \\   /
   |   \\/   |               [IL]
   v  /  \\  v               /   \\
  BN <----> KN             BN    KN
"""),
    out("direct = 0.72            # adequacy of a direct Kannada->Gujarati model\n"
        "kn_en, en_gu = 0.85, 0.80  # adequacy of each leg via English\n"
        "pivot = kn_en * en_gu\n"
        "print(round(pivot, 2), pivot < direct)",
        ["0.68 True", "0.82 False", "0.8 False", "1.65 False"], 0,
        "If each leg independently keeps a fraction of the meaning, the fractions multiply.",
        "A rough model: 0.85 x 0.80 = 0.68 of the meaning survives two hops, below the direct system's 0.72, even though each leg looks better on its own. Pivoting via a link language (English) is the default when there's no Kannada-Gujarati data, but errors compound and information English lacks (verb gender, honorifics) can be lost on the way.",
        analogy='Like converting a JPEG to PNG and back to JPEG: each lossy hop throws a bit away, and the losses multiply.',
        topic="indic-mt", level=3,
        diagram="""
Kannada --0.85--> English --0.80--> Gujarati   = 0.68
Kannada ---------------0.72-------> Gujarati   (direct)
"""),
    mcq("IndicBART and IndicTrans2 use 'script unification' for Indian languages. What is it and why does it help low-resource languages?",
        ["Transliterating related scripts into one common script, so cognates like Hindi 'kamal' and Bengali 'kamal' share subword tokens and transfer across languages",
         "Translating every language into English before training",
         "Removing all vowels from the text",
         "Using a separate vocabulary for each script"], 0,
        "Same word, different alphabet.",
        "Hindi, Marathi, Bengali, Gujarati and others share many cognates but write them in different scripts, so a subword vocabulary would treat them as unrelated strings. Mapping them to one script (e.g. Devanagari) lets the model see the shared vocabulary, which the course credits for gains on Kashmiri, Manipuri, Sindhi and Santali.",
        topic="indic-mt", level=3),
    out("bn = \"\\u0995\\u09ae\\u09b2\"          # Bengali word 'kamal'\n"
        "dev = \"\".join(chr(ord(ch) - 0x80) for ch in bn)\n"
        "print(dev, dev == \"\\u0915\\u092e\\u0932\")",
        ["कमल True", "কমল False", "कमल False", "UnicodeDecodeError"], 0,
        "Unicode lays out the Brahmi-derived Indic blocks in parallel, 0x80 apart.",
        "Bengali (U+0980-09FF) and Devanagari (U+0900-097F) blocks follow the same layout, so subtracting 0x80 maps ক -> क, ম -> म, ল -> ल. This offset trick is how Indic NLP toolkits do rule-based script conversion for script unification. It handles letters but not every script-specific sign, so real converters add exception tables.",
        topic="indic-mt", level=3),
    fill("Writing the place name 'Bengaluru' in Kannada or Hindi script by its SOUND, rather than translating its meaning, is called ____.", "transliteration",
         "Trans + literation (letters).",
         "Names, brands and many code-mixed words are transliterated, not translated. Indic MT pipelines need transliteration both for named entities in the output and for romanised input ('mera loan status') typed by users.",
         topic="indic-mt", level=3),
    tf("Because NMT is a single end-to-end network, forcing a rule such as 'always translate EMI as EMI, never as a paraphrase' is as easy as adding a dictionary entry in rule-based MT.", False,
       "The course lists 'difficult to control' as an NMT disadvantage.",
       "NMT has no rule table to edit: 'can't easily specify rules or guidelines for translation'. Teams use constrained decoding with terminology lists, placeholder tagging for entities, or fine-tuning on in-domain glossaries (DeepL's glossary controls in the course). RBMT's strength was exactly this predictability.",
       topic="mt-risks", level=3),

    # ------------------------------------------------------------------ L4
    mcq("Two students run a SECOND EM iteration on the course trace (green house / casa verde, the house / la casa). One gets t(casa | house) = 2/3, the other 3/5. Which is right for IBM Model 1, and where does the other number come from?",
        ["3/5 is Model 1: each Spanish word's posterior is computed independently over all source words. 2/3 comes from enumerating only the two one-to-one alignments per sentence, as the slide's trace does",
         "2/3 is Model 1; 3/5 is Model 2",
         "Both are Model 1; the difference is rounding",
         "3/5 is right because NULL was added; 2/3 has no NULL"], 0,
        "Model 1 lets two Spanish words align to the same English word.",
        "After iteration 1, t(casa|house) = t(casa|green) = 1/2, t(verde|green) = 1/2, t(verde|house) = 1/4. Model 1 per word: casa splits 1/2 : 1/2 in both sentences, verde splits 2/3 : 1/3 (green : house), la splits 2/3 : 1/3 (the : house), so c(casa, house) = 1 out of house's total 1/2 + 1/3 + 1/3 + 1/2 = 5/3 -> 3/5. The slide (from an older lecture deck) enumerates only the permutations and normalises (1/8 vs 1/4 -> 1/3 vs 2/3), which drops the many-to-one alignments. Both agree at iteration 1 from a uniform start, which is all the exams ask.",
        topic="ibm-em", level=4),
    out("l, m = 2, 2                       # English words (plus NULL), Spanish words\n"
        "eps = 1.0\n"
        "t_vals = [0.5, 0.4]               # t(f_j | e_a(j)) for one chosen alignment\n"
        "p = eps / (l + 1) ** m\n"
        "for x in t_vals:\n"
        "    p *= x\n"
        "print((l + 1) ** m, round(p, 4))",
        ["9 0.0222", "4 0.05", "9 0.2", "6 0.0333"], 0,
        "Each of the m target words may pick any of the l + 1 source positions (NULL included).",
        "IBM Model 1: P(f, a | e) = eps / (l + 1)^m x prod_j t(f_j | e_a(j)). With NULL there are (2 + 1)^2 = 9 alignments, each with prior 1/9, so this one scores 0.5 x 0.4 / 9 = 0.0222. Without NULL it would be 4 alignments and 0.05. The (l + 1)^m blow-up is why the E-step is computed per word instead of enumerating alignments.",
        topic="ibm-em", level=4),
    out("from collections import defaultdict\n"
        "corpus = [(\"the cat sleeps\", \"le chat dort\"), (\"the dog sleeps\", \"le chien dort\"), (\"cat eats\", \"chat mange\")]\n"
        "t = defaultdict(lambda: 1 / 5)\n"
        "for _ in range(2):\n"
        "    c, tot = defaultdict(float), defaultdict(float)\n"
        "    for es, fs in corpus:\n"
        "        for f in fs.split():\n"
        "            z = sum(t[(f, e)] for e in es.split())\n"
        "            for e in es.split():\n"
        "                c[(f, e)] += t[(f, e)] / z; tot[e] += t[(f, e)] / z\n"
        "    t = defaultdict(float, {k: v / tot[k[1]] for k, v in c.items()})\n"
        "print(round(t[(\"mange\", \"eats\")], 2), round(t[(\"chat\", \"eats\")], 2))",
        ["0.55 0.45", "0.5 0.5", "1.0 0.0", "0.45 0.55"], 0,
        "'eats' appears only once, next to 'cat'. Who explains 'chat' better?",
        "After iteration 1 both are 0.5 (eats sees only 'chat mange'). But iteration 1 also raised t(chat | cat) to 5/12, so in iteration 2 'cat' claims more of 'chat' in sentence 3, leaving more of 'mange' for 'eats': 0.55 vs 0.45. This 'explaining away' through other sentences is how EM sharpens alignments without ever seeing a labelled link.",
        topic="ibm-em", level=4),
    tf("The course notes 'use dynamic programming (as in Baum-Welch) to avoid explicitly enumerating all possible alignments'. For IBM Model 1 this is easy: the E-step posterior of each target word can be computed independently, in O(l x m) time instead of O((l + 1)^m).", True,
       "Model 1's alignment of word j doesn't depend on the alignment of word j'.",
       "Because the alignment prior is uniform and each f_j depends only on its own a_j, the sum over all alignments factorises into a product of per-word sums. So P(a_j = i | e, f) = t(f_j | e_i) / sum_i' t(f_j | e_i'). Models 3-5 lose this property (fertility couples the words) and need approximate search.",
        topic="ibm-em", level=4),
    fill("IBM Models 3 and 4 put some probability on impossible outputs (two words in the same target position). Model 5 removes this flaw, which Brown et al. call being ____.", "deficient",
         "The course table: Model 5 = 'non-____ distortion'.",
         "Deficiency means probability mass leaks onto invalid alignments, so the probabilities of valid outputs sum to less than 1. Model 5 tracks free positions so every placement is valid. In practice Models 1-2 initialise 3-5, and the resulting alignments seed phrase extraction.",
         topic="ibm-em", level=4),
    mcq("With beam size 1 your NMT system outputs translation X. With beam size 50 it outputs Y, which has a HIGHER model probability than X but is rated worse by humans. What kind of error does this reveal?",
        ["A model error: the model's scores are wrong, since better search found a worse translation the model likes more",
         "A search error: the beam was too small",
         "A BLEU error",
         "A tokenisation error"], 0,
        "Search error = the decoder missed the model's best. Here the decoder found something the model rates higher.",
        "If a wider beam finds a higher-scoring but worse output, the search is doing its job and the model is to blame (often by preferring short or generic outputs). A search error would be the reverse: a better translation exists that the model scores higher, but the beam pruned it. Koehn uses this split to decide whether to fix the decoder or the model.",
        analogy="Search error is a bug in the query planner (it missed the best row); model error is a bug in the scoring function (the 'best' row is the wrong one).",
        topic="phrase-decode", level=4),
    tf("In NMT, increasing the beam size from 5 to 100 reliably improves BLEU.", False,
       "Koehn's 'six challenges' paper reports the opposite trend.",
       "Quality typically peaks at small beams (about 4-10) and then drops: very wide beams find short, high-probability outputs and BLEU falls (partly via the brevity penalty). Length normalisation softens but doesn't remove this. So 'beam = 100 is safer' is a trap, and costs latency as well.",
       topic="phrase-decode", level=4),
    out("import numpy as np\n"
        "vocab = [\"bank\", \"shore\", \"river\"]\n"
        "m1 = np.array([0.40, 0.35, 0.25])   # next-word distributions\n"
        "m2 = np.array([0.40, 0.30, 0.30])   # from three NMT models\n"
        "m3 = np.array([0.05, 0.90, 0.05])\n"
        "avg = (m1 + m2 + m3) / 3\n"
        "print([vocab[int(m.argmax())] for m in (m1, m2, m3)], vocab[int(avg.argmax())], round(float(avg.max()), 2))",
        ["['bank', 'bank', 'shore'] shore 0.52", "['bank', 'bank', 'shore'] bank 0.4", "['bank', 'bank', 'shore'] bank 0.28", "['shore', 'shore', 'shore'] shore 0.9"], 0,
        "Averaging probabilities is not the same as majority voting.",
        "Two models narrowly prefer 'bank' (0.40), one is very sure of 'shore' (0.90). Averaged: bank 0.28, shore 0.52, so the ensemble picks 'shore' although a vote would say 'bank'. Ensembles in Koehn's framing average the per-step distributions inside beam search; the course's 'errors are random, correct decisions unique' is why the averaged distribution is usually better than any single model.",
        topic="phrase-decode", level=4,
        analogy="Like averaging confidence scores from three replicas rather than counting votes: one strongly sure replica can outweigh two lukewarm ones."),
    out("import math\n"
        "cand = \"the meeting moved to monday\".split()\n"
        "refs = [\"the meeting is postponed to monday\".split(),\n"
        "        \"the meeting has been moved to monday\".split()]\n"
        "bi = lambda s: list(zip(s, s[1:]))\n"
        "p1 = sum(any(w in r for r in refs) for w in cand) / len(cand)\n"
        "p2 = sum(any(b in bi(r) for r in refs) for b in bi(cand)) / len(bi(cand))\n"
        "c = len(cand)\n"
        "for r in (7, 6):   # 7 = ref with most matches (course), 6 = closest length\n"
        "    bp = 1.0 if c > r else math.exp(1 - r / c)\n"
        "    print(r, round(bp * math.sqrt(p1 * p2), 3))",
        ["7 0.581\n6 0.709", "7 0.709\n6 0.581", "7 0.866\n6 0.866", "7 0.67\n6 0.819"], 0,
        "p1 = 5/5, p2 = 3/4; only BP differs.",
        "All candidate words appear in some reference (moved is in R2): p1 = 1. Bigrams: the meeting, moved to, to monday match, 'meeting moved' doesn't: p2 = 0.75. The course defines r as the length of the reference with the most n-gram matches (R2, 7): BP = e^(-0.4) = 0.670, BLEU 0.581. Standard BLEU (and sacreBLEU) uses the closest reference length (R1, 6): BP = 0.819, BLEU 0.709. State which rule you use in an exam.",
        topic="bleu-mt", level=4),
    tf("The course warns that BLEU correlates with human judgement when comparing two SMT systems, but not when comparing an SMT system with a rule-based system like SYSTRAN or with human translations.", True,
       "BLEU rewards the kind of n-grams SMT systems produce.",
       "SMT outputs share the statistical habits that BLEU's n-gram matching rewards. A rule-based system or a human may produce equally good but differently worded output, so a BLEU gap across system types says little. Compare like with like, or use human evaluation / learned metrics.",
       topic="bleu-mt", level=4),
    mcq("A vendor's rule-based system scores 9 BLEU points below your SMT system on a 2,000-sentence test set, but its outputs are rated better in a human adequacy study. Your manager wants to drop the vendor 'because BLEU says so'. What is the course-based reply?",
        ["BLEU is known not to track human judgement across different system types (SMT vs rule-based); trust the human study, or add a learned metric like COMET",
         "BLEU must be miscomputed; rerun it with 4-grams",
         "Human evaluation is always biased; BLEU is objective",
         "The test set is too large for BLEU"], 0,
        "Which comparisons does the course say BLEU is valid for?",
        "Same-family comparisons (SMT vs SMT, or one NMT checkpoint vs the next) are where BLEU is useful. Across families, its n-gram bias favours the SMT system's style. The human study measures what users care about, so it wins; a neural metric and a targeted error analysis can back it up.",
        topic="bleu-mt", level=4),
    out("import numpy as np\n"
        "s = np.array([1.0, 0.0])                            # decoder state\n"
        "H = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])  # 3 encoder states\n"
        "v = np.array([1.0, 1.0])                            # W = U = I for simplicity\n"
        "scores = np.tanh(s + H) @ v                         # v . tanh(W s + U h)\n"
        "w = np.exp(scores) / np.exp(scores).sum()\n"
        "print(scores.round(2).tolist(), int(w.argmax()))",
        ["[0.96, 1.52, 1.73] 2", "[1.0, 0.0, 1.0] 0", "[0.96, 1.52, 1.73] 0", "[2.0, 1.0, 3.0] 2"], 0,
        "tanh(2) = 0.96, tanh(1) = 0.76; add the components.",
        "Bahdanau's additive score: s + h = [2, 0], [1, 1], [2, 1]; tanh gives [0.96, 0], [0.76, 0.76], [0.96, 0.76]; summing with v = [1, 1] gives 0.96, 1.52, 1.73. Softmax preserves the order, so source word 2 gets the most weight. [1, 0, 1] is the dot product s . h (Luong-style), a different scoring function; [2, 1, 3] skips the tanh.",
        topic="nmt", level=4),
    out("merges = [(\"e\", \"r\"), (\"l\", \"o\"), (\"lo\", \"w\"), (\"n\", \"e\")]  # learnt order\n"
        "def bpe(word):\n"
        "    s = list(word)\n"
        "    for a, b in merges:\n"
        "        i = 0\n"
        "        while i < len(s) - 1:\n"
        "            if s[i] == a and s[i + 1] == b:\n"
        "                s[i:i + 2] = [a + b]\n"
        "            else:\n"
        "                i += 1\n"
        "    return s\n"
        "print(bpe(\"lower\"), bpe(\"newer\"))",
        ["['low', 'er'] ['ne', 'w', 'er']", "['lo', 'w', 'er'] ['n', 'e', 'w', 'er']", "['low', 'er'] ['new', 'er']", "['l', 'o', 'w', 'e', 'r'] ['n', 'e', 'w', 'e', 'r']"], 0,
        "Apply the merges in the order they were learnt, not the order that looks nicest.",
        "lower: e+r -> l o w er; l+o -> lo w er; lo+w -> low er. newer: e+r first turns n e w e r into n e w er; then n+e -> ne w er. There is no ('ne', 'w') merge, so 'new' is never formed. Applying merges in learnt order is what makes BPE deterministic; tokenizers at train and inference must share the same merge list.",
        topic="subword-data", level=4),
    out("sizes = {\"hi\": 8_000_000, \"ta\": 500_000}   # parallel pairs per language\n"
        "for T in (1, 5):\n"
        "    w = {k: n ** (1 / T) for k, n in sizes.items()}\n"
        "    z = sum(w.values())\n"
        "    print(T, {k: round(x / z, 2) for k, x in w.items()})",
        ["1 {'hi': 0.94, 'ta': 0.06}\n5 {'hi': 0.64, 'ta': 0.36}",
         "1 {'hi': 0.94, 'ta': 0.06}\n5 {'hi': 0.94, 'ta': 0.06}",
         "1 {'hi': 0.5, 'ta': 0.5}\n5 {'hi': 0.64, 'ta': 0.36}",
         "1 {'hi': 0.64, 'ta': 0.36}\n5 {'hi': 0.94, 'ta': 0.06}"], 0,
        "p_k is proportional to n_k^(1/T); T = 1 is plain proportional sampling.",
        "With T = 1 Tamil is 6% of batches and gets drowned out. T = 5 flattens the distribution: 8M^0.2 = 24.0 vs 0.5M^0.2 = 13.8, so Tamil rises to 36%. This is the course's Method 1 ('sample from C1, C2 and combine') made concrete; too high a T over-samples the small corpus until the model memorises it.",
        topic="subword-data", level=4),
    tf("A multilingual model trained only on Hindi<->English and Tamil<->English pairs usually translates Hindi -> Tamil (zero-shot) as well as a model trained directly on Hindi-Tamil parallel data.", False,
       "The course shows zero-shot works; it doesn't say it matches supervised.",
       "Zero-shot directions work surprisingly well (the course's evidence for an interlingua-like space), but usually trail supervised or pivoted systems and sometimes output the wrong language. Adding even a little direct data, or back-translated Hindi-Tamil pairs, closes much of the gap.",
       topic="subword-data", level=4),
    mcq("COMET is listed with BERTScore as a neural metric with better human correlation. What does COMET use that BLEU and BERTScore do not?",
        ["The source sentence, and a model trained to predict human quality judgements from (source, hypothesis, reference)",
         "Character n-grams",
         "The brevity penalty",
         "Only the reference, matched by exact words"], 0,
        "BLEU and BERTScore compare hypothesis and reference only.",
        "COMET encodes source, hypothesis and reference with a multilingual encoder and regresses onto human scores (direct assessment / MQM). Seeing the source lets it notice meaning errors a reference-only metric can miss; its quality-estimation variants even work with no reference. Its weakness: it is only as good as the languages and domains its human data covered.",
        topic="mt-eval", level=4),
    tf("chrF gives partial credit when the candidate is romanised Hindi ('mera khata band karo') but the reference is in Devanagari script.", False,
       "Character n-grams across two scripts.",
       "Latin and Devanagari characters never match, so chrF (and BLEU) score almost zero for a perfectly correct romanised output. Indic evaluation must first normalise script (transliterate one side), which is another reason the course stresses script handling for Indic MT.",
       topic="mt-eval", level=4),
    mcq("A state government wants Odia <-> Assamese translation of circulars. It has 20k parallel sentence pairs, plenty of monolingual Odia and Assamese news, and a small GPU budget. Which plan best follows the course?",
        ["Fine-tune a pretrained multilingual Indic model (IndicTrans2-style, shared/unified script vocabulary), add back-translated monolingual data, and evaluate with chrF plus human adequacy",
         "Train a Transformer from scratch on the 20k pairs and evaluate with BLEU only",
         "Write a rule-based transfer system for the pair",
         "Translate everything via English with two generic systems and skip evaluation"], 0,
        "Low resource: borrow from related languages and from monolingual text.",
        "20k pairs is too little to train from scratch. A multilingual model already shares parameters and script-unified subwords across related Indo-Aryan languages (Odia and Assamese are close to Bengali); back-translation turns monolingual news into extra pairs; chrF suits rich morphology, and human adequacy catches meaning errors. Pivoting via English is a fallback, with compounding errors.",
        topic="indic-mt", level=4,
        analogy="Like starting a new microservice from your company's battle-tested template instead of an empty repo: most of the plumbing is already proven."),
    fill("Samanantar-style corpora were built by embedding sentences from multilingual news sites in one shared vector space and pairing nearest neighbours across languages. This is called parallel-corpus (bitext) ____.", "mining",
         "The course slide: '____ from machine readable sources'.",
         "Sites like DD National or IndianExpress publish the same story in several languages. A multilingual sentence encoder (e.g. LaBSE) puts translations close together, so cosine similarity finds candidate pairs, which are then filtered by a threshold. BPCC, IndicTrans2's training data, extends this.",
         topic="indic-mt", level=4),
    mcq("Your English -> Hindi medical-instructions MT scores BLEU 41 on the test set, but an audit finds 1 in 200 outputs drops a 'do not'. What is the strongest set of safeguards before launch?",
        ["A negation/number/entity test suite, a reference-free quality-estimation gate that routes low-confidence outputs to a human, and human review for dosage instructions",
         "Raise the beam size to 50",
         "Retrain until BLEU reaches 50",
         "Replace BLEU with BERTScore and launch"], 0,
        "BLEU barely moves when one 'not' disappears.",
        "Dropping two tokens from a 20-token sentence costs little BLEU but reverses the meaning, so a higher BLEU target can't guarantee safety. Targeted test suites measure the exact failure, quality estimation (COMET-QE-style) flags risky outputs without a reference, and humans review the safety-critical ones. The end-sem's healthcare-chatbot question is this scenario.",
        topic="mt-risks", level=4,
        analogy="Like unit tests for edge cases plus a canary gate: overall uptime (BLEU) can look great while one critical path is broken."),
    mcq("Match each failure to its cause. F1: Japanese 'Tabemashita' (no subject) -> 'Ate.' F2: 'I saw the movie and it is good' -> German 'sie ist gut'. F3: English 'river' -> French 'rivière' when the river reaches the sea.",
        ["F1 pro-drop, F2 pronominal anaphora (gender of Film), F3 lexical gap",
         "F1 lexical gap, F2 pro-drop, F3 anaphora",
         "F1 word order, F2 lexical gap, F3 pro-drop",
         "F1 anaphora, F2 word order, F3 pro-drop"], 0,
        "Missing subject, wrong pronoun, a distinction English doesn't make.",
        "F1: Japanese drops the subject, so English needs it inferred ('I ate'). F2: 'it' -> Film (masculine) needs 'er'; 'sie' is the feminine form. F3: French splits English 'river' into fleuve (reaches the sea) and rivière, so information must be added. Exams like 'name the phenomenon' questions; the trick is to pick the one that matches what went wrong, not the most famous term.",
        topic="mt-hard", level=4),
    tf("The course reads Google's zero-shot translation (language pairs never seen together in training) as evidence that neural models learn an interlingua-like shared representation, the neural version of the Vauquois apex.", True,
       "The Google Translate slide's 'Lesson'.",
       "If a model trained on Portuguese-English and English-Spanish can do Portuguese-Spanish, its encoder must map sentences into a space shared across languages. It is 'interlingua-like', not a hand-designed interlingua: it is learnt, not interpretable, and leaky (zero-shot quality trails supervised). The deck's 'Interlingua using neural network' slide makes the same link.",
       topic="rbmt", level=4),
]
