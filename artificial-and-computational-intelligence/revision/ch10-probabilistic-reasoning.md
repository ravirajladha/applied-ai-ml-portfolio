# Ch 10 — Probabilistic Reasoning & Bayesian Networks
**Slides: CS#11 & CS#12** (post-midsem deck, pages 23–41)

> Open `explainers/ch10-bayesian-networks.html` first if this topic is cold.

---

## 1. Why probability at all?

Logic is **brittle**. `Bird(x) ⇒ Flies(x)` breaks the moment you meet a penguin.
You cannot encode exceptions, and you cannot encode "usually".

The slide framing is **monotonic vs non-monotonic reasoning**:

| Monotonic | Non-Monotonic |
|---|---|
| Consistent | Relaxed consistency |
| Complete knowledge | Incomplete knowledge |
| Static | Dynamic |
| Discrete | Continuous & learning agent |
| **Predicate logic** | **Probabilistic model** |

*Monotonic* = adding a new fact never cancels an old conclusion. The real world
is not like that: "the bird flies" dies the second you learn "it's a penguin".

Sources of uncertainty an agent faces: **partial observability**, **sensor
noise**, **actuator error**, **non-determinism**.

Slide example: *"You can reach Bangalore Airport from MG Road within 90 mins via
route A."* Logic would have to enumerate every possible world (accidents, rain,
signals) to state this. Probability just says: 0.85.

---

## 2. Vocabulary (one line each)

- **Sample space `S`** — set of all outcomes. Die: `{1,2,3,4,5,6}`.
- **Sample point / atomic event / possible world** — one `x` in `S`.
- **Probability model** — `S` plus an assignment `P(x)` with `0 <= P(x) <= 1` and `sum P(x) = 1`.
- **Event `A`** — any subset of `S`, e.g. `A = "roll < 4"`.
- **Random variable** — a function from sample points to a range (reals or Booleans).

---

## 3. Formula box — memorise this block

```
Axioms          0 <= P(A) <= 1 ,  P(true) = 1 ,  P(false) = 0

Disjunction     P(A v B) = P(A) + P(B) - P(A ^ B)

Conditional     P(A | B) = P(A ^ B) / P(B)          [requires P(B) > 0]

Product rule    P(A ^ B) = P(A | B) . P(B) = P(B | A) . P(A)

Chain rule      P(X1,...,Xn) = PROD P(Xi | X1,...,X(i-1))

Independence    A _|_ B    <=>  P(A ^ B) = P(A).P(B)   <=>  P(A|B) = P(A)

Cond. indep.    A _|_ B|C  <=>  P(A,B|C) = P(A|C).P(B|C)

Bayes rule      P(A | B) = P(B | A) . P(A) / P(B)

Normalisation   P(X | e) = alpha . P(X, e),  alpha = 1 / sum_x P(X=x, e)

BAYES NET chain rule (THE one to remember):
      P(x1,...,xn) = PROD_i  P( xi | Parents(Xi) )
```

Enumeration cost: worst-case time **and** space `O(d^n)` — `d` = max arity
(values per variable), `n` = number of variables. That cost is the whole reason
Bayesian networks exist.

---

## 4. Inference by enumeration — the dentist table

Full joint distribution over `Cavity`, `Toothache`, `Catch` (the probe catches):

|  | toothache ^ catch | toothache ^ ¬catch | ¬toothache ^ catch | ¬toothache ^ ¬catch |
|---|---|---|---|---|
| **cavity**  | 0.108 | 0.012 | 0.072 | 0.008 |
| **¬cavity** | 0.016 | 0.064 | 0.144 | 0.576 |

Two operations only:
- **Marginalise** = add every cell where the thing you want is true.
- **Condition** = marginalise, then divide (normalise).

### Worked (straight from the slides)

```
P(toothache)          = 0.108 + 0.012 + 0.016 + 0.064          = 0.20
P(cavity)             = 0.108 + 0.012 + 0.072 + 0.008          = 0.20
P(cavity v toothache) = 0.108+0.012+0.072+0.008+0.016+0.064    = 0.28
```

Sanity check with the disjunction axiom:
`P(cav) + P(tooth) - P(cav ^ tooth) = 0.20 + 0.20 - (0.108+0.012) = 0.28` ✓

### Worked — conditional

**Q: P(cavity | toothache)?**

```
P(cavity ^ toothache) = 0.108 + 0.012 = 0.12
P(toothache)          = 0.20
P(cavity | toothache) = 0.12 / 0.20 = 0.60
```

