from db.connect import MongoDBSingleton
from bson import ObjectId
from pymongo.errors import PyMongoError
from typing import List, Optional, Dict
from datetime import datetime
import uuid
from models.booking import Booking

db = MongoDBSingleton().get_database()
if db is not None:
    bookings_collection = db["bookings"]
    events_collection = db["events"]
else:
    bookings_collection = None
    events_collection = None

class BookingRepo:
    @staticmethod
    async def create_booking(booking_data: Booking) -> Optional[Dict]:
        print(f"create_bookinggggggg : {booking_data}")
        """
        Create a new booking in the database
        
        Args:
            booking_data (Booking): The booking data to be added
        
        Returns:
            Optional[Dict]: The newly created booking document with _id
            
        Raises:
            PyMongoError: If there's an error during database operation
            Exception: For any other unexpected errors
        """
        try:
            if bookings_collection is None or events_collection is None:
                raise Exception("Database connection not established")
            
            # Convert Pydantic model to dict
            booking_dict = booking_data
            print(f"booking_dict : {booking_data['event_id']}")
            # Generate booking number if not provided
            if "booking_number" not in booking_dict:
                booking_dict["booking_number"] = f"BK-{uuid.uuid4().hex[:8].upper()}"
            
            # Validate event exists
            event = events_collection.find_one({"_id": ObjectId(booking_data['event_id'])})
            if not event:
                raise Exception(f"Event with id {booking_data['event_id']} not found")
            
            # Insert the booking
            result = bookings_collection.insert_one(booking_dict)
            
            if result.inserted_id:
                # Fetch and return the newly created booking
                new_booking = bookings_collection.find_one(
                    {"_id": result.inserted_id}
                )
                return new_booking
            else:
                raise Exception("Failed to create booking")
                
        except PyMongoError as e:
            print(f"Database error occurred: {str(e)}")
            raise Exception(f"Database error occurred: {str(e)}")
        except Exception as e:
            print(f"Error creating booking: {str(e)}")
            raise Exception(f"Error creating booking: {str(e)}")

    @staticmethod
    async def get_user_bookings(user_id: str) -> List[Dict]:
        """
        Get all bookings for a specific user
        
        Args:
            user_id (str): The ID of the user
            
        Returns:
            List[Dict]: List of booking documents
            
        Raises:
            PyMongoError: If there's an error during database operation
            Exception: For any other unexpected errors
        """
        try:
            if bookings_collection is None:
                raise Exception("Database connection not established")
            
            if not ObjectId.is_valid(user_id):
                raise Exception("Invalid user ID format")
                
            cursor = bookings_collection.find(
                {"user_id": user_id}
            ).sort("created_at", -1)
            print(f"cursor : {cursor.count()}")
            tickets = []
            for ticket in cursor:
                print(f"ticket : {ticket}")
                tickets.append(ticket)        
            return tickets
            
        except PyMongoError as e:
            print(f"Database error occurred: {str(e)}")
            raise Exception(f"Database error occurred: {str(e)}")
        except Exception as e:
            print(f"Error retrieving bookings: {str(e)}")
            raise Exception(f"Error retrieving bookings: {str(e)}")

    @staticmethod
    async def get_event_bookings(event_id: str) -> List[Dict]:
        """
        Get all bookings for a specific event
        
        Args:
            event_id (str): The ID of the event
            
        Returns:
            List[Dict]: List of booking documents
            
        Raises:
            PyMongoError: If there's an error during database operation
            Exception: For any other unexpected errors
        """
        try:
            if bookings_collection is None:
                raise Exception("Database connection not established")
            
            if not ObjectId.is_valid(event_id):
                raise Exception("Invalid event ID format")
                
            cursor = bookings_collection.find(
                {"event_id": event_id}
            ).sort("created_at", -1)

            print(f"cursor : {cursor.count()}")
            tickets = []
            for ticket in cursor:
                print(f"ticket : {ticket}")
                tickets.append(ticket)
            
            return tickets
            
        except PyMongoError as e:
            print(f"Database error occurred: {str(e)}")
            raise Exception(f"Database error occurred: {str(e)}")
        except Exception as e:
            print(f"Error retrieving bookings: {str(e)}")
            raise Exception(f"Error retrieving bookings: {str(e)}")

    @staticmethod
    async def get_booking_by_id(booking_id: str) -> Optional[Dict]:
        """
        Get a specific booking by its ID
        
        Args:
            booking_id (str): The ID of the booking
            
        Returns:
            Optional[Dict]: The booking document if found, None otherwise
            
        Raises:
            PyMongoError: If there's an error during database operation
            Exception: For any other unexpected errors
        """
        try:
            if bookings_collection is None:
                raise Exception("Database connection not established")
            
            if not ObjectId.is_valid(booking_id):
                raise Exception("Invalid booking ID format")
                
            booking = bookings_collection.find_one({"_id": ObjectId(booking_id)})
            return booking
            
        except PyMongoError as e:
            print(f"Database error occurred: {str(e)}")
            raise Exception(f"Database error occurred: {str(e)}")
        except Exception as e:
            print(f"Error retrieving booking: {str(e)}")
            raise Exception(f"Error retrieving booking: {str(e)}")

    @staticmethod
    async def update_booking_status(booking_id: str, status: str) -> Optional[Dict]:
        """
        Update the status of a booking
        
        Args:
            booking_id (str): The ID of the booking
            status (str): The new status
            
        Returns:
            Optional[Dict]: The updated booking document if found, None otherwise
            
        Raises:
            PyMongoError: If there's an error during database operation
            Exception: For any other unexpected errors
        """
        try:
            if bookings_collection is None:
                raise Exception("Database connection not established")
            
            if not ObjectId.is_valid(booking_id):
                raise Exception("Invalid booking ID format")
                
            result = bookings_collection.update_one(
                {"_id": ObjectId(booking_id)},
                {
                    "$set": {
                        "status": status,
                        "updated_at": datetime.now()
                    }
                }
            )
            
            if result.modified_count == 0:
                return None
                
            updated_booking = bookings_collection.find_one(
                {"_id": ObjectId(booking_id)}
            )
            return updated_booking
            
        except PyMongoError as e:
            print(f"Database error occurred: {str(e)}")
            raise Exception(f"Database error occurred: {str(e)}")
        except Exception as e:
            print(f"Error updating booking: {str(e)}")
            raise Exception(f"Error updating booking: {str(e)}")

    @staticmethod
    async def update_booking_payment(
        booking_id: str, 
        payment_id: str, 
        ticket_id: Optional[str] = None
    ) -> Optional[Dict]:
        """
        Update the payment and ticket information of a booking
        
        Args:
            booking_id (str): The ID of the booking
            payment_id (str): The ID of the payment
            ticket_id (Optional[str]): The ID of the ticket
            
        Returns:
            Optional[Dict]: The updated booking document if found, None otherwise
            
        Raises:
            PyMongoError: If there's an error during database operation
            Exception: For any other unexpected errors
        """
        try:
            if bookings_collection is None:
                raise Exception("Database connection not established")
            
            if not ObjectId.is_valid(booking_id):
                raise Exception("Invalid booking ID format")
            
            update_dict = {
                "payment_id": ObjectId(payment_id),
                "updated_at": datetime.now()
            }
            
            if ticket_id:
                update_dict["ticket_id"] = ObjectId(ticket_id)
            
            result = await bookings_collection.update_one(
                {"_id": ObjectId(booking_id)},
                {"$set": update_dict}
            )
            
            if result.modified_count == 0:
                return None
                
            updated_booking = await bookings_collection.find_one(
                {"_id": ObjectId(booking_id)}
            )
            return updated_booking
            
        except PyMongoError as e:
            print(f"Database error occurred: {str(e)}")
            raise Exception(f"Database error occurred: {str(e)}")
        except Exception as e:
            print(f"Error updating booking: {str(e)}")
            raise Exception(f"Error updating booking: {str(e)}")

    @staticmethod
    async def delete_booking(booking_id: str) -> bool:
        """
        Delete a booking from the database
        
        Args:
            booking_id (str): The ID of the booking to delete
            
        Returns:
            bool: True if deletion was successful, False otherwise
            
        Raises:
            PyMongoError: If there's an error during database operation
            Exception: For any other unexpected errors
        """
        try:
            if bookings_collection is None:
                raise Exception("Database connection not established")
            
            if not ObjectId.is_valid(booking_id):
                raise Exception("Invalid booking ID format")
                
            result = bookings_collection.delete_one({"_id": ObjectId(booking_id)})
            return result.deleted_count > 0
            
        except PyMongoError as e:
            print(f"Database error occurred: {str(e)}")
            raise Exception(f"Database error occurred: {str(e)}")
        except Exception as e:
            print(f"Error deleting booking: {str(e)}")
            raise Exception(f"Error deleting booking: {str(e)}")