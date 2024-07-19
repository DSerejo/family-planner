from sqlalchemy import Column, String,  ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship

class Family(Base):
    __tablename__ = 'families'

    id = Column(String(36), primary_key=True)
    owner_id = Column(String(36), ForeignKey('users.id'))
    name = Column(String(255), index=True)
    members = relationship("FamilyMember", backref='family')
