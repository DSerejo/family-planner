from pydantic import BaseModel, EmailStr
from typing import List, Optional

class FamilyCreateBody(BaseModel):
    name: str

class FamilyCreate(BaseModel):
    name: str
    owner_id: str

class FamilyUpdate(BaseModel):
    name: str
class FamilyMemberAdd(BaseModel):
    email: EmailStr
    name: str

class FamilyInvite(BaseModel):
    email: EmailStr

class FamilyInviteResponse(BaseModel):
    success: bool
    message: str

class FamilyFilter(BaseModel):
    id: Optional[str] = None