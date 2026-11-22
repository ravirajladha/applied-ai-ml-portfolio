# Computational Imaging (AIMLC ZG542) — Study spec

> How cameras, CT scanners and satellites turn raw sensor measurements into clean images by modelling the physics and solving "undo the blur and noise" problems with classic maths and deep learning. · Status: spec only (not built yet)

---

## 1. What it is and why an AI engineer should care

Every imaging device measures a distorted version of the scene: blurred by optics, corrupted by sensor noise, sampled incompletely (a CT scanner only sees projections, a satellite sees through haze).
Computational imaging writes that distortion down as a **forward model** (y = A·x + noise) and then solves the **inverse problem**: recover x from y.
This course walks that idea through phone cameras (ISP, HDR, denoising, deblurring), medical imaging (X-ray, CT reconstruction), remote sensing (geometric and atmospheric correction) and deep learning (CNN/UNet denoisers, diffusion-model priors).
The transferable skill for an AI engineer is framing a problem as "known corruption + prior knowledge → best guess", which is exactly how modern image restoration and generative models work.

**Job relevance: 2/5** — real but niche: phone camera teams, medical-imaging AI, satellite analytics. The deep-learning restoration and diffusion parts transfer to general computer vision work.

---

## 2. Sources in this folder

| Kind | File (relative path) | Notes |
|---|---|---|
| Handout (current) | `handouts/Handout - CI - 28-Jul-2026.docx` | v2.0, First Semester 2026-27, author Prof. Raghavendra Singh; 16 contact sessions (CS), 5 labs, evaluation scheme |

**Gaps:** handout only. No slides, past papers, lab sheets or books. The course description also mentions light-field imaging, compressive sensing, spectral imaging, microscopy and video/motion, but **none of these appear in the 16-session plan**; this spec follows the session plan. The experiential-learning objective says "fundamental NLP algorithms" (an apparent copy-paste in the handout), and the lab "Module" column (3, 5, 9, 11, 14) does not match the module structure cleanly. Hours per session: not stated.

Note: Computational Photography (`../computational-photography/`, same author) shares most of M1–M5 of this course.

---

## 3. Running scenario

**LumaLab** sells an image-restoration SDK. Its single core engine models every device as *y = A·x + noise* and solves for the clean image x.
Three customers use it: a **phone maker** (RAW photos at night: noisy, shaky, high dynamic range), a **diagnostic-imaging chain** (low-dose X-ray and CT scans to reconstruct), and an **agri-analytics firm** (satellite tiles that need geometric and haze correction before crop analysis).
Data stand-ins: RAW sample photos (rawpy), the Shepp–Logan CT phantom (scikit-image), and public Sentinel-2 / Landsat tiles.
Each module adds one capability to the LumaLab engine, moving from "understand the camera" to "plug in a learned prior".

---

## 4. Module map

Module names follow the handout's Modular Content Structure; sessions from Part B. M8 appears only in the session plan.

### M1 · Anatomy of a Camera (ISP) — image formation and the imaging pipeline (≈ CS 1–2)

Topics: digital photography; perception of colour, depth, contrast, resolution; ray optics, aperture, depth of field, exposure, sensor, noise; physics of light and camera models; image formation and the imaging pipeline; camera ISP, demosaicking.

| Concept | One-line definition | Analogy |
|---|---|---|
| Image formation | Light from the scene passes through a lens and lands on a sensor grid | A render pipeline from 3D scene to pixels |
| Aperture / depth of field | Lens opening size; bigger opening = more light but thinner sharp zone | Wide search = more results, less precision |
| Exposure | Total light collected: aperture × shutter time × sensor gain | Throughput = rate × time window |
| RAW image | Unprocessed sensor values, one colour per pixel, before any cleanup | Raw event logs before ETL |
| Bayer pattern / demosaicking | Sensor pixels each see one colour; demosaicking fills in the missing two | Interpolating missing metrics |
| ISP (image signal processor) | Fixed pipeline: black level, demosaic, white balance, denoise, colour, tone, compress | An ETL pipeline for pixels |
| Forward model y = A·x + n | Maths description of how the device distorts the true image | A spec of how the system corrupts data |

