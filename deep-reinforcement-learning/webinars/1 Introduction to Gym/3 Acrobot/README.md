# Acrobot — Practice Problem

## The problem
A **two-link robotic arm** hangs down from a fixed point (like a gymnast hanging from a bar).
You can apply torque at the middle joint. Goal: **swing the free tip up** above a target line.

```
   o  <- fixed pivot
   |
   o  <- middle joint (you apply torque here)
   |
   *  <- free tip (must swing ABOVE the line)
```

Unlike CartPole, a single push isn't enough — you must **pump** back and forth to build
momentum, like a kid on a swing.

## Environment: `Acrobot-v1`
- **Action** — `Discrete(3)`: `0` = torque left, `1` = no torque, `2` = torque right.
- **Observation** — 6 numbers: the angles (as cos/sin) and angular velocities of the two links.
- **Reward** — `-1` for **every** step the tip is *not* high enough. Higher (less negative)
  total = you succeeded faster. Episode ends on success or after 500 steps.

## Learning objectives
- Reuse the Gym loop (`reset → step → repeat`) on a new environment.
- See that the action space can have **more than 2 choices** (here, 3).
- Understand a **negative reward** (penalty per step) vs CartPole's positive reward.

## Your tasks (in `Acrobot_Practice.ipynb`)
- [ ] Create the environment and print its action/observation spaces.
- [ ] Write `random_policy` and run 20 episodes; record total reward.
- [ ] Plot the rewards and compute the average.
- [ ] Write `smarter_policy` that **pumps** to build momentum.
- [ ] Compare random vs smarter. Did the average improve?

## Hints (peek only if stuck)
- Random action: `env.action_space.sample()`.
- Don't expect random to ever reach the top — that's the point.
- For the smarter rule, look at the **angular velocity of the second link** (`obs[5]`):
  push (`0` or `2`) in the *same* direction it's already moving to add energy; otherwise `1`.

## What to try
- Print the observation each step for one episode — which numbers change the most?
- Increase `num_episodes` and watch how rarely random ever wins.

## Takeaway
Some goals can't be reached by reacting to "right now" — you must build up over time.
This is a stepping stone toward why **learned** policies (RL) matter.
