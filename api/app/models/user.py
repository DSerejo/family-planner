from sqlalchemy import Column, Integer, String
from app.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    sessions = relationship("Session", back_populates="user")
    family_member_list = relationship("FamilyMember", back_populates="user")

    @hybrid_property
    def families(self):
        return [family_member.family for family_member in self.family_member_list]