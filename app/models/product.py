from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date
from uuid import UUID
from decimal import Decimal

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: UUID
    created_at: datetime

class ProductImageBase(BaseModel):
    image_url: str
    is_primary: bool = False

class ProductVariantBase(BaseModel):
    sku: str
    price: Decimal = Field(..., ge=0)
    stock: int = Field(..., ge=0)

class ProductVariantCreate(ProductVariantBase):
    product_id: UUID

class ProductVariantResponse(ProductVariantBase):
    id: UUID
    product_id: UUID
    created_at: datetime

class ProductDetailBase(BaseModel):
    ingredients_material: Optional[str] = None
    pet_species_tags: Optional[List[str]] = None
    lifestyle_tags: Optional[List[str]] = None
    weight: Optional[str] = None
    flavor: Optional[str] = None
    expiry_date: Optional[date] = None

class ProductBase(BaseModel):
    name: str
    category_id: UUID
    short_description: Optional[str] = None
    brand: Optional[str] = None
    is_active: bool = True

class ProductCreate(ProductBase):
    details: Optional[ProductDetailBase] = None
    variants: Optional[List[ProductVariantBase]] = None
    images: Optional[List[ProductImageBase]] = None

class ProductResponse(ProductBase):
    id: UUID
    created_at: datetime
    details: Optional[ProductDetailBase] = None
    variants: Optional[List[ProductVariantResponse]] = None

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    category_id: Optional[UUID] = None
    short_description: Optional[str] = None
    brand: Optional[str] = None
    is_active: Optional[bool] = None
    details: Optional[ProductDetailBase] = None
    variants: Optional[List[ProductVariantBase]] = None
    images: Optional[List[ProductImageBase]] = None
