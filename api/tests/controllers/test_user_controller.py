import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI, HTTPException, Header
import mock

import sys
import os

# Add the root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.controllers.user_controller import router, validate_api_key
from app.schemas.user_schema import UserCreate
from app.database import get_db
from app.services.user_service import create_user_service

# Mock dependencies
def mock_validate_api_key(authorization : str | None =  Header(None)):
    if authorization != f"Bearer mock_api_key":
        raise HTTPException(status_code=401, detail="Unauthorized")

def mock_user_service():
    class UserService:
        def get_user_by_email(self, email: str):
            if email == "existing@example.com":
                return {"email": email, "name": "Existing User"}
            return None
        def create_user(self, user: UserCreate):
            return {"email": user.email, "name": user.name}
    return UserService()

def mock_get_db():
    pass

# Apply mocks
app = FastAPI()
app.include_router(router)
app.dependency_overrides[validate_api_key] = mock_validate_api_key
app.dependency_overrides[get_db] = mock_get_db
app.dependency_overrides[create_user_service] = mock_user_service

client = TestClient(app)

def test_google_login_existing_user():
    response = client.post("/user", json={"email": "existing@example.com", "name": "Existing User"}, headers={"Authorization": "Bearer mock_api_key"})
    assert response.status_code == 200
    assert response.json() == {"success": True, "user": {"email": "existing@example.com", "name": "Existing User"}}

def test_google_login_new_user():
    response = client.post("/user", json={"email": "new@example.com", "name": "New User"}, headers={"Authorization": "Bearer mock_api_key"})
    assert response.status_code == 200
    assert response.json() == {"success": True, "user": {"email": "new@example.com", "name": "New User"}}

def test_google_login_new_user_wrong_request_body():
    response = client.post("/user", json={"email": "new@example.com"}, headers={"Authorization": "Bearer mock_api_key"})
    assert response.status_code == 422

def test_google_login_invalid_token():
    response = client.post("/user", json={"email": "invalid@example.com", "name": "Invalid User"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Unauthorized"}


