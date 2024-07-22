import pytest

import sys
import os

# Add the root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.schemas.family_schema import FamilyCreate, FamilyUpdate
from app.services.family_service import FamilyService
from app.models.family import Family
from app.models.user import User
from app.services.user_service import UserService
from app.services.family_member_service import FamilyMemberService

def create_family(db, user_id, family_id):
    create_user(db, user_id)
    family = Family(id=family_id, name="Test Family", owner_id=user_id)
    db.add(family)
    db.commit()
    db.refresh(family)
    return family

def create_user(db, user_id):
    user = User(id=user_id, email="test@test.com", name="Test User")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture()
def family_service(db):
    user_service = UserService(db)
    family_service = FamilyService(db, None)  
    family_member_service = FamilyMemberService(db, user_service, family_service)
    family_service.setFamilyMemberService(family_member_service)
    return family_service

def test_create_family(db, family_service):
    user = create_user(db, "1234567890")
    family = FamilyCreate(name="New Family", owner_id=user.id)
    result = family_service.create_family(family)
    assert result.id is not None
    assert result.name == "New Family"
    assert result.owner_id == user.id

def test_get_family_by_id(db, family_service):
    create_family(db, "1234567890", "1234567890")
    fetched_family = family_service.get_family_by_id("1234567890")
    assert fetched_family is not None
    assert fetched_family.id is not None
    assert fetched_family.name == "Test Family"

def test_update_family(db, family_service):
    create_family(db, "1234567890", "1234567890")
    family = family_service.update_family("1234567890",  FamilyUpdate(name="Updated Family"))
    assert family.name == "Updated Family"

def test_delete_family(db, family_service):
    create_family(db, "1234567890", "1234567890")
    family_service.delete_family("1234567890")
    assert family_service.get_family_by_id("1234567890") is None