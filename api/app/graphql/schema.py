from typing import List

import strawberry
from strawberry.extensions import Extension
from app.services.user_service import create_user_service
from app.services.family_service import create_family_service
from app.database import get_db
from .definitions import types, Query

class SQLAlchemySession(Extension):

    def on_request_end(self):
        self.execution_context.context["db"].close()
        

schema = strawberry.Schema(
    Query, 
    extensions=[SQLAlchemySession],
    types=types
)