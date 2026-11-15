# Ch 2 — Problem Formulation & Uninformed Search
**Slides: CS#2 (end) and CS#3** (pre-midsem deck, pages 13–23)

> Open `explainers/ch02-uninformed-search.html` first — you can step through
> BFS, DFS, UCS, DLS and IDS one node at a time and watch the frontier change.

This chapter is where the **numericals start**. Four things get asked:
1. Formulate a problem in the **5 components**.
2. **Count** the states in a state space.
3. Give the **traversal order** / frontier trace for a named algorithm.
4. Fill in the **complexity table** (b, d, m).

---

## 1. The problem-solving agent — three phases

```
1. FORMULATE  - define the problem and its components
2. SEARCH     - solve it with a search algorithm
3. EXECUTE    - carry out the fixed sequence of actions
```

Note the shape of that: the agent thinks **completely** first, then acts
**blindly**. It does not re-plan mid-execution. That only works because of four
assumptions.

### The four assumptions that make this work

| Assumption | Meaning | If it broke... |
|---|---|---|
| **Observable** | Agent always knows the current state | it wouldn't know where it is |
| **Discrete** | At any state, only **finitely many** actions | it couldn't enumerate successors |
| **Known** | It knows which state each action reaches | it couldn't build the tree |
| **Deterministic** | Each action always gives the same resulting state | one plan wouldn't be enough |

> Under these four assumptions, **the solution is a fixed sequence of actions**.
> That sentence is the entire justification for this chapter, and it is worth a
> mark on its own.

**Search** = the process of looking for that fixed sequence.
**Search algorithm** = takes a problem as input, outputs a sequence of actions.

---

## 2. The 5 components of a problem  ← *guaranteed exam question*

| # | Component | Notation | Romania example |
|---|---|---|---|
| 1 | **Initial state** | — | `In(Arad)` |
| 2 | **Possible actions** (operators) | `ACTIONS(s)` | `ACTIONS(In(Arad)) = {Go(Sibiu), Go(Timisoara), Go(Zerind)}` |
| 3 | **Transition model** (successor function) | `RESULT(s, a)` | `RESULT(In(Arad), Go(Sibiu)) = In(Sibiu)` |
| 4 | **Goal test** | `IsGoal(s)` | `IsGoal(In(Bucharest)) = Yes` |
| 5 | **Path cost** | `g(n)` | `cost(In(Arad), Go(Sibiu)) = 140 km` |

```
Solution = Path Cost Function + Optimal Solution
```

### Abstraction — why the model is allowed to be a lie

In `In(Arad)` the agent could really be near the airport, in a hotel, at a
shopping centre. It could take a detour, halt, turn the radio on. **All of that
is irrelevant to finding a path to Bucharest**, so it is **abstracted away**.

> Good abstraction = removing detail that cannot change the solution. A one-line
> answer if asked "why abstract?": *the state space would otherwise be infinite
> and every extra detail multiplies it.*

---

## 3. State, state space, node — three things that get confused

- **State** — all information about the environment needed to make a decision.
- **State space** — the set of **all states reachable from the initial state**.
  It forms a **graph**: nodes = states, arcs = actions. A **path** is a sequence
  of states connected by actions.
- **Node** — a **bookkeeping data structure** in the search tree.

| | Node | State |
|---|---|---|
| What it is | data structure for the search **tree** | configuration of the **world** |
| Fields | `STATE`, `PARENT`, `ACTION`, `PATH-COST g(n)` | just the configuration |
| Uniqueness | **Two different nodes can hold the same state** — reached by two different paths | one configuration = one state |

> That last row is the exam point. Nodes ≠ states. If a state is reachable by
> three routes, you get three nodes carrying it.

### The frontier
The set of generated-but-not-yet-expanded nodes. **The queue discipline IS the
algorithm:**

| Queue | Pops | Gives you |
|---|---|---|
| **FIFO** (First In First Out) | oldest element | **BFS** |
| **LIFO** (Last In First Out) — a stack | newest element | **DFS** |
| **Priority queue** | highest priority (lowest `g(n)`) | **UCS** |

Memorise that table. It converts "which algorithm?" into "which queue?" and back.

---

## 4. Numerical Pattern A — counting the state space

### Formula box

```
Vacuum world, n locations:      n x 2^n  states
    (n positions for the agent) x (each location dirty or clean)
    n = 2  ->  2 x 2^2 = 8 states

8-puzzle:                       9! / 2   = 181,440 states
15-puzzle:                      16! / 2  = 10,461,394,944,000  (~1.3 x 10^13)

  Why "/ 2": exactly HALF of all permutations are reachable.
  The other half is a separate, disconnected parity class.
```

