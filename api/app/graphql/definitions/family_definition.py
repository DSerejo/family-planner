import strawberry
from ...models import Family as FamilyModel
from typing import Annotated, TYPE_CHECKING, Optional


if TYPE_CHECKING:
    from .user_definition import User

@strawberry.type
class FamilyMember:
    id: strawberry.ID
    name: Optional[str]
    email: Optional[str]
    user: Optional[Annotated["User", strawberry.lazy(".user_definition") ]]

@strawberry.type
class Family:
    id: strawberry.ID
    name: str
    members: list[FamilyMember]

    @classmethod
    def from_instance(cls, family: FamilyModel):
        return cls(id=family.id, name=family.name, members=family.members)
    
@strawberry.type
class FamilyQuery:

    @strawberry.field
    def family(self, id: strawberry.ID, info) -> Family:
        family_service = info.context["family_service"]
        family = family_service.get_family_by_id(id)
        return Family.from_instance(family)