from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from typing import List, Dict
from schemas.ticketSchema import TicketSchemaReq, TicketSchemaRes
from services.ticketService import TicketService
from datetime import datetime

ticketrouter = APIRouter(
    prefix="/tickets",
    tags=["tickets"]
)

@ticketrouter.post("/", response_model=TicketSchemaRes, status_code=status.HTTP_201_CREATED)
async def create_ticket(ticket: TicketSchemaReq):
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
        print(f"Tickets found: {tickets}")
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
async def update_payment(ticket_id: str, payment_status: str):
    """
    Update payment status for a specific ticket by ID
    """
    try:
        updated_ticket = await TicketService.update_payment(ticket_id, payment_status)
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