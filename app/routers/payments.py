from fastapi import APIRouter, Depends, HTTPException, status
from app.core.supabase_client import get_supabase
from app.core.dependencies import get_current_user
from app.models.order import PaymentBase, PaymentResponse
from supabase import Client

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("/", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
def process_payment(payment: PaymentBase, current_user: dict = Depends(get_current_user), db: Client = Depends(get_supabase)):
    # 1. Verify order exists and belongs to user
    order_res = db.table("orders").select("user_id").eq("id", str(payment.order_id)).execute()
    if not order_res.data:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if str(order_res.data[0]["user_id"]) != str(current_user["id"]):
        raise HTTPException(status_code=403, detail="Not authorized to pay for this order")
    
    # 2. Record Payment
    pay_dict = payment.model_dump(mode="json")
    pay_dict["payment_status"] = "Completed" # Simulating successful payment
    
    res = db.table("payments").insert(pay_dict).execute()
    if not res.data:
        raise HTTPException(status_code=500, detail="Failed to record payment")
    
    # 3. Update Order Status
    db.table("orders").update({"payment_status": "Paid"}).eq("id", str(payment.order_id)).execute()
    
    # 4. Trigger Shipment (Automatic for MVP)
    shipment_dict = {
        "order_id": str(payment.order_id),
        "tracking_id": f"TRK-{str(payment.order_id)[:8].upper()}",
        "shipment_status": "Processing"
    }
    db.table("shipments").insert(shipment_dict).execute()
    
    return res.data[0]