> **Exam habit:** always write the two numbers (numerator, denominator) on
> separate lines before dividing. Most lost marks here are arithmetic, not method.

---

## 5. Bayesian Network — what it is

> A directed **acyclic** graph where each node is a random variable, each edge
> means "directly influences", and each node carries a **CPT** (conditional
> probability table): `P(Xi | Parents(Xi))`.

Why it is worth anything: the full joint over `n` Booleans needs `2^n - 1`
numbers. A BN needs only the CPT entries. It buys that compression by asserting
**conditional independences**.

Two independence facts to quote verbatim in theory questions:

1. A node is conditionally independent of its **non-descendants**, given its **parents**.
2. A node is conditionally independent of **all other nodes**, given its **Markov blanket** = its **parents + children + children's other parents**.

### Query types (slide: "Belief Nets")

| Type | Direction | Example |
|---|---|---|
| **Diagnostic** | effect → cause | `P(Burglary | JohnCalls)` |
| **Causal** | cause → effect | `P(JohnCalls | Burglary)` |
| **Inter-causal** | between two causes of a shared effect | `P(Burglary | Alarm, Earthquake)` |
| **Mixed** | both at once | `P(Alarm | JohnCalls, ¬Earthquake)` |

**Explaining away** is the inter-causal one: learning the earthquake happened
*lowers* the probability of burglary, even though B and E are independent a
priori. Two independent causes become dependent once you observe their shared
effect.

---

## 6. Numerical Pattern A — joint probability query

**This is the easiest full-mark question in the paper. Never drop it.**

### Network: Cavity example (Bayes Net #1)

`Weather` stands alone. `Cavity → Toothache` and `Cavity → Catch`.
`Toothache _|_ Catch | Cavity`.

**Q: P(W, ¬T, ¬V, C)** — good weather, no toothache, no cavity, probe catches.

By the BN chain rule, multiply each node's CPT entry given its parents:

```
P(W, ¬T, ¬V, C) = P(W) . P(¬V) . P(¬T | ¬V) . P(C | ¬V)
```

Note `W` contributes just `P(W)` — no parents, and independent of everything else.

### WORKED EXAMPLE — Burglary network

Structure: `Burglary → Alarm ← Earthquake`, `Alarm → JohnCalls`, `Alarm → MaryCalls`.

CPTs:

| P(B) | P(E) |
|---|---|
| 0.001 | 0.002 |

| B | E | P(A=T\|B,E) |
|---|---|---|
| T | T | 0.95 |
| T | F | 0.94 |
| F | T | 0.29 |
| F | F | 0.001 |

| A | P(J=T\|A) | P(M=T\|A) |
|---|---|---|
| T | 0.90 | 0.70 |
| F | 0.05 | 0.01 |

**Q: "Calculate the probability that the alarm has sounded, but neither burglary
nor earthquake happened, and both John and Mary called."**

That is the joint `P(¬B, ¬E, A, J, M)`. Every variable is fixed → **no summing**,
just one product.

```
P(¬B, ¬E, A, J, M)
  = P(¬B) . P(¬E) . P(A | ¬B, ¬E) . P(J | A) . P(M | A)
  = 0.999 x 0.998 x 0.001 x 0.90 x 0.70

  0.999 x 0.998 = 0.997002
  x 0.001       = 0.000997002
  x 0.90        = 0.0008973018
  x 0.70        = 0.00062811126

  = 0.000628   (6.28 x 10^-4)
```

**Method in three lines** (write these in the exam — they carry the marks):
1. Write the BN chain-rule expansion in symbols.
2. Substitute the CPT lookups, saying which row you used.
3. Multiply.

---

## 7. Numerical Pattern B — conditional query with hidden variables

**Q: `P(B | J, M)` — probability of a burglary given both neighbours called.**

`E` and `A` appear in neither the query nor the evidence → they are **hidden**.
You must **sum them out** (marginalise), then **normalise**.

```
P(B | J, M) = P(B, J, M) / P(J, M)
            = P(B,J,M) / [ P(B,J,M) + P(¬B,J,M) ]
```

### Step 1 — expand with marginalisation over the hidden variables

```
P(B, J, M) = sum_E sum_A  P(B).P(E).P(A|B,E).P(J|A).P(M|A)
```
Two hidden Booleans → **4 terms**.

### Step 2 — the four terms

