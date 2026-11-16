from helpers import mcq, tf, out, fill

# Machine Learning on the Edge (AIMLCZG535), Module 8, Sessions 15-16:
# Benchmarking and Future Directions. Built from the handout sub-topics and the
# Sep 2026 end-sem Q3 (Pareto frontier under a strict p95 SLA); the rest is standard
# practice (T1, TFLite and MLPerf Tiny docs) because the sessions are "Instructor Supplied Material".

SUBJECT = "edge-benchmarking"

TOPICS = [
    ("bench-metrics", "Benchmarking metrics: latency, throughput, power, memory"),
    ("latency-stats", "Latency distributions: p50, p95, p99 and jitter"),
    ("methodology", "Benchmark methodology"),
    ("bench-tools", "Profiling tools: TFLite benchmark tool, MLPerf Tiny"),
    ("energy-kpis", "Industry KPIs for edge energy efficiency"),
    ("reports", "Visualizing and interpreting benchmark reports"),
    ("pareto", "Pareto dominance and the frontier"),
    ("sla-selection", "Selecting a model under an SLA"),
    ("tinyml", "TinyML on microcontrollers"),
    ("edge-genai", "Edge generative AI: tiny LLMs and compressed diffusion"),
    ("collab-trends", "Multimodal fusion, swarm edge AI, federated analytics and split learning"),
    ("green-ai", "Energy-aware scheduling and Green AI"),
]

