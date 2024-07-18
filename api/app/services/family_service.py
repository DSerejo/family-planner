from sqlalchemy.orm import Session
from app.models.family import Family
from app.schemas.family_schema import FamilyCreate
from typing import Optional
from app.utils.helper_functions import generate_unique_id

def get_family_by_id(db: Session, family_id) -> Optional[Family]:
    try:
        return db.query(Family).filter(Family.id == family_id).first()
    except Exception as e:
        return None

def create_family(db: Session, family_data: FamilyCreate):
    id = generate_unique_id()
    db_family = Family(id=id, **family_data.model_dump())
    db.add(db_family)
    db.commit()
    db.refresh(db_family)
    return db_family

def update_family(db: Session, family_id, family_data: FamilyCreate):
    db_family = get_family_by_id(db, family_id)
    if db_family:
        for key, value in family_data.model_dump().items():
            setattr(db_family, key, value)
        db.commit()
        db.refresh(db_family)
    return db_family


def delete_family(db: Session, family_id):
    db_family = get_family_by_id(db, family_id)
    if db_family:
        db.delete(db_family)
        db.commit()
    return True
