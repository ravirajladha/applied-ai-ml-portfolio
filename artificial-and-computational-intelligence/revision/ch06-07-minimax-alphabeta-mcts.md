# Ch 6 & 7 — Adversarial Search: Minimax, Alpha-Beta Pruning & MCTS
**Slides: CS#7 and CS#8** (pre-midsem deck, pages 67–82)

> **This is Q1 on the real paper — 9 marks, the largest single question.**
> The Apr 2025 Connect-Three question is worked in full in §8, against its own
> marking scheme.
>
> Open `explainers/ch06-07-minimax-alphabeta.html` first if you want to watch the
> pruning happen.

### The learning objectives, straight off the slide — this is the exam spec
```
1. Convert a given problem into an adversarial search problem
2. Formulate the problem-solving agent components
3. DESIGN a static evaluation function value for a problem
4. Construct a game tree
5. Apply Min-Max
6. Apply and LIST nodes pruned by alpha pruning and nodes pruned by beta pruning
```

---

## 1. What adversarial search is

> **Adversarial search** is search in a setting where **two or more agents have
> conflicting goals**. One player's gain is another's loss.

In ordinary search the agent asks *"what action gets me closer to my goal?"*
In adversarial search it must **also** ask *"what will my opponent do to reduce
my chance of success?"*

| Aspect | Normal search | Adversarial search |
|---|---|---|
| Number of agents | usually one | **at least two** |
| Goal | reach a goal state | **win / maximise utility** |
| Environment | **passive** | **strategic and competitive** |
| Next state depends on | our action | **our action AND the opponent's** |
| Example | route finding | chess |

**Characteristics of games:** observability · stochasticity · time granularity ·
number of players.

---

## 2. Formal definition of a game — six components

```
1. INITIAL STATE   S0            the starting board
2. PLAYER(s)                     whose turn it is
3. ACTIONS(s)                    the legal moves from state s
4. RESULT(s, a)                  the new state after a move
5. TERMINAL-TEST(s)              is the game over?
6. UTILITY(s, p)                 the final value of the outcome
```

Typical utilities: **Win = +1 · Draw = 0 · Loss = −1**.

### Two-player zero-sum
- Two players; **one player's gain is the other's loss**; exactly opposite goals.
- **MAX** — trying to **maximise** the score.
- **MIN** — the opponent, trying to **minimise** MAX's score.
- If MAX gets +1, MIN effectively gets −1.

Examples: tic-tac-toe, chess, checkers.

---

## 3. Minimax

> The minimax algorithm chooses the move that gives the **best guaranteed
> outcome, assuming the opponent also plays optimally.**

```
At MAX nodes -> choose the LARGEST value
At MIN nodes -> choose the SMALLEST value
Values are BACKED UP from the leaves to the root
```

> **The sentence that captures it:** *MAX does not choose the branch with the
> best possible outcome. **MAX chooses the branch whose worst-case outcome is
> best.*** The principle is "minimise the maximum possible loss."

### ⚠ The mistake the slides call out by name

Given this tree (MAX at root, MIN below, leaves `+3, +5` and `−2, +4`):

```
          MAX
        /     \
     MIN       MIN
    /   \     /   \
  +3    +5  -2    +4
```

> *"A common mistake students do is to say: MAX should choose the branch that
> contains +5. But MAX cannot directly choose +5. **After MAX chooses a branch,
> MIN gets a turn!** So if MAX chooses the left branch, MIN will choose +3, not
> +5."*

```
Left  MIN : min(+3, +5) = +3
Right MIN : min(-2, +4) = -2
Root  MAX : max(+3, -2) = +3
```
**Best move: left branch. Backed-up minimax value: +3.**

---

## 4. Why we cannot search the whole tree

For tic-tac-toe, full search works. For chess the tree is enormous. So we use:
1. a **depth limit**, and
2. a **static evaluation function**.

> A **static evaluation function** estimates the utility of a **non-terminal**
> state. It is called *static* because it evaluates the board **as it is,
> without searching further**.

A good one should: give **higher** values to states good for MAX · **lower**
values to states good for MIN · be **fast to compute** · **correlate** with the
actual chance of winning.

---

## 5. The static evaluation functions — all four, from the formula sheet

```
CS-7
  Evaluation = Material advantage + King safety + Mobility + Board control
  Score      = MAX pieces − MIN pieces
  Evaluation = 2×Soldier Advantage + 3×Gate Damage + 2×MAX Safety + 4×Supply Control

CS-8
  Utility value = 3(MAX's win chance − MIN's win chance)
                + 2(MAX's adjacent pairs − MIN's adjacent pairs)
```

**Chess example:**

| Feature | Meaning | Score |
|---|---|---|
| Material advantage | Does White have more pieces? | +5 |
| King safety | Is White's king safe? | +2 |
| Mobility | Many useful moves available? | +1 |
| Board control | Does White control the centre? | +2 |
| | **Evaluation** | **+10** |

**Simple version:** `Score = MAX pieces − MIN pieces`. MAX has 8, MIN has 5 →
`8 − 5 = +3`. Positive = good for MAX, negative = good for MIN, zero = balanced.

> **The exam always GIVES you the evaluation function.** Your job is to apply it
> correctly, not invent it. Read it character by character — the coefficients and
> the minus sign are where marks are lost.

---

## 6. Alpha-Beta Pruning

> Alpha-beta is **minimax plus a heuristic**. It stops evaluating a move once it
> is sure the move is **worse than a previously examined move** — such moves need
> not be evaluated further.
>
> **It gives the SAME output as minimax**, but cuts off branches that cannot
> possibly affect the final decision.

```
ALPHA (α) : best already-explored option for MAX     -- a LOWER bound
BETA  (β) : best already-explored option for MIN     -- an UPPER bound

Initially   α = −∞ ,  β = +∞      (worst possible for both players)
```

> **General principle (quote this):** *at a node `n`, if a player has a better
> option at the parent of `n` or further up, then `n` will never be reached —
> hence the entire subtree from `n` can be pruned.*

### The algorithm — the slides' own three steps

```
1. At the root, initialise alpha = −∞ and beta = +∞
2. Navigate to the specified depth and get the static evaluated value
3. For every value VAL analysed, loop until all leaf/terminal nodes are
   analysed OR until beta <= alpha:

   If the player is MAX:
       if VAL > alpha  ->  reset alpha = VAL
       then check if beta <= alpha -> tag the path unpromising, PRUNE the branch;
       the remaining siblings are not considered

   Else if the player is MIN:
       if VAL < beta   ->  reset beta = VAL
       then check if beta <= alpha -> tag the path unpromising, PRUNE the branch;
       the remaining siblings are not considered
```

### Formula box (CS-8, official sheet)
```
1.  α = −∞ ,  β = +∞                    initial values
2.  If VAL ≥ α, then α = VAL             ALPHA update (at MAX nodes)
3.  If VAL < β, then β = VAL             BETA update  (at MIN nodes)
4.  PRUNE WHEN  β ≤ α                    the pruning condition
```

> **Memorise the pruning condition as `β ≤ α`.** Everything else follows.
> α only ever **increases**, β only ever **decreases**. When they cross, the
> window is empty and there is nothing left worth finding.

### WORKED — the slides' own alpha-beta example

Tree: root **MAX** → 2 **MIN** nodes → 4 **MAX** nodes → 8 leaves
`6, 5, 8, 10, 2, 1, 9, 12`

**First, plain minimax for comparison:**
```
level-2 MAX : max(6,5)=6   max(8,10)=10   max(2,1)=2   max(9,12)=12
level-1 MIN : min(6,10)=6                 min(2,12)=2
root    MAX : max(6, 2) = 6
```

**Now with alpha-beta:**

| Step | Node | Action | α | β |
|---|---|---|---|---|
| 1 | leaf 6 | first MAX node takes 6 | α=6 | |
| 2 | leaf 5 | 5 < 6, no change | α=6 | |
| 3 | MIN (left) | receives 6 | | **β=6** |
| 4 | leaf 8 | second MAX node: 8 > α | **α=8** | β=6 |
| 5 | **PRUNE** | `β=6 ≤ α=8` → **cut leaf 10** | | |
| 6 | MIN (left) | returns `min(6, 8) = 6` | | |
| 7 | root | receives 6 | **α=6** | |
| 8 | leaf 2, leaf 1 | third MAX node → 2 | | |
| 9 | MIN (right) | receives 2 | | **β=2** |
| 10 | **PRUNE** | `β=2 ≤ α=6` → **cut the whole fourth subtree (leaves 9, 12)** | | |

```
Root value = 6                   -- identical to plain minimax ✓
Leaves examined : 6, 5, 8, 2, 1   (5 of 8)
Leaves PRUNED   : 10, 9, 12       (3 of 8)
```

> **Answering "list the nodes pruned"** — the learning objective asks for
> exactly this. Say **which** nodes and **why**: *"leaf 10 was pruned by
> **beta pruning** at the left MIN node since β=6 ≤ α=8; the fourth subtree
> (leaves 9, 12) was pruned at the right MIN node since β=2 ≤ α=6."*

### Move ordering — computational efficiency

Alpha-beta's saving depends entirely on the **order** the moves are examined.

| Ordering | Nodes examined |
|---|---|
| Worst case (bad ordering) | `O(b^d)` — no better than minimax |
| **Perfect ordering** | **`O(b^(d/2))`** — effectively **doubles the searchable depth** |

> **The rule:** at MAX nodes examine the **best** moves first; at MIN nodes
> examine the **worst** (for MAX) first. Finding a good value early raises α (or
> lowers β) sooner, so more of the rest gets cut.

---

## 7. Monte Carlo Tree Search

> **MCTS** is a heuristic search algorithm for decision processes, most notably
> in board-game software. It is a **probabilistic** search combining classic tree
> search with **reinforcement-learning** principles.

**Why not just use simulations inside alpha-beta?** The slides give the numbers:
- A single simulation is **very noisy** — only a 0/1 signal.
- Running many simulations per evaluation is **very slow**. Chess programs do
  ~1 million evals/second; in Go, at 400 moves/simulation and 100
  simulations/eval, you get **25 evals/second**.
- **Result: Monte Carlo was ignored for over 10 years in Go.**

**The fix:** use the results of simulations to **guide the growth of the tree**,
balancing:
- **Exploitation** — focus on promising moves
- **Exploration** — focus on moves where uncertainty is high

### The four phases — *guaranteed exam question, name all four in order*

| # | Phase | What happens |
|---|---|---|
| 1 | **Selection** | Start at the root and repeatedly choose the most promising child, balancing exploitation (high win rate) against exploration (tried fewer times) |
| 2 | **Expansion** | On reaching a node where not all moves have been explored, **add a new child node** for one unexplored legal move |
| 3 | **Simulation** (rollout) | From the new node, **play the game to the end** with random / simple-rule / lightweight-heuristic moves. The point is not to play well but to estimate win/loss/draw |
| 4 | **Backpropagation** | Send the result back through **every node visited** in that iteration, updating **visit count**, **win score**, and **average value / win rate** |

### UCB — the selection formula (CS-8, official sheet)

```
                    ┌─────────┐
                    │  ln(N)  │
   UCB = v_i + C · √│ ─────── │
                    │   n_i   │
                    └─────────┘

   v_i = average value / win rate of node i     <- EXPLOITATION
   n_i = number of visits to node i
   N   = number of visits to the parent
   C   = exploration constant
```

