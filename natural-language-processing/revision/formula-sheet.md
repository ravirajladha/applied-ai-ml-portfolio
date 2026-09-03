# NLP Pre-Midsem — Formula Sheet (Sessions 1–8)

Everything on one page. Open this in the last 30 minutes, not the first.

---

## Ch 1 — Evaluation

```
                  ACTUAL yes   ACTUAL no
    PRED yes         TP           FP
    PRED no          FN           TN

    Precision = TP / (TP + FP)
    Recall    = TP / (TP + FN)
    Accuracy  = (TP + TN) / (TP + FP + FN + TN)
    F1        = 2PR / (P + R)          harmonic mean
```

**Six levels of language (bottom-up):**
Morphological → Lexical → Syntactic → Semantic → Pragmatic → Discourse

**Three ambiguities:** Structural · Grammatical · Lexical (polysemy / homonymy)

**Four pre-processing steps:** remove punctuation → tokenize → remove stop words
→ lemmatize/stem

---

## Ch 2 — Vector semantics

```
DOT PRODUCT      a · b = Σᵢ aᵢbᵢ
LENGTH           |a|   = sqrt( Σᵢ aᵢ² )

                        a · b
COSINE           cos = ---------            range −1…+1
                       |a| |b|              (0…1 for count matrices)

TERM FREQUENCY   tf(t,d)  = log₁₀( count(t,d) + 1 )
DOC FREQUENCY    df(t)    = number of DOCUMENTS containing t
INVERSE DF       idf(t)   = log₁₀( N / df(t) )       N = total documents
TF-IDF           w(t,d)   = tf(t,d) × idf(t)

    word in EVERY document  ->  idf = 0  ->  tf-idf = 0
```

**Sparse vs dense:**

| | Sparse | Dense |
|---|---|---|
| Built by | Counting | Predicting |
| Length | \|V\| = 20k–50k | 50–1000 |
| Values | Mostly zero | Mostly non-zero |
| Methods | Count, TF-IDF, co-occurrence, PPMI | word2vec, GloVe |

**Why dense:** fewer weights · generalises better · **captures synonymy**
(car/automobile are unrelated dimensions in a sparse vector) · works better in
practice.

---

## Ch 3 — Word embeddings

```
SIGMOID          σ(x) = 1 / (1 + e^(−x))

SGNS classifier  P(+ | w,c) = σ(w · c)
                 P(− | w,c) = 1 − σ(w·c) = σ(−w·c)
                 P(+ | w, c₁:L) = Π σ(w · cᵢ)

SGNS LOSS        L = − [ log σ(c_pos·w) + Σᵢ log σ(−c_negᵢ·w) ]

SGD UPDATES      c_pos ← c_pos − η [ σ(c_pos·w) − 1 ] w
                 c_neg ← c_neg − η [ σ(c_neg·w) − 0 ] w
                 w     ← w − η [ (σ(c_pos·w)−1)c_pos + Σᵢ σ(c_negᵢ·w) c_negᵢ ]

ANALOGY          b̂* = argmax_x cos( x , a* − a + b )
                 king − man + woman ≈ queen
```

- **k negatives per positive:** 2–5 (large data), 5–20 (small data)
- **Two matrices:** target `W` + context `C`; represent word *i* as `wᵢ + cᵢ`
- **Skip-gram** = centre → context; small data, rare words
- **CBOW** = context → centre; faster, better on frequent words
- **Window ±2** → syntactic/taxonomic; **±5** → semantic field
- **GloVe** = global co-occurrence + ratios of co-occurrence probabilities

---

## Ch 4 — N-gram language models

```
CHAIN RULE       P(x₁…xₙ) = P(x₁)P(x₂|x₁)P(x₃|x₁x₂)…P(xₙ|x₁…xₙ₋₁)

MARKOV           P(wᵢ | w₁…wᵢ₋₁) ≈ P(wᵢ | wᵢ₋ₙ₊₁…wᵢ₋₁)

BIGRAM MLE       P(wᵢ|wᵢ₋₁) = c(wᵢ₋₁,wᵢ) / c(wᵢ₋₁)

ADD-1 (LAPLACE)  P(wᵢ|wᵢ₋₁) = [ c(wᵢ₋₁,wᵢ) + 1 ] / [ c(wᵢ₋₁) + V ]
                 V = number of UNIQUE words

RECONSTITUTED    c*(wᵢ₋₁,wᵢ) = [ c(wᵢ₋₁,wᵢ) + 1 ] × c(wᵢ₋₁) / [ c(wᵢ₋₁) + V ]

INTERPOLATION    P̂ = λ₁P(wₙ|wₙ₋₂wₙ₋₁) + λ₂P(wₙ|wₙ₋₁) + λ₃P(wₙ),   Σλ = 1
                 λs set on a HELD-OUT corpus

STUPID BACKOFF   S = count(wᵢ₋ₖ₊₁ⁱ)/count(wᵢ₋ₖ₊₁ⁱ⁻¹) if >0, else 0.4 × S(shorter)

PERPLEXITY       PP(W) = P(w₁…w_N)^(−1/N)
                       = ᴺ√ Π 1/P(wᵢ|wᵢ₋₁)

    LOWER perplexity = BETTER model.  Minimising PP = maximising P.
    Uniform choice among 10 -> PP = 10  (branching factor)
    WSJ: unigram 962, bigram 170, trigram 109
```

Work in **log space** to avoid underflow. Add-1 is **not** used for n-grams.
OOV → fixed lexicon `L`, map unseen words to `<UNK>`, train it as a normal word.

---

## Ch 5 — Neural networks & neural LMs

