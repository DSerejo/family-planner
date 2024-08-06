from fastapi import APIRouter, HTTPException, Depends
from app.schemas.family_schema import FamilyCreateBody, FamilyCreate
from app.services.family_member_service import FamilyMemberService, create_family_member_service
from app.schemas.family_member_schema import FamilyMemberCreateBody, FamilyMemberCreate
from app.models.session import Session
from app.utils.session_validate import validate_session
from app.models.family_member import FamilyMember
router = APIRouter()

@router.post("/family/{family_id}/member")
def create_family(
        family_id: str,
        body: FamilyMemberCreateBody, 
        family_member_service: FamilyMemberService = Depends(create_family_member_service),
        session: Session = Depends(validate_session)):
    member = FamilyMemberCreate(family_id=family_id, **body.model_dump())
    member, db_family = family_member_service.create_family_member(member)
    return member

@router.delete("/family/{family_id}/member/{member_id}")
def delete_family_member(
        family_id: str,
        member_id: str,
        family_member_service: FamilyMemberService = Depends(create_family_member_service),
        session: Session = Depends(validate_session)):
    family_member_service.remove_family_member(member_id)
    return {"success": True, "message": "Family member deleted"}