> **Read it as two halves.** `v_i` rewards nodes that have **done well**.
> The square-root term rewards nodes that have been **tried rarely** — as `n_i`
> grows the bonus shrinks, and as the parent is visited more (`ln N` grows) every
> untried child becomes more attractive.
>
> Because the bonus → ∞ as `n_i` → 0, **MCTS always tries every option at least
> once.**

**MCTS applies to combinatorial games** — sequential games with **perfect
information**. Preconditions: two players · players alternate turns · a **finite
set of well-defined moves**. Examples: chess, checkers, Go, tic-tac-toe.

---

## 8. ⭐ PAST PAPER — Apr 2025, Q1 (9 marks) fully worked

> *"Consider the **Connect Three** game on a **3×4 board**. Player1 has 12 Blue
> checkers, Player2 has 12 Green. The objective is to align three of your
> checkers horizontally, vertically or diagonally. On your turn, place one
> checker into an open slot at the top; **it falls to the lowest unoccupied space
> in that column**. Blue moves first."*
>
> **(a)** Construct the game tree from the current state (level 0) up to **exactly
> 2 levels** — one round for each player. **[3]**
> **(b)** Calculate the utility of the leaves with the static evaluation
> function **[3]**
> ```
> Board value = 5 × (MAX player chance of Win) − 2 × (MIN player chance of Win)
> Player Chance of Win = No. of Matches possible if this player alone is
>                        allowed to fill all the empty cells with its checkers
> ```
> **(c)** Apply Min-Max and **highlight the best path**. **[3]**

### Marking scheme (from the paper)
```
a. Search tree, level 1 expansion        1 mark
   Search tree, level 2 expansion        2 marks
b. Calculating static evaluation values  3 marks   <- the biggest single chunk
c. Min-max on the game tree              2 marks
   Best path chosen                      1 mark
```

### How to read the evaluation function — *this is the whole question*

> **"Player Chance of Win = number of matches possible if this player alone is
> allowed to fill all the empty cells with its checkers."**

Decoded into a procedure:

```
To find MAX's chance of win:
  1. Pretend EVERY empty cell is filled with MAX's colour.
  2. Count how many three-in-a-row LINES (horizontal, vertical, diagonal)
     are then all-MAX.
  3. Equivalently and faster:  count the lines that contain NO MIN checker.

Do the same for MIN, counting lines that contain no MAX checker.
```

> **The shortcut is the key insight.** A line is winnable by MAX **if and only if
> it contains no MIN checker** — because MAX gets to fill everything else. So you
> never actually fill the board; you just **scan every line and ask "is the
> opponent in it?"**
>
> Count **lines, not cells**. On a 3×4 board that means every horizontal triple,
> every vertical triple, and every diagonal triple.

### (a) The tree

Column 0 is full, so there are **3 legal moves** (columns 1, 2, 3) → **S1, S2, S3**
at level 1. At level 2, S1 and S3 each have 3 children, but **S2 has only 2** —
because the move leading to S2 filled a column, cutting the legal moves to 2.

```
                          S0  (MAX)
              ┌────────────┼────────────┐
            S1            S2            S3      (MIN)
          ┌──┼──┐        ┌─┴─┐       ┌──┼──┐
        S4  S5  S6     S7   S8     S9  S10 S11  (MAX / leaves)
```

> **Notice the uneven branching.** Do not assume every node has the same number
> of children — in Connect-N a column disappears the moment it fills. The
> examiner is checking whether you actually tracked the board.

### (b) Static evaluation of the 8 leaves

| Leaf | MAX chance | MIN chance | `5×MAX − 2×MIN` | Value |
|---|---|---|---|---|
| S4 | 0 | 4 | `5(0) − 2(4)` | **−8** |
| S5 | 0 | 4 | `5(0) − 2(4)` | **−8** |
| S6 | 2 | 4 | `5(2) − 2(4)` | **+2** |
| S7 | 1 | 5 | `5(1) − 2(5)` | **−5** |
| S8 | 2 | 5 | `5(2) − 2(5)` | **0** |
| S9 | 0 | 5 | `5(0) − 2(5)` | **−10** |
| S10 | 0 | 5 | `5(0) − 2(5)` | **−10** |
| S11 | 1 | 5 | `5(1) − 2(5)` | **−5** |

