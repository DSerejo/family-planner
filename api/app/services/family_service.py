from sqlalchemy.orm import Session
from app.models.family import Family
from app.schemas.family_schema import FamilyCreate
from typing import Optional
from app.utils.helper_functions import generate_unique_id
from fastapi import Depends
from app.database import get_db

class FamilyService:
    def __init__(self, db: Session):
        self.db = db

    def get_family_by_id(self, family_id) -> Optional[Family]:
        try:
            return self.db.query(Family).filter(Family.id == family_id).first()
        except Exception as e:
            return None

    def create_family(self, family_data: FamilyCreate):
        id = generate_unique_id()
        db_family = Family(id=id, **family_data.model_dump())
        self.db.add(db_family)
        self.db.commit()
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
        
def create_family_service(db: Session = Depends(get_db)):
    return FamilyService(db)
