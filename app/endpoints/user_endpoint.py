from fastapi import APIRouter, Depends
from app.auth.auth import get_current_user
from app.db.connection import get_supabase
from app.models.user_model import UserResponse
from app.query.user_query import UserQuery
from supabase import Client

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserResponse)
def get_me(current_user: dict = Depends(get_current_user), db: Client = Depends(get_supabase)):
    query = UserQuery(db)
    return query.get_user_by_id(current_user["id"])
