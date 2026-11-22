# Audio Analysis (AIML ZG539) — Study spec

> Turning raw sound into features, labels, transcripts, search results and generated audio, from STFT and MFCCs to Whisper, CLAP, MusicGen and voice agents. · Status: spec only (not built yet)

Folder slug is `audio-analytics`; the handout's course title is **Audio Analysis**.

---

## 1. What it is and why an AI engineer should care

Audio is a 1-D signal sampled thousands of times a second; this course teaches how to turn it into something a model can use (spectrograms, MFCCs, embeddings) and then covers the main product tasks: classifying sounds, transcribing speech (ASR), speaking text (TTS), recommending music, searching audio with text (CLAP), generating audio, monitoring machines and patients by sound, and building voice agents.
The current handout (25-May-2026) is very modern: pretrained transformers (Wav2Vec2, HuBERT, AST), Whisper, CLAP, MusicGen, diffusion audio, agentic AI and deepfake detection.
Labware is unusually complete: 26 notebooks covering almost every module.
For a software engineer it connects directly to voice assistants, call-centre analytics, meeting transcription and predictive maintenance.

**Job relevance: 4/5** — voice agents, ASR/TTS pipelines and audio search are live product areas; the feature-engineering half is less common day to day, but the pretrained-model and agent half is directly hireable.

---

## 2. Sources in this folder

| Kind | File (relative path) | Notes |
|---|---|---|
| Handout (current) | `handouts/Handout - AA - 25-May-2026.pdf` | v2, 11 modules, 16 contact sessions (CS), 11 labs, evaluation scheme. **This one wins.** |
| Handout (older) | `handouts/Older batch - AIML_ ZG539 Audio Analysis.pdf` | v2 dated 24-Apr-2026, 10 modules. Has a separate "Machine Learning for Audio" module (k-NN, SVM, random forest, augmentation, evaluation) and explicitly lists quantization/Nyquist; no separate classification/tagging, music recommendation or ethics modules. Past papers and labware follow this older plan. |
| Slides | `lecture-slides/Audio_M1_Introduction.pdf` | M1 |
| Slides | `lecture-slides/Audio_M2_Basics_Features.pdf` | M2 sampling, time/frequency features |
| Past paper | `past-question-papers/AA - Jun 2026 - Midsem Regular Set 1.pdf` | 6 Qs × 5 marks, closed book |
| Past paper | `past-question-papers/AA - Jun 2026 - Midsem Regular Set 2.pdf` | 6 Qs × 5 marks |
| Past paper | `past-question-papers/AA - Sep 2026 - Endsem Regular Set 1.pdf` | 4 Qs × 10 marks, open book |
| Past paper | `past-question-papers/AA - Sep 2026 - Endsem Regular Set 2.pdf` | 4 Qs × 10 marks |
| EC-1 proforma | `EC1_Proforma_AIML_ZG539.pdf` | Current term: 3 quizzes (best 2 of 3, 5% each), 2 auto-graded assignments (10% each, A1 25-Nov to 08-Dec-2026, A2 12-Jan to 26-Jan-2027) |
| Labware | `labware/Lab 1A-Audio_IO_and_Understanding.ipynb`, `Lab 1B-Batch_Audio_Processing.ipynb` | Loading, waveform, batch processing |
| Labware | `labware/Lab 2-Time_Frequency_Representations.ipynb` | STFT, spectrograms |
| Labware | `labware/Lab 3A/3B/3C-...ipynb` | Time-domain, frequency-domain, MFCC + chroma features |
| Labware | `labware/Lab 4A-Audio_Data_Augmentation.ipynb`, `Lab 4B-ML_Algorithm_Comparison.ipynb`, `Lab 4C-Wake Word Detection - 1D CNN.ipynb` | Augmentation, classic ML, 1-D CNN wake word |
| Labware | `labware/Lab 5A/5B/5C_..._YAMNet.ipynb` | Environmental sound, acoustic scene, sound event detection with YAMNet |
| Labware | `labware/Lab 6A_Speech_ASR_Whisper.ipynb`, `Lab 6B_TTS.ipynb`, `Lab 6C_VoiceCloning.ipynb` (+ `reference_speaker.wav`) | ASR, TTS, voice cloning |
| Labware | `labware/Lab 7A_Genre_Classification.ipynb`, `Lab 7B_MatrixFactorization_MSD.ipynb` | Genre classification, matrix factorisation on Million Song Dataset |
| Labware | `labware/Lab 8A/8B/8C-...ipynb` | Audio embeddings + similarity, CLAP text-to-audio retrieval, audio RAG with CLAP + LLM |
| Labware | `labware/Lab 9A_NeuralCodec_and_Generation.ipynb`, `Lab 9B_Diffusion_Audio.ipynb` | Neural codecs, diffusion |
| Labware | `labware/Lab 10A/10B/10C_...ipynb` | Respiratory sounds (ICBHI), industrial anomaly detection, BirdNET |
| Labware | `labware/Lab 11A Agentic_ AI_Audio.ipynb` | Audio agent |

