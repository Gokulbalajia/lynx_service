from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from app.db.connection import get_supabase
from app.auth.auth import get_current_user
from app.models.address import AddressResponse, AddressCreate, AddressUpdate
from supabase import Client

router = APIRouter(prefix="/addresses", tags=["Addresses"])

@router.get("/", response_model=List[AddressResponse])
def get_addresses(current_user: dict = Depends(get_current_user), db: Client = Depends(get_supabase)):
    res = db.table("addresses").select("*").eq("user_id", str(current_user["id"])).execute()
    return res.data

@router.post("/", response_model=AddressResponse)
def create_address(address: AddressCreate, current_user: dict = Depends(get_current_user), db: Client = Depends(get_supabase)):
    addr_dict = address.model_dump(mode="json")
    addr_dict["user_id"] = str(current_user["id"])
    
    res = db.table("addresses").insert(addr_dict).execute()
    if not res.data:
        raise HTTPException(status_code=500, detail="Failed to create address")
    return res.data[0]

@router.put("/{id}", response_model=AddressResponse)
def update_address(id: UUID, address: AddressUpdate, current_user: dict = Depends(get_current_user), db: Client = Depends(get_supabase)):
    # Verify ownership
    existing = db.table("addresses").select("user_id").eq("id", str(id)).execute()
    if not existing.data or str(existing.data[0]["user_id"]) != str(current_user["id"]):
        raise HTTPException(status_code=403, detail="Not authorized to update this address")
    
    res = db.table("addresses").update(address.model_dump(exclude_unset=True)).eq("id", str(id)).execute()
    return res.data[0]

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_address(id: UUID, current_user: dict = Depends(get_current_user), db: Client = Depends(get_supabase)):
    # Verify ownership
    existing = db.table("addresses").select("user_id").eq("id", str(id)).execute()
    if not existing.data or str(existing.data[0]["user_id"]) != str(current_user["id"]):
        raise HTTPException(status_code=403, detail="Not authorized to delete this address")
    
    db.table("addresses").delete().eq("id", str(id)).execute()
    return None
