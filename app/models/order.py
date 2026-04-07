from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from decimal import Decimal

class OrderItemBase(BaseModel):
    product_variant_id: Optional[UUID] = None
    pet_id: Optional[UUID] = None
    quantity: int = Field(..., ge=1)
    price: Decimal = Field(..., ge=0)

class OrderBase(BaseModel):
    address_id: UUID
    total_amount: Decimal = Field(0, ge=0)
    payment_status: str = "Pending"

class OrderCreate(OrderBase):
    user_id: Optional[UUID] = None
    items: List[OrderItemBase]

class OrderResponse(OrderBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    items: Optional[List[OrderItemBase]] = None

class PaymentBase(BaseModel):
    order_id: UUID
    payment_method: str
    transaction_id: Optional[str] = None
    payment_status: str = "Pending"

class PaymentResponse(PaymentBase):
    id: UUID
    paid_at: Optional[datetime] = None

class ShipmentBase(BaseModel):
    order_id: UUID
    tracking_id: Optional[str] = None
    shipment_status: str = "Processing"

class ShipmentResponse(ShipmentBase):
    id: UUID
    shipped_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
