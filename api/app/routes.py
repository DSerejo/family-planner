from app.controllers.user_controller import router as user_router
from fastapi import FastAPI

def setRoutes(app: FastAPI):
    app.include_router(user_router)