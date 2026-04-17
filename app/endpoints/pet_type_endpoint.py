from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from app.db.connection import get_supabase
from app.query.pet_type_query import PetTypeQuery
from app.models.pet_type_model import PetTypeResponse, PetTypeCreate, PetTypeUpdate
from supabase import Client

router = APIRouter(prefix="/pet-types", tags=["Pet Types"])

@router.get("/", response_model=List[PetTypeResponse])
def get_all(db: Client = Depends(get_supabase)):
    query = PetTypeQuery(db)
    return query.get_all()

@router.get("/{id}", response_model=PetTypeResponse)
def get_one(id: UUID, db: Client = Depends(get_supabase)):
    query = PetTypeQuery(db)
    item = query.get_by_id(id)
    if not item:
        raise HTTPException(status_code=404, detail="Pet type not found")
    return item

@router.post("/", response_model=PetTypeResponse, status_code=status.HTTP_201_CREATED)
def create_pet_type(data: PetTypeCreate, db: Client = Depends(get_supabase)):
    query = PetTypeQuery(db)
    return query.create(data.model_dump(mode="json"))

@router.put("/{id}", response_model=PetTypeResponse)
def update_pet_type(id: UUID, data: PetTypeUpdate, db: Client = Depends(get_supabase)):
    query = PetTypeQuery(db)
    # Check if category exists
    item = query.get_by_id(id)
    if not item:
        raise HTTPException(status_code=404, detail="Pet type not found")
    
    try:
        query.update_pet_type(id, data.model_dump(mode="json"))
        return query.get_by_id(id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{id}")
def delete_pet_type(id: UUID, db: Client = Depends(get_supabase)):
    query = PetTypeQuery(db)
    # Check if category exists
    item = query.get_by_id(id)
    if not item:
        raise HTTPException(status_code=404, detail="Pet type not found")
    
    try:
        query.delete_pet_type(id)
        return {"message": "Pet type deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