Diagram ideas: lens/aperture ray diagram with depth-of-field band; ISP as a box-and-arrow pipeline from RAW to JPEG; Bayer RGGB tile.
Scenario step: LumaLab reads the phone's RAW files and rebuilds a minimal ISP so later modules can swap stages.
Notebook idea: read a RAW (DNG) with rawpy, apply black level, bilinear demosaic, gray-world white balance, gamma; compare to the camera JPEG (handout Lab 1). Laptop.
Production angle: Qualcomm/Apple ISPs, libraw, Halide. **Breaks:** wrong white balance under mixed lighting; ISP tuned for one sensor breaks on a new one.

### M2 · Great ideas in computational photography (≈ CS 3)

Topics: HDR, tone mapping, coded aperture, flutter shutter.

| Concept | One-line definition | Analogy |
|---|---|---|
| Dynamic range | Ratio between the brightest and darkest detail a sensor can record | Range of a numeric type |
| HDR merge | Combine several exposures into one image with full range | Merging partial logs into one complete view |
| Tone mapping | Squeeze HDR values into a screen's limited range while keeping detail | Log scale on a dashboard |
| Coded aperture | A patterned mask in the lens so blur is easier to undo later | Adding checksums to make recovery possible |
| Flutter shutter | Open/close the shutter in a code during exposure so motion blur is invertible | Sending data with a known pattern to aid decoding |

Diagram ideas: exposure bracket → radiance map → tone-mapped output; box-blur vs coded-blur frequency spectra (zeros vs no zeros).
Scenario step: the phone customer wants backlit portraits without blown-out skies.
Notebook idea: merge 3 bracketed exposures with OpenCV (`createMergeDebevec`), tone-map with Reinhard; plot histograms. Laptop.
Production angle: Google HDR+, Apple Smart HDR. **Breaks:** ghosting when people move between exposures.

### M3 · Denoising, and Noise and Edge-aware Filtering (≈ CS 4–5)

Topics: noise profile and types; kernel methods (smoothing, bilateral filter, non-local means); BM3D; wavelets and soft thresholding.

| Concept | One-line definition | Analogy |
|---|---|---|
| Shot vs read noise | Random photon arrival (grows with signal) vs sensor electronics noise (constant) | Traffic-dependent jitter vs fixed baseline jitter |
| Gaussian smoothing | Replace each pixel by a weighted average of neighbours; also blurs edges | Moving average on a metric |
| Bilateral filter | Average only neighbours that are close *and* similar in brightness, so edges survive | Smoothing that ignores outliers across a step change |
| Non-local means | Average pixels whose surrounding patches look alike, anywhere in the image | Deduplicating similar records across the whole DB |
| BM3D | Group similar patches into stacks, denoise each stack jointly in a transform domain | Batch-processing similar tickets together |
| Wavelet soft thresholding | Transform, shrink small coefficients toward zero, transform back | Dropping low-signal features |

Diagram ideas: noise vs signal curve (shot noise ∝ √signal); bilateral weight = spatial × range kernels; BM3D patch grouping.
Scenario step: night photos and low-dose X-rays are grainy; LumaLab adds a denoising stage.
Notebook idea: add Gaussian + Poisson noise to an image; compare Gaussian, bilateral, NL-means (OpenCV/scikit-image), wavelet thresholding (PyWavelets) by PSNR/SSIM. Laptop.
Production angle: BM3D-class denoisers, learned denoisers on phones. **Breaks:** over-smoothing removes real texture (or a small lesion in medical images). Monitor PSNR/SSIM plus human review.

### M4 · Deconvolution and Deblurring (≈ CS 6, 8; CS 7 review)

Topics: natural image priors; blind deconvolution; efficient deconvolution with image priors; Alternating Direction Method of Multipliers (ADMM).

