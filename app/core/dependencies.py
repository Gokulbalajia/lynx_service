from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.security import decode_token
from app.core.supabase_client import get_supabase
from supabase import Client
from uuid import UUID

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Client = Depends(get_supabase)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_token(token)
    if payload is None:
        raise credentials_exception
    
    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    
    # Verify user exists and fetch role
    # Assuming role is included in token to avoid DB hit every time, 
    # but still verifying user existence for security
    res = db.table("users").select("id, role_id").eq("id", user_id).execute()
    if not res.data:
        raise credentials_exception
    
    return {"id": user_id, "role": payload.get("role"), "role_id": res.data[0]["role_id"]}

def admin_required(current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return current_user
