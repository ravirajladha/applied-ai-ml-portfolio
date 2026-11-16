# Model Lifecycle & Deployment (M4, S7-S8): coverage spec

**Ladder:** Machine Learning on the Edge (AIMLCZG535) › Module 4 Model Lifecycle & Deployment   ·   **Prerequisites:** edge-foundations, edge-hardware (device tiers, accelerators), edge-data-iot; ops-serving for general serving and containers
**Why it matters for AI/ML:** A trained model is not a deployed one. Module 4 covers the edge ML pipeline (data -> train -> optimize -> deploy -> update), where training happens, the runtimes that execute models on devices (TensorFlow Lite, PyTorch Mobile/ExecuTorch, ONNX Runtime, OpenVINO, TensorRT), how to package them (Docker, Podman) and how to roll them out to fleets (EdgeX Foundry, AWS IoT Greengrass, Azure IoT Edge). The end-sem papers test it with a mixed Jetson / Intel NUC / Raspberry Pi fleet that must run one model artefact: ONNX Runtime with execution providers.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `pipeline` | Edge ML pipeline: data -> train -> optimize -> deploy -> update | the stages in order | what each stage produces (dataset, model, optimized artefact, deployed package, feedback) | why the loop closes with field data; where conversion breaks | designing the pipeline for a fleet with several hardware targets |
| 2 | `training-workflows` | Cloud-based vs on-device training | where training normally happens | why most edge models train in the cloud | on-device fine-tuning of the last layer, personalisation, memory cost of backprop | when on-device or federated training is worth it |
| 3 | `tflite` | TensorFlow Lite (LiteRT) and TFLite Micro | .tflite file, interpreter | converter, delegates (GPU, NNAPI, Edge TPU, XNNPACK) | TFLite Micro: no OS, tensor arena, op resolver, model as a C array; full-int8 for Edge TPU | Edge TPU compile partition at the first unsupported op |
| 4 | `pytorch-mobile` | PyTorch Mobile and ExecuTorch | PyTorch's on-device runtime | TorchScript and the lite interpreter; ExecuTorch as successor | torch.export -> .pte with backend delegates (XNNPACK, Core ML, QNN) | choosing PyTorch-native vs ONNX export for a fleet |
| 5 | `onnx-runtime` | ONNX and ONNX Runtime execution providers | one portable model file | providers list and priority; CPU EP always there | TensorRT/CUDA EP on Jetson, OpenVINO EP on NUC, CPU EP on Pi; graph partitioning | fallback when an EP fails, opset compatibility, engine caching in the TensorRT EP |
| 6 | `openvino-tensorrt` | OpenVINO and TensorRT | Intel's and NVIDIA's optimizers | OpenVINO IR (.xml + .bin), devices; TensorRT engine | TensorRT fusion, precision, kernel auto-tuning; why an engine is device-specific | rebuilding engines per GPU/version, Movidius support history |
| 7 | `framework-choice` | Choosing a runtime for a target or a mixed fleet | match runtime to hardware | native format vs portable format | the papers' one-artefact mixed fleet | trade-offs: peak speed vs portability vs maintenance |
| 8 | `containers` | Containerization and microservices (Docker, Podman) | what a container is | multi-arch images, Podman daemonless/rootless | GPU access on Jetson, base image tied to JetPack, layer reuse over cellular | memory limits, microservice split of the edge app |
| 9 | `orchestration` | Deployment orchestration (EdgeX Foundry, AWS IoT Greengrass, Azure IoT Edge) | what each platform is | Greengrass components and deployments; IoT Edge modules, edgeAgent, edgeHub | deployment manifests, thing groups, target conditions, offline behaviour | choosing a platform; layered deployments and priorities |
| 10 | `update-hooks` | Model monitoring hooks and update mechanisms | why a deployed model needs hooks | version, latency and confidence logging; model as a separate artefact | update via desired properties / component versions; hash verification; atomic swap | safe update design across a fleet (rollback trigger, version pinning) |

