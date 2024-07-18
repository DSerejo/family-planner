

import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI, HTTPException, Header
import mock

import sys
import os

# Add the root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.schemas.family_schema import FamilyCreate
from app.database import get_db# Mock dependencies
def mock_validate_api_key(authorization: str | None = Header(None)):
    if authorization != f"Bearer mock_api_key":
        raise HTTPException(status_code=401, detail="Unauthorized")

def mock_create_family(db, family: FamilyCreate):
    return {"id": 1, "name": family.name}

def mock_delete_family(db, family_id: int):
    return {"id": family_id, "name": "New Family"}


@pytest.fixture(autouse=True)
def patch_create_family():
    with mock.patch('app.controllers.family_controller.create_family', wraps=mock_create_family) as mock_function:
        yield mock_function


@pytest.fixture(autouse=True)
def patch_delete_family():
    with mock.patch('app.controllers.family_controller.delete_family', wraps=mock_delete_family) as mock_function:
        yield mock_function

def mock_get_db():
    pass


from app.controllers.family_controller import router, validate_api_key

# Apply mocks
app = FastAPI()
app.include_router(router)
app.dependency_overrides[validate_api_key] = mock_validate_api_key
app.dependency_overrides[get_db] = mock_get_db

client = TestClient(app)

def test_create_family():
    response = client.post("/family", json={"name": "New Family"}, headers={"Authorization": "Bearer mock_api_key"})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "New Family"}

def test_create_family_wrong_body():
    response = client.post("/family", json={"name1": "New Family"}, headers={"Authorization": "Bearer mock_api_key"})
    assert response.status_code == 422

def test_delete_family():
    response = client.delete("/family/1", headers={"Authorization": "Bearer mock_api_key"})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "New Family"}
