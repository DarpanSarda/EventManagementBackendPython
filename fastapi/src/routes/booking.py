# fastapi/src/routes/booking.py
from fastapi import APIRouter, HTTPException
from services.bookingService import BookingService
from schemas.bookingSchema import BookingSchemaReq
from bson import ObjectId
from typing import List, Optional, Dict

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
        result = await BookingService.get_bookings()
        return {"message": "Bookings retrieved successfully", "data": result}
    except HTTPException as e:
        raise e

@bookingRouter.get("/{booking_id}")
async def get_booking(booking_id: str):
    try:
        result = await BookingService.get_booking_by_id(booking_id)
        return {"message": "Booking retrieved successfully", "data": result}
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