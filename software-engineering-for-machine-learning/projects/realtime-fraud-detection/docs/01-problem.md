# 1. The Problem

## The situation

A payment company sits in the middle of every card tap, every online checkout,
every transfer. Money moves through it constantly.

A small slice of that money is not moving legitimately. Someone stole a card
number. Someone took over an account. Someone set up a fake merchant to cash out
stolen cards. This is fraud, and it is a permanent, adapting, adversarial
problem — the people committing it change their behaviour specifically because
you are trying to stop them.

## The decision

When a transaction arrives, the system must answer one question:

> **Approve this, or block it?**

Two constraints make it hard:

1. **There is no time.** A card terminal or a checkout page is waiting. If the
   answer takes a second, the customer experience is ruined. Realistically the
   fraud decision gets a slice of a much larger budget — this project targets
   **under 50 milliseconds at the 99th percentile**, meaning 99 out of every 100
   transactions are answered faster than that.

2. **There is no undo.** Once approved, the money has moved. Once blocked, the
   customer has already been embarrassed.

## The cost of being wrong

This is the part most tutorials skip, and it is the most important part.

There are two ways to be wrong, and they cost completely different amounts:

|  | The transaction was actually fine | The transaction was actually fraud |
| --- | --- | --- |
| **We approved it** | Correct. No cost. | **False negative.** The money is gone. Cost = the transaction amount, plus investigation and chargeback fees. |
| **We blocked it** | **False positive.** Cost = the lost sale, a support call, and some chance the customer leaves. | Correct. Fraud prevented. |

Rough numbers a real team would use:

- A missed fraud costs roughly **the full transaction amount** — say ₹8,000 on
  an average fraudulent transaction, plus a fixed ₹500 handling cost.
- A wrongly blocked customer costs perhaps **₹300** — the margin on the lost
  sale, a support contact, and a small chance of losing the customer entirely.

So a missed fraud is roughly **25× more expensive** than a false alarm. That
ratio is the single most important number in the project, because it determines
where the decision threshold goes.

Most machine learning tutorials pick a threshold of 0.5 ("if the model says more
than 50% likely, call it fraud") or optimise something called an F1 score. Both
are wrong here. The correct threshold is the one that minimises:

```
expected cost = (number of missed frauds  × cost of a missed fraud)
              + (number of false alarms   × cost of a false alarm)
```

Because false alarms are cheap relative to missed fraud, the optimal threshold
lands far below 0.5 — the system should be willing to raise a lot of false
alarms to catch one more fraud. **This project computes that threshold from the
cost numbers and shows the curve.**

## The five things that make this an engineering problem, not a modelling problem

### 1. Fraud is rare

Around 1 transaction in 1,000 is fraud. A model that flatly predicts "not fraud"
for everything is 99.9% accurate. Accuracy is therefore a meaningless metric
here, and any project that reports it is signalling that the author has not
thought about the problem. This project reports **precision, recall, and area
under the precision-recall curve**, plus the cost figure above.

### 2. A transaction means nothing on its own

A ₹40,000 purchase is not suspicious. A ₹40,000 purchase from an account whose
largest previous transaction was ₹2,000, made four minutes after a ₹1 test
charge, from a device never seen before — that is suspicious.

The signal lives in the *history*, not the transaction. Which means the system
has to keep a live, constantly-updating summary of every account's recent
behaviour, and be able to fetch it in under a millisecond. That component is the
**online feature store**, and it is the heart of the system.

### 3. The training numbers and the serving numbers must match exactly

This one is subtle and it is where real systems fail silently.

The model is trained on historical data, where it is easy to compute "spend in
the last hour" with a database query. In production, the same number is computed
by a streaming job maintaining a rolling counter in Redis.

If those two computations differ *at all* — a different time window boundary, a
different way of handling missing values, an off-by-one in which transactions
are included — then the model is being fed different numbers than it learned on.
Nothing crashes. No error appears. The model just quietly gets worse.

This is called **train/serve skew**, and detecting it is a core deliverable of
this project.

Closely related: when building the training data, each row must only contain
information that was actually available *at that moment in the past*. If a
feature accidentally includes information from after the transaction, the model
looks brilliant in testing and fails immediately in production. This is called
**leakage**, and avoiding it requires **point-in-time correct** feature
construction.

### 4. The truth arrives weeks late

We do not learn that a transaction was fraud when it happens. We learn it when
the cardholder notices the charge on their statement and disputes it — typically
**30 to 60 days later**.

This breaks the normal machine learning loop completely:

- You cannot measure today's model performance today. You are always measuring
  a model as it was two months ago.
- Recent data has fewer confirmed frauds simply because the complaints have not
  arrived yet, not because fraud went down. A naive retraining job will read
  that as "fraud is decreasing" and get worse.
- Retraining must therefore only use data old enough to have settled.

The system models this delay explicitly rather than pretending labels are
instant.

### 5. The world changes underneath you

Two separate things drift apart over time:

- **Data drift** — the incoming transactions start to look different. A new
  country goes live, a new payment method launches, a festival season doubles
  the average basket size.
- **Concept drift** — the transactions look the same but the *meaning* changed.
  Fraudsters discovered that transactions under ₹5,000 are not being checked, so
  they all moved below ₹5,000. Nothing about the data distribution screams, but
  the model's logic is now obsolete.

A deployed model is a perishable good. The system needs to notice the smell
before the customers do, which is why monitoring and scheduled retraining are
first-class parts of this project rather than an afterthought.

## What "done" looks like

The project is finished when all of the following are true and demonstrable:

- [ ] A live stream of transactions is being scored end to end.
- [ ] The 99th-percentile response time is under 50 ms under realistic load.
- [ ] The decision threshold is derived from the cost model, with the curve shown.
- [ ] Training data is provably point-in-time correct, with a test that fails
      if leakage is introduced.
- [ ] Train/serve skew is measured and reported, not assumed to be zero.
- [ ] Labels arrive on a delay, and retraining respects that delay.
- [ ] A new model can only reach production by beating the current one on a
      scripted evaluation.
- [ ] A single command rolls back to the previous model.
- [ ] Dashboards show traffic, latency, score distribution and feature drift.
- [ ] At least three real incidents are written up in `docs/incidents/`.

---

Next: [2. How It Works](02-how-it-works.md)
