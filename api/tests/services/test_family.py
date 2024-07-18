import pytest

import sys
import os

# Add the root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.schemas.family_schema import FamilyCreate
from app.services.family_service import create_family, get_family_by_id, update_family, delete_family
from app.database import Base
from app.models.family import Family

def test_create_family(db):
    family = FamilyCreate(name="New Family")
    result = create_family(db, family)
    assert result.id is not None
    assert result.name == "New Family"

def test_get_family_by_id(db):
     # Create a family
    family = Family(id="1234567890", name="Test Family")
    db.add(family)
    db.commit()
    db.refresh(family)

    # Test get_user_by_email
    fetched_family = get_family_by_id(db, "1234567890")
    assert fetched_family is not None
    assert fetched_family.id is not None
    assert fetched_family.name == "Test Family"

def test_update_family(db):
    family = Family(id="12345678901", name="Test Family")
    db.add(family)
    db.commit()
    db.refresh(family)
    family = update_family(db, family.id,  FamilyCreate(name="Updated Family"))
    assert family.name == "Updated Family"

def test_delete_family(db):
    family = Family(id="12345678902", name="Test Family")
    id = family.id
    db.add(family)
    db.commit()
    db.refresh(family)
    delete_family(db, id)
    assert get_family_by_id(db, id) is None