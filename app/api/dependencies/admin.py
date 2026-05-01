from fastapi import Header, HTTPException
import os

ADMIN_KEY = os.getenv("ADMIN_KEY")

def verify_admin(x_admin_key: str = Header(None)):
    if x_admin_key != ADMIN_KEY:
        raise HTTPException(status_code=403, detail="Not authorized")
