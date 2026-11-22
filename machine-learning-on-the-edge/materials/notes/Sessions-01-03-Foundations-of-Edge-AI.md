# Machine Learning on the Edge — Revision notes, Sessions 1–3

**Course:** AIMLC ZG535 · Prof. Sharon Christa · S1-26
**Covers:** Contact sessions 1, 2, 3 (25-Oct, ~8-Nov, 14-Nov-2026) = handout Module 1 "Foundations of Edge AI I & II"
**Built from:** the 3 lecture transcripts, the CS1 slide deck (`materials/handouts/CS1 (1).pptx`), the course handout,
the Chapter 1 study guide PDF (`materials/handouts/Edge_AI_Chapter1_Study_Guide.pdf`) and the past mid-sem papers.

> **How to use this file.** Read §0 first (what is this subject even for?). Then §1–§3 one session at a time.
> §4 shows how the exam actually asks this material, with worked numbers. §5 is the one-page sheet for the night before.

---

## 0. Scope of the subject: what this course is *for*

### 0.1 The one-line version

> **This course is NOT about building ML models. It is about taking a model that's already trained and making it run
> on a small, cheap, battery-powered device that sits right where the data is produced.**

The professor said this in the first 5 minutes of Session 1: *"We are not learning how to design a machine learning model.
What we are learning is how an already built machine learning model can be used in edge devices."*

### 0.2 The SDE analogy (this is the whole subject in one table)

You already know this problem from web/mobile development. Edge AI is the same problem, with models in place of code.

| You know this (SDE) | Edge AI version |
|---|---|
| Your backend runs on a big server; the phone app calls the API | **Cloud AI**: model runs in a data centre, device sends data, waits for the answer |
| Client-side form validation in JavaScript (instant, works offline) | **Edge AI**: model runs *on the device itself* |
| A CDN edge node near the user, between the user and your origin server | **Fog AI**: a middle box (gateway, local server) near many devices |
| Minifying + tree-shaking your JS bundle so it loads on a slow 3G phone | **Model optimisation**: quantization, pruning, distillation, so the model fits in KBs/MBs |
| Building for Android *and* iOS *and* web: different toolchains | **Heterogeneous hardware**: MCU, Raspberry Pi, Jetson, FPGA, each with its own runtime |
| Pushing an app update through the Play Store to 1M phones | **OTA (Over-The-Air) updates**: pushing a new model to 10,000 devices in a forest |
| Production monitoring, alerts when error rate climbs | **Edge MLOps**: monitoring drift on devices you can't SSH into easily |
| Don't log every request to the server; send only errors and metrics | **"Transmit only what matters"**: send the alert, not the raw sensor stream |

### 0.3 The practical applications (where this is used in real life)

You use edge AI every day without noticing:

