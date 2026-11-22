# ML System Optimisation (AIML ZG516) — Study spec

> How ML algorithms run fast on real hardware: parallel training, clusters, GPUs, and squeezing models onto small devices. · Status: spec only (not built yet)

## 1. What it is and why an AI engineer should care

This course is about the computer underneath the model. It asks: how long does training take, how much memory does it
need, and how do we make it faster by splitting the work across cores, GPUs or machines (parallel and distributed
computing)? It then flips to deployment: how to shrink a model (quantization, pruning, distillation) so it fits a phone
or a microcontroller and still answers fast. The handout says plainly that the focus is the systems side, not the
algorithms themselves, and that MLOps covers the pipeline side. For an engineer this is where GPU bills, latency SLAs
and "why is training so slow" get answered.

**Job relevance: 4/5** — inference cost and latency work (quantization, batching, GPU use) is in demand; deep CUDA and cluster theory less so.

## 2. Sources in this folder

| Kind | File (relative path) | Notes |
|---|---|---|
| Handout (older batch) | `handouts/Older batch - ML System Optimisation - handout.pdf` | v1.0, 11 Mar 2023, author Shan Sundar Balasubramaniam, 4 modules, 16 sessions; "Text / References: NONE" |
| Old-batch slides | `old-batch-slides/MLSysOpts Slides.pdf` | A later batch (a session dated 1 Dec 2024, instructor Murali Parameswaran). Covers sessions 1–12 plus compression, edge case study, federated learning, CPU/GPU/TPU/FPGA, SLMs |

Differences slides vs handout (handout wins for topic names; slides show what was actually taught):
- Slides add memory hierarchy and locality (cache-aware matrix multiply), multi-threading speedups, and CUDA programming
  (grids, blocks, threads, GPU memory model) that the handout only covers as "parallel execution on multicore and GPGPUs".
- Slides add an edge case study (AxIS, approximate computing for a wrist-worn device) and FPGA fixed-point arithmetic.
- Course code appears as AIML ZG516 (Part A), AIML CLZG516 (Part B) and AML CCZG516 (slides).

Gaps:
- No current-batch handout, no past question papers, no prescribed textbook (handout says readings assigned per session).
- No assignment or project briefs, though they are 45% of the grade.

## 3. Running scenario

**FreshCart** is a quick-commerce grocery app with 2,000 dark stores. It has two ML workloads. (1) Nightly training on
200 million order rows: k-means customer segments, a random-forest demand model and an SGD-trained ranking model,
currently a 9-hour single-machine job. (2) A CNN that recognises products from shelf photos, which must run on cheap
Android handhelds in stores with poor network. The goal: get nightly training under 1 hour on a small cluster without
losing accuracy, and ship a shelf-scanner model under 5 MB that answers in under 100 ms on the device.

## 4. Module map

Contact hours per module: not stated. Sessions per module are from the handout.

### M1 · Introduction — contour of ML solutions, parallelization, modern systems (sessions 1–3)

Topics: performance metrics (time complexity, running time, memory, response time, throughput); scaling and tuning;
training vs deployment environments; distributed/cloud vs embedded/mobile; speedup and Amdahl's law; data vs task vs
request parallelism; scale-up vs scale-out and the cost of communication; parallel execution on multicore and GPGPUs;
data distribution strategies on clusters.

| Concept | One-line definition (≤20 words, no jargon) | Analogy |
|---|---|---|
| Throughput vs response time | Jobs finished per second vs time one job waits from request to answer. | Requests per second vs p95 latency |
| Speedup | Time on one processor divided by time on p processors. | How much faster the build is with more CI runners |
| Amdahl's law | The serial fraction f caps speedup at 1/f, however many processors you add. | One slow DB migration step blocks the whole deploy |
| Data parallelism | Same operation on different slices of the data at once. | Sharding a table across workers |
| Task parallelism | Different operations run at the same time on separate workers. | Microservices each doing their own job |
| Request parallelism | Many independent user requests served side by side. | A load balancer in front of web servers |
| Scale-up vs scale-out | Bigger machine vs more machines; scale-out pays network communication cost. | Vertical vs horizontal scaling |

Diagram ideas:
- Amdahl curve: speedup vs processors for f = 0.05, 0.1, 0.25.
- Tree-parallel summation (reduction) of 8 numbers in log2(8) = 3 steps (from slides).
- Training vs deployment range: data centre → cloud → mobile → microcontroller.

