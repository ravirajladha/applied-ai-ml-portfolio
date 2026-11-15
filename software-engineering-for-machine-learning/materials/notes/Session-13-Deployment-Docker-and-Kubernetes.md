# Session 13 — Deployment: Docker & Kubernetes

> **Module 6 · Lecture 13** · Slides: `Session 13.pptx`
>
> **One-line goal:** get the trained model off your laptop and onto a machine that serves real users — **containerise it (Docker)**, then **orchestrate it (Kubernetes)**.

### Contents
1. [What deployment means in ML](#1-what-deployment-means-in-ml)
2. [Key components of ML deployment](#2-key-components-of-ml-deployment-exam-favourite)
3. [Why containers exist — the singer analogy](#3-why-containers-exist--the-singer-analogy)
4. [Containers vs Virtual Machines](#4-containers-vs-virtual-machines-exam-favourite)
5. [Docker: file, image, container](#5-docker--dockerfile-image-container-exam-favourite)
6. [Docker for ML models](#6-docker-applied-to-ml-systems)
7. [Kubernetes basics](#7-kubernetes--what-and-why)
8. [Kubernetes architecture](#8-kubernetes-architecture-exam-favourite)
9. [YAML: Pod and Deployment](#9-yaml--pod-vs-deployment)
10. [CI/CD lifecycle](#10-cicd-lifecycle)
11. [Recap](#-recap)

---

## 1. What deployment means in ML

**Deployment** in ML systems is the process of **integrating a trained machine learning model into a real-world production environment** so it can begin generating predictions on **live, unseen data**.

- Once deployed, the model becomes accessible to applications, services or end users through interfaces such as **REST or gRPC APIs**.
- Deployment also involves ensuring the model is **scalable, reliable, secure, and continuously monitored**, so it delivers accurate predictions while **adapting to changing workloads and evolving data over time**.

### Evolution of deployment

```
Physical servers  ──▶  Virtual Machines  ──▶  Containers  ──▶  Orchestrated containers
one app per box       many VMs per box      many containers    Kubernetes schedules
weeks to provision    minutes to boot       seconds to start   them across a cluster
heavy, wasteful       full OS each          share the host OS  self-healing, auto-scaling
```

> 🎯 Each step made the unit of deployment **smaller, faster to start, and cheaper to run** — until it became small enough that a scheduler could move thousands of them around automatically.

---

## 2. Key components of ML deployment (exam favourite)

| Component | What it does |
|---|---|
| **Model packaging & containerisation** | the trained model — with its **weights, dependencies, runtime environment and preprocessing steps** — is packaged into a **portable, reproducible container** using **Docker** |
| **Model serving** | the containerised model is deployed as a service, typically exposing a **REST or gRPC API** using **FastAPI** or **Flask** |
| **Scalability & orchestration** | **Kubernetes** orchestrates the Docker containers to handle high volumes of concurrent inference requests — **horizontal pod autoscaling**, **load balancing**, **self-healing** (restarting failed containers), **rolling updates** |
| **MLOps** | automates and manages the **end-to-end ML lifecycle**: model versioning, CI/CD pipelines, automated testing, deployment, monitoring, logging, performance tracking, and **model retraining** |

> 🎯 Four words: **Package · Serve · Orchestrate · Operate.**

---

## 3. Why containers exist — the singer analogy

> 🌍 **The singer analogy (straight from the deck).**
> 1. A singer is invited to a concert. He arrives — **the mike doesn't work.**
> 2. He is invited to a second concert — **the speakers don't work.**
> 3. So he **invests in his own mike and speakers and carries them to every concert.**
>
> This way, **the vagaries of the environment are avoided.** A container is the singer's own equipment.

That is exactly the "**I cannot replicate the production issue in the development environment**" problem — the same code behaving differently across **Development, Testing, CERT and Production**.

### What a container actually is

- A **software container** is a **standardised package of software**.
- **Everything needed for the software to run is inside the container.**
- The **software code, runtime, system libraries and settings** are all inside a **single container**.

> 💡 Slogan: **"Build, Ship, Run — Any App, Anywhere."**

**Docker** is the popular container technology: **lightweight, portable and self-sufficient**.

---

## 4. Containers vs Virtual Machines (exam favourite)

```
   CONTAINERS                          VIRTUAL MACHINES
┌───────────────────────┐          ┌───────────────────────┐
│ App A │ App B │ App C │          │ App A │ App B │ App C │
├───────┼───────┼───────┤          ├───────┼───────┼───────┤
│ Bins/Libs per container│          │ Bins/Libs per VM      │
├───────────────────────┤          ├───────┬───────┬───────┤
│   Container Engine    │          │Guest  │Guest  │Guest  │  ← a FULL OS each
├───────────────────────┤          │ OS    │ OS    │ OS    │
│      Host OS          │          ├───────┴───────┴───────┤
├───────────────────────┤          │      Hypervisor       │
│     Infrastructure    │          ├───────────────────────┤
└───────────────────────┘          │  Host OS / Infra      │
                                   └───────────────────────┘
```

| | **Container** | **Virtual Machine** |
|---|---|---|
| **Virtualises** | the **operating system** | the **hardware** |
| **Guest OS** | none — **shares the host OS kernel** | a **full guest OS** per VM |
| **Size** | megabytes | gigabytes |
| **Startup** | **seconds** | minutes |
| **Overhead** | minimal | high (whole OS per instance) |
| **Density** | many per host | few per host |
| **Isolation** | process-level (lighter) | hardware-level (stronger) |

> 🎯 **The single sentence:** *a VM virtualises the hardware and carries a whole OS; a container virtualises the OS and shares the host kernel — which is why it is megabytes and seconds instead of gigabytes and minutes.*

---

## 5. Docker — Dockerfile, Image, Container (exam favourite)

**Docker** is a way to **package software so that it runs on any hardware (any OS and hardware)**. It requires knowledge of **three things**:

| Term | Definition | Analogy |
|---|---|---|
| **Dockerfile** | a **blueprint for building a Docker image** — a **set of instructions** in a text file named `Dockerfile` | the **recipe** |
| **Docker Image** | a **template for running containers** — a **lightweight, standalone, executable package** that includes everything needed to run the software: **code, runtime, libraries, system tools** | the **cake mix**, ready to bake |
| **Docker Container** | a **portable unit of software** with the application plus its dependencies and configuration — it is the **running process of the image**. May include an application (Node.js web) and a database (MySQL). **One image file can spawn multiple processes across environments.** | the **baked cake** |

```
Dockerfile ──docker build──▶ Image ──docker run──▶ Container
```

### Purpose of Docker

- **Reproduce the environment** in Development, Staging and Production.
- **Define the environment** with the Dockerfile.
- Others use the Dockerfile to create an image; images are **uploaded to cloud (public or private) repositories with `docker push`** and retrieved with **`docker pull`**.

### The Dockerfile keywords

| Keyword | What it does |
|---|---|
| **`FROM`** | the base image to start from |
| **`RUN`** | execute a command **at build time** (installing packages) |
| **`COPY` / `ADD`** | copy files from your machine into the image |
| **`WORKDIR`** | set the working directory inside the image |
| **`EXPOSE`** | declare the port the container listens on |
| **`ENV`** | set an environment variable |
| **`CMD`** | the **default command at run time** (overridable) |
| **`ENTRYPOINT`** | the command that **always** runs at start |

**Worked example from the deck:**

```dockerfile
FROM ubuntu:latest
RUN mkdir /vim
RUN apt update
RUN apt install vim -y
WORKDIR /vim
ENTRYPOINT ["/bin/bash"]
```
→ `docker build` → **IMAGE** → `docker run` → **CONTAINER**

### The surrounding tools

| Tool | What it is |
|---|---|
| **Docker Desktop** | a **one-click-install application** for Mac, Linux or Windows to build and share containerised applications and microservices, with a **GUI** to manage containers, applications and images from your machine |
| **Docker Hub** | **the world's largest library and community for container images** — official images for MongoDB, Node.js, Redis, Ubuntu, Python, MySQL, etc. (`hub.docker.com`) |
| **Docker Architecture** | the **Docker client** (`docker` CLI) talks to the **Docker daemon**, which builds/runs/manages images and containers and pulls from a **registry** (Docker Hub) |

---

## 6. Docker applied to ML systems

**Containerising an ML model is one of the most common ways to deploy it in production.** The container packages everything required to run the model **consistently across environments**:

| Inside the container |
|---|
| the **trained model** (`model.pkl`, `model.onnx`, `model.pt`, `model.h5`) |
| **inference code** (a Python script or REST API) |
| **dependencies** (TensorFlow, PyTorch, scikit-learn, NumPy…) |
| **runtime environment** (Python version, OS libraries) |
| **configuration files** |
| optional **preprocessing and postprocessing** logic |

**The reference project layout:**

```
ML-Model-Container/
├── model.pkl            # the trained model
├── train.py             # training script
├── app.py               # FastAPI inference API
├── preprocess.py
├── postprocess.py
├── requirements.txt
├── Dockerfile
└── config.yaml
```

*(code: `Session 13 - dockermlexample`; basics: `Session 13 - Docker Basics.docx`)*

> ⚠️ **The classic ML container bug:** shipping the model but **forgetting the preprocessing code**. Training scaled the features one way, the container scales them another, and predictions are quietly wrong — the training/serving skew problem (see Session 14, *Feature Encoding*).

---

## 7. Kubernetes — what and why

**Kubernetes (K8s)** is a **container orchestration tool** that manages applications/services running on a container platform like Docker.

| Fact | Detail |
|---|---|
| Origin | developed by **Google labs**, later donated to the **CNCF** (Cloud Native Computing Foundation) |
| Status | the **first CNCF project to graduate**; **open source** |
| Written in | **Golang** |

### Features of Kubernetes

| Feature | What you get |
|---|---|
| **High availability** | **no downtime** |
| **Scalability** | high performance under load |
| **Disaster recovery** | **backup and restore** |

> 🌍 **Docker vs Kubernetes in one line.** Docker gives you **one** running container. Kubernetes runs **thousands** of them across many machines, restarts the ones that die, adds more when traffic spikes, and updates them without downtime. Docker is the shipping container; Kubernetes is the port.

---

## 8. Kubernetes architecture (exam favourite)

```
┌──────────────────────── CLUSTER ─────────────────────────┐
│                                                          │
│   MASTER NODE (Control Plane)                            │
│   ┌────────────┬──────┬──────────────────┬────────────┐  │
│   │ API Server │ etcd │ Controller Mgr   │ Scheduler  │  │
│   └────────────┴──────┴──────────────────┴────────────┘  │
│                          ▲                               │
│        kubectl ──────────┘                               │
│                          │                               │
│   WORKER NODES           ▼                               │
│   ┌──────────────────┐   ┌──────────────────┐            │
│   │ Node 1           │   │ Node 2           │            │
│   │  kubelet         │   │  kubelet         │            │
│   │  kube-proxy      │   │  kube-proxy      │            │
│   │  ┌────┐  ┌────┐  │   │  ┌────┐          │            │
│   │  │Pod │  │Pod │  │   │  │Pod │          │            │
│   │  └────┘  └────┘  │   │  └────┘          │            │
│   └──────────────────┘   └──────────────────┘            │
└──────────────────────────────────────────────────────────┘
```

### The core objects

| Object | Definition |
|---|---|
| **Master Node** (Control Plane) | responsible for **managing the entire cluster**; contains the API server, etcd, controller manager and scheduler |
| **Worker Nodes** | where **containers actually run**; they run the application workload and communicate with the master node |
| **Pod** | **the smallest deployable unit** you can create and manage in Kubernetes — **a group of one or more containers with shared storage and network resources** |
| **Service** | **exposes a group of pods to the network**, providing a **stable IP address and DNS name** other services and pods can use |
| **Controller** | manages the **lifecycle of pods and services** — ensures the **desired number of replicas** is running, creating or deleting pods as necessary |

### Master node components

| Component | Role |
|---|---|
| **API Server** | the **central control point** — exposes the Kubernetes API used by every other component; **stores cluster state in etcd** |
| **etcd** | a **distributed key-value store** holding the cluster's configuration data — the **single source of truth** for current cluster state, used by the API server, controller manager and scheduler |
| **Controller Manager** | runs the controllers that **regulate cluster state** — e.g. the **ReplicaSet controller** keeps the desired pod count, the **Deployment controller** manages rolling updates |
| **Scheduler** | **assigns pods to nodes**, considering **resource requirements, node availability and user-defined policies** |

### Worker node components

| Component | Role |
|---|---|
| **kubelet** | **manages the state of the node** — ensures containers are running and healthy, monitors them and **restarts them if they fail** |
| **kube-proxy** | **manages network connectivity to and from the pods** |
| **kubectl** | the **Kubernetes command-line tool** — deploy applications, inspect and manage cluster resources, view logs |

> ⚠️ **`kubectl` is not a worker-node daemon** — it is the CLI *you* run to talk to the API server. The deck lists it beside kubelet/kube-proxy; keep the roles distinct: **kubectl = you → cluster · kubelet = node agent · kube-proxy = node networking.**

> 🎯 **Memory hook for the master:** *the **API Server** takes the order, **etcd** writes it down, the **Scheduler** decides where it goes, the **Controller Manager** makes sure it stays that way.*

---

## 9. YAML — Pod vs Deployment

**Layers of abstraction:** a **Deployment** is a **template for creating pods**, written in a YAML file.

```
Deployment ──manages──▶ ReplicaSet ──manages──▶ Pods ──contain──▶ Containers
```

**A bare Pod:**

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  containers:
    - name: my-cont
      image: nginx:latest
```

**A Deployment (2 replicas):**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-deployment
spec:
  replicas: 2
  template:
    metadata:
      labels:
        app: my-app        # labels are used to manage and select resources,
    spec:                  # e.g. in Services or ReplicaSets
      containers:
        - name: my-cont
          image: nginx:latest
```

Apply either with:

```bash
kubectl apply -f pod-definition.yaml
```

| Field | Purpose |
|---|---|
| `apiVersion` | `v1` for a Pod, `apps/v1` for a Deployment |
| `kind` | the object type |
| `metadata` | name, and **labels** used to **manage and select resources, such as in Services or ReplicaSets** |
| `spec` | the desired state — for a Deployment, **`replicas`** plus the **pod `template`** |

> 🎯 **Never deploy a bare Pod in production.** A Pod that dies stays dead; a **Deployment** notices and recreates it. That self-healing is the entire point.

*(demo: `Session 13 - minikube - kubernetes`; basics: `Session 13 - Kubernetes Basics (MiniKube).docx`)*

---

## 10. CI/CD lifecycle

*(Self-study section of the deck — DevOps end-to-end demo.)*

```
Plan ──▶ Code ──▶ Build ──▶ Test ──▶ Release ──▶ Deploy ──▶ Operate ──▶ Monitor
 │                                                                          │
 └──────────────────────── feedback ────────────────────────────────────────┘

  ├──────── Continuous Integration ────────┤├──── Continuous Delivery/Deployment ────┤
```

| Term | Meaning |
|---|---|
| **CI — Continuous Integration** | every commit is automatically **built and tested**, so integration problems surface within minutes rather than at release |
| **CD — Continuous Delivery** | every passing build is **automatically prepared for release**; a human presses the button |
| **CD — Continuous Deployment** | every passing build **goes to production automatically**, no human gate |

> 💡 **For ML there is a third C — Continuous Training (CT):** monitoring detects drift → retraining is triggered → the new model is validated → it re-enters the same CD pipeline. That is the loop from Session 12 wired into DevOps.

---

## 🎯 Recap

- **Deployment** = integrating a trained model into production so it predicts on **live, unseen data**, exposed via **REST/gRPC**, and kept **scalable, reliable, secure, monitored**.
- **Four key components:** **Package** (Docker) · **Serve** (FastAPI/Flask, REST/gRPC) · **Orchestrate** (Kubernetes: autoscaling, load balancing, self-healing, rolling updates) · **Operate** (MLOps).
- **Singer analogy:** carry your own mike and speakers → the container removes the vagaries of the environment.
- **Container vs VM:** container virtualises the **OS** and **shares the host kernel** (MB, seconds); VM virtualises the **hardware** and carries a **full guest OS** (GB, minutes).
- **Docker's three things:** **Dockerfile** (blueprint/instructions) → `docker build` → **Image** (template, standalone executable package) → `docker run` → **Container** (running process). Share via `docker push`/`docker pull` on **Docker Hub**.
- **Kubernetes:** container orchestration from **Google → CNCF** (first project to graduate), written in **Go**. Gives **high availability, scalability, disaster recovery**.
- **Master node:** **API Server** (central control, stores state in etcd) · **etcd** (distributed key-value source of truth) · **Controller Manager** (ReplicaSet, Deployment controllers) · **Scheduler** (assigns pods to nodes).
- **Worker node:** **kubelet** (node/container health, restarts) · **kube-proxy** (pod networking). **kubectl** = the CLI you use.
- **Pod** = smallest deployable unit, one-or-more containers with shared storage & network. **Deployment** = YAML template creating and maintaining `replicas` of pods. Apply with `kubectl apply -f`.

⬅️ **Prev:** [Session 12 — Quality Assurance](Session-12-Quality-Assurance-Testing-and-RAGAS.md) · ➡️ **Next:** [Session 14 — Inference, Serving & Deployment Strategies](Session-14-Inference-Serving-and-Deployment-Strategies.md) · 🏠 [Back to index](README.md)
