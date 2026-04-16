from app.query.base_query import BaseQuery
from supabase import Client
from typing import Dict, Any, List, Optional
from uuid import UUID

class PetQuery(BaseQuery):
    def __init__(self, client: Client):
        super().__init__(client, "pets")

    def get_all_with_relations(self, breed_id: Optional[UUID] = None) -> List[Dict[str, Any]]:
        query = self.client.table("pets").select("*, images:pet_images(*)")
        if breed_id:
            query = query.eq("breed_id", str(breed_id))
        res = query.execute()
        return res.data

    def get_by_id_with_relations(self, id: UUID) -> Optional[Dict[str, Any]]:
        res = self.client.table("pets").select("*, images:pet_images(*)").eq("id", str(id)).execute()
        return res.data[0] if res.data else None

    def create_pet(self, pet_dict: Dict[str, Any], images: Optional[List[Dict[str, Any]]]):
        res = self.client.table("pets").insert(pet_dict).execute()
        if not res.data:
            return None
        
        pet_id = res.data[0]["id"]

        if images:
            for img in images:
                img["pet_id"] = pet_id
                self.client.table("pet_images").insert(img).execute()

        return self.get_by_id_with_relations(pet_id)

    def update_pet(self, id: UUID, pet_dict: Dict[str, Any], images: Optional[List[Dict[str, Any]]]):
        if pet_dict:
            self.client.table("pets").update(pet_dict).eq("id", str(id)).execute()
        
        if images is not None:
            self.client.table("pet_images").delete().eq("pet_id", str(id)).execute()
            for img in images:
                img["pet_id"] = str(id)
                self.client.table("pet_images").insert(img).execute()

        return self.get_by_id_with_relations(id)

    def delete_pet(self, id: UUID):
        res = self.client.table("pets").delete().eq("id", str(id)).execute()
        return res.data if res.data else None
