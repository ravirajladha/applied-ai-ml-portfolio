# Ch 12 — Multi-Agent Decision Making I: Non-Cooperative Game Theory
**Slides: CS#14** (post-midsem deck, PDF pages 56–66)

> ### ⚠ Read this before you decide to skip it
> This chapter scored **0 marks across all three past papers**. That is *not*
> evidence it is safe to skip. The papers are from **2024–25**; your deck was
> generated **16-Aug-2026** and contains CS#14 and CS#15 on exactly this
> material. If it is new to the syllabus this session, it has never *had* a
> chance to appear — and new content is **more** likely to be examined, not less.
> Treat the zero as *"no evidence"*, not *"evidence of absence"*.

> Open `explainers/ch12-maximin-mixed-strategy.html` first — it draws the
> maximin graph line by line so you can see why the answer sits at the crossing
> point before you do any algebra.

---

## 1. Why game theory shows up in an AI course

Everything in Ch 1–11 assumed **one decision maker** against a passive world:

| Ch 1–11 problems | Ch 12 problems |
|---|---|
| Path planning · image classification · speech recognition | Chess · autonomous driving · online auctions |
| The world does not fight back | Another **intelligent agent** is trying to change your outcome |
| Optimise your own choice | Optimise your choice **given what they will choose** |

Game theory is the mathematics for the second column. It lets an agent answer
three questions:

1. **What should I do?**
2. **What will my opponent do?**
3. **What is my best possible response?**

**Applications from the slides:** chess and board games · autonomous vehicles ·
robot soccer · cybersecurity · business negotiation · online auctions ·
financial trading · multi-robot systems.

---

## 2. The five elements of a game — *learn these five words*

Any exam answer that starts "a game consists of…" should list exactly these.

| # | Element | One-line definition | Examples from the slides |
|---|---|---|---|
| 1 | **Players** | The decision makers | humans, AI agents, companies, robots |
| 2 | **Actions** | Possible moves available to each player | Move Left, Raise, Fold, Attack, Defend |
| 3 | **Strategy** | A **complete plan** saying what action to take in **every** possible situation | *more than one move* |
| 4 | **Payoff (Utility)** | The reward obtained after the game ends | winning, profit, score, utility value |
| 5 | **Information** | What a player knows before deciding | complete · partial · imperfect |

> **⚠ Action ≠ Strategy.** This is the distinction markers look for.
> An **action** is "I play Left, once." A **strategy** is "if he goes Left I go
> Right, if he goes Right I go Left, and if he stalls I go Centre." A strategy is
> a whole rulebook; an action is one line of it.

> **Think about it (from the slides):** *Can two players choose the same action
> and get different payoffs?*
> **Yes** — the payoff depends on the **combination** of everyone's actions, not
> on your action alone.

---

## 3. Rational agents — and what "rational" does NOT mean

A rational agent maximises **expected utility**. Concretely it:

- selects the best available action
- predicts opponent behaviour
- plans several steps ahead
- evaluates future consequences
- avoids actions leading to lower utility

**Assumptions game theory makes about players.** They know the rules, know their
available actions, prefer higher utility, make logical decisions, and never
intentionally pick a worse outcome when a better one exists.

> **⚠ Important observation the slides call out explicitly:**
> **Rational does not mean selfish.** A rational player will happily **cooperate**
> if cooperating gives a higher payoff. This one line is a likely short-answer
> question — it is exactly the sort of "common misconception" markers like.

---

## 4. Types of games — the four labels

| Type | Rule | Examples |
|---|---|---|
| **Zero-sum** | One player's gain **equals** another's loss; total payoff is constant | Chess, Tic Tac Toe, Checkers |
| **Non-zero-sum** | Both may gain; both may lose | Trade negotiation, climate agreements, traffic management |
| **Cooperative** | Players **communicate** and work together (binding agreements) | Multi-robot coordination, team sports |
| **Non-cooperative** | Players act **independently** | Chess, Poker, online auctions |

> **The slides' own quiz:** *Which category does Poker belong to?*
> **Answer: Non-Cooperative, Imperfect Information.** Note it needs **two**
> labels — the cooperation axis and the information axis are separate. If a
> question says "classify this game", give both.

> **⚠ Zero-sum and cooperative are different axes.** Chess is *zero-sum* **and**
> *non-cooperative*. Don't treat "zero-sum" and "non-cooperative" as synonyms.

