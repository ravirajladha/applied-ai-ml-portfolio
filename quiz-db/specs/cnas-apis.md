# API Basics: HTTP, REST & OpenAPI (S1): coverage spec

**Ladder:** API-driven Cloud Native Solutions (AIMLCZG549) › Session 1 API Basics   ·   **Prerequisites:** none (basic web development helps); cnas-api-styles follows on with GraphQL, gRPC and versioning
**Why it matters for AI/ML:** Every cloud AI service the course uses (Amazon Bedrock, Hugging Face, LangChain servers, Prefect, MLflow) is reached through an HTTP API, and every model you deploy is exposed as one. Session 1 sets the vocabulary: an API as a contract, sync vs async calls, the parts of an HTTP request and response, REST and its trade-offs, OpenAPI, and the seven-step bookstore lifecycle that the labs follow with FastAPI.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `api-basics` | What an API is: a contract between a service and its clients | the three slide definitions; Google Maps API, RapidAPI, Bedrock as examples | contract = what you may rely on, not how it is built | what changes break the contract | API as product: consumers you do not control |
| 2 | `sync-async` | Synchronous vs asynchronous APIs | REST/gRPC/GraphQL sync; RabbitMQ/Kafka async | blocking caller vs broker; webhooks as server-to-client callbacks | latency of chains vs fan-out; choosing async for slow work | availability coupling, 202 + polling vs webhook vs queue |
| 3 | `http-components` | Components of an HTTP API: endpoint, request, response | endpoint = URL of a resource; JSON/XML bodies | method, URI, headers, body; path vs query params | Content-Type vs Accept, Authorization header | parsing and routing a request by hand |
| 4 | `http-methods` | HTTP methods, safe and idempotent methods | GET/POST/PUT/DELETE and CRUD | safe vs idempotent; PATCH | retries and duplicate POSTs | Idempotency-Key design for payments |
| 5 | `status-codes` | Status codes and families | 200, 201, 204, 400, 401, 403, 404, 500 | 1xx-5xx families; 401 vs 403 | 409, 422, 304, 502/503/504 picks | who must act on each family; client retry policy by family |
| 6 | `rest-architecture` | REST architecture and constraints | Fielding 2000; resources and URIs; representations | stateless, cacheable, uniform interface | layered system, HATEOAS, ETags | Richardson maturity, statelessness vs sessions at scale |
| 7 | `rest-design` | REST resource design, benefits and drawbacks | nouns in URIs (students example) | nested resources, collections vs items, filtering | multiple round trips (profile, posts, comments); reduced availability | design review of a bad API (verbs in URIs, 200 for errors) |
| 8 | `openapi` | OpenAPI (formerly Swagger) | a standard description of an HTTP API | what a spec holds: paths, operations, parameters, schemas, responses | mocking, code generation, contract tests; design-first vs code-first | spec drift, breaking-change detection from the spec |
| 9 | `api-lifecycle` | The bookstore API lifecycle with FastAPI | the seven stages in order | the stage outputs: CRUD list, endpoints, data model, /docs | FastAPI + Uvicorn, pytest, 422 on bad input | where design-first fits, test pyramid, deploy concerns |

## Must-know facts
- The course defines an API three ways: a contract between a service and its clients; a set of rules and protocols for interacting with an application; a way for systems to exchange data and functions without knowing each other's code.
- Synchronous APIs (REST, gRPC, GraphQL): the caller waits for the reply. Asynchronous APIs (message brokers such as RabbitMQ and Apache Kafka, webhooks): the caller hands off the work and continues.
- Components of an HTTP API: endpoints (URLs for a collection or a single object), the request (method, URI with path and query parameters, headers, optional body) and the response (status code, headers, body in JSON or XML).
- GET retrieves, POST creates/submits, PUT replaces/updates, DELETE removes. Safe methods (GET, HEAD, OPTIONS) do not change server state; idempotent methods (the safe ones plus PUT and DELETE) leave the same state however often they are repeated. POST and PATCH are not guaranteed idempotent.
- Status families: 1xx informational, 2xx success, 3xx redirection, 4xx client error, 5xx server error. Slide codes: 200 OK, 201 Created, 204 No Content, 400 Bad Request, 401 Unauthorized (not authenticated), 403 Forbidden (authenticated but not allowed), 404 Not Found, 500 Internal Server Error.
- REST (Roy Fielding, 2000) is an architectural style, the architecture of the web: every piece of content is a resource with a URI, exchanged as a representation (JSON/XML) using the HTTP methods.
- REST constraints: client-server, stateless, cacheable, uniform interface, layered system, optional code on demand.
- REST benefits (slides): mature and ubiquitous, simple to test, synchronous request-response, no intermediate broker, supported everywhere. Drawbacks: reduced availability (client and service must both be up) and several round trips to fetch related resources.
- Most cloud AI services (Amazon Bedrock, Hugging Face, LangChain, Prefect) expose RESTful APIs: e.g. Bedrock's invoke and list-models endpoints with an access token and a JSON response.
- The OpenAPI Specification (formerly the Swagger specification) is a formal, language-neutral description of an HTTP API in YAML or JSON: paths, operations, parameters, request bodies, responses and component schemas. From it you get docs, mock servers, client/server code and tests.
- Bookstore lifecycle: requirements -> design -> configure -> publish -> develop -> test -> deploy. FastAPI + Uvicorn; FastAPI generates the OpenAPI document and serves Swagger UI at /docs; pytest/unittest for tests; Heroku/AWS/Google Cloud for deployment.

## Common traps (each one must have at least one question)
- "Synchronous means one request at a time on the server" -> it means the caller waits for this call's reply; servers still serve many callers concurrently.
- Webhooks thought to be polling -> the provider calls your URL when the event happens.
- PUT treated as non-idempotent or POST as idempotent -> the reverse.
- DELETE called twice returns 404 the second time, so "DELETE is not idempotent" -> idempotency is about server state, not the response code.
- 401 vs 403 swapped -> 401 means "who are you?", 403 means "I know you, and no".
- Returning 200 with {"error": ...} in the body -> clients, caches and monitors read the status code.
- 500 for bad client input -> 4xx; 5xx tells the client to retry later, which is wrong for a malformed request.
- Verbs in URIs (/getBooks, /deleteBook?id=3) -> nouns for resources, the method carries the verb.
- Server-side session state assumed to be RESTful -> REST is stateless; each request carries what it needs (e.g. a token).
- "OpenAPI is a tool" -> it is a specification; Swagger UI, Swagger Editor and generators are tools that use it.
- Path vs query parameters mixed up -> path identifies the resource, query filters, sorts or pages it.
- Content-Type vs Accept confused -> Content-Type describes the body sent; Accept asks for the reply format.

## Interview angle
1. **"What makes an API RESTful?"** Resources named by URIs, a uniform interface of HTTP methods and status codes, stateless requests, cacheable responses, and a layered client-server design.
2. **"PUT vs POST vs PATCH?"** POST creates under a collection (server picks the ID, not idempotent); PUT replaces the resource at a known URI (idempotent); PATCH applies a partial change (not guaranteed idempotent).
3. **"How do you make a payment POST safe to retry?"** The client sends an Idempotency-Key; the server stores the first result for that key and replays it for repeats.
4. **"Sync or async for a slow job?"** Accept with 202 and process through a queue, then notify by webhook or let the client poll a status URL; do not hold an HTTP connection open for minutes.
5. **"Why write the OpenAPI spec first?"** Frontend, backend and test teams work in parallel against a mock, reviews happen on the contract, and clients and server stubs are generated from one source.

## Source material
- Old-batch slides p1-26 (`cloud-src/cnas-apis.txt`), session 1 "API Basics": agenda (introduction to APIs, HTTP APIs, OpenAPI, REST/GraphQL/gRPC, versioning, examples: Google Maps API, RapidAPI, Conference API).
- The three API definitions (contract; rules and protocols; communication without knowing the code).
- Synchronous vs asynchronous execution and APIs: an order service calling other services over REST; the async variant through message brokers (RabbitMQ, Apache Kafka).
- HTTP API components: endpoints as the "doors" to resources, requests with methods (GET/POST/PUT/DELETE), responses in JSON/XML with the eight status codes listed above.
- REST: Fielding 2000, resources and URIs, XML and JSON representations of a user, CRUD mapping, the BITS students URI table with curl commands, the RESTful food-delivery app, benefits and drawbacks (reduced availability; three calls for profile, posts and comments).
- Why REST matters for the course: Amazon Bedrock model-inference and list-models endpoints; Hugging Face, LangChain and Prefect also expose REST.
- OpenAPI (previously Swagger): formal standard for describing HTTP APIs, used for docs, client code generation and tests.
- The bookstore scenario with Python and FastAPI: requirements (CRUD), design (five endpoints, the book data model), configure (FastAPI, Uvicorn, JSON), publish (/docs at localhost:8000), develop, test (pytest/unittest), deploy (Heroku, AWS, Google Cloud).
- No past papers; scenario style modelled on BITS WILP papers (Indian startups, ₹ amounts, "which method/status code and why", "spot the flaw").
- **Standard practice (slides thin):** the full REST constraint list, HATEOAS, the Richardson maturity model, safe vs idempotent methods, PATCH, the status families and the codes 202/304/409/422/502/503/504, headers (Content-Type, Accept, Authorization, ETag/If-None-Match, Location), path vs query parameters, webhooks, Idempotency-Key, OpenAPI document structure, mocking, generators, design-first vs code-first and contract tests (R2 Mastering API Architecture, RFC 9110, the OpenAPI 3 specification).
- **Slide wording corrected:** the slide defines a synchronous API as one where "each request must wait for the previous one to complete"; the standard meaning is that the caller blocks until it gets the reply to its own call. The slides map PUT only to "update existing data"; by the HTTP standard PUT replaces the resource at the given URI (and may create it). In the bookstore lifecycle "publish" (FastAPI /docs) comes before "develop", but FastAPI generates /docs from the code, so the docs only exist once endpoints are written; the questions treat publish as publishing the designed contract.
