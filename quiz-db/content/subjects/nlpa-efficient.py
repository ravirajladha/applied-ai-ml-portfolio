from helpers import mcq, tf, out, fill

SUBJECT = "nlpa-efficient"

TOPICS = [
    ("need-efficiency", "Why efficiency is a product requirement"),
    ("data-pipelines", "Scalable data pipelines and training cost"),
    ("quantization", "Quantization of NLP models"),
    ("pruning", "Pruning weights and attention heads"),
    ("distillation", "Knowledge distillation (DistilBERT, TinyBERT)"),
    ("low-rank", "Low-rank factorisation"),
    ("efficient-arch", "Efficient architectures (ALBERT, MobileBERT, MoE, efficient attention)"),
    ("inference-opt", "Inference optimisation for BERT-style models"),
    ("deployment-scale", "Deployment and serving at scale"),
]

QUESTIONS = [
    # ------------------------------------------------------------------ L1
    mcq("The Session 15 deck says efficiency is 'a product requirement, not an afterthought'. Which is NOT one of the reasons it gives?",
        ["Smaller models always give higher accuracy than large ones",
         "Extra latency measurably reduces how much people use a product",
         "Serving compute over a model's lifetime can exceed its one-time training cost",
         "Cheaper models let organisations without hyperscale budgets deploy NLP"], 0,
        "Three are on the slide; one is simply false.",
        "The slide lists latency and UX (400 ms slower search results cut searches), serving cost, environmental footprint and access and equity. Compression usually costs a little accuracy; it does not raise it.",
        topic="need-efficiency", level=1,
        analogy="Like page-load time on a website: every extra 100 ms loses users, so performance is a feature, not polish."),
    tf("According to the course, the inference (serving) compute a popular model uses across millions of users can exceed the one-time cost of training it.", True,
       "Training happens once; serving runs every day.",
       "Training is a one-off bill. Serving runs continuously for every request, so over a model's lifetime it can cost more. That is why the course says the biggest real-world wins now come from inference serving.",
       topic="need-efficiency", level=1),
    mcq("What is deduplication in a training-data pipeline?",
        ["Removing exact and near-duplicate documents before training",
         "Copying each document twice so the model sees it more",
         "Splitting documents into sentences",
         "Translating documents into one language"], 0,
        "The name says it.",
        "Web crawls repeat the same text many times (boilerplate, mirrors, reposts). Lee et al. (2022) showed removing duplicates cuts training compute while keeping or improving quality.",
        topic="data-pipelines", level=1,
        analogy="Like de-duplicating rows before a big batch job: you stop paying to process the same record ten times."),
    fill("The course's rough training-compute formula is C ≈ ____ × parameters × tokens (a number).", "6",
         "Forward pass ~2, backward pass ~4 FLOPs per parameter per token.",
         "C ≈ 6ND: about 2 FLOPs per parameter per token for the forward pass and 4 for the backward pass. Every end-sem Q5 on training cost starts from it.",
         topic="data-pipelines", level=1),
    mcq("What does quantizing a BERT model from FP32 to INT8 do?",
        ["Stores each weight in 1 byte instead of 4, so the model is about 4x smaller",
         "Removes half of the layers",
         "Trains a new smaller model to copy the old one",
         "Shortens the input sentences"], 0,
        "Precision, not structure.",
        "Quantization lowers numeric precision: FP32 = 4 bytes, FP16 = 2, INT8 = 1, INT4 = 0.5 bytes per parameter. The architecture is unchanged. Removing layers is pruning; training a copy is distillation.",
        topic="quantization", level=1,
        diagram="""
bytes per parameter
FP32 |#### 4
FP16 |##   2
INT8 |#    1
INT4 |.    0.5
"""),
    fill("At INT8 precision each parameter takes ____ byte(s) (a number).", "1",
         "8 bits.",
         "8 bits = 1 byte. A 340M-parameter BERT-large is ~1.36 GB in FP32 and ~0.34 GB in INT8.",
         topic="quantization", level=1),
    mcq("What is pruning?",
        ["Removing weights, neurons or attention heads that contribute little to the output",
         "Lowering the precision of every weight",
         "Training a small student on a teacher's outputs",
         "Cutting long documents into chunks"], 0,
        "Like trimming a tree.",
        "Pruning deletes parts of the network that matter least. The course's table: 30-60% fewer parameters at similar accuracy. It is one of the three core ways to shrink a model, with quantization and distillation.",
        diagram="""
before:  w1 --0.80-- o     after:  w1 --0.80-- o
         w2 --0.01-- o             w2          o
         w3 --0.45-- o             w3 --0.45-- o
small-magnitude connection removed
""",
        topic="pruning", level=1),
    mcq("In knowledge distillation, which model is trained?",
        ["The small student, to match the outputs of the large teacher",
         "The large teacher, to match the student",
         "Both, from scratch, on separate data",
         "Neither; distillation only deletes weights"], 0,
        "One model teaches, one learns.",
        "The teacher is already trained and frozen. The student (e.g. DistilBERT) learns to reproduce the teacher's output distribution, so it inherits most of the teacher's quality in fewer layers.",
        topic="distillation", level=1,
        diagram="""
input --> [Teacher: BERT-base, 12 layers] --> soft probs
   |                                             | match
   +----> [Student: 6 layers] ---------> probs <-+
"""),
    tf("DistilBERT, as the course describes it, is about 40% smaller and 60% faster than BERT-base while keeping about 97% of its GLUE score.", True,
       "The three headline numbers on the DistilBERT slide.",
       "Sanh et al. (2019): 6 layers instead of 12, ~66M vs ~110M parameters. Teams could swap it in and roughly halve inference cost without changing their serving stack.",
       topic="distillation", level=1),
    mcq("Low-rank factorisation replaces one big weight matrix W with:",
        ["Two thinner matrices whose product approximates W",
         "A copy of W stored in INT8",
         "W with half its rows deleted",
         "The average of W's columns"], 0,
        "m×n ≈ (m×r)(r×n).",
        "If W is m×n, write W ≈ A·B with A (m×r) and B (r×n). For small r this needs r(m+n) numbers instead of m·n. ALBERT uses the same idea for its embedding matrix.",
        analogy="Like storing a times table as its two short header lists and multiplying on demand, instead of storing every cell.",
        topic="low-rank", level=1),
    mcq("The course names ALBERT (2019) as an example of which efficiency idea?",
        ["Parameter sharing: the same transformer-block weights are reused at every layer",
         "Mixture-of-experts routing",
         "4-bit quantization",
         "Sliding-window attention"], 0,
        "A Lite BERT.",
        "ALBERT shares one block's parameters across all depths, cutting memory 'without cutting depth'. It also factorises the embedding matrix. MoE is the Switch Transformer / Mixtral idea; sliding-window attention is Longformer.",
        topic="efficient-arch", level=1),
    mcq("In a mixture-of-experts (MoE) transformer, what happens to each token?",
        ["A router sends it to a small subset of expert sub-networks",
         "It passes through every expert and the outputs are summed",
         "It is dropped if it is not important",
         "It is processed by a separate model per language"], 0,
        "Only part of the model 'wakes up'.",
        "Each token activates only a few experts (Mixtral: 2 of 8 per layer), so per-token compute is far below what the total parameter count suggests.",
        topic="efficient-arch", level=1,
        analogy="Like a support desk that routes each ticket to two specialists instead of copying all eight teams on every email."),
    tf("Standard self-attention cost grows with the square of the sequence length, which is why sparse and linear attention variants exist.", True,
       "Every token attends to every token.",
       "n tokens give an n×n score matrix: O(n²). Longformer and BigBird use sparse patterns; Performer and Linformer use linear-time approximations, enabling longer inputs at lower cost.",
       topic="efficient-arch", level=1),
    mcq("What is batching at inference time?",
        ["Running several requests through the model together in one forward pass",
         "Splitting one request across many GPUs",
         "Storing answers for repeated questions",
         "Training on mini-batches"], 0,
        "Many requests, one pass.",
        "A GPU multiplies big matrices efficiently; one short sentence leaves it mostly idle. Grouping requests raises throughput (requests per second), usually at a small cost in per-request latency.",
        analogy="Like a lift carrying ten people per trip instead of one: each trip takes a bit longer, but far more people move per minute.",
        topic="inference-opt", level=1),
    mcq("Which pair correctly defines latency and throughput?",
        ["Latency = time for one request; throughput = requests completed per second",
         "Latency = requests per second; throughput = time per request",
         "Both mean the same thing",
         "Latency = model size; throughput = GPU memory"], 0,
        "One is per request, one is per second.",
        "A chatbot user feels latency; your finance team pays for throughput. Batching typically raises throughput while slightly raising latency.",
        topic="inference-opt", level=1),
    fill("The open format for exporting a trained model so it can run in an optimised runtime outside its training framework is ____ (four letters).", "ONNX",
         "Open Neural Network Exchange.",
         "The deck lists TensorRT, ONNX Runtime and Triton as the serving frameworks that 'optimise the serving path end-to-end'. Exporting BERT to ONNX lets ONNX Runtime fuse operations and run fast on CPU or GPU.",
         topic="inference-opt", level=1),
    mcq("A bank wants a small intent classifier to run inside its mobile app with no network connection. Which deployment pillar from the course is this?",
        ["Edge / on-device deployment with a compressed model",
         "Autoscaling infrastructure",
         "Hardware acceleration with TPUs",
         "Continuous batching on a GPU server"], 0,
        "Where does the model run?",
        "Edge deployment runs compressed models directly on devices for low latency and offline use. It needs a small model: distilled and quantized, e.g. a quantized DistilBERT or MobileBERT.",
        topic="deployment-scale", level=1),
    tf("llama.cpp, as the course describes it, runs quantized open models in plain C/C++ and can do so without a GPU.", True,
       "Laptops and phones.",
       "llama.cpp uses aggressive 4- and 8-bit quantization (the GGUF format). A 7B model at 4-bit is about 3.9 GB, so it fits comfortably on an 8 GB laptop with no CUDA.",
       topic="deployment-scale", level=1),
    mcq("What does autoscaling do for a model-serving deployment?",
        ["Adds or removes serving replicas as real-time demand rises and falls",
         "Automatically picks the best model architecture",
         "Compresses the model when traffic is high",
         "Scales the input text to a fixed length"], 0,
        "Elastic compute.",
        "Autoscaling is the fifth pillar on the deck's deployment slide: capacity follows demand, so you do not pay for peak capacity all day.",
        topic="deployment-scale", level=1),
    # ------------------------------------------------------------------ L2
    out("params = 110e6          # BERT-base\n"
        "for name, b in [('FP32', 4), ('FP16', 2), ('INT8', 1)]:\n"
        "    print(name, int(params * b / 1e6), 'MB')",
        ["FP32 440 MB\nFP16 220 MB\nINT8 110 MB",
         "FP32 110 MB\nFP16 220 MB\nINT8 440 MB",
         "FP32 440 MB\nFP16 220 MB\nINT8 55 MB",
         "FP32 3520 MB\nFP16 1760 MB\nINT8 880 MB"], 0,
        "Memory = parameters × bytes per parameter.",
        "110M × 4 B = 440 MB, × 2 = 220 MB, × 1 = 110 MB. The 3520 option multiplies by bits instead of bytes, a common slip in exam answers.",
        topic="quantization", level=2),
    out("m, n, r = 768, 768, 64\n"
        "full = m * n\n"
        "factored = m * r + r * n\n"
        "print(full, factored, round(factored / full, 3))",
        ["589824 98304 0.167", "589824 4096 0.007", "589824 49152 0.083", "1536 98304 64.0"], 0,
        "A is m×r, B is r×n.",
        "768·768 = 589,824 weights; 768·64 + 64·768 = 98,304, about 1/6 of the original. Whether accuracy survives depends on how much of W's energy lives in its top 64 singular values.",
        topic="low-rank", level=2,
        diagram="""
 W (768x768)    ~   A (768x64)  x  B (64x768)
 [##########]       [##]           [##########]
 [##########]       [##]
 589,824            49,152    +    49,152
"""),
    out("import numpy as np\n"
        "z = np.array([4.0, 2.0, 0.0])      # teacher logits\n"
        "for T in (1, 4):\n"
        "    p = np.exp(z / T) / np.exp(z / T).sum()\n"
        "    print(T, np.round(p, 3).tolist())",
        ["1 [0.867, 0.117, 0.016]\n4 [0.506, 0.307, 0.186]",
         "1 [0.506, 0.307, 0.186]\n4 [0.867, 0.117, 0.016]",
         "1 [0.867, 0.117, 0.016]\n4 [0.973, 0.026, 0.001]",
         "1 [0.667, 0.333, 0.0]\n4 [0.667, 0.333, 0.0]"], 0,
        "Dividing logits by T > 1 flattens the softmax.",
        "At T = 1 the teacher is nearly one-hot; at T = 4 the wrong classes get visible probability. Those relative probabilities ('class 2 is more plausible than class 3') are the dark knowledge the student learns from soft targets.",
        topic="distillation", level=2),
    mcq("Why does distillation use the teacher's soft probabilities instead of only the hard gold labels?",
        ["Soft targets carry how similar the wrong classes are to the right one, giving the student far more signal per example",
         "Soft targets are cheaper to store than labels",
         "Hard labels cannot be used with neural networks",
         "Soft targets make the student larger"], 0,
        "What does a 0.30 on a wrong class tell you?",
        "A hard label says only 'positive'. The teacher's softened distribution says 'positive, a bit neutral, not negative': information about the similarity structure of the task. Hinton et al. called it dark knowledge.",
        analogy="Like a senior reviewer who says not just 'B is right' but 'C was close, D is nonsense': the junior learns far more per review.",
        topic="distillation", level=2),
    mcq("Mixtral 8x7B has 46.7B total parameters and about 12.9B active per token. Which number sets its GPU memory for weights, and which sets its per-token compute?",
        ["Memory: 46.7B (all experts must be loaded); compute: 12.9B",
         "Memory: 12.9B; compute: 46.7B",
         "Both follow 12.9B",
         "Both follow 46.7B"], 0,
        "Which experts must be resident, and which actually run?",
        "Any token might be routed to any expert, so all experts sit in memory. Only the 2 routed experts run per token (~28%), which is why Mixtral runs about as fast as a ~13B dense model but needs the memory of a ~47B one.",
        topic="efficient-arch", level=2,
        diagram="""
token -> router -> E1  E2  E3  E4  E5  E6  E7  E8
                   [x]          [x]
loaded in memory:  all 8 (46.7B total)
run for this token: 2   (~12.9B active)
"""),
    fill("Mixtral 8x7B routes each token to ____ of its 8 experts per layer (a number).", "2",
         "Top-k routing with a small k.",
         "Top-2 routing: 2 of 8 experts per layer, about 28% of the parameters active per token.",
         topic="efficient-arch", level=2),
    mcq("Which describes unstructured vs structured pruning correctly?",
        ["Unstructured removes individual weights anywhere; structured removes whole units such as heads, neurons or layers",
         "Unstructured removes whole layers; structured removes single weights",
         "Both remove whole layers, but structured needs retraining",
         "Structured pruning is the same as quantization"], 0,
        "Scattered zeros vs smaller shapes.",
        "Unstructured pruning leaves the matrix shapes unchanged with zeros scattered inside. Structured pruning deletes rows, columns or whole heads, so the dense matrices really get smaller.",
        topic="pruning", level=2),
    out("import numpy as np\n"
        "w = np.array([0.8, -0.05, 0.3, 0.01, -0.6, 0.02, -0.4, 0.07])\n"
        "k = len(w) // 2                     # prune 50%\n"
        "thr = np.sort(np.abs(w))[k - 1]\n"
        "w[np.abs(w) <= thr] = 0\n"
        "print(w.tolist())",
        ["[0.8, 0.0, 0.3, 0.0, -0.6, 0.0, -0.4, 0.0]",
         "[0.8, -0.05, 0.3, 0.0, -0.6, 0.0, -0.4, 0.07]",
         "[0.0, -0.05, 0.0, 0.01, 0.0, 0.02, 0.0, 0.07]",
         "[0.8, 0.0, 0.3, 0.0, 0.0, 0.0, -0.4, 0.0]"], 0,
        "Magnitude pruning keeps the largest |w|.",
        "The four smallest magnitudes (0.01, 0.02, 0.05, 0.07) are zeroed; sign does not matter, only |w|. Keeping the smallest is the reverse, and dropping -0.6 forgets the absolute value.",
        topic="pruning", level=2),
    tf("Because training compute is C ≈ 6 × parameters × tokens, cutting the training tokens in half by deduplication roughly halves the training bill for the same model.", True,
       "Compute is linear in tokens.",
       "The course's takeaway: 'compute scales linearly with tokens, doubling training data doubles the bill'. Lee et al. (2022) showed dedup keeps or improves quality, so it is a quality step and a cost step at once.",
       topic="data-pipelines", level=2),
    mcq("Why does the deck recommend streaming pipelines (WebDataset, MosaicML StreamingDataset) for large corpora?",
        ["They read sharded data in streamed batches instead of loading the whole corpus into memory",
         "They remove duplicates automatically",
         "They make the model smaller",
         "They translate data on the fly"], 0,
        "Terabytes do not fit in RAM.",
        "Shards are read sequentially from disk or object storage as training needs them, so the corpus can be far larger than memory and many workers can read in parallel.",
        topic="data-pipelines", level=2,
        analogy="Like streaming a video instead of downloading the whole file before pressing play."),
    mcq("What did Together AI's RedPajama project (2023) do, according to the deck?",
        ["Open-sourced a ~1.2-trillion-token dataset and pipeline reproducing LLaMA's data recipe, with the same dedup and quality filtering",
         "Released a 4-bit quantization format for laptops",
         "Introduced PagedAttention for serving",
         "Distilled LLaMA into a 6-layer student"], 0,
        "Reproducing LLaMA's data, not its weights.",
        "LLaMA was trained on 1.4T tokens mixed at fixed proportions (CommonCrawl ~67%, C4 15%, GitHub, Wikipedia, books, arXiv ~4.5% each). RedPajama made that recipe reproducible so smaller labs (MPT, RedPajama-INCITE) did not have to repeat costly ad hoc collection.",
        topic="data-pipelines", level=2),
    mcq("A team serves a BERT classifier and pads every batch to 512 tokens, although most inputs are 20-60 tokens. What is the simplest fix?",
        ["Dynamic padding: pad each batch only to its longest sequence (and bucket similar lengths together)",
         "Quantize the model to INT4",
         "Increase max_length to 1024",
         "Switch to a larger GPU"], 0,
        "Where is the wasted compute?",
        "Padding tokens still go through every layer, and attention cost grows with the square of length. Padding to the batch maximum, and grouping similar lengths so that maximum is small, removes most of the waste with no accuracy change.",
        diagram="""
fixed:   [tok tok PAD PAD PAD ... PAD]  -> 512
         [tok tok tok PAD PAD ... PAD]  -> 512
dynamic: [tok tok PAD]                  -> batch max
         [tok tok tok]
""",
        topic="inference-opt", level=2),
    out("lengths = [16, 30, 18, 40]\n"
        "fixed = len(lengths) * 512\n"
        "dynamic = len(lengths) * max(lengths)\n"
        "print(fixed, dynamic, round(sum(lengths) / dynamic, 2))",
        ["2048 160 0.65", "2048 104 1.0", "512 160 0.65", "2048 160 0.05"], 0,
        "Tokens processed = batch size × padded length.",
        "Fixed 512 padding processes 2,048 token positions; dynamic padding to 40 processes 160, and 104 of those 160 (65%) are real tokens. Under fixed padding only 104/2,048 ≈ 5% are real.",
        topic="inference-opt", level=2),
    out("V, H, E = 30000, 768, 128\n"
        "bert = V * H\n"
        "albert = V * E + E * H\n"
        "print(bert, albert)",
        ["23040000 3938304", "23040000 3840000", "3938304 23040000", "23040000 98304"], 0,
        "ALBERT projects a small E-dim embedding up to H.",
        "BERT's embedding is V×H = 23.04M. ALBERT's factorised embedding is V×E + E×H = 3.84M + 98,304 ≈ 3.94M. Forgetting the E×H projection gives 3,840,000.",
        diagram="""
BERT:    one-hot (V) --[V x H]--> 768
ALBERT:  one-hot (V) --[V x E]--> 128 --[E x H]--> 768
         30000 x 128 + 128 x 768  vs  30000 x 768
""",
        topic="low-rank", level=2),
    tf("Because ALBERT reuses the same weights at every layer, it needs far fewer FLOPs per input than BERT of the same depth and width.", False,
       "Sharing weights is not skipping layers.",
       "Every layer still runs its full matrix multiplies, just with the same weights. Sharing cuts parameters and memory (ALBERT-base ~12M vs BERT-base ~108M), not compute, so inference latency is about the same.",
       diagram="""
BERT:    x -> [L1] -> [L2] -> ... -> [L12]   12 weight sets
ALBERT:  x -> [ L ] -> [ L ] -> ... -> [ L ]  1 weight set
         both run 12 layers of matrix multiplies
""",
       topic="efficient-arch", level=2),
    mcq("How is the 6-layer DistilBERT student initialised before distillation?",
        ["From the 12-layer BERT-base teacher, taking one layer out of every two",
         "Randomly, with no link to the teacher",
         "From the teacher's first 6 layers only",
         "From GPT-2's layers"], 0,
        "The student and teacher have the same hidden size (768).",
        "Same width means teacher layers can be copied directly; Sanh et al. take every other layer. A good starting point is part of why the student reaches 97% of BERT's GLUE score.",
        analogy="Like a new service forked from an existing codebase by keeping every other module, then refactored, rather than written from an empty repo.",
        topic="distillation", level=2),
    mcq("Compared with DistilBERT, what extra does TinyBERT distil from the teacher?",
        ["Intermediate representations: embeddings, hidden states and attention matrices, layer by layer",
         "Nothing; it only matches the final logits",
         "The teacher's optimizer state",
         "The tokenizer vocabulary"], 0,
        "Inside the network, not just at the output.",
        "Jiao et al. (2020) add layer-to-layer losses on attention maps and hidden states (with a learned projection when widths differ), plus prediction-layer distillation, giving a 4-layer model that is much smaller and faster than BERT-base.",
        diagram="""
teacher (12 layers)      student (4 layers)
 layer 3  ----------->    layer 1   attn + hidden loss
 layer 6  ----------->    layer 2
 layer 9  ----------->    layer 3
 layer 12 ----------->    layer 4
 logits   ----------->    logits    soft-target loss
""",
        topic="distillation", level=2),
    mcq("What is the key design trick of MobileBERT?",
        ["It keeps BERT-large's depth (24 layers) but makes each layer thin with bottleneck structures, then distils layer by layer from a specially designed teacher",
         "It removes half of BERT's layers",
         "It shares one layer's weights across all layers",
         "It uses 2-bit weights"], 0,
        "Deep and thin.",
        "Sun et al. (2020): bottleneck and inverted-bottleneck blocks shrink each layer to ~25M total parameters while keeping 24 layers; it is task-agnostic (fine-tune like BERT) and aimed at phones.",
        topic="efficient-arch", level=2),
    mcq("What problem does LLM.int8() (Dettmers et al., 2022) solve when quantizing large models?",
        ["Rare high-magnitude outlier features ruin plain INT8, so it keeps those columns in FP16 and quantizes the rest",
         "It removes all attention heads",
         "It distils the model into a smaller one",
         "It shortens the context window"], 0,
        "Mixed precision.",
        "One huge value forces a large scale, which crushes all the small values to zero. Isolating outliers in FP16 lets BLOOM-176B drop from 352 GB to ~180 GB with no measurable quality loss; it ships in bitsandbytes.",
        diagram="""
X (activations) columns:  c1  c2  c3* c4
  c3* has huge values  ->  FP16 matmul
  c1, c2, c4           ->  INT8 matmul
  sum both partial results -> output
""",
        topic="quantization", level=2),
    fill("Longformer replaces full attention with a sliding-window pattern plus a few ____ attention tokens (such as [CLS]) that see every position.", "global",
         "Some tokens look at everything.",
         "Local windows make cost linear in length; global tokens keep task-level information flowing. It lets BERT-style models read thousands of tokens.",
         diagram="""
      t1 t2 t3 t4 t5 t6
 CLS   G  G  G  G  G  G   global token sees all
 t2    G  x  x  .  .  .
 t3    G  x  x  x  .  .   window of 3
 t4    G  .  x  x  x  .
""",
         topic="efficient-arch", level=2),
    out("prefill_ms, out_tokens, decode_ms = 150, 300, 15\n"
        "L = prefill_ms + out_tokens * decode_ms\n"
        "print(L, 'ms =', L / 1000, 's')",
        ["4650 ms = 4.65 s", "4500 ms = 4.5 s", "465 ms = 0.465 s", "45150 ms = 45.15 s"], 0,
        "Course formula: L = prefill + tokens × decode time.",
        "150 + 300 × 15 = 4,650 ms. Dropping the prefill gives 4,500; the course always adds it once, because the prompt is processed once before decoding starts.",
        topic="deployment-scale", level=2),
    out("import math\n"
        "L_s = 4.65            # seconds per request\n"
        "batch = 24            # requests per GPU at once\n"
        "X = batch / L_s\n"
        "G = math.ceil(30 / X) # peak demand 30 req/s\n"
        "print(round(X, 2), G)",
        ["5.16 6", "5.16 5", "111.6 1", "0.19 158"], 0,
        "X = batch ÷ L; G = demand ÷ X, rounded up.",
        "24 / 4.65 = 5.16 req/s per GPU; 30 / 5.16 = 5.81, so 6 GPUs. Rounding down to 5 leaves demand unserved. Multiplying batch × L instead of dividing gives the 111.6 nonsense.",
        analogy="Like sizing checkout counters: time per customer, customers served per counter per minute, then counters needed at the rush hour.",
        topic="deployment-scale", level=2,
        diagram="""
L = prefill + tokens x decode      (seconds/request)
X = batch / L                      (requests/s per GPU)
G = ceil(peak demand / X)          (GPUs)
"""),
    tf("The course says quantization, pruning and distillation are complementary: production pipelines often quantize a distilled or pruned model to stack the savings.", True,
       "Key takeaway 2.",
       "They act on different things: distillation and pruning reduce the number of parameters, quantization reduces bytes per parameter. A quantized DistilBERT is a standard CPU deployment.",
       topic="need-efficiency", level=2),
    mcq("Which goal-to-technique match is best?",
        ["Cut GPU memory for weights fast with no retraining: post-training quantization",
         "Cut GPU memory for weights fast with no retraining: train a new distilled student",
         "Handle 16k-token documents in a BERT-style encoder: INT8 quantization",
         "Lower per-token compute of a huge model: cross-layer parameter sharing"], 0,
        "Which one needs no training at all?",
        "PTQ just converts the existing weights. Distillation needs a training run. Long inputs need sparse/linear attention (Longformer, BigBird). Sharing cuts parameters, not compute; MoE is the per-token compute lever.",
        topic="need-efficiency", level=2),
    mcq("Your BERT classifier serves 5 requests per minute from an internal tool. Which deployment is most sensible?",
        ["A quantized model on CPU: the load is tiny, so a GPU would sit idle while still billing",
         "A dedicated multi-GPU cluster with tensor parallelism",
         "TPU pods with autoscaling",
         "Continuous batching across 8 GPUs"], 0,
        "Utilisation drives cost.",
        "GPUs pay off when there is enough concurrent work to batch. A ~66-110M parameter encoder at low traffic runs fine on CPU, especially after INT8 dynamic quantization and ONNX Runtime export.",
        topic="inference-opt", level=2),
    # ------------------------------------------------------------------ L3
    out("C = 6 * 13e9 * 260e9          # 13B params, 260B tokens\n"
        "eff = 400e12 * 0.35            # 400 TFLOP/s at 35% MFU\n"
        "H = C / eff / 3600             # GPU-hours\n"
        "print(f\"{C:.3e}\", round(H), round(H * 2.5))   # $2.50 / GPU-hr",
        ["2.028e+22 40238 100595", "2.028e+22 14083 35208", "3.380e+21 6706 16766", "2.028e+22 40238 40238"], 0,
        "Step 1 C = 6ND; step 2 divide by effective FLOP/s and 3600; step 3 multiply by the rate.",
        "C = 6 × 13e9 × 260e9 = 2.028e22 FLOPs. Effective throughput 400 × 0.35 = 140 TFLOP/s, so H = 2.028e22 / 1.4e14 / 3600 ≈ 40,238 GPU-hours, ≈ $100,595. Using peak FLOP/s without MFU gives 14,083 hours: the most common exam slip.",
        topic="data-pipelines", level=3,
        diagram="""
STEP 1  C = 6 x params x tokens          FLOPs
STEP 2  H = C / (peak x MFU) / 3600       GPU-hours
STEP 3  $ = H x price per GPU-hour
"""),
    mcq("Same 13B / 260B-token plan (~40,238 GPU-hours, ~$100.6k). Deduplication removes 40% of the tokens with no quality loss. What is the new cost?",
        ["About $60.4k: compute is linear in tokens, so cost falls by 40%",
         "About $40.2k: cost falls by 60%",
         "About $100.6k: dedup changes quality, not cost",
         "About $36.2k: cost falls with the square of tokens"], 0,
        "C ∝ tokens.",
        "Tokens 260B -> 156B, so C, H and cost all scale by 0.6: ~24,143 GPU-hours, ~$60.4k, a 40% saving. The end-sem asks exactly this 'new cost and % saved' step.",
        topic="data-pipelines", level=3),
    fill("A plan needs 40,238 GPU-hours and must finish in 14 days of wall-clock time. The minimum number of GPUs running in parallel is ____.", "120",
         "GPUs = GPU-hours ÷ (days × 24), rounded up.",
         "14 × 24 = 336 hours; 40,238 / 336 = 119.76, rounded up to 120. Rounding down to 119 misses the deadline by a few hours.",
         topic="data-pipelines", level=3),
    out("import math\n"
        "params = 65e9\n"
        "for name, b in [('FP16', 2), ('INT8', 1), ('INT4', 0.5)]:\n"
        "    gb = params * b / 1e9\n"
        "    print(name, gb, math.ceil(gb / 80))   # 80 GB GPUs",
        ["FP16 130.0 2\nINT8 65.0 1\nINT4 32.5 1",
         "FP16 130.0 1\nINT8 65.0 0\nINT4 32.5 0",
         "FP16 260.0 4\nINT8 130.0 2\nINT4 65.0 1",
         "FP16 130.0 2\nINT8 65.0 1\nINT4 32.5 0.5"], 0,
        "Bytes per parameter, then ceil.",
        "65B × 2 B = 130 GB -> ceil(1.625) = 2 GPUs; INT8 65 GB -> 1; INT4 32.5 GB -> 1. Plain floor division gives 1 / 0 / 0 GPUs, which cannot host anything. The 260 GB row uses 4 bytes (FP32).",
        topic="quantization", level=3),
    mcq("An exam answer says: 'A 90B model in FP16 needs 180 GB, so 180 / 80 = 2.25, therefore 2 GPUs of 80 GB.' What is wrong?",
        ["GPU counts must be rounded up: 2 GPUs hold only 160 GB, so 3 are needed",
         "FP16 uses 4 bytes per parameter, so it is 360 GB",
         "Nothing: 2.25 rounds to 2",
         "It should divide by 40 GB, not 80"], 0,
        "Can 0.25 of a GPU be skipped?",
        "Weights that do not fit do not run. Always round up (and in practice leave headroom for the KV cache and activations, which push the real number even higher).",
        topic="quantization", level=3),
    out("import numpy as np\n"
        "w = np.array([0.02, -0.03, 0.05, 8.0])     # one outlier\n"
        "s = np.abs(w).max() / 127                  # absmax INT8 scale\n"
        "q = np.round(w / s).astype(int)\n"
        "print(q.tolist(), round(s, 4))",
        ["[0, 0, 1, 127] 0.063", "[51, -76, 127, 127] 0.063", "[0, 0, 0, 127] 8.0", "[2, -3, 5, 127] 0.063"], 0,
        "The outlier sets the scale for everyone.",
        "s = 8 / 127 ≈ 0.063, so 0.02 and -0.03 round to 0 and 0.05 to 1: the small weights are wiped out. Without the outlier the same three would map to [51, -76, 127]. LLM.int8() keeps outlier features in FP16 for exactly this reason.",
        topic="quantization", level=3),
    out("import torch, torch.nn as nn\n"
        "torch.manual_seed(0)\n"
        "m = nn.Sequential(nn.Embedding(100, 16), nn.Linear(16, 16), nn.ReLU(), nn.Linear(16, 2))\n"
        "q = torch.ao.quantization.quantize_dynamic(m, {nn.Linear}, dtype=torch.qint8)\n"
        "print(q[1].weight().dtype, q[0].weight.dtype)",
        ["torch.qint8 torch.float32", "torch.qint8 torch.qint8", "torch.float32 torch.float32", "torch.float32 torch.qint8"], 0,
        "Which module types did you ask it to quantize?",
        "quantize_dynamic swaps only the listed types (nn.Linear) for dynamic-quantized versions with INT8 weights; activations are quantized on the fly at run time. The Embedding stays FP32. This is the classic one-line CPU speed-up for BERT, whose FLOPs are almost all in Linear layers.",
        topic="quantization", level=3),
    mcq("A team prunes 50% of BERT-base's individual weights by magnitude and sees almost no latency change on GPU. Why?",
        ["Unstructured sparsity leaves the dense matrix shapes unchanged; standard GPU kernels still multiply the zeros",
         "Pruning only works on CPU",
         "50% is too little; pruning helps only above 99%",
         "The pruned weights grow back during inference"], 0,
        "Did any matrix get smaller?",
        "Scattered zeros save storage (if stored sparsely) but dense GEMMs do the same work. Real speed needs structured pruning (whole heads, FFN neurons, layers) or hardware/kernels built for specific sparsity patterns (e.g. 2:4 on recent GPUs).",
        analogy="Like blanking cells in a spreadsheet versus deleting whole columns: only deleting columns makes the sheet faster to process.",
        topic="pruning", level=3,
        diagram="""
unstructured           structured (drop a head)
[w 0 w 0]              [w w]
[0 w 0 w]  same shape  [w w]  smaller shape
[w 0 0 w]  same FLOPs  [w w]  fewer FLOPs
"""),
    mcq("Michel et al. (2019), 'Are Sixteen Heads Really Better than One?', found what about BERT's attention heads?",
        ["Many heads can be removed at test time with little loss; some layers work with a single head",
         "Every head is essential; removing any one breaks the model",
         "Adding more heads always improves accuracy",
         "Heads can be pruned only before pre-training"], 0,
        "Redundancy.",
        "Heads are highly redundant, which is what the course's 'remove redundant weights or attention heads' row refers to. Head pruning is structured: it shrinks the Q, K, V and output projections, so it gives real speed-ups.",
        topic="pruning", level=3),
    mcq("A team reports: 'We switched from BERT-base to ALBERT-base, parameters fell from ~108M to ~12M, but latency is unchanged.' What is the best explanation?",
        ["Cross-layer sharing reuses one block's weights at all 12 layers; all 12 layers still run, so FLOPs are about the same",
         "ALBERT uses INT8 internally, which is slow on GPU",
         "Their benchmark is wrong; ALBERT-base is 9x faster",
         "ALBERT has more attention heads"], 0,
        "Parameters vs computation.",
        "ALBERT saves memory, download size and communication in distributed training. Latency follows compute, which sharing does not cut. For speed, use distillation (fewer layers), structured pruning or quantization.",
        topic="efficient-arch", level=3,
        analogy="Like calling the same function 12 times in a loop: the code is stored once, but the CPU still runs it 12 times."),
    out("import numpy as np\n"
        "rng = np.random.default_rng(0)\n"
        "W = rng.normal(size=(6, 2)) @ rng.normal(size=(2, 5))   # a rank-2 matrix\n"
        "U, S, Vt = np.linalg.svd(W, full_matrices=False)\n"
        "r = 2\n"
        "W_r = (U[:, :r] * S[:r]) @ Vt[:r]\n"
        "print(np.round(S, 3).tolist()[2:], round(float(np.abs(W - W_r).max()), 6), 6 * 5, r * (6 + 5))",
        ["[0.0, 0.0, 0.0] 0.0 30 22", "[0.0, 0.0, 0.0] 0.0 30 60", "[1.0, 1.0, 1.0] 0.5 30 22", "[0.0, 0.0] 0.0 30 10"], 0,
        "A rank-2 matrix has only 2 non-zero singular values.",
        "Truncated SVD keeps the top r singular values: W ≈ (U_r S_r) V_rᵀ, stored as a 6×2 and a 2×5 matrix = 22 numbers instead of 30, with zero error here because W really is rank 2. Real weight matrices are only approximately low rank, so the error depends on the discarded singular values.",
        topic="low-rank", level=3),
    mcq("A tokenizer change makes the average input 30% shorter (in tokens) for the same text. Roughly how much does the self-attention score computation shrink?",
        ["About 51%, because attention is O(n²): 0.7² ≈ 0.49 of the original",
         "About 30%, the same as the length",
         "About 9%",
         "Not at all; tokenization does not affect the model"], 0,
        "Square the ratio.",
        "The deck lists efficient tokenization as an efficient-by-default design: fewer tokens directly lower attention compute. Feed-forward cost falls linearly (30%), the n² attention part by ~51%.",
        topic="efficient-arch", level=3),
    mcq("DistilBERT's training loss combines which three terms?",
        ["Soft-target distillation loss (with temperature), masked-language-modelling loss, and a cosine loss aligning student and teacher hidden states",
         "Cross-entropy on GLUE labels, L2 weight decay, and a pruning penalty",
         "Next-sentence prediction, sentence-order prediction and MLM",
         "Only KL divergence on the final logits"], 0,
        "Sanh et al.'s 'triple loss'.",
        "L = distillation (KL on softened teacher vs student MLM distributions) + MLM (the student's own masked-token loss) + cosine embedding loss (align hidden-state directions). NSP was dropped, as in RoBERTa.",
        topic="distillation", level=3),
    tf("DistilBERT was distilled during pre-training, giving a general-purpose (task-agnostic) model that teams then fine-tune on their own task like BERT.", True,
       "The slide says 'during pre-training, rather than only fine-tuning separately'.",
       "That is why it became a drop-in replacement: teams kept their fine-tuning code and task heads. Task-specific distillation (as in TinyBERT's second stage) distils again on the task data.",
       topic="distillation", level=3),
    fill("Mixtral 8x7B has 46.7B total parameters. In FP16, the minimum number of 80 GB GPUs just to hold its weights is ____.", "2",
         "Memory follows TOTAL parameters.",
         "46.7B × 2 B = 93.4 GB > 80 GB, so 2 GPUs. Sizing by the 12.9B active parameters (25.8 GB, 1 GPU) is the classic MoE mistake: inactive experts still have to be resident.",
         topic="efficient-arch", level=3),
    out("import math\n"
        "for decode_ms in (16, 8):                 # 8 = after speculative decoding\n"
        "    L = 200 + 250 * decode_ms             # prefill 200 ms, 250 output tokens\n"
        "    X = 32 / (L / 1000)                   # batch capacity 32\n"
        "    print(L, round(X, 2), math.ceil(45 / X))   # peak 45 req/s",
        ["4200 7.62 6\n2200 14.55 4", "4200 7.62 5\n2200 14.55 3", "4000 8.0 6\n2000 16.0 3", "4200 7.62 6\n2200 14.55 3"], 0,
        "Recompute L, then X, then G, rounding G up each time.",
        "4,200 ms -> 7.62 req/s -> ceil(5.9) = 6 GPUs. Halving decode gives 2,200 ms -> 14.55 req/s -> ceil(3.09) = 4 GPUs: a 33% fleet reduction. Not 50%, because the 200 ms prefill does not shrink.",
        topic="deployment-scale", level=3),
    tf("In the course's latency model, halving the decode time per token exactly doubles throughput per GPU.", False,
       "L = prefill + tokens × decode.",
       "Only the decode part halves; prefill stays. The course itself says halving decode 'nearly doubles' throughput. With long outputs the effect is close to 2x, with long prompts and short outputs much less.",
       topic="deployment-scale", level=3),
    mcq("Besides saving compute, what else did Lee et al. (2022) report deduplication does?",
        ["Reduces memorised (verbatim) output and train-test overlap, while keeping or improving quality",
         "Makes the model use INT8 weights",
         "Increases the vocabulary size",
         "Removes the need for quality filtering"], 0,
        "Repeated text gets memorised.",
        "Text seen many times gets regurgitated verbatim and leaks into validation sets, inflating scores. Dedup is complementary to quality filtering (CCNet, Gopher rules), which removes low-value text rather than repeats.",
        topic="data-pipelines", level=3),
    mcq("A team enables 'KV caching' to speed up a BERT-base sentiment classifier that reads each review once and outputs a label. Why will it barely help?",
        ["The KV cache saves recomputation across autoregressive decoding steps; an encoder classifier makes one forward pass per input",
         "BERT has no attention layers",
         "KV caching only works in INT4",
         "It will help a lot; KV caching halves every model's latency"], 0,
        "Where is there repeated work to save?",
        "In a decoder generating tokens, every step would recompute keys/values of the earlier tokens; caching avoids that. An encoder classifier has no steps. For it, useful caches are at the application level (cache labels or embeddings of repeated inputs).",
        topic="inference-opt", level=3),
    mcq("What does exporting a fine-tuned BERT to ONNX Runtime (or TensorRT) typically do to speed it up?",
        ["Graph optimisations such as fusing operators (e.g. attention, GELU, LayerNorm), constant folding and hardware-specific kernels, often with FP16/INT8",
         "It retrains the model with fewer layers",
         "It removes the tokenizer",
         "It changes the model's predictions to a simpler rule set"], 0,
        "Same maths, fewer and faster kernel launches.",
        "The exported static graph lets the runtime merge many small ops into fused kernels and pick optimised implementations. Outputs should match closely; check a sample after export, as tiny numeric differences can flip borderline predictions.",
        analogy="Like compiling and minifying a JavaScript bundle: same behaviour, fewer and faster operations at run time.",
        topic="inference-opt", level=3),
    mcq("Which pairing of efficient-attention method and idea is right?",
        ["Longformer: sliding window + global tokens; Linformer: project keys/values to a short fixed length (low rank); Performer: kernel approximation of softmax",
         "Longformer: kernel approximation; Linformer: sliding window; Performer: global tokens",
         "All three compute exact full attention, just on faster hardware",
         "Linformer: mixture of experts; Performer: parameter sharing"], 0,
        "Sparse pattern vs low-rank vs kernel trick.",
        "Sparse methods (Longformer, BigBird) skip most token pairs; Linformer assumes the attention matrix is low rank; Performer approximates softmax with random features. All make cost ~linear in length. FlashAttention, by contrast, is exact and only changes memory access.",
        topic="efficient-arch", level=3),
    fill("For a 768×768 matrix, low-rank factorisation saves parameters only when the rank r is below ____ (a whole number).", "384",
         "Solve r(m + n) < m·n.",
         "r < 768·768 / 1536 = 384. In practice useful ranks are far smaller (e.g. 64-128), otherwise the accuracy cost buys little saving.",
         topic="low-rank", level=3),
    tf("Quantizing an LLM's weights from FP16 to INT4 also cuts its KV-cache memory by 4x.", False,
       "Weights vs runtime state.",
       "Weight-only quantization shrinks the stored weights only. The KV cache and activations stay FP16 unless you separately quantize them (e.g. an INT8 KV cache). Budget GPU memory as weights + KV cache + overhead.",
       topic="quantization", level=3),
    # ------------------------------------------------------------------ L4
    mcq("A support team's BERT-base intent classifier must run on CPU under 40 ms (now 160 ms) with at most 1.5 points accuracy loss. Which plan is most defensible?",
        ["Distil to a 6-layer student, apply dynamic INT8 quantization to Linear layers, export to ONNX Runtime with dynamic padding, and measure accuracy and latency after each step",
         "Quantize to INT4 and ship without re-evaluation",
         "Switch to ALBERT-base because it has 9x fewer parameters",
         "Prune 50% of individual weights and keep the dense CPU kernels"], 0,
        "Stack levers that cut compute, and verify each.",
        "Distillation (~2x), INT8 Linear layers (~2x on CPU) and runtime/padding savings stack towards 4x. ALBERT does not cut FLOPs; unstructured pruning gives no dense-kernel speed-up; untested INT4 risks the accuracy budget.",
        topic="inference-opt", level=4),
    mcq("ALBERT-xxlarge has fewer parameters than BERT-large yet trains and runs more slowly. Why?",
        ["Its hidden size is very large (4096), and shared weights still run at every layer, so compute per token is much higher",
         "Parameter sharing adds a synchronisation step between layers",
         "Its embedding is not factorised",
         "It uses sentence-order prediction at inference time"], 0,
        "Parameters measure storage; width × depth measures FLOPs.",
        "Lan et al. scale width aggressively because sharing keeps parameters small, but FLOPs grow with H². 'Fewer parameters' and 'faster' are different axes; exam answers that equate them lose marks.",
        topic="efficient-arch", level=4),
    mcq("What does the lottery ticket hypothesis (Frankle & Carbin, 2019) claim?",
        ["A dense network contains a sparse subnetwork that, reset to its original initial weights and trained alone, can match the full network's accuracy",
         "Randomly pruned networks always beat trained ones",
         "Any subnetwork works if you train it long enough",
         "Pruning only works for convolutional networks"], 0,
        "Prune, rewind, retrain.",
        "Train, prune the smallest weights, rewind survivors to their initial (or early) values, retrain; repeat. It explains why big models compress so well, but finding the ticket needs full training first, so it is not a training-cost saver by itself.",
        diagram="""
init W0 -> train -> prune smallest p% -> mask m
   ^                                     |
   +---- rewind survivors to W0 <--------+
        retrain sparse net (m * W0); repeat
""",
        topic="pruning", level=4),
    fill("In the lottery ticket procedure, the surviving weights are reset to their ____ values before retraining (one word).", "initial",
         "Rewind, don't re-randomise.",
         "Re-randomised sparse networks train worse; the original initialisation is the 'winning ticket'. For large models, rewinding to an early-training checkpoint works better than iteration 0.",
         topic="pruning", level=4),
    mcq("When fine-tuning BERT, why can movement pruning beat magnitude pruning at high sparsity?",
        ["It removes weights moving towards zero during fine-tuning, so it keeps weights the task needs even if they were small after pre-training",
         "It removes the largest weights first",
         "It quantizes instead of pruning",
         "It prunes before pre-training, avoiding fine-tuning"], 0,
        "Magnitude reflects pre-training; movement reflects the task.",
        "In transfer learning, pre-trained magnitudes say little about what the downstream task needs. Movement pruning (Sanh et al. 2020) scores weights by how fine-tuning changes them, and holds accuracy better at 90%+ sparsity.",
        topic="pruning", level=4),
    mcq("Why does TinyBERT's task-specific distillation stage use data augmentation?",
        ["The task dataset is small; augmenting it (e.g. word replacement with embeddings/MLM predictions) gives the student many more teacher outputs to imitate",
         "Augmentation makes the teacher smaller",
         "It replaces the general distillation stage",
         "Augmentation is needed because the student has a different tokenizer"], 0,
        "Distillation signal comes from teacher outputs on inputs.",
        "TinyBERT: stage 1 general distillation on a large corpus, stage 2 task distillation. The teacher can label any text, so extra synthetic inputs are free supervision. Ablations show augmentation matters most on small GLUE tasks.",
        topic="distillation", level=4),
    mcq("MobileBERT is distilled layer by layer from IB-BERT, an inverted-bottleneck BERT-large, rather than from plain BERT-large. Why?",
        ["Layer-wise feature-map transfer needs teacher and student to have the same feature width at each layer, and IB-BERT is built to match MobileBERT's",
         "Plain BERT-large is too small",
         "IB-BERT uses INT8, which MobileBERT copies",
         "Plain BERT-large has no attention maps"], 0,
        "Matching shapes for per-layer losses.",
        "MobileBERT's thin layers use bottlenecks to a narrow width; IB-BERT adds inverted bottlenecks so its per-layer feature maps match that width while keeping BERT-large quality. The result: ~25M parameters, task-agnostic, much faster on phones.",
        topic="distillation", level=4),
    out("m = n = 768\n"
        "for r in (64, 400):\n"
        "    print(r, r * (m + n), r * (m + n) < m * n)",
        ["64 98304 True\n400 614400 False", "64 98304 True\n400 614400 True", "64 4096 True\n400 160000 True", "64 98304 False\n400 614400 False"], 0,
        "Compare r(m+n) with m·n = 589,824.",
        "Rank 64 needs 98,304 parameters (6x fewer). Rank 400 needs 614,400, MORE than the original 589,824, and still loses accuracy, so it is strictly worse. Pick r well below mn/(m+n).",
        topic="low-rank", level=4),
    tf("Hinton-style distillation multiplies the soft-target loss by T² so that its gradients keep a comparable size to the hard-label loss when the temperature T changes.", True,
       "Softening by T shrinks gradients by about 1/T².",
       "Gradients of the softened cross-entropy scale like 1/T². Multiplying by T² keeps the balance between the soft and hard terms stable, so you can tune T without re-tuning the loss weights.",
       topic="distillation", level=4),
    out("per_head = 4 * 768 * 64      # Q, K, V columns + output rows, one head\n"
        "pruned = 48                  # of BERT-base's 144 heads\n"
        "print(per_head, per_head * pruned, round(per_head * pruned / 110e6 * 100, 1))",
        ["196608 9437184 8.6", "49152 2359296 2.1", "196608 9437184 33.3", "589824 28311552 25.7"], 0,
        "Each head owns a 64-wide slice of Q, K, V and of the output projection.",
        "One head = 4 × 768 × 64 = 196,608 weights; 48 heads ≈ 9.4M, only ~8.6% of BERT-base. A third of the heads is not a third of the model: the FFN (~2/3 of layer weights) and embeddings are untouched. Head pruning mainly saves attention compute.",
        topic="pruning", level=4,
        diagram="""
one BERT-base layer (H = 768, 12 heads x 64)
  attention: Q K V O  = 4 x 768 x 768   (~2.4M)
  FFN:       768x3072 + 3072x768        (~4.7M)
  pruning heads touches only the first row
"""),
    mcq("For BERT on CPU, why is dynamic INT8 quantization usually preferred to static quantization?",
        ["Dynamic computes activation scales on the fly per input, so it needs no calibration set and handles varying sequence lengths and activation ranges; Linear layers dominate the cost anyway",
         "Static quantization cannot quantize weights",
         "Dynamic quantization also prunes heads",
         "Static quantization only works on GPU"], 0,
        "Who decides the activation scale, and when?",
        "Static quantization fixes activation scales from a calibration run and can be faster, but transformer activations vary a lot across inputs. Dynamic quantization stores INT8 weights and quantizes activations per batch, a good accuracy/effort trade-off for BERT.",
        topic="quantization", level=4),
    tf("Quantization-aware training (QAT), which simulates INT8 rounding during fine-tuning, usually loses less accuracy than post-training quantization, at the cost of a training run.", True,
       "Let the model adapt to the rounding.",
       "PTQ is cheaper (no training) and fine at INT8 for most BERT tasks; QAT (as in Q8BERT) is the fallback when PTQ loses too much, especially at lower bit-widths.",
       topic="quantization", level=4),
    out("import math\n"
        "C = 6 * 30e9 * 400e9                 # 30B params, 400B tokens\n"
        "H = C / (500e12 * 0.40) / 3600       # 500 TFLOP/s, 40% MFU\n"
        "cost = H * 3.00\n"
        "print(f\"{C:.1e}\", round(H), round(cost), cost <= 350000, math.ceil(H / (30 * 24)))",
        ["7.2e+22 100000 300000 True 139", "7.2e+22 40000 120000 True 56", "7.2e+22 100000 300000 True 138", "7.2e+21 10000 30000 True 14"], 0,
        "Budget $350k, 30-day deadline: GPUs = H ÷ 720, rounded up.",
        "C = 7.2e22; effective 2e14 FLOP/s gives 3.6e8 s = 100,000 GPU-hours = $300,000, inside the $350k budget. 100,000 / 720 = 138.9 -> 139 GPUs in parallel. Flooring to 138 misses the deadline; skipping MFU gives the 40,000-hour row.",
        topic="data-pipelines", level=4),
    mcq("In the course's serving model, which change cuts the fleet more: doubling batch capacity per GPU, or halving decode time per token?",
        ["Doubling batch capacity doubles X exactly in the formula, while halving decode does not (prefill stays); but in reality bigger batches need more KV-cache memory and raise per-token decode time",
         "Halving decode always cuts more, because the formula ignores prefill",
         "They are identical in every respect",
         "Neither affects the number of GPUs"], 0,
        "X = batch ÷ (prefill + tokens × decode).",
        "The formula treats batch and latency as independent, which is a simplification. Real batches are bounded by memory and make each decode step slower. A good exam answer computes the formula and then names this caveat.",
        topic="deployment-scale", level=4),
    mcq("Which technique gives NO benefit for a BERT-based NER tagger that labels each token in one forward pass?",
        ["Speculative decoding",
         "Dynamic INT8 quantization",
         "Distillation to a smaller encoder",
         "Dynamic padding with length bucketing"], 0,
        "Which technique assumes token-by-token generation?",
        "Speculative decoding speeds up autoregressive generation by letting a draft model propose tokens for the big model to verify. An encoder tagger generates nothing, so there is nothing to speculate. The other three cut its compute directly.",
        topic="inference-opt", level=4),
    out("n, k = 4096, 256          # sequence length, Linformer projection size\n"
        "print(n * n // (n * k))",
        ["16", "256", "4096", "64"], 0,
        "Full attention n×n vs projected n×k.",
        "Full attention builds a 4096×4096 score matrix; Linformer projects K and V to k = 256 rows, so scores are 4096×256: 16x fewer. The approximation assumes attention is low rank, which can hurt tasks needing precise long-range token matches.",
        topic="efficient-arch", level=4),
    mcq("A team must serve a 46.7B-total / 12.9B-active MoE model on GPUs with 24 GB each in INT4. What is the binding constraint?",
        ["Memory for all experts: 46.7B × 0.5 B ≈ 23.4 GB of weights alone leaves almost nothing for the KV cache, so in practice more than one GPU is needed",
         "Compute, because all 46.7B parameters run per token",
         "Nothing: 12.9B × 0.5 B = 6.5 GB fits easily",
         "Tokenizer speed"], 0,
        "Total for memory, active for compute.",
        "Per-token compute is that of a ~13B model, but every expert must be resident. 23.4 GB on a 24 GB card leaves ~0.6 GB for activations, KV cache and CUDA overhead: not viable at any real context length.",
        topic="efficient-arch", level=4),
    # ------------------------------------------------------------- extra
    mcq("The deck's 'cost of scale' slide shows parameter counts BERT-L 0.34B (2018), GPT-2 1.5B, T5 11B, GPT-3 175B, Megatron-Turing 530B, PaLM 540B (2022). What is the slide's point?",
        ["Model size grew about 500x in four years, so training and serving cost are no longer a hidden detail",
         "Larger models are always cheaper to serve per request",
         "Parameter count stopped growing after GPT-3",
         "Only encoder models grew"], 0,
        "~0.34B -> 540B.",
        "Roughly 500x growth between BERT and PaLM; GPT-3 alone cost an estimated $4.6M and 1,287 MWh to train once. That growth is what makes compression and efficient serving a requirement for anyone without hyperscale budgets.",
        topic="need-efficiency", level=3,
        diagram="""
params (B, log scale)
BERT-L  0.34 |
GPT-2   1.5  |#
T5      11   |###
GPT-3   175  |######
PaLM    540  |#######
"""),
    mcq("A news-tagging service built on BERT-large misses its p95 latency target. Profiling shows 70% of time in tokenisation and JSON handling in Python and 30% in the model. What should the team do first?",
        ["Fix the pipeline bottleneck (fast Rust-based tokenizer, batch requests, cheaper serialisation) before compressing the model",
         "Distil BERT-large to a 2-layer model",
         "Quantize to INT4",
         "Buy faster GPUs"], 0,
        "Amdahl's law.",
        "Even an infinitely fast model saves at most 30%. The course's first takeaway: efficiency is a system-wide concern, not just model architecture. Measure, then attack the biggest share.",
        topic="need-efficiency", level=4,
        analogy="Like optimising a SQL query when the profiler says the time is spent serialising the response: tune the slow part, not the famous one."),
    tf("vLLM's PagedAttention, as the course describes it, borrows virtual-memory paging from operating systems to store the KV cache in fixed-size non-contiguous blocks, raising serving throughput under mixed-length traffic.", True,
       "OS idea, GPU memory.",
       "Allocating KV memory in pages instead of one big block per request wastes far less GPU memory, so more requests fit in a batch; the deck reports up to ~24x throughput vs naive Hugging Face Transformers serving.",
       topic="deployment-scale", level=2,
       analogy="Like an OS giving a process memory pages on demand instead of reserving its maximum heap up front."),
    fill("In the training-cost examples, MFU stands for Model FLOP ____ (one word).", "Utilization",
         "The fraction of peak the GPU really achieves.",
         "MFU = achieved model FLOP/s ÷ peak FLOP/s; 30-40% is typical. Effective throughput = peak × MFU, and GPU-hours scale with 1/MFU.",
         topic="data-pipelines", level=2),
]
