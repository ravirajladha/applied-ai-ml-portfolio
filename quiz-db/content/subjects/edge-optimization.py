from helpers import mcq, tf, out, fill

# Machine Learning on the Edge (AIMLCZG535), Module 6, Sessions 11-12:
# Model Optimization Techniques. Built from the handout sub-topics, lab Exp 6 and the
# past papers (Jun 2026 midsem Set 2 Q1(d) pruning trap); the rest is standard practice
# (T1 and primary sources) because the sessions are "Instructor Supplied Material".

SUBJECT = "edge-optimization"

TOPICS = [
    ("compression-why", "Why optimize for the edge: the compression toolbox"),
    ("quant-ptq-qat", "Quantization: PTQ vs QAT and the TFLite modes"),
    ("quant-math", "INT8 scale and zero-point arithmetic"),
    ("pruning", "Pruning and sparsity"),
    ("distillation", "Knowledge distillation for compact models"),
    ("nas", "Neural Architecture Search for edge networks"),
    ("mobilenet", "MobileNet: depthwise-separable convolutions"),
    ("efficientnet-shufflenet", "EfficientNet compound scaling and ShuffleNet"),
    ("slm", "Small language models on the edge (DistilBERT, TinyBERT)"),
    ("compilers", "Compiler-level optimization: TVM, TensorRT INT8, XLA"),
    ("opt-metrics", "Evaluation metrics for optimized models"),
]

