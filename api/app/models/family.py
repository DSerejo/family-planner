from sqlalchemy import Column, String, JSON
from app.database import Base
from sqlalchemy.orm import relationship

class Family(Base):
    __tablename__ = 'families'

    id = Column(String(36), primary_key=True)
    name = Column(String(255), index=True)
    members = relationship("FamilyMember", backref='family')
    # children = relationship("Family", backref='parent', remote_side=[id])
