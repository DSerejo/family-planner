from fastapi import FastAPI
from .context_middleware import add_context

def add_middlewares(app: FastAPI):
    add_context(app)