**Gaps:** slides only for M1–M2; labware numbering follows the older plan (no dedicated ethics/deepfake notebook); past papers are from the older batch, so M6 music and M11 ethics are lightly tested; no textbook PDFs.

---

## 3. Running scenario

**SoundOps** is a start-up selling an "ears for your building" platform to a chain of hospitals and factories. Microphones stream 16 kHz audio from **factory floors** (pumps, valves, fans) and **hospital wards** (coughs, alarms, staff conversations), plus a separate product for **meeting/podcast transcription**.
The goal: classify sounds and flag anomalies in real time on edge devices, transcribe and summarise spoken notes, let staff search recordings by text ("alarm beeping near bed 4"), and generate short voice prompts, all without leaking private speech.
Data: public stand-ins the labs already use (ESC-50, UrbanSound8K, LibriSpeech, GTZAN, MIMII/DCASE, COUGHVID, ICBHI).
Each module adds one feature to the SoundOps platform, and the past-paper scenarios (smart factory, hospital ward, siren detector, valve monitor, meeting agent) map straight onto it.

---

## 4. Module map

Contact sessions from the current handout; each CS is a ~2 h lecture (hours per CS not stated).

### M1 · Introduction to Audio Analysis (≈ CS 1)

Topics: what and why of audio analysis; real-world applications (healthcare, predictive maintenance, speech, entertainment, security); digital audio acquisition; digital audio formats.

| Concept | One-line definition | Analogy |
|---|---|---|
| Waveform | Air-pressure level recorded at each instant, stored as a list of numbers | A time-series metric sampled every few microseconds |
| Audio format (WAV, FLAC, MP3) | How samples are packed in a file: raw, lossless-compressed or lossy-compressed | PNG vs ZIP vs JPEG |
| Lossy compression | Throws away sound humans barely hear to save space | JPEG for images |
| Channel / bit depth | Number of parallel recordings / number of bits per sample | Columns in a table / precision of each number |
| Audio analytics task | Classify, detect, transcribe, retrieve or generate from audio | The CRUD verbs of audio products |

Diagram ideas: microphone → ADC → samples → file → model pipeline; application map (health, industry, speech, music, security) with one product each.
Scenario step: SoundOps lists which sounds matter in a factory vs a ward and picks file formats and storage.
Notebook idea: load a WAV and an MP3 of the same clip with librosa/soundfile, compare sizes, sample rates, plot waveforms. Laptop.
Production angle: ffmpeg, soundfile, cloud object storage. **Breaks:** mixed sample rates and stereo/mono across devices silently change features. Monitor input sample rate and clipping rate.

### M2 · Audio Fundamentals and Feature Extraction (≈ CS 2–3)

