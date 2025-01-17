from sqlalchemy.orm import Session
from app.services.family_service import FamilyService, create_family_service
from app.schemas.family_member_schema import FamilyMemberCreate
from app.models.family_member import FamilyMember
from fastapi import HTTPException, Depends
from app.services.user_service import UserService, create_user_service
from app.database import get_db
from app.services.context_service import get_context
class FamilyMemberService:
    def __init__(
            self, 
            db: Session, 
            user_service: UserService, 
            family_service: FamilyService
            ):
        self.db = db
        self.user_service = user_service
        self.family_service = family_service

    def setFamilyService(self, family_service: FamilyService):
        self.family_service = family_service
        
    def create_family_member(self, family_member: FamilyMemberCreate):
        db_family = self.family_service.get_family_by_id(family_member.family_id)
        if not db_family:
            raise HTTPException(status_code=404, detail="Family does not exist")
        
        if family_member.email:
            self._invite_family_member(family_member)

        if family_member.user_id:   
            self._prepare_user_member(family_member)
        
        try:
            member = FamilyMember(**family_member.model_dump(), family=db_family)
            self.db.add(member)
            self.db.commit()
            self.db.refresh(member)
        except Exception as e:
            raise HTTPException(status_code=400, detail="Family member already exists") from e
        return [member, db_family]
    
    def _prepare_user_member(self, family_member: FamilyMemberCreate):
        db_user = self.user_service.get_user_by_id(family_member.user_id)
        if not db_user :
            family_member.user_id = None
        else:
            family_member.name = db_user.name
            family_member.email = db_user.email

    def _invite_family_member(self, family_member: FamilyMemberCreate):
        db_user = self.user_service.get_user_by_email(family_member.email)
        context = get_context()
        family_member.invited_by_user_id = context.get_session().user.id
        if db_user:
            family_member.user_id = db_user.id

    def get_family_member_by_id(self, member_id):
        return self.db.query(FamilyMember).filter(FamilyMember.id == member_id).first()

    def remove_family_member(self, member_id):
        member = self.get_family_member_by_id(member_id)
        if not member:
            raise HTTPException(status_code=404, detail="Family member does not exist")
        self.db.delete(member)
        self.db.commit()
        return member
    
def create_family_member_service(
        db: Session = Depends(get_db), 
        user_service: UserService = Depends(create_user_service),
        family_service: FamilyService = Depends(create_family_service)
        ):
    return FamilyMemberService(db, user_service, family_service)