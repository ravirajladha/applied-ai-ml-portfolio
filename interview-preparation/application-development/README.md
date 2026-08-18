# Application Developer interview preparation

**Open it in a browser: https://ravirajladha.github.io/applied-ai-ml-portfolio/interview-preparation/application-development/**
— works on phone and desktop, no install, nothing to run.

Revision notes for a mid-level (roughly 4–6 year) **cloud-native application developer** role:
Python, JavaScript/TypeScript, C# or Java, API and microservice design, Azure, Git and CI/CD,
databases and data engineering, and integrating ML models into applications.

Each page opens with a **concepts primer written from zero** before the interview questions start,
so it works whether you are revising a topic or meeting it for the first time. Answers are written
to be *spoken* in 60–90 seconds, not just read.

## The stack it covers

Python · FastAPI · TypeScript · React · Node · C#/.NET · Java Spring Boot · REST · OAuth2/JWT ·
microservices · Docker · Kubernetes · Azure · Azure DevOps · CI/CD · SQL · Cosmos DB · Spark ·
Databricks · MLOps · system design

## Read it by category

| # | Category | What's in it |
|---|----------|--------------|
| 01 | [Application development foundations](categories/01-foundations.html) | Client/server, the HTTP request lifecycle, runtimes, layering, environments, SOLID, coupling and cohesion, and what cloud-native actually means. |
| 02 | [Python for application development](categories/02-python.html) | From syntax to OOP, typing, decorators, asyncio, FastAPI, SQLAlchemy, pytest, packaging — and the traps that get asked. |
| 03 | [JavaScript, TypeScript, front-end & mobile](categories/03-javascript-typescript-frontend.html) | The event loop, ES6+, TypeScript depth, React, turning wireframes into responsive accessible UI, performance and mobile. |
| 04 | [C#/.NET and Java Spring Boot](categories/04-csharp-dotnet-java.html) | The two enterprise backend stacks mapped onto each other: DI, JPA and EF Core, LINQ and streams, async in both. |
| 05 | [API design and integration](categories/05-api-design.html) | Resource modelling, pagination, versioning, idempotency, error contracts, OAuth2 and JWT, rate limiting, webhooks, GraphQL and gRPC. |
| 06 | [Microservices & cloud-native](categories/06-microservices-cloud-native.html) | Service boundaries, sync vs event-driven, saga and outbox, Docker and Kubernetes, resilience patterns, and the anti-patterns. |
| 07 | [Azure for developers](categories/07-azure.html) | Compute options, storage, SQL and Cosmos, Service Bus and Event Hubs, Entra ID and managed identity, Key Vault, App Insights, Bicep and cost. |
| 08 | [Git, Azure DevOps, CI/CD & observability](categories/08-devops-cicd.html) | Branching, pull requests, pipeline YAML, quality gates, deployment strategies, zero-downtime migrations, SLOs and performance debugging. |
| 09 | [Databases & data engineering](categories/09-databases-data-engineering.html) | SQL depth, indexes, execution plans, transactions and concurrency, ORMs — then ETL vs ELT, Spark, medallion architecture and data quality. |
| 10 | [Integrating ML into applications](categories/10-ml-ai-integration.html) | Training vs inference, serving patterns, training-serving skew, model registry, MLOps, drift, Azure ML, evaluation metrics and RAG. |
| 11 | [System design & architecture](categories/11-system-design.html) | A framework you can run under pressure, back-of-envelope numbers, and five worked designs with their failure modes. |

## How to use it

- **Study mode** (default) — answers are open. Read a category end to end, out loud.
- **Quiz mode** — collapses every answer. Read the question, say your answer aloud in 60–90
  seconds, then reveal. Speaking is the skill being tested; reading is not.
- **Search** — press <kbd>/</kbd> and type a keyword (`idempotent`, `circuit breaker`, `drift`).
- **Print / PDF** — expands every answer and prints cleanly.

Tags mark each question: **core** (know it cold), **advanced** (senior differentiator),
**trap** (commonly answered wrong), **new** (new territory coming from a testing background),
**bridge** (already familiar under a different name).

## Generated

These pages are generated from a working set that also contains personal interview notes, which
are not published. Regenerate with:

```bash
node build-public.js <outputDir>
```
