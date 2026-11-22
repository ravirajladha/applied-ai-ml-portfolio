# 3D Computer Vision (AIMLC ZG538) — Study spec

> How a computer recovers 3D shape, depth, camera position and motion from ordinary 2D photos and video, from homogeneous coordinates to NeRF, Gaussian splatting and SLAM. · Status: spec only (not built yet)

---

## 1. What it is and why an AI engineer should care

A photo flattens a 3D world onto a 2D grid; 3D vision is the maths and learning that reverses this.
The course goes from the geometry toolkit (homogeneous coordinates, camera intrinsics/extrinsics, calibration, homographies), through measuring from one image and learning depth from one image, to two-view and multi-view geometry (epipolar geometry, stereo, structure from motion, SIFT + RANSAC), motion (optical and scene flow), and modern neural 3D (NeRF, Gaussian splatting) and SLAM.
For an engineer this powers AR try-on and room scanning, robot and drone navigation, 3D reconstruction for e-commerce and mapping, and self-driving perception.
It also explains *why* deep-learning depth models fail when geometry assumptions break.

**Job relevance: 3/5** — AR/VR, robotics, autonomous driving and mapping teams need it; general ML roles rarely do, but camera geometry is a strong differentiator in vision interviews.

---

## 2. Sources in this folder

| Kind | File (relative path) | Notes |
|---|---|---|
| Handout (older batch) | `handouts/Older batch - 3D Computer Vision (S2-25_AIMLCZG538) COURSE HANDOUT.docx` | v2.0 dated 15-12-2025, Second Semester 2025-26, author Prof. Raghavendra Singh; 12 modules, 16 contact sessions (CS), lab list, evaluation scheme |

**Gaps:** handout only, older batch. No slides, past papers, lab notebooks or books. Lab list skips Lab 3 (labs numbered 1, 2, 4, 5). Module 10 is titled "Optimal and Scene Flow" in the handout, almost certainly meaning **optical** and scene flow. Several CS references are paper names only ("Paper 1", "[ECCV '20]"). Hours per session: not stated.

---

## 3. Running scenario

**RoomFit** is a furniture e-commerce app. A customer walks around their living room filming with a phone; RoomFit must **measure the room** (wall heights, floor size), **build a 3D model**, and **place a virtual sofa** that stays locked to the floor as the camera moves.
Data: the customer's phone video and photos, a printed checkerboard for calibration, and public datasets for testing (Middlebury stereo pairs, TUM RGB-D / KITTI sequences, NYU Depth v2 samples).
The goal: accurate scale (a 2.1 m sofa must look 2.1 m), stable AR anchoring, and a photo-real room model for the product page.
Each module unlocks one step, from calibrating the phone camera to a full SLAM + Gaussian-splat room.

---

## 4. Module map

Module names from the handout's Modular Content Structure; sessions from Part B (CS 1 introduction, CS 8 and CS 16 reviews).

### M1 · Representing Images and Geometry (≈ CS 1–2)

Topics: homogeneous and heterogeneous coordinates; image transforms; lines and planes in homogeneous coordinates; image warping.

| Concept | One-line definition | Analogy |
|---|---|---|
| Homogeneous coordinates | Add an extra 1 to a point so translation, rotation and projection become one matrix multiply | Wrapping data in an envelope so one handler fits all |
| 2D transforms | Translation, rotation, scale, affine, projective, as 3×3 matrices | CSS transforms |
| Line as a vector | A 2D line is three numbers; intersection of two lines = cross product | A compact ID that supports one-line joins |
| Image warping | Move each pixel by a transform, sampling the source image | Re-indexing an array via a lookup |

Diagram ideas: transform hierarchy (Euclidean ⊂ similarity ⊂ affine ⊂ projective) on a square; line intersection by cross product.
Scenario step: RoomFit's AR overlay needs a common language for moving points between images.
Notebook idea: build 3×3 transform matrices in numpy, warp an image with OpenCV `warpPerspective`, assert a point maps correctly. Laptop.
Production angle: OpenCV, Kornia. **Breaks:** forgetting to divide by the last coordinate.

### M2 · Camera Models (≈ CS 3–4)

Topics: 3D camera projections in homogeneous coordinates; camera intrinsic parameters; camera extrinsic parameters; camera calibration.

