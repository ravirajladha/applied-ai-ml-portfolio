# Computational Photography (AIMLC ZG541) — Study spec

> How a phone turns a noisy RAW sensor dump into a great photo: colour science, the ISP pipeline, deblurring, edge-aware filters, HDR, deep-learning ISP stages and depth. · Status: spec only (not built yet)

---

## 1. What it is and why an AI engineer should care

A modern phone photo is mostly software: the sensor captures a noisy, single-colour-per-pixel RAW image, and an **image signal processor (ISP)** plus learned models turn it into the picture you see.
This course starts with how eyes and colour spaces work, builds the camera and ISP pipeline (white balance, demosaicing, denoising, tone mapping, super-resolution, alignment), then covers deblurring, edge-aware filtering, HDR and coded photography, deep-learning replacements for ISP stages (UNet), and depth ("shape from X": focus stacks, stereo, time-of-flight).
For an AI engineer it is a concrete case study of **classic pipeline vs learned pipeline**, data generation for image-to-image models, and shipping vision models on device.

**Job relevance: 2/5** — camera/ISP and imaging teams (phones, drones, cars) hire for this, but it is a narrow niche; image-to-image deep learning skills transfer more widely.

---

## 2. Sources in this folder

| Kind | File (relative path) | Notes |
|---|---|---|
| Handout (older batch) | `handouts/Older batch - Computational Photography (S2-25_AIMLCZG541) COURSE HANDOUT.docx` | v2.0 dated 15-12-2025, Second Semester 2025-26, author Prof. Raghavendra Singh; 8 modules, 16 contact sessions (CS), 5 labs |

**Gaps:** handout only, and from an older batch (no current-term handout). No slides, past papers, lab sheets or books. The experiential-learning objective says "fundamental NLP algorithms" (apparent copy-paste in the handout). CS 14 lists "Deconvolution with Gaussian Splatting" without detail. Hours per session: not stated.

Note: Computational Imaging (`../computational-imaging/`, same author) repeats much of M2–M7 here and adds medical and remote-sensing imaging.

---

## 3. Running scenario

**PixelNight** is the camera-software team at a mid-range Android phone maker. Their phones have a small, noisy sensor; reviews complain about dull colours, blurry night shots, blown-out skies and fake-looking portrait blur.
The goal for the next release: a better **RAW-to-JPEG pipeline** (accurate colour, clean night shots, sharp handheld photos, HDR skies) and a **portrait mode** with real depth.
Data: public RAW datasets (e.g. MIT-Adobe FiveK, SIDD smartphone denoising samples) and a few bracketed/focus-stack sequences shot on any phone in Pro/RAW mode.
Each module upgrades one stage of PixelNight's pipeline, and a before/after test gallery tracks progress.

---

## 4. Module map

Module names and order from the handout's Modular Content Structure; sessions from Part B.

### M1 · Anatomy of an Eye — colour theory and colour spaces (≈ CS 1–3)

Topics: what computational photography is and its applications; perception of colour, depth, contrast, resolution; colour theory; CIE 1931 XYZ and its derivatives (sRGB, L\*a\*b\*, YUV); colour transforms on camera phones.

| Concept | One-line definition | Analogy |
|---|---|---|
| Cones / trichromacy | The eye has three colour receptors, so any colour is three numbers | A 3-field schema for colour |
| CIE XYZ | A device-independent reference space for all visible colours | A canonical data format everyone converts through |
| sRGB | The standard colour space screens and the web assume, with gamma | The default locale everyone renders in |
| L\*a\*b\* | Colour space where equal distances look equally different to humans | A metric designed for perceived similarity |
| YUV | Brightness (Y) separated from colour (U, V); used for compression | Separating hot and cold data |
| Gamma | Non-linear encoding so dark tones get more precision | Log-scale storage of values |

Diagram ideas: CIE chromaticity horseshoe with the sRGB triangle; conversion chain camera RGB → XYZ → sRGB; same image split into Y, U, V channels.
Scenario step: PixelNight fixes "dull colours" by getting the colour pipeline right.
Notebook idea: convert an image between sRGB, linear RGB, XYZ, L\*a\*b\* and YUV with scikit-image/OpenCV; compute ΔE between two patches. Laptop.
Production angle: colour-managed pipelines, ICC profiles. **Breaks:** skipping linearisation before maths makes blends and white balance look wrong.

### M2 · Anatomy of a Camera (ISP) — optics, exposure, image formation (≈ CS 4)

Topics: ray optics, aperture, depth of field, exposure, sensor, noise; the physics of light and camera models; image formation and the imaging pipeline.

