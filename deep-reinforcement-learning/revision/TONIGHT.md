# DRL Endsem — Tonight

**Open book — but only the watermarked course material may be carried in.**

> **You cannot take this file into the exam.** It is a study aid for tonight
> only. What you carry in is `AIMLCZG512 - DRL - Lecture notes.pdf` — see
> **"The lookup map"** at the end, which tells you the exact page for every
> formula on this sheet. Read that section *last*, but do not skip it.

---

## STEP 0 — Tab the printed notes (do this FIRST, 20 minutes)

**This is the single most important thing you will do tonight.** More important
than any recipe below.

You are never going to *search* 191 pages in an exam. You are going to **grab a
tab.** So tonight you stop treating the notes as something to read and start
treating them as a **filing cabinet you built yourself.**

Get sticky flags, torn paper strips, folded corners — anything. Put **nine
tabs** in the printed notes at these printed page numbers, and **write the
slot label on the tab, not the topic name**:

| Write on tab | Printed page | What's there |
|--------------|-------------|--------------|
| **CONTENTS** | **1** | The master list. When lost, come back here. |
| **Q1** | **19** | Bandits — UCB formula, incremental update, constant α |
| **Q2** | **45** | Dynamic Programming — value & policy iteration |
| **Q3a** | **65** | Off-policy Monte Carlo — importance sampling |
| **Q3b** | **83** | TD control — Q-learning, Sarsa, Expected Sarsa |
| **Q4a** | **93** | Semi-gradient TD(0), linear approximation |
| **Q4b** | **106** | Deep Q-Networks — replay, target network |
| **Q5a** | **153** | MCTS, AlphaGo, AlphaZero |
| **Q5b** | **166** | Imitation learning, behaviour cloning, DAGGER |
| **REVIEW** | **179** | Course summary — go here for any 1-mark definition |

Label them **Q1…Q5**, matching the five exam slots. Then the exam stops being
"where is this in 191 pages?" and becomes **"this is a Q2 → grab the Q2 tab."**

> **Remember: printed page = PDF page − 2.** The number printed in the page
> header is the one on the tabs above.

---

## STEP 0.5 — How to tell which tab from the question

Your worry: *"even if the question comes, I won't be able to find it."* You
will, because there are only five possibilities and each one announces itself
in the **first two lines**. Learn these tells:

| If the question mentions… | It's | Grab tab |
|---------------------------|------|----------|
| arms / treatments / ads / stocks / machines, `N(a)`, `Q(a)`, "exploration constant c", "t =" — and **no states** | Bandit | **Q1** |
| states + actions + **transition probabilities** + γ, "V(s) =", "one sweep", "greedy policy" | MDP / DP | **Q2** |
| **episodes** written as ⟨s,a,r,s,a,r⟩, "behaviour policy b", "target policy π" | Off-policy MC | **Q3a** |
| `Q(s,a) = …`, α, "next state", Q-learning / Sarsa / Expected Sarsa | TD control | **Q3b** |
| **feature vector** φ(s), weight vector **w**, "linear", "approximation" | Semi-gradient | **Q4a** |
| neural network, replay, target network, "stabilise", DQN | DQN | **Q4b** |
| **tree**, child nodes, **visit counts**, rollout, AlphaGo | MCTS | **Q5a** |
| expert demonstrations, cloning, drift, "the expert rarely visited" | Imitation | **Q5b** |

**The giveaway pairs:** *no states → Q1.* *States + probabilities → Q2.*
*φ(s) → Q4.* *Visit counts on a tree → Q5.* That's 80% of the identification
done in one glance.

---

## STEP 0.75 — The find drill (20 minutes, do it with the printed notes open)

Don't just read the tabs — **use** them. Time yourself. Target: **under 30
seconds each.** Cover the answers.

| # | "Find me…" | Tab | Printed p. |
|---|-----------|-----|-----------|
| 1 | the UCB formula | Q1 | 19–21 |
| 2 | the value-iteration update rule | Q2 | 45–48 |
| 3 | weighted vs ordinary importance sampling | Q3a | 65–71 |
| 4 | the Expected Sarsa target | Q3b | 83 |
| 5 | the semi-gradient weight update | Q4a | 93–99 |
| 6 | two things that stabilise DQN | Q4b | 106–115 |
| 7 | the UCB tree-policy score for MCTS | Q5a | 153–156 |
| 8 | how AlphaGo Zero gets its training targets | Q5a | 153–165 |
| 9 | what DAGGER does | Q5b | 166–169 |
| 10 | on-policy vs off-policy, in one line | REVIEW | 179 |

