# Cloud-Native Applications (S2-S3): coverage spec

**Ladder:** API-driven Cloud Native Solutions (AIMLCZG549) › Cloud-Native Applications (S2-S3)   ·   **Prerequisites:** cnas-apis (HTTP, REST), basic Git; cnas-containers-k8s goes deep on Docker and Kubernetes
**Why it matters for AI/ML:** Every model the course later serves (MLflow, RAG, IoT analytics) runs as a cloud-native service. Sessions 2-3 give the vocabulary the rest of the course and the midsem assume: cloud-enabled vs cloud-based vs cloud-native, monolith vs microservices, serverless, DevOps, CI/CD, GitOps and containers.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `modern-apps` | Modern application requirements and the cloud-native evolution | the four general requirements; quality attributes | the four shifts of the last years; cloud-native = DevOps + microservices + containers + cloud | mapping a requirement (zero downtime, short feedback) to a practice | trade-offs among quality attributes in a design |
| 2 | `cloud-models` | Cloud-enabled vs cloud-based vs cloud-native | what each means | which one a given app is; "where vs how" | focus areas: design for failure, implementation speed, pricing | classifying a migration and its limits; lift-and-shift cost traps |
| 3 | `microservices` | Monolith vs microservices (food delivery, FTGO) | monolith and microservice definitions | monolith limitations; SRP; API-first design | scaling one service vs the whole app; deployment frequency | when microservices are the wrong choice; distributed-monolith smells; chained availability |
| 4 | `pipelines` | CI/CD pipelines for monolith vs microservices | single pipeline vs pipeline per service | FTGO monolithic hell | pipeline time and blast radius by hand | shared-library and contract-test traps in per-service pipelines |
| 5 | `service-mesh` | Service mesh (sidecar, mTLS, retries) | what a mesh is | sidecar proxy; data plane vs control plane | mTLS, retries, timeouts, traffic split moved out of code | when a mesh is overkill; retry success odds |
| 6 | `serverless` | Serverless, FaaS, the serverless stack, AWS Lambda | serverless and FaaS definitions; examples | compute + database + HTTP gateway (Lambda, DynamoDB, API Gateway); the thumbnail example | cold start; pay-per-use cost by hand in ₹ | serverless vs always-on break-even; lock-in; long-running jobs |
| 7 | `devops` | DevOps definition, dimensions, process, team formation | DevOps definition | people/process/products = culture/methodology/tools | the DevOps loop stages; team formation (you build it, you run it) | anti-patterns: a separate "DevOps team" silo |
| 8 | `ci-cd` | Continuous integration, delivery and deployment | what CI is | delivery vs deployment: the manual approval | picking the practice for a scenario; staging tests | regulated release, feature flags, broken-main cost |
| 9 | `gitops` | GitOps | Git as the single source of truth | pull-based reconciliation; Argo CD / Flux; tooling table | drift detection and self-healing; rollback by git revert | push vs pull security; secrets in Git |
| 10 | `containers-intro` | Containers, VMs vs containers, Kubernetes intro, CNCF | what a container is; Docker | VM vs container (guest OS vs shared kernel) | density by hand; Kubernetes' role (orchestration) | what containers do not isolate |
| 11 | `twelve-factor` | The twelve-factor app and the CNCF landscape | what the 12-factor app is; CNCF | config in env, stateless processes, logs as streams | spotting factor violations in a design | backing services, disposability and dev/prod parity in a real migration |

## Must-know facts
- General requirements of modern apps: zero downtime, shortened feedback cycles, mobile and multi-device support, data driven.
- The course's evolution formula: Cloud-native app = DevOps + Microservices + Containers + Cloud.
- Cloud-enabled: a legacy monolith, on-premises, that integrates with some cloud services; cannot use cloud scalability because the architecture stays monolithic.
- Cloud-based: an existing app moved to the cloud without redesign (lift and shift); gains managed resources, pay-per-use, scaling.
- Cloud-native: born in the cloud and built of small, independent, loosely coupled services; "cloud is where we compute, cloud-native is how" (IBM).
- Focus areas: cloud-native designs for failure; deploys faster from container images; uses consumption-based pricing.
- Microservices: autonomous, loosely coupled, independently deployable services modelled around a business domain, each one business capability (Single Responsibility Principle: gather things that change for the same reason).
- Monolith limitations: technology barrier, scale only as a whole, size/complexity, every new joiner must understand everything.
- Monolith = one build pipeline (a bug fix delays every feature); microservices = one pipeline per service (pipeline-per-service pattern).
- A service mesh moves service-to-service concerns (mTLS, retries, timeouts, traffic splitting, telemetry) into sidecar proxies (data plane) configured by a control plane.
- Serverless: run on demand, pay only for the resources used, no infrastructure to manage; FaaS examples AWS Lambda, Google Cloud Functions, Azure Functions.
- The serverless stack: compute (Lambda) + database (DynamoDB) + HTTP gateway (API Gateway).
- Serverless drawbacks: not for long-running work (Lambda's limit is 15 minutes), vendor lock-in, cold start.
- DevOps (Microsoft): the union of people, process and products (culture, methodology, tools) to continuously deliver value.
- CI: commit to the shared repo often; a CI service builds and runs unit tests on every change.
- Continuous delivery: every change is automatically prepared and tested in staging; production needs a manual approval. Continuous deployment: no manual approval.
- GitOps (Weaveworks, 2017): Git is the single source of truth for declarative config; an agent in the cluster (Argo CD, Flux) pulls and reconciles.
- Containers share the host kernel; VMs each carry a guest OS on a hypervisor. Kubernetes orchestrates containers (deployment, scaling, operation); it came from Google and was donated to the CNCF.

## Common traps (each one must have at least one question)
- "Moved to AWS" taken as cloud-native -> that is cloud-based; without redesign it is not cloud-native.
- Cloud-native read as "runs in a public cloud" -> it is about how it is built, not where.
- Microservices assumed always better -> small teams and simple domains pay distributed-system costs for nothing.
- Microservices sharing one database -> a distributed monolith; services cannot deploy independently.
- Chained synchronous calls assumed as available as one service -> availabilities multiply.
- Continuous delivery confused with continuous deployment -> the difference is the manual approval to production.
- CI read as "a CI server exists" -> CI means merging small changes to main often, with automated build and tests.
- Serverless read as "no servers" -> servers exist; the provider manages them.
- Serverless assumed cheaper at any load -> at steady high load an always-on instance can be cheaper.
- Cold start blamed on the code -> it is a new execution environment being created after idle time.
- Running a 40-minute batch job on Lambda -> exceeds the 15-minute limit.
- GitOps treated as "CI pushes kubectl apply" -> GitOps is pull-based reconciliation from Git.
- kubectl edit in production under GitOps -> the agent reverts the drift to what Git says.
- Containers assumed to include a full OS kernel -> they share the host kernel.
- A "DevOps team" between dev and ops -> recreates the silo DevOps was meant to remove.
- Config hard-coded in the image -> twelve-factor puts config in the environment.
- Service mesh retries on non-idempotent POSTs -> duplicate orders.

## Interview angle
1. **"Cloud-based vs cloud-native?"** Cloud-based is an existing app lifted to the cloud for managed infrastructure and pay-per-use; cloud-native is designed for the cloud: microservices, containers, CI/CD, designed for failure and elastic scaling.
2. **"When would you not split into microservices?"** Small team, unclear domain boundaries, low scale. Start with a modular monolith and split when a part needs independent scaling or release.
3. **"Continuous delivery vs deployment?"** Both automate build, test and staging; delivery stops for a human approval before production, deployment does not.
4. **"What does GitOps add over CI/CD?"** Git holds the desired state; an in-cluster agent pulls and reconciles, so drift is reverted, the audit trail is git log and rollback is git revert; CI no longer needs cluster credentials.
5. **"When is serverless a bad fit?"** Long-running or steady high-throughput workloads, strict latency (cold starts) and portability needs (lock-in).

## Source material
- Old-batch slides (`cloud-src/cnas-cloudnative.txt`, deck p48-97) and handout sessions 2-3: Cloud Native Application module (DevOps and GitOps, microservices and service mesh, containers and Kubernetes, serverless computing and serverless stack).
- Modern application requirements: zero downtime, shortened feedback cycles, mobile/multi-device, data driven; the quality-attribute list; the four shifts (monolith -> microservices, on-prem -> cloud, VM -> Docker/Kubernetes, traditional CI/CD -> cloud-native CI/CD).
- Evolution: cloud-native app = DevOps + microservices + containers + cloud; cloud-enabled vs cloud-based vs cloud-native with the Red Hat, VMware and IBM definitions and the focus areas (design, implementation, pricing).
- Monolith and microservices: the food-delivery monolith and its microservices/API-first version, monolithic limitations, Robert C. Martin's SRP, deployments per day (Amazon 23,000, Google 5,500, Netflix 500, Twitter 3/week), the FTGO "monolithic hell" pipeline vs pipeline-per-service.
- Serverless: definition, FaaS examples, the image-upload thumbnail example, the serverless stack (Lambda + DynamoDB + API Gateway) and the Fiddler demo with GET/POST Lambdas, drawbacks (long-running jobs, lock-in, cold start).
- DevOps: definitions (alignment of Dev and Ops; Microsoft's people/process/products), CI, continuous delivery, continuous deployment, the CI/CD pipeline, team formation.
- GitOps: Weaveworks 2017, Atlassian and GitLab definitions, the tooling table (Git hosts, CI tools, Argo CD/Flux/Spinnaker, registries, IaC, config managers, orchestrators).
- Containers, Docker, VMs vs containers and the Kubernetes introduction (Google, CNCF, Go). Kubernetes stays at intro level here; cnas-containers-k8s covers its architecture, YAML and deployment strategies.
- No past papers; scenario style modelled on BITS WILP papers (Bengaluru food-delivery startup, Pune smart-city, agritech cooperative, ₹ costs).
- **Standard practice (slides thin or image-only):** service mesh (sidecar, data/control plane, mTLS, retries, traffic split), the twelve-factor app, the CNCF landscape, the DevOps loop stages and team topologies, GitOps pull vs push and drift, serverless pricing (GB-seconds) and the 15-minute Lambda limit, chained availability, and container density are written from R3 Cloud Native Patterns, the twelve-factor site and vendor documentation. The technologies pyramid and the DevOps dimensions slides are images in the extract, so they are tested only through the text around them.
- **Slide notes:** the slide's "Lambda keeps containers alive for 30-45 minutes" is an observation, not a documented guarantee; AWS does not publish an idle timeout and it is often much shorter, so questions treat the window as a given number in a scenario. The Twitter "3/week" figure is dated. GitOps was coined by Alexis Richardson (the slide spells it "Richarson").