| E | A | product | value |
|---|---|---|---|
| T | T | 0.001 x 0.002 x 0.95 x 0.90 x 0.70 | 0.000001197 |
| T | F | 0.001 x 0.002 x 0.05 x 0.05 x 0.01 | 0.00000000005 |
| F | T | 0.001 x 0.998 x 0.94 x 0.90 x 0.70 | 0.000591 |
| F | F | 0.001 x 0.998 x 0.06 x 0.05 x 0.01 | 0.00000002994 |

```
P(B, J, M) = 0.0005935
```

> Watch the `A = F` rows: you need `P(¬A|B,E) = 1 - P(A|B,E)`, and
> `P(J|¬A) = 0.05`, `P(M|¬A) = 0.01`. Forgetting the complement is the #1 error
> in this question.

### Step 3 — repeat for ¬B

| E | A | product | value |
|---|---|---|---|
| T | T | 0.999 x 0.002 x 0.29 x 0.90 x 0.70 | 0.0003650346 |
| T | F | 0.999 x 0.002 x 0.71 x 0.05 x 0.01 | 0.00000070929 |
| F | T | 0.999 x 0.998 x 0.001 x 0.90 x 0.70 | 0.00062811126 |
| F | F | 0.999 x 0.998 x 0.999 x 0.05 x 0.01 | 0.000498002499 |

```
P(¬B, J, M) = 0.001492
```

### Step 4 — normalise

```
P(B | J, M) = 0.0005935 / (0.0005935 + 0.001492)
            = 0.0005935 / 0.0020855
            = 0.2846        ->  about 28.5 %
```

**The intuition worth one sentence in the answer:** both neighbours calling pushes
burglary from a prior of 0.1 % up to ~28 %, a 285x jump — but it is still more
likely *not* a burglary, because burglaries are that rare. Base rates win.

---

## 8. D-separation — are two variables independent?

Two nodes `X` and `Y` are **d-separated by evidence Z** (so: conditionally
independent given `Z`) if **every** path between them is *blocked*.

Check each path one triple at a time. Three patterns, only three:

```
1. CHAIN       X -> M -> Y     blocked  <=>  M is observed
2. FORK        X <- M -> Y     blocked  <=>  M is observed
3. COLLIDER    X -> M <- Y     blocked  <=>  M is NOT observed
   (v-structure)                             AND no descendant of M observed
```

> **Mnemonic:** chains and forks are *pipes* — observing the middle node plugs
> them. Colliders are *doors that open when you knock* — observing the middle
> node (or any descendant of it) opens the path.
>
> If **any single path** is unblocked → **d-connected** → NOT independent.

### WORKED EXAMPLE — the Flu network (used all through the slides)

```
      Viral (V)          fooDPoison (D)
         |                     |
         v                     |
      fLu (L)                  |
         |                     |
         +------> Fever (F) <--+
```

CPTs:

| P(V=T) | P(V=F) |
|---|---|
| 0.6 | 0.4 |

| P(D=T) | P(D=F) |
|---|---|
| 0.1 | 0.9 |

| V | P(L=T\|V) | P(L=F\|V) |
|---|---|---|
| T | 0.8 | 0.2 |
| F | 0.01 | 0.99 |

| L | D | P(F=T\|L,D) | P(F=F\|L,D) |
|---|---|---|---|
| T | T | 0.99 | 0.01 |
| T | F | 0.80 | 0.20 |
| F | T | 0.80 | 0.20 |
| F | F | 0.05 | 0.95 |

**Q1: Is `V` d-separated from `F` given `L`?**
Only path: `V → L → F`. That is a **chain** with `L` in the middle, and `L` is
observed → **blocked**. → **d-separated. YES.**
So `P(V | F, L) = P(V | L)`.

**Q2: Is `V` d-separated from `D` given `L`?**
Path: `V → L → F ← D`. First triple `V → L → F` is a chain with `L` observed →
blocked. The path is already dead. → **d-separated. YES.**

**Q3 (the trap): Is `V` d-separated from `D` given `F`?**
Path `V → L → F ← D`, two triples:
- `V → L → F` : chain, `L` **not** observed → open.
- `L → F ← D` : **collider** at `F`, and `F` **is** observed → **open**.

Every triple open → path open → **d-CONNECTED. NO, not independent.**

That is explaining away: knowing the patient has a fever makes flu and food
poisoning compete as explanations for it.

---

## 9. Variable elimination

Enumeration recomputes the same products over and over. VE does each sum once
and stores the result as a **factor** (a small table).

