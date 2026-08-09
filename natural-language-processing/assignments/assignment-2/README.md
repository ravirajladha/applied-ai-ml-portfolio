# Customer Review Summarization — NLP Assignment 2 (PS-11)

An end-to-end application that reads many customer reviews for a product and
produces (a) a short summary of each review and (b) an aggregate verdict listing
the aspects customers praise and criticise most.

The summarizer is a **fine-tuned t5-small encoder–decoder** trained on the
Amazon Fine Food Reviews dataset. The interface is a **Streamlit** web app.

New to this project? Read **[JOURNEY.md](JOURNEY.md)** first — it explains what
was built, in what order, and why, in plain language. Then check
**[one.md](one.md)** for the open questions that still need answering.

---

## Files — organised by assignment task and owner

| Task | Module | What it does | Owner |
|---|---|---|---|
| — | `config.py` | Every path, constant and hyper-parameter | 1 |
| 2 | `data_prep.py` | Cleaning, filtering, train/val/test splits | 1 |
| 3.1 | `attention.py` | Bahdanau additive attention | 2 |
| 3.1 | `model_lstm.py` | Seq2Seq bi-LSTM encoder–decoder | 2 |
| 3.1 | `train_lstm.py` / `infer_lstm.py` | Train and run the LSTM baseline | 2 |
| 3.2 | `model_t5.py` | The T5 encoder–decoder wrapper | 3 |
| 3.2 | `train_t5.py` | Fine-tunes t5-small | 3 |
| 3.2 | `aggregate.py` | Map–reduce over many reviews | 3 |
| 3.3 | `aspects.py` | Praise/criticism aspect mining | 3 |
| 4 | `summarizer_service.py` | Shared service both front ends call | 4 |
| 4 | `app.py` | Streamlit web app | 4 |
| 4 | `flask_app.py` | Flask web app + JSON API | 4 |
| 4 | `run_osha.sh` | One-command setup for the OSHA lab | 4 |
| 5 | `evaluate_rouge.py` | ROUGE across all models | 5 |
| 5 | `demo_cases.py` | The demonstration scenarios | 5 |
| 6 | `assignment2.ipynb` | The graded notebook, all six tasks | 5 |
| — | `verify.py` | **Run this first** — checks everything works | all |
| — | `summarizer.py` | Compatibility layer re-exporting the above | — |
| — | `JOURNEY.md` | Plain-English build log |  |
| — | `one.md` | Open questions for the group |  |
| — | `TEAM_UPDATE.md` | Status summary for the group |  |

### Supporting files

| Path | What it is |
|---|---|
| `train.py` | One-command driver: prepares the data, then fine-tunes t5-small |
| `requirements.txt` | Python dependencies |
| `data/` | Held-out test split and the sample product used by the app demo |
| `models/` | The saved fine-tuned model (git-ignored, ~234 MB — rebuild with `train.py`) |
| `screenshots/` | App screenshots embedded in §4.4 of the notebook |
| `Group140.pdf` / `Group140.html` | The exported notebook — this is the graded submission file |

## Quick start

```bash
python verify.py            # is everything working on this machine?
python verify.py --trace    # watch the pipeline stage by stage
python demo_cases.py        # run the demonstration scenarios
```

---

## Setup

This machine is Windows on ARM64, where PyTorch has no native wheel, so the
project runs on the **x64 Anaconda Python** under emulation.

```bash
# from the assignment-2 folder
"C:/ProgramData/anaconda3/python.exe" -m venv .venv --system-site-packages
./.venv/Scripts/python.exe -m pip install -r requirements.txt
```

On a normal x64 machine, any Python 3.10+ works:

```bash
python -m venv .venv
.venv/Scripts/activate          # Windows
pip install -r requirements.txt
```

## Train the model

```bash
./.venv/Scripts/python.exe train.py                       # what was submitted: 4k reviews, ~50 min on CPU
./.venv/Scripts/python.exe train.py --train-size 20000    # better quality, several hours on CPU
```

This downloads the dataset, fine-tunes t5-small, and writes:

- `models/t5-review-summarizer/` — the trained model
- `data/test_reviews.csv` — held-out split used for ROUGE
- `data/sample_reviews.csv` — one real product's reviews for the app demo

## Run the web app

```bash
./.venv/Scripts/python.exe -m streamlit run app.py
```

Then open http://localhost:8501. The app accepts pasted text, an uploaded
`.txt`/`.csv`, or the built-in sample product.

> If no fine-tuned model is found the app still runs, falling back to plain
> `t5-small`, and says so in the sidebar.

## Run the notebook

```bash
./.venv/Scripts/python.exe -m jupyter lab assignment2.ipynb
```