### WORKED — Vacuum world (slide's own example)

> "There are two locations and two possibilities of dirt. Hence there would be a
> total of **8** possible states, i.e. `2 x 2²`."

Read the formula out loud: **2** places the agent could be, times **2²** because
each of the 2 squares is independently dirty-or-clean.

Full formulation:

| Component | Vacuum world |
|---|---|
| Initial state | Any state — agent position + dirt configuration |
| Actions | `Left`, `Right`, `Suck` |
| Transition model | `Left` moves left, **except in the leftmost location where it has no effect**; same for `Right`. `Suck` removes dirt if any |
| Goal test | Are **all** locations clean? |
| Path cost | Each step costs 1, so path cost = **total number of steps** |

### WORKED — 8-puzzle

| Component | 8-puzzle |
|---|---|
| Initial state | Any permutation of 1–8 plus a blank |
| Actions | Move the **blank** Left, Right, Up or Down |
| Transition model | The blank swaps with the digit it moves into |
| Goal test | Does the state match the goal configuration? |
| Path cost | Each step costs 1 |

States = `9!/2 = 362880/2 = 181,440`

> **Two traps here.** (1) The actions are defined on the **blank**, not on the
> tiles — that keeps the branching factor at ≤ 4 instead of 8. (2) Do not forget
> the `/2`. Half of all configurations are unreachable from any given start.

---

## 5. How search strategies are judged — five dimensions

| Dimension | The question |
|---|---|
| **Completeness** | Does it always find a solution if one exists? |
| **Time complexity** | Number of nodes **generated** |
| **Space complexity** | Maximum number of nodes **in memory** |
| **Optimality** | Does it always find a **least-cost** solution? |
| **Systematicity** | Does it visit each search node **at most once**? |

### The three parameters — memorise these letters

```
b = maximum BRANCHING FACTOR of the search tree
d = DEPTH of the least-cost / shallowest goal  (number of steps from the start)
m = MAXIMUM DEPTH of the state space  (may be infinite)
```

> `d` is where the goal is; `m` is how deep the tree goes. `d ≤ m` always.
> Getting these two the wrong way round is the classic way to fail the
> complexity table.

---

## 6. The six uninformed algorithms

Uninformed ("blind") = **no information beyond the problem definition**. It can
generate successors and tell a goal from a non-goal. That is all.

| # | Algorithm | Queue | Idea in one line |
|---|---|---|---|
| 1 | **BFS** | FIFO | Generate all nodes at a depth before going deeper |
| 2 | **UCS** | Priority on `g(n)` | Expand the **cheapest path so far** |
| 3 | **DFS** | LIFO (stack) | Go as deep as possible, then back up |
| 4 | **DLS** | LIFO + depth cap `l` | DFS that refuses to go past depth `l` |
| 5 | **IDS** | LIFO, repeated | DLS with `l = 0, 1, 2, 3 …` until found |
| 6 | **Bidirectional** | two frontiers | Search from start AND goal, meet in the middle |

DFS is described in the slides as **"aggressive"** — it examines complete paths.

**Applications (a one-mark question):**
- BFS — finding a path in a graph (many solutions), finding **bipartitions**.
- DFS — finding **connectedness** in a graph, **topological sorting**.

---

## 7. THE COMPLEXITY TABLE — learn this cold

|  | BFS | UCS | DFS | DLS | IDS | Bidirectional |
|---|---|---|---|---|---|---|
| **Complete?** | Yes¹ | Yes² | **No** | **No** (if `l < d`) | Yes¹ | Yes¹ |
| **Time** | O(b^d) | O(b^(1+⌊C*/ε⌋)) | O(b^m) | O(b^l) | O(b^d) | O(b^(d/2)) |
| **Space** | O(b^d) | O(b^(1+⌊C*/ε⌋)) | **O(bm)** | **O(bl)** | **O(bd)** | O(b^(d/2)) |
| **Optimal?** | Yes³ | **Yes** | No | No | Yes³ | Yes³ |

¹ if `b` is finite  ² if every step cost ≥ ε > 0  ³ if all step costs are identical
`C*` = cost of the optimal solution.

### The only three facts you need to reconstruct that whole table

1. **BFS and IDS have the same TIME** — `O(b^d)`. But **IDS space is `O(bd)`,
   linear**, while BFS space is `O(b^d)`, exponential. That is the entire reason
   IDS exists.
