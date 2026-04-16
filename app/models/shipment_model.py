from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class ShipmentBase(BaseModel):
    order_id: UUID
    tracking_id: Optional[str] = None
    shipment_status: str = "Processing"

class ShipmentResponse(ShipmentBase):
    id: UUID
    shipped_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
