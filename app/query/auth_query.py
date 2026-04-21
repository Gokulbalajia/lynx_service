from app.query.base_query import BaseQuery
from supabase import Client
from typing import Dict, Any

class AuthQuery(BaseQuery):
    def __init__(self, client: Client):
        super().__init__(client, "users")

    def get_by_email(self, email: str):
        res = self.client.table("users").select("*, roles(name)").eq("email", email).execute()
        return res.data[0] if res.data else None

    def create_user(self, user_data: Dict[str, Any]):
        res = self.client.table("users").insert(user_data).execute()
        return res.data[0] if res.data else None

    def get_role_name(self, role_id: int):
        role_res = self.client.table("roles").select("name").eq("id", role_id).execute()
        return role_res.data[0]["name"] if role_res.data else "user"
