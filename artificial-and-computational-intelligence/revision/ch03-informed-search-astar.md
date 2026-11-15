# Ch 3 — Informed (Heuristic) Search: Greedy, A*, and Heuristic Design
**Slides: CS#3 (end) and CS#4** (pre-midsem deck, pages 23–36)

> Open `explainers/ch03-informed-search-astar.html` first — it runs Greedy and A*
> side by side on the same graph so you can watch them disagree.

This is the **highest-yield numerical chapter in the pre-midsem half**. Four
things get asked:
1. Run **A\*** on a graph, show `g`, `h`, `f` at every step.
2. Check a heuristic for **admissibility and consistency**.
3. Compute **h1 / h2** (misplaced tiles / Manhattan) for an 8-puzzle state.
4. Compute the **effective branching factor `b*`**.

---

## 1. What a heuristic is

> **Heuristic** — a practical rule of thumb or educated guess that estimates the
> cost **from the current state to the goal**. From the Greek *heuriskein*,
> "to find" or "to discover".

**Key insight (slide wording):** prioritise exploring paths that *seem* most
promising, rather than exploring all possibilities blindly. Like using a compass
and a map in a maze instead of wandering aimlessly.

Why we need it: the **15-puzzle has ~1.3 trillion states**. BFS and DFS explore
systematically but blindly, "like navigating a maze blindfolded". Exponential
growth makes brute force impossible.

Real-life heuristics: Google Maps suggesting routes · chess engines evaluating
board positions · doctors inferring diseases from symptoms · robots estimating
distance to a target.

> **The trade-off spectrum, worth quoting:**
> **Perfect heuristic → `O(d)`. Zero heuristic → `O(b^d)`.**
> A heuristic buys you the entire gap between linear and exponential.
> *"The better the heuristic, the less time."* — Ellen Walker, Hiram College

---

## 2. Formula box — the whole chapter in one box

```
Greedy Best-First Search      f(n) = h(n)
    "how close does this LOOK to the goal?"    -- ignores what you already spent

A* Search                     f(n) = g(n) + h(n)
    g(n) = actual cost from START to n         (what you HAVE spent)
    h(n) = estimated cost from n to GOAL       (what you EXPECT to spend)
    f(n) = estimated total cost of a path through n

Uniform Cost Search           f(n) = g(n)      -- A* with h(n) = 0

ADMISSIBLE (optimistic)       0 <= h(n) <= h*(n)
    h*(n) = the TRUE cost from n to the goal
    "never overestimates"

CONSISTENT (monotonic)        h(n) <= c(n, a, n') + h(n')
    for every node n and every successor n' via action a
    "the estimate never drops by more than the actual step cost"
    => f values never decrease along a path:  f(n') >= f(n)

DOMINANCE                     if h2(n) >= h1(n) for all n, and both admissible,
                              then h2 DOMINATES h1 and is the better heuristic

EFFECTIVE BRANCHING FACTOR    N + 1 = 1 + b* + (b*)^2 + ... + (b*)^d
    N = number of nodes generated,  d = depth of the solution
```

> **The one-line summary of the three algorithms:**
> UCS looks only **backwards** (`g`). Greedy looks only **forwards** (`h`).
> **A\* looks both ways** (`g + h`) — which is why it is the only one that is
> both efficient *and* optimal.

---

## 3. Greedy Best-First Search

Expands the node that **appears closest to the goal**: `f(n) = h(n)`.
It completely ignores `g(n)` — how much you already spent getting here.

The slides describe it as: *"Optimise DFS. Choose next nearest to goal in the
same hill."*

| Property | Greedy Best-First |
|---|---|
| Complete? | **No** (can loop) |
| Optimal? | **No** |
| Time | `O(b^m)` worst case |
| Space | `O(b^m)` — keeps all nodes |

### Slide's own example
h values: `h(1)=60, h(2)=120, h(3)=30, h(4)=40, h(5)=0`, goal = 5.

```
(1)
(1 3) (1 4) (1 2)          <- sorted by h: 30, 40, 120
(1 3 5) (1 3 4)            <- expand 3, its child 5 has h = 0
C(1-3-5) = 100 + 125 = 225

Expanded: 2      Generated: 6      Max queue length: 3
```

