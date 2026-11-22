# Webinar — Edge AI Experiment 1: Edge vs Cloud inference

Notebook: [Edge_AI_Experiment_1.ipynb](Edge_AI_Experiment_1.ipynb) (run on Google Colab, TF 2.21).

## The question the experiment answers

> If the same model runs **on the device** (edge) or **on a server you call over HTTP** (cloud),
> how much does the trip to the server cost you?

The notebook trains one small model, shrinks it for the edge, then runs it both ways and compares latency, throughput and data sent.

## The pipeline at a glance

```
MNIST -> train small CNN (Keras) -> save .keras
      -> convert to TFLite + int8 weight quantization -> model.tflite (54.65 KB)
            |-- EDGE:  load .tflite in-process, call interpreter.invoke()      ~0.03-0.08 ms
            '-- CLOUD: same .tflite inside a FastAPI server, client POSTs JSON  ~5.3 ms
      -> compare mean / median / P95 latency, throughput, bytes per request
```

## Part 1 — Setup (cells 1-2)
Installs `fastapi`, `uvicorn` (the web server), `requests` (HTTP client). TensorFlow and NumPy are already on Colab.

## Part 2 — Train the CNN (cells 4-11)

| Step | What happens | Why |
|---|---|---|
| Load MNIST | 60,000 train + 10,000 test grayscale 28x28 digits | Tiny, standard dataset |
| Normalize | reshape to `(N, 28, 28, 1)`, divide by 255 | Conv2D needs a channel axis; inputs in [0, 1] train better |
| Build model | Conv2D(8, 3x3) -> MaxPool(2) -> Flatten -> Dense(32) -> Dense(10, softmax) | Deliberately tiny, edge-friendly |
| Train | Adam, sparse categorical cross-entropy, 5 epochs, batch 64, 10% validation | Labels are integers 0-9, hence *sparse* |
| Evaluate | **Test accuracy 98.05%** | |
| Save | `mnist_model.keras` and one test image `test_sample.npy` (a "7") | |

**Parameter count — work it out yourself (exam-style):**

| Layer | Output shape | Params |
|---|---|---|
| Conv2D, 8 filters, 3x3, 1 input channel, `padding='same'` | 28x28x8 | (3·3·1 + 1)·8 = **80** |
| MaxPool 2x2 | 14x14x8 | 0 |
| Flatten | 14·14·8 = 1568 | 0 |
| Dense 32 | 32 | 1568·32 + 32 = **50,208** |
| Dense 10 | 10 | 32·10 + 10 = **330** |
| **Total** | | **50,618** (x 4 bytes float32 = 197.7 KB) |

Note that 99% of the weights sit in the first Dense layer — Flatten→Dense is where small CNNs get expensive.

## Part 3 — Convert to TensorFlow Lite (cell 13)

```python
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]   # dynamic-range quantization
```

- **TFLite** = a flat, compact model format plus a small interpreter, made for phones and microcontrollers (now renamed **LiteRT**).
- **Dynamic-range quantization**: weights are stored as **int8** (1 byte instead of 4); activations stay float and are computed at runtime. No calibration data needed.
- Result: Keras file 622.59 KB -> TFLite 54.65 KB, "compression ratio 11.39x".

**Careful reading the 11.39x:** quantization alone gives about **4x** (float32 -> int8: 197.7 KB -> ~50 KB). The rest comes from the `.keras` file also storing the **Adam optimizer state** (two extra copies of every weight) and metadata, which TFLite drops. So "11x" is file-to-file, not what quantization does.

## Part 4 — Edge inference (cells 14-15)

```python
interpreter = tf.lite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()
interpreter.set_tensor(input_index, x); interpreter.invoke(); interpreter.get_tensor(output_index)
```

- Input shape `[1, 28, 28, 1]`, output `[1, 10]` (one probability per digit).
- One **warm-up** run first (first call pays one-time setup cost), then 100 timed runs with `time.perf_counter()`.
- Result: predicted **7**, confidence 0.99985, **median 0.028 ms**, mean 0.079 ms, P95 0.067 ms, ~12,585 inferences/s.

**Why is mean > P95?** P95 means 95% of runs were faster than 0.067 ms — yet the mean is 0.079 ms. That only happens when a few runs (fewer than 5) were *huge* outliers (OS scheduling, garbage collection) that drag the average up. This is exactly why latency is reported as **median and P95/P99**, not just mean.

## Part 5 — "Cloud" inference with FastAPI (cells 16-19)

- **Server** (cell 16): FastAPI app with `GET /` (health check) and `POST /infer`. It loads the same `.tflite`, takes a JSON list of 784 floats, runs the model, and returns prediction, confidence, server-side time and payload bytes.
- **Start it** (cell 17): uvicorn runs in a background thread on `127.0.0.1:8000`; the loop polls `/` until it answers `{'status': 'healthy'}`.
- **Client** (cell 18): flattens the image to a list, sends it as JSON.
  - JSON payload = **5,687 bytes**, but the raw data is only 784 x 4 = **3,136 bytes**. Encoding numbers as text adds ~80% overhead.
- **Benchmark** (cell 19): 100 requests, measuring round-trip time (RTT) on the client and model time on the server.

| | Value |
|---|---|
| Model time on server | 0.13 ms |
| Round-trip time (client) | 5.30 ms mean, 6.23 ms P95 |
| HTTP + JSON overhead | **5.17 ms** — 97% of the total |

## Part 6 — Edge vs Cloud (cells 20-21)

| Metric | Edge | Cloud RTT |
|---|---|---|
| Mean latency | 0.079 ms | 5.299 ms |
| Median latency | 0.028 ms | 5.161 ms |
| P95 latency | 0.067 ms | 6.233 ms |
| Throughput | 12,585 inf/s | 189 inf/s |
| Data per request | 0 bytes | 5,687 B |
| Needs network | No | Yes |
| Prediction | 7 | 7 |

**Edge speedup ~67x, predictions match.** Cell 21 plots this as a bar chart; cell 22 just downloads the files from Colab.

## What to take away

1. **The model is not the bottleneck — the trip is.** Running the model took ~0.1 ms either way; the cloud path spent 97% of its time on HTTP and JSON.
2. **This "cloud" is on the same machine (`127.0.0.1`).** There is no real network here — no Wi-Fi, no internet, no TLS. A real cloud adds tens to hundreds of ms, so the real edge advantage is much larger than 67x. Treat 67x as a *lower bound*.
3. **The "edge" here is a Colab CPU, not a real device.** On a Raspberry Pi or a microcontroller the edge number would be slower. A fair benchmark runs on the target hardware.
4. **Edge also wins on privacy and bandwidth** (0 bytes leave the device) and **works offline** — these map to the BLERP points from CS2 (Bandwidth, Latency, Economics, Reliability, Privacy).
5. **Cloud still has its place:** large models that don't fit on the device, central updates, aggregating data from many devices.

## Gaps worth noticing (good things to try yourself)

- **Accuracy after quantization was never checked.** Run the TFLite model on all 10,000 test images and compare with 98.05%.
- **One image only.** The benchmark reuses one sample; fine for latency, but say so.
- **Throughput = 1000 / mean latency** assumes one request at a time; batching or parallel requests change it.
- Try **full int8 quantization** (needs a `representative_dataset`) and compare size, speed and accuracy.
- `tf.lite.Interpreter` is deprecated (see the warning in cell 14) — the replacement is `from ai_edge_litert.interpreter import Interpreter`.
- Send the payload as raw bytes (or base64) instead of a JSON list and see how the overhead changes.

## Quick self-check

1. Why does Conv2D with `padding='same'` keep the output 28x28?
2. Where do ~99% of this model's parameters live, and why?
3. What does dynamic-range quantization store as int8, and what stays float?
4. Why is the Keras-to-TFLite ratio 11x when int8 only saves 4x?
5. How can the mean latency be higher than the P95?
6. Why is the 67x edge speedup an underestimate of a real deployment?
