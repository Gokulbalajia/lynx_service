from app.query.base_query import BaseQuery
from supabase import Client
from uuid import UUID

class PetBreedQuery(BaseQuery):
    def __init__(self, client: Client):
        super().__init__(client, "pet_breeds")

    def create_pet_breed(self, data: dict):
        return self.create(data)

    def update_pet_breed(self, id: UUID, data: dict):
        return self.update(id, data)

    def delete_pet_breed(self, id: UUID):
        return self.delete(id)
