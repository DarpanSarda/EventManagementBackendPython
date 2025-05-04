from typing import Optional, Dict , List
from schemas.paymentSchema import PaymentSchemaReq
from repository.payments_repo import PaymentRepo
import razorpay
from razorpay.errors import SignatureVerificationError
import os
from dotenv import load_dotenv

class PaymentService:
    def __init__(self):
        client_id ="rzp_test_rJSE0fMsM9i0lv"
        client_secret = "bowX7pTbpno8sbVFugSpcHGo"
        self.client = razorpay.Client(auth=(client_id, client_secret))
        print(f"client_id {client_id} , client_secret {client_secret}")
        print(f"selct client {self.client}")
        
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
            if not payment_data.amount or payment_data.amount <= 0:
                raise ValueError("Amount must be greater than 0")
            
            if not payment_data.currency or payment_data.currency not in ["INR", "USD"]:
                raise ValueError("Invalid currency. Supported currencies: INR, USD")

            amount = int(payment_data.amount * 100)  # Convert to paise
            currency = payment_data.currency
            print(f"amount {amount} , currency {currency}")
            # Create Razorpay order
            order_data = {
            "amount": amount,
            "currency": currency,
            "payment_capture": 1,
            "notes": {
                "payment_for": "Event Registration"
            }
            }
        
            print(f"Attempting to create Razorpay order with data: {order_data}")
            try:
                razorpay_order = self.client.order.create(
                    data = order_data
                )   
                print(f"Razorpay order created successfully: {razorpay_order}")
            except Exception as razorpay_error:
                print(f"Error creating Razorpay order: {razorpay_error}")
                raise Exception("Failed to create Razorpay order") 
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
        print(f"verify payment {razorpay_payment_id}, {razorpay_order_id}, {razorpay_signature}")
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
        
    async def get_all_payments(self) -> List[Dict]:
        print("get all payments")
        return await PaymentRepo.get_all_payments()
    
    async def get_payment_by_id(self,payment_id: str) -> Optional[Dict]:
        return await PaymentRepo.get_payment_by_id(payment_id)