Scenario step: profile the 9-hour job; find that 15% is serial CSV parsing, so Amdahl says max ≈ 6.7x.

Notebook idea: sum and dot-product with `multiprocessing` on 1, 2, 4, 8 processes; plot measured vs Amdahl speedup.
Cache-aware matrix multiply (IJK vs IKJ loop order) in numpy/numba to see locality. CPU only.

Production angle: profilers (py-spy, perf, PyTorch profiler), Ray, Dask. Breaks: adding workers makes the job slower
because communication and data shuffling now dominate.

### M2 · Parallel / distributed ML algorithms (sessions 4–6)

Topics (training phase): CNN; gradient descent and SGD; SVM; k-means; kNN; decision trees / random forests. Slides also
show AdaBoost (why boosting is hard to parallelise), map-reduce formulations, and MPI / Hadoop / Spark options.

| Concept | One-line definition (≤20 words, no jargon) | Analogy |
|---|---|---|
| Map-reduce | Map work over chunks independently, then reduce partial results with an associative operator. | `Promise.all` then a fold |
| Parallel k-means | Each worker assigns its points to centroids; partial sums are merged to update centroids. | Each team counts votes locally, HQ adds them |
| Parallel kNN | Split the data across nodes; each returns its local k nearest; merge to a global k. | Querying shards and merging top-k |
| Parallel trees / forests | Forest trees are independent so train in parallel; one tree parallelises split search per feature. | Independent CI jobs vs one job with parallel steps |
| Sequential dependency | When step t needs step t-1's result (boosting, plain SGD), parallelism is limited. | Database migrations that must run in order |
| Mini-batch SGD | Update weights from gradients averaged over a small batch; batches can be split across workers. | Batching writes to cut round trips |

Diagram ideas:
- k-means map step (distances per point) and reduce step (new centroids) on 4 workers.
- AdaBoost loop showing why round m waits for round m-1 (slides "AdaBoost: Pipelining?").
- kNN on p nodes with N/p points each and a merge of local top-k lists.

Scenario step: rewrite customer segmentation as map-reduce k-means and train the 300 demand forests in parallel.

Notebook idea: implement k-means as explicit map and reduce functions in numpy, run with `joblib` on 4 cores, check same
centroids as sklearn; time `RandomForestClassifier(n_jobs=1 vs -1)`. CPU only.

Production angle: Spark MLlib, Dask-ML, XGBoost/LightGBM distributed. Breaks: data skew, where one partition holds most
rows and every other worker waits for it.

### M3 · Scale-out ML — platforms and distributed neural networks (sessions 7–12)

Topics: parameter server model; Spark architecture; TensorFlow architecture; performance improvement and trade-offs on
distributed systems; decentralised and local SGD; system support (all-reduce, asynchronous parallelism); large-scale
deep NNs; systems for federated learning. Slides also cover memory hierarchy and locality (session 9), cache-aware and
multi-threaded matrix multiply (session 10), and GPU / CUDA programming (session 11).

| Concept | One-line definition (≤20 words, no jargon) | Analogy |
|---|---|---|
| Parameter server | Central servers hold the weights; workers pull weights, compute gradients, push updates. | A central config store with many clients writing |
| All-reduce | Every worker ends up with the sum of all workers' gradients, no central server. | Peer-to-peer gossip until everyone has the total |
| Sync vs async SGD | Sync waits for all workers each step; async applies updates whenever they arrive, risking stale gradients. | Strict consistency vs eventual consistency |
| Local SGD | Workers take several local steps before averaging, trading accuracy for less communication. | Batching commits before pushing |
| Federated learning | Train on users' devices; only model updates, not raw data, are sent to the server. | Each branch office sends summaries, never raw files |
| Memory locality | Programs run faster when they reuse nearby data already in cache. | Reading a table in index order vs random seeks |
| GPU kernel | A function run by thousands of lightweight threads arranged in blocks on the GPU. | A massively parallel `map` |

Diagram ideas:
- Parameter server vs ring all-reduce, with messages per step counted.
- Memory hierarchy pyramid: registers → caches → RAM → disk → network, with access costs.
- CUDA grid → blocks → threads, mapped onto a matrix-addition example (slides configurations).

Scenario step: move the SGD ranking model to 4-worker data-parallel training with all-reduce; consider federated
learning so store handhelds improve the scanner without uploading photos.

