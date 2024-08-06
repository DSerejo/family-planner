from fastapi import FastAPI, Request, Depends
from typing import Annotated
from app.services.context_service import ContextService, set_context
from sqlalchemy.orm import Session
from app.database import get_db
from starlette.middleware.base import BaseHTTPMiddleware

class ContextMiddleware:
    def __init__(self, app: FastAPI, db: Session = Depends(get_db)):
        self.app = app
        self.db = next(db.dependency())

    async def __call__(self, request: Request, call_next):
        context = ContextService(request, self.db)
        set_context(context)
        request.state.context = context
        response = await call_next(request)
        return response

def add_context(app: FastAPI):
    my_middleware = ContextMiddleware(app)
    app.add_middleware(BaseHTTPMiddleware, dispatch=my_middleware)