# Strawberry GraphQL Bookstore: Code-first Python Demo

Python 3.10+ required; tested with Python 3.12. No database, API key or paid service.
Data is fictional and read-only. Queries demonstrate field selection, nested
objects, arguments, variables, aliases and errors. No mutations are implemented.

## Windows Command Prompt
Extract the archive and open a terminal in the folder containing main.py.
```
py -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8001
```
PowerShell activation: `.\.venv\Scripts\Activate.ps1`. If activation is blocked,
use `.\.venv\Scripts\python.exe` instead of `python` for pip and uvicorn commands.
No execution policy change is necessary.

## macOS/Linux
```
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8001
```

Open http://127.0.0.1:8001/graphql for GraphiQL. Paste one operation at a time from
queries.graphql, then press the Run/play button. Keep the server terminal open;
Ctrl+C stops it. Port 8001 allows the earlier REST demo to stay on port 8000.
GraphiQL may need internet access to load its browser assets; query execution is local.

## Code-first sequence
1. Define Author and Book using Python annotations and @strawberry.type.
2. Define fields/resolvers on Query using @strawberry.field.
3. Build strawberry.Schema(query=Query). Strawberry derives the schema from code.
4. Mount GraphQLRouter at /graphql to accept HTTP requests.
5. Run a GraphQL operation; the resolvers return data and GraphQL selects fields.
6. Print the generated schema with `python main.py`. See schema.graphql for a copy.

Python snake_case becomes camelCase by default: in_stock becomes inStock.
A GraphQL object field needs a selection set, e.g. books { title }.
These in-memory synchronous resolvers do no blocking I/O; production resolvers
must handle database/network calls appropriately.

## Teaching sequence (about one minute per query)
1. `{ hello }`: establish that the API is running.
2. `{ books { title } }`: ask students to predict the response fields.
3. `{ books { title price inStock } }`: more fields, same HTTP endpoint.
4. `{ books { title author { name } } }`: nested objects in one operation.
5. `{ book(id:1) { title } }`: choose one record using an argument.
6. `{ books(search:"python", inStock:true) { title } }`: filter the collection.
7. Variables: paste the FindBook operation below and put {"bookId":2} in Variables.
8. Aliases: compare two books in one operation (see queries.graphql).
9. Missing ID: nullable book field returns null; it is not a REST 404 in this demo.
10. Invalid field: books { rating } fails validation before the resolver runs.

Variable operation:
```graphql
query FindBook($bookId: Int!) {
  book(id: $bookId) { title price }
}
```
Variables (separate panel):
```json
{"bookId":2}
```

## Fiddler Composer
Method POST, URL http://127.0.0.1:8001/graphql
Header: Content-Type: application/json
Body:
```json
{"query":"query FindBook($bookId: Int!) { book(id: $bookId) { title price author { name } } }","variables":{"bookId":1}}
```
Expected:
```json
{"data":{"book":{"title":"Python for Beginners","price":499.0,"author":{"name":"Anita Rao"}}}}
```
GraphQL is the query language; HTTP POST is the transport method here.
Inspect the JSON errors array as well as the HTTP status: GraphQL execution
errors may coexist with HTTP 200; request validation status can depend on media
negotiation and server implementation. Do not assume every GraphQL error is 404.
The request is not SQL and clients can select only fields exposed in the schema.
Field selection shapes the response; it does not automatically optimize database I/O.

## Test
```
python -m pip install -r requirements-test.txt
python test_demo.py
```
The invalid-field test intentionally logs a GraphQL validation error.
Other checks verify selection, nesting, variables, aliases, filters, nullable
missing results, explorer HTML and the generated schema.

## Student exercise
Add `category: str` to Book and supply a category for each sample book. Restart
and query books { title category }. Inspect the schema to see the new field.

Official references:
https://strawberry.rocks/docs
https://strawberry.rocks/docs/integrations/fastapi
