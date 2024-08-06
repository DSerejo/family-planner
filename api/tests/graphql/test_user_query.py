import pytest
from unittest.mock import patch
from app.models.user import User as UserModel
from fastapi import FastAPI
from fastapi.testclient import TestClient
from strawberry.fastapi import GraphQLRouter
from app.graphql import graphql_app
from app.database import get_db
from sqlalchemy.orm import Session
from conftest import get_db as mock_db
from app.models.session import Session as SessionModel
from app.models.family_member import FamilyMember as FamilyMemberModel
from app.models.family import Family as FamilyModel

import os
import sys

# Add the root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

@pytest.fixture
def client(db):
    def mock_db():
        return db
    app = FastAPI()
    app.include_router(graphql_app, prefix="/graphql")
    app.dependency_overrides[get_db] = mock_db

    return TestClient(app)

def create_family(db, id, name, owner_id="1"):
    family = FamilyModel(id=id, name=name, owner_id=owner_id)
    db.add(family)
    db.commit()
    db.refresh(family)
    return family

def create_family_member(db, id, name, email, user_id, family_id):
    family_member = FamilyMemberModel(id=id, name=name, email=email, user_id=user_id, family_id=family_id)
    db.add(family_member)
    db.commit()
    db.refresh(family_member)
    return family_member

def create_test_data(db):
    user = UserModel(id="1", email="test@example.com", name="Test User")
    db.add(user)
    db.commit()
    db.refresh(user)
    session = SessionModel(id="1", user_id="1")
    db.add(session)
    db.commit()
    db.refresh(session)
    create_family(db, "1", "Test Family", "1")
    create_family(db, "2", "Test Family 2", "1")
    create_family_member(db, "1", "Test User", "test@example.com", "1", "1")
    create_family_member(db, "2", "Test User", "test@example.com", "1", "2")
    return user, session

def test_user_query_fails_with_no_session(client, db):
    query = """
    query GetUser($email: String!) {
        user(email: $email) {
            id
            email
            name
        }
    }
    """
    variables = {"email": "test@example.com"}
    response = client.post("/graphql", json={"query": query, "variables": variables})
    assert response.status_code == 401

def test_user_query(client, db):
    u, session = create_test_data(db)
    
    query = """
    query GetUser($email: String!) {
        user(email: $email) {
            id
            email
            name
            sessions {
                id
            }
            families {
                id,
                name
            }
        }
    }
    """
    variables = {"email": "test@example.com"}
    response = client.post("/graphql", 
                           json={"query": query, "variables": variables}, 
                           headers={f"Authorization": f"Bearer {session.id}"})
    
    assert response.status_code == 200
    respUser  = response.json()["data"]["user"] 
    assert respUser["email"] == "test@example.com"
    assert respUser["name"] == "Test User"
    assert respUser["id"] == "1"
    assert respUser["sessions"] == [{"id": "1"}]
    assert respUser["families"][0] == {"id": "1", "name": "Test Family"}
    assert respUser["families"][1] == {"id": "2", "name": "Test Family 2"}

def test_user_query_with_family_filter(client, db):
    u, session = create_test_data(db)

    query = """
    query GetUser($email: String!, $familyId: ID!) {
        user(email: $email) {
            families(where: {id: $familyId}) {
                id,
                name
            }
        }
    }
    """

    variables = {"email": "test@example.com", "familyId": "2"}
    response = client.post("/graphql", 
                           json={"query": query, "variables": variables}, 
                           headers={f"Authorization": f"Bearer {session.id}"})
    assert response.status_code == 200
    data =  response.json()["data"]
    assert len(data["user"]["families"]) == 1
    assert data["user"]["families"][0]["id"] == "2"
