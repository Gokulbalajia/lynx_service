from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class PaymentBase(BaseModel):
    order_id: UUID
    payment_method: str
    transaction_id: Optional[str] = None
    payment_status: str = "Pending"

class PaymentResponse(PaymentBase):
    id: UUID
    paid_at: Optional[datetime] = None
