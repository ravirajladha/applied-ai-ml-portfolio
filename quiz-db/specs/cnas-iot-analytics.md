# IoT & Data Analytics (S13-S15): coverage spec

**Ladder:** API-driven Cloud Native Solutions (AIMLCZG549) › IoT & Data Analytics (S13-S15)   ·   **Prerequisites:** cnas-data-pipelines (DataOps, pipelines), cnas-cloudnative (serverless); edge-data-iot and edge-foundations go deeper on edge streaming, MQTT QoS and latency; pd-cleaning covers the pandas mechanics
**Why it matters for AI/ML:** Most real ML systems outside the browser start with sensors. This module ties the course together: what kind of analytics a question needs (descriptive to cognitive), how IoT data moves from sensor to dashboard (layers, gateway, platform, device APIs, serverless), and why IoT data must be cleaned before any model sees it (noise vs outliers, missing, inconsistent, duplicate, biased data, imputation, EDA).

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `analytics-types` | Data analytics, its goals and the five analytics types | definition; the question each type answers | techniques per type; the Instagram Reels, Covid discharge, Apollo and Woebot examples | classify a business question; cognitive analytics as advisor vs AI as doer | the slide's "what might happen" wording for prescriptive; designing a type ladder for one product |
| 2 | `iot-architecture` | IoT architecture: sensing, network, data processing, application layers | what each layer does | map a component to its layer (wearable, air-pollution examples) | where the processing layer sits (gateway or cloud); network-layer security duties | spot a misplaced responsibility in a design |
| 3 | `edge-gateway` | Edge computing for IoT and the IoT gateway | edge definition; gateway as hub | the six gateway functions; key edge benefits | aggregation bandwidth maths; protocol translation and connectivity-management scenarios | — (gateway single point of failure and irreversible edge reduction are already tested in edge-foundations / edge-data-iot) |
| 4 | `iot-platforms` | IoT platforms and the technology stack | platform as middleware; provisioning, management, automation | open-source vs commercial (OpenRemote, ThingsBoard, AWS IoT) | build vs buy for a city project | platform lock-in and data ownership trade-offs |
| 5 | `openremote` | OpenRemote and the SmartCity parking demo | assets and attributes; map view | When-Then rules vs Flow rules; insights dashboard | group occupancy % by hand; parking data sources (ground sensors, cameras, meters, ANPR) | rule thresholds with flapping; weighted vs averaged occupancy |
| 6 | `lifecycle` | IoT analytics life cycle: generate, collect, analyze, react, predict | the five stages in order; telemetry | what happens in collect (buffering) and analyze (pre-process + EDA) | react vs predict examples; simple next-day forecast | closing the loop: prediction feeding automatic reaction |
| 7 | `data-quality` | IoT data quality: noise, outliers, missing, inconsistent, duplicate, biased | the five issue types | match symptom to issue and technique; noise vs outlier | ETL with a broker and stream processor; format standardization; dedup by (device, timestamp) | legitimate repeats vs duplicates; bias from deployment location |
| 8 | `imputation` | Imputation techniques for IoT data | mean, median, mode | when each fits; the slide examples | by-hand mean/median/mode; forward fill and interpolation for time series | leakage and long gaps; imputing vs flagging |
| 9 | `dataset-traits` | Characteristics of IoT datasets | dimensionality, sparsity, resolution | curse of dimensionality and PCA; sparse storage | resolution too fine vs too coarse; malfunctioning-sensor columns | storage saving from sparse formats; resampling choice |
| 10 | `eda` | EDA for IoT: univariate, multivariate, temporal, spatial | the four EDA types and their plots | box plot five-number summary; IQR fences; scatter + Pearson | compute fences and flag outliers; correlation vs causation | whisker convention on the slides vs Tukey; percentile methods |
| 11 | `device-apis` | Device-communication APIs (MQTT, CoAP, HTTP) and ThingsBoard | device APIs vs server-side APIs | MQTT vs CoAP vs HTTP fit; ThingsBoard telemetry vs attributes, access tokens | Gateway MQTT API; RPC direction | protocol choice for constrained, battery devices |
| 12 | `aws-serverless` | AWS IoT components and serverless functions in IoT | AWS IoT Core, rules engine, Lambda | Device Shadow, registry, X.509 certificates | rule -> Lambda per message cost in ₹; when serverless fits | cold starts, stateful windows and fan-out limits |

## Must-know facts
- Data analytics is the process of cleaning, transforming and modelling data to discover useful information for decision-making. Its goals: predict something, find patterns, find relationships.
- Descriptive = what happened (dashboards, summary statistics); diagnostic = why it happened (root cause, drill down, regression); predictive = what is likely to happen (ML models); prescriptive = what should we do (actions, business rules, optimisation); cognitive = learns and reasons like a human, collaborates or advises (NLP, semantics, all data types).
- IoT architecture layers: sensing (sensors/devices), network (transfer via a gateway; protocol configuration, encryption, malware protection, authentication), data processing (analysis; in the gateway or the cloud), application (shows data to the user, usually in the cloud).
- Edge computing processes data at the periphery of the network, as close to the source as possible. Benefits for IoT: low latency, longer battery life, access to analytics/AI (MEC), resilience, scalability, efficient data management.
- IoT gateway functions: data aggregation, protocol translation, data processing, security, connectivity management, edge computing capabilities. Modern gateways are bidirectional.
- An IoT platform is multi-layer middleware for provisioning, managing and automating connected devices.
- OpenRemote: open-source; assets with attributes; When-Then rules (condition -> action) and Flow rules (visual calculation graph); Insights dashboards. The demo computes group occupancy as total occupied / total spaces = 1246 / 1275 = 97.7%.
- IoT analytics life cycle: generate (telemetry) -> collect (cache/buffer at edge) -> analyze (pre-process + EDA) -> react (automatic real-time decisions) -> predict (predictive analytics).
- IoT data quality issues: noise and outliers, missing, inconsistent, duplicate, biased/unrepresentative. Noise is erroneous; an outlier is valid but rare.
- Mean imputation for values that fluctuate around a stable range; median when outliers exist; mode for categorical data.
- IoT dataset characteristics: dimensionality (curse, PCA), sparsity (store only non-zeros), level of resolution (too fine buries the pattern in noise, too coarse loses it).
- EDA types: univariate (histogram, box plot, summary stats), multivariate (scatter, correlation heatmap), temporal (time-series plot, decomposition), spatial (geospatial heat map, clustering). IQR fences: Q1 - 1.5 IQR, Q3 + 1.5 IQR.
- ThingsBoard device APIs: MQTT, CoAP, HTTP, Gateway MQTT; server-side: administration REST API, RPC API, REST client.
- MQTT = TCP publish/subscribe through a broker; CoAP = REST-like over UDP for constrained devices; HTTP = TCP request/response, heavier but universal.
- AWS IoT Core: device gateway, message broker, rules engine, Device Shadow, registry, X.509 authentication; rules route messages to services such as Lambda.

