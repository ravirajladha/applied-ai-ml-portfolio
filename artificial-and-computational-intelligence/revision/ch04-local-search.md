# Ch 4 — Local Search & Optimization
**Slides: CS#4 (end) and CS#5 (start)** (pre-midsem deck, pages 36–41)

> Open `explainers/ch04-local-search.html` first — it lets you climb the hill
> yourself and get stuck in a local maximum on purpose.

---

## 1. The shift in thinking

Everything up to Chapter 3 said: **the path is the solution**. Local search says
the opposite.

| Chapters 2–3 (path search) | Chapter 4 (local search) |
|---|---|
| The **path to the goal** is the solution | **A state itself** is the solution |
| Builds a whole search tree | Keeps a **single current state** |
| Must remember where it's been | **Ignores paths entirely** |
| Memory `O(b^d)` or `O(bm)` | **Very little memory** |
| Needs a finite, enumerable space | Works in **large or infinite (continuous)** spaces |

> **Slide wording:** *"In many optimization problems, the path to the goal is
> irrelevant; the goal state itself is the solution."*

Think 8-queens. Nobody cares *how* you arrived at a non-attacking arrangement —
only that the final board is valid.

### Pure optimization problems
- All states have an **objective function**.
- The goal is to find the state with the **max (or min)** objective value.
- Does not fit the path-cost / goal-state formulation.
- Local search does **quite well** on these.

### Applications (a short list question)
Hyperparameter tuning in ML · feature selection · robotics path planning ·
scheduling and timetabling · **VLSI design**.

---

## 2. The classification table — memorise this

> **Local search** — search in the state space **in the neighbourhood of the
> current position** until an optimal solution is found.

| | **Single instance based** | **Multiple instance (population) based** |
|---|---|---|
| | Hill Climbing | Genetic Algorithm |
| | Local Beam Search | Ant Colony Optimization |
| | Simulated Annealing | Particle Swarm Optimization |
| | Tabu Search | |

- **Goal:** navigate a state space so that an optimal solution can be found.
- **Objective:** minimise or maximise the objective evaluation function.
- **Scope:** **local**.
- **Objective function / fitness value:** evaluates the *goodness* of the current
  solution.

> **Careful with Local Beam Search.** It keeps `k` states, so it *looks*
> population-based — but the slides classify it as **single-instance**. Quote the
> table as given.

---

## 3. Terminology, on one 4-Queens example

Representation: `[V1 V2 V3 V4]` where `Vi` = the **row** of the queen in
**column i**. So `[2,4,2,2]` means column 1's queen is on row 2, column 2's on
row 4, and so on.

**Fitness `h(n)` = number of conflicting pairs of queens** (to **minimise**).
Two queens conflict if they share a **row** or a **diagonal**
(`|Δrow| = |Δcolumn|`). Columns can never clash — one queen per column by
construction.

| State | Name | h(n) = conflicting pairs |
|---|---|---|
| `[2,4,2,2]` | **Feasible state** (the start) | **4** |
| `[2,4,3,2]` | Neighbour state | **4** |
| `[2,4,2,3]` | Neighbour state | **2** |
| `[2,4,1,3]` | **Optimal solution** | **0** |

### Working out h(n) for `[2,4,2,2]` — all 6 pairs

There are `C(4,2) = 6` pairs to check.

| Pair | Rows | Same row? | Diagonal? `|Δrow| = |Δcol|` | Conflict? |
|---|---|---|---|---|
| (1,2) | 2, 4 | no | `|2−4|=2`, `|1−2|=1` | no |
| (1,3) | 2, 2 | **yes** | — | **✗ conflict** |
| (1,4) | 2, 2 | **yes** | — | **✗ conflict** |
| (2,3) | 4, 2 | no | `2 ≠ 1` | no |
| (2,4) | 4, 2 | no | `|4−2|=2`, `|2−4|=2` | **✗ conflict (diagonal)** |
| (3,4) | 2, 2 | **yes** | — | **✗ conflict** |

**h(n) = 4 conflicting pairs.**

> **Two fitness functions, opposite directions — the formula sheet lists both:**
> - `h(n) = number of CONFLICTING pairs of queens` → **MINIMISE**, goal is 0
> - `h(n) = number of NON-CONFLICTING pairs` → **MAXIMISE**, goal is `C(n,2)`
>
> For 4 queens they sum to **6**; for 8 queens they sum to **28**.
> **Read the question carefully** — using the wrong direction turns a correct
> calculation into a wrong answer.