| Concept | One-line definition | Analogy |
|---|---|---|
| Pinhole projection | A 3D point maps to the image by x = K [R \| t] X | A render function from world to screen |
| Intrinsics K | Camera's internal settings: focal length, pixel centre, skew | Device config |
| Extrinsics [R \| t] | Camera's rotation and position in the world | Deployment location of the device |
| Calibration | Estimating K (and lens distortion) from photos of a known pattern | Calibrating a sensor against a reference |
| Lens distortion | Straight lines curving near image edges | Systematic bias needing correction |

Diagram ideas: world → camera → image coordinate frames; checkerboard calibration views; barrel distortion before/after.
Scenario step: RoomFit calibrates the customer's phone camera once with a checkerboard.
Notebook idea: OpenCV `calibrateCamera` on checkerboard images; report reprojection error; project a 3D cube onto the board (handout Lab 1). Laptop.
Production angle: phone vendors ship factory intrinsics; ARKit/ARCore expose them. **Breaks:** autofocus/zoom changes intrinsics mid-session.

### M3 · Homographies (≈ CS 4)

Topics: homography; creating image panoramas.

| Concept | One-line definition | Analogy |
|---|---|---|
| Homography | 3×3 matrix mapping one view of a plane (or a pure rotation) to another | A mapping table between two coordinate systems |
| DLT | Solve for H from ≥ 4 point matches with linear algebra | Fitting a config from sample pairs |
| Panorama stitching | Warp overlapping photos with homographies and blend | Merging overlapping log windows |
| Rectification | Warp a slanted plane to a front-on view | Normalising input format |

Diagram ideas: four point pairs → H → warped plane; panorama pipeline (features → match → H → warp → blend).
Scenario step: RoomFit makes a front-on view of a wall to read a poster size.
Notebook idea: estimate H from 4 clicked points with DLT in numpy; compare to `cv2.findHomography`; stitch two photos. Laptop.
Production angle: phone panorama modes. **Breaks:** parallax from moving (not rotating) the camera breaks single-H stitching.

### M4 · Single View Metrology (≈ CS 5)

Topics: linear perspective; measuring heights using parallel lines; 3D metrology from a single view.

| Concept | One-line definition | Analogy |
|---|---|---|
| Vanishing point | Where parallel 3D lines meet in the image | All roads converging at the horizon |
| Horizon / vanishing line | Line through vanishing points of a plane | Baseline for every height measurement |
| Cross-ratio | A ratio of distances preserved by perspective | An invariant that survives transformation |
| Height from reference | Measure an unknown height relative to a known one using vanishing geometry | Estimating a size from a known reference object |

Diagram ideas: room photo with three vanishing points; person-vs-door height measurement construction.
Scenario step: RoomFit estimates wall height from one photo with a door of known height.
Notebook idea: compute vanishing points from line pairs (cross products), then a height ratio; assert against a synthetic render. Laptop.
Production angle: forensic and real-estate measurement apps. **Breaks:** curved walls or lens distortion skew vanishing points.

### M5 · Learning to Estimate Depth from a Single Image (≈ CS 6)

Topics: monocular depth cues; 3D representations; methods for depth from a single image (deep learning).

| Concept | One-line definition | Analogy |
|---|---|---|
| Monocular cues | Hints like size, occlusion, texture gradient, perspective | Inferring server load from indirect metrics |
| 3D representations | Depth map, point cloud, mesh, voxels, implicit function | Different serialisation formats for the same data |
| Supervised monocular depth | Network trained on images with ground-truth depth | Supervised regression |
| Self-supervised depth | Learn depth by predicting one video frame from another | Learning from consistency checks, not labels |
| Scale ambiguity | One image can't tell a small near room from a big far one | Units missing from a metric |

Diagram ideas: depth map vs point cloud vs mesh of one chair; self-supervised view-synthesis loop.
Scenario step: RoomFit gives a quick depth preview from the first frame.
Notebook idea: run a pretrained monocular depth model (e.g. MiDaS small or Depth Anything via Hugging Face) on room photos; back-project to a point cloud with Open3D (handout Lab 4). CPU works for small models; GPU faster.
Production angle: Depth Anything / DPT models. **Breaks:** relative not metric depth; glass and mirrors.

### M6 · Epipolar Geometry (≈ CS 7)

Topics: lines and plane; essential and fundamental matrices.

| Concept | One-line definition | Analogy |
|---|---|---|
| Epipolar constraint | A point in one image must lie on a specific line in the other | A foreign-key constraint narrowing the search |
| Fundamental matrix F | 3×3 matrix linking matching pixels in two uncalibrated views: x′ᵀ F x = 0 | Join condition between two tables |
| Essential matrix E | Same idea in calibrated (normalised) coordinates; encodes R and t | F after unit normalisation |
| Eight-point algorithm | Estimate F from ≥ 8 matches by linear algebra + rank-2 fix | Least-squares fit with a constraint |

