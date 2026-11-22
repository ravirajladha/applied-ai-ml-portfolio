"""Code-first GraphQL bookstore: Python types -> GraphQL schema."""
import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter


# 1. Define the data types in Python, rather than writing a schema first.
@strawberry.type
class Author:
    id: int
    name: str


@strawberry.type
class Book:
    id: int
    title: str
    price: float  # INR; float is sufficient for this read-only classroom demo.
    in_stock: bool
    author: Author  # Nested GraphQL object.


# 2. Add fictional sample data. No database or API key is required.
authors = [
    Author(id=1, name="Anita Rao"),
    Author(id=2, name="Arun Kumar"),
]
catalog = [
    Book(id=1, title="Python for Beginners", price=499,
         in_stock=True, author=authors[0]),
    Book(id=2, title="Cloud Native Basics", price=699,
         in_stock=True, author=authors[1]),
    Book(id=3, title="Learning GraphQL", price=399,
         in_stock=False, author=authors[0]),
]


# 3. Resolvers provide the data for the fields on the root Query type.
@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Welcome to the GraphQL Bookstore!"

    @strawberry.field
    def books(self, search: str | None = None,
              in_stock: bool | None = None) -> list[Book]:
        result = catalog
        if search is not None:
            result = [b for b in result if search.casefold() in b.title.casefold()]
        if in_stock is not None:
            result = [b for b in result if b.in_stock == in_stock]
        return result

    @strawberry.field
    def book(self, id: int) -> Book | None:
        # Nullable return: a missing book gives {"data":{"book":null}}.
        return next((b for b in catalog if b.id == id), None)


# 4. Strawberry generates the schema from the Python classes and type hints.
schema = strawberry.Schema(query=Query)

# 5. FastAPI exposes the GraphQL HTTP endpoint and the GraphiQL explorer.
app = FastAPI(title="Strawberry Bookstore Demo")
app.include_router(GraphQLRouter(schema, graphql_ide="graphiql"), prefix="/graphql")


@app.get("/")
def home():
    return {"message": "Open /graphql for the GraphiQL query explorer"}


if __name__ == "__main__":
    # Run python main.py to print the generated schema without starting a server.
    print(schema.as_str())
