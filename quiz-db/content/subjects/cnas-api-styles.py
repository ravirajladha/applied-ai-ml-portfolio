from helpers import mcq, tf, out, fill

SUBJECT = "cnas-api-styles"

TOPICS = [
    ("graphql-basics", "GraphQL: query language, query and mutation, one endpoint"),
    ("graphql-schema", "Schema (SDL), resolvers, validation and execution"),
    ("graphql-fetching", "Over-fetching, under-fetching and the N+1 problem"),
    ("rpc", "Remote Procedure Call: client and server stubs"),
    ("grpc-protobuf", "gRPC and Protocol Buffers: the .proto file, protoc, HTTP/2"),
    ("grpc-demos", "The learner's gRPC user and student demos"),
    ("grpc-streaming", "The four gRPC call types, advantages and disadvantages"),
    ("api-comparison", "REST vs GraphQL vs gRPC"),
    ("api-versioning", "API versioning: why, when, and strategies"),
    ("semver", "Semantic versioning MAJOR.MINOR.PATCH"),
]

QUESTIONS = [
    # ------------------------------------------------------------------ L1
    mcq("Which company created GraphQL, and why, according to the slides?",
        ["Facebook, in 2015, to overcome REST's drawback of needing several calls to fetch related data",
         "Google, in 2015, to replace JSON with Protocol Buffers",
         "Roy Fielding, in 2000, to describe the web",
         "Amazon, to call Bedrock models"], 0,
        "Same year as gRPC, different company.",
        "Facebook released GraphQL in 2015: a query language that pulls data from several sources in a single API call with an all-inclusive reply. Google released gRPC the same year; Fielding defined REST in 2000.",
        topic="graphql-basics", level=1),
    mcq("In GraphQL, which operation type reads data and which changes it?",
        ["query reads; mutation inserts, updates or deletes",
         "mutation reads; query changes",
         "GET reads; POST changes",
         "select reads; update changes"], 0,
        "One of the words means 'change'.",
        "The slides: GraphQL 'uses query operation to fetch data' and 'mutation operations to insert, update, or delete data'. HTTP verbs do not carry the meaning in GraphQL; the operation type does.",
        topic="graphql-basics", level=1),
    tf("A GraphQL API usually exposes a single endpoint, such as /graphql, instead of one URL per resource.", True,
       "The slides name the endpoint.",
       "The server validates and executes every query 'on the endpoint /graphql'. Which data comes back is decided by the query text, not by the URL. REST, by contrast, has /users, /users/{id}/posts and so on.",
       topic="graphql-basics", level=1,
       diagram="""
REST:     /users/5   /users/5/posts   /posts/9/comments
GraphQL:  /graphql  <- every query and mutation
"""),
    fill("The in-browser IDE for writing and testing GraphQL queries, mentioned in the slides, is called ____.", "GraphiQL",
         "GraphQL with an extra 'i' (for interactive).",
         "GraphiQL lets you type a query with autocomplete from the schema, run it and see the JSON reply, much like Swagger UI at /docs does for a REST API.",
         topic="graphql-basics", level=1),
    mcq("In GraphQL, what is the schema?",
        ["A definition, written in the Schema Definition Language (SDL), of the types of data that can be queried and how they relate",
         "The database table layout",
         "The list of URLs the API exposes",
         "The JSON reply the server sends"], 0,
        "Step 1 on the slides.",
        "The schema is the contract: e.g. type Book { title: String, author: String }. The server validates every query against it, and tools like GraphiQL read it to offer autocomplete.",
        topic="graphql-schema", level=1,
        analogy="Like a TypeScript type file shared by the front end and the back end: both sides compile against the same shapes."),
    fill("In GraphQL, the server-side functions that produce the value for each field of a query or mutation are called ____.", "resolvers",
         "They resolve a field to data.",
         "Each field (Query.books, Book.author) has a resolver that fetches its data from a database, another API or a cache. The engine walks the query and calls the resolvers it needs.",
         topic="graphql-schema", level=1,
         analogy="Like route handlers in Express or FastAPI, but one per field instead of one per URL."),
    mcq("What does RPC stand for?",
        ["Remote Procedure Call", "REST Protocol Converter", "Request Processing Cluster", "Remote Packet Channel"], 0,
        "You call a procedure that lives somewhere else.",
        "RPC lets a program call a function on another machine as if it were local. The slides describe it as communication between a client and a remote server, used for distributed client-server applications.",
        topic="rpc", level=1,
        analogy="Like phoning a colleague's extension: you ask, they do the work in their office and tell you the result."),
    mcq("In RPC, what does the client stub do?",
        ["It packs the procedure call and its arguments into a message and sends it over the network, then unpacks the reply",
         "It runs the business logic on the server",
         "It stores the database",
         "It renders the web page"], 0,
        "It stands in for the remote function on the client side.",
        "The client calls the stub like a normal function; the stub marshals the arguments into a message. The server stub unpacks it, calls the real procedure and sends the result back the same way.",
        topic="rpc", level=1,
        diagram="""
client --> client stub ==network==> server stub --> server
client <-- client stub <==network== server stub <-- server
         (marshal)                  (unmarshal, call)
"""),
    mcq("Which pair does gRPC use instead of REST's usual JSON over HTTP/1.1?",
        ["Protocol Buffers for messages and HTTP/2 for transport",
         "XML for messages and FTP for transport",
         "GraphQL for messages and WebSockets for transport",
         "CSV for messages and SMTP for transport"], 0,
        "A binary format and a newer HTTP.",
        "gRPC (Google, 2015) defines services and messages in Protocol Buffers, a compact binary format, and carries them over HTTP/2. The slides' 'instead of HTTP' means instead of HTTP/1.1: HTTP/2 is still HTTP.",
        topic="grpc-protobuf", level=1),
    fill("The compiler that turns a .proto file into message classes and client/server stubs is called ____.", "protoc",
         "Proto + c.",
         "protoc generates code for many languages. In the learner's demos it runs as `python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. user.proto`.",
         topic="grpc-protobuf", level=1),
    tf("In the learner's user.proto, `string name = 2;` sets the default value of name to 2.", False,
       "The README explains these numbers.",
       "The 2 is the field number: the identifier used for this field in the binary message. Values come from your code at runtime. Keep field numbers stable and never reuse an old one.",
       topic="grpc-protobuf", level=1,
        analogy="Like a roll number in class: it identifies the student on every register; it is not the student's marks."),
    mcq("In the learner's grpc-user-demo, which file contains the server logic that answers GetUser, CreateUser and ListUsers?",
        ["server.py", "user.proto", "user_pb2.py", "client.py"], 0,
        "The .proto is only the contract; the _pb2 files are generated.",
        "user.proto defines the contract, protoc generates user_pb2.py (messages) and user_pb2_grpc.py (stub, servicer base, registration), server.py implements the servicer, and client.py calls the stub.",
        topic="grpc-demos", level=1),
    mcq("In grpc_student_demo, running `python client.py 999` prints an RPC failure. Which gRPC status does the server send?",
        ["NOT_FOUND", "OK", "INVALID_ARGUMENT", "ALREADY_EXISTS"], 0,
        "Only students 101, 102 and 103 exist.",
        "The server looks up STUDENTS.get(999), gets None and calls context.abort(grpc.StatusCode.NOT_FOUND, ...). The client catches grpc.RpcError and prints the code name and details.",
        topic="grpc-demos", level=1),
    tf("Both learner demos (user and student) must have the server running in one terminal before the client is started in another.", True,
       "Who listens on port 50051?",
       "The server binds port 50051 and waits; the client opens a channel to it. Without a server, the user client's channel_ready_future times out after 5 s and prints 'Cannot connect'.",
       topic="grpc-demos", level=1),
    mcq("What is a unary gRPC call?",
        ["The client sends one request and gets one response, like a normal function call",
         "The server sends a stream of responses",
         "Both sides stream messages at the same time",
         "A call with no request message"], 0,
        "Unary = one.",
        "Unary is the simplest of the four call types; every RPC in the learner's demos (GetUser, CreateUser, ListUsers, GetStudent) is unary. The others are server streaming, client streaming and bidirectional streaming.",
        topic="grpc-streaming", level=1),
    mcq("According to the slides, where is gRPC the best fit?",
        ["Communication between internal services (inter-service calls)",
         "Public APIs called directly from any web browser",
         "Static web pages",
         "Sending email"], 0,
        "Look at its listed disadvantages.",
        "Advantages: well-defined interfaces, many languages, lightweight and fast, 'best for inter-service communication'. Disadvantages: less suited to external-facing services and limited browser support.",
        topic="grpc-streaming", level=1),
    mcq("Which payload format does each style use, per the course comparison?",
        ["REST: JSON or XML; GraphQL: JSON; gRPC: Protocol Buffers",
         "REST: Protocol Buffers; GraphQL: XML; gRPC: JSON",
         "All three use only XML",
         "REST: CSV; GraphQL: YAML; gRPC: HTML"], 0,
        "Only one of them is binary.",
        "REST representations are JSON or XML; GraphQL replies are JSON shaped like the query; gRPC sends binary Protocol Buffers, which is part of why it is fast.",
        topic="api-comparison", level=1,
        diagram="""
         REST        GraphQL      gRPC
format   JSON/XML    JSON         Protobuf
browser  yes         yes          via gRPC-Web
caching  HTTP, easy  harder       in the app
codegen  OpenAPI     GQL codegen  protoc
"""),
    mcq("What is API versioning?",
        ["Managing changes to an API so they can be made without disrupting existing clients, who can upgrade at their own pace",
         "Counting how many requests an API receives",
         "Renaming the API every month",
         "Encrypting API traffic"], 0,
        "The slides' definition mentions clients' pace.",
        "Versioning communicates changes clearly and keeps old behaviour available, so a third-party app built on your API does not break the day you ship.",
        topic="api-versioning", level=1,
        analogy="Like a railway timetable change: announced in advance, with the old timings honoured until a stated date."),
    mcq("In the semantic version 3.54.4 (the slides' Google Maps JavaScript API example), what is 54?",
        ["The minor version", "The major version", "The patch version", "The build date"], 0,
        "MAJOR.MINOR.PATCH.",
        "X.Y.Z = MAJOR.MINOR.PATCH: major 3, minor 54, patch 4. Minor 54 means many backward-compatible feature releases since 3.0.0.",
        topic="semver", level=1,
        diagram="""
  3 . 54 . 4
  |    |   +-- PATCH: compatible bug fixes
  |    +------ MINOR: compatible new features
  +----------- MAJOR: breaking changes
"""),
    tf("By semantic versioning, a MAJOR version bump signals changes that are incompatible with the previous version.", True,
       "Which number warns clients to check their code?",
       "MAJOR = incompatible API change; MINOR = backward-compatible new functionality; PATCH = backward-compatible bug fixes. A client on 2.x knows it can take 2.7.1 safely but must test before 3.0.0.",
       topic="semver", level=1,
        analogy="Like a power socket: a new plug shape (MAJOR) needs new adapters; a brighter bulb (MINOR) or a fixed loose wire (PATCH) fits the same socket."),
    mcq("In the slides' social-media scenario (user profile, the user's posts, comments on the posts), how many requests does the GraphQL version need?",
        ["1: one query that nests posts and comments under the user",
         "3: one per resource, as with REST",
         "2: one for users and one for comments",
         "It depends on the number of HTTP verbs"], 0,
        "'Single request and all-inclusive reply.'",
        "The GraphQL query asks for user(id: \"123\") { name posts { title comments { content } } } in one round trip. REST needs GET /users/{id}, GET /users/{id}/posts and GET /posts/{id}/comments.",
        topic="graphql-fetching", level=1),
    fill("In semantic versioning, a release that only fixes bugs in a backward-compatible way bumps the ____ number.", "PATCH",
         "The third number.",
         "1.1.0 -> 1.1.1 in the slides' movies example 'fixes some bugs ... doesn't introduce any new features'. New backward-compatible features bump MINOR instead.",
         topic="semver", level=1),
    # ------------------------------------------------------------------ L2
    out("""book = {"id": 1, "title": "1984", "author": "George Orwell",
        "isbn": "978-0451524935", "publishedDate": "June 8, 1949", "price": 299}

def resolve(obj, fields):          # a tiny GraphQL-style field selector
    return {f: obj[f] for f in fields}

print(resolve(book, ["title", "author"]))""",
        ["{'title': '1984', 'author': 'George Orwell'}",
         "{'id': 1, 'title': '1984', 'author': 'George Orwell'}",
         "['1984', 'George Orwell']",
         "{'id': 1, 'title': '1984', 'author': 'George Orwell', 'isbn': '978-0451524935', 'publishedDate': 'June 8, 1949', 'price': 299}"], 0,
        "Only the requested fields come back.",
        "This is the core GraphQL idea: the reply has exactly the fields the client asked for, in a JSON object shaped like the query. A REST GET /books/1 would usually return all six fields (over-fetching).",
        topic="graphql-basics", level=2),
    mcq("The slides' query is `query { books { title author publishedDate } }`. What is the shape of the reply?",
        ["{\"data\": {\"books\": [ {\"title\": ..., \"author\": ..., \"publishedDate\": ...}, ... ]}}",
         "A list of complete book objects including id, isbn and price",
         "An XML document",
         "{\"books\": \"title,author,publishedDate\"}"], 0,
        "The reply mirrors the query and sits under one top-level key.",
        "GraphQL wraps results in a top-level \"data\" object whose keys follow the query: books is a list, and each item has just the three requested fields, as on the slide with 'To Kill a Mockingbird', '1984' and 'The Great Gatsby'.",
        topic="graphql-basics", level=2),
    mcq("What is the difference between over-fetching and under-fetching?",
        ["Over-fetching: a response carries fields you do not need; under-fetching: one response lacks data you need, so you make more calls",
         "Over-fetching: too many servers; under-fetching: too few",
         "They are two names for the N+1 problem",
         "Over-fetching only happens in GraphQL"], 0,
        "Too much in one call vs too little in one call.",
        "A mobile list screen that needs only book titles but gets full book objects over-fetches (wasted bandwidth). A screen that needs a user plus their posts and has to call twice under-fetches (extra round trips). GraphQL addresses both by letting the client choose fields and nest related data.",
        topic="graphql-fetching", level=2,
        analogy="Over-fetching is getting the whole newspaper for the cricket score; under-fetching is having to buy a second paper for the weather."),
    mcq("A client sends `query { books { title rating } }`, but the Book type in the schema has no `rating` field. What happens?",
        ["The server rejects the query in validation, before running any resolver, and returns an error naming the unknown field",
         "The server returns rating: null for every book",
         "The server runs the query and ignores rating silently",
         "The server crashes with a 500"], 0,
        "Step 4 on the slides: validation comes before execution.",
        "Every query is checked against the schema first. Unknown fields, wrong argument types and missing required arguments are caught there, so resolvers never run on an invalid query. This is one benefit of a typed schema.",
        topic="graphql-schema", level=2,
        diagram="""
client --query--> /graphql
                  | 1 parse
                  | 2 validate vs schema --x error
                  | 3 run resolvers
client <--JSON {data, errors}--+
"""),
    tf("In a GraphQL schema, `title: String!` means the title field can never be null.", True,
       "The exclamation mark.",
       "! marks a non-null type; [Book!]! is a non-null list of non-null books. Clients and code generators rely on these markers, so a resolver that returns null for a String! field produces an error.",
       topic="graphql-schema", level=2),
    out("""class Calculator:                    # plays the server side
    def Add(self, a, b): return a + b
    def Divide(self, a, b): return a / b

def call(server, method, **args):      # plays the stub + network
    message = {"method": method, "args": args}       # marshal
    handler = getattr(server, message["method"])     # dispatch
    return handler(**message["args"])

srv = Calculator()
print(call(srv, "Add", a=7, b=5), call(srv, "Divide", a=7, b=2))""",
        ["12 3.5", "12 3", "75 3.5", "12 3.0"], 0,
        "True division in Python.",
        "The stub packs the method name and arguments into a message, the server side looks up the procedure and calls it. 7/2 is 3.5, which is why the slides' Calculator proto declares DivideResponse.result as float while the others use int32.",
        topic="rpc", level=2),
    fill("Packing a procedure call's arguments into a message that can travel over the network (done by the client stub) is called ____.", "marshalling",
         "Also called serialization.",
         "Marshalling (serializing) turns in-memory arguments into bytes; the server stub unmarshals them. In gRPC, Protocol Buffers do this, which is why the .proto must describe every message.",
         topic="rpc", level=2),
    mcq("In the learner's user.proto, what does `message ListUsersResponse { repeated User users = 1; }` declare?",
        ["A response holding a list of zero or more User messages in field number 1",
         "A response that streams users one at a time",
         "A request that repeats until it succeeds",
         "A User whose id is always 1"], 0,
        "repeated = list.",
        "repeated makes a field a list (a Python repeated container, a Java List). ListUsers still returns one response message containing the whole list; the README stresses that it is not server streaming.",
        topic="grpc-protobuf", level=2,
        diagram="""
service UserService {
  rpc ListUsers (ListUsersRequest)
      returns (ListUsersResponse);
}
message ListUsersResponse {
  repeated User users = 1;   <- a list, field #1
}
"""),
    mcq("Match the `stream` keyword placement to the gRPC call type: `rpc Track (OrderId) returns (stream Location);`",
        ["Server streaming: one request, a stream of responses",
         "Client streaming: a stream of requests, one response",
         "Bidirectional streaming",
         "Unary"], 0,
        "Which side has the word stream?",
        "stream on the response = server streaming (e.g. a delivery rider's live location for one order). stream on the request = client streaming (upload many sensor readings, get one summary). On both = bidirectional (chat). On neither = unary.",
        topic="grpc-streaming", level=2,
        diagram="""
unary        rpc A (Req)        returns (Res)
server-strm  rpc B (Req)        returns (stream Res)
client-strm  rpc C (stream Req) returns (Res)
bidi         rpc D (stream Req) returns (stream Res)
"""),
    tf("The learner's ListUsers RPC is an example of server streaming, because it returns many users.", False,
       "Check the proto: is there a stream keyword?",
       "ListUsers returns one ListUsersResponse with a repeated field, so it is unary: the whole list arrives at once. Server streaming would be `returns (stream User)`, sending users one message at a time, which helps when the list is huge or produced gradually.",
       topic="grpc-streaming", level=2),
    mcq("After running protoc on user.proto, what does user_pb2_grpc.py contain?",
        ["The client stub (UserServiceStub), the server base class (UserServiceServicer) and the registration function add_UserServiceServicer_to_server",
         "The message classes User and GetUserRequest only",
         "The business logic for GetUser",
         "The list of users"], 0,
        "_pb2 = messages, _pb2_grpc = service plumbing.",
        "user_pb2.py holds the Protocol Buffer message classes; user_pb2_grpc.py holds the communication glue. The README warns not to edit either by hand: change user.proto and regenerate.",
        topic="grpc-demos", level=2,
        diagram="""
user.proto --protoc--> user_pb2.py      (messages)
                   +--> user_pb2_grpc.py (stub, servicer,
                                         add_..._to_server)
server.py subclasses the servicer; client.py uses the stub
"""),
    mcq("In the learner's client.py, what is the difference between the channel and the stub?",
        ["The channel is the connection to host:port; the stub is the generated object whose methods (GetUser, CreateUser) send RPCs over that channel",
         "They are the same object",
         "The stub opens the TCP connection and the channel holds the business logic",
         "The channel is only used by the server"], 0,
        "One is plumbing, the other is the API you call.",
        "`with grpc.insecure_channel(target) as channel:` opens the connection; `rpc.UserServiceStub(channel)` wraps it in typed methods. Many stubs can share one channel, and HTTP/2 multiplexes their calls over it.",
        topic="grpc-demos", level=2,
        analogy="The channel is the phone line; the stub is the speed-dial pad with one named button per RPC."),
    tf("gRPC uses HTTP/2, which can carry many concurrent calls over one TCP connection (multiplexing) with binary framing and compressed headers.", True,
       "A key reason gRPC is 'lightweight and fast'.",
       "HTTP/1.1 handles one request at a time per connection, so clients open several connections. HTTP/2 interleaves streams on one connection, and gRPC maps each RPC to a stream, which also makes streaming RPCs possible.",
       topic="grpc-protobuf", level=2),
    out("""def bump(version, change):
    major, minor, patch = map(int, version.split("."))
    if change == "breaking":
        return f"{major + 1}.0.0"
    if change == "feature":
        return f"{major}.{minor + 1}.0"
    return f"{major}.{minor}.{patch + 1}"

v = "1.9.3"
print(bump(v, "fix"), bump(v, "feature"), bump(v, "breaking"))""",
        ["1.9.4 1.10.0 2.0.0", "1.9.4 2.0.0 2.0.0", "1.9.4 1.10.3 2.9.3", "1.10.0 1.10.0 2.0.0"], 0,
        "Bumping a number resets the ones to its right.",
        "A fix bumps PATCH (1.9.4). A feature bumps MINOR and resets PATCH (1.10.0, not 2.0.0: minor numbers can go past 9). A breaking change bumps MAJOR and resets both (2.0.0).",
        topic="semver", level=2),
    mcq("In the slides' movies API, version 1.1.0 'allows users to search for movies by genre or actor' without changing existing calls. Why is it 1.1.0 and not 2.0.0?",
        ["It adds backward-compatible functionality, which is a MINOR bump; existing clients keep working",
         "Search features always bump PATCH",
         "Any new endpoint is a breaking change",
         "Version numbers are chosen at random"], 0,
        "Did any existing client break?",
        "Adding a new endpoint or optional parameter is additive. 2.0.0 comes later when the API 'may switch to a new data format', which breaks old clients.",
        topic="semver", level=2,
        diagram="""
1.0.0 -> 1.1.0 -> 1.1.1 -> 2.0.0 -> 2.1.0 -> 2.1.1
 base   +search    fix   new format +feature  fix
"""),
    mcq("Which change from the slides' list is NOT a breaking change?",
        ["Adding a new optional field to a response",
         "Switching the response format from JSON to XML",
         "Changing a field's type from string to integer",
         "Adding a new required field to client requests"], 0,
        "Would an existing client still work unchanged?",
        "The slides' breaking changes: changing the data format, changing a type, renaming a resource, removing resources/fields/methods, and adding a required request field. A new optional response field is ignored by clients that do not know it.",
        topic="api-versioning", level=2),
    mcq("Name the versioning strategy: the client calls GET /books with the header `Accept: application/vnd.bookstore.v2+json`.",
        ["Media-type (content negotiation) versioning",
         "URI path versioning",
         "Query parameter versioning",
         "Semantic versioning of the server binary"], 0,
        "The version hides inside a content type.",
        "Four common strategies: URI path (/v2/books), query parameter (/books?version=2), custom header (X-API-Version: 2) and media type (Accept: application/vnd.bookstore.v2+json). The URI is the most visible; media types keep one URI per resource.",
        topic="api-versioning", level=2,
        diagram="""
URI path     GET /v2/books
query param  GET /books?version=2
header       GET /books   X-API-Version: 2
media type   GET /books   Accept: application/vnd.bk.v2+json
"""),
    mcq("A food-delivery startup's mobile home screen shows a restaurant's name, rating, three dishes and the user's last order, all from different services. Which API style does the course suggest fits this screen best?",
        ["GraphQL: one query fetches exactly those fields from several sources",
         "gRPC directly from the phone's browser",
         "Three REST calls, because GraphQL cannot combine sources",
         "Email"], 0,
        "One screen, many entities, only some fields.",
        "GraphQL lets the client name precisely the fields it needs across related data in one round trip, which matters on slow mobile networks. gRPC is aimed at service-to-service calls and has limited browser support.",
        topic="api-comparison", level=2),
    out("""versions = ["1.9.0", "1.10.0", "1.2.5"]

as_text = max(versions)
as_numbers = max(versions, key=lambda v: tuple(map(int, v.split("."))))
print(as_text, as_numbers)""",
        ["1.9.0 1.10.0", "1.10.0 1.10.0", "1.9.0 1.9.0", "1.2.5 1.10.0"], 0,
        "Strings compare character by character.",
        "As text, '1.9.0' > '1.10.0' because '9' > '1' at the third character. As integer tuples, (1, 10, 0) > (1, 9, 0). Clients and deploy scripts that pick 'the latest version' must compare numerically, or 1.10.0 never rolls out.",
        topic="semver", level=2),
    out("""from dataclasses import dataclass

@dataclass
class GetUserRequest:      # proto3: unset int32 reads as 0
    id: int = 0

def get_user(req, users={1: "Arun", 2: "Meera"}):
    if req.id <= 0:
        return "INVALID_ARGUMENT"
    return users.get(req.id, "NOT_FOUND")

print(get_user(GetUserRequest()), get_user(GetUserRequest(2)), get_user(GetUserRequest(9)))""",
        ["INVALID_ARGUMENT Meera NOT_FOUND", "NOT_FOUND Meera NOT_FOUND",
         "Arun Meera NOT_FOUND", "INVALID_ARGUMENT Meera INVALID_ARGUMENT"], 0,
        "What is id when the client never set it?",
        "This mirrors the learner's server.py. In proto3 a field the client did not set reads as its default, 0 for int32, so an empty GetUserRequest hits the id <= 0 check: INVALID_ARGUMENT. ID 2 is Meera; ID 9 is a valid ID that does not exist: NOT_FOUND.",
        topic="grpc-demos", level=2),
    out("""users = {1: "arun@example.com", 2: "meera@example.com"}

def create_user(email):
    email = email.strip().lower()
    if email in users.values():
        return "ALREADY_EXISTS"
    users[max(users) + 1] = email
    return f"created id={max(users)}"

print(create_user("  Kavya@Example.com"))
print(create_user("ARUN@example.com "))""",
        ["created id=3\nALREADY_EXISTS", "created id=3\ncreated id=4",
         "ALREADY_EXISTS\nALREADY_EXISTS", "created id=2\nALREADY_EXISTS"], 0,
        "Normalise first, then compare.",
        "Like the learner's CreateUser, the email is stripped and lowercased before the duplicate check, so 'ARUN@example.com ' matches arun@example.com and returns ALREADY_EXISTS. Without normalising, the same person could register twice with different capitals.",
        topic="grpc-demos", level=2),
    tf("A web page running in a browser can call a normal gRPC service directly with fetch(), with no extra layer.", False,
       "The slides call browser support 'primitive'.",
       "Browsers do not give JavaScript the low-level HTTP/2 control (trailers, framing) gRPC needs. gRPC-Web plus a proxy (e.g. Envoy) translates, or the service also exposes REST/JSON. That is why the slides call gRPC less suited to external-facing services.",
       topic="grpc-streaming", level=2),
    mcq("Which is a valid GraphQL mutation for adding a book?",
        ["mutation { addBook(title: \"Godan\", author: \"Premchand\") { id title } }",
         "query { DELETE books }",
         "POST /books { title: \"Godan\" }",
         "mutation GET /books"], 0,
        "Operation type, field with arguments, then the fields you want back.",
        "A mutation calls a field defined on the schema's Mutation type with arguments, and like a query it selects which fields of the result to return (here the new id and title).",
        topic="graphql-basics", level=2),
    fill("With URI path versioning, the bookstore's version-2 endpoint for books would usually look like /____/books.", "v2",
         "A short prefix in the path.",
         "URI versioning puts the major version in the path (/v1/books, /v2/books). It is the easiest to see, route and test in a browser; standard practice puts only the MAJOR number there.",
         topic="api-versioning", level=2),
    mcq("Why is HTTP caching easiest with REST among the three styles?",
        ["Each resource has its own URL and is read with GET, so browsers, CDNs and proxies can cache by URL; GraphQL usually sends POSTs to one /graphql URL and gRPC uses binary POSTs over HTTP/2",
         "REST responses are smaller",
         "GraphQL forbids caching",
         "gRPC has no responses"], 0,
        "What does a CDN use as the cache key?",
        "Standard HTTP caches key on method + URL. REST GETs fit perfectly. GraphQL needs client-side normalised caches or persisted queries sent as GET; gRPC caching is done in the application.",
        topic="api-comparison", level=2),
    mcq("A product-details screen in a mobile app needs only a product's name and price, but GET /products/42 returns 40 fields including long descriptions and image arrays. What problem is this and what does GraphQL change?",
        ["Over-fetching; with GraphQL the app asks for { product(id: 42) { name price } } and gets just those two fields",
         "Under-fetching; GraphQL adds more fields",
         "The N+1 problem; GraphQL caches it",
         "No problem; mobile data is free"], 0,
        "Too much data in one reply.",
        "Extra fields cost bandwidth, battery and parse time on phones. In REST you would add a sparse-fieldset parameter (?fields=name,price) or a dedicated endpoint; GraphQL makes field selection the default.",
        topic="graphql-fetching", level=2),
    # ------------------------------------------------------------------ L3
    out("""db_calls = []
def fetch_users():            db_calls.append("users");  return [1, 2, 3, 4, 5]
def fetch_posts(uid):         db_calls.append(f"posts:{uid}"); return []
def fetch_posts_batch(uids):  db_calls.append("posts:batch"); return {u: [] for u in uids}

users = fetch_users()
for u in users:               # naive resolver: Query.users -> User.posts
    fetch_posts(u)
naive = len(db_calls)

db_calls.clear()
fetch_posts_batch(fetch_users())   # DataLoader-style batching
print(naive, len(db_calls))""",
        ["6 2", "5 1", "6 6", "2 2"], 0,
        "One query for the list, then one per user.",
        "The naive User.posts resolver runs once per user: 1 + 5 = 6 database calls, the N+1 problem. A DataLoader collects the 5 user IDs in one tick and fetches posts in one batched query (WHERE user_id IN (...)): 2 calls. GraphQL hides the round trips from the client, not from the database.",
        topic="graphql-fetching", level=3,
        diagram="""
naive:    users -> posts(1) posts(2) ... posts(5)   = 1 + N
batched:  users -> posts(1,2,3,4,5)                 = 2
"""),
    tf("Moving from REST to GraphQL automatically removes the N+1 problem, because the client makes only one request.", False,
       "Where do the extra queries happen?",
       "GraphQL fixes N+1 round trips between client and server, but naive field resolvers can create N+1 queries between the server and the database. You still need batching (DataLoader), joins, or caching per request.",
       topic="graphql-fetching", level=3,
        analogy="Like a waiter who takes the whole table's order before going to the kitchen, instead of one trip per diner."),
    out("""response = {
    "data": {"user": None},
    "errors": [{"message": "User 99 not found", "path": ["user"]}],
}
http_status = 200

ok_by_status = http_status == 200
ok_by_body = not response.get("errors")
print(ok_by_status, ok_by_body)""",
        ["True False", "False False", "True True", "False True"], 0,
        "The transport says one thing, the body another.",
        "Many GraphQL servers return HTTP 200 even when a field fails, and report the problem in an 'errors' array next to partial 'data'. A client (or monitor) that checks only the status code thinks it worked. Always inspect 'errors'.",
        topic="graphql-basics", level=3,
        diagram="""
HTTP/1.1 200 OK
{"data": {"user": null},
 "errors": [{"message": "User 99 not found"}]}
"""),
    mcq("Version 1 of a proto has `string email = 3;`. A developer deletes email and, in the next release, adds `string phone = 3;`. Old clients still send email. What happens?",
        ["The server decodes old clients' email bytes as phone, because field number 3 identifies the field on the wire; deleted numbers should be marked `reserved 3;` and never reused",
         "protoc refuses to compile any file with a field number 3",
         "Nothing; field names are sent on the wire, so email and phone are distinct",
         "Old clients get a NOT_FOUND status"], 0,
        "What travels on the wire: the name or the number?",
        "Protobuf sends field numbers and values, not names. Reusing 3 makes old data parse into the new field silently. The learner's README says the same: keep identifiers stable and do not reuse old field numbers. `reserved 3; reserved \"email\";` makes protoc reject any reuse.",
        topic="grpc-protobuf", level=3,
        analogy="Like a cricket scorer who records shirt numbers: give a retired player's number to a new player and the old stats land on the wrong person."),
    mcq("In the learner's demos the student server binds `[::]:50051` and the user server binds `127.0.0.1:50051`. A classmate on the same Wi-Fi tries to call both from her laptop. What happens?",
        ["She can reach the student server (it listens on all interfaces), but not the user server (it listens on loopback only)",
         "She can reach both, because the port is the same",
         "She can reach neither, because gRPC never works across machines",
         "She can reach the user server only, because IPv6 is blocked"], 0,
        "127.0.0.1 is 'this machine only'.",
        "Loopback accepts connections from the same host; [::] is the 'all interfaces' address (on most systems including IPv4). Firewalls aside, only the student server is reachable over the LAN. Both use insecure channels, so exposing one on a network without TLS is fine only in a classroom.",
        topic="grpc-demos", level=3,
        diagram="""
laptop B ---- Wi-Fi ----> laptop A
  [::]:50051        student server  <- reachable
  127.0.0.1:50051   user server     <- same host only
"""),
    mcq("Why does the learner's UserService wrap reads and writes of self.users and self.next_id in `with self.lock:`?",
        ["The server runs handlers on a ThreadPoolExecutor (max_workers=4), so two CreateUser calls can run at once and could read the same next_id or both pass the duplicate-email check",
         "Locks make gRPC calls faster",
         "protoc requires a lock in every servicer",
         "The lock encrypts the data"], 0,
        "How many threads may run CreateUser at the same moment?",
        "A gRPC Python server calls handlers concurrently from its thread pool. Check-then-insert (duplicate email, then assign next_id) is a race without a lock. Real services push this into the database with a unique constraint and a sequence.",
        topic="grpc-demos", level=3),
    out("""deadline_s = 5.0
server_times = {"GetUser": 0.2, "CreateUser": 1.1,
                "ListUsers": 6.5, "Report": 4.9}

for rpc, t in server_times.items():
    status = "OK" if t <= deadline_s else "DEADLINE_EXCEEDED"
    print(rpc, status)""",
        ["GetUser OK\nCreateUser OK\nListUsers DEADLINE_EXCEEDED\nReport OK",
         "GetUser OK\nCreateUser OK\nListUsers OK\nReport OK",
         "GetUser OK\nCreateUser OK\nListUsers DEADLINE_EXCEEDED\nReport DEADLINE_EXCEEDED",
         "GetUser OK\nCreateUser DEADLINE_EXCEEDED\nListUsers DEADLINE_EXCEEDED\nReport OK"], 0,
        "Compare each time with 5 s.",
        "The learner's client passes timeout=5 on every call: a deadline. If the server has not answered in 5 s the client gets DEADLINE_EXCEEDED and stops waiting. Note the server may still finish the work, so a retried CreateUser could create a duplicate unless it is idempotent.",
        topic="grpc-demos", level=3),
    mcq("An agritech cooperative's field gateway uploads 10,000 soil-moisture readings collected overnight and wants one summary (average, min, max) back. Which gRPC call type fits?",
        ["Client streaming: rpc Upload (stream Reading) returns (Summary)",
         "Server streaming: rpc Upload (Reading) returns (stream Summary)",
         "Unary with 10,000 separate calls",
         "Bidirectional streaming, because there are two sides"], 0,
        "Many messages up, one message down.",
        "Client streaming sends a sequence of messages and gets a single response when the client closes the stream. It avoids 10,000 round trips and does not need the whole batch in memory at once.",
        topic="grpc-streaming", level=3),
    fill("A delivery app's live chat between rider and customer, where both sides send messages whenever they like over one call, uses ____ streaming in gRPC.", "bidirectional",
         "Both directions, independently.",
         "Bidirectional streaming: `rpc Chat (stream Message) returns (stream Message)`. The two streams are independent, so either side can send at any time, all multiplexed on one HTTP/2 connection.",
         topic="grpc-streaming", level=3),
    mcq("A Bengaluru mapping startup wants to offer a public API that thousands of outside developers, many using only a browser and curl, will call, similar to the Google Maps API. Which style should the external API use?",
        ["REST over HTTPS with JSON, documented with OpenAPI; gRPC can still be used between its internal services",
         "gRPC only, because it is fastest",
         "GraphQL only, because REST is deprecated",
         "Raw TCP sockets"], 0,
        "Who are the clients and what tools do they have?",
        "REST is the 'ubiquitous standard for the web': every language and tool can call it, it caches well and developers know it. gRPC's limited browser support and binary payloads make it a poor public face; many companies run gRPC inside and expose REST (or GraphQL) at the edge.",
        topic="api-comparison", level=3,
        analogy="Like English as the language of business email: not always the most compact, but every partner can read it."),
    mcq("The bookstore API is at 2.4.1. The next release fixes a pricing bug, adds GET /books/{id}/reviews, and removes the long-deprecated field 'isbn10'. What is the new version?",
        ["3.0.0", "2.5.0", "2.5.1", "2.4.2"], 0,
        "The most severe change decides.",
        "Removing a field breaks clients that read it, so MAJOR goes up and MINOR and PATCH reset: 3.0.0. The feature and the fix ride along. If the removal were held back, the release would be 2.5.0 (feature, patch reset).",
        topic="semver", level=3),
    out("""SEVERITY = {"fix": 0, "feature": 1, "breaking": 2}

def next_version(current, changes):
    major, minor, patch = map(int, current.split("."))
    worst = max(SEVERITY[c] for c in changes)
    if worst == 2: return f"{major + 1}.0.0"
    if worst == 1: return f"{major}.{minor + 1}.0"
    return f"{major}.{minor}.{patch + 1}"

print(next_version("3.54.4", ["fix", "fix"]),
      next_version("3.54.4", ["fix", "feature"]),
      next_version("0.9.12", ["feature", "breaking"]))""",
        ["3.54.5 3.55.0 1.0.0", "3.54.6 3.55.1 0.10.0", "3.54.5 3.55.0 0.10.0", "3.54.5 4.0.0 1.0.0"], 0,
        "Bump once per release, by the most severe change.",
        "Two fixes are still one PATCH bump (3.54.5). A fix plus a feature is a MINOR bump with PATCH reset (3.55.0). A breaking change bumps MAJOR. (Semver allows anything to change in 0.y.z, and many 0.x projects bump MINOR for breaks; this rule-based tool simply bumps MAJOR.)",
        topic="semver", level=3),
    mcq("The slides' movies example exposes /api/v1.0.0/movies, /api/v1.1.0/movies/search and /api/v2.0.0/movies. What is the flaw in putting full versions in the URI?",
        ["Every backward-compatible minor or patch release would force clients to change URLs; only the MAJOR version (/api/v1/, /api/v2/) needs to be in the path",
         "URIs cannot contain dots",
         "Semver forbids URIs",
         "There is no flaw; this is the recommended practice"], 0,
        "What does a MINOR release promise clients?",
        "MINOR and PATCH changes are compatible by definition, so clients on /v1/ should get them automatically. Putting 1.1.0 in the path multiplies routes and makes upgrades manual. Standard practice: /api/v1/movies with the full version in docs, change logs or a response header.",
        topic="api-versioning", level=3),
    mcq("A Pune smart-city complaints API wants every new complaint to carry a ward number. Thousands of citizens use an older app that sends POST /v1/complaints without it. Which plan avoids breaking them?",
        ["Make wardId optional in v1 (derive it from the location or default it) and require it only in a new /v2/complaints, with a deprecation period for v1",
         "Make wardId required in v1 today",
         "Return 500 when wardId is missing",
         "Silently drop complaints without wardId"], 0,
        "The slides list 'adding a new required field' as breaking.",
        "A new required request field breaks existing clients. Keep v1 working by making the field optional or derivable, ship the stricter contract as v2, announce a sunset date for v1 and monitor its traffic before switching it off.",
        topic="api-versioning", level=3,
        diagram="""
old app --POST /v1/complaints (no wardId)--> v1: derive
new app --POST /v2/complaints {wardId}----> v2: required
      v1 sunset date announced, traffic watched
"""),
    mcq("A developer says: 'The stub makes GetUser look like a normal Python method, so I can treat it like one.' What is the flaw?",
        ["A remote call can fail in ways a local call cannot (server down, network loss, timeouts, partial failure) and is far slower, so it needs deadlines, error handling and sometimes retries",
         "None; stubs make remote calls identical to local ones",
         "Stubs cannot return values",
         "Remote calls are always faster than local calls"], 0,
        "The README: 'network failures and deadlines still matter'.",
        "RPC hides the network, but it does not remove it. The learner's client sets timeout=5 and catches grpc.RpcError for exactly this reason. Treating remote calls as local is the root of many distributed-system outages.",
        topic="rpc", level=3),
    out("""calls = []
resolvers = {
    "Query.user":   lambda: (calls.append("user"),  {"id": 5})[1],
    "User.name":    lambda u: (calls.append("name"),  "Asha")[1],
    "User.posts":   lambda u: (calls.append("posts"), [{"id": 1}, {"id": 2}])[1],
    "Post.title":   lambda p: (calls.append("title"), f"post {p['id']}")[1],
}
u = resolvers["Query.user"]()
result = {"name": resolvers["User.name"](u),
          "posts": [{"title": resolvers["Post.title"](p)} for p in resolvers["User.posts"](u)]}
print(len(calls), result["posts"][1]["title"])""",
        ["5 post 2", "4 post 2", "5 post 1", "3 post 2"], 0,
        "Post.title runs once per post.",
        "For query { user { name posts { title } } } the engine calls Query.user, User.name, User.posts, then Post.title for each of the 2 posts: 5 resolver calls. The resolver count grows with the data, which is why cost and depth limits matter on public GraphQL APIs.",
        topic="graphql-schema", level=3),
    mcq("A client calls the slides' Calculator service with `Divide(a=10, b=0)`. What should a well-written server do?",
        ["Reject it with the INVALID_ARGUMENT status and a clear message, instead of crashing the handler",
         "Return result = 0 silently",
         "Return NOT_FOUND",
         "Let the ZeroDivisionError escape so the client sees UNKNOWN"], 0,
        "It is the client's bad input.",
        "Like the learner's GetUser rejecting id <= 0, a server validates inputs and aborts with INVALID_ARGUMENT. An unhandled exception reaches the client as UNKNOWN with no useful detail; a silent 0 is a wrong answer that looks right.",
        topic="grpc-protobuf", level=3),
    out("""WIRE_VARINT, WIRE_LEN = 0, 2

def tag(field_number, wire_type):
    return (field_number << 3) | wire_type

# message User { int32 id = 1; string name = 2; string email = 3; }
print(tag(1, WIRE_VARINT), tag(2, WIRE_LEN), tag(3, WIRE_LEN), hex(tag(2, WIRE_LEN)))""",
        ["8 18 26 0x12", "1 2 3 0x2", "8 16 24 0x10", "9 18 27 0x12"], 0,
        "Shift the field number left by 3 bits, then OR in the wire type.",
        "Each protobuf field starts with a tag = field_number << 3 | wire_type. id (field 1, varint) -> 8; name (field 2, length-delimited) -> 18 = 0x12; email (3) -> 26. The field name never travels, which is why renumbering breaks old clients and why fields 1-15 (one-byte tags) are best kept for frequent fields.",
        topic="grpc-protobuf", level=3,
        diagram="""
tag = field_number << 3 | wire_type
name: field 2, wire type 2 (length-delimited)
      00010 010 = 0x12 = 18
"""),
    mcq("Code generation per the course comparison: which statement is right?",
        ["gRPC generates client and server code natively with protoc for 10+ languages; REST relies on third-party tools such as Swagger/OpenAPI generators; GraphQL on tools such as GraphQL Code Generator",
         "REST generates code natively from URLs",
         "GraphQL cannot be used with code generation",
         "gRPC requires writing the serialization by hand"], 0,
        "Which one ships its own compiler?",
        "The .proto is both the contract and the input to protoc, so typed stubs come for free. REST gets the same benefit only if you maintain an OpenAPI spec; GraphQL tools generate types from the schema plus your queries.",
        topic="api-comparison", level=3),
    tf("A GraphQL client can ask the server for its own schema (types, fields, arguments) with an introspection query such as `{ __schema { types { name } } }`.", True,
       "How does GraphiQL know what to autocomplete?",
       "Introspection is built into GraphQL: the schema is queryable. GraphiQL and code generators use it. Some teams disable it on public production endpoints to make probing harder, but it is a standard feature.",
       topic="graphql-schema", level=3),
    mcq("A cricket-score app wants the server to push every new ball's update to clients as it happens. Which GraphQL operation type is designed for that?",
        ["subscription", "query", "mutation", "fragment"], 0,
        "The third operation type, beyond the two on the slides.",
        "Besides query and mutation, GraphQL defines subscription: the client subscribes to an event and the server pushes results, usually over WebSockets. Polling a query every second wastes calls; gRPC's equivalent would be server streaming.",
        topic="graphql-basics", level=3),
    fill("Announcing that an old API version (or field) still works but will be removed on a set date, so clients can migrate, is called ____ (one word).", "deprecation",
         "GraphQL even has a @____ed directive for fields.",
         "Deprecation is the polite half of versioning: mark it (docs, a Deprecation/Sunset response header, @deprecated in GraphQL, [deprecated = true] in protobuf), give a timeline, watch the remaining traffic, then remove it in the next MAJOR.",
         topic="api-versioning", level=3),
    # ------------------------------------------------------------------ L4
    out("""import json

def varint(n):
    out = []
    while True:
        b = n & 0x7F; n >>= 7
        out.append(b | 0x80 if n else b)
        if not n: return bytes(out)

def field_len(num, s):      # tag + length + utf-8 bytes
    data = s.encode()
    return bytes([(num << 3) | 2]) + varint(len(data)) + data

pb = bytes([1 << 3]) + varint(300) + field_len(2, "Arun") + field_len(3, "arun@example.com")
js = json.dumps({"id": 300, "name": "Arun", "email": "arun@example.com"}, separators=(",", ":"))
print(list(varint(300)), len(pb), len(js))""",
        ["[172, 2] 27 51", "[44, 2] 27 51", "[172, 2] 26 51", "[300] 25 54"], 0,
        "300 needs two 7-bit groups; the low group comes first with the continuation bit set.",
        "300 = 0b10_0101100: low 7 bits 44 with the high bit set (172), then 2. The protobuf User is 1 tag + 2 id bytes + 6 for name + 18 for email = 27 bytes; compact JSON with field names is 51. No field names on the wire is most of the saving, which is the 'lightweight' in the slides' gRPC advantages.",
        topic="grpc-protobuf", level=4),
    mcq("The learner's README says: 'A missing user produces gRPC NOT_FOUND. It is a gRPC status, not an HTTP 404 response.' What actually happens on the wire?",
        ["The HTTP/2 response normally has HTTP status 200, and the gRPC status (grpc-status: 5, NOT_FOUND) plus grpc-message travel in the trailers at the end of the stream",
         "The server sends HTTP 404 and the client library renames it",
         "No response is sent; the client times out",
         "The status is encoded inside the User message's id field"], 0,
        "gRPC carries its own status after the body.",
        "gRPC uses HTTP/2 as a transport and reports application outcomes in trailers (grpc-status, grpc-message). So HTTP-level monitoring that counts 4xx/5xx sees all 200s; you need gRPC-aware metrics. Mapping guides exist (NOT_FOUND <-> 404, UNAVAILABLE <-> 503) for gateways that translate.",
        topic="grpc-demos", level=4,
        analogy="Like a courier who always reports 'delivered' (HTTP 200) while the note inside the parcel says 'item not found' (grpc-status 5)."),
    mcq("A public GraphQL API for a Bengaluru events app gets this query from a bot: `{ user(id: 1) { friends { friends { friends { friends { name } } } } } }`. Each user has ~200 friends. What is the risk and the defence?",
        ["About 200^4 = 1.6 billion resolver results from one request; enforce maximum depth and complexity/cost limits (or allow only persisted, pre-approved queries)",
         "No risk; GraphQL returns only requested fields",
         "It returns a 404 because the query is nested",
         "Rate limiting by request count alone is enough, because it is one request"], 0,
        "One request is not one unit of work.",
        "Flexible queries let a client ask for exponential work. Counting requests misses it; servers compute a cost or depth before execution and reject expensive queries, and first-party apps often ship persisted queries identified by hash.",
        topic="graphql-fetching", level=4,
        analogy="Like an all-you-can-eat buffet with no plate limit: one ticket, unlimited load on the kitchen."),
    out("""query = "{ user(id: 1) { name friends { name friends { name } } } }"

depth = max_depth = 0
for ch in query:
    if ch == "{":
        depth += 1
        max_depth = max(max_depth, depth)
    elif ch == "}":
        depth -= 1
LIMIT = 3
print(max_depth, "rejected" if max_depth > LIMIT else "accepted")""",
        ["4 rejected", "3 accepted", "4 accepted", "2 accepted"], 0,
        "Count the deepest nesting of braces, including the outer one.",
        "Braces open for the operation, user, friends and the inner friends: depth 4, above the limit of 3, so the server refuses it before running a resolver. Real servers walk the parsed query (fragments, aliases) rather than counting characters, but the idea is the same.",
        topic="graphql-schema", level=4),
    mcq("A team needs user IDs to become UUID strings. The proto has `int32 id = 1;`. What is the safe evolution?",
        ["Add `string uuid = 4;`, populate both for a while, mark id [deprecated = true], move clients over, and remove id (reserving 1) only in a new major version",
         "Change it in place to `string id = 1;`",
         "Change it to `string id = 1;` and renumber the other fields",
         "Delete the field and let clients guess"], 0,
        "Changing a field's type is on the slides' breaking-change list.",
        "Changing the type of field 1 makes old and new binaries decode each other's bytes wrongly (a varint vs a length-delimited string). Additive change with a new number, a transition period and then a reserved number keeps every client working.",
        topic="grpc-protobuf", level=4),
    mcq("A food-delivery company has 30 internal microservices speaking gRPC. Its Android app and web site need flexible data. Which architecture fits the course comparison best?",
        ["A GraphQL (or REST) gateway / backend-for-frontend at the edge whose resolvers call the internal gRPC services",
         "Expose all 30 gRPC services directly to browsers",
         "Replace all internal gRPC with GraphQL between services",
         "Use one REST endpoint per microservice for the app, called 30 times per screen"], 0,
        "Each style where it is strongest.",
        "gRPC is 'best for inter-service communication' but weak in browsers; GraphQL suits client-driven screens. A gateway translates: the app sends one GraphQL query, resolvers fan out to gRPC services over fast HTTP/2 connections. Many large companies run exactly this split.",
        topic="api-comparison", level=4,
        diagram="""
Android/Web --GraphQL--> [ BFF / gateway ]
                          |      |      |
                        gRPC   gRPC   gRPC
                          |      |      |
                      orders  menu   riders
"""),
    out("""handlers = {"1": lambda: {"title": "Godan", "author": "Premchand"},
            "2": lambda: {"title": "Godan", "author": {"name": "Premchand"}}}

def get_book(headers):
    version = headers.get("X-API-Version", "1")
    h = handlers.get(version)
    return (200, h()) if h else (400, {"error": f"unknown version {version}"})

print(get_book({})[1]["author"])
print(get_book({"X-API-Version": "2"})[1]["author"]["name"])
print(get_book({"X-API-Version": "3"})[0])""",
        ["Premchand\nPremchand\n400", "Premchand\nPremchand\n200",
         "{'name': 'Premchand'}\nPremchand\n400", "KeyError"], 0,
        "What does a client that sends no header get?",
        "With header versioning, clients that send nothing get the default (v1, author as a string); v2 clients get the new object shape; an unknown version is a client error (400). Defaulting to v1 keeps old clients working; defaulting to 'latest' would break them on every major release. Caches must also Vary on X-API-Version.",
        topic="api-versioning", level=4),
    tf("By semver precedence, 2.0.0-beta.2 is lower than 2.0.0, so a client asking for 'the latest stable 2.x' should not get the beta.", True,
       "A hyphen marks a pre-release.",
       "Pre-release versions (2.0.0-alpha, 2.0.0-beta.2, 2.0.0-rc.1) sort before the release they lead up to, and they promise no stability. Publishing a beta lets early adopters test a breaking MAJOR before it becomes the default.",
       topic="semver", level=4),
    out("""def key(v):
    core, _, pre = v.partition("-")
    nums = tuple(map(int, core.split(".")))
    return (nums, 0 if pre else 1, pre)   # pre-release sorts first

vs = ["2.0.0", "1.10.0", "2.0.0-rc.1", "1.9.9", "2.0.0-beta.2"]
print(sorted(vs, key=key))""",
        ["['1.9.9', '1.10.0', '2.0.0-beta.2', '2.0.0-rc.1', '2.0.0']",
         "['1.10.0', '1.9.9', '2.0.0', '2.0.0-beta.2', '2.0.0-rc.1']",
         "['1.9.9', '1.10.0', '2.0.0', '2.0.0-beta.2', '2.0.0-rc.1']",
         "['1.9.9', '1.10.0', '2.0.0-rc.1', '2.0.0-beta.2', '2.0.0']"], 0,
        "Numbers numerically; a pre-release before its release; 'beta' < 'rc' as text.",
        "Core versions compare as integers (1.9.9 < 1.10.0). For the same core, any pre-release ranks below the release, and pre-release labels compare by identifier ('beta.2' < 'rc.1' alphabetically). Real semver compares dot-separated identifiers one by one, numbers numerically; this key is enough for these labels.",
        topic="semver", level=4),
    mcq("A partner pinned your SDK at 0.4.x, and your 0.5.0 release renamed a method. They complain that semver was violated. Who is right?",
        ["Neither rule was broken: semver says 0.y.z is initial development and anything may change; the fix is to reach 1.0.0 once partners depend on the API",
         "The partner: 0.5.0 must be backward compatible",
         "Semver forbids versions below 1.0.0",
         "You must call it 0.4.1"], 0,
        "Major version zero is special.",
        "Under 1.0.0 the public API is not considered stable. Many ecosystems treat a 0.MINOR bump as breaking by convention, which is what happened here. Once real users rely on the API, release 1.0.0 and follow the full rules.",
        topic="semver", level=4),
    mcq("ListUsers returns all users in one ListUsersResponse. With 5 lakh users the client starts failing with RESOURCE_EXHAUSTED. What is the likely cause and the fix?",
        ["The single response exceeds gRPC's default maximum message size (4 MB for receiving in most implementations); paginate (page_size/page_token) or switch to server streaming `returns (stream User)`",
         "The server ran out of user IDs",
         "HTTP/2 cannot carry more than 1,000 items",
         "repeated fields are limited to 100 entries"], 0,
        "One giant message.",
        "gRPC caps message sizes by default to protect memory. Raising the limit only postpones the problem; page through results or stream them so each message stays small and the client can process users as they arrive.",
        topic="grpc-streaming", level=4,
        analogy="Like sending a 500-page book as one courier packet instead of chapter by chapter: it may not fit through the door."),
    mcq("The learner's client calls CreateUser with a fixed email, the call hits DEADLINE_EXCEEDED, and the client retries. The retry returns ALREADY_EXISTS. What most likely happened, and how should the API be designed?",
        ["The first call did succeed after the deadline; make creation idempotent with a client-supplied request ID so a retry returns the original user instead of an error",
         "The server is broken; ALREADY_EXISTS should never appear",
         "Deadlines cancel the server's work, so the first call cannot have succeeded",
         "The client should retry forever until it gets OK"], 0,
        "A deadline stops the waiting, not necessarily the work.",
        "The client gave up at 5 s, but the server finished and stored the user. The duplicate-email check then rejected the retry. The demo sidesteps this with a unique email per run; production APIs accept a request_id field and replay the stored result, like an Idempotency-Key in REST.",
        topic="grpc-demos", level=4,
        diagram="""
client --CreateUser--> server  (slow)
   |  5 s: DEADLINE_EXCEEDED     | ... stores user 7
client --CreateUser--> server
   <-- ALREADY_EXISTS ----------|
"""),
    tf("After an RPC fails with DEADLINE_EXCEEDED, retrying it is always safe because the server never responded.", False,
       "Never responded is not the same as never acted.",
       "The server may have completed the work after the client stopped waiting. Retry automatically only idempotent RPCs (GetUser) or ones protected by a request ID; gRPC's built-in retry policy is configured per method for this reason.",
       topic="rpc", level=4),
    mcq("Which operation fits an RPC style more naturally than a resource-oriented REST design?",
        ["Calculator.Add(a, b): a computation with no resource to create, read, update or delete",
         "Reading book 42",
         "Deleting order 9",
         "Listing a customer's orders"], 0,
        "Is there a noun to name with a URI?",
        "REST models nouns (resources) and maps actions to a few methods; RPC models verbs (procedures). Pure actions like Add, Translate, Predict fit RPC well; in REST they end up as awkward POST /additions. Neither style is wrong; choose by the shape of the operations.",
        topic="rpc", level=4),
    out("""calls_per_day = 5 * 10**7        # 5 crore internal calls
json_bytes, proto_bytes = 1200, 400
rupees_per_gb = 7                 # network transfer cost

def daily_cost(size):
    return calls_per_day * size / 10**9 * rupees_per_gb

saving = (daily_cost(json_bytes) - daily_cost(proto_bytes)) * 30
print(round(daily_cost(json_bytes)), round(daily_cost(proto_bytes)), round(saving))""",
        ["420 140 8400", "420 140 280", "60 20 1200", "4200 1400 84000"], 0,
        "Bytes per day = calls × bytes per call; divide by 10^9 for GB.",
        "JSON: 5×10^7 × 1,200 B = 60 GB/day -> ₹420. Protobuf: 20 GB/day -> ₹140. Over 30 days that saves ₹8,400 in transfer alone, before counting the CPU saved on parsing text. At internal-service volumes this is a concrete reason the slides call gRPC 'lightweight and fast'.",
        topic="api-comparison", level=4),
    fill("In a .proto file, the keyword written before a deleted field's number and name, so that nobody can reuse them later, is ____.", "reserved",
         "It reserves them forever.",
         "`reserved 3; reserved \"email\";` makes protoc fail if a later edit reuses field 3 or the name email, preventing the silent decoding bug where old data lands in a new field.",
         topic="grpc-protobuf", level=4),
    tf("If an API versions by a request header (X-API-Version) and sits behind a CDN, responses must include `Vary: X-API-Version`, or the CDN may serve a cached v1 response to a v2 client.", True,
       "A CDN keys on the URL unless told otherwise.",
       "With URI versioning, /v1/books and /v2/books are different cache keys automatically. Header and media-type versioning use one URL, so the Vary header must tell caches that the header changes the response. Forgetting it causes version mix-ups that are hard to reproduce.",
       topic="api-versioning", level=4),
    out("""def list_users_unary(users):
    return {"users": list(users)}          # one message with the whole list

def list_users_stream(users):
    for u in users:                        # server streaming: one message each
        yield {"user": u}

users = ["Arun", "Meera", "Kavya"]
print(len([list_users_unary(users)]), len(list(list_users_stream(users))))
first = next(list_users_stream(users))
print(first)""",
        ["1 3\n{'user': 'Arun'}", "3 3\n{'user': 'Arun'}", "1 1\n{'users': ['Arun', 'Meera', 'Kavya']}", "1 3\n{'user': 'Kavya'}"], 0,
        "Count messages, not users.",
        "The unary version (like the learner's ListUsers) sends one message holding all three users. A server-streaming version sends three messages, and the client can start on the first one before the rest are produced, as a Python generator yields items one at a time.",
        topic="grpc-streaming", level=2),
]
