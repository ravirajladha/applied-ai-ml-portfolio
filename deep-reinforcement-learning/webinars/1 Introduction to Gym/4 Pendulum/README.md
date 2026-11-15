# Pendulum — Practice Problem

## The problem
A pendulum swings freely from a pivot. You apply torque to **swing it up and hold it
upright** (pointing straight up), then keep it balanced there.

```
   *      <- goal: balance the mass up here
    \
     \
      o   <- pivot (you apply torque here)
```

## The NEW concept: continuous actions
In CartPole/Acrobot/Blackjack the action is a **choice from a list** (0, 1, 2…).
In Pendulum the action is a **continuous number** — any float you like in a range.

- **Action** — `Box(-2.0, 2.0, (1,))`: a single float between `-2` and `+2` (the torque).
  You must return it as a numpy array, e.g. `np.array([0.5])`.
- **Observation** — 3 numbers: `cos(angle)`, `sin(angle)`, `angular velocity`.
- **Reward** — a **negative cost** each step based on how far from upright you are and how
  much torque you used. Closer to upright and gentler = closer to `0` (better).
- **Episode length** — fixed at 200 steps (it never "falls over" and ends early).

## Learning objectives
- Handle a **continuous** action space (a `Box`, not `Discrete`).
- Return actions as numpy arrays.
- Read an angle encoded as `cos`/`sin` instead of a raw number.

## Your tasks (in `Pendulum_Practice.ipynb`)
- [ ] Create the environment; note the action space is a `Box`, not `Discrete`.
- [ ] Write `random_policy` using `env.action_space.sample()` (it returns an array — good).
- [ ] Run 20 episodes and plot the (negative) rewards.
- [ ] Write `smarter_policy` that returns a torque based on the angular velocity.
- [ ] Compare: does your rule get the average reward closer to 0?

## Hints (peek only if stuck)
- Random action already returns the correct array shape: `env.action_space.sample()`.
- A simple damping rule: push *against* the spin to slow it near the top —
  `np.array([-2.0 if obs[2] > 0 else 2.0])`. Then experiment with the strength.
- Because reward is always negative, "better" means **less negative** (closer to 0).

## What to try
- Print `obs` for a few steps. `cos≈1` means near the bottom; `cos≈-1` means near the top.
- Try a constant action like `np.array([0.0])` (no torque) — what happens?

## Takeaway
Many real control problems (motors, robot joints, throttles) are continuous.
A hand rule barely works here — which is exactly why RL is used for real control.
