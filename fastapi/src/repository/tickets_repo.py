from db.connect import MongoDBSingleton
from bson import ObjectId
from schemas.ticketSchema import TicketSchemaReq
from pymongo.errors import PyMongoError
from typing import List, Optional, Dict
from datetime import datetime
import uuid

db = MongoDBSingleton().get_database()
if db is not None:
    tickets_collection = db["tickets"]
    events_collection = db["events"]
else:
    tickets_collection = None
    events_collection = None

class TicketsRepo:
    @staticmethod
    async def create_ticket(ticket_data: TicketSchemaReq) -> Optional[Dict]:
        print(f"Creating ticket with data: {ticket_data}")
        """
        Create a new ticket in the database
        
        Args:
            ticket_data (TicketSchemaReq): The ticket data to be added
        
        Returns:
            Optional[Dict]: The newly created ticket document with _id
            
        Raises:
            PyMongoError: If there's an error during database operation
            Exception: For any other unexpected errors
        """
        try:
            if tickets_collection is None or events_collection is None:
                raise Exception("Database connection not established")
            
            # Convert Pydantic model to dict
            ticket_dict = ticket_data.dict(exclude_none=True, by_alias=True)
            print(f"Ticket dict: {ticket_dict}")
            # Validate event exists
            if not ObjectId.is_valid(ticket_data.event):
                raise Exception("Invalid event ID format")
                
            event = events_collection.find_one({"_id": ObjectId(ticket_data.event)})
            print(f"Event found: {event}")
            if not event:
                raise Exception(f"Event with id {ticket_data.event} not found")
            
            # Generate ticket number
            ticket_number = f"TKT-{uuid.uuid4().hex[:8].upper()}"
            print(f"Generated ticket number: {ticket_number}")
            # Create complete ticket document
            complete_ticket = {
                **ticket_dict,
                "status": "pending",
                "purchase_date": datetime.now(),
                "ticket_number": ticket_number,
                "payment_status": "pending",
                "qr_code": None  # Will be generated later
            }
            
            # Insert the ticket
            result = tickets_collection.insert_one(complete_ticket)
            print(f"Insert result: {result}")
            if result.inserted_id:
                # Fetch and return the newly created ticket
                new_ticket = tickets_collection.find_one(
                    {"_id": result.inserted_id}
                )
                print(f"New ticket: {new_ticket}")
                return new_ticket
            else:
                raise Exception("Failed to create ticket")
                
        except PyMongoError as e:
            print(f"Database error occurred: {str(e)}")
            raise Exception(f"Database error occurred: {str(e)}")
        except Exception as e:
            print(f"Error creating ticket: {str(e)}")
            raise Exception(f"Error creating ticket: {str(e)}")
    
    @staticmethod
    async def get_tickets_by_user(user_id: str) -> List[Dict]:
        """
        Get all tickets for a specific user
        
        Args:
            user_id (str): The ID of the user
            
        Returns:
            List[Dict]: List of ticket documents
            
        Raises:
            PyMongoError: If there's an error during database operation
            Exception: For any other unexpected errors
        """
        print(f"Getting tickets for user with ID: {user_id}")
        try:
            if tickets_collection is None:
                raise Exception("Database connection not established")
            
            if not ObjectId.is_valid(user_id):
                raise Exception("Invalid user ID format")
                
            cursor = tickets_collection.find({"user": user_id})
            tickets = []
            for ticket in cursor:
                tickets.append(ticket)
            print(f"Tickets found: {tickets}")
            return tickets
            
        except PyMongoError as e:
            print(f"Database error occurred: {str(e)}")
            raise Exception(f"Database error occurred: {str(e)}")
        except Exception as e:
            print(f"Error retrieving tickets: {str(e)}")
            raise Exception(f"Error retrieving tickets: {str(e)}")

    @staticmethod
    async def get_tickets_by_event(event_id: str) -> List[Dict]:
        """
        Get all tickets for a specific event
        
        Args:
            event_id (str): The ID of the event
            
        Returns:
            List[Dict]: List of ticket documents
            
        Raises:
            PyMongoError: If there's an error during database operation
            Exception: For any other unexpected errors
        """
        try:
            if tickets_collection is None:
                raise Exception("Database connection not established")
            
            if not ObjectId.is_valid(event_id):
                raise Exception("Invalid event ID format")
                
            cursor = tickets_collection.find({"event": event_id})
            tickets = []
            for ticket in cursor:
                tickets.append(ticket)
            print(f"Tickets found: {tickets}")
            return tickets
        
        except PyMongoError as e:
            print(f"Database error occurred: {str(e)}")
            raise Exception(f"Database error occurred: {str(e)}")
        except Exception as e:
            print(f"Error retrieving tickets: {str(e)}")
            raise Exception(f"Error retrieving tickets: {str(e)}")

    @staticmethod
    async def get_ticket_by_id(ticket_id: str) -> Optional[Dict]:
        """
        Get a specific ticket by its ID
        
        Args:
            ticket_id (str): The ID of the ticket
            
        Returns:
            Optional[Dict]: The ticket document if found, None otherwise
            
        Raises:
            PyMongoError: If there's an error during database operation
            Exception: For any other unexpected errors
        """
        try:
            if tickets_collection is None:
                raise Exception("Database connection not established")
            
            if not ObjectId.is_valid(ticket_id):
                raise Exception("Invalid ticket ID format")
                
            ticket = tickets_collection.find_one({"_id": ObjectId(ticket_id)})
            return ticket
            
        except PyMongoError as e:
            print(f"Database error occurred: {str(e)}")
            raise Exception(f"Database error occurred: {str(e)}")
        except Exception as e:
            print(f"Error retrieving ticket: {str(e)}")
            raise Exception(f"Error retrieving ticket: {str(e)}")
    
    @staticmethod
    async def get_ticket_by_number(ticket_number: str) -> Optional[Dict]:
        """
        Get a specific ticket by its ticket number
        
        Args:
            ticket_number (str): The ticket number
            
        Returns:
            Optional[Dict]: The ticket document if found, None otherwise
            
        Raises:
            PyMongoError: If there's an error during database operation
            Exception: For any other unexpected errors
        """
        try:
            if tickets_collection is None:
                raise Exception("Database connection not established")
                
            ticket = tickets_collection.find_one({"ticket_number": ticket_number})
            return ticket
            
        except PyMongoError as e:
            print(f"Database error occurred: {str(e)}")
            raise Exception(f"Database error occurred: {str(e)}")
        except Exception as e:
            print(f"Error retrieving ticket: {str(e)}")
            raise Exception(f"Error retrieving ticket: {str(e)}")
    
    @staticmethod
    async def update_ticket_status(ticket_id: str, status: str) -> Optional[Dict]:
        """
        Update the status of a ticket
        
        Args:
            ticket_id (str): The ID of the ticket
            status (str): The new status
            
        Returns:
            Optional[Dict]: The updated ticket document if found, None otherwise
            
        Raises:
            PyMongoError: If there's an error during database operation
            Exception: For any other unexpected errors
        """
        try:
            if tickets_collection is None:
                raise Exception("Database connection not established")
            
            if not ObjectId.is_valid(ticket_id):
                raise Exception("Invalid ticket ID format")
                
            result = tickets_collection.update_one(
                {"_id": ObjectId(ticket_id)},
                {"$set": {"status": status, "updated_at": datetime.now()}}
            )
            
            if result.modified_count == 0:
                return None
                
            updated_ticket = tickets_collection.find_one({"_id": ObjectId(ticket_id)})
            return updated_ticket
            
        except PyMongoError as e:
            print(f"Database error occurred: {str(e)}")
            raise Exception(f"Database error occurred: {str(e)}")
        except Exception as e:
            print(f"Error updating ticket: {str(e)}")
            raise Exception(f"Error updating ticket: {str(e)}")
    
    @staticmethod
    async def update_payment_status(ticket_id: str, payment_status: str) -> Optional[Dict]:
        """
        Update the payment status of a ticket
        
        Args:
            ticket_id (str): The ID of the ticket
            payment_status (str): The new payment status
            
        Returns:
            Optional[Dict]: The updated ticket document if found, None otherwise
            
        Raises:
            PyMongoError: If there's an error during database operation
            Exception: For any other unexpected errors
        """
        try:
            if tickets_collection is None:
                raise Exception("Database connection not established")
            
            if not ObjectId.is_valid(ticket_id):
                raise Exception("Invalid ticket ID format")
                
            result = tickets_collection.update_one(
                {"_id": ObjectId(ticket_id)},
                {"$set": {"payment_status": payment_status, "updated_at": datetime.now()}}
            )
            
            if result.modified_count == 0:
                return None
                
            updated_ticket = tickets_collection.find_one({"_id": ObjectId(ticket_id)})
            return updated_ticket
            
        except PyMongoError as e:
            print(f"Database error occurred: {str(e)}")
            raise Exception(f"Database error occurred: {str(e)}")
        except Exception as e:
            print(f"Error updating payment status: {str(e)}")
            raise Exception(f"Error updating payment status: {str(e)}")
    
    @staticmethod
    async def generate_qr_code(ticket_id: str, qr_code: str) -> Optional[Dict]:
        """
        Generate and store QR code for a ticket
        
        Args:
            ticket_id (str): The ID of the ticket
            qr_code (str): The QR code data
            
        Returns:
            Optional[Dict]: The updated ticket document if found, None otherwise
            
        Raises:
            PyMongoError: If there's an error during database operation
            Exception: For any other unexpected errors
        """
        try:
            if tickets_collection is None:
                raise Exception("Database connection not established")
            
            if not ObjectId.is_valid(ticket_id):
                raise Exception("Invalid ticket ID format")
                
            result = tickets_collection.update_one(
                {"_id": ObjectId(ticket_id)},
                {"$set": {"qr_code": qr_code, "updated_at": datetime.now()}}
            )
            
            if result.modified_count == 0:
                return None
                
            updated_ticket = tickets_collection.find_one({"_id": ObjectId(ticket_id)})
            return updated_ticket
            
        except PyMongoError as e:
            print(f"Database error occurred: {str(e)}")
            raise Exception(f"Database error occurred: {str(e)}")
        except Exception as e:
            print(f"Error generating QR code: {str(e)}")
            raise Exception(f"Error generating QR code: {str(e)}")
    
    @staticmethod
    async def delete_ticket(ticket_id: str) -> bool:
        """
        Delete a ticket from the database
        
        Args:
            ticket_id (str): The ID of the ticket to delete
            
        Returns:
            bool: True if deletion was successful, False otherwise
            
        Raises:
            PyMongoError: If there's an error during database operation
            Exception: For any other unexpected errors
        """
        try:
            if tickets_collection is None:
                raise Exception("Database connection not established")
            
            if not ObjectId.is_valid(ticket_id):
                raise Exception("Invalid ticket ID format")
                
            result = await tickets_collection.delete_one({"_id": ObjectId(ticket_id)})
            return result.deleted_count > 0
            
        except PyMongoError as e:
            print(f"Database error occurred: {str(e)}")
            raise Exception(f"Database error occurred: {str(e)}")
        except Exception as e:
            print(f"Error deleting ticket: {str(e)}")
            raise Exception(f"Error deleting ticket: {str(e)}")