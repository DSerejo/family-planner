from fastapi import APIRouter, HTTPException, Depends
from app.schemas.session_schema import GoogleSession, ApiSession
from app.services.user_service import create_user_service, UserService
from app.schemas.user_schema import UserCreate
from app.services.session_service import create_session_service, SessionService
from app.database import get_db
from sqlalchemy.orm import Session
from app.utils.helper_functions import validate_api_key

router = APIRouter()


@router.post("/session")
def create_session(googleSession: GoogleSession,
                    db: Session = Depends(get_db), 
                    validate_api_key: bool = Depends(validate_api_key), 
                    userService: UserService = Depends(create_user_service),
                    sessionService: SessionService = Depends(create_session_service)):
    user = userService.get_user_by_email(googleSession.email)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    session = sessionService.create_session(user.id)
    return ApiSession(token=session.id)

@router.get("/session/{token}")
def validate_session(token: str, db: Session = Depends(get_db),
                     sessionService: SessionService = Depends(create_session_service)):
    session = sessionService.get_session_by_token(token)
    if not session:
        raise HTTPException(status_code=401, detail="Invalid session")
    return ApiSession(token=session.id)

@router.get("/session/{token}/signout")
def delete_session(token: str, db: Session = Depends(get_db),
                    sessionService: SessionService = Depends(create_session_service)):
    sessionService.delete_session(token)
    return {"message": "Signed out"}