import os
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models import Family, FamilyMember
import sys

def pytest_configure(config):
    os.environ['ENV'] = 'testing'

# import logging
# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


# Setup the test database
DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



@pytest.fixture(scope="session", autouse=True)
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db

    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(autouse=True)
def clean_db(db):
    tables = [Family.__tablename__, FamilyMember.__tablename__]
    for table in tables:
        try:
            db.execute(text(f'delete from {table}'))
        except Exception as e:
            db.rollback()
            db.execute(text(f'delete from {table}'))
    db.commit()