QUESTIONS = [
    # ------------------------------------------------------------------ L1
    mcq("Session 15 names four benchmarking metrics. Which list is it?",
        ["Latency, throughput, power, memory usage",
         "Accuracy, recall, precision, F1",
         "Epochs, batch size, learning rate, loss",
         "Price, weight, colour, brand"], 0,
        "Three are about time and energy, one about space.",
        "Latency (ms per inference), throughput (inferences/s), power (W, which with latency gives energy) and memory usage (Flash/storage and peak RAM) describe whether a model fits the device. Accuracy is checked too, but it is a quality metric, not a benchmarking one.",
        topic="bench-metrics", level=1),
    tf("An edge model should be benchmarked on the target device (or a faithful simulator of it), because the same model can be several times faster or slower on different hardware.", True,
       "A laptop is not a Raspberry Pi.",
       "CPU type, clock, memory bandwidth, accelerators and the runtime's kernels all change latency, power and memory. A number from a development laptop says little about a Cortex-A72 or an MCU, so the course's lab benchmarks run on the device or an edge simulator.",
       topic="bench-metrics", level=1),
    mcq("A benchmark report says 'p95 latency = 18 ms'. What does that mean?",
        ["95% of the measured inferences took 18 ms or less",
         "The average inference took 18 ms",
         "The slowest inference took 18 ms",
         "18 ms is 95% faster than the cloud"], 0,
        "p = percentile.",
        "The 95th percentile is the value below which 95% of measurements fall; 5% were slower. SLAs are usually written on p95 or p99 because users and control loops feel the slow cases, which the average hides.",
        analogy="Like 'pages load in under 2 s for 95% of visitors' in a web-performance report: the slowest 5% are the users who complain.",
        topic="latency-stats", level=1,
        diagram="""
sorted latencies (100 runs)
|....................................|...|
fast                               p95  max
95 runs at or below p95 | 5 slower
"""),
    fill("The 50th-percentile latency, p50, is also called the ____. (one word)", "median",
         "Half the runs are faster, half slower.",
         "p50 = median. Unlike the mean, one very slow run barely moves it, so p50 shows the typical case and p95/p99 show the tail.",
         topic="latency-stats", level=1),
    mcq("Why do benchmark tools run a few warm-up inferences before timing?",
        ["The first runs pay one-off costs (memory allocation, delegate set-up, cold caches) that do not happen in steady operation",
         "To heat the processor so it runs faster",
         "To download the model from the cloud",
         "To train the model a little before measuring"], 0,
        "What is different about the very first inference?",
        "The first inference often takes many times longer: buffers are allocated, the GPU/NPU delegate compiles or prepares kernels, caches are cold. Steady-state latency is what users see after start-up, so warm-up runs are discarded (start-up time is reported separately).",
        topic="methodology", level=1,
        analogy="Like load-testing a web server: you ignore the first requests that hit cold caches and JIT compilation, then measure."),
    tf("A fair benchmark repeats the inference many times and reports statistics, instead of timing a single run.", True,
       "One run can be unlucky.",
       "Single timings vary with background tasks, interrupts and caches. Tens to hundreds of runs give a stable average and let you compute percentiles.",
       topic="methodology", level=1),
    mcq("What is the TensorFlow Lite benchmark tool (benchmark_model)?",
        ["A command-line tool that loads a .tflite model on the device and reports its initialisation time, inference latency and memory use",
         "A website that ranks phones by price",
         "A training script that tunes hyperparameters",
         "A converter from PyTorch to TFLite"], 0,
        "It runs the model; it does not change it.",
        "benchmark_model (also packaged as an Android app) runs a model with random or given inputs for a set number of runs and prints timings and memory. Flags choose threads, warm-up runs, number of runs and delegates (GPU, NNAPI, XNNPACK).",
        topic="bench-tools", level=1),
    mcq("What is MLPerf Tiny?",
        ["An industry benchmark suite (MLCommons) for running ML on microcontroller-class devices, with fixed tasks, reference models and measured latency and energy",
         "A small version of a large language model",
         "A tiny GPU made by MLCommons",
         "A Python library for training small models"], 0,
        "MLPerf is the benchmark family; Tiny is the microcontroller track.",
        "MLPerf Tiny gives everyone the same tasks and rules (keyword spotting, visual wake words, image classification, anomaly detection) so results from different MCUs and accelerators are comparable. Energy is measured with EEMBC's EnergyRunner set-up.",
        topic="bench-tools", level=1),
    fill("Energy per inference = average power × ____. (one word)", "latency",
         "Watts times seconds gives joules.",
         "E = P × t. A board drawing 2 W for a 15 ms inference uses 30 mJ per inference. A low-power chip is not automatically low-energy: if it is much slower, the product can be larger.",
         topic="energy-kpis", level=1),
    tf("'Inferences per joule' is a higher-is-better energy-efficiency KPI.", True,
       "More work per unit of energy.",
       "Inferences per joule = 1 / (energy per inference in joules). 10 mJ per inference = 100 inferences per joule. For battery devices it maps directly to how much work one charge buys.",
       topic="energy-kpis", level=1),
    mcq("In the accuracy-latency comparison used in the end-sem papers, what does 'model A dominates model C' mean?",
        ["A is at least as good as C on both accuracy and latency, and strictly better on at least one",
         "A has higher accuracy than C, whatever the latency",
         "A is faster than C, whatever the accuracy",
         "A and C have the same file size"], 0,
        "Better or equal everywhere, strictly better somewhere.",
        "Dominance needs both conditions. In the paper, A (74%, 8 ms) dominates C (74%, 10 ms): same accuracy, faster. If A were more accurate but slower, neither would dominate: that is a trade-off, not dominance.",
        analogy="Like comparing two laptops: if one is both cheaper and faster, the other is simply out; if one is cheaper but slower, you have a real choice.",
        topic="pareto", level=1),
    fill("The set of models that no other model dominates is called the Pareto ____. (one word)", "frontier",
         "Also called the Pareto front.",
         "The Pareto frontier holds the best available trade-offs: moving along it you can only gain accuracy by giving up speed. Every model off the frontier is beaten by some model on it.",
         topic="pareto", level=1,
        diagram="""
accuracy
  ^          * D
  |     * A
  |  * B   o C (dominated by A)
  +-------------------> latency
frontier: B - A - D
"""),
    mcq("A deployment SLA says 'p95 latency strictly below 10 ms'. What is an SLA here?",
        ["A hard requirement the deployed model must meet; models that miss it are rejected",
         "A suggestion that can be ignored if the model is accurate",
         "The model's accuracy target",
         "The price of the edge device"], 0,
        "Service-level agreement.",
        "An SLA is a contract-like limit, often on tail latency. Model selection filters out every candidate that violates it first, then picks the best among the rest.",
        topic="sla-selection", level=1,
        analogy="Like an API's response-time SLO in a contract: a faster-but-buggy release and a correct-but-too-slow release both fail it."),
    tf("If the SLA requires latency strictly below 10 ms, a model measured at exactly 10 ms p95 meets the SLA.", False,
       "Read 'strictly' carefully.",
       "'Strictly below' means < 10, not ≤ 10. A 10 ms model fails. This is exactly the trap in the Sep 2026 paper, where model C (10 ms) sits on the boundary.",
       topic="sla-selection", level=1),
    mcq("What does TinyML mean in Session 16?",
        ["Running ML models on microcontrollers at milliwatt power levels or below, often always-on and battery-powered",
         "Training very small models in the cloud",
         "A version of Python for small screens",
         "Any model with fewer than 1,000 training examples"], 0,
        "Tiny device, tiny power.",
        "TinyML targets MCUs (e.g. ARM Cortex-M with ~256 KB SRAM and 1 MB Flash) for tasks like keyword spotting or vibration anomaly detection, running for months on a battery. TFLite Micro is the usual runtime.",
        topic="tinyml", level=1),
    mcq("What does 'Edge Generative AI' refer to?",
        ["Running compact language models and compressed image-generation (diffusion) models directly on phones, laptops or edge boards",
         "Generating new edge devices with AI",
         "Using the cloud to generate training data",
         "Building websites with generative design"], 0,
        "Generative models, but on the device.",
        "Small LLMs (about 1-4B parameters, quantized to 4-bit) and distilled diffusion models now run on phones and Jetsons. Benefits are the usual edge ones: privacy, offline use, no per-request cloud cost.",
        topic="edge-genai", level=1),
    mcq("A traffic system combines camera images, radar and microphone audio to decide whether an emergency vehicle is approaching. This is an example of:",
        ["Multimodal edge AI (sensor fusion)",
         "Split learning",
         "Federated analytics",
         "Model pruning"], 0,
        "Several kinds of input, one decision.",
        "Multimodal fusion combines different sensor types so each covers the others' blind spots: the siren is heard before the vehicle is visible, radar works in fog.",
        topic="collab-trends", level=1),
    mcq("What is swarm edge AI?",
        ["Many autonomous devices (drones, vehicles, robots) sharing information and making decisions together, without one central controller",
         "Training one model on many GPUs in a data centre",
         "A virus that spreads across IoT devices",
         "Buying a large number of the same device"], 0,
        "Think of a flock of birds.",
        "In a swarm each device senses and decides locally and coordinates with neighbours (e.g. drones splitting a search area for a missing person). No single point of failure, at the cost of communication and agreement overhead.",
        topic="collab-trends", level=1,
        analogy="Like a peer-to-peer network instead of a client-server one: no central server, nodes gossip state to their neighbours."),
    mcq("What is 'Green AI'?",
        ["Treating energy use and carbon emissions as first-class metrics, reported and optimized alongside accuracy",
         "AI used only for agriculture",
         "Models trained on images of plants",
         "Painting edge devices green to reduce heat"], 0,
        "Environmental cost of AI.",
        "Schwartz et al. (2020) contrasted 'Red AI' (accuracy at any compute cost) with 'Green AI' (efficiency reported and valued). For edge fleets it means measuring energy per inference and scheduling work to save energy.",
        topic="green-ai", level=1),
    tf("Reading a benchmark report, a model with lower average latency but a much higher p99 can be the worse choice for a real-time control loop.", True,
       "Control loops break on the slow cases.",
       "A robot arm or braking system must meet its deadline every cycle. Occasional long stalls (high p99) cause missed deadlines even when the mean looks good. Reports should show percentiles, not just averages.",
       topic="reports", level=1),
    # ------------------------------------------------------------------ L2
    mcq("benchmark_model prints: 'Init: 412000, First inference: 96000, Warmup (avg): 31000, Inference (avg): 24500' (microseconds). Which number is the steady-state latency to compare models with?",
        ["Inference (avg): 24.5 ms",
         "First inference: 96 ms",
         "Init: 412 ms",
         "The sum of all four: 563.5 ms"], 0,
        "Which line excludes one-off start-up costs?",
        "Init is loading the model and building the interpreter/delegate; first inference includes allocation and cold caches; warm-up runs are still settling. The 'Inference (avg)' line averages the timed runs after warm-up. Init and first inference matter for cold-start budgets and are reported separately.",
        topic="bench-metrics", level=2),
    out("latency_ms = 25                     # one inference, batch 1\n"
        "streams = 4                         # 4 cameras, one core each\n"
        "print(1000 / latency_ms, streams * 1000 / latency_ms)",
        ["40.0 160.0", "40 160", "0.04 0.16", "40.0 40.0"], 0,
        "Throughput = runs per second per stream × streams.",
        "One stream: 1000 / 25 = 40 inferences/s. Four independent streams on four cores: 160/s, while each inference still takes 25 ms. Parallelism raises throughput without lowering latency. (Python's / always returns a float: 40.0, not 40.)",
        question="Throughput of a gate-camera model on a quad-core board. What does this print?",
        topic="bench-metrics", level=2),
    tf("The peak memory a benchmark reports for a model includes more than the model file: the runtime, the activation (tensor) buffers and any delegate allocations.", True,
       "What else is in RAM while the model runs?",
       "A 3 MB model can need 10+ MB at run time: activations, the interpreter and delegate workspaces. benchmark_model reports a memory footprint for this reason. On an MCU the equivalent is the tensor arena size plus code.",
       topic="bench-metrics", level=2),
    out("import numpy as np\n"
        "rng = np.random.default_rng(1)\n"
        "lat = np.round(rng.normal(18, 1.0, 200), 1)   # 200 timed runs (ms)\n"
        "lat[::40] += 25                               # 5 runs hit a GC/IO stall\n"
        "print(round(float(lat.mean()), 1), float(np.percentile(lat, 50)),\n"
        "      round(float(np.percentile(lat, 99)), 1))",
        ["18.6 18.0 43.8", "18.0 18.6 43.8", "18.6 18.0 18.6", "43.8 18.0 18.6"], 0,
        "Five slow runs out of 200 is 2.5% of runs.",
        "The 5 stalls nudge the mean to 18.6 ms and leave the median at 18.0, but 2.5% of runs are slow, so p99 lands inside the stall group at ~43.8 ms. An SLA on p99 fails even though the mean looks fine.",
        question="Mean, p50 and p99 of a dairy-line inspection model. What does this print?",
        topic="latency-stats", level=2),
    mcq("A vendor reports only average latency (15 ms) for a crash-detection model. Your SLA is p99 < 20 ms. What should you ask for?",
        ["The per-run timings or a percentile summary (p50, p95, p99) from the same runs",
         "Nothing: if the average is 15 ms, p99 must be below 20 ms",
         "The model's training accuracy",
         "The price of the board"], 0,
        "Can an average tell you about the slowest 1%?",
        "The average says nothing about the tail: 95 runs at 12 ms plus 5 at 70 ms average 14.9 ms, but p99 is 70 ms. To check a tail SLA you need the distribution.",
        topic="latency-stats", level=2),
    fill("A safety system must meet its deadline in all but 1 run in 100. The latency statistic to check is p____ (a number).", "99",
         "1 in 100 slower.",
         "p99: 99% of runs at or below it. For harder real-time guarantees teams also look at p99.9 and the worst case seen, measured over many thousands of runs.",
         topic="latency-stats", level=2),
    out("runs = [210.0, 24.1, 23.8, 24.3, 23.9, 24.0, 24.2, 23.7, 24.0, 24.0]\n"
        "print(round(sum(runs) / len(runs), 1), round(sum(runs[1:]) / len(runs[1:]), 1))",
        ["42.6 24.0", "24.0 42.6", "42.6 42.6", "21.0 24.0"], 0,
        "The first run is the cold one.",
        "Including the 210 ms cold first run pulls the average of 10 runs to 42.6 ms, almost double the true steady state of 24.0 ms. This is the most common benchmarking mistake: discard warm-up runs and report start-up time separately.",
        question="Ten timings from a Raspberry Pi, the first one cold. What does this print?",
        analogy="Like timing a web page using the first request, which compiles templates and fills caches: true once, misleading as 'typical'.",
        diagram="""
run:  1     2     3     4    ...  10
ms:   210   24.1  23.8  24.3      24.0
      ^ cold start: discard (report separately)
""",
        topic="methodology", level=2),
    mcq("Two teams benchmark the same model on the same Jetson and get 9 ms and 21 ms. Which difference is most likely to explain it?",
        ["Different power modes / clock settings or thread counts (e.g. MAXN vs a 10 W mode), which must be fixed and reported",
         "One team used a newer laptop to type the command",
         "The model file was copied twice",
         "Latency is random and cannot be reproduced"], 0,
        "What settings change the hardware's speed?",
        "Jetson power modes (nvpmodel), DVFS governors, thread counts, delegates and batch size all change latency by 2x or more. A benchmark report must state them, or the numbers are not comparable.",
        topic="methodology", level=2),
    tf("For a product, end-to-end latency (capture + preprocessing + inference + postprocessing) can be much larger than the model-only latency that benchmark_model reports.", True,
       "What happens before and after the interpreter's invoke()?",
       "Resizing a 1080p frame, colour conversion, NMS on detections and drawing results can cost as much as the model. benchmark_model times only invoke(). Report both, and optimize the biggest stage.",
       topic="methodology", level=2,
       diagram="""
camera -> resize/normalise -> [ model ] -> NMS -> action
  8 ms         11 ms           14 ms      6 ms
model-only: 14 ms     end-to-end: 39 ms
"""),
    mcq("Which benchmark_model flags would you set to time a model fairly on 4 CPU threads with XNNPACK, 10 warm-up runs and 200 timed runs?",
        ["--graph=model.tflite --num_threads=4 --use_xnnpack=true --warmup_runs=10 --num_runs=200",
         "--model=model.tflite --cores=4 --repeat=200",
         "--graph=model.tflite --num_runs=1",
         "--train --epochs=200"], 0,
        "The tool names the model file 'graph'.",
        "--graph points at the .tflite file; --num_threads, --use_xnnpack (or --use_gpu, --use_nnapi) choose the execution set-up; --warmup_runs and --num_runs control the statistics. Add --enable_op_profiling=true for a per-operator breakdown.",
        topic="bench-tools", level=2),
    mcq("Which list gives the four MLPerf Tiny benchmark tasks?",
        ["Keyword spotting, visual wake words (person / no person), image classification (CIFAR-10), anomaly detection (machine sounds)",
         "Machine translation, summarisation, question answering, chat",
         "Object detection, segmentation, pose estimation, depth estimation at 4K",
         "Training ResNet-50, BERT, GPT-3 and a recommender"], 0,
        "Tasks small enough for a microcontroller.",
        "MLPerf Tiny v0.5 (2021): KWS on Speech Commands with a DS-CNN, VWW with a MobileNetV1 0.25x, CIFAR-10 with ResNet-8, and anomaly detection on ToyADMOS audio with a fully-connected autoencoder. Each has a quality target, so speed is not bought with accuracy.",
        topic="bench-tools", level=2),
    fill("To get a per-operator time breakdown from benchmark_model, add --____=true. (the flag name, no dashes)", "enable_op_profiling",
         "It profiles each op.",
         "--enable_op_profiling=true prints a table of operators (CONV_2D, DEPTHWISE_CONV_2D, RESIZE_BILINEAR...) with their time and % of the total, so you can see which op to optimise or which ones fell back from the delegate to the CPU.",
         topic="bench-tools", level=2),
    out("p_mw, t_ms = 12, 3.5          # MCU active power, keyword-spotting latency\n"
        "e_uj = p_mw * t_ms             # mW x ms = microjoules\n"
        "print(e_uj, round(1e6 / e_uj))   # uJ per inference, inferences per joule",
        ["42.0 23810", "42.0 238", "3.43 291545", "42 23810"], 0,
        "mW × ms = µJ; 1 J = 1,000,000 µJ.",
        "12 mW × 3.5 ms = 42 µJ per inference, so one joule buys 1e6 / 42 ≈ 23,810 inferences. MLPerf Tiny reports energy in µJ per inference for exactly this kind of always-on task. 42.0, not 42: 12 × 3.5 is a float.",
        question="Energy KPIs for an MLPerf-Tiny-style keyword spotter. What does this print?",
        topic="energy-kpis", level=2),
    mcq("A chip datasheet says '4 TOPS/W'. Why is that not the same as the energy efficiency of your model on it?",
        ["TOPS/W is a peak figure for ideal operations; your model's real efficiency depends on utilisation, memory traffic and which ops the accelerator supports, so you must measure inferences per joule",
         "TOPS/W measures storage, not compute",
         "It is the same: divide 4 TOPS/W by the model's operations to get exact energy",
         "TOPS/W only applies to training"], 0,
        "Peak vs achieved.",
        "Peak TOPS assume every MAC unit is busy every cycle on INT8 data already on-chip. Real models stall on memory, run unsupported ops on the CPU and leave units idle. Measured energy per inference (power meter × latency) is the honest KPI.",
        topic="energy-kpis", level=2,
        analogy="Like a car's top speed vs your commute time: the spec sheet number is real, but traffic decides when you arrive."),
    mcq("A latency histogram from 1,000 runs shows two separate humps, one at ~12 ms and one at ~45 ms. What does that usually indicate?",
        ["Two different execution behaviours, e.g. some runs fall back to the CPU, hit a cache miss path, or get preempted by another task",
         "The model is accurate",
         "The benchmark is perfectly stable",
         "The device has two batteries"], 0,
        "One hump = one behaviour.",
        "A bimodal histogram means the runs are not one distribution: find what differs between the fast and slow group (delegate fallback, thermal state, background service, garbage collection). The mean (somewhere between the humps) describes neither.",
        analogy="Like an API latency graph with two humps, cache hits and cache misses: the average is a latency no user ever sees.",
        topic="reports", level=2,
        diagram="""
count
 ##
 ##                       #
 ###                     ###
 ####                   ####
-----------------------------> ms
 12                      45
"""),
    out("ops = {\"CONV_2D\": 14.2, \"DEPTHWISE_CONV_2D\": 6.1, \"ADD\": 0.9,\n"
        "       \"RESIZE_BILINEAR\": 7.8, \"SOFTMAX\": 0.2}      # ms per op type\n"
        "total = sum(ops.values())\n"
        "print(round(total, 1), {k: round(100 * v / total) for k, v in ops.items()})",
        ["29.2 {'CONV_2D': 49, 'DEPTHWISE_CONV_2D': 21, 'ADD': 3, 'RESIZE_BILINEAR': 27, 'SOFTMAX': 1}",
         "29.2 {'CONV_2D': 14, 'DEPTHWISE_CONV_2D': 6, 'ADD': 1, 'RESIZE_BILINEAR': 8, 'SOFTMAX': 0}",
         "29.2 {'CONV_2D': 49, 'DEPTHWISE_CONV_2D': 21, 'ADD': 3, 'RESIZE_BILINEAR': 0, 'SOFTMAX': 1}",
         "14.2 {'CONV_2D': 100}"], 0,
        "Share of total = op time / total time.",
        "RESIZE_BILINEAR takes 27% of the time though it is not a learned layer: a classic sign that a preprocessing op ran on the CPU instead of the accelerator. Op-profile tables tell you where to optimise; total FLOPs would never show it.",
        question="Reading a per-op profile from benchmark_model. What does this print?",
        topic="reports", level=2),
    out("models = {\"P\": (81, 22), \"Q\": (84, 30), \"R\": (84, 35),   # (accuracy %, p95 ms)\n"
        "          \"S\": (79, 25), \"T\": (87, 41)}\n"
        "def dominates(a, b):\n"
        "    return a[0] >= b[0] and a[1] <= b[1] and a != b\n"
        "front = [m for m in models\n"
        "         if not any(dominates(models[o], models[m]) for o in models if o != m)]\n"
        "print(front)",
        ["['P', 'Q', 'T']", "['P', 'Q', 'R', 'T']", "['T']", "['P', 'S', 'T']"], 0,
        "Check each model: is there another at least as accurate AND at least as fast?",
        "R (84%, 35 ms) is dominated by Q (84%, 30 ms): same accuracy, faster. S (79%, 25 ms) is dominated by P (81%, 22 ms): better on both. P, Q and T survive. T alone would be 'highest accuracy', which is not the frontier.",
        question="Pareto frontier for five toll-plaza ANPR models. What does this print?",
        topic="pareto", level=2),
    mcq("Model X: 86% accuracy, 14 ms p95. Model Y: 83% accuracy, 11 ms p95. Which statement is right?",
        ["Neither dominates the other: X is more accurate, Y is faster, so both can be on the frontier",
         "X dominates Y because accuracy matters more",
         "Y dominates X because it is faster",
         "Both are dominated"], 0,
        "Dominance needs 'at least as good on both'.",
        "X wins on accuracy, Y on latency: a trade-off. Neither dominates. Which one to deploy depends on the SLA and how much accuracy you need, not on dominance. Calling the more accurate model 'dominant' is the common exam slip.",
        diagram="""
acc %
 86 |             X (14 ms)
 83 |      Y (11 ms)
    +----------------------> p95 ms
X wins on accuracy, Y on latency: no dominance
""",
        topic="pareto", level=2),
    out("def dominates(a, b):              # a, b = (accuracy %, p95 ms)\n"
        "    return a[0] >= b[0] and a[1] <= b[1] and a != b\n"
        "print(dominates((80, 10), (80, 10)),\n"
        "      dominates((80, 10), (80, 12)),\n"
        "      dominates((82, 12), (80, 10)))",
        ["False True False", "True True False", "False True True", "True True True"], 0,
        "Identical models: is either strictly better on anything?",
        "Equal on both metrics: no strict improvement, so no dominance (that is what a != b enforces). Same accuracy, 2 ms faster: dominates. More accurate but slower: a trade-off, no dominance. This mirrors the paper's A (74%, 8 ms) vs C (74%, 10 ms).",
        question="Three dominance checks. What does this print?",
        topic="pareto", level=2),
    out("models = {\"P\": (81, 22), \"Q\": (84, 30), \"T\": (87, 41)}   # the frontier\n"
        "ok = [m for m in models if models[m][1] < 30]   # SLA: p95 strictly below 30 ms\n"
        "print(ok, max(ok, key=lambda m: models[m][0]))",
        ["['P'] P", "['P', 'Q'] Q", "['P', 'Q', 'T'] T", "[] None"], 0,
        "Q sits exactly at 30 ms.",
        "Strictly below 30 ms means Q (30 ms) fails along with T (41 ms), so only P remains and is selected. Using <= would pick Q, the most common wrong answer. If the business needs Q's accuracy, the fix is to optimize Q, not to bend the SLA.",
        question="Selecting from the frontier under a strict SLA. What does this print?",
        topic="sla-selection", level=2),
    mcq("What is the right order of steps to select a model from a candidate table under a latency SLA?",
        ["Remove dominated models (find the frontier), remove models that violate the SLA, then pick the most accurate remaining model and check other constraints (size, power)",
         "Pick the most accurate model, then ask for the SLA to be relaxed",
         "Pick the fastest model, whatever its accuracy",
         "Average the accuracy and latency of each model and pick the highest average"], 0,
        "Frontier, filter, pick.",
        "The frontier step removes models that are never worth choosing; the SLA filter removes the infeasible ones (the two steps commute); among what remains you maximise accuracy. Mixing units into one 'average score' has no meaning.",
        diagram="""
candidates -> drop dominated   -> frontier
frontier   -> drop SLA misses  -> feasible
feasible   -> max accuracy     -> check size/power
""",
        topic="sla-selection", level=2),
    mcq("A TinyML benchmark report for a keyword spotter on a Cortex-M4 lists memory. Which two numbers should it give?",
        ["Flash used (model weights + code, read-only) and SRAM used (tensor arena + stack + buffers, read-write)",
         "Only the .tflite file size",
         "GPU memory and disk space",
         "The size of the training dataset and the number of epochs"], 0,
        "One memory holds what never changes, the other what changes every inference.",
        "On an MCU the weights live in Flash (often 1-2 MB) and run in place, while activations need SRAM (often 128-512 KB), which is usually the tighter limit. A report with only the model size cannot tell you whether the model will run.",
        topic="tinyml", level=2,
        diagram="""
Flash (1 MB):  [ firmware code ][ model weights 180 KB ]
SRAM (256 KB): [ stack ][ audio buffer ][ tensor arena ]
"""),
    tf("A common TinyML pattern is a cascade: a tiny always-on model (e.g. wake-word or motion detection) on the MCU wakes a larger model or a more powerful processor only when needed.", True,
       "Think of 'Hey Google' or 'Alexa'.",
       "The tiny first stage runs at ~mW all the time; the expensive stage runs rarely. Average power stays close to the tiny model's, while accuracy comes from the big one.",
       topic="tinyml", level=2,
       diagram="""
mic --> [KWS on MCU, ~1 mW, always on]
             | wake word detected (rare)
             v
        [big ASR on app CPU / cloud, ~1 W, seconds]
"""),
    out("params = 3e9                       # a 3B small language model\n"
        "for name, b in [(\"FP16\", 2), (\"INT8\", 1), (\"INT4\", 0.5)]:\n"
        "    gb = params * b / 1e9\n"
        "    print(name, gb, gb <= 4 * 0.5)  # phone with 4 GB, ~half free for one app",
        ["FP16 6.0 False\nINT8 3.0 False\nINT4 1.5 True", "FP16 6.0 False\nINT8 3.0 True\nINT4 1.5 True",
         "FP16 3.0 True\nINT8 1.5 True\nINT4 0.75 True", "FP16 6.0 False\nINT8 3.0 False\nINT4 1.5 False"], 0,
        "Weights only, before the KV cache and the app itself.",
        "3B × 2 B = 6 GB, × 1 B = 3 GB, × 0.5 B = 1.5 GB. Only 4-bit fits the ~2 GB an Android app can realistically use on a 4 GB phone, and the KV cache still needs room. That is why edge LLMs ship 4-bit.",
        question="Can a 3B edge LLM fit on a 4 GB phone? What does this print?",
        topic="edge-genai", level=2),
    mcq("Why does cutting the number of denoising steps (e.g. from 50 to 4 by step distillation) matter so much for running a diffusion image generator on a phone?",
        ["Each step is a full pass of the large denoising network, so generation time and energy scale almost linearly with the number of steps",
         "Fewer steps make the model file smaller",
         "Phones can only run 4 steps because of their screen",
         "Steps only affect training, not inference"], 0,
        "A diffusion image is generated by repeating one network many times.",
        "50 UNet passes at 0.4 s each is 20 s; 4 passes is 1.6 s. Step distillation (and smaller, quantized UNets) is how compressed diffusion models reach on-device speed. The file size depends on the network, not on the step count.",
        topic="edge-genai", level=2),
    mcq("An ATM-security system fuses a camera and a vibration sensor. What is the difference between early and late fusion?",
        ["Early fusion combines raw data or features into one model input; late fusion runs a model per sensor and combines their decisions",
         "Early fusion runs in the morning; late fusion at night",
         "Early fusion uses one sensor; late fusion uses two",
         "Late fusion trains the models later"], 0,
        "When are the streams merged: before or after the models?",
        "Early fusion can learn cross-sensor patterns but needs synchronised, always-present inputs. Late fusion is simpler and degrades gracefully if one sensor fails, but misses fine interactions. Intermediate fusion merges learned features in between.",
        topic="collab-trends", level=2,
        diagram="""
early: cam + vib --> [one model] --> decision
late:  cam --> [model A] --\\
                            +--> combine --> decision
       vib --> [model B] --/
"""),
    mcq("How does federated analytics differ from federated learning?",
        ["Federated analytics computes aggregate statistics (counts, histograms, averages) across devices without collecting raw data; federated learning trains a model",
         "They are the same thing",
         "Federated analytics sends all raw data to the cloud",
         "Federated learning never leaves the device; federated analytics trains in the cloud"], 0,
        "Statistics vs model weights.",
        "Example: a city learns how many e-scooter rides cross each zone per hour by having each scooter report only local counts to an aggregator (often with differential privacy). No model is trained. FL instead sends model updates.",
        diagram="""
FA: local counts   -> aggregator -> city-wide statistics
FL: local training -> updates    -> global model
raw data stays on the devices in both
""",
        topic="collab-trends", level=2),
    out("devices, watts, hours = 2000, 15, 24        # Jetson fleet, average draw\n"
        "kwh = devices * watts * hours / 1000\n"
        "print(kwh, round(kwh * 0.7))                 # kg CO2 at 0.7 kg/kWh (India grid)",
        ["720.0 504", "720 504", "720000.0 504000", "720.0 1029"], 0,
        "W × h / 1000 = kWh; then × grid intensity.",
        "2,000 × 15 W × 24 h = 720 kWh per day; × 0.7 kg CO2/kWh ≈ 504 kg CO2 per day. Dividing by 0.7 (1029) is the slip. Carbon follows energy, so every mJ per inference saved scales across the fleet.",
        question="Daily energy and carbon of a city-wide edge fleet. What does this print?",
        topic="green-ai", level=2),
    mcq("What is 'race-to-idle' in energy-aware scheduling?",
        ["Finish the work as fast as possible at high clock speed, then drop to a deep sleep state, because idle/sleep power is very low and static power is paid for every second awake",
         "Let devices race each other to finish first",
         "Always run at the lowest clock speed",
         "Keep the processor busy all the time to avoid sleeping"], 0,
        "Static power is paid for every second the chip is awake.",
        "Energy = power × time. Running slowly at low clock lowers dynamic power but stretches the awake time, during which static/leakage and board power keep draining. Often finishing fast and sleeping uses less energy; measure both on your device, because the best point varies.",
        analogy="Like batching background jobs so a server can sleep longer, instead of trickling them all day and never idling.",
        topic="green-ai", level=2),
    # ------------------------------------------------------------------ L3
    mcq("Delhi Metro evaluates four fare-gate face-mask models: A (91%, 16 ms p95, 7 MB), B (88%, 11 ms, 4 MB), C (88%, 13 ms, 5 MB), D (93%, 21 ms, 9 MB). The SLA requires p95 strictly below 16 ms. Which model is selected?",
        ["B: C is dominated by B, the frontier is B, A, D, and A (exactly 16 ms) and D (21 ms) both fail the strict SLA",
         "A: it is the most accurate model that meets 16 ms",
         "D: it is the most accurate model overall",
         "C: it meets the SLA and is more accurate than the slowest model"], 0,
        "Check the boundary case before picking the most accurate one.",
        "Dominance: B beats C (same 88%, faster). A, B, D are a trade-off chain: the frontier. SLA filter: A at 16 ms is not strictly below 16, D is far over, so B (88%, 11 ms) is the pick. 'A' is the boundary trap; C is never chosen because B is at least as good on everything.",
        topic="sla-selection", level=3,
        diagram="""
acc %
 93 |                      D (21)
 91 |               A (16)
 88 |      B (11)  C (13)
    +------|-------|----|----|----> p95 ms
          11      13   16   21
               SLA: < 16 ms
"""),
    out("models = {\"A\": (91, 16), \"B\": (88, 11), \"C\": (88, 13), \"D\": (93, 21)}\n"
        "def dominates(a, b):\n"
        "    return a[0] >= b[0] and a[1] <= b[1] and a != b\n"
        "front = [m for m in models\n"
        "         if not any(dominates(models[o], models[m]) for o in models if o != m)]\n"
        "ok = [m for m in front if models[m][1] < 16]\n"
        "print(front, ok, max(ok, key=lambda m: models[m][0]))",
        ["['A', 'B', 'D'] ['B'] B", "['A', 'B', 'D'] ['A', 'B'] A", "['A', 'B', 'C', 'D'] ['B', 'C'] C", "['D'] [] D"], 0,
        "Frontier first, then the strict filter, then the most accurate survivor.",
        "C is dominated by B. Of the frontier A, B, D only B is strictly below 16 ms. Changing < to <= would wrongly admit A: one character decides the exam answer.",
        question="The same metro selection, as code. What does this print?",
        topic="pareto", level=3),
    mcq("End-sem style, 1 mark: why should a Pareto-dominated model never be selected, even if it satisfies every deployment constraint?",
        ["Some frontier model is at least as good on every metric and strictly better on one, and it also satisfies the constraints, so choosing the dominated one gives up something for nothing",
         "Dominated models are always inaccurate",
         "Dominated models cannot be deployed technically",
         "Because the frontier always contains exactly one model"], 0,
        "If C meets the SLA, what about the model that dominates it?",
        "If B dominates C and C meets a latency SLA, B is at least as fast, so B meets it too, with equal or better accuracy. There is no situation (on these metrics) where C is the better choice. If another metric (size, power) matters, add it to the dominance check instead.",
        topic="pareto", level=3),
    mcq("A Surat diamond-sorting line has a frontier of three models: X (95%, 8 ms, 12 MB), Y (93%, 6 ms, 3 MB), Z (97%, 14 ms, 20 MB). SLA: p95 strictly below 10 ms; the controller has 8 MB free for the model. Which is selected?",
        ["Y: Z fails latency, X fails the 8 MB memory limit, Y passes both",
         "X: highest accuracy under 10 ms",
         "Z: highest accuracy",
         "None: no model is on the frontier"], 0,
        "Apply every constraint, not just latency.",
        "Latency removes Z (14 ms). Memory removes X (12 MB > 8 MB). Y remains. Picking X is the slip of checking only the latency SLA; the papers' size column is there for this check.",
        topic="sla-selection", level=3),
    mcq("A team measures their candidate at 9.2 ms p95 on a development laptop, against an SLA of p95 < 10 ms on a Raspberry Pi 4 in a hot enclosure. What is the sound conclusion?",
        ["Nothing yet: the SLA must be measured on the target device, in its real thermal and power conditions, ideally with some headroom",
         "It passes: 9.2 is below 10",
         "It fails, because laptops are always slower",
         "Add 0.8 ms to account for the Pi and it passes"], 0,
        "Where does the SLA apply?",
        "A laptop CPU can be 3-10x faster than a Cortex-A72, and a hot enclosure throttles clocks. The SLA is a property of the model on the deployed device. Teams also leave headroom (e.g. target 8 ms) for OS jitter and future features.",
        topic="sla-selection", level=3),
    out("import numpy as np\n"
        "a = np.array([12, 12, 13, 12, 13, 12, 12, 13, 12, 40])   # model A, ms\n"
        "b = np.array([15, 15, 15, 16, 15, 15, 16, 15, 15, 16])   # model B, ms\n"
        "for x in (a, b):\n"
        "    print(float(np.percentile(x, 50)), round(float(np.percentile(x, 99)), 2),\n"
        "          round(float(x.mean()), 1))",
        ["12.0 37.57 15.1\n15.0 16.0 15.3", "12.0 40.0 15.1\n15.0 16.0 15.3",
         "12.5 37.57 15.1\n15.0 16.0 15.3", "15.1 37.57 12.0\n15.3 16.0 15.0"], 0,
        "NumPy interpolates: position 0.99 × 9 = 8.91 in the sorted array.",
        "A is faster typically (p50 12 ms) but its one 40 ms stall puts p99 at 37.57 ms (13 + 0.91 × 27). B is slower on average yet tight (p99 16 ms, jitter ~1 ms). For a 20 ms motor-control deadline B is the safer model, though A has the better median.",
        question="Median, p99 and mean of two robot-arm models (10 runs each, NumPy's linear percentile). What does this print?",
        topic="latency-stats", level=3),
    out("import numpy as np\n"
        "lat = np.array([8.2, 9.1, 9.9, 10.0, 8.7, 9.5, 10.4, 9.0, 8.8, 9.7])\n"
        "print(int((lat < 10).sum()), round(float(np.percentile(lat, 95)), 2))",
        ["8 10.22", "9 10.22", "8 10.4", "10 9.9"], 0,
        "Strictly below 10: is 10.0 counted?",
        "Eight runs are strictly below 10 ms (10.0 and 10.4 are not). p95 interpolates between 10.0 and 10.4: 10.22 ms, which fails a 'p95 < 10 ms' SLA. Counting 10.0 as passing gives 9, the boundary slip again.",
        question="Checking ten runs of a weighbridge model against 'strictly below 10 ms'. What does this print?",
        topic="latency-stats", level=3),
    out("t = [20] * 30 + [32] * 90      # latency (ms) once per second for 2 minutes\n"
        "print(round(sum(t[:10]) / 10, 1), round(sum(t) / len(t), 1),\n"
        "      round(sum(t[-30:]) / 30, 1))",
        ["20.0 29.0 32.0", "20.0 26.0 32.0", "32.0 29.0 20.0", "20.0 29.0 29.0"], 0,
        "The board throttles after 30 s.",
        "A 10-second benchmark sees 20 ms. After 30 s the SoC heats up and drops its clocks: 32 ms. The 2-minute average (29 ms) mixes both. A product running all day sees the sustained 32 ms, so benchmark until temperature and latency stabilise, or add cooling.",
        question="Latency of a fanless Jetson in a toll booth over two minutes. What does this print?",
        topic="methodology", level=3,
        diagram="""
ms
32 |              ________________________
   |             |
20 |_____________|
   +-------------|------------------------> s
   0            30 (throttling starts)  120
"""),
    mcq("A report compares Board A (FP32 model, 640×640 input) at 48 ms with Board B (INT8 model, 320×320 input) at 9 ms and concludes 'B is 5x faster hardware'. What is wrong?",
        ["The model, precision and input size all differ, so the result mixes hardware with model changes; a fair hardware comparison runs the same model, precision and input on both",
         "Nothing; latency is latency",
         "INT8 models are always slower, so B must be faster still",
         "The comparison should use training time instead"], 0,
        "Change one variable at a time.",
        "320×320 is 4x fewer pixels and INT8 is often 2-3x faster than FP32 on the same chip, so most of the gap may be the model, not the board. MLPerf's closed division exists precisely to fix the model for hardware comparisons.",
        topic="methodology", level=3,
        analogy="Like comparing two databases by running different queries on each: the result says more about the queries than the engines."),
    mcq("In MLPerf Tiny, what is the difference between the closed and open divisions?",
        ["Closed: everyone runs the same reference model (to the quality target), so results compare hardware and software stacks. Open: submitters may change the model, to show what co-design achieves",
         "Closed results are secret; open results are public",
         "Closed division is for training, open for inference",
         "Closed uses batch 1, open uses batch 32"], 0,
        "What is held fixed?",
        "Fixing the model isolates the platform: if Board X beats Board Y in the closed division, it is the hardware/runtime, not a smaller network. The open division rewards model innovation but its numbers cannot be read as pure hardware comparisons.",
        diagram="""
task               data          reference model
keyword spotting   Speech Cmds   DS-CNN
visual wake words  COCO person   MobileNetV1 0.25x
image classif.     CIFAR-10      ResNet-8
anomaly detection  ToyADMOS      FC autoencoder
""",
        topic="bench-tools", level=3),
    mcq("benchmark_model with --use_gpu=true is barely faster than CPU. The op profile shows most CONV_2D ops on the GPU delegate but several RESIZE and custom ops on the CPU, with many 'delegate' partitions. What is the likely problem?",
        ["Unsupported ops split the graph into several GPU partitions with CPU ops between them, so data is copied back and forth and the gains are eaten up",
         "The GPU is broken",
         "Op profiling slows everything down, so the numbers are meaningless",
         "The model is too accurate for the GPU"], 0,
        "Each hop between delegate and CPU copies tensors.",
        "A delegate only runs the ops it supports. Each unsupported op forces a CPU island, and each transition costs a memory copy and synchronisation. Fixes: replace unsupported ops, move resize into preprocessing, or keep the whole model on one backend.",
        topic="bench-tools", level=3,
        diagram="""
[GPU: conv x12] -> CPU: RESIZE -> [GPU: conv x8]
     -> CPU: CUSTOM_OP -> [GPU: conv x4] -> out
each arrow = copy + sync
"""),
    tf("MLPerf Tiny attaches a quality target (e.g. a minimum accuracy) to each task, so a submission cannot report a faster time with a model that has lost too much accuracy.", True,
       "Speed without accuracy is not a result.",
       "Each benchmark has a target (e.g. ~90% top-1 for keyword spotting, ~85% for CIFAR-10, ~80% for visual wake words, AUC ~0.85 for anomaly detection). The rule mirrors product reality: latency only counts at acceptable accuracy.",
       topic="bench-tools", level=3),
    out("p_active_mw, p_sleep_mw = 30.0, 0.05\n"
        "t_active_ms, period_ms = 50, 1000          # one inference per second\n"
        "d = t_active_ms / period_ms\n"
        "avg_mw = p_active_mw * d + p_sleep_mw * (1 - d)\n"
        "battery_j = 2.5 * 3 * 3600                  # 2500 mAh at 3 V\n"
        "print(round(avg_mw, 4), round(battery_j / (avg_mw / 1000) / 86400, 1))",
        ["1.5475 201.9", "30.05 10.4", "1.5 208.3", "1.5475 8.4"], 0,
        "Average power = active × duty + sleep × (1 − duty).",
        "Duty cycle 5%: 30 × 0.05 + 0.05 × 0.95 = 1.5475 mW. A 7.5 Wh (27,000 J) pack lasts 27,000 / 0.0015475 s ≈ 202 days. Using active power alone (30 mW) predicts ~10 days. Ignoring sleep power (1.5 mW) gives 208 days: small here, but sleep dominates at lower duty cycles.",
        question="Battery life of a duty-cycled cold-chain sensor in a Kochi fish market. What does this print?",
        diagram="""
power
30 mW   |##                    ##
        |##                    ##
0.05 mW |##____________________##____
        0  50 ms            1000  1050 ms
""",
        topic="energy-kpis", level=3),
    out("chips = {\"A\": (4, 8), \"B\": (2, 5)}   # (datasheet TOPS/W, measured mJ/inference)\n"
        "for name, (tops_w, mj) in chips.items():\n"
        "    print(name, tops_w, round(1000 / mj))   # inferences per joule",
        ["A 4 125\nB 2 200", "A 4 200\nB 2 125", "A 4 8\nB 2 5", "A 4 0.125\nB 2 0.2"], 0,
        "1 J = 1000 mJ.",
        "Chip A has twice the datasheet TOPS/W but needs 8 mJ per inference on this model (125 inferences/J); chip B manages 200/J. Low utilisation, memory traffic or ops falling back to the CPU make peak efficiency irrelevant. Choose by the measured KPI on your model.",
        question="Datasheet vs measured efficiency for a dairy-cattle ID model. What does this print?",
        topic="energy-kpis", level=3),
    mcq("Which energy KPI best fits an always-on vibration sensor that runs one 2 ms inference every 10 seconds on a coin cell?",
        ["Average power over the duty cycle (dominated by sleep current), and the battery life it implies",
         "Peak TOPS of the MCU",
         "Inferences per second at full load",
         "Energy per inference only"], 0,
        "What is the chip doing 99.98% of the time?",
        "Active for 2 ms in 10 s is a 0.02% duty cycle, so sleep power and wake-up overhead dominate the battery budget. Energy per inference matters for burst workloads; for rare inferences, average power and battery life are the honest KPIs.",
        topic="energy-kpis", level=3),
    mcq("A box plot of latency for three runtimes shows: R1 median 20 ms, short box, few outliers; R2 median 15 ms, tall box, whiskers to 60 ms; R3 median 25 ms, very short box. For a p95 < 30 ms SLA, what can you read off?",
        ["R1 and R3 are likely to meet it (tight spread under 30); R2 has the best median but its wide spread and long whisker put its p95 at risk; check the actual p95 values",
         "R2 is best because its median is lowest",
         "R3 is worst because its median is highest",
         "Box plots cannot show latency"], 0,
        "The box spans the middle 50%; whiskers and dots show the tail.",
        "Box plots show median, interquartile range and outliers: exactly the distribution information an average hides. A low median with a long upper whisker is the classic 'fast usually, slow sometimes' profile that fails tail SLAs.",
        topic="reports", level=3),
    mcq("A latency-vs-batch-size chart for a Jetson shows throughput rising from 60 to 400 images/s as batch goes 1 -> 16, then flattening, while per-batch latency grows from 17 ms to 40 ms and then keeps growing. How should a CCTV-analytics team read it?",
        ["Batch ~16 is where the GPU saturates: larger batches only add latency. Choose the largest batch whose latency still meets the per-frame SLA",
         "Always use batch 1, because it has the lowest latency",
         "Always use the largest batch, because throughput never stops rising",
         "Latency and throughput are unrelated, so the chart is useless"], 0,
        "Find the knee of the throughput curve.",
        "Before the knee, batching fills idle GPU units, so throughput rises much faster than latency. After it, the GPU is saturated: more batching just makes each frame wait. The operating point sits at or below the knee, inside the SLA.",
        topic="reports", level=3,
        diagram="""
throughput                 latency
400 |      ________         |            /
    |     /                 |         /
 60 |____/                  |______/
    +---|-----> batch       +---|-----> batch
        16                      16
"""),
    out("sram_kb, reserved_kb = 256, 64     # Cortex-M4: app, stack, buffers\n"
        "arena_kb = 210                      # TFLite Micro arena reported for the model\n"
        "print(arena_kb <= sram_kb - reserved_kb, sram_kb - reserved_kb - arena_kb)",
        ["False -18", "True 46", "True -18", "False 46"], 0,
        "Only what is left after the application is available to the arena.",
        "256 − 64 = 192 KB free, the arena needs 210 KB: it does not fit by 18 KB. Comparing the arena with the full 256 KB says 'fits' and fails at start-up. Fixes: smaller input, fewer channels in early layers, INT8 activations, or a board with more SRAM.",
        question="Does a TinyML gesture model fit the MCU's SRAM? What does this print?",
        topic="tinyml", level=3),
    mcq("Which workload is a poor fit for TinyML on a Cortex-M class MCU?",
        ["Real-time multi-object detection on 1080p video at 30 FPS",
         "Keyword spotting on a 1-second audio window",
         "Vibration anomaly detection on a pump",
         "Person / no-person detection on a 96×96 grayscale image"], 0,
        "Compare the data rate and compute with ~100 KB of RAM and ~100 MHz.",
        "KWS, vibration and visual wake words use tiny inputs and models of tens to hundreds of KB: the MLPerf Tiny tasks. 1080p detection needs MBs of activations and billions of MACs per frame: a Jetson/NPU job. Knowing the boundary is part of designing the system.",
        topic="tinyml", level=3),
    out("bw_gb_s = 51.2                       # phone LPDDR5 memory bandwidth\n"
        "for model_gb in (1.5, 4.0):          # 3B and 8B models at 4-bit\n"
        "    print(round(bw_gb_s / model_gb, 1))   # tokens/s upper bound",
        ["34.1\n12.8", "12.8\n34.1", "76.8\n204.8", "34\n13"], 0,
        "Each generated token reads every weight once.",
        "Decoding one token streams the whole weight file from memory, so tokens/s ≤ bandwidth ÷ model bytes: ~34 tokens/s for a 1.5 GB model, ~13 for 4 GB, before any compute limits. That is why edge LLM benchmarks report tokens/s and why 4-bit and smaller models matter more than NPU TOPS.",
        question="Upper bound on decode speed for two on-device LLMs. What does this print?",
        diagram="""
every token: read ALL weights from DRAM
DRAM ==51.2 GB/s==> SoC
1.5 GB / 51.2 GB/s = 29 ms/token -> ~34 tok/s
""",
        topic="edge-genai", level=3),
    mcq("A benchmark of an on-device 3B LLM reports 'time to first token 2.8 s, decode 14 tokens/s'. A user complains that summarising a long WhatsApp chat takes ages before anything appears. Which number explains it, and what drives it?",
        ["Time to first token: the prompt (prefill) is processed before output starts, and it grows with prompt length",
         "Decode speed: 14 tokens/s is too slow to start",
         "Neither; the phone's screen is slow",
         "Model loading only happens once, so it cannot matter"], 0,
        "Which phase runs before the first word appears?",
        "Prefill processes all input tokens (compute-heavy, grows with prompt length) before the first output token; decode then produces tokens one by one (bandwidth-bound). Long prompts on phones hurt TTFT, so edge GenAI benchmarks report both, at stated prompt lengths.",
        topic="edge-genai", level=3),
    out("h, w, c = 28, 28, 32                 # cut-layer activation per image\n"
        "act_bytes = h * w * c * 4             # float32\n"
        "print(act_bytes, round(act_bytes * 32 / 1e6, 2))   # per image, per batch of 32 (MB)",
        ["100352 3.21", "25088 0.8", "100352 0.1", "401408 12.85"], 0,
        "Smashed data = the cut layer's activations, sent every step.",
        "28 × 28 × 32 × 4 B = 100,352 B per image, ~3.2 MB per batch of 32, uploaded every training step, with gradients of the same size coming back. Split learning saves device compute and memory but needs a steady link; compare with FL, which sends one model update per round.",
        question="Upload per training step in split learning for a smartphone-camera model. What does this print?",
        topic="collab-trends", level=3,
        diagram="""
device: input -> layers 1..k -> smashed acts --+
                                               | up
server: layers k+1..n -> loss <----------------+
device: <------ gradients at the cut (down)
"""),
    mcq("Why is split learning attractive for very small devices compared with federated learning?",
        ["The device runs only the first few layers, so it needs far less compute and memory than training the whole model locally as FL requires",
         "Split learning sends no data at all",
         "Split learning works offline for weeks",
         "Split learning makes the model more accurate than centralised training"], 0,
        "Who trains which layers?",
        "In FL every client trains the full model. In split learning the client only holds layers up to the cut, so a microcontroller-class device can take part. The price: a round-trip to the server every step, and activations that can leak information about the inputs.",
        analogy="Like a thin client that does the first bit of work locally and lets the server do the heavy part, at the cost of a network round-trip per interaction.",
        topic="collab-trends", level=3),
    mcq("Eight drones search a flooded area in Assam. Option 1: each streams video to a ground server that assigns zones. Option 2: drones share compact detections with neighbours and re-divide zones among themselves (swarm). When is option 2 the better design?",
        ["When the link to the ground is weak or may drop, because the swarm keeps working without a central point of failure and sends far less data",
         "When the ground link has unlimited bandwidth and never fails",
         "Always, because central control is never useful",
         "Only when all drones run identical models"], 0,
        "What happens to option 1 if the ground link fails?",
        "Central control is simpler and globally optimal when communication is reliable. Swarms trade that for robustness and bandwidth: local decisions, only small messages exchanged, graceful degradation if a drone or link is lost. The cost is coordination (agreement) overhead and harder testing.",
        topic="collab-trends", level=3),
    out("saved_j = (0.108 - 0.0468) * 10 * 86400 * 500   # J saved per inference x rate x s/day x devices\n"
        "print(round(saved_j / 3.6e6, 2))                  # kWh per day",
        ["7.34", "26438400.0", "0.73", "73.44"], 0,
        "1 kWh = 3.6 million joules.",
        "Saving 61.2 mJ per inference at 10 inferences/s on 500 devices saves 26.4 MJ, i.e. 7.34 kWh per day (~5 kg CO2 at 0.7 kg/kWh). Small per inference, large across a fleet and a year: the Green AI case for optimizing deployed models.",
        question="Fleet energy saved by an INT8 model (108 -> 46.8 mJ per inference). What does this print?",
        topic="green-ai", level=3),
    mcq("A cold-start budget says the app must show a result within 1.5 s of launch. benchmark_model reports Init 900 ms, First inference 650 ms, Inference (avg) 40 ms. Does it meet the budget?",
        ["No: launch needs init + first inference ≈ 1.55 s, so the steady-state 40 ms is irrelevant for this budget",
         "Yes: inference takes only 40 ms",
         "Yes: init does not count",
         "No: 40 ms is too slow"], 0,
        "Which numbers does a user pay at launch?",
        "Cold start = model load and interpreter/delegate set-up + the slow first inference: 900 + 650 = 1,550 ms > 1,500 ms. Fixes: cache the compiled delegate (e.g. GPU serialization), load in the background, or warm the model before showing the screen.",
        diagram="""
launch |--- init 900 ---|-- first 650 --|> 1550 ms
budget |------------ 1500 ms ----------|
""",
        topic="bench-metrics", level=3),
    # ------------------------------------------------------------------ L4
    out("m = {\"A\": (90, 12, 6.0), \"B\": (88, 9, 3.0),     # (acc %, p95 ms, MB)\n"
        "     \"C\": (88, 10, 2.5), \"D\": (86, 10, 4.0)}\n"
        "def dom(a, b):     # acc up, latency down, size down\n"
        "    return a[0] >= b[0] and a[1] <= b[1] and a[2] <= b[2] and a != b\n"
        "print([k for k in m if not any(dom(m[o], m[k]) for o in m if o != k)])",
        ["['A', 'B', 'C']", "['A', 'B']", "['A', 'B', 'C', 'D']", "['B', 'C']"], 0,
        "On accuracy and latency alone, B dominates C. Does it still with size added?",
        "With two objectives C (88%, 10 ms) is dominated by B (88%, 9 ms). With size as a third objective C is the smallest (2.5 MB), so nothing beats it on all three: it rejoins the frontier. D is dominated by C (better accuracy, same latency, smaller). Which objectives you include changes the frontier, so state them.",
        question="A three-objective Pareto frontier for a smart-meter model. What does this print?",
        topic="pareto", level=4),
    mcq("The paper's Pareto question uses accuracy and p95 latency only, and the table also lists model size. When should size be added as a third objective rather than checked afterwards as a constraint?",
        ["When smaller is genuinely better across the range (e.g. OTA bandwidth costs or many models sharing Flash), not just 'must be under X MB'; a hard limit is handled as a constraint filter",
         "Never: Pareto analysis only works with two metrics",
         "Always: every column in a table must be an objective",
         "Only when all models have the same size"], 0,
        "Objective = 'more is better'; constraint = 'must pass'.",
        "A hard limit (≤ 8 MB) is a filter: any model under it is equally fine. If every MB costs money (cellular OTA to 10,000 meters), size is a real objective and belongs in the dominance check. Adding objectives makes the frontier larger, so fewer models can be discarded.",
        topic="pareto", level=4),
    out("import numpy as np\n"
        "rng = np.random.default_rng(3)\n"
        "lat = rng.lognormal(mean=3.0, sigma=0.3, size=20000)   # 'true' distribution, ms\n"
        "print(round(float(lat[:20].max()), 1), round(float(np.percentile(lat, 99)), 1))",
        ["54.4 40.3", "40.3 54.4", "54.4 54.4", "20.1 40.3"], 0,
        "With 20 runs, how many land in the slowest 1%?",
        "The max of the first 20 runs (54.4 ms) is not the p99 (40.3 ms over 20,000 runs): with 20 samples the 'tail' is one or two lucky or unlucky values, so it can over- or under-state p99 badly. Estimating p99 needs hundreds to thousands of runs; p99.9 needs more.",
        question="Is the slowest of 20 runs a good p99 estimate? What does this print?",
        topic="latency-stats", level=4),
    out("import math\n"
        "import numpy as np\n"
        "x = np.array([10, 11, 11, 12, 12, 12, 13, 14, 15, 30])   # ms, 10 runs\n"
        "interp = round(float(np.percentile(x, 95)), 2)\n"
        "nearest = int(np.sort(x)[math.ceil(0.95 * len(x)) - 1])\n"
        "print(interp, nearest)",
        ["23.25 30", "30 30", "15 30", "23.25 15"], 0,
        "Nearest-rank takes an actual sample; NumPy interpolates.",
        "Linear interpolation: position 0.95 × 9 = 8.55, so 15 + 0.55 × 15 = 23.25 ms. Nearest-rank: the ceil(9.5) = 10th value, 30 ms. Same data, two 'p95s'. With few runs the convention matters, so state it in the answer (the bank uses NumPy's default) and prefer more runs.",
        question="Two percentile conventions on the same 10 runs. What does this print?",
        topic="latency-stats", level=4),
    out("idle_w, busy_w, t_ms = 3.1, 4.3, 20      # USB power meter on a Pi\n"
        "print(round(busy_w * t_ms, 1), round((busy_w - idle_w) * t_ms, 1))   # mJ",
        ["86.0 24.0", "24.0 86.0", "86.0 62.0", "4.3 1.2"], 0,
        "Total energy vs energy above the idle baseline.",
        "Total: 4.3 W × 20 ms = 86 mJ per inference. Marginal (above idle): 1.2 W × 20 ms = 24 mJ. For a dedicated device that is on anyway, the total over time matters; for comparing models on the same board, the marginal energy isolates the model. Reports must say which they used.",
        question="Two ways to report energy per inference from a wall-plug meter. What does this print?",
        topic="energy-kpis", level=4),
    mcq("A Pi benchmarked under the default 'ondemand' CPU governor shows the first ~50 timed runs much slower and very spiky, then stable. What is the best practice for a reproducible benchmark?",
        ["Fix the governor and clocks (e.g. 'performance') or warm up long enough for clocks to settle, and report the setting; also check for thermal throttling during long runs",
         "Average all runs anyway; spikes cancel out",
         "Use only the fastest run",
         "Benchmark only on the cloud"], 0,
        "Who is changing the clock speed?",
        "Dynamic governors raise clocks only after load is detected, so early runs run slow. Fixing the governor removes one source of variance; reporting it lets others reproduce the number. Product teams may also benchmark with the default governor, because that is what users get: say which.",
        topic="methodology", level=4),
    mcq("In MLPerf Inference's edge category, what metric does the single-stream scenario report, and what does offline report?",
        ["Single-stream: 90th-percentile latency of one-at-a-time queries. Offline: throughput (samples per second) with all data available at once",
         "Single-stream: average latency. Offline: average latency at batch 1",
         "Single-stream: energy only. Offline: accuracy only",
         "Both report the maximum latency"], 0,
        "One models a phone camera, the other a batch job.",
        "Single-stream mimics an app sending one query after another (a tail-latency metric, the 90th percentile). Offline mimics batch processing (photo library indexing), where only throughput matters. Multi-stream models several cameras. Picking the scenario that matches your product is the point.",
        topic="bench-tools", level=4),
    tf("In MLPerf Tiny energy runs, EEMBC's EnergyRunner set-up powers the device under test from a separate energy monitor and talks to it through an isolated IO manager, so the host's USB connection does not distort the energy measurement.", True,
       "What else would a USB cable supply?",
       "If the host's USB powered the board, its current would mix into the reading. The EnergyRunner rig isolates the device's supply, measures only its energy, and times inferences via a separate interface. Home-made energy numbers that skip this often include large board and USB overheads.",
       topic="bench-tools", level=4),
    mcq("After an update, the report says 'average latency improved 20% (25 -> 20 ms)', but p99 went from 40 to 85 ms. The model drives a conveyor reject gate with a 50 ms deadline. Ship?",
        ["No: the deadline is a tail requirement and the new p99 (85 ms) misses it; investigate what causes the new slow runs before release",
         "Yes: the average improved by 20%",
         "Yes: p99 is only 1% of runs, which never matters",
         "No: averages above 15 ms are never acceptable"], 0,
        "1% of a conveyor's items is a lot of items.",
        "At 20 items per second, 1% slow means a missed reject every 5 seconds. Reports that headline averages can hide tail regressions (new CPU fallback, garbage collection, a larger buffer). Release gates on edge should check p95/p99 against the deadline.",
        analogy="Like a deploy that improves average API latency but doubles p99: the dashboard looks green while the slowest users time out.",
        topic="reports", level=4),
    mcq("A candidate's p95 over 100 runs is 9.6 ms; the SLA is p95 < 10 ms. A bootstrap of the runs gives a 95% interval of [9.3, 10.4] ms for p95. What is the sound engineering call?",
        ["Not yet proven: the interval crosses 10 ms; collect more runs (and under field conditions) or optimise for headroom before declaring the SLA met",
         "Pass: the point estimate 9.6 is below 10",
         "Fail: any interval above 10 means it always fails",
         "Bootstraps cannot be used for latency"], 0,
        "How sure are you that the true p95 is below 10?",
        "A p95 from 100 runs is set by the 5-6 slowest values, so it is noisy. When the uncertainty band straddles the limit, gather thousands of runs and test in the real thermal/power state, or make the model faster so the margin is comfortable.",
        topic="sla-selection", level=4),
    out("p_kws_mw, p_big_mw, t_big_s = 1.0, 900.0, 2   # stage 1 always on; stage 2 per wake\n"
        "for wakes_per_hour in (30, 300):              # true wakes + false wakes\n"
        "    avg = p_kws_mw + p_big_mw * t_big_s * wakes_per_hour / 3600\n"
        "    print(wakes_per_hour, round(avg, 1))",
        ["30 16.0\n300 151.0", "30 901.0\n300 901.0", "30 1.0\n300 1.0", "30 16.0\n300 16.0"], 0,
        "Average power = always-on stage + big stage × its share of time.",
        "At 30 wakes/hour the cascade averages 16 mW instead of 900 mW for an always-on big model (~56x less). If the wake-word model's false-accept rate pushes wakes to 300/hour, average power jumps to 151 mW. In a cascade, the first stage's false-positive rate is an energy metric, not just an accuracy one.",
        question="Average power of a TinyML wake-word cascade in a smart speaker. What does this print?",
        analogy="Like a cheap health-check endpoint that runs every second and only triggers the expensive full diagnostic when something looks wrong.",
        topic="tinyml", level=4),
    mcq("A Jetson's NPU/GPU has 4x the TOPS of the CPU. Moving an 8B 4-bit LLM to it speeds up prompt processing a lot but token generation only a little. Why?",
        ["Prefill processes many tokens per weight read (compute-bound), so more TOPS help; decode reads all weights for every single token (bandwidth-bound), and the memory bandwidth is shared and unchanged",
         "The NPU cannot run 4-bit models at all",
         "Decode runs on the CPU no matter what",
         "Token generation is limited by the screen refresh rate"], 0,
        "Arithmetic per byte: many tokens vs one token.",
        "Benchmarks of edge LLMs must report prefill (tokens/s or TTFT) and decode separately. On unified-memory SoCs CPU, GPU and NPU share one memory bus, so decode speed tracks bandwidth ÷ model bytes whichever unit runs it.",
        analogy="Like upgrading a server's CPU when the query is waiting on disk: the faster CPU just waits faster.",
        topic="edge-genai", level=4),
    mcq("For an offline Hindi voice assistant with a fixed 2 GB memory budget, the team compares a 3B model at 4-bit (~1.5 GB) with a 1.5B model at 8-bit (~1.5 GB). How should they decide?",
        ["Benchmark task quality (e.g. intent accuracy, answer quality on Hindi prompts), TTFT and tokens/s for both on the target phone: more parameters at lower precision often wins, but it must be measured",
         "Always the 8-bit model, because higher precision is always better",
         "Always the 3B model, because bigger is always better",
         "Pick the one with the smaller file, they are identical otherwise"], 0,
        "Same memory, different trade-off.",
        "At equal bytes, a larger 4-bit model usually beats a smaller 8-bit one on quality, but low-resource languages and aggressive quantization can break that rule. The two have similar decode speed (same bytes), so quality on the real task decides.",
        topic="edge-genai", level=4),
    tf("Split learning keeps raw data on the device, but the activations sent from the cut layer can still leak information about the inputs, so defences such as moving the cut deeper, adding noise or combining with differential privacy may be needed.", True,
       "The first layers of a CNN look a lot like the image.",
       "Activations from early layers can be inverted to reconstruct inputs (model-inversion attacks). More device-side layers, noise/DP on the smashed data, or decorrelation losses reduce leakage, each costing device compute or accuracy. 'No raw data leaves the device' is not the same as 'private'.",
       topic="collab-trends", level=4),
    mcq("An early-fusion model combines a 30 FPS camera with a 100 Hz IMU on a delivery robot. In the field, accuracy drops sharply whenever the camera stutters. What design change addresses this?",
        ["Timestamp-align the streams and train with modality dropout, or move to intermediate/late fusion so the model can still decide when one modality is late or missing",
         "Increase the IMU rate to 1 kHz",
         "Remove the IMU so only one sensor is used",
         "Lower the camera to 1 FPS so it never stutters"], 0,
        "Early fusion assumes both inputs are always there and in sync.",
        "Early fusion learns joint patterns but breaks when one stream is missing or misaligned. Explicit synchronisation, modality dropout during training and later fusion make the system degrade gracefully. Benchmarks of multimodal edge systems should include missing-modality cases.",
        topic="collab-trends", level=4),
    mcq("A solar-powered crop-monitoring station runs real-time pest detection plus a nightly 3 kWh model-refresh and analytics job. What is the most effective energy-aware scheduling change?",
        ["Move the deferrable 3 kWh job into the midday solar window (or when the battery is full) and keep real-time detection as is; only deferrable work should be shifted",
         "Shift real-time pest detection to midday only",
         "Run everything at night when the grid is less busy",
         "Run the 3 kWh job twice to finish faster"], 0,
        "Which workloads can wait?",
        "Energy-aware scheduling moves flexible work to when energy is cheap or clean and leaves latency-critical inference alone. Here the 3 kWh job at night would come from the battery or grid (~2.1 kg CO2 at 0.7 kg/kWh); at midday it can come from surplus solar.",
        topic="green-ai", level=4),
    mcq("Green AI advocates reporting efficiency (energy, FLOPs, carbon) alongside accuracy. For an edge fleet, which reporting practice best follows that idea?",
        ["Report energy per inference and per-day fleet energy (with the grid intensity used) next to accuracy for every model version, so efficiency regressions are as visible as accuracy gains",
         "Report only accuracy, because energy is the hardware team's problem",
         "Report only the training energy, because inference is free",
         "Report the chip's TOPS/W instead of measuring"], 0,
        "Make the cost visible per version.",
        "Schwartz et al. (2020) argue efficiency should be a first-class evaluation criterion. At fleet scale, inference energy usually exceeds one-time training energy, so a version that adds 1% accuracy for 2x the energy should be a visible trade-off, not a silent one.",
        topic="green-ai", level=4),
    mcq("Which pairing of product and primary benchmark metric is right?",
        ["Emergency-braking camera: p99 latency on the device; photo-library tagging at night: throughput and total energy; coin-cell leak sensor: average power / battery life",
         "Emergency-braking camera: throughput; photo tagging: p99 latency; leak sensor: TOPS",
         "All three: average latency",
         "All three: model file size"], 0,
        "Ask what failure looks like for each product.",
        "A braking system fails on one late frame (tail latency). An overnight batch job fails if it does not finish or drains the battery (throughput, energy). A coin-cell sensor fails when the battery dies (average power). Benchmarks should measure the metric that maps to the product's failure.",
        topic="bench-metrics", level=4),
    # ------------------------------------------------------------------ extra fills
    fill("The usual runtime for TinyML on microcontrollers is TensorFlow Lite for ____. (one word)", "Microcontrollers",
         "Often shortened to TFLite Micro or TFLM.",
         "TFLite for Microcontrollers is a small C++ interpreter with no dynamic allocation and no OS dependency. It runs the same .tflite flatbuffer, compiled into the firmware as a C array, inside a fixed tensor arena.",
         topic="tinyml", level=2),
    fill("MLPerf Tiny measures energy per inference with EEMBC's ____ framework. (one word)", "EnergyRunner",
         "EEMBC's tool that runs the energy measurements.",
         "EnergyRunner drives the device under test, an energy monitor and an IO manager, so energy can be measured without the host's USB supply polluting the reading. Latency-only runs use a simpler set-up.",
         topic="bench-tools", level=2),
    fill("A board draws 2.5 W during a 12 ms inference. Its energy per inference is ____ mJ (a number).", "30",
         "W × ms = mJ.",
         "2.5 W × 12 ms = 30 mJ, i.e. ~33 inferences per joule. The common slips are mixing units (0.03 is in joules) or using idle power instead of the power drawn during the inference.",
         topic="energy-kpis", level=3),
    fill("In split learning, the cut-layer activations a device sends to the server are often called ____ data. (one word)", "smashed",
         "The input after it has been 'smashed' through the first layers.",
         "Smashed data is what crosses the network in split learning, every step, together with the gradients coming back. It is not raw data, but it is not automatically private either.",
         topic="collab-trends", level=3),
    fill("Carbon emitted (kg CO2) = energy used (kWh) × the grid's carbon ____. (one word)", "intensity",
         "kg CO2 per kWh.",
         "Grid carbon intensity varies by country and hour (India ~0.7 kg CO2/kWh, the convention used here; much lower when solar or hydro dominate). The same kWh can therefore cost very different carbon, which is why carbon-aware schedulers move flexible work in time.",
         topic="green-ai", level=2),
    fill("Models E (85%, 9 ms) and F (85%, 9 ms) are identical on accuracy and latency. How many of these two models are Pareto-dominated? ____ (a number)", "0",
         "Dominance needs a strict improvement somewhere.",
         "Neither is strictly better on any metric, so neither dominates the other: both stay on the frontier (as ties). Answering 1 assumes 'at least as good' is enough; the strict part of the definition matters in exam answers.",
         topic="pareto", level=3),
    fill("A chart that draws the middle 50% of runs as a box, the median as a line and outliers as dots is a ____ plot. (one word)", "box",
         "Also called a box-and-whisker plot.",
         "Box plots compare latency distributions across devices or runtimes in one picture: the median, the interquartile range (the box), whiskers and outliers show both the typical case and the tail.",
         topic="reports", level=2),
]
