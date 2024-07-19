import pytest
import sys
import os

# Add the root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.services.session_service import SessionService
from app.services.user_service import UserService
from app.schemas.user_schema import UserCreate
from datetime import datetime

@pytest.fixture()
def session_service(db):
    return SessionService(db)

def test_create_session(db, session_service):
    user_service = UserService(db)
    user = user_service.create_user(UserCreate(email="test@test.com", name="Test User"))
    session = session_service.create_session(user.id)
    assert session.user_id == user.id
    assert session.id is not None

def test_get_session_by_token(db, session_service):
    user_service = UserService(db)
    user = user_service.create_user(UserCreate(email="test@test.com", name="Test User"))
    session = session_service.create_session(user.id)
    assert session.user_id == user.id
    assert session.id is not None
    assert session_service.get_session_by_token(session.id) is not None