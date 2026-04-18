from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class PetTypeInfo(BaseModel):
    id: UUID
    name: str

class PetBreedBase(BaseModel):
    name: str
    pet_type_id: UUID

class PetBreedResponse(PetBreedBase):
    id: UUID
    pet_types: Optional[PetTypeInfo] = None

class PetBreedCreate(PetBreedBase):
    pass

class PetBreedUpdate(BaseModel):
    name: str
