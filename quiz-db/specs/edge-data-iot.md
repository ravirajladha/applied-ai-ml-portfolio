# Edge Data & IoT Integration (M3, S5-S6): coverage spec

**Ladder:** Machine Learning on the Edge (AIMLCZG535) › Module 3 Edge Data & IoT Integration   ·   **Prerequisites:** edge-foundations (pipeline stages, decision framework), edge-hardware (device tiers), basic Python/NumPy
**Why it matters for AI/ML:** An edge model is only as good as the data path that feeds it. Module 3 covers how sensor data is ingested, windowed, turned into features on the device, fused, stored and shipped (MQTT, Kafka, REST, gRPC), and why sending features instead of raw samples is the core economic argument for edge AI. The mid-sem papers test it with by-hand bandwidth and cost calculations, MQTT QoS handshakes and streaming-window arithmetic.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `ingestion` | Edge data ingestion, preprocessing and storage | sampling rate, sample size in bytes, timestamps | Nyquist and aliasing, ring buffers, consistent normalisation | store-and-forward under patchy links, flash wear and retention | clock skew, event time vs arrival time, edge storage budgets |
| 2 | `bandwidth` | Raw vs feature bandwidth and cost | bytes = rate x 4 B x 86,400 | raw daily MB and cost; feature daily MB | reduction ratio = window / bins; MB vs MiB convention | the cost argument vs the latency/privacy argument; "compute where the data is" |
| 3 | `feature-extraction` | On-device feature extraction and transformation | what a feature vector is; RMS, FFT | FFT bins and resolution fs / N; band energies | feature pipeline must match training exactly; window length vs resolution | choosing features for a slow-wear signal; DSP cost on an MCU |
| 4 | `windows` | Streaming windows (tumbling, sliding/hopping, session) | the three window names | inferences per minute = 60 / step; overlap | which window for gradual wear vs bursts vs sessions | Azure hopping vs sliding naming; detection delay; compute cost of overlap |
| 5 | `event-driven` | Event-driven pipelines and streaming analytics | event vs polling | threshold triggers, cascades, wake-on-event | back-pressure, late and out-of-order events | watermarks, exactly-once effects, designing an event pipeline |
| 6 | `fusion` | Data fusion techniques | combining sensors | early vs feature-level vs late fusion | time alignment and resampling; inverse-variance weighting | Kalman/complementary filter intuition; failure of one modality |
| 7 | `storage-queues` | Lightweight databases and message queues | SQLite, time-series DB | local queue / buffer for offline periods | choosing SQLite vs TSDB vs ring buffer; queue sizing | durability vs flash wear; brokerless (ZeroMQ) vs broker |
| 8 | `mqtt` | MQTT protocol and QoS | publish/subscribe, broker, topic | QoS 0/1/2 guarantees and handshakes (PUBACK; PUBREC/PUBREL/PUBCOMP) | wildcards, retained messages, LWT, keep-alive, effective QoS = min | message counts per QoS, duplicates under QoS 1, persistent sessions |
| 9 | `protocols` | MQTT vs Kafka vs REST vs gRPC | what each is for | pub/sub vs request/response; footprint | Kafka log and replay vs MQTT broker; gRPC streaming | choosing a protocol per tier of an edge-to-cloud path |
| 10 | `edge-analytics` | Edge analytics frameworks (EdgeX, Azure Stream Analytics) | what an edge analytics service does | EdgeX device/core/app services; ASA on IoT Edge | SQL-like window queries, rules engine (eKuiper) | where analytics runs vs where the model runs |
| 11 | `use-cases` | Use cases and fleet data volumes | predictive maintenance, robotics, IIoT | fleet daily volume per vehicle and total | cheap transmission is not the same as viable | vendor proposals that fail on latency, connectivity or confidentiality |

