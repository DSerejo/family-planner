from fastapi import Request, HTTPException
from sqlalchemy.orm import Session
from app.services.session_service import SessionService

class ContextService:
    def __init__(self, request: Request, db: Session):
        self.request = request
        self.db = db
        self.sessionService = SessionService(db)
    def get_auth_token(self):
        bearerToken = self.request.headers.get('Authorization')
        if not bearerToken:
            raise HTTPException(status_code=401, detail="Unauthorized")
        token = bearerToken.split(' ')[1]
        return token
    
    def get_session(self):
        token = self.get_auth_token()
        return self.sessionService.get_session_by_token(token) 
    
def set_context(context: ContextService):
    global _context  # add this line!
    _context = context
        

def get_context() -> ContextService:
    global _context
    return _context