| Concept | One-line definition | Analogy |
|---|---|---|
| Pinhole / thin-lens model | Simple maths for how scene points map to sensor points | An API contract for projection |
| Aperture (f-number) | Lens opening; wider = more light, shallower depth of field | Wider cache = more hits, less precision |
| Shutter / ISO | Exposure time / sensor gain; long time blurs motion, high gain amplifies noise | Longer polling vs louder logging |
| Exposure triangle | Aperture, shutter and ISO trade off brightness, blur and noise | Latency, throughput and cost trade-off |
| Sensor noise (shot, read) | Photon randomness that grows with signal + fixed electronic noise | Variable vs fixed overhead |

Diagram ideas: exposure triangle; thin-lens diagram with circle of confusion; noise vs brightness curve.
Scenario step: PixelNight decides exposure settings for night mode before any processing.
Notebook idea: simulate exposure: scale a linear image by time × gain, add Poisson + Gaussian noise, plot SNR vs ISO. numpy, laptop.
Production angle: auto-exposure algorithms, sensor calibration. **Breaks:** auto-exposure hunting in flickering LED light.

### M3 · Image Sensing Processor (ISP) pipeline (≈ CS 5–6)

Topics: computational colour constancy (auto white balance); colorimetric conversion; image demosaicing; image denoising; tone mapping; super-resolution; image alignment and registration.

| Concept | One-line definition | Analogy |
|---|---|---|
| ISP | Ordered stages that turn RAW sensor data into a display-ready image | An ETL pipeline for pixels |
| Auto white balance | Estimate the light colour and cancel it so whites look white | Removing a constant bias |
| Gray-world assumption | Assume the scene averages to gray, scale channels to match | Normalising by the mean |
| Colour correction matrix | 3×3 matrix mapping camera RGB to a standard space | A schema migration |
| Demosaicing | Fill in the two missing colours at every Bayer pixel | Imputing missing columns |
| Super-resolution | Produce a higher-resolution image from one or several low-res inputs | Upsampling a time series with a smart model |
| Alignment / registration | Shift or warp frames so they line up before merging | Aligning logs from servers with clock skew |

Diagram ideas: full ISP flowchart with stage order; Bayer tile → bilinear demosaic; burst frames aligned then merged.
Scenario step: PixelNight rebuilds the ISP stage by stage so each can be swapped for a better version.
Notebook idea: RAW (rawpy) → black level → gray-world AWB → bilinear demosaic → CCM → gamma; compare against the camera JPEG (handout Labs 1–2). Laptop.
Production angle: Qualcomm Spectra, Google HDR+ burst pipeline. **Breaks:** stage order bugs (white balance after gamma) and zipper artefacts at edges.

### M4 · Deconvolution and Deblurring (≈ CS 7, 9; CS 8 review)

Topics: natural image priors; blind deconvolution; efficient deconvolution with image priors; Alternating Direction Method of Multipliers (ADMM).

| Concept | One-line definition | Analogy |
|---|---|---|
| Blur kernel / PSF | How a single point of light gets smeared (shake, defocus) | A smoothing function applied to every value |
| Deconvolution | Undo a known blur | Reversing a known transformation |
| Wiener filter | Deconvolution that holds back where noise is larger than signal | Inverse with a safety margin |
| Natural image prior | Real photos have sparse gradients (mostly flat, few sharp edges) | Validation rule: most diffs are small |
| Blind deconvolution | Estimate both blur kernel and sharp image | Debugging with both the input and the bug unknown |
| ADMM | Split a hard optimisation into easy steps that alternate until they agree | Splitting a job across services that sync state |

Diagram ideas: motion-blur kernel shape; gradient histogram (heavy-tailed) of sharp vs blurred images; ADMM three-step loop.
Scenario step: handheld night shots are smeared by shake; PixelNight adds deblur.
Notebook idea: blur with a known motion kernel; implement Wiener (numpy FFT) and TV-regularised deconvolution with a short ADMM loop; compare PSNR. Laptop.
Production angle: gyro-assisted deblur on phones. **Breaks:** wrong kernel → ringing halos.

### M5 · Edge-aware Filtering (≈ CS 10)

Topics: bilateral filtering, non-local means.

| Concept | One-line definition | Analogy |
|---|---|---|
| Edge-aware filter | Smooths flat areas but stops at edges | Smoothing a metric without flattening real incidents |
| Bilateral filter | Weights neighbours by distance and by brightness similarity | Averaging only with similar peers |
| Non-local means | Averages pixels whose surrounding patches look alike, anywhere | Deduplicating similar records across the DB |
| Detail / base decomposition | Split an image into smooth base and fine detail layers | Separating trend from noise |

