from app.query.base_query import BaseQuery
from supabase import Client
from uuid import UUID
from typing import List, Dict, Any, Optional

class PetBreedQuery(BaseQuery):
    def __init__(self, client: Client):
        super().__init__(client, "pet_breeds")

    def get_all(self, query_params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        query = self.client.table(self.table_name).select("id,name,pet_type_id,pet_types(id,name)")
        if query_params:
            for key, value in query_params.items():
                query = query.eq(key, value)
        response = query.execute()
        return response.data

    def get_by_id(self, id: UUID) -> Optional[Dict[str, Any]]:
        response = self.client.table(self.table_name).select("id,name,pet_type_id,pet_types(id,name)").eq("id", str(id)).execute()
        return response.data[0] if response.data else None

    def create_pet_breed(self, data: dict):
        return self.create(data)

    def update_pet_breed(self, id: UUID, data: dict):
        return self.update(id, data)

    def delete_pet_breed(self, id: UUID):
        return self.delete(id)
