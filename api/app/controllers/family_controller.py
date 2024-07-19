from fastapi import APIRouter, HTTPException, Depends
from app.schemas.family_schema import FamilyCreateBody, FamilyCreate
from app.services.family_service import FamilyService, create_family_service
from app.models.session import Session
from app.utils.session_validate import validate_session

router = APIRouter()

@router.get("/family/{family_id}")
def get_family(family_id: int, family_service: FamilyService = Depends(create_family_service)):
    family = family_service.get_family_by_id(family_id)
    if not family:
        raise HTTPException(status_code=404, detail="Family not found")
    return family

@router.post("/family")
def create_family(familyBody: FamilyCreateBody, 
                  family_service: FamilyService = Depends(create_family_service),
                  session: Session = Depends(validate_session)):
    family = FamilyCreate(name=familyBody.name, owner_id=session.user_id)
    return family_service.create_family(family)

@router.delete("/family/{family_id}")
def delete_family(family_id: str, 
                  family_service: FamilyService = Depends(create_family_service),
                  session: Session = Depends(validate_session)):
    return {"deleted": family_service.delete_family(family_id)}