Diagram ideas: two cameras, baseline, epipolar plane and lines; matches with drawn epipolar lines.
Scenario step: RoomFit links two frames of the video to start reconstruction.
Notebook idea: normalised eight-point algorithm in numpy, compare with `cv2.findFundamentalMat`, draw epipolar lines (handout Lab 2). Laptop.
Production angle: OpenCV, COLMAP. **Breaks:** degenerate motion (pure rotation) or planar scenes make F unstable.

### M7 · Stereo Vision (≈ CS 9)

Topics: depth from image disparities; triangulation; stereo matching.

| Concept | One-line definition | Analogy |
|---|---|---|
| Disparity | Horizontal pixel shift of a point between rectified left/right images | Parallax |
| Depth = f·B / d | Depth equals focal length × baseline ÷ disparity | Farther objects shift less |
| Triangulation | Intersect two viewing rays to get the 3D point | GPS from two known positions |
| Stereo matching | Find each pixel's partner along the same row (block matching, SGM, learned) | Fuzzy join along one key |

Diagram ideas: stereo triangle with baseline B and disparity d; disparity map vs ground truth.
Scenario step: RoomFit's dual-camera phones get metric depth.
Notebook idea: OpenCV `StereoSGBM` on Middlebury, convert disparity to depth, assert with the f·B/d formula on one point. Laptop.
Production angle: depth cameras, FoundationStereo-style learned matchers (named in handout). **Breaks:** textureless walls, repetitive patterns, occlusions.

### M8 · Structure from Motion (≈ CS 10–11)

Topics: problem formulation; reprojection error; optimisation; pose estimation.

| Concept | One-line definition | Analogy |
|---|---|---|
| Structure from motion (SfM) | Recover 3D points and all camera poses from many photos | Reconstructing a timeline from scattered logs |
| Reprojection error | Pixel distance between where a 3D point projects and where it was seen | Residual between prediction and observation |
| Bundle adjustment | Jointly optimise all poses and points to minimise reprojection error | Global reconciliation of a ledger |
| Pose estimation (PnP) | Find camera pose from known 3D points and their 2D images | Locating a device from known landmarks |

Diagram ideas: SfM pipeline (features → matches → two-view init → add views → bundle adjust); reprojection error arrows.
Scenario step: RoomFit turns the walkaround video into a sparse 3D room.
Notebook idea: two-view SfM: E from matches → recoverPose → triangulate → `scipy.optimize.least_squares` mini bundle adjustment. Laptop.
Production angle: COLMAP, OpenMVG. **Breaks:** drift and wrong matches without loop closure.

### M9 · Fitting and Matching (≈ CS 11)

Topics: SIFT; RANSAC (pose estimation is grouped here in CS 11).

| Concept | One-line definition | Analogy |
|---|---|---|
| Keypoint + descriptor | A distinctive spot and a vector describing its neighbourhood | An index key + fingerprint |
| SIFT | Scale- and rotation-invariant keypoint detector and descriptor | A robust hash that survives resize/rotate |
| Ratio test | Keep a match only if the best is clearly better than the second best | Rejecting ambiguous search results |
| RANSAC | Fit models to random minimal samples; keep the one most data agrees with | Majority vote that ignores outliers |

Diagram ideas: matches before/after RANSAC; RANSAC loop with inlier count.
Scenario step: RoomFit needs reliable matches between frames despite blank walls.
Notebook idea: SIFT + ratio test + RANSAC homography in OpenCV; plot inlier ratio vs threshold; implement a 2D line RANSAC from scratch. Laptop.
Production angle: ORB for speed, SuperPoint/LightGlue learned features. **Breaks:** repetitive textures (tiles) create confident wrong matches.

### M10 · Optical and Scene Flow (≈ CS 12–13)

Topics: motion estimation; 3D motion and its 2D projection; 2D motion field and optical flow; model-based approaches; learning-based approaches; feature tracking. Lab 5: extended Kalman filter with nonlinear observation model; linear Kalman filter with learned inverse observation model.

| Concept | One-line definition | Analogy |
|---|---|---|
| Optical flow | Per-pixel 2D motion between two frames | A diff of positions between snapshots |
| Brightness constancy | Assume a point keeps its brightness while moving | Assuming IDs stay stable across versions |
| Lucas–Kanade | Solve flow in small windows assuming locally constant motion | Local least-squares fit |
| Scene flow | 3D motion of each point | Optical flow plus depth change |
| Kalman / extended Kalman filter | Predict state, then correct with measurements; EKF linearises a nonlinear model | Forecast then update with actuals |

