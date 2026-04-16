from app.query.base_query import BaseQuery
from supabase import Client
from typing import Dict, Any, List, Optional
from uuid import UUID

class AddressQuery(BaseQuery):
    def __init__(self, client: Client):
        super().__init__(client, "addresses")

    def get_by_user(self, user_id: UUID) -> List[Dict[str, Any]]:
        res = self.client.table("addresses").select("*").eq("user_id", str(user_id)).execute()
        return res.data

    def create_address(self, address_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        res = self.client.table("addresses").insert(address_data).execute()
        return res.data[0] if res.data else None

    def update_address(self, id: UUID, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        res = self.client.table("addresses").update(data).eq("id", str(id)).execute()
        return res.data[0] if res.data else None

    def delete_address(self, id: UUID):
        res = self.client.table("addresses").delete().eq("id", str(id)).execute()
        return res.data if res.data else None

    def get_address_owner(self, id: UUID) -> Optional[str]:
        res = self.client.table("addresses").select("user_id").eq("id", str(id)).execute()
        return res.data[0]["user_id"] if res.data else None