Topics: sampling and digital audio representation; time-domain features (amplitude, zero crossing rate, energy); frequency-domain features (FFT, power spectrum); STFT; mel spectrograms; similarity metrics; MFCCs; chroma; spectral contrast. (Older handout also: quantization, Nyquist, spectral centroid/flux/band-energy ratio.)

| Concept | One-line definition | Analogy |
|---|---|---|
| Sampling rate / Nyquist | Samples per second; you can only capture frequencies below half of it | Frame rate: too low and wheels spin backwards |
| Aliasing | High frequencies sampled too slowly appear as fake lower frequencies | Integer overflow wrapping to a wrong value |
| Zero crossing rate (ZCR) | How often the waveform crosses zero; high for noisy/hissy sounds | Count of sign flips in a metric |
| RMS energy | Average loudness of a frame | Average CPU load over a window |
| STFT / spectrogram | Chop audio into short overlapping windows and take each window's frequency content | A sliding-window histogram over time |
| Window vs hop size | Window length sets frequency detail; hop sets time step between windows | Batch size vs polling interval |
| Mel spectrogram | Spectrogram with frequency bins squeezed to match human pitch perception | Log scale on a chart axis |
| MFCC | Compact summary of the mel spectrum's shape; low coefficients = overall timbre | A hash/fingerprint of a frame's tone colour |

Diagram ideas:
- Time–frequency trade-off: same clip with window 256 vs 2048 side by side.
- Aliasing fold diagram: 5 kHz and 9 kHz tones sampled at 12 kHz landing at 5 kHz and 3 kHz.
- Feature pipeline: waveform → frames → FFT → mel filterbank → log → DCT → MFCC.

Scenario step: SoundOps builds the feature extractor that every downstream model in the platform reads.
Notebook idea: compute frequency resolution (sr / n_fft) and time resolution (hop / sr) and assert them; reproduce the midsem bug (`sr / hop_length` is wrong); extract STFT, mel, MFCC, chroma, ZCR, RMS from speech vs music with librosa. Laptop.
Production angle: librosa, torchaudio, on-device DSP. **Breaks:** training features computed at 22.05 kHz, device streams 16 kHz (training–serving skew). Monitor feature distributions per device.

### M3 · Deep Learning for Audio (≈ CS 4–5)

Topics: CNNs for spectrograms; RNNs/LSTMs for audio sequences; attention; audio transformers (Wav2Vec2, HuBERT, AudioMAE); transfer learning (YAMNet, Wav2Vec2, AST).

| Concept | One-line definition | Analogy |
|---|---|---|
| CNN on spectrogram | Treat the spectrogram as an image and learn local time–frequency patterns | Image classifier on a heatmap |
| LSTM on frames | Reads frame features in order and remembers context over time | A stateful stream processor |
| Self-supervised pretraining | Learn from unlabeled audio by predicting masked parts | Autocomplete trained on all your logs |
| Wav2Vec2 / HuBERT | Transformers pretrained on raw speech to give rich per-frame embeddings | A pretrained SDK you call instead of writing your own parser |
| AST | Audio Spectrogram Transformer: splits a spectrogram into patches like a vision transformer | ViT for sound |
| Transfer learning / fine-tuning | Reuse a pretrained model; retrain only the top or all layers on your data | Forking a mature library vs writing from scratch |

Diagram ideas: CNN vs LSTM receptive field on a spectrogram; Wav2Vec2 masked prediction; freeze-vs-unfreeze ladder for 500 vs 50,000 samples.
Scenario step: SoundOps has only 500 labelled factory clips, so it builds on pretrained YAMNet/AST embeddings.
Notebook idea: YAMNet or AST embeddings + logistic regression on an ESC-50 subset vs a small CNN trained from scratch. CPU works for embeddings; fine-tuning AST wants a GPU (Colab).
Production angle: Hugging Face Transformers, TensorFlow Hub, ONNX for edge. **Breaks:** fully unfreezing AST on 500 clips overfits (a midsem question). Monitor validation gap.

