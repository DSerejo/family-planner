

import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI, HTTPException, Header
import mock

import sys
import os

# Add the root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.schemas.family_schema import FamilyCreate
from app.database import get_db
from app.services.family_service import create_family_service
from app.services.session_service import create_session_service
from app.models.session import Session
from app.utils.session_validate import validate_session
from tests.utils.mock_validate_session import mock_validate_session
# Mock dependencies
def mock_validate_api_key(authorization: str | None = Header(None)):
    if authorization != f"Bearer mock_api_key":
        raise HTTPException(status_code=401, detail="Unauthorized")

def mock_family_service():
    class FamilyService:
        def get_family_by_id(self, id: int):
            if id == 1:
                return {"id": id, "name": "New Family"}
            return None
        
        def create_family(self, family: FamilyCreate):
            return {"id": 1, "name": family.name}
        
        def delete_family(self, id: int):
            return True
    return FamilyService()

def mock_session_service():
    class SessionService:
        def get_session_by_token(self, token: str):
            return Session(id=token, user_id="mock_user_id")    
    return SessionService()

def mock_get_db():
    pass


from app.controllers.family_controller import router

# Apply mocks
app = FastAPI()
app.include_router(router)
# app.dependency_overrides[validate_api_key] = mock_validate_api_key
app.dependency_overrides[get_db] = mock_get_db
app.dependency_overrides[create_family_service] = mock_family_service
app.dependency_overrides[create_session_service] = mock_session_service
app.dependency_overrides[validate_session] = mock_validate_session

client = TestClient(app)

def test_create_family():
    response = client.post("/family", json={"name": "New Family"}, headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "New Family"}

def test_create_family_fails_with_wrong_token():
    response = client.post("/family", json={"name": "New Family"}, headers={"Authorization": "Bearer wrong_token"})
    assert response.status_code == 401

def test_create_family_wrong_body():
    response = client.post("/family", json={"name1": "New Family"}, headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 422

def test_delete_family_wrong_token():
    response = client.delete("/family/1", headers={"Authorization": "Bearer wrong_token"})
    assert response.status_code == 401

def test_delete_family():
    response = client.delete("/family/1", headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 200
    assert response.json() == {"deleted": True}