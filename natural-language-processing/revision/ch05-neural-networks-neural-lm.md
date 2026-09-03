# Ch 5 — Neural Networks and Neural Language Models
**Session 5** (deck: *NLP Session 5 — Neural networks and Neural language Models*)
**Textbook: Jurafsky & Martin, Chapter 7**

The bridge chapter. It replaces the *counting* of Ch 4 with a *network*, and
feeds it the *embeddings* of Ch 3. Everything from here to BERT is this chapter
with more layers.

---

## 1. The neural unit

> A unit takes a set of real-valued numbers as input, performs some computation
> on them, and produces an output.

```
    Inputs  x₁ x₂ x₃   +1(bias)
       \      |     /   /
        w₁   w₂    w₃  b
          \   |    /   /
        [ weighted sum ]        z = b + Σᵢ wᵢxᵢ    =    w · x + b
                |
        [ non-linear f ]        a = f(z)
                |
             output y
```

### Formula box

```
WEIGHTED SUM        z = b + Σᵢ wᵢ xᵢ        =  w · x + b

ACTIVATION          y = a = f(z)

    z is just a real number. Without f, a stack of layers collapses into a
    single linear map — the non-linearity is what makes depth worth anything.

SIGMOID             σ(z) = 1 / (1 + e^(−z))          range (0, 1)
TANH                tanh(z) = (e^z − e^(−z))/(e^z + e^(−z))   range (−1, 1)
ReLU                relu(z) = max(z, 0)              range [0, ∞)   ← MOST COMMON

So the full unit:   y = σ(w · x + b)
```

> **The slide's own joke:** the biological neuron picture "is in your brain"; the
> next slide's unit diagram "is **not** in your brain". Do not over-read the
> analogy.

### ⭐ Worked example — one unit, by hand
Given `w = [0.2, 0.3, 0.9]`, `b = 0.5`, input `x = [0.5, 0.6, 0.1]`:

```
Step 1  weighted sum
    z = b + w·x
      = 0.5 + (0.2)(0.5) + (0.3)(0.6) + (0.9)(0.1)
      = 0.5 + 0.10 + 0.18 + 0.09
      = 0.87

Step 2  activation (sigmoid)
    y = σ(0.87) = 1 / (1 + e^(−0.87))
                = 1 / (1 + 0.4190)
                = 1 / 1.4190
                = 0.70
```

---

## 2. The XOR problem — why we need hidden layers

**Perceptron** = a very simple neural unit: **binary output (0 or 1)**, **no
non-linear activation function**.

```
    y = 1  if  w·x + b > 0
    y = 0  otherwise
```

**AND and OR are easy to build with perceptrons. XOR is not possible.**
(Minsky and Papert, 1969 — the result that caused the first AI winter.)

### Why: perceptrons are linear classifiers

The perceptron equation in two inputs is the equation of a **line**:
```
    w₁x₁ + w₂x₂ + b = 0     ⇔     x₂ = (−w₁/w₂) x₁ + (−b/w₂)
```
That line is a **decision boundary**: output 0 on one side, 1 on the other.

```
    AND               OR                XOR
  x2                x2                x2
  1 | 0   1         1 | 1   1         1 | 1   0
    |                 |                 |
  0 | 0   0         0 | 0   1         0 | 0   1
    +--------x1        +--------x1        +--------x1
      0   1             0   1             0   1

  one line works    one line works    NO SINGLE LINE WORKS
```

> **XOR is not a linearly separable function.** No single line can put
> {(0,1),(1,0)} on one side and {(0,0),(1,1)} on the other.

### The solution: a layered network
XOR **can** be computed by a **layered network of units**. The standard solution
(ReLU activations):

```
    W = [ 1  1 ]      b = [ 0 ]      U = [ 1  −2 ]
        [ 1  1 ]          [−1 ]

    h = relu(W x + b)
    y = U · h
```

Trace all four inputs:

| x | Wx + b | h = relu(·) | y = U·h | XOR |
|---|---|---|---|---|
| [0,0] | [0, −1] | [0, 0] | 0 | 0 ✅ |
| [0,1] | [1, 0] | [1, 0] | 1 | 1 ✅ |
| [1,0] | [1, 0] | [1, 0] | 1 | 1 ✅ |
| [1,1] | [2, 1] | [2, 1] | 2 − 2 = 0 | 0 ✅ |

> **The point of the hidden representation `h`.** The hidden layer maps [0,1] and
> [1,0] onto the *same* point [1,0], which makes the problem linearly separable
> in `h`-space. **With learning, hidden layers learn to form useful
> representations.** That sentence is the whole justification for deep learning.

