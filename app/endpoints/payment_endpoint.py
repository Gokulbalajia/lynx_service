from fastapi import APIRouter, Depends, HTTPException, status
from app.db.connection import get_supabase
from app.auth.auth import get_current_user
from app.models.payment_model import PaymentBase, PaymentResponse
from app.query.payment_query import PaymentQuery
from supabase import Client

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("/", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
def process_payment(payment: PaymentBase, current_user: dict = Depends(get_current_user), db: Client = Depends(get_supabase)):
    query = PaymentQuery(db)
    
    # Verify order owner
    owner_id = query.get_order_owner(payment.order_id)
    if not owner_id:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if str(owner_id) != str(current_user["id"]):
        raise HTTPException(status_code=403, detail="Not authorized to pay for this order")
    
    res = query.record_payment(payment.model_dump(mode="json"))
    if not res:
        raise HTTPException(status_code=500, detail="Failed to record payment")
    
    return res