> Note what the answer *isn't*: greedy reports **225**, and never checks whether
> some other route is cheaper. It stopped as soon as something looked close.

---

## 4. A* Search

> A* extends the path that minimises `f(n) = g(n) + h(n)`.
> The idea in one line: **avoid expanding paths that are already expensive.**

At each step:
1. Generate successor states.
2. Compute `h` for each successor.
3. Compute `f(n) = g(n) + h(n)`.
4. **Expand the node with the smallest `f(n)`.**

### WORKED EXAMPLE 1 — the slide's 5-node graph

h values: `h(1)=60, h(2)=120, h(3)=70, h(4)=40, h(5)=0`. Start 1, goal 5.
Edges from 1: `1→2 = 70`, `1→3 = 125`, `1→4 = 100`. And `4→5 = 50`.

| Path | g | h | **f = g + h** |
|---|---|---|---|
| `1→2` | 70 | 120 | **190** |
| `1→3` | 125 | 70 | **195** |
| `1→4` | 100 | 40 | **140** ← smallest, expand this |

Expanding `1→4` generates `1→4→5`:

| Path | g | h | **f** |
|---|---|---|---|
| `1→4→5` | 100 + 50 = 150 | 0 | **150** ← smallest, and it's the goal |
| `1→2` | 70 | 120 | 190 |
| `1→3` | 125 | 70 | 195 |

**Answer: `1 → 4 → 5`, cost 150.**
`Expanded: 2 · Generated: 5 · Max queue length: 3`

### WORKED EXAMPLE 2 — Exercise 2 from your slides

```
        S
     1 /  \ 10
      A     \
   2 / \ 1   \
    B    C    \
   5 \  / \ 4  \
      D --- --- G
       \  2    /
        -------
```
Edges: `S→A=1, S→G=10, A→B=2, A→C=1, B→D=5, C→D=3, C→G=4, D→G=2`
Heuristics: `h(S)=5, h(A)=3, h(B)=4, h(C)=2, h(D)=6, h(G)=0`

#### First — Greedy Best-First on this graph

| Step | Expand | Generates | Frontier (sorted by **h**) |
|---|---|---|---|
| 1 | S | A (h=3), G (h=0) | `G(h=0), A(h=3)` |
| 2 | **G (h=0)** | goal test → pass | done |

**Greedy answer: `S → G`, cost = 10.**

Greedy took the direct edge because `h(G) = 0` looked irresistible. It never
noticed that edge costs **10**. This is exactly why greedy is not optimal.

#### Now — A* on the same graph

| Step | Expand | Node | g | h | **f** |
|---|---|---|---|---|---|
| 1 | S (f=5) | A | 1 | 3 | **4** |
| | | G | 10 | 0 | **10** |
| | | *frontier* | | | `A(4), G(10)` |
| 2 | **A (f=4)** | B | 1+2 = 3 | 4 | **7** |
| | | C | 1+1 = 2 | 2 | **4** |
| | | *frontier* | | | `C(4), B(7), G(10)` |
| 3 | **C (f=4)** | D | 2+3 = 5 | 6 | **11** |
| | | G | 2+4 = 6 | 0 | **6** ← cheaper than 10, replace |
| | | *frontier* | | | `G(6), B(7), D(11)` |
| 4 | **G (f=6)** | goal test on expansion → pass | | | |

**A\* answer: `S → A → C → G`, cost 6.**

Verification — every complete path:

| Path | Cost |
|---|---|
| `S→A→C→G` | 1+1+4 = **6** ← optimal |
| `S→A→C→D→G` | 1+1+3+2 = 7 |
| `S→G` | 10 |
| `S→A→B→D→G` | 1+2+5+2 = 10 |

> **Greedy said 10. A\* said 6.** Same graph, same heuristic. The only difference
> is that A* added `g(n)`. If you can explain that in one sentence in the exam,
> you have the concept.

---

## 5. Admissibility and consistency — *guaranteed exam question*

### Admissible (optimistic)

```
0 <= h(n) <= h*(n)        h*(n) = TRUE cost from n to goal
```

