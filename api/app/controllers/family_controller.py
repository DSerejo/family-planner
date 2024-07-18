from fastapi import APIRouter, HTTPException, Depends
from app.utils.helper_functions import validate_api_key
from app.schemas.family_schema import FamilyCreate, FamilyMemberAdd
from app.services.family_service import get_family_by_id, create_family 
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/family/{family_id}")
def get_family(family_id: int, db: Session = Depends(get_db)):
    family = get_family_by_id(db, family_id)
    if not family:
        raise HTTPException(status_code=404, detail="Family not found")
    return family

@router.post("/family")
def create_family_action(family: FamilyCreate, db: Session = Depends(get_db)):
    return create_family(db, family)

@router.delete("/family/{family_id}")
def delete_family(family_id: int, db: Session = Depends(get_db)):
    return delete_family(db, family_id)