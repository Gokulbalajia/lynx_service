from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from uuid import UUID
from app.core.supabase_client import get_supabase
from app.models.product import ProductResponse, ProductCreate, ProductUpdate
from supabase import Client

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=List[ProductResponse])
def get_products(category_id: Optional[UUID] = None, db: Client = Depends(get_supabase)):
    query = db.table("products").select("*, details:product_details(*), variants:product_variants(*)")
    if category_id:
        query = query.eq("category_id", str(category_id))
    res = query.execute()
    return res.data

@router.get("/{id}", response_model=ProductResponse)
def get_product(id: UUID, db: Client = Depends(get_supabase)):
    res = db.table("products").select("*, details:product_details(*), variants:product_variants(*)").eq("id", str(id)).single().execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Product not found")
    return res.data

@router.post("/", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Client = Depends(get_supabase)):
    # This would typically involve multiple inserts for details and variants
    # For now, implementing the core product insert
    product_dict = product.model_dump(exclude={"details", "variants", "images"})
    res = db.table("products").insert(product_dict).execute()
    return res.data[0]
