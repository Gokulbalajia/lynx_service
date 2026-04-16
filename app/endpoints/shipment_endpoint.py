from fastapi import APIRouter, Depends, HTTPException
from app.db.connection import get_supabase
from app.auth.auth import get_current_user
from app.models.shipment_model import ShipmentResponse
from app.query.shipment_query import ShipmentQuery
from supabase import Client
from uuid import UUID

router = APIRouter(prefix="/shipments", tags=["Shipments"])

@router.get("/{order_id}", response_model=ShipmentResponse)
def get_shipment_status(order_id: UUID, current_user: dict = Depends(get_current_user), db: Client = Depends(get_supabase)):
    query = ShipmentQuery(db)
    
    shipment = query.get_shipment_by_order(order_id)
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found for this order")
    
    # Check ownership
    owner_id = query.get_order_owner(order_id)
    if not owner_id or str(owner_id) != str(current_user["id"]):
        if current_user.get("role") != "admin":
            raise HTTPException(status_code=403, detail="Not authorized to view this shipment")
            
    return shipment