*(These are the official values from the answer key. **Always write the
substituted form `5(0) − 2(4)` before the answer** — the scheme marks the working,
and 3 of the 9 marks live here.)*

### (c) Minimax backup

**Level 1 is MIN** (Blue moved to reach level 1... whichever player is MIN, take
the minimum):
```
S1 = min(S4, S5, S6)    = min(−8, −8, +2)   = −8
S2 = min(S7, S8)        = min(−5,  0)       = −5
S3 = min(S9, S10, S11)  = min(−10, −10, −5) = −10
```

**Root is MAX:**
```
S0 = max(S1, S2, S3) = max(−8, −5, −10) = −5
```

```
BEST PATH:  S0 → S2 → S7        Minimax value = −5
```

> **Sanity check that costs nothing:** the value must equal one of the leaves
> reachable along the chosen path. `−5 = S7` ✓
>
> And note the answer is **negative** — this position is bad for MAX no matter
> what. Minimax does not promise a good outcome, only the **least bad guaranteed**
> one. Say that in one line; it shows you understand what you computed.

---

## 9. Solved-samples deck — the sliding-tile variant

The faculty's sample deck uses the same shape with a different game:

> Three "A" tiles, three "B" tiles and two empty spaces. A player wins by getting
> three of their own tiles **adjacent** (same row or same column). Two legal
> moves: **(1)** a tile may move into an adjacent empty location; **(2)** a tile
> may **hop over one tile** in the same row into the empty position.
> **Expand the tree to exactly 3 levels.** Then apply **Minimax** *and*
> **Alpha-Beta pruning**.
>
> ```
> Utility = 3 × (MAX's win chance − MIN's win chance)
>         + 2 × (MAX's adjacent pairs − MIN's adjacent pairs)
> ```
> *"For the initial configuration, MAX's win chance is 3 because 3 MAX coins (A)
> are adjacent to an empty cell; MIN's win chance is 1 because 1 MIN coin (B) is
> adjacent to an empty cell."*

**Note how differently "win chance" is defined here** — adjacency to an empty
cell, not lines-without-the-opponent. **Read the definition the question gives
you every single time.** Two different papers, two different meanings of the same
phrase.

---

## 10. You try

**Q1 (minimax).** Root is MAX with three MIN children. Leaves left to right:
```
B1: 3, 12, 8        B2: 2, 4, 6        B3: 14, 5, 2
```
Give the value of each MIN node, the root value, and MAX's best move.

**Q2 (alpha-beta).** Run alpha-beta on the same tree, left to right. Show α and β
as they change, state **which leaves are pruned**, and name **whether each cut is
an alpha or a beta prune**.

**Q3 (static evaluation).** A 3×3 Connect-Three board, MAX = `X`, MIN = `O`:
```
        c0   c1   c2
  r0     .    .    .
  r1     .    .    X
  r2     O    X    O
```
Using `Board value = 5×(MAX chance) − 2×(MIN chance)` with the past paper's
definition of "chance of win", compute the board value. **List which lines you
counted** for each player. *(There are 8 lines: 3 rows, 3 columns, 2 diagonals.)*

**Q4 (MCTS / UCB).** A parent node has been visited **N = 100** times. Three
children, with `C = 1.41`:

| child | win rate `v` | visits `n` |
|---|---|---|
| A | 0.60 | 20 |
| B | 0.55 | 5 |
| C | 0.75 | 60 |

Compute the UCB for each and say which MCTS selects. Explain the result in one
sentence.

**Q5 (concept).** In minimax, why can MAX not simply pick the branch containing
the highest leaf value? Answer in two sentences.

**Q6 (concept).** State the alpha-beta pruning condition, and say what α and β
each represent. Why does alpha-beta give **exactly** the same answer as minimax?

