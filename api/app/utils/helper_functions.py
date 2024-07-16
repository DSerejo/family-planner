from fastapi import HTTPException, Header
import os

def validate_api_key(authorization : str | None =  Header(None)):
    if authorization != f"Bearer {os.getenv('API_KEY')}":
        raise HTTPException(status_code=401, detail="Unauthorized")