Diagram ideas: flow field arrows on a moving scene; aperture problem; Kalman predict/update cycle for a tracked point.
Scenario step: RoomFit keeps the sofa anchored while the camera and the customer's dog move.
Notebook idea: OpenCV Lucas–Kanade tracking + Farneback dense flow on a short video; a 2D constant-velocity Kalman filter smoothing a tracked point. Laptop. (Learned flow like RAFT needs GPU.)
Production angle: RAFT, ARKit tracking. **Breaks:** fast motion, motion blur and lighting changes break brightness constancy.

### M11 · Advanced Topics: Neural Radiance Fields and Gaussian Splatting (≈ CS 14)

| Concept | One-line definition | Analogy |
|---|---|---|
| Novel view synthesis | Rendering the scene from a viewpoint never photographed | Interpolating missing data points |
| NeRF | A neural network mapping 3D position + view direction to colour and density, rendered by ray marching | A function you query instead of a stored table |
| Volume rendering | Accumulate colour along a ray weighted by density | Weighted sum along a path |
| 3D Gaussian splatting | Scene as millions of small 3D Gaussians rasterised fast | Pre-baked cache instead of computing on demand |

Diagram ideas: NeRF ray samples → MLP → accumulated pixel; Gaussian splat ellipsoids → rasterised image.
Scenario step: RoomFit renders a photo-real room for the product page.
Notebook idea: volume rendering of a single ray in numpy with synthetic density; optionally run nerfstudio / a gsplat demo. Full training needs a GPU.
Production angle: nerfstudio, gsplat, Luma/Polycam. **Breaks:** needs accurate poses (from SfM); floaters with few views.

### M12 · State-of-the-art Applications: 3D Reconstruction and SLAM (≈ CS 15; CS 16 review)

| Concept | One-line definition | Analogy |
|---|---|---|
| Dense 3D reconstruction | Full surface model from many views or depth frames | Full table vs sample rows |
| SLAM | Track the camera and build the map at the same time, in real time | Writing docs while discovering endpoints |
| Visual odometry | Frame-to-frame camera motion estimate; drifts over time | Dead reckoning |
| Loop closure | Recognising a revisited place and correcting accumulated drift | Detecting a duplicate and merging history |

Diagram ideas: SLAM front-end/back-end block diagram; drifted vs loop-closed trajectory.
Scenario step: RoomFit runs live SLAM so AR furniture stays put while the customer walks around.
Notebook idea: monocular visual odometry on a KITTI/TUM snippet with ORB + essential matrix; plot trajectory vs ground truth; fuse depth frames with Open3D TSDF. Laptop.
Production angle: ARKit/ARCore, ORB-SLAM3, RTAB-Map. **Breaks:** scale drift in monocular SLAM, dynamic objects, low light.

---

## 5. Codebase plan

`codebase/` — **roomfit3d**: a small geometry library with a CLI that measures and reconstructs a room. numpy, scipy, OpenCV, Open3D, matplotlib; optional torch for M5.

```
codebase/
├── README.md                 run instructions, module → file map             (M1)
├── roomfit3d/
│   ├── geometry.py           homogeneous helpers, transforms, warps          (M1)
│   ├── camera.py             projection, calibration wrapper, undistort      (M2)
│   ├── homography.py         DLT + panorama stitch                           (M3)
│   ├── metrology.py          vanishing points, height from reference         (M4)
│   ├── mono_depth.py         pretrained depth → point cloud                  (M5)
│   ├── epipolar.py           eight-point F, E, recoverPose                   (M6)
│   ├── stereo.py             disparity → depth, triangulation                (M7)
│   ├── sfm.py                two-view init + mini bundle adjustment          (M8)
│   ├── features.py           SIFT + ratio test + RANSAC                      (M9)
│   ├── tracking.py           optical flow + Kalman filter                    (M10)
│   └── vo.py                 visual odometry trajectory                      (M12)
└── tests/
    ├── test_geometry.py      transform round trips; line intersection        (M1)
    ├── test_camera.py        project/backproject a known point               (M2)
    ├── test_epipolar.py      x'ᵀFx ≈ 0 on synthetic matches                  (M6)
    └── test_stereo.py        depth = f·B/d on synthetic data                 (M7)
```

