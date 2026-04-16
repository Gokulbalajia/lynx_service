from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class AddressBase(BaseModel):
    street: str
    city: str
    state: str
    country: str
    pincode: str
    is_default: bool = False

class AddressCreate(AddressBase):
    user_id: Optional[UUID] = None

class AddressResponse(AddressBase):
    id: UUID
    user_id: UUID
    created_at: datetime

class AddressUpdate(BaseModel):
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    pincode: Optional[str] = None
    is_default: Optional[bool] = None