Three rules straight off the slide:
1. Each variable is conditionally independent of its non-descendants given its parents.
2. **Eliminate hidden variables** — those that are neither query nor evidence.
3. Two variables are d-separated if they are conditionally independent given the evidence.

### WORKED — eliminate `V` from the Flu network

We want a factor over `L` alone: `P(L) = sum_V P(V) . P(L|V)`.

Multiply `P(V)` into `P(L|V)`:

| V | L | P(V).P(L\|V) |
|---|---|---|
| T | T | 0.6 x 0.80 = 0.48 |
| T | F | 0.6 x 0.20 = 0.12 |
| F | T | 0.4 x 0.01 = 0.004 |
| F | F | 0.4 x 0.99 = 0.396 |

Now **sum out `V`** — add rows sharing the same `L`:

| L | P(L) |
|---|---|
| T | 0.48 + 0.004 = **0.484** |
| F | 0.12 + 0.396 = **0.516** |

Check: `0.484 + 0.516 = 1.0` ✓ — *always* verify a factor over a single variable
sums to 1. Free error detection, costs three seconds.

**Pruning irrelevant nodes** is also VE. From the slide's travel network: to
compute `P(B)` you can drop every variable that is neither evidence, nor query,
nor an ancestor of one — those sum to 1 and vanish.

---

## 10. Approximate inference — the three sampling methods

Used when the network is too big for exact inference. All three consume a stream
of random numbers in `[0,1)` and walk the network in **topological order**
(parents before children).

**How to use one random number:** for `P(V=T) = 0.6`, if `r < 0.6` set `V=T`,
else `V=F`.

### (a) Prior sampling
Ignore the evidence entirely. Sample every variable. Then count.

The slide's 8 samples for the Flu net:

| V | L | D | F |
|---|---|---|---|
| T | T | F | T |
| F | F | F | F |
| T | F | F | T |
| F | T | F | T |
| T | T | F | T |
| T | F | F | F |
| F | F | F | T |
| T | F | F | F |

```
P(L)      = 3/8      (rows with L=T)
P(F ^ L)  = 3/8
P(L | F)  = 3/5      (of the 5 rows with F=T, 3 have L=T)
P(¬V | F) = 2/5
```
Problem: if the evidence is rare, almost no sample matches it. Wasteful.

### (b) Rejection sampling
Sample as above, then **throw away** every sample inconsistent with the evidence.
Count within what survives.

Slide: `P(F | D)` — keep only rows with `D=T`. Of the 8 retained samples,
5 have `F=T` → `P(F | D) = 5/8`.

Problem: the same one. With rare evidence you reject nearly everything.

### (c) Likelihood weighting  ← **the one that gets examined**
Never reject anything. **Fix** the evidence variables at their observed values,
sample only the non-evidence ones, and give each sample a **weight**:

```
w = PROD  P( e | Parents(e) )     over every EVIDENCE variable e
```

That is: multiply the CPT entry of each *clamped* variable. Non-evidence
variables contribute nothing to the weight (a factor of 1).

```
P(query | evidence) = ( sum of weights of samples where query holds )
                      ------------------------------------------------
                      ( sum of weights of ALL samples )
```

#### WORKED — `P(F | D, ¬L)` on the Flu network

Evidence: `D = T` and `L = F`. Sample `V` and `F` only.

Weight per sample = `P(L=F | V) x P(D=T)`:
- if `V = F` : `w = 0.99 x 0.1 = 0.099`
- if `V = T` : `w = 0.20 x 0.1 = 0.020`

The slide's four samples:

| V | L | D | F | weight |
|---|---|---|---|---|
| F | F | T | F | 1 x 0.99 x 0.1 x 1 = 0.099 |
| F | F | T | T | 0.099 |
| F | F | T | T | 0.099 |
| T | F | T | F | 1 x 0.20 x 0.1 x 1 = 0.020 |

```
               0.099 + 0.099          0.198
P(F | D, ¬L) = -------------------- = ------- = 0.6246
               3(0.099) + 0.020       0.317
```

> Two things the grader looks for: (1) the weight uses **only evidence nodes**;
> (2) you divided by the **total weight**, not the sample count.

---

## 11. You try — attempt before looking at §12

Use the **Flu network** CPTs from §8 for Q1–Q3, and the **Burglary** CPTs from §6
for Q4–Q5.

**Q1 (joint).** What is `P(V, L, ¬D, F)` — viral infection, flu, no food
poisoning, and fever?

