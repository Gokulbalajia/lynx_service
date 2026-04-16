from app.query.base_query import BaseQuery
from supabase import Client
from typing import Dict, Any, Optional
from uuid import UUID

class ShipmentQuery(BaseQuery):
    def __init__(self, client: Client):
        super().__init__(client, "shipments")

    def get_shipment_by_order(self, order_id: UUID) -> Optional[Dict[str, Any]]:
        res = self.client.table("shipments").select("*").eq("order_id", str(order_id)).execute()
        return res.data[0] if res.data else None

    def get_order_owner(self, order_id: UUID) -> Optional[str]:
        res = self.client.table("orders").select("user_id").eq("id", str(order_id)).execute()
        return res.data[0]["user_id"] if res.data else None