2. **DFS space is `O(bm)`, linear** — its one virtue. It pays with
   incompleteness (an infinite branch traps it forever) and non-optimality.
3. **UCS is optimal for any step costs**; BFS/IDS are only optimal when every
   step costs the same.

### Why IDS repeating work doesn't matter (slide derivation)

```
Nodes generated = (d+1)b^0 + d.b^1 + (d-1)b^2 + ... + 1.b^d
                = O(b^d)
```
The **root is regenerated d+1 times**, but the **deepest level only once** — and
the deepest level is almost the whole tree. With `b = 10, d = 5`, IDS generates
about 123,456 nodes vs BFS's 111,111: roughly **11% overhead** for an exponential
saving in memory.

> Optimal? "**Yes, if step cost = 1.**" Can be modified for a uniform-cost tree —
> that variant is called **iterative lengthening**.

---

## 8. Numerical Pattern B — traversal order

Use this tree. **Left-to-right** expansion order, `A` is the root, `I` is the goal.

```
              A
          /   |   \
         B    C    D
        / \   |   / \
       E   F  G  H   I
```

### BFS — FIFO
Take from the front, add to the back.

| Step | Pop | Frontier after |
|---|---|---|
| 0 | — | `A` |
| 1 | A | `B C D` |
| 2 | B | `C D E F` |
| 3 | C | `D E F G` |
| 4 | D | `E F G H I` |
| 5 | E | `F G H I` |
| 6 | F | `G H I` |
| 7 | G | `H I` |
| 8 | H | `I` |
| 9 | I | **goal** |

**Order: `A B C D E F G H I`** — level by level.
Max frontier size = **5**.

### DFS — LIFO
Take from the front, add to the **front** (push children so leftmost pops first).

| Step | Pop | Frontier after |
|---|---|---|
| 0 | — | `A` |
| 1 | A | `B C D` |
| 2 | B | `E F C D` |
| 3 | E | `F C D` |
| 4 | F | `C D` |
| 5 | C | `G D` |
| 6 | G | `D` |
| 7 | D | `H I` |
| 8 | H | `I` |
| 9 | I | **goal** |

**Order: `A B E F C G D H I`** — dive first.
Max frontier size = **4**. Notice it never exceeds `b × depth`.

### DLS with limit `l = 1`
Only expands to depth 1. **Order: `A B C D`.** Then it **fails** — the goal `I`
is at depth 2, and `l < d`. This is the concrete demonstration that
**DLS is incomplete when `l < d`.**

### IDS
Run DLS with `l = 0`, then `1`, then `2`:

```
l = 0 :  A                                   (1 node,  fail)
l = 1 :  A B C D                             (4 nodes, fail)
l = 2 :  A B E F C G D H I                   (9 nodes, GOAL found)
                                             ------
                          total generated  =  14
```
BFS on the same tree generates 9. IDS generates 14 — **5 extra nodes** — but its
peak memory was 4 instead of 5, and on a deep tree that gap becomes exponential.

---

## 9. Numerical Pattern C — Uniform Cost Search trace

**UCS in one line:** instead of expanding the shallowest node, expand the node
`n` with the **lowest path cost `g(n)`**. The frontier is a priority queue
ordered by `g(n)`.

### Two rules people get wrong

> **1. The goal test is applied when a node is EXPANDED, not when it is
> GENERATED.** Because a goal node that has just been generated **may not be on
> the optimal path** — a cheaper route to it might still be sitting in the
> frontier.
>
> **2. If you generate a node already on the frontier with a cheaper `g`,
> REPLACE it.** Do not add a duplicate.

### WORKED — the slide's Romania trace (Sibiu → Bucharest)

| Step | Expand | Generates | Frontier after |
|---|---|---|---|
| 1 | Sibiu | RimnicuVilcea 80, Fagaras 99 | `(RV, 80) (Fagaras, 99)` |
| 2 | **RV (80)** — cheapest | Pitesti 177 | `(Fagaras, 99) (Pitesti, 177)` |
| 3 | **Fagaras (99)** | **Bucharest 310** | `(Pitesti, 177) (Bucharest, 310)` |
| 4 | **Pitesti (177)** | **Bucharest 278** → *replace* | `(Bucharest, 278)` |
| 5 | **Bucharest (278)** | — goal test passes | **return solution** |

**Answer: `Sibiu → RimnicuVilcea → Pitesti → Bucharest`, cost 278.**

