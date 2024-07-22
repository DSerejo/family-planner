import strawberry
from ...models import Family as FamilyModel

@strawberry.type
class Family:
    id: strawberry.ID
    name: str

    @classmethod
    def from_instance(cls, family: FamilyModel):
        return cls(id=family.id, name=family.name)
    
@strawberry.type
class FamilyQuery:

    @strawberry.field
    def family(self, id: strawberry.ID, info) -> Family:
        family_service = next(info.context["family_service"])
        family = family_service.get_family_by_id(id)
        return Family.from_instance(family)