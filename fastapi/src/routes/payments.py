from fastapi import APIRouter, HTTPException, Depends, status
from typing import Dict
from schemas.paymentSchema import PaymentSchemaReq, PaymentSchemaRes
from services.paymentService import PaymentService
from datetime import datetime

paymentrouter = APIRouter(
    prefix="/payments",
    tags=["payments"]
    # dependencies=[Depends(JWTBearer())]
)

# Initialize PaymentService with Razorpay credentials
payment_service = PaymentService(client_id="rzp_test_nP3SqoPnodlV1N", client_secret="Odlne0wJUEmSL3e4DBZjFZWS")

@paymentrouter.post("/", response_model=PaymentSchemaRes, status_code=status.HTTP_201_CREATED)
async def create_payment(payment: PaymentSchemaReq):
    print(f"17 {payment}")
    """
    Create a new payment and initiate Razorpay order
    """
    try:
        result = await payment_service.create_payment(payment)
        print(f"23 {result}")
        def transform(doc: dict) -> dict:
            doc["_id"] = str(doc["_id"])
            doc["user_id"] = str(doc["user_id"])
    
            # Add missing created_at if not present
            if "created_at" not in doc:
                doc["created_at"] = datetime.utcnow()  # or whatever timestamp logic you use

            return doc

        result = transform(result)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@paymentrouter.post("/verify", status_code=status.HTTP_200_OK)
async def verify_payment(razorpay_payment_id: str, razorpay_order_id: str, razorpay_signature: str):
    """
    Verify Razorpay payment
    """
    try:
        verified = await payment_service.verify_payment(razorpay_payment_id, razorpay_order_id, razorpay_signature)
        if not verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Payment verification failed"
            )
        return {"message": "Payment verified successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@paymentrouter.put("/{payment_id}/status", response_model=PaymentSchemaRes)
async def update_payment_status(payment_id: str, status: str):
    """
    Update payment status
    """
    try:
        updated_payment = await payment_service.update_payment_status(payment_id, status)
        if not updated_payment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Payment with ID {payment_id} not found"
            )
        def transform(doc: dict) -> dict:
            doc["_id"] = str(doc["_id"])
            doc["user_id"] = str(doc["user_id"])
    
            # Add missing created_at if not present
            if "created_at" not in doc:
                doc["created_at"] = datetime.utcnow()  # or whatever timestamp logic you use

            return doc
        updated_payment = transform(updated_payment)
        return updated_payment
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )