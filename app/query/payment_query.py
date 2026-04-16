from app.query.base_query import BaseQuery
from supabase import Client
from typing import Dict, Any, Optional
from uuid import UUID

class PaymentQuery(BaseQuery):
    def __init__(self, client: Client):
        super().__init__(client, "payments")

    def get_order_owner(self, order_id: UUID) -> Optional[str]:
        res = self.client.table("orders").select("user_id").eq("id", str(order_id)).execute()
        return res.data[0]["user_id"] if res.data else None

    def record_payment(self, payment_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        # Set payment status to completed (simulation)
        payment_data["payment_status"] = "Completed"
        
        res = self.client.table("payments").insert(payment_data).execute()
        if not res.data:
            return None
            
        # Update Order Status
        self.client.table("orders").update({"payment_status": "Paid"}).eq("id", str(payment_data["order_id"])).execute()
        
        # Trigger Shipment (Automatic for MVP)
        shipment_dict = {
            "order_id": str(payment_data["order_id"]),
            "tracking_id": f"TRK-{str(payment_data['order_id'])[:8].upper()}",
            "shipment_status": "Processing"
        }
        self.client.table("shipments").insert(shipment_dict).execute()
        
        return res.data[0]
