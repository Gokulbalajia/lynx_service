from pydantic import BaseModel
from uuid import UUID

class PetTypeBase(BaseModel):
    name: str

class PetTypeCreate(PetTypeBase):
    pass

class PetTypeResponse(PetTypeBase):
    id: UUID

class PetTypeUpdate(BaseModel):
    name: str