> An admissible heuristic **never overestimates** the cost to reach the goal.
> It may underestimate, but must never exaggerate.

**Example:** straight-line distance is admissible for route planning, because
the actual road distance can never be *shorter* than the straight line.

### Consistent (monotonic)

```
h(n) <= c(n, a, n') + h(n')     for every node n and every successor n'
```

> The estimate should **not suddenly drop by more than the actual step cost**.
> This is just the **triangle inequality** on the graph.

**Why it matters:** if `h` is consistent, `f` values **never decrease along a
path**: `f(n') ≥ f(n)`. That guarantees that **once A\* expands a node, the best
path to that node has already been found** — so you never have to reopen it.

### The relationship — memorise this sentence

> **Every consistent heuristic is admissible** (provided `h(goal) = 0`).
> **But every admissible heuristic need NOT be consistent.**

Consistency is the **stronger** condition. Consistent ⇒ admissible, one way only.

### WORKED — the slide's consistency table

Graph edges: `1→2 = 70, 1→4 = 100, 2→4 = 75, 2→5 = 125, 4→5 = 50, 5→1 = 75`.
**Goal = node 3.** Heuristics: `h(1)=80, h(2)=60, h(3)=0, h(4)=200, h(5)=190`.

| n | h(n) | Admissible? `h(n) ≤ h*(n)` | Consistent? for every arc `h(i) ≤ c(i,j) + h(j)` |
|---|---|---|---|
| 1 | 80 | **Y** | **N** — arc `5→1`: needs `190 ≤ 75 + 80 = 155` ✗ |
| 2 | 60 | **N** | Y — `1→2`: `80 ≤ 70 + 60 = 130` ✓ |
| 3 | 0 | Y | — (goal) |
| 4 | 200 | Y | Y — `1→4`: `80 ≤ 100+200 = 300` ✓ · `2→4`: `60 ≤ 75+200 = 275` ✓ |
| 5 | 190 | Y | Y — `2→5`: `60 ≤ 125+190 = 315` ✓ · `4→5`: `200 ≤ 50+190 = 240` ✓ |

**How to actually do this in the exam:**
- **Admissibility** — compute `h*(n)` (the *true* shortest cost from `n` to the
  goal) for each node, then compare. One check per node.
- **Consistency** — one check **per edge**, not per node. Walk every arc `i→j`
  and test `h(i) ≤ c(i,j) + h(j)`. A single failing arc kills consistency.

### The same check on Exercise 2 — a perfect illustration

Optimal costs to `G`: `h*(S)=6, h*(A)=5, h*(B)=7, h*(C)=4, h*(D)=2, h*(G)=0`.

| n | h(n) | h*(n) | Admissible? |
|---|---|---|---|
| S | 5 | 6 | ✓ |
| A | 3 | 5 | ✓ |
| B | 4 | 7 | ✓ |
| C | 2 | 4 | ✓ |
| **D** | **6** | **2** | ✗ **overestimates!** |
| G | 0 | 0 | ✓ |

Consistency, arc by arc:

| Arc | Check | OK? |
|---|---|---|
| `S→A` | `h(S)=5 ≤ 1 + h(A)=3` → `5 ≤ 4` | ✗ **fails** |
| `S→G` | `5 ≤ 10 + 0 = 10` | ✓ |
| `A→B` | `3 ≤ 2 + 4 = 6` | ✓ |
| `A→C` | `3 ≤ 1 + 2 = 3` | ✓ (tight) |
| `B→D` | `4 ≤ 5 + 6 = 11` | ✓ |
| `C→D` | `2 ≤ 3 + 6 = 9` | ✓ |
| `C→G` | `2 ≤ 4 + 0 = 4` | ✓ |
| `D→G` | `6 ≤ 2 + 0 = 2` | ✗ **fails** |

Two things fall out of this, and both are worth stating in an answer:

1. **`h(S)` is admissible but inconsistent** (`5 ≤ 6` ✓, but the `S→A` arc
   fails). This is the concrete proof that **admissible does not imply
   consistent**.
2. **A\* still returned the optimal path (6)** despite `h(D)` overestimating.
   An inadmissible heuristic does not *always* break optimality — it just
   removes the **guarantee**. Here `D` was never on the optimal path, so its
   inflated `h` only pushed it out of the way, harmlessly.

---

## 6. What makes a good heuristic

A good heuristic should be:
1. **Admissible** — never overestimates.
2. **Consistent** — satisfies the triangle inequality across neighbours.
3. **Informative** — close to the actual cost.

> "A good heuristic is like a helpful guide. It does not lie about the distance,
> but it gives enough direction to avoid exploring everywhere."

### Dominance

```
If  h2(n) >= h1(n)  for all n,  and both are admissible,
then h2 DOMINATES h1  and is the better heuristic.
```
Closer to the true cost ⇒ fewer nodes expanded. Extremes:
- `h1(n) = 0` → this **is** Uniform Cost Search. Optimal but slow.
- `h2(n) = straight-line distance` → better guidance, explores fewer nodes.

### The good-vs-poor table

| Heuristic type | Effect on A* |
|---|---|
| `h(n) = 0` | Always optimal, but slow. Same as **UCS**. |
| Admissible but **weak** | Optimal, but may explore many nodes |
| Admissible **and informative** | **Optimal and efficient** ← the target |
| **Overestimating** | May be faster, but **can lose optimality** |
| **Inconsistent** | May require **reopening nodes** to preserve optimality |

> **Combining heuristics:** if you have several admissible heuristics and none
> dominates, take `h(n) = max(h1(n), h2(n), …)`. The max of admissible
> heuristics is still admissible, and it dominates all of them.

---

## 7. Numerical Pattern — the 8-puzzle heuristics

The two standard heuristics, and where they come from:

| | Definition | Relaxation it comes from |
|---|---|---|
| **h1** | Number of **misplaced tiles** | Tiles can **teleport** anywhere |
| **h2** | Sum of **Manhattan distances** of tiles from their goal positions | Tiles can **move through each other** |

Both are **admissible**. `h2 ≥ h1` always, so **h2 dominates h1**.

> **Never count the blank.** Counting the blank breaks admissibility.

### WORKED — the slide's own N-Tile example

```
  Initial            Goal
  1  7  6          -  1  2
  4  8  5          3  4  5
  -  2  3          6  7  8
```

Goal positions (row, col), 0-indexed:
`1→(0,1) · 2→(0,2) · 3→(1,0) · 4→(1,1) · 5→(1,2) · 6→(2,0) · 7→(2,1) · 8→(2,2)`

| Tile | Is at | Should be at | Misplaced? | Manhattan `|Δrow| + |Δcol|` |
|---|---|---|---|---|
| 1 | (0,0) | (0,1) | ✓ | 0 + 1 = **1** |
| 7 | (0,1) | (2,1) | ✓ | 2 + 0 = **2** |
| 6 | (0,2) | (2,0) | ✓ | 2 + 2 = **4** |
| 4 | (1,0) | (1,1) | ✓ | 0 + 1 = **1** |
| 8 | (1,1) | (2,2) | ✓ | 1 + 1 = **2** |
| 5 | (1,2) | (1,2) | ✗ correct | **0** |
| 2 | (2,1) | (0,2) | ✓ | 2 + 1 = **3** |
| 3 | (2,2) | (1,0) | ✓ | 1 + 2 = **3** |

```
h1 = 7   (7 tiles out of place; tile 5 is already home)
h2 = 1 + 2 + 4 + 1 + 2 + 0 + 3 + 3 = 16
```

Check `h2 ≥ h1`: `16 ≥ 7` ✓ — consistent with h2 dominating h1.

> The slide's other test case gives `h1(S) = 8` and
> `h2 = 3+1+2+2+2+3+3+2 = 18`. Same method, different start state.

---

## 8. Heuristic design — the four named techniques

The slides list four ways to get a good heuristic:

### (a) Effective branching factor `b*`
A way to **measure** how good a heuristic is, after the fact.

```
N + 1 = 1 + b* + (b*)^2 + (b*)^3 + ... + (b*)^d
```
`N` = nodes generated, `d` = solution depth. **`b*` closer to 1 = better heuristic.**

**WORKED:** A* generates `N = 6` nodes and finds the solution at depth `d = 2`.

