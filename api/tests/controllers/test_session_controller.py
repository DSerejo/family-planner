import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI, HTTPException, Header
import mock

import sys
import os

# Add the root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.controllers.session_controller import router, validate_api_key
from app.database import get_db
from app.schemas.user_schema import UserCreate
from app.services.user_service import create_user_service
from app.services.session_service import create_session_service
from app.models.session import Session
from app.models.user import User

# Mock dependencies
def mock_validate_api_key(authorization: str | None = Header(None)):
    if authorization != "Bearer mock_api_key":
        raise HTTPException(status_code=401, detail="Unauthorized")

def mock_user_service():
    class UserService:
        def get_user_by_email(self, email: str):
            if email == "existing@example.com":
                return User(id=1, email=email, name="Existing User")
            return None
        def create_user(self, user: UserCreate):
            return User(id=1, email=user.email, name=user.name)
        
    return UserService()

def mock_session_service():
    class SessionService:
        def create_session(self, user_id: int):
            return Session(id="mock_session_id", user_id=user_id)
        def get_session_by_token(self, token: str):
            if token == "valid_token":
                return Session(id=token, user_id="mock_user_id")
            return None
        def delete_session(self, token: str):
            return  {"message": "Signed out"}
    return SessionService()

def mock_get_db():
    pass

# Apply mocks
app = FastAPI()
app.include_router(router)
app.dependency_overrides[validate_api_key] = mock_validate_api_key
app.dependency_overrides[get_db] = mock_get_db
app.dependency_overrides[create_user_service] = mock_user_service
app.dependency_overrides[create_session_service] = mock_session_service

client = TestClient(app)

def test_create_session_existing_user(db):
    response = client.post("/session", json={"email": "existing@example.com", "name": "Existing User"}, headers={"Authorization": "Bearer mock_api_key"})
    assert response.status_code == 200
    assert response.json() == {"token": "mock_session_id"}

def test_create_session_fails_user_not_found(db):
    response = client.post("/session", json={"email": "nonexistent@example.com", "name": "Nonexistent User"}, headers={"Authorization": "Bearer mock_api_key"})
    assert response.status_code == 401
    assert response.json() == {"detail": "User not found"}

def test_create_session_fails_invalid_key(db):
    response = client.post("/session", json={"email": "existing@example.com", "name": "Existing User"}, headers={"Authorization": "Bearer invalid_key"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Unauthorized"}

def test_validate_session_valid_token(db):
    response = client.get("/session/valid_token", headers={"Authorization": "Bearer mock_api_key"})
    assert response.status_code == 200
    assert response.json() == {"token": "valid_token"}

def test_validate_session_invalid_token(db):
    response = client.get("/session/invalid_token", headers={"Authorization": "Bearer mock_api_key"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid session"} 

def test_delete_session(db):
    mock_session_id = "mock_session_id"
    response = client.get(f"/session/{mock_session_id}/signout", headers={"Authorization": "Bearer mock_api_key"})
    assert response.status_code == 200
    assert response.json() == {"message": "Signed out"}
