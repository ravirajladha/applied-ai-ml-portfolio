# GraphQL, gRPC & API Versioning (S1): coverage spec

**Ladder:** API-driven Cloud Native Solutions (AIMLCZG549) › Session 1 API Basics (second half)   ·   **Prerequisites:** cnas-apis (HTTP, REST, status codes, OpenAPI); ops-serving for model-serving APIs in general
**Why it matters for AI/ML:** REST is not the only way to expose a model or a data service. GraphQL lets one screen fetch exactly the fields it needs in one call; gRPC with Protocol Buffers gives fast, typed calls between internal services (feature stores, model servers, the microservices of later sessions). Once clients depend on any of them, changes must be versioned so nobody breaks: semantic versioning and a versioning strategy are part of the API contract.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `graphql-basics` | GraphQL: query language, query and mutation, one endpoint | Facebook 2015, query vs mutation, /graphql, GraphiQL, JSON reply | reading a query and predicting the response shape | errors and status codes in GraphQL, subscriptions | operation design for a mobile screen |
| 2 | `graphql-schema` | Schema (SDL), resolvers, validation and execution | schema defines types and relationships | resolvers per field; validation against the schema | non-null and list types, arguments, introspection | resolver cost, depth limits |
| 3 | `graphql-fetching` | Over-fetching, under-fetching and the N+1 problem | REST's multiple calls vs one GraphQL call | over- vs under-fetching | counting resolver calls (N+1), batching with a DataLoader | caching difficulty, query cost limits |
| 4 | `rpc` | Remote Procedure Call: client and server stubs | RPC = calling a function on another machine | the four RPC parts: client node/stub, network, server stub/node | marshalling and why a remote call is not a local call | timeouts, retries and idempotency of RPCs |
| 5 | `grpc-protobuf` | gRPC and Protocol Buffers: the .proto file, protoc, HTTP/2 | Google 2015, protobuf instead of JSON, HTTP/2, protoc | reading a .proto: service, rpc, message, field numbers, repeated | default values, wire tags, field number rules, reserved | binary encoding by hand, evolution rules |
| 6 | `grpc-demos` | The learner's gRPC user and student demos | what server.py, client.py and the generated files do | channel, stub, servicer, add_..._to_server, the protoc command | status codes (NOT_FOUND, INVALID_ARGUMENT, ALREADY_EXISTS), deadlines, the lock | binding addresses, gRPC status vs HTTP status, insecure channels |
| 7 | `grpc-streaming` | The four gRPC call types, advantages and disadvantages | unary vs streaming | server, client and bidirectional streaming | repeated field vs server streaming; HTTP/2 multiplexing | browser limits, gRPC-Web, picking a mode |
| 8 | `api-comparison` | REST vs GraphQL vs gRPC | the three styles and their formats | the course comparison table | which style for a mobile app, a public API, internal services | mixed architectures (gateway, BFF) |
| 9 | `api-versioning` | API versioning: why, when, and strategies | what versioning is and why clients need it | the slides' breaking-change list | URI, query parameter, header and media-type versioning | deprecation, running versions side by side |
| 10 | `semver` | Semantic versioning MAJOR.MINOR.PATCH | the three numbers and what each means | the movies example; resetting lower numbers | the bump for a given change; comparing versions | pre-releases, 0.y.z, why only MAJOR goes in the URI |

## Must-know facts
- GraphQL (Facebook, 2015) is a query language for APIs: one endpoint (/graphql), the client names exactly the fields it wants, and the reply is JSON shaped like the query. `query` reads, `mutation` inserts, updates or deletes. GraphiQL is its in-browser IDE.
- GraphQL flow from the slides: schema in SDL -> client sends a query or mutation -> server resolvers (one function per field) -> validate against the schema, execute, reply in JSON.
- Over-fetching: getting fields you do not need; under-fetching: one call does not return enough, so you make more. REST suffers both; GraphQL addresses both. The N+1 problem: a naive resolver issues one query for the list and one per item; batching (DataLoader) fixes it.
- RPC: the client stub packs the call into a message (marshalling), the network carries it, the server stub unpacks it and calls the real procedure, and the result travels back the same way.
- gRPC (Google, 2015): an open-source RPC framework using Protocol Buffers as the IDL and serialization format and HTTP/2 as the transport; protoc compiles .proto files into message classes and client/server stubs for 10+ languages.
- A .proto has `syntax = "proto3"`, a `package`, a `service` with `rpc Name (Request) returns (Response)`, and `message` types whose fields have numbers (`string name = 2`). Field numbers identify fields on the wire: never change or reuse them; mark deleted ones `reserved`.
- In proto3 an unset scalar field reads as its default (0, "", false); the user demo's GetUser rejects id <= 0 with INVALID_ARGUMENT, so an empty request fails.
- The four call types: unary, server streaming, client streaming, bidirectional streaming (`stream` keyword on the request, response or both). A `repeated` field in one response (ListUsers) is still unary.
- gRPC advantages (slides): simple, well-defined interfaces, polyglot, lightweight and fast, best for inter-service communication. Disadvantages: less suited to external-facing services, limited browser support (gRPC-Web).
- Comparison: REST is the ubiquitous web standard, JSON/XML, easy HTTP caching; GraphQL fetches exactly what the client needs, JSON, harder caching; gRPC has native code generation and binary Protocol Buffers, weak browser support.
- API versioning manages changes without disrupting clients. Version on breaking changes: changing the data format (JSON -> XML), a field's type, a resource's name, removing resources/fields/methods, or adding a new required request field. Strategies: URI path (/v1/), query parameter (?version=1), custom header, media type (Accept: application/vnd.x.v2+json).
- Semantic versioning X.Y.Z: MAJOR for incompatible changes, MINOR for backward-compatible features, PATCH for backward-compatible bug fixes; no leading zeros; bumping one resets the ones to its right (1.9.3 -> 2.0.0). Google Maps JavaScript API 3.54.4 is the slides' example.

