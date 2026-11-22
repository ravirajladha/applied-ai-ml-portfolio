# Speech Processing (AIMLC ZG520) — Study spec

> How machines turn speech into text (ASR) and text into speech (TTS): from HMMs and MFCCs to Whisper. · Status: spec only (not built yet)

## 1. What it is and why an AI engineer should care

Speech processing covers automatic speech recognition (ASR: audio in, words out) and speech synthesis (TTS: words in,
audio out). This course teaches the classic statistical pipeline first: acoustic features (MFCCs), hidden Markov models
and Gaussian mixtures for sounds, n-gram language models for word sequences, WFSTs and Viterbi/beam search to decode.
It then moves to neural acoustic models, neural TTS (WaveNet, Tacotron, FastSpeech) and transformer models such as
wav2vec 2.0, HuBERT and Whisper. Voice bots, call-centre analytics and meeting transcription all run on this stack.

**Job relevance: 3/5** — voice AI is a real niche (call centres, voice agents); most teams use Whisper/APIs, so deep HMM/WFST maths is mostly exam value.

## 2. Sources in this folder

| Kind | File (relative path) | Notes |
|---|---|---|
| Handout (older batch) | `handouts/Older batch - Speech Processing (S2-25_AIMLCZG520) COURSE HANDOUT.docx` | v1.0, 27-02-2025, Second Semester 2025-2026, Dr. Vijayalakshmi Anand; 9 content modules, 16 sessions |

Gaps:
- Only an older-batch handout: no current handout, slides, past papers or lab sheets.
- The session plan skips session 6 (it jumps from 5 WFST to 7 neural acoustic models); what session 6 covers is not stated.
- The lab table in the handout is empty ("Lab work: 0"; 2 assignments, 4 webinars).

## 3. Running scenario

**VaaniPay** is a payments company whose phone helpline gets 40,000 calls a day in English, Hindi and Hinglish.
Today callers press keys; the product team wants callers to just speak: first their 6-digit customer PIN, then free
requests like "mera last transaction status batao". The data: 2,000 hours of recorded, consented calls with partial
transcripts, plus a list of banking phrases. The goal: an ASR service with word error rate under 15%, a spoken reply
in a natural voice, and per-call transcripts for analytics. Each module adds one stage of the VaaniPay voice pipeline.

## 4. Module map

Contact hours per module: not stated. Sessions per module are from the handout's learning plan.

### M1 · Introduction to statistical speech recognition (session 1)

Topics: statistical speech recognition; history of ASR; architecture of an ASR system; the recognition process; isolated
digit recognition as a simple example; evaluation of ASR.

| Concept | One-line definition (≤20 words, no jargon) | Analogy |
|---|---|---|
| ASR | Converting a speech recording into the most likely word sequence. | A compiler from sound to text |
| Noisy-channel view | Pick words W maximising P(audio given W) x P(W): acoustic model times language model. | A spell-checker weighing typo likelihood and word frequency |
| Acoustic model | Scores how well a stretch of audio matches each speech sound. | A per-character OCR confidence |
| Language model | Scores how likely a word sequence is in the language. | Autocomplete's sense of "normal" sentences |
| Word error rate (WER) | (substitutions + deletions + insertions) / words in the reference transcript. | Edit distance, counted in words |
| Isolated word recognition | Recognising one word at a time from a small vocabulary, like digits. | Matching against an enum, not free text |

Diagram ideas:
- ASR block diagram: audio → features → acoustic model + lexicon + LM → decoder → words.
- WER alignment of reference vs hypothesis with S/D/I marked.

Scenario step: recognise the caller's spoken 6-digit PIN (10-word vocabulary).

Notebook idea: compute WER with `jiwer` by hand-checked examples; template-matching digit recogniser on the Free Spoken
Digit Dataset (FSDD) using MFCC + DTW. CPU.

Production angle: WER dashboards per accent and channel. Breaks: WER on clean test audio is 5% but 30% on real phone
lines (8 kHz, noise).

### M2 · Speech signal: production, perception, acoustic-phonetic characterisation (session 2)

Topics: speech production process; time and frequency representations; speech sounds and their features.

| Concept | One-line definition (≤20 words, no jargon) | Analogy |
|---|---|---|
| Source-filter model | Vocal folds make a buzz (source); the mouth and throat shape it (filter). | A synth oscillator plus an EQ |
| Phoneme | The smallest sound unit that changes meaning (p vs b in "pat"/"bat"). | A token in the sound vocabulary |
| Fundamental frequency (pitch, F0) | How fast the vocal folds vibrate; heard as how high the voice is. | Clock rate of the source |
| Formants | Resonant frequency peaks set by mouth shape; they identify vowels. | Peaks in an EQ curve |
| Spectrogram | A picture of frequency energy over time. | A heat map of a log stream by minute |
| Voiced vs unvoiced | Voiced sounds use vocal-fold vibration (a, m); unvoiced do not (s, f). | Powered vs passive components |

Diagram ideas:
- Source-filter diagram with a waveform, a spectrum and a vowel's formants.
- Spectrogram of "seven" with the voiced and fricative parts labelled.

Scenario step: understand why 8 kHz phone audio loses "s"/"f" detail that hurts digit recognition ("six" vs "fix").

Notebook idea: record or load a word, plot waveform, spectrogram and pitch (`librosa.pyin`) with `librosa`/`matplotlib`. CPU.

Production angle: resampling, codecs. Breaks: training on 16 kHz audio and serving 8 kHz phone audio.

### M3 · Acoustic model: HMM, GMM, WFST, neural acoustic models (sessions 3, 4, 5, 7)

Topics: Markov chains; HMMs and their three problems; forward, Viterbi and EM (Baum-Welch) algorithms; Gaussian and
Gaussian-mixture models and parameter estimation; GMMs for speech features; WFST definition, algorithms and use in ASR;
DNN-HMM hybrid systems (architecture, decoding, training of CD-DNN-HMMs); tandem/bottleneck features; DNN-HMM vs GMM-HMM;
time-delay neural networks (TDNN); RNNs and backpropagation through time.

| Concept | One-line definition (≤20 words, no jargon) | Analogy |
|---|---|---|
| HMM | Hidden states (sounds) that emit visible observations (feature frames), with transition probabilities. | A state machine you only see through its logs |
| Three HMM problems | Evaluation (forward), decoding (Viterbi), learning (Baum-Welch / EM). | Score a trace, explain a trace, learn from traces |
| Viterbi algorithm | Dynamic programming that finds the single most likely hidden-state path. | Shortest path through a layered graph |
| GMM | A probability model that is a weighted sum of several Gaussian bell curves. | Several clusters, each with its own spread |
| WFST | A weighted finite-state transducer: a graph mapping input symbols to output symbols with costs. | A routing table that rewrites as it routes |
| DNN-HMM hybrid | A neural network gives state probabilities; the HMM still handles timing. | Swapping a heuristic for an ML model inside the same pipeline |
| TDNN | A network that looks at a sliding window of frames at several time offsets. | A 1-D convolution over time |

Diagram ideas:
- Left-to-right 3-state HMM for one phoneme, with emission and transition arrows.
- Viterbi trellis for 3 states x 4 frames with the best path highlighted (worked numerical).
- WFST composition H o C o L o G as four stacked boxes.

Scenario step: train one HMM per digit on MFCCs; later swap GMM scores for a small neural network.

Notebook idea: forward and Viterbi written in numpy on a toy HMM (assert vs brute force); `hmmlearn` GMM-HMM per digit on
FSDD, accuracy table. WFST: a tiny hand-written transducer in Python (OpenFst/pynini is hard to install on Windows). CPU.

Production angle: Kaldi (GMM/DNN-HMM, WFST), k2/icefall. Breaks: Viterbi underflows without log probabilities.

### M4 · Language model for speech processing (sessions 9–10)

Topics: n-gram models; smoothing: add-1, back-off and interpolation, Good-Turing, Kneser-Ney; n-gram models as WFSAs;
recognising an utterance; word embeddings and word2vec; decoding with neural LMs (lattice rescoring, shortlists); RNN
and LSTM LMs and their comparison.

| Concept | One-line definition (≤20 words, no jargon) | Analogy |
|---|---|---|
| N-gram model | Predicts the next word from the previous n-1 words using counts. | Autocomplete from a frequency table |
| Smoothing | Giving some probability to word sequences never seen in training. | A default value for cache misses |
| Back-off / interpolation | Use shorter contexts when longer ones are unseen, or blend all lengths. | Fallback config layers |
| Kneser-Ney | Smoothing that favours words appearing in many different contexts. | Trusting a library used by many projects |
| Perplexity | How surprised the model is by test text; lower is better. | Average branching factor of guesses |
| Lattice rescoring | Re-rank a decoder's candidate word graph with a stronger (neural) LM. | A second-pass re-ranker |

Diagram ideas:
- Bigram table and a back-off arrow from trigram → bigram → unigram.
- Word lattice for "send money / sent money" rescored by an LSTM LM.

Scenario step: a banking-phrase LM makes "check balance" beat "chess balance".

Notebook idea: bigram LM with add-1 and interpolation on banking phrases, perplexity on held-out text; small LSTM LM in
torch (CPU, minutes). CPU.

Production angle: KenLM, shallow fusion with neural ASR, contextual biasing (boosting names). Breaks: new product names
are out of vocabulary and never recognised.

### M5 · Speech analysis: acoustic feature extraction (session 11)

Topics: acoustic features for ASR; MFCCs: windowing, DFT, mel filter bank. (Learning outcomes also name PLPs and log-mel
spectrograms.)

| Concept | One-line definition (≤20 words, no jargon) | Analogy |
|---|---|---|
| Framing and windowing | Cut audio into 25 ms frames every 10 ms, tapering edges with a window. | Sliding-window metrics on a stream |
| DFT / FFT | Converts a frame from amplitude-over-time into energy-per-frequency. | Turning a log into a histogram by category |
| Mel filter bank | Triangular filters spaced like human hearing, finer at low frequencies. | Log-scale buckets |
| Log-mel spectrogram | Log energies of mel filters over time; the standard input for neural ASR. | A normalised heat map |
| MFCC | DCT of log-mel energies, keeping ~13 coefficients per frame. | Compressing the heat map to a few principal knobs |

Diagram ideas:
- Full MFCC pipeline: pre-emphasis → frame → window → FFT → mel → log → DCT, with array shapes at each step.
- Mel scale vs linear Hz curve.

Scenario step: one feature extractor shared by training and the live call stream.

Notebook idea: MFCC from scratch in numpy (frame, Hamming, FFT, mel filters, log, DCT), compare with `librosa.feature.mfcc`
within tolerance. CPU.

Production angle: torchaudio/librosa feature extraction in streaming. Breaks: different normalisation between offline
features and streaming features (training-serving skew).

### M6 · Search and decoding (session 12)

Topics: Viterbi search; beam search; multipass decoding; A* (stack) decoding; translating in low-resource situations.

| Concept | One-line definition (≤20 words, no jargon) | Analogy |
|---|---|---|
| Decoding | Searching for the best word sequence given acoustic and language scores. | Query planning over a huge search space |
| Beam search | Keep only the best k partial hypotheses at each step. | Keeping the top-k candidates in a priority queue |
| Beam width | Larger beams are more accurate but slower. | Search depth vs latency budget |
| Multipass decoding | A fast first pass makes a lattice or n-best list; a stronger model rescores it. | Cheap filter, expensive re-rank |
| A* (stack) decoding | Best-first search using a cost-so-far plus an estimate of cost remaining. | A* path finding in maps |

