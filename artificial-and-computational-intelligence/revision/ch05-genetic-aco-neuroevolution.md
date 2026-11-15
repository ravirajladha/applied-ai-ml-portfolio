# Ch 5 — Genetic Algorithms, Ant Colony Optimization & Neuroevolution
**Slides: CS#5 and CS#6** (pre-midsem deck, pages 42–66)

> **You marked this chapter as never touched.** Open
> `explainers/ch05-genetic-aco.html` first — it runs the GA generation and the
> ACO ant tour click by click.

These are the **population-based** local search methods: instead of one current
state, keep **many parallel instances**.

Two heavy numericals live here, and both are fully worked below using **your
slides' own numbers**:
1. **GA**: fitness → selection probability → crossover → mutation.
2. **ACO**: transition probability → pheromone update.

---

## 1. Genetic Algorithms — what they are

> A **genetic algorithm** is a search technique used to find true or approximate
> solutions to optimization and search problems. GAs are categorised as
> **global search heuristics**, and are a class of **evolutionary algorithms**
> using techniques inspired by evolutionary biology: **inheritance, mutation,
> selection, crossover (recombination)**.

Evolution starts from a population of randomly generated individuals and happens
in **generations**. Each generation: evaluate fitness of every individual, select
multiple individuals based on fitness, modify them to form a new population.

**Termination:** when a maximum number of generations is produced, **or** a
satisfactory fitness level is reached.

> **Write this down — it gets asked:** **"No convergence rule or guarantee."**
> A GA is not guaranteed to find the optimum, and there is no theorem telling you
> when it will converge.

### Vocabulary — biology vs algorithm

| Term | Biology | Algorithm |
|---|---|---|
| **Population** | Collection of individuals | **Collection of states** |
| **Individual** | An organism | **Any possible solution** |
| **Fitness** | More healthy, less prone to disease | **Closest to the final solution** — the target function we optimise |
| **Selection** | Selecting the most biologically fit species | **Selecting states closest to the solution** |
| **Crossover** | Mating / reproducing | **Interchanging values between selected states** |
| **Mutation** | Change or variation in DNA | **Alteration of a state (randomly)** |
| **Trait** | A feature | Possible aspect/feature of an individual |
| **Genome** | All chromosomes | **Collection of all chromosomes (traits) for an individual** |

---

## 2. The 7 steps — learn this list

```
Step 01: Representing individuals
Step 02: Generating an initial population
Step 03: Applying a fitness function
Step 04: Selecting parents for mating according to their fitness
Step 05: Crossover of parents to produce a new generation
Step 06: Mutation of the new generation to bring diversity
Step 07: Repeat until a solution is reached
```

The operational version from the slides:
```
1. Select 'k' random states                        -- Initialization, k = 4
2. Evaluate the fitness value of all states
3. If a state reaches the THRESHOLD fitness, or threshold new states,
   or no change from the previous iteration  ->  STOP
4. Else, use the ROULETTE WHEEL mechanism to select pair(s)
5. Selected pairs produce a new state (successor) by CROSSOVER
6. The successor is allowed to MUTATE
7. Repeat from step 2
```

---

## 3. NUMERICAL — the full GA generation (slides' own 4-Queens run)

Representation: `[V1 V2 V3 V4]`, `Vi` = row of the queen in column `i`.
**Fitness = number of NON-attacking pairs of queens** (maximise).
**Threshold = 6** (which for 4 queens is `C(4,2) = 6`, i.e. a perfect solution).

### Step 1–3: initial population and fitness, `k = 4`

| # | State | Fitness (non-attacking pairs) |
|---|---|---|
| B1 | `1 4 2 2` | **4** |
| B2 | `2 1 3 4` | **4** |
| B3 | `1 4 3 2` | **2** |
| B4 | `2 1 4 1` | **3** |

Nobody hit 6, so we continue.

<details>
<summary>Working for B1 = [1,4,2,2] — click to expand</summary>

