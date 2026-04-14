from typing import List, Dict, Any
from uuid import UUID
from supabase import Client
from fastapi import HTTPException
from app.models.order import OrderCreate, OrderItemBase

class OrderQuery:
    def __init__(self, admin_client: Client):
        self.admin_client = admin_client

    def process_checkout(self, order_data: OrderCreate) -> Dict[str, Any]:
        try:
            # 1. Validate Stock
            for item in order_data.items:
                if item.product_variant_id:
                    variant_res = self.admin_client.table("product_variants").select("stock").eq("id", str(item.product_variant_id)).execute()
                    if not variant_res.data:
                        raise HTTPException(status_code=400, detail=f"Product variant {item.product_variant_id} not found")
                    if variant_res.data[0]["stock"] < item.quantity:
                        raise HTTPException(status_code=400, detail=f"Insufficient stock for product variant {item.product_variant_id}")
                
                if item.pet_id:
                    pet_res = self.admin_client.table("pets").select("stock, is_available").eq("id", str(item.pet_id)).execute()
                    if not pet_res.data:
                        raise HTTPException(status_code=400, detail=f"Pet {item.pet_id} not found")
                    pet = pet_res.data[0]
                    if not pet["is_available"] or pet["stock"] < item.quantity:
                        raise HTTPException(status_code=400, detail=f"Pet {item.pet_id} is no longer available")

            # 2. Create Order
            order_payload = {
                "user_id": str(order_data.user_id),
                "address_id": str(order_data.address_id),
                "total_amount": float(order_data.total_amount),
                "payment_status": order_data.payment_status
            }
            order_res = self.admin_client.table("orders").insert(order_payload).execute()
            if not order_res.data:
                raise Exception("Order data is empty")
            
            order_id = order_res.data[0]["id"]

            # 3. Create Order Items & Update Stock
            for item in order_data.items:
                item_payload = {
                    "order_id": order_id,
                    "product_variant_id": str(item.product_variant_id) if item.product_variant_id else None,
                    "pet_id": str(item.pet_id) if item.pet_id else None,
                    "quantity": item.quantity,
                    "price": float(item.price)
                }
                self.admin_client.table("order_items").insert(item_payload).execute()

                # Update Stock
                if item.product_variant_id:
                    self.admin_client.rpc("decrement_product_stock", {"variant_id": str(item.product_variant_id), "qty": int(item.quantity)}).execute()
                
                if item.pet_id:
                    self.admin_client.table("pets").update({"is_available": False, "stock": 0}).eq("id", str(item.pet_id)).execute()

            # 4. Clear Cart
            self.admin_client.table("cart").delete().eq("user_id", str(order_data.user_id)).execute()

            return order_res.data[0]
        except Exception as e:
            if isinstance(e, HTTPException): raise e
            raise HTTPException(status_code=500, detail=f"Checkout Process Error: {str(e)}")