Diagram ideas:
- Beam search tree with pruned branches greyed out (beam = 2).
- Two-pass decoding: n-gram pass → lattice → neural LM rescoring.

Scenario step: tune beam width to meet a 300 ms latency budget per utterance.

Notebook idea: beam search over a toy acoustic-score matrix + bigram LM; plot accuracy vs beam width and time. CPU.

Production angle: CTC beam decoders (pyctcdecode), WFST decoders in Kaldi. Breaks: beam too narrow under noise drops the
right hypothesis early.

### M7 · Speech synthesis (sessions 13–14)

Topics: what speech synthesis is; text normalisation; phonetic analysis; prosodic analysis; diphone waveform synthesis;
unit-selection synthesis; neural TTS (WaveNet, Tacotron, FastSpeech); evaluation.

| Concept | One-line definition (≤20 words, no jargon) | Analogy |
|---|---|---|
| Text normalisation | Turning "₹1,500 on 3/4" into words a voice can say. | Input sanitising before rendering |
| Grapheme-to-phoneme | Converting spelling to pronunciation symbols. | A transpiler from text to sound codes |
| Prosody | Rhythm, stress and intonation of speech. | Formatting, not content |
| Unit selection | Glue together recorded snippets chosen to fit target sounds and prosody. | Assembling a page from cached fragments |
| Tacotron / FastSpeech | Neural models mapping text to a mel spectrogram; FastSpeech is non-autoregressive and faster. | Serial vs parallel rendering |
| Vocoder (WaveNet) | Turns a mel spectrogram into an audio waveform. | A codec decoder |
| MOS | Mean opinion score: listeners rate naturalness 1–5. | User satisfaction survey |

Diagram ideas:
- TTS pipeline: text → normalise → phonemes + prosody → acoustic model → vocoder → audio.
- Autoregressive (Tacotron) vs parallel (FastSpeech) generation timelines.

Scenario step: VaaniPay speaks back "Your last payment of 1,500 rupees succeeded".

Notebook idea: write a rule-based text normaliser for amounts and dates with asserts; run a pretrained CPU TTS (Piper or
Coqui TTS) and compare two voices by a small self-MOS. CPU.

Production angle: Piper, Coqui, cloud TTS, SSML. Breaks: numbers and abbreviations read wrongly ("Dr." as "drive").

### M8 · Acoustic signal processing (session 15)

Topics: acoustic processing of speech; sound waves; interpreting a waveform; feature extraction; computing acoustics;
training a speech recogniser; waveform generation for synthesis; pitch and duration modification.

| Concept | One-line definition (≤20 words, no jargon) | Analogy |
|---|---|---|
| Sampling and quantisation | Recording amplitude at fixed intervals with fixed bit depth. | Polling a sensor at a fixed rate |
| Nyquist rate | You must sample at twice the highest frequency you want to keep. | Polling faster than the event rate |
| Energy and zero-crossing rate | Loudness and how often the signal crosses zero; separate speech from silence. | Simple health metrics on a stream |
| Pitch modification | Changing how high a voice sounds without changing speed. | Changing colour without resizing |
| Duration modification (time stretch) | Changing speed without changing pitch (e.g. PSOLA). | Changing playback rate of a video without chipmunk audio |

Diagram ideas:
- Sampling at two rates showing aliasing.
- Energy + ZCR curves over a waveform with speech/silence regions marked (voice activity detection).

Scenario step: voice activity detection trims silence so the ASR only processes speech, cutting compute.

Notebook idea: energy/ZCR voice activity detector in numpy; `librosa.effects.pitch_shift` and `time_stretch` demos. CPU.

Production angle: WebRTC VAD, Silero VAD. Breaks: VAD clips the first syllable, so digits at the start are lost.

### M9 · Transformer-based acoustic and language models (session 16)

