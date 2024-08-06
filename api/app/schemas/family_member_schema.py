from pydantic import BaseModel, EmailStr
from typing import List, Optional


class FamilyMemberCreateBody(BaseModel):
    user_id: Optional[str] = None
    email: Optional[EmailStr] = None
    name: Optional[str] = None

class FamilyMemberCreate(FamilyMemberCreateBody):
    family_id: str
    invited_by_user_id: Optional[str] = None
    accepted: bool = False