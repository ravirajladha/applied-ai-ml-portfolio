# Edge Hardware & Systems (M2, S3-S4): coverage spec

**Ladder:** Machine Learning on the Edge (AIMLCZG535) › Module 2 Edge Hardware & Systems (Sessions 3-4)   ·   **Prerequisites:** edge-foundations
**Why it matters for AI/ML:** Once Module 1 says "inference must run at the edge", Module 2 decides on what. It covers the hardware tiers (MCUs, gateways, mobile devices, edge servers), the accelerator zoo (CPU, GPU, NPU, TPU, DSP, FPGA), the course's platforms (Jetson, Coral, Movidius, Raspberry Pi, Arduino), ARM vs RISC-V, hardware-software co-design, power and performance profiling, and the software environments (RTOS, embedded Linux, TinyML runtimes). The mid-sem papers test it with ₹ break-even volumes for a custom ASIC vs an off-the-shelf SoC vs an MCU plus external chip, and with a model that fits in Flash but crashes because its tensor arena does not fit in SRAM.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `tiers` | Edge hardware tiers: MCUs, gateways, mobile devices, edge servers | the four tiers and an example of each | typical clock, RAM, power and OS per tier | choosing a tier from a workload's data rate, model size and power budget | over- and under-provisioning across a fleet |
| 2 | `accelerators` | AI accelerators: CPU, GPU, NPU, TPU, DSP, FPGA | what an accelerator is | strengths of each type | TOPS, TOPS/W, INT8-only accelerators, peak vs achieved throughput | operator coverage, CPU fallback and memory-bound layers |
| 3 | `platforms` | Edge platforms: Jetson, Coral, Movidius, Raspberry Pi, Arduino | which platform is which | toolchain per platform (TensorRT, Edge TPU compiler, OpenVINO, TFLite, TFLite Micro) | matching a platform to a product | Edge TPU compilation and partial delegation |
| 4 | `arm-riscv` | Edge processors: ARM vs RISC-V | both are instruction set architectures | licensed vs open ISA, Cortex-M vs Cortex-A | extensions (NEON, Helium, RVV), ecosystem maturity | choosing an ISA for a product: risk, cost, custom instructions |
| 5 | `memory` | Memory on MCUs: Flash, SRAM and the tensor arena | Flash stores, SRAM computes | weights in Flash, activations in SRAM | peak activation memory and why "fits in Flash" is not enough | reducing the arena: resolution, width multiplier, operator order, in-place ops |
| 6 | `codesign` | Hardware-software co-design and deployment environments | design model and hardware together | SoC vs MCU + external accelerator | quantize for the accelerator, op support, interface bottlenecks | system-level trade-offs: BOM, power, board area, supply |
| 7 | `power-profiling` | Power and performance profiling for AI workloads | power vs energy | P = V × I, energy = P × t, duty cycling | average power and battery life by hand, profiling tools | race-to-idle vs slow-and-low, thermal throttling |
| 8 | `rtos-tinyml` | RTOS, embedded Linux and TinyML environments | what an RTOS is | RTOS vs embedded Linux | TFLite Micro: no OS, no dynamic allocation, static arena | determinism, MMU, update and security implications |
| 9 | `economics` | Hardware economics: NRE, unit cost and break-even | NRE and unit cost | total cost = NRE + units × unit cost | break-even volume = NRE ÷ unit-cost difference; option C vs SoC | what break-even ignores: time to market, risk, respins |

