from pydantic import BaseModel, EmailStr
from typing import List, Optional

class FamilyMemberCreate(BaseModel):
    family_id: str
    user_id: Optional[str] = None
    email: Optional[EmailStr] = None
    name: Optional[str] = None