| Pair | Rows | Attacking? |
|---|---|---|
| (1,2) | 1, 4 | no — `|1−4|=3 ≠ 1` |
| (1,3) | 1, 2 | no — `|1−2|=1 ≠ 2` |
| (1,4) | 1, 2 | no — `|1−2|=1 ≠ 3` |
| (2,3) | 4, 2 | no — `|4−2|=2 ≠ 1` |
| (2,4) | 4, 2 | **yes** — `|4−2|=2 = |2−4|=2` diagonal |
| (3,4) | 2, 2 | **yes** — same row |

Attacking = 2, so **non-attacking = 6 − 2 = 4**.
</details>

### Step 4: Selection — the roulette wheel

```
                    fitness of individual i
   Probability_i = ──────────────────────────
                     total fitness of all
```

Total fitness = `4 + 4 + 2 + 3 = 13`.

| # | State | Fitness | Probability |
|---|---|---|---|
| B1 | `1 4 2 2` | 4 | `4/13 = 0.3077` → **0.31** |
| B2 | `2 1 3 4` | 4 | `4/13 = 0.3077` → **0.31** |
| B3 | `1 4 3 2` | 2 | `2/13 = 0.1538` → **0.15** |
| B4 | `2 1 4 1` | 3 | `3/13 = 0.2308` → **0.23** |
| | | **13** | **1.00** ✓ |