```
6 + 1 = 1 + b* + (b*)^2
    7 = 1 + b + b^2
    b^2 + b - 6 = 0
    (b + 3)(b - 2) = 0
    b* = 2          (discard the negative root)
```

### (b) Relaxed problems
> A **relaxed problem** removes some constraints from the original, making it
> easier to solve. **The cost of the relaxed problem is a lower bound on the
> original cost** — which is exactly what "admissible" means.

That is *why* relaxation always gives you an admissible heuristic, and it is the
one-line justification examiners want.

- 8-puzzle, drop "you can only move into the blank" → tiles teleport → **h1**.
- 8-puzzle, drop "tiles can't overlap" → tiles pass through each other → **h2**.

Note: the state-space graph of a relaxed problem is a **supergraph** of the
original, because removing restrictions only ever *adds* edges.

### (c) Pattern databases
Solve a **small part** of the puzzle first (say just tiles 1–4), store **every
possible configuration and its exact cost** in a table. During search, just look
the answer up. Also: **sub-problem** heuristics.

### (d) Landmarks
Pick a set of **landmark** states that are easy to reach from many others, and
pre-compute distances to them. `h(n)` is then based on the distance from `n` to
the nearest landmark. Used in real road networks — you cannot pre-compute
between every pair of street corners, so you pre-compute to major cities.

### (e) Learning heuristics from experience
- **Metalevel learning** — the AI "thinks about its own thinking", looking at the
  search paths it took and learning to avoid dead ends in future.
- **Feature learning** — solve thousands of random puzzles, spot which features
  (e.g. number of out-of-order tiles) predict the true cost, and combine them
  into a formula.
- **Neural networks** — train a network `h(s, θ)` to predict cost-to-goal from
  the state. The reference paper in your slides uses **7 convolution layers, 4
  CoAt (Convolution + Attention) blocks, mean pooling, and a fully connected
  layer** producing one scalar, evaluated on **Sokoban**, **Maze with Teleports**
  and the **Sliding Tile Puzzle** — all encodable as 2D grids.

---

## 9. Memory-bounded variants

A*'s real weakness is **memory** — it keeps every generated node.

| Variant | What it does |
|---|---|
| **IDA\*** (Iterative Deepening A*) | Memory-bounded A*: depth-first search with an **`f`-cost limit** instead of a depth limit. Raise the limit each round. |
| **SMA\*** (Simplified Memory-bounded A*) | **Drops the worst nodes when memory is full**, retaining the best paths (and remembering their `f` value in the parent so they can be regenerated). |

---

## 10. Problem formulations from CS#4

### N-Queens

| Component | N-Queens |
|---|---|
| Initial state | `<Xi, Yi>` — board positions |
| Possible actions | Place a queen in any non-occupied row |
| Transition model | `isValid` |
| Goal test | Non-attacking — no queen attacks another |
| Path cost | Transition + valid queens |
| **No. of states** | **n!** |

Search tree is built **one row of the board at a time**.

Three candidate heuristics from the slides:
- `H1(n)` = number of **non-conflicting** pairs of queens → **MAXIMISE**
- `H2(n)` = number of **conflicting** pairs of queens → **MINIMISE**
- `H3(n)` = number of **safest** queens → **MAXIMISE**

### N-Tile

| Component | N-Tile |
|---|---|
| Initial state | `<LOC, ID>` |
| Possible actions | Move the **empty** square to a nearby tile |
| Transition model | `ID = LOC + 1` |
| Goal test | Transition + positional + distance (+ other approaches) |
| **No. of states** | **9!** |

---

## 11. You try

**Q1 (A\*).** Run A* on this graph from `S` to `G`. Show `g`, `h`, `f` at every
step and give the final path and cost.

```
   S→A = 2      A→C = 3      C→G = 4
   S→B = 5      B→C = 1      B→G = 7

   h(S)=6,  h(A)=4,  h(B)=5,  h(C)=3,  h(G)=0
```

**Q2 (Greedy vs A\*).** Run **Greedy Best-First** on the same graph. Do the two
algorithms agree? If not, explain in one sentence *why* A* found the better path.

