from fastapi import APIRouter, Depends
from app.core.dependencies import get_current_user
from app.core.supabase_client import get_supabase
from app.models.user import UserResponse
from supabase import Client

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserResponse)
def get_me(current_user: dict = Depends(get_current_user), db: Client = Depends(get_supabase)):
    res = db.table("users").select("*").eq("id", str(current_user["id"])).execute()
    return res.data[0]
