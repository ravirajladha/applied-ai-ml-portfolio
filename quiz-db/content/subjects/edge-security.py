from helpers import mcq, tf, out, fill

SUBJECT = "edge-security"

TOPICS = [
    ("threats", "Security and privacy challenges in Edge AI"),
    ("fl-basics", "Federated learning workflow"),
    ("fedavg", "FedAvg weighting and the global update"),
    ("fl-challenges", "Non-IID data, client dominance and FL system challenges"),
    ("byzantine", "Poisoning / Byzantine attacks and robust aggregation"),
    ("dp-crypto", "Differential privacy, secure aggregation and encryption"),
    ("model-extraction", "Model extraction and model protection"),
    ("identity-trust", "Device identity, authentication and trust management"),
    ("tee-secure-boot", "Trusted execution environments and secure boot"),
    ("secure-comms", "Secure communication between edge and cloud"),
]

QUESTIONS = [
    # ------------------------------------------------------------------ L1
    mcq("Why is security harder for an edge device than for a model running in a locked data centre?",
        ["Attackers can physically get hold of the device, open it and read its storage",
         "Edge devices never connect to a network",
         "Edge models are always open source",
         "Data centres do not run machine learning"], 0,
        "Who can touch the hardware?",
        "A camera on a pole or a sensor in a field can be stolen, opened and probed. Its flash can be dumped to copy the model or keys. A data centre has guards, cages and audited access; an edge fleet does not.",
        topic="threats", level=1),
    mcq("In federated learning (FL), what leaves each participant and goes to the central server?",
        ["Model updates (trained weights or weight changes), not the raw data",
         "The raw training data, encrypted",
         "An anonymised copy of the data",
         "Nothing at all"], 0,
        "The data stays where it is; something learned from it travels.",
        "Each client trains the shared model on its own data and sends back only the updated parameters. The server combines them. 'Anonymised data' is the common wrong answer: in FL no data records are sent at all.",
        topic="fl-basics", level=1,
        diagram="""
 server: global model w
   |  broadcast w        ^ upload w_k (weights only)
   v                     |
 bank A    bank B    bank C   (raw data never leaves)
"""),
    tf("The main reason to use federated learning is that the raw data is not allowed to, or should not, leave the organisations or devices that hold it.", True,
       "Think of banks that regulation forbids from sharing transactions.",
       "FL is privacy-preserving training: the model goes to the data instead of the data going to the model. That is why the papers use banks and telecom operators bound by regulation.",
       topic="fl-basics", level=1),
    mcq("FedAvg combines client models with a weighted average. What decides each client's weight?",
        ["Its share of the total training examples, n_k / N",
         "How fast its servers are",
         "Every client always gets an equal weight",
         "How much it paid to join"], 0,
        "More data, more say.",
        "FedAvg weight = client's examples / total examples. A bank with 40,000 of 100,000 transactions gets 0.40. This makes the average behave like training on the pooled data when clients are similar.",
        topic="fedavg", level=1,
        analogy="Like an overall product rating that weights each store's average by its number of reviews, not one vote per store."),
    fill("In FedAvg, a client with 30,000 of the federation's 100,000 examples gets an aggregation weight of ____ (a decimal).", "0.3",
         "n_k / N.",
         "30,000 / 100,000 = 0.3. All the weights add up to 1.",
         topic="fedavg", level=1),
    mcq("What does 'non-IID data' mean in federated learning?",
        ["Different clients' data come from different distributions (different patterns, classes or users)",
         "The data has no ID column",
         "The data is encrypted",
         "Every client has exactly the same data"], 0,
        "IID = independent and identically distributed.",
        "In real federations a rural telecom operator's users behave differently from urban ones, and one bank sees a fraud pattern others rarely see. Their data is not identically distributed, which makes training harder.",
        topic="fl-challenges", level=1),
    mcq("A 'poisoning' attack in federated learning means:",
        ["A participant sends crafted or corrupted updates (or trains on tampered data) to damage or bias the global model",
         "The server's power supply is cut",
         "A participant leaves the federation",
         "Someone reads the network traffic"], 0,
        "The attacker is inside the federation.",
        "Because the server cannot see clients' data, a malicious client can send updates that push the global model wherever it wants, or random noise that just breaks it. Defences work on the updates themselves.",
        topic="byzantine", level=1),
    mcq("What is differential privacy (DP) in one line?",
        ["Adding carefully calibrated noise so that no single person's data noticeably changes what is released",
         "Encrypting the data with a different key for each user",
         "Deleting names from a dataset",
         "Storing data on different servers"], 0,
        "It is a mathematical guarantee, not just anonymisation.",
        "DP limits how much any one record can influence the output (a model, a statistic). Removing names is not DP: people can often be re-identified from the remaining columns.",
        topic="dp-crypto", level=1,
        analogy="Like publishing a crowd photo blurred just enough that no single face can be recognised, while the crowd's size and mood stay visible."),
    mcq("What is a model extraction (model stealing) attack?",
        ["Querying a model many times and using its answers to train a copy that behaves the same",
         "Deleting the model from the device",
         "Reading the training data from the server's database",
         "Slowing the model down with many requests"], 0,
        "The attacker never needs the weights file.",
        "By sending many chosen inputs and recording the outputs (especially full probability vectors), an attacker trains a 'surrogate' model that mimics yours. They steal your work without touching your servers' storage.",
        topic="model-extraction", level=1,
        analogy="Like rebuilding a competitor's pricing algorithm by requesting thousands of quotes and fitting a model to the answers."),
    mcq("What is a Trusted Execution Environment (TEE)?",
        ["An isolated area of the processor where code and data are protected even from the main operating system",
         "A testing environment for new models",
         "A cloud server that the vendor trusts",
         "A firewall rule"], 0,
        "Think of a locked room inside the chip.",
        "A TEE (ARM TrustZone, Intel SGX) runs sensitive code, such as decrypting model weights or holding keys, separately from the normal OS. Even if the OS is compromised, it cannot read the TEE's memory.",
        topic="tee-secure-boot", level=1,
        analogy="Like a bank vault inside the bank building: even staff with keys to the building cannot open it."),
    mcq("What does secure boot do?",
        ["At start-up each stage checks the signature of the next stage before running it, so only trusted software boots",
         "It starts the device faster",
         "It encrypts the user's files",
         "It blocks network access during boot"], 0,
        "Boot ROM -> bootloader -> OS -> app.",
        "Secure boot builds a chain of trust: the immutable boot ROM verifies the bootloader, the bootloader verifies the OS or firmware, and so on. Tampered firmware fails its signature check and does not run.",
        topic="tee-secure-boot", level=1,
        analogy="Like a deployment pipeline that only runs container images whose signatures check out, at every stage."),
    tf("TLS encrypts the data sent between an edge device and the cloud so that someone listening on the network cannot read it.", True,
       "It is the S in HTTPS.",
       "TLS gives confidentiality and integrity in transit, and it authenticates the server (with mTLS, both sides). It does not protect data stored on the device.",
       topic="secure-comms", level=1),
    mcq("What is the difference between TLS and mutual TLS (mTLS)?",
        ["In mTLS the device also presents a certificate, so the server knows exactly which device is talking",
         "mTLS uses two layers of encryption",
         "mTLS is TLS without encryption",
         "There is no difference"], 0,
        "Who proves their identity in each?",
        "Normal TLS: only the server proves who it is (your browser checks the bank's certificate). mTLS: the client proves it too, with its own certificate. Edge platforms such as AWS IoT Core use mTLS so each device has its own identity.",
        topic="secure-comms", level=1,
        diagram="""
 TLS:   device --checks server cert--> cloud
 mTLS:  device <--both check certs--> cloud
        (fleet CA signs every device cert)
"""),
    fill("The standard port for MQTT over TLS is ____ (plain MQTT uses 1883).", "8883",
         "Plain is 1883.",
         "MQTT over TLS listens on 8883. Anything sensitive in an edge pipeline should use 8883 with certificates, not 1883 in plain text.",
         topic="secure-comms", level=1),
    mcq("Why should every edge device have its own unique identity (key and certificate) rather than all devices sharing one password?",
        ["If one device is stolen and its secret extracted, only that one device has to be revoked",
         "Shared passwords are harder to type",
         "Unique identities make devices faster",
         "Certificates are cheaper than passwords"], 0,
        "What happens when one device is dumped?",
        "With a shared secret, one opened device gives the attacker the key to the whole fleet. With per-device keys you revoke one certificate and the rest stay trusted.",
        topic="identity-trust", level=1,
        analogy="Like giving every microservice its own API key instead of one shared key: you can rotate one without breaking all."),
    tf("In federated learning the central aggregator can look at each participant's raw data to check whether it is honest.", False,
       "What is the whole point of FL?",
       "By design the aggregator never receives raw data; it only sees model updates. That is also why poisoning is hard to confirm: the server cannot open the suspected client's records (and regulation forbids it in the papers' bank and telecom cases).",
       topic="fl-basics", level=1),
    mcq("Which of these is a privacy risk of keeping data on an edge device, even though it never goes to the cloud?",
        ["A stolen or resold device can still hold personal data in its storage",
         "There is no privacy risk if data stays on the device",
         "Edge devices automatically delete all data",
         "The cloud can read the device's memory at any time"], 0,
        "Local is better, not perfect.",
        "Edge processing reduces exposure, but data at rest on the device (images, logs) needs encryption and retention limits. A doorbell camera sold second-hand with old clips still on it is a real privacy breach.",
        topic="threats", level=1),
    fill("In differential privacy, the privacy-loss parameter is written with the Greek letter ____ (one word, as spelled in English).", "epsilon",
         "It also means 'a small amount' in maths.",
         "ε (epsilon) bounds how much one record can change the output. The papers and libraries such as Opacus report a model's privacy as an (ε, δ) pair.",
         topic="dp-crypto", level=1),

    # ------------------------------------------------------------------ L2
    out("""n = [18_000, 12_000, 6_000, 4_000]     # four cooperative banks
N = sum(n)
w = [k / N for k in n]
print([round(x, 2) for x in w], round(sum(w), 6))""",
        ["[0.45, 0.3, 0.15, 0.1] 1.0", "[0.25, 0.25, 0.25, 0.25] 1.0", "[0.45, 0.3, 0.15, 0.1] 0.25", "[18, 12, 6, 4] 40"], 0,
        "Each client's examples over the total.",
        "N = 40,000, so the weights are 0.45, 0.30, 0.15 and 0.10, and they sum to 1. In the exam, show each n_k / N and the check that they add to 1 before writing the update.",
        topic="fedavg", level=2),
    out("""import numpy as np
n = np.array([18, 12, 6, 4])          # thousands of examples
w_k = np.array([0.8, 0.5, 0.2, 1.0])  # one parameter after local training
fedavg = float(np.sum(n / n.sum() * w_k))
plain = float(np.mean(w_k))
print(round(fedavg, 3), round(plain, 3))""",
        ["0.64 0.625", "0.625 0.64", "0.64 0.64", "2.5 0.625"], 0,
        "0.45 x 0.8 + 0.30 x 0.5 + ...",
        "FedAvg: 0.45(0.8) + 0.30(0.5) + 0.15(0.2) + 0.10(1.0) = 0.36 + 0.15 + 0.03 + 0.10 = 0.64. A plain mean gives 0.625, over-weighting the smallest client's value of 1.0. Global update: w_global = Σ (n_k / N) w_k.",
        topic="fedavg", level=2),
    mcq("Which is the correct order of one federated learning round?",
        ["Server sends the global model -> clients train locally -> clients send updates -> server aggregates into a new global model",
         "Clients send data -> server trains -> server sends the model back",
         "Server aggregates -> clients train -> server sends the model",
         "Clients train -> clients share data with each other -> server averages"], 0,
        "Data never moves; the model makes the round trip.",
        "Each round: broadcast w_t, each client runs a few local epochs on its data, uploads w_k (or the change w_k - w_t), and the server computes w_{t+1} = Σ (n_k / N) w_k. Repeat for many rounds.",
        topic="fl-basics", level=2,
        diagram="""
 round t:  server --w_t--> clients
           clients: local epochs on own data
           clients --w_k--> server
           server: w_t+1 = sum (n_k/N) w_k
"""),
    mcq("In the Flower framework (used in the course lab), which part decides how client updates are combined?",
        ["The server's strategy, for example FedAvg",
         "Each client's fit() function",
         "The dataset loader",
         "The network router"], 0,
        "Clients train; who aggregates?",
        "Flower clients implement fit() (train locally, return weights and number of examples) and evaluate(). The server runs a Strategy such as FedAvg that selects clients and aggregates their results using those example counts.",
        topic="fl-basics", level=2),
    out("""import numpy as np
u = np.array([0.10, 0.12, 0.11, 0.09, 5.00])   # one coordinate from 5 clients
print(round(float(u.mean()), 3), float(np.median(u)))""",
        ["1.084 0.11", "0.11 1.084", "1.084 0.105", "0.105 0.11"], 0,
        "One client's value is far from the others.",
        "The mean is dragged to 1.084 by the single 5.00 update; the coordinate-wise median stays at 0.11. That is why median-based aggregation resists a Byzantine client: one extreme value cannot move it far.",
        topic="byzantine", level=2),
    out("""import numpy as np
u = np.sort(np.array([0.10, 0.12, 0.11, 0.09, 5.00]))
beta = 1                       # drop 1 lowest and 1 highest
print(round(float(u[beta:-beta].mean()), 3))""",
        ["0.11", "1.084", "0.105", "0.083"], 0,
        "After dropping 0.09 and 5.00, average what is left.",
        "Trimmed mean with beta = 1 keeps 0.10, 0.11, 0.12, mean 0.11. Note that it also throws away the honest lowest value (0.09) every time: trimming is blind to who is honest.",
        topic="byzantine", level=2),
    fill("The robust aggregation rule that selects the single client update with the smallest total squared distance to its nearest neighbours is called ____.", "Krum",
         "Named after a Bulgarian king; starts with K.",
         "Krum (Blanchard et al. 2017) scores each update by the sum of squared distances to its n - f - 2 closest updates and keeps the lowest-scoring one. Outliers far from the crowd never win.",
         topic="byzantine", level=2),
    mcq("A camera app owner sees one API key send 9,000 requests in a day, all small variations of the same 20 images, and store every full probability vector. Typical users send about 40 natural photos a day. What is most likely happening?",
        ["A model extraction attempt: the client is mapping the model's outputs to train a copy",
         "A normal power user",
         "A denial-of-service attack aimed only at slowing the server",
         "A data-poisoning attack on the training set"], 0,
        "Look at what is being collected, not just how much.",
        "Systematic perturbations plus saved full probability vectors are the fingerprints of extraction. DoS attackers do not care about the answers; poisoning needs a path into training data. The volume (about 225x normal) is the second signal.",
        topic="model-extraction", level=2,
        diagram="""
 gateway log, one API key, 24 h
   requests:   9,000   (normal ~40)
   inputs:     20 base images x small nudges
   recorded:   full probability vector each time
"""),
    mcq("ARM TrustZone and Intel SGX are both TEEs. What is the main difference?",
        ["TrustZone splits the processor into a 'secure world' and a 'normal world'; SGX creates small encrypted enclaves inside an application on x86",
         "TrustZone is for GPUs and SGX is for MCUs",
         "SGX runs only in the cloud and TrustZone only offline",
         "They are two names for the same technology"], 0,
        "One is a whole second world, the other a protected island.",
        "TrustZone (ARM Cortex-A and Cortex-M, so most edge SoCs and MCUs) runs a separate secure OS alongside the normal one. SGX (Intel x86, e.g. NUC-class gateways and servers) isolates enclaves within a process. Both protect keys and code from a compromised OS.",
        topic="tee-secure-boot", level=2),
    tf("Once a device has passed secure boot, the software it is running is protected against all later attacks while it runs.", False,
       "Secure boot checks things at one moment.",
       "Secure boot verifies what is loaded at start-up. A bug exploited at runtime (a buffer overflow in the MQTT client) is not detected. Runtime protection needs patching, least privilege, TEEs and attestation on top.",
       topic="tee-secure-boot", level=2),
    out("""import numpy as np
g = np.array([3.0, 4.0])          # one client's update
C = 1.0                           # clipping norm
norm = np.linalg.norm(g)
clipped = g * min(1.0, C / norm)
print(np.round(clipped, 2).tolist(), round(float(np.linalg.norm(clipped)), 2))""",
        ["[0.6, 0.8] 1.0", "[1.0, 1.0] 1.41", "[3.0, 4.0] 5.0", "[0.75, 1.0] 1.25"], 0,
        "Scale the whole vector so its length is at most C.",
        "The norm is 5, so the update is scaled by 1/5 to [0.6, 0.8], length 1. Clipping bounds how much any one client (or record) can move the model, the 'sensitivity'. Only then does a fixed amount of noise give a DP guarantee. Clipping each coordinate to 1 ([1, 1]) is a different, wrong operation.",
        topic="dp-crypto", level=2,
        diagram="""
   y
 4 |    * g = (3, 4), |g| = 5
   |   /
 1 |  * clipped (0.6, 0.8), |.| = C = 1
   +-----------> x
"""),
    mcq("In DP-FedAvg (federated averaging with differential privacy), what are the two steps added to plain FedAvg?",
        ["Clip each client's update to a maximum norm C, then add Gaussian noise scaled to C to the aggregate",
         "Encrypt the updates, then decrypt them on the server",
         "Drop the largest client, then average the rest",
         "Add noise to the raw data, then send the data to the server"], 0,
        "Bound the influence, then hide it.",
        "Clipping bounds each client's contribution; noise of standard deviation sigma x C masks whether any one client took part. Without clipping, one huge update could still dominate, so the noise would guarantee nothing.",
        topic="dp-crypto", level=2),
    mcq("What does secure aggregation give a federated learning system?",
        ["The server learns only the SUM (or average) of the clients' updates, never any individual client's update",
         "A guarantee that the final model reveals nothing about any record",
         "Protection against poisoned updates",
         "Faster training"], 0,
        "It hides the parts, not the whole.",
        "With pairwise masks that cancel in the sum, the server cannot read a single bank's update. But the final model can still leak (that needs DP), and the server can no longer inspect individual updates for poisoning: privacy and robustness pull in opposite directions.",
        topic="dp-crypto", level=2,
        analogy="Like a ballot box: the count is public, individual votes are not."),
    tf("Even though FL sends only model updates, an attacker who sees an individual update can sometimes reconstruct parts of the client's training data.", True,
       "Gradients are computed from the data.",
       "Gradient-inversion and membership-inference attacks recover images or test whether a record was used, especially from small batches. FL alone is not a formal privacy guarantee; secure aggregation and DP close the gap.",
       topic="fl-basics", level=2),
    mcq("A federation of hospitals finds that one hospital, which treats mostly children, has very different data from the rest. What typically happens to plain FedAvg training?",
        ["Local models pull in different directions (client drift), convergence slows and the global model may underfit the children's patterns",
         "Training becomes faster because the data is more varied",
         "Nothing changes; FedAvg assumes nothing about the data",
         "The children's hospital automatically gets a higher weight"], 0,
        "Each local model fits its own distribution.",
        "Non-IID data makes local updates disagree. Averaging them gives a compromise that fits the majority best, and the minority patterns (the very reason to include that hospital) are diluted. Fixes: FedProx regularisation, more rounds with fewer local epochs, personalisation layers.",
        topic="fl-challenges", level=2,
        diagram="""
 global optimum (pooled data)  *
   urban clients pull ->  o o o
   children's hospital pulls ->     x
 FedAvg lands near the majority, away from x
"""),
    mcq("One telecom operator holds 0.50 of the FedAvg weight in a four-operator federation. What is the main risk?",
        ["The global model leans toward that operator's data, and if it is compromised or buggy it can steer the model almost alone",
         "The other operators' updates are ignored completely",
         "The model cannot converge with uneven weights",
         "FedAvg refuses to run when one weight exceeds 0.5"], 0,
        "Half the vote in every round.",
        "Dominance makes the global model behave like a model of the largest client, and creates a single point of failure. Mitigations: cap per-client weight (e.g. at 0.3 and renormalise), clip update norms, monitor per-client contribution.",
        topic="fl-challenges", level=2,
        diagram="""
 FedAvg weight
 A |##########  0.50
 B |######      0.30
 C |##          0.12
 D |#           0.08
"""),
    mcq("Which pairing of edge attack and target is correct?",
        ["Dumping flash -> the model and keys; adversarial patch -> the model's predictions; eavesdropping -> data in transit",
         "Dumping flash -> data in transit; eavesdropping -> the model's weights",
         "Adversarial patch -> the network; dumping flash -> the cloud database",
         "Eavesdropping -> the boot ROM"], 0,
        "Where does each attack actually touch the system?",
        "Map attacks to assets: physical access hits storage (model IP, keys, cached data); adversarial inputs hit inference; network attackers hit the channel; poisoned updates hit training. Each needs its own control (encryption at rest/TEE, robust models, TLS, robust aggregation).",
        topic="threats", level=2,
        diagram="""
 asset          attack                control
 storage        flash dump            encrypt, TEE
 inference      adversarial input     robustness
 channel        sniff / spoof         mTLS
 training       poisoned update       robust agg
"""),
    mcq("A retail API decides to return only the top-1 label, with no probability vector, to every client. What is the effect on a model extraction attack?",
        ["It slows the attack (far less information per query) but does not stop it; legitimate apps lose the confidence scores they used for thresholds",
         "It makes extraction impossible",
         "It has no effect on extraction",
         "It speeds the attack up because responses are smaller"], 0,
        "Labels still carry information.",
        "Label-only extraction still works, just with many more queries (and it pairs badly for the attacker with rate limits). The cost falls on honest users: an app that sends low-confidence cases to a human can no longer do that.",
        topic="model-extraction", level=2),
    tf("Watermarking a model prevents an attacker from stealing it.", False,
       "When does a watermark help?",
       "A watermark (e.g. a secret set of trigger inputs with planned outputs) lets you prove later that a suspect model was copied from yours. It deters and supports legal action; it does not stop the queries. That is why it is the third layer, not the only one.",
       topic="model-extraction", level=2,
       analogy="Like the fake 'trap streets' map-makers add: they do not stop copying, but they prove it."),
    out("""devices = 10_000
validity_days = 90            # short-lived device certificates
print(round(devices / validity_days, 1))""",
        ["111.1", "900000", "90", "11.1"], 0,
        "Each device renews once per validity period.",
        "About 111 certificate renewals a day, every day. Short-lived certificates limit the damage of a stolen key, but only work if renewal is automated (e.g. EST or the platform's provisioning API); manual renewal at this scale guarantees outages.",
        topic="identity-trust", level=2,
        analogy="Like 90-day web certificates with automatic renewal: short life is only safe when renewal is automated."),
    mcq("What is remote attestation?",
        ["The device proves to a remote verifier, with a hardware-protected key, which firmware and software it actually booted",
         "A technician visiting the device to check it",
         "The server sending its certificate to the device",
         "Encrypting the model before sending it"], 0,
        "Proof of state, not just of identity.",
        "A certificate says 'I am device 4,017'. Attestation adds 'and I am running signed firmware 3.2 with secure boot on', signed by a key the OS cannot touch. Servers can then release models or keys only to devices in a known-good state.",
        topic="identity-trust", level=2),
    fill("Each device's X.509 certificate is signed by the fleet's certificate authority, abbreviated ____.", "CA",
         "Two letters.",
         "The CA (often a private fleet CA) signs device certificates; servers trust any certificate chaining to it and can revoke individual ones.",
         topic="identity-trust", level=2),

    # ------------------------------------------------------------------ L3
    mcq("Four telecom operators train a SIM-fraud model with FedAvg: A 50,000 records, B 30,000, C 12,000, D 8,000. Which answer is correct?",
        ["Weights 0.50, 0.30, 0.12, 0.08; w_global = 0.50 w_A + 0.30 w_B + 0.12 w_C + 0.08 w_D",
         "Weights 0.25 each; w_global = (w_A + w_B + w_C + w_D) / 4",
         "Weights 0.50, 0.30, 0.12, 0.08; w_global = w_A, because A has the most data",
         "Weights 0.08, 0.12, 0.30, 0.50, to give small operators a bigger say"], 0,
        "n_k / N with N = 100,000.",
        "N = 100,000, so n_k / N gives 0.50, 0.30, 0.12, 0.08 (sum 1). The global model is the weighted sum of the four locally trained models. Equal weights is the classic wrong answer; inverse weighting is a fairness idea, not FedAvg.",
        topic="fedavg", level=3),
    out("""import numpy as np
U = np.array([[0.20, 0.10], [0.22, 0.12], [0.18, 0.09],
              [0.60, -0.40], [0.21, 0.11]])      # 5 client updates
n, f = len(U), 1                                  # assume 1 attacker
d = ((U[:, None, :] - U[None, :, :]) ** 2).sum(-1)
scores = [float(np.sort(d[i])[1:n - f - 1].sum()) for i in range(n)]
print(np.round(scores, 4).tolist(), int(np.argmin(scores)))""",
        ["[0.0007, 0.001, 0.0018, 0.8222, 0.0004] 4",
         "[0.0007, 0.001, 0.0018, 0.8222, 0.0004] 3",
         "[0.0004, 0.0007, 0.001, 0.0018, 0.8222] 0",
         "[0.8222, 0.001, 0.0018, 0.0007, 0.0004] 4"], 0,
        "Each score sums squared distances to the n - f - 2 = 2 nearest other updates.",
        "Client 3's update points the other way, so its distances are huge (score 0.82). Client 4 sits in the middle of the honest cluster (score 0.0004) and Krum keeps it as the round's update. Note Krum keeps ONE update and throws the rest away, which wastes honest information.",
        topic="byzantine", level=3),
    mcq("Four state electricity discoms train a power-theft detector by FL. Discom D, in a hilly region, sees a theft pattern (meter bypass during monsoon outages) the others never see. Midway, one discom is suspected of sending crafted updates, and the team switches to Krum. What is the design tension?",
        ["Krum and other robust rules drop updates far from the majority, so they may discard Discom D's honest but unusual updates and lose the very pattern the federation needed",
         "Krum is too slow for four clients",
         "Krum increases the weight of the attacker",
         "There is no tension; robust aggregation only removes attackers"], 0,
        "Robust rules cannot tell 'malicious' from 'different'.",
        "Distance-based defences assume honest clients look alike. Under non-IID data an honest minority client also looks like an outlier. That is the exam's 'tension' answer: robustness vs inclusion of genuine minority patterns (Bank A, Operator D).",
        topic="byzantine", level=3),
    mcq("The aggregator suspects one cooperative bank of poisoning but cannot inspect its data. What CAN it legitimately check?",
        ["Statistics of the updates themselves: norm, direction (cosine similarity) versus others across rounds, and the effect of each update on a small server-held validation set",
         "The bank's raw transactions, after asking politely",
         "Nothing at all",
         "The bank's employees' email"], 0,
        "It sees updates, so analyse updates.",
        "Update norms, cosine similarity to the median update, consistency over rounds and per-update validation loss are all available. None is proof: a non-IID honest client can look odd too, so these signals feed weighting or review, not instant expulsion.",
        topic="byzantine", level=3),
    mcq("An insurer's partner API returns full confidence vectors. The team wants to round every probability to one decimal place instead of returning only the top-1 label. What is the advantage for legitimate partners?",
        ["Partners still get the ranking and a coarse confidence for triage, while the attacker loses most of the fine-grained signal per query",
         "Rounding stops extraction completely",
         "Rounding makes the model more accurate",
         "There is no difference from top-1"], 0,
        "What do partners use the probabilities for?",
        "A partner that routes 'damage probability 0.6' to a human assessor can still do so. The attacker, who needs small changes in output for small changes in input, sees flat steps instead. It reduces leakage, like top-1, but keeps more usefulness.",
        topic="model-extraction", level=3),
    out("""import numpy as np
p = np.array([0.62, 0.27, 0.08, 0.03])    # full softmax
print(np.round(p, 1).tolist(), int(np.argmax(p)))""",
        ["[0.6, 0.3, 0.1, 0.0] 0", "[0.62, 0.27, 0.08, 0.03] 0", "[1.0, 0.0, 0.0, 0.0] 0", "[0.6, 0.3, 0.1, 0.0] 1"], 0,
        "Round to one decimal place; argmax is the top-1 index.",
        "Rounded output: [0.6, 0.3, 0.1, 0.0]; top-1 is class 0. Rounding keeps a usable confidence (60%) for honest clients but hides tiny changes: an input nudge that moves 0.62 to 0.64 shows no difference, so the attacker learns much less per query.",
        topic="model-extraction", level=3),
    out("""needed = 25_000          # queries the attacker wants
limit = 500              # per account per day
days_one_account = needed / limit
accounts_for_one_day = needed / limit
print(days_one_account, accounts_for_one_day)""",
        ["50.0 50.0", "50 50", "0.02 0.02", "12500000 12500000"], 0,
        "Divide the queries by the daily allowance.",
        "One account needs 50 days; 50 fake accounts finish in one day. Rate limiting raises cost and buys time but a sybil attack (many identities) gets around it. That is why it needs anomaly detection across accounts and the other two layers.",
        topic="model-extraction", level=3),
    mcq("A retail-analytics model's API faces a suspected extraction attack. Which three-layer defence, deployed together, matches the papers' reasoning?",
        ["(1) rate limiting + query-pattern anomaly detection; (2) output hardening (top-1 or rounded scores); (3) watermarking + legal terms of service",
         "(1) bigger servers; (2) more GPUs; (3) faster network",
         "(1) retrain weekly; (2) add more training data; (3) increase model size",
         "(1) TLS; (2) TLS with a longer key; (3) mTLS"], 0,
        "Detect and slow, leak less, prove and deter.",
        "Layer 1 slows and spots abuse but sybil accounts evade it; layer 2 cuts information per query but label-only attacks still work; layer 3 does nothing in the moment but proves theft afterwards and creates legal risk. Each covers a gap the others leave. TLS protects the channel, not the answers.",
        topic="model-extraction", level=3,
        diagram="""
 query -> [1 rate limit + anomaly detect]
       -> model
       -> [2 top-1 / rounded output]
       -> client
 [3 watermark + ToS]: proves a copy later
"""),
    out("""attack = 10_000 / 2        # queries per day over 48 hours
normal = 50
print(attack, attack / normal)""",
        ["5000.0 100.0", "10000 200.0", "5000.0 0.01", "20000.0 400.0"], 0,
        "48 hours is two days.",
        "10,000 queries in 48 h is 5,000 a day, 100x a typical client's 50. Volume alone could be a big honest customer; together with systematic perturbations and recorded full vectors it is a clear extraction signature.",
        topic="model-extraction", level=3),
    out("""eps_per_round = 0.1
rounds = 50
print(round(eps_per_round * rounds, 2))""",
        ["5.0", "0.1", "0.002", "50"], 0,
        "Under basic composition, privacy losses add up.",
        "Each round that touches the data spends privacy budget. Basic composition adds them: 50 x 0.1 = ε 5.0 in total, a much weaker guarantee than 0.1. Advanced composition and accountants (the moments/RDP accountant in Opacus) give tighter totals, but the budget always grows with rounds.",
        topic="dp-crypto", level=3),
    mcq("A smartwatch fleet wants FL with DP. Option 1: each watch adds noise before uploading (local DP). Option 2: watches upload clipped updates through secure aggregation and noise is added once to the sum (central/distributed DP). Which statement is right?",
        ["Local DP needs no trust in the server but needs far more noise per device, so accuracy suffers; aggregated noise gets the same ε with much less total noise",
         "Local DP always gives better accuracy",
         "Both give identical accuracy and trust",
         "Central DP needs no clipping"], 0,
        "Noise on every device vs noise once on the total.",
        "With local DP every upload must be private on its own, so noise is large and does not average out cheaply. Adding noise once to an aggregate over many devices hides each one in the crowd. Secure aggregation lets you get close to central DP without trusting the server to see individual updates.",
        topic="dp-crypto", level=3,
        diagram="""
 local DP:   each device adds big noise -> server
 central DP: devices --secure agg--> sum + noise once
 same epsilon, far less total noise in the second
"""),
    mcq("Why does secure aggregation make poisoning defences harder?",
        ["The server sees only the sum, so it cannot inspect or filter individual updates with Krum, trimmed mean or norm checks",
         "Secure aggregation makes updates larger",
         "It removes the need for any defence",
         "It reveals the attacker's identity"], 0,
        "Robust rules need to look at each update.",
        "Robust aggregation works on individual updates; secure aggregation hides them. Practical systems combine them carefully: norm-bound proofs from clients, clipping before masking, or robust aggregation inside a TEE on the server.",
        topic="dp-crypto", level=3),
    mcq("A tea-estate cooperative wants model weights on its gateways protected even if the Linux OS is compromised. How is a TEE typically used?",
        ["Store the model encrypted; the key lives in the secure world, which decrypts and runs inference (or the sensitive layers) there and returns only results",
         "Copy the model into /tmp at boot for speed",
         "Run the whole Linux OS inside the TEE",
         "Encrypt the model with a key stored next to it on the SD card"], 0,
        "Key and plaintext model must never be visible to the normal OS.",
        "The normal world only ever sees ciphertext and outputs. Limits: secure-world memory is small (often a few MB on TrustZone devices), so large models run partly outside or need careful partitioning. A key on the same SD card protects nothing.",
        topic="tee-secure-boot", level=3,
        diagram="""
 normal world (Linux)   |  secure world (TEE)
 encrypted model  ----->|  key -> decrypt -> infer
 input            ----->|
 result          <------|
"""),
    mcq("In a secure boot chain, where must the very first trusted key or key hash live?",
        ["In immutable hardware: boot ROM code plus a public-key hash burned into one-time-programmable fuses",
         "In the bootloader file on flash",
         "In the OS configuration",
         "On a cloud server the device contacts at boot"], 0,
        "If an attacker can rewrite it, it is not a root.",
        "Every stage is checked by the stage before it, so the first check must be something an attacker cannot modify. Flash can be rewritten, and a cloud check fails offline. The ROM + fuses are the root of trust.",
        topic="tee-secure-boot", level=3,
        diagram="""
 ROM + fused key hash  (immutable root)
   verifies -> bootloader
     verifies -> kernel / RTOS firmware
       verifies -> app + signed model
"""),
    mcq("How should a device's identity key be created during manufacturing for the strongest security?",
        ["Generated inside the device's secure element; only a certificate signing request leaves, and the CA returns a signed certificate",
         "Generated on the factory PC and copied to each device",
         "One key generated once and flashed onto every device",
         "Typed in by the installer at the customer site"], 0,
        "Where should the private key ever exist?",
        "If the private key is born inside tamper-resistant hardware and never leaves it, nobody (not even the factory) can copy it. Keys made on a PC can leak from that PC; a shared key compromises the fleet at once.",
        topic="identity-trust", level=3),
    tf("When a device is reported stolen, revoking its certificate (or disabling it in the IoT registry) stops it from connecting, without affecting any other device.", True,
       "Per-device identity, per-device revocation.",
       "Each device authenticates with its own certificate, so blocking one does not touch the others. This is the pay-off for per-device keys. Revocation must be enforced (registry check, CRL or OCSP), otherwise a revoked certificate still works until it expires.",
       topic="identity-trust", level=3),
    mcq("Battery sensors on a farm send readings over UDP with CoAP. What is the usual way to secure this channel?",
        ["DTLS (TLS adapted for datagrams), often with pre-shared keys or raw public keys to keep the handshake small",
         "Plain TLS over UDP without changes",
         "No security is possible over UDP",
         "Base64-encoding the payload"], 0,
        "TLS assumes a reliable stream.",
        "TLS needs TCP's ordered, reliable delivery; DTLS adds its own handling for lost and reordered records. On constrained devices, PSK or raw public keys avoid large certificate chains. Base64 is an encoding, not encryption.",
        topic="secure-comms", level=3),
    mcq("A firmware developer disabled server-certificate checks in the device's TLS client 'to make testing easier' and shipped it. What does an attacker on the network gain?",
        ["A man-in-the-middle: they present any certificate, the device accepts it, and they read or alter all traffic, including model updates",
         "Nothing, because the traffic is still encrypted",
         "Only the device's IP address",
         "They can only slow the connection"], 0,
        "Encrypted, but to whom?",
        "Encryption to an unverified party is encryption to the attacker. Always validate the server chain (and consider pinning the fleet's CA). This one setting turns TLS into a false sense of security.",
        topic="secure-comms", level=3),
    fill("In Krum with n = 7 clients and f = 2 assumed attackers, each client's score sums squared distances to its ____ nearest neighbours (a number).", "3",
         "n - f - 2.",
         "7 - 2 - 2 = 3. Krum's guarantee needs n > 2f + 2. With only 4 banks that fails even for f = 1 (4 is not > 4), so small cross-silo federations usually pair a median or trimmed mean with human review rather than rely on Krum alone.",
         topic="byzantine", level=3),
    tf("Coordinate-wise median aggregation ignores dataset sizes, so a bank with 4,000 examples gets the same say as a bank with 40,000.", True,
       "Does a median use weights?",
       "The plain median treats every client as one vote, unlike FedAvg's n_k / N. That helps against a dominant or compromised large client, but it can bias the model toward small clients. Weighted medians exist if you need both.",
       topic="byzantine", level=3),
    mcq("A random-noise update and a carefully crafted backdoor update are both Byzantine. Which is harder to defend against, and why?",
        ["The crafted one: it can be kept within normal norms and directions so distance- and median-based filters accept it",
         "The random one, because noise is unpredictable",
         "Both are equally easy to stop with Krum",
         "Neither can be stopped"], 0,
        "Which one looks like an honest update?",
        "Random noise has a large norm and points nowhere, so median, trimmed mean and Krum discard it easily. A backdoor can be scaled to look ordinary while teaching a trigger -> label rule. Norm clipping plus small DP noise reduces backdoors; detection needs more than distance.",
        topic="byzantine", level=3),
    mcq("A Mumbai hospital chain moves X-ray triage onto devices in each hospital and trains with FL. Under India's DPDP Act 2023, what does this design mainly help with?",
        ["Data minimisation and purpose limitation: patient images stay where they were collected and only model updates leave",
         "It makes the hospitals exempt from the Act",
         "It removes the need for patient consent and security at the hospitals",
         "It guarantees the model cannot leak any patient data"], 0,
        "Helpful, not a free pass.",
        "Keeping data local reduces what is transferred and stored centrally, which supports minimisation. The hospitals are still data fiduciaries with duties (consent, security safeguards, breach reporting), and updates can still leak without DP or secure aggregation.",
        topic="threats", level=3),

    # ------------------------------------------------------------------ L4
    out("""import numpy as np
w = np.array([0.50, 0.30, 0.12, 0.08])   # FedAvg weights, operator A dominates
capped = np.minimum(w, 0.35)              # cap any client at 0.35 ...
renorm = capped / capped.sum()            # ... then renormalise once
print(np.round(renorm, 3).tolist(), bool(renorm.max() <= 0.35))""",
        ["[0.412, 0.353, 0.141, 0.094] False", "[0.35, 0.3, 0.12, 0.08] True",
         "[0.412, 0.353, 0.141, 0.094] True", "[0.35, 0.35, 0.15, 0.15] True"], 0,
        "Capping removed 0.15 of weight; renormalising hands it back to everyone, A included.",
        "After the cap the weights sum to 0.85; dividing by 0.85 pushes A back to 0.412, above the cap, and B over it too. Correct capping is iterative (fix the capped clients at the cap, renormalise only the rest) or caps the shares after renormalising. A one-line 'cap and renormalise' is the bug.",
        topic="fl-challenges", level=4),
    mcq("Operator D (rural, 8% of the data) is honest but unusual; one other operator starts sending random-noise updates. Which aggregation design best handles both?",
        ["Use norm clipping plus a coordinate-wise median or trimmed mean (random noise is easy to cut), and track each client's update direction over rounds so a consistently different but stable client like D is not treated as an attacker",
         "Krum with f = 1, keeping one update per round",
         "Plain FedAvg, since D's weight is small anyway",
         "Expel the two clients with the most unusual updates each round"], 0,
        "Random noise is loud and inconsistent; D is different but consistent.",
        "Noise has a large norm and a random direction round to round; D's updates differ from the majority but agree with themselves over time. Clipping + median-style aggregation removes the noise; reputation over rounds (and possibly personalisation layers for D) protects the honest minority. Krum with 4 clients has no guarantee and keeps only one update.",
        topic="byzantine", level=4),
    out("""sigma, C = 1.1, 1.0          # DP noise multiplier and clip norm
for clients in (20, 4):
    print(clients, round(sigma * C / clients, 3))   # noise std on the average""",
        ["20 0.055\n4 0.275", "20 0.275\n4 0.055", "20 1.1\n4 1.1", "20 0.055\n4 0.055"], 0,
        "The noise is added once to the sum, then divided by the number of clients.",
        "With 20 clients per round the noise on the averaged update has std 0.055; with only 4 banks it is 0.275, five times larger relative to the signal. Central DP is cheap for cross-device FL (thousands of phones) and expensive for small cross-silo federations, which is why banks often combine secure aggregation with a modest ε or record-level DP inside each bank.",
        topic="dp-crypto", level=4),
    mcq("A competitor buys your smart camera, dumps its flash and finds model.tflite in plain form. Which protection actually addresses this?",
        ["Encrypt the model at rest with a device-unique key held in a secure element or TEE, decrypt only inside the TEE, and enable flash read-out protection",
         "Rate limiting the camera's API",
         "Returning only top-1 labels",
         "Renaming the file to something less obvious"], 0,
        "This attacker never sends a query.",
        "Query-side defences do not apply to white-box theft from the hardware. Encryption at rest with a key the attacker cannot extract (secure element, TEE, fused keys) plus debug and read-out protection is the answer. If the model is decrypted into normal RAM, a determined attacker can still dump it there, which is why sensitive inference runs in the TEE.",
        topic="model-extraction", level=4),
    mcq("Why must the papers' three extraction defences be deployed simultaneously rather than picking the best one?",
        ["Each fails alone: rate limits are beaten by many accounts, output hardening by label-only attacks with more queries, and watermarking acts only after the theft",
         "Because one defence is too cheap to be credible",
         "Because regulators require exactly three",
         "They must not be combined, since they interfere with each other"], 0,
        "Think about how an attacker beats each layer on its own.",
        "Defence in depth: layer 1 raises cost and detects, layer 2 lowers information per query (so layer 1's limits bite harder), layer 3 converts a successful theft into evidence and legal risk. Together they make extraction slow, expensive, detectable and provable.",
        topic="model-extraction", level=4),
    mcq("A TrustZone-protected model runs inference on a shared SoC. A researcher recovers parts of it by measuring timing and cache behaviour from the normal world. What does this show?",
        ["TEEs isolate memory, but side channels (timing, cache, power) can still leak secrets; constant-time code, cache partitioning and limiting query access are needed",
         "TrustZone was not enabled",
         "The model was not encrypted at rest",
         "TEEs leak everything and are useless"], 0,
        "Isolation is not the same as invisibility.",
        "Shared caches and timing are observable from outside. TEEs raise the bar a lot but are not unbreakable; the threat model must include side channels, especially when the attacker owns the device.",
        topic="tee-secure-boot", level=4),
    mcq("A model-decryption key should be released only to cameras running genuine firmware. Which flow achieves this?",
        ["The camera boots with secure/measured boot, sends a signed attestation of its measurements, and the key server releases the key (wrapped for that device) only if they match known-good values",
         "Every camera downloads the key at boot over TLS",
         "The key is hard-coded in the firmware",
         "The installer emails the key to the site"], 0,
        "Identity says who; attestation says what state.",
        "A valid certificate on a device running tampered firmware is still a compromised device. Attestation binds the key release to a measured, known-good software state, and wrapping the key for the device's own public key means it is useless if copied.",
        topic="identity-trust", level=4,
        diagram="""
 camera: measured boot -> quote(measurements) signed
         by hardware key  ----------->  verifier
 verifier: measurements == known-good?
     yes -> key wrapped for this device
     no  -> refuse, flag device
"""),
    tf("If all edge-to-cloud traffic uses mutual TLS, a device whose firmware has been compromised cannot send poisoned data or updates.", False,
       "What does mTLS authenticate: the device's identity or its honesty?",
       "mTLS proves the message came from a device holding a valid key; a compromised device still holds that key. Protection against a malicious insider needs attestation, robust aggregation, anomaly detection on its data and fast revocation.",
       topic="secure-comms", level=4),
    mcq("The intermediate CA that signed 50,000 devices' certificates at one factory is found to be compromised. What should the fleet design have made possible?",
        ["Revoke that intermediate CA, re-provision only the devices it signed (with new keys or certificates via an authenticated renewal path), while the offline root and other factories' CAs stay trusted",
         "Nothing: a CA compromise requires replacing every device",
         "Keep using it, since the devices themselves were not stolen",
         "Disable TLS until new hardware arrives"], 0,
        "Why do PKIs use an offline root and several intermediates?",
        "A hierarchy (offline root in an HSM, per-factory or per-batch intermediates) limits blast radius. Devices that support certificate renewal over an attested, authenticated channel can be re-issued in the field. Designing that renewal path before launch is what separates a bad week from a recall.",
        topic="identity-trust", level=4,
        diagram="""
 root CA (offline, HSM)
   +-- factory-1 intermediate  (compromised: revoke)
   |     +-- 50,000 devices -> re-issue
   +-- factory-2 intermediate  (still trusted)
"""),
    mcq("A model is attacked with a backdoor: a small sticker on a parcel makes the sorter output 'priority'. The attacker was one FL client. Overall accuracy is unchanged. Which combination is most effective?",
        ["Clip update norms and add small DP noise during aggregation (weakens the backdoor), plus test the global model on trigger-style probes before each release",
         "Only check overall accuracy, which is unchanged so the model is fine",
         "Switch to unweighted averaging",
         "Return top-1 labels from the API"], 0,
        "A backdoor hides inside normal accuracy.",
        "Backdoors are designed to leave clean accuracy intact, so accuracy checks miss them. Norm clipping limits how much one client can inject, small noise erases fragile backdoor directions, and targeted probes catch known trigger styles. API output hardening is a different threat.",
        topic="byzantine", level=4),
    out("""x = [5, 3, 7]                          # each client's private value
m = {(0, 1): 4, (0, 2): -2, (1, 2): 6}  # pairwise masks agreed by client pairs
sent = []
for i in range(3):
    y = x[i] + sum(v for (a, b), v in m.items() if a == i) \\
             - sum(v for (a, b), v in m.items() if b == i)
    sent.append(y)
print(sent, sum(sent))""",
        ["[7, 5, 3] 15", "[5, 3, 7] 15", "[7, 5, 3] 23", "[9, 1, 5] 15"], 0,
        "Client i adds masks it shares with higher-numbered clients and subtracts those with lower-numbered ones.",
        "Client 0 sends 5 + 4 - 2 = 7, client 1 sends 3 + 6 - 4 = 5, client 2 sends 7 + 2 - 6 = 3. Each sent value looks random, yet the masks cancel in the sum: 15 = 5 + 3 + 7. That is the core of secure aggregation; real protocols add secret-shared mask recovery for clients that drop out mid-round.",
        topic="dp-crypto", level=4,
        diagram="""
 client 0: 5 + m01 + m02      = 7
 client 1: 3 - m01 + m12      = 5
 client 2: 7 - m02 - m12      = 3
 server:   7 + 5 + 3 = 15  (masks cancel)
"""),
    mcq("In cross-device FL on 2 million phones, one heavy user contributes 5,000 keyboard samples. Why do practitioners prefer user-level DP (clip each device's whole update) over record-level DP?",
        ["Record-level DP protects one sample, but this user's 5,000 samples together could still be revealed; clipping per device bounds the whole user's influence",
         "Record-level DP needs more devices",
         "User-level DP needs no noise",
         "They are the same thing"], 0,
        "What is the unit you are promising to protect: a sentence or a person?",
        "The privacy unit should be the person. With record-level DP the guarantee degrades with the number of records a person contributes (group privacy). DP-FedAvg clips each device's full update, so ε applies to everything one user did.",
        topic="dp-crypto", level=4),
    mcq("Four cooperative banks use trimmed mean with beta = 1 against one possible attacker. What is the hidden cost?",
        ["In every coordinate it discards the highest and lowest of only four values, so half the information is thrown away each round, including honest Bank A's extreme but genuine values",
         "None: trimmed mean only removes attackers",
         "It doubles the attacker's influence",
         "It cannot run with an even number of clients"], 0,
        "With n = 4 and beta = 1, how many values survive per coordinate?",
        "Only the middle two of four values are averaged: effectively a median. Honest clients whose data is distinctive (non-IID) will often be at the extremes and get trimmed, slowing convergence and erasing their pattern. With few clients, robustness is expensive.",
        topic="byzantine", level=4),
    fill("An attacker who creates many fake accounts to stay under a per-account rate limit is running a ____ attack (one word).", "Sybil",
         "Named after a book about a woman with many identities.",
         "A Sybil attack defeats per-identity limits. Defences: tie accounts to verified identities or payment, rate-limit by device/IP/organisation as well, and detect coordinated query patterns across accounts.",
         topic="model-extraction", level=4),
    mcq("Non-IID clients make plain FedAvg drift. What does FedProx change to help?",
        ["Each client's local loss adds a proximal term (mu / 2) ||w - w_global||^2 that keeps its local model near the global one",
         "The server ignores clients with unusual data",
         "Clients share a small amount of raw data with each other",
         "Each client trains for more local epochs"], 0,
        "Keep local training on a leash.",
        "The proximal term penalises wandering far from the current global model during local epochs, so heterogeneous clients cannot drift as much. More local epochs make drift worse; sharing raw data breaks the premise of FL.",
        topic="fl-challenges", level=4,
        analogy="Like rebasing a long-lived feature branch often, so it never drifts too far from main to merge cleanly."),
    mcq("A field-service team wants to apply 'zero trust' to an edge fleet on a factory network. What does that mean in practice?",
        ["No device or service is trusted because of where it sits on the network; every connection is authenticated (mTLS), authorised per request, short-lived credentials are used and device health is checked",
         "No one is allowed to access the devices at all",
         "The factory firewall is removed and nothing replaces it",
         "Trust devices on the factory VLAN and verify only internet traffic"], 0,
        "'Inside the network' is not a credential.",
        "Zero trust replaces perimeter trust with per-connection identity and policy. On the edge, a compromised device on the same VLAN should gain nothing it would not gain from the internet. Attestation adds the 'device health' signal.",
        topic="identity-trust", level=4,
        analogy="Like moving from a VPN where everything inside is trusted to per-request authentication for every service."),

    # ------------------------------------------------------------------ more practice (mixed levels)
    out("""import numpy as np
U = np.array([[0.20, 0.10], [0.22, 0.12], [0.18, 0.09],
              [0.60, -0.40], [0.21, 0.11]])   # 5 clients, 2 parameters
print(np.median(U, axis=0).tolist())""",
        ["[0.21, 0.1]", "[0.282, 0.004]", "[0.2, 0.1]", "[0.6, -0.4]"], 0,
        "Sort each column separately and take the middle value.",
        "Column 0 sorted: 0.18, 0.20, 0.21, 0.22, 0.60 -> 0.21. Column 1: -0.40, 0.09, 0.10, 0.11, 0.12 -> 0.10. The plain mean would be [0.282, 0.004], dragged by client 3. 'Coordinate-wise' means each parameter gets its own median, so the result may not equal any single client's update.",
        topic="byzantine", level=2),
    out("""w_global = 1.0
n      = [5_000, 3_000, 2_000]
deltas = [0.2, -0.1, 0.4]          # w_k - w_global after local training
N = sum(n)
w_new = w_global + sum(nk / N * d for nk, d in zip(n, deltas))
print(round(w_new, 3))""",
        ["1.15", "1.167", "0.15", "1.5"], 0,
        "Weighted average of the changes, added to the old model.",
        "0.5(0.2) + 0.3(-0.1) + 0.2(0.4) = 0.10 - 0.03 + 0.08 = 0.15, so w = 1.15. Averaging deltas and adding them is identical to averaging the new weights (Σ (n_k/N) w_k), because the weights sum to 1. The plain mean of the deltas would give 1.167.",
        topic="fedavg", level=3),
    out("""n = [12_000, 9_000, 6_000, 3_000]      # four hospitals
full = [round(k / sum(n), 3) for k in n]
left = n[:3]                            # hospital D drops out this round
part = [round(k / sum(left), 3) for k in left]
print(full, part)""",
        ["[0.4, 0.3, 0.2, 0.1] [0.444, 0.333, 0.222]",
         "[0.4, 0.3, 0.2, 0.1] [0.4, 0.3, 0.2]",
         "[0.25, 0.25, 0.25, 0.25] [0.333, 0.333, 0.333]",
         "[0.4, 0.3, 0.2, 0.1] [0.5, 0.3, 0.2]"], 0,
        "N is the total of the clients that actually reported this round.",
        "With all four, weights are 0.4/0.3/0.2/0.1. If D drops out (a straggler or offline device), N becomes 27,000 and the others become 0.444/0.333/0.222. Keeping D's 0.1 'reserved' would shrink the update. Stragglers are a normal FL system challenge, especially cross-device.",
        topic="fedavg", level=3),
    out("""n = [40_000, 25_000, 20_000, 15_000]   # banks A-D
fraud_rate = [0.05, 0.01, 0.01, 0.01]   # A sees UPI social-engineering fraud
cases = [k * r for k, r in zip(n, fraud_rate)]
print(round(sum(cases) / sum(n), 3), round(cases[0] / sum(cases), 3))""",
        ["0.026 0.769", "0.02 0.4", "0.026 0.4", "0.05 0.769"], 0,
        "Fraud cases per bank, then pooled rate and A's share of all fraud cases.",
        "Cases: 2,000 + 250 + 200 + 150 = 2,600 out of 100,000, a pooled rate of 2.6%. Bank A holds 40% of the data but 77% of the fraud examples. This is label-distribution skew, a form of non-IID data: if A is down-weighted or trimmed by a robust rule, the federation loses most of its fraud signal.",
        topic="fl-challenges", level=3),
    out("""from statistics import median
q = {"partner1": 120, "partner2": 3_400, "partner3": 95, "partner4": 140}
m = median(q.values())
flagged = [k for k, v in q.items() if v > 10 * m]
print(m, flagged)""",
        ["130.0 ['partner2']", "130 ['partner2']", "939 ['partner2']", "130.0 []"], 0,
        "Median of four values is the mean of the middle two.",
        "Sorted counts: 95, 120, 140, 3,400; median (120 + 140) / 2 = 130.0, threshold 1,300, so only partner2 is flagged. Using the median, not the mean (939), keeps the attacker from inflating the baseline. Real detectors also look at input diversity and perturbation patterns, not only volume.",
        topic="model-extraction", level=3),
    out("""days_left = [400, 25, 3, 90, -2, 31]     # device certificate expiry
soon = sum(1 for d in days_left if 0 <= d <= 30)
expired = sum(1 for d in days_left if d < 0)
print(soon, expired)""",
        ["2 1", "3 1", "2 0", "3 0"], 0,
        "Count 0-30 days, then below 0.",
        "Two certificates (25 and 3 days) need renewal within 30 days and one has already expired, so that device cannot connect over mTLS. Expired device certificates are a common cause of 'the fleet went offline on Monday' incidents; monitor them like any other SLO.",
        topic="identity-trust", level=2),
    mcq("What does TLS between a gateway and the cloud NOT protect?",
        ["Data stored on the gateway's disk, and anything an attacker does after taking over the gateway",
         "Readings while they travel over the internet",
         "The integrity of messages in transit",
         "The server's identity, checked through its certificate"], 0,
        "TLS is for data in motion.",
        "TLS covers confidentiality, integrity and server authentication in transit. Data at rest needs disk or file encryption; a compromised endpoint sends whatever it likes over a perfectly valid TLS session.",
        topic="secure-comms", level=2),
    tf("A small printed sticker that makes a camera model misclassify a stop sign is an example of an adversarial input attack at inference time.", True,
       "The model was not changed; the input was.",
       "Adversarial patches and perturbations attack inference. They differ from poisoning (corrupting training or updates) and from extraction (stealing the model). Edge cameras are exposed because attackers control the physical scene.",
       topic="threats", level=2),
    mcq("Which statement about cross-silo vs cross-device federated learning is correct?",
        ["Cross-silo has a few reliable organisations with large datasets (banks, hospitals); cross-device has thousands to millions of unreliable phones or sensors, each with little data",
         "Cross-silo uses phones; cross-device uses banks",
         "Only cross-device FL uses FedAvg",
         "Cross-silo FL needs no security because the parties trust each other"], 0,
        "The papers' four banks are which kind?",
        "The exam's banks and operators are cross-silo: few clients, all participate every round, strong identities. Cross-device has client sampling, dropouts and tiny per-client data, which changes how DP noise, stragglers and robustness behave.",
        topic="fl-basics", level=2),
    fill("A tamper-resistant chip on an IoT board that stores the device's private key so it can never be read out is called a secure ____.", "element",
         "Two words: secure ...",
         "A secure element (e.g. ATECC608-class chips) or a TPM generates and keeps keys inside; the main processor asks it to sign, but never sees the private key.",
         topic="identity-trust", level=3),
    tf("Running inference on the device instead of in the cloud removes the need to secure the model, because nobody outside can reach it.", False,
       "Who holds the device?",
       "Edge inference reduces data exposure on the network, but it moves the model onto hardware the attacker may own. The model file, keys and debug ports now need protection that the cloud gave for free.",
       topic="threats", level=2,
       analogy="Like shipping your backend logic inside a mobile app: no network call to intercept, but anyone can decompile the APK."),
    tf("In federated learning, stragglers (slow or offline clients) are mainly a cross-device problem, which servers handle by sampling clients each round and aggregating whoever reports before a deadline.", True,
       "Millions of phones are never all online at once.",
       "Cross-device FL picks a sample of available devices per round and closes the round at a deadline; late updates are dropped and N is the total of those who reported. In the papers' four-bank setting all clients usually report.",
       topic="fl-challenges", level=3),
    tf("Measured boot records a hash of each stage into a TPM or TEE for later attestation, whereas secure boot refuses to run a stage whose signature fails.", True,
       "One logs, one blocks.",
       "Secure boot enforces locally; measured boot produces evidence (PCR values) a remote verifier can check. Devices often use both: block known-bad code, and prove to the cloud exactly what booted.",
       topic="tee-secure-boot", level=3),
    tf("Using MQTT over TLS on port 8883 with a username and password shared by every device in the fleet gives each device its own identity.", False,
       "Encrypted channel, but whose credentials?",
       "TLS encrypts the session, but a shared password means the broker cannot tell devices apart, cannot revoke one and loses everything when one device is dumped. Use per-device client certificates (mTLS) or per-device tokens.",
       topic="secure-comms", level=2),
    fill("The FL algorithm that adds a proximal term to each client's local loss, so non-IID clients cannot drift far from the global model, is called ____ (one word).", "FedProx",
         "Fed + the first four letters of 'proximal'.",
         "FedProx (Li et al. 2020) generalises FedAvg with a (mu / 2) ||w - w_global||^2 penalty and tolerates clients doing different amounts of local work. With mu = 0 it is plain FedAvg.",
         topic="fl-challenges", level=3),
    fill("ARM's TEE technology, which splits the processor into a secure world and a normal world, is called ARM ____ (one word).", "TrustZone",
         "Trust + Zone.",
         "ARM TrustZone exists on Cortex-A (application processors) and, as TrustZone-M, on Cortex-M33/M55 microcontrollers, so even MCU-class edge devices can keep keys and model decryption in a secure world.",
         topic="tee-secure-boot", level=2),
]