Notebook idea: simulate sync vs async SGD with 4 "workers" in numpy on logistic regression; plot loss vs messages sent.
Run PyTorch DDP with the `gloo` backend on 2 CPU processes. Optional: one CUDA kernel via `numba.cuda` (needs NVIDIA GPU,
else read only).

Production angle: PyTorch DDP/FSDP, Horovod, NCCL, Spark, Flower for federated learning. Breaks: one slow worker
(straggler) stalls every synchronous step.

### M4 · ML under systems constraints (sessions 13–16)

Topics: model compression and its effect on inference; quantization and limited numerical precision; pruning CNNs and
evaluating pruning; deep compression (quantization + pruning + sparsity); TinyML and TensorFlow Lite; energy
constraints; trade-offs among accuracy, model size, throughput, response time and energy. Slides add low-rank
factorization, knowledge distillation, fixed-point arithmetic on FPGAs, CPU vs GPU vs TPU, and small language models.

| Concept | One-line definition (≤20 words, no jargon) | Analogy |
|---|---|---|
| Quantization | Store weights and activations in fewer bits (float32 → int8) to shrink and speed up. | Compressing images from PNG to JPEG |
| Pruning | Remove weights or channels that barely affect output, then fine-tune. | Deleting dead code |
| Knowledge distillation | Train a small student model to copy a big teacher model's outputs. | A senior writing a runbook a junior can follow |
| Low-rank factorization | Replace a big weight matrix with the product of two thin matrices. | Normalising a wide table into two narrow ones |
| Fixed-point arithmetic | Numbers with a fixed number of fractional bits, cheap on small chips. | Storing money as integer paise |
| TinyML | Running ML on microcontrollers with kilobytes of memory and milliwatts of power. | Writing firmware, not a web app |
| Accuracy-size-latency-energy trade-off | Every compression choice gains some resources and loses some accuracy; measure all four. | The CAP theorem of edge ML |

Diagram ideas:
- Float32 vs int8 number line with a scale and zero-point.
- Deep compression pipeline: prune → quantize → encode, with size after each stage.
- Radar chart of accuracy, size, latency, energy for baseline / int8 / pruned / distilled models.

Scenario step: shrink the shelf-scanner CNN from 45 MB to under 5 MB and measure accuracy and latency on CPU.

Notebook idea: train a small CNN on CIFAR-10 subset (CPU, ~10 min), then apply PyTorch dynamic/static int8 quantization,
`torch.nn.utils.prune`, and a distilled student; table of size, accuracy and latency. Export to ONNX / TFLite. CPU only.

Production angle: TensorRT, ONNX Runtime, TFLite / LiteRT, OpenVINO, bitsandbytes for LLMs. Breaks: int8 model is
accurate on the test set but fails on real store photos because calibration data did not include dim lighting.

## 5. Codebase plan

`freshcart-perf`: a benchmarking lab that grows from parallel training to an edge model.

```
codebase/
├── README.md                    how to run; which module added which file             (M1)
├── data/make_orders.py          synthetic orders + small image subset download        (M1)
├── src/perf/
│   ├── bench.py                 timer, speedup and Amdahl helpers                     (M1)
│   ├── locality.py              loop-order matrix multiply comparison                 (M1, M3)
│   ├── kmeans_mr.py             map-reduce k-means with joblib                         (M2)
│   ├── knn_sharded.py           sharded kNN with top-k merge                           (M2)
│   ├── sgd_sim.py               sync / async / local SGD simulator                     (M3)
│   ├── ddp_train.py             PyTorch DDP on 2 CPU processes (gloo)                  (M3)
│   ├── compress.py              quantize, prune, distill a small CNN                   (M4)
│   └── export.py                ONNX export + latency benchmark                        (M4)
└── tests/
    ├── test_bench.py            Amdahl formula values                                  (M1)
    ├── test_kmeans_mr.py        same centroids as sklearn                              (M2)
    ├── test_sgd_sim.py          sync SGD converges                                     (M3)
    └── test_compress.py         int8 model smaller, accuracy drop < 2 points           (M4)
```

## 6. Practice topics plan

