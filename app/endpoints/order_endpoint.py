from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from app.db.connection import get_supabase, get_supabase_admin
from app.auth.auth import get_current_user, admin_required
from app.models.order import OrderResponse, OrderCreate
from app.query.order_query import OrderQuery
from supabase import Client

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.get("/", response_model=List[OrderResponse])
def get_user_orders(current_user: dict = Depends(get_current_user), db: Client = Depends(get_supabase)):
    # Users can only see their own orders
    query = db.table("orders").select("*, items:order_items(*)").eq("user_id", str(current_user["id"]))
    res = query.execute()
    return res.data

@router.get("/admin/all", response_model=List[OrderResponse])
def get_all_orders(_admin: dict = Depends(admin_required), db: Client = Depends(get_supabase)):
    # Admins can see all orders
    res = db.table("orders").select("*, items:order_items(*)").execute()
    return res.data

@router.post("/checkout", response_model=OrderResponse)
def checkout(order_data: OrderCreate, current_user: dict = Depends(get_current_user), db: Client = Depends(get_supabase)):
    # Ensure user is creating an order for themselves
    if str(order_data.user_id) != str(current_user["id"]):
        raise HTTPException(status_code=403, detail="Cannot create order for another user")
    
    order_query = OrderQuery(db)
    return order_query.process_checkout(order_data)

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: UUID, current_user: dict = Depends(get_current_user), db: Client = Depends(get_supabase)):
    res = db.table("orders").select("*, items:order_items(*)").eq("id", str(order_id)).single().execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Check ownership unless admin
    if str(res.data["user_id"]) != str(current_user["id"]) and current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to view this order")
    
    return res.data
