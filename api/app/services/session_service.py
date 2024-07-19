from sqlalchemy.orm import Session
from app.models.session import Session as SessionModel
from datetime import datetime, timedelta
from app.utils.helper_functions import generate_unique_id
from fastapi import Depends
from app.database import get_db

class SessionService:
    def __init__(self, db: Session):
        self.db = db
    def create_session(self, user_id: str):
        id = generate_unique_id()
        session = SessionModel(id=id, user_id=user_id)
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session

    def get_session_by_token(self, token: str):
        return self.db.query(SessionModel).filter(SessionModel.id == token).first()

    def delete_session(self, token: str):
        try:
            self.db.query(SessionModel).filter(SessionModel.id == token).delete()
            self.db.commit()
        except Exception:
            pass
        return {"message": "Signed out"}

def create_session_service(db: Session = Depends(get_db)):
    return SessionService(db)