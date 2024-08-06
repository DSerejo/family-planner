from sqlalchemy import Column, String,  ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship

class Family(Base):
    __tablename__ = 'families'

    id = Column(String(36), primary_key=True)
    owner_id = Column(String(36), ForeignKey('users.id'))
    name = Column(String(255), index=True)
    members = relationship("FamilyMember", backref='family', lazy='select', cascade='all, delete')
    family_members = None

    def populate_members(self):
        for member in self.members:
            if member.user:
                member.name = member.user.name
                member.email = member.user.email
        self.family_members = [
            {
                "id": member.id,
                "name": member.name,
                "email": member.email
            } for member in self.members
        ]
        return self