---

## 5. Four ways to represent a game

| # | Representation | Use when | Shows |
|---|---|---|---|
| 1 | **Payoff Matrix** (normal form) | Players act **simultaneously** | Payoff for every combination of actions |
| 2 | **Game Tree** | **Sequential** decision making | Every possible move from start to end |
| 3 | **Extensive Form** | Sequential + uncertainty | Decision nodes, **chance nodes**, **information sets**, utilities |
| 4 | **Finite State Machine** | **Repeated** games | Memory-based strategies compactly |

The slides' payoff-matrix example:

```
            B1    B2
     A1      3    -1
     A2      2     4
```

**Game tree components:** root node · decision nodes · branches · terminal nodes
· utility values. Leaf nodes carry the final outcome's utility.

> **Extensive form vs plain game tree:** the extensive form adds **information
> sets** — a dotted line grouping nodes a player *cannot tell apart*. That is how
> you draw *imperfect information* (poker). A plain game tree assumes you can see
> everything.

---

## 6. Minimax — the recap

Fully worked in **`ch06-07-minimax-alphabeta-mcts.md`** (that is where the
9-mark Connect-Three question lives). CS#14 re-states it because it is the
foundation for maximin.

```
Step 1: Generate the complete game tree.
Step 2: Assign utility values to terminal nodes.
Step 3: MIN nodes take the MINIMUM of their children.
Step 4: MAX nodes take the MAXIMUM of the values returned by MIN.
Step 5: Propagate upward. The root value = the optimal outcome.
```

The slides' two key sentences, both good short-answer material:

- *"Why doesn't MAX simply choose the branch with the highest leaf value?"*
  → **Because MIN controls the next move.** MAX only ever receives what MIN is
  willing to hand back.
- *"The algorithm never assumes the opponent will make mistakes."* Minimax gives
  the **best worst-case** outcome — the guaranteed payoff. Even if the root value
  is negative (the slides use −3), that is still the best available option.

---

## 7. Pure vs mixed strategies

**Pure strategy** = always choose one specific action.

**The problem with pure strategies:** if the opponent can predict you, they can
exploit you.

> **The goalkeeper analogy (straight off the slides).** A goalkeeper who *always*
> dives left is 100% predictable. The striker just shoots right, every time. The
> strategy is not "bad" in isolation — it is bad **because it is readable**.

**Mixed strategy** = a **probability distribution over pure strategies**. Instead
of always doing the same thing, randomise:

```
     Left  40%        Right 40%        Centre 20%
```

Now the striker cannot confidently predict anything.

**Why mixed strategies work:** the randomness is **not** for its own sake. It is
used strategically to **prevent exploitation**.

> **The one-line exam definition:** *A mixed strategy makes every possible action
> appear equally risky to the opponent.*

**Advantages:** reduces predictability · increases robustness against intelligent
opponents · better long-term performance.
**Applications:** poker · security patrol scheduling · cybersecurity · military
planning · autonomous robotics.

---

## 8. Maximin — the definition and the procedure

> **Maximin selects the action that produces the highest minimum payoff.**

```
MAXIMIN (for the row / first player)
   1. For every one of MY strategies, find the MINIMUM payoff it can produce.
   2. Compare all those minimums.
   3. Choose the strategy with the LARGEST minimum.

MINIMAX (for the column / second player)
   Mirror image: for each of MY strategies find the MAXIMUM the opponent gets,
   then choose the strategy with the SMALLEST maximum.
```

**Why maximin?** It protects you against a highly intelligent opponent. It is a
**conservative, risk-minimising** rule — you are guaranteed *at least* the
maximin value no matter what they do.

**AI applications:** chess engines · military planning · financial risk
management · autonomous systems.

### Saddle point

If **maximin value = minimax value**, that cell is a **saddle point** and the
game has a **solution in pure strategies**. If they differ, **no pure-strategy
solution exists** and you must go to **mixed strategies** — which is exactly what
§10 does.

---

## 9. Formula box

