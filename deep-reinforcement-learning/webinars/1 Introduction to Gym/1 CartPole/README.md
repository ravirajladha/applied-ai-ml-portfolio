# CartPole — What Is It and What Does It Do?

## The idea in one line
A pole is hinged on top of a cart. The cart can be pushed **left** or **right**.
The goal: **keep the pole upright for as long as possible** by moving the cart.

It's the classic "balance a broomstick on your palm" problem — but for a computer.

```
        |   <- pole (wants to fall over)
        |
     [=====]   <- cart (we can push it left or right)
   ----------- track
```

## How the environment works (the Gym loop)
CartPole is a **Gymnasium** environment. Every environment speaks the same language:

| Step | Code | Meaning |
|------|------|---------|
| Start | `obs, info = env.reset()` | begin a fresh episode |
| Act   | `obs, reward, terminated, truncated, info = env.step(action)` | push the cart, see what happens |
| Repeat | loop until `terminated or truncated` | keep going until the pole falls or time runs out |

- **Action** — `0` = push left, `1` = push right (`Discrete(2)`).
- **Observation** — 4 numbers: `[cart position, cart velocity, pole angle, pole angular velocity]`.
- **Reward** — `+1` for **every** timestep the pole stays up. Longer balance = higher score (max 500).
- **Episode ends** when the pole tilts too far, the cart leaves the screen, or 500 steps pass.

## "Does it balance itself automatically?"
Not in this notebook — and that's the most important thing to understand. There are **three levels**:

1. **Random policy** (Exercise 1) — pushes left/right at random, ignores the pole.
   ➜ Fails fast. Average reward ~20. *Random is dumb.*
2. **Rule-based policy** (Exercise 2) — "if the pole leans right, push right; else push left."
   ➜ Much better (often 50–200 steps). *We hand-wrote the smarts.*
3. **Learned policy** (later, after Markov Decision Processes + RL algorithms) —
   the agent **figures out the balancing rule by itself** through trial and error.
   ➜ *This* is the "it balances itself automatically" magic. We're not here yet.

So today we learn **how to drive the environment**. Teaching it to balance *itself*
comes after the Markov / reinforcement-learning topics in the course.

## Files in this folder
- `CartPole_Problem.docx` — the original problem statement / lab sheet.
- `CartPole_RandomPolicy_Code.ipynb` — the **blank** lab notebook (fill in the TODOs yourself for practice).
- `CartPole_SOLVED_runnable.ipynb` — the **completed, runnable** version with explanations and a video animation.

## How to run
1. Open **Anaconda Prompt**.
2. ```
   cd "C:\dev\ai-ml\deep-reinforcement-learning\webinars\1 Introduction to Gym\1 CartPole"
   jupyter notebook
   ```
3. Open `CartPole_SOLVED_runnable.ipynb` and run each cell with **Shift+Enter**.

> Requires `gymnasium[classic-control]` (already installed). If on a fresh machine:
> `pip install "gymnasium[classic-control]"`

## What to try (to actually learn it)
- In `smarter_policy`, flip `pole_angle > 0` to `< 0` — watch it get *worse*.
- Change `num_episodes` and see how the average reward plot changes.
- Compare the random vs. smarter policy survival times. Why is one better?

## Key takeaway
The pattern `reset() → step() → repeat` is the foundation of **every** RL environment
you'll use in this course. Master it here on CartPole and the rest get much easier.