### Neighbourhood expansion (1NN and 2NN)

From `[2,4,2,2]`, the **1-nearest-neighbour** set means "change **one** queen":
`(2→1) (2→3) (2→4)` for each column, and so on. The **2NN** set means change
**two** queens at once — the slide shows all 6 column pairs
(`V1V2, V1V3, V1V4, V2V3, V2V4, V3V4`), each with **9** variants.

---

## 4. Hill Climbing

### The algorithm
```
1. Select a random state
2. Evaluate the fitness scores of ALL successors of the current state
3. Move to the best successor
4. Repeat until no successor is better
```

That is it. It is sometimes called **greedy local search** — it always takes the
steepest uphill step and never looks back.

| Property | Hill Climbing |
|---|---|
| Memory | **`O(1)`** — one state |
| Complete? | **No** |
| Optimal? | **No** |
| Fails on | local maxima, ridges, plateaux |

### The three ways it fails — *a guaranteed exam question*

| Failure | What it is | The analogy |
|---|---|---|
| **Local maximum** | A peak that is higher than all neighbours but **lower than the global maximum**. Nothing nearby improves, so it stops. | You climb the nearest hill and declare it Everest |
| **Plateau / shoulder** | A flat region where all neighbours have **equal** fitness. No direction looks better, so it has no reason to move. | Standing in fog on a flat field |
| **Ridge** | A sequence of local maxima where **every single step downhill is required** to make progress. Steep on both sides, and no single move improves. | Walking a knife-edge where every step forward feels like falling |

### Termination conditions (slides list three)
1. When **no successor has a better fitness value**.
2. When the **global maximum / minimum** is attained.
3. When a predefined number of restarts **`k`** is reached.

---

## 5. The three hill-climbing variants

### (a) Hill Climbing with Random Restart
When stuck, **throw the state away and start again from a new random state**.
Keep the best result found across all restarts.

> **The one-line justification:** *if the probability of any single run reaching
> the global optimum is `p`, then with enough restarts success becomes almost
> certain — the expected number of restarts is `1/p`.* Random restart trades
> **time** for **completeness**.

### (b) Stochastic Hill Climbing — *this one has a formula*
Instead of always taking the best successor, **pick a successor at random, with
probability proportional to its fitness**. Better neighbours are more likely, but
worse ones are still possible — which is how it escapes local maxima.

```
FORMULA SHEET (CS-4, #5):

                    Frequency
   Probability = ─────────────────────────
                 Total number of observations
```

#### WORKED — the slide's own example

Neighbour fitness values: `N = {4, 2, 2, 3, 3, 2, 1, 3, 2, 1, 3, 2}` — **12
observations**.

| F(n) | Frequency | Probability |
|---|---|---|
| 1 | 2 | **2/12** = 0.167 |
| 2 | 5 | **5/12** = 0.417 |
| 3 | 4 | **4/12** = 0.333 |
| 4 | 1 | **1/12** = 0.083 |
| | **12** | **12/12 = 1.00** ✓ |

> **Always check the probabilities sum to 1.** Free error detection, three seconds.

### (c) Simulated Annealing
Named after **annealing in metallurgy** — heat metal, then cool it slowly so the
atoms settle into a low-energy crystal instead of a brittle mess.

```
Accept a WORSE move with probability  p = e^(−ΔE / T)

  ΔE = how much worse the move is
  T  = temperature, which DECREASES over time (the cooling schedule)
```

Read the formula as a story:
- **T high (early)** → `p` is near 1 → accepts almost anything → **explores**.
- **T low (late)** → `p` near 0 → refuses downhill moves → **behaves like plain
  hill climbing** → **exploits**.
- **ΔE large** (much worse) → `p` small → very bad moves are rejected even when hot.

> **The intuition worth a sentence:** hill climbing gets stuck because it never
> accepts a worse move. Simulated annealing accepts bad moves *early*, when it
> can still afford to wander, then gradually stops — so it climbs out of local
> maxima at the start and settles at the end.

---

## 6. Local Beam Search

### The algorithm (slide's own steps)
```
1. Initialize k random states
2. Evaluate the fitness scores for ALL successors of the k states
3. Calculate the probability of selecting a successor based on fitness score
4. Select the next state based on the highest probability
5. If the goal is not found, select the next 'k' states based on the probability
6. Repeat from Step 2
```

> **The critical difference from "k independent hill climbers":** at each round
> the successors of **all `k` states are pooled together**, and the best `k` are
> chosen from that **combined pool**. So a state with several good children can
> take over slots from a state with none. **Information passes between the
> threads.** That is the whole point — and it is exactly what an examiner asks
> to distinguish it from parallel random-restart.

### Stochastic Beam Search
Same, but the `k` successors are chosen **probabilistically** (weighted by
fitness) rather than by taking the top `k` deterministically.

**Why:** plain beam search can let all `k` states collapse onto the same region
of the space — you lose diversity and it degenerates into expensive hill
climbing. Sampling keeps the beam spread out.

| | Local Beam Search | Stochastic Beam Search |
|---|---|---|
| Picks the next `k` | **best k** from the pool | **samples k**, weighted by fitness |
| Risk | states clump together, diversity dies | slower to converge |

---

## 7. Online vs Offline Search

Not local search, but taught here — and it is an easy compare-and-contrast question.

| | **Offline search** | **Online search** |
|---|---|---|
| Model of the problem | **Complete, known before acting** | **Unknown** in advance |
| State space | Known or generable in advance | Discovered **while moving** |
| Simulation | Can simulate actions before taking them | Must act to find out |
| Plan vs execute | **Complete plan first, then execute** | Planning and execution **happen together** |
| Must balance | — | **exploration vs progress** toward the goal |
| Examples | BFS, UCS, **A\***, Hill Climbing, Local Beam Search | robot in an unfamiliar building |

**Offline example:** a route planner that knows the full map, road connections
and costs before suggesting a path.
**Online example:** a robot exploring an unfamiliar building — it cannot plan the
full route, so it moves, senses nearby paths, updates its map, and decides again.

Online search is useful when the environment is **unknown, dynamic, or too large
to fully model**.

---

## 8. You try

**Q1 (fitness).** For the 4-Queens state `[3,1,4,2]`, compute **both** the number
of conflicting pairs and the number of non-conflicting pairs. Show all 6 pairs.
Is it a solution?

**Q2 (fitness).** Same for `[2,4,3,2]`. Check your two numbers add to 6.

**Q3 (stochastic HC).** A state's neighbours have fitness values
`{3, 1, 2, 3, 3, 4, 2, 1, 3, 2}`. Build the frequency/probability table and
verify it sums to 1. Which fitness value is most likely to be selected?

**Q4 (concept).** Name the three ways hill climbing fails, and for each say in
one line *why* the algorithm cannot escape.

**Q5 (concept).** In simulated annealing, what happens to the acceptance
probability `p = e^(−ΔE/T)` as `T → 0`? What algorithm does SA become at that
point?

**Q6 (concept).** Explain the difference between **local beam search with k
states** and **k independent random-restart hill climbers**. One sentence.

**Q7 (concept).** Classify each as single-instance or population-based:
Tabu Search · Ant Colony Optimization · Simulated Annealing · Genetic Algorithm ·
Local Beam Search · Particle Swarm Optimization.

**Q8 (concept).** Give one example each of a problem best solved by **offline**
search and one by **online** search, and say what makes the difference.

---

## 9. Answers

<details>
<summary>Open only after attempting</summary>

**Q1 — `[3,1,4,2]`**

| Pair | Rows | Same row? | `|Δrow|` vs `|Δcol|` | Conflict? |
|---|---|---|---|---|
| (1,2) | 3, 1 | no | 2 vs 1 | no |
| (1,3) | 3, 4 | no | 1 vs 2 | no |
| (1,4) | 3, 2 | no | 1 vs 3 | no |
| (2,3) | 1, 4 | no | 3 vs 1 | no |
| (2,4) | 1, 2 | no | 1 vs 2 | no |
| (3,4) | 4, 2 | no | 2 vs 1 | no |

**Conflicting = 0. Non-conflicting = 6.**
**Yes — this is a valid solution** to the 4-Queens problem.

**Q2 — `[2,4,3,2]`**

