from fastapi import APIRouter, HTTPException, Depends
from app.utils.helper_functions import validate_api_key
from app.schemas.user_schema import UserCreate
from app.services.user_service import UserService, create_user_service
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/user")
def create_user_with_google(
    body: UserCreate, 
    db: Session = Depends(get_db),
    service: UserService = Depends(create_user_service),
    validate_api_key: bool = Depends(validate_api_key)
):
    try:
        user = service.get_user_by_email(body.email)
        if not user:
            user = service.create_user(body)
        return {"success": True, "user": user}
    except ValueError as e:
        print(e)
        raise HTTPException(status_code=400, detail="Invalid token")