from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from uuid import UUID
from app.core.supabase_client import get_supabase
from app.core.dependencies import admin_required
from app.models.pet import PetResponse, PetCreate, PetUpdate
from supabase import Client

router = APIRouter(prefix="/pets", tags=["Pets"])

@router.get("/", response_model=List[PetResponse])
def get_pets(breed_id: Optional[UUID] = None, db: Client = Depends(get_supabase)):
    query = db.table("pets").select("*, images:pet_images(*)")
    if breed_id:
        query = query.eq("breed_id", str(breed_id))
    res = query.execute()
    return res.data

@router.get("/{id}", response_model=PetResponse)
def get_pet(id: UUID, db: Client = Depends(get_supabase)):
    try:
        res = db.table("pets").select("*, images:pet_images(*)").eq("id", str(id)).single().execute()
        if not res.data:
            raise HTTPException(status_code=404, detail="Pet not found")
        return res.data
    except Exception:
        raise HTTPException(status_code=404, detail="Pet not found")

@router.post("/", response_model=PetResponse, status_code=status.HTTP_201_CREATED)
def create_pet(pet: PetCreate, db: Client = Depends(get_supabase), _admin=Depends(admin_required)):
    pet_dict = pet.model_dump(mode="json", exclude={"images"})
    res = db.table("pets").insert(pet_dict).execute()
    if not res.data:
        raise HTTPException(status_code=500, detail="Failed to create pet")
    
    pet_id = res.data[0]["id"]

    # Insert Images
    if pet.images:
        for img in pet.images:
            i_dict = img.model_dump(mode="json")
            i_dict["pet_id"] = pet_id
            db.table("pet_images").insert(i_dict).execute()

    # Refetch full object
    return get_pet(pet_id, db)

@router.put("/{id}", response_model=PetResponse)
def update_pet(id: UUID, pet: PetUpdate, db: Client = Depends(get_supabase), _admin=Depends(admin_required)):
    # 1. Update Core Pet
    pet_dict = pet.model_dump(exclude_unset=True, exclude={"images"})
    if pet_dict:
        db.table("pets").update(pet_dict).eq("id", str(id)).execute()
    
    # 2. Replace Images
    if pet.images is not None:
        db.table("pet_images").delete().eq("pet_id", str(id)).execute()
        for img in pet.images:
            i_dict = img.model_dump(mode="json")
            i_dict["pet_id"] = str(id)
            db.table("pet_images").insert(i_dict).execute()

    return get_pet(id, db)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pet(id: UUID, db: Client = Depends(get_supabase), _admin=Depends(admin_required)):
    res = db.table("pets").delete().eq("id", str(id)).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Pet not found")
    return None