## Common traps (each one must have at least one question)
- A 1,000 °C reading from an electrical fault called an "outlier" -> it is noise (an error); outliers are valid but rare.
- Mean imputation on data with an outlier -> pulled far off (131 vs 40 µg/m³); use the median.
- Mean or median imputation on ON/OFF status -> use the mode.
- Prescriptive read as "what might happen" (the slide's wording) -> that is predictive; prescriptive recommends an action.
- Diagnostic confused with descriptive -> "how many" is descriptive, "why" is diagnostic.
- Group occupancy computed as the average of per-lot percentages -> must be total occupied / total spaces.
- Dedup removing legitimate identical readings -> dedup on (device_id, timestamp) or a message id, not on the value.
- Biased deployment fixed with more data from the same places -> need stratified, diverse placement.
- Whiskers drawn to the fences -> whiskers stop at the most extreme data point inside the fences.
- Correlation from a scatter plot treated as causation.
- Finer resolution assumed always better -> per-second can bury a trend in noise.
- Serverless per-message function assumed right for stateful sliding windows -> functions are stateless and short-lived.
- CoAP assumed to run over TCP like HTTP -> it runs over UDP.

## Interview angle
1. **"Walk me through the four types of analytics for one product."** Reels: descriptive = views and likes; diagnostic = why engagement dropped; predictive = trending topics; prescriptive = tips to raise watch time.
2. **"Noise or outlier?"** Ask whether the value is physically possible and confirmed by redundancy. Errors are noise; real rare events are outliers and may be the most important data.
3. **"How would you impute missing IoT data?"** Short gaps in a smooth series: interpolate or forward-fill; outliers present: median; categorical: mode; long gaps: flag and alert instead of inventing data.
4. **"Where does processing happen in an IoT system?"** At the gateway for latency, bandwidth and dedup; in the cloud for history, heavy models and dashboards.
5. **"MQTT, CoAP or HTTP for a battery sensor?"** MQTT for pub/sub telemetry over TCP, CoAP for very constrained UDP devices, HTTP when the device is powerful and simplicity wins.

## Source material
- Old-batch slides for S13-S15 (`cloud-src/cnas-iot-analytics.txt`): data analytics definition and goals (predict, patterns, relationships with banking, weather and healthcare examples).
- Analytics types with the slides' questions and techniques; the Covid discharge prediction project (1,233 patients, random forest 92%); Apollo cardiovascular risk tool (predictive + prescriptive); the Instagram Reels exercise; cognitive analytics and the Woebot example.
- IoT definition and the four-layer architecture, with the wearable fitness tracker and air-pollution monitoring examples.
- Edge computing definitions, benefits for IoT, the wearable edge survey and MEC; the IoT gateway and its six functions.
- IoT platform as middleware and the three course platforms (OpenRemote, AWS IoT, ThingsBoard); OpenRemote SmartCity parking demo (map, assets Lijnbaan/Erasmusbrug/Markthal, When-Then "Parking: Almost Full", Flow occupancy 1246/1275 = 97.7%, Insights dashboard).
- IoT analytics life cycle (generate, collect, analyze, react, predict) with the support-ticket and conference-room examples.
- The five data-quality issues with examples and techniques; ETL with Kafka/RabbitMQ, Flink/Kinesis and BI tools; the Flink format-normalisation example (rewritten in plain Python).
- Imputation (mean 22.95, median 40 vs mean 131, mode ON); dataset characteristics (dimensionality, sparsity, resolution); EDA types, box plot and IQR (PM2.5 fences 0 and 80), scatter plot and Pearson, temporal and spatial analysis, EDA tools.
- ThingsBoard device and server-side API list.
- No past papers; scenario style modelled on BITS WILP papers (Pune smart city, Bengaluru deliveries, agritech cooperatives, ₹ costs).
- **Standard practice (slides thin or image-only):** MQTT/CoAP/HTTP comparison, ThingsBoard access tokens, telemetry vs attributes, RPC and Gateway MQTT API, ThingsBoard architecture, AWS IoT components (IoT Core, rules engine, Device Shadow, registry, certificates), serverless functions in IoT, forward fill and interpolation, Tukey whiskers.
- **Slide issues:** prescriptive analytics is captioned "what might happen" (standard: what should we do); the box-plot slide says whiskers extend to the minimum and maximum, and the next slide places them at the fences, while the Tukey convention stops them at the most extreme point inside the fences. Questions follow the standard and say so.
