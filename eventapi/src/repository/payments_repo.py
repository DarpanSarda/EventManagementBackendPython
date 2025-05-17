from db.connect import MongoDBSingleton
from bson import ObjectId
from pymongo.errors import PyMongoError
from typing import Optional, Dict ,List
from datetime import datetime
from models.payment import Payment

db = MongoDBSingleton().get_database()
if db is not None:
    payments_collection = db["payments"]
else:
    payments_collection = None

class PaymentRepo:
    @staticmethod
    async def create_payment(payment_data: Payment) -> Optional[Dict]:
        """
        Create a new payment in the database
        
        Args:
            payment_data (Payment): The payment data to be added
        
        Returns:
            Optional[Dict]: The newly created payment document with _id
            
        Raises:
            PyMongoError: If there's an error during database operation
            Exception: For any other unexpected errors
        """
        try:
            if payments_collection is None:
                raise Exception("Database connection not established")
            
            # Convert Pydantic model to dict
            if isinstance(payment_data, dict):
                payment_dict = payment_data
            else:
                payment_dict = payment_data.dict(exclude_none=True, by_alias=True)

            
            # Insert the payment
            result = payments_collection.insert_one(payment_dict)
            
            if result.inserted_id:
                # Fetch and return the newly created payment
                new_payment = payments_collection.find_one(
                    {"_id": result.inserted_id}
                )
                return new_payment
            else:
                raise Exception("Failed to create payment")
                
        except PyMongoError as e:
            print(f"Database error occurred: {str(e)}")
            raise Exception(f"Database error occurred: {str(e)}")
        except Exception as e:
            print(f"Error creating payment: {str(e)}")
            raise Exception(f"Error creating payment: {str(e)}")
    
    @staticmethod
    async def get_payment_by_id(payment_id: str) -> Optional[Dict]:
        """
        Get a specific payment by its ID
        
        Args:
            payment_id (str): The ID of the payment
            
        Returns:
            Optional[Dict]: The payment document if found, None otherwise
            
        Raises:
            PyMongoError: If there's an error during database operation
            Exception: For any other unexpected errors
        """
        try:
            if payments_collection is None:
                raise Exception("Database connection not established")
            
            if not ObjectId.is_valid(payment_id):
                raise Exception("Invalid payment ID format")
                
            payment = await payments_collection.find_one({"_id": ObjectId(payment_id)})
            return payment
            
        except PyMongoError as e:
            print(f"Database error occurred: {str(e)}")
            raise Exception(f"Database error occurred: {str(e)}")
        except Exception as e:
            print(f"Error retrieving payment: {str(e)}")
            raise Exception(f"Error retrieving payment: {str(e)}")
    
    @staticmethod
    async def update_payment_status(payment_id: str, status: str) -> Optional[Dict]:
        """
        Update the status of a payment
        
        Args:
            payment_id (str): The ID of the payment
            status (str): The new status
            
        Returns:
            Optional[Dict]: The updated payment document if found, None otherwise
            
        Raises:
            PyMongoError: If there's an error during database operation
            Exception: For any other unexpected errors
        """
        try:
            if payments_collection is None:
                raise Exception("Database connection not established")
            
            if not ObjectId.is_valid(payment_id):
                raise Exception("Invalid payment ID format")
                
            result = payments_collection.update_one(
                {"_id": ObjectId(payment_id)},
                {"$set": {"status": status, "updated_at": datetime.now()}}
            )
            
            if result.modified_count == 0:
                return None
                
            updated_payment = payments_collection.find_one({"_id": ObjectId(payment_id)})
            return updated_payment
            
        except PyMongoError as e:
            print(f"Database error occurred: {str(e)}")
            raise Exception(f"Database error occurred: {str(e)}")
        except Exception as e:
            print(f"Error updating payment: {str(e)}")
            raise Exception(f"Error updating payment: {str(e)}")
        
    
    async def get_all_payments() -> List[dict]:
        payments_cursor = payments_collection.find({})
        payments = []
        for payment in payments_cursor:
            payments.append(payment)
        return payments

    async def get_payment_by_id(payment_id: str) -> Optional[dict]:
        return await payments_collection.find_one({"_id": ObjectId(payment_id)})