```
PURE MAXIMIN / MINIMAX

    maximin  =  max_i  ( min_j  u(i, j) )        row player's guarantee
    minimax  =  min_j  ( max_i  u(i, j) )        column player's guarantee

    maximin = minimax   ->  SADDLE POINT, solve in pure strategies
    maximin < minimax   ->  no pure solution, use a MIXED strategy


MIXED STRATEGY, 2x2 ZERO-SUM  (payoffs are to the ROW player)

                  C1        C2
        R1        a         b
        R2        c         d

    Row plays R1 with probability p, R2 with probability (1 - p).

        vs C1 :  E1(p)  =  a·p + c·(1 - p)
        vs C2 :  E2(p)  =  b·p + d·(1 - p)

    Row's guaranteed value  V(p) = MIN( E1(p), E2(p) )      <- lower envelope
    Maximise it by SOLVING   E1(p) = E2(p)                  <- the crossing point

    Column's q found the same way by setting the ROW payoffs equal.
    Game value V is the same either way (that is the minimax theorem).


PARAMETERIZED GAME TREE
    Replace a fixed branch choice with "probability p / (1 - p)".
    The leaf values become linear FUNCTIONS of p.
    Then optimise over p instead of over branches.
```

> **The trick in one line:** you pick `p` so that the opponent's two options give
> you **exactly the same** payoff. Once they are equal, the opponent has nothing
> to exploit — whichever they pick, you get the same. That crossing point is the
> answer.

---

## 10. NUMERICAL — Two-finger Morra, maximin mixed strategy (the slides' own example)

This is the one genuine calculation in CS#14. Learn this shape.

### The game

Two players, **E** (even) and **O** (odd), each show one or two fingers.
Payoffs to **E**:

```
                O: one     O: two
     E: one       +2         -3
     E: two       -3         +4
```

### Step 1 — check for a pure-strategy solution first

```
     Row minimums:   E:one -> min(+2, -3) = -3
                     E:two -> min(-3, +4) = -3        maximin = -3

     Col maximums:   O:one -> max(+2, -3) = +2
                     O:two -> max(-3, +4) = +4        minimax = +2
```

`maximin = -3` and `minimax = +2` are **not equal** → **no saddle point** →
E must play a **mixed** strategy. *(Always run this check first. It is one line
and it justifies everything that follows.)*

### Step 2 — parameterize

E plays **one** with probability `p`, **two** with probability `(1 − p)`.
This is the parameterized game tree on slide 35:

```
              E   [p: one ;  (1-p): two]
              |
              O
             / \
          one   two
           |     |
    2p - 3(1-p)   -3p + 4(1-p)
```

> **⚠ Typo watch in your deck.** Slide 35 prints the right-hand leaf as
> `3p + 4(1−p)`. The **leading minus sign is missing** — it must be
> `−3p + 4(1−p)`. You can prove it from the deck's own graph on slide 38: that
> line hits **−3 at p = 1**, and only `−3p + 4(1−p)` does that. Use `−3p`.

### Step 3 — simplify the two lines

```
     If O plays "one":   E1(p) = 2p - 3(1 - p)  = 2p - 3 + 3p =  5p - 3
     If O plays "two":   E2(p) = -3p + 4(1 - p) = -3p + 4 - 4p = 4 - 7p
```

Sanity-check the endpoints against the graph:

| p | E1 = 5p − 3 | E2 = 4 − 7p | min (what E actually gets) |
|---|---|---|---|
| 0 | −3 | +4 | **−3** |
| 1 | +2 | −3 | **−3** |

Both ends give −3. So the lower envelope is a **tent** — it rises from −3, peaks
somewhere in the middle, and falls back to −3. The peak is the answer.

### Step 4 — O is minimising, so E gets the LOWER of the two lines

```
     V(p)  =  min( 5p - 3 ,  4 - 7p )
```

`5p − 3` **rises** with p; `4 − 7p` **falls** with p. The minimum of a rising and
a falling line is maximised **exactly where they cross**.

### Step 5 — solve for the crossing point

```
        5p - 3  =  4 - 7p
        5p + 7p =  4 + 3
            12p =  7
              p =  7/12  =  0.5833
```

### Step 6 — the value of the game

```
     V  =  5(7/12) - 3   =  35/12 - 36/12  =  -1/12  =  -0.0833

     check with the other line:
     V  =  4 - 7(7/12)   =  48/12 - 49/12  =  -1/12   ✓
```

### Answer

> **E should show one finger with probability 7/12 and two fingers with
> probability 5/12. The value of the game to E is −1/12.**