1. 01 Speedup and Amdahl's law — M1 — 3 h
2. 02 Data, task and request parallelism — M1 — 3 h
3. 03 Parallel classic ML: k-means, kNN, forests — M2 — 5 h
4. 04 Memory locality and multi-threading — M1, M3 — 4 h
5. 05 Parameter server vs all-reduce, sync vs async SGD — M3 — 5 h
6. 06 GPU programming model (reading + optional numba.cuda) — M3 — 3 h
7. 07 Federated learning systems — M3 — 3 h
8. 08 Quantization and pruning — M4 — 5 h
9. 09 Distillation, TinyML and the four-way trade-off — M4 — 4 h

## 7. Exam signal

No past question papers in this folder. Evaluation scheme (older handout):

| Component | Weight | Duration |
|---|---|---|
| Assignment (take-home, before mid-term) | 15% | 3–4 weeks |
| Project (take-home, after mid-term) | 30% | about 6 weeks |
| Mid-Semester Test | 25% | 120 min |
| Comprehensive Exam | 30% | 150 min |

Open/closed book: not stated. Mid-sem syllabus split: not stated. Slides include worked items likely to be examinable:
Amdahl speedup, tree reduction speedup N/log N, map-reduce formulations of k-means / keyword extraction, CUDA grid and
block configurations for matrix addition, loop-order timing tables.

## 8. Interview angle

1. **What does Amdahl's law say?** Speedup is capped by the serial fraction: max = 1/f.
2. **Data vs model parallelism?** Data: same model, split the batch; model: split the model's layers or tensors across devices.
3. **Parameter server vs all-reduce?** Central weight store vs peer-to-peer gradient summing; all-reduce avoids the server bottleneck.
4. **Sync vs async SGD trade-off?** Sync is consistent but waits for stragglers; async is faster but uses stale gradients.
5. **Why are GPUs fast for deep learning?** Thousands of simple cores doing the same matrix maths in parallel with high memory bandwidth.
6. **How does int8 quantization work?** Map floats to 8-bit integers with a scale and zero-point; about 4x smaller, faster integer maths.
7. **Pruning vs distillation?** Pruning removes parts of the same model; distillation trains a new smaller model to imitate it.
8. **How do you decide a model is "edge-ready"?** Measure size, latency, memory, energy and accuracy on the target device, not the laptop.
9. **Why might adding GPUs not speed up training?** Communication, data loading or a serial step becomes the bottleneck.
10. **What is federated learning's main systems challenge?** Unreliable, slow, heterogeneous devices and limited upload bandwidth.

## 9. Repetition plan

| Concept | First met (module) | Revisited in (modules) |
|---|---|---|
| Speedup / Amdahl | M1 | M2 (parallel algorithms), M3 (cluster scaling) |
| Data parallelism | M1 | M2 (k-means, kNN), M3 (data-parallel SGD) |
| Communication cost | M1 | M3 (parameter server, all-reduce, federated) |
| Map-reduce | M2 | M3 (Spark) |
| SGD | M2 | M3 (distributed SGD, local SGD) |
| Memory locality | M3 (slides S9) | M3 (GPU memory), M4 (model size) |
| Throughput vs latency | M1 | M4 (edge trade-offs) |
| Accuracy trade-off | M3 (async staleness) | M4 (compression) |

## 10. Overlap with my other courses

- [../../machine-learning-on-the-edge/](../../machine-learning-on-the-edge/) — strong overlap with M4 (compression, TinyML, deployment on constrained devices).
- [../../llm-engineering/](../../llm-engineering/) — assignment 1B (4-bit quantization, speculative decoding, cost) applies M4 ideas to LLMs.
- [../../software-engineering-for-machine-learning/](../../software-engineering-for-machine-learning/) — practice/09 Code Performance Profiling is the M1 measuring skill.
- [../mlops/](../mlops/) — the handout says the training/deployment pipeline belongs to MLOps; this course is the hardware side.

## 11. Build checklist

- [ ] SPEC reviewed
- [ ] cards.json (M1…M4, 8–12 cards each)
- [ ] practice/01 Speedup and Amdahl's law
- [ ] practice/02 Data, task and request parallelism
- [ ] practice/03 Parallel classic ML
- [ ] practice/04 Memory locality and multi-threading
- [ ] practice/05 Parameter server vs all-reduce
- [ ] practice/06 GPU programming model
- [ ] practice/07 Federated learning systems
- [ ] practice/08 Quantization and pruning
- [ ] practice/09 Distillation, TinyML and trade-offs
- [ ] codebase/ runs + tests

Total estimated study hours: ≈ 35 h practice + ≈ 10 h codebase + ≈ 5 h cards/revision = **≈ 50 h**.