Diagram ideas: bilateral weight = spatial Gaussian × range Gaussian at an edge; base/detail split used for local tone mapping.
Scenario step: noise reduction that keeps hair and text sharp.
Notebook idea: compare Gaussian, bilateral and NL-means (OpenCV) on a noisy photo with PSNR/SSIM; do base/detail enhancement (handout Lab 3 includes bilateral filtering and motion deblurring). Laptop.
Production angle: fast approximations (bilateral grid, guided filter). **Breaks:** waxy "plastic skin" from over-filtering.

### M6 · Great ideas in computational photography (≈ CS 11–12)

Topics: HDR, tone mapping, coded aperture, flutter shutter.

| Concept | One-line definition | Analogy |
|---|---|---|
| HDR merge | Combine bracketed exposures into one image covering all brightness levels | Merging partial views into one complete record |
| Camera response curve | How sensor values map to real light; needed to merge exposures | Calibration table for a sensor |
| Tone mapping (global/local) | Compress HDR into display range, one curve for all vs per region | One-size config vs per-tenant config |
| Coded aperture | Patterned lens mask so defocus blur is easier to invert and encodes depth | Adding checksums to make recovery possible |
| Flutter shutter | Shutter flickers in a code so motion blur keeps all frequencies | Encoding data with a known pattern |

Diagram ideas: bracket → radiance map → tone-mapped image; box vs coded shutter frequency response.
Scenario step: "blown-out skies" bug: PixelNight ships HDR.
Notebook idea: OpenCV Debevec merge + Reinhard/Mantiuk tone map on a 3-shot bracket (handout Lab 4). Laptop.
Production angle: HDR+ burst merge, Smart HDR. **Breaks:** ghosting from moving people; halos from local tone mapping.

### M7 · Deep Learning for ISP (≈ CS 13–14)

Topics: deep learning review; AI-based methods targeting individual ISP components; UNet; applications; deconvolution with Gaussian splatting (named only).

| Concept | One-line definition | Analogy |
|---|---|---|
| Learned ISP stage | A network replacing one hand-tuned stage (denoise, demosaic, AWB) | Swapping one microservice for an ML service |
| End-to-end learned ISP | One network maps RAW straight to the final image | Replacing the whole pipeline with one model |
| UNet | Encoder–decoder with skip connections for pixel-to-pixel tasks | Summary plus original attached to each reply |
| Paired training data | (bad input, good target) image pairs, often synthesised | Golden test fixtures |
| Perceptual loss | Compare deep features, not just pixels, so results look natural | Judging by meaning, not exact string match |

Diagram ideas: classic ISP with one box replaced by a CNN; UNet shape; synthetic data generation loop (clean → add noise/blur → pair).
Scenario step: PixelNight trains a small UNet denoiser for night mode.
Notebook idea: train a tiny UNet on 64×64 synthetic noisy/clean patches with PyTorch; compare PSNR to NL-means (handout Lab 5). CPU feasible at small scale; GPU/Colab faster.
Production angle: on-device inference via Core ML / TFLite / NNAPI. **Breaks:** synthetic noise ≠ real sensor noise; model slow or hot on device.

### M8 · Shape from X (≈ CS 15; CS 16 review)

Topics: focus stack, stereo multi-view, time-of-flight imaging.

| Concept | One-line definition | Analogy |
|---|---|---|
| Depth from focus | For each pixel, find the focus setting where it is sharpest | Binary search for the best setting |
| Stereo disparity | Depth from how far a point shifts between two cameras | Parallax: near things move more |
| Time-of-flight | Depth from light round-trip time | Ping round-trip time |
| Synthetic bokeh | Blur the background using a depth map to mimic a big lens | Applying a filter based on a mask |

Diagram ideas: focus-stack sharpness curve; stereo triangle with baseline and disparity; depth-map → blur-strength map.
Scenario step: portrait mode with real depth instead of a cut-out mask.
Notebook idea: depth from focus with Laplacian variance on a focus stack; OpenCV `StereoSGBM` on a Middlebury pair; depth-based background blur. Laptop.
Production angle: dual-pixel depth, phone LiDAR/ToF. **Breaks:** hair and glass edges; textureless walls.

---

## 5. Codebase plan

`codebase/` — **pixelnight**: a modular RAW-to-JPEG pipeline where each stage can be swapped. numpy, scipy, OpenCV, scikit-image, rawpy; torch (CPU) for M7.

