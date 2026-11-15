# Blackjack — Practice Problem

## The problem
Play the card game **Blackjack** against the dealer. Each turn you either:
- **Hit** (`1`) — take another card, or
- **Stick** (`0`) — stop and let the dealer play.

Goal: get your card total as close to **21** as possible **without going over**. Go over → bust → lose.

## The NEW concept: a tuple observation
So far the observation was a list of numbers about *physics*. Here it's a **tuple** describing
a *game state*:

- **Observation** — `(player_sum, dealer_card, usable_ace)`:
  - `player_sum` — your current total (e.g. 18)
  - `dealer_card` — the dealer's one face-up card (1–10)
  - `usable_ace` — `1` if you hold an ace counted as 11, else `0`
- **Action** — `Discrete(2)`: `0` = stick, `1` = hit.
- **Reward** — `+1` win, `-1` lose, `0` draw. Given only at the **end** of the hand.
- **Episode length** — very short (a few cards).

## Learning objectives
- Read a **tuple** observation and unpack it.
- Work with **sparse reward** (you only learn win/lose at the very end).
- See an environment with no "physics" — pure decision-making.

## Your tasks (in `Blackjack_Practice.ipynb`)
- [ ] Create the environment and inspect the tuple observation.
- [ ] Write `random_policy` (random hit/stick) and play many episodes (try 1000).
- [ ] Compute your **win rate** (fraction of episodes with reward `+1`).
- [ ] Write `smarter_policy` using a simple rule and compare win rates.

## Hints (peek only if stuck)
- Unpack the observation: `player_sum, dealer_card, usable_ace = obs`.
- A classic simple rule: **hit while your sum is below 17, otherwise stick.**
  ```python
  return 1 if player_sum < 17 else 0
  ```
- Random wins roughly ~28%. A simple rule should beat that noticeably.
- Because rewards are `+1/-1/0`, track wins with something like
  `wins += 1 if total_reward == 1 else 0`.

## What to try
- Change the threshold (16, 17, 18, 20) and see which wins most.
- Does the dealer's showing card matter? Try a rule that also looks at `dealer_card`.

## Takeaway
This is a true **decision-making** problem with sparse, end-of-game feedback — the
natural setting for reinforcement learning (and a classic RL textbook example).