**Q3 (admissibility).** For the graph in Q1, compute `h*(n)` for every node and
state whether the heuristic is admissible. Show the comparison as a table.

**Q4 (consistency).** For the same graph, check consistency **arc by arc**.
List every arc and whether it passes. Is `h` consistent?

**Q5 (8-puzzle).** Compute `h1` (misplaced tiles) and `h2` (Manhattan distance)
for this state. Show the per-tile working for `h2`.

```
  Current            Goal
  2  8  3          1  2  3
  1  6  4          8  -  4
  7  -  5          7  6  5
```

**Q6 (effective branching factor).** A* generates `N = 14` nodes and finds the
solution at depth `d = 3`. Find `b*`.

**Q7 (concept).** State the relationship between admissibility and consistency in
one sentence, and give a one-line reason why **relaxed problems always produce
admissible heuristics**.

**Q8 (concept).** You have two admissible heuristics `h1` and `h2`, and neither
dominates the other. How do you combine them, and why is the result still
admissible?

---

## 12. Answers

<details>
<summary>Open only after attempting</summary>

**Q1 — A\***

| Step | Expand | Node | g | h | **f** | Frontier after |
|---|---|---|---|---|---|---|
| 1 | S (f=6) | A | 2 | 4 | **6** | `A(6), B(10)` |
| | | B | 5 | 5 | **10** | |
| 2 | **A (f=6)** | C | 2+3 = 5 | 3 | **8** | `C(8), B(10)` |
| 3 | **C (f=8)** | G | 5+4 = 9 | 0 | **9** | `G(9), B(10)` |
| 4 | **G (f=9)** | goal test on expansion → pass | | | | done |

**Answer: `S → A → C → G`, cost 9.**

Check all paths: `S→A→C→G = 2+3+4 = 9` ✓ · `S→B→C→G = 5+1+4 = 10` ·
`S→B→G = 5+7 = 12`. So 9 is optimal.

**Q2 — Greedy Best-First** (`f = h` only)

| Step | Expand | Generates | Frontier (by h) |
|---|---|---|---|
| 1 | S | A (h=4), B (h=5) | `A(4), B(5)` |
| 2 | **A (h=4)** | C (h=3) | `C(3), B(5)` |
| 3 | **C (h=3)** | G (h=0) | `G(0), B(5)` |
| 4 | **G** | goal | done |

**Greedy answer: `S → A → C → G`, cost 9.**

**They agree here.** Greedy got lucky — the heuristic happened to point down the
optimal path at every step. That is not a guarantee, and the honest one-sentence
answer is: *greedy has no mechanism to prefer the cheaper path, so any agreement
is luck; A\* adds `g(n)`, which makes it prefer paths that are cheap so far, not
just paths that look close.*

(Contrast with Exercise 2 in §4, where the same setup gave Greedy 10 and A* 6.)

**Q3 — Admissibility**

True costs to `G`:
- `h*(G) = 0`
- `h*(C) = 4` (only `C→G`)
- `h*(B) = min(1+4, 7) = 5`
- `h*(A) = 3 + 4 = 7`
- `h*(S) = min(2+7, 5+5) = 9`

| n | h(n) | h*(n) | `h ≤ h*`? |
|---|---|---|---|
| S | 6 | 9 | ✓ |
| A | 4 | 7 | ✓ |
| B | 5 | 5 | ✓ (tight) |
| C | 3 | 4 | ✓ |
| G | 0 | 0 | ✓ |

**Admissible. Yes** — every estimate is ≤ the true cost.

**Q4 — Consistency**, one check per **arc**:

| Arc | `h(i) ≤ c(i,j) + h(j)` | OK? |
|---|---|---|
| `S→A` | `6 ≤ 2 + 4 = 6` | ✓ (tight) |
| `S→B` | `6 ≤ 5 + 5 = 10` | ✓ |
| `A→C` | `4 ≤ 3 + 3 = 6` | ✓ |
| `B→C` | `5 ≤ 1 + 3 = 4` | ✗ **FAILS** |
| `B→G` | `5 ≤ 7 + 0 = 7` | ✓ |
| `C→G` | `3 ≤ 4 + 0 = 4` | ✓ |

