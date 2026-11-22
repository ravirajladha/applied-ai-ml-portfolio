# Quantum Machine Learning (AIMLC ZG545) — Study spec

> How qubits, quantum circuits and data encoding can be used as machine-learning models (variational circuits, quantum kernels, hybrid quantum–classical networks), and an honest look at when that is worth it. · Status: spec only (not built yet)

---

## 1. What it is and why an AI engineer should care

Quantum computers manipulate **qubits**, which can hold a weighted mix (superposition) of 0 and 1 and can be linked (entangled), so n qubits describe a 2ⁿ-dimensional state.
This course teaches the maths (complex vector spaces, tensor products, bra-ket notation, unitary operations), the circuit model (gates, measurement), how to **encode classical data into quantum states**, and then three families of quantum ML models: **variational quantum circuits** (circuits with trainable angles, trained like neural nets), **quantum kernels** (quantum feature maps plugged into a classical SVM), and **hybrid quantum–classical networks**; it ends with quantum RL and research frontiers.
Labs run on simulators (Qiskit, PennyLane), so a laptop is enough.
For an AI engineer the honest takeaway is: today's NISQ hardware (noisy, small) gives no proven advantage on ordinary business data; the value is in understanding the field well enough to evaluate claims and to recognise the familiar ML ideas (kernels, gradients, overfitting) in a new setting.

**Job relevance: 1/5** — very few roles outside quantum-computing companies and research labs; useful mainly for consulting-style "should we invest in quantum?" evaluations.

---

## 2. Sources in this folder

| Kind | File (relative path) | Notes |
|---|---|---|
| Handout (older batch) | `handouts/Older batch - Quantum Machine Learning (S2-25_AIMLCZG545) COURSE HANDOUT.docx` | Version 3 by Prof. Neha (6-Mar-2026), Second Semester 2025-26; lead instructor Prof. Neha Vinayak; 10 topics, 16 contact sessions (CS), 7 labs, 6 case studies |

**Gaps:** handout only, older batch. No slides, past papers, lab sheets (handout says "TBD") or books (T1 Schuld & Petruccione, *Machine Learning with Quantum Computers*, 2021; T2 Wong, *Introduction to Classical and Quantum Computing*, 2022). Credit model: not stated. The midsem syllabus line is garbled ("Contact Hours: 1 to 16 (or) 1 to 5"); the plan puts the midsem review at CS 8, so CS 1–7 is the likely scope. Hours per session: not stated.

---

## 3. Running scenario