QUESTIONS = [
    # ------------------------------------------------------------------ L1
    mcq("A model trained in the cloud is 90 MB in FP32 and must run on a ₹900 microcontroller board with 1 MB of Flash. Which of these is NOT one of the Module 6 levers for making it fit?",
        ["Adding more training data to the same architecture",
         "Quantization: storing each number in fewer bits",
         "Pruning: removing weights that contribute little",
         "Distillation or a lighter architecture: training a smaller model"], 0,
        "Three levers change the model's size; one only changes what it learned.",
        "Module 6's toolbox is quantization, pruning, distillation and efficient architectures / NAS, followed by a compiler for the target. More data can improve accuracy, but the model is exactly as big as before.",
        topic="compression-why", level=1,
        analogy="Like shrinking a web bundle: minify (quantize), tree-shake dead code (prune), or rewrite with a lighter library (distil / new architecture). Adding more tests does not make the bundle smaller."),
    tf("Converting a model's weights from FP32 to INT8 makes the stored weights about 4 times smaller.", True,
       "Count the bytes per number.",
       "FP32 uses 4 bytes per weight and INT8 uses 1, so the weights shrink ~4x. The file shrinks slightly less because of metadata and the scales and zero points.",
       topic="quant-ptq-qat", level=1),
    mcq("What does Post-Training Quantization (PTQ) mean?",
        ["Quantizing a model that has already been trained, without retraining it",
         "Training the model from scratch in 8-bit integers",
         "Quantizing the training data before training",
         "Pruning a model after training"], 0,
        "The name says when it happens.",
        "PTQ converts a finished float model to lower precision (often with a small calibration set). Quantization-Aware Training (QAT) instead simulates quantization during training or fine-tuning so the weights adapt to it.",
        analogy="Like minifying a finished JS bundle after the build (PTQ), versus writing the code with the minifier's limits in mind from the start (QAT).",
        diagram="""
PTQ: train FP32 --> convert (+ calib data) --> INT8
QAT: train FP32 --> fine-tune with fake-quant --> INT8
""",
        topic="quant-ptq-qat", level=1),
    fill("In affine quantization, real_value = scale × (q − ____). (two words, with an underscore)", "zero_point",
         "The integer that stands for 0.0.",
         "real = scale × (q − zero_point). The scale is the size of one integer step; the zero point is the integer that maps exactly to 0.0.",
         diagram="""
real: -1.0        0.0                  3.0
       |-----------|--------------------|
int8: -128        -64                  127
       (scale = 4.0 / 255, zero_point = -64)
""",
         topic="quant-math", level=1),
    mcq("What is magnitude-based pruning?",
        ["Setting the weights with the smallest absolute values to zero",
         "Removing the largest weights because they dominate",
         "Lowering every weight to 8 bits",
         "Deleting the last layer of the network"], 0,
        "Small in size, small in effect.",
        "Weights near zero contribute little to the output, so magnitude pruning zeroes the smallest |w|. The model is usually fine-tuned afterwards to recover accuracy.",
        analogy="Like deleting unused CSS rules: the rules that never change the page go first, and the site looks the same.",
        topic="pruning", level=1,
        diagram="""
weights:  0.82  -0.03   0.41   0.01  -0.67   0.02
prune 50% smallest |w|:
          0.82   0       0.41   0     -0.67   0
"""),
    mcq("In knowledge distillation, what does the student model learn from?",
        ["The outputs (soft probabilities) of a larger, already-trained teacher model",
         "Only the raw sensor data, with no other model involved",
         "The teacher's weights, copied into a smaller file",
         "The test set labels"], 0,
        "One model teaches the other.",
        "The large teacher is trained first and frozen. The small student is trained to match the teacher's output distribution (plus the true labels), so it inherits much of the teacher's skill at a fraction of the size.",
        analogy="Like a junior developer learning from a senior's code reviews, which explain why an answer is nearly right, instead of only from pass/fail CI results.",
        topic="distillation", level=1),
    mcq("What does Neural Architecture Search (NAS) automate?",
        ["Choosing the network's layers and their sizes, by searching over many candidate designs",
         "Searching the internet for a pre-trained model",
         "Tuning only the learning rate",
         "Finding the fastest edge device to buy"], 0,
        "Architecture = the design of the network.",
        "NAS searches a space of possible architectures (layer types, kernel sizes, widths, depths) with a search strategy and scores each candidate. MobileNetV3 and EfficientNet-B0 were found this way.",
        analogy="Like a load-test-driven autotuner, but it tunes the shape of the network instead of config values.",
        topic="nas", level=1),
    mcq("A MobileNet depthwise-separable convolution splits one standard convolution into which two steps?",
        ["A depthwise convolution (one filter per input channel) followed by a 1×1 pointwise convolution",
         "Two standard 3×3 convolutions in a row",
         "A pooling layer followed by a dense layer",
         "A 1×1 convolution followed by dropout"], 0,
        "Filter space and mix channels separately.",
        "Depthwise: each input channel gets its own K×K filter (spatial filtering only). Pointwise: a 1×1 convolution mixes channels. Together they replace one K×K×M×N convolution at a fraction of the cost.",
        topic="mobilenet", level=1,
        diagram="""
standard:  [H×W×M] --K×K×M×N conv--> [H×W×N]
separable: [H×W×M] --K×K depthwise--> [H×W×M]
                   --1×1×M×N pointwise--> [H×W×N]
"""),
    mcq("EfficientNet's main idea, compound scaling, means:",
        ["Scaling the network's depth, width and input resolution together with fixed ratios",
         "Making the network deeper only",
         "Doubling the input image size only",
         "Compressing the network with zip"], 0,
        "Three dimensions, one knob.",
        "Earlier models were scaled one way (ResNet-50 -> 152 by depth). EfficientNet uses one coefficient φ to grow depth, width and resolution together, which gives better accuracy per FLOP.",
        diagram="""
depth       d = 1.2^phi    (more layers)
width       w = 1.1^phi    (more channels)
resolution  r = 1.15^phi   (bigger input)
FLOPs ~ d x w^2 x r^2 ~ 2^phi
""",
        topic="efficientnet-shufflenet", level=1),
    mcq("Why are DistilBERT and TinyBERT called small language models in Session 12?",
        ["They are compressed versions of BERT with far fewer layers and parameters, small enough to run on phones and edge devices",
         "They only understand short words",
         "They are trained on less than 1 MB of text",
         "They run only in the cloud"], 0,
        "Think about BERT-base's 110M parameters.",
        "DistilBERT (6 layers, ~66M parameters) and TinyBERT-4 (4 layers, ~14.5M) are distilled from BERT-base (12 layers, ~110M). They keep most of its accuracy while fitting the memory and latency of a phone or gateway.",
        topic="slm", level=1),
    mcq("What does a model compiler such as TVM, TensorRT or XLA do?",
        ["Turns a model graph into optimized code for one specific target (fusing operations and tuning kernels)",
         "Trains the model faster in the cloud",
         "Translates Python into Java",
         "Labels the training data automatically"], 0,
        "Like gcc, but for neural network graphs.",
        "A model compiler takes the network graph, rewrites it (fusing layers, folding constants, choosing precisions) and generates fast kernels for a particular CPU, GPU or accelerator. The weights and accuracy stay (almost) the same; the runtime gets faster.",
        diagram="""
TFLite / ONNX / PyTorch graph
   --> IR: fuse ops, fold constants, pick precision
   --> tune kernels for ONE target
   --> ARM CPU | Jetson GPU | MCU binary
""",
        topic="compilers", level=1,
        analogy="Like a production build: the same React app, but bundled, minified and tuned for the browser it ships to."),
    mcq("Session 12 lists the evaluation metrics for an optimized model. Which list matches?",
        ["Accuracy, latency, throughput, energy, memory footprint",
         "Accuracy only",
         "Training loss, learning rate, epochs",
         "Lines of code, number of files, commit count"], 0,
        "One quality metric and four cost metrics.",
        "An edge model has to stay accurate AND fit the device's time, power and memory budgets. Reporting only accuracy, or only file size, hides whether the optimization actually helped.",
        topic="opt-metrics", level=1),
    tf("Latency is the time one inference takes, while throughput is how many inferences the device completes per second.", True,
       "One is per request, one is per second.",
       "Latency (ms per inference) is what a single user or control loop feels. Throughput (inferences/s) is the capacity. Batching can raise throughput while making each request wait longer.",
       topic="opt-metrics", level=1),
    tf("Edge devices often need optimized models because they have far less memory, compute and power than a cloud GPU server.", True,
       "Compare a 1 MB-RAM microcontroller with an 80 GB GPU.",
       "An MCU may have 256 KB-1 MB of SRAM and run on a coin cell; a phone has a few GB of RAM and a battery. A cloud GPU has tens of GB and a wall socket. The same model rarely fits both without optimization.",
       topic="compression-why", level=1),
    fill("The fraction of weights that are exactly zero after pruning is called the model's ____.", "sparsity",
         "80% pruned = 80% ____.",
         "Sparsity = zero weights / total weights. A model pruned to 80% sparsity keeps only 20% of its weights non-zero.",
         topic="pruning", level=1),
    fill("In distillation the teacher's logits are divided by a ____ T > 1 before the softmax, to soften the probabilities. (one word)", "temperature",
         "Borrowed from physics: higher means more spread out.",
         "softmax(z / T): with T = 1 you get the usual sharp probabilities; with T = 4 the wrong classes get visibly non-zero probabilities, which is the extra information the student learns from.",
         topic="distillation", level=1),
    tf("Hardware-aware NAS can use the latency measured on the actual target device, not just the FLOP count, when scoring candidate networks.", True,
       "MnasNet ran candidates on real phones.",
       "MnasNet measured latency on a Pixel phone and put it in the reward; others use per-layer latency lookup tables built on the device. FLOPs are a poor proxy for real speed on edge hardware.",
       topic="nas", level=1),
    out("std = 3 * 3 * 16 * 32          # K*K*M*N weights, standard conv\n"
        "dw = 3 * 3 * 16 + 16 * 32      # depthwise + pointwise weights\n"
        "print(std, dw)",
        ["4608 656", "4608 144", "656 4608", "4608 512"], 0,
        "Depthwise: one 3×3 filter per input channel. Pointwise: M × N 1×1 weights.",
        "Standard: 3·3·16·32 = 4,608 weights. Separable: 3·3·16 = 144 depthwise + 16·32 = 512 pointwise = 656, about 7x fewer. '4608 512' forgets the depthwise part; '4608 144' forgets the pointwise part.",
        question="Weights in a standard 3×3 conv (16 -> 32 channels) vs a depthwise-separable one. What does this print?",
        topic="mobilenet", level=1),
    fill("ShuffleNet adds a channel ____ operation after group convolutions so information can flow between groups. (one word)", "shuffle",
         "It is in the name.",
         "Group convolutions only connect channels inside each group. Reordering (shuffling) channels between layers lets the next group see outputs from every group, at almost no compute cost.",
         topic="efficientnet-shufflenet", level=1),
    tf("TensorRT INT8 mode needs a calibration step, in which representative input data is run through the network to choose activation ranges.", True,
       "INT8 needs to know the range of every activation.",
       "TensorRT runs a calibration dataset (typically a few hundred representative images) through the FP32 network, records activation histograms and picks a range per tensor. The result can be saved as a calibration cache for later builds.",
       diagram="""
FP32 network + ~500 images
   --> activation histograms per tensor
   --> range per tensor (entropy / min-max / pct)
   --> INT8 engine  (+ calibration cache)
""",
       topic="compilers", level=1),
    # ------------------------------------------------------------------ L2
    mcq("The TFLite converter offers three post-training quantization modes. Which description is right?",
        ["Dynamic-range: weights INT8, activations float (quantized on the fly). Full-integer: weights and activations INT8, needs a representative dataset. Float16: weights FP16, ~2x smaller, suits GPUs",
         "Dynamic-range: weights and activations INT8. Full-integer: weights INT8 only. Float16: INT16 integers",
         "All three modes need a representative dataset and give the same 4x size reduction",
         "Full-integer quantizes only the input and output tensors; everything inside stays float"], 0,
        "Ask of each mode: what is INT8, and does it need data?",
        "Dynamic-range is the no-data default (~4x smaller, CPU speed-up). Full-integer also quantizes activations, so it needs sample inputs to measure their ranges; it is what integer-only hardware needs. Float16 halves size and keeps GPU delegates happy.",
        topic="quant-ptq-qat", level=2,
        code="converter = tf.lite.TFLiteConverter.from_saved_model(path)\n"
             "converter.optimizations = [tf.lite.Optimize.DEFAULT]\n"
             "converter.representative_dataset = rep_data   # full-integer only\n"
             "converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]",
        lang="text"),
    tf("Post-training quantization never needs any data: you only need the trained model.", False,
       "Weights are known; activations depend on inputs.",
       "Dynamic-range PTQ needs no data. Full-integer PTQ must know each activation's range, which depends on real inputs, so it needs a representative dataset (typically 100-500 samples). Common exam slip: saying 'PTQ is data-free' without the mode.",
       topic="quant-ptq-qat", level=2),
    mcq("A dairy cooperative in Anand wants its milk-adulteration image model on a Google Coral Edge TPU. Which quantization is required?",
        ["Full-integer INT8 (weights and activations), then compiled with the Edge TPU compiler",
         "Dynamic-range quantization only",
         "Float16 quantization",
         "No quantization; the Edge TPU runs FP32 natively"], 0,
        "The Edge TPU has integer hardware only.",
        "The Edge TPU executes only 8-bit integer ops, so the model must be fully integer-quantized (PTQ with a representative dataset, or QAT) and then compiled. Any op it cannot map falls back to the slower host CPU.",
        topic="quant-ptq-qat", level=2),
    out("lo, hi = -1.0, 3.0               # observed activation range\n"
        "qmin, qmax = -128, 127            # int8\n"
        "scale = (hi - lo) / (qmax - qmin)\n"
        "zero_point = qmin - round(lo / scale)\n"
        "print(round(scale, 5), zero_point)",
        ["0.01569 -64", "0.01569 64", "0.01176 -128", "0.01569 0"], 0,
        "scale = range / 255; then find the integer that sits on 0.0.",
        "scale = 4.0 / 255 = 0.01569. lo / scale = -63.75 -> round -64; zero_point = -128 - (-64) = -64. Check: q = -64 dequantizes to 0.0 exactly. '0' is the symmetric-quantization answer, which this skewed range does not use.",
        question="Asymmetric INT8 parameters for an activation in [-1.0, 3.0]. What does this print?",
        topic="quant-math", level=2),
    out("import numpy as np\n"
        "x = np.array([-1.0, 0.0, 0.5, 3.0])\n"
        "scale, zp = 4 / 255, -64\n"
        "q = np.clip(np.round(x / scale) + zp, -128, 127).astype(np.int8)\n"
        "print(q.tolist())\n"
        "print((scale * (q.astype(int) - zp)).round(3).tolist())",
        ["[-128, -64, -32, 127]\n[-1.004, 0.0, 0.502, 2.996]",
         "[-128, -64, -32, 127]\n[-1.0, 0.0, 0.5, 3.0]",
         "[-64, 0, 32, 191]\n[-1.004, 0.0, 0.502, 2.996]",
         "[0, 64, 96, 255]\n[-1.0, 0.0, 0.5, 3.0]"], 0,
        "Quantize, clip to int8, then dequantize: the round trip is not exact.",
        "x / scale + zp gives -127.75 -> -128, -64, -32.1 -> -32, 127. 191 would overflow int8; that is why the clip is there. Dequantizing returns values close to, but not equal to, the originals: that gap is the quantization error, except 0.0, which is exact by construction.",
        topic="quant-math", level=2),
    out("import numpy as np\n"
        "rng = np.random.default_rng(0)\n"
        "w = rng.normal(size=(64, 64))\n"
        "t = np.quantile(np.abs(w), 0.8)     # magnitude threshold\n"
        "mask = np.abs(w) >= t\n"
        "print(round(1 - mask.mean(), 2), int(mask.sum()))",
        ["0.8 820", "0.2 3276", "0.8 3276", "0.2 820"], 0,
        "The threshold is the 80th percentile of |w|; keep only weights above it.",
        "Weights below the 80th-percentile magnitude are zeroed, so sparsity = 0.8 and 4,096 × 0.2 ≈ 820 weights survive. Mixing up 'pruned fraction' and 'kept fraction' gives the 0.2 / 3276 answers.",
        question="80% magnitude pruning of a 64×64 layer. What does this print?",
        topic="pruning", level=2),
    mcq("Why does the standard pruning recipe prune gradually (a little at a time, with fine-tuning in between) instead of zeroing 80% of the weights in one shot?",
        ["The remaining weights get to adapt after each step, so accuracy recovers; one big cut can drop accuracy too far to recover",
         "Gradual pruning makes the final file smaller than one-shot pruning to the same sparsity",
         "One-shot pruning is not supported by any framework",
         "Fine-tuning is only needed for quantization, not pruning"], 0,
        "Think of healing between cuts.",
        "Iterative prune -> fine-tune -> prune (TF-MOT's PolynomialDecay schedule ramps sparsity up during training) lets the network redistribute what the removed weights did. At the same final sparsity the file size is the same; the accuracy is better.",
        topic="pruning", level=2),
    tf("Structured pruning removes whole filters or channels, so the remaining weight tensors are smaller dense tensors that ordinary CPU kernels run faster.", True,
       "Compare a matrix with zeros in it to a matrix with fewer rows.",
       "Dropping 50% of a conv layer's filters turns a 64-filter layer into a 32-filter one: fewer multiply-adds for any dense kernel. Unstructured pruning keeps the shape and just fills it with zeros, which dense kernels still multiply.",
       topic="pruning", level=2),
    out("import numpy as np\n"
        "teacher = np.array([0.6, 0.3, 0.1])      # soft target: cow, buffalo, goat\n"
        "for s in ([0.7, 0.25, 0.05], [0.7, 0.05, 0.25]):   # two students\n"
        "    s = np.array(s)\n"
        "    hard = -np.log(s[0])                 # CE with the one-hot label 'cow'\n"
        "    soft = -np.sum(teacher * np.log(s))  # CE with the teacher\n"
        "    print(round(float(hard), 3), round(float(soft), 3))",
        ["0.357 0.929\n0.357 1.251", "0.357 0.929\n0.357 0.929",
         "0.357 1.251\n0.357 0.929", "0.929 0.357\n1.251 0.357"], 0,
        "Both students give 'cow' 0.7. Which one also gets the wrong classes right?",
        "The hard label cannot tell the two students apart (0.357 each). The teacher's soft target can: the student who thinks a buffalo is likelier than a goat scores 0.929, the other 1.251. That extra signal about the wrong classes is the dark knowledge distillation transfers to a small edge model.",
        question="Hard-label vs soft-target loss for two livestock-classifier students. What does this print?",
        topic="distillation", level=2),
    mcq("What is the 'dark knowledge' that distillation transfers?",
        ["The relative probabilities the teacher gives to the wrong classes, which show how similar the classes are",
         "Hidden backdoors in the teacher's weights",
         "The teacher's training data, recovered from its outputs",
         "The labels of the test set"], 0,
        "A hard label says 'cow'; a soft label says more.",
        "A one-hot label says only 'this is a cow'. The teacher's soft output says 'cow, a bit like a buffalo, nothing like a tractor'. That similarity structure is a richer training signal, which is why small students learn faster and generalize better from a teacher.",
        topic="distillation", level=2),
    mcq("A NAS method is described by three components. Which set is it?",
        ["Search space, search strategy, performance estimation strategy",
         "Training set, validation set, test set",
         "Encoder, decoder, attention",
         "Quantization, pruning, distillation"], 0,
        "What can be built, how to explore it, how to score a candidate.",
        "The search space defines the allowed layers and connections; the strategy (reinforcement learning, evolution, gradient-based DARTS) picks candidates; performance estimation scores them (full training, early stopping, or shared supernet weights). Most cost lives in the third part.",
        topic="nas", level=2,
        diagram="""
+-------------+  candidate  +-------------+
| search      |------------>| performance |
| strategy    |<------------| estimation  |
+-------------+   score     +-------------+
      ^ picks from
+-------------+
| search space|
+-------------+
"""),
    tf("The first reinforcement-learning NAS (Zoph & Le, 2017) trained every candidate from scratch and needed hundreds of GPUs for weeks; weight-sharing methods later cut the cost to a few GPU-days.", True,
       "Training thousands of networks fully is expensive.",
       "The 2017 search used ~800 GPUs for about four weeks. ENAS, DARTS and one-shot supernets share weights between candidates, so each candidate is scored without full training. That is what made NAS practical for edge models.",
       topic="nas", level=2),
    mcq("For a K×K depthwise-separable convolution with N output channels, compute relative to a standard convolution is:",
        ["1/N + 1/K²",
         "1/K²",
         "1/N",
         "K² / N"], 0,
        "Divide (depthwise + pointwise) by the standard cost.",
        "Standard = K²·M·N·H·W. Separable = K²·M·H·W + M·N·H·W. Dividing gives 1/N + 1/K². With K = 3 and N = 64 that is 1/64 + 1/9 ≈ 0.127, about 8x cheaper. Writing only 1/K² overstates the saving.",
        topic="mobilenet", level=2),
    out("def sep(K, M, N, H, W):            # depthwise-separable multiply-adds\n"
        "    return K * K * M * H * W + M * N * H * W\n"
        "full = sep(3, 128, 128, 28, 28)\n"
        "half = sep(3, 64, 64, 28, 28)       # width multiplier alpha = 0.5\n"
        "print(round(half / full, 3))",
        ["0.266", "0.5", "0.25", "0.133"], 0,
        "α thins both input and output channels.",
        "The pointwise term scales with αM·αN = α², the depthwise term with α. Pointwise dominates, so the cost is ~α² = 0.25, plus a little from the depthwise term: 0.266. The common wrong answer is 0.5: halving width does not halve compute.",
        question="MobileNet width multiplier α = 0.5 on one layer. What does this print?",
        topic="mobilenet", level=2),
    mcq("What is an inverted residual block in MobileNetV2?",
        ["Expand channels with a 1×1 conv (×6), filter with a 3×3 depthwise conv, project back down with a linear 1×1 conv, with a skip connection between the thin ends",
         "A ResNet block with the skip connection removed",
         "A block that halves the channels and then halves them again",
         "A block that runs the layers in reverse order at inference"], 0,
        "Thin -> wide -> thin, the opposite of a ResNet bottleneck.",
        "ResNet bottlenecks go wide -> thin -> wide. MobileNetV2 inverts that: the skip connects the thin bottleneck tensors (cheap to store), the depthwise conv works in the wide space, and the projection has no ReLU (a 'linear bottleneck') because ReLU in low dimensions destroys information.",
        topic="mobilenet", level=2,
        diagram="""
x (24 ch) --1x1 expand--> 144 ch --3x3 dw--> 144 ch
                                              |
          <---1x1 project (no ReLU)-----------+
   y = x + projected (24 ch)
"""),
    fill("EfficientNet compound scaling picks α, β, γ so that α · β² · γ² ≈ ____ (a number), meaning each step of φ roughly doubles FLOPs.", "2",
         "FLOPs grow with depth, width² and resolution².",
         "FLOPs scale with d · w² · r². With α = 1.2, β = 1.1, γ = 1.15: 1.2 × 1.21 × 1.3225 ≈ 1.92 ≈ 2, so EfficientNet-B(φ) costs ~2^φ times B0.",
         topic="efficientnet-shufflenet", level=2),
    out("M, N, H, W = 240, 240, 28, 28\n"
        "for g in (1, 3):                    # g = number of groups\n"
        "    print(g, (M // g) * N * H * W)  # 1x1 conv multiply-adds",
        ["1 45158400\n3 15052800", "1 45158400\n3 5017600", "1 45158400\n3 45158400", "1 15052800\n3 45158400"], 0,
        "Each output channel only sees M/g input channels.",
        "A group convolution with g groups divides a 1×1 conv's cost by g: 45.2M -> 15.1M multiply-adds for g = 3. Dividing by g² (5.0M) is the common slip. The catch: channels never mix across groups, which is why ShuffleNet shuffles.",
        question="ShuffleNet-style pointwise group convolution. What does this print?",
        analogy="Like teams that only talk inside their own channel: cheap, but nothing crosses teams until someone routes messages between them (the shuffle).",
        topic="efficientnet-shufflenet", level=2),
    mcq("Which comparison of the two Session 12 small language models is right (relative to BERT-base, ~110M parameters)?",
        ["DistilBERT: 6 layers, ~66M params, ~60% faster, ~97% of the score. TinyBERT-4: 4 layers, ~14.5M params, ~9x faster, ~96% of the score",
         "DistilBERT: 2 layers, ~5M params. TinyBERT: 12 layers, ~110M params",
         "Both are larger than BERT-base but faster because of better hardware",
         "DistilBERT is quantized BERT; TinyBERT is pruned BERT"], 0,
        "Tiny is the smaller one.",
        "Both are distilled students of BERT-base. DistilBERT halves the depth; TinyBERT-4 also narrows the hidden size (312) and is distilled layer by layer (embeddings, hidden states, attention). TinyBERT is the better fit for a tight phone budget; neither is merely quantized or pruned.",
        topic="slm", level=2),
    out("params = 66e6                    # DistilBERT total\n"
        "emb = 30522 * 768                # word-embedding table\n"
        "rest = params - emb              # Linear layers etc.\n"
        "# dynamic INT8 quantizes Linear layers only; embeddings stay FP32\n"
        "print(round(emb / 1e6, 1), round((emb * 4 + rest * 1) / 1e6, 1))",
        ["23.4 136.3", "23.4 66.0", "23.4 264.0", "42.6 136.3"], 0,
        "Price each part at its own bytes per parameter.",
        "The embedding table is 23.4M parameters and stays at 4 bytes (93.8 MB); the other 42.6M become 1 byte (42.6 MB): ~136 MB, not the 66 MB that 'INT8 = 1 byte per parameter' predicts. On a phone app the fix is to quantize the embedding too or shrink the vocabulary.",
        question="Size of DistilBERT after dynamic INT8 quantization of its Linear layers, in M params and MB. What does this print?",
        topic="slm", level=3),
    mcq("What is operator (layer) fusion, the optimization TensorRT, TVM and XLA all perform?",
        ["Merging consecutive ops (e.g. Conv + BatchNorm + ReLU) into one kernel so intermediate results are not written to and read back from memory",
         "Averaging the weights of two models",
         "Running two different models on the same input",
         "Splitting one layer across two devices"], 0,
        "Fewer kernel launches, fewer memory round-trips.",
        "Unfused, Conv writes its output to memory, BatchNorm reads and writes it, ReLU reads and writes again. Fused, the data stays in registers or cache. On edge devices memory traffic often costs more time and energy than the arithmetic, so fusion gives real speed-ups.",
        analogy="Like replacing three API calls that each write to the database with one call that keeps the data in memory and writes once.",
        topic="compilers", level=2,
        diagram="""
before: Conv -> [mem] -> BN -> [mem] -> ReLU -> [mem]
after:  [Conv+BN+ReLU] -------------------------> [mem]
"""),
    mcq("Match the compilers to their home ground.",
        ["TVM: open-source, many frameworks in, many targets out (incl. microTVM for MCUs). TensorRT: NVIDIA GPUs and Jetson. XLA: TensorFlow and JAX graphs",
         "TVM: NVIDIA only. TensorRT: any CPU. XLA: PyTorch only",
         "All three are the same tool under different brand names",
         "TVM and XLA only run in the cloud; only TensorRT targets edge devices"], 0,
        "One is vendor-specific, one is framework-attached, one is general.",
        "TVM imports TFLite, ONNX, PyTorch etc. and compiles for ARM, x86, GPUs, accelerators and microcontrollers. TensorRT is NVIDIA's optimizer for its own GPUs (including Jetson). XLA is the compiler inside TensorFlow (jit_compile=True) and JAX.",
        topic="compilers", level=2),
    mcq("A textile mill in Tiruppur quantizes its defect detector to dynamic-range INT8: the file drops from 12 MB to 3.2 MB. Peak RAM during inference barely changes. Why?",
        ["Dynamic-range quantization stores weights in INT8 but keeps activations in float, and the activation buffers dominate peak RAM",
         "The converter silently failed and the model is still FP32",
         "INT8 weights need 4x more RAM than FP32 weights at runtime",
         "Peak RAM depends only on the input image size, never on the model"], 0,
        "Weights live in the file; activations are created at run time.",
        "Model size counts weights; peak RAM counts the activation (tensor arena) buffers plus the runtime. Dynamic-range keeps activations float, so those buffers stay the same size. Full-integer quantization makes activations INT8 too and cuts their memory ~4x.",
        diagram="""
Flash: [ weights INT8 3.2 MB ]
RAM:   [ input ][ act1 FP32 ][ act2 FP32 ]  <- peak
dynamic-range INT8 shrinks Flash, not the RAM row
""",
        topic="opt-metrics", level=2),
    out("orig_mb, new_mb = 14.2, 3.9\n"
        "print(f\"{orig_mb / new_mb:.2f}x\", f\"{100 * (1 - new_mb / orig_mb):.1f}%\")",
        ["3.64x 72.5%", "3.64x 27.5%", "0.27x 72.5%", "4.00x 75.0%"], 0,
        "Compression ratio = old / new; reduction = 1 - new / old.",
        "14.2 / 3.9 = 3.64x smaller, a 72.5% size reduction. Not a clean 4x because some tensors (biases, scales, metadata) stay larger than 1 byte per number. 27.5% is the fraction that remains.",
        question="Compression ratio and size reduction after INT8 + pruning. What does this print?",
        topic="opt-metrics", level=2),
    mcq("A toll-plaza ANPR model on a Raspberry Pi is accurate but too slow. Which lever is MOST likely to cut CPU latency on its own?",
        ["Full-integer INT8 quantization, so the CPU runs 8-bit integer kernels",
         "80% unstructured magnitude pruning",
         "Zipping the model file",
         "Adding more training data"], 0,
        "Which one actually reduces the work each multiply-add costs?",
        "INT8 kernels (XNNPACK, Ruy) process more values per SIMD instruction and move 4x fewer bytes, typically 2-3x faster on ARM. Unstructured pruning and zipping only shrink storage; dense kernels still do every multiply. More data does not change speed.",
        topic="compression-why", level=2),
    tf("The compression techniques stack: a common recipe is distil a smaller student, prune it, then quantize it to INT8.", True,
       "Each lever works on a different property.",
       "Distillation changes the architecture, pruning removes weights, quantization lowers precision. Applied in that order (checking accuracy after each step) the savings multiply. Quantization usually comes last, because training after it is awkward unless you use QAT.",
       topic="compression-why", level=2),
    mcq("Why do quantization schemes stretch the [min, max] range so that it always contains 0.0, and make 0.0 map to an exact integer (the zero point)?",
        ["Zero padding and ReLU outputs are extremely common; if 0.0 were not exact, every padded pixel and every zero activation would carry an error",
         "So that the scale is always 1.0",
         "Because negative numbers cannot be stored in INT8",
         "To make the model file smaller"], 0,
        "Where do exact zeros appear in a CNN?",
        "Convolutions pad borders with zeros and ReLU outputs many exact zeros. If 0.0 were represented as, say, 0.007, those errors would add up across the network. So the range is widened to include 0 and the zero point is an integer.",
        topic="quant-math", level=2),
    # ------------------------------------------------------------------ L3
    mcq("A smart-meter company in Pune applies 75% unstructured magnitude pruning to its INT8 TFLite load-forecasting model on a Raspberry Pi 5 (ARM Cortex-A76). The compressed model drops from 4.8 MB to 1.2 MB, but latency stays at 60 ms. What explains this, and what would cut latency?",
        ["The zeros are still stored and multiplied by dense ARM kernels, so only storage shrank; structured (channel/filter) pruning that removes whole channels would cut latency",
         "The Pi's cache is too small; buying a Pi with more RAM would make the pruned model faster",
         "Pruning needs more fine-tuning epochs; after that the latency will drop by 75%",
         "INT8 and pruning cannot be combined; going back to FP32 would let the pruning take effect"], 0,
        "What does a dense matrix multiply do with a zero?",
        "Unstructured sparsity keeps every tensor's shape. XNNPACK's dense kernels multiply 0 × x just as fast as any other value, so the work is unchanged; only compressed storage benefits. Structured pruning shrinks the tensor shapes, so every kernel does less work. Common wrong answer: 'fine-tune longer'.",
        analogy="Like setting half the cells of a SQL table to NULL: the backup compresses better, but a full scan still reads every row. Dropping columns (structured pruning) makes every query cheaper.",
        diagram="""
unstructured (same shape)   structured (filters gone)
[0 a 0 b]                   [a b c d]
[c 0 0 d]                   [e f g h]
[0 0 e 0]   dense kernel    smaller dense tensor:
[f 0 0 g]   still does 16   kernel does 8
""",
        topic="pruning", level=3),
    out("def conv(K, M, N, H, W):          # multiply-adds of a KxK conv\n"
        "    return K * K * M * N * H * W\n"
        "before = conv(3, 64, 128, 56, 56) + conv(3, 128, 128, 56, 56)\n"
        "# keep 50% of the filters in BOTH layers (layer 2 also loses inputs)\n"
        "after = conv(3, 64, 64, 56, 56) + conv(3, 64, 64, 56, 56)\n"
        "print(round(after / before, 3))",
        ["0.333", "0.5", "0.25", "0.667"], 0,
        "Removing a filter in layer 1 removes an input channel of layer 2 as well.",
        "Layer 1 keeps half its outputs (×0.5). Layer 2 keeps half its outputs AND has half the inputs (×0.25). Layer 2 was twice as expensive, so the total is (0.5 + 0.25 × 2) / 3 = 0.333. The common answer 0.5 forgets that structured pruning compounds across consecutive layers.",
        question="Structured filter pruning of two consecutive conv layers. What fraction of the compute remains?",
        topic="pruning", level=3),
    out("import numpy as np\n"
        "w = np.array([[0.02, -0.01, 0.015],   # channel 0: tiny weights\n"
        "              [1.6, -2.0, 0.9]])       # channel 1: large weights\n"
        "def err(s):\n"
        "    q = np.clip(np.round(w / s), -127, 127)\n"
        "    return np.abs(q * s - w)[0].round(4).tolist()\n"
        "print(err(np.abs(w).max() / 127))                        # per-tensor\n"
        "print(err(np.abs(w).max(axis=1, keepdims=True) / 127))   # per-channel",
        ["[0.0043, 0.0057, 0.0007]\n[0.0, 0.0001, 0.0]",
         "[0.0, 0.0001, 0.0]\n[0.0043, 0.0057, 0.0007]",
         "[0.0, 0.0, 0.0]\n[0.0, 0.0, 0.0]",
         "[0.0043, 0.0057, 0.0007]\n[0.0043, 0.0057, 0.0007]"], 0,
        "With one scale, how many integer steps does channel 0 get?",
        "Per-tensor, the scale is set by -2.0 (0.0157 per step), so channel 0's weights fall on 0 or ±1 step: errors of 20-60% of each weight. Per-channel, channel 0 gets its own scale (0.02/127) and is nearly exact. Depthwise layers have exactly this spread of channel ranges, which is why TFLite quantizes weights per-channel.",
        question="Quantization error on channel 0, per-tensor vs per-channel scales. What does this print?",
        analogy="Like storing a paise column and a crore column with one shared unit of 'lakhs': the small column rounds to zero.",
        topic="quant-math", level=3),
    mcq("A weight tensor's channel has values in [-0.5, 0.4]. Using TFLite's symmetric INT8 weight scheme (range −127..127, zero_point = 0), what is its scale?",
        ["0.5 / 127 ≈ 0.003937",
         "0.9 / 255 ≈ 0.003529",
         "0.4 / 127 ≈ 0.00315",
         "0.5 / 128 ≈ 0.003906"], 0,
        "Symmetric: use the largest absolute value.",
        "Symmetric scale = max|w| / 127 = 0.5 / 127. The (max - min)/255 formula is the asymmetric one used for activations. Using 0.4 would clip -0.5. TFLite uses −127..127 for weights (not −128) so the range is exactly symmetric.",
        topic="quant-math", level=3),
    mcq("A Bengaluru agritech startup quantizes a MobileNetV2 leaf-disease classifier with full-integer PTQ. Accuracy falls from 91% to 79%. Per-channel weights are already on. What is the standard next step?",
        ["Quantization-aware training: fine-tune with fake-quantization ops for a few epochs, then convert to INT8 again",
         "Ship it: a 12-point drop is normal and cannot be fixed",
         "Switch to dynamic-range quantization to make the Edge TPU run it",
         "Prune 80% of the weights to make up for the lost accuracy"], 0,
        "When post-training is not enough, train with the rounding in the loop.",
        "QAT simulates INT8 rounding and clipping in the forward pass while keeping float weights, so training finds weights that are robust to quantization. It usually recovers most of the drop for depthwise-heavy nets. Dynamic-range is not integer-only (no Edge TPU), and pruning adds error.",
        topic="quant-ptq-qat", level=3),
    tf("Quantization-aware training runs the training itself in INT8 arithmetic.", False,
       "What happens to the gradients?",
       "QAT trains in float. Fake-quantization ops round and clip values to the INT8 grid in the forward pass; the backward pass treats rounding as identity (straight-through estimator). Real INT8 tensors appear only when the model is converted.",
       topic="quant-ptq-qat", level=3,
       diagram="""
forward:  w_float --fake_quant--> w_q (INT8 grid) --> conv
backward: dL/dw_float = dL/dw_q  (straight-through)
convert:  w_q stored as int8 + scale, zero_point
"""),
    mcq("For full-integer PTQ of a poultry-farm camera model that runs 24×7, the engineer passes 10 daytime images as the representative dataset. In deployment, night-time accuracy is poor. Most likely cause?",
        ["The calibrated activation ranges came from bright daytime images only, so night inputs fall in a poorly covered part of the INT8 range (or get clipped)",
         "The representative dataset changes the model's weights, and 10 images overfit them",
         "Night images need FP16, which INT8 models cannot accept",
         "The representative dataset only affects the input tensor, not internal layers"], 0,
        "What does the converter use those images for?",
        "The representative dataset is only used to measure activation ranges; it does not retrain anything. If it does not cover the deployment conditions (night, IR, rain), the scales fit the wrong distribution. Use a few hundred samples that span real operating conditions.",
        topic="quant-ptq-qat", level=3),
    out("import numpy as np\n"
        "def sm(z, T=1.0):\n"
        "    e = np.exp(z / T)\n"
        "    return e / e.sum()\n"
        "zt, zs = np.array([5.0, 2.0, 0.0]), np.array([3.0, 2.5, 0.5])\n"
        "T, alpha, y = 2.0, 0.5, 0\n"
        "pt, ps = sm(zt, T), sm(zs, T)\n"
        "kl = float(np.sum(pt * np.log(pt / ps)))\n"
        "ce = float(-np.log(sm(zs)[y]))\n"
        "print(round(ce, 3), round(kl, 3), round(alpha * ce + (1 - alpha) * T * T * kl, 3))",
        ["0.524 0.167 0.595", "0.524 0.167 0.346", "0.167 0.524 0.595", "0.524 0.167 0.69"], 0,
        "Remember the T² factor on the soft term.",
        "Hard term CE = -ln(softmax(zs)[0]) = 0.524. Soft term KL(teacher_T ‖ student_T) = 0.167. Loss = 0.5 × 0.524 + 0.5 × 4 × 0.167 = 0.595. Leaving out T² gives 0.346: the soft signal would then be four times too weak.",
        question="Hinton-style distillation loss (α on the hard-label term). What does this print?",
        diagram="""
teacher: softmax(z_t/T) = p_t --+
                                +-- KL(p_t||p_s)
student: softmax(z_s/T) = p_s --+
student: softmax(z_s) vs label ---- CE
loss = a x CE + (1-a) x T^2 x KL
""",
        topic="distillation", level=3),
    mcq("Why is the soft-target term of the distillation loss multiplied by T²?",
        ["The gradients of the softened term shrink by about 1/T², so multiplying by T² keeps the soft and hard terms on a comparable scale when T changes",
         "To make the loss always positive",
         "Because the teacher has T² more layers than the student",
         "To square the error so large mistakes count more"], 0,
        "What does dividing the logits by T do to their gradients?",
        "Softening by T makes the soft-target gradients roughly 1/T² as large (Hinton et al. 2015). Scaling by T² means you can change T without retuning α. Convention note: some write α on the soft term instead; the T² factor is the same either way.",
        topic="distillation", level=3),
    mcq("A Hyderabad logistics firm has a ResNet-50 parcel-damage classifier (25M parameters) and wants a model for a Jetson Nano. Which distillation plan is sound?",
        ["Use the ResNet-50 as teacher and train a MobileNetV3 student on the same images with soft + hard targets, then quantize the student",
         "Copy every other ResNet-50 layer into the student; distillation requires the same architecture family",
         "Distil without any images: the teacher's weights are enough",
         "Train the student only on hard labels, then call it distilled"], 0,
        "Does the student have to look like the teacher?",
        "Response-based distillation only needs the teacher's outputs on training images, so the student can be any architecture that suits the device. Copying layers (DistilBERT-style initialisation) is an option for same-family students, not a requirement. Hard labels only is ordinary training.",
        topic="distillation", level=3),
    out("acc_lat = [(0.75, 80), (0.76, 120), (0.73, 60)]   # (accuracy, ms on phone)\n"
        "T, w = 80, -0.07                                  # target latency, exponent\n"
        "for acc, lat in acc_lat:\n"
        "    print(lat, round(acc * (lat / T) ** w, 4))",
        ["80 0.75\n120 0.7387\n60 0.7448", "80 0.75\n120 0.76\n60 0.73",
         "80 0.75\n120 0.7813\n60 0.7148", "80 0.7387\n120 0.75\n60 0.7448"], 0,
        "w is negative: being slower than T is penalised, being faster is rewarded a little.",
        "MnasNet's reward is ACC × (LAT / T)^w. The 120 ms model has the best accuracy but (1.5)^-0.07 = 0.972 pulls it to 0.7387; the 60 ms model gets a small bonus (0.7448); the on-target 80 ms model wins at 0.75. The search therefore trades accuracy for measured latency instead of FLOPs.",
        question="MnasNet-style hardware-aware NAS reward for three candidates. What does this print?",
        topic="nas", level=3),
    out("lut = {\"conv3x3_s2\": 1.8, \"mbconv_e6_k3\": 2.4,      # ms, measured on\n"
        "       \"mbconv_e3_k5\": 3.1, \"pool_fc\": 0.6}         # the target phone\n"
        "arch = [\"conv3x3_s2\"] + [\"mbconv_e6_k3\"] * 4 + [\"mbconv_e3_k5\"] * 3 + [\"pool_fc\"]\n"
        "print(round(sum(lut[op] for op in arch), 1))",
        ["21.3", "7.9", "18.5", "9"], 0,
        "Predicted latency = sum of the measured latency of each block used.",
        "1.8 + 4 × 2.4 + 3 × 3.1 + 0.6 = 21.3 ms. A latency lookup table lets NAS predict a candidate's on-device latency in microseconds instead of deploying every candidate. 7.9 adds each block type once and ignores repeats.",
        question="Predicting a candidate's latency from a per-block lookup table. What does this print?",
        topic="nas", level=3),
    mcq("A team ranks NAS candidates by FLOPs to save time. On their ARM phone, the lowest-FLOP model is slower than one with 30% more FLOPs. What is the best explanation?",
        ["FLOPs ignore memory access, parallelism and how well each op is implemented on that chip; depthwise and fragmented ops can be memory-bound, so real latency must be measured or looked up",
         "The phone's clock was throttled during the second test, so the result is noise",
         "FLOPs count only additions; multiplications are free",
         "Lower FLOPs always means lower latency; the measurement must be wrong"], 0,
        "ShuffleNet V2 and MnasNet made exactly this point.",
        "FLOPs are an indirect proxy. Memory access cost, number of kernel launches, element-wise ops and kernel quality all change real speed. That is why hardware-aware NAS uses measured latency or latency tables per target device.",
        topic="nas", level=3),
    out("K, M, N, H, W = 3, 64, 128, 56, 56\n"
        "std = K * K * M * N * H * W\n"
        "sep = K * K * M * H * W + M * N * H * W\n"
        "print(round(std / 1e6, 1), round(sep / 1e6, 1), round(std / sep, 2))",
        ["231.2 27.5 8.41", "231.2 1.8 128.0", "231.2 25.7 9.0", "28.9 27.5 1.05"], 0,
        "Compute both costs in millions of multiply-adds.",
        "Standard: 9·64·128·56·56 = 231.2M MACs. Depthwise 9·64·3136 = 1.8M + pointwise 64·128·3136 = 25.7M = 27.5M. Ratio 8.41 = 1 / (1/128 + 1/9). The 9.0 answer uses only 1/K²; 128 forgets the pointwise conv.",
        question="By-hand FLOP saving of one MobileNet layer (56×56, 64 -> 128 channels). What does this print?",
        topic="mobilenet", level=3),
    mcq("A MobileNetV1 layer cuts MACs 8x compared with a standard conv, but on the target CPU the layer only runs ~3x faster. Why?",
        ["The depthwise part has very little arithmetic per byte loaded, so it is limited by memory bandwidth rather than compute, and kernels for it are less efficient",
         "MAC counts for depthwise layers are always wrong by a factor of 3",
         "The pointwise 1×1 conv is slower than a 3×3 conv",
         "CPUs cannot run depthwise convolutions at all and fall back to emulation"], 0,
        "Arithmetic intensity: operations per byte moved.",
        "A depthwise filter touches each input value only K² times and never reuses it across output channels, so the time goes to moving data, not multiplying it. FLOP savings therefore overstate speed-ups. Measure on the device.",
        topic="mobilenet", level=3),
    out("a, b, g = 1.2, 1.1, 1.15        # depth, width, resolution bases\n"
        "phi = 2\n"
        "print(round(a ** phi, 2), round(b ** phi, 2), round(224 * g ** phi),\n"
        "      round((a * b * b * g * g) ** phi, 2))",
        ["1.44 1.21 296 3.69", "1.44 1.21 258 4.0", "2.4 2.2 515 3.69", "1.44 1.21 296 1.92"], 0,
        "Each multiplier is base^φ; FLOPs follow (α·β²·γ²)^φ.",
        "φ = 2: depth ×1.44, width ×1.21, resolution 224 × 1.3225 ≈ 296 px, FLOPs × 1.92² ≈ 3.69 (≈ 2^φ = 4). 2.4/2.2 multiply instead of raising to a power; 1.92 is one φ step only.",
        question="EfficientNet compound scaling from B0 with φ = 2. What does this print?",
        topic="efficientnet-shufflenet", level=3),
    mcq("What goes wrong if you stack several pointwise group convolutions (g groups each) without a channel shuffle in between?",
        ["Each output group only ever sees the channels of its own group, so the groups become independent sub-networks and accuracy drops",
         "The compute goes up by a factor of g",
         "The layers produce an error because the shapes do not match",
         "Nothing; the shuffle exists only to make training faster"], 0,
        "Trace one channel through two grouped layers.",
        "Group 1's outputs feed only group 1 of the next layer, forever. The channel shuffle (reshape to g×n, transpose, flatten) sends each group's outputs to every group in the next layer, restoring cross-channel information at almost no cost.",
        topic="efficientnet-shufflenet", level=3,
        diagram="""
no shuffle:   G1 -> G1 -> G1     G2 -> G2 -> G2  (isolated)
with shuffle: G1 --\\  /--> G1
                    \\/
              G2 ---/\\---> G2   (groups mix)
"""),
    tf("ShuffleNet V2's authors argue that FLOPs alone are not a reliable measure of speed, and give guidelines such as keeping input and output channel widths equal to minimise memory access cost.", True,
       "The paper is subtitled 'Practical Guidelines for Efficient CNN Architecture Design'.",
       "Ma et al. (2018): (1) equal channel widths minimise memory access, (2) too many groups raise it, (3) network fragmentation hurts parallelism, (4) element-wise ops are not free. They benchmarked on real GPU and ARM hardware.",
       topic="efficientnet-shufflenet", level=3),
    mcq("A bank's on-device cheque-text classifier must fit in 80 MB of RAM and answer in under 40 ms on a mid-range Android phone. Measured options: BERT-base INT8 (110 MB, 120 ms), DistilBERT INT8 (66 MB, 75 ms), TinyBERT-4 INT8 (15 MB, 14 ms), DistilBERT FP32 (264 MB, 150 ms). Which meets both budgets?",
        ["TinyBERT-4 INT8",
         "DistilBERT INT8",
         "BERT-base INT8",
         "DistilBERT FP32"], 0,
        "Check memory AND latency for each.",
        "DistilBERT INT8 fits the 80 MB budget but misses 40 ms; BERT-base and FP32 DistilBERT fail both. Only TinyBERT-4 INT8 passes both. Then check its accuracy on the bank's own data; ~96% of BERT on GLUE does not guarantee 96% on cheques.",
        diagram="""
model             RAM<=80MB  p<40ms
BERT-base INT8      110 x     120 x
DistilBERT INT8      66 ok     75 x
TinyBERT-4 INT8      15 ok     14 ok
DistilBERT FP32     264 x     150 x
""",
        topic="slm", level=3),
    out("bert_ms = 120\n"
        "# DistilBERT paper: '60% faster' means 1.6x the speed\n"
        "print(round(bert_ms / 1.6, 1), round(bert_ms * (1 - 0.6), 1))",
        ["75.0 48.0", "48.0 75.0", "75.0 75.0", "72.0 48.0"], 0,
        "'60% faster' is a speed ratio, not a 60% time cut.",
        "60% faster = 1.6x throughput, so time = 120 / 1.6 = 75 ms (that is the DistilBERT paper's meaning: inference time is ~62% of BERT's). Cutting time by 60% (48 ms) would be 2.5x faster. Exam answers should state the convention used.",
        question="BERT-base takes 120 ms per query on a phone. What does this print?",
        topic="slm", level=3),
    mcq("A traffic camera's activations are mostly in [0, 3] but a rare glare frame produces a value of 60. Why does TensorRT's entropy (KL-divergence) calibrator usually beat plain min-max calibration here?",
        ["Min-max sets the INT8 range to [0, 60], so the bulk of values in [0, 3] get only ~6 of the 127 levels; the entropy calibrator clips the rare outlier and keeps fine resolution where the data actually is",
         "Min-max calibration cannot handle positive-only activations",
         "The entropy calibrator keeps every activation in FP32",
         "Entropy calibration needs no calibration images, so it cannot overfit"], 0,
        "Count how many integer levels cover [0, 3] under each range.",
        "Range [0, 60] makes one step 0.47, so values 0-3 map to integers 0-6: huge rounding error for the common case. The entropy calibrator picks the clipping threshold that keeps the INT8 distribution closest (in KL divergence) to the FP32 one: a few outliers saturate, everything else is precise.",
        analogy="Like a chart whose y-axis is set by one spike: every normal value collapses into a flat line at the bottom.",
        topic="compilers", level=3),
    tf("TVM's auto-tuners (AutoTVM, Ansor/MetaSchedule) choose loop tiling and other kernel schedules by compiling candidates and timing them on the target device.", True,
       "It searches, then measures.",
       "For each operator TVM generates many candidate schedules (tile sizes, unrolling, vectorisation), runs them on the real board (or via an RPC tracker) and keeps the fastest. The tuning log is device-specific: a schedule tuned for a Cortex-A72 is not optimal for a Jetson GPU.",
       topic="compilers", level=3),
    out("p_fp32_w, t_fp32_ms = 2.4, 45     # board power (W), latency (ms)\n"
        "p_int8_w, t_int8_ms = 2.6, 18\n"
        "e32 = p_fp32_w * t_fp32_ms           # W x ms = mJ\n"
        "e8 = p_int8_w * t_int8_ms\n"
        "print(round(e32, 1), round(e8, 1), round(e32 / e8, 2))",
        ["108.0 46.8 2.31", "108.0 46.8 2.5", "2.4 2.6 0.92", "47.4 20.6 2.3"], 0,
        "Energy per inference = power × time.",
        "FP32: 2.4 W × 45 ms = 108 mJ. INT8: 2.6 W × 18 ms = 46.8 mJ, 2.31x less energy. The INT8 run draws slightly more power, but for much less time. 2.5 is the latency ratio alone; comparing power alone (0.92) wrongly suggests INT8 costs more.",
        question="Energy per inference before and after INT8 on a Raspberry Pi. What does this print?",
        topic="opt-metrics", level=3),
    mcq("A people-counting model for a Kolkata metro gate fits in Flash after INT8 quantization, but its peak activation RAM is 2.6x too large for the MCU's SRAM. Which change targets activation memory most directly?",
        ["Reduce the input resolution (e.g. 160×160 -> 96×96) or thin the early high-resolution layers, since activation size scales with H × W × channels",
         "Prune 90% of the weights unstructured",
         "Distil a student with the same input size and layer widths",
         "Switch the weights from per-tensor to per-channel quantization"], 0,
        "Which tensors are biggest at run time?",
        "Peak RAM is set by the largest activation tensors, which live in the early, high-resolution layers. Going from 160² to 96² cuts them to (96/160)² = 0.36x. Weight pruning and per-channel scales change the weights, not the activation buffers.",
        topic="opt-metrics", level=3),
    mcq("Why does keeping a model small enough to stay in on-chip SRAM save so much energy on an edge accelerator?",
        ["Reading a value from off-chip DRAM costs on the order of 100x the energy of an on-chip SRAM read, and far more than the multiply itself",
         "SRAM runs at a lower voltage only when the model is INT8",
         "DRAM cannot store INT8 values",
         "SRAM reads are free"], 0,
        "Horowitz (2014): a 32-bit DRAM read ~640 pJ, an 8 KB SRAM read ~5 pJ.",
        "At 45 nm a 32-bit float multiply is ~3.7 pJ and an 8-bit integer multiply ~0.2 pJ, but a DRAM access is ~640 pJ. Data movement dominates, so quantization (fewer bytes) and small models (stay on-chip) save more energy than the arithmetic savings alone suggest.",
        topic="compression-why", level=3,
        diagram="""
energy per op (pJ, 45 nm, approx.)
INT8 multiply   | 0.2
FP32 multiply   |# 3.7
SRAM 32b read   |# 5
DRAM 32b read   |######################## 640
"""),
    fill("In the TFLite converter, full-integer PTQ is enabled by setting converter.____ to a generator that yields sample inputs.", "representative_dataset",
         "The calibration data's attribute name.",
         "converter.representative_dataset = gen, where gen yields ~100-500 real input samples. Without it the converter cannot size the activation ranges, so only dynamic-range quantization is possible.",
         topic="quant-ptq-qat", level=3),
    # ------------------------------------------------------------------ L4
    mcq("A warehouse robot company uses both a Jetson Orin (Ampere GPU) and a Raspberry Pi 4. They apply 2:4 semi-structured sparsity (2 zeros in every block of 4 weights) and fine-tune. What speed-up should they expect?",
        ["Up to ~2x on the matrix-multiply layers on the Orin's Sparse Tensor Cores via TensorRT; roughly none on the Pi 4, whose dense kernels do not exploit the pattern",
         "Exactly 2x on both devices, because half the weights are zero",
         "None on either device, because any sparsity is unstructured",
         "4x on the Pi 4 and 2x on the Orin"], 0,
        "Sparsity speeds things up only where hardware or kernels skip the zeros.",
        "2:4 is a fixed pattern that Ampere and later Tensor Cores can skip in hardware, giving up to ~2x math throughput (end-to-end gains are smaller). The Pi's ARM CPU has no such support, so the zeros are multiplied as usual. The same sparse model is fast on one device and not the other.",
        topic="pruning", level=4),
    mcq("An engineer applies one global magnitude threshold across a whole MobileNet to reach 70% sparsity. Accuracy collapses, and the first conv and several depthwise layers are almost entirely zero. Why, and what is the fix?",
        ["Those layers have few weights with small magnitudes, so a single global threshold wipes them out; use layer-wise sparsity targets and keep small sensitive layers (first conv, depthwise) dense or lightly pruned",
         "Global pruning always prunes the largest weights first",
         "Depthwise layers cannot be pruned at all, so the converter deleted them",
         "70% sparsity is impossible for any CNN"], 0,
        "Compare weight scales and counts across layers.",
        "Global thresholds compare magnitudes across layers that have different scales. Tiny layers like depthwise filters (9 weights per channel) carry critical information with small values and get erased. Practice: per-layer targets from a sensitivity scan, skip first/last and depthwise layers.",
        topic="pruning", level=4),
    tf("After pruning, running standard quantization-aware training can re-introduce non-zero values into pruned weights, which is why TF-MOT offers pruning-preserving QAT.", True,
       "QAT updates every float weight unless told not to.",
       "Standard QAT fine-tunes all weights, so zeros can drift away from zero and the sparsity is lost. Pruning-preserving QAT (and sparsity-preserving clustering) keep the mask fixed while learning quantization-robust values. The order and the mask both matter in a combined pipeline.",
       topic="pruning", level=4),
    out("s_in, s_w, s_out, z_out = 0.02, 0.005, 0.05, -10\n"
        "acc = 1234                       # int32 accumulator of int8 x int8 products\n"
        "M = s_in * s_w / s_out           # requantization multiplier\n"
        "print(round(M, 4), int(round(acc * M)) + z_out)",
        ["0.002 -8", "0.002 2", "0.002 -10", "2.0 2458"], 0,
        "acc is in units of s_in × s_w; convert to units of s_out and add the zero point.",
        "Integer-only inference accumulates int8 × int8 products in int32, whose unit is s_in·s_w. Re-expressing it in the output scale needs M = s_in·s_w/s_out = 0.002: 1234 × 0.002 = 2.47 -> 2, plus zero_point -10 = -8. On an MCU M is stored as a fixed-point int32 multiplier plus a shift, so no float math runs.",
        question="Requantizing a conv's int32 accumulator to an INT8 output. What does this print?",
        analogy="Like integer money code that stores paise and converts with a fixed multiplier and rounding, never touching floats.",
        topic="quant-math", level=4),
    mcq("Why are BatchNorm layers folded into the preceding convolution's weights and bias before (or during) quantization for edge deployment?",
        ["Folding turns Conv + BN into one conv with adjusted weights, so there is one op and one set of ranges to quantize; quantizing them separately adds rounding error and an extra float op that integer-only hardware cannot run",
         "BatchNorm only works in FP64",
         "BatchNorm stores the training data, which must be removed for privacy",
         "Folding doubles the number of parameters, which improves accuracy"], 0,
        "At inference BN is just a fixed scale and shift.",
        "At inference BN computes γ(x − μ)/σ + β with frozen statistics: a per-channel affine map. Merging it into W and b removes an op, a memory round-trip and a separately-quantized tensor. QAT simulates the folded weights so training sees the same rounding as deployment.",
        topic="quant-ptq-qat", level=4),
    fill("QAT passes gradients through the non-differentiable rounding step by treating it as identity in the backward pass. This trick is called the ____ estimator. (hyphenated word)", "straight-through",
         "Gradients go straight through.",
         "round() has zero gradient almost everywhere, which would stop learning. The straight-through estimator (STE) uses dL/dx ≈ dL/dq (often zeroed outside the clipping range), so float weights can still learn to sit well on the INT8 grid.",
         topic="quant-ptq-qat", level=4),
    mcq("A team distils a crop-classifier teacher into a tiny student and sets T = 50 to 'transfer as much dark knowledge as possible'. The student learns poorly. Why?",
        ["At very high T the teacher's softened distribution is almost uniform, so it carries almost no information about which classes are similar; moderate T (about 2-5) is usually best, tuned on validation data",
         "High T makes the teacher's outputs one-hot",
         "T only affects the student, not the teacher",
         "Distillation only works with T below 1"], 0,
        "What does softmax(z / T) look like as T grows without bound?",
        "As T -> ∞, softmax(z / T) -> 1/C for every class: no signal. As T -> 1 it is nearly one-hot: little dark knowledge. The sweet spot is in between, and smaller students often prefer lower T because they cannot match fine detail anyway.",
        topic="distillation", level=4),
    mcq("You want a small student to also match a teacher's intermediate feature maps (feature distillation), but the student's layer has 64 channels and the teacher's has 256. What is the standard approach?",
        ["Add a small learned projection (e.g. a 1×1 conv from 64 to 256 channels) on the student side during training, and drop it at deployment",
         "Delete 192 of the teacher's channels at random",
         "Feature distillation is impossible unless the widths match",
         "Pad the student's features with 192 channels of zeros"], 0,
        "FitNets used a 'regressor'.",
        "FitNets-style hint training adds a regressor that maps student features into the teacher's space, and the loss compares them there. The projection is a training-only scaffold, so the deployed student keeps its small size. Zero padding cannot match the teacher's information.",
        topic="distillation", level=4),
    mcq("A company ships the same vision feature on 12 phone models and 3 Jetson variants. Why is Once-for-All (OFA) attractive compared with running hardware-aware NAS once per device?",
        ["OFA trains one large supernet once; a specialised subnet (depth, width, kernel size, resolution) is then picked per device with a latency predictor, without retraining from scratch",
         "OFA produces one fixed network that is optimal on all 15 devices",
         "OFA needs no training at all",
         "OFA only works for language models"], 0,
        "Train once, specialise many times.",
        "Per-device NAS repeats an expensive search and training for every target. OFA decouples training from search: the supernet's weights are shared, and picking a subnet for a new device is a cheap search over the latency table, plus optional brief fine-tuning. The cost grows with devices only at the cheap step.",
        analogy="Like one responsive web app that serves the right layout per screen size, instead of a separate app built for every device.",
        topic="nas", level=4),
    tf("In weight-sharing (one-shot) NAS, the ranking of candidates by their accuracy inside the supernet can differ from their ranking when each is trained alone, so the final pick should be retrained and re-measured.", True,
       "Shared weights are a compromise across many subnets.",
       "Supernet accuracy is a cheap proxy. Studies found its correlation with stand-alone accuracy can be weak, so finalists are trained from scratch (or fine-tuned) and measured on the device before deployment. The same 'proxy vs reality' issue as FLOPs vs latency.",
       topic="nas", level=4),
    mcq("Why does MobileNetV2 leave out the ReLU after the 1×1 projection layer (the 'linear bottleneck')?",
        ["In the thin bottleneck there are few channels, and ReLU zeroes every negative value, destroying information that cannot be recovered; keeping it linear preserves it",
         "ReLU is too slow on mobile CPUs",
         "The projection layer has no weights, so an activation would do nothing",
         "To make the network non-differentiable"], 0,
        "ReLU is safe in wide spaces, lossy in narrow ones.",
        "Sandler et al. show that ReLU on a low-dimensional manifold collapses parts of it, while in the expanded (×6) space the information survives. So non-linearity is applied in the wide layers and the thin bottleneck stays linear. Adding ReLU there measurably lowers accuracy.",
        topic="mobilenet", level=4),
    out("import numpy as np\n"
        "x = np.array([-4.0, -1.0, 0.0, 1.0, 4.0])\n"
        "hswish = x * np.clip(x + 3, 0, 6) / 6 + 0.0   # MobileNetV3\n"
        "print(hswish.round(3).tolist())",
        ["[0.0, -0.333, 0.0, 0.667, 4.0]", "[0.0, 0.0, 0.0, 1.0, 4.0]",
         "[-0.072, -0.269, 0.0, 0.731, 3.928]", "[0.0, -0.333, 0.0, 0.667, 6.0]"], 0,
        "h-swish(x) = x · ReLU6(x + 3) / 6.",
        "-4 -> 0; -1 -> -1 × 2/6 = -0.333; 1 -> 4/6 = 0.667; 4 -> 4 × 6/6 = 4. The third option is real swish (x·sigmoid(x)). h-swish approximates it with ReLU6 pieces, which are cheap on phones and quantize well because there is no exponential.",
        question="MobileNetV3's hard-swish on five inputs. What does this print?",
        topic="mobilenet", level=4),
    mcq("EfficientNet-Lite (the edge variant) removes squeeze-and-excitation blocks and replaces swish with ReLU6. Why?",
        ["Both changes make the model friendlier to INT8 quantization and to edge accelerators: SE adds poorly supported ops and swish's unbounded smooth output is harder to quantize than ReLU6's fixed [0, 6] range",
         "To make the model larger and more accurate",
         "Because swish cannot be trained on GPUs",
         "SE blocks are only used in language models"], 0,
        "Think about the Edge TPU and an INT8 range.",
        "SE blocks need global pooling plus small FC layers and element-wise multiplies, which some accelerators run poorly. ReLU6 bounds activations, so their INT8 scale is stable. The Lite models lose a little float accuracy but keep much more after INT8 PTQ.",
        topic="efficientnet-shufflenet", level=4),
    out("vocab, hidden = 30522, 312          # TinyBERT-4\n"
        "emb = vocab * hidden\n"
        "print(emb, round(emb / 14.5e6, 2))  # share of its ~14.5M parameters",
        ["9522864 0.66", "9522864 0.34", "97344 0.01", "9522864 1.52"], 0,
        "The word-embedding table is vocab × hidden.",
        "30,522 × 312 = 9.5M parameters: about two-thirds of TinyBERT-4. The 4 transformer layers are the small part. So on-device you shrink the vocabulary (domain vocabulary pruning) or quantize the embedding table too; quantizing only the Linear layers (typical dynamic INT8) leaves the biggest tensor in FP32.",
        question="How much of TinyBERT-4 is the embedding table? What does this print?",
        topic="slm", level=4),
    mcq("A hospital in Chennai wants an offline triage-note classifier on nurses' ₹12,000 Android phones. Which plan is the strongest?",
        ["Distil BERT into a TinyBERT-sized student on in-domain notes, quantize to INT8 (embeddings included), then benchmark latency, RAM and accuracy on the actual phone",
         "Use BERT-base FP32 and ask nurses to wait",
         "Quantize BERT-base to INT8 and skip validation, since INT8 never changes predictions",
         "Prune BERT-base 90% unstructured; the file gets small enough"], 0,
        "Stack the levers, then measure on the real device.",
        "Distillation cuts layers (latency), INT8 cuts memory and speeds integer kernels, and in-domain data keeps accuracy on clinical text. Unstructured pruning would only shrink storage; skipping on-device benchmarking hides RAM and thermal problems.",
        topic="slm", level=4),
    mcq("A model compiled with XLA (jit_compile=True) runs fast in tests but very slowly in production, where each request has a different sequence length. What is happening?",
        ["XLA specialises the compiled program to the input shapes; each new shape triggers a recompile. Pad or bucket inputs into a few fixed shapes",
         "XLA only works on GPUs, so production fell back to an interpreter",
         "XLA disables operator fusion for text models",
         "Production servers have slower clocks"], 0,
        "Compilers love static shapes.",
        "XLA (like TensorRT engines with fixed profiles) generates code for specific tensor shapes. Variable shapes mean compile time is paid again and again. Bucketing to a few padded lengths keeps the cache hits high. On edge devices, static shapes are the norm for exactly this reason.",
        analogy="Like a query planner that caches one plan per query shape: send a new shape every time and you pay for planning on every request.",
        topic="compilers", level=4),
    out("import numpy as np\n"
        "rng = np.random.default_rng(0)\n"
        "a = np.abs(rng.normal(0, 1, 10000)); a[0] = 60.0   # one glare outlier\n"
        "bulk = a < 3\n"
        "for name, hi in [(\"minmax\", a.max()), (\"p99.99\", np.quantile(a, 0.9999))]:\n"
        "    s = hi / 127\n"
        "    q = np.clip(np.round(a / s), 0, 127) * s\n"
        "    rms = np.sqrt(np.mean((q[bulk] - a[bulk]) ** 2))\n"
        "    print(name, round(float(s), 4), round(float(rms), 4))",
        ["minmax 0.4724 0.137\np99.99 0.0307 0.0089", "minmax 0.0307 0.0089\np99.99 0.4724 0.137",
         "minmax 0.4724 0.0089\np99.99 0.0307 0.137", "minmax 0.4724 0.137\np99.99 0.4724 0.137"], 0,
        "A tighter range means a smaller step for the common values.",
        "Min-max lets one outlier set the step to 0.47, so typical values (0-3) have ~0.14 RMS error. Clipping at the 99.99th percentile gives a step of 0.03 and ~15x less error on the bulk, at the price of saturating the outlier. This is the idea behind TensorRT's percentile and entropy calibrators.",
        question="Calibrating one activation's INT8 range: min-max vs percentile clipping. What does this print?",
        topic="compilers", level=4),
    mcq("A vendor's report for a quantized model says: 'FP32: 40 ms latency. INT8: 1,600 inferences/s throughput, so 0.6 ms per inference: 66x faster!' What is wrong?",
        ["The INT8 throughput was measured with a large batch, so 1/throughput is not single-request latency; compare batch-1 latency with batch-1 latency",
         "Nothing; 1/throughput always equals latency",
         "INT8 throughput can never exceed FP32 throughput",
         "Latency should be reported in seconds, not ms"], 0,
        "Batch 32 at 20 ms also gives 1,600/s.",
        "Throughput with batching hides the per-request wait: 32 inputs in 20 ms is 1,600/s, yet each user waits 20 ms. A fair before/after table fixes batch size, threads, warm-up and the device, and reports latency, throughput, energy and RAM separately.",
        analogy="Like quoting a server's requests per second under full load as if it were the page-load time one user sees.",
        topic="opt-metrics", level=4),
    out("inf_mj, radio_mj, sleep_mj = 5, 120, 30   # energy per minute, per source\n"
        "total = inf_mj + radio_mj + sleep_mj\n"
        "after = inf_mj / 4 + radio_mj + sleep_mj   # INT8 makes inference 4x cheaper\n"
        "print(round(inf_mj / total, 3), round(1 - after / total, 3))",
        ["0.032 0.024", "0.032 0.75", "0.25 0.024", "0.968 0.75"], 0,
        "Amdahl's law, for energy.",
        "Inference is only 3.2% of the energy budget; the radio dominates. Making inference 4x cheaper saves just 2.4% of battery. Optimizing the model would not move the needle; sending fewer, smaller messages (features, not raw data) would. Always find the real bottleneck before compressing.",
        question="A battery LoRa soil sensor in a Nashik vineyard. What does this print?",
        analogy="Like optimizing a function that takes 3% of request time while the database call takes 80%: profile before you optimize.",
        topic="compression-why", level=4),
    # ------------------------------------------------------------------ extra fills
    fill("MobileNet's ____ multiplier α thins the channels of every layer; compute then scales by about α².", "width",
         "The other one is the resolution multiplier.",
         "Width multiplier α (e.g. 0.75, 0.5, 0.35) scales input and output channels, so the dominant pointwise cost scales by α². The resolution multiplier ρ shrinks the input image and scales cost by ρ². Both trade accuracy for a smaller, faster model.",
         topic="mobilenet", level=2),
    fill("Hardware-aware NAS often predicts a candidate's on-device latency by summing per-block timings stored in a latency ____ table.", "lookup",
         "Measure each block once, reuse many times.",
         "Each candidate block (e.g. MBConv, expansion 6, kernel 3) is timed once on the target device. A network's latency is then estimated as the sum of its blocks' entries, so thousands of candidates can be scored without deploying them.",
         topic="nas", level=2),
    fill("In TVM, the hardware you compile for is given as the ____, e.g. \"llvm -mtriple=aarch64-linux-gnu\" for a 64-bit ARM board. (one word)", "target",
         "The thing you aim the compiler at.",
         "relay.build(mod, target=...) produces a library for exactly that target. Another device (a Jetson GPU via 'cuda', or an MCU via microTVM) needs its own build, and auto-tuning logs are per target too.",
         topic="compilers", level=2),
    fill("Asymmetric 8-bit quantization maps [min, max] onto qmax − qmin = ____ integer steps (a number).", "255",
         "int8 runs from -128 to 127.",
         "127 − (−128) = 255 steps (256 levels), so scale = (max − min) / 255. Symmetric INT8 weights in TFLite use −127..127, i.e. 254 steps, so the range is exactly balanced around zero.",
         topic="quant-math", level=2),
    # ---- top-up 19-Nov-2026: Webinar Experiment 1 (edge vs cloud)
    mcq("In the webinar, the converter is given `converter.optimizations = [tf.lite.Optimize.DEFAULT]` and no representative dataset. What kind of quantization does that produce?",
        ["Dynamic-range quantization: weights stored as int8, activations kept in float",
         "Full-integer quantization: weights and activations int8",
         "Float16 quantization of all weights",
         "No quantization; DEFAULT only removes unused ops"], 0,
        "Without sample inputs, the converter cannot learn activation ranges.",
        "Optimize.DEFAULT on its own quantizes the weights, whose ranges are known from the weights themselves. Activation ranges depend on real inputs, so full int8 needs a representative_dataset as well. Float16 needs target_spec.supported_types = [tf.float16].",
        topic="quant-ptq-qat", level=1),
    tf("Dynamic-range quantization, as used in the webinar, needs no calibration data: the converter only needs the trained model.", True,
       "Which tensors does it quantize ahead of time?",
       "Only weights are quantized at conversion time, and their min/max are read straight from the weights. That makes it the easiest PTQ mode to try first, which is why the notebook uses it. Full-integer PTQ is the mode that needs calibration samples.",
       topic="quant-ptq-qat", level=1),
    fill("The webinar's first layer is Conv2D with 8 filters of 3x3 on a 1-channel image. Its parameter count, (3·3·1 + 1)·8, is ____.", "80",
         "Each filter has 9 weights plus 1 bias.",
         "3 x 3 x 1 = 9 weights + 1 bias = 10 per filter, x 8 filters = 80, matching model.summary(). Forgetting the bias gives 72, a common exam slip.",
         topic="opt-metrics", level=1),
    mcq("Where do about 99% of the webinar CNN's 50,618 parameters sit?",
        ["In the first Dense layer: Flatten turns the 14x14x8 feature map into 1,568 inputs, each connected to 32 units (50,208 params)",
         "In the Conv2D layer, because convolutions are the expensive part",
         "In the MaxPooling layer",
         "In the final Dense(10) softmax layer"], 0,
        "Count inputs x outputs for each Dense layer.",
        "Conv2D shares a 3x3 kernel across the image (80 params); pooling and Flatten have none; Dense(10) has 330. Flatten -> Dense multiplies the whole feature map by the layer width. So to shrink a small CNN, shrink what reaches Flatten (more pooling, global average pooling) instead of trimming conv filters.",
        diagram="""
Conv2D 8x3x3      80     |
MaxPool             0     |
Flatten (1568)      0     |
Dense 32       50,208     ################## 99.2%
Dense 10          330     |
""",
        topic="compression-why", level=1),
    out("params = 50_618\nprint(round(params * 4 / 1024, 2), round(params / 1024, 2))   # KB at FP32, at INT8",
        ["197.73 49.43", "202.47 50.62", "197.73 24.72", "49.43 197.73"], 0,
        "FP32 = 4 bytes per weight, INT8 = 1 byte; 1 KB = 1024 bytes here.",
        "50,618 x 4 B = 197.73 KB, the figure model.summary() printed. At 1 byte per weight the weights need 49.43 KB, so int8 alone is a 4x cut. The real .tflite was 54.65 KB: the extra ~5 KB is graph structure, quantization scales and float biases. Dividing by 1000 instead of 1024 gives the 202.47 option.",
        question="The webinar model's weights at FP32 and at INT8. What does this print?",
        topic="opt-metrics", level=1),
    out("conv = (3 * 3 * 1 + 1) * 8        # 'same' padding keeps 28x28x8\nflat = 14 * 14 * 8                # after MaxPool(2)\nd1 = flat * 32 + 32\nd2 = 32 * 10 + 10\nprint(conv, flat, d1, d2, conv + d1 + d2)",
        ["80 1568 50208 330 50618", "72 1568 50176 320 50568", "80 6272 200736 330 201146", "80 1568 50208 330 50618.0"], 0,
        "Each Dense layer: inputs x units + one bias per unit.",
        "These are the exact numbers in the webinar's model.summary(). The trap option without biases gives 50,568; forgetting the MaxPool (28 x 28 x 8 = 6,272 inputs) quadruples the Dense layer to ~200k parameters. One pooling layer cut the model 4x before any quantization.",
        question="Parameter count of the webinar CNN, layer by layer. What does this print?",
        topic="opt-metrics", level=2),
    mcq("What does 'dynamic' mean in the webinar's dynamic-range quantization?",
        ["Activation ranges are not fixed at conversion; where a kernel supports it, activations are quantized on the fly from their range in each inference, while the int8 weights are fixed in the file",
         "The weights are re-quantized every time the model is loaded",
         "The model switches between FP32 and INT8 depending on the battery level",
         "The quantization scale is learned during training"], 0,
        "What is known at conversion time and what is only known at run time?",
        "Weights are fixed, so their int8 scales are computed once. Activations depend on the input, so the runtime either computes in float (dequantizing weights) or measures each activation's range during the inference and quantizes it then. No calibration is needed, but this per-inference work is why full int8 is usually faster on integer hardware.",
        topic="quant-math", level=2),
    tf("The webinar's '11.39x compression ratio' (622.59 KB .keras -> 54.65 KB .tflite) is the size reduction produced by int8 quantization.", False,
       "What is the most that 32-bit -> 8-bit can give?",
       "Going from 4 bytes to 1 byte per weight is at most 4x. The rest is a file-format effect: the .keras file also stores the Adam optimizer's two moment tensors per weight plus metadata, and the .tflite drops them. Quoting 11x as 'what quantization does' is the slip to avoid in an exam answer.",
       topic="compression-why", level=2),
    mcq("The webinar's .keras file is 622.59 KB, while the FP32 weights are only 197.73 KB. What fills the rest?",
        ["The optimizer state saved with the model (Adam keeps two moment tensors the size of the weights) plus the model config and metadata",
         "The MNIST training images",
         "A second copy of the model in float64",
         "The training history (loss and accuracy curves)"], 0,
        "model.save() keeps what you need to resume training.",
        "3 x 197.73 = 593.2 KB covers weights + Adam's m and v; the remaining ~29 KB is the architecture JSON and archive metadata. model.save(..., include_optimizer=False) or exporting to TFLite drops the optimizer slots, which nobody needs for inference.",
        diagram="""
.keras 622.59 KB
  weights (fp32)   197.7 |#####
  Adam m           197.7 |#####
  Adam v           197.7 |#####
  config, meta     ~29   |#
""",
        topic="compression-why", level=2),
    fill("The webinar enables quantization with `converter.optimizations = [tf.lite.Optimize.____]`.", "DEFAULT",
         "The only non-deprecated member of tf.lite.Optimize.",
         "Optimize.DEFAULT turns on the converter's size and latency optimizations, which means weight quantization. Older members (OPTIMIZE_FOR_SIZE, OPTIMIZE_FOR_LATENCY) are deprecated aliases. What you add next decides the mode: a representative_dataset for full int8, or supported_types=[tf.float16] for FP16.",
         topic="quant-ptq-qat", level=2),
    mcq("Decompose the webinar's 11.39x (622.59 KB .keras -> 54.65 KB .tflite), using the FP32 weight size of 197.73 KB as the midpoint.",
        ["About 3.15x from dropping the .keras extras (optimizer state, metadata: 622.59 -> 197.73) times about 3.62x from int8 weights plus TFLite overhead (197.73 -> 54.65)",
         "About 4x from int8 times about 2.85x from pruning",
         "All 11.39x comes from int8 quantization",
         "About 8x from int8 (32 bits -> 4 bits) times about 1.4x from metadata"], 0,
        "Two ratios that multiply to 11.39.",
        "622.59 / 197.73 = 3.15 and 197.73 / 54.65 = 3.62; 3.15 x 3.62 = 11.39. Only the second factor is quantization, and it is below the ideal 4x because the .tflite also holds the graph, scales and float biases. No pruning was done, and int8 is 8 bits, not 4.",
        diagram="""
.keras 622.59 --/3.15 (drop Adam + meta)--> 197.73 fp32
fp32   197.73 --/3.62 (int8 + tflite)----->  54.65 .tflite
              total 3.15 x 3.62 = 11.39
""",
        topic="compression-why", level=3),
    mcq("The webinar suggests trying full-integer quantization next. Which converter set-up does that need, on top of Optimize.DEFAULT?",
        ["A representative_dataset generator yielding ~100-500 real training images shaped [1, 28, 28, 1] float32, supported_ops = [TFLITE_BUILTINS_INT8], and optionally inference_input_type / inference_output_type = tf.int8",
         "Nothing more: Optimize.DEFAULT already gives full int8",
         "A representative dataset of the 10,000 test images with their labels",
         "Set target_spec.supported_types = [tf.float16]"], 0,
        "Calibration needs inputs, not labels, and not the test set.",
        "The generator lets the converter observe activation ranges; TFLITE_BUILTINS_INT8 makes conversion fail loudly if an op cannot be int8. Using the test set for calibration leaks it into the model-building process, and labels are never used. Float16 is a different mode that halves size and keeps float maths.",
        code="def rep_data():\n    for img in x_train[:200]:\n        yield [img[None].astype('float32')]\nconverter.optimizations = [tf.lite.Optimize.DEFAULT]\nconverter.representative_dataset = rep_data\nconverter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]",
        lang="text",
        topic="quant-ptq-qat", level=3),
    tf("Since the .tflite model predicted 7 with confidence 0.99985 on the saved test image, its test accuracy can be reported as the Keras model's 98.05%.", False,
       "One image or 10,000?",
       "One confident correct prediction is a smoke test, not an accuracy measurement. The webinar never ran the .tflite on the test set, so the quantized accuracy is unknown. The fix is a loop over all 10,000 x_test images through the interpreter, comparing argmax with y_test, and reporting the drop next to the size gain.",
       topic="opt-metrics", level=3),
    out("def total(side, filters):        # side = feature-map width after pooling\n    conv = (3 * 3 * 1 + 1) * filters\n    dense1 = side * side * filters * 32 + 32\n    return conv + dense1 + (32 * 10 + 10)\nprint(total(14, 8), total(7, 8), total(14, 16))",
        ["50618 12986 100874", "50618 25298 100874", "50618 12986 50778", "50618 12986 101168"], 0,
        "Dense1's input is side x side x filters.",
        "The webinar's model is total(14, 8). Adding a second MaxPool (7x7) quarters the Flatten size and cuts the model to ~13k parameters, a 3.9x shrink before any quantization. Doubling the conv filters doubles the Dense layer instead. Architecture changes at the Flatten boundary beat trimming the conv layer.",
        question="How the webinar CNN's size reacts to two design changes. What does this print?",
        topic="compression-why", level=3),
    fill("TFLite's int8 scheme quantizes Conv2D weights per output channel. The webinar's Conv2D (8 filters, 3x3) therefore gets ____ weight scales (a number).", "8",
         "One scale per filter.",
         "Per-channel (per-axis) quantization gives each output channel its own scale (and zero point 0 for weights), so a filter with small weights is not crushed by a neighbour with large ones. 8 filters -> 8 scales; per-tensor would use 1 for the whole layer.",
         topic="quant-math", level=3),
    out("keras_kb, tflite_kb, params = 622.59, 54.65, 50_618\nfp32_kb = params * 4 / 1024\nint8_kb = params / 1024\nprint(round(keras_kb - 3 * fp32_kb, 1), round(tflite_kb - int8_kb, 1))",
        ["29.4 5.2", "424.9 5.2", "29.4 -143.1", "227.1 5.2"], 0,
        "Adam: weights + m + v = 3 copies.",
        "Taking weights and both Adam slots out of the .keras leaves ~29 KB of config and archive overhead; taking the int8 weights out of the .tflite leaves ~5 KB of FlatBuffer graph, per-channel scales and float biases. So both files are explained by their tensors. Subtracting only one FP32 copy (424.9) is the mistake that makes '11x from quantization' look plausible.",
        question="What is left in each file after the tensors are accounted for (KB)? What does this print?",
        topic="compression-why", level=4),
    mcq("You want a ratio that isolates what dynamic-range quantization did to the webinar's model. Which baseline should the 54.65 KB .tflite be compared with?",
        ["A float32 .tflite of the same model converted without optimizations (roughly 200 KB), giving about 3.6x",
         "The .keras file saved after training, as the notebook did",
         "The 'Total params' count x 1 byte",
         "The dynamic-range .tflite compressed with gzip"], 0,
        "Change one thing at a time: same format, different precision.",
        "Same converter, same format, only the precision differs, so the ratio is purely quantization. The .keras baseline mixes in the optimizer state; params x 1 byte is the int8 size itself, not a baseline; gzip measures a different thing again. The same rule applies to latency: compare float .tflite vs int8 .tflite on the same device.",
        analogy="Like measuring a code change's speed-up: you compare the same build with and without the change, not a debug build against a release build.",
        topic="opt-metrics", level=4),
    tf("Switching the webinar's model from dynamic-range to full-integer quantization would make the .tflite file about 4x smaller again.", False,
       "What is still 32-bit in the dynamic-range file?",
       "Weights are already int8 in the dynamic-range file. Full int8 adds activation scales and zero points, and makes biases int32, so the file stays roughly the same size. Its gains are at run time: integer-only kernels, int8 activations (less RAM traffic), and compatibility with integer-only accelerators such as the Edge TPU and many NPUs.",
       topic="quant-ptq-qat", level=4),
    out("import numpy as np\nw = np.array([0.31, -0.12, 0.05, -0.27, 0.0])      # one weight row\ns = np.abs(w).max() / 127                           # symmetric int8\nq = np.round(w / s).astype(np.int8)\nerr = np.abs(q * s - w).max()\nprint(q.tolist(), round(float(s), 5), round(float(err), 5), bool(err <= s / 2))",
        ["[127, -49, 20, -111, 0] 0.00244 0.00118 True", "[127, -49, 21, -111, 0] 0.00244 0.00118 True", "[127, -49, 20, -111, 0] 0.00122 0.00118 True", "[255, -98, 41, -221, 0] 0.00122 0.00059 True"], 0,
        "scale = max|w| / 127; rounding error is at most half a step.",
        "This is how the webinar's int8 weights are stored: zero point 0, one scale per tensor or channel. The largest weight maps to 127, 0.0 stays exactly 0, and every weight is off by at most scale/2 (here 0.00118 for 0.05). The 255 option uses an unsigned range that symmetric int8 cannot hold.",
        question="Symmetric int8 quantization of one weight row. What does this print?",
        topic="quant-math", level=4),
    mcq("A project report says: 'After quantizing to TFLite, inference became 67x faster (5.30 ms -> 0.079 ms).' What is wrong with that claim?",
        ["Both numbers come from the same .tflite file: 5.30 ms is the HTTP + JSON round trip to a local server, 0.079 ms is the in-process call, so the 67x measures transport, not quantization",
         "Nothing: quantization usually gives a 67x speed-up",
         "The numbers are swapped: the cloud was faster",
         "The 67x is right but should be 11.39x, the compression ratio"], 0,
        "Which model did each path run?",
        "To measure what quantization did to latency, time a float32 .tflite and the int8 .tflite with the same in-process loop on the target device. Size, speed and transport are three different ratios; mixing them up gives headline numbers that do not survive review.",
        topic="opt-metrics", level=4),
]
