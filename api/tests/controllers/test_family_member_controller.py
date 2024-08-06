

import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI, HTTPException, Header
import mock

import sys
import os

# Add the root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.controllers.family_member_controller import router, validate_session
from app.schemas.family_member_schema import  FamilyMemberCreate
from app.services.family_member_service import create_family_member_service
from app.database import get_db

# Mock dependencies
def mock_validate_session(authorization: str | None = Header(None)):
    if authorization != f"Bearer token":
        raise HTTPException(status_code=401, detail="Unauthorized")
    
def mock_family_member_service():
    class FamilyMemberService:
        def create_family_member(self, member: FamilyMemberCreate):
            return {**member.model_dump(), "id": 1}
        
        def remove_family_member(self, member_id: int):
            return True
        
    return FamilyMemberService()




def mock_get_db():
    pass

# Apply mocks
app = FastAPI()
app.include_router(router)
app.dependency_overrides[validate_session] = mock_validate_session
app.dependency_overrides[get_db] = mock_get_db
app.dependency_overrides[create_family_member_service] = mock_family_member_service

client = TestClient(app)
def test_add_family_member_with_no_session():
    response = client.post("/family/1/member", json={"email": "newmember@example.com", "name": "New Member"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Unauthorized"}

def test_add_family_member():
    response = client.post("/family/1/member", json={"email": "newmember@example.com", "name": "New Member"}, headers={"Authorization": "Bearer token"})
    assert response.status_code == 200
    resp =  response.json()
    assert resp["name"] == "New Member"
    assert resp["email"] == "newmember@example.com"
    assert resp["family_id"] == '1'

def test_delete_family_member():
    response = client.delete("/family/1/member/1", headers={"Authorization": "Bearer token"})
    assert response.status_code == 200
    assert response.json() == {"success": True, "message": "Family member deleted"}

# def test_remove_family_member():
#     response = client.delete("/family/1/members/member@example.com", headers={"Authorization": "Bearer mock_api_key"})
#     assert response.status_code == 200
#     assert response.json() == {"id": 1, "members": []}

# def test_invite_family_member():
#     response = client.post("/family/1/invite", json={"email": "invitee@example.com"}, headers={"Authorization": "Bearer mock_api_key"})
#     assert response.status_code == 200
#     assert response.json() == {"success": True, "message": "Invitation sent"}

# def test_accept_family_invitation():
#     response = client.post("/family/1/invite/accept", json={"email": "invitee@example.com"}, headers={"Authorization": "Bearer mock_api_key"})
#     assert response.status_code == 200
#     assert response.json() == {"success": True, "message": "Invitation accepted"}

# def test_reject_family_invitation():
#     response = client.post("/family/1/invite/reject", json={"email": "invitee@example.com"}, headers={"Authorization": "Bearer mock_api_key"})
#     assert response.status_code == 200
#     assert response.json() == {"success": True, "message": "Invitation rejected"}