Do all ten. Then do them again shuffled. After the second pass your hand will
go to the right tab without thinking — **that is the skill being tested by an
open-book exam**, and it is the only skill you can still reliably build tonight.

**Three worked examples are already inside the notes** — they're gold, because
they show the format of a full answer:

- printed **p22** — Worked Example: bandit reward above baseline
- printed **p114** — Worked Example: one DQN update
- printed **p133** — Worked Example: Gaussian policy (this is Q4d, the drone)

There are also numbered practice questions around printed **p89–90**.

---

## The decision: do NOT read the slides

Nine decks, ~400 MB of PDF. You cannot read them in five hours and you do not
need to. Here is why.

I read three past endsem papers — **Sep 2026** (the most recent, same format as
tomorrow), **Compre Regular 24-24**, and **Jun 2024 Endsem**. They are the same
five questions every single time, with a different story wrapped around them:

| Slot | What it always is | Sep 2026 | Compre 24-24 | Jun 2024 |
|------|-------------------|----------|--------------|----------|
| 1 | **Bandit / UCB** numerical | Q1 (clinical trial) | Q1 (lab tests) | Q1 (stock trading) |
| 2 | **MDP → Value Iteration** numerical | Q2 (server cluster) | Q2 (warehouse robot) | Q2 (2-state MDP) |
| 3 | **MC / TD / Q-learning** numerical | Q3 (tutoring platform) | Q3 (lab tests) | Q3 (MC issues) |
| 4 | **Linear FA / semi-gradient TD(0)** + policy gradient theory | Q4 (AI tutor) | Q4 (lab tests) | Q3c, Q4d |
| 5 | **MCTS UCB** + AlphaGo + imitation learning | Q5 | Q5, Q6 | Q4, Q5 |

That's it. **Five recipes.** Each one is a ten-line calculation you can execute
from a formula, tonight, without understanding the derivation.

Your goal tonight is not "learn DRL." It is **"be able to execute five
procedures and look up the rest."** It's open book — the book is for the theory
parts. The numericals are what you must be able to do cold.

---

## Schedule

Sleep is a step, not an optional extra. You will lose more marks tired than
under-read.

| Time | Do this |
|------|---------|
| **now → +20 min** | **STEP 0 — tab the printed notes.** Nine tabs. Physical. Do not skip. |
| **+20 → +40 min** | **STEP 0.75 — the find drill.** Ten lookups, timed, twice. |
| **+40 min → 1h40** | **Recipe 1 & 2** (Bandit/UCB, Value Iteration). Work them on paper with the Sep 2026 numbers. Check against the answers here. |
| **1h40 → 2h40** | **Recipe 3** (MC importance sampling, TD(0), Q-learning/Sarsa/Expected Sarsa). The fattest slot — 3+1+3 marks. |
| **2h40 → 2h55** | Break. Walk. Eat something. |
| **2h55 → 3h35** | **Recipe 4** (semi-gradient TD(0)). Shortest recipe, easiest 3 marks on the paper. |
| **3h35 → 4h15** | **Recipe 5** (MCTS UCB) + read the theory answers once. |
| **4h15 → 4h50** | Re-do Recipe 2 and Recipe 3 **from blank paper**, no looking. These are the two that go wrong under time pressure. |
| **4h50 → 5h00** | Run the find drill **one last time**. Then stop. |
| **then** | **Sleep.** Put the tabbed notes in your bag before you sleep, not in the morning. |

---

## Skip list — deliberately do not open these tonight

Justified by what actually scored marks in three papers:

- ❌ `AIMLCZG512 - DRL - Lecture notes.pdf` (191 pages) **as reading material**.
  Too big to skim tonight. But it is the **one file you carry in** — so instead
  of reading it, learn *where things are in it*. That's the lookup map below.
- ❌ Decks 1–9 as reading material. Keep them **closed** tonight and **open**
  tomorrow — that's what open book is for.
- ❌ All the **midsem** papers in `QP/`. Their topics reappear in endsem slots
  1–3, and this file already covers those.
- ❌ The `webinars/` and `assignments/` notebooks. **Zero** code-writing
  questions appeared in any of the three endsem papers. Not one.
- ❌ Derivations, proofs, convergence guarantees. Never asked.

---

## Recipe 1 — Bandit / UCB

**Formula (write this on your sheet):**

```
UCB score for arm a:   Q(a) + c · sqrt( ln t / N(a) )
```

Pick the arm with the **highest score**.

**Worked — Sep 2026 Q1.** Three treatments, `t = 13`, `c = 1`. `ln 13 = 2.5649`.

| Arm | N | Q | bonus = √(2.5649/N) | score |
|-----|---|---|---------------------|-------|
| T1 | 4 | 0.6 | 0.8008 | **1.4008** |
| T2 | 6 | 0.5 | 0.6538 | 1.1538 |
| T3 | 2 | 0.3 | 1.1325 | **1.4325** ← picked |

T3 wins despite the *worst* Q, because it's been tried least. That sentence is
the answer to "explain the role of the exploration term."

**The c\* trick (they asked this in 2026 and it's the only algebra in the paper):**

Set the two scores equal and solve for c:

```
Q(T1) + c·b1 = Q(T3) + c·b3       where b = sqrt(ln t / N)
c* = (Q(T3) − Q(T1)) / (b1 − b3)
   = (0.3 − 0.6) / (0.8008 − 1.1325)  =  −0.3 / −0.3317  =  0.9045
```

- **c > c\*** → exploration dominates → the **less-visited** arm (T3) wins.
- **c < c\*** → exploitation dominates → the **higher-Q** arm (T1) wins.

**Two value-update rules (asked every time):**

```
Sample average:   Q ← Q + (1/N_new)·(R − Q)      N_new = N + 1
Constant step:    Q ← Q + α·(R − Q)
```

Sep 2026: T3 gets R = 1. N was 2 → 3.
- Sample average: `0.3 + (1/3)(1 − 0.3) = 0.5333`
- Constant α = 0.4: `0.3 + 0.4(1 − 0.3) = 0.58`

**"Which would you trust if things shift?"** → **Constant α.** It's an
exponential recency-weighted average: old rewards decay, so it tracks a moving
target. Sample-average weights every reward equally forever, so it gets anchored
to stale data. (Non-stationary → constant α. Memorise that one line.)

**Contextual bandit (2026 Q1d):** the moment you observe per-patient features
before choosing, the *context* is that feature vector (age, baseline severity,
medication history). One `Q(a)` per arm is no longer enough because the best arm
now **depends on who the patient is**. You must estimate `Q(context, a)` — a
function of features, e.g. `θ_aᵀx`, not a single scalar per arm.

---

## Recipe 2 — Value Iteration (in-place)

**Formula:**

```
V(s) ← max over a of  Σ_s'  P(s'|s,a) · [ R + γ·V(s') ]
```

"In-place / asynchronous" means: **as soon as you update a state, use the new
value for the next state in the sweep.** This is where people lose marks — they
keep using the old numbers. Follow the exact order the question gives.

**Worked — Sep 2026 Q2.** γ = 0.9, start V(L)=0, V(M)=4, V(H)=8, order **H, M, L**.

**State H:**
- `Cl`: 0.7(5 + 0.9×8) + 0.3(5 + 0.9×4) = 0.7(12.2) + 0.3(8.6) = 8.54 + 2.58 = **11.12**
- `Do`: 1.0(−1 + 0.9×8) = **6.2**
- → **V(H) = 11.12, greedy = Cl**

**State M** — now use the **new** V(H) = 11.12:
- `Cl`: 0.6(3 + 0.9×4) + 0.4(3 + 0.9×0) = 0.6(6.6) + 0.4(3) = 3.96 + 1.2 = **5.16**
- `Do`: 1.0(1 + 0.9×**11.12**) = 1 + 10.008 = **11.008**
- → **V(M) = 11.008, greedy = Do**

**State L** — now use the **new** V(M) = 11.008:
- `Cl`: 1.0(−3 + 0.9×0) = **−3.0**
- `Do`: 1.0(1 + 0.9×**11.008**) = 1 + 9.9072 = **10.9072**
- → **V(L) = 10.9072, greedy = Do**

| State | V after sweep | Greedy action |
|-------|---------------|---------------|
| H | 11.12 | Cl |
| M | 11.008 | Do |
| L | 10.9072 | Do |

**The γ question (2026 Q2c).** Recompute Q(M,·) with the **original** values,
γ = 0.2:
- `Q(M,Cl)` = 0.6(3 + 0.2×4) + 0.4(3 + 0.2×0) = 2.28 + 1.2 = **3.48**
- `Q(M,Do)` = 1.0(1 + 0.2×8) = **2.6**
- → greedy flips to **Cl**. (At γ = 0.9 it was Do: 5.16 vs 8.2.)

**Why:** `Do` pays a small immediate reward (+1) but leads to the high-value
state H. `Cl` pays +3 now. A low γ crushes the future term, so the bigger
immediate reward wins. **Low γ = myopic.**

**VI vs PI (asked in general terms):** each VI sweep is cheap (one max, no
solving), but it only propagates value one step per sweep, so it needs many
sweeps. PI does a full (expensive) policy evaluation each round and so converges
in very few rounds. **Prefer VI when the state space is large** — you can't
afford to solve the full linear system for evaluation, and VI can be stopped
early once the greedy policy stops changing.

---

## Recipe 3 — Monte Carlo IS, TD(0), and the three control updates

This slot is worth the most marks. Do it twice.

### 3a. Off-policy MC with importance sampling

**Why IS is needed:** the episodes were generated by the *behaviour* policy `b`,
but you want the value under the *target* policy `π`. The returns are drawn from
the wrong distribution, so you reweight them.

**Coverage condition:** `b(a|s) > 0` wherever `π(a|s) > 0`. (If π can take an
action that b never takes, you have no data for it and the estimate is invalid.)

**Formula:**

```
ρ = Π over the episode of  π(a_t | s_t) / b(a_t | s_t)
G = discounted return from the state you're evaluating

Ordinary IS:   V(s) = ( Σ ρ_i · G_i ) / N            ← divide by number of episodes
Weighted IS:   V(s) = ( Σ ρ_i · G_i ) / ( Σ ρ_i )    ← divide by the sum of ratios
```

**Worked — Sep 2026 Q3.** γ = 0.9.

E1 = ⟨s₁,a₁,2, s₂,a₁,5, s_T⟩:
- `G₁ = 2 + 0.9×5 = 6.5`
- `ρ₁ = (0.7/0.5) × (0.6/0.4) = 1.4 × 1.5 = 2.1`

E2 = ⟨s₁,a₂,1, s_T⟩:
- `G₂ = 1`
- `ρ₂ = 0.3/0.5 = 0.6`

- **Ordinary:** (2.1×6.5 + 0.6×1) / 2 = 14.25 / 2 = **7.125**
- **Weighted:** 14.25 / (2.1 + 0.6) = 14.25 / 2.7 = **5.2778**

**Higher variance → ordinary IS.** The ratios are unbounded, so one episode with
a huge ρ swings the estimate. Ordinary is *unbiased but high variance*; weighted
is *biased but far lower variance* (and the bias vanishes as episodes grow).

### 3b. TD(0) prediction

```
V(S) ← V(S) + α [ R + γ·V(S') − V(S) ]
```

Sep 2026: V(s₁)=5, R=3, V(s₂)=4, α=0.3, γ=0.9.
`V(s₁) = 5 + 0.3(3 + 0.9×4 − 5) = 5 + 0.3(1.6) = ` **5.48**

### 3c. Q-learning vs SARSA vs Expected SARSA

All three are `Q ← Q + α[ target − Q ]`. **Only the target differs:**

| Method | Target | Uses |
|--------|--------|------|
| **Q-learning** (off-policy) | `R + γ·max_a Q(S',a)` | the **best** next action |
| **SARSA** (on-policy) | `R + γ·Q(S',A')` | the next action **actually taken** |
| **Expected SARSA** | `R + γ·Σ_a π(a\|S')·Q(S',a)` | the **average** under the policy |

**Worked — Sep 2026 Q3d.** Q(s₁,a₁)=2.0, R=3, α=0.5, γ=0.9.
Next state s₂: Q(s₂,a₁)=4.0, Q(s₂,a₂)=1.0. Behaviour picks **a₂**. ε-greedy, ε=0.2, 2 actions.

- **Q-learning:** target = 3 + 0.9×max(4,1) = 6.6 → `2 + 0.5(6.6−2)` = **4.3**
- **SARSA:** target = 3 + 0.9×Q(s₂,a₂) = 3 + 0.9×1 = 3.9 → `2 + 0.5(3.9−2)` = **2.95**
- **Expected SARSA:** ε-greedy probabilities with 2 actions, greedy is a₁:
  - `π(a₁) = 1 − ε + ε/2 = 0.8 + 0.1 = 0.9`
  - `π(a₂) = ε/2 = 0.1`
  - `E[Q] = 0.9×4 + 0.1×1 = 3.7` → target = 3 + 0.9×3.7 = 6.33 → `2 + 0.5(6.33−2)` = **4.165**

**Ranking: Q-learning (4.3) > Expected SARSA (4.165) > SARSA (2.95).**

**Why Expected SARSA sits in the middle:** Q-learning takes the *maximum*, the
most optimistic possible value. SARSA takes the *single sampled* action, which
here happened to be the bad one (a₂), so it's pessimistic and noisy. Expected
SARSA averages over the policy — it puts most weight (0.9) on the greedy action
so it lands near Q-learning, but the ε-weight on a₂ pulls it slightly below.
Same expected behaviour as SARSA, **without the sampling variance**.

**ε-greedy probabilities** (needed constantly — write on your sheet):
```
greedy action:      1 − ε + ε/|A|
each other action:  ε/|A|
```

**Maximisation bias** (asked in Compre 24-24): Q-learning's `max` over noisy
estimates systematically overestimates — if any action's estimate is randomly
too high, `max` picks exactly that one. Fix: **Double Q-learning** (one network
picks the action, the other evaluates it).

---

## Recipe 4 — Linear function approximation, semi-gradient TD(0)

**Formulas:**

```
v̂(s,w) = wᵀφ(s)                    ← just a dot product
δ = R + γ·v̂(s',w) − v̂(s,w)          ← TD error
w ← w + α·δ·φ(s)                    ← note: φ(s), NOT φ(s')
```

That last line is the whole reason it's called **semi**-gradient: you treat the
target `R + γv̂(s')` as a constant and don't differentiate through it.

**Worked — Sep 2026 Q4.** φ(s)=[1,2,0], φ(s')=[1,0,1], w=[0.1,0.3,0.2], R=3, γ=0.9, α=0.1.

1. `v̂(s) = 0.1(1) + 0.3(2) + 0.2(0) = ` **0.7**
2. `v̂(s') = 0.1(1) + 0.3(0) + 0.2(1) = ` **0.3**
3. `δ = 3 + 0.9(0.3) − 0.7 = 3 + 0.27 − 0.7 = ` **2.57**
4. `w' = [0.1,0.3,0.2] + 0.1(2.57)[1,2,0]`
   = `[0.1 + 0.257, 0.3 + 0.514, 0.2 + 0]` = **[0.357, 0.814, 0.2]**

Note the third weight **doesn't move** — because φ(s)₃ = 0. Say that out loud in
the answer; it shows you know it's φ(s) driving the update.

**Why function approximation (1 mark, always asked):**
1. The state space is too large (or continuous) to store one entry per state.
2. It **generalises** — states with similar features share learning, so you can
   value a learner/state you have never seen before.

**DQN stabilisation (2 marks, always asked):**
1. **Experience replay** — store transitions, sample random minibatches.
   Breaks the strong correlation between consecutive samples and stops the
   network forgetting old experience.
2. **Target network** — a frozen copy used to compute the target, synced every N
   steps. Without it the target moves every time you update, and you're chasing
   a moving goalpost → divergence.
   (Spare: reward clipping; Double DQN for maximisation bias.)

**Actor-critic design (2 marks, 2026 Q4d — continuous drone control):**
- **Actor** outputs the **action** itself: for thrust ∈ [0,1] and tilt ∈
  [−30°,+30°], output the **mean (and standard deviation) of a Gaussian for each
  of the two continuous dimensions** — squashed into range with a tanh/sigmoid.
- **Critic** outputs a **single scalar**, V(s) (or Q(s,a)), used to compute the
  TD error that criticises the actor.
- **Stochastic Gaussian, not categorical.** The actions are real-valued;
  discretising into categories loses precision and blows up combinatorially
  across two dimensions. A Gaussian policy also gives built-in exploration,
  which matters in gusty (stochastic) wind. (A deterministic policy — DDPG/TD3 —
  is a defensible answer too if you say you'd add exploration noise.)

**REINFORCE baseline (asked in Compre 24-24):** without a baseline, the update is
`∇logπ · G`. If all returns are positive, *every* action gets pushed up, just by
differing amounts — so learning is slow and high-variance. Subtracting a
baseline b(s) (usually V(s)) gives the **advantage** `G − V(s)`, which is
negative for below-average actions and genuinely pushes them down. **Lower
variance, same expected gradient, unbiased.**

**Policy-based preferable over value-based when:** actions are continuous;
you need a stochastic policy (partial observability, or a game where being
predictable loses); or the policy is simpler to represent than the value
function.

---

## Recipe 5 — MCTS, AlphaGo, and imitation learning

### 5a. MCTS tree policy (same UCB formula as Recipe 1)

```
score(child i) = X̄ᵢ + c · sqrt( ln N / nᵢ )
```
`N` = visits to the **parent/root**, `nᵢ` = visits to that **child**.

**Worked — Sep 2026 Q5.** N = 6, c = 1. `ln 6 = 1.7918`.

| Child | X̄ | n | bonus | score |
|-------|-----|---|-------|-------|
| C1 | 5.0 | 3 | 0.7728 | 5.7728 |
| C2 | 4.5 | 2 | 0.9465 | 5.4465 |
| C3 | 4.7 | 1 | 1.3386 | **6.0386** ← selected |

**With c = 0** the bonus vanishes → pure exploitation → **C1** (highest mean, 5.0).

**What the contrast shows:** the exploration term protects a node that has only
been sampled once from being written off on the strength of a single rollout.
C3's mean is based on one simulation and could easily be wrong; the bonus buys
it another look. As nᵢ grows the bonus shrinks and the mean takes over.

**Backup rule** (asked in Compre 24-24): mean = total return / visit count. Add a
rollout of value 8 to a node with mean 4 and n=1 → new mean `(4 + 8)/2 = 6`, n=2.

**The four MCTS phases:** Selection (UCB down the tree) → Expansion (add a child)
→ Simulation (random rollout to terminal) → Backpropagation (update means up the path).

### 5b. AlphaGo

- **Policy network** — proposes a short list of promising moves, so the search
  doesn't branch over all ~250 legal moves. It **narrows the breadth**.
- **Value network** — estimates who's winning at a leaf, so you don't have to
  roll out all the way to the end of the game. It **cuts the depth**.
- **AlphaGo Zero's self-play targets** — this is the bit people miss:
  - the **policy target** is the MCTS **visit-count distribution** at the root
    (search is better than the raw network, so the network is trained to imitate
    its own search);
  - the **value target** is the **actual winner of that self-play game** (+1/−1).
- **Why supervised learning first (in original AlphaGo):** expert human games give
  a strong starting policy immediately; learning from random play would take
  impossibly long. Its shortcoming — it can only ever match humans, and it never
  sees states off the expert distribution — is mitigated by **self-play RL and
  MCTS**, which generate fresh data beyond the human dataset.

### 5c. Behaviour cloning, compounding error, and DAGGER

This is 3 marks and it's a *story*, not a calculation. Learn the chain:

**Why the error compounds (step by step):**
1. Behaviour cloning is plain supervised learning on expert states only. It is
   only accurate **on the distribution it was trained on** — the centre of the aisle.
2. A perturbation puts the robot slightly off-centre — a state the expert
   **rarely visited**, so the policy has almost no training signal there.
3. It outputs a poor action, which moves the robot **further** off-distribution.
4. That new state is even less represented in the data → an even worse action.
5. Errors **feed their own input distribution**, so the deviation grows instead
   of shrinking. (Nothing in the training objective rewards *returning* to the
   centre — the expert never had to, so no such example exists.)

**How DAGGER fixes it (iterative data aggregation):**
1. Run the **current learned policy** in the real environment — deliberately
   letting it drift into the states it actually visits, including near the shelf.
2. Send those visited states to the **expert** and ask "what would you do here?"
3. **Aggregate** the new (state, expert action) pairs into the dataset — you
   never throw away old data.
4. Retrain on the union, and repeat.

The training distribution converges to the **learner's own** state distribution,
so recovery behaviour ("you've drifted right, steer left") finally enters the
dataset. The drift stays bounded because every new failure mode becomes training
data on the next round.

**Inverse RL (one-liner, asked in Compre 24-24):** don't copy the actions —
infer the **reward function** that makes the expert's demonstrations look
optimal, then run normal RL on it. Driving: from watching a good driver you
recover "smooth acceleration good, tailgating bad, lane centre good", and that
reward generalises to roads the demonstrator never drove.

---

## The one-liners that keep reappearing

Read this block once before you sleep and once in the morning.

- **On-policy vs off-policy (SARSA vs Q-learning), navigation example:** a robot
  on a cliff edge. **SARSA** learns the value of the policy it is actually
  following *including its ε-random mistakes*, so it learns to walk the **safe
  route away from the cliff**. **Q-learning** learns the optimal greedy policy
  assuming no mistakes, so it hugs the **cliff edge** — and falls off during
  training whenever exploration fires.
- **Model-based vs model-free:** model-based knows/learns P and R, can plan
  ahead and is sample-efficient (use when real interaction is expensive or
  dangerous). Model-free learns from experience only, simpler and doesn't
  suffer model bias (use when a simulator is cheap or the dynamics are too
  complicated to model).
- **MC vs TD:** MC needs complete episodes, no bootstrapping, unbiased but high
  variance. TD updates every step, bootstraps, biased but low variance, works on
  continuing tasks.
- **MDP / POMDP / CMDP:** fully observable state → MDP (value/policy iteration,
  Q-learning). State only partially observable, agent sees an observation →
  POMDP (belief states, recurrent policies). MDP with extra cost constraints to
  satisfy → CMDP (constrained/Lagrangian policy optimisation).
- **Exploration strategies table:** ε-greedy (random with prob ε — simple,
  explores blindly), UCB (bonus for uncertainty — explores what it knows least),
  softmax/Boltzmann (probability proportional to value — explores in proportion
  to promise).
- **γ:** near 0 myopic, near 1 far-sighted. Constant reward R forever → `G = R/(1−γ)`.

---

## Exam-hall rules

1. **Do the numericals first.** They're deterministic marks. The theory parts
   you can reason out under time pressure; a value-iteration sweep you cannot.
2. **Show every substitution.** Every one of these papers says "show the
   numerical computation clearly." Method marks are real — write the formula,
   then the numbers in it, then the result.
3. **"Justify w.r.t. the given use case."** The Sep 2026 paper says vague answers
   are penalised. Never write "it reduces variance" — write "it reduces variance
   *in the patient-satisfaction estimate*, because...". Name the objects in
   their story.
4. **In-place value iteration: use the updated numbers.** The single most common
   way to lose 3 marks.
5. **Semi-gradient update uses φ(s), not φ(s').** Second most common.

---

## The lookup map

You may only carry the **watermarked** material. So the question stops being
"what do I remember?" and becomes **"how fast can I find it?"**

I searched every course PDF for all 23 things this exam asks about.
**`AIMLCZG512 - DRL - Lecture notes.pdf` was the only file that contained all
of them.** Everything on this sheet is in that one document. Nothing has to be
memorised from scratch — but you do have to be able to *land on the page*.

> **Page numbering:** the number printed in the page header is **2 less** than
> the PDF page number. The map below gives you **both**. If you have it printed,
> use the "printed" column; if it's a PDF on screen, use the "PDF" column.

### The five pages that matter

Rehearse these five. This is the whole list.

| Recipe | Topic | Printed p. | PDF p. |
|--------|-------|-----------|--------|
| **1** | Bandits — UCB, incremental update, constant α | **19–24** | 21–26 |
| **2** | Dynamic Programming — Value & Policy Iteration | **45–51** | 47–53 |
| **3** | Off-policy MC + TD control (Q-learning/SARSA) | **65–90** | 67–92 |
| **4** | Approximation, semi-gradient, DQN | **93–115** | 95–117 |
| **5** | MCTS, AlphaGo, imitation/DAGGER | **155–171** | 157–173 |

If you remember nothing else: **20, 48, 84, 105, 158.** Those five printed page
numbers put you within a page of every formula you need.

### Full index

| What you need | Printed p. | PDF p. |
|---------------|-----------|--------|
| UCB formula | 19–24 | 21–26 |
| Incremental / sample-average update | 9–18 | 11–20 |
| Constant step-size, non-stationary | 15–24 | 17–26 |
| Contextual bandits | 15–24 | 17–26 |
| Bellman optimality equation | 25–45 | 27–47 |
| Value Iteration | 45–51 | 47–53 |
| Policy Iteration | 43–51 | 45–53 |
| Importance sampling (ordinary) | 62–76 | 64–78 |
| **Weighted** importance sampling | 65–76 | 67–78 |
| TD(0) prediction | 78–90 | 80–92 |
| Q-learning | 83–90 | 85–92 |
| SARSA | 83–90 | 85–92 |
| Expected SARSA | 83–90 | 85–92 |
| Maximisation bias / Double Q | 86–90 | 88–92 |
| Semi-gradient TD(0) | 91–105 | 93–107 |
| DQN — replay & target network | 102–115 | 104–117 |
| Actor-critic | 21–49, 177 | 23–51, 179 |
| MCTS | 153–164 | 155–166 |
| AlphaGo / AlphaZero | 153–165 | 155–167 |
| Behaviour cloning / imitation | 166–180 | 168–182 |
| DAGGER | 166–187 | 168–189 |
| Inverse RL | 169–187 | 171–189 |

### The course contents page

The notes have a printed contents list on **page 1**. Turning to it is often
faster than remembering a number:

| Lecture | Topic | Printed p. |
|---------|-------|-----------|
| 1 | Introduction to RL | 1 |
| 2–3 | Multi-armed Bandits | 9, 15 |
| 4 | Finite MDPs | 25 |
| 5–6 | **Dynamic Programming** | 39 |
| 7 | Monte Carlo — On-Policy | 53 |
| 8 | **Off-Policy Monte Carlo** | 65 |
| 9 | **Temporal-Difference Learning** | 78 |
| 10 | On-Policy Prediction with Approximation | 91 |
| 11 | **Deep Q-Networks** | 106 |
| 12–13 | Policy Gradient Methods | 125 |
| 14 | **Model-Based Planning: MCTS, AlphaZero** | 153 |
| 15 | Selected Topics | 166 |
| 16 | Course Review and Summary | 179 |

**Lecture 16 (p. 179) is a course review/summary** — if you're stuck on a
one-mark definition, look there first. It's the densest page-per-mark in the
whole document.

### Where the other decks help

Only if the notes fail you — the decks have more worked examples:

- **Deck 5, "Race car"** — the single best source of *worked* DP / MC / TD
  examples (value iteration p. 8–15, policy iteration p. 19–25, SARSA p. 75–79,
  Expected SARSA p. 80–86). If you need to see a calculation done, go here.
- **Deck 4, Temporal Difference** — Expected SARSA p. 37, maximisation bias p. 38.
- **Deck 6, Value Approximation** — DQN p. 45–57.
- **Deck 9, Imitation Learning** — DAGGER p. 20–31.

### If you are allowed to write on the watermarked notes

Many open-book rules permit annotating the permitted material. **Check yours.**
If it's allowed, this is the highest-value 15 minutes you will spend tonight:
copy onto the inside cover of the printed notes —

```
UCB:      Q(a) + c·sqrt(ln t / N(a))
Update:   Q ← Q + α(R − Q)          [α=1/N → sample average]
VI:       V(s) ← max_a Σ P·[R + γV(s')]      IN-PLACE: use new values
IS:       ρ = Π π/b    ord = ΣρG/N    wtd = ΣρG/Σρ
TD(0):    V ← V + α[R + γV(s') − V]
Q-learn:  target R + γ·max Q(s',·)    SARSA: R + γQ(s',a')
ExpSARSA: R + γ·Σ π(a|s')Q(s',a)      ε-greedy: 1−ε+ε/|A| , ε/|A|
Semi-grad: δ = R + γŵᵀφ(s') − wᵀφ(s) ;  w ← w + αδ·φ(s)   [φ(s)!]
MCTS:     X̄ᵢ + c·sqrt(ln N / nᵢ)
```

That block is nine lines and covers every numerical mark on the paper.