**Not consistent** — the arc `B→C` violates it. One failing arc is enough.

Note this is another admissible-but-inconsistent heuristic, same as `h(S)` in
Exercise 2. It confirms the direction of the implication: **consistent ⇒
admissible, but not the reverse.**

**Q5 — 8-puzzle**

Goal positions: `1→(0,0) · 2→(0,1) · 3→(0,2) · 8→(1,0) · blank→(1,1) · 4→(1,2) · 7→(2,0) · 6→(2,1) · 5→(2,2)`

| Tile | Is at | Goal | Misplaced? | Manhattan |
|---|---|---|---|---|
| 2 | (0,0) | (0,1) | ✓ | 0 + 1 = **1** |
| 8 | (0,1) | (1,0) | ✓ | 1 + 1 = **2** |
| 3 | (0,2) | (0,2) | ✗ correct | **0** |
| 1 | (1,0) | (0,0) | ✓ | 1 + 0 = **1** |
| 6 | (1,1) | (2,1) | ✓ | 1 + 0 = **1** |
| 4 | (1,2) | (1,2) | ✗ correct | **0** |
| 7 | (2,0) | (2,0) | ✗ correct | **0** |
| 5 | (2,2) | (2,2) | ✗ correct | **0** |

```
h1 = 4      (tiles 2, 8, 1, 6 are out of place)
h2 = 1 + 2 + 0 + 1 + 1 + 0 + 0 + 0 = 5
```
Check `h2 ≥ h1`: `5 ≥ 4` ✓. Blank excluded from both, as required.

**Q6 — Effective branching factor**

```
N + 1 = 1 + b* + (b*)^2 + (b*)^3
14 + 1 = 1 + b + b^2 + b^3
    15 = 1 + b + b^2 + b^3

Try b = 2:  1 + 2 + 4 + 8 = 15   ✓ exact
```
**`b* = 2`.**

**Q7.** **Every consistent heuristic is admissible (provided `h(goal) = 0`), but
not every admissible heuristic is consistent** — consistency is the stronger
condition.

Relaxed problems always give admissible heuristics because **removing
constraints can only make the problem easier**, so the optimal cost in the
relaxed problem is a **lower bound** on the optimal cost in the original — and
"lower bound on the true cost" is precisely the definition of admissible.

**Q8.** Take the **maximum**: `h(n) = max(h1(n), h2(n))`.

It stays admissible because **each of `h1` and `h2` is individually ≤ `h*(n)`**,
so the larger of the two is still ≤ `h*(n)`. And since `max ≥ h1` and
`max ≥ h2`, the combined heuristic **dominates both**, so it expands no more
nodes than either alone.

</details>

---

## 13. Two-minute recall card

- `Greedy: f = h` · `A*: f = g + h` · `UCS: f = g` (= A* with h = 0).
- **UCS looks back, Greedy looks forward, A\* looks both ways.**
- **Admissible:** `0 ≤ h(n) ≤ h*(n)` — never overestimates. Check **per node**.
- **Consistent:** `h(n) ≤ c(n,a,n') + h(n')` — triangle inequality. Check **per arc**.
- **Consistent ⇒ admissible. Admissible ⇏ consistent.**
- Consistent ⇒ `f` never decreases along a path ⇒ **no node reopening**.
- **Dominance:** `h2 ≥ h1`, both admissible ⇒ h2 better. Combine with **max**.
- 8-puzzle: **h1 = misplaced tiles** (teleport relaxation), **h2 = Manhattan**
  (pass-through relaxation). **Never count the blank.** `h2` dominates `h1`.
- **`N + 1 = 1 + b* + (b*)² + … + (b*)^d`** — `b*` near 1 is a good heuristic.
- Relaxed problem cost is a **lower bound** ⇒ automatically admissible.
- Design methods: **relaxed problems, pattern databases, landmarks, learning from experience**.
- Memory-bounded: **IDA\*** (f-cost limit), **SMA\*** (drops worst nodes when full).
- Spectrum: **perfect heuristic `O(d)`, zero heuristic `O(b^d)`.**
- Greedy is **neither complete nor optimal**; A* is both, *if* `h` is admissible.