This trace is the whole reason for rule 1. At **step 3** Bucharest was generated
at cost **310**. If UCS had goal-tested on generation, it would have returned 310
and been **wrong** — the 278 route was still to come.

### WORKED — a second UCS problem (do this one with me)

```
        S
    1 /   \ 4
     A ---- B          edges:  S-A = 1    S-B = 4
     |  2   |                  A-B = 2    A-C = 5
   5 |      | 8                B-C = 2    B-G = 8
     C ---- G                  C-G = 3
        3
```
Start `S`, goal `G`.

| Step | Expand (cost) | Generated | Frontier after |
|---|---|---|---|
| 1 | S (0) | A=1, B=4 | `(A,1) (B,4)` |
| 2 | A (1) | B = 1+2 = **3** → replaces B=4; C = 1+5 = 6 | `(B,3) (C,6)` |
| 3 | B (3) | C = 3+2 = **5** → replaces C=6; G = 3+8 = 11 | `(C,5) (G,11)` |
| 4 | C (5) | G = 5+3 = **8** → replaces G=11 | `(G,8)` |
| 5 | G (8) | goal test on expansion → **pass** | done |

**Answer: `S → A → B → C → G`, total cost 8.**

Sanity-check the alternatives: `S→B→G = 4+8 = 12`. `S→A→C→G = 1+5+3 = 9`.
`S→A→B→G = 1+2+8 = 11`. Our 8 is the cheapest. ✓

> **Exam habit:** after you finish a UCS trace, list 2–3 alternative paths and
> their costs to show the answer really is minimal. It catches your own errors
> and reads as confidence.

---

## 10. Uninformed vs Informed — the comparison table

Asked as a straight 5-mark compare-and-contrast.

| Parameter | Uninformed | Informed |
|---|---|---|
| Using knowledge | Does **not** use knowledge while searching | **Uses** knowledge while searching |
| Speed | Much slower | Quicker |
| Completion | **Always** complete | Can be complete **or incomplete** |
| Time consumed | More | Much less |
| Cost incurred | Higher | Lower |
| Suggestion/direction | Gets **no** hint about where the solution is | Gets a hint on how and where to find it |
| Efficiency | Less efficient | More efficient |
| Implementation length | Lengthier | Shorter |
| Examples | BFS, DFS, UCS, DLS, IDS, Bidirectional | Best-First, A*, AO* |

The slide's summary of the whole chapter: **"All these methods are slow (blind).
Solution → add guidance (a heuristic estimate) → informed search."** That is the
bridge into Chapter 3.

---

## 11. You try

**Q1 (state counting).** A vacuum world has **3** locations in a row. How many
states? Show the formula, not just the number.

**Q2 (state counting).** How many states does the **15-puzzle** have? Leave it as
a factorial expression and then give the order of magnitude.

**Q3 (formulation).** Formulate **solving a maze** using all 5 components.
*(From Exercise 1 on the slides.)*

**Q4 (traversal).** For the tree in §8, give the visit order for
**DLS with `l = 2`**, and state how many nodes it generates.

**Q5 (traversal).** Same tree, but now the goal is **`G`** instead of `I`.
Give the order for BFS and for DFS, and say which finds it in fewer expansions.

**Q6 (UCS).** Run UCS on this graph from `S` to `G`. Show the frontier at every
step, then verify by listing all complete paths and their costs.

```
   S -> A = 2      A -> C = 3
   S -> B = 5      B -> C = 1
   S -> C = 8      C -> G = 4
                   B -> G = 7
```

**Q7 (complexity).** Fill in from memory, no peeking:

| | BFS | DFS | IDS | UCS |
|---|---|---|---|---|
| Complete? | | | | |
| Time | | | | |
| Space | | | | |
| Optimal? | | | | |

**Q8 (concept).** In the Romania UCS trace, Bucharest was generated at cost 310
at step 3 but the answer was 278. Explain in two sentences **why UCS goal-tests
on expansion rather than on generation**.

---

## 12. Answers

<details>
<summary>Open only after attempting</summary>

**Q1.** `n × 2ⁿ` with `n = 3` → `3 × 2³ = 3 × 8 = ` **24 states**.
(3 possible agent positions × 8 dirt configurations.)

**Q2.** `16!/2 = 20,922,789,888,000 / 2 = 10,461,394,944,000`
≈ **1.05 × 10¹³ states**. The `16!` is because there are 16 tiles including the
blank; the `/2` is the unreachable parity half.

**Q3 — Maze**