---

## 6. Practice topics plan

01 Homogeneous coordinates and transforms — M1 — 3 h
02 Camera model and calibration — M2 — 5 h
03 Homographies and single-view metrology — M3, M4 — 5 h
04 Monocular depth and 3D representations — M5 — 4 h
05 Epipolar geometry and stereo — M6, M7 — 6 h
06 Features, RANSAC and structure from motion — M8, M9 — 6 h
07 Optical flow and tracking with Kalman filters — M10 — 4 h
08 NeRF, Gaussian splatting and SLAM — M11, M12 — 5 h

---

## 7. Exam signal

No past papers in this folder. Evaluation scheme (older handout):

| Component | Type | Duration | Weight | Date (that term) |
|---|---|---|---|---|
| EC-1(a) Quizzes | Online | 1 week | 10% | TBA |
| EC-1(b) Assignments | Take home | 10 days | 20% | TBA |
| EC-2 Mid-semester | Closed book | 2 h | 30% | 21-06-2026 (AN) |
| EC-3 Comprehensive | Open book | 2.5 h | 40% | 06-09-2026 (AN) |

Midsem syllabus: CS 1–8 (M1–M6). Comprehensive: all topics. Question style: not stated.

---

## 8. Interview angle

1. **Why homogeneous coordinates?** — They make translation and perspective projection linear, so a whole camera is one matrix.
2. **Intrinsics vs extrinsics?** — Intrinsics are the camera's internal geometry (focal length, centre); extrinsics are its pose in the world.
3. **Fundamental vs essential matrix?** — Both encode two-view geometry; F works in pixels for uncalibrated cameras, E in normalised coordinates and gives R, t.
4. **How does RANSAC work?** — Fit a model to a random minimal sample, count inliers, repeat, keep the best; robust to outliers.
5. **How does stereo get depth?** — Rectify, match pixels along rows to get disparity, then depth = f·B / d.
6. **What is bundle adjustment?** — Joint nonlinear least-squares over all camera poses and 3D points minimising reprojection error.
7. **Why is monocular depth scale-ambiguous and how do apps fix it?** — One image can't separate size from distance; fuse IMU, a known object, or stereo/LiDAR.
8. **NeRF vs Gaussian splatting?** — NeRF queries a neural field per ray (slow, compact); splatting rasterises explicit Gaussians (real-time, more memory).
9. **What breaks visual SLAM in production?** — Low texture, fast motion, moving objects, lighting changes, and scale drift without loop closure.

---

## 9. Repetition plan

| Concept | First met | Revisited in |
|---|---|---|
| Homogeneous coordinates | M1 | M2, M3, M6, M8 |
| Projection matrix K[R\|t] | M2 | M4, M7, M8, M11 |
| Homography | M3 | M4 (rectification), M9 (RANSAC model) |
| Feature matching | M3 (panorama) | M6, M8, M9, M12 |
| Least-squares fitting | M3 (DLT) | M6 (eight-point), M8 (bundle adjustment) |
| Depth representation | M5 | M7, M11, M12 |
| Outlier robustness (RANSAC) | M9 | M6, M8, M12 |
| Drift and correction | M10 (Kalman) | M12 (loop closure) |

---

## 10. Overlap with my other courses

- [../../machine-learning-on-the-edge/](../../machine-learning-on-the-edge/) — real-time depth and tracking models on phones.
- Sibling electives: [../ai-ml-for-robotics/](../ai-ml-for-robotics/) (SLAM, Kalman filters, localization), [../computational-photography/](../computational-photography/) and [../computational-imaging/](../computational-imaging/) (Shape from X: stereo, focus stack, time-of-flight).
- No real overlap with the LLM, NLP or RL courses.

---

## 11. Build checklist

- [ ] SPEC reviewed
- [ ] cards.json (M1, M2, M3, M4, M5, M6, M7, M8, M9, M10, M11, M12)
- [ ] practice/01 Homogeneous coordinates and transforms
- [ ] practice/02 Camera model and calibration
- [ ] practice/03 Homographies and single-view metrology
- [ ] practice/04 Monocular depth and 3D representations
- [ ] practice/05 Epipolar geometry and stereo
- [ ] practice/06 Features, RANSAC and structure from motion
- [ ] practice/07 Optical flow and tracking
- [ ] practice/08 NeRF, Gaussian splatting and SLAM
- [ ] codebase/ runs + tests

**Total estimated study hours: ≈ 46 h** (38 h practice topics + 8 h codebase).
