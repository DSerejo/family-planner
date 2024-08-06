from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .routes import setRoutes
from strawberry.asgi import GraphQL
from .graphql import schema
from .middlewares import add_middlewares
from .database import get_db
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

add_middlewares(app)
setRoutes(app)

@app.get("/")
def read_root():
    return {"Hello": "World"}

app.mount("/graphql", GraphQL(schema=schema))