### M4 · Audio Classification and Tagging (≈ CS 6)

Topics: environmental sound classification; acoustic scene classification; sound event detection; evaluation metrics (accuracy, mAP, F1).

| Concept | One-line definition | Analogy |
|---|---|---|
| Sound classification | One label per clip ("dog bark") | Classifying a support ticket |
| Acoustic scene classification | Label the place/context ("metro station") | Tagging a log file by which service produced it |
| Sound event detection (SED) | Find what happens *and when* (start/end times) | Log parsing with timestamps |
| Multi-label tagging | A clip can have several labels at once | GitHub issue labels |
| Precision / recall / F1 | Of alarms raised, how many real / of real events, how many caught / their balance | Alert precision vs on-call misses |
| mAP | Average precision across classes, ranking-aware | Search-quality score across many queries |

Diagram ideas: clip vs scene vs event timeline; confusion matrix for a rare "siren" class showing why 96.8% accuracy misleads.
Scenario step: SoundOps raises alerts for alarms and glass breaks in wards without paging nurses for every door slam.
Notebook idea: compute accuracy/precision/recall/F1 from the endsem siren confusion matrix (18, 12, 20, 950) with asserts; frame-level SED on UrbanSound8K clips using YAMNet frame scores + threshold. Laptop.
Production angle: DCASE-style pipelines, threshold tuning per site. **Breaks:** model trained on ESC-50 collapses on UrbanSound8K (domain shift, label mismatch). Monitor per-site alert rate.

### M5 · Speech-Language Models (≈ CS 7–8)

Topics: ASR problem formulation; Whisper (architecture, multilingual); Deep Speech (CTC); WER and CER; speaker identification and diarization; TTS problem formulation; Tacotron; FastSpeech; voice cloning; voice assistants.

| Concept | One-line definition | Analogy |
|---|---|---|
| ASR | Turn speech audio into text | OCR for sound |
| CTC loss | Lets a model align audio frames to text without per-frame labels | Diffing two sequences of different lengths |
| Whisper | Encoder–decoder transformer trained on huge weakly labelled multilingual audio | A general-purpose pretrained API |
| WER / CER | (substitutions + deletions + insertions) ÷ reference words / characters | Edit distance as an error rate |
| Diarization | Working out "who spoke when" | Attributing commits to authors |
| TTS (Tacotron vs FastSpeech) | Text to speech; Tacotron generates step by step, FastSpeech generates in parallel | Sequential vs parallel rendering |
| Voice cloning | Making TTS sound like a specific person from a few samples | Theming a UI from a style guide |

Diagram ideas: ASR pipeline (audio → log-mel → encoder → decoder → text); WER alignment table for "please transfer the funds to my savings account"; Tacotron vs FastSpeech timing diagram.
Scenario step: doctors dictate notes; SoundOps transcribes, attributes speakers and reads back confirmations.
Notebook idea: implement WER with edit distance and assert the endsem example (1 deletion "the" + 1 substitution "savings→saving" = 2/8 = 25%); run `openai-whisper` tiny/base on LibriSpeech samples. Whisper tiny/base runs on CPU; larger models want GPU.
Production angle: Whisper/faster-whisper, pyannote for diarization, cloud TTS. **Breaks:** accented or domain-specific vocabulary (drug names) spikes WER; hallucinated text on silence. Monitor WER on a labelled sample weekly.

### M6 · Music Analysis and Recommendation (≈ CS 9)

Topics: genre classification; music recommendation (collaborative filtering, content-based); evaluation metrics.

| Concept | One-line definition | Analogy |
|---|---|---|
| Genre classification | Predict a music style from audio features | Language detection for code files |
| Spectral centroid / rolloff | "Centre of mass" of the spectrum / frequency below which most energy lies; high = bright | Average vs 85th-percentile latency |
| Collaborative filtering | Recommend what similar users liked | "Customers also bought" |
| Content-based recommendation | Recommend items whose features resemble what you liked | Search by similar tags |
| Cold start | New items or users with no history to learn from | A new service with no metrics yet |
| Audio fingerprinting | Hash of spectrogram peaks to identify an exact recording (Shazam-style) | Content hash / checksum |

