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
from app.services.family_member_service import create_family_member, remove_family_member, get_family_member_by_id
from app.schemas.family_member_schema import FamilyMemberCreate




def create_family(db, id, name="Test Family"):
    family = Family(id=id,name=name)
    db.add(family)
    db.commit()
    db.refresh(family)
    return family

def test_add_non_user_member_to_family(db):
    create_family(db, "1")
    [member, db_family] = create_family_member(db, FamilyMemberCreate(family_id="1", name="Member"))
    assert member.id is not None
    assert db_family.id == "1"
    assert db_family.members[0].id == member.id
    assert db_family.members[0].name == "Member"

def test_add_non_user_member_to_family_fails_if_member_exists(db):
    create_family(db, "2")
    create_family_member(db, FamilyMemberCreate(family_id="2", name="Member"))
    with pytest.raises(HTTPException) as e:
        create_family_member(db, FamilyMemberCreate(family_id="2", name="Member"))
    assert e.value.status_code == 400
    assert e.value.detail == "Family member already exists"

def test_add_non_user_member_to_family_fails_if_family_does_not_exist(db):
    with pytest.raises(HTTPException) as e:
        create_family_member(db, FamilyMemberCreate(family_id="3", name="Member"))
    assert e.value.status_code == 404
    assert e.value.detail == "Family does not exist"
    
def test_remove_family_member(db):
    create_family(db, "4")
    [member, db_family] = create_family_member(db, FamilyMemberCreate(family_id="4", name="Member"))
    remove_family_member(db, member.id)
    assert get_family_member_by_id(db, member.id) is None
    assert db_family.members == []

def test_remove_family_member_fails_if_member_does_not_exist(db):
    with pytest.raises(HTTPException) as e:
        remove_family_member(db, "5")
    assert e.value.status_code == 404
    assert e.value.detail == "Family member does not exist"