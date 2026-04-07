from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from decimal import Decimal

class PetTypeBase(BaseModel):
    name: str

class PetTypeResponse(PetTypeBase):
    id: UUID

class PetBreedBase(BaseModel):
    name: str
    pet_type_id: UUID

class PetBreedResponse(PetBreedBase):
    id: UUID

class PetImageBase(BaseModel):
    image_url: str
    is_primary: bool = False

class PetBase(BaseModel):
    name: str
    pet_type_id: UUID
    breed_id: UUID
    age_months: Optional[int] = Field(None, ge=0)
    gender: Optional[str] = None
    price: Decimal = Field(..., ge=0)
    stock: int = Field(1, ge=0)
    description: Optional[str] = None
    is_available: bool = True

class PetCreate(PetBase):
    images: Optional[List[PetImageBase]] = None

class PetResponse(PetBase):
    id: UUID
    created_at: datetime
    images: Optional[List[PetImageBase]] = None

class PetUpdate(BaseModel):
    name: Optional[str] = None
    pet_type_id: Optional[UUID] = None
    breed_id: Optional[UUID] = None
    age_months: Optional[int] = Field(None, ge=0)
    gender: Optional[str] = None
    price: Optional[Decimal] = Field(None, ge=0)
    stock: Optional[int] = Field(None, ge=0)
    description: Optional[str] = None
    is_available: Optional[bool] = None
