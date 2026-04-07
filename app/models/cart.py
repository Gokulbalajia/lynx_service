from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime

class CartBase(BaseModel):
    item_type: str = Field(..., pattern="^(product|pet)$")
    product_variant_id: Optional[UUID] = None
    pet_id: Optional[UUID] = None
    quantity: int = Field(1, ge=1)

class CartCreate(CartBase):
    user_id: Optional[UUID] = None

class CartResponse(CartBase):
    id: UUID
    user_id: UUID
    created_at: datetime
