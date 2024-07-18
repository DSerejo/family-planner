from sqlalchemy import Column, String, Integer, ForeignKey, UniqueConstraint
from app.database import Base

class FamilyMember(Base):
    __tablename__ = "family_members"
    id = Column(Integer, primary_key=True)
    #name is optional, if the member is a user, it will be null
    name = Column(String(255), nullable=True)
    #email is optional, it is used to invite a user to the family
    email = Column(String(255), nullable=True)
    #user_id is optional, if the member is not a user, it will be null
    user_id = Column(String(36), ForeignKey('users.id'), nullable=True)
    family_id = Column(String(36), ForeignKey('families.id'), nullable=False)
    #name user_id and family_id must be unique
    __table_args__ = (
        UniqueConstraint(name, family_id, name='unique_family_member_1'),
        UniqueConstraint(user_id, family_id, name='unique_family_member_2'),
    )
