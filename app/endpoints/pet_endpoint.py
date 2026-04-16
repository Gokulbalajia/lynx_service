from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from uuid import UUID
from app.db.connection import get_supabase
from app.auth.auth import admin_required
from app.models.pet_model import PetResponse, PetCreate, PetUpdate
from app.query.pet_query import PetQuery
from supabase import Client

router = APIRouter(prefix="/pets", tags=["Pets"])

@router.get("/", response_model=List[PetResponse])
def get_pets(breed_id: Optional[UUID] = None, db: Client = Depends(get_supabase)):
    query = PetQuery(db)
    return query.get_all_with_relations(breed_id)

@router.get("/{id}", response_model=PetResponse)
def get_pet(id: UUID, db: Client = Depends(get_supabase)):
    query = PetQuery(db)
    pet = query.get_by_id_with_relations(id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    return pet

@router.post("/", response_model=PetResponse, status_code=status.HTTP_201_CREATED)
def create_pet(pet: PetCreate, db: Client = Depends(get_supabase), _admin=Depends(admin_required)):
    query = PetQuery(db)
    pet_dict = pet.model_dump(mode="json", exclude={"images"})
    images_list = [img.model_dump(mode="json") for img in pet.images] if pet.images else None

    res = query.create_pet(pet_dict, images_list)
    if not res:
        raise HTTPException(status_code=500, detail="Failed to create pet")
    return res

@router.put("/{id}", response_model=PetResponse)
def update_pet(id: UUID, pet: PetUpdate, db: Client = Depends(get_supabase), _admin=Depends(admin_required)):
    query = PetQuery(db)
    pet_dict = pet.model_dump(exclude_unset=True, exclude={"images"})
    images_list = [img.model_dump(mode="json") for img in pet.images] if pet.images is not None else None

    return query.update_pet(id, pet_dict, images_list)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pet(id: UUID, db: Client = Depends(get_supabase), _admin=Depends(admin_required)):
    query = PetQuery(db)
    res = query.delete_pet(id)
    if not res:
        raise HTTPException(status_code=404, detail="Pet not found")
    return None