**Q2 (conditional, hidden variables).** What is `P(F | ¬V)` — probability of
fever given the blood test shows *no* viral infection?
*(Hint: `L` and `D` are both hidden — sum out both, 4 terms.)*

**Q3 (d-separation).** For each, state d-separated YES/NO **and name the pattern**:

| | X | Y | Evidence Z | d-sep? |
|---|---|---|---|---|
| a | V | F | L | ? |
| b | L | D | nothing observed | ? |
| c | L | D | F | ? |
| d | V | D | F | ? |

**Q4 (joint, Burglary).** Probability that a burglary happened, no earthquake,
the alarm rang, John called but Mary did **not**.

**Q5 (likelihood weighting).** Estimate `P(¬F | D, ¬V)` on the Flu net. Write the
weight formula first. *(The slide used 7 samples that all had weight
`0.4 x 0.1` — work out why every weight comes out identical.)*

Send me your answers — "I don't know" is a fine answer for any of them — and I
will mark them and patch whatever is shaky before we move to Chapter 11.

---

## 12. Answers

<details>
<summary>Open only after attempting</summary>

**Q1.** `P(V,L,¬D,F) = P(V) . P(L|V) . P(¬D) . P(F|L,¬D)`
= `0.6 x 0.8 x 0.9 x 0.8` = **0.3456**
(Row `L=T, D=F` of the fever CPT gives 0.8.)

**Q2.** `P(F|¬V) = sum_L sum_D P(L|¬V) . P(D) . P(F|L,D)`

| L | D | P(L\|¬V) | P(D) | P(F\|L,D) | product |
|---|---|---|---|---|---|
| T | T | 0.01 | 0.1 | 0.99 | 0.00099 |
| T | F | 0.01 | 0.9 | 0.80 | 0.0072 |
| F | T | 0.99 | 0.1 | 0.80 | 0.0792 |
| F | F | 0.99 | 0.9 | 0.05 | 0.044550 |

Sum = **0.13194**, about 0.132.
No normalising needed here — `V` is a root, so conditioning on `¬V` costs
nothing extra and the four terms already add to `P(F|¬V)`.

**Q3.**
- a) `V → L → F`, **chain**, `L` observed → blocked → **YES, d-separated**.
- b) `L → F ← D`, **collider** at `F`; `F` not observed and no descendant
  observed → blocked → **YES, d-separated** (marginally independent).
- c) Same collider, but `F` **is** observed → **unblocked** → **NO, d-connected**
  (explaining away).
- d) `V → L → F ← D`. The chain `V→L→F` has `L` unobserved → open; the collider
  at observed `F` → open. Whole path open → **NO, d-connected**.

**Q4.** `P(B,¬E,A,J,¬M) = P(B) . P(¬E) . P(A|B,¬E) . P(J|A) . P(¬M|A)`
= `0.001 x 0.998 x 0.94 x 0.90 x 0.30`

```
0.001 x 0.998 = 0.000998
x 0.94        = 0.00093812
x 0.90        = 0.000844308
x 0.30        = 0.0002532924
```
= **2.53 x 10^-4**.
`P(¬M|A) = 1 - 0.70 = 0.30` — that complement is the whole trick.

**Q5.** Evidence is `D = T` and `V = F`. Both are **root nodes**, so their CPT
entries do not depend on anything that gets sampled:

```
w = P(V=F) x P(D=T) = 0.4 x 0.1 = 0.04
```

Identical for every sample — which is why the slide writes `0.04 / (7 x 0.04)`.
With 7 samples, if exactly 1 has `F = F`:
`P(¬F | D, ¬V) = 0.04 / (7 x 0.04) = 1/7 = 0.1429`.
When all weights are equal, likelihood weighting degenerates to plain counting.

</details>

---

## 13. Two-minute recall card

- `P(A|B) = P(A^B)/P(B)` · `P(AvB) = P(A)+P(B)-P(A^B)` · Bayes `P(A|B)=P(B|A)P(A)/P(B)`
- BN joint = **product of CPT entries given parents**.
- Query with hidden vars = **sum out hidden**, then **normalise**.
- Markov blanket = parents + children + children's other parents.
- D-sep: chain/fork blocked *when observed*; **collider blocked when NOT observed**.
- Likelihood weighting: clamp evidence, `w = PROD P(e | parents(e))`, then divide weighted count by total weight.
- Enumeration is `O(d^n)` — the motivation for BNs and VE.
- **Always** check that a single-variable factor sums to 1.