Diagram ideas: user–item matrix factorised into two thin matrices; hybrid recommender where content features fill cold-start rows.
Scenario step: SoundOps' sister app recommends calming ward music; new tracks have no plays yet.
Notebook idea: genre classifier on GTZAN features (centroid, ZCR, MFCC means) with sklearn; tiny matrix factorisation with numpy SGD on a toy listen matrix (Lab 7B idea). Laptop.
Production angle: implicit-feedback MF, two-tower models, Spotify-style hybrids. **Breaks:** fingerprints fail on live/cover versions because exact peak positions change. Monitor coverage of new items.

### M7 · Audio Retrieval & Language Models (≈ CS 10)

Topics: audio embeddings; text-to-audio and audio-to-audio similarity search; CLAP; audio captioning; audio question answering.

| Concept | One-line definition | Analogy |
|---|---|---|
| Audio embedding | A fixed-length vector that places similar sounds close together | A semantic hash for search |
| Cosine similarity | Angle-based closeness of two vectors, from −1 to 1 | Matching score in a search engine |
| CLAP | Trains audio and text encoders together so matching pairs land close | CLIP for sound |
| Zero-shot classification | Classify by comparing audio to text prompts, no training labels | Routing by keyword without training a router |
| Audio captioning / QA | Generate a sentence describing audio / answer questions about it | Alt-text generation for sound |

Diagram ideas: shared embedding space with "dog barking" text vector near wolf-howl and child-crying clips (endsem diagnosis question); vector index → top-k → re-rank pipeline.
Scenario step: a nurse searches "alarm beeping near bed 4" across last night's recordings.
Notebook idea: CLAP zero-shot on 20 clips with `laion_clap` or Hugging Face CLAP; build a numpy cosine top-k index; compute precision@k. CPU feasible for small sets.
Production angle: FAISS, pgvector, Qdrant. **Breaks:** biased training captions rank semantically wrong clips higher. Monitor click-through / relevance labels.

### M8 · Audio Generation (≈ CS 11–12)

Topics: WaveNet; GANs for audio (MelGAN); diffusion for audio (DiffWave); text-to-audio (AudioGen); music generation (MusicGen); stem separation. (Older handout also: neural audio codecs.)

| Concept | One-line definition | Analogy |
|---|---|---|
| Autoregressive generation (WaveNet) | Predict the next sample from all previous ones, one at a time | Autocomplete one character at a time |
| Vocoder / GAN (MelGAN) | Turns a mel spectrogram back into a waveform; GAN uses a critic to sharpen output | Code reviewer pushing a junior's output to look real |
| Diffusion (DiffWave) | Start from noise and remove it step by step toward realistic audio | Iterative refactoring from a rough draft |
| Neural audio codec | Compress audio into discrete tokens a language model can generate | gzip that produces tokens |
| MusicGen / AudioGen | Transformer that generates codec tokens from a text prompt | Text-to-image, but for sound |
| Stem separation | Split a mix into vocals, drums, bass, other | Splitting a monolith into services |

Diagram ideas: autoregressive vs diffusion timeline (latency vs length); codec bitrate ladder (1.5 / 6 / 24 kbps) with expected artefacts.
Scenario step: SoundOps generates short spoken and ambient prompts for its kiosks.
Notebook idea: MusicGen-small via AudioCraft or Transformers for a 5 s clip (slow on CPU; GPU recommended); stem separation demo with Demucs. Mark as GPU-preferred.
Production angle: AudioCraft, Demucs, ElevenLabs-style APIs. **Breaks:** latency for long autoregressive outputs; copyright and consent issues. Monitor generation time and abuse reports.