**LedgerGuard** is a fintech that flags fraudulent card transactions. Its board has read that "quantum ML will transform fraud detection" and asks the ML team for a proof-of-concept and a straight answer. (The handout's case study 2 is exactly this problem.)
Data: a small, public, imbalanced fraud dataset (e.g. the Kaggle credit-card PCA features) reduced to 2–4 features and a few hundred rows, because simulators only handle a handful of qubits.
The goal: build a quantum-kernel SVM, a variational classifier and a hybrid network on the same data, compare them honestly to a classical SVM / logistic regression baseline, and write a one-page recommendation covering accuracy, cost, noise and scalability.
Each module adds one piece of that PoC.

---

## 4. Module map

Module names from the handout's Modular Content Structure; sessions from Part B (CS 8 midsem review, CS 16 compre review).

### M1 · Introduction to Quantum Machine Learning (≈ CS 1–2)

Topics: overview of ML paradigms; motivation for quantum ML; limitations of classical hardware for ML; quantum ML solutions; toy example: squared-distance classifier, interference with the Hadamard transformation, quantum squared-distance classifier, insights.

| Concept | One-line definition | Analogy |
|---|---|---|
| Qubit | A unit of quantum information that is a weighted mix of 0 and 1 until measured | A coin spinning in the air, not yet heads or tails |
| Measurement | Reading a qubit, which returns 0 or 1 with probabilities from its amplitudes | Sampling from a distribution, which also collapses it |
| Interference | Amplitudes add or cancel, steering probability toward the right answer | Noise-cancelling headphones |
| Hadamard gate | Turns a definite 0/1 into an equal mix, or back | A 50/50 load balancer that can also merge streams |
| Squared-distance classifier | Label a point by its (weighted) distance to training points; done here with interference | k-NN using one distance score |

Diagram ideas: classical vs quantum workflow; the toy classifier circuit with Hadamard interference; hype vs evidence ladder.
Scenario step: LedgerGuard's team learns what QML claims to offer before building anything.
Notebook idea: compute the classical squared-distance classifier in numpy, then simulate the Hadamard-interference version with a 2–3 qubit PennyLane circuit and compare predictions. Needs `pennylane` (pip; laptop simulator).
Production angle: IBM Quantum, Amazon Braket, cloud simulators. **Breaks:** marketing claims of "exponential speed-up" that ignore data-loading cost.

### M2 · Machine Learning Principles for Quantum Models (≈ CS 3)

Topics: the learning problem (data, model, loss); risk minimisation and generalisation; kernel methods; neural networks and optimisation.

| Concept | One-line definition | Analogy |
|---|---|---|
| Empirical risk minimisation | Pick the model that minimises average loss on training data | Tuning config to pass the test suite |
| Generalisation | Doing well on new data, not just training data | Working in production, not only in CI |
| Kernel | A similarity function between two inputs, equal to a dot product in some feature space | A similarity score from a search engine |
| Gradient-based optimisation | Adjust parameters step by step in the direction that reduces loss | Hill-descending with small steps |

Diagram ideas: data → model → loss loop; kernel as "map to bigger space then dot product".
Scenario step: LedgerGuard fixes the classical baseline and evaluation protocol before any quantum work.
Notebook idea: logistic regression and RBF-SVM baselines on the reduced fraud data with sklearn; record precision/recall/F1 on the fraud class. Laptop.
Production angle: the baseline is the product today. **Breaks:** comparing a quantum model to a weak baseline.

### M3 · Mathematical Foundations for Quantum Machine Learning (≈ CS 4)

Topics: Hilbert spaces; complex vector spaces; tensor products; bra-ket notation; unitary transformations.

| Concept | One-line definition | Analogy |
|---|---|---|
| State vector | A list of complex amplitudes whose squared sizes sum to 1 | A probability table with signed, complex entries |
| Bra-ket notation | \|ψ⟩ is a column vector, ⟨ψ\| its conjugate row; ⟨φ\|ψ⟩ is their overlap | Shorthand syntax for vectors and dot products |
| Tensor product | Combine systems: n qubits give a 2ⁿ-long state vector | Cartesian product of two tables |
| Unitary matrix | A reversible operation that preserves total probability | A lossless, invertible transform |
| Hilbert space | The complex vector space where quantum states live, with an inner product | The schema all states conform to |

Diagram ideas: tensor product growth 2 → 4 → 8 → 2ⁿ; unitary as rotation preserving vector length.
Scenario step: the team learns why 4 features may need few qubits but exponentially large state vectors.
Notebook idea: numpy-only: build \|0⟩, \|1⟩, Hadamard and CNOT matrices, take tensor products, assert unitarity (U†U = I), create a Bell state (handout Lab 1 topic). Laptop.
Production angle: simulators are just big complex linear algebra. **Breaks:** classical simulation memory doubles per qubit (~30 qubits ≈ 16 GB at complex128).

### M4 · Quantum Foundations for Machine Learning (≈ CS 5)

Topics: quantum information theory; qubits; quantum circuits and gates; single-qubit gates (Pauli, Hadamard, rotation); multi-qubit gates (CNOT, controlled operations); circuit model.

| Concept | One-line definition | Analogy |
|---|---|---|
| Bloch sphere | Picture of one qubit's state as a point on a sphere | A 3D dial for a single qubit |
| Pauli gates X, Y, Z | Basic flips/phase flips of a qubit | Bitwise NOT and sign flip |
| Rotation gates RX, RY, RZ | Rotate a qubit by a chosen angle; angles become trainable parameters | A knob with a tunable setting |
| CNOT | Flip the target qubit only if the control qubit is 1; creates entanglement | A conditional write |
| Entanglement | Qubits whose outcomes are correlated beyond any classical explanation | Two replicas that always agree when read |
| Expectation value | Average measurement outcome over many shots | Mean of a metric over many samples |

Diagram ideas: Bloch sphere with RY rotation path; circuit diagram H → CNOT making a Bell state; shots histogram.
Scenario step: the team builds the gate vocabulary its models will use.
Notebook idea: Qiskit/PennyLane: rotate a qubit with RY(θ), plot ⟨Z⟩ vs θ; build a Bell state and check correlations over 1,000 shots (handout Lab 2). Needs `qiskit` or `pennylane`; laptop.
Production angle: transpilation to hardware-native gates. **Breaks:** circuits deeper than hardware coherence time become noise.

### M5 · Data encoding and Representation in Quantum systems (≈ CS 6–7)

Topics: basis encoding; amplitude encoding; time-evolution (angle/rotation) encoding; Hamiltonian encoding; encoding binary inputs into basis states; arbitrary state preparation for amplitude encoding; encoding inputs as time evolutions; encoding a dataset via the Hamiltonian; data encoding as a feature map.

| Concept | One-line definition | Analogy |
|---|---|---|
| Basis encoding | Write a bit string directly as qubit 0s and 1s | Storing a binary ID |
| Angle encoding | Each feature sets a rotation angle on one qubit | One feature per dial |
| Amplitude encoding | Pack 2ⁿ normalised features into the amplitudes of n qubits | Extreme compression with an expensive load step |
| Hamiltonian encoding | Data defines the "energy" operator that evolves the state | Data becomes the program |
| Feature map | The encoding seen as a map from input x to a quantum state | Feature engineering, but into quantum space |
| Data-loading bottleneck | Preparing arbitrary states can cost as much as the computation saved | Network transfer dominating compute time |

Diagram ideas: same 4-feature row as basis / angle / amplitude circuits with qubit and depth counts; feature map x → \|φ(x)⟩.
Scenario step: LedgerGuard chooses how its 4 transaction features enter the circuit.
Notebook idea: PennyLane `AngleEmbedding` vs `AmplitudeEmbedding` vs basis encoding; compare qubit count and circuit depth (handout Lab 3). Laptop.
Production angle: encoding choice dominates resource cost. **Breaks:** amplitude encoding needs normalisation; scale information is lost if not handled.

### M6 · Variational Quantum Circuits as Machine Learning Models (≈ CS 9–10)

Topics: deterministic and probabilistic quantum models; variational quantum classifiers; variational quantum generators (Born machine); expressibility; gradients of quantum computations; parameter-shift rules; barren plateaus and trainability; quantum circuits and neural networks.

| Concept | One-line definition | Analogy |
|---|---|---|
| Variational circuit / ansatz | A circuit with trainable rotation angles, a fixed layout chosen by the designer | A neural-net architecture whose weights are angles |
| Variational quantum classifier (VQC) | Encode x, apply ansatz, measure, map expectation to a class | Logistic regression with a quantum feature layer |
| Born machine | A circuit whose measurement probabilities form a generative model | Sampling from a learned distribution |
| Parameter-shift rule | Exact gradient by running the circuit at θ ± π/2 and differencing | Finite difference with an exact formula |
| Barren plateau | Gradients vanish exponentially with qubits/depth, so training stalls | Vanishing gradients, but worse |
| Expressibility | How much of the state space the ansatz can reach | Model capacity |

Diagram ideas: VQC pipeline (encode → ansatz layers → measure → loss → optimiser loop); parameter-shift two-evaluation diagram; gradient variance vs qubit count plot.
Scenario step: LedgerGuard trains a VQC fraud classifier and checks if it beats the baseline.
Notebook idea: PennyLane VQC on the reduced fraud data; implement the parameter-shift rule by hand and assert it matches autodiff and beats finite differences in accuracy; plot gradient variance vs qubits (handout Labs 4–5). Laptop simulator.
Production angle: PennyLane, Qiskit Machine Learning. **Breaks:** barren plateaus; shot noise makes gradients noisy and training expensive.

### M7 · Hybrid Quantum-Classical Models (≈ CS 11–12)

Topics: hybrid architectures; quantum layers in deep-learning pipelines; training hybrid models; hardware-aware training; noise and NISQ constraints; hybrid QNNs: circuit-based QNNs, data re-uploading QNNs, quantum CNNs, expressive design choices, applications; Quantum Approximate Optimization Algorithm (QAOA).

| Concept | One-line definition | Analogy |
|---|---|---|
| Hybrid model | Classical layers and a quantum circuit layer trained together | A microservice call inside a monolith |
| NISQ | Noisy Intermediate-Scale Quantum: today's small, error-prone hardware | Early beta hardware with flaky results |
| Data re-uploading | Encode the input several times between trainable layers to boost expressiveness | Feeding context again at each layer |
| Quantum CNN | Circuit with convolution-like and pooling-like qubit layers | CNN structure in circuit form |
| Hardware-aware training | Design circuits to match the device's gates, connectivity and noise | Optimising code for a specific CPU |
| QAOA | Alternating problem and mixer circuits tuned to solve combinatorial optimisation | Simulated annealing driven by a circuit |

Diagram ideas: classical NN → quantum layer → classical head; noise-free vs noisy simulator accuracy curves; QAOA layer structure.
Scenario step: LedgerGuard wraps the circuit as a layer inside a small PyTorch network.
Notebook idea: PennyLane `TorchLayer` in a tiny PyTorch model; compare noiseless vs noisy (depolarising) simulator (handout Lab 7). Laptop; CPU only.
Production angle: PennyLane + PyTorch, cloud QPUs via Braket/IBM. **Breaks:** queue times and per-shot cost on real hardware; noise erases gains.

### M8 · Quantum Kernel Methods (≈ CS 13–14)

Topics: quantum feature maps; quantum kernels; RKHS of quantum kernels; kernel-based training; comparison of kernel-based and variational training; regularisation; applications in clustering and combinatorial ML.

| Concept | One-line definition | Analogy |
|---|---|---|
| Quantum kernel | Similarity k(x, x′) = \|⟨φ(x)\|φ(x′)⟩\|², estimated on a quantum device | A similarity score computed by a special co-processor |
| Kernel matrix | All pairwise similarities; a classical SVM trains on it | Precomputed join table |
| RKHS | The function space a kernel defines, where the model lives | The schema of all models the kernel allows |
| Kernel vs variational training | Kernels give a convex problem but cost O(N²) circuit runs; VQCs scale better but are non-convex | Exact batch job vs approximate streaming job |
| Exponential concentration | Kernel values all become near-equal for many qubits, so nothing is learnable | Every search result scoring 0.5 |

Diagram ideas: feature map → overlap circuit → kernel matrix heatmap → SVM; N² cost curve.
Scenario step: LedgerGuard builds the quantum-kernel SVM the board specifically asked about.
Notebook idea: PennyLane feature map + overlap circuit to build a kernel matrix; `sklearn.svm.SVC(kernel="precomputed")`; compare to RBF baseline (handout Lab 6). Laptop.
Production angle: Qiskit Machine Learning `FidelityQuantumKernel`. **Breaks:** O(N²) kernel evaluations limit you to hundreds of samples; kernel concentration.

### M9 · Quantum Reinforcement Learning, and M10 · Research frontiers (≈ CS 15)

Topics: quantum agents; speed-ups in exploration; quantum Markov decision processes; open problems in QML; recent paper discussions; ethical and societal implications.

| Concept | One-line definition | Analogy |
|---|---|---|
| Quantum agent | An RL agent whose policy or value function is a quantum circuit | Swapping the policy network for a circuit |
| Exploration speed-up | Using quantum search ideas to find rewarding actions faster (in theory) | Faster search over a big option space |
| Quantum MDP | An MDP generalised to quantum states and operations | A state machine on quantum states |
| Dequantisation | Classical algorithms later matching a claimed quantum speed-up | A "faster" library beaten by a better classical algorithm |

Diagram ideas: RL loop with a circuit-policy box; claimed-speed-up vs dequantised timeline.
Scenario step: the team writes the final recommendation: where QML might matter later, what to monitor, what not to fund now.
Notebook idea: tiny toy: a 2-qubit circuit policy for a 2-armed bandit trained with parameter-shift gradients. Laptop.
Production angle: research only. **Breaks:** results that don't survive a strong classical baseline.

---

## 5. Codebase plan

`codebase/` — **qml-fraud-poc**: reproducible comparison of classical vs quantum models on the same small dataset. numpy, sklearn, pennylane, torch (CPU); qiskit optional.

```
codebase/
├── README.md                  how to run, module → file map, final verdict table (M1)
├── qmlpoc/
│   ├── data.py                load + PCA-reduce + scale fraud data             (M2)
│   ├── baselines.py           logistic regression, RBF-SVM, metrics            (M2)
│   ├── linalg.py              numpy states, gates, tensor products             (M3)
│   ├── circuits.py            gate helpers, Bell state, expectation values     (M4)
│   ├── encodings.py           basis / angle / amplitude embeddings             (M5)
│   ├── vqc.py                 variational classifier + parameter-shift grads   (M6)
│   ├── hybrid.py              PyTorch model with a quantum layer; noise option (M7)
│   └── qkernel.py             quantum kernel matrix + precomputed SVC          (M8)
├── compare.py                 runs everything, writes results table            (M8, M9–M10)
└── tests/
    ├── test_linalg.py         unitarity, normalisation, Bell correlations      (M3, M4)
    ├── test_encodings.py      qubit counts and state norms                     (M5)
    └── test_gradients.py      parameter-shift = autodiff within tolerance      (M6)
```

---

## 6. Practice topics plan

01 What QML promises: toy interference classifier — M1, M2 — 4 h
02 Linear algebra for qubits — M3 — 5 h
03 Gates, circuits and measurement — M4 — 4 h
04 Data encoding strategies — M5 — 4 h
05 Variational classifiers, parameter-shift and barren plateaus — M6 — 6 h
06 Hybrid quantum–classical networks and NISQ noise — M7 — 4 h
07 Quantum kernels vs classical kernels — M8 — 4 h
08 Quantum RL and research frontiers — M9, M10 — 2 h

---

## 7. Exam signal

No past papers in this folder. Evaluation scheme (older handout):

| Component | Type | Duration | Weight | Date (that term) |
|---|---|---|---|---|
| EC-1 Quiz I | Online | – | 5% | TBA |
| EC-1 Quiz II | Online | – | 5% | TBA |
| EC-1 Assignment / Lab | Offline | – | 20% | TBA |
| EC-2 Mid-semester | Closed book | 1.5 h | 30% | 20-06-2026 |
| EC-3 Comprehensive | Open book | 2.5 h | 40% | 05-09-2026 |

Midsem scope: garbled in the handout; likely CS 1–7 (M1–M5). Comprehensive: all topics. The six handout case studies (QML migration architecture, fraud quantum-kernel SVM, gold-price hybrid model, stock QNN, drug-discovery variational model, healthcare kernel classifier) are a strong hint at open-book design questions, but that is an inference.

---

## 8. Interview angle

1. **What is a qubit vs a bit?** — A bit is 0 or 1; a qubit is a normalised complex mix of both until measured, giving 0 or 1 with set probabilities.
2. **Why can't we just simulate quantum circuits classically?** — State size doubles per qubit; beyond ~40–50 qubits exact simulation becomes infeasible.
3. **What is a variational quantum circuit?** — A parameterised circuit trained by a classical optimiser, used like a neural network layer.
4. **How do you get gradients from a quantum circuit?** — The parameter-shift rule: evaluate at θ ± π/2 and take a scaled difference.
5. **What is a barren plateau?** — Gradients vanish exponentially with circuit size, making training impossible; mitigated by shallow, structured ansätze and good initialisation.
6. **What is a quantum kernel and its main limitation?** — Overlap of encoded states used as an SVM kernel; costs O(N²) circuit runs and can concentrate to uninformative values.
7. **Which encoding would you pick for 4 tabular features and why?** — Angle encoding: 4 qubits, shallow circuit, easy to load; amplitude encoding saves qubits but needs deep state preparation.
8. **Is there a proven quantum advantage for ML on classical business data today?** — No; NISQ noise, data loading and strong classical baselines mean no practical advantage has been shown.
9. **How would you evaluate a vendor's QML pitch?** — Same data, strong classical baseline, fair compute budget, noise-aware results, and total cost including queue and shots.

---

## 9. Repetition plan

| Concept | First met | Revisited in |
|---|---|---|
| State vector / amplitudes | M1 | M3, M4, M5 |
| Unitary gate / rotation | M3 | M4, M6, M7 |
| Measurement and expectation value | M1 | M4, M6, M8 |
| Feature map / encoding | M2 (kernels) | M5, M6, M8 |
| Kernel | M2 | M8 |
| Gradient-based training | M2 | M6 (parameter shift), M7, M9 |
| Noise / NISQ limits | M4 | M6 (shot noise), M7, M10 |
| Classical baseline comparison | M2 | M6, M7, M8, M10 |

---

## 10. Overlap with my other courses

- [../../deep-reinforcement-learning/](../../deep-reinforcement-learning/) — MDPs and policy gradients behind M9 quantum RL.
- [../../artificial-and-computational-intelligence/](../../artificial-and-computational-intelligence/) — optimisation and search background for QAOA (local search, annealing).
- Sibling elective [../computational-learning-theory/](../computational-learning-theory/) — kernels, RKHS and generalisation (M2, M8).
- No real overlap with the LLM, NLP or edge courses.

---

## 11. Build checklist

- [ ] SPEC reviewed
- [ ] cards.json (M1, M2, M3, M4, M5, M6, M7, M8, M9–M10)
- [ ] practice/01 What QML promises
- [ ] practice/02 Linear algebra for qubits
- [ ] practice/03 Gates, circuits and measurement
- [ ] practice/04 Data encoding strategies
- [ ] practice/05 Variational classifiers and parameter-shift
- [ ] practice/06 Hybrid quantum-classical networks
- [ ] practice/07 Quantum kernels
- [ ] practice/08 Quantum RL and research frontiers
- [ ] codebase/ runs + tests

**Total estimated study hours: ≈ 39 h** (33 h practice topics + 6 h codebase).
