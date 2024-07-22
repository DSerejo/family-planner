from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import setRoutes
from strawberry.asgi import GraphQL
from .graphql import schema

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

setRoutes(app)

@app.get("/")
def read_root():
    return {"Hello": "World"}

app.mount("/graphql", GraphQL(schema=schema))

