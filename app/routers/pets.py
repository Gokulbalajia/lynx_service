from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from uuid import UUID
from app.core.supabase_client import get_supabase
from app.models.pet import PetResponse, PetCreate
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
    res = db.table("pets").select("*, images:pet_images(*)").eq("id", str(id)).single().execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Pet not found")
    return res.data
