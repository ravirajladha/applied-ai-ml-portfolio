# PS5 — COVID-19 Diagnosis with a Decision Tree in Prolog

AIMLCZG557 / AECLZG557 — Assignment 2. A Prolog expert system that asks four
symptom questions, walks the given decision tree, and reports the likely
disease.

New to this project? Read **[JOURNEY.md](JOURNEY.md)** first — it explains
Prolog from scratch and walks through every decision we made.

## Run it

Against an input file (this is how it will be graded):

```
swipl -q -g main -t halt PS05.pl < inputPS05.txt
```

Interactively:

```
swipl PS05.pl
?- main.
```

On Windows, if `swipl` is not on your PATH:

```
"C:\Program Files\swipl\bin\swipl.exe" -q -g main -t halt PS05.pl < inputPS05.txt
```

Results print on screen and are written to `outputPS05.txt` (rewritten each run).

## Answer format

Four questions, each answered with a word and a **full stop**:

| Question | Valid answers |
|---|---|
| Fever intensity | `high_sudden.` `high.` `mild.` `none.` — or a temperature, e.g. `101.9.` |
| Cough type | `severe_dry.` `persistent_dry.` `mild.` `none.` |
| Body pain severity | `severe.` `excruciating.` `mild.` `none.` |
| Skin rash type | `absent.` `patchy.` |

An input file is just those answers, one per line, four lines per patient. Put
several patients in one file and the program diagnoses each in turn.

## Files

| File | Purpose | In the zip? |
|---|---|---|
| `PS05.pl` | The whole program — single file, as required | yes |
| `inputPS05.txt` | Test input | yes |
| `outputPS05.txt` | Generated results | yes |
| `designPS05.md` | Design document — export to `designPS05_Gxxx.pdf` | yes, as PDF |
| `Gxxx_Contribution.csv` | Contribution sheet — save as `.xlsx` | yes, as XLSX |
| `JOURNEY.md` | How the project was built, for a beginner | no |
| `README.md` | This file | no |
| `tests/` | Extra inputs and saved transcripts | no |

### tests/

| File | What it covers |
|---|---|
| `input_all_cases.txt` | Both PDF samples plus all required edge cases (6 patients) |
| `output_all_cases.txt` | Results from the above |
| `transcript_all_cases.txt` | Full screen transcript from the above |
| `input_errors.txt` | An invalid value and a truncated case |
| `input_malformed.txt` | An answer that is not readable Prolog |
| `transcript.txt` | Screen transcript of the `inputPS05.txt` run |

## Before submitting

1. Fill in the **Group Id and member names** in the header of `PS05.pl` and at
   the top of `designPS05.md`.
2. Export `designPS05.md` to **`designPS05_Gxxx.pdf`** (max 4 pages).
3. Fill in `Gxxx_Contribution.csv` and save it as **`Gxxx_Contribution.xlsx`**
   with columns *Student Registration Number*, *Name*, *Percentage of
   contribution out of 100%*.
4. Rename `Gxxx` to your real group id everywhere (e.g. `G026`).
5. Zip `PS05.pl`, `inputPS05.txt`, `outputPS05.txt`, the design PDF and the
   contribution XLSX as **`Gxxx_A2_PS05.zip`**.
6. Confirm the run still works from a clean folder.

Deadline: **17 Aug 2026, 23:55 IST**.
