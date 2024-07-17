from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    name: str

class User(BaseModel):
    id: str
    email: str
    name: str