Reading it back: even playing optimally, E **loses** on average — just very
slowly, 1/12 of a point per round. Morra is slightly unfair to E, and the best
E can do is minimise the bleeding. **A negative value is still the right answer**
— maximin picks the best of the bad options.

### Step 7 — the mirror check (slide 36 / figure (b))

Now let **O** play *one* with probability `q`. E's payoffs:

```
     If E plays "one":  2q - 3(1 - q)  =  5q - 3
     If E plays "two":  -3q + 4(1 - q) =  4 - 7q
```

E **maximises**, so E takes the **upper** envelope; O picks `q` to **minimise**
that upper envelope — again at the crossing:

```
     5q - 3 = 4 - 7q   ->   q = 7/12,   value = -1/12
```

> **maximin = minimax = −1/12.** The game has a **value**. This is von Neumann's
> minimax theorem in action: for a two-player zero-sum game, the row player's
> guarantee and the column player's guarantee meet at the same number once you
> allow mixed strategies.

---

## 11. Graphical interpretation of maximin — how to draw it for marks

The exam may say *"depict with neat diagrams in addition to tabular
representation"*. Here is what to draw.

```
    U
   +4 |\
      | \                    "two"  =  4 - 7p
   +2 |  \              _____________/
      |   \       _____/
    0 |----\----X--------------------------  p
      |     \  /|
      |  ___\/  |
   -2 |_/    \  |            "one"  =  5p - 3
   -3 |       \ |
      +---------+---------------------------
      0      7/12                       1

    HEAVY LINE = the lower envelope = what E actually receives.
    E picks the p at the INTERSECTION POINT.
```

Say these four things next to the graph — they are the marking points:

1. **Each line = one of the opponent's pure strategies.**
2. The opponent will always pick the **better (for them) of the two**, so E's real
   payoff is the **heavy lower envelope**.
3. E chooses the probability where that **lowest payoff is as high as possible**.
4. At the **intersection point**: neither strategy dominates · the opponent
   cannot exploit predictable behaviour · the minimum payoff is maximised.

> **Why the intersection and not somewhere else?** Anywhere left of 7/12, O plays
> "one" and drags you down the rising line. Anywhere right of 7/12, O plays "two"
> and drags you down the falling line. Only at the crossing does it stop
> mattering which one they pick — and that is the highest point of the tent.

---

## 12. Repeated games

Most real interactions are not one-shot. The **same players** meet again.

| One-shot game | Repeated game |
|---|---|
| Played once | Played multiple times |
| No history | **History influences future actions** |
| Short-term strategy | Long-term strategy |
| Limited cooperation | **Cooperation often develops** |

**Characteristics:** previous actions influence future decisions · players learn
from experience · **reputation** becomes important · cooperation may emerge over
time · players can reward cooperation and punish betrayal.

> **The corridor analogy from the slides.** Two delivery robots repeatedly share
> a narrow corridor. If both cooperate, traffic flows. If one barges through
> once, the other refuses to yield next time. **Memory turns isolated decisions
> into long-term strategy** — and that is what makes trust and reputation
> possible at all.

**AI applications:** multi-agent reinforcement learning · cloud resource
allocation · swarm robotics · autonomous transportation · network routing.

---

## 13. The five repeated-game strategies — *this table is very examinable*

| Strategy | First move | Reaction to defection | Forgiveness | Suitable environment |
|---|---|---|---|---|
| **Hawk** | Defect | Always defect | **No** | Highly competitive |
| **Dove** | Cooperate | Continue cooperating | **Yes** | Cooperative systems |
| **Grim** | Cooperate | **Defect forever** | **No** | Stable environments |
| **Tit-for-Tat** | Cooperate | **Defect once** | **Yes** | Most real-world systems |
| **Tat-for-Tit** | Defect | Mimics opponent | Limited | Defensive scenarios |

**Hawk / Dove.** Hawk is always aggressive, never compromises, maximises
immediate payoff — and causes disaster against another Hawk. Dove avoids
conflict, shares resources, seeks mutual benefit — and gets exploited by Hawks.
*The narrow-bridge example:* Hawk behaviour = neither vehicle gives way; Dove
behaviour = one yields and traffic flows.

**Grim.** Cooperate initially → keep cooperating while they cooperate → **if they
defect even once, defect forever.**
*Good:* strongly discourages betrayal, simple, encourages long-term cooperation.
*Bad:* **extremely unforgiving** — one accidental mistake permanently destroys
cooperation. **Unsuitable for noisy environments** where signals get garbled.

