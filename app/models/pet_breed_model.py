from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class PetTypeInfo(BaseModel):
    id: Optional[UUID] = None
    name: str

class PetBreedBase(BaseModel):
    name: str
    description: Optional[str] = None
    pet_type_id: Optional[UUID] = None

class PetBreedResponse(PetBreedBase):
    id: UUID
    pet_types: Optional[PetTypeInfo] = None

class PetBreedCreate(PetBreedBase):
    pass

class PetBreedUpdate(BaseModel):
    name: str