```
UNIT             z = b + Σ wᵢxᵢ = w·x + b        y = f(z)

SIGMOID          σ(z) = 1/(1 + e^(−z))            (0,1)
TANH             (e^z − e^−z)/(e^z + e^−z)        (−1,1)
ReLU             max(z, 0)                        [0,∞)      ← most common

SOFTMAX          softmax(zᵢ) = e^(zᵢ) / Σⱼ e^(zⱼ)

2-LAYER NET      h = f(W x + b);   z = U h;   y = σ(z) or softmax(z)

MULTI-LAYER      a[0] = x;  z[i] = W[i]a[i−1] + b[i];  a[i] = g[i](z[i])

XOR SOLUTION     W = [[1,1],[1,1]]  b = [0,−1]  U = [1,−2]   with ReLU

NEURAL LM        e = [E x_{t−3} ; E x_{t−2} ; E x_{t−1}]
                 h = σ(W e + b);  z = U h;  ŷ = softmax(z)

CROSS-ENTROPY    L_CE = −[ y log ŷ + (1−y) log(1−ŷ) ]

GRADIENT DESCENT θ ← θ − η ∂L/∂θ
DERIVATIVE       ∂L_CE/∂wⱼ = ( σ(w·x+b) − y ) · xⱼ
```

**XOR is not linearly separable** (Minsky & Papert 1969) — needs a hidden layer.
Do **not** count the input layer. Neural LMs beat n-grams because embeddings
transfer *cat* → *dog*.

---

## Ch 6 — POS tagging (the heaviest numerical)

```
HMM COMPONENTS
    states T = tags,  observations W = words
    A = {aᵢⱼ} = P(tⱼ|tᵢ)   transition   (tag -> tag)
    B = {bᵢ(k)} = P(wₖ|tᵢ) emission     (tag -> WORD, not word -> tag)
    π = initial vector

COUNTS
    P(tᵢ|tᵢ₋₁) = C(tᵢ₋₁,tᵢ)/C(tᵢ₋₁)        P(wᵢ|tᵢ) = C(tᵢ,wᵢ)/C(tᵢ)

BAYES DERIVATION
    t̂ = argmax P(T|W) = argmax P(W|T)P(T)/P(W)
                       = argmax P(W|T)P(T)          [drop P(W)]

HMM TAGGING EQUATION
    t̂₁ⁿ = argmax  Π_{i}  P(wᵢ|tᵢ) · P(tᵢ|tᵢ₋₁)
                         emission    transition

MARKOV CHAIN
    P(q₁ q₂ … q_T) = π_{q₁} · Π aᵢⱼ       (T states -> T−1 transitions!)

VITERBI
    init       V[t,1] = P(t|<S>) · P(w₁|t)
    recursion  V[t,j] = max_{t'} [ V[t',j−1] · P(t|t') ] · P(wⱼ|t)
               bp[t,j] = argmax_{t'} [ V[t',j−1] · P(t|t') ]
    terminate  max_t V[t,T] · P(STOP|t)
    backtrace  follow bp back to column 1
    complexity O(N²T)

MEMM
    t̂ = argmax Π P(tᵢ | wᵢ, tᵢ₋₁)         DISCRIMINATIVE, POSTERIOR
    HMM  vₜ(j) = max v_{t−1}(i) · aᵢⱼ · bⱼ(oₜ)
    MEMM vₜ(j) = max v_{t−1}(i) · P(sⱼ | sᵢ, oₜ)
```

- **4 open classes** in English: Noun, Verb, Adjective, Adverb
- **Penn Treebank = 45 tags**; `IN` for prepositions, except *to* → `TO`
- **HMM = generative (likelihood)**; **MEMM = discriminative (posterior)**
- HMM issues: unknown words · limited context · sparsity
- Greedy decoding is bad — use Viterbi

---

## Ch 7 — Modern POS tagging

| Approach | Accuracy |
|---|---|
| Bi-LSTM-CRF | ~97–98% |
| BERT / RoBERTa fine-tuned | **~98.5–99.5%** (SOTA) |

- **LSTM gates:** Input, Forget, Output — solve **vanishing gradients**
- **Character embeddings** handle unknown words
- **CRF layer** enforces valid tag *sequences*, scores whole paths
- **Transformer** = self-attention replaces recurrence; encoder blocks =
  Multi-Head Attention + Feed-Forward
- **LLM agent** = an LLM that can call external tools

---

## Ch 8 — LLM, prompting, transfer

```
        NO WEIGHTS CHANGE      SOME CHANGE            ALL/MOST CHANGE
        PROMPTING              TRANSFER LEARNING      FINE-TUNING
        zero-/few-shot         freeze backbone,       unfreeze pre-trained
        in-context learning    train new head         layers too
        data: none             data: small            data: large + similar
```

- **Zero-shot** = instruction only; **few-shot** = instruction + a few examples.
  **Neither updates any weights.**
- **Transfer learning** = pre-trained weights **frozen**, train only new layers.
- **Fine-tuning** = pre-trained layers **updated**. Needs a large, similar dataset.
- **Transductive** = no labelled target data (domain adaptation).
  **Inductive** = labelled target data available (multi-task, pre-training).
- Deep learning needs **>50K** data items — the reason transfer learning exists.

---

## The five things most likely to cost you marks

1. **Emission is `P(word | tag)`**, not `P(tag | word)`.
2. **Add-1 denominator adds `V`**, the number of *unique* words — not 1, not the
   corpus size.
3. **T states = T−1 transitions** in a Markov chain probability.
4. In Viterbi, the **max is over the predecessor**; the emission multiplies in
   **after** the max, once.
5. **`df` counts documents**, not occurrences — and a word in every document has
   **tf-idf = 0**.
