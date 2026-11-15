# Serving Models: coverage spec

**Ladder:** L5 · Shipping It › Production ML   ·   **Prerequisites:** ml-basics (train / predict), Python functions and classes, basic HTTP APIs
**Why it matters for AI/ML:** A model only earns its keep once something can call it. Serving is where ML meets ordinary backend engineering (APIs, containers, SLOs, deploys) plus a few ML-only problems: big artifacts, GPU memory, batching, train/serve skew and per-token costs.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `artifacts` | Model artifacts and serialisation | what a model file is; pickle/joblib save and load | pickle runs code on load; sklearn version mismatch; ONNX as a portable format | safetensors (tensors only, mmap, no code); what ONNX export can and cannot carry | supply-chain risk of loading third-party weights; choosing formats per runtime |
| 2 | `patterns` | Serving patterns | online API vs batch job vs edge | streaming (event-driven) inference; picking a pattern from latency needs | precompute-and-lookup vs live inference; edge constraints | hybrid designs (batch features + online model), staleness trade-offs |
| 3 | `api` | API serving (FastAPI) | POST /predict, JSON in and out, load once | Pydantic validation and 422s; health/readiness endpoints | `async def` vs `def` for CPU-bound inference; workers multiply model memory | GIL, threadpools and event-loop blocking; gRPC vs REST |
| 4 | `containers` | Containers and train/serve skew | what a Docker image is; why pin versions | layer order and caching; secrets not in the image | train/serve skew from different preprocessing; ship the Pipeline | baking weights into the image vs pulling at start; reproducibility |
| 5 | `latency` | Latency, throughput and batching | latency vs throughput; p95 | percentiles vs mean; Little's law | dynamic batching (max batch, max wait) trade-off | batching arithmetic; tail latency under load |
| 6 | `llm-servers` | GPU serving, LLM inference servers and token streaming | what vLLM/TGI/Triton are; streaming tokens | TTFT vs time per output token; SSE | continuous batching; PagedAttention; KV cache size | prefill compute-bound vs decode bandwidth-bound; capacity maths |
| 7 | `quantisation` | Quantisation for serving | fewer bits per weight = smaller model | memory maths fp16 / int8 / 4-bit | scale + rounding, quality trade-offs, outliers | weight-only vs activation quantisation; when it does not speed up |
| 8 | `caching` | Caching | why cache identical requests | hit rate; cache key normalisation | semantic cache thresholds; provider prompt caching needs identical prefix | cache invalidation on model change; stale and wrong hits |
| 9 | `scaling` | Scaling and cost | horizontal scaling; cost per request | tokens x price arithmetic; cold starts | autoscaling signals for GPU (queue depth, not CPU); scale to zero | GPU cost per million requests; utilisation vs latency SLO |
| 10 | `deploy` | Deployment strategies, registry and rollbacks | canary and blue-green in one line | shadow vs canary vs A/B; model registry and versions | sticky routing; immutable versions; rollback plan | metric-gated progressive rollout; why shadow can be unsafe |
| 11 | `reliability` | Reliability and security | timeouts; secrets in env vars | retries with backoff and jitter; rate limits (429) | fallback models; input size limits; retry only safe errors | retry storms and budgets; PII in logs; prompt injection at the edge |

