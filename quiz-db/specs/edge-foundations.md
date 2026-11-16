# Edge AI Foundations (M1, S1-S2): coverage spec

**Ladder:** Machine Learning on the Edge (AIMLCZG535) › Module 1 Foundations of Edge AI (Sessions 1-2)   ·   **Prerequisites:** ml-what, ops-serving (for general serving patterns)
**Why it matters for AI/ML:** Module 1 answers the first architectural question of every edge project: where must inference run, and why? It defines Edge AI, contrasts cloud, fog and edge AI, places them on the edge-cloud continuum, names the key characteristics (latency, bandwidth, privacy, power) and the sensing → inference → actuation architecture. The mid-sem papers test it with latency-budget arithmetic (position error = speed × latency), the five-stage Edge AI pipeline and its preprocessing failure mode, and the five-question deployment decision framework applied to an Indian fleet scenario with a vendor "upload every N hours" proposal.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `definition` | Definition, motivation and scope of Edge AI | inference on or near the device that makes the data | convergence of embedded systems, ML and IoT/networking; what each field contributes | T1's BLERP reasons (bandwidth, latency, economics, reliability, privacy) mapped to a scenario | when "edge" is the wrong answer; scope of training vs inference at the edge |
| 2 | `cloud-limits` | Limitations of cloud-only AI | needs a network, adds round-trip delay | four limitations and a consequence for each | why a faster cloud server cannot close a propagation-bound gap | quantifying a cloud-only design's failure in a scenario |
| 3 | `cloud-fog-edge` | Cloud AI vs Edge AI vs Fog AI | where each runs | fog as the gateway / local-server layer; typical latency and compute per tier | assigning workloads to the right tier | fog aggregation and its failure modes (single point of failure, extra hop) |
| 4 | `latency-budget` | Latency budgets and real-time control | what a latency budget is | compare budget vs round-trip; budget breakdown | position error = speed × latency; speed-of-light floor | jitter and tail latency vs a hard deadline, control-loop budgets |
| 5 | `continuum` | The edge-cloud continuum and hybrid intelligence | the continuum from sensor to data centre | split of work: inference at edge, training in cloud | cascades / early exit, store-and-forward, partial offload | designing graceful degradation when the link drops |
| 6 | `characteristics` | Key characteristics: latency, bandwidth, privacy, power | the four characteristics | bandwidth and daily data volume by hand | privacy by data minimisation; power and battery life trade-offs | conflicts between characteristics (accuracy vs power vs privacy) |
| 7 | `domains` | Market landscape and application domains | example domains (automotive, health, industry, agriculture, retail) | which constraint dominates in each domain | matching a domain to device tier and constraints | market claims vs engineering reality |
| 8 | `architecture` | System architecture: sensing → inference → actuation and the five pipeline stages | sense, infer, act | the five stages in order | which stage owns which latency and failure | closing the loop on an actuator; post-processing and thresholds |
| 9 | `pipeline-failures` | Pipeline failure modes: preprocessing mismatch | train/deploy mismatch exists | normalisation with the wrong μ and σ | why preprocessing is the stage most likely to degrade accuracy | debugging a "model file is correct but outputs are random" device |
| 10 | `decision-framework` | The five-question deployment decision framework and vendor proposals | the five questions | forcing vs non-forcing constraints | applying the framework to a fleet scenario | rebutting a vendor "upload every N hours" proposal with numbers |

## Must-know facts
- Edge AI = running ML inference on (or very near) the device that produces the data, instead of sending raw data to a remote cloud.
- Edge AI sits at the convergence of three fields: embedded systems (run on constrained, real-time hardware), machine learning (turn raw signals into decisions) and IoT / networking (connect, collect, update and coordinate devices). None of the three alone gives "intelligent decisions on a connected, constrained device".
- T1 (Situnayake & Plunkett) summarises the reasons for edge with BLERP: Bandwidth, Latency, Economics, Reliability, Privacy.
- Cloud-only limitations: round-trip latency, dependence on connectivity, bandwidth and data-transfer cost, privacy / regulatory exposure of raw data, and energy spent on the radio.
- Physics sets a floor: light in fibre covers about 200 km per ms, so distance alone adds round-trip delay that no faster server can remove. Server speed only shrinks compute time, not network time.
- Position error (or distance travelled blind) = speed × latency. 3 mm/s × 35 ms = 0.105 mm; 20 m/s × 100 ms = 2 m.
- If the budget is smaller than the cloud round-trip (10 ms vs 80 ms), inference must run on the device: it is a forcing constraint.
- Cloud AI: huge compute, central, high latency. Fog AI: gateway / on-premises server layer near the devices, aggregates many sensors. Edge AI: on the device itself, lowest latency, tightest resources.
- The edge-cloud continuum: device → gateway / fog → regional edge → cloud. Hybrid intelligence splits work: real-time inference at the edge, heavy training, fleet analytics and retraining in the cloud.
- The canonical five-stage Edge AI pipeline (course framing, reconstructed): data acquisition (sensing) → preprocessing → inference → post-processing / decision → action (actuation or communication).
- Preprocessing mismatch is the stage most likely to degrade accuracy when moving from laptop to device: different normalisation constants, sample rate, resizing, colour order or feature code than training used.
- Normalisation: z = (x − μ) / σ with the TRAINING μ and σ. Using μ = 0, σ = 1 by mistake feeds raw-scale inputs to the model and gives garbage predictions even though the model file is correct.
- The five-question deployment decision framework (course framing, reconstructed): latency, connectivity, bandwidth / cost, privacy, power / autonomy. For each: is the constraint forcing (on its own it rules out cloud-only) or not, and what does it imply for the architecture?
- One forcing constraint is enough to require on-device inference; the cloud can still be used for non-critical work (training, dashboards).
- Daily data volume = rate (Hz) × bytes per sample × 86,400 s. 1 Hz × 4 B = 345,600 B/day. Costs in the papers use decimal MB (10^6 B).
- A vendor's "upload every N hours" plan adds up to N hours of delay, which breaks any minutes-level alert requirement, assumes connectivity that may not exist, and sends confidential raw data over the air. A cheap data bill does not rescue it.

