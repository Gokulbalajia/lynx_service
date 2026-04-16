from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from app.db.connection import get_supabase
from app.auth.auth import get_current_user, admin_required
from app.models.order_model import OrderResponse, OrderCreate
from app.query.order_query import OrderQuery
from supabase import Client

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.get("/", response_model=List[OrderResponse])
def get_user_orders(current_user: dict = Depends(get_current_user), db: Client = Depends(get_supabase)):
    query = OrderQuery(db)
    return query.get_user_orders(current_user["id"])

@router.get("/admin/all", response_model=List[OrderResponse])
def get_all_orders(_admin: dict = Depends(admin_required), db: Client = Depends(get_supabase)):
    query = OrderQuery(db)
    return query.get_all_orders()

@router.post("/checkout", response_model=OrderResponse)
def checkout(order_data: OrderCreate, current_user: dict = Depends(get_current_user), db: Client = Depends(get_supabase)):
    if str(order_data.user_id) != str(current_user["id"]):
        raise HTTPException(status_code=403, detail="Cannot create order for another user")
    
    query = OrderQuery(db)
    return query.process_checkout(order_data)

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: UUID, current_user: dict = Depends(get_current_user), db: Client = Depends(get_supabase)):
    query = OrderQuery(db)
    order = query.get_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Check ownership unless admin
    if str(order["user_id"]) != str(current_user["id"]) and current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to view this order")
    
    return order
