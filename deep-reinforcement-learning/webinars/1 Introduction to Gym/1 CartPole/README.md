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

## Why does the rule-based policy work, but random doesn't?

This is the most important idea in the whole notebook, so let's go slow.

### The physics first
A pole balanced upright is **unstable**. The moment it leans even slightly, gravity
pulls it further in that direction — and it accelerates. To stop it falling, you must
move the cart **underneath** the pole, in the **same direction it's leaning**. (Same as
balancing a broom on your hand: when it tips right, your hand chases it to the right.)

So there is a *correct* action at every moment, and it depends entirely on **which way
the pole is currently leaning** — that's the `pole_angle` number in the observation.

### Why the RANDOM policy fails
```python
def random_policy(env):
    return env.action_space.sample()   # 0 or 1, chosen by coin flip
```
- It **never looks at `pole_angle`**. It throws away the one piece of information that matters.
- It picks left/right by coin flip, so it's correct only ~50% of the time — like balancing
  a broom with your eyes closed.
- Because the pole is unstable, a few wrong pushes in a row are enough to tip it past the
  point of no return. Random can't *recover*, because it isn't even *trying* to correct.
- Result: episodes end in ~10–30 steps. Average reward stays low.

### Why the RULE-BASED policy works
```python
def smarter_policy(obs):
    cart_pos, cart_vel, pole_angle, pole_ang_vel = obs
    if np.random.rand() < 0.1:           # 10% explore (small randomness)
        return env.action_space.sample()
    return 1 if pole_angle > 0 else 0    # lean right -> push right(1); lean left -> push left(0)
```
- It **reads `pole_angle`** and acts on it. This is the whole difference.
- `pole_angle > 0` means the pole leans right → it returns action `1` (push right) to slide
  the cart back under the pole. If it leans left, it pushes left. So it **actively corrects**.
- This creates a **feedback loop**: lean → correct → lean the other way → correct again.
  The pole wobbles but stays up much longer (often 50–200 steps).
- The 10% randomness is just to make the motion visible/explore a bit; the other 90% is the
  smart rule doing the real work.

### The one-sentence takeaway
> **Random ignores the state; the rule-based policy uses the state (`pole_angle`) to push
> the cart in the direction that counteracts the fall.** Using information beats ignoring it.

### So why don't we always just write rules?
The rule above is simple because CartPole is simple. For hard problems (a robot arm, a game
of Go, self-driving), nobody can hand-write the correct rule for every situation. That's the
whole reason **reinforcement learning** exists: instead of *us* writing the rule, the agent
**learns the rule by itself** from trial-and-error and reward. That's the next stage of the
course (after Markov Decision Processes), and it's what makes the pole eventually look like
it "balances itself."

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
