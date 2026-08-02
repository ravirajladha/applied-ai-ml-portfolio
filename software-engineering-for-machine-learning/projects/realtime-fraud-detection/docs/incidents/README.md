# Incidents

Write-ups of things that broke.

Some of these will be genuine accidents found while building. Others will be
faults injected on purpose during Milestone 5 to prove the monitoring actually
catches them. Both are worth recording, and each write-up says which it was.

## Why this folder exists

Almost every portfolio project presents a system that has never failed. Real
systems fail constantly, and the interesting engineering is in how failure is
detected, diagnosed and prevented from recurring. A folder of honest postmortems
says more about how someone works than a green test badge does.

It is also the most useful interview preparation available. "Tell me about a
time something broke in production" is a certainty, and these are the answers.

## Format

One file per incident, named `NNNN-short-description.md`.

```markdown
# INC-NNNN — Short description

**Date:** YYYY-MM-DD
**Type:** discovered | injected deliberately
**Severity:** how bad it would have been in production
**Detected by:** what actually surfaced it — an alert, a test, or by accident

## What happened
Plain description of the symptom, in the order it was observed.

## Timeline
Times and what was known at each point. Include the wrong theories — the
detours are the useful part.

## Root cause
What was actually wrong. Keep going until the answer explains the symptom
completely; the first plausible cause is usually not the real one.

## Why it was not caught earlier
The gap in tests, validation or monitoring that let it through.

## Fix
What was changed.

## Prevention
The test, schema rule or alert added so this class of problem fails loudly next
time. If nothing was added, say so and explain why.
```

## Candidates already anticipated

Faults worth injecting during M5, chosen because each fails in a different way:

- **Unit change** — an upstream field starts arriving in paise instead of
  rupees. Every amount is 100× larger. Should be caught by the pandera schema
  range check, and if not, by feature drift.
- **Stale features** — the feature builder consumer dies but the scoring API
  keeps serving. Redis returns increasingly old values and nothing errors. Should
  be caught by a feature-freshness metric, which is easy to forget to build.
- **Null flood** — a field starts arriving null 40% of the time. LightGBM
  handles nulls natively, so the model degrades silently rather than crashing.
  Should be caught by a null-rate alert.
- **Silent leakage** — a feature is added that accidentally sees the future.
  Offline evaluation looks excellent, live performance does not match. Should be
  caught by the leakage test, and this is the best demonstration of why that
  test exists.
- **Schema drift on retrain** — a column is renamed upstream, the retrain
  succeeds on differently-ordered features, and the promotion gate is the last
  line of defence.

*No incidents recorded yet — the system does not exist. First entries expected
during M1 and M2.*
