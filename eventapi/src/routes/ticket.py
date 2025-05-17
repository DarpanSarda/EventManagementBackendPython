from eventapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from typing import List, Dict
from schemas.ticketSchema import TicketSchemaReq, TicketSchemaRes , TicketSchemaUpdate
from services.ticketService import TicketService
from datetime import datetime
from services.eventService import EventService 

ticketrouter = APIRouter(
    prefix="/tickets",
    tags=["tickets"]
)

@ticketrouter.post("/", status_code=status.HTTP_201_CREATED)
async def create_ticket(ticket: TicketSchemaReq):
    print(f"Creating ticket with data: {ticket}")
    try:
        result = await TicketService.create_ticket(ticket)

        result["_id"] = str(result["_id"])
        result["user"] = str(result["user"])
        result["event"] = str(result["event"])
        if "payment_id" in result and result["payment_id"]:
            result["payment_id"] = str(result["payment_id"])

        return result

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@ticketrouter.get("/user/{user_id}", response_model=List[TicketSchemaRes])
async def get_user_tickets(user_id: str):
    """
    Get all tickets for a specific user
    """
    try:
        tickets = await TicketService.get_user_tickets(user_id)
        transformed_tickets = []
        
        for ticket in tickets:
            # Transform the basic ticket data
            transformed_ticket = {
                "_id": str(ticket["_id"]),
                "user": str(ticket["user"]),
                "event": str(ticket["event"])
            }
            
            # Get and add event details
            event = await EventService.getEventById(ticket["event"])
            if event:
                transformed_ticket["event_detail"] = {
                    "name": event["name"],
                    "state": event["state"],
                    "city": event["city"],
                    "venue": event["venue"],
                    "date": event["date"],
                    "time": event["time"],
                    "description": event["description"],
                }
            
            # Transform other fields
            if "payment_id" in ticket and ticket["payment_id"]:
                transformed_ticket["payment_id"] = str(ticket["payment_id"])
            if "purchase_date" in ticket and isinstance(ticket["purchase_date"], datetime):
                transformed_ticket["purchase_date"] = ticket["purchase_date"].isoformat()
            if "updated_at" in ticket and isinstance(ticket["updated_at"], datetime):
                transformed_ticket["updated_at"] = ticket["updated_at"].isoformat()
            
            # Add any remaining fields from the original ticket
            for key, value in ticket.items():
                if key not in transformed_ticket:
                    transformed_ticket[key] = value
            
            # print(f"Transformed ticket: {transformed_ticket[0]}")
            transformed_tickets.append(transformed_ticket)
            # print(transformed_tickets)
        return transformed_tickets
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@ticketrouter.get("/event/{event_id}", response_model=List[TicketSchemaRes])
async def get_event_tickets(event_id: str):
    """
    Get all tickets for a specific event
    """
    try:
        tickets = await TicketService.get_event_tickets(event_id)
        def transform(doc: dict) -> dict:
            doc["_id"] = str(doc["_id"])
            doc["user"] = str(doc["user"])
            doc["event"] = str(doc["event"])
            if "payment_id" in doc and doc["payment_id"]:
                doc["payment_id"] = str(doc["payment_id"])
            if "purchase_date" in doc and isinstance(doc["purchase_date"], datetime):
                doc["purchase_date"] = doc["purchase_date"].isoformat()
            if "updated_at" in doc and isinstance(doc["updated_at"], datetime):
                doc["updated_at"] = doc["updated_at"].isoformat()
            return doc
        return [transform(ticket) for ticket in tickets]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@ticketrouter.get("/{ticket_id}", response_model=TicketSchemaRes)
async def get_ticket(ticket_id: str):
    """
    Get a specific ticket by ID
    """
    try:
        ticket = await TicketService.get_ticket(ticket_id)
        def transform(doc: dict) -> dict:
            doc["_id"] = str(doc["_id"])
            doc["user"] = str(doc["user"])
            doc["event"] = str(doc["event"])
            if "payment_id" in doc and doc["payment_id"]:
                doc["payment_id"] = str(doc["payment_id"])
            if "purchase_date" in doc and isinstance(doc["purchase_date"], datetime):
                doc["purchase_date"] = doc["purchase_date"].isoformat()
            if "updated_at" in doc and isinstance(doc["updated_at"], datetime):
                doc["updated_at"] = doc["updated_at"].isoformat()
            return doc
        if not ticket:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ticket with ID {ticket_id} not found"
            )
        ticket = transform(ticket)
        return ticket
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@ticketrouter.put("/{ticket_id}/confirm", response_model=TicketSchemaRes)
async def confirm_ticket(ticket_id: str):
    """
    Confirm a specific ticket by ID
    """
    try:
        updated_ticket = await TicketService.confirm_ticket(ticket_id)
        if not updated_ticket:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ticket with ID {ticket_id} not found"
            )
        return updated_ticket
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@ticketrouter.put("/{ticket_id}/cancel", response_model=TicketSchemaRes)
async def cancel_ticket(ticket_id: str):
    """
    Cancel a specific ticket by ID
    """
    try:
        updated_ticket = await TicketService.cancel_ticket(ticket_id)
        if not updated_ticket:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ticket with ID {ticket_id} not found"
            )
        return updated_ticket
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@ticketrouter.put("/{ticket_id}/payment", response_model=TicketSchemaRes)
async def update_payment(ticket_id: str, payload:TicketSchemaUpdate):
    """
    Update payment status for a specific ticket by ID
    """
    try:
        updated_ticket = await TicketService.update_payment(ticket_id, payload.payment_status)
        if not updated_ticket:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ticket with ID {ticket_id} not found"
            )
        def transform(doc: dict) -> dict:
            doc["_id"] = str(doc["_id"])
            doc["user"] = str(doc["user"])
            doc["event"] = str(doc["event"])
            if "payment_id" in doc and doc["payment_id"]:
                doc["payment_id"] = str(doc["payment_id"])
            if "purchase_date" in doc and isinstance(doc["purchase_date"], datetime):
                doc["purchase_date"] = doc["purchase_date"].isoformat()
            if "updated_at" in doc and isinstance(doc["updated_at"], datetime):
                doc["updated_at"] = doc["updated_at"].isoformat()
            return doc
        updated_ticket = transform(updated_ticket)
        return updated_ticket
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@ticketrouter.delete("/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ticket(ticket_id: str):
    """
    Delete a specific ticket by ID
    """
    try:
        success = await TicketService.delete_ticket(ticket_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ticket with ID {ticket_id} not found"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@ticketrouter.get("/verify/{ticket_number}", response_model=Dict)
async def verify_ticket(ticket_number: str):
    """
    Verify a ticket for event entry
    """
    try:
        verification_result = await TicketService.verify_ticket(ticket_number)
        return verification_result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    

@ticketrouter.get("/", response_model=List[TicketSchemaRes])
async def get_all_tickets():
    """
    Get all tickets
    """
    try:
        tickets = await TicketService.get_all_tickets()
        def transform(doc: dict) -> dict:
            doc["_id"] = str(doc["_id"])
            doc["user"] = str(doc["user"])
            doc["event"] = str(doc["event"])
            if "payment_id" in doc and doc["payment_id"]:
                doc["payment_id"] = str(doc["payment_id"])
            if "purchase_date" in doc and isinstance(doc["purchase_date"], datetime):
                doc["purchase_date"] = doc["purchase_date"].isoformat()
            if "updated_at" in doc and isinstance(doc["updated_at"], datetime):
                doc["updated_at"] = doc["updated_at"].isoformat()
            return doc
        return [transform(ticket) for ticket in tickets]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )