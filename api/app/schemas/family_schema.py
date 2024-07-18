from pydantic import BaseModel, EmailStr
from typing import List, Optional

class FamilyCreate(BaseModel):
    name: str

class FamilyMemberAdd(BaseModel):
    email: EmailStr
    name: str

class FamilyInvite(BaseModel):
    email: EmailStr

class FamilyInviteResponse(BaseModel):
    success: bool
    message: str
