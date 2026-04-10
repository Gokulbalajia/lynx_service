from fastapi import APIRouter, Depends, HTTPException
from app.core.supabase_client import get_supabase
from app.core.dependencies import get_current_user
from app.models.order import ShipmentResponse
from supabase import Client
from uuid import UUID

router = APIRouter(prefix="/shipments", tags=["Shipments"])

@router.get("/{order_id}", response_model=ShipmentResponse)
def get_shipment_status(order_id: UUID, current_user: dict = Depends(get_current_user), db: Client = Depends(get_supabase)):
    res = db.table("shipments").select("*").eq("order_id", str(order_id)).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Shipment not found for this order")
    
    # Check ownership (fetch order user_id)
    order_res = db.table("orders").select("user_id").eq("id", str(order_id)).execute()
    if not order_res.data or str(order_res.data[0]["user_id"]) != str(current_user["id"]):
        if current_user.get("role") != "admin":
            raise HTTPException(status_code=403, detail="Not authorized to view this shipment")
            
    return res.data[0]
