# Session 16 — Course Review

> **Lecture 16** · Slides: `Session 16.pptx` (6 slides — course review and discussion)
>
> **One-line goal:** the map of the whole course, and what the exam actually weighs.

---

## 1. The SE4ML course structure — eight modules

| Module | Description | Sessions |
|---|---|---|
| **1** | **Foundations of ML Systems Engineering** | 1–2 |
| **2** | **Requirements Engineering for ML Systems** | 3 |
| **3** | **Architecture & Design** | 4–7 |
| **4** | **Implementation and Code Sharing** | 9–11 |
| **5** | **Quality Assurance** | 12 |
| **6** | **Deployment** | 13–14 |
| **7** | **Responsible ML Engineering** | 15 |
| **8** | **Application of SE Principles for Agentic AI** | woven through 7, 10, 12 |

> 💡 **Module 8 has no dedicated session** — Agentic AI is applied *inside* the other modules: coordination patterns in **S7**, OOP for agents in **S10** and **S12**, AgentOps in **S14**.

---

## 2. Evaluation components

| Component | Name | Type | Weight | Comments |
|---|---|---|---|---|
| **EC-1** | Quiz | Online | **5%** | before mid-term |
| | Situated Learning | Online | **5%** | after mid-term |
| | Assignment I | Online | **10%** | before mid-term |
| | Assignment II | Online | **10%** | after mid-term |
| **EC-2** | **Mid-term Exam** | **Closed book** | **30%** | 2 hours |
| **EC-3** | **End Semester Exam** | **Open book** | **40%** | **2.5 hours** |

> 🎯 **The end-sem is OPEN BOOK, 40%, 2.5 hours.** That changes how to prepare: you are not being tested on recall, you are being tested on **finding the right frame fast and applying it to a scenario**. Bring **tables and decision rules**, not prose — see the revision packs in [`../../revision/`](../../revision/README.md).

---

## 3. The course in one spine

```
S1–2   Foundations       the model is a small box inside a much larger system
  ↓
S3     Requirements      when to even use ML; goals → requirements (GR4ML)
  ↓
S4     Quality attributes  the "how well" that architecture must deliver
  ↓
S5–7   Architecture      CQRS · RAG · Monolith/Microservices · Event-driven ·
                         Model registry · SAGA · Blackboard · Agentic AI
  ↓
S9–11  Implementation    good code · complexity · data structures · OOP ·
                         errors/logging · style · refactoring · APIs · packaging
  ↓
S12    Quality Assurance data/model/pipeline/system tests · slicing ·
                         production experimentation · security · RAGAS
  ↓
S13–14 Deployment        Docker · Kubernetes · serving designs ·
                         deployment strategies · MLOps/LLMOps/AgentOps
  ↓
S15    Responsible ML    versioning/provenance/reproducibility · explainability ·
                         fairness · safety · security · privacy
```

> 🎯 **The spine, in one sentence:** *an ML model is a small box inside a much larger software system, and engineering that system well — specifying it, architecting it, coding it, testing it, deploying it and taking responsibility for it — is the real job.*

---

⬅️ **Prev:** [Session 15 — Responsible ML Engineering](Session-15-Responsible-ML-Engineering.md) · 🏠 [Back to index](README.md)
