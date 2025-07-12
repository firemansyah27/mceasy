from fastapi import Header, HTTPException
import os

def verify_api_key(x_api_key: str = Header(...)):
    valid_key = os.getenv("API_KEY")
    if x_api_key != valid_key:
        raise HTTPException(status_code=403, detail="Unauthorized")
