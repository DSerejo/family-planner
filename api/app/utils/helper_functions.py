from fastapi import HTTPException, Header, Depends
import os
import uuid
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.session import Session as SessionModel

def validate_api_key(authorization : str | None =  Header(None)):
    if authorization != f"Bearer {os.getenv('API_KEY')}":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True

def extract_token(authorization : str | None =  Header(None)):
    return authorization.split(" ")[1] if authorization else None

def validate_session(db: Session = Depends(get_db), token: str = Depends(extract_token)):
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    session = db.query(SessionModel).filter(SessionModel.id == token).first()
    if not session:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return session

def generate_unique_id(length: int = 36):
    return str(uuid.uuid4())[:length]