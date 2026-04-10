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
    query = db.table("products").select("*, details:product_details(*), variants:product_variants(*), images:product_images(*)")
    if category_id:
        query = query.eq("category_id", str(category_id))
    res = query.execute()
    return res.data

@router.get("/{id}", response_model=ProductResponse)
def get_product(id: UUID, db: Client = Depends(get_supabase)):
    try:
        res = db.table("products").select("*, details:product_details(*), variants:product_variants(*), images:product_images(*)").eq("id", str(id)).single().execute()
        if not res.data:
            raise HTTPException(status_code=404, detail="Product not found")
        return res.data
    except Exception:
        raise HTTPException(status_code=404, detail="Product not found")

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Client = Depends(get_supabase), _admin=Depends(admin_required)):
    # core product insert
    product_dict = product.model_dump(mode="json", exclude={"details", "variants", "images"})
    res = db.table("products").insert(product_dict).execute()
    if not res.data:
        raise HTTPException(status_code=500, detail="Failed to create product")
    
    product_id = res.data[0]["id"]

    # Insert Details
    if product.details:
        details_dict = product.details.model_dump(mode="json")
        details_dict["product_id"] = product_id
        db.table("product_details").insert(details_dict).execute()
    
    # Insert Variants
    if product.variants:
        for variant in product.variants:
            v_dict = variant.model_dump(mode="json")
            v_dict["product_id"] = product_id
            db.table("product_variants").insert(v_dict).execute()
            
    # Insert Images
    if product.images:
        for img in product.images:
            i_dict = img.model_dump(mode="json")
            i_dict["product_id"] = product_id
            db.table("product_images").insert(i_dict).execute()

    # Refetch full object
    return get_product(product_id, db)

@router.put("/{id}", response_model=ProductResponse)
def update_product(id: UUID, product: ProductUpdate, db: Client = Depends(get_supabase), _admin=Depends(admin_required)):
    # 1. Update Core Product
    product_dict = product.model_dump(exclude_unset=True, exclude={"details", "variants", "images"})
    if product_dict:
        db.table("products").update(product_dict).eq("id", str(id)).execute()
    
    # 2. Update Details (Upsert style)
    if product.details is not None:
        details_dict = product.details.model_dump(mode="json", exclude_unset=True)
        details_dict["product_id"] = str(id)
        db.table("product_details").upsert(details_dict, on_conflict="product_id").execute()
    
    # 3. Replace Variants
    if product.variants is not None:
        db.table("product_variants").delete().eq("product_id", str(id)).execute()
        for variant in product.variants:
            v_dict = variant.model_dump(mode="json")
            v_dict["product_id"] = str(id)
            db.table("product_variants").insert(v_dict).execute()
            
    # 4. Replace Images
    if product.images is not None:
        db.table("product_images").delete().eq("product_id", str(id)).execute()
        for img in product.images:
            i_dict = img.model_dump(mode="json")
            i_dict["product_id"] = str(id)
            db.table("product_images").insert(i_dict).execute()

    return get_product(id, db)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: UUID, db: Client = Depends(get_supabase), _admin=Depends(admin_required)):
    res = db.table("products").delete().eq("id", str(id)).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Product not found")
    return None
