# MDP Practice — Value Iteration (Build Guide)

**Date:** 2026-07-01
**Files in this topic folder:**
- `explainer.html` — interactive, click-to-learn visual explanation (open this first!)
- `practice.ipynb` — the template notebook you fill in
- `guide.md` — this cell-by-cell build guide
**Goal:** Learn Markov Decision Processes by building a value-iteration solver for Frozen Lake **cell by cell.**

This is the *basic version*: the problem statement and an empty scaffold. We fill in the code together, one cell at a time.

---

## How we'll work (cell by cell)

For each cell below we follow the same loop:

1. **Read the concept** for that cell in plain English.
2. **You write** the code (the notebook has `# TODO` blanks for the important lines).
3. **You run it** and check the output (or any error).
4. **Verify** it and move to the next cell.

> Rule for today: don't jump to the finished answer up front. Try each `# TODO` first, then check. That's how it sticks.

---

## The problem

Frozen Lake, deterministic 4×4 grid. Start top-left `S`, reach goal `G` bottom-right, avoid holes `H`.

```
S F F F
F H F H
F F F H
H F F G
```

Reward: **+1** for reaching `G`, **0** everywhere else. Non-slippery, so moves are deterministic.

## The MDP in one table — **(S, A, P, R, γ)**

| Symbol | Name | In Frozen Lake |
|--------|------|----------------|
| **S** | States | 16 tiles (0–15) |
| **A** | Actions | 0=Left, 1=Down, 2=Right, 3=Up |
| **P** | Transitions | `env.unwrapped.P[s][a]` |
| **R** | Reward | +1 at goal, else 0 |
| **γ** | Discount | 0.9 |

---

## Build plan — the cells

- [ ] **Cell 0 — Setup.** Import `gymnasium`, create the env, print state/action counts. *(done for you)*
- [ ] **Cell 1 — Inspect `env.P`.** Read the `(prob, next_state, reward, done)` tuples. *(done for you)*
- [ ] **Cell 2 — `value_iteration()`.** ✏️ Fill in the Bellman update:
  `V(s) ← max over actions of  Σ prob · (reward + γ · V(next_state))`
- [ ] **Cell 3 — `extract_policy()`.** ✏️ Same Q-value idea, but keep the best *action* (`argmax`) instead of the best *value* (`max`).
- [ ] **Cell 4 — Run.** Print the value table and the policy as 4×4 grids.
- [ ] **Cell 5 — Check + stretch goals.** Verify values grow toward the goal; try `gamma` changes and the slippery version.

---

## Key idea to hold onto

The **Bellman optimality equation** is the whole game:

```
V(s) = max over actions a of:  sum over outcomes of  prob * (reward + gamma * V(next_state))
```

Everything in Cell 2 and Cell 3 is just this one line, read straight from `env.P`.

## Progress log

Use this to track what we finished together:

- [ ] Understood `env.P` output
- [ ] `value_iteration` runs without error
- [ ] Values increase toward the goal
- [ ] `extract_policy` produces a goal-directed policy
- [ ] Tried a stretch goal
