from .user_definition import User, UserQuery
from .family_definition import Family, FamilyQuery
from strawberry.tools import merge_types

types = [User, Family]
Query = merge_types("Query", (UserQuery, FamilyQuery))