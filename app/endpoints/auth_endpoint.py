from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.auth import create_access_token, verify_password, get_password_hash
from app.db.connection import get_supabase
from app.models.user_model import UserCreate, UserResponse
from app.models.auth_model import Token
from app.query.auth_query import AuthQuery
from supabase import Client

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Client = Depends(get_supabase)):
    query = AuthQuery(db)
    # Check if user already exists
    if query.get_by_email(user_data.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash password
    user_dict = user_data.model_dump()
    user_dict["password"] = get_password_hash(user_dict["password"])
    
    # Create user
    user = query.create_user(user_dict)
    if not user:
        raise HTTPException(status_code=500, detail="Failed to create user")
    
    return user

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Client = Depends(get_supabase)):
    query = AuthQuery(db)
    user = query.get_by_email(form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    if not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    # Fetch role name
    role_name = "user"
    if user.get("role_id"):
        role_name = query.get_role_name(user["role_id"])
    
    access_token = create_access_token(data={"sub": str(user["id"]), "role": role_name})
    return {"access_token": access_token, "token_type": "bearer"}