### M9 · Acoustic AI Applications (≈ CS 13)

Topics: acoustics and sound propagation; psychoacoustics; healthcare (respiratory, cardiac, cough); industrial predictive maintenance; specialised applications (underwater, ultrasound).

| Concept | One-line definition | Analogy |
|---|---|---|
| Psychoacoustics | How humans actually perceive loudness and pitch | UX research for ears |
| Anomaly detection (normal-only training) | Learn what "normal" sounds like and flag large deviations | Alert on metrics outside the usual band |
| Reconstruction error threshold | Autoencoder error above a percentile of normal data = anomaly | p99 latency alert |
| Domain shift | Deployment audio differs from training audio (new machine, new room) | Prod traffic unlike staging |
| Cough / respiratory detection | Classify cough, wheeze, crackle from chest or room audio | Classifying error types in logs |

Diagram ideas: autoencoder anomaly pipeline with threshold set at p99 of normal errors; lab vs factory domain-shift diagram.
Scenario step: SoundOps flags a failing pump before it breaks and detects coughing fits in a ward.
Notebook idea: train a small dense autoencoder on log-mel frames of "normal" MIMII/DCASE pump audio, set threshold from normal-only validation, evaluate AUC. CPU OK.
Production angle: edge inference, per-machine thresholds. **Breaks:** new valve model → false-positive spike (endsem). Recheck normalisation and threshold before retraining.

### M10 · Agentic AI for Audio (≈ CS 14)

Topics: audio perception–reasoning–action loops; RAG for audio; voice agents and conversational AI.

| Concept | One-line definition | Analogy |
|---|---|---|
| Agent | An LLM that decides which tool to call next, observes the result, and repeats | An orchestrator service calling microservices |
| ReAct | Interleave reasoning steps with tool calls | Debugging: think, run a command, read output, repeat |
| Audio RAG | Retrieve relevant audio/transcripts, then let an LLM answer using them | Search + summarise over call recordings |
| Voice agent | Speech in → ASR → LLM → TTS → speech out, in real time | A phone IVR with a brain |
| Guardrail | A check that blocks or corrects an unsafe or wrong agent step | Input validation and circuit breakers |

Diagram ideas: meeting-to-action-items tool-call graph (diarize → transcribe → summarise → extract owners); voice-agent latency budget bar.
Scenario step: SoundOps turns a recorded shift handover into action items with owners and deadlines.
Notebook idea: chain Whisper (tiny) → simple diarization stub → an LLM or rule-based extractor → JSON action items; add schema validation as a guardrail. CPU; LLM via any API or a local small model.
Production angle: LiveKit/Pipecat-style voice stacks, function calling. **Breaks:** diarization errors assign tasks to the wrong person; hallucinated deadlines. Guardrails: confidence thresholds and human review.

### M11 · Ethics and Privacy in Audio AI (≈ CS 15; CS 16 review)

Topics: deepfake detection and audio forensics; privacy and surveillance; responsible AI for audio generation.

| Concept | One-line definition | Analogy |
|---|---|---|
| Audio deepfake | Synthetic speech made to sound like a real person | Phishing email spoofing a known sender |
| Deepfake detector | Classifier spotting artefacts of synthetic audio | Spam filter |
| Watermarking | Hidden signal in generated audio that marks it as synthetic | Signed commits |
| Privacy by design | Process on-device, keep features not raw audio, minimise retention | Storing hashed passwords, not plaintext |

Diagram ideas: threat model of a voice-cloning fraud call; on-device vs cloud privacy data-flow.
Scenario step: SoundOps must prove it doesn't store raw ward conversations and can detect cloned voices.
Notebook idea: train a logistic-regression detector on MFCC stats of real vs TTS-generated clips from M5. Laptop.
Production angle: consent logs, retention policies, watermarking. **Breaks:** detector trained on one TTS engine misses a new one. Monitor with fresh synthetic samples.

---

## 5. Codebase plan

`codebase/` — **soundops**: a small audio pipeline library + CLI. Python, librosa, numpy, sklearn, torch (CPU), optional transformers/whisper.

```
codebase/
├── README.md                    run instructions, module → file map            (M1)
├── soundops/
│   ├── io.py                    load/resample/mono, format checks              (M1)
│   ├── features.py              STFT, mel, MFCC, ZCR, RMS, centroid            (M2)
│   ├── embed.py                 YAMNet/AST/CLAP embedding wrappers             (M3, M7)
│   ├── classify.py              clip classifier + SED thresholding             (M4)
│   ├── metrics.py               precision/recall/F1, WER/CER, precision@k      (M4, M5, M7)
│   ├── asr.py                   Whisper wrapper + diarization stub             (M5)
│   ├── recommend.py             matrix factorisation + content hybrid          (M6)
│   ├── search.py                cosine top-k index for text→audio              (M7)
│   ├── anomaly.py               autoencoder, normal-only threshold             (M9)
│   └── agent.py                 meeting → action items with JSON guardrail     (M10)
├── cli.py                       `soundops classify|transcribe|search file.wav` (M4–M10)
└── tests/
    ├── test_features.py         resolution maths, shapes, sample rate          (M2)
    ├── test_metrics.py          siren confusion matrix, WER example            (M4, M5)
    └── test_anomaly.py          threshold flags injected fault                 (M9)
```

---

## 6. Practice topics plan

01 Sampling, aliasing and the STFT trade-off — M1, M2 — 5 h
02 Feature extraction: ZCR, RMS, centroid, MFCC, chroma — M2 — 5 h
03 Classic ML vs CNN vs pretrained transformers — M3 — 6 h
04 Classification, tagging, SED and metrics — M4 — 4 h
05 ASR and TTS: Whisper, CTC, WER, diarization — M5 — 6 h
06 Music: genre, recommendation, fingerprinting — M6 — 4 h
07 Audio search with embeddings and CLAP — M7 — 4 h
08 Audio generation: autoregressive, GAN, diffusion, codecs — M8 — 4 h
09 Acoustic anomaly detection — M9 — 4 h
10 Audio agents, privacy and deepfakes — M10, M11 — 5 h

---

## 7. Exam signal

Past papers (2025-26 Sem 2, older handout) exist for midsem and endsem, 2 sets each.
- **Midsem (closed book, 30%)**: 6 questions × 5 marks. Every question opens with a short scenario, then a computation or comparison (3 marks) and an "evaluate this decision" part (2 marks). One question is **find-the-bug in librosa code**.
- **Endsem (open book, 40%)**: 4 questions × 10 marks (3 + 3 + 4). Numericals (aliasing, SQNR, WER, confusion-matrix metrics, cosine ranking) plus design questions (edge pipeline, anomaly detector, audio agent with failure modes and guardrails).

Repeating themes:
1. **STFT resolution maths**: frequency resolution = sr / n_fft, time resolution = hop / sr (or window / sr); can it resolve an 8 ms event or notes 20 Hz apart?
2. **Feature reading**: ZCR + RMS → silence/noise/tone; low vs high MFCCs; centroid + rolloff → flute vs hi-hat; genre profiles.
3. **Metrics**: precision/recall/F1 for a rare class; WER with substitutions/deletions/insertions; CER vs WER.
4. **Model choice with little data**: SVM vs k-NN on edge; CNN vs LSTM; scratch vs fine-tune vs zero-shot (Whisper/Wav2Vec2/AST); freeze vs unfreeze.
5. **Systems design**: always-on edge pipeline, normal-only anomaly detector, hybrid recommender for cold start, audio agent with 2 failure modes + guardrails.

---

## 8. Interview angle

