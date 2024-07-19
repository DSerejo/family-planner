from pydantic import BaseModel
from datetime import datetime

class GoogleSession(BaseModel):
    email: str
    name: str

class ApiSession(BaseModel):
    token: str