**Tit-for-Tat.** Start by cooperating, then **copy whatever the opponent did last
round**. The most successful strategy discovered in game theory. Four properties
— **memorise these four words**:

| Property | Meaning |
|---|---|
| **Nice** | Never defects first |
| **Forgiving** | Returns to cooperation as soon as they do |
| **Retaliatory** | Punishes betrayal immediately |
| **Clear** | Easy to understand, so opponents can learn to cooperate with it |

> **The slides' own question:** *Why is Tit-for-Tat often more successful than
> Grim?* → **Because it forgives occasional mistakes.** Grim treats one slip as
> permanent; Tit-for-Tat lets you recover.

**Tat-for-Tit.** The mirror image: **defect first**, then imitate. Less
cooperative initially, builds trust slowly, may increase conflict. Suitable where
deception is common. Modern AI systems generally prefer **Tit-for-Tat** because
it promotes stable cooperation.

> **No strategy is universally optimal.** The best strategy depends on the
> environment. Say that sentence if asked "which is best?" — then justify with
> the environment column of the table.

---

## 14. Finite State Machine strategies

An FSM has **states · transitions · inputs · outputs**. Each state represents the
player's current strategy; the next state depends on the **opponent's previous
action**.

**Tit-for-Tat as an FSM:**

```
                 opponent COOPERATES
              +---------------------+
              |                     |
              v     opponent        |
        [ COOPERATE ] --DEFECTS--> [ DEFECT ]
              ^                     |
              +---------------------+
                 opponent COOPERATES
```

- Start in state **Cooperate**.
- Opponent cooperates → **stay** in Cooperate.
- Opponent defects → **transition** to Defect.
- Opponent resumes cooperating → **return** to Cooperate.

*(Grim is the same picture with the return arrow deleted — once in Defect, you
never leave. That single missing arrow is the entire difference between Grim and
Tit-for-Tat, and it is a nice thing to say in an answer.)*

**Why FSM?** Instead of remembering the **entire history**, the agent only
remembers its **current state**. That is the whole point: compact memory.

**Advantages:** easy implementation · minimal memory · fast decisions · suitable
for embedded AI. Many robot soccer teams use FSM behavioural controllers.

---

## 15. Sequential games, backward induction, and SPNE

**Sequential game:** players move **one after another**, and later players can
observe earlier decisions. The **order of play** influences the outcome.
*Examples:* chess, company negotiation, investment decisions, political
campaigns, supply chain management.

Represented in **extensive form**: decision nodes · branches · terminal nodes ·
payoff values · **information sets**.

### Backward Induction

```
   1. Identify the terminal nodes.
   2. Determine the optimal decision at the LAST stage.
   3. Replace each subtree with its optimal payoff.
   4. Continue moving backward until you reach the root.
```

**Why it works:** every rational player picks the payoff-maximising action at
every stage, so earlier players can *predict* the later decisions and plan
around them.

> This is **the same machinery as minimax**, with one difference: in minimax the
> two players want opposite things (zero-sum), so one maximises and one
> minimises. In general backward induction, **each player maximises their own
> entry** in the payoff pair. Read the correct number out of the tuple.

### Subgame Perfect Nash Equilibrium (SPNE)

> A strategy profile is an **SPNE** if it is a **Nash equilibrium in every
> subgame** of the original game.

**Why we need it:** some Nash equilibria contain **non-credible threats** —
actions a player threatens but would never actually carry out, because carrying
them out would hurt them. SPNE **eliminates** those.

**Properties:** always based on rational behaviour · **removes non-credible
threats** · obtained using **backward induction** · produces stable solutions.

### Worked — the non-credible threat, in numbers

An **Entrant** decides whether to enter a market. If it enters, the **Incumbent**
decides whether to Fight or Accommodate. Payoffs `(Entrant, Incumbent)`:

```
                        Entrant
                       /       \
                 Stay Out       Enter
                    |             |
                  (0, 10)     Incumbent
                               /      \
                           Fight    Accommodate
                             |            |
                          (-2, 2)       (3, 5)
```

**Backward induction — start at the LAST decision (the Incumbent):**

