from pydantic import BaseModel
from uuid import UUID

class PetBreedBase(BaseModel):
    name: str
    pet_type_id: UUID

class PetBreedResponse(PetBreedBase):
    id: UUID

class PetBreedCreate(PetBreedBase):
    pass

class PetBreedUpdate(BaseModel):
    name: str
