from typing import List, Optional, Dict
from schemas.ticketSchema import TicketSchemaReq
from repository.tickets_repo import TicketsRepo
import qrcode
import base64
import io
import uuid

class TicketService:
    @staticmethod
    async def create_ticket(ticket_data: TicketSchemaReq) -> Dict:
        print(f"ticket service {ticket_data}")
        """
        Create a new ticket
        
        Args:
            ticket_data (TicketSchemaReq): The ticket data
            
        Returns:
            Dict: The newly created ticket
            
        Raises:
            Exception: If there's an error creating the ticket
        """
        try:
            # Create the ticket
            ticket = await TicketsRepo.create_ticket(ticket_data)
            
            if ticket:
                # Generate QR code
                qr_data = await TicketService.generate_qr_code_data(str(ticket["_id"]), ticket["ticket_number"])
                print(f"QR code data: {qr_data}")
                # Update ticket with QR code
                updated_ticket = await TicketsRepo.generate_qr_code(str(ticket["_id"]), qr_data)
                print(f"Updated ticket: {updated_ticket}")
                return updated_ticket if updated_ticket else ticket
            
            raise Exception("Failed to create ticket")
        except Exception as e:
            raise Exception(f"Error creating ticket: {str(e)}")
    
    @staticmethod
    async def get_user_tickets(user_id: str) -> List[Dict]:
        """
        Get all tickets for a user
        
        Args:
            user_id (str): The user ID
            
        Returns:
            List[Dict]: List of tickets
            
        Raises:
            Exception: If there's an error retrieving tickets
        """
        try:
            tickets = await TicketsRepo.get_tickets_by_user(user_id)
            # print(f"Tickets found: {tickets}")
            return tickets
        except Exception as e:
            raise Exception(f"Error retrieving user tickets: {str(e)}")
    
    @staticmethod
    async def get_event_tickets(event_id: str) -> List[Dict]:
        """
        Get all tickets for an event
        
        Args:
            event_id (str): The event ID
            
        Returns:
            List[Dict]: List of tickets
            
        Raises:
            Exception: If there's an error retrieving tickets
        """
        try:
            return await TicketsRepo.get_tickets_by_event(event_id)
        except Exception as e:
            raise Exception(f"Error retrieving event tickets: {str(e)}")
    
    @staticmethod
    async def get_ticket(ticket_id: str) -> Optional[Dict]:
        """
        Get a specific ticket
        
        Args:
            ticket_id (str): The ticket ID
            
        Returns:
            Optional[Dict]: The ticket if found, None otherwise
            
        Raises:
            Exception: If there's an error retrieving the ticket
        """
        try:
            return await TicketsRepo.get_ticket_by_id(ticket_id)
        except Exception as e:
            raise Exception(f"Error retrieving ticket: {str(e)}")
    
    @staticmethod
    async def get_ticket_by_number(ticket_number: str) -> Optional[Dict]:
        """
        Get a specific ticket by its number
        
        Args:
            ticket_number (str): The ticket number
            
        Returns:
            Optional[Dict]: The ticket if found, None otherwise
            
        Raises:
            Exception: If there's an error retrieving the ticket
        """
        try:
            return await TicketsRepo.get_ticket_by_number(ticket_number)
        except Exception as e:
            raise Exception(f"Error retrieving ticket: {str(e)}")
    
    @staticmethod
    async def confirm_ticket(ticket_id: str) -> Optional[Dict]:
        """
        Confirm a ticket
        
        Args:
            ticket_id (str): The ticket ID
            
        Returns:
            Optional[Dict]: The updated ticket if found, None otherwise
            
        Raises:
            Exception: If there's an error confirming the ticket
        """
        try:
            return await TicketsRepo.update_ticket_status(ticket_id, "confirmed")
        except Exception as e:
            raise Exception(f"Error confirming ticket: {str(e)}")
    
    @staticmethod
    async def cancel_ticket(ticket_id: str) -> Optional[Dict]:
        """
        Cancel a ticket
        
        Args:
            ticket_id (str): The ticket ID
            
        Returns:
            Optional[Dict]: The updated ticket if found, None otherwise
            
        Raises:
            Exception: If there's an error cancelling the ticket
        """
        try:
            return await TicketsRepo.update_ticket_status(ticket_id, "cancelled")
        except Exception as e:
            raise Exception(f"Error cancelling ticket: {str(e)}")
    
    @staticmethod
    async def update_payment(ticket_id: str, payment_status: str) -> Optional[Dict]:
        """
        Update ticket payment status
        
        Args:
            ticket_id (str): The ticket ID
            payment_status (str): The new payment status
            
        Returns:
            Optional[Dict]: The updated ticket if found, None otherwise
            
        Raises:
            Exception: If there's an error updating payment status
        """
        try:
            ticket = await TicketsRepo.update_payment_status(ticket_id, payment_status)
            
            # If payment is completed, also confirm the ticket
            if payment_status == "completed" and ticket:
                ticket = await TicketsRepo.update_ticket_status(ticket_id, "confirmed")
                
            return ticket
        except Exception as e:
            raise Exception(f"Error updating payment status: {str(e)}")
    
    @staticmethod
    async def delete_ticket(ticket_id: str) -> bool:
        """
        Delete a ticket
        
        Args:
            ticket_id (str): The ticket ID
            
        Returns:
            bool: True if deletion was successful, False otherwise
            
        Raises:
            Exception: If there's an error deleting the ticket
        """
        try:
            return await TicketsRepo.delete_ticket(ticket_id)
        except Exception as e:
            raise Exception(f"Error deleting ticket: {str(e)}")
    
    @staticmethod
    async def generate_qr_code_data(ticket_id: str, ticket_number: str) -> str:
        """
        Generate QR code for a ticket
        
        Args:
            ticket_id (str): The ticket ID
            ticket_number (str): The ticket number
            
        Returns:
            str: Base64 encoded QR code image
            
        Raises:
            Exception: If there's an error generating the QR code
        """
        try:
            # Create QR code data with ticket ID and number for verification
            qr_data = {
                "id": ticket_id,
                "number": ticket_number,
                "verification": uuid.uuid4().hex
            }
            
            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(str(qr_data))
            qr.make(fit=True)
            
            # Create QR code image
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Convert to base64
            buffer = io.BytesIO()
            img.save(buffer)
            qr_base64 = base64.b64encode(buffer.getvalue()).decode()
            
            return f"data:image/png;base64,{qr_base64}"
        except Exception as e:
            raise Exception(f"Error generating QR code: {str(e)}")
    
    @staticmethod
    async def verify_ticket(ticket_number: str) -> Dict:
        """
        Verify a ticket for event entry
        
        Args:
            ticket_number (str): The ticket number to verify
            
        Returns:
            Dict: Verification result with ticket details
            
        Raises:
            Exception: If there's an error verifying the ticket
        """
        try:
            ticket = await TicketsRepo.get_ticket_by_number(ticket_number)
            
            if not ticket:
                return {
                    "verified": False,
                    "message": "Ticket not found"
                }
            
            if ticket["status"] == "cancelled":
                return {
                    "verified": False,
                    "message": "Ticket has been cancelled"
                }
            
            if ticket["payment_status"] != "completed":
                return {
                    "verified": False,
                    "message": "Payment incomplete"
                }
            
            # Return verification success with ticket details
            return {
                "verified": True,
                "message": "Ticket verified successfully",
                "ticket": {
                    "id": str(ticket["_id"]),
                    "ticket_number": ticket["ticket_number"],
                    "event": str(ticket["event"]), 
                    "persons": ticket["persons"],
                    "status": ticket["status"]
                }
            }
        except Exception as e:
            raise Exception(f"Error verifying ticket: {str(e)}")

    @staticmethod
    async def get_all_tickets() -> List[Dict]:
        """
        Get all tickets
        
        Returns:
            List[Dict]: List of all tickets
            
        Raises:
            Exception: If there's an error retrieving tickets
        """
        try:
            tickets = await TicketsRepo.get_all_tickets()
            return tickets
        except Exception as e:
            raise Exception(f"Error retrieving tickets: {str(e)}")