from app.controllers.user_controller import router as user_router
from app.controllers.family_controller import router as family_router
from app.controllers.session_controller import router as session_router
from fastapi import FastAPI

def setRoutes(app: FastAPI):
    app.include_router(user_router)
    app.include_router(family_router)
    app.include_router(session_router)