| Thing you use | What runs on the device | Why not in the cloud |
|---|---|---|
| Phone **face unlock** | Face recognition model | Must be instant, work in airplane mode; your face is biometric data |
| **Instagram/Snapchat filters** | Face tracking on every video frame | Sending 30 frames/second to a server would be too slow (prof's example) |
| **"Hey Google" / "Alexa"** wake word | Tiny keyword-spotting model | Always listening; streaming all audio to the cloud = privacy + battery disaster |
| **Teams/Zoom background blur** | Person segmentation | Video frames don't need to go to a separate server (Session 3) |
| **Noise suppression** on calls | Audio signal processing | The prof's own house-construction noise was removed this way (Session 3) |
| Smartwatch **fall detection / heart alerts** | Anomaly detection on sensor data | Hiker with no signal still needs the alert |
| Car **ABS / pedestrian detection** | Object detection | Cloud round trip = the car has already crashed |

And in industry (the course's running examples):

- **Smart factory / predictive maintenance:** vibration sensors on motors detect a failing bearing *before* it breaks.
  This is *the* example the professor keeps returning to.
- **Wildlife:** smart collars on elephants (OpenCollar Edge), camera traps that only save photos of the target animal.
- **Healthcare:** bedside monitors that raise alarms, low-cost oral-cancer screening devices in villages.
- **Agriculture:** coffee-leaf disease detection on a cheap device a farmer carries (Brazil).
- **Smart cities:** traffic cameras that only report signal-jumpers, not the 98% who follow the rules.
- **Infrastructure:** sensors in fresh concrete that alert if curing is going wrong (prof said this will be an assignment use case).

### 0.4 Why this matters for *your* AI-engineer pivot

This looks like an "IoT hardware" course, but the **middle third of it is exactly what GenAI engineers do**:

- **Quantization** (FP32 → INT8/INT4) is how people run Llama on a laptop with GGUF/llama.cpp, or cut GPU serving cost.
- **Knowledge distillation** is how DistilBERT and small LLMs are made.
- **Small Language Models / on-device LLMs** (Gemini Nano on phones, Apple Intelligence, Phi) are a hot hiring area.
- **Latency / throughput / memory / cost benchmarking** is the daily job of anyone serving models.
- **BLERP** is a good framework for a system-design interview question: "should this model run on-device or server-side?"

### 0.5 The 8 modules, as one pipeline

Think of the course as the life of one model, from "where should it run?" to "is it secure and fast enough?":

```
 M1 Foundations     M2 Hardware        M3 Data & IoT        M4 Lifecycle &       M5 Edge MLOps
 WHY run at edge? → ON WHAT chip?    → HOW does sensor   → HOW to convert &   → HOW to update/monitor
 (BLERP, cloud/     (MCU, Pi, Jetson,   data flow in?        deploy? (TFLite,     10,000 devices? (OTA,
  fog/edge)          TPU, FPGA)         (MQTT, pipelines)    ONNX, TensorRT,      drift, A/B, shadow)
                                                             Docker, Greengrass)
        ─────────────── mid-sem: sessions 1–8 ───────────────┘
 M6 Optimisation          M7 Security & Trust            M8 Benchmarking & Future
 HOW to make it fit?    → HOW to keep it safe?         → HOW to prove it's fast? What's next?
 (quantization, pruning,   (federated learning, DP,       (latency, throughput, power, MLPerf Tiny,
  distillation, NAS,        TEE, secure boot)              TinyML, edge LLMs, swarm AI, green AI)
  MobileNet, TinyBERT)
```

### 0.6 How you're graded (from the handout + Session 1)

| Component | Weight | What | When |
|---|---|---|---|
| EC-1 Quiz | 5 | One online quiz | Opens after next week's class (Session 4, ~week of 21-Nov-2026) |
| EC-1 Lab 1 | 5 | Edge Impulse on your phone (collect data → train → quantize → deploy back to phone) + Exp 1 (TFLite local vs cloud latency) | Opens after webinar 1 |
| EC-1 Lab 2 | 10 | Exp 3 + 4 + 5 combined (MQTT anomaly detection, CNN → TFLite, OTA + drift) | Opens after webinar 3 |
| EC-1 Assignment | 10 | Individual "situated learning": take a real deployed use case, design an architecture, compare with alternatives | Released around contact session 12 |
| EC-2 Mid-sem | 30 | **Closed book**, 2 h, sessions 1–8 | **27-Dec-2026 (AN)** |
| EC-3 Comprehensive | 40 | **Open book** (printed textbook only), 2.5 h, everything | **07-Mar-2027 (AN)** |

- **No hardware needed.** Labs run in Python on your laptop/Colab; the Edge Impulse lab uses your phone.
- **Exam questions are all scenario-based with calculations**, never "define X". See §4.
- Textbook: *AI at the Edge* (Situnayake & Plunkett, O'Reilly 2023): `books/`. The prof also recommends the free
  *Machine Learning Systems* book (volume 1).
- Lab/assignment issues: contact Prof. Amogh (lead faculty).

---

## 1. Session 1 (25-Oct-2026): the vocabulary

### 1.1 Embedded system

**Definition:** a small computer built to do **one specific job** inside a physical device.
Examples: washing-machine controller (water level, wash cycle), car ABS, smartwatch, digital watch, Bluetooth headphones.

| | General-purpose computer (laptop) | Embedded system |
|---|---|---|
| Purpose | Runs many apps; you install software | One dedicated function; firmware fixed |
| RAM / storage | Plenty | Very limited (often KBs) |
| Power | Wall socket | Often battery |
| Compute | Fast CPU, maybe GPU | Slow clock, tiny chip |

> **Constraints to memorise:** limited **memory**, **compute**, **battery/power**. That's why "we cannot just deploy
> large ML models directly on an embedded system", and why this whole course exists.
> Fact on the slide: 28 billion+ microcontrollers shipped in 2020 alone.

### 1.2 IoT, the edge, edge computing, sensors

- **IoT (Internet of Things):** physical objects with **sensors + software + network connection**, so they can collect
  and exchange data. First IoT device (1982): a Coke machine at Carnegie Mellon connected to ARPANET so students could
  check whether it was empty.
- **The edge:** *where the data is produced*, the outer boundary of the network, close to the physical world.
- **Edge device:** any device with a processor at the network's edge (phones, laptops, IoT devices, routers, local switches).
- **Edge computing:** processing and storing data at the edge, near the source, instead of relying entirely on a central server.
  The network is still used, but the heavy work doesn't *depend* on it. Results/alerts go up when connected.
- **Sensor:** a device that measures a physical property (temperature, pressure, humidity, acceleration) and converts it
  into an electrical signal a computer can read. Accelerometer → acceleration, thermometer → temperature.

**How the pieces fit (prof's summary):**
embedded system = the computing hardware · IoT = lets devices exchange data · sensors = give real-world data ·
edge computing = process near the source · **+ AI = the system makes predictions/decisions from that data → Edge AI.**

**The factory story (comes back in every class):** a factory has hundreds of sensors on machines measuring vibration and
temperature. Normally data goes to the cloud. But if the factory's internet is slow or down, nobody detects the fault.
Edge computing: connect a **Raspberry Pi** to the vibration sensor and run the fault-detection model *there*. No internet needed.

### 1.3 AI and ML

- **AI:** a system that does tasks that normally need human intelligence. Slide definition: *"knowing the right thing to
  do at the right time"* (take a photo when the animal enters the frame, brake before a crash, alert when a machine sounds broken).
  Even simple if-else rules can count as "AI". (Slime-mould example: solves a maze with no brain, so intelligence can be narrow.)
- **ML:** one way to build AI. Instead of hand-coding every rule, **train a model on data** so it learns the patterns.

**The four ML words (wristband example):**

| Step | Meaning | Wristband example |
|---|---|---|
| **Collect** | Gather labelled data | Accelerometer logs while athletes run, swim, rest |
| **Train** | Algorithm learns a mapping data → label. The mapping = **the model** | Learns "this motion pattern = running" |
| **Infer** | Use the trained model on new data | New wrist data → predicts "swimming" |
| **Generalize** | Works on data it never saw | Works on a new athlete |

> **Key edge point:** during training the parameters change; during inference they're **fixed**.
> **Training needs far more compute than inference.** So: train on a big machine, infer on the small device.

### 1.4 The normal ML pipeline (prof walked through this)

```
raw data → clean → feature extraction → train → test ──(bad? go back to data)──→ deploy → monitor ─┐
   ↑                                                                                                │
   └──────────────────────────── drift detected → redo ←──────────────────────────────────────────┘
```

- **Clean:** remove noise, duplicates, bad readings (a faulty temperature sensor reporting 90 °C instead of 32 °C).
- **Feature extraction:** turn raw numbers into useful summaries, e.g. raw vibration → **RMS, standard deviation**.
- **Monitor:** it's an **iterative** cycle, not "deploy and forget". Sensors get replaced, conditions change → **data drift** → retrain. This is MLOps.

### 1.5 When do you even need ML? (Q&A in class)

- **Fixed, known rules → no ML.** Marks 40–50 → CGPA 4. A lookup table is enough.
- **Rules that vary and a large feature space → ML.** Bearing faults have ~5 types (inner race, outer race...), but the
  vibration pattern changes a lot from machine to machine, so you can't hand-write the rules.

### 1.6 What changes in the Edge AI lifecycle

The difference from the normal pipeline: **training happens elsewhere; inference happens on the edge device.**

> Vibration sensor → Raspberry Pi collects data → train the model *somewhere else* (laptop/cloud GPU) → evaluate →
> **deploy to the Raspberry Pi** → Pi runs inference locally on each new reading. It does not send every reading to the cloud.

| | General ML pipeline | Edge AI lifecycle |
|---|---|---|
| Where deployed | Cloud server | Near/at the data source |
| Constraints | Depends on environment, usually relaxed | **Latency, battery life, RAM, memory** |
| Maintenance | Model maintenance | Model maintenance **+ managing the devices themselves** (sensors, hardware quality) |

**Model update workflow** (a model won't stay accurate forever: machines age, humidity/temperature change, new faults appear):

```
edge device collects operational data → new samples sent to cloud storage → cloud ML pipeline retrains & validates
→ deployment service distributes the new model → devices install & activate it → (repeat forever)
```

### 1.7 High volume, low information density

> Traffic cameras across a city produce a huge amount of footage, but ~98% of drivers follow the rules. We only care about
> the ~2% who jump signals. The same holds for factory vibration data: most of it is "normal".
> **So: process on-device, transmit only what matters** (the alert, the fault, the violation frame).
> Sending everything from 2,000–3,000 cameras to the cloud would be very costly.

---

## 2. Session 2 (~8-Nov-2026): defining Edge AI, BLERP, cloud vs fog vs edge

### 2.1 Edge AI = edge devices + AI

- Edge devices produce a **"fire hose"** of high-frequency sensor data: high volume, low information per reading.
  Historically most of it was thrown away because sending it was too costly.
- **Edge AI processes data on the device where it's generated.** It makes local decisions without connectivity and
  transmits only what matters.
- It ranges from **simple** (a temperature threshold `if temp > X: alert`) to **sophisticated** (a compressed deep-learning
  model on a Jetson Nano). Edge AI is not one type of model or hardware.

### 2.2 The cloud-to-device continuum (Zhou et al., 2019, 6 levels)

It's not a binary "cloud OR edge" choice. Moving from all-cloud to all-device:

| Level | What happens |
|---|---|
| 1. **Cloud intelligence** | Everything runs in the cloud. Device sends data, cloud infers, returns result |
| 2. **Cloud-edge co-inference** | Edge runs the first layers of the neural network, sends intermediate features, cloud does the rest |
| 3. **Edge-cloud split inference** | Inference divided between edge and cloud; the split depends on how model/workload is partitioned |
| 4. **Edge inference** | Inference runs on an edge computing node (edge server, local gateway) |
| 5. **Edge on-device** | The device does the processing locally |
| 6. **Fully on-device intelligence** | Training *and* inference on the device (rare) |

> **Where you train and where you infer don't have to be the same place.** Train a CNN on a cloud GPU, deploy to a
> Raspberry Pi, infer there. Class question: *"Can we train in the cloud and still call it Edge AI?"* **Yes.** Edge AI
> refers to where **inference** happens at deployment, not where training happened.

### 2.3 Related terms (concept hierarchy)

```
AI  ⊃  ML  ⊃  Embedded ML  ⊃  TinyML          (DSP is paired with all of them)
```

| Term | One line |
|---|---|
| **Edge computing** | Processing data close to the source |
| **Edge AI** | Running AI/ML (usually inference) at or near the edge |
| **Embedded ML** | Running ML models on embedded systems (MCUs, industrial controllers, embedded boards). Usually **inference only** |
| **TinyML** | Embedded ML on the *most constrained* hardware: microcontrollers, DSPs, small FPGAs. Often just **kilobytes** of RAM/ROM. You must care about model size, RAM use, compute, power |
| **DSP (Digital Signal Processing)** | Maths that **cleans, denoises and transforms** raw sensor signals (e.g. time → frequency domain) *before* the model sees them |

**DSP example (bearing fault):** raw vibration → **filter** → compute features (**RMS, frequency, spectral energy**) →
feed *features* to the model, not the raw data. DSP transforms the signal; ML finds the relationship.

> **Co-design rule:** don't pick the pre-processing and the model independently. Both use memory and energy on the same
> tiny device, so design them together as one system.

### 2.4 BLERP: why move AI to the edge? ⭐ (most important framework of Module 1)

Coined by **Jeff Bier (Edge AI and Vision Alliance)**, used in Chapter 1 of the textbook. Five questions to judge whether a
use case benefits from edge AI:

| Letter | Question | Lecture example | Memory hook |
|---|---|---|---|
| **B: Bandwidth** | Can I even ship all this data? | 100 machines × 3 sensors (temp, vibration, IR camera) = 300 streams. Put an anomaly-detection box near the machines and send only fault alerts | Guard phones head office only when something happens |
| **L: Latency** | How fast must I respond? (delay between getting input and acting on the result) | Self-driving car must brake for a pedestrian in ~50 ms. **NASA Mars rovers** navigate on-device because Earth is minutes away by radio | Reflex arc: hand off the hot stove before the brain thinks |
| **E: Economics** | Who pays, for how long? | **Camera traps** in a forest: on-device model drops leaves/shadows/wrong animals, so you don't pay satellite costs for useless images. *But* edge hardware has its own maintenance/energy cost, so evaluate total system cost | Owning a bike vs paying for auto-rickshaws |
| **R: Reliability** | Does it work when the network doesn't? | Factory monitoring keeps running if the internet goes down; forest animal detection with intermittent signal | Lift emergency brake works with no power |
| **P: Privacy** | Where does sensitive data go? | Hospital ICU cameras: process locally so raw images never leave the hospital; if data must go out, encrypt + access control. Home security camera flags intruders on-device | Diary in your own drawer |

**Three rules about BLERP:**
1. **Filter, not a score.** One strong factor alone (e.g. latency, or privacy) can justify the edge. You don't need all five.
2. **Not every application needs the edge.** Some are better in the cloud; many are **hybrid**.
3. **Apply it per task, not per device.** One phone: face unlock = edge, chatbot answer = cloud.

### 2.5 Edge AI for good (4 real projects)

| Project | Domain | What it does | Why edge |
|---|---|---|---|
| **Smart Parks** collars | Conservation | ML collars track elephant movement/behaviour for rangers (Africa) | Remote, little connectivity, battery limits |
| **Izoelektro RAM-1** | Environment | Detects developing faults in power-line hardware → **preventive maintenance → prevents forest fires** | Remote infrastructure, no need to send full data |
| **Oral cancer screening** (Dr. Zubair Shamim, King Khalid Univ.) | Healthcare | Low-cost device flags suspicious cases so basic health workers can screen without a specialist | No cloud needed. Note: it's **screening, not diagnosis** |
| **Coffee plant disease ID** (UNIFEI, Brazil) | Agriculture | Farmer photographs a leaf, on-device classifier predicts the disease | Works offline in rural fields |

> Takeaway: small cheap models + no backend = developers anywhere can build for their local markets.

### 2.6 Edge AI vs traditional (server-side) AI: 7 differences

1. **Training on the edge is rare.** Training = repeated forward pass, backward pass, gradients, updates → needs lots of compute and memory. Train on powerful machines, deploy for inference only.
2. **Focus is sensor data**: continuous, noisy, high-sample-rate streams (vibration, audio, video), not neat tables. Pre-processing, signal processing, buffering and real-time handling become central.
3. **Models must be small.** A model at 98% accuracy on your laptop may not even *fit* in an MCU with a few KB of RAM. You need small architectures + optimisation (covered in sessions 11–12).
4. **Feedback loops are limited.** Devices are offline or barely connected (100 devices in a forest, 50 across a farm), so collecting new data, retraining and pushing updates is hard. Model drift creeps in.
5. **Compute is heterogeneous** (*heterogeneous* = many different kinds): MCUs, SoCs, GPU boards, FPGAs, each with different tools/runtimes. A model that runs on a Jetson won't run unchanged on an MCU.
6. **"Good enough" is the goal.** 99% accurate but huge vs 95% accurate that fits the MCU and meets latency → pick the 95% one, *if the application allows*. **Exception: safety-critical systems**, where you can't trade accuracy away. "Edge AI is use-case based."
7. **Tools and best practices are still evolving.** Deploying at the edge is not "copy a file to the device": you deal with device runtimes, model conversion, quantization, hardware compatibility, security, remote updates.

> Edge AI is a **subset** of AI: same principles, tighter constraints.

### 2.7 Cloud AI vs Edge AI vs Fog AI

| | **Cloud AI** | **Edge AI** | **Fog AI** |
|---|---|---|---|
| What | Centralised: devices stream raw data to a data centre; it trains, infers, returns results | Inference runs **on the sensor-bearing device itself**; training done beforehand off-device | **Middle tier** between end devices and cloud. Coined by **Cisco (2012)**, defined by the **OpenFog Consortium** |
| Nodes | Data-centre servers | Phone, camera, MCU, Pi, Jetson | **Fog nodes (FCN)**: routers, set-top boxes, switches, **IoT gateways** |
| Strengths | ~Unlimited compute/storage; big models; training; aggregates many sites | Near-instant; works offline; strong privacy; low running cost | Low latency for *many* devices in one area; local aggregation/filtering before cloud |
| Weaknesses | Network round-trip latency; needs constant connectivity; highest bandwidth cost; needs a fallback if the link drops | Tight compute/memory/power; size-vs-accuracy trade-offs | **Cannot run standalone**: it's an *extension* of the cloud for a geographic area |
| Use when | Model too big for any device; need global insight across sites/countries; latency budget is seconds; long-term retraining & analytics | Millisecond decisions; unreliable/absent connectivity; privacy/regulation; low running cost | Many devices in one area need real-time response **and** individual devices are too weak to infer alone |
| Example | Netflix recommendations; BI across thousands of stores | Self-driving perception; wearable health; security camera intruder detection | Factory gateway collects 100 machines' sensors, runs fault detection, sends summary to cloud |

**Cloudlet vs Fog vs MEC** (all "computing closer than the cloud"):

| | **Cloudlet** | **Fog computing** | **MEC** |
|---|---|---|---|
| Origin | CMU, 2009 | Cisco, 2012 / OpenFog | ETSI, 2014 (Mobile Edge Computing) → renamed **Multi-access** Edge Computing, 2016 |
| What it is | "**Data centre in a box**" near users; phones offload heavy compute to it | Architecture spreading compute between device and cloud; **multiple interconnected nodes** | Edge server **inside the mobile base station** |
| Node | Local/outdoor install | Routers, set-top boxes, gateways | Radio network / base station |
| Access | Wi-Fi | Bluetooth, Wi-Fi, mobile network | Mobile network |
| Hops | Single | Single or multiple | Single |
| Context awareness | Low | Mid | High |
| Inter-node communication | Partial | Supported | Partial |

### 2.8 The continuum: they collaborate, they don't compete

```
 End devices  ⇄   Edge                ⇄   Fog                    ⇄   Cloud
 sensors,         on-device inference,     gateways, routers,         data centres:
 wearables,       ms latency,              aggregate many devices,    training, analytics,
 vehicles         local decisions          coordinate local decisions centralised storage
 ──────────── compute power & storage increase →
 ←──────────── closer to data, lower latency
```

- **Arrows go both ways:** data flows up (device → cloud); **updated models flow down** (cloud trains → pushes to edge).
- Cloud will **not** be replaced. It still does what tiny devices can't (deep-learning training).

**Industry mapping (slide):**

| Industry | Tier | Why |
|---|---|---|
| Healthcare | **Edge** | Wearables/bedside monitors flag anomalies in real time; trends synced to cloud |
| Manufacturing | **Fog** | Gateway aggregates many machines' vibration/vision data for predictive maintenance; some sensors too weak to infer |
| Retail | **Edge + Cloud** | In-store cameras analyse locally (privacy), send hourly visitor counts; cloud combines all stores |
| Smart cities | **Fog + Cloud** | Fog nodes adjust traffic signals in real time; city-wide planning in cloud |

### 2.9 The three "edges" (Edge AI Foundation)

| Edge | What | Examples |
|---|---|---|
| **Heavy edge** | Servers on-site, near the data but much more powerful | Store backroom server running analytics for all store cameras; factory on-site server; traffic control room |
| **Smart edge** | Devices that sense *and* compute *and* decide locally | Robot vacuum (camera + distance sensors → navigation), vision AI cameras, robot-arm controller, drones, traffic-sign controller |
| **Embedded edge** | Tiny, right on the sensor, very constrained | Vibration sensor with an MCU (samples, filters, extracts features), motion sensor, smart label |

### 2.10 Edge hardware at a glance (detail comes in Sessions 3–4)

| # | Hardware | One line |
|---|---|---|
| 1 | **Microcontroller (MCU)** | Processor + memory + interfaces on **one chip**; 8–32-bit; KBs of RAM. Cheap, low-power, always-on: the classic TinyML target |
| 2 | **SoC with Linux** | CPU + GPU + memory controllers on one chip, runs **embedded Linux**, Python, cameras, ML runtimes (Raspberry Pi) |
| 3 | **GPU accelerators** | CPU + GPU boards (NVIDIA **Jetson**) for vision/deep learning |
| 4 | **FPGA** | Field-Programmable Gate Array: **reconfigurable** hardware circuits; parallel, high throughput, predictable latency. Needs specialised design skills |
| 5 | **Fixed-architecture accelerator** | Chip built for one kind of workload (e.g. neural-net ops). Very efficient, **not reconfigurable**, only supports certain operators/formats, so check model compatibility first |

### 2.11 Edge software stack and connectivity

- **OS options:**
  - **Bare metal:** no OS; a small C program loops forever: read sensor → infer → send (MCUs).
  - **RTOS (Real-Time OS)**, e.g. **FreeRTOS, Zephyr**: structured task scheduling with predictable timing (sensor acquisition → DSP → inference → communication).
  - **Embedded Linux**: memory management, multitasking, networking, file system (Raspberry Pi). Costs memory/compute overhead.
  - Trade-off: **OS overhead vs real-time determinism** (*determinism* = always responds in the same, predictable time).
- **Software:** inference runtimes (**TFLite Micro**, **ONNX Runtime**, **Edge Impulse**), firmware + DSP libraries, model conversion & quantization tools.
  The device can't run the full training framework, so the model is **converted** to a compact format and executed by a runtime.
- **Connectivity:**
  - Low-power radios for small data: **BLE** (Bluetooth Low Energy, short range, wearables), **Zigbee** (low-power sensor/automation networks), **LoRa** (long range, low data rate).
  - **Wi-Fi / cellular** for images or high-volume data.
  - Protocols: **MQTT** (Message Queuing Telemetry Transport: lightweight publish/subscribe for IoT; **demo in webinar 2**), **CoAP** (Constrained Application Protocol: for constrained devices/networks).

### 2.12 Edge AI development lifecycle

```
Develop & Train → Optimize & Deploy → Run Inference → Monitor & Diagnose → Iterate ─┐
       ↑────────────────────────────────────────────────────────────────────────────┘
```

Bearing-fault walkthrough:
1. **Develop & train:** collect vibration data in normal + fault conditions → features → train a classifier → evaluate (accuracy, precision, recall, F1) on a workstation/GPU/cloud.
2. **Optimize:** runs fine on a GPU ≠ fits on an MCU → **quantization, pruning, transfer learning** (after mid-sem).
3. **Deploy:** transfer the model, integrate with the app, update firmware. **Firmware flashing** or **OTA updates**, because nobody wants to walk to 100 devices in a forest for every update.
4. **Run inference:** new readings → processed → prediction. **No retraining per reading.**
5. **Monitor & iterate:** model misclassifies in one operating condition → collect those samples → verify labels → retrain/fine-tune → re-optimise → redeploy. **It never ends.**

### 2.13 Responsible Edge AI

| | Point |
|---|---|
| **Privacy** | Biggest win: raw data stays on-device. But on-device stores and biometric matching still need protecting |
| **Security** | Devices are **physically reachable**, so they're easier to tamper with than a locked data centre (modify software, extract data, swap the model). Countermeasures: **firmware signing, secure boot** (Session 14) |
| **Sustainability** | Less transmission + smaller models = less energy. **But** making lakhs of devices (chips, batteries, boards) costs materials and energy, and they become **e-waste**. Edge AI is **not automatically green**; think full lifecycle |

### 2.14 Class discussion answers (also in the Chapter 1 study guide PDF)

- **Q1. Apply BLERP to a device you own.** Name the *task*, not just the device. Phone face unlock: L, R, P very strong, E strong, B weak → edge. Same phone's chatbot → cloud.
- **Q2. Hospital, real-time vital alerts for 200 beds?** **Hybrid.** Edge at each bed for instant alarms; **fog** per ward/hospital collects many beds and does ward-level processing; **cloud** for compute-heavy long-term analytics. (Prof's answer.) Deciding factors: L, R, P.
- **Q3. Home camera AI moves from cloud to fully on-device: privacy trade-offs?** Gains: no frame-by-frame upload, you control retention, no cloud copy to leak. **New risks:** camera stolen or remotely accessed exposes locally stored images; limited memory/compute may weaken detection; software updates become harder. *Privacy is relocated, not solved.* Design the device securely.
- **Extra use case (prof):** **concrete curing**: moisture sensors embedded in large new buildings monitor curing in real time and alert if it isn't happening properly. It will appear in the written assignment.

---

## 3. Session 3 (14-Nov-2026): characteristics, market, architecture, platforms

### 3.1 Hybrid intelligence: who does what

> **Edge reacts, fog coordinates, cloud learns.**

| Layer | Responsibilities |
|---|---|
| **Edge** | Fast on-device processing, immediate decisions/actions, filtering data, identifying events |
| **Fog** | Coordinating multiple edge devices, short-term buffering, filtering, local data consolidation |
| **Cloud** | Heavy model training, cross-device/cross-site analytics, long-term storage, retraining, tasks needing global knowledge |

### 3.2 The four key characteristics of edge computing ⭐ (handout sub-topic: latency, bandwidth, privacy, power)

| Characteristic | Definition | Key points |
|---|---|---|
| **Bandwidth** | Amount of data that can be sent over a network in a given time | Sensor data = **high volume, low information density**. **Cellular links are often the scarcest resource in remote industrial sites.** Send alerts/summaries/events only → lower cost, better battery life, works with weak links |
| **Latency** | Time delay between an event happening and the system responding | Some decisions can't wait for a round trip (braking). For **remote assets**, the alternative is a delayed cloud response or *periodic human inspection*; on-device monitoring catches problems **between scheduled visits** before they escalate |
| **Privacy** | Keep raw data on device/on site to reduce exposure | Digital assistants process on-device; **video-call background blur** processes frames locally; **on-device filtering protects bystanders** (blur faces before sharing). It **reduces** exposure; it does not guarantee 100% privacy |
| **Power efficiency** | Use less energy per useful result | **Radio transmission is the most energy-hungry task on an embedded device.** Transmit less → longer battery. Battery operation also improves reliability (keeps working in a mains power cut). Efficient edge AI can turn a frequently-serviced device into one that **runs for years**. Savings depend on radio tech, model, compute, hardware |

### 3.3 Real products mapped to BLERP

| Product | What | Notable |
|---|---|---|
| **Izoelektro RAM-1** | Sensors on power lines detect conditions that can start **forest fires** | **~20-year** battery life; no regular power or comms in forests; can't change batteries often. B (send only when needed), L (early detection), E (less comms + maintenance), R (long unattended operation), P (raw data processed locally) |
| **SlateSafety BioTrac band** | Wearable for **first responders / workers** in critical environments; monitors physiological + environmental condition | B (only relevant info sent), L (timely danger detection), R (harsh environments), P (personal health data). On TIME's Best Inventions list |
| **OpenCollar Edge** | Collar monitoring **elephant behaviour** with sensors + edge AI | Animals cover huge areas; no raw stream; remote, no maintenance; **~5-year** battery life |

### 3.4 Edge AI market landscape: 4 application domains

| Domain | Focus | Examples |
|---|---|---|
| **1. Keeping track of objects** | Identify, detect, monitor, track physical objects | Smart packaging / damage sensors on parcels, counting products, tracking movement & location |
| **2. Understanding & controlling systems** | Monitor machines/infrastructure, understand operating condition, support control decisions | **Predictive maintenance on an oil rig**: ~80% of readings are normal; transmit when vibration starts drifting as the machine degrades |
| **3. Understanding people & living things** | Interpret information about humans/animals | BioTrac band, OpenCollar, wildlife cameras |
| **4. Transforming signals** | Process a signal to produce better information | **Noise suppression** on calls |

### 3.5 Edge AI system architecture: sensing → inference → actuation ⭐

```
 SENSING                       INFERENCE                          ACTUATION
 get input from sensors   →    edge model analyses the input  →   act on the result
 (vibration, temperature,      → classify / detect / predict /    (raise an alert, stop the production
  camera, microphone)            monitor, close to the data        line, send info to another system)
```

(The prof said "activation"; the handout and textbook say **actuation**. Use *actuation* in the exam.)

**The same 3 stages in 4 different products:**

| Product | Sensing | Inference | Actuation |
|---|---|---|---|
| RAM-1 | Temperature, humidity | Is there fire risk? | Communicate the risk |
| BioTrac | Physiological data | Unsafe physiological condition? | Alert / safety monitoring |
| OpenCollar | Movement, location | Animal activity pattern | Send info for wildlife management |
| Trail camera | Image/video | Is this the wildlife of interest? | Send selected images only |

> Only the **sensor type, inference task and action** change. The architecture is identical.

### 3.6 Three technical hardware architectures

| | **GPU** | **FPGA** | **ASIC** |
|---|---|---|---|
| Full name | Graphics Processing Unit | Field-Programmable Gate Array | Application-Specific Integrated Circuit |
| Idea | Many cores doing maths **in parallel** | Digital logic you can **reconfigure** for a specific computation | Chip **purpose-built** for one application/class of tasks |
| Reconfigurable after manufacture? | Software-programmable | **Yes** | **No** |
| Good for | Neural networks, vision | Specialised processing pipelines | Max efficiency for supported ops |
| Example | NVIDIA Jetson | | Google Edge TPU (Coral) |

**Commercial platforms:** integrated commodity platforms (**NVIDIA Jetson, Google Coral**) and AI accelerator chips
(**Qualcomm, Google, Hailo**). **Edge node devices:** NVIDIA Jetson; **Microsoft Azure Data Box Edge** (local processing,
still integrated with Azure, a good example of edge + cloud working together); **Huawei Atlas** (AI acceleration for inference).

### 3.7 Edge computing frameworks (to deploy & manage apps on fleets of devices)

| Framework | By | One line |
|---|---|---|
| **KubeEdge** | open source (CNCF) | Kubernetes for the edge: containerised apps across cloud + edge |
| **Azure IoT Edge** | Microsoft | Deploy/manage workloads on edge devices, integrates with Azure |
| **AWS IoT Greengrass** | Amazon | Local data processing and app execution on connected devices |
| **OpenEdge** | Baidu | Edge computing framework |
| **EdgeX Foundry** | open source (Linux Foundation) | Vendor-neutral IoT edge platform |
| **NVIDIA EGX** | NVIDIA | Platform for running AI workloads at the edge |
| **Google Cloud IoT** | Google | Cloud IoT for connecting devices and processing data (Google retired IoT Core in 2023) |

> Pick based on the application's requirements. SDE view: these are "Kubernetes/PaaS for device fleets."

### 3.8 Making big models fit (preview of Module 6)

Deep-learning models need lots of memory, compute and energy. Tools/architectures named in class:
- **TensorFlow Lite**: inference on resource-limited devices.
- **SqueezeNet**: a compact CNN *architecture* with far fewer parameters at similar accuracy.
- **Caffe2** (Meta): lightweight deep-learning framework for deployment (now merged into PyTorch).

### 3.9 Building an Edge AI solution: two stages

1. **Development** (on a normal computer/cloud): design the network architecture (layers, structure) → collect training data → train → **save the learned weights and the base model**. *Not on the edge.*
2. **Deployment** (on the edge device): the model becomes part of the running app, receives input and infers (e.g. classification result).

**Developer platforms:** **Roboflow** (computer vision: prepare datasets, train, deploy) and **Edge Impulse** (embedded ML:
sensor data → DSP → model → deploy). **You'll use Edge Impulse in the webinar/Lab 1.**

### 3.10 Breakout-room takeaways

- **Not every application needs an LLM** (or even deep learning). SVMs and simpler models work well when the problem is simple.
- Look up **Intel oneAPI**: an open SDK for parallel/data-parallel programming, one way to optimise.
- Raspberry Pi can now run deep-learning object detection, and handle **multi-sensor integration**. Then design a hybrid edge/fog/cloud split.
- Traffic: one signal alone can't fix congestion on a long stretch, so integrate data across many junctions (fog/cloud).
- Retail: a sensor on *every item* fails on **cost and labour** at warehouse/D-Mart scale; fine for a factory unit. **Always: it depends on the use case.**
- This activity is practice for the **post-mid-sem individual assignment**: take an existing deployed use case, design an alternative architecture, identify sensors and inputs, find what's missing and how to improve performance.

---

## 4. How the exam asks this (from the Jun-2026 mid-sem papers)

Past mid-sem papers are **all scenarios + numbers**. Module 1 shows up in 3 recurring question types.

### 4.1 Type A: "Why can't the cloud do this?" (latency arithmetic)

> *Set 1 Q1(b): Pedestrian detection must respond in < 10 ms. Cloud round trip is ≥ 80 ms. Where must inference run,
> and why can't a faster cloud server fix it?*

**Answer:** 80 ms > 10 ms, so the budget is blown **before any computation happens**. Inference must run **on the vehicle (edge)**.
A faster server only reduces *processing* time. The **network round trip** (distance, physics of signal travel, routing,
radio hops, variable jitter) stays, so even zero-time processing can't get below 80 ms.

> *Set 2 Q1(a): Surgical tool moves at 3 mm/s; loop must close in 5 ms; data centre round trip 35 ms.
> Positional error?*

**Answer:** error = speed × delay = 3 mm/s × 0.035 s = **0.105 mm** (vs 3 × 0.005 = 0.015 mm allowed), **7× the safe limit**.
Same reason: latency is network-bound, not compute-bound → close the control loop locally.

### 4.2 Type B: bandwidth/cost calculation ("transmit features, not raw data")

> *Set 1 Q2: Vibration sensor samples at 5,000 Hz, 32-bit float. Cellular costs $0.15/MB.
> (i) Daily cost sending raw. (ii) Daily cost if edge computes 32 FFT bins per 1,024-sample window and sends only those.
> (b) Bandwidth reduction. (c) The principle.*

Worked (state your assumption: 1 MB = 10⁶ bytes):

| | Raw | Features on edge |
|---|---|---|
| Bytes/second | 5,000 samples × 4 B = **20,000 B/s** | windows/s = 5,000 / 1,024 = 4.883; each window = 32 × 4 B = 128 B → **625 B/s** |
| Bytes/day (× 86,400 s) | 1,728,000,000 B = **1,728 MB** | 54,000,000 B = **54 MB** |
| Cost/day | 1,728 × 0.15 = **$259.20** | 54 × 0.15 = **$8.10** |

- **Reduction:** 1,024 / 32 = **32×** (≈ 97% less data).
- **Principle:** *process at the edge, transmit only information, not data*. This is the **B (and E)** in BLERP:
  high-volume, low-information-density sensor streams should be reduced on-device (DSP/feature extraction).

**Try it yourself (Set 2 Q2):** 8,000 Hz acoustic sensor, 32-bit, $0.12/MB, edge sends 64 FFT bins per 2,048-sample window.
*(Answers at the bottom of this file. Don't peek until you've tried.)*

### 4.3 Type C: the "five-question deployment decision framework" (= BLERP applied)

> *Set 1 Q3: 180 fishing trawlers, 50–120 km offshore, 25–35% cellular connectivity, cloud round trip 210 ms,
> recommendation needed within 8 minutes, GPS/sonar data commercially confidential (rivals intercepted it).
> For each question say forcing or not, which constraint, architectural implication.*

How to answer: go letter by letter and say **forcing / not forcing**:

| Factor | Forcing? | Why | Implication |
|---|---|---|---|
| Bandwidth | Moderate | Sensor data is tiny (1 Hz + 0.25 Hz × 4 B), but the link is weak/costly offshore | Send summaries, not raw history |
| Latency | **Not forcing** | 8-minute budget ≫ 210 ms round trip | Latency alone doesn't require edge |
| Economics | Check numbers | Compute daily MB × fleet × price | Usually small here; state it |
| Reliability | **Forcing** | Only 25–35% connectivity, so cloud-only fails most of the time | Inference must run **on the vessel** |
| Privacy | **Forcing** | Confidential GPS/sonar; past interception | Keep raw data on-board; encrypt anything sent |

> The trick examiners like: **not every factor forces the edge**. Saying "latency is NOT the reason here" earns marks.
> A vendor's "97% accuracy" doesn't matter if the system only works 30% of the time (reliability) and leaks
> confidential data (privacy).

**Later-session topics seen in the same papers** (not taught yet, so don't panic): canonical 5-stage pipeline and where
accuracy drops (pre-processing/normalisation mismatch between training and device), quantised model fits Flash but
crashes (**RAM for activations/tensor arena**, not just Flash), unstructured pruning doesn't speed up a CPU (need
**structured** pruning), **MQTT QoS 0/1/2**, streaming **window types** (tumbling, sliding/hopping, session), ASIC NRE vs per-unit cost.

---

## 5. One-page revision sheet

**Definitions in one line each**
- **Embedded system:** a computer that does one dedicated job inside a device; limited memory, compute, power.
- **IoT:** physical things + sensors + software + network → collect and exchange data.
- **Edge:** where the data is produced. **Edge computing:** process and store data there.
- **Edge AI:** run AI (mostly *inference*) on or near the device where data is generated.
- **Embedded ML:** ML inference on embedded systems. **TinyML:** embedded ML on KB-sized MCUs/DSPs/small FPGAs.
- **DSP:** clean/transform raw signals into features (filter → RMS, FFT bins) before the model.
- **Training vs inference:** learning parameters from data (heavy, done in cloud/GPU) vs using fixed parameters on new data (light, done on the edge).
- **Fog:** middle tier (gateways, routers), Cisco 2012 / OpenFog; extension of cloud, can't run standalone.
- **Cloudlet:** "data centre in a box" (CMU 2009). **MEC:** edge server in the mobile base station (ETSI 2014 → Multi-access 2016).

**Frameworks to draw from memory**
1. **BLERP** (Jeff Bier): Bandwidth, Latency, Economics, Reliability, Privacy. Filter, not score; per task; one factor can be enough.
2. **Continuum:** End devices ⇄ Edge ⇄ Fog ⇄ Cloud. Compute grows to the right; latency is lowest at the left. Models flow down, data flows up.
3. **Hybrid intelligence:** edge reacts · fog coordinates · cloud learns.
4. **Architecture:** Sensing → Inference → Actuation.
5. **Lifecycle:** Develop & Train → Optimize & Deploy (OTA) → Run Inference → Monitor & Diagnose → Iterate.
6. **6 levels (Zhou 2019):** cloud · cloud-edge co-inference · edge-cloud split · edge inference · edge on-device · fully on-device.
7. **3 edges:** heavy (on-site servers) · smart (vacuum, AI camera, drone) · embedded (sensor + MCU).
8. **4 characteristics:** bandwidth, latency, privacy, power efficiency (radio = biggest energy cost).
9. **4 market domains:** tracking objects · understanding/controlling systems · understanding people & living things · transforming signals.
10. **Hardware 5:** MCU · SoC+Linux · GPU (Jetson) · FPGA (reconfigurable) · fixed accelerator/ASIC (not reconfigurable).

**Edge vs traditional AI (7):** training rare on edge · sensor streams · small models · limited feedback loops ·
heterogeneous hardware · "good enough" (except safety-critical) · tools still evolving.

**Examples to cite**
- Bandwidth: factory vibration, 100 machines × 3 sensors · Latency: Mars rover, self-driving braking · Economics: camera traps ·
  Reliability: factory without internet · Privacy: home camera, ICU cameras.
- For good: Smart Parks elephants · Izoelektro RAM-1 (forest fires, 20-yr battery) · oral cancer screening · coffee leaf disease.
- Products: BioTrac band (first responders) · OpenCollar Edge (5-yr battery).
- Everyday: phone filters, face unlock, background blur, noise suppression, wake word.

**Common mistakes**
- Saying "edge is always better". Always say what stays in the cloud.
- Treating BLERP as a points total.
- Saying Edge AI means training on the device. It's about **inference**.
- Claiming on-device = fully private (theft, firmware, bystanders remain).
- Forgetting fog in the hospital answer.

**Self-test (answer out loud, no peeking)**
1. Why can't a faster cloud server fix a 10 ms latency requirement?
2. Give one example per BLERP letter, and one case where a letter is *not* forcing.
3. Draw End–Edge–Fog–Cloud and label what each layer does.
4. When would you NOT use ML at all? (CGPA table vs bearing fault)
5. Why does a model at 98% accuracy on your laptop fail on an MCU?
6. Difference between FPGA and ASIC in one sentence.
7. Why is OTA needed? Why is power efficiency mostly about the radio?
8. Redo the 5,000 Hz bandwidth calculation from memory.

---

## 6. Interview angle

**One-minute answer: "When would you run a model on-device instead of on a server?"**
> I use the BLERP checklist: bandwidth, latency, economics, reliability, privacy. If the data is too big to ship
> (video, high-rate sensors), the answer must come in milliseconds, the device must work offline, the per-request cloud
> cost adds up across millions of users, or the data is sensitive like faces or health data, I push inference to the
> device. One strong factor is enough. Training and heavy analytics usually stay in the cloud, so most real systems are
> hybrid: the device reacts, a local gateway coordinates, the cloud learns and pushes updated models down. The cost is
> tight memory and power, so the model has to be quantized or distilled, and you accept "good enough" accuracy unless
> it's safety-critical.

**SDE analogy:** client-side validation (edge) + server-side validation (cloud) + CDN in the middle (fog). Good apps do all three.

---

<details>
<summary>Answers: Set 2 Q2 practice (8,000 Hz)</summary>

- Raw: 8,000 × 4 = 32,000 B/s × 86,400 = 2,764.8 MB/day × $0.12 = **$331.78/day**
- Features: 8,000 / 2,048 = 3.906 windows/s × (64 × 4 = 256 B) = 1,000 B/s × 86,400 = 86.4 MB/day × $0.12 = **$10.37/day**
- Reduction: 2,048 / 64 = **32×**
- Principle: on-device feature extraction, transmit information not raw data (Bandwidth + Economics).
</details>