## Must-know facts
- `pickle.load` / `joblib.load` can execute arbitrary code; only load files you trust.
- A scikit-learn pickle is tied to the library version that wrote it; loading in another version warns (`InconsistentVersionWarning`) and may break.
- safetensors stores only tensors plus a JSON header: no code runs on load and it can be memory-mapped.
- ONNX is a framework-neutral graph format, run by ONNX Runtime and others.
- Load the model once at process start; each worker process holds its own copy in memory.
- In FastAPI, a plain `def` endpoint runs in a threadpool; CPU-heavy work inside `async def` blocks the event loop for every request.
- Pydantic validation rejects bad requests with HTTP 422 before your code runs.
- Train/serve skew: the same raw input gets different features at serve time; fix by shipping the fitted preprocessing with the model (one Pipeline artifact).
- Report latency as percentiles (p50/p95/p99), not the mean; tail latency is what users feel.
- Little's law: concurrency = throughput x latency.
- Dynamic batching trades a little latency (the wait window) for much higher throughput.
- LLM servers use continuous batching (requests join and leave at every decode step) and PagedAttention (KV cache in fixed-size blocks, like OS pages).
- Weights memory = parameters x bytes per parameter: 7B at fp16 = 14 GB, int8 = 7 GB, 4-bit = 3.5 GB (plus KV cache and overhead).
- Decode is usually memory-bandwidth bound; prefill (reading the prompt) is compute bound.
- LLM API cost = input tokens x input price + output tokens x output price; output tokens usually cost more.
- Provider prompt caching only hits on an identical prefix: put static content first.
- Canary = small slice of real users; shadow = copy of traffic, responses thrown away; blue-green = two full environments, flip all traffic; A/B = controlled experiment on a business metric.
- Retry only transient errors (timeouts, 429, 5xx), with exponential backoff plus jitter and a cap.
- Never bake secrets into images or code; never log raw PII.

## Common traps (each one must have at least one question)
- "Pickle is just a data format" -> loading a pickle can run any code the author put in it.
- "A pickled sklearn model works on any sklearn version" -> it is version-bound; pin and record the version.
- Putting CPU-bound `model.predict` inside `async def` -> blocks the event loop; all other requests stall.
- "4 workers = 4x throughput for free" -> 4x model memory too; may not fit on a GPU.
- Re-implementing preprocessing in the serving code -> train/serve skew, silent accuracy loss.
- Scaling a single request inside the request (per-request mean/std) -> NaN or meaningless features.
- Judging latency by the mean -> hides the slow tail; one outlier moves the mean, not p50.
- "Bigger batch is always better" -> throughput rises but per-request latency rises too.
- "4-bit quantisation is always faster" -> it saves memory; speed depends on kernels and whether you were bandwidth bound.
- Forgetting the KV cache when sizing GPU memory -> long contexts or many users run out of memory.
- Counting only input tokens in cost estimates -> output tokens are priced higher and often dominate.
- Changing a timestamp or user name at the start of the prompt -> kills the provider prompt cache.
- Semantic cache with too low a threshold -> returns another question's answer.
- Not including the model version in the cache key -> stale answers after a deploy.
- Using Python's built-in `hash()` for sticky canary routing -> string hashes change per process.
- "Shadow is risk-free" -> shadow traffic can still trigger side effects (emails, payments) and doubles load on dependencies.
- Deploying `model:latest` -> no reliable rollback; use immutable versions.
- Retrying every error immediately -> retry storm; retrying a 400 never helps.
- Autoscaling GPU servers on CPU utilisation -> the wrong signal; use queue depth / in-flight requests.
- Scale to zero on a large model -> cold starts of minutes.
- No input length limit on an LLM endpoint -> one huge request eats cost and capacity.

## Interview angle
- **"How would you serve this model?"** Start from the latency need: if nobody waits, a batch job writing to a table; if a user waits, a REST/gRPC service that loads the model once, validates input, and returns JSON; if it must work offline or private, on-device. Containerise with pinned versions, ship preprocessing with the model, put it behind autoscaling and a canary. SDE analogy: it is a stateless microservice whose "binary" happens to be the model weights.
- **"Your p99 latency doubled after launch. What do you check?"** Queueing (Little's law: traffic up or concurrency limit hit), batch size / batching wait window, cold starts from autoscaling, input length growth (LLM prompts), GPU memory pressure from the KV cache, and downstream calls without timeouts.
- **"How does vLLM get high throughput?"** Continuous batching keeps the GPU full by letting new requests join at every token step; PagedAttention stores the KV cache in small blocks so memory is not wasted on fragmentation, allowing more concurrent sequences.
- **"How do you roll out a new model safely?"** Register an immutable version, shadow it to compare outputs, canary 1-5% with automatic rollback on error/latency/business guardrails, then ramp. Keep the previous version warm for instant rollback.
- **"Estimate the monthly cost of this LLM feature."** requests per month x (input tokens x input price + output tokens x output price), then cut it with caching, a smaller model for easy requests, and shorter outputs.

## Source material
To be added.
