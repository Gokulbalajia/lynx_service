from app.query.base_query import BaseQuery
from supabase import Client

class UserQuery(BaseQuery):
    def __init__(self, client: Client):
        super().__init__(client, "users")