## Must-know facts
- The edge ML pipeline: data -> train -> optimize -> deploy -> update, and update feeds new data back to training. Deployment is the start of the loop, not the end.
- Most edge models are trained in the cloud and only run inference on the device. On-device training is usually limited fine-tuning (last layer, personalisation) because backprop needs gradients, optimizer state and stored activations.
- TensorFlow Lite (now LiteRT) runs .tflite FlatBuffer files with an interpreter; delegates hand supported ops to accelerators (GPU, NNAPI, Hexagon, Core ML, Edge TPU); XNNPACK accelerates the CPU path.
- TFLite Micro runs on MCUs without an OS or dynamic memory: the model is compiled in as a C array, all tensors live in a fixed tensor arena, and an op resolver registers only the ops used.
- The Edge TPU needs a fully int8-quantized model compiled with edgetpu_compiler; at the first unsupported op the graph is cut and that op and everything after it run on the CPU.
- PyTorch Mobile (TorchScript + lite interpreter) is superseded by ExecuTorch: torch.export -> edge dialect -> backend delegates (XNNPACK, Core ML, Qualcomm QNN, Arm Ethos-U, Vulkan) -> a .pte file run by a small C++ runtime.
- ONNX is a framework-neutral graph format; ONNX Runtime runs it through execution providers (EPs) chosen by a priority list. The CPU EP is always available and runs any node no other EP claims.
- Mixed fleet, one artefact: model.onnx + ONNX Runtime; TensorRT EP (or CUDA EP) on Jetson, OpenVINO EP on the Intel NUC, CPU EP on the Raspberry Pi.
- If an accelerator EP cannot initialise, the session falls back to the next provider and finally the CPU EP: the app keeps running, slower. Monitor for it, because the latency SLA may now be broken.
- A TensorRT engine is compiled for one GPU architecture (compute capability) and one TensorRT version; it is not portable across devices or upgrades and must be rebuilt (the ORT TensorRT EP builds and caches it on each device from the same ONNX file).
- TensorRT optimizes by layer and tensor fusion, FP16/INT8 precision (INT8 with calibration), kernel auto-tuning for the exact GPU, and memory reuse.
- OpenVINO's IR is a pair: .xml (topology) + .bin (weights); it runs on Intel CPU, integrated GPU and NPU, with an AUTO device plugin. Movidius (MYRIAD/NCS2) support ended after the 2022.3 LTS release.
- Containers on the edge must match the CPU architecture: multi-arch images (linux/amd64, linux/arm64, linux/arm/v7) under one tag; the wrong one fails with 'exec format error'.
- Podman is daemonless and rootless by default with a Docker-compatible CLI; Jetson containers need the NVIDIA container runtime and an L4T base image matching the JetPack version.
- AWS IoT Greengrass v2: the nucleus on the device runs components (recipe + artefacts) deployed from the cloud to things or thing groups. Azure IoT Edge: the edgeAgent pulls and runs modules from a deployment manifest; the edgeHub brokers messages and stores them while offline. EdgeX Foundry: vendor-neutral open-source microservices (device, core, application services), usually run with Docker Compose.
- Update hooks: log model version, latency, confidence and input statistics; ship the model as a versioned artefact with a hash; swap atomically and report the running version back.

## Common traps (each one must have at least one question)
- Shipping a TensorRT engine built on a desktop GPU to a Jetson -> it will not load; engines are device- and version-specific.
- "One artefact" read as "one TensorRT engine for all" -> the portable artefact is the ONNX file; per-device engines are built locally.
- Assuming an EP failure crashes the app -> ORT falls back to the CPU EP; the risk is a silent latency regression.
- Listing CPUExecutionProvider first -> it claims every node and the accelerator is never used.
- Expecting the Edge TPU to run a float model or to resume after an unsupported op -> it needs full int8, and ops after the first unsupported one run on the CPU.
- Thinking TFLite Micro can malloc or load a model file from disk -> fixed arena, model compiled in.
- On-device training assumed to be as cheap as inference -> gradients, optimizer state and activations multiply memory.
- Pulling an amd64 image on a Raspberry Pi -> exec format error.
- Baking the model into the app image -> every model update re-ships the whole image over cellular.
- Comparing model versions as strings ("1.10" < "1.9") -> wrong rollout target.
- Deploying an unverified download -> always check a hash or signature before swapping.
- Greengrass / IoT Edge treated as model optimizers -> they deploy and manage software; they do not compress models.
- PyTorch Mobile treated as the current path -> ExecuTorch replaced it.

