"""M1/M2 · Where the data comes from.

DeliverEase is a food-delivery app. We predict **delivery time in minutes** for each order.
Real data would come from the orders database; here we generate realistic fake orders so everything runs offline.

`monsoon=True` makes the world change, in two different ways:
- **Data drift** (inputs change): more rain, longer detours, busier kitchens. Visible in the features.
- **Concept drift** (the input -> output rule changes): waterlogged roads add minutes that NO feature explains,
  and rain hurts more than it used to. Same inputs, slower deliveries. Only visible once real times arrive.
"""
import numpy as np
import pandas as pd

FEATURES = ["distance_km", "hour", "items", "prep_min", "is_raining"]
TARGET = "delivery_min"


def make_orders(n: int = 2000, seed: int = 0, monsoon: bool = False) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    distance = rng.gamma(shape=2.0, scale=2.0, size=n).clip(0.3, 20)          # km, most orders are short
    hour = rng.choice(np.arange(10, 24), size=n)                               # 10:00 to 23:00
    items = rng.integers(1, 8, size=n)
    prep = rng.normal(12, 4, size=n).clip(3, 40)                               # kitchen minutes
    rain_p = 0.6 if monsoon else 0.05
    raining = (rng.random(n) < rain_p).astype(int)
    if monsoon:                                                                # the world changed
        distance = distance * 1.3                                              # detours around flooded roads
        prep = prep + 4                                                        # kitchens overloaded

    peak = np.isin(hour, [13, 14, 20, 21]).astype(int)
    rain_cost = 15 if monsoon else 9                                           # concept drift: rain hurts more
    hidden_slowdown = 6 if monsoon else 0                                      # concept drift: no feature explains it
    minutes = (8 + 3.2 * distance + 0.9 * prep + 1.1 * items + 6 * peak
               + rain_cost * raining + hidden_slowdown + rng.normal(0, 3, size=n))
    return pd.DataFrame({
        "distance_km": distance.round(2), "hour": hour, "items": items,
        "prep_min": prep.round(1), "is_raining": raining, TARGET: minutes.round(1),
    })
