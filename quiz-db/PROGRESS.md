# Quiz bank progress

Read this first in every quiz-creation session. Update it at the end.

## Round 2: deepen every subject (started 15-Nov-2026)

Target: 120-160 questions per subject, with more L3/L4, informative explanations and a real ML-code topic per subject.

| Rung | Subject | Round 1 | Round 2 | Status |
|------|---------|---------|---------|--------|
| Foundations | py-basics | 73 | 148 | done, pushed |
| Foundations | py-variables | 78 | 155 | done, pushed |
| Foundations | py-strings | 87 | 153 | done, pushed |
| Foundations | py-lists | 80 | 158 | done, pushed |
| Foundations | py-dicts | 70 | 146 | done, pushed |
| Foundations | py-conditions | 71 | 151 | done, pushed |
| Foundations | py-loops | 73 | 149 | done, pushed |
| Foundations | py-functions | 67 | 150 | done, pushed |
| Foundations | py-comprehensions | 61 | 136 | done, pushed |
| Foundations | py-errors | 104 | 167 | done, pushed |
| Foundations | py-classes | 108 | 192 | done, pushed |
| Foundations | np-arrays, np-operations | 139, 153 | 203, 215 | done, pushed |
| Foundations | pd-dataframes, pd-cleaning | 151, 163 | 194, 208 | done, pushed |
| Foundations | **plotting** | 99 | — | **next** (L4 only 13: add L3/L4) |
| L1 | ml-what | 69 | 126 | done, pushed |
| L1 | ml-types | 65 | 122 | done, pushed |
| L1 | ml-data | 72 | 159 | done, pushed |
| L1 | ml-splits | 90 | 160 | done, pushed |
| L1 | ml-overfitting | 76 | 130 | done, pushed |
| L1 | ml-metrics | 94 | 148 | done, pushed |
| L1 | ml-models | 88 | 157 | done, pushed |
| L2 | dl-neuron, dl-loss-gd | 77, 76 | 132, 128 | done, pushed |
| L2 | dl-training | 85 | 144 | done, pushed |
| L3 | nlp-tokens, nlp-embeddings | 98, 95 | 139, 137 | done, pushed |
| L3 | tf-attention, tf-generation | 86, 83 | 131, 131 | done, pushed |
| L4 | llm-prompting, llm-rag | 65, 65 | 130, 130 | done, pushed |
| L4 | llm-finetuning | 63 | 131 | done, pushed |
| L5 | ops-serving, ops-monitoring | 91, 80 | 134, 137 | done, pushed |

Pushed: commit `71dcb2e` on branch `quiz-db` (5,373 questions). The `aiml_quiz` database is loaded from that commit (16-Nov-2026).

## Known follow-ups
- Writers stall if they write a whole question block in one edit. Tell them to append at most 10 questions per edit.
- New questions in dl-neuron and dl-loss-gd are about 42-45% `out` (target 35%).
- The Python core banks are 55-79% `out` questions (STANDARD.md wants about 35%). Add conceptual mcq/tf questions in a later pass instead of converting existing ones.
- Python 3.12+ `sum()` of floats is compensated: `sum([0.1]*10) == 1.0` is True. Explanations must contrast it with a `+=` loop.
- Course material (llm-engineering, nlp-applications, edge ML, cloud-native) is not in the bank yet. These would be new subjects once the ladder round is done.

## Log
| Date | What happened |
|------|---------------|
| 15-Nov-2026 | Round 1 (earlier): 35 subjects, 3,238 questions, pushed. |
| 15-Nov-2026 | Round 2: Python core and six ML fundamentals subjects deepened, 4,450 questions, pushed `f941be6`. Stopped early to save tokens. ml-models is half-reviewed on disk. |
| 16-Nov-2026 | Round 2: ml-models committed, and all L2-L5 subjects deepened to 128-144 each (5,159 questions). Vendor names removed from tf-generation and nlp-embeddings. Pushed `779e5dd`, DB reloaded. |
| 16-Nov-2026 | NumPy and Pandas subjects deepened with L3/L4 and ML topics (`ml-arrays`, `ml-numpy`, `ml-features`, `windows`). 5,373 questions, pushed `71dcb2e`, DB reloaded. Plotting is next; then course-material subjects. |