## Common traps (each one must have at least one question)
- "Buy a faster cloud server" to meet a 10 ms budget -> the round-trip is network and propagation time; server speed cannot remove it.
- Treating the cloud round-trip as the only latency -> sensor, preprocessing and actuation also consume the budget.
- Forgetting units in position error (mm/s × ms) -> 3 mm/s × 35 ms is 0.105 mm, not 105 mm.
- Fog = cloud -> fog is a local layer (gateway, on-prem server) close to the devices.
- Edge AI means training on the device -> the core idea is inference at the edge; training usually stays in the cloud.
- Blaming the model file when a deployed model outputs random classes -> check preprocessing (μ, σ, sample rate, input layout) first.
- Thinking the inference stage is where accuracy is most often lost -> it is preprocessing mismatch.
- A cheap daily upload cost means the cloud plan is viable -> latency, connectivity and privacy can still force the edge.
- Counting only one constraint in the framework -> answer all five, stating forcing or not for each.
- "Hybrid" read as "everything twice" -> each tier does the work it is best at.
- MB vs MiB confusion in cost calculations -> state the convention (the papers use 10^6 bytes).
- Assuming more accuracy in the cloud wins the argument -> an answer that arrives too late has zero value in a control loop.

## Interview angle
1. **"When would you NOT put a model on the edge?"** When no constraint forces it: latency is loose, connectivity is reliable, data is small and not sensitive, and the model is too big for affordable devices. Then cloud is simpler to update and monitor.
2. **"Your budget is 10 ms and the cloud round-trip is 80 ms. Options?"** Inference must move on-device or to a co-located edge node; a faster server does not help because the gap is network time.
3. **"A model works on the laptop but gives random output on the MCU. Where do you look?"** Preprocessing: the normalisation constants, sample rate, window length and input layout must match training exactly. Add a golden-input test that compares device and laptop outputs.
4. **"Explain fog computing to a web developer."** It is like a regional CDN or a BFF layer: a local tier that aggregates and pre-processes many devices before anything goes to the origin.
5. **"How do you decide edge vs cloud for a new product?"** Run the five questions: latency, connectivity, bandwidth/cost, privacy, power/autonomy. Any forcing answer pushes inference to the edge; the rest decide what the cloud still does.

## Source material
- Handout (`edge-src/handout.txt`), Session 1 sub-topics: Edge Computing Fundamentals; Definition, motivation, and scope of Edge AI; Cloud AI vs. Edge AI vs. Fog AI (T1 Ch 1, R1 Ch 1, 9).
- Handout, Session 2 sub-topics: The Edge–Cloud continuum and hybrid intelligence; Key characteristics: latency, bandwidth, privacy, power efficiency; Edge AI market landscape and application domains; Edge AI system architecture: sensing → inference → actuation (T1 Ch 2, R1 Ch 1).
- Handout lab Exp 1 (M1): run a TFLite inference locally and compare latency with a cloud-based inference task.
- Jun 2026 mid-sem Set 1 Q1(a)-(c): four limitations of cloud-only AI with consequences; 10 ms pedestrian-detection budget vs 80 ms cloud round-trip ("why can a faster cloud server not close this gap"); the five stages of the canonical Edge AI pipeline and the stage most likely to degrade accuracy.
- Jun 2026 mid-sem Set 2 Q1(a)-(c): remote surgery, 3 mm/s tool tip, 5 ms loop vs 35 ms round-trip -> position error; Edge AI as the convergence of three fields; keyword-spotting model normalised with μ = 42.3, σ = 8.7 in training but μ = 0, σ = 1 on the STM32H7.
- Jun 2026 mid-sem Set 1 Q3 and Set 2 Q3: trawler cooperative (Rameswaram, 180 vessels) and dairy tanker cooperative (Punjab, 150 trucks): apply the five-question framework (forcing or not, constraint, implication), rebut a vendor "upload X hours every Y hours" proposal on two constraints, compute daily volume per vehicle, fleet total and ₹ cost, and judge viability.
- Exam patterns: (1) latency gap and position error = speed × latency, with a "why not a faster server" justification; (2) pipeline stages in order plus preprocessing mismatch as the failure; (3) the five-question framework, forcing vs non-forcing per question; (4) per-vehicle volume = Σ(rate × 4 B × 86,400), fleet total, ₹ cost per day, and the twist that the cost is tiny so the rebuttal must rest on latency, connectivity and confidentiality.
- **Reconstructed frameworks (no slides):** the "five stages of the canonical Edge AI pipeline" are written as acquisition → preprocessing → inference → post-processing → action; the "five-question deployment decision framework" as latency, connectivity, bandwidth/cost, privacy, power/autonomy (from the brief and the paper wording). Questions test the reasoning, not one exact wording.
- **Standard practice:** there are no slides for this course. BLERP (T1 Ch 1), the cloud/fog/edge tier descriptions, the edge-cloud continuum and hybrid patterns (cascades, store-and-forward, early exit), speed-of-light latency floors, data-volume conventions and the application-domain examples are written from T1 and general engineering knowledge.
- **Gap flagged:** Set 1 Q3(b)'s "transmit all 6 hours every 4 hours" is ambiguous (overlapping windows send 1.5x the raw data); the bank's own scenarios state the upload volume explicitly. The papers' ₹ fleet costs come out tiny (a few rupees a day), so the intended answer is that cost is not the deciding constraint.
