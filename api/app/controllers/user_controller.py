from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from app.utils.helper_functions import validate_api_key
# from sqlalchemy.orm import Session
# from app.database import get_db
# from app.models.user import User
# from app.schemas.user_schema import UserCreate
# from app.services.user_service import create_user, get_user_by_email
import os

router = APIRouter()

class Body(BaseModel):
    email: str



@router.post("/auth/google")
def google_login(body: Body, a: str = Depends(validate_api_key)):
    try:
        
        return {"success": True, "user": body.email}
    except ValueError as e:
        print(e)
        raise HTTPException(status_code=400, detail="Invalid token")