| Concept | One-line definition | Analogy |
|---|---|---|
| Convolution / PSF | Blur = each point spread by a kernel (point spread function) | A smoothing function applied to every value |
| Inverse filter | Divide by the blur in the frequency domain; explodes noise | Dividing by near-zero numbers |
| Wiener filter | Inverse filter that backs off where noise dominates | Inverting with a safety margin |
| Image prior | Assumption about what natural images look like (e.g. mostly smooth, sparse edges) | Validation rules on input data |
| Regularisation (e.g. total variation) | Penalty added to the fit so the answer obeys the prior | L2 penalty on model weights |
| Blind deconvolution | Estimate both the sharp image and the unknown blur kernel | Debugging with both the bug and the input unknown |
| ADMM | Split a hard optimisation into easy alternating steps that agree at the end | Divide a big job into services that sync state |

Diagram ideas: blur kernel in space and frequency; inverse vs Wiener vs TV-regularised results; ADMM loop (x-step, z-step, dual update).
Scenario step: handheld night shots are blurred by shake; LumaLab adds a deblur stage.
Notebook idea: blur with a known motion kernel + noise; implement inverse, Wiener (numpy FFT) and TV-regularised deconvolution via a short ADMM loop; compare PSNR (handout Lab 2). Laptop.
Production angle: phone stabilisation + deblur, astronomy pipelines. **Breaks:** wrong kernel estimate creates ringing artefacts.

### M5 · Deep Learning for imaging (≈ CS 9–10, 15)

Topics: MLPs, CNNs, ResNets review; denoising with CNNs; solving inverse problems with neural networks (UNet, deconvolution with CNNs); AI methods targeting individual ISP components; introduction to diffusion models (score-based generative modelling, image generation, solving inverse problems with diffusion-model priors).

| Concept | One-line definition | Analogy |
|---|---|---|
| CNN denoiser | Network trained on (noisy, clean) pairs to output the clean image | Learned replacement for a hand-written filter |
| Residual learning | Predict the noise and subtract it, instead of the full image | Shipping a diff instead of the whole file |
| UNet | Encoder–decoder with skip connections keeping fine detail | Summary + original attached to every reply |
| Learned prior | A network that has learned what clean images look like | Learned validation rules from data |
| Diffusion model | Learns to remove noise step by step; can generate images from pure noise | Iteratively refining a draft |
| Diffusion prior for inverse problems | Run diffusion denoising while forcing agreement with measurements | Autocomplete constrained by known characters |

Diagram ideas: UNet shape with skips; classic (prior by hand) vs learned (prior from data) pipelines; diffusion reverse chain with a "measurement consistency" arrow.
Scenario step: LumaLab replaces hand-tuned denoise/deblur stages with a small UNet and evaluates a diffusion prior.
Notebook idea: train a tiny UNet/DnCNN on 64×64 patches for denoising with PyTorch (CPU feasible for small patches, faster on GPU/Colab) (handout Lab 3). Diffusion part: GPU recommended; read-and-run a pretrained model only.
Production angle: PyTorch, ONNX/Core ML on device. **Breaks:** network trained on synthetic Gaussian noise fails on real sensor noise; hallucinated detail in medical images.

### M6 · Medical Imaging Reconstruction (≈ CS 11–12)

Topics: introduction to radiographic imaging; modelling radiographic imaging systems; image quality metrics for linear imaging systems; X-ray imaging; computed tomography; classic CT reconstruction methods.

| Concept | One-line definition | Analogy |
|---|---|---|
| X-ray attenuation | Tissue absorbs X-rays by density; the detector records what gets through | Packet loss measured along a route |
| Projection / sinogram | Sum of attenuation along each ray, collected at many angles | Aggregated metrics per path, from many viewpoints |
| Radon transform | Maths that maps an image to its set of projections | The forward model for CT |
| Filtered back-projection (FBP) | Smear each filtered projection back across the image and add them up | Rebuilding a table from row and column sums |
| Iterative reconstruction | Repeatedly adjust the image so its projections match the measurements | Reconciliation loop until totals match |
| MTF / image quality metric | How well a system preserves detail at each spatial frequency | Frequency response of an audio system |