```
codebase/
├── README.md                 run instructions, module → file map              (M1)
├── pixelnight/
│   ├── color.py              sRGB/linear/XYZ/Lab/YUV conversions, ΔE          (M1)
│   ├── sensor.py             exposure + noise simulation                      (M2)
│   ├── isp.py                black level, AWB, demosaic, CCM, gamma pipeline  (M3)
│   ├── align.py              burst alignment                                  (M3)
│   ├── deblur.py             Wiener + TV-ADMM                                 (M4)
│   ├── filters.py            bilateral, NL-means, base/detail                 (M5)
│   ├── hdr.py                merge + tone mapping                             (M6)
│   ├── learned.py            tiny UNet denoiser + training script             (M7)
│   └── depth.py              depth from focus, stereo, synthetic bokeh        (M8)
├── run_pipeline.py           RAW in → JPEG out with chosen stages             (M3–M8)
└── tests/
    ├── test_color.py         round-trip conversions within tolerance          (M1)
    ├── test_isp.py           output shape, range, gray patch stays gray       (M3)
    └── test_restore.py       deblur/denoise improve PSNR                      (M4, M5, M7)
```

---

## 6. Practice topics plan

01 Colour science and colour spaces — M1 — 4 h
02 Camera, exposure and sensor noise — M2 — 3 h
03 Build an ISP from RAW — M3 — 6 h
04 Deconvolution, priors and ADMM — M4 — 5 h
05 Edge-aware filtering — M5 — 3 h
06 HDR, tone mapping, coded photography — M6 — 4 h
07 Deep learning for ISP (UNet) — M7 — 5 h
08 Shape from X and portrait mode — M8 — 3 h

---

## 7. Exam signal

No past papers in this folder. Evaluation scheme (older handout):

| Component | Type | Duration | Weight | Date (that term) |
|---|---|---|---|---|
| EC-1(a) Quizzes | Online | 1 week | 10% | TBA |
| EC-1(b) Assignments | Take home | 10 days | 20% | TBA |
| EC-2 Mid-semester | Closed book | 2 h | 30% | 21-06-2026 (FN) |
| EC-3 Comprehensive | Open book | 2.5 h | 40% | 06-09-2026 (FN) |

Midsem syllabus: CS 1–8 (M1–M4 first half). Comprehensive: all topics. Question style: not stated.

---

## 8. Interview angle

1. **Walk me through a camera ISP.** — Black level, demosaic, white balance, colour correction, denoise, tone map, sharpen, compress.
2. **Why work in linear RGB before gamma?** — Physical operations (blending, white balance, HDR merge) are only correct on linear light values.
3. **How does auto white balance work?** — Estimate the illuminant (gray-world, white-patch or learned) and scale channels to cancel it.
4. **Bilateral filter in one sentence?** — A blur that weights neighbours by both distance and brightness similarity, so edges survive.
5. **How does HDR+ style burst photography work?** — Capture many short frames, align them, merge to cut noise, then tone-map.
6. **Classic ISP stage vs learned stage — trade-offs?** — Learned is often better quality but needs paired data, compute and careful testing on real sensor noise.
7. **How does portrait mode get depth?** — Stereo/dual-pixel disparity, ToF, or monocular depth networks, then depth-dependent blur.
8. **What goes wrong shipping an image model on a phone?** — Latency, heat and memory limits; domain gap between training and real sensor data.

---

## 9. Repetition plan

| Concept | First met | Revisited in |
|---|---|---|
| Linear light vs gamma | M1 | M3, M6 |
| Sensor noise model | M2 | M3 (denoise), M5, M7 (synthetic data) |
| ISP pipeline order | M3 | M6 (HDR), M7 (learned stages) |
| Convolution / blur kernel | M4 | M5, M6 (coded aperture), M7 (CNN), M8 (bokeh) |
| Image prior / regularisation | M4 | M5, M7 (learned prior) |
| PSNR / SSIM | M3 | M4, M5, M7 |
| Alignment / registration | M3 | M6 (HDR ghosting), M8 (stereo) |

---

## 10. Overlap with my other courses

- [../../machine-learning-on-the-edge/](../../machine-learning-on-the-edge/) — running learned ISP stages on phone hardware.
- Sibling electives: [../computational-imaging/](../computational-imaging/) (same author; overlapping M2–M7) and [../3d-computer-vision/](../3d-computer-vision/) (stereo and depth for M8).
- No real overlap with the LLM, NLP or RL courses.

---

## 11. Build checklist

- [ ] SPEC reviewed
- [ ] cards.json (M1, M2, M3, M4, M5, M6, M7, M8)
- [ ] practice/01 Colour science and colour spaces
- [ ] practice/02 Camera, exposure and sensor noise
- [ ] practice/03 Build an ISP from RAW
- [ ] practice/04 Deconvolution, priors and ADMM
- [ ] practice/05 Edge-aware filtering
- [ ] practice/06 HDR, tone mapping, coded photography
- [ ] practice/07 Deep learning for ISP
- [ ] practice/08 Shape from X and portrait mode
- [ ] codebase/ runs + tests

**Total estimated study hours: ≈ 41 h** (33 h practice topics + 8 h codebase).