---

## 3. Feedforward neural networks

Also called **multi-layer perceptrons (MLPs)**, for historical reasons — the name
is a misnomer since the units are not perceptrons.

### Building up

| Network | Shape | Output |
|---|---|---|
| **Binary logistic regression** | 1 layer: input vector → σ node | a **scalar** |
| **Fully connected single layer** | `W` is a matrix, `b` is a vector → softmax nodes | a **vector** |
| **Two-layer network** | input → hidden (`W`, ReLU/tanh) → output (`U`, σ) | scalar or vector |

> **Counting convention:** we do **not** count the input layer when counting
> layers. A "2-layer network" has one hidden layer and one output layer.

### Formula box — two-layer network

```
    h  =  f( W x + b )         hidden layer;  f = ReLU or tanh
    z  =  U h
    y  =  σ(z)      (binary)   or   y = softmax(z)   (multiclass)

MULTI-LAYER NOTATION (superscripts = layer index)
    a[0] = x
    z[i] = W[i] a[i−1] + b[i]
    a[i] = g[i]( z[i] )
    ŷ    = a[n]

REPLACING THE BIAS UNIT (a notational convenience, not a change of model)
    Add a dummy node a₀ = 1 to each layer; its weight w₀ IS the bias.
    x = x₁ … x_n     becomes      x = x₀, x₁ … x_n   with x₀ = 1
```

### Softmax — the generalisation of sigmoid
For a vector `z` of dimensionality `k`:
```
                        e^(zᵢ)
    softmax(zᵢ)  =  ---------------          for 1 ≤ i ≤ k
                     Σⱼ e^(zⱼ)

    Output is a probability distribution: all entries in (0,1), summing to 1.
```
Use **sigmoid** for 2 classes, **softmax** for more than 2 (one output unit per
class).

---

## 4. Applying feedforward nets to NLP tasks

### Task 1: text classification (sentiment analysis)

Three generations of the same task, in order:

| Version | Input layer | Comment |
|---|---|---|
| **Logistic regression** | Hand-built binary features | The baseline |
| **2-layer feedforward net** | Same hand-built features, plus a hidden layer | The hidden layer lets the network use **non-linear interactions between features**, which *may or may not* help |
| **Representation learning** | **Learned embeddings** e₁…eₙ | ⭐ The real power of deep learning |

> **The key sentence:** *the real power of deep learning comes from the ability to
> learn features from the data*, instead of using hand-built, human-engineered
> features.

### The fixed-size problem, and three fixes
A feedforward net needs a **fixed-length** input, but texts come in different
sizes. The slide's solutions:

1. **Pad / truncate.** Make the input the length of the longest review; pad
   shorter ones with zero embeddings; truncate longer ones at test time.
2. **Mean pooling.** Create a single "sentence embedding" (same dimensionality as
   a word) by taking the **mean** of all the word embeddings.
3. **Max pooling.** Take the **element-wise max** — for each dimension, pick the
   largest value across all words.

---

## 5. Neural language models

> **Language modelling: calculating the probability of the next word in a
> sequence given some history.**

- We have seen n-gram LMs (Ch 4).
- **Neural network LMs far outperform n-gram LMs.**
- State-of-the-art neural LMs use more powerful architectures (**Transformers**),
  **but simple feedforward LMs can do almost as well.**

### The architecture

**Task:** predict the next word `wₜ` given prior words `wₜ₋₁, wₜ₋₂, wₜ₋₃, …`
**Output:** a probability distribution over possible next words.
**Problem:** sequences are of arbitrary length.
**Solution:** **sliding windows** of fixed length.

```
    3 context words
         |
    one-hot vectors  x_{t−3}, x_{t−2}, x_{t−1}     each of length |V|
         |  (multiply by embedding matrix E — really just a row lookup)
    3 embeddings
         |  CONCATENATE
    embedding layer  e
         |
    h = σ( W e + b )          hidden layer
         |
    z = U h
         |
    y = softmax(z)            distribution over the whole vocabulary
```

### Formula box

```
    e = [ E x_{t−3} ; E x_{t−2} ; E x_{t−1} ]     (concatenation)
    h = σ( W e + b )
    z = U h
    ŷ = softmax( z )

    P(wₜ = i | wₜ₋₁, wₜ₋₂, wₜ₋₃)  =  ŷᵢ
```

`E` is the **embedding matrix**; a one-hot vector times `E` selects one row, so
in practice you use a specialised **lookup** function rather than a matrix
multiply.