| Component | Maze |
|---|---|
| Initial state | The agent's starting cell, e.g. `At(1,1)` |
| Actions | `Up`, `Down`, `Left`, `Right` |
| Transition model | `RESULT(At(x,y), Up) = At(x, y+1)` **if no wall between them**, else no change |
| Goal test | `Is the current cell the exit cell?` |
| Path cost | 1 per move → path cost = number of moves |

The component people miss is the **wall condition inside the transition model**.
Without it the model is wrong, because walls are what make a maze a maze.

**Q4 — DLS with `l = 2`.**
Depth 2 is exactly where the leaves are, so it behaves like a full DFS:
**`A B E F C G D H I`**, **9 nodes** generated. It succeeds because `l = d`.

**Q5 — goal is `G`** (depth 2, middle branch).
- **BFS:** `A B C D E F G` → found on the **7th** expansion.
- **DFS:** `A B E F C G` → found on the **6th** expansion.

**DFS wins here** — it dives into B's subtree, exhausts it, then hits C and G
immediately. BFS had to clear the whole of level 1 and then E and F first.
This is the honest lesson: DFS is not worse, it is *differently* risky. It wins
when the goal is deep-ish and on an early branch; it loses catastrophically when
the tree has an infinite branch on the left.

**Q6 — UCS trace**

| Step | Expand (cost) | Generated | Frontier after |
|---|---|---|---|
| 1 | S (0) | A=2, B=5, C=8 | `(A,2) (B,5) (C,8)` |
| 2 | A (2) | C = 2+3 = **5** → replaces C=8 | `(B,5) (C,5)` |
| 3 | B (5) | C = 5+1 = 6 → **worse than 5, discard**; G = 5+7 = 12 | `(C,5) (G,12)` |
| 4 | C (5) | G = 5+4 = **9** → replaces G=12 | `(G,9)` |
| 5 | G (9) | goal test passes | done |

**Answer: `S → A → C → G`, cost 9.**

Verification, all complete paths:
- `S→A→C→G = 2+3+4 = 9` ← **cheapest**
- `S→B→C→G = 5+1+4 = 10`
- `S→B→G   = 5+7    = 12`
- `S→C→G   = 8+4    = 12`

At step 3, note that B offered C at cost 6 but C was already on the frontier at
5 — you **keep the cheaper one and discard**, you do not add a second entry.
Ties at step 2/3 (both B and C sit at 5) can be broken either way; the final
answer is unaffected.

**Q7 — Complexity table**

| | BFS | DFS | IDS | UCS |
|---|---|---|---|---|
| Complete? | Yes (if b finite) | **No** | Yes | Yes (if step cost ≥ ε) |
| Time | O(b^d) | O(b^m) | O(b^d) | O(b^(1+⌊C*/ε⌋)) |
| Space | O(b^d) | **O(bm)** | **O(bd)** | O(b^(1+⌊C*/ε⌋)) |
| Optimal? | Yes (if step costs equal) | No | Yes (if step costs equal) | **Yes** |

**Q8.** A node is generated as soon as it is *reached by any path*, but the first
path that reaches it is not necessarily the cheapest — a cheaper route to the
same state can still be sitting unexpanded in the frontier. UCS therefore waits
until a node comes off the priority queue for **expansion**, at which point its
`g` value is guaranteed minimal, and only then applies the goal test.

</details>

---

## 13. Two-minute recall card

- Phases: **Formulate → Search → Execute**. Assumptions: observable, discrete, known, deterministic → solution is a **fixed action sequence**.
- 5 components: **Initial state, Actions, Transition model, Goal test, Path cost `g(n)`**.
- Node fields: `STATE, PARENT, ACTION, PATH-COST`. **Two nodes can share one state.**
- Queue = algorithm: **FIFO → BFS**, **LIFO → DFS**, **priority on g(n) → UCS**.
- `b` branching, `d` depth of shallowest goal, `m` max depth of the space. `d ≤ m`.
- Vacuum world `n × 2ⁿ`; 8-puzzle `9!/2 = 181,440`; 15-puzzle `16!/2`.
- BFS `O(b^d)` time **and space**. IDS `O(b^d)` time but **`O(bd)` space** — that's the point of IDS.
- DFS space `O(bm)` linear, but **not complete, not optimal**.
- **UCS is optimal for any step costs**; BFS/IDS only when step costs are equal.
- UCS: **goal test on expansion, not generation**; replace a frontier node if you find it cheaper.
- IDS node count: `(d+1)b⁰ + d·b¹ + … + b^d = O(b^d)`.
- Dimensions: completeness, time, space, optimality, **systematicity**.
