from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from uuid import UUID
from app.core.supabase_client import get_supabase
from app.core.dependencies import admin_required
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
    try:
        res = db.table("products").select("*, details:product_details(*), variants:product_variants(*)").eq("id", str(id)).single().execute()
        if not res.data:
            raise HTTPException(status_code=404, detail="Product not found")
        return res.data
    except Exception:
        raise HTTPException(status_code=404, detail="Product not found")

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Client = Depends(get_supabase), _admin=Depends(admin_required)):
    # core product insert
    product_dict = product.model_dump(exclude={"details", "variants", "images"})
    res = db.table("products").insert(product_dict).execute()
    if not res.data:
        raise HTTPException(status_code=500, detail="Failed to create product")
    return res.data[0]

@router.put("/{id}", response_model=ProductResponse)
def update_product(id: UUID, product: ProductUpdate, db: Client = Depends(get_supabase), _admin=Depends(admin_required)):
    product_dict = product.model_dump(exclude_unset=True, exclude={"details", "variants", "images"})
    res = db.table("products").update(product_dict).eq("id", str(id)).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Product not found")
    return res.data[0]

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: UUID, db: Client = Depends(get_supabase), _admin=Depends(admin_required)):
    res = db.table("products").delete().eq("id", str(id)).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Product not found")
    return None
