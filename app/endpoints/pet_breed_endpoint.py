from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from app.db.connection import get_supabase
from app.query.pet_breed_query import PetBreedQuery
from app.models.pet_breed_model import PetBreedResponse, PetBreedCreate, PetBreedUpdate
from supabase import Client

router = APIRouter(prefix="/pet-breeds", tags=["Pet Breeds"])

@router.get("/", response_model=List[PetBreedResponse])
def get_all(db: Client = Depends(get_supabase)):
    query = PetBreedQuery(db)
    return query.get_all()

@router.get("/{id}", response_model=PetBreedResponse)
def get_one(id: UUID, db: Client = Depends(get_supabase)):
    query = PetBreedQuery(db)
    item = query.get_by_id(id)
    if not item:
        raise HTTPException(status_code=404, detail="Pet breed not found")
    return item

@router.post("/", response_model=PetBreedResponse, status_code=status.HTTP_201_CREATED)
def create_pet_breed(data: PetBreedCreate, db: Client = Depends(get_supabase)):
    query = PetBreedQuery(db)
    return query.create_pet_breed(data.model_dump(mode="json"))

@router.put("/{id}", response_model=PetBreedResponse)
def update_pet_breed(id: UUID, data: PetBreedUpdate, db: Client = Depends(get_supabase)):
    query = PetBreedQuery(db)
    item = query.get_by_id(id)
    if not item:
        raise HTTPException(status_code=404, detail="Pet breed not found")
    
    try:
        query.update_pet_breed(id, data.model_dump(mode="json"))
        return query.get_by_id(id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{id}")
def delete_pet_breed(id: UUID, db: Client = Depends(get_supabase)):
    query = PetBreedQuery(db)
    item = query.get_by_id(id)
    if not item:
        raise HTTPException(status_code=404, detail="Pet breed not found")
    
    try:
        query.delete_pet_breed(id)
        return {"message": "Pet breed deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