## Interview angle
1. **"You have Jetsons, Intel NUCs and Raspberry Pis. How do you ship one model?"** Export to ONNX, run ONNX Runtime everywhere, and pick providers per device: TensorRT/CUDA on Jetson, OpenVINO on the NUC, CPU on the Pi. The CPU EP is the safety net.
2. **"Why not just ship the TensorRT engine?"** It is compiled for one GPU architecture and TensorRT version; it will not run on the NUC or Pi, and may not even run on a different Jetson or after a JetPack upgrade.
3. **"TFLite vs TFLite Micro?"** TFLite runs on phones and Linux boards with an OS and file system; TFLite Micro runs on MCUs with a static arena and the model as a C array.
4. **"Greengrass or Azure IoT Edge?"** Both deploy containerised or packaged components to device groups from the cloud and work offline; choose by the cloud you already use. EdgeX is vendor-neutral and on-prem.
5. **"How do you update a model on 5,000 devices?"** Versioned artefact with a hash, separate from the app image; deploy through the platform to a group; device verifies, swaps atomically, reports its version and metrics; roll back on failure.

## Source material
- Handout (`edge-src/handout.txt`), session 7 (Model Lifecycle & Deployment I): edge ML pipeline data -> train -> optimize -> deploy -> update; cloud-based vs on-device training workflows; model deployment frameworks TensorFlow Lite, PyTorch Mobile, ONNX Runtime, OpenVINO, TensorRT (T1 Ch 6, 4, 5; R1 Ch 7).
- Handout, session 8 (Model Lifecycle & Deployment II): containerization and microservices (Docker, Podman); deployment orchestration EdgeX Foundry, AWS Greengrass, Azure IoT Edge; model monitoring hooks and update mechanisms (MLOps integration) (T1 Ch 9, 10; R1 Ch 7).
- Lab experiment 4 (M4): convert a pre-trained CNN into a TFLite model and deploy it on a local edge simulator.
- End-sem Sep 2026 Set 1 Q1: logistics fleet of Jetson AGX Orin (hubs), Intel NUC (depots), Raspberry Pi 4 (vans); one codebase and one model file -> ONNX Runtime; why a TensorRT engine fails; execution providers per device; a device with no accelerator runs on the CPU EP.
- End-sem Sep 2026 Set 2 Q1: smart-city fleet of Jetson Orin NX, Intel NUC and bus-mounted Raspberry Pi 4; same mandate; a botched driver update stops the GPU EP on some Jetsons -> the app falls back to the CPU EP and keeps running, which matters at city scale.
- **Exam patterns:** the bank mirrors the Q1 pattern with new fleets (agriculture drones, hospital carts, retail stores, toll plazas): pick the framework, explain why the native engine fails, name the EP per device, and predict the fallback behaviour. Numeric `out` questions cover provider selection, graph partitioning, engine-cache compatibility, layer-reuse download costs, memory for on-device training and version comparison.
- **Standard practice (no slides exist):** TFLite converter and delegates, TFLite Micro (arena, op resolver, C array), Edge TPU compilation, PyTorch Mobile -> ExecuTorch, ONNX opsets and graph partitioning, OpenVINO IR and devices, TensorRT build steps and portability, multi-arch Docker images, Podman, NVIDIA container runtime, Greengrass v2 components and deployments, Azure IoT Edge runtime and deployment manifests, EdgeX service layers and update-hook design are written from T1 (Ch 4-6, 9-10) and vendor documentation.
- **Framework reconstructed:** the handout names the pipeline only as five words; the questions treat each stage by what it produces and test the reasoning (why update must loop back, where conversion belongs), not one exact wording. The brief's shorter "train -> optimize -> deploy -> update" is the same loop without the data stage.
- **Gaps flagged:** the papers expect fallback to the CPU EP when the GPU EP fails. In ONNX Runtime this is the behaviour when an EP is unavailable or rejects nodes; a provider that throws during session creation can also surface as an error, depending on version and options, so production code should catch it and retry with a reduced provider list. Questions follow the papers and note this. PyTorch Mobile is now deprecated in favour of ExecuTorch, and the handout's "EdgeX Analytics Services" and "MLOps integration" have no further detail.
