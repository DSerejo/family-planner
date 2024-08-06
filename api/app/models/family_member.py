from sqlalchemy import Column, String, Integer, ForeignKey, UniqueConstraint, Boolean
from app.database import Base
from sqlalchemy.orm import relationship, mapped_column

class FamilyMember(Base):
    __tablename__ = "family_members"
    id = Column(Integer, primary_key=True)
    #name is optional, if the member is a user, it will be null
    name = Column(String(255), nullable=True)
    #email is optional, it is used to invite a user to the family
    email = Column(String(255), nullable=True)
    #user_id is optional, if the member is not a user, it will be null
    user_id = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    family_id = mapped_column(ForeignKey('families.id', ondelete='CASCADE'), nullable=False)
    invited_by_user_id = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    accepted = Column(Boolean, nullable=False, default=False)
    user = relationship("User", back_populates="family_member_list", single_parent=True, foreign_keys=[user_id])
    #name user_id and family_id must be unique
    __table_args__ = (
        UniqueConstraint(name, family_id, name='unique_family_member_1'),
        UniqueConstraint(user_id, family_id, name='unique_family_member_2'),
    )

