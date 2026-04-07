from fastapi import APIRouter, Depends, HTTPException
from typing import List
from uuid import UUID
from app.core.supabase_client import get_supabase, get_supabase_admin
from app.models.order import OrderResponse, OrderCreate
from app.services.checkout_service import CheckoutService
from supabase import Client

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.get("/{user_id}", response_model=List[OrderResponse])
def get_user_orders(user_id: UUID, db: Client = Depends(get_supabase)):
    res = db.table("orders").select("*, items:order_items(*)").eq("user_id", str(user_id)).execute()
    return res.data

@router.post("/checkout", response_model=OrderResponse)
def checkout(order_data: OrderCreate, db_admin: Client = Depends(get_supabase_admin)):
    checkout_service = CheckoutService(db_admin)
    return checkout_service.process_checkout(order_data)
