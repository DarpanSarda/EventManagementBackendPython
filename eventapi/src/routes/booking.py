# fastapi/src/routes/booking.py
from fastapi import APIRouter, HTTPException, status
from services.bookingService import BookingService
from schemas.bookingSchema import BookingSchemaReq
from bson import ObjectId
from typing import List, Optional, Dict
from fastapi.responses import JSONResponse

bookingRouter = APIRouter(
    prefix="/bookings",
    tags=["bookings"],
)

@bookingRouter.post("/")
async def create_booking(booking_data: BookingSchemaReq):
    print(f"create_booking called with data: {booking_data}")
    try:
        result = await BookingService.create_booking(booking_data)
        return {"message": "Booking created successfully", "data": result}
    except HTTPException as e:
        raise e

@bookingRouter.get("/")
async def get_bookings():
    try:
        bookings = await BookingService.getAllBookings()
        for booking in bookings:
            booking["_id"] = str(booking["_id"])
            booking["user_id"] = str(booking["user_id"])
            booking["event_id"] = str(booking["event_id"])
        return bookings
    except HTTPException as e:
        raise e

@bookingRouter.get("/{booking_id}")
async def get_booking(booking_id: str):
    try:
        booking = await BookingService.get_booking_by_id(booking_id)
        if booking:
            booking["_id"] = str(booking["_id"])
            booking["user_id"] = str(booking["user_id"])
            booking["event_id"] = str(booking["event_id"])
            booking["booking_date"] = booking["booking_date"].isoformat() if booking.get("booking_date") else None
            booking["created_at"] = booking["created_at"].isoformat() if booking.get("created_at") else None
            print(f"Booking found: {booking}")
            response = {
                "status": "success",
                "data": booking,
            }
            return JSONResponse(content=response, status_code=status.HTTP_200_OK)
        
        response = {
            "status": "failed",
            "message": "Event not found",
        }
        return JSONResponse(content=response, status_code=status.HTTP_404_NOT_FOUND)
    except HTTPException as e:
        raise e

@bookingRouter.put("/{booking_id}")
async def update_booking(booking_id: str, status: str):
    try:
        result = await BookingService.update_booking_status(booking_id, status)
        return {"message": "Booking updated successfully", "data": result}
    except HTTPException as e:
        raise e

@bookingRouter.delete("/{booking_id}")
async def delete_booking(booking_id: str):
    try:
        result = await BookingService.delete_booking(booking_id)
        return {"message": "Booking deleted successfully", "data": result}
    except HTTPException as e:
        raise e

@bookingRouter.get("/user/{user_id}")
async def get_user_bookings(user_id: str):
    print(f"get_user_bookings called with user_id: {user_id}")
    try:
        result = await BookingService.get_user_bookings(user_id)
        print(f"jhsfhds : {result}")
        def serialize_booking(booking):
            booking["_id"] = str(booking["_id"])
            booking["user_id"] = str(booking["user_id"])
            booking["event_id"] = str(booking["event_id"])
            booking["booking_date"] = booking["booking_date"].isoformat() if booking.get("booking_date") else None
            booking["created_at"] = booking["created_at"].isoformat() if booking.get("created_at") else None
            booking["updated_at"] = booking["updated_at"].isoformat() if booking.get("updated_at") else None
            return booking
        result = [serialize_booking(booking) for booking in result]
        return {"message": "User bookings retrieved successfully", "data": result}
    except HTTPException as e:
        raise e

@bookingRouter.get("/event/{event_id}")
async def get_event_bookings(event_id: str):
    try:
        result = await BookingService.get_event_bookings(event_id)
        return {"message": "Event bookings retrieved successfully", "data": result}
    except HTTPException as e:
        raise e