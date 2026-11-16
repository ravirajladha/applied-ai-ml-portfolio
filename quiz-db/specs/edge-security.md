# Edge Security & Trust (M7, S13-S14): coverage spec

**Ladder:** Machine Learning on the Edge (AIMLCZG535) › Module 7 Edge Security & Trust   ·   **Prerequisites:** edge-foundations (why privacy pushes inference to the edge), edge-mlops (signed OTA images), llmc-safety and nlpa-ethics (for LLM-side attacks and fairness, not repeated here)
**Why it matters for AI/ML:** An edge model sits on hardware an attacker can hold in their hand, learns from data that legally cannot leave its owner, and answers queries from clients you do not control. Module 7 covers federated learning (FedAvg, non-IID data, poisoning and robust aggregation), differential privacy and encryption, model extraction and its defences, and the device trust stack: identity, attestation, TEEs, secure boot and mutual TLS. The end-sem papers give two 8-mark questions here every time: a four-party FedAvg scenario and a model-extraction defence design.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `threats` | Security and privacy challenges in Edge AI | physical access, data privacy | attack surface: device, model, data, channel | threat model for a deployed fleet, DPDP Act / sector rules | which threat each control addresses, residual risk |
| 2 | `fl-basics` | Federated learning workflow | data stays local, updates travel | rounds: broadcast, local train, upload, aggregate | cross-silo vs cross-device, Flower roles | what FL does and does not protect (gradient leakage) |
| 3 | `fedavg` | FedAvg weighting and the global update | weight = share of data | n_k / N weights, weighted sum of client models | the papers' four-party weights and update expression | weighted vs unweighted averaging, update-delta form |
| 4 | `fl-challenges` | Non-IID data, dominance and FL system challenges | what non-IID means | client drift, minority clients, stragglers | dominance by the largest client and mitigations (caps, FedProx) | fairness vs accuracy, personalisation |
| 5 | `byzantine` | Poisoning / Byzantine attacks and robust aggregation | malicious client | data vs model poisoning, Byzantine noise | Krum, trimmed mean, coordinate-wise median by hand | the tension: robust rules discard honest but unusual clients |
| 6 | `dp-crypto` | Differential privacy, secure aggregation and encryption | DP adds noise, ε | smaller ε = more privacy, clipping + noise | DP-SGD / DP-FedAvg steps, Laplace scale = sensitivity / ε | privacy budget composition, secure aggregation vs DP vs HE |
| 7 | `model-extraction` | Model extraction and model protection | stealing a model by querying | query sweep, full probability vectors | three-layer defence (rate limiting + anomaly detection, output hardening, watermarking/legal) | top-1 vs rounding trade-off, on-device model theft, encrypted models |
| 8 | `identity-trust` | Device identity, authentication and trust management | each device needs an identity | X.509 certificates, per-device keys, provisioning | attestation, revocation, zero trust | fleet-scale key compromise, trust chains |
| 9 | `tee-secure-boot` | TEEs and secure boot | what a TEE is | TrustZone vs SGX, chain of trust | what runs inside a TEE for ML, measured boot | TEE limits (side channels, memory), root of trust in ROM/fuses |
| 10 | `secure-comms` | Secure communication between edge and cloud | TLS encrypts traffic | TLS vs mTLS, MQTT over TLS (8883) | cert rotation, pinning, constrained-device options (DTLS, PSK) | what TLS does not protect |