## Must-know facts
- Raw daily bytes = sampling rate (Hz) x bytes per sample x 86,400 s. A 32-bit float is 4 bytes. The course uses 1 MB = 10^6 bytes.
- Features per day = (rate x 86,400 / window samples) windows x bins x 4 B. Reduction ratio = window samples / bins per window (1,024 / 32 = 32x).
- "Compute where the data is" (data gravity): move the computation to the sensor and ship the small result, not the big raw stream.
- Nyquist: sample at more than twice the highest frequency you need, or high frequencies alias into low ones.
- An N-point FFT at sampling rate fs has frequency resolution fs / N and N/2 useful bins; band energies compress those bins further.
- Preprocessing and feature extraction on the device must be the same code and constants as in training.
- Tumbling windows: fixed size, no overlap (step = size). Sliding/hopping windows: fixed size, step < size, overlap. Session windows: close after an inactivity gap, variable length.
- Results per minute = 60 / step in seconds (30 s window, 5 s step -> 12 per minute).
- MQTT QoS 0 = at most once (PUBLISH only); QoS 1 = at least once (PUBLISH -> PUBACK, duplicates possible); QoS 2 = exactly once (PUBLISH -> PUBREC -> PUBREL -> PUBCOMP).
- MQTT effective delivery QoS = min(publisher QoS, subscription QoS). `+` matches one topic level, `#` matches all remaining levels and must be last.
- Retained message: the broker stores the last one per topic and gives it to new subscribers. Last Will and Testament: the broker publishes it when a client drops without a clean DISCONNECT.
- Kafka is a partitioned, replicated, replayable log for edge servers and cloud; MQTT is a lightweight broker protocol for constrained devices; REST is request/response over HTTP; gRPC is HTTP/2 + protobuf with streaming.
- Fusion levels: early (raw data), feature-level (intermediate), decision-level (late). Sensors must be time-aligned before early fusion.
- Inverse-variance weighting gives the minimum-variance combination of two independent noisy readings.
- EdgeX Foundry: device services -> core services (core data, metadata, command) -> application services, with eKuiper as the rules/analytics engine. Azure Stream Analytics runs SQL-like window queries in the cloud or as an IoT Edge module.
- Store-and-forward: buffer locally while offline, forward when the link returns; size the buffer from data rate x longest outage.
- Low transmission cost does not make a cloud-only design viable: latency deadlines, connectivity and confidentiality can still force edge inference.

## Common traps (each one must have at least one question)
- Forgetting the 86,400 seconds per day, or using 3,600 -> answer off by 24x.
- Using bits instead of bytes, or 1 byte per float -> off by 4x or 8x.
- Mixing MiB (2^20) with the course's MB (10^6) -> 1,648 vs 1,728 MB.
- Reduction ratio computed as bins / window or from total bytes with the wrong window count.
- Inferences per minute computed as 60 / window size instead of 60 / step.
- Thinking a tumbling window catches slow trends as well as a sliding one -> it reports less often and splits events at boundaries.
- QoS 1 assumed to be exactly once -> duplicates when PUBACK is lost; consumers must be idempotent.
- QoS 2 assumed to be free -> four packets and broker state per message.
- Publishing at QoS 2 but subscribing at QoS 0 -> delivered at QoS 0.
- `#` placed in the middle of a filter -> invalid.
- Retained message confused with a queued message -> only the last one per topic is kept.
- Kafka put on a microcontroller -> too heavy; MQTT (or MQTT-SN) at the device, Kafka at the edge server/cloud.
- "Transmission is cheap, so the cloud proposal is viable" -> the papers' fleet numbers are tiny; the proposal fails on deadline and confidentiality.
- Training features computed with one FFT size and deployment with another -> silent accuracy loss.
- Early fusion of unsynchronised streams -> misaligned samples.

