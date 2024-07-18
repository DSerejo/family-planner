import pytest
import sys
import os

# Add the root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


from app.models.user import User
from app.schemas.user_schema import UserCreate
from app.services.user_service import get_user_by_email, create_user
from app.database import Base



def test_get_user_by_email(db):
    # Create a user
    user = User(id="1234567890", email="test@example.com", name="Test User")
    db.add(user)
    db.commit()
    db.refresh(user)

    # Test get_user_by_email
    fetched_user = get_user_by_email(db, "test@example.com")
    assert fetched_user is not None
    assert fetched_user.id is not None
    assert fetched_user.email == "test@example.com"
    assert fetched_user.name == "Test User"

def test_create_user(db):
    user_create = UserCreate(email="newuser@example.com", name="New User")
    created_user = create_user(db, user_create)
    assert created_user is not None
    assert created_user.email == "newuser@example.com"
    assert created_user.name == "New User"

   