### ⭐ Why neural LMs beat n-gram LMs — memorise this example

> **Training data:** *I have to make sure that the **cat** gets fed.*
> **Never seen:** *dog gets fed*
> **Test data:** *I forgot to make sure that the **dog** gets ___*
>
> - An **n-gram LM cannot predict "fed"** — it never saw the trigram *the dog gets*.
> - A **neural LM can**, because it represents words by their **embeddings**, and
>   *cat* and *dog* have similar embeddings.

> Neural LMs represent words in the prior context **by their embeddings, rather
> than just by their word identity** as n-gram models do. **Using embeddings
> allows neural language models to generalize better to unseen data.**

### Two ways to train the embedding layer

| | What you do | When to use |
|---|---|---|
| **Freeze `E`** | Initialise `E` with word2vec (or another pretraining algorithm) and **hold it constant** — only modify `W`, `U`, `b` | Default; less data needed |
| **Learn `E` jointly** | Train the embeddings simultaneously with the network | Useful when the task (sentiment classification, translation, parsing) **places strong constraints on what makes a good word representation** |

### N-gram vs NLM — the comparison table

| | N-gram LM | Neural LM |
|---|---|---|
| History length | Short, fixed | **Much longer** histories |
| Generalisation | None across similar words | **Generalises over contexts of similar words** |
| Word prediction accuracy | Lower | **More accurate** |
| Complexity | Simple | Much more complex |
| Speed | Fast | Slower |
| Energy to train | Low | **Much higher** |
| Interpretability | **Interpretable** | Less interpretable |

> **The honest conclusion on the slide:** for many (especially smaller) tasks,
> **an n-gram language model is still the right tool.**

---

## 6. Training: loss, gradient descent, backpropagation

### Formula box

```
CROSS-ENTROPY LOSS, binary logistic regression

    L_CE(ŷ, y) = − [ y log ŷ  +  (1 − y) log(1 − ŷ) ]

    A measure of how far off the current answer is from the right answer.

GRADIENT DESCENT WEIGHT UPDATE

    θ_{t+1}  =  θ_t  −  η · ∂L(f(x;θ), y) / ∂θ

    η = the learning rate.

DERIVATIVE FOR ONE WEIGHT (via the chain rule, f(x) = u(v(x)))

    ∂L_CE / ∂wⱼ  =  ( σ(w·x + b) − y ) · xⱼ

                     \_____________/    \__/
                      derivative of      derivative of
                      loss × activation  the weighted sum
```

### Why backpropagation is needed
Those derivatives only give the updates for **one weight layer — the last one**.
For deeper networks with many layers and different activation functions, we need
**even more use of the chain rule**: **computation graphs and backward
differentiation**.

> **The summary sentence:** for training we need the derivative of the loss with
> respect to weights in **early** layers, but the loss is computed only at the
> **very end** of the network. Backward differentiation solves this: given a
> computation graph and the derivatives of all the functions in it, we can
> automatically compute the derivative of the loss with respect to those early
> weights.

---

## 7. Quick recall table (cover the right column)

| Question | Answer |
|---|---|
| Equation for the weighted sum in a unit? | z = b + Σ wᵢxᵢ = w·x + b |
| Why a non-linear activation at all? | Without it, stacked layers collapse into one linear map |
| Three activation functions? | Sigmoid, tanh, **ReLU** (most common) |
| ReLU formula? | max(z, 0) |
| What is a perceptron? | A simple unit with **binary output** and **no non-linear activation** |
| Which function can a perceptron NOT compute? | **XOR** — it is not linearly separable |
| Who showed that, and when? | Minsky and Papert, **1969** |
| How is XOR solved? | A **layered** network — the hidden layer makes it separable |
| Another name for a feedforward net? | Multi-layer perceptron (MLP) |
| Do we count the input layer? | **No** |
| Sigmoid vs softmax? | Sigmoid for 2 classes; softmax for >2 |
| Softmax formula? | e^(zᵢ) / Σⱼ e^(zⱼ) |
| Three fixes for variable-length text? | Pad/truncate; mean of embeddings; element-wise max |
| Neural LM handles arbitrary length how? | **Sliding window** of fixed size |
| Why do neural LMs beat n-grams? | They use **embeddings**, so *dog* inherits what was learned about *cat* |
| Two ways to handle `E` in training? | Freeze it (word2vec init) or learn it jointly |
| Loss function? | Cross-entropy |
| How are early-layer gradients found? | Backward differentiation over the computation graph |

---

## 8. LLMs, prompting and transfer learning
These sit at the tail of this deck but are treated as their own chapter:
→ [`ch08-llm-prompt-engineering.md`](ch08-llm-prompt-engineering.md)

---

## 9. You try
*Attempt on paper before scrolling. Answers at the very bottom.*

**Q1 (one unit).** `w = [0.5, −0.3, 0.8]`, `b = −0.2`, `x = [1.0, 2.0, 0.5]`.
Compute `z`, then the output under (i) sigmoid and (ii) ReLU.

**Q2 (XOR).** Using `W = [[1,1],[1,1]]`, `b = [0, −1]`, `U = [1, −2]` with ReLU,
verify the network's output for `x = [1,1]` and for `x = [0,1]`, showing `h`
each time. Then say in one sentence *why* the hidden layer makes XOR solvable.

**Q3 (softmax).** `z = [1.0, 2.0, 0.5]`. Compute `softmax(z)` to 3 decimals and
check the three values sum to 1.

**Q4 (concept).** Your training corpus contains *"the cat gets fed"* but never
*"the dog gets fed"*. At test time you see *"the dog gets ___"*. Explain in three
sentences why a trigram model fails and a neural LM succeeds.

**Q5 (architecture).** A neural LM uses a 3-word sliding window, 100-dimensional
embeddings, a hidden layer of 200 units, and |V| = 10,000. Give the dimensions
of the embedding layer `e`, the matrix `W`, and the matrix `U`.

---

## Next
**Chapter 6 — POS Tagging.** The first *sequence labelling* task, and the home of
the Viterbi algorithm.
→ [`ch06-pos-tagging-hmm-viterbi.md`](ch06-pos-tagging-hmm-viterbi.md)

---
---
---

<!-- ANSWERS BELOW - stop scrolling until you have attempted -->

## Answers

**A1.**
```
z = −0.2 + (0.5)(1.0) + (−0.3)(2.0) + (0.8)(0.5)
  = −0.2 + 0.5 − 0.6 + 0.4
  = 0.1

(i)  σ(0.1)    = 1 / (1 + e^(−0.1)) = 1 / (1 + 0.9048) = 1/1.9048 = 0.525
(ii) relu(0.1) = max(0.1, 0)        = 0.1
```

**A2.**
```
x = [1,1]:  Wx     = [1·1+1·1, 1·1+1·1] = [2, 2]
            Wx + b = [2, 1]
            h      = relu([2,1]) = [2, 1]
            y      = U·h = (1)(2) + (−2)(1) = 0        ✅ XOR(1,1) = 0

x = [0,1]:  Wx     = [1, 1]
            Wx + b = [1, 0]
            h      = relu([1,0]) = [1, 0]
            y      = U·h = (1)(1) + (−2)(0) = 1        ✅ XOR(0,1) = 1
```
*Why it works:* the hidden layer projects the four inputs into a new space where
the two "1" cases land on the same point `[1,0]` and the two "0" cases separate
away from it — and in that new space a single linear boundary suffices.

**A3.**
```
e^1.0 = 2.7183     e^2.0 = 7.3891     e^0.5 = 1.6487
sum   = 2.7183 + 7.3891 + 1.6487 = 11.7561

softmax = [ 2.7183/11.7561 , 7.3891/11.7561 , 1.6487/11.7561 ]
        = [ 0.231 , 0.629 , 0.140 ]

check:    0.231 + 0.629 + 0.140 = 1.000  ✅
```

**A4.**
A trigram model estimates `P(fed | dog gets)` by counting the trigram
*"dog gets fed"*, which never occurs, so the count is 0 and (unsmoothed) the
probability is 0 — the word is represented only by its **identity**, and *dog* is
simply a different string from *cat*. A neural LM instead feeds the network the
**embeddings** of *the*, *dog*, *gets*, and the embedding of *dog* is close to
that of *cat* because the two occur in similar contexts. The hidden layer
therefore produces almost the same activation it produced for the *cat* case, so
softmax still puts high probability on *fed* — generalisation the n-gram model
structurally cannot do.

**A5.**
```
e :  3 words × 100 dims, concatenated   ->  300 × 1

W :  maps e (300) to the hidden layer (200)
     ->  200 × 300      (plus a bias b of 200 × 1)

U :  maps the hidden layer (200) to one score per vocabulary word (10,000)
     ->  10,000 × 200
```
Note that `U` holds 2 million weights — the output layer over the full vocabulary
is where nearly all the cost of a neural LM lives.