```
   Incumbent compares its OWN payoff:  Fight = 2   vs   Accommodate = 5
   5 > 2   ->   Incumbent will ACCOMMODATE.
   Replace that whole subtree with its value: (3, 5).
```

**Now move up to the Entrant:**

```
   Entrant compares its OWN payoff:  Stay Out = 0   vs   Enter = 3
   3 > 0   ->   Entrant will ENTER.
```

> **SPNE = (Enter, Accommodate), with payoffs (3, 5).**

**Where the non-credible threat hides.** "Entrant stays out, Incumbent fights"
*is* a Nash equilibrium: given the threat of Fight, the Entrant prefers 0 over
−2, and given that the Entrant stays out, the Incumbent's threat is never tested
so it costs nothing. But the threat is **not credible** — if the Entrant actually
walks in, fighting earns 2 and accommodating earns 5, so the Incumbent would
never really fight. **Backward induction kills it, and SPNE is what remains.**

> **Say this sentence in the exam:** *"A non-credible threat survives as a Nash
> equilibrium because it is never tested on the equilibrium path; SPNE requires
> rationality at every node, including nodes that are never reached, so the
> threat is eliminated."*

---

## 16. Games with imperfect information

| Perfect information | Imperfect information |
|---|---|
| All moves visible | Some information hidden |
| Deterministic planning | **Probabilistic reasoning** |
| **Chess** | **Poker** |

**Characteristics:** hidden information · uncertainty about opponents' actions ·
decisions based on probabilities and beliefs · multiple possible futures.
*Examples:* poker, card games, auctions, cybersecurity, military operations.

**What an AI must do instead:** estimate the unknown using **probability theory ·
Bayesian reasoning · opponent modelling · learning from previous observations**.

### Poker

> **Why is poker harder for AI than chess?**
> **Because players must decide with incomplete information.** In chess the
> entire state is on the board; in poker the most important part of the state —
> the opponent's cards — is invisible. So the agent must reason over a
> *distribution* of possible states, not one state.

**What poker success depends on:** hidden information · probability calculations
· **bluffing** · opponent modelling · risk assessment.

**AI techniques used:** Bayesian networks · **MCTS** · reinforcement learning ·
deep neural networks · **Counterfactual Regret Minimization (CFR)**.

**Named systems:** **Pluribus** and **Libratus** achieved superhuman multiplayer
poker. *(Worth naming — "give a real-world case study" questions reward it.)*

---

## 17. Assistance games (the Paperclip Game)

An **assistance game** is a **cooperative** game in which an AI agent helps a
human achieve a **shared** objective — but **the AI does not know the human's
exact preferences**.

**Characteristics:** human and AI collaborate · shared objective · the AI
**learns human preferences over time** · communication and observation matter.

**The Paperclip Game.** A human and a robot collect paperclips together. The
robot starts out uncertain about what the human actually wants. By observing
actions and receiving feedback it gradually learns **which tasks are preferred**,
**how to assist effectively**, and **when to ask for clarification**.

**Applications:** healthcare assistants · autonomous robots · personal digital
assistants · smart homes · human–robot collaboration.

> **The point of this slide, and the closing line of CS#14:** the field is moving
> from *competing against* humans to *understanding and assisting* them. If a
> question asks about the future direction of multi-agent AI, this is the answer.

---

## 18. You try

Attempt all of these before opening §19. Reading a solved sum feels like
learning and isn't.

**Q1 — Pure maximin/minimax.** Payoffs to the Row player:

```
            C1    C2    C3
     R1      4     2     5
     R2      3     6     1
     R3      7     3     2
```
(a) Find Row's maximin value and strategy.
(b) Find Column's minimax value and strategy.
(c) Is there a saddle point? What does your answer imply Row must do?

**Q2 — Mixed strategy, 2×2.** Payoffs to Row:

```
            C1    C2
     R1      3    -1
     R2     -2     4
```
(a) Confirm there is no saddle point.
(b) Find Row's optimal `p` (probability of playing R1) and the value of the game.
(c) Find Column's optimal `q` (probability of playing C1). Does the value agree?

**Q3 — Backward induction / SPNE.** Payoffs `(Player 1, Player 2)`:

```
                      P1
                    /    \
                   L      R
                   |       |
                  P2      P2
                 /  \    /  \
                a    b  c    d
                |    |  |    |
             (3,1)(0,0)(2,2)(1,5)
```
(a) Solve by backward induction. What does each player do?
(b) State the SPNE and the resulting payoffs.