> **How the roulette wheel works (the slide's words):** the population is divided
> on a wheel according to their respective **percentages of fitness**, and two
> fixed points are placed. The wheel is spun, and the individuals the fixed
> points land on are selected.
>
> **Other selection methods** to name if asked: **roulette wheel, tournament,
> rank**.

**Slide's spin results** — winners of games 1,2,3,4 were `B4, B1, B1, B3`.
So the selected parent pairs are **`<B4, B1>`** and **`<B1, B3>`**.

| Pair | Parent A | Parent B |
|---|---|---|
| 1 | B4 = `2 1 4 1` | B1 = `1 4 2 2` |
| 2 | B1 = `1 4 2 2` | B3 = `1 4 3 2` |

> Note B1 was selected **twice** — that is the wheel working correctly. High
> fitness means more slots, and nothing stops the same individual winning twice.

### Step 5: Crossover

**Three strategies to name:** single-point (randomly select one crossover point),
**multi-point**, **uniform** crossover.

**Pair 1** — crossover point after gene **1**:
```
   B4 = 2 | 1 4 1          child1 = 2 | 4 2 2   ->   2 4 2 2
   B1 = 1 | 4 2 2          child2 = 1 | 1 4 1   ->   1 1 4 1
```

**Pair 2** — crossover point after gene **2**:
```
   B1 = 1 4 | 2 2          child3 = 1 4 | 3 2   ->   1 4 3 2
   B3 = 1 4 | 3 2          child4 = 1 4 | 2 2   ->   1 4 2 2
```

Successors: `2 4 2 2` · `1 1 4 1` · `1 4 3 2` · `1 4 2 2`

> Pair 2's parents share their first two genes, so crossover produced children
> that are just **swaps of the parents**. That is normal and it is exactly why
> **mutation is needed** — without it, a converged population stops producing
> anything new.

### Step 6: Mutation — change one gene at random

| Successor | After mutation | Gene changed |
|---|---|---|
| `2 4 2 2` | **`2 4 1 2`** | gene 3: 2 → 1 |
| `1 1 4 1` | **`1 3 4 1`** | gene 2: 1 → 3 |
| `1 4 3 2` | **`1 4 2 2`** | gene 3: 3 → 2 |
| `1 4 2 2` | **`1 4 2 3`** | gene 4: 2 → 3 |

**Iteration 1 complete.**

### Step 7: Repeat
Calculate the new fitnesses — if anyone has fitness 6, **STOP**. Otherwise
recompute probabilities, spin the wheel, crossover, mutate again.

> **Exam method — write these five lines and you get the marks:**
> 1. Fitness of each individual (show the pair-counting for at least one).
> 2. Total fitness, then `p_i = f_i / Σf`. **Check they sum to 1.**
> 3. State which parents the wheel selected.
> 4. Show the crossover point explicitly with a `|` and write both children.
> 5. Show which gene mutated.

### GA techniques and applications
**Techniques:** (1) design of the fitness function, (2) **diversity in the
population** must be accounted for, (3) randomization.
**Applications:** creative tasks · exploratory in nature · planning problems ·
static applications.

---

## 4. Ant Colony Optimization — the idea

Real ants find short paths without a map: they lay **pheromone** as they walk,
and prefer paths with more pheromone. A short path gets traversed more often per
unit time, so it accumulates pheromone faster — and the colony converges on it.
Meanwhile pheromone **evaporates**, so bad old paths fade.

> **The two forces to name in every ACO answer:**
> **pheromone reinforcement → exploitation** (enhancing the found path) and
> **pheromone evaporation → exploration** (discovering new paths).

### Pseudo-code
```
Procedure ACO
  Schedule Activities
      Initialization
      Construction
      Update Pheromone
      Daemon Actions   {optional}   // local search, elitism
  End schedule activities
End ACO
```

### Parameters — memorise this table

| Symbol | Meaning |
|---|---|
| `N` | Total number of ants, `N > 1` |
| `τ₀` | Initial pheromone amount |
| `τij` | Pheromone deposited while traversing from `i` to `j` |
| `ηij` | **Visibility / heuristic information** = `1/dij`, where `dij` is the cost of link (i,j) |
| `α` | Importance coefficient of **pheromone** intensity |
| `β` | Importance coefficient of **route cost / visibility** |
| `ρ` | **Evaporation coefficient**, `0 < ρ < 1` |
| `visit_k` | Visited-nodes table of the `k`th ant |
| `Q` | Constant pertaining to the pheromone trail |
| `f_k` (or `L_k`) | **Route cost obtained by ant k** |

### Formula box — straight off the official formula sheet (CS-5)

```
1.  TRANSITION PROBABILITY

              [τij]^α · [ηij]^β
    P^k_ij = ────────────────────────        summed over h NOT in visit_k
              Σ  [τih]^α · [ηih]^β

2.  VISIBILITY          ηij = 1 / dij

3.  PHEROMONE DEPOSITED BY ANT k

    Δτ^k_ij =  Q / L_k    if ant k passes i and j
               0          otherwise

4.  PHEROMONE UPDATE    τij  <-  (1 − ρ)·τij  +  Σ Δτ^k_ij

5.  PHEROMONE EVAPORATION (unused edges)    τij  <-  (1 − ρ)·τij
```

> **Read the transition probability as a tug-of-war.** `τ^α` is *"how many ants
> came this way before"* (experience). `η^β = (1/d)^β` is *"how short this edge
> is"* (greed). `α` and `β` set who wins. The denominator just normalises over
> the cities **not yet visited**.

**Stopping criterion:** reaching a predetermined number of iterations.
**Problem with that:** reaching the iteration limit *before* reaching the
destination — leading to **ant drop**.

---

## 5. NUMERICAL — the TSP tour (slides' own numbers, fully verified)

**Problem:** given `n` cities, find the shortest tour visiting each exactly once.
Consider a complete graph; `dij` is the route cost over `(i,j)`.

### Setup
`No. of ants = No. of cities = 5` · **start at city 4** ·
`α = 0.5` · `β = 0.75` · `ρ = 0.1` · `Q = 100`

**Distance matrix `d`:**

| | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| **1** | 0 | 65 | 52 | 69 | 72 |
| **2** | 65 | 0 | 39 | 28 | 43 |
| **3** | 52 | 39 | 0 | 72 | 62 |
| **4** | 69 | 28 | 72 | 0 | 49 |
| **5** | 72 | 43 | 62 | 49 | 0 |

**Initial pheromone `τ` (symmetric):**

| edge | τ | edge | τ |
|---|---|---|---|
| 1–2 | 0.54 | 2–3 | 0.53 |
| 1–3 | 0.53 | 2–4 | 0.39 |
| 1–4 | 0.35 | 2–5 | 0.18 |
| 1–5 | 0.24 | 3–4 | 0.32 |
| | | 3–5 | **0.90** |
| | | 4–5 | 0.68 |

### Step 1 — at city 4, unvisited {1, 2, 3, 5}

Numerator for each candidate `j` is `τ4j^0.5 × (1/d4j)^0.75`:

| j | τ4j | τ^0.5 | d4j | (1/d)^0.75 | product |
|---|---|---|---|---|---|
| 1 | 0.35 | 0.59161 | 69 | 0.041770 | **0.024711** |
| 2 | 0.39 | 0.62450 | 28 | 0.082155 | **0.051305** |
| 3 | 0.32 | 0.56569 | 72 | 0.040458 | **0.022886** |
| 5 | 0.68 | 0.82462 | 49 | 0.053995 | **0.044525** |
| | | | | **Σ =** | **0.143429** |

```
P41 = 0.024711 / 0.143429 = 0.1723
P42 = 0.051305 / 0.143429 = 0.3577   <- MAXIMUM
P43 = 0.022886 / 0.143429 = 0.1596
P45 = 0.044525 / 0.143429 = 0.3104
                              ------
                          sum = 1.0000  ✓
```

**`P42` is max → the ant moves from 4 to 2.**

### Step 2 — at city 2, `visit_k = 4–2`, unvisited {1, 3, 5}

| j | τ2j | τ^0.5 | d2j | (1/d)^0.75 | product |
|---|---|---|---|---|---|
| 1 | 0.54 | 0.73485 | 65 | 0.043683 | **0.032101** |
| 3 | 0.53 | 0.72801 | 39 | 0.064077 | **0.046649** |
| 5 | 0.18 | 0.42426 | 43 | 0.059552 | **0.025266** |
| | | | | **Σ =** | **0.104015** |

```
P21 = 0.3086
P23 = 0.4485   <- MAXIMUM
P25 = 0.2429
```

**Ant moves from 2 to 3.**

### Step 3 — at city 3, `visit_k = 4–2–3`, unvisited {1, 5}

| j | τ3j | τ^0.5 | d3j | (1/d)^0.75 | product |
|---|---|---|---|---|---|
| 1 | 0.53 | 0.72801 | 52 | 0.051641 | **0.037595** |
| 5 | 0.90 | 0.94868 | 62 | 0.045259 | **0.042937** |
| | | | | **Σ =** | **0.080532** |

```
P31 = 0.4668
P35 = 0.5332   <- MAXIMUM
```

**Ant moves from 3 to 5.**

### Steps 4 and 5 — forced moves
Only city 1 is left, so `5 → 1` (probability 1). Then the tour must return to
the origin: `1 → 4`.

```
visit_k = 4 - 2 - 3 - 5 - 1 - 4
```

### Tour cost and pheromone update

```
L = d42 + d23 + d35 + d51 + d14
  = 28  + 39  + 62  + 72  + 69
  = 270

Δτ = Q / L = 100 / 270 = 0.3704
```

Now apply `τij ← (1 − ρ)·τij + Δτ`, with `ρ = 0.1` so `(1 − ρ) = 0.9`:

| Edge | On the tour? | Calculation | New τ |
|---|---|---|---|
| 4–2 | **yes** | `0.9 × 0.39 + 0.3704 = 0.3510 + 0.3704` | **0.7214** |
| 2–3 | **yes** | `0.9 × 0.53 + 0.3704 = 0.4770 + 0.3704` | **0.8474** |
| 3–5 | **yes** | `0.9 × 0.90 + 0.3704 = 0.8100 + 0.3704` | **1.1804** |
| 5–1 | **yes** | `0.9 × 0.24 + 0.3704 = 0.2160 + 0.3704` | **0.5864** |
| 1–4 | **yes** | `0.9 × 0.35 + 0.3704 = 0.3150 + 0.3704` | **0.6854** |
| 1–2 | no | `0.9 × 0.54` (evaporation only) | **0.4860** |
| 1–3 | no | `0.9 × 0.53` | **0.4770** |
| 2–5 | no | `0.9 × 0.18` | **0.1620** |
| 3–4 | no | `0.9 × 0.32` | **0.2880** |
| 4–5 | no | `0.9 × 0.68` | **0.6120** |

> **The mechanism in one sentence:** edges on the tour get evaporation *plus* a
> deposit and grow; edges off the tour get evaporation *only* and shrink. Over
> many ants, short tours accumulate more pheromone because `Q/L` is larger when
> `L` is smaller.
>
> The slides apply the deposit **after each move** rather than at the end of the
> tour — same formula, just using the partial route cost as `f_k`. Follow
> whichever the question sets up.

> **Exam traps in ACO:**
> 1. `η = 1/d`, **not** `d`. Forgetting the reciprocal inverts the whole answer.
> 2. The denominator sums **only over unvisited cities** (`h ∉ visit_k`).
> 3. `α` applies to `τ`, `β` applies to `η`. Swapping them is the commonest slip.
> 4. **Check your probabilities sum to 1** at every step.

---

## 6. Neuroevolution — NEAT → DeepNEAT → CoDeepNEAT

> **Neuroevolution = using genetic algorithms to evolve neural networks.**

### The core loop
```
1. Create many neural networks (population)
2. Train each network
3. Measure performance (fitness)
4. Select the best networks
5. Generate new networks using mutation and crossover
6. Repeat
```
- **Population** → set of networks
- **Fitness** → how well the network performs
- **Generation** → one cycle of evolution

### The progression — *the exam wants the "why" at each arrow*

| | What it evolves | Why the next one was needed |
|---|---|---|
| **NEAT**<br>*NeuroEvolution of Augmenting Topologies* | Networks as a **graph**: nodes = **individual neurons**, edges = connections. Starts minimal, gradually adds nodes and connections. | **Does not scale to deep learning.** It evolves individual neurons, not layered architectures. Modern CNNs/LSTMs need layer-wise design. |
| **DeepNEAT** | Each **node = an entire LAYER**, storing type (Convolution, Dense, LSTM) and hyperparameters (filters, kernel size, activation). Edges define data flow and **do not store weights**. | Networks come out **random, complex and unstructured**. Real models (ResNet, GoogLeNet) use **repeated, well-organised blocks**. DeepNEAT does not reuse structures. |
| **CoDeepNEAT**<br>*Co-evolving DeepNEAT* | **Two co-evolving populations** — **Blueprints** (macro) and **Modules** (micro). | — the answer |

### Two NEAT concepts that get asked
- **Innovation numbers** — a unique ID assigned to each structural mutation.
  They let you **match corresponding genes correctly during crossover**, so
  recombining two different topologies is meaningful rather than random.
- **Speciation** — similar networks are grouped into **species** by structure;
  each species evolves separately, which **maintains diversity** and protects
  new (initially weak) structures from being wiped out immediately.

### CoDeepNEAT — genotype vs phenotype

| | **Blueprint** (macro-architecture) | **Module** (micro-architecture) |
|---|---|---|
| Represents | High-level structure — the **skeleton** | A small reusable **sub-network** |
| Each node | Refers to a **module species ID** — a **placeholder**, NOT a direct layer | Defines layer types (Conv, Dense, LSTM) and hyperparameters |
| Edges | Data flow between modules | — |
| Evolved | as one population | **independently, in subpopulations** |

**Phenotype construction** — the phenotype is the **actual neural network** used
for training:
```
1. Select a blueprint                    (defines the overall data flow)
2. Identify nodes in the blueprint       (each = a module placeholder / species ID)
3. For each node, select a module        from its subpopulation
4. Replace each node with its module     (node expands into a subnetwork)
5. Connect the modules                   following the blueprint topology
```
When multiple inputs arrive at a node they are combined by **concatenation or
summation**; if there is a **size mismatch**, **pooling or downsampling** is
applied.

> **The one-line reason CoDeepNEAT beats DeepNEAT:** separating blueprint from
> module means a good building block can be **reused and repeated** at several
> positions — which is exactly what ResNet and GoogLeNet do by hand.

### Bilevel optimization — *"DNA vs Weights"*

| Level | What | How |
|---|---|---|
| **Architecture** (DNA / topology) | Which layers, how connected | **Evolutionary algorithm** — high-level search |
| **Weights** (learned parameters) | The numbers inside those layers | **Gradient descent during training** — low-level learning |

> Evolution explores **structural design**; learning optimizes **performance
> within** that structure.

### Formula box (CS-6, official formula sheet)
```
Normalized value = Pixel value / 255       -- image normalization
ReLU(x) = max(0, x)                        -- activation

                Correct predictions
Accuracy   =  ───────────────────── × 100
                Total predictions

Fitness    =  Validation Performance       -- architecture evaluation
```

**Fitness in neuroevolution is whatever measures the network** — validation
accuracy for classification, and the slides' image-captioning example uses the
**BLEU score**.

### Worked mini-examples from the slides
- **Selection:** four architectures with fitness `A: 80%, B: 60%, C: 40%,
  D: 20%` — the top performers are kept as parents.
- **Mutation:** original architecture `Convolution (3×3) → Pooling → Dense`;
  mutation changes the convolution filter size to **5×5**.
- **Application:** an image-captioning system evolving **CNN modules** for image
  feature extraction and **LSTM modules** for text generation, scored by BLEU.

---

## 7. You try

**Q1 (GA, full generation).** Population of 4, fitness = **non-attacking pairs**
of 4 queens, threshold 6:

```
   A = 2 4 1 3        B = 1 1 4 4        C = 3 1 4 2        D = 2 2 3 3
```
(a) Compute the fitness of each. (b) Should the algorithm stop? Why?
(c) If not, compute the roulette-wheel probabilities and check they sum to 1.

**Q2 (GA, crossover).** Take parents `P1 = 2 4 1 3` and `P2 = 1 3 4 2` with a
single-point crossover **after gene 2**. Write both children. Then mutate gene 4
of the first child from its value to `1` and give the result.

**Q3 (ACO).** Using the same TSP setup (`α = 0.5, β = 0.75`), an ant is at
**city 1** with `visit_k = {1}` — so cities 2, 3, 4, 5 are all unvisited. Using
the original τ and d tables from §5, compute `P12, P13, P14, P15`. Which city
does it move to? *(Check they sum to 1.)*

**Q4 (ACO update).** An ant completes the tour `1–3–2–4–5–1`. (a) Compute the
tour length `L`. (b) Compute `Δτ = Q/L` with `Q = 100`. (c) Update `τ13` and
`τ12` with `ρ = 0.1` — one is on the tour and one is not.

**Q5 (concept).** Why does ACO need **both** pheromone reinforcement and
evaporation? What would go wrong if you removed evaporation?

**Q6 (concept).** In `P^k_ij`, what do `α` and `β` control? What happens if you
set `α = 0`? What if you set `β = 0`?

**Q7 (concept).** NEAT → DeepNEAT → CoDeepNEAT. Give **one sentence per arrow**
explaining the limitation that forced the next method.

**Q8 (concept).** What is the difference between a **blueprint** and a **module**
in CoDeepNEAT, and what does a blueprint *node* actually contain?

**Q9 (concept).** Explain "bilevel optimization" in CoDeepNEAT — which part uses
evolution and which uses gradient descent, and why not use one method for both?

---

## 8. Answers

<details>
<summary>Open only after attempting</summary>

**Q1 (a) Fitness = non-attacking pairs (out of 6)**

| State | Attacking pairs | **Fitness** |
|---|---|---|
| A = `2 4 1 3` | none | **6** |
| B = `1 1 4 4` | (1,2) same row · (3,4) same row · **(1,4) diagonal** `|1−4|=3 = |1−4|=3` → **3 attacking** | **3** |
| C = `3 1 4 2` | none | **6** |
| D = `2 2 3 3` | (1,2) same row · (3,4) same row · (2,3) diagonal `|2−3|=1 = |2−3|=1` → **3 attacking** | **3** |

> **The one people miss is B's pair (1,4).** Columns 1 and 4 are 3 apart, and
> rows 1 and 4 are also 3 apart — so they are on a diagonal. It is easy to spot
> the two same-row pairs and stop counting. **Always walk all `C(4,2) = 6` pairs.**

**(b) YES, STOP.** Both A and C have fitness **6 = the threshold**, which for
4 queens is a complete non-attacking solution. Step 3 of the algorithm says halt
as soon as any state reaches the threshold — you do **not** run selection.

**(c)** If you were asked to continue anyway: total = `6+3+6+3 = 18`, so
`p_A = 6/18 = 0.333`, `p_B = 3/18 = 0.167`, `p_C = 6/18 = 0.333`,
`p_D = 3/18 = 0.167`. Sum = `18/18 = 1.00` ✓

**Q2 — Crossover after gene 2**
```
   P1 = 2 4 | 1 3        child1 = 2 4 | 4 2   ->   2 4 4 2
   P2 = 1 3 | 4 2        child2 = 1 3 | 1 3   ->   1 3 1 3
```
Mutating gene 4 of child1 from `2` to `1`: **`2 4 4 1`**.

**Q3 — ACO from city 1**

Numerator `= τ1j^0.5 × (1/d1j)^0.75`:

| j | τ1j | τ^0.5 | d1j | (1/d)^0.75 | product |
|---|---|---|---|---|---|
| 2 | 0.54 | 0.73485 | 65 | 0.043683 | 0.032101 |
| 3 | 0.53 | 0.72801 | 52 | 0.051641 | 0.037595 |
| 4 | 0.35 | 0.59161 | 69 | 0.041770 | 0.024711 |
| 5 | 0.24 | 0.48990 | 72 | 0.040458 | 0.019820 |
| | | | | **Σ =** | **0.114227** |

```
P12 = 0.032101 / 0.114227 = 0.2810
P13 = 0.037595 / 0.114227 = 0.3291   <- MAXIMUM
P14 = 0.024711 / 0.114227 = 0.2163
P15 = 0.019820 / 0.114227 = 0.1735
                              ------
                        sum = 0.9999 ≈ 1  ✓
```
**The ant moves from 1 to 3.**

**Q4 — Tour `1–3–2–4–5–1`**

(a) `L = d13 + d32 + d24 + d45 + d51 = 52 + 39 + 28 + 49 + 72 = ` **240**

(b) `Δτ = Q/L = 100/240 = ` **0.4167**

(c) Edge **1–3 is on the tour**:
`τ13 = 0.9 × 0.53 + 0.4167 = 0.4770 + 0.4167 = ` **0.8937**
Edge **1–2 is NOT on the tour** — evaporation only:
`τ12 = 0.9 × 0.54 = ` **0.4860**

Note this tour (240) is shorter than §5's tour (270), so it deposits *more*
pheromone (`0.4167 > 0.3704`). That is the entire mechanism in one comparison.

**Q5.** **Reinforcement** is **exploitation** — it strengthens paths that ants
actually found good, so the colony converges. **Evaporation** is **exploration**
— it lets old information decay so the colony is not permanently locked into an
early, mediocre discovery.

Without evaporation, pheromone would only ever accumulate. The first tour found
— however bad — would keep gaining trail, every later ant would be more likely
to follow it, and that positive feedback would lock the colony into a
**premature local optimum** with no way to recover.

**Q6.** `α` is the **importance of pheromone intensity** (accumulated experience);
`β` is the **importance of route cost / visibility** (`η = 1/d`, i.e. greed for
short edges).

- **`α = 0`** → pheromone is ignored (`τ^0 = 1`). The ants never learn from each
  other; the algorithm degenerates into a **stochastic greedy nearest-neighbour
  search** driven purely by edge length.
- **`β = 0`** → distance is ignored. Ants follow pheromone only, so the colony
  latches onto whatever was found first and converges very fast to a likely-bad
  tour — **premature convergence**.

**Q7 — The two arrows**
- **NEAT → DeepNEAT:** NEAT evolves *individual neurons and connections*, which
  does not scale to deep models like CNNs and LSTMs that need **layer-wise**
  design — so DeepNEAT makes each node an **entire layer**.
- **DeepNEAT → CoDeepNEAT:** DeepNEAT's networks come out **random and
  unstructured** with no reuse of learned structures, unlike real architectures
  (ResNet, GoogLeNet) built from **repeated blocks** — so CoDeepNEAT splits
  evolution into **reusable modules** plus a **blueprint** that arranges them.

**Q8.** A **blueprint** is the **macro-architecture** — the skeleton defining
overall structure and data flow. A **module** is the **micro-architecture** — a
small reusable sub-network defining actual layer types and hyperparameters.

**A blueprint node contains a module *species ID* — a placeholder — not a layer.**
That is the key point: the node is filled in at phenotype-construction time by
picking a module from that species.

**Q9.** **Architecture (the DNA/topology) is evolved** by the genetic algorithm;
**weights are learned** by gradient descent during training.

They are split because the two search problems have different shapes. Architecture
is **discrete and non-differentiable** — you cannot take a gradient with respect
to "add a convolution layer" — so it needs a derivative-free method like
evolution. Weights are **continuous and differentiable**, where gradient descent
is enormously more efficient than evolution would be. Each method is used where
it is strongest: **evolution explores structure, learning optimizes performance
within that structure.**

</details>

---

## 9. Two-minute recall card

**Genetic Algorithms**
- 7 steps: represent → initial population → fitness → **selection** → **crossover** → **mutation** → repeat.
- **`p_i = fitness_i / Σ fitness`** — the roulette wheel. Check it sums to 1.
- Selection methods: **roulette wheel, tournament, rank**.
- Crossover: **single-point, multi-point, uniform**.
- Mutation exists to **restore diversity** — without it a converged population is stuck.
- Stop on: threshold fitness reached · max generations · no change from last iteration.
- **"No convergence rule or guarantee."**

**ACO**
- `η = 1/d` (**reciprocal!**) · `α` weights **τ** · `β` weights **η**.
- `P^k_ij = τij^α · ηij^β / Σ_{h ∉ visit_k} τih^α · ηih^β` — denominator over **unvisited only**.
- `Δτ^k = Q / L_k` · update `τ ← (1−ρ)τ + ΣΔτ` · unused edges get `(1−ρ)τ` only.
- Reinforcement = **exploitation**; evaporation = **exploration**.
- `0 < ρ < 1`. Stop on iteration limit — risk is **ant drop**.

**Neuroevolution**
- **NEAT** = neurons as nodes · **DeepNEAT** = layers as nodes · **CoDeepNEAT** = blueprints + modules.
- **Innovation numbers** align genes during crossover; **speciation** preserves diversity.
- Blueprint node = **module species ID (placeholder)**, not a layer.
- **Bilevel:** evolution for architecture, **gradient descent for weights**.
- `Fitness = validation performance` · `Accuracy = correct/total × 100` ·
  `normalized = pixel/255` · `ReLU(x) = max(0,x)`.
