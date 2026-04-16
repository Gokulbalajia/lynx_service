from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from app.db.connection import get_supabase
from app.auth.auth import get_current_user
from app.models.cart_model import CartResponse, CartCreate, CartUpdate
from app.query.cart_query import CartQuery
from supabase import Client

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.get("/", response_model=List[CartResponse])
def get_cart(current_user: dict = Depends(get_current_user), db: Client = Depends(get_supabase)):
    query = CartQuery(db)
    return query.get_by_user(current_user["id"])

@router.post("/", response_model=CartResponse)
def add_to_cart(item: CartCreate, current_user: dict = Depends(get_current_user), db: Client = Depends(get_supabase)):
    query = CartQuery(db)
    cart_item = item.model_dump(mode="json")
    cart_item["user_id"] = str(current_user["id"])
    
    res = query.create_item(cart_item)
    if not res:
        raise HTTPException(status_code=500, detail="Failed to add item to cart")
    return res

@router.put("/{id}", response_model=CartResponse)
def update_cart_item(id: UUID, item: CartUpdate, current_user: dict = Depends(get_current_user), db: Client = Depends(get_supabase)):
    query = CartQuery(db)
    # Verify ownership
    owner_id = query.get_item_owner(id)
    if not owner_id or str(owner_id) != str(current_user["id"]):
        raise HTTPException(status_code=403, detail="Not authorized to update this cart item")
    
    res = query.update_item(id, item.model_dump(exclude_unset=True))
    return res

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_from_cart(id: UUID, current_user: dict = Depends(get_current_user), db: Client = Depends(get_supabase)):
    query = CartQuery(db)
    # Verify ownership
    owner_id = query.get_item_owner(id)
    if not owner_id or str(owner_id) != str(current_user["id"]):
        raise HTTPException(status_code=403, detail="Not authorized to remove this cart item")
    
    query.remove_item(id)
    return None
