from app.query.base_query import BaseQuery
from supabase import Client
from typing import Dict, Any, List, Optional
from uuid import UUID

class CartQuery(BaseQuery):
    def __init__(self, client: Client):
        super().__init__(client, "cart")

    def get_by_user(self, user_id: UUID) -> List[Dict[str, Any]]:
        res = self.client.table("cart").select("*").eq("user_id", str(user_id)).execute()
        return res.data

    def create_item(self, cart_item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        res = self.client.table("cart").insert(cart_item).execute()
        return res.data[0] if res.data else None

    def update_item(self, id: UUID, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        res = self.client.table("cart").update(data).eq("id", str(id)).execute()
        return res.data[0] if res.data else None

    def remove_item(self, id: UUID):
        res = self.client.table("cart").delete().eq("id", str(id)).execute()
        return res.data if res.data else None

    def get_item_owner(self, id: UUID) -> Optional[str]:
        res = self.client.table("cart").select("user_id").eq("id", str(id)).execute()
        return res.data[0]["user_id"] if res.data else None