Diagram ideas: CT geometry (source, rotating detector, rays); phantom → sinogram → FBP reconstruction; few-angle streak artefacts.
Scenario step: the imaging chain wants lower-dose CT (fewer angles) without losing diagnostic quality.
Notebook idea: scikit-image `radon`/`iradon` on Shepp–Logan with 180 vs 30 angles; compare FBP and SART (handout Lab 5). Laptop.
Production angle: vendor reconstruction (GE, Siemens), regulatory validation. **Breaks:** low-dose streaks; an AI reconstruction inventing structure. Monitor with phantom QA scans.

### M7 · Remote Sensing Imaging (≈ CS 13–14)

Topics: remote sensing platforms and sensors; characteristics of imaging platforms; preprocessing of remotely sensed data; geometric correction; atmospheric correction.

| Concept | One-line definition | Analogy |
|---|---|---|
| Spatial / spectral / temporal resolution | Ground size per pixel / number of colour bands / revisit frequency | Granularity, dimensions and sampling rate of a dataset |
| Multispectral bands | Images in several wavelength bands, including invisible ones (near-infrared) | Extra columns beyond RGB |
| Geometric correction | Warp the image so pixels line up with true map coordinates | Normalising timestamps to UTC |
| Ground control points | Known locations used to fit the warp | Reference records for reconciliation |
| Atmospheric correction | Remove haze and scattering so pixel values reflect the ground | Removing a constant bias from sensor readings |
| NDVI | Vegetation index from red and near-infrared bands | A derived KPI from two raw metrics |

Diagram ideas: satellite → atmosphere → ground light path; warp with ground control points; NDVI map before/after dark-object subtraction.
Scenario step: the agri customer needs accurate crop-health maps from hazy, slightly misaligned tiles.
Notebook idea: load a Sentinel-2 sample with rasterio, apply dark-object subtraction, compute NDVI, co-register two dates with OpenCV feature matching (handout Lab 4). Laptop.
Production angle: Google Earth Engine, GDAL, Sentinel Hub. **Breaks:** clouds and shadows mistaken for crop stress; misregistration between dates.

### M8 · Shape from X (≈ CS 16; session plan only)

Topics: focus stack, stereo multi-view, time-of-flight imaging.

| Concept | One-line definition | Analogy |
|---|---|---|
| Depth from focus | Find, per pixel, which photo in a focus stack is sharpest | Binary search for the sharpest setting |
| Stereo depth | Depth from how far a point shifts between two views (disparity) | Parallax: closer things move more |
| Time-of-flight | Depth from how long emitted light takes to return | Round-trip time of a ping |

Diagram ideas: focus-stack sharpness curve per pixel; stereo disparity triangle; ToF pulse timing.
Scenario step: the phone customer wants portrait-mode depth.
Notebook idea: depth-from-focus with Laplacian variance over a synthetic focus stack; OpenCV `StereoBM` on a Middlebury pair. Laptop.
Production angle: phone ToF/LiDAR sensors, dual cameras. **Breaks:** textureless walls give no stereo matches.

---

## 5. Codebase plan

`codebase/` — **lumalab**: a tiny inverse-problem toolkit. numpy, scipy, scikit-image, OpenCV, rawpy, PyWavelets, rasterio; torch (CPU) for M5.

```
codebase/
├── README.md                  run instructions, module → file map            (M1)
├── lumalab/
│   ├── isp.py                 black level, demosaic, white balance, gamma    (M1)
│   ├── hdr.py                 exposure merge + tone mapping                  (M2)
│   ├── noise.py               noise models (Gaussian, Poisson) + metrics     (M3)
│   ├── denoise.py             bilateral, NL-means, wavelet threshold         (M3)
│   ├── deblur.py              Wiener, TV-ADMM deconvolution                  (M4)
│   ├── learned.py             small UNet/DnCNN denoiser                      (M5)
│   ├── ct.py                  radon forward model, FBP, iterative recon      (M6)
│   ├── remote.py              dark-object subtraction, NDVI, co-registration (M7)
│   └── depth.py               depth from focus, stereo wrapper               (M8)
└── tests/
    ├── test_isp.py            output shape/range, white balance gray-world   (M1)
    ├── test_restore.py        denoise/deblur improve PSNR over input         (M3, M4)
    └── test_ct.py             FBP on phantom beats a PSNR threshold          (M6)
```

---

## 6. Practice topics plan

