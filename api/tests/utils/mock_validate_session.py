from app.models.session import Session
from fastapi import HTTPException, Header

def mock_validate_session(authorization: str | None = Header(None)):
    if authorization != f"Bearer valid_token":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return Session(id="valid_token", user_id="mock_user_id")