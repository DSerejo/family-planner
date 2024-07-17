from fastapi import APIRouter, HTTPException, Depends
from app.utils.helper_functions import validate_api_key
from app.schemas.user_schema import UserCreate
from app.services.user_service import create_user, get_user_by_email
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/auth/google")
def google_login(
    body: UserCreate, 
    a: str = Depends(validate_api_key), 
    db: Session = Depends(get_db)
):
    try:
        user = get_user_by_email(db,body.email)
        if not user:
            user = create_user(db, body)
        return {"success": True, "user": user}
    except ValueError as e:
        print(e)
        raise HTTPException(status_code=400, detail="Invalid token")