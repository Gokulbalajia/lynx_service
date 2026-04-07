from fastapi import APIRouter, Depends, HTTPException
from typing import List
from uuid import UUID
from app.core.supabase_client import get_supabase
from app.models.cart import CartResponse, CartCreate
from supabase import Client

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.get("/{user_id}", response_model=List[CartResponse])
def get_cart(user_id: UUID, db: Client = Depends(get_supabase)):
    res = db.table("cart").select("*").eq("user_id", str(user_id)).execute()
    return res.data

@router.post("/", response_model=CartResponse)
def add_to_cart(item: CartCreate, db: Client = Depends(get_supabase)):
    res = db.table("cart").insert(item.model_dump()).execute()
    return res.data[0]

@router.delete("/{id}")
def remove_from_cart(id: UUID, db: Client = Depends(get_supabase)):
    db.table("cart").delete().eq("id", str(id)).execute()
    return {"message": "Item removed from cart"}