1. **What does a mel spectrogram give you over raw audio?** — A compact time–frequency picture on a perceptual scale that CNNs and transformers learn from easily.
2. **Window size trade-off in STFT?** — Longer windows give finer frequency detail but blur timing; shorter windows do the opposite.
3. **Why might accuracy be misleading for an alarm detector?** — With rare events, predicting "no alarm" scores high accuracy; report precision, recall and F1.
4. **How is WER computed?** — Edit distance (substitutions + deletions + insertions) between hypothesis and reference, divided by reference word count.
5. **Whisper vs a CTC model like Deep Speech?** — Whisper is an encoder–decoder trained on huge weakly labelled data (robust, multilingual, can hallucinate); CTC models are simpler, streaming-friendly, need cleaner labels.
6. **You have 500 labelled clips. What do you do?** — Use pretrained embeddings (YAMNet/AST/Wav2Vec2) with a small head, add augmentation, avoid fully unfreezing.
7. **How do you detect machine faults with no fault data?** — Train an autoencoder on normal audio and flag reconstruction error above a percentile of normal.
8. **What is CLAP and what does it enable?** — Joint audio–text embeddings: zero-shot classification and text-to-audio search.
9. **What breaks when an audio model goes to production?** — Mic/room/sample-rate differences (domain shift), clipping, background noise; monitor feature drift and per-site alert rates.
10. **Design a voice agent's latency budget.** — Streaming ASR, short LLM turns, streaming TTS; target under ~1 s to first audio; cut with smaller models and partial results.

---

## 9. Repetition plan

| Concept | First met | Revisited in |
|---|---|---|
| Sampling rate / Nyquist | M2 | M3 (input resampling), M9 (edge budget), M11 (forensics) |
| Spectrogram / mel | M2 | M3, M4, M5, M8 (vocoder input) |
| MFCC | M2 | M4, M6 (genre), M11 (deepfake features) |
| Transfer learning | M3 | M4, M5, M7, M9 |
| Embedding + cosine similarity | M3 | M6 (content-based), M7, M10 (audio RAG) |
| Precision / recall / F1 | M4 | M5 (WER companion), M7 (precision@k), M9 (anomaly), M11 |
| Domain shift | M3 | M4 (ESC-50 → UrbanSound8K), M5 (accents), M9 (new valve) |
| Pipeline guardrails | M5 | M10, M11 |

---

## 10. Overlap with my other courses

- [../../natural-language-processing/](../../natural-language-processing/) — edit distance (WER), sequence models, transformers, attention.
- [../../llm-engineering/](../../llm-engineering/) — agents, tool calling, RAG, embeddings (M7, M10).
- [../../nlp-applications/](../../nlp-applications/) — conversational AI and speech-to-text applications.
- [../../machine-learning-on-the-edge/](../../machine-learning-on-the-edge/) — always-on, battery-powered classifiers (endsem baby-cry vs smoke-alarm design, wake-word 1-D CNN).
- [../../software-engineering-for-machine-learning/](../../software-engineering-for-machine-learning/) — monitoring, drift, training–serving skew.
- Sibling elective [../speech-processing/](../speech-processing/) — deeper ASR/TTS theory.

---

## 11. Build checklist

- [ ] SPEC reviewed
- [ ] cards.json (M1, M2, M3, M4, M5, M6, M7, M8, M9, M10, M11)
- [ ] practice/01 Sampling, aliasing and STFT
- [ ] practice/02 Feature extraction
- [ ] practice/03 Classic ML vs CNN vs pretrained transformers
- [ ] practice/04 Classification, tagging, SED and metrics
- [ ] practice/05 ASR and TTS
- [ ] practice/06 Music analysis and recommendation
- [ ] practice/07 Audio search with CLAP
- [ ] practice/08 Audio generation
- [ ] practice/09 Acoustic anomaly detection
- [ ] practice/10 Audio agents, privacy and deepfakes
- [ ] codebase/ runs + tests

**Total estimated study hours: ≈ 60 h** (47 h practice topics + 8 h codebase + 5 h past-paper drills).
