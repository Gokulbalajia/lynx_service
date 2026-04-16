from app.query.base_query import BaseQuery
from supabase import Client
from uuid import UUID

class UserQuery(BaseQuery):
    def __init__(self, client: Client):
        super().__init__(client, "users")

    def get_user_by_id(self, user_id: UUID):
        return self.get_by_id(user_id)
