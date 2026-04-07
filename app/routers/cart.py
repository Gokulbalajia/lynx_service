from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from app.core.supabase_client import get_supabase
from app.core.dependencies import get_current_user
from app.models.cart import CartResponse, CartCreate, CartUpdate
from supabase import Client

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.get("/", response_model=List[CartResponse])
def get_cart(current_user: dict = Depends(get_current_user), db: Client = Depends(get_supabase)):
    res = db.table("cart").select("*").eq("user_id", str(current_user["id"])).execute()
    return res.data

@router.post("/", response_model=CartResponse)
def add_to_cart(item: CartCreate, current_user: dict = Depends(get_current_user), db: Client = Depends(get_supabase)):
    # Automatically assign current user id
    cart_item = item.model_dump()
    cart_item["user_id"] = str(current_user["id"])
    
    res = db.table("cart").insert(cart_item).execute()
    if not res.data:
        raise HTTPException(status_code=500, detail="Failed to add item to cart")
    return res.data[0]

@router.put("/{id}", response_model=CartResponse)
def update_cart_item(id: UUID, item: CartUpdate, current_user: dict = Depends(get_current_user), db: Client = Depends(get_supabase)):
    # Verify ownership
    existing = db.table("cart").select("user_id").eq("id", str(id)).single().execute()
    if not existing.data or str(existing.data["user_id"]) != str(current_user["id"]):
        raise HTTPException(status_code=403, detail="Not authorized to update this cart item")
    
    res = db.table("cart").update(item.model_dump(exclude_unset=True)).eq("id", str(id)).execute()
    return res.data[0]

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_from_cart(id: UUID, current_user: dict = Depends(get_current_user), db: Client = Depends(get_supabase)):
    # Verify ownership
    existing = db.table("cart").select("user_id").eq("id", str(id)).single().execute()
    if not existing.data or str(existing.data["user_id"]) != str(current_user["id"]):
        raise HTTPException(status_code=403, detail="Not authorized to remove this cart item")
    
    db.table("cart").delete().eq("id", str(id)).execute()
    return None