## Interview angle
1. **"Why not stream raw vibration data to the cloud?"** 5 kHz x 4 B x 86,400 = 1.73 GB/day per sensor; 32 FFT bins per 1,024 samples cuts it 32x. Compute where the data is, send features or alerts.
2. **"Explain MQTT QoS levels."** 0 fire-and-forget; 1 PUBLISH/PUBACK, at least once, duplicates possible; 2 four-way PUBREC/PUBREL/PUBCOMP, exactly once, costliest. Pick 1 with idempotent consumers for most telemetry.
3. **"Tumbling or sliding window for bearing wear?"** Sliding: 30 s window, 5 s step gives 12 overlapping results per minute, a smooth RMS trend and no boundary splits.
4. **"MQTT or Kafka?"** MQTT from devices to the gateway (small footprint, QoS, LWT); Kafka from the gateway/edge server to the cloud when you need durable replayable streams and many consumers.
5. **"How do you fuse a camera and a radar?"** Time-align, then choose early, feature-level or late fusion by bandwidth, synchronisation and robustness to one sensor failing.

## Source material
- Handout (`edge-src/handout.txt`), session 5 (Edge Data & IoT Integration I): edge data ingestion, preprocessing and storage; event-driven pipelines and streaming analytics; data fusion techniques; on-device feature extraction and transformation (T1 Ch 5, 7; R1 Ch 6).
- Handout, session 6 (Edge Data & IoT Integration II): lightweight databases and message queues; communication protocols MQTT, Kafka, REST APIs, gRPC; edge analytics frameworks EdgeX Analytics Services and Azure Stream Analytics; use cases predictive maintenance, robotics, industrial IoT (T1 Ch 5, 7; R1 Ch 4).
- Lab experiment 3 (M3): simulate real-time IoT data ingestion via MQTT and perform on-device inference for anomaly detection.
- Mid-sem Jun 2026 Set 1 Q2: 5,000 Hz, 32-bit floats, $0.15/MB -> 1,728 MB and $259.20/day raw; 32 FFT bins per 1,024-sample window -> 54 MB and $8.10/day; 32x reduction; the architectural principle.
- Mid-sem Jun 2026 Set 2 Q2: 8,000 Hz, $0.12/MB -> 2,764.8 MB and $331.78 raw; 64 bins per 2,048 samples -> 86.4 MB and $10.37; 32x.
- Mid-sem Set 1 Q1(e): the three MQTT QoS levels with their guarantees and message exchanges.
- Mid-sem Set 2 Q1(e): the three streaming window types; 2,000 Hz bearing vibration, 30 s window and 5 s step -> 12 inferences per minute, sliding window, why better than tumbling for gradual wear.
- Mid-sem Q3 (both sets): fleet volumes. Trawlers: (1 + 0.25) Hz x 4 B x 86,400 = 0.432 MB/vessel/day, 77.76 MB for 180 vessels, ~₹7/day. Tankers: (2 + 1) Hz -> 1.0368 MB/truck, 155.52 MB for 150 trucks, ~₹10.89/day. Both are cheap; the vendor proposals fail on deadline, connectivity and confidentiality, not cost.
- **Exam patterns:** the bank mirrors these with new scenarios and numbers: raw vs feature MB and cost per day, the reduction ratio, results per minute = 60 / step, QoS handshake packet counts, and fleet volume totals with a "cheap but not viable" twist. MB = 10^6 bytes throughout, as the papers' numbers imply.
- **Standard practice (no slides exist):** Nyquist and aliasing, ring buffers, store-and-forward, FFT resolution, fusion levels and inverse-variance weighting, Kalman/complementary filters, event time and watermarks, MQTT details beyond QoS (wildcards, retained messages, LWT, keep-alive, effective QoS, MQTT 5 shared subscriptions), Kafka/REST/gRPC trade-offs, EdgeX Foundry service layers and eKuiper, Azure Stream Analytics window functions (where Azure's "hopping" is the course's "sliding" and Azure's own "sliding" window is event-triggered), SQLite and time-series databases are written from T1 Ch 5/7, protocol specifications and vendor documentation.
- **Gap flagged:** the handout names "EdgeX Analytics Services" but gives no detail; questions use the EdgeX Foundry architecture (device, core, application services, eKuiper rules engine) as documented by LF Edge.