| Pair | Rows | Conflict? | Why |
|---|---|---|---|
| (1,2) | 2, 4 | no | 2 ≠ 1 |
| (1,3) | 2, 3 | no | 1 ≠ 2 |
| (1,4) | 2, 2 | **✗** | same row |
| (2,3) | 4, 3 | **✗** | `|4−3|=1 = |2−3|=1` diagonal |
| (2,4) | 4, 2 | **✗** | `|4−2|=2 = |2−4|=2` diagonal |
| (3,4) | 3, 2 | **✗** | `|3−2|=1 = |3−4|=1` diagonal |

**Conflicting = 4. Non-conflicting = 2.** Check: `4 + 2 = 6` ✓
(This matches the slide's stated `h(n) = 4` for this state.)

**Q3 — Stochastic hill climbing**

`{3, 1, 2, 3, 3, 4, 2, 1, 3, 2}` — **10 observations**.

| F(n) | Frequency | Probability |
|---|---|---|
| 1 | 2 | 2/10 = 0.20 |
| 2 | 3 | 3/10 = 0.30 |
| 3 | 4 | **4/10 = 0.40** |
| 4 | 1 | 1/10 = 0.10 |
| | **10** | **1.00** ✓ |

**Fitness value 3 is most likely** (p = 0.40) — note it is *not* the best value
(4 is), which is exactly the point of stochastic hill climbing: it favours good
moves without committing to the best one.

**Q4 — The three failures**
- **Local maximum** — every neighbour is worse, so the "move only if better" rule
  forbids any move. It has no mechanism to go downhill.
- **Plateau / shoulder** — all neighbours are *equal*, so there is no gradient to
  follow; the algorithm has no basis for choosing a direction.
- **Ridge** — the peak lies along a narrow crest, and **every available single
  move steps down** off the crest, even though a sequence of moves would climb.
  Hill climbing only looks one step ahead, so it cannot see the sequence.

**Q5.** As `T → 0`, the exponent `−ΔE/T → −∞`, so **`p → 0`** — it accepts
essentially **no** worse moves. At that point simulated annealing has become
**ordinary hill climbing**. That is the design: explore while hot, exploit while
cold.

**Q6.** In **local beam search** the successors of all `k` states are pooled and
the best `k` are chosen from that **shared** pool, so a productive state can take
over slots from unproductive ones — **information flows between the threads**;
`k` independent restarts share nothing and each run is completely isolated.

**Q7 — Classification**

| Single instance | Population based |
|---|---|
| Tabu Search | Ant Colony Optimization |
| Simulated Annealing | Genetic Algorithm |
| Local Beam Search | Particle Swarm Optimization |

(Local Beam Search is the counter-intuitive one — it keeps `k` states but the
slides classify it as single-instance.)

**Q8.** **Offline:** a route planner with the full road map — the entire state
space is known in advance, so it can produce a complete plan and then execute it
blindly. **Online:** a robot exploring an unfamiliar building — it cannot plan
ahead because it discovers the environment by moving through it, so planning and
execution are interleaved and it must balance exploration against progress.

**The difference is whether the agent has a complete model of the problem before
it acts.**

</details>

---

## 10. Two-minute recall card

- Local search: **single current state, move to neighbours, ignore paths**. Memory `O(1)`.
- **The state IS the solution** — the path is irrelevant.
- Single-instance: **Hill Climbing, Local Beam, Simulated Annealing, Tabu**.
  Population: **GA, ACO, PSO**.
- 4-Queens fitness: conflicting pairs (**minimise**, goal 0) or non-conflicting
  (**maximise**, goal 6 for n=4, **28 for n=8**). They sum to `C(n,2)`.
- Queens conflict on **same row** or `|Δrow| = |Δcol|` (diagonal). Never columns.
- HC fails three ways: **local maximum, plateau/shoulder, ridge**.
- Stochastic HC: **`Probability = Frequency / Total observations`**.
- Simulated annealing: **`p = e^(−ΔE/T)`**. `T` high → explore; `T → 0` → becomes
  plain hill climbing.
- Beam search pools **all successors of all k states** and picks the best `k`
  from the shared pool — *not* `k` independent runs.
- Stochastic beam search **samples** the `k` instead, to preserve diversity.
- HC termination: no better successor · global optimum reached · `k` restarts done.
- Offline = complete model before acting (BFS, UCS, A*, HC, Beam).
  Online = discovers the environment while moving; plan and execute together.
