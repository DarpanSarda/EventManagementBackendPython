from fastapi import APIRouter, HTTPException, Depends, status
from typing import Dict , List
from schemas.paymentSchema import PaymentSchemaReq, PaymentSchemaRes , VerifyPaymentSchema
from services.paymentService import PaymentService
from datetime import datetime

paymentrouter = APIRouter(
    prefix="/payments",
    tags=["payments"]
    # dependencies=[Depends(JWTBearer())]
)

# Initialize PaymentService with Razorpay credentials
# payment_service = PaymentService(client_id="rzp_test_nP3SqoPnodlV1N", client_secret="Odlne0wJUEmSL3e4DBZjFZWS")
payment_service = PaymentService()

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
async def verify_payment(payload : VerifyPaymentSchema):
    """
    Verify Razorpay payment
    """
    try:
        print(f"38 === > {payload.razorpay_payment_id}, {payload.razorpay_order_id}, {payload.razorpay_signature}")
        verified = await PaymentService.verify_payment(payload.razorpay_payment_id, payload.razorpay_order_id, payload.razorpay_signature)
        print(f"50 === > {verified}")
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
        updated_payment = await PaymentService.update_payment_status(payment_id, status)
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
    

def transform(doc: dict) -> dict:
    doc["_id"] = str(doc["_id"])
    doc["user_id"] = str(doc["user_id"])
    return doc


@paymentrouter.get("/", response_model=List[PaymentSchemaRes])
async def get_all_payments():
    print(f"17 hellooo")
    """
    Get all payments
    """
    try:
        payments = await PaymentService.get_all_payments()
        return [transform(p) for p in payments]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@paymentrouter.get("/{payment_id}", response_model=PaymentSchemaRes)
async def get_payment_by_id(payment_id: str):
    """
    Get a single payment by ID
    """
    try:
        payment = await PaymentService.get_payment_by_id(payment_id)
        if not payment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Payment with ID {payment_id} not found"
            )
        return transform(payment)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )