from sqlalchemy.orm import Session
from app.models.family import Family
from app.schemas.family_schema import FamilyCreate
from app.schemas.family_member_schema import FamilyMemberCreate
from typing import Optional
from app.utils.helper_functions import generate_unique_id
from fastapi import Depends
from app.database import get_db


class FamilyService:
    def __init__(self, db: Session, family_member_service):
        self.db = db
        self.family_member_service = family_member_service

    def setFamilyMemberService(self, family_member_service):
        self.family_member_service = family_member_service

    def get_family_by_id(self, family_id) -> Optional[Family]:
        try:
            return self.db.query(Family).filter(Family.id == family_id).first()
        except Exception as e:
            print(e)
            return None
      
    
    def create_family(self, family_data: FamilyCreate):
        id = generate_unique_id()
        db_family = Family(id=id, **family_data.model_dump())
        self.db.add(db_family)
        self.db.commit()
        self.family_member_service.create_family_member(FamilyMemberCreate(family_id=db_family.id, user_id=db_family.owner_id))
        self.db.refresh(db_family)
        return db_family

    def update_family(self, family_id, family_data: FamilyCreate):
        db_family = self.get_family_by_id(family_id)
        if db_family:
            for key, value in family_data.model_dump().items():
                setattr(db_family, key, value)
            self.db.commit()
            self.db.refresh(db_family)
            return db_family


    def delete_family(self, family_id):
        db_family = self.get_family_by_id(family_id)
        if db_family:
            self.db.delete(db_family)
            self.db.commit()
            return True
        return False
        
def create_family_service(db: Session = Depends(get_db), family_member_service = None):
    if family_member_service is None:
        from app.services.family_member_service import FamilyMemberService
        from app.services.user_service import UserService
        user_service = UserService(db)
        family_member_service = FamilyMemberService(db, user_service, None)
        family_service = FamilyService(db, family_member_service)
        family_member_service.setFamilyService(family_service)
        yield family_service
    else:
        family_service = FamilyService(db, family_member_service)
        yield family_service
