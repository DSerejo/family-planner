from fastapi import HTTPException, Header, Depends
from app.services.session_service import SessionService, create_session_service

import os

def validate_session(authorization: str | None = Header(None), 
                     sessionService: SessionService = Depends(create_session_service)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = authorization.split(" ")[1]
    session = sessionService.get_session_by_token(token)
    if session is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return session