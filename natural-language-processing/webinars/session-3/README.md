# Session 3 — Question & Answer Chat Bots (End-to-End Memory Networks)

Build a small chatbot that reads a short **story**, is asked a **question**, and
answers **yes** or **no**. It does this with an *End-to-End Memory Network* — a
neural network that learns to "look back" at the right part of the story before
answering.

---

## What's in this folder

| File | What it is | Needed to run? |
|------|------------|----------------|
| `02-Chat-Bots.ipynb` | The full, worked solution notebook | ✅ Yes — this is the lab |
| `train_qa.txt` | Training data: 10,000 `(story, question, answer)` tuples, pickled | ✅ Yes |
| `test_qa.txt` | Test data: 1,000 `(story, question, answer)` tuples, pickled | ✅ Yes |
| `Lab2_Slides.pptx` | Lecture slides for the session | Reference (not committed — hosted on Drive) |
| `SYNTHETIC LAB DATASET.docx` | An advanced "where / what" dataset for a stretch exercise (open-vocabulary answers, not just yes/no) | Reference / challenge |
| `End-to-End Memory Networks.pdf` | The original paper the model is based on | Reference (not committed — hosted on Drive) |

> The `.txt` files are **pickled Python lists**, not plain text — open them with
> `pickle.load`, not a text editor.

---

## The data (bAbI dataset from Facebook Research)

Each example is a tuple of three parts:

```python
(['Mary', 'got', 'the', 'milk', 'there', '.', 'John', 'moved', 'to', 'the', 'bedroom', '.'],   # story
 ['Is', 'John', 'in', 'the', 'kitchen', '?'],                                                    # question
 'no')                                                                                            # answer
```

* **Story** — a few short sentences of facts.
* **Question** — a yes/no question about those facts.
* **Answer** — always the single word `yes` or `no`.

Full details: https://research.fb.com/downloads/babi/

---

## The solution — how the notebook works

Plain-English walkthrough of the pipeline in `02-Chat-Bots.ipynb`:

1. **Load the data** — unpickle `train_qa.txt` and `test_qa.txt`.
2. **Build the vocabulary** — collect every unique word across all stories and
   questions (plus `yes`/`no`). This becomes the dictionary the model knows.
3. **Vectorize** — turn each word into an integer ID (a `Tokenizer`), then pad
   every story and question to a fixed length (`pad_sequences`) so they all have
   the same shape. Answers become one-hot vectors over the vocabulary.
4. **Build the Memory Network** (this is the interesting part). It has two
   inputs — the story and the question — and combines them like this:
   * **Encoders** — the story is embedded two ways (`m` and `c`), and the
     question is embedded once (`u`). Embedding = turn each word ID into a dense
     vector that captures meaning.
   * **Attention / match** — take the dot product of the story embedding `m`
     with the question `u`, then `softmax` it. This produces a weight for every
     sentence in the story: *how relevant is this part to the question?*
   * **Response** — multiply those weights by the second story embedding `c` and
     add them up, so the model keeps mostly the relevant facts.
   * **Answer** — concatenate the response with the question, run it through an
     `LSTM`, then a `Dense` + `softmax` over the whole vocabulary. In practice
     the network learns the answer is only ever `yes` or `no`.
5. **Train** — `rmsprop` optimizer, `categorical_crossentropy` loss, 120 epochs.
   The trained model is saved to `chatbot_120_epochs.h5`.
6. **Evaluate & play** — plot train/validation accuracy, predict on the test
   set, and finally feed the model **your own** story + question (using only
   words from the vocabulary) and read off its yes/no answer with a confidence
   score.

### Model architecture at a glance

```
 story ──► Embedding m ─┐
                        ├─► dot ─► softmax ─► (match / attention)
 question ─► Embedding u ┘                        │
                                                  ▼
 story ──► Embedding c ───────────────────────►  add ─► Permute
                                                  │
 question ─► Embedding u ────────────────────► concatenate
                                                  │
                                                  ▼
                                    LSTM ─► Dropout ─► Dense ─► softmax ─► yes / no
```

Reference paper: Sukhbaatar, Szlam, Weston, Fergus — *End-To-End Memory
Networks*, https://arxiv.org/abs/1503.08895

---

## How to run

```bash
# from this folder
pip install tensorflow keras matplotlib numpy
jupyter lab 02-Chat-Bots.ipynb   # or jupyter notebook
```

Run the cells top to bottom. Training 120 epochs takes a few minutes on CPU. The
notebook already contains saved outputs so you can also just read through it.

---

## Stretch exercise

`SYNTHETIC LAB DATASET.docx` swaps the yes/no answers for **open-vocabulary**
answers (e.g. *"Where is the map?" → "attic"*). Try adapting the same network to
predict any word in the vocabulary instead of just `yes`/`no`, and see how
accuracy changes.
