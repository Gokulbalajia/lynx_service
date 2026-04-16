from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from typing import List
from app.db.connection import get_supabase
from app.query.category_query import CategoryQuery
from app.models.category_model import CategoryBase, CategoryResponse, CategoryCreate
from supabase import Client

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("/", response_model=List[CategoryResponse])
def get_categories(db: Client = Depends(get_supabase)):
    query = CategoryQuery(db)
    return query.get_all_categories()

@router.get("/{id}", response_model=CategoryResponse)
def get_category(id: UUID, db: Client = Depends(get_supabase)):
    query = CategoryQuery(db)
    category = query.get_category_by_id(id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(category_data: CategoryCreate, db: Client = Depends(get_supabase)):
    query = CategoryQuery(db)
    try:
        return query.create_category(category_data.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{id}")
def update_category(id: UUID, category_data: CategoryBase, db: Client = Depends(get_supabase)):
    query = CategoryQuery(db)
    category = query.get_by_id(id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    try:
        query.update_category(id, category_data.model_dump())
        return {"message": "Category updated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{id}")
def delete_category(id: UUID, db: Client = Depends(get_supabase)):
    query = CategoryQuery(db)
    category = query.get_by_id(id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    try:
        query.delete_category(id)
        return {"message": "Category deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