**Q4 — Concept, exam-phrased.** *"Differentiate between Grim and Tit-for-Tat as
repeated-game strategies. State which is preferred for a noisy multi-agent
system and justify with a relatable real-world case study."* (3 marks)

**Q5 — Classification.** Classify each on **both** axes (zero-sum vs non-zero-sum,
and cooperative vs non-cooperative), and state the information type:
(a) Chess (b) Poker (c) Two warehouse robots sharing a charging dock
(d) Two airlines setting ticket prices independently.

---

## 19. Answers

### Q1

**(a) Row's maximin.**
```
     R1 -> min(4, 2, 5) = 2
     R2 -> min(3, 6, 1) = 1
     R3 -> min(7, 3, 2) = 2
     maximin = max(2, 1, 2) = 2       via R1 or R3  (tie)
```
**(b) Column's minimax.** Column pays out the row-player payoff, so Column wants
the **maximum in each of its columns to be small**:
```
     C1 -> max(4, 3, 7) = 7
     C2 -> max(2, 6, 3) = 6
     C3 -> max(5, 1, 2) = 5
     minimax = min(7, 6, 5) = 5       via C3
```
**(c)** `maximin = 2`, `minimax = 5`. They are **not equal**, so there is **no
saddle point** and **no pure-strategy solution**. Row must use a **mixed
strategy**. The value of the game lies somewhere in `2 ≤ V ≤ 5`.

> *If you flagged the tie in (a) as a problem — it isn't. Ties are fine; state
> both and, if the paper asks, apply alphabetical/lowest-index tiebreaking (R1).*

### Q2

**(a)**
```
     Row mins:  R1 -> min(3, -1) = -1 ;  R2 -> min(-2, 4) = -2   maximin = -1
     Col maxes: C1 -> max(3, -2) =  3 ;  C2 -> max(-1, 4) = 4    minimax =  3
```
`-1 ≠ 3` → no saddle point → mixed strategy needed. ✓

**(b)** Row plays R1 with probability `p`:
```
     vs C1:   3p + (-2)(1 - p)  =  3p - 2 + 2p  =  5p - 2
     vs C2:  -1p +   4 (1 - p)  = -p + 4 - 4p   =  4 - 5p

     Set equal:   5p - 2 = 4 - 5p
                     10p = 6
                       p = 0.6

     Value:  V = 5(0.6) - 2 = 3 - 2 = 1
     check:  V = 4 - 5(0.6) = 4 - 3  = 1   ✓
```
> **Row plays R1 with probability 0.6 and R2 with probability 0.4. V = 1.**

**(c)** Column plays C1 with probability `q`:
```
     Row's R1 payoff:   3q + (-1)(1 - q)  =  4q - 1
     Row's R2 payoff:  -2q +   4 (1 - q)  =  4 - 6q

     Set equal:   4q - 1 = 4 - 6q
                     10q = 5
                       q = 0.5

     Value:  V = 4(0.5) - 1 = 1   ✓  same as (b)
```
**Yes — the value agrees at V = 1**, as the minimax theorem requires.

### Q3

**(a) Backward induction — start at P2's nodes.**
```
   P2 at the LEFT node  (after L): compares its own payoff, 1 (a) vs 0 (b)
                                   1 > 0  ->  P2 plays a.  Subtree value = (3, 1)

   P2 at the RIGHT node (after R): compares its own payoff, 2 (c) vs 5 (d)
                                   5 > 2  ->  P2 plays d.  Subtree value = (1, 5)

   P1 at the root:  L now yields 3,  R now yields 1
                    3 > 1  ->  P1 plays L.
```
**(b) SPNE = (L; a after L, d after R), payoffs (3, 1).**

> **The trap here, and it is the whole point of the question.** P1's *best
> possible* leaf is 3 at `(L, a)` — which it does get. But look at the right
> branch: the leaf `c` would give P1 a payoff of 2, and P1 has no way to reach
> it, because **P2 controls that choice and prefers d (5) over c (2)**. You must
> read the **second** number when deciding what P2 does. Reading P1's number at
> P2's node is the single most common error in this question type.
>
> Note also that an SPNE specifies **what P2 would do at the node that never gets
> reached** (d after R). That is exactly what "Nash in *every* subgame" means —
> off-path behaviour is part of the answer. Write both.

