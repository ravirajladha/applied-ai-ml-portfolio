from helpers import mcq, tf, out, fill

SUBJECT = "llmc-foundations"

TOPICS = [
    ("lm-basics", "Language models as next-token probability"),
    ("pipeline", "The LLM pipeline and LM head"),
    ("token-types", "Word, subword, character and byte tokens"),
    ("bpe", "BPE: token learner and segmenter"),
    ("markers-libs", "Byte-level BPE, WordPiece, SentencePiece, libraries"),
    ("embeddings", "Token embeddings and the |V| x d table"),
    ("similarity", "Static vs contextual embeddings, cosine"),
    ("positional", "Positional encoding: sinusoidal, learned, RoPE"),
    ("context-window", "Context window"),
    ("families-tasks", "Encoder vs decoder families, NLU vs NLG"),
]

QUESTIONS = [
    # ------------------------------------------------------------------ L1
    mcq("In the course's definition, what does a language model (LM) do?",
        ["It assigns probabilities to sequences of tokens, or equivalently to the next token given the previous ones",
         "It looks up the dictionary meaning of every word",
         "It translates text into a database query",
         "It stores every sentence it has read and returns the closest one"], 0,
        "Think 'P(...)', not 'lookup'.",
        "An LM is a probability model: P(w1..wn), or P(next token | context). An LLM is the same thing, just huge and trained on trillions of tokens. It does not store and retrieve sentences.",
        topic="lm-basics", level=1,
        analogy="Phone autocomplete: it ranks which word is likely to come next."),
    tf("A language model should give the sentence 'three guys standing on the sidewalk' a higher probability than the same words shuffled into 'sidewalk the on standing guys three'.", True,
       "Does word order change how natural the text is?",
       "The course's own example: the natural order gets a high probability and the shuffled one a low one. Same words, different order, very different probability. That is why LMs must model order.",
       topic="lm-basics", level=1),
    fill("An LLM generates text one token at a time, appending each new token to its input before predicting the next. This style of generation is called ____.", "autoregressive",
         "Auto = self: it feeds on its own output.",
         "Autoregressive = generate, append, repeat. It is why chat replies stream word by word and why a long answer takes longer: one full model pass per generated token.",
         topic="lm-basics", level=1),
    mcq("Put the building blocks of an LLM in the order the text flows through them.",
        ["Tokenizer → token embeddings + position → Transformer blocks → LM head",
         "LM head → Transformer blocks → tokenizer → embeddings",
         "Embeddings → tokenizer → LM head → Transformer blocks",
         "Tokenizer → LM head → embeddings → Transformer blocks"], 0,
        "Text has to become numbers before any layer can work on it.",
        "Text is split into token IDs, turned into vectors (plus position), processed by N Transformer blocks, and the LM head turns the last hidden state into next-token probabilities.",
        topic="pipeline", level=1,
        diagram="""
"Write an email..."
      |  tokenizer
  [token IDs]
      |  embeddings + position
  [n x d vectors]
      |  Transformer block 1..N
      |  LM head (unembedding + softmax)
  next token: "Dear"
"""),
    mcq("Slide 13 of the intro deck sums up the two sub-layers of a Transformer block in a few words. Which pairing is right?",
        ["Attention = tokens talk to each other; FFN = each token thinks on its own",
         "Attention = each token thinks on its own; FFN = tokens talk to each other",
         "Attention = picks the next token; FFN = tokenizes the input",
         "Attention = stores the vocabulary; FFN = stores the positions"], 0,
        "Which one mixes information ACROSS positions?",
        "Attention moves information between positions (talk). The feed-forward network is applied to each position separately (think). The residual stream adds each sub-layer's output to X instead of replacing it.",
        topic="pipeline", level=1),
    mcq("What is a token?",
        ["The unit a model reads and writes: a word, a piece of a word, a punctuation mark or a byte",
         "Always exactly one English word",
         "Always exactly one character",
         "A password that unlocks the model's API"], 0,
        "'unhappiness!' can be 4 of them.",
        "A token is whatever unit the tokenizer produces: 'unhappiness!' → un | happi | ness | !. Context length, price and speed are all counted in tokens, not words.",
        analogy="LEGO: common words are big pre-made bricks; rare words are built from small ones.",
        topic="token-types", level=1),
    mcq("An old word-level model meets the new word 'Transformerify', which is not in its vocabulary. What happens?",
        ["It is replaced by [UNK] (unknown) and its meaning is lost",
         "The model adds the word to its vocabulary on the fly",
         "It is split into characters automatically",
         "The model refuses to process the sentence"], 0,
        "OOV = out of vocabulary.",
        "A word-level vocabulary is fixed, so an out-of-vocabulary word becomes [UNK]. Subword tokenizers split it into known pieces (Transformer + ify), and byte-level ones never need [UNK].",
        topic="token-types", level=1),
    mcq("A tokenizer has two parts. Which part runs on every new input at inference time?",
        ["The token segmenter, which applies the learned merge rules",
         "The token learner, which builds the vocabulary",
         "The embedding layer",
         "The LM head"], 0,
        "One part runs once at training time, the other on every request.",
        "The learner runs once, at tokenizer-training time, and outputs the vocabulary plus merge rules. The segmenter replays those rules on every input: hugs → [hug, s] → [12, 5].",
        diagram="""
ONCE (tokenizer training)        EVERY INPUT (inference)
corpus -> token LEARNER          "hugs" -> token SEGMENTER
          -> vocab + merges ---------> [hug, s] -> [12, 5]
""",
        analogy="The learner is the compiler run once; the segmenter is the compiled binary you run on every request.",
        topic="bpe", level=1),
    tf("BPE (byte-pair encoding) builds its vocabulary by repeatedly merging the most frequent adjacent pair of symbols in the corpus.", True,
       "Count pairs, merge the winner, repeat.",
       "That is the whole idea: start from single characters (or bytes), count adjacent pairs weighted by word frequency, merge the most frequent pair into a new token, and repeat until the target vocabulary size.",
       topic="bpe", level=1),
    mcq("What is a token embedding?",
        ["A dense vector of learned numbers (length d) that represents a token",
         "The integer ID of the token",
         "The token's spelling stored as bytes",
         "A one-hot vector as long as the vocabulary"], 0,
        "Dense, short, learned.",
        "The ID is just a label; the embedding is a dense vector (e.g. d = 4096 in Llama 3 8B) learned during training, so tokens used in similar ways end up with similar vectors.",
        topic="embeddings", level=1),
    tf("Token ID 3 means 'more' than token ID 2, so the model can use the raw ID number as a measure of meaning.", False,
       "Is the ID a value or a label?",
       "A token ID is only a row number in the vocabulary, like a primary key. Its size carries no meaning; the learned embedding vector does. That is why the ID is looked up in the embedding table first.",
       topic="embeddings", level=1,
       analogy="A user ID 1002 isn't 'more' of a user than 1001; it's just a key into the users table."),
    mcq("Cosine similarity between two vectors ranges from −1 to 1. What does a value of 1 mean?",
        ["The vectors point in the same direction (most similar)",
         "The vectors are unrelated",
         "The vectors point in opposite directions",
         "The vectors have the same length"], 0,
        "Cosine compares direction, not length.",
        "1 = same direction, 0 = unrelated (perpendicular), −1 = opposite. Length is divided out, so [1, 2] and [2, 4] score 1.0.",
        diagram="""
  b  a          a  b              a      b
  ^ ^           ^                <--  -->
  |/            |___> b
cos = 1       cos = 0          cos = -1
""",
        topic="similarity", level=1),
    tf("In a static embedding such as word2vec, 'bank' has the same vector in 'river bank' and in 'bank loan'.", True,
       "Static = one vector per word.",
       "Static embeddings give one fixed vector per word whatever the sentence. Contextual embeddings (the hidden states inside a Transformer) give different vectors for the two meanings.",
       topic="similarity", level=1,
       analogy="Static = a printed dictionary entry; contextual = a friend who heard the whole sentence."),
    mcq("Why does a Transformer need positional encoding at all?",
        ["Attention has no built-in sense of order, so 'dog bites man' and 'man bites dog' would look the same",
         "To make the vocabulary smaller",
         "To tell the model which tokens are rare",
         "To turn token IDs into embeddings"], 0,
        "Same words, different order, different meaning.",
        "Self-attention treats its input as a set: shuffle the tokens and each one gets the same mix of the others. Position must be injected separately, by adding position vectors or (RoPE) rotating Q and K.",
        topic="positional", level=1),
    mcq("What is an LLM's context window?",
        ["The maximum number of tokens the model can process in one call",
         "The number of documents it was trained on",
         "The size of the browser window that shows the chat",
         "The number of layers in the model"], 0,
        "It is counted in tokens.",
        "The context window is the maximum sequence the model can process at a time: 512 for BERT and GPT-2, 4,096 for Llama 2, 128K for Llama 3.",
        topic="context-window", level=1),
    mcq("A shop wants to label each review as positive or negative. Is that an NLU or an NLG task?",
        ["NLU (natural language understanding): it extracts a label from text",
         "NLG (natural language generation): it writes new text",
         "Neither; it is a database task",
         "Both equally, by definition"], 0,
        "Is the output a label or a new piece of writing?",
        "Classification, NER and intent detection extract meaning: NLU. Writing a reply to the review would be NLG. An LLM does NLU by generating the label word ('positive').",
        diagram="""
NLU  text -> meaning   (label, entities, intent)
     "Is this review positive?" -> positive
NLG  text -> new text
     "Write a reply to this review." -> "Thanks for..."
""",
        topic="families-tasks", level=1),
    mcq("Which Transformer family do almost all modern LLMs (GPT, Llama 3, Qwen3, DeepSeek-V3) belong to?",
        ["Decoder-only",
         "Encoder-only",
         "Encoder-decoder",
         "Recurrent (RNN)"], 0,
        "They read left to right and generate one token at a time.",
        "Decoder-only models use a causal mask (each token sees only earlier tokens) and generate autoregressively. Encoder-only (BERT) does not generate; encoder-decoder (T5) is used for translation/summarisation.",
        topic="families-tasks", level=1),
    tf("BERT, an encoder-only model, reads the whole input in both directions at once and is mainly used for classification, NER and embeddings rather than for writing long text.", True,
       "Bidirectional readers don't naturally generate.",
       "Encoder-only = bidirectional attention, trained with MLM. Strong at understanding tasks (classification, NER, embeddings for RAG search); not naturally generative.",
       topic="families-tasks", level=1),
    fill("Byte-level tokenization uses a base vocabulary of only ____ symbols, one per possible byte value.", "256",
         "A byte has 8 bits.",
         "2^8 = 256 byte values, so any text in any script can be written with them and nothing is ever out of vocabulary. The price: longer sequences.",
         topic="token-types", level=1),
    mcq("According to the course, the 'Large' in LLM refers to three things. Which list is right?",
        ["Parameters (billions), training data (trillions of tokens) and context window",
         "Parameters, GPU price and electricity bill",
         "Vocabulary size, number of languages and number of users",
         "Number of layers, number of heads and batch size only"], 0,
        "If it were only architecture, we'd just say 'Transformer LM'.",
        "The professor's point: 'Large' = billions of parameters (Llama 3 8B-405B), trillions of training tokens (Llama 3 ~15T, Qwen3 ~36T) and long context windows (2K for GPT-3 → 128K+).",
        topic="lm-basics", level=1),

    # ------------------------------------------------------------------ L2
    out('p_first = 0.2          # P(the)\n'
        'p_second = 0.5         # P(cat | the)\n'
        'p_third = 0.04         # P(sat | the cat)\n'
        'print(round(p_first * p_second * p_third, 4))',
        ["0.004", "0.74", "0.0133", "0.04"], 0,
        "Chain rule: multiply the conditional probabilities.",
        "P(w1 w2 w3) = P(w1) · P(w2 | w1) · P(w3 | w1 w2) = 0.2 × 0.5 × 0.04 = 0.004. Adding them (0.74) is the classic slip; probabilities of a sequence multiply.",
        diagram="""
P(the cat sat) = P(the) x P(cat | the) x P(sat | the cat)
               =  0.2   x     0.5     x      0.04
               =  0.004
""",
        topic="lm-basics", level=2),
    mcq("At each step an LLM outputs a probability for every token in its vocabulary. In ML terms, what kind of problem is one next-token step?",
        ["Classification with a softmax, where the classes are the vocabulary tokens",
         "Regression that predicts the token ID as a number",
         "Clustering of the input tokens",
         "Ranking of whole documents"], 0,
        "How many 'classes' does a 50,000-token vocabulary have?",
        "The LM head produces one logit per vocabulary token and softmax turns them into probabilities: a |V|-way classification. Predicting the ID as a number (regression) makes no sense because IDs carry no order.",
        topic="lm-basics", level=2),
    mcq("Why do LLMs usually SAMPLE the next token instead of always taking the single most likely one?",
        ["Many tokens are near-synonyms; sampling the 2nd or 3rd best gives variety, and that is what makes the model generative",
         "Sampling is always more accurate than taking the top token",
         "The top token is usually a special token",
         "Taking the top token is too slow to compute"], 0,
        "What would the output look like if it were always the top word?",
        "The course: sampling is what makes it generative. Always taking the top token (greedy) is deterministic and tends to be repetitive. Sampling is not 'more accurate'; it trades some precision for variety. Decoding strategies come in Module 4.",
        topic="lm-basics", level=2),
    mcq("How does the course phrase sentiment classification as next-word prediction for an LLM?",
        ["Compare P('positive' | \"The sentiment of the sentence 'I like Jackie Chan' is:\") with P('negative' | same prompt)",
         "Train a separate BERT classifier and call it from the LLM",
         "Count positive words in the sentence",
         "Ask the LLM to output the sentiment as a number from 0 to 1 and threshold it"], 0,
        "Any task = prompt + next word.",
        "Conditional generation: write a prompt whose natural next word is the label, then compare the label words' probabilities. One LLM, many tasks, via the prompt, instead of one fine-tuned model per task.",
        topic="lm-basics", level=2),
    out('word = "unhappiness!"\n'
        'print(len(word.split()), len(list(word)), len(word.encode("utf-8")))',
        ["1 12 12", "1 11 12", "4 12 12", "1 12 24"], 0,
        "Plain ASCII: one byte per character.",
        "Word-level: 1 token. Character-level: 12 characters (including '!'). Byte-level: 12 bytes, because every ASCII character is 1 byte in UTF-8. A subword tokenizer would give about 4 (un | happi | ness | !).",
        topic="token-types", level=2),
    out('for s in ["Apple", "क", "café"]:\n'
        '    print(s, len(s), len(s.encode("utf-8")))',
        ["Apple 5 5\nक 1 3\ncafé 4 5", "Apple 5 5\nक 1 1\ncafé 4 4", "Apple 5 5\nक 3 3\ncafé 4 5", "Apple 5 10\nक 1 2\ncafé 4 8"], 0,
        "ASCII = 1 byte, accented Latin = 2, Devanagari = 3.",
        "UTF-8 uses 1 byte for ASCII, 2 for 'é' and 3 for Devanagari 'क' (224 164 149 in the course slide). A byte-level tokenizer starts from these bytes, which is why Hindi text often costs more tokens than English.",
        topic="token-types", level=2),
    mcq("Which row of the course's tokenization table is correct?",
        ["Character-level: tiny vocabulary but long sequences (mainly research, e.g. CANINE)",
         "Word-level: tiny vocabulary and never any OOV",
         "Byte-level: vocabulary of about 50,000 and short sequences",
         "Subword: used only by research models, not by modern LLMs"], 0,
        "Smaller units = smaller vocabulary = longer sequences.",
        "Word: short sequences but OOV and a bloated vocab. Subword: the modern default. Character: tiny vocab, long sequences. Byte: vocab 256, never OOV, longest sequences (ByT5).",
        topic="token-types", level=2,
        diagram="""
unit:      word     subword     char      byte
vocab:     huge  >  ~32K-262K > ~100s  >  256
seq len:   short <  medium    < long   <  longest
OOV:       yes      rare        rare      never
"""),
    out('from collections import Counter\n'
        'words = {("h","u","g"): 10, ("p","u","g"): 5, ("p","u","n"): 12,\n'
        '         ("b","u","n"): 4, ("h","u","g","s"): 5}\n'
        'pairs = Counter()\n'
        'for w, f in words.items():\n'
        '    for a, b in zip(w, w[1:]):\n'
        '        pairs[a, b] += f\n'
        'print(pairs.most_common(3))',
        ["[(('u', 'g'), 20), (('p', 'u'), 17), (('u', 'n'), 16)]",
         "[(('u', 'n'), 16), (('u', 'g'), 15), (('h', 'u'), 15)]",
         "[(('u', 'g'), 3), (('u', 'n'), 2), (('p', 'u'), 2)]",
         "[(('h', 'u'), 15), (('u', 'g'), 20), (('p', 'u'), 17)]"], 0,
        "Each pair count is weighted by the word's frequency.",
        "(u,g) appears in hug 10 + pug 5 + hugs 5 = 20; (p,u) in pug 5 + pun 12 = 17; (u,n) in pun 12 + bun 4 = 16. So BPE's first merge is 'ug'. Counting each word once (3, 2, 2) forgets the frequencies.",
        topic="bpe", level=2),
    mcq("The course's toy BPE vocabulary after three merges is [b, g, h, n, p, s, u, ug, un, hug]. How does the segmenter split the new word 'bug'?",
        ["b ug",
         "bu g",
         "b u g",
         "[UNK]"], 0,
        "Replay the learned merges in order on b u g.",
        "Start from characters b u g; merge 1 (u,g) gives b ug; merges 'un' and 'hug' don't apply. So 'bug' → [b, ug]. 'bu' was never learned, and every character is in the vocab, so no [UNK].",
        diagram="""
merges (in order): 1 u+g  2 u+n  3 h+ug
b u g  --merge 1-->  b ug   (merges 2, 3 don't match)
""",
        topic="bpe", level=2),
    tf("In BPE, the pair (u, g) and the pair (g, u) are counted as the same pair.", False,
       "Does 'ug' spell the same as 'gu'?",
       "Pairs are ordered: (u, g) is 'u then g'. The professor stressed this in class: ug ≠ gu. Merges build on the previous iteration's symbols.",
       topic="bpe", level=2),
    mcq("Three tokenizers mark word pieces differently. Which matching is right?",
        ["WordPiece (BERT) '##ing' = continuation of a word; byte-level BPE (GPT, Llama, Qwen) 'Ġtasty' = token with a leading space; SentencePiece (T5, Gemma) '▁New' = space before the token",
         "'##' marks a leading space; 'Ġ' marks a continuation; '▁' marks an unknown token",
         "All three symbols mean 'unknown token'",
         "'Ġ' and '▁' mark the end of a sentence"], 0,
        "Two of them are about spaces, one about continuing a word.",
        "WordPiece marks the pieces that continue a word (to ##ken). Byte-level BPE folds the space into the next token and shows it as Ġ. SentencePiece replaces spaces with ▁ so it can work on raw text without a pre-tokenizer.",
        topic="markers-libs", level=2),
    tf("A byte-level BPE tokenizer (as in Llama, Qwen or DeepSeek) never needs an [UNK] token, because any text can fall back to its 256 base bytes.", True,
       "What is the smallest piece it can always use?",
       "Every character is some sequence of UTF-8 bytes, and all 256 bytes are in the base vocabulary. A brand-new word or script is never unknown; it just costs more tokens.",
       topic="markers-libs", level=2),
    mcq("You want to estimate how many tokens your prompts will cost on a hosted model whose tokenizer is available in tiktoken. You also want to train a custom tokenizer for your own model. Which tools match the course table?",
        ["tiktoken for counting the hosted model's tokens; Hugging Face `tokenizers` for training the custom one",
         "tiktoken for both: it can train new vocabularies too",
         "Hugging Face `transformers` for counting the hosted model; tiktoken for training",
         "Neither: tokenizers cannot be trained by users"], 0,
        "One of them can only encode and count.",
        "The course table: HF `tokenizers` = train or extend a tokenizer; HF `transformers` = load any Hub model's tokenizer and chat template; tiktoken = fast exact counting for those models, but it cannot train. With an API, the server tokenizes; you only count and trim.",
        topic="markers-libs", level=2),
    out('import numpy as np\n'
        'E = np.array([[0.34, -0.18], [0.92, 1.58], [1.28, -0.20], [-0.40, 0.97]])\n'
        'one_hot = np.array([0, 0, 1, 0])\n'
        'print(one_hot @ E)',
        ["[ 1.28 -0.2 ]", "[ 2.14  2.17]", "[ 0.92  1.58]", "[1.28]"], 0,
        "A one-hot vector times a matrix keeps exactly one row.",
        "one-hot (1 × |V|) × E (|V| × d) = row 2 of E, here 'fox' = [1.28, −0.20]. That is why real code skips the multiplication and just indexes the row: an embedding layer is a table lookup.",
        topic="embeddings", level=2),
    mcq("The course vocab is {brown: 0, dog: 1, fox: 2, jumps: 3, lazy: 4, over: 5} with d = 3. What is the shape of X for 'fox jumps over dog'?",
        ["4 × 3 (one row per token, one column per embedding dimension)",
         "3 × 4",
         "6 × 3 (the whole table)",
         "1 × 3 (one averaged vector)"], 0,
        "n tokens, each a d-dimensional row.",
        "IDs [2, 3, 5, 1] pick 4 rows of the 6 × 3 table, so X is n × d = 4 × 3. Nothing is averaged at this stage; each token keeps its own row.",
        topic="embeddings", level=2,
        diagram="""
E (|V| x d = 6 x 3)        IDs [2, 3, 5, 1]
0 brown  .34 -.18 -.17
1 dog    .92 1.58 1.30  <- 4th
2 fox   1.28 -.20 -.16  <- 1st     X = 4 x 3
3 jumps -.40  .97 -1.15 <- 2nd
4 lazy -1.16  .33 -.63
5 over -2.84 -.78 -1.41 <- 3rd
"""),
    tf("Running BPE on the corpus produces the vocabulary, the token IDs and the embedding vectors for each token.", False,
       "What does the tokenizer output, and what is trained later?",
       "BPE gives only the vocabulary, merge rules and IDs. Embedding vectors start random and are learned while training the MODEL. As the professor put it: the corpus is never trained, the model is trained.",
       topic="embeddings", level=2),
    out('import numpy as np\n'
        'a = np.array([1.0, 2.0])\n'
        'b = np.array([2.0, 4.0])\n'
        'c = np.array([-2.0, 1.0])\n'
        'cos = lambda x, y: x @ y / (np.linalg.norm(x) * np.linalg.norm(y))\n'
        'print(round(float(cos(a, b)), 2), round(float(cos(a, c)), 2))',
        ["1.0 0.0", "0.5 0.0", "1.0 -1.0", "10.0 0.0"], 0,
        "b is a scaled copy of a; c is perpendicular to a.",
        "cos(a, b) = 10 / (√5 · √20) = 1.0: same direction even though b is twice as long. a · c = −2 + 2 = 0, so cos = 0 (unrelated). 10.0 is the raw dot product, not the cosine.",
        topic="similarity", level=2),
    mcq("Inside an LLM, which vectors are static and which are contextual?",
        ["The input embedding table is static (one row per token); the hidden states after the Transformer layers are contextual",
         "Both the table and the hidden states are static",
         "The input embedding table is contextual; the hidden states are static",
         "Neither: LLMs have no embeddings"], 0,
        "Where does attention mix in the surrounding words?",
        "Looking up 'bank' always returns the same row of E. Each Transformer layer then mixes in the surrounding tokens through attention, so the hidden state for 'bank' differs between 'river bank' and 'bank loan'.",
        analogy="The embedding table is a static config map; the hidden states are the runtime values computed per request.",
        topic="similarity", level=2),
    mcq("Which matching of positional-encoding method to model is right?",
        ["Sinusoidal: original Transformer (2017); learned table: GPT-2 and BERT; RoPE: Llama, Qwen, DeepSeek",
         "Sinusoidal: Llama 3; learned: original Transformer; RoPE: BERT",
         "All modern LLMs use sinusoidal encodings",
         "RoPE: GPT-2; learned: Llama; sinusoidal: DeepSeek"], 0,
        "Which one is the modern default?",
        "Sinusoidal = fixed sines/cosines added to the input (Vaswani 2017). Learned = a trainable vector per position, added (GPT-2, BERT; less common now). RoPE = rotate Q and K in every attention layer (Llama, Qwen, DeepSeek).",
        diagram="""
sinusoidal:  X = E[ids] + PE_fixed     (input, added)
learned:     X = E[ids] + P[pos]       (input, added)
RoPE:        q, k rotated by pos*theta (every attn layer)
""",
        topic="positional", level=2),
    tf("Sinusoidal positional encodings have no trainable parameters: each position's vector is computed from fixed sine and cosine formulas.", True,
       "Is there anything to learn in sin(pos / 10000^(2i/d))?",
       "Sinusoidal encodings are fully deterministic. Learned positional embeddings are the variant with a trainable table, one vector per position.",
       topic="positional", level=2),
    tf("The context window limit applies to the prompt and the generated answer together, not to the prompt alone.", True,
       "Where does each generated token go before the next step?",
       "Generation is autoregressive: every new token is appended to the input. So the window must hold query + output in one call, which the professor flagged as 'very important' in Session 3.",
       analogy="Like a fixed-size buffer that holds both the request and the response being written into it.",
        topic="context-window", level=2),
    mcq("A model has an 8,192-token context window. Your system prompt plus retrieved documents take 7,000 tokens. What is the most the model can generate in this call?",
        ["About 1,192 tokens",
         "8,192 tokens: the output has its own separate budget",
         "7,000 tokens",
         "Unlimited, as long as you stream the output"], 0,
        "Prompt + output share the window.",
        "8,192 − 7,000 = 1,192 tokens left for the answer. Streaming changes how tokens are delivered, not how many fit.",
        diagram="""
|<------------------ 8,192 tokens ------------------>|
| system + docs: 7,000              | answer: 1,192 |
""",
        topic="context-window", level=2),
    mcq("Which pairing of family, attention and training objective matches the course's review table?",
        ["Encoder-only: bidirectional, MLM · Decoder-only: causal mask, CLM · Encoder-decoder: bidirectional encoder + causal decoder with cross-attention, span corruption / seq2seq",
         "Encoder-only: causal mask, CLM · Decoder-only: bidirectional, MLM · Encoder-decoder: no attention",
         "All three use a causal mask and CLM",
         "Encoder-only: cross-attention, span corruption · Decoder-only: bidirectional, MLM · Encoder-decoder: causal, CLM"], 0,
        "BERT masks tokens; GPT predicts the next one.",
        "BERT (encoder-only) sees both sides and fills masked tokens (MLM). GPT/Llama (decoder-only) see only the past and predict the next token (CLM). T5/BART (encoder-decoder) read bidirectionally and write causally, linking the two with cross-attention.",
        topic="families-tasks", level=2,
        diagram="""
encoder-only   [a b c d]  every token sees all   (BERT)
decoder-only   a -> b -> c -> d   past only      (GPT)
enc-dec        [read all] ==cross-attn==> write  (T5)
"""),
    mcq("An NER system must tag '[Charles Darwin]PERSON published in [London]LOCATION in [1859]DATE'. How does the course say an LLM can do this without a task-specific model?",
        ["Prompt it to return the entities as structured (JSON) output",
         "It cannot: NER always needs a separate CRF model",
         "Ask it to translate the sentence into entity IDs",
         "Use only its tokenizer, since tokens are entities"], 0,
        "LLMs do NLU by generating the answer.",
        "NER is an NLU task, but an LLM can do it by generating: a prompt plus a JSON output format, as used for invoices and contracts. An encoder-only model (BERT) fine-tuned for token classification is the classic cheaper alternative.",
        topic="families-tasks", level=2),
    mcq("According to the course, what is the main reason Transformers replaced RNNs/LSTMs for language modelling?",
        ["Parallelisation: self-attention processes all tokens of a sequence together, while an RNN goes one token at a time",
         "Transformers need no training data",
         "Transformers have smaller vocabularies",
         "RNNs cannot represent probabilities"], 0,
        "Think GPU utilisation during training.",
        "An RNN must finish token t before t+1, so training is sequential. Self-attention computes all positions at once, which maps well to GPUs and made billion-parameter training practical. (Hybrids such as Jamba add Mamba state-space layers back for long-context memory.)",
        diagram="""
RNN:          t1 -> t2 -> t3 -> t4   (one after another)
Transformer:  t1  t2  t3  t4          (all at once)
              +--- attention ---+
""",
        analogy="An RNN is a single checkout queue; attention is opening a till for every customer at once.",
        topic="lm-basics", level=2),
    fill("The final part of an LLM that turns the last hidden state into one score per vocabulary token, then a softmax, is called the language-modelling ____.", "head",
         "LM ____.",
         "LM head = unembedding (a d × |V| matrix giving logits) + softmax (probabilities). Those probabilities score text or are sampled to generate.",
         topic="pipeline", level=2),
    mcq("The course says raw files are not yet a 'corpus'. What turns them into one?",
        ["Pre-processing: collecting the documents and cleaning/de-duplicating them",
         "Training the LLM on them",
         "Translating them into English",
         "Tokenizing them with the model's tokenizer only"], 0,
        "Session 1 defines corpus = documents after ...",
        "Corpus = documents (PDFs, emails, web pages, chats) after pre-processing. The cleaning steps (filter, de-duplicate, remove PII) are covered in Module 2.",
        topic="pipeline", level=2),
    fill("Llama 3 8B has |V| = 128,256 and d = 4096. Its input embedding table has about ____ million parameters (nearest whole number).", "525",
         "|V| × d.",
         "128,256 × 4096 = 525,336,576 ≈ 525M. The LM head (d × |V|) is the same size again unless its weights are tied to E.",
         topic="embeddings", level=2),
    tf("In a decoder-only LLM, the residual stream means each sub-layer ADDS its output to the running vector X instead of replacing it.", True,
       "x = x + sublayer(x).",
       "Residual connections compute X + Attention(X) and X + FFN(X). Information from earlier layers is kept and refined, which also helps gradients flow in deep stacks.",
       topic="pipeline", level=2,
       analogy="Like appending commits to a branch rather than overwriting the file each time."),
    mcq("Why is a 1,000-token answer slower to generate than a 100-token answer, even with the same prompt?",
        ["Each generated token needs one full forward pass of the model, run one after another",
         "Long answers use a bigger vocabulary",
         "The tokenizer is slower on long text",
         "The model re-reads its training data for longer answers"], 0,
        "Autoregressive = one step per token.",
        "Generation is serial: token t+1 depends on token t. 1,000 output tokens = 1,000 sequential passes. This is the root of inference cost and of tricks like KV caching (Module 4).",
        topic="lm-basics", level=2),

    # ------------------------------------------------------------------ L3
    mcq("In the course BPE example, after the first merge 'ug' (20), a classmate says the next merge must be 'pu', because (p, u) had a count of 17. Why is that wrong?",
        ["Pair counts are recomputed after each merge: pug is now p + ug, so (p, u) only appears in pun (12) and 'un' (16) wins",
         "Because 'pu' is not a real English syllable, BPE skips it",
         "Because BPE always merges pairs that contain the last merged token",
         "The classmate is right; the slide is wrong"], 0,
        "Rewrite the words after merging ug, then count again.",
        "After merging, the words are h ug, p ug, p u n, b u n, h ug s. (p, u) survives only in pun: 12. (u, n) = 12 + 4 = 16 and (h, ug) = 15. So real BPE does give ug → un → hug. In an exam, show the recomputed counts.",
        analogy="Like re-running a query after an UPDATE: the old counts are stale the moment you merge.",
        topic="bpe", level=3,
        diagram="""
before: h u g | p u g | p u n | b u n | h u g s
merge (u,g)=20
after:  h ug  | p ug  | p u n | b u n | h ug s
recount: (u,n)=16  (h,ug)=15  (p,u)=12  (p,ug)=5
"""),
    out('from collections import Counter\n'
        'w = {"h u g": 10, "p u g": 5, "p u n": 12, "b u n": 4, "h u g s": 5}\n'
        'merges = []\n'
        'for _ in range(4):\n'
        '    c = Counter()\n'
        '    for s, f in w.items():\n'
        '        for pair in zip(s.split(), s.split()[1:]):\n'
        '            c[pair] += f\n'
        '    a, b = c.most_common(1)[0][0]\n'
        '    merges.append(a + b)\n'
        '    w = {s.replace(f"{a} {b}", a + b): f for s, f in w.items()}\n'
        'print(merges)',
        ["['ug', 'un', 'hug', 'pun']", "['ug', 'pu', 'un', 'hug']", "['ug', 'un', 'hug', 'hugs']", "['ug', 'un', 'pu', 'hug']"], 0,
        "After hug, look at what is left: p ug (5), p un (12), b un (4), hug s (5).",
        "Merges 1-3 match the slide (ug 20, un 16, hug 15). Then the remaining pairs are (p, un) 12, (p, ug) 5, (hug, s) 5, (b, un) 4, so merge 4 is 'pun'. 'hugs' (5) loses to 'pun' (12).",
        topic="bpe", level=3),
    mcq("With the course's character-based toy vocabulary [b, g, h, n, p, s, u, ug, un, hug], the segmenter meets 'mug'. What happens, and what is the fix the course gives?",
        ["'m' is not in the vocabulary, so it becomes [UNK]; the fix is to start from the 256 bytes instead of characters (byte-level BPE)",
         "'mug' becomes 'm ug' with 'm' added to the vocabulary automatically",
         "'mug' becomes 'hug' because it is the closest token",
         "The segmenter crashes; the fix is a bigger target vocabulary"], 0,
        "Which base symbol is missing?",
        "The base alphabet came from the training words, which had no 'm'. So 'm' → [UNK] and the segment is [UNK] ug. Starting from all 256 bytes means every character is representable, so byte-level BPE never needs [UNK].",
        topic="bpe", level=3),
    mcq("Which two settings does the course name as BPE hyper-parameters?",
        ["The target vocabulary size and a minimum pair frequency",
         "The learning rate and the batch size",
         "The embedding dimension d and the number of layers",
         "The temperature and top-p"], 0,
        "When do you stop merging, and which pairs are too rare to merge?",
        "BPE stops at the target vocab size (or number of merges) and can skip pairs below a minimum frequency. Learning rate, d and temperature belong to the model or decoding, not the tokenizer.",
        topic="bpe", level=3),
    fill("A BPE learner starts from 256 byte tokens, performs 50,000 merges, and adds one special end-of-text token. The vocabulary size is ____.", "50257",
         "Base + one new token per merge + specials.",
         "256 + 50,000 + 1 = 50,257: exactly GPT-2's byte-level BPE vocabulary, as the old-batch slides note. Each merge adds one token.",
         topic="markers-libs", level=3),
    mcq("BPE and WordPiece train in a similar loop. What is the difference in how WordPiece chooses the pair to merge?",
        ["WordPiece scores a pair by its frequency relative to the frequencies of its parts (a likelihood score), so it prefers pairs whose parts are rare on their own; BPE just takes the most frequent pair",
         "WordPiece merges the least frequent pair",
         "WordPiece chooses pairs at random",
         "There is no difference; only the '##' marker differs"], 0,
        "count(ab) / (count(a) · count(b)).",
        "WordPiece's score ≈ freq(pair) / (freq(first) × freq(second)). A pair of two very common symbols can lose to a less frequent pair of rare symbols. The old-batch slide: 'likelihood-based scoring distinguishes it from BPE's simpler frequency-based approach'.",
        topic="markers-libs", level=3),
    mcq("Why is SentencePiece popular for languages such as Chinese, Japanese and Thai?",
        ["It is language-agnostic and needs no pre-tokenizer: it works on raw text and treats the space as an ordinary symbol (▁)",
         "It contains a built-in Chinese dictionary",
         "It always uses one token per character",
         "It only works with WordPiece"], 0,
        "These scripts don't put spaces between words.",
        "BPE normally pre-tokenizes on whitespace first. SentencePiece skips that, learning BPE or Unigram directly from raw text with spaces encoded as ▁, which suits scripts without word spaces. Used by T5, Gemma and Llama 1/2.",
        topic="markers-libs", level=3),
    out('import math\n'
        'd = 4\n'
        'def pe(pos, k):\n'
        '    i = k // 2\n'
        '    angle = pos / 10000 ** (2 * i / d)\n'
        '    return math.sin(angle) if k % 2 == 0 else math.cos(angle)\n'
        'print([round(pe(2, k), 2) for k in range(d)])',
        ["[0.91, -0.42, 0.02, 1.0]", "[0.91, 0.91, 0.02, 0.02]", "[0.03, 1.0, 0.0, 1.0]", "[0.91, -0.42, 0.91, -0.42]"], 0,
        "Dimensions 0-1 use angle 2; dimensions 2-3 use angle 2/100.",
        "i = 0: sin 2 ≈ 0.91, cos 2 ≈ −0.42 (the course's sample). i = 1: angle = 2 / 10000^(2/4) = 0.02, so sin ≈ 0.02 and cos ≈ 1.0. Higher dimensions rotate more slowly, which lets the encoding carry both fine and coarse position.",
        topic="positional", level=3),
    mcq("How does RoPE differ from sinusoidal and learned positional encodings in WHERE it acts?",
        ["It is not added to the input embeddings; it rotates the query and key vectors inside every attention layer",
         "It is added to the output logits",
         "It replaces the token embeddings entirely",
         "It is a separate token inserted between words"], 0,
        "Which vectors meet in the attention score q · k?",
        "Sinusoidal and learned encodings are added once to X at the input. RoPE multiplies Q and K in each attention layer by a position-dependent rotation, so the score q·k depends on the relative distance between tokens.",
        topic="positional", level=3,
        analogy="Learned/sinusoidal = a seat number on each guest's badge; RoPE = turn each guest by an angle so any two can tell how far apart they sit."),
    tf("A model with learned absolute positional embeddings trained up to position 2,048 has a trained vector for position 3,000 too, so longer inputs work out of the box.", False,
       "Which rows of the position table were ever trained?",
       "A learned table has rows only up to the training length; positions beyond it either don't exist or were never trained. The old-batch slides note the same limit for sinusoidal ('positions beyond training length have never been seen'). RoPE-based models are easier to extend.",
       topic="positional", level=3),
    out('V, d = 128_256, 4096\n'
        'embed = V * d\n'
        'head = d * V\n'
        'print(round((embed + head) / 1e9, 2), round(embed / 1e9, 2))',
        ["1.05 0.53", "0.53 0.53", "1.05 1.05", "0.26 0.53"], 0,
        "The LM head is d × |V|.",
        "E (|V| × d) ≈ 0.53B and an untied LM head (d × |V|) ≈ 0.53B, so ≈ 1.05B of an '8B' model sits in vocabulary-sized matrices. With weight tying (head = Eᵀ) only one copy, ≈ 0.53B, is stored. This is why a bigger vocabulary makes a model bigger: two layers depend on |V|.",
        topic="embeddings", level=3),
    mcq("During TRAINING, how many positions of a length-n sequence get next-token logits from the LM head, and during INFERENCE which position's logits are used?",
        ["Training: all n positions in parallel; inference: only the last position",
         "Training: only the last position; inference: all n positions",
         "Both: only the first position",
         "Both: all n positions, averaged"], 0,
        "Training wants n predictions per pass; generation wants one next token.",
        "With the causal mask, position t has seen only tokens ≤ t, so every position gives a valid next-token prediction and training gets n losses in one pass. At inference only the last hidden state has seen the whole prompt, so its logits pick the next token.",
        topic="pipeline", level=3),
    mcq("A team compares two tokenizers on the same Hindi customer-chat data: tokenizer A (32K vocab, mostly English training text) gives 3× more tokens per message than tokenizer B (150K vocab, trained on many languages). What does this mean in practice?",
        ["With A, the same Hindi conversation costs ~3× more per call, fills the context window ~3× faster and is slower to generate",
         "Nothing: tokens are free, only words are billed",
         "A is always better because a smaller vocabulary means a smaller model",
         "B must have a bug, since more vocabulary should mean more tokens"], 0,
        "Everything (price, window, speed) is counted in tokens.",
        "A tokenizer trained mostly on English has few Hindi merges, so Hindi text falls back to small pieces (down to UTF-8 bytes). More tokens = higher price, a context window that fills sooner and more decode steps. B pays for this with a bigger embedding table and LM head.",
        diagram="""
same Hindi message
tokenizer A (32K, English-heavy): ############ 3x tokens
tokenizer B (150K, multilingual): ####         1x
cost, window use, decode steps all scale with tokens
""",
        topic="token-types", level=3),
    tf("Making a BPE vocabulary bigger (more merges) shortens the token sequences but enlarges both the embedding table and the LM head.", True,
       "Count which matrices have a |V| dimension.",
       "More merges → common strings become single tokens → shorter sequences. But E is |V| × d and the head is d × |V|, so parameters grow linearly with |V|. Llama 3 (128K) and Gemma 3 (262K) chose large vocabularies for multilingual efficiency.",
       analogy="A bigger vocabulary is like a bigger dictionary-based compressor: shorter output, but a heavier dictionary to ship.",
        topic="token-types", level=3),
    mcq("A bank wants to classify short customer complaints into 12 fine-grained sentiment categories, with millions of messages a day and a tight latency budget. Which architecture family and model fit best?",
        ["Encoder-only, e.g. BERT/RoBERTa with a classification head: bidirectional context, small and fast for a fixed label set",
         "Decoder-only, e.g. a 70B Llama prompted for every message",
         "Encoder-decoder, e.g. T5, because it can generate the label",
         "No Transformer; use a sinusoidal encoder"], 0,
        "Understanding, fixed labels, huge volume.",
        "Classification is NLU. An encoder-only model reads the whole text in both directions and a small classifier head on top is cheap at scale. A big decoder LLM can do it via prompting, but the course stresses 'you don't have to use an LLM everywhere': cost decides.",
        analogy="Using a 70B decoder for 12-way classification is like spinning up a full app server to evaluate a regex.",
        topic="families-tasks", level=3),
    mcq("A developer-tools company wants inline Python code completion as the user types in their IDE. Which family fits, and why?",
        ["Decoder-only (e.g. a Llama/Qwen-style code model): it predicts the next token left to right, exactly what completion needs",
         "Encoder-only (e.g. BERT): it reads both directions, so it sees the code after the cursor",
         "Encoder-decoder (e.g. T5), because code is a translation from English",
         "Any family works equally; only vocabulary size matters"], 0,
        "Completion = continue the text.",
        "Code completion is open-ended generation, autoregressive by nature: decoder-only with CLM training. Encoder-only models are not naturally generative. (Fill-in-the-middle tricks also run on decoder-only models by reordering the input.)",
        topic="families-tasks", level=3),
    mcq("A service must translate German support queries into English for US agents. Which family is the classic fit named by the course?",
        ["Encoder-decoder (e.g. T5, BART, or the original 2017 Transformer): the encoder reads the German, the decoder writes English using cross-attention",
         "Encoder-only (BERT): bidirectional reading is all translation needs",
         "Decoder-only only, because encoder-decoder models cannot translate",
         "A static word2vec model"], 0,
        "Input sequence in, a different output sequence out.",
        "Seq2seq tasks (translation, summarisation) are what encoder-decoders were built for: bidirectional encoding of the source plus causal decoding with cross-attention. Modern decoder-only LLMs also translate well via prompting; in the exam, name encoder-decoder and a model such as T5/mBART.",
        topic="families-tasks", level=3),
    mcq("Why does the course say encoder-only models generally give richer contextual embeddings than decoder-only models?",
        ["The decoder's causal mask lets each token see only earlier tokens, while an encoder token sees the whole sentence",
         "Decoder-only models have no embedding table",
         "Encoder-only models use bigger vocabularies",
         "Decoders are trained with MLM, which removes context"], 0,
        "What can the first token of a sentence see in each family?",
        "In a decoder, the vector for 'bank' at position 2 has seen only positions 1-2; in an encoder it has seen the full sentence, both sides. That is why BERT-style models still power embedding search for RAG.",
        analogy="A decoder reads a sentence like a live log tail; an encoder reads the whole file before deciding.",
        topic="similarity", level=3),
    mcq("A RAG system must match 'How do I reset my password?' with a help article titled 'I forgot my login details'. Why does embedding similarity work here when keyword matching fails?",
        ["The two texts share almost no words, but their embeddings point in similar directions because they mean similar things",
         "Embeddings copy the exact words, so they share more tokens",
         "Cosine similarity rewards longer documents",
         "Keyword matching cannot handle question marks"], 0,
        "Semantic similarity = closeness of meaning.",
        "Semantic similarity measures meaning, not shared words. Cosine on embeddings scores these two high even with no word overlap, which is the basis of RAG retrieval (Module 8). Cosine also ignores length, so long documents are not favoured by default.",
        topic="similarity", level=3),
    out('import math\n'
        'short = [0.2, 0.1]\n'
        'long = [0.6, 0.5, 0.5]\n'
        'print(round(math.prod(short), 3), round(math.prod(long), 3))\n'
        'print(round(sum(math.log(p) for p in long), 2))',
        ["0.02 0.15\n-1.9", "0.15 0.02\n-1.9", "0.02 0.15\n1.9", "0.3 1.6\n-1.9"], 0,
        "Multiply probabilities; logs turn the product into a sum.",
        "Short: 0.2 × 0.1 = 0.02. Long: 0.6 × 0.5 × 0.5 = 0.15. The longer sentence is MORE probable here because its tokens are each likely. Real code sums log-probabilities (−0.51 − 0.69 − 0.69 ≈ −1.9) because multiplying thousands of small numbers underflows to 0.",
        topic="lm-basics", level=3),
    mcq("A model's context window is 4,096 tokens. Each turn of a chat app re-sends the whole history. After 5 turns the history is 3,800 tokens and the user asks for a 500-token answer. What happens, and what is the usual fix?",
        ["Prompt + answer = 4,300 > 4,096, so the answer is cut short (or the call fails); trim or summarise the oldest turns",
         "The model reads the history in a second pass, so nothing breaks",
         "Only the answer is limited to 4,096, so it works",
         "The tokenizer compresses the history automatically"], 0,
        "Add the prompt and the requested output.",
        "The window holds query + output in one call. 3,800 + 500 exceeds 4,096, so at most 296 tokens can be generated. Chat apps drop or summarise old turns (keeping the system prompt) to stay inside the window.",
        topic="context-window", level=3),
    tf("Because generation is autoregressive, the sequence the model attends over grows by one token with every token it generates.", True,
       "Where does each output token go?",
       "Each new token is appended to the input for the next step, so the context grows during generation. This is why the window limit covers the output and why long outputs get progressively more expensive (Module 4: KV cache).",
       topic="context-window", level=3),

    # ------------------------------------------------------------------ L4
    out('V, d = 50_000, 4096\n'
        'untied = 2 * V * d\n'
        'tied = V * d\n'
        'print(f"{V}x{d}", f"{d}x{V}", round((untied - tied) / 1e6, 1))',
        ["50000x4096 4096x50000 204.8", "50000x4096 50000x4096 204.8", "50000x4096 4096x50000 409.6", "4096x50000 50000x4096 102.4"], 0,
        "E is |V| × d; the unembedding is its transpose.",
        "E = [50,000 × 4,096], Eᵀ = [4,096 × 50,000]. Weight tying makes the LM head reuse E, saving |V| × d = 204.8M parameters (the old-batch answer key rounds it to ~205M). The tied matrix must be good at both reading and writing tokens.",
        topic="pipeline", level=4),
    mcq("In the old-batch practice question, h (the final hidden state at position N) has shape [1 × 4,096] and |V| = 50,000 with tied weights. Which line gives the logits and the probabilities correctly?",
        ["u = h · Eᵀ, shape [1 × 50,000]; y = softmax(u)",
         "u = h · E, shape [1 × 4,096]; y = softmax(u)",
         "u = Eᵀ · h, shape [4,096 × 1]; y = argmax(u)",
         "u = h · Eᵀ, shape [50,000 × 4,096]; y = sigmoid(u)"], 0,
        "[1 × d] × [d × |V|] = ?",
        "The unembedding is Eᵀ (d × |V|), so u = h · Eᵀ is a 1 × |V| logit vector, one score per vocabulary token, and softmax gives a distribution. Using E itself doesn't match shapes; sigmoid would not give a distribution over tokens.",
        diagram="""
h [1 x 4096]  x  E^T [4096 x 50000]  =  u [1 x 50000]
                                         |
                                  softmax -> y
""",
        topic="pipeline", level=4),
    out('import numpy as np\n'
        'def rot(v, pos, theta=0.5):\n'
        '    a = pos * theta\n'
        '    R = np.array([[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]])\n'
        '    return R @ v\n'
        'q = np.array([1.0, 0.0])\n'
        'k = np.array([0.6, 0.8])\n'
        's1 = rot(q, 5) @ rot(k, 3)\n'
        's2 = rot(q, 12) @ rot(k, 10)\n'
        's3 = rot(q, 12) @ rot(k, 3)\n'
        'print(round(float(s1), 3), round(float(s2), 3), round(float(s3), 3))',
        ["0.997 0.997 -0.909", "0.6 0.6 0.6", "0.997 -0.909 0.997", "0.997 0.997 0.997"], 0,
        "Rotating q by m·θ and k by n·θ leaves an angle of (m − n)·θ between them.",
        "s1 (positions 5, 3) and s2 (12, 10) both have offset 2, so the scores are identical; s3 (offset 9) differs. That is RoPE's key property: the q·k score depends only on the relative distance, not on absolute positions.",
        topic="positional", level=4,
        diagram="""
pos 3:  k rotated by 3θ       pos 5: q rotated by 5θ
pos 10: k rotated by 10θ      pos 12: q rotated by 12θ
angle between q and k = (5-3)θ = (12-10)θ = 2θ
=> same attention score for the same offset
"""),
    mcq("A team swaps the sinusoidal encoding of a small Transformer for RoPE and notices that the input embeddings X entering layer 1 are now identical for the same token at every position. Is that a bug?",
        ["No: RoPE adds nothing to X; position enters only when Q and K are rotated inside each attention layer",
         "Yes: every position must have a different input vector",
         "Yes: RoPE should be added to X before layer 1",
         "No, but only because RoPE is learned and starts at zero"], 0,
        "Where does RoPE act?",
        "With RoPE the input X is just the token-embedding lookup, the same row for the same token. Position is injected later by rotating Q and K by position-dependent angles. RoPE has no learned parameters in its standard form.",
        topic="positional", level=4),
    mcq("A BPE tokenizer learned the merges in this order: 1. (e, s) 2. (es, t) 3. (l, o) 4. (lo, w) 5. (w, e). A teammate's re-implementation segments 'west' by greedily taking the longest vocabulary token from the left. The real segmenter applies merges in learned order. What do they each output?",
        ["Real: w est (merge 2 makes 'est' before merge 5 is reached); greedy longest-match: we s t",
         "Both give 'we st'",
         "Real: we st; greedy: w est",
         "Both give 'west' as one token"], 0,
        "Apply merges by priority, lowest number first, wherever they occur.",
        "w e s t: merge 1 (e, s) → w es t; merge 2 (es, t) → w est; merges 3-4 don't match; merge 5 (w, e) no longer applies because 'e' is already inside 'est'. Greedy longest-match from the left grabs 'we' (vocab token) then s, t. Same vocabulary, different splits: the merge order IS the tokenizer.",
        topic="bpe", level=4),
    tf("After a model is trained, you can safely add 20,000 new tokens to its vocabulary and use them immediately with no further training.", False,
       "What would the rows for the new tokens contain?",
       "The vocabulary is fixed when the tokenizer is trained; adding tokens means new rows in E and the LM head that were never trained (random or averaged), plus shifted segmentation of existing text. Using them requires further training, which is why each model ships with its own tokenizer.",
       topic="token-types", level=4),
    mcq("You load the weights of model A but accidentally tokenize with model B's tokenizer, which happens to have the same vocabulary size. What goes wrong?",
        ["The same ID means a different string in B, so A looks up the wrong embedding rows: the input is effectively scrambled and the output is nonsense",
         "Nothing: same vocabulary size means the tokenizers are interchangeable",
         "Only speed suffers, because B's merges are slower",
         "It raises an error because the IDs are out of range"], 0,
        "Token ID 4521 in A and 4521 in B: same string?",
        "Each publisher trains its own tokenizer; IDs are positions in that tokenizer's vocabulary. With equal |V| no index error is raised, so the bug is silent: rows of A's table are fetched for unrelated strings. The course rule: at inference, always use the model's own tokenizer.",
        analogy="Like joining two tables on an ID column that comes from a different database: no error, wrong rows.",
        topic="markers-libs", level=4),
    out('text = "नमस्ते"\n'
        'chars = len(text)\n'
        'nbytes = len(text.encode("utf-8"))\n'
        'print(chars, nbytes, nbytes // chars)',
        ["6 18 3", "1 6 6", "6 6 1", "3 18 6"], 0,
        "Count Unicode code points, not visible letters: Devanagari uses combining signs.",
        "'नमस्ते' is 6 code points (न म स ् त े, including the virama and vowel sign), each 3 bytes in UTF-8 → 18 bytes. With no learned Hindi merges, a byte-level tokenizer's worst case is 18 tokens for one word, against 1 for a common English word.",
        topic="token-types", level=4),
    out('pair = {("u", "g"): 20, ("p", "u"): 17, ("u", "n"): 16, ("h", "u"): 15, ("g", "s"): 5}\n'
        'sym = {"u": 36, "g": 20, "p": 17, "n": 16, "h": 15, "s": 5}\n'
        'bpe = max(pair, key=pair.get)\n'
        'wp = max(pair, key=lambda p: pair[p] / (sym[p[0]] * sym[p[1]]))\n'
        'print(bpe, wp)',
        ["('u', 'g') ('g', 's')", "('u', 'g') ('u', 'g')", "('g', 's') ('u', 'g')", "('u', 'g') ('p', 'u')"], 0,
        "WordPiece divides the pair count by the product of its parts' counts.",
        "BPE takes the raw maximum, (u, g) = 20. WordPiece scores: ug 20/(36·20) ≈ 0.028, pu 17/(17·36) ≈ 0.028, gs 5/(20·5) = 0.05. So WordPiece merges the rare-but-always-together pair (g, s) first. Same corpus, different first merge: that is the 'likelihood vs frequency' difference.",
        topic="markers-libs", level=4),
    out('old_V, new_V, d = 32_000, 128_256, 4096\n'
        'extra = (new_V - old_V) * d * 2   # embedding table + untied LM head\n'
        'print(round(extra / 1e6), "M")',
        ["789 M", "394 M", "525 M", "1051 M"], 0,
        "Both vocabulary-sized matrices grow.",
        "Going from a Llama 2-sized vocabulary (32K) to Llama 3's 128,256 adds 96,256 rows to E and 96,256 columns to the LM head: 96,256 × 4096 × 2 ≈ 789M parameters. Forgetting the head gives 394M, the common wrong answer.",
        topic="embeddings", level=4),
    fill("A model gives P('I am') = 0.04 and P('I am teaching') = 0.002. By the chain rule, P('teaching' | 'I am') = ____.", "0.05",
         "P(a, b) = P(a) · P(b | a), so P(b | a) = P(a, b) / P(a).",
         "0.002 / 0.04 = 0.05, the course's own number for P(teaching | I am). Running the chain rule backwards like this is how an LM's sentence scores and next-token probabilities stay consistent.",
         topic="lm-basics", level=4),
    mcq("Spot the common wrong answer. A student writes: 'To compare two candidate replies, pick the one with the higher total probability P(w1..wn).' What is the flaw?",
        ["The product of n probabilities (each < 1) shrinks with every extra token, so the total probability favours short replies; compare per-token averages of log-probability instead",
         "There is no flaw: total probability is always the right comparison",
         "Probabilities can't be multiplied for text",
         "The flaw is that LLMs do not output probabilities"], 0,
        "What happens to a product when you multiply in one more number below 1?",
        "Every extra token multiplies in a factor ≤ 1, so longer texts almost always score lower. Dividing the log-probability by the number of tokens (the average NLL, i.e. the log of perplexity in Module 2) removes the length bias. Beam search uses length normalisation for the same reason.",
        topic="lm-basics", level=4),
    out('import numpy as np\n'
        'n = 5\n'
        'causal = np.tril(np.ones((n, n), dtype=int))\n'
        'bidir = np.ones((n, n), dtype=int)\n'
        'print(int(causal.sum()), int(bidir.sum()), causal[1].tolist())',
        ["15 25 [1, 1, 0, 0, 0]", "10 25 [1, 1, 0, 0, 0]", "15 25 [0, 1, 1, 1, 1]", "25 25 [1, 1, 1, 1, 1]"], 0,
        "np.tril keeps the diagonal and everything below it.",
        "A causal mask lets token i attend to positions 0..i: 1 + 2 + ... + 5 = 15 allowed pairs, and row 1 (the second token) sees positions 0 and 1 only. Bidirectional (encoder) attention allows all 25. This is the mid-sem 'bidirectional vs causal' point in one picture.",
        topic="families-tasks", level=4,
        diagram="""
causal (decoder)      bidirectional (encoder)
1 0 0 0 0             1 1 1 1 1
1 1 0 0 0             1 1 1 1 1
1 1 1 0 0             1 1 1 1 1
1 1 1 1 0             1 1 1 1 1
1 1 1 1 1             1 1 1 1 1
"""),
    mcq("Spot the common wrong answer for 'Why not use encoder-decoder models for everything, since they have both halves?'",
        ["Two stacks mean more training cost and more latency, and for open-ended generation a single decoder-only stack does the job; for pure classification an encoder alone is cheaper",
         "Encoder-decoder models cannot generate text",
         "Encoder-decoder models have no attention",
         "Encoder-decoder models can only be used for images"], 0,
        "Check the 'weak at' row of the course table.",
        "The course table lists encoder-decoder's weakness as 'two stacks → more training cost and latency'. Decoder-only is weaker at classification efficiency; encoder-only is not naturally generative. Pick the family by task and cost, not by 'more parts is better'.",
        topic="families-tasks", level=4),
    mcq("A model was pre-trained with an 8K context window. A team sets max_length = 128K at inference and feeds it a 100K-token contract. Answers about the end of the contract are poor. What does the course's material point to?",
        ["The model never trained on positions beyond ~8K; long-context ability is built by a staged training curriculum (Llama 3 went 8K → 128K in six stages), not by a config flag",
         "The tokenizer cannot handle more than 8K tokens",
         "Context windows only limit output, so the cause must be the prompt wording",
         "Sinusoidal encodings are always used for long inputs, which are less accurate"], 0,
        "Which positions did the model actually see during training?",
        "Positional patterns beyond the training length were never learned. Llama 3 and Qwen3 extend the window with a dedicated long-context stage near the end of pre-training. Raising a limit in the config does not create that ability.",
        analogy="Raising max_length is like raising a web server's request-size limit: the handler still has to cope with payloads it never saw in testing.",
        topic="context-window", level=4),
    mcq("A search team embeds documents with an encoder and ranks them by raw dot product. Long, rambling documents keep winning over short, precise ones. Which change is the course's standard fix, and why?",
        ["Use cosine similarity (or normalise vectors first): it divides out vector length, so only direction (meaning) counts",
         "Use a bigger vocabulary",
         "Switch to a decoder-only model's input embedding table, which is contextual",
         "Add positional encodings to the document vectors"], 0,
        "a · b = |a||b| cos θ.",
        "The dot product grows with vector length, which can track document length or token count. Cosine = a·b / (|a||b|) ranks by angle only. The tempting 'use the LLM's input embedding table' is wrong twice: that table is static, and decoder states see only the past.",
        topic="similarity", level=4),
    mcq("A batch of 8 sequences, each 512 tokens, enters a model with d = 4096. What is the shape of the embedded input, and roughly how much memory does it take in 16-bit precision?",
        ["8 × 512 × 4096, about 34 MB",
         "512 × 4096, about 4 MB",
         "8 × 4096, about 66 KB",
         "8 × 512 × 128,256, about 1 GB"], 0,
        "Batch × tokens × d, 2 bytes each.",
        "Each token becomes a d-vector, so X is (batch, n, d) = 8 × 512 × 4096 = 16.8M numbers × 2 bytes ≈ 34 MB. The |V|-sized dimension appears only in the logits at the LM head, not in the input.",
        diagram="""
ids     [8 x 512]
  | look up rows of E [128,256 x 4096]
X       [8 x 512 x 4096]
  | ... N blocks ...
logits  [8 x 512 x 128,256]   (|V| appears only here)
""",
        topic="embeddings", level=3),
    tf("The 'Ġ' at the start of a GPT/Llama token such as 'Ġtasty' marks that the token begins with a space, so 'tasty' at the start of a text and ' tasty' mid-sentence can be different tokens with different IDs.", True,
       "The space is glued onto the word that follows.",
       "Byte-level BPE folds the preceding space into the token (the old-batch example: ' sun' = one token, ID 6035). That is why the same word can have two IDs, and why a stray trailing space in a prompt can change the next token.",
       topic="markers-libs", level=3),

    # ------------------------------------------------------------------ extra fills
    fill("The fixed list of every token a model knows, set when the tokenizer is trained, is called the ____.", "vocabulary",
         "Its size is written |V|.",
         "The vocabulary (|V| tokens: 128,256 for Llama 3, ≈151,669 for Qwen3) fixes the number of rows in the embedding table and the number of outputs of the LM head.",
         topic="token-types", level=1),
    fill("Encoder-only models such as BERT are pre-trained by hiding about 15% of tokens and predicting them. This objective is abbreviated ____.", "MLM",
         "Masked ... modelling.",
         "MLM = masked language modelling, using context on both sides. Decoder-only models use CLM (causal language modelling: predict the next token from the past only).",
         topic="families-tasks", level=2),
    fill("Translation, summarisation and question answering produce new text, so the course classes them as ____ tasks (abbreviation).", "NLG",
         "Natural Language ____.",
         "NLG = natural language generation. Classification, NER and POS tagging are NLU (understanding). LLMs are generators but can do NLU by generating the label.",
         topic="families-tasks", level=2),
    fill("In the course BPE example (hug 10, pug 5, pun 12, bun 4, hugs 5), the third merge creates the token ____.", "hug",
         "After ug (20) and un (16), count (h, ug).",
         "(h, ug) appears in hug 10 + hugs 5 = 15, beating (p, u) = 12 and (p, ug) = 5. The toy vocabulary is then [b, g, h, n, p, s, u, ug, un, hug].",
         topic="bpe", level=2),
    fill("Using the transpose of the input embedding matrix E as the LM head's unembedding matrix, so both share one set of parameters, is called weight ____.", "tying",
         "The two matrices are 'tied' together.",
         "Weight tying saves |V| × d parameters (≈205M for |V| = 50,000, d = 4,096) and makes one matrix serve both reading and writing tokens.",
         topic="pipeline", level=3),
    fill("RoPE, the positional method used by Llama, Qwen and DeepSeek, stands for ____ Position Embedding.", "Rotary",
         "It rotates query and key vectors.",
         "Rotary Position Embedding rotates Q and K by position-dependent angles inside attention, so q·k depends on the relative offset between tokens.",
         topic="positional", level=2),
]
