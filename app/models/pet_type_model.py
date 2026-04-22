from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class PetTypeBase(BaseModel):
    name: str

class PetTypeCreate(PetTypeBase):
    pass

class PetTypeResponse(PetTypeBase):
    id: UUID
    description: Optional[str] = None

class PetTypeUpdate(BaseModel):
    name: str