01 Camera, RAW and a minimal ISP — M1 — 5 h
02 HDR and tone mapping, coded imaging — M2 — 3 h
03 Noise models and denoising (bilateral, NLM, BM3D, wavelets) — M3 — 5 h
04 Deconvolution, priors and ADMM — M4 — 6 h
05 Deep learning for inverse problems (UNet, diffusion priors) — M5 — 6 h
06 CT reconstruction — M6 — 4 h
07 Remote sensing preprocessing — M7 — 3 h
08 Shape from X — M8 — 2 h

---

## 7. Exam signal

No past papers in this folder. Evaluation scheme from the handout:

| Component | Type | Weight | Date |
|---|---|---|---|
| EC-1(a) Quizzes | Online | 10% | not stated |
| EC-1(b) Assignments | Take home | 20% | not stated |
| EC-2 Mid-semester | Closed book | 30% | 27-12-2026 (FN) |
| EC-3 Comprehensive | Open book | 40% | 07-03-2027 (FN) |

Midsem syllabus: CS 1–8 (M1–M4). Comprehensive: all topics. Question style: not stated. Likely numericals (exposure, convolution/Wiener, PSNR) are a guess, not evidence.

---

## 8. Interview angle

1. **What is an inverse problem?** — Recovering the cause (clean image) from a measured effect (blurred, noisy data) given a forward model.
2. **Why is plain inverse filtering bad?** — It divides by near-zero frequency responses and blows up noise; regularise or use Wiener.
3. **Bilateral vs Gaussian filter?** — Bilateral also weights by intensity similarity, so it smooths noise but keeps edges.
4. **What does a camera ISP do?** — Turns RAW sensor data into a viewable image: demosaic, white balance, denoise, colour, tone map, compress.
5. **Why UNet for restoration?** — Skip connections carry fine detail from encoder to decoder, ideal for pixel-to-pixel output.
6. **How does HDR work and what goes wrong?** — Merge bracketed exposures and tone-map; moving objects cause ghosts.
7. **How is a CT image reconstructed?** — From projections at many angles, by filtered back-projection or iterative methods.
8. **What is the risk of deep-learning reconstruction in medicine?** — It can hallucinate plausible but false structure; needs validation and uncertainty checks.

---

## 9. Repetition plan

| Concept | First met | Revisited in |
|---|---|---|
| Forward model y = A·x + n | M1 | M3, M4, M5, M6, M7 |
| Noise models | M1 (sensor) | M3, M4 (Wiener), M5 (training data), M6 (low dose) |
| Convolution / kernels | M3 (smoothing) | M4, M5 (CNN), M6 (filter in FBP) |
| Image prior / regularisation | M4 | M5 (learned and diffusion priors), M6 (iterative recon) |
| PSNR / SSIM quality metrics | M3 | M4, M5, M6 (MTF) |
| Frequency domain | M2 (coded aperture) | M4, M6 |
| Geometric warping | M7 | M8 (stereo) |

---

## 10. Overlap with my other courses

- [../../machine-learning-on-the-edge/](../../machine-learning-on-the-edge/) — on-device CNN denoisers and ISP-stage models under compute limits.
- Sibling electives: [../computational-photography/](../computational-photography/) (same author; M1–M5 nearly identical) and [../3d-computer-vision/](../3d-computer-vision/) (stereo, depth, M8).
- No real overlap with the LLM, NLP or RL courses beyond general deep-learning basics.

---

## 11. Build checklist

- [ ] SPEC reviewed
- [ ] cards.json (M1, M2, M3, M4, M5, M6, M7, M8)
- [ ] practice/01 Camera, RAW and a minimal ISP
- [ ] practice/02 HDR and tone mapping
- [ ] practice/03 Noise models and denoising
- [ ] practice/04 Deconvolution, priors and ADMM
- [ ] practice/05 Deep learning for inverse problems
- [ ] practice/06 CT reconstruction
- [ ] practice/07 Remote sensing preprocessing
- [ ] practice/08 Shape from X
- [ ] codebase/ runs + tests

**Total estimated study hours: ≈ 42 h** (34 h practice topics + 8 h codebase).
