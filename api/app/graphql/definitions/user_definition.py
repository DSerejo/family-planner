from ...models import User as UserModel, Session as SessionModel, FamilyMember as FamilyMemberModel

import strawberry
from typing import Optional, List
from .family_definition import Family

@strawberry.type
class Session:
    id: str
    user_id: str
    
    @classmethod
    def from_instance(cls, instance: SessionModel):
        return cls(
            id=instance.id,
            user_id=instance.user_id,
        )


@strawberry.type
class User:
    email: Optional[str]
    name: Optional[str]
    id: str
    model: strawberry.Private[UserModel]

    @strawberry.field(graphql_type=List["Family"])
    def families(self, info: strawberry.Info) -> List[Family]:
        families = self.model.families
        return [Family.from_instance(family) for family in families]
    
    @strawberry.field
    def sessions(self, info: strawberry.Info) -> Optional[List[Session]]:
        return [Session.from_instance(session) for session in self.model.sessions]

    @classmethod
    def from_instance(cls, instance: UserModel):
        user = cls(
            id=instance.id,
            name=instance.name,
            email=instance.email,
            model=instance
        )
        return user
    
@strawberry.type
class UserQuery:

    @strawberry.field
    def user(self, email: str, info, limit: int = 250) -> User:
        db = info.context["db"]
        user_service = info.context["user_service"]
        print(email)
        print(db.query(UserModel).filter(UserModel.email == email).first())
        db_user = user_service.get_user_by_email(email)
        if db_user is None:
            raise Exception("User not found")
        user = User.from_instance(db_user)
        return user