### Q4 (model 3-mark answer)

> **Assumption stated first:** agents observe each other's actions, but the
> channel is noisy, so a cooperative action is occasionally misread as a
> defection.
>
> **Grim:** cooperate first; cooperate while the opponent cooperates; **if the
> opponent defects even once, defect forever**. Unforgiving, no recovery path.
> **Tit-for-Tat:** cooperate first; then **copy the opponent's previous move**.
> It defects **once** in retaliation, then returns to cooperation as soon as the
> opponent does. It is **nice, forgiving, retaliatory and clear**.
>
> **Preferred for a noisy system: Tit-for-Tat.** Under Grim, a **single**
> misread signal is irreversible — both agents are locked into mutual defection
> for the rest of the interaction, and total payoff collapses. Tit-for-Tat costs
> one round of retaliation and then recovers.
>
> **Case study:** two autonomous delivery robots sharing a narrow corridor. A
> sensor glitch makes Robot A read Robot B's yield as a barge-through. Under
> Grim, A refuses to yield for the rest of the day and the corridor deadlocks
> permanently. Under Tit-for-Tat, A refuses once, B yields on the next
> encounter, and normal traffic resumes.

*(Note the structure: assumption → both definitions → the verdict with a reason →
a concrete named example. That maps onto the marking scheme's three marks.)*

### Q5

| Game | Zero-sum? | Cooperative? | Information |
|---|---|---|---|
| (a) **Chess** | **Zero-sum** | **Non-cooperative** | **Perfect** |
| (b) **Poker** | **Zero-sum** | **Non-cooperative** | **Imperfect** |
| (c) **Two warehouse robots sharing a dock** | **Non-zero-sum** | **Cooperative** | Typically perfect/complete |
| (d) **Two airlines pricing independently** | **Non-zero-sum** | **Non-cooperative** | Imperfect (simultaneous, private costs) |

> **(d) is the one to get right.** Independent pricing is *non-cooperative* — no
> binding agreement — but it is emphatically **not zero-sum**: both airlines can
> lose in a price war, and both can gain from restraint. That is the classic
> non-zero-sum, non-cooperative combination (the Prisoner's Dilemma shape).

---

## 20. Two-minute recall card

- **Five elements:** Players · Actions · **Strategy** · Payoff · Information.
- **Action = one move. Strategy = a complete plan for every situation.**
- **Rational ≠ selfish.** A rational agent cooperates if cooperation pays more.
- Same action, different payoff? **Yes** — payoff depends on the *combination*.
- **Poker = non-cooperative + imperfect information.** Give **both** labels.
- **Four representations:** payoff matrix (simultaneous) · game tree (sequential)
  · extensive form (+ chance nodes, **information sets**) · **FSM** (repeated).
- **Why not just take the biggest leaf? Because MIN controls the next move.**
- **Mixed strategy** = probability distribution over pure strategies; it *makes
  every action look equally risky to the opponent*.
- **Maximin = max of the row minimums.** Minimax = min of the column maximums.
- **maximin = minimax → saddle point → pure strategy. Not equal → go mixed.**
- **Mixed-strategy method: set the two expected-payoff lines EQUAL and solve.**
- **Morra: p = 7/12, value = −1/12.** Lines `5p − 3` and `4 − 7p`.
- Deck typo: slide 35's right leaf must be **`−3p + 4(1−p)`**, not `3p`.
- The optimal `p` is at the **intersection point** of the payoff lines — neither
  strategy dominates and the opponent cannot exploit you there.
- **Grim = defect forever** (unforgiving, dies in noise). **Tit-for-Tat = defect
  once** — **Nice, Forgiving, Retaliatory, Clear**.
- **Tat-for-Tit starts by defecting.** Hawk = always aggressive; Dove = always yields.
- **Backward induction:** start at the last decision, replace subtrees with their
  values, walk to the root. **At each node read THAT player's own number.**
- **SPNE = Nash in every subgame → removes NON-CREDIBLE THREATS.**
- **Poker harder than chess** because decisions are made with **incomplete
  information**. Techniques: **CFR**, MCTS, Bayesian nets. Systems: **Pluribus, Libratus**.
- **Assistance game / Paperclip Game:** shared goal, but the AI must **learn the
  human's preferences** by observation and feedback.
