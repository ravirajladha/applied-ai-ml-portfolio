"""M7 · Testing in production: shadow and canary.

- **Shadow:** the new (candidate) model sees real traffic and its predictions are logged, but users only ever
  get the current model's answer. Zero risk, used to compare.
- **Canary:** a small share of users (say 10%) get the candidate's answer. If its metrics hold, raise the share.

Routing by a hash of the order id (not random) means the same customer always lands on the same model.
"""
import hashlib


def bucket(key: str) -> int:
    """Stable number 0-99 for a key: same key, same bucket, every time."""
    return int(hashlib.sha256(key.encode()).hexdigest(), 16) % 100


class Router:
    def __init__(self, current, candidate=None, canary_percent: int = 0, shadow: bool = False):
        if not 0 <= canary_percent <= 100:
            raise ValueError("canary_percent must be 0-100")
        self.current, self.candidate = current, candidate
        self.canary_percent, self.shadow = canary_percent, shadow
        self.shadow_log: list[dict] = []

    def predict(self, order_id: str, X):
        use_candidate = self.candidate is not None and bucket(order_id) < self.canary_percent
        served_by = "candidate" if use_candidate else "current"
        y = (self.candidate if use_candidate else self.current).predict(X)
        if self.shadow and self.candidate is not None and not use_candidate:
            self.shadow_log.append({"order_id": order_id, "served": float(y[0]),
                                    "shadow": float(self.candidate.predict(X)[0])})
        return y, served_by
