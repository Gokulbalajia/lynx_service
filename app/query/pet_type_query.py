from app.query.base_query import BaseQuery
from supabase import Client
from uuid import UUID

class PetTypeQuery(BaseQuery):
    def __init__(self, client: Client):
        super().__init__(client, "pet_types")

    def update_pet_type(self, id: UUID, data: dict):
        return self.update(id, data)

    def delete_pet_type(self, id: UUID):
        return self.delete(id)