**Q7 (concept).** Name the four phases of MCTS in order and give one line each.

**Q8 (concept).** What is the best-case and worst-case node count for alpha-beta,
and what determines which you get?

---

## 11. Answers

<details>
<summary>Open only after attempting</summary>

**Q1 — Minimax**
```
B1 = min(3, 12, 8)  = 3
B2 = min(2, 4, 6)   = 2
B3 = min(14, 5, 2)  = 2

Root (MAX) = max(3, 2, 2) = 3
```
**Best move: B1**, guaranteed value **3**.

**Q2 — Alpha-beta**

| Step | Node | Value seen | α | β | Action |
|---|---|---|---|---|---|
| 1 | B1 leaves 3, 12, 8 | min = 3 | | β: 3 → 3 → 3 | no cut (α is still −∞) |
| 2 | root | B1 returns 3 | **α = 3** | | |
| 3 | B2 leaf 2 | 2 | α = 3 | **β = 2** | **`β=2 ≤ α=3` → PRUNE** |
| | | | | | **leaves 4 and 6 cut** |
| 4 | root | B2 returns 2 | α stays 3 | | |
| 5 | B3 leaf 14 | 14 | α = 3 | β = 14 | no cut |
| 6 | B3 leaf 5 | 5 | α = 3 | β = 5 | no cut |
| 7 | B3 leaf 2 | 2 | α = 3 | β = 2 | `β ≤ α` — but **nothing left to cut** |
| 8 | root | B3 returns 2 | α = 3 | | |

```
Root value = 3                    -- same as minimax ✓
Leaves examined : 7 of 9
Leaves PRUNED   : 4 and 6  (B2's second and third leaves)
```

**Type of cut:** both are **beta cuts** — they happen **at a MIN node** where β
dropped to or below the inherited α. *(An "alpha cut" is the mirror image: it
happens at a MAX node when α rises to or above the inherited β.)*

> Note B3 is **not** pruned even though it also ends at 2 — the cut condition was
> only met on its **last** leaf, so nothing remained to skip. Ordering matters.

**Q3 — Static evaluation**

A line counts for a player **if it contains no opponent checker**.

**MAX (X) — lines with no `O`:**

| Line | Contents | No O? |
|---|---|---|
| Row0 | `. . .` | ✓ |
| Row1 | `. . X` | ✓ |
| Row2 | `O X O` | ✗ |
| Col0 | `. . O` | ✗ |
| Col1 | `. . X` | ✓ |
| Col2 | `. X O` | ✗ |
| Diag `(0,0)(1,1)(2,2)` | `. . O` | ✗ |
| Anti-diag `(0,2)(1,1)(2,0)` | `. . O` | ✗ |

**MAX chance = 3** (Row0, Row1, Col1)

**MIN (O) — lines with no `X`:**

| Line | Contents | No X? |
|---|---|---|
| Row0 | `. . .` | ✓ |
| Row1 | `. . X` | ✗ |
| Row2 | `O X O` | ✗ |
| Col0 | `. . O` | ✓ |
| Col1 | `. . X` | ✗ |
| Col2 | `. X O` | ✗ |
| Diag | `. . O` | ✓ |
| Anti-diag | `. . O` | ✓ |

**MIN chance = 4** (Row0, Col0, Diag, Anti-diag)

```
Board value = 5 × 3 − 2 × 4 = 15 − 8 = +7
```

> Row0 counts for **both** players — it is completely empty, so either could fill
> it. That is correct and expected under this definition.

**Q4 — UCB**

```
UCB = v + 1.41 × sqrt( ln(100) / n )        ln(100) = 4.6052

A:  0.60 + 1.41 × sqrt(4.6052/20) = 0.60 + 1.41 × 0.4799 = 0.60 + 0.677 = 1.277
B:  0.55 + 1.41 × sqrt(4.6052/5)  = 0.55 + 1.41 × 0.9597 = 0.55 + 1.353 = 1.903
C:  0.75 + 1.41 × sqrt(4.6052/60) = 0.75 + 1.41 × 0.2770 = 0.75 + 0.391 = 1.141
```

