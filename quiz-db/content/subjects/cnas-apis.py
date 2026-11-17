from helpers import mcq, tf, out, fill

SUBJECT = "cnas-apis"

TOPICS = [
    ("api-basics", "What an API is: a contract between a service and its clients"),
    ("sync-async", "Synchronous vs asynchronous APIs"),
    ("http-components", "Components of an HTTP API: endpoint, request, response"),
    ("http-methods", "HTTP methods, safe and idempotent methods"),
    ("status-codes", "Status codes and families"),
    ("rest-architecture", "REST architecture and constraints"),
    ("rest-design", "REST resource design, benefits and drawbacks"),
    ("openapi", "OpenAPI (formerly Swagger)"),
    ("api-lifecycle", "The bookstore API lifecycle with FastAPI"),
]

QUESTIONS = [
    # ------------------------------------------------------------------ L1
    mcq("The course's first definition of an API is 'a ____ between a service and its clients'. Which word fits?",
        ["contract", "database", "server", "programming language"], 0,
        "Both sides agree on it in advance.",
        "An API is a contract: the service promises which requests it accepts and what it returns; clients rely only on that promise, not on the code behind it. That is why changing an API carelessly breaks other people's software.",
        topic="api-basics", level=1,
        analogy="Like a restaurant menu: you order from the menu and get the dish, without ever seeing the kitchen."),
    tf("An API lets two software systems exchange data and functions without the caller needing to understand the other system's internal code.", True,
       "Think of calling the Google Maps API from your app.",
       "This is the slides' third definition. Your app sends a request to the Google Maps API and gets directions back; you never see or need Google's code. You depend only on the documented requests and responses.",
       topic="api-basics", level=1),
    mcq("RapidAPI is mentioned in the course as an API example. What is it?",
        ["A marketplace/hub where developers find, test and subscribe to many third-party APIs with one account and key",
         "A programming language for writing fast APIs",
         "A database that stores API responses",
         "Google's mapping API"], 0,
        "Think 'app store', but for APIs.",
        "RapidAPI is an API hub: providers publish APIs, consumers browse, try them in the browser and call them with one key. It shows the idea of APIs as products that other developers buy and build on.",
        topic="api-basics", level=1),
    mcq("Which of these is an asynchronous API style according to the slides?",
        ["Communication through a message broker such as RabbitMQ or Apache Kafka",
         "REST", "gRPC", "GraphQL"], 0,
        "Which option has a middleman holding messages?",
        "The slides list REST, gRPC and GraphQL as synchronous (the caller waits for the reply) and message brokers like RabbitMQ and Kafka as asynchronous (the sender puts a message on the broker and carries on).",
        topic="sync-async", level=1),
    tf("In a synchronous API call, the client waits for the server's reply before it continues with that piece of work.", True,
       "Synchronous = in step.",
       "Synchronous means request -> wait -> response. The order service in the slides calls the payment service over REST and cannot finish the order until payment answers. Asynchronous calls hand off the work and continue.",
       topic="sync-async", level=1,
       diagram="""
client            server
  |--- request ---->|
  |   (waiting)     | works
  |<--- response ---|
  | continues       |
"""),
    fill("An API ____ is the URL a client sends requests to, such as https://www.bits.edu/institute/students (one word).", "endpoint",
         "The slides call it the 'door' to a resource.",
         "An endpoint is a URL that represents a collection (/students) or one object (/students/123). Each endpoint plus method performs one function, e.g. GET /students/123 fetches one student.",
         topic="http-components", level=1),
    mcq("In which formats do HTTP APIs usually return data, according to the slides?",
        ["JSON or XML", "PDF or DOCX", "CSV only", "HTML only"], 0,
        "The slides show the same user in two formats.",
        "The slides show one user as XML (<user><id>1</id>...) and as JSON ({\"id\": 1, ...}). JSON dominates modern APIs because it is light and maps directly to JavaScript and Python objects.",
        topic="http-components", level=1),
    mcq("Which HTTP method should a client use to retrieve the list of books without changing anything?",
        ["GET", "POST", "PUT", "DELETE"], 0,
        "Read-only.",
        "GET retrieves a representation of a resource. POST submits data to create, PUT updates or replaces, DELETE removes. GET /books lists the books.",
        topic="http-methods", level=1),
    fill("The HTTP method that creates a new resource, e.g. submitting a new student's details to /institute/students, is ____.", "POST",
         "CRUD's C.",
         "POST sends data to a collection and the server creates a new item (and usually assigns its ID). GET reads, PUT updates, DELETE removes.",
         topic="http-methods", level=1),
    mcq("A request succeeds and the server returns the requested data. Which status code is that?",
        ["200 OK", "201 Created", "204 No Content", "404 Not Found"], 0,
        "The most common success code.",
        "200 OK means success with a body. 201 is for a newly created resource, 204 is success with no body, and 404 means the resource does not exist.",
        topic="status-codes", level=1),
    tf("Status 404 Not Found means the server crashed while handling the request.", False,
       "Which family is 4xx?",
       "404 is a client-side error: the requested resource does not exist (e.g. GET /books/999 when there is no book 999). A crash is 500 Internal Server Error, a 5xx code.",
       topic="status-codes", level=1),
    fill("The status code a server returns after a POST successfully creates a new book is ____ Created.", "201",
         "Just after 200.",
         "201 Created tells the client a new resource exists, usually with a Location header pointing at it, e.g. Location: /books/42. Plain 200 works but says less.",
         topic="status-codes", level=1),
    mcq("Who introduced REST, and when?",
        ["Roy Fielding, in his 2000 doctoral dissertation", "Facebook, in 2015",
         "Google, in 2015", "Tim Berners-Lee, in 1989"], 0,
        "It describes the architecture of the web.",
        "Roy Fielding defined REST (Representational State Transfer) in 2000 to describe why the web scales. Facebook released GraphQL in 2015 and Google released gRPC in 2015; Berners-Lee invented the web itself.",
        topic="rest-architecture", level=1),
    mcq("In REST, what is a 'resource'?",
        ["Any piece of content the API exposes, such as a student, a web page, an image or a PDF, identified by a URI",
         "The server's CPU and memory",
         "A function name like getStudent()",
         "The database table only"], 0,
        "REST treats every content as one.",
        "The slides: 'REST architecture treats every content as a resource', each identified by a URI, e.g. /institute/students/123. Clients act on resources through standard methods; how the server stores them is hidden.",
        topic="rest-architecture", level=1,
        analogy="Like files on a shared drive: every file has a path, and open, save and delete work the same way on any of them."),
    tf("REST is a protocol, in the same way that HTTP is a protocol.", False,
       "The slides call it an 'architectural ____'.",
       "REST is an architectural style: a set of constraints (client-server, stateless, cacheable, uniform interface, layered). HTTP is the protocol most REST APIs use to follow that style.",
       topic="rest-architecture", level=1),
    mcq("Following the slides' BITS example, which URI and method fetch only the student with ID 123?",
        ["GET https://www.bits.edu/institute/students/123",
         "GET https://www.bits.edu/institute/getStudent?id=123",
         "POST https://www.bits.edu/institute/students/123",
         "DELETE https://www.bits.edu/institute/students/123"], 0,
        "Collection noun, then the item ID.",
        "REST URIs name resources with nouns: /students is the collection, /students/123 one item. The method carries the verb, so GET reads it. 'getStudent' puts the verb in the URI, which REST avoids.",
        topic="rest-design", level=1),
    mcq("What is the OpenAPI Specification?",
        ["A formal standard for describing HTTP (mainly RESTful) APIs, previously called the Swagger specification",
         "A free public API anyone can call",
         "A Python web framework",
         "A protocol that replaces HTTP"], 0,
        "It describes APIs; it does not run them.",
        "OpenAPI is a machine-readable description (YAML/JSON) of an API's endpoints, parameters and responses. From it, people and tools can read the docs, generate client code and create tests.",
        topic="openapi", level=1,
        analogy="Like a TypeScript interface for a whole web service: it states the shapes and signatures, not the implementation."),
    fill("Before it was renamed OpenAPI in 2016, the specification was called the ____ specification.", "Swagger",
         "Its UI tool still has this name.",
         "The Swagger specification was donated to the OpenAPI Initiative and renamed. The name lives on in tools such as Swagger UI (the interactive docs FastAPI serves at /docs) and Swagger Editor.",
         topic="openapi", level=1),
    mcq("What is the first stage of the slides' bookstore API lifecycle?",
        ["Requirements: decide what the API must do (add, retrieve, update and delete books)",
         "Deploy to AWS", "Write pytest tests", "Start Uvicorn"], 0,
        "You cannot design what you have not defined.",
        "The order is requirements -> design -> configure -> publish -> develop -> test -> deploy. Requirements for the bookstore were CRUD on books.",
        topic="api-lifecycle", level=1),
    mcq("In the bookstore scenario, where does FastAPI publish the auto-generated interactive documentation?",
        ["At /docs, e.g. http://localhost:8000/docs", "At /index.html", "In a PDF in the project folder", "Only in the README"], 0,
        "The slides give the exact URL.",
        "FastAPI builds an OpenAPI document from your route functions and serves Swagger UI at /docs (and ReDoc at /redoc, the raw spec at /openapi.json). Uvicorn serves it on port 8000 by default.",
        topic="api-lifecycle", level=1),
    fill("In the bookstore scenario, the web server that runs the FastAPI app (the slides' 'configure' step) is ____.", "Uvicorn",
         "An ASGI server whose name starts with U.",
         "FastAPI is the framework (routes, validation, docs); Uvicorn is the ASGI server that listens on the port and passes requests to it: `uvicorn main:app --reload`. Like Express (framework) running on Node's HTTP server.",
         topic="api-lifecycle", level=1),
    tf("Amazon Bedrock, Hugging Face and Prefect can all be called through RESTful HTTP APIs, which is one reason the course starts with REST.", True,
       "The slides list a Bedrock model-inference endpoint.",
       "The slides show Bedrock's /models/{model-id}/invoke and /models endpoints: you send a request with an access token and get JSON back. Hugging Face, LangChain servers and Prefect expose REST too, so the same HTTP skills apply to every AI service in the course.",
       topic="api-basics", level=1),
    # ------------------------------------------------------------------ L2
    out("""def family(code):
    return {1: "informational", 2: "success", 3: "redirection",
            4: "client error", 5: "server error"}[code // 100]

for c in (201, 304, 403, 503):
    print(c, family(c))""",
        ["201 success\n304 redirection\n403 client error\n503 server error",
         "201 success\n304 client error\n403 client error\n503 server error",
         "201 informational\n304 redirection\n403 client error\n503 server error",
         "201 success\n304 redirection\n403 server error\n503 server error"], 0,
        "Integer-divide by 100 to get the first digit.",
        "The first digit is the family: 2xx success, 3xx redirection (304 Not Modified tells the client to use its cached copy), 4xx client error, 5xx server error. Clients and monitors route on the family first.",
        topic="status-codes", level=2,
        diagram="""
1xx informational   2xx success   3xx redirection
4xx client error -> fix the request, do not retry
5xx server error -> maybe retry later
"""),
    mcq("A user is logged in to a food-delivery admin portal as a normal customer and calls DELETE /restaurants/17. Only admins may do that. Which status fits?",
        ["403 Forbidden", "401 Unauthorized", "404 Not Found", "400 Bad Request"], 0,
        "The server knows who the user is.",
        "403: authenticated, but not allowed. 401 means the credentials are missing or invalid ('who are you?'). The names are confusing: 401 is really 'unauthenticated'. Some APIs return 404 to hide that the resource exists, but the textbook answer is 403.",
        topic="status-codes", level=2,
        analogy="401 is the guard asking for your ID card; 403 is the guard reading it and saying you are not on the list."),
    mcq("Which HTTP methods are idempotent, i.e. sending the same request twice leaves the server in the same state as sending it once?",
        ["GET, PUT and DELETE", "POST and PATCH only", "Only GET", "All four: GET, POST, PUT, DELETE"], 0,
        "Repeat 'set price to 450' vs repeat 'add a book'.",
        "PUT /books/7 with the same body sets the same final state each time; DELETE /books/7 leaves the book gone however often you call it; GET changes nothing. POST /books creates a new book each time, so it is not idempotent.",
        topic="http-methods", level=2,
        diagram="""
method  safe  idempotent
GET     yes   yes
PUT     no    yes
DELETE  no    yes
POST    no    no
PATCH   no    not guaranteed
"""),
    out("""books, next_id = {}, 1
def post(body):
    global next_id
    books[next_id] = body; next_id += 1
def put(book_id, body):
    books[book_id] = body

for _ in range(3):
    post({"title": "Godan"})
for _ in range(3):
    put(10, {"title": "Gitanjali"})
print(len(books))""",
        ["4", "6", "2", "3"], 0,
        "Each POST picks a fresh ID; each PUT targets the same ID.",
        "Three POSTs create books 1, 2 and 3. Three PUTs all write to ID 10, so they leave one book there. 3 + 1 = 4. This is idempotency in code: repeating PUT changes nothing after the first call; repeating POST keeps adding.",
        topic="http-methods", level=2),
    tf("A method being 'safe' means it does not change the server's state; GET and HEAD are safe, PUT and DELETE are not.", True,
       "Safe is stricter than idempotent.",
       "Safe = read-only (GET, HEAD, OPTIONS). Every safe method is idempotent, but PUT and DELETE are idempotent without being safe, because they do change state, just the same way every time. Crawlers and prefetchers assume GET is safe, so a GET that deletes data is a real bug.",
       topic="http-methods", level=2),
    mcq("In GET /restaurants/42/menu?veg=true&page=2, which part is a path parameter and which are query parameters?",
        ["42 is a path parameter (which restaurant); veg and page are query parameters (filter and paging)",
         "veg and page are path parameters; 42 is a query parameter",
         "All three are headers",
         "menu is the query parameter"], 0,
        "Path identifies, query refines.",
        "Path parameters pick the resource: /restaurants/{id}/menu. Query parameters after ? filter, sort or page the result. A useful rule: if removing it changes which resource you mean, it belongs in the path.",
        topic="http-components", level=2,
        analogy="The path is the shelf and accession number of a library book; the query is 'only Hindi editions, page 2 of the results'."),
    out("""from urllib.parse import urlsplit, parse_qs

u = urlsplit("https://api.foodapp.example/v1/restaurants/42/menu?veg=true&page=2")
print(u.path.split("/")[3])
print(parse_qs(u.query))""",
        ["42\n{'veg': ['true'], 'page': ['2']}",
         "restaurants\n{'veg': ['true'], 'page': ['2']}",
         "42\n{'veg': 'true', 'page': '2'}",
         "42\n{'veg': [True], 'page': [2]}"], 0,
        "Split '/v1/restaurants/42/menu' on '/' and count from 0; the first piece is empty.",
        "The path splits into ['', 'v1', 'restaurants', '42', 'menu'], so index 3 is '42'. parse_qs returns lists of strings because a key may repeat (?tag=a&tag=b) and everything in a URL is text; your framework converts types.",
        topic="http-components", level=2),
    mcq("A mobile client sends a JSON body and wants JSON back. Which pair of request headers says that?",
        ["Content-Type: application/json (what I am sending) and Accept: application/json (what I want back)",
         "Accept: application/json for both directions",
         "Content-Length: json and Host: json",
         "Authorization: application/json"], 0,
        "One header describes the body, the other asks for a format.",
        "Content-Type labels the body in this message; Accept is content negotiation for the reply. A server that cannot produce the Accept type may answer 406 Not Acceptable; a body it cannot read gets 415 Unsupported Media Type.",
        topic="http-components", level=2,
        analogy="Content-Type is the language your letter is written in; Accept is the language you want the reply in."),
    mcq("Where does a client usually put its access token when calling a protected REST API such as Bedrock's model-inference endpoint?",
        ["In the Authorization request header, e.g. Authorization: Bearer <token>",
         "In the URL path, e.g. /models/<token>/invoke",
         "In the response body",
         "In the status code"], 0,
        "Headers carry metadata about the request.",
        "Credentials go in a header (Authorization, or a signed header set as with AWS SigV4). Tokens in URLs end up in server logs, browser history and proxies. The body carries the business data; the status code belongs to the response.",
        topic="http-components", level=2,
        diagram="""
POST /books HTTP/1.1            <- method + URI
Host: localhost:8000            <- headers
Content-Type: application/json
Authorization: Bearer eyJ...
                                <- blank line
{"title": "Godan", "price": 299}  <- body
"""),
    tf("In the slides' asynchronous design, the client and the order service put messages on a broker such as Kafka, and the other services pick them up when they are ready.", True,
       "Who is between the services?",
       "With a broker, the producer does not need the consumer to be up right now: the message waits in the queue or topic. That removes the availability coupling of synchronous REST at the cost of eventual results and more moving parts.",
       topic="sync-async", level=2,
       diagram="""
order svc --msg--> [Kafka/RabbitMQ] --msg--> payment svc
(continues)       (stores message)    (reads when ready)
"""),
    mcq("A payment gateway says: 'Give us a URL and we will POST a JSON event to it when the payment succeeds.' What is this pattern called?",
        ["A webhook: the provider calls the client's URL when the event happens",
         "Polling", "A GraphQL subscription", "Server-side rendering"], 0,
        "A reverse API call.",
        "Webhooks are asynchronous: you do not wait or poll; the provider pushes an HTTP request to your endpoint when something happens. Your endpoint should reply 2xx fast, verify the signature and process the event idempotently because providers retry deliveries.",
        topic="sync-async", level=2,
        analogy="Polling is calling the restaurant every two minutes to ask if the food is ready; a webhook is the restaurant calling you when it is."),
    mcq("Which statement correctly describes the REST 'stateless' constraint?",
        ["Each request carries everything the server needs (e.g. the token and IDs); the server keeps no client session between requests",
         "The server must not store any data at all, not even in a database",
         "The client must not cache any response",
         "Every request must use GET"], 0,
        "It is about session state, not data.",
        "Stateless means no per-client conversation state on the server: request 2 does not rely on the server remembering request 1. Resource state (books in a database) is fine. This is what lets any replica behind a load balancer handle any request.",
        topic="rest-architecture", level=2,
        analogy="Like a bank counter where any clerk can serve you because you bring your passbook every time, instead of one clerk remembering you."),
    mcq("Which list gives the REST architectural constraints?",
        ["Client-server, stateless, cacheable, uniform interface, layered system, and optional code on demand",
         "Schema, query, mutation, resolver",
         "Atomicity, consistency, isolation, durability",
         "Requirements, design, configure, publish"], 0,
        "Fielding's six (one optional).",
        "These are Fielding's constraints. The second option describes GraphQL, the third is ACID for databases, the fourth is the start of the bookstore lifecycle.",
        topic="rest-architecture", level=2,
        diagram="""
client -> cache/CDN -> gateway -> API server -> DB
  stateless requests, cacheable replies,
  each layer sees only its neighbour
"""),
    fill("The REST constraint that says clients use the same small set of methods, URIs and representations for every resource is called the uniform ____.", "interface",
         "Two words: uniform ____.",
         "The uniform interface (resource identification by URI, manipulation through representations, self-descriptive messages, hypermedia) is what makes a generic tool like curl or a browser work with any REST API.",
         topic="rest-architecture", level=2),
    mcq("The course's food-delivery app uses REST. Which endpoint design follows REST conventions for placing an order for a customer?",
        ["POST /customers/{customerId}/orders", "GET /placeOrder?customer=5",
         "POST /createNewOrderForCustomer", "PUT /orders/create"], 0,
        "Noun collections, the method is the verb.",
        "POST to the orders collection creates an order; nesting under the customer shows ownership. A GET that places an order breaks the safe-method rule (a prefetcher could order food), and verbs in URIs duplicate what the method already says.",
        topic="rest-design", level=2),
    tf("The slides list 'no intermediate broker' as a benefit of REST.", True,
       "Compare with the async design.",
       "REST calls go straight from client to service: fewer components to run and debug. The other slide benefits: mature and ubiquitous, simple to test, synchronous request-response, supported by most languages and frameworks.",
       topic="rest-design", level=2),
    mcq("In the slides' social-media scenario, a REST client needs a user's profile, their posts and the comments on one post. How many HTTP requests does it make?",
        ["3: GET /users/{userId}, GET /users/{userId}/posts, GET /posts/{postId}/comments",
         "1: GET /users/{userId}", "2: GET /users and GET /comments", "0: REST pushes the data"], 0,
        "One resource, one endpoint.",
        "Each resource has its own endpoint, so related data costs one round trip each. This is the 'fetching multiple resources' drawback on the slides and the reason GraphQL exists (next subject). For comments on every post it grows to 2 + number of posts.",
        topic="rest-design", level=2,
        diagram="""
app --GET /users/5----------> profile
app --GET /users/5/posts----> [post 9, ...]
app --GET /posts/9/comments-> [comments]
      3 round trips for one screen
"""),
    out("""spec = {
    "openapi": "3.1.0",
    "info": {"title": "Bookstore API", "version": "1.0.0"},
    "paths": {
        "/books": {"get": {}, "post": {}},
        "/books/{id}": {"get": {}, "put": {}, "delete": {}},
    },
}
ops = sum(len(item) for item in spec["paths"].values())
print(len(spec["paths"]), ops)""",
        ["2 5", "5 5", "2 2", "5 2"], 0,
        "Paths are URL templates; operations are path + method.",
        "An OpenAPI document lists paths, and under each path one operation per HTTP method. The bookstore design has 2 paths and 5 operations, exactly the five endpoints on the design slide.",
        topic="openapi", level=2,
        diagram="""
paths
 |- /books        get, post
 |- /books/{id}   get, put, delete
components
 |- schemas: Book
"""),
    mcq("Which of these is NOT something an OpenAPI document describes?",
        ["The SQL queries the server runs internally",
         "The paths and HTTP methods",
         "The request parameters and body schemas",
         "The possible responses and their status codes"], 0,
        "OpenAPI is the outside view.",
        "OpenAPI describes the contract: info, servers, paths, operations, parameters, request bodies, responses, reusable component schemas and security schemes. Implementation details stay hidden, which is the point of a contract.",
        topic="openapi", level=2),
    tf("OpenAPI documents can be written in YAML or JSON.", True,
       "FastAPI serves one at /openapi.json.",
       "Both are valid. Teams often hand-write YAML (easier to read and review) while frameworks such as FastAPI generate JSON. Tools accept either.",
       topic="openapi", level=2),
    mcq("From one OpenAPI file, which of these can tools produce?",
        ["Interactive docs, a mock server, client SDKs and server stubs, and contract tests",
         "Only a PDF manual",
         "A trained ML model",
         "The production database"], 0,
        "The slides: 'generate client code, create tests'.",
        "Swagger UI/ReDoc render docs, mock servers (e.g. Prism) return example responses, OpenAPI Generator writes clients and stubs in many languages, and contract-test tools check the real server against the spec.",
        topic="openapi", level=2),
    mcq("Put the bookstore lifecycle stages in the slides' order.",
        ["requirements -> design -> configure -> publish -> develop -> test -> deploy",
         "requirements -> develop -> design -> test -> publish -> configure -> deploy",
         "design -> requirements -> develop -> configure -> test -> deploy -> publish",
         "configure -> requirements -> design -> develop -> deploy -> test -> publish"], 0,
        "Design and its contract come before the code.",
        "Define what the API must do, design endpoints and the data model, configure the stack (FastAPI, Uvicorn, JSON storage), publish the docs, develop the handlers, test with pytest, then deploy.",
        topic="api-lifecycle", level=2,
        diagram="""
1 requirements -> 2 design -> 3 configure -> 4 publish
                                               |
        7 deploy <- 6 test <- 5 develop <------+
"""),
    mcq("In the bookstore design stage, which endpoint updates the book with ID 7?",
        ["PUT /books/7", "POST /books/7/update", "GET /books?update=7", "PUT /books"], 0,
        "The slides' list: GET /books, POST /books, GET /books/{id}, PUT /books/{id}, DELETE /books/{id}.",
        "Item-level operations use /books/{id}; PUT /books/7 replaces that book's data. PUT /books would mean replacing the whole collection.",
        topic="api-lifecycle", level=2),
    tf("In the bookstore data model, 'price' is declared as an integer; storing prices as whole units (e.g. paise) avoids floating-point rounding errors.", True,
       "0.1 + 0.2 in floating point.",
       "The slides' model has price: integer. Money APIs commonly store the smallest unit (₹499.00 = 49900 paise) or a decimal string, because binary floats cannot represent 0.1 exactly. A good habit for any payment or pricing API.",
       topic="api-lifecycle", level=2),
    mcq("A developer changes the bookstore API's response field 'author' to 'authorName'. Why does the course call this risky?",
        ["The API is a contract: existing clients read 'author' and will break, even though the server code still works",
         "JSON does not allow camelCase names",
         "It makes the server slower",
         "It is not risky: clients adapt automatically"], 0,
        "Who else depends on the field name?",
        "Clients you may not control (mobile apps, partners) are coded against the contract. Renaming a field is a breaking change; you add the new field alongside, deprecate the old one, or release a new major version (versioning is covered in the next subject).",
        topic="api-basics", level=2),
    out("""def call_chain(times_ms):
    return sum(times_ms)        # sync: wait for each in turn

def fan_out(times_ms):
    return max(times_ms)        # async/parallel: wait for slowest

t = [120, 80, 200]  # payment, restaurant, delivery services
print(call_chain(t), fan_out(t))""",
        ["400 200", "200 400", "400 400", "133 200"], 0,
        "One adds up, the other waits only for the slowest.",
        "Calling three services one after another costs 120 + 80 + 200 = 400 ms. If the calls are independent and issued in parallel (or handed to a broker), the caller waits only for the slowest, 200 ms. Long synchronous chains add their latencies.",
        topic="sync-async", level=2),
    # ------------------------------------------------------------------ L3
    out("""books = {7: "Godan", 8: "Gitanjali"}
def delete(book_id):
    if book_id in books:
        del books[book_id]
        return 204
    return 404

codes = [delete(7), delete(7), delete(7)]
print(codes, sorted(books))""",
        ["[204, 404, 404] [8]", "[204, 204, 204] [8]", "[204, 404, 404] [7, 8]", "[404, 404, 404] [8]"], 0,
        "Watch the server state, not just the codes.",
        "The first DELETE removes book 7 (204); the repeats find nothing (404). The codes differ, but the state after one call and after three calls is the same: only book 8 left. Idempotency is defined on server state, so DELETE is idempotent even though the replies change.",
        topic="http-methods", level=3),
    mcq("A Bengaluru food-delivery app sends POST /orders. The network drops before the reply arrives, the app retries, and the customer is charged twice. What is the standard fix?",
        ["The client sends a unique Idempotency-Key header per order attempt; the server stores the result for that key and returns the same result for any retry",
         "Switch the endpoint to GET so it becomes idempotent",
         "Never retry any request",
         "Return 500 on the second request"], 0,
        "Make the retry recognisable.",
        "POST is not idempotent, so a blind retry creates a second order. An idempotency key turns 'create' into 'create once': the server sees the same key, skips the work and replays the stored 201. GET must never change state, and refusing all retries loses orders on flaky mobile networks.",
        topic="http-methods", level=3,
        analogy="Like a cheque number: the bank honours cheque 000123 once, however many times it is presented."),
    out("""seen, orders = {}, []
def post_order(key, amount):
    if key in seen:
        return seen[key]
    orders.append(amount)
    seen[key] = (201, len(orders))
    return seen[key]

print(post_order("k-1", 450))
print(post_order("k-1", 450))   # retry after a timeout
print(post_order("k-2", 300))
print(len(orders))""",
        ["(201, 1)\n(201, 1)\n(201, 2)\n2", "(201, 1)\n(201, 2)\n(201, 3)\n3",
         "(201, 1)\n(409, 1)\n(201, 2)\n2", "(201, 1)\n(201, 1)\n(201, 2)\n3"], 0,
        "The retry reuses the key.",
        "The retry with key k-1 returns the stored (201, 1) without appending; the new key k-2 creates order 2. Two orders, not three. Replaying the same response (rather than 409) lets the client treat the retry exactly like the original success.",
        topic="http-methods", level=3),
    mcq("A client calls POST /books with {\"title\": \"Godan\", \"price\": \"abc\"}. The FastAPI bookstore declares price: int. Which status should come back, and which family is it in?",
        ["422 Unprocessable Content (FastAPI's validation error), a 4xx client error",
         "500 Internal Server Error, because the server could not save it",
         "200 OK with an error message in the body",
         "201 Created with price set to 0"], 0,
        "Whose mistake is it?",
        "Bad input is the client's fault, so it must be 4xx: FastAPI's Pydantic validation returns 422 with details of which field failed (many APIs use 400 for the same thing). 500 would tell clients 'our bug, retry later', and a retry would fail forever.",
        topic="status-codes", level=3),
    mcq("POST /books with an ISBN that already exists in the bookstore. Which status code best describes the problem?",
        ["409 Conflict", "404 Not Found", "201 Created", "503 Service Unavailable"], 0,
        "The request is well-formed but clashes with current state.",
        "409 Conflict means the request conflicts with the resource's current state, such as a uniqueness rule. 404 is for a missing resource, 201 would be a lie, 503 blames the server.",
        topic="status-codes", level=3),
    tf("Returning HTTP 200 with a body like {\"error\": \"book not found\"} is fine, because the client can read the error field.", False,
       "Who else looks at the status code?",
       "Caches, API gateways, monitoring dashboards, retry logic and generated clients all decide from the status code. A 200 'error' is cached as success, counted as success in your SLO and never raised as an exception in the client SDK. Use 404 (and put the details in the body).",
       topic="status-codes", level=3),
    mcq("The API gateway in front of a Pune smart-city service returns 504. What does that tell you?",
        ["The gateway did not get a reply from the upstream service in time: a gateway timeout, a server-side (5xx) problem",
         "The client's request was malformed",
         "The client must log in",
         "The resource was moved permanently"], 0,
        "Fifth hundred, and the word 'gateway'.",
        "502 Bad Gateway: the upstream replied with something invalid; 503 Service Unavailable: the service is down or overloaded; 504 Gateway Timeout: the upstream was too slow. All are 5xx, so the client did nothing wrong and may retry with backoff.",
        topic="status-codes", level=3,
        diagram="""
client -> [API gateway] -> upstream service
             |   waits 30 s ... no reply
             v
          504 Gateway Timeout
"""),
    out("""import hashlib, json

body = json.dumps({"id": 7, "title": "Godan"})
etag = hashlib.md5(body.encode()).hexdigest()[:8]

def get_book(if_none_match=None):
    return (304, "") if if_none_match == etag else (200, body)

status1, _ = get_book()
status2, b = get_book(if_none_match=etag)
print(status1, status2, len(b))""",
        ["200 304 0", "200 200 30", "304 304 0", "200 304 30"], 0,
        "The second call sends back the tag it already has.",
        "The first GET returns 200 with the body and its ETag. The client caches both and next time sends If-None-Match: <etag>; if nothing changed, the server answers 304 Not Modified with an empty body. This is REST's 'cacheable' constraint saving bandwidth on mobile data.",
        topic="rest-architecture", level=3,
        analogy="Like asking the restaurant 'has the menu changed since version 7?' instead of reprinting the whole menu every visit."),
    mcq("An agritech cooperative's API runs a 'retrain the crop-yield model' job that takes 20 minutes. What is a good API design?",
        ["POST /training-jobs returns 202 Accepted with a job URL; the client polls GET /training-jobs/{id} or receives a webhook when it finishes",
         "Keep the POST connection open for 20 minutes and return 200 at the end",
         "Return 500 until the job is done",
         "Make the client call the endpoint every second with POST"], 0,
        "Do not hold an HTTP connection hostage.",
        "Long work should be asynchronous: accept it (202), give the client a status resource, and notify via polling or a webhook. A 20-minute synchronous request will be cut by load balancer and gateway timeouts (often 30-60 s) and a retried POST starts a second job.",
        topic="sync-async", level=3),
    out("""services = {"order": 0.999, "payment": 0.999,
            "restaurant": 0.999, "delivery": 0.999}
p = 1.0
for a in services.values():
    p *= a
minutes_per_month = 30 * 24 * 60
print(round(p, 4), round((1 - p) * minutes_per_month))""",
        ["0.996 173", "0.999 43", "0.996 43", "0.9996 17"], 0,
        "A synchronous chain is up only when every link is up.",
        "With synchronous REST, a request succeeds only if all four services are up: 0.999^4 ≈ 0.996, about 173 minutes of failed requests a month instead of 43 for one service. This is the slides' 'reduced availability' drawback; a broker lets the order service accept orders while payment is briefly down.",
        topic="rest-design", level=3),
    out("""import re
routes = {("GET", r"/books"): "list", ("POST", r"/books"): "create",
          ("GET", r"/books/(\\d+)"): "read", ("DELETE", r"/books/(\\d+)"): "delete"}

def dispatch(method, path):
    matched = {m: name for (m, pat), name in routes.items()
               if re.fullmatch(pat, path)}
    if not matched:
        return 404
    return matched.get(method, 405)

print(dispatch("GET", "/books/12"), dispatch("PUT", "/books/12"), dispatch("GET", "/authors"))""",
        ["read 405 404", "read 404 404", "read 405 405", "404 405 404"], 0,
        "A path that exists with the wrong method is a different error from a path that does not exist.",
        "/books/12 matches the item pattern, so GET dispatches to 'read'. PUT is not registered for that path, so the router answers 405 Method Not Allowed. /authors matches no route: 404. Frameworks like FastAPI make exactly this distinction.",
        topic="http-components", level=3),
    mcq("Spot the flaw in this bookstore API: `GET /deleteBook?id=3` deletes the book and returns 200.",
        ["A state-changing action on GET breaks the safe-method rule, and the verb belongs in the method: use DELETE /books/3 returning 204",
         "Nothing; any method can delete",
         "Only the status code is wrong: it should be 201",
         "The ID should be in a header"], 0,
        "What happens when a browser prefetches or a crawler follows the link?",
        "Browsers, caches and crawlers assume GET is safe and may call it without the user meaning to, so books vanish. REST puts the action in the method and the resource in the path: DELETE /books/3, 204 No Content.",
        topic="rest-design", level=3),
    mcq("The bookstore API runs as three replicas behind a load balancer. A developer keeps each user's shopping cart in a Python dict inside the server process. What goes wrong, and which REST constraint was broken?",
        ["Requests from one user land on different replicas, so the cart appears and disappears; it breaks statelessness (keep the cart in a shared store or send it with the request)",
         "Nothing; dicts are fast",
         "It breaks the uniform interface, because dicts are not JSON",
         "It breaks the layered-system constraint because there are three servers"], 0,
        "Which replica remembers the cart?",
        "In-process session state ties a user to one machine. Stateless servers keep no client session: the client sends a token, and resource state lives in a database or cache every replica can read. That is what makes horizontal scaling and restarts painless.",
        topic="rest-architecture", level=3,
        diagram="""
user --req1--> LB --> replica A  {cart: [book7]}
user --req2--> LB --> replica B  {cart: []}  <- empty?
"""),
    mcq("A Bengaluru startup's mobile team and backend team must start work on the same day on a new ordering API. Which approach lets both progress in parallel?",
        ["Design-first: agree an OpenAPI spec, run a mock server from it for the mobile team, and generate server stubs for the backend",
         "Code-first: the backend finishes the API, then the mobile team starts",
         "Skip the spec and share Postman screenshots",
         "Let each team define its own JSON format"], 0,
        "What can the mobile team call before the backend exists?",
        "With the contract written first, a mock server returns the spec's example responses, so the app can be built and tested against it; the backend implements the same spec, and contract tests check it. Code-first (as FastAPI does by default) works when one team owns both sides.",
        topic="openapi", level=3,
        analogy="Like agreeing the building plan before the electrician and the plumber start work in parallel."),
    tf("FastAPI is a code-first tool: it generates the OpenAPI document from your Python route functions and Pydantic models.", True,
       "Where does /openapi.json come from?",
       "FastAPI inspects the decorators, type hints and models and builds the spec at runtime. Design-first is the reverse: write the spec, then generate or write code to match. Both end with a spec; they differ in which is the source of truth.",
       topic="openapi", level=3),
    out("""import math
total_restaurants, limit = 1043, 50

pages = math.ceil(total_restaurants / limit)
last_offset = (pages - 1) * limit
print(pages, last_offset, total_restaurants - last_offset)""",
        ["21 1000 43", "20 1000 43", "21 1050 -7", "20 950 93"], 0,
        "Round the page count up.",
        "GET /restaurants?limit=50&offset=... needs ceil(1043/50) = 21 pages; the last starts at offset 1000 and holds 43 items. Paging through query parameters keeps responses small; returning all 1,043 in one response would be slow on mobile data.",
        topic="rest-design", level=3,
        diagram="""
offset  0     50    100  ...  950   1000
       [50]  [50]  [50] ...  [50]  [43]
        page 1 ............... page 21
"""),
    mcq("A client sends POST /books with Content-Type: text/plain and a CSV line in the body. The API only accepts JSON. Which response is most precise?",
        ["415 Unsupported Media Type", "406 Not Acceptable", "404 Not Found", "500 Internal Server Error"], 0,
        "It is about what the client sent, not what it asked for.",
        "415 says 'I cannot read the body format you sent' (Content-Type). 406 says 'I cannot produce the format you asked for' (Accept). Both are 4xx client errors.",
        topic="status-codes", level=3),
    fill("When POST /books returns 201 Created, the response header that gives the URL of the new book (e.g. /books/42) is the ____ header.", "Location",
         "It tells the client where the new resource lives.",
         "201 + Location: /books/42 lets the client fetch or update the new resource without guessing its ID. 3xx redirects use the same header.",
         topic="http-components", level=3),
    mcq("In the bookstore 'test' stage, which pytest assertion best checks the not-found case for GET /books/999?",
        ["assert response.status_code == 404",
         "assert response.status_code != 200",
         "assert 'error' in response.text",
         "assert response.json() == []"], 0,
        "A test should pin the contract exactly.",
        "Asserting the exact code catches regressions such as returning 500 (which != 200 would let through). FastAPI's TestClient calls the app in-process, so these tests need no running server or network.",
        topic="api-lifecycle", level=3),
    mcq("The bookstore stores books in a JSON file (the slides' 'configure' step). The app is then deployed on two cloud instances. What is the main risk?",
        ["Each instance has its own file, so writes on one are invisible to the other and concurrent writes can corrupt it; production needs a shared database",
         "JSON cannot store prices",
         "Uvicorn cannot read files",
         "There is no risk; JSON files are a database"], 0,
        "Two machines, two disks.",
        "A local JSON file is fine for a classroom demo but it is per-instance state. Move to a managed database (or at least one shared store) before scaling out. The 'deploy' stage is where these configure-time shortcuts bite.",
        topic="api-lifecycle", level=3),
    # ------------------------------------------------------------------ L4
    out("""IDEMPOTENT = {"GET", "PUT", "DELETE", "HEAD"}

def should_retry(method, status, has_key=False):
    if status < 500:
        return False
    return method in IDEMPOTENT or has_key

calls = [("GET", 503), ("POST", 504), ("POST", 504, True),
         ("PUT", 400), ("DELETE", 502)]
print([should_retry(*c) for c in calls])""",
        ["[True, False, True, False, True]", "[True, True, True, False, True]",
         "[True, False, False, False, True]", "[True, False, True, True, True]"], 0,
        "Two conditions: the failure must be the server's, and repeating must be harmless.",
        "Retry only 5xx (a 4xx will fail again identically) and only when a repeat cannot duplicate work: idempotent methods, or a POST carrying an Idempotency-Key. The bare POST after a 504 is not retried, because the order may already have been created upstream.",
        topic="http-methods", level=4),
    mcq("A client sends PUT /books/7 with only {\"price\": 399}, intending to change just the price. What happens on a server that follows HTTP semantics?",
        ["PUT replaces the whole resource, so title, author and ISBN are lost or rejected as missing; a partial change should be PATCH",
         "Only the price changes, because PUT merges fields",
         "The server must return 201",
         "PUT is not allowed on item URIs"], 0,
        "Replace vs modify.",
        "PUT means 'store this representation at this URI'. Sending part of it either wipes the other fields or fails validation. PATCH applies a partial update. The slides describe PUT as 'update existing data', which hides this replace semantics.",
        topic="http-methods", level=4),
    out("""stock = {"book7": 10}
def put(qty):          # PUT /stock/book7  {"qty": qty}
    stock["book7"] = qty
def patch_inc(n):      # PATCH /stock/book7 {"op": "inc", "by": n}
    stock["book7"] += n

put(12); put(12)
a = stock["book7"]
patch_inc(1); patch_inc(1)   # client retried once
print(a, stock["book7"])""",
        ["12 14", "12 13", "24 26", "12 12"], 0,
        "Set vs add.",
        "Two identical PUTs set 12 twice: still 12. Two identical 'increment by 1' PATCHes add 2, so the retry changed state: 14, not the intended 13. PATCH is idempotent only if the patch document is (e.g. 'set price'). That is why HTTP does not guarantee PATCH idempotency.",
        topic="http-methods", level=4),
    mcq("An API has resource URIs, uses GET/POST/PUT/DELETE and proper status codes, but responses contain no links to related actions. Where is it on the Richardson maturity model?",
        ["Level 2 (HTTP verbs); Level 3 adds hypermedia controls (HATEOAS)",
         "Level 0 (one endpoint, RPC over HTTP)",
         "Level 1 (resources only)",
         "Level 3, because it uses status codes"], 0,
        "Levels: 0 swamp of POX, 1 resources, 2 verbs, 3 hypermedia.",
        "Most 'REST' APIs in practice are Level 2. Level 3 responses include links such as {\"_links\": {\"cancel\": \"/orders/9/cancel\"}} so clients discover the next valid actions instead of hard-coding URLs. Fielding argues only Level 3 is truly REST.",
        topic="rest-architecture", level=4,
        diagram="""
L3  hypermedia (links in responses)
L2  HTTP verbs + status codes      <- most APIs
L1  resources (/orders/9)
L0  one endpoint, POST everything
"""),
    mcq("A payment gateway delivers webhooks to your food-delivery backend and retries any delivery that does not get a 2xx within 10 s. Your handler updates the order, emails the customer and calls the restaurant API, which takes 40 s. What happens, and what is the fix?",
        ["Every delivery times out and is retried, so customers get several emails; reply 2xx at once after storing the event, process it from a queue, and skip event IDs already handled",
         "Nothing; the gateway waits as long as needed",
         "Return 500 so the gateway stops retrying",
         "Switch the webhook to GET"], 0,
        "At-least-once delivery plus a slow handler.",
        "Webhook providers deliver at least once and retry on timeout. Acknowledge fast, do the slow work asynchronously and make processing idempotent by event ID. A 500 causes more retries, not fewer.",
        topic="sync-async", level=4),
    out("""deliveries = ["evt_1", "evt_2", "evt_1", "evt_3", "evt_2", "evt_1"]
done, emails = set(), 0
for event_id in deliveries:
    if event_id in done:
        continue
    done.add(event_id)
    emails += 1
print(emails, len(deliveries) - emails)""",
        ["3 3", "6 0", "3 0", "4 2"], 0,
        "Count distinct IDs.",
        "Six deliveries carry three distinct events, so three emails go out and three redeliveries are skipped. Deduplicating on the provider's event ID is the standard way to make an at-least-once webhook effectively exactly-once for your side effects.",
        topic="sync-async", level=4,
        diagram="""
gateway --evt_1--> you   (slow, times out)
gateway --evt_1--> you   (retry: already done, skip)
gateway --evt_2--> you   (new: process)
"""),
    out("""old = {"required": {"title", "author"}, "response": {"id", "title", "author"}}
new = {"required": {"title", "author", "isbn"},
       "response": {"id", "title", "author", "price"}}

breaking = []
if new["required"] - old["required"]:
    breaking.append("new required request field")
if old["response"] - new["response"]:
    breaking.append("response field removed")
print(breaking or "safe")""",
        ["['new required request field']", "safe",
         "['new required request field', 'response field removed']",
         "['response field removed']"], 0,
        "Adding to a response is fine; demanding more from clients is not.",
        "Old clients do not send isbn, so making it required breaks them (the slides list 'adding a new required field' as breaking). Adding price to the response is additive: tolerant clients ignore unknown fields. Spec-diff tools in CI run exactly this comparison on two OpenAPI files.",
        topic="openapi", level=4),
    mcq("Six months after launch, the bookstore's hand-written OpenAPI file says GET /books/{id} returns 'publishedDate', but the code now returns 'published_on'. Partners generated clients from the file. What is the root problem and the durable fix?",
        ["Spec drift: the spec and the code are two sources of truth; make one authoritative (generate the spec from code, or test the server against the spec in CI)",
         "Partners should stop using generated clients",
         "OpenAPI does not support dates",
         "Delete the spec; code is the documentation"], 0,
        "Two documents, nobody keeping them in sync.",
        "A spec nobody checks drifts. Code-first frameworks (FastAPI) regenerate it on each build; design-first teams run contract tests that fail the pipeline when the server does not match. Either way, the contract partners depend on stays true.",
        topic="openapi", level=4,
        diagram="""
openapi.yaml: publishedDate -> partner SDK expects it
server code:  published_on  -> real JSON
          mismatch = broken partner apps
"""),
    tf("A 401 Unauthorized response should include a WWW-Authenticate header telling the client how to authenticate, while a 403 does not need one.", True,
       "401 invites the client to try again with credentials.",
       "By the HTTP standard, 401 means 'authenticate and retry' and must carry WWW-Authenticate (e.g. Bearer). 403 means credentials would not help: the identity is known and not permitted.",
       topic="status-codes", level=4),
    mcq("A shared CDN sits in front of GET /me/orders, which returns the logged-in user's orders. Which response header prevents one user's orders from being served to another?",
        ["Cache-Control: private (or no-store), so shared caches do not store it",
         "Cache-Control: public, max-age=3600",
         "Content-Type: application/json",
         "Location: /me/orders"], 0,
        "Cacheable is a constraint, but whose cache?",
        "REST responses should label their cacheability. Per-user data must be private (browser cache only) or no-store. 'public' lets the CDN hand user A's orders to user B, a real-world data-leak pattern.",
        topic="rest-architecture", level=4),
    out("""calls, free = 150_000, 10_000
rate_per_1000 = 420          # ₹ per 1,000 billable calls

def bill(n):
    return max(0, n - free) / 1000 * rate_per_1000

cache_hit = 0.60             # cache geocodes of repeat addresses
print(round(bill(calls)), round(bill(calls * (1 - cache_hit))))""",
        ["58800 21000", "63000 25200", "58800 35280", "60200 24080"], 0,
        "Subtract the free tier first, then price per thousand.",
        "Without a cache: (150,000 - 10,000)/1,000 × ₹420 = ₹58,800. Caching 60% leaves 60,000 calls: 50 × ₹420 = ₹21,000. A paid API such as Google Maps is part of your cost model, and the free tier makes savings larger than the hit rate alone suggests (64%, not 60%).",
        topic="api-basics", level=4),
    mcq("A partner app parsed GET /books and relied on the books always coming back sorted by ID, though the docs never promised an order. You switch to sorting by title and the partner breaks. What lesson does this illustrate?",
        ["With enough clients, any observable behaviour becomes part of the de facto contract (Hyrum's law); document guarantees explicitly and treat changes to observable behaviour carefully",
         "The partner is wrong, so nothing needs to change in how you release",
         "JSON arrays have no order",
         "Sorting must always be done on the client"], 0,
        "The written contract and the observed contract differ.",
        "Clients code against what they see, not only what you wrote. Make the order explicit (?sort=id, a default stated in the OpenAPI spec) and announce behaviour changes like any other contract change. 'Not in the docs' does not stop the outage.",
        topic="api-basics", level=4,
        analogy="Like a colleague relying on a private helper function in your module: you never exported it, but renaming it still breaks their build."),
    out("""order, payment, broker = 0.999, 0.999, 0.9999

sync_ok = order * payment        # order waits on payment over REST
async_ok = order * broker        # order only needs the broker to accept
print(round(sync_ok, 6), round(async_ok, 6))""",
        ["0.998001 0.9989", "0.999 0.9999", "0.998001 0.998001", "0.9989 0.998001"], 0,
        "Multiply the parts that must be up at the moment of the request.",
        "Synchronously, accepting an order needs order and payment up: 0.998001. With a broker, order only needs itself and the broker: 0.999 × 0.9999 = 0.9989001 ≈ 0.9989; payment processes the message when it recovers. Async moves the dependency off the critical path, at the price of the customer seeing 'payment pending'.",
        topic="sync-async", level=4),
    mcq("Design review for a Pune smart-city app: (a) a citizen asks for the current parking fee at a lot, (b) the system sends a 'challan issued' SMS to 2 lakh vehicle owners. Which split is right?",
        ["(a) synchronous REST, because the user is waiting for one fast answer; (b) asynchronous through a queue, because it is slow, bulky and must survive failures",
         "Both synchronous REST",
         "Both asynchronous through a queue",
         "(a) asynchronous, (b) synchronous"], 0,
        "Who is waiting, and how long is the work?",
        "Use sync for short request-response interactions a user is waiting on. Use a queue for fan-out and long work: workers drain it at their own rate, failed sends retry, and the API that triggered it returns quickly (202). Holding one HTTP call open for 2 lakh SMS would time out.",
        topic="sync-async", level=4,
        diagram="""
(a) app --GET /lots/12/fee--> API --200 {fee: 40}--> app
(b) API --202--> admin
     +--> [queue: 200,000 SMS jobs] --> workers --> SMS
"""),
    fill("A server that has accepted a request for processing but has not finished it (e.g. a queued report job) returns status ____ Accepted.", "202",
         "2xx, but the work is not done yet.",
         "202 Accepted says 'received, will process later', usually with a Location or status URL to poll. 200/201 claim the work is done; 202 is honest for asynchronous jobs.",
         topic="status-codes", level=4),
    mcq("For the bookstore's 'test' and 'deploy' stages, which pipeline order gives the strongest guarantee that partners are not broken by a release?",
        ["Unit tests -> contract tests against the OpenAPI spec -> deploy to staging -> smoke tests on /docs and key endpoints -> production",
         "Deploy to production -> run pytest there",
         "Run tests only when a partner complains",
         "Deploy -> regenerate the spec -> publish"], 0,
        "Fail before the users see it.",
        "The slides list pytest/unittest for testing and Heroku/AWS/Google Cloud for deployment; in practice CI runs the tests and a spec-conformance check before anything ships, then smoke-tests the deployed instance. Testing in production after deploy finds bugs through your partners.",
        topic="api-lifecycle", level=4),
    out("""posts = 20
latency_ms = 80

rest_calls = 1 + 1 + posts        # profile, posts, comments per post
print(rest_calls, rest_calls * latency_ms)""",
        ["22 1760", "3 240", "21 1680", "22 240"], 0,
        "Comments are per post.",
        "One call for the profile, one for the posts, then one comments call per post: 22 requests, 1,760 ms if made one after another on an 80 ms mobile round trip. The slides show three calls for one post; with many posts this is the N+1 pattern that pushes teams to GraphQL or to a combined endpoint.",
        topic="rest-design", level=3),
    tf("Sending an API key as a query parameter (?key=abc) is as safe as sending it in a header, because HTTPS encrypts both.", False,
       "Where do full URLs get written down?",
       "HTTPS protects both in transit, but URLs are logged by servers, proxies and analytics and kept in browser history, so keys in URLs leak. Put credentials in the Authorization header.",
       topic="http-components", level=3),
    fill("A DELETE that succeeds and has nothing to send back usually returns status ____ No Content.", "204",
         "Success, empty body.",
         "204 tells the client the action worked and there is no body to parse. Returning 200 with an empty body also works but is less precise.",
         topic="status-codes", level=2),
    fill("The 3xx family of status codes (301, 302, 304) is called ____.", "redirection",
         "The client must go elsewhere or use what it has.",
         "3xx codes tell the client to look elsewhere (301 moved permanently, 302 found) or to use its cached copy (304 Not Modified).",
         topic="status-codes", level=2),
    tf("Because REST is a synchronous API style, a REST server can handle only one client's request at a time.", False,
       "Synchronous describes the caller, not the server.",
       "'Synchronous' means each caller waits for the reply to its own call. The server still serves many callers at once with threads, processes or an event loop (Uvicorn workers, for example). The slide wording 'each request must wait for the previous one' describes one client's sequence, not a one-at-a-time server.",
       topic="sync-async", level=2),
    tf("Swagger UI and the OpenAPI Specification are the same thing.", False,
       "One is a document format, the other renders it.",
       "The OpenAPI Specification is the standard for describing an API. Swagger UI is a tool that reads an OpenAPI document and renders interactive docs (what FastAPI shows at /docs). Swagger Editor, Prism and OpenAPI Generator are other tools built on the same spec.",
       topic="openapi", level=2),
]
