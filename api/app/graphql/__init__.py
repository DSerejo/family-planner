

from typing import Any, Coroutine
from starlette.requests import Request
from starlette.responses import Response
from strawberry.fastapi import GraphQLRouter
import strawberry
from sqlalchemy.orm import Session
from fastapi import Depends
from app.database import get_db
from .schema import schema
from app.services.user_service import UserService
from app.models.user import User
from app.services.user_service import create_user_service
from app.utils.helper_functions import validate_session
from app.models.session import Session as SessionModel

def get_context(db: Session = Depends(get_db), 
                user_service: UserService = Depends(create_user_service),
                validate_session: SessionModel = Depends(validate_session)) -> Coroutine[Any, Any, Any]:
    print (db.query(User).all())
    return {
            "db": db, 
            "user_service": user_service,
            "session": validate_session
            }

    

graphql_app = GraphQLRouter(
        schema, 
        context_getter=get_context
)