**MCTS selects B (UCB = 1.903).**

**In one sentence:** B has the **worst** win rate but has only been tried **5**
times, so its exploration bonus (1.353) dwarfs the others — UCB deliberately
re-tests under-sampled options because a 55% estimate from 5 trials is far less
trustworthy than a 75% estimate from 60.

**Q5.** Because **after MAX chooses a branch, MIN moves next** — so MAX never
actually receives the best leaf in that branch, only whatever MIN is willing to
leave. MAX therefore evaluates each branch by its **worst-case** outcome (the MIN
value) and picks the branch whose worst case is best.

**Q6.**
```
PRUNE WHEN  β ≤ α
```
- **α** = the best value **MAX** is already guaranteed somewhere up the tree — a
  **lower bound**. It only ever **increases**.
- **β** = the best value **MIN** is already guaranteed — an **upper bound**. It
  only ever **decreases**.

Alpha-beta returns **exactly** the same answer as minimax because it only ever
cuts branches that **cannot affect the root value**: once `β ≤ α`, the player
above already has a better option elsewhere and will never let play reach this
node, so whatever is inside it is irrelevant. **No information that could change
the decision is discarded.**

**Q7 — MCTS phases**
1. **Selection** — from the root, repeatedly pick the most promising child,
   balancing exploitation (high win rate) and exploration (few visits).
2. **Expansion** — at a node with unexplored legal moves, add **one new child**.
3. **Simulation (rollout)** — play from that new node to the end with random or
   lightweight-heuristic moves, to estimate win/loss/draw.
4. **Backpropagation** — push the result back through **every node on the path**,
   updating visit count, win score and win rate.

**Q8.**
```
Best case  (PERFECT move ordering) :  O(b^(d/2))   -- effectively doubles the depth searchable
Worst case (bad move ordering)     :  O(b^d)       -- no better than plain minimax
```
What determines it is the **order in which moves are examined**. Examining strong
moves first raises α (or lowers β) early, which makes the `β ≤ α` condition fire
sooner and cuts more of the remaining tree.

</details>

---

## 12. Two-minute recall card

- Adversarial search: **two+ agents, conflicting goals**; next state depends on **our action AND the opponent's**.
- Six game components: **Initial state · Player(s) · Actions(s) · Result(s,a) · Terminal-test · Utility(s,p)**.
- **MAX maximises, MIN minimises.** Zero-sum: one's gain is the other's loss.
- **Minimax: MAX picks the branch whose WORST CASE is best.** Not the branch containing the biggest leaf.
- Back values up **from the leaves to the root**; MAX nodes take max, MIN nodes take min.
- Static evaluation = estimate a **non-terminal** state **without searching further**.
- `Score = MAX pieces − MIN pieces` · `Eval = material + king safety + mobility + board control`.
- **Alpha-beta gives the SAME answer as minimax**, just faster.
- `α = −∞, β = +∞` initially · `VAL ≥ α → α = VAL` · `VAL < β → β = VAL` · **PRUNE WHEN `β ≤ α`**.
- **α only rises, β only falls.** α = MAX's lower bound, β = MIN's upper bound.
- Move ordering: perfect → **`O(b^(d/2))`**, bad → `O(b^d)`.
- **MCTS four phases: Selection · Expansion · Simulation (rollout) · Backpropagation.**
- **`UCB = v_i + C·√(ln N / n_i)`** — first term exploit, second term explore. Bonus → ∞ as `n_i` → 0, so **every option is tried at least once**.
- MCTS needs a **combinatorial game**: two players, alternating turns, finite well-defined moves, perfect information.
- Past paper Q1 answer: **`S0 = −5`, best path `S0 → S2 → S7`.**
- **Read the question's own definition of "chance of win" every time** — the endsem and the sample deck define it differently.