## Common traps (each one must have at least one question)
- GraphQL needing one endpoint per resource -> one endpoint, the query selects.
- GraphQL errors always arriving as 4xx/5xx -> many servers return 200 with an `errors` array; check the body.
- Thinking GraphQL removes the N+1 problem -> it can make it worse unless resolvers batch.
- Field numbers read as default values -> `string name = 2` means "field number 2".
- Renumbering or reusing a field number -> old clients decode data into the wrong field.
- ListUsers with a repeated field called "server streaming" -> it is one unary response.
- A gRPC NOT_FOUND treated as an HTTP 404 -> it is a gRPC status, sent in trailers on an HTTP/2 response.
- Calling a stub as if it were a local function -> it can fail with UNAVAILABLE or DEADLINE_EXCEEDED; set deadlines.
- Using gRPC directly from a browser front end -> needs gRPC-Web and a proxy.
- Comparing versions as strings ("1.10.0" < "1.9.0") -> compare numerically.
- Forgetting to reset MINOR and PATCH on a MAJOR bump.
- Bumping PATCH for a new feature -> MINOR.
- Putting minor and patch numbers in the URI (/api/v1.1.0/) -> only breaking changes need a new URI; the slides' example does this, standard practice does not.

## Interview angle
1. **"REST, GraphQL or gRPC?"** Public web/partner API: REST. A mobile or web front end that composes many entities on one screen: GraphQL. Internal, high-volume, typed service-to-service calls or streaming: gRPC.
2. **"What is the N+1 problem in GraphQL and how do you fix it?"** One query for the list plus one per item from naive resolvers; batch per request with a DataLoader (one IN query), and limit query depth and cost.
3. **"How do you evolve a protobuf message safely?"** Add new fields with new numbers; never change a field's number or type; reserve the numbers and names of deleted fields; treat a missing field as its default.
4. **"Explain semantic versioning and when you bump MAJOR."** MAJOR.MINOR.PATCH; MAJOR when a change breaks existing clients (removing or renaming a field, changing a type, adding a required input), and you run the old major side by side until clients move.
5. **"Where do you put the version?"** URI path is the most visible and cache-friendly; headers and media types keep URIs clean but are harder to test in a browser. Pick one and apply it consistently.

## Source material
- Old-batch slides p26-47 (`cloud-src/cnas-api-styles.txt`): the REST multi-resource drawback (profile, posts, comments) as the motivation for GraphQL.
- GraphQL: Facebook 2015, GraphiQL, one request with an all-inclusive reply, query vs mutation; the five-step flow (SDL schema, query/mutation, resolvers, validation and execution on /graphql, fetch only the fields needed); the books query with its JSON reply; the REST vs GraphQL social-media example.
- RPC: client node and stub, network, server stub and node.
- gRPC: Google 2015, Protocol Buffers as IDL, HTTP/2, protoc, 10+ languages; the proto file explanation (generated classes and stubs); the Calculator proto (Add, Subtract, Multiply, Divide with a float DivideResponse); the ecommerce ProductInfo proto (addProduct, getProduct); advantages and disadvantages.
- The REST/GraphQL/gRPC comparison table (ubiquity, data fetch, browser support, caching, code generation, payload format).
- API versioning (definition, why, when: the breaking-change list) and semantic versioning (X.Y.Z rules, Google Maps JavaScript API 3.54.4, the movies API example 1.0.0 -> 2.1.1 and its /api/vX.Y.Z/movies endpoints).
- The learner's practice demos in `api-driven-cloud-native-solutions/practice/grpc/`: `grpc-user-demo` (user.proto with GetUser, CreateUser, ListUsers; server with validation, a lock and NOT_FOUND / INVALID_ARGUMENT / ALREADY_EXISTS; client with channel_ready_future and five-second deadlines; README notes on field numbers and ListUsers not being streaming) and `grpc_student_demo` (student.proto with GetStudent, server on [::]:50051, client with timeout=5, the protoc command with --pyi_out). Snippets imitate them with plain Python; none imports grpc.
- No past papers; scenario style modelled on BITS WILP papers.
- **Standard practice (slides thin):** GraphQL SDL types, non-null/list modifiers, arguments, subscriptions, introspection, error handling, the N+1 problem and DataLoader, query cost limits; the four gRPC streaming modes, deadlines, gRPC status codes and trailers, gRPC-Web; protobuf defaults, wire tags and varints, field-number ranges and `reserved`; the versioning strategies (URI, query, header, media type), deprecation and the semver rules on pre-releases and 0.y.z (R2 Mastering API Architecture, graphql.org, grpc.io, protobuf.dev, semver.org).
- **Slide content corrected or flagged:** the slides say a patch release "introduces non-breaking functionality"; by semver a PATCH carries only backward-compatible bug fixes, new functionality is MINOR. The movies example puts full versions in URIs (/api/v1.1.0/movies); common practice puts only the MAJOR version in the URI, because MINOR and PATCH releases are backward compatible by definition. The comparison table on the slide is garbled in the extract; the questions use the standard comparison. "Uses HTTP/2 as the protocol [instead of HTTP]" should read "instead of HTTP/1.1": HTTP/2 is still HTTP.
