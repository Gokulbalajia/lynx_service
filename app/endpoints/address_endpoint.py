from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from app.db.connection import get_supabase
from app.auth.auth import get_current_user
from app.models.address_model import AddressResponse, AddressCreate, AddressUpdate
from app.query.address_query import AddressQuery
from supabase import Client

router = APIRouter(prefix="/addresses", tags=["Addresses"])

@router.get("/", response_model=List[AddressResponse])
def get_addresses(current_user: dict = Depends(get_current_user), db: Client = Depends(get_supabase)):
    query = AddressQuery(db)
    return query.get_by_user(current_user["id"])

@router.post("/", response_model=AddressResponse)
def create_address(address: AddressCreate, current_user: dict = Depends(get_current_user), db: Client = Depends(get_supabase)):
    query = AddressQuery(db)
    addr_dict = address.model_dump(mode="json")
    addr_dict["user_id"] = str(current_user["id"])
    
    res = query.create_address(addr_dict)
    if not res:
        raise HTTPException(status_code=500, detail="Failed to create address")
    return res

@router.put("/{id}", response_model=AddressResponse)
def update_address(id: UUID, address: AddressUpdate, current_user: dict = Depends(get_current_user), db: Client = Depends(get_supabase)):
    query = AddressQuery(db)
    # Verify ownership
    owner_id = query.get_address_owner(id)
    if not owner_id or str(owner_id) != str(current_user["id"]):
        raise HTTPException(status_code=403, detail="Not authorized to update this address")
    
    res = query.update_address(id, address.model_dump(exclude_unset=True))
    return res

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_address(id: UUID, current_user: dict = Depends(get_current_user), db: Client = Depends(get_supabase)):
    query = AddressQuery(db)
    # Verify ownership
    owner_id = query.get_address_owner(id)
    if not owner_id or str(owner_id) != str(current_user["id"]):
        raise HTTPException(status_code=403, detail="Not authorized to delete this address")
    
    query.delete_address(id)
    return None
