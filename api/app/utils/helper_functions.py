from fastapi import HTTPException, Header
import os
import uuid

def validate_api_key(authorization : str | None =  Header(None)):
    if authorization != f"Bearer {os.getenv('API_KEY')}":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True
    
def generate_unique_id(length: int = 36):
    return str(uuid.uuid4())[:length]