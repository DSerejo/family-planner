from sqlalchemy.orm import Session
from app.services.family_service import get_family_by_id
from app.services.user_service import get_user_by_id
from app.schemas.family_member_schema import FamilyMemberCreate
from app.models.family_member import FamilyMember
from fastapi import HTTPException

def create_family_member(db: Session, family_member: FamilyMemberCreate):
    db_family = get_family_by_id(db, family_member.family_id)
    if not db_family:
        raise HTTPException(status_code=404, detail="Family does not exist")
    db_user = get_user_by_id(db, family_member.user_id)
    if not db_user :
        family_member.user_id = None
    try:
        member = FamilyMember(**family_member.model_dump(), family=db_family)
        db.add(member)
        db.commit()
        db.refresh(member)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Family member already exists") from e
    return [member, db_family]

def get_family_member_by_id(db: Session, member_id):
    return db.query(FamilyMember).filter(FamilyMember.id == member_id).first()

def remove_family_member(db: Session, member_id):
    member = get_family_member_by_id(db, member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Family member does not exist")
    db.delete(member)
    db.commit()
    return member