from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import create_access_token, verify_password, get_password_hash
from app.core.supabase_client import get_supabase
from app.models.user import UserCreate, UserResponse, Token
from supabase import Client

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Client = Depends(get_supabase)):
    # Check if user already exists
    existing = db.table("users").select("*").eq("email", user_data.email).execute()
    if existing.data:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash password
    user_dict = user_data.model_dump()
    user_dict["password"] = get_password_hash(user_dict["password"])
    
    # Create user
    res = db.table("users").insert(user_dict).execute()
    if not res.data:
        raise HTTPException(status_code=500, detail="Failed to create user")
    
    return res.data[0]

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Client = Depends(get_supabase)):
    res = db.table("users").select("*").eq("email", form_data.username).execute()
    if not res.data:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    user = res.data[0]
    if not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    # Fetch role name
    role_name = "user"
    if user.get("role_id"):
        role_res = db.table("roles").select("name").eq("id", user["role_id"]).execute()
        if role_res.data:
            role_name = role_res.data[0]["name"]
    
    access_token = create_access_token(data={"sub": str(user["id"]), "role": role_name})
    return {"access_token": access_token, "token_type": "bearer"}
