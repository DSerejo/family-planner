import pytest

from sqlalchemy import text
from fastapi import HTTPException

import sys
import os

# Add the root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.database import Base
from app.models.family import Family
from app.models.family_member import FamilyMember
from app.services.family_member_service import FamilyMemberService
from app.services.user_service import UserService
from app.services.family_service import FamilyService
from app.schemas.family_member_schema import FamilyMemberCreate


@pytest.fixture(scope="module")
def family_member_service(db):
    user_service = UserService(db)
    family_service = FamilyService(db, None)  
    family_member_service = FamilyMemberService(db, user_service, family_service)
    family_service.setFamilyMemberService(family_member_service)
    return family_member_service

def create_family(db, id, name="Test Family"):
    family = Family(id=id,name=name)
    db.add(family)
    db.commit()
    db.refresh(family)
    return family

def test_add_non_user_member_to_family(db, family_member_service):
    create_family(db, "1")
    [member, db_family] = family_member_service.create_family_member(FamilyMemberCreate(family_id="1", name="Member"))
    assert member.id is not None
    assert db_family.id == "1"
    assert db_family.members[0].id == member.id
    assert db_family.members[0].name == "Member"

def test_add_non_user_member_to_family_fails_if_member_exists(db, family_member_service: FamilyMemberService):
    create_family(db, "2")
    family_member_service.create_family_member(FamilyMemberCreate(family_id="2", name="Member"))
    with pytest.raises(HTTPException) as e:
        family_member_service.create_family_member(FamilyMemberCreate(family_id="2", name="Member"))
    assert e.value.status_code == 400
    assert e.value.detail == "Family member already exists"

def test_add_non_user_member_to_family_fails_if_family_does_not_exist(db, family_member_service):
    with pytest.raises(HTTPException) as e:
        family_member_service.create_family_member(FamilyMemberCreate(family_id="3", name="Member"))
    assert e.value.status_code == 404
    assert e.value.detail == "Family does not exist"
    
def test_remove_family_member(db, family_member_service):
    create_family(db, "4")
    [member, db_family] = family_member_service.create_family_member(FamilyMemberCreate(family_id="4", name="Member"))
    family_member_service.remove_family_member(member.id)
    assert family_member_service.get_family_member_by_id(member.id) is None
    assert db_family.members == []

def test_remove_family_member_fails_if_member_does_not_exist(db, family_member_service):
    with pytest.raises(HTTPException) as e:
        family_member_service.remove_family_member("5")
    assert e.value.status_code == 404
    assert e.value.detail == "Family member does not exist"