Topics: from RNNs to transformers in ASR; self-attention for speech; wav2vec 2.0, HuBERT, Whisper; fine-tuning for
low-resource and domain-specific ASR; comparison with RNN/LSTM; applications: multilingual ASR, diarisation, zero-shot
transfer.

| Concept | One-line definition (≤20 words, no jargon) | Analogy |
|---|---|---|
| Self-supervised pretraining | Learning from unlabelled audio by predicting masked or hidden parts. | Learning a codebase by reading it, before any tickets |
| wav2vec 2.0 / HuBERT | Transformer encoders pretrained on raw audio, then fine-tuned with a few labelled hours. | A pretrained base image you extend |
| Whisper | An encoder-decoder trained on 680k hours of weakly labelled audio for multilingual ASR and translation. | A batteries-included SDK |
| CTC | A loss letting the model output characters per frame without exact alignment. | Diffing streams that may have repeats and gaps |
| Diarisation | Working out who spoke when in a recording. | Attributing log lines to users |
| Low-resource fine-tuning | Adapting a pretrained model with little in-domain data (e.g. Hinglish banking calls). | Tuning config for one client |

Diagram ideas:
- Evolution timeline: GMM-HMM → DNN-HMM → RNN/CTC → transformer (wav2vec 2.0, Whisper).
- Whisper encoder-decoder with log-mel input and task tokens.

Scenario step: replace the HMM pipeline with Whisper for free-form Hinglish requests; fine-tune if WER is too high.

Notebook idea: run `openai/whisper-tiny` or `base` via `transformers` on 20 sample clips (CPU, slow but fine), compute WER;
LoRA fine-tuning shown as reading only (needs a GPU).

Production angle: faster-whisper, whisper.cpp, pyannote for diarisation, streaming ASR. Breaks: Whisper hallucinates text
during long silences; trim with VAD first.

## 5. Codebase plan

`vaanipay-voice`: a local speech pipeline from digits to Whisper.

```
codebase/
├── README.md                   how to run; which module added which file           (M1)
├── data/fetch_fsdd.py          download Free Spoken Digit Dataset + sample clips    (M1)
├── src/vaani/
│   ├── metrics.py              WER via edit distance                               (M1)
│   ├── features.py             framing, MFCC from scratch, log-mel                 (M2, M5)
│   ├── hmm.py                  forward + Viterbi in log space                       (M3)
│   ├── digits.py               GMM-HMM digit recogniser                             (M3)
│   ├── lm.py                   n-gram LM with smoothing, perplexity                 (M4)
│   ├── decode.py               beam search with LM weight                           (M6)
│   ├── vad.py                  energy/ZCR voice activity detection                  (M8)
│   ├── tts.py                  text normaliser + pretrained TTS wrapper             (M7)
│   └── whisper_asr.py          Whisper transcription + WER report                  (M9)
└── tests/
    ├── test_metrics.py         WER on known examples                               (M1)
    ├── test_features.py        matches librosa within tolerance                    (M5)
    ├── test_hmm.py             Viterbi equals brute force on toy HMM               (M3)
    └── test_tts_norm.py        "₹1,500" → "one thousand five hundred rupees"       (M7)
```

## 6. Practice topics plan

1. 01 ASR overview and WER — M1 — 3 h
2. 02 Speech signals and spectrograms — M2, M8 — 3 h
3. 03 MFCC from scratch — M5 — 4 h
4. 04 HMMs: forward and Viterbi — M3 — 5 h
5. 05 GMM-HMM digit recogniser and WFST basics — M3 — 5 h
6. 06 N-gram LMs and smoothing — M4 — 4 h
7. 07 Beam search decoding — M6 — 3 h
8. 08 Speech synthesis pipeline — M7 — 4 h
9. 09 Whisper and self-supervised ASR — M9 — 4 h

## 7. Exam signal

No past question papers in this folder. Evaluation scheme (older handout):

| Component | Type | Weight | Date (that batch) |
|---|---|---|---|
| EC-1(a) Quizzes | Online | 10% | TBA |
| EC-1(b) Assignments | Take home | 20% | TBA |
| EC-2 Mid-Semester Test | Closed book, 2 h | 30% | 21-06-2026 |
| EC-3 Comprehensive Exam | Open book, 2.5 h | 40% | 06-09-2026 |

Mid-sem = sessions 1–8 (M1–M3), closed book. The course objectives name implementing Viterbi, beam search and WFST beam
decoding (CO4), so expect worked numericals: forward/Viterbi trellis, n-gram probability with smoothing, WER.

## 8. Interview angle

1. **How do you measure ASR quality?** WER: substitutions + deletions + insertions over reference word count, sliced by accent and channel.
2. **What are MFCCs?** Compact per-frame features from a log mel spectrogram via DCT; classic ASR input.
3. **What does Viterbi do?** Finds the most likely hidden-state path with dynamic programming in O(T x N²).
4. **Why is a language model needed in ASR?** Acoustically similar phrases are disambiguated by which word sequence is likely.
5. **What is CTC?** A loss that aligns per-frame outputs to a shorter label sequence using blank tokens.
6. **Whisper vs wav2vec 2.0?** Whisper is a supervised encoder-decoder trained on huge weak labels; wav2vec 2.0 is self-supervised and needs fine-tuning.
7. **How do you adapt ASR to a new domain?** Contextual biasing or an in-domain LM first, then fine-tune on a few hours of labelled audio.
8. **What makes TTS sound robotic?** Poor prosody and text normalisation, or a weak vocoder.
9. **What breaks with phone audio?** 8 kHz bandwidth, codecs and noise; train or fine-tune on matched audio.
10. **How do you cut ASR latency?** Streaming models, VAD, smaller models (quantised Whisper), narrower beams.

## 9. Repetition plan

| Concept | First met (module) | Revisited in (modules) |
|---|---|---|
| Noisy-channel (AM x LM) | M1 | M3, M4, M6 |
| Spectrogram / frequency view | M2 | M5, M8, M9 (log-mel input) |
| MFCC | M1 (digit demo) | M3, M5 |
| HMM / Viterbi | M3 | M6 (Viterbi search) |
| Language model | M1 | M4, M6, M9 |
| WER | M1 | M3, M9 |
| Beam search | M6 | M9 (Whisper decoding) |
| Mel spectrogram | M5 | M7 (TTS target), M9 |

## 10. Overlap with my other courses

- [../../natural-language-processing/](../../natural-language-processing/) — n-gram LMs (revision ch04), HMM + Viterbi (ch06), word2vec (ch03): same algorithms, applied to text.
- [../../nlp-applications/](../../nlp-applications/) — textbook T1 (Jurafsky & Martin) is shared; NLP apps uses it too.
- [../../llm-engineering/](../../llm-engineering/) — transformer and self-attention basics for M9.
- [../audio-analytics/](../audio-analytics/) — audio features, spectrograms and MFCCs with real labware.
- [../multimodal-information-retrieval/](../multimodal-information-retrieval/) — its M5 audio retrieval and spoken term search use the same features.

## 11. Build checklist

- [ ] SPEC reviewed
- [ ] cards.json (M1…M9, 5–8 cards each)
- [ ] practice/01 ASR overview and WER
- [ ] practice/02 Speech signals and spectrograms
- [ ] practice/03 MFCC from scratch
- [ ] practice/04 HMMs: forward and Viterbi
- [ ] practice/05 GMM-HMM digit recogniser and WFST basics
- [ ] practice/06 N-gram LMs and smoothing
- [ ] practice/07 Beam search decoding
- [ ] practice/08 Speech synthesis pipeline
- [ ] practice/09 Whisper and self-supervised ASR
- [ ] codebase/ runs + tests

Total estimated study hours: ≈ 35 h practice + ≈ 10 h codebase + ≈ 5 h cards/revision = **≈ 50 h**.
