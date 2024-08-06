from sqlalchemy import Column, Integer, String
from app.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from typing import Optional
from app.schemas.family_schema import FamilyFilter
from app.models import Family, FamilyMember
from app.database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    sessions = relationship("Session", back_populates="user")
    family_member_list = relationship("FamilyMember", back_populates="user", lazy="select", foreign_keys="[FamilyMember.user_id]")

    @hybrid_property
    def families(self):
        return [family_member.family for family_member in self.family_member_list]
    
    def listFamilies(self, where: Optional[FamilyFilter] = None, db: Session = Depends(get_db)):
        if hasattr(db, "dependency"):
            db = next(db.dependency())
        query = db.query(Family).join(FamilyMember, Family.id == FamilyMember.family_id).filter(FamilyMember.user_id == self.id).order_by(Family.name)
        if where and where.id:
            query = query.filter(Family.id == where.id)
        return query.all()