## Must-know facts
- Tiers (rough orders of magnitude): MCU (Cortex-M, ESP32: 10s-100s of MHz, KB to ~1 MB SRAM, up to a few MB Flash, mW, bare metal or RTOS); gateway / single-board computer (Raspberry Pi, industrial gateway: Cortex-A, GBs of RAM, a few W, Linux); mobile devices (phone SoCs with CPU + GPU + NPU + DSP, a few W); edge servers (x86 + GPU, tens to hundreds of W).
- CPU: flexible, sequential. GPU: thousands of parallel lanes, FP16/INT8, power-hungry. NPU: fixed MAC arrays for neural ops, efficient INT8. TPU: Google's matrix ASIC (Edge TPU: about 4 TOPS INT8 at about 2 W). DSP: efficient fixed-point multiply-accumulate for audio and signal processing. FPGA: reconfigurable logic, deterministic low latency, harder to program.
- TOPS = tera operations per second; one MAC = 2 ops. Peak TOPS is rarely reached: memory bandwidth and unsupported operators set the real speed. TOPS/W measures efficiency.
- Edge TPU and many NPUs run INT8 only; models must be fully integer-quantized and compiled (edgetpu_compiler). Unsupported ops run on the host CPU, and every switch costs time.
- Platforms: NVIDIA Jetson (Nano, Orin Nano/NX, AGX Orin; CUDA, TensorRT, JetPack), Google Coral (Edge TPU USB stick, Dev Board; TFLite), Intel Movidius (Myriad X VPU, Neural Compute Stick 2; OpenVINO), Raspberry Pi (Cortex-A CPU, Linux, TFLite / ONNX Runtime; add-on accelerators), Arduino (Nano 33 BLE Sense: Cortex-M4F at 64 MHz, 1 MB Flash, 256 KB SRAM; TFLite Micro).
- ARM: a licensed, proprietary ISA with a huge ecosystem (Cortex-M for MCUs, Cortex-A for application processors; CMSIS-NN, NEON, Helium on Cortex-M55/M85, Ethos-U micro-NPUs). RISC-V: an open, royalty-free ISA with a small base plus optional extensions (M, A, F, D, C, V) and room for custom instructions; younger tooling.
- Flash is non-volatile and holds the program and the weights; SRAM is volatile working memory for activations, the tensor arena, stack and heap. A model can fit in Flash and still fail because its peak activations do not fit in SRAM.
- Peak activation memory ≈ the largest sum of tensors alive at the same time (typically a layer's input + output). Lower input resolution shrinks it quadratically; a smaller width multiplier shrinks it linearly.
- TFLite Micro runs without an OS, uses no dynamic allocation, and takes one statically allocated tensor arena whose size you choose; AllocateTensors() fails (or the device crashes) if it is too small.
- RTOS (FreeRTOS, Zephyr): deterministic priority-based scheduling, KB footprint, no MMU required. Embedded Linux (Yocto, Raspberry Pi OS): rich drivers, networking, containers, needs an MMU and far more RAM, not hard real-time by default.
- Power: P = V × I; energy = P × t. Average power with duty cycle d = d × P_active + (1 − d) × P_sleep. Battery energy (J) = mAh × V × 3.6.
- Co-design: pick operators the accelerator supports, quantize for it, size the model to the memory, and choose the hardware for the model family. Option C (MCU + external accelerator) adds a chip-to-chip link (SPI/USB/PCIe), board area, power and integration work compared with a single SoC.
- Total cost = NRE + units × unit cost. Break-even volume between a high-NRE / low-unit option and a no-NRE / high-unit option = NRE ÷ (unit cost difference). 1 crore = 10^7; 1 lakh = 10^5.
- If neither option has NRE, the cheaper per-unit option is cheaper at every volume: no break-even exists.

## Common traps (each one must have at least one question)
- "The model is 3.5 MB and Flash is 4 MB, so it will run" -> activations need SRAM; check the arena size.
- Comparing accelerators on peak TOPS only -> real throughput depends on memory bandwidth, supported ops and utilisation.
- Thinking a GPU is always the most power-efficient choice -> NPUs/Edge TPUs give more inferences per joule for INT8 CNNs.
- Deploying a float model to the Edge TPU -> it needs full INT8 quantization and compilation; otherwise it runs on the CPU or fails.
- "RISC-V is a chip" -> it is an ISA; many vendors make RISC-V cores.
- "Open ISA means free chips" -> the ISA licence is free; design, verification and fabrication still cost money.
- Using crore = 10^6 -> 1 crore = 10^7, so ₹4 crore = ₹40,000,000.
- Dividing NRE by the wrong difference (or by one unit cost) -> divide by (expensive unit − cheap unit).
- Forgetting to round the break-even volume up -> you need whole units; the crossover is the next integer.
- Claiming a break-even between two options with no NRE -> the lower unit cost wins at every volume.
- Confusing power and energy -> a 5 W chip that finishes in 2 ms uses less energy than a 1 W chip that takes 20 ms.
- Assuming embedded Linux is real-time -> it needs PREEMPT_RT or an RTOS core for hard deadlines.
- Option C cheaper per unit, so it is always better -> integration, board space, power and a slow chip-to-chip link can erase the saving, and an external chip that is not an accelerator does not run the model.

## Interview angle
1. **"Your model fits in Flash but the MCU crashes on the first inference. Why?"** The tensor arena (activations, scratch buffers) does not fit in SRAM. Measure the arena with the interpreter, then lower the input resolution, use a smaller width multiplier, or pick a chip with more SRAM.
2. **"Edge TPU vs Jetson for a camera product?"** Edge TPU: INT8 CNNs at ~2 W, cheap, but only supported TFLite ops. Jetson: CUDA/TensorRT, flexible (FP16, transformers, multiple streams) at 10-60 W and higher cost.
3. **"When does a custom ASIC make sense?"** When volume is above NRE ÷ (unit-cost saving), the design is stable, and time to market allows a 12-24 month silicon cycle.
4. **"ARM or RISC-V for a new sensor?"** ARM for ecosystem, tools and certified IP; RISC-V for royalty-free cost at scale, custom instructions and supply-chain independence, accepting younger tooling.
5. **"How do you profile power on an edge device?"** Measure current with a power analyser (or tegrastats on Jetson), compute energy per inference = average power × latency, and model battery life with the duty cycle.

## Source material
- Handout (`edge-src/handout.txt`), Session 3 sub-topics: Edge hardware tiers: MCUs, gateways, mobile devices, edge servers; AI accelerators: CPUs, GPUs, NPUs, TPUs, DSPs, FPGAs; Edge platforms: Jetson, Coral, Movidius, Raspberry Pi, Arduino (T1 Ch 3, R1 Ch 5).
- Handout, Session 4 sub-topics: Hardware–software co-design and deployment environments; Power and performance profiling for AI workloads; Role of RTOS, embedded Linux, and TinyML environments (T1 Ch 3, R1 Ch 5).
- Handout course description: microcontrollers and embedded systems, edge processors (ARM, RISC-V), AI accelerators, Edge TPU, neural compute sticks, power consumption considerations. Lab Exp 2 (M2): deploy a simple model on a simulated Jetson Nano or Coral Edge TPU and explore ARM and RISC-V trade-offs.
- Jun 2026 mid-sem Set 1 Q4: 10,000-unit product; A = custom NPU ASIC ₹250/unit + ₹4 crore NRE, B = off-the-shelf NPU SoC ₹1,100/unit, C = ARM MCU ₹180 + ₹600 external accelerator. Break-even A vs B = 4×10^7 ÷ 850 ≈ 47,059 units; C (₹780) is cheaper than B at every volume; 10,000 is far below break-even.
- Jun 2026 mid-sem Set 2 Q4: 20,000 units; A = ₹400 + ₹6 crore NRE, B = ₹950, C = ₹220 + ₹480 external BLE module. Break-even ≈ 109,091 units; totals at 20,000: A ₹6.8 crore, B ₹1.9 crore, C ₹1.4 crore. (Note: C's external chip is a BLE radio, not an accelerator, so C's ML capability must be checked, not assumed.)
- Jun 2026 mid-sem Set 1 Q1(d): INT8 MobileNetV2, 3.5 MB file in 4 MB Flash on an STM32H7, crashes immediately: the tensor arena / activations do not fit in SRAM; check peak RAM before deploying.
- Exam patterns: (1) break-even = NRE ÷ (unit cost B − unit cost A), rounded up, with crore = 10^7; (2) "is C cheaper at all volumes?" -> with no NRE on either side, compare unit costs only; (3) total cost at the planned volume for each option and the lesson that custom silicon only pays at high volume; (4) Flash vs SRAM diagnosis of a crashing MCU deployment.
- **Standard practice:** there are no slides for this course. Tier specifications, accelerator characteristics, platform toolchains, ARM vs RISC-V details, TFLite Micro's arena model, RTOS vs embedded Linux, power formulas and profiling tools are written from T1 Ch 3 and general embedded-systems knowledge. Figures such as "Edge TPU ≈ 4 TOPS at ≈ 2 W" and the Arduino Nano 33 BLE Sense specs are vendor datasheet values quoted as approximations.
- **Gap flagged:** the papers do not say whether option C's external chip can run the model (Set 1 calls it an accelerator, Set 2 a BLE module). The bank treats break-even purely as cost arithmetic and adds separate questions on whether the cheaper option is technically adequate.
