from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from uuid import UUID
from app.db.connection import get_supabase
from app.auth.auth import admin_required
from app.models.product_model import ProductResponse, ProductCreate, ProductUpdate
from app.query.product_query import ProductQuery
from supabase import Client

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=List[ProductResponse])
def get_products(category_id: Optional[UUID] = None, db: Client = Depends(get_supabase)):
    query = ProductQuery(db)
    return query.get_all_with_relations(category_id)

@router.get("/{id}", response_model=ProductResponse)
def get_product(id: UUID, db: Client = Depends(get_supabase)):
    query = ProductQuery(db)
    product = query.get_by_id_with_relations(id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Client = Depends(get_supabase), _admin=Depends(admin_required)):
    query = ProductQuery(db)
    
    product_dict = product.model_dump(mode="json", exclude={"details", "variants", "images"})
    details_dict = product.details.model_dump(mode="json") if product.details else None
    variants_list = [v.model_dump(mode="json") for v in product.variants] if product.variants else None
    images_list = [img.model_dump(mode="json") for img in product.images] if product.images else None

    res = query.create_product(product_dict, details_dict, variants_list, images_list)
    if not res:
        raise HTTPException(status_code=500, detail="Failed to create product")
    return res

@router.put("/{id}", response_model=ProductResponse)
def update_product(id: UUID, product: ProductUpdate, db: Client = Depends(get_supabase), _admin=Depends(admin_required)):
    query = ProductQuery(db)
    
    product_dict = product.model_dump(exclude_unset=True, exclude={"details", "variants", "images"})
    details_dict = product.details.model_dump(mode="json", exclude_unset=True) if product.details else None
    variants_list = [v.model_dump(mode="json") for v in product.variants] if product.variants is not None else None
    images_list = [img.model_dump(mode="json") for img in product.images] if product.images is not None else None

    return query.update_product(id, product_dict, details_dict, variants_list, images_list)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: UUID, db: Client = Depends(get_supabase), _admin=Depends(admin_required)):
    query = ProductQuery(db)
    res = query.delete_product(id)
    if not res:
        raise HTTPException(status_code=404, detail="Product not found")
    return None