## Must-know facts
- Edge threats: physical access to devices (dump flash, probe buses), model theft, adversarial inputs, data and model poisoning, eavesdropping on links, spoofed devices, privacy of on-device data (India's DPDP Act 2023, banking/telecom rules).
- Federated learning: data never leaves the client; each round the server broadcasts the global model, clients train locally, and send model updates (weights or gradients/deltas), never raw data. The aggregator cannot see raw data by design, so it cannot inspect it to verify an attack.
- FedAvg: w_global = Σ (n_k / N) · w_k, with N = Σ n_k. Papers: banks 40k/25k/20k/15k -> 0.40/0.25/0.20/0.15; operators 50k/30k/12k/8k -> 0.50/0.30/0.12/0.08.
- Non-IID data (one client's distribution differs, e.g. Bank A's UPI social-engineering fraud, Operator D's rural users): local models drift in different directions, the average converges slowly and may underfit minority patterns.
- Dominance: a client with 0.50 of the weight pulls the global model toward its distribution and is a single point of failure for poisoning. Mitigations: cap per-client weight, clip update norms, FedProx-style regularisation, fairness-aware aggregation.
- Poisoning / Byzantine attacks: crafted (targeted) or random-noise updates. Robust aggregation: Krum (pick the update closest to its n - f - 2 nearest neighbours), coordinate-wise trimmed mean (drop the β largest and smallest per coordinate), coordinate-wise median.
- The tension: robust rules treat outliers as attackers, so they may discard an honest but unusual client (Bank A, Operator D), losing exactly the rare pattern the federation needed.
- Differential privacy: a mechanism is ε-DP if one record's presence changes output probabilities by at most a factor e^ε. Smaller ε = more noise = more privacy, less accuracy. DP-SGD / DP-FedAvg: clip each update's norm to C, then add Gaussian noise scaled to C. Laplace mechanism scale = sensitivity / ε.
- Secure aggregation lets the server see only the sum of updates; homomorphic encryption computes on ciphertexts; DP bounds what the result reveals. They solve different problems and are combined.
- Model extraction: an attacker sweeps the input space and records the full softmax vectors to train a functionally equivalent surrogate (steal IP, avoid paying, then craft adversarial examples offline). Signals: one identity, huge query volume (10,000 in 48 h vs ~50/day), synthetic or systematically perturbed inputs.
- Three-layer defence, deployed together: (1) rate limiting + query-pattern anomaly detection (slows and detects, but sybil accounts evade it), (2) output hardening: top-1 label only or rounded probabilities (cuts the information per query, but a determined attacker can still learn from labels), (3) watermarking + legal terms (proves theft after the fact, does not prevent it).
- Top-1 only removes the confidence signal for everyone (hurts legitimate apps that threshold on confidence); rounding to one decimal keeps a coarse confidence for partners while removing most of the fine-grained gradient-like signal.
- Device identity: a unique key pair per device, private key in a secure element/TPM, X.509 certificate from the fleet CA; mutual TLS authenticates both sides; certificates can be revoked per device.
- Attestation: the device proves to a verifier what software it booted (measurements signed by a hardware key) before it is trusted with data or models.
- TEE: an isolated execution environment (ARM TrustZone secure world on Cortex-A/M; Intel SGX enclaves on x86) that protects code and data, e.g. model weights and decryption keys, from the normal OS.
- Secure boot: an immutable root of trust (boot ROM + key hash in fuses) verifies the bootloader, which verifies the OS/firmware, which verifies the app and model: a chain of trust.
- MQTT over TLS uses port 8883 (1883 is plain). TLS protects data in transit only; it does nothing for a compromised endpoint or for data at rest.

## Common traps (each one must have at least one question)
- "FL sends anonymised data to the server" -> it sends model updates only.
- Unweighted averaging of client models -> FedAvg weights by n_k / N.
- Weights not summing to 1 (arithmetic slip) -> always check Σ = 1.
- "The aggregator can just inspect the suspected bank's data" -> it cannot by design (and legally).
- Robust aggregation assumed free -> it can drop honest minority clients (Bank A / Operator D).
- "Model updates leak nothing" -> gradient inversion and membership inference can recover data; add DP / secure aggregation.
- Larger ε = more privacy -> it is the reverse.
- Adding noise without clipping -> sensitivity is unbounded, so no DP guarantee.
- One defence layer for extraction -> each layer alone fails (sybils, label-only attacks, after-the-fact only).
- Top-1 only "stops the attack" -> it slows it; label-only extraction still works with more queries.
- Watermarking "prevents" theft -> it proves ownership afterwards.
- Signing = encryption, TLS = protection at rest -> different properties.
- Secure boot alone stops runtime attacks -> it verifies what boots, not what happens later.
- A shared fleet-wide key or password -> one dumped device compromises all.
- TEE treated as unbreakable -> side channels and small secure memory limit it.

## Interview angle
1. **"Four hospitals want a joint model but cannot share records. Design it."** Cross-silo FL (e.g. Flower), FedAvg weighted by n_k / N, secure aggregation so the server sees only the sum, DP clipping + noise for formal guarantees, robust aggregation with care for honest minority sites, mTLS between parties.
2. **"Someone is stealing your model through the API. What do you do?"** Detect (rate limits, query-pattern anomaly detection), reduce information (top-1 or rounded scores), deter and prove (watermark, terms of service), and accept no single layer is enough.
3. **"How do you know a device in the field is genuine and unmodified?"** Per-device keys in a secure element, mTLS with a fleet CA, secure boot chain of trust, remote attestation before secrets or models are released, revocation on compromise.
4. **"What does a TEE give an edge ML model?"** Weights and keys decrypted only inside the secure world, inference isolated from the normal OS, attestation of what code runs; limited secure memory and side channels are the catch.

## Source material
- Handout (`edge-src/handout.txt`), Session 13 (R1 Ch 8): security and privacy challenges in Edge AI; federated learning for privacy-preserving training; differential privacy and encryption mechanisms.
- Handout Session 14 (Instructor Supplied Material): secure inference and model protection; authentication and trust management across devices; Trusted Execution Environments (TEE) and secure boot processes; secure communication protocols between edge and cloud.
- Handout lab 7: a simple federated learning setup with Flower or FedML and its privacy implications. LO7: security and privacy mechanisms for trust and compliance.
- Sep 2026 end-sem Set 1 Q2: four banks (40k/25k/20k/15k), FedAvg weights and global update, Bank A's distinctive UPI social-engineering fraud (non-IID), crafted gradient updates (poisoning), two defences and their tension, why the aggregator cannot inspect raw data.
- Sep 2026 end-sem Set 2 Q2: four telecom operators (50k/30k/12k/8k), rural Operator D (non-IID), Operator A's 0.50 weight (dominance risk and a mitigation), random-noise updates (Byzantine), defences vs Operator D.
- Sep 2026 end-sem Set 1 Q4: retail-analytics API, one identity, 10,000 systematic perturbation queries in 48 h vs ~50/day, full softmax recorded: model extraction; three-layer defence; top-1 only effect and cost.
- Sep 2026 end-sem Set 2 Q4: insurance damage-assessment partner API, 25,000 synthetic renders in a week vs a few hundred real photos; rounding probabilities to one decimal vs top-1.
- Exam patterns: FedAvg weights n_k / N shown per client and Σ (n_k / N) w_k; naming non-IID and its effect; naming poisoning/Byzantine attacks with Krum / trimmed mean / median and the honest-outlier tension; "what precisely is transmitted"; identify extraction from log signals, three simultaneous defence layers with why each alone fails, and output-hardening trade-offs. L3/L4 questions here use new parties (cooperative banks, hospitals, dairy unions, discoms, ride-hailing fleets) and numbers.
- **Standard practice (no slides exist):** Session 14 is "Instructor Supplied Material" with no slides in the source set. Krum, trimmed mean and median (Blanchard et al. 2017; Yin et al. 2018), DP definitions and DP-SGD (Dwork; Abadi et al. 2016), secure aggregation (Bonawitz et al. 2017), extraction attacks (Tramèr et al. 2016), TrustZone/SGX, secure boot, remote attestation and mTLS are written from standard references and T1/R1-level material.
- **Course framework reconstructed:** the papers' "three-layer defence" is not named layer by layer in the handout; questions use the layers the papers imply (access control/anomaly detection, output hardening, watermarking/legal) and test the reasoning (each layer covers a gap the others leave), not one exact wording.
- **Gap flagged:** the papers ask for "two defence algorithms" without fixing which; any two of Krum, trimmed mean and coordinate-wise median are treated as correct here.
