from typing import Optional, Dict
from schemas.paymentSchema import PaymentSchemaReq
from repository.payments_repo import PaymentRepo
import razorpay

class PaymentService:
    def __init__(self, client_id: str, client_secret: str):
        self.client = razorpay.Client(auth=(client_id, client_secret))

    async def create_payment(self, payment_data: PaymentSchemaReq) -> Dict:
        """
        Create a new payment and initiate Razorpay order
        
        Args:
            payment_data (PaymentSchemaReq): The payment data
            
        Returns:
            Dict: The newly created payment with Razorpay order details
            
        Raises:
            Exception: If there's an error creating the payment
        """
        print(f"create payment {payment_data}")
        try:
            # Create Razorpay order
            razorpay_order = self.client.order.create({
                "amount": int(payment_data.amount * 100),  # Amount in paise
                "currency": payment_data.currency,
                "payment_capture": 1
            })
            
            # Prepare payment data with Razorpay order details
            payment_record = {
                **payment_data.dict(),
                "status": "created",
                "razorpay_order_id": razorpay_order['id']
            }
            print(f"razorpay order {razorpay_order}")
            # Store payment in the database
            payment = await PaymentRepo.create_payment(payment_record)
            return payment
        except Exception as e:
            raise Exception(f"Error creating payment: {str(e)}")

    async def verify_payment(self, razorpay_payment_id: str, razorpay_order_id: str, razorpay_signature: str) -> bool:
        """
        Verify Razorpay payment signature
        
        Args:
            razorpay_payment_id (str): Razorpay payment ID
            razorpay_order_id (str): Razorpay order ID
            razorpay_signature (str): Razorpay signature
            
        Returns:
            bool: True if verification is successful, False otherwise
            
        Raises:
            Exception: If there's an error verifying the payment
        """
        try:
            # Verify payment signature
            self.client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            })
            return True
        except razorpay.errors.SignatureVerificationError:
            return False
        except Exception as e:
            raise Exception(f"Error verifying payment: {str(e)}")

    async def update_payment_status(self, payment_id: str, status: str) -> Optional[Dict]:
        """
        Update the status of a payment
        
        Args:
            payment_id (str): The ID of the payment
            status (str): The new status
            
        Returns:
            Optional[Dict]: The updated payment document if found, None otherwise
            
        Raises:
            Exception: If there's an error updating the payment status
        """
        try:
            return await PaymentRepo.update_payment_status(payment_id, status)
        except Exception as e:
            raise Exception(f"Error updating payment status: {str(e)}")