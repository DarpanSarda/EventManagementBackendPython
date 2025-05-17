# fastapi/src/services/bookingService.py
from typing import List, Optional, Dict
from datetime import datetime
from schemas.bookingSchema import BookingSchemaReq,BookingSchemaRes
from repository.bookings_repo import BookingRepo
from bson import ObjectId
from pymongo.errors import PyMongoError
from eventapi import HTTPException

class BookingService:
    @staticmethod
    async def create_booking(booking_data: BookingSchemaReq) -> Optional[Dict]:
        print(f"create_booking : {booking_data}")
        try:
            # Validate booking data
            if not booking_data.user_id or not booking_data.event_id:
                raise HTTPException(status_code=400, detail="User ID and Event ID are required")

            booking_dict = {
                "user_id": ObjectId(booking_data.user_id),
                "event_id": ObjectId(booking_data.event_id),
                "slot_name": booking_data.slot_name,
                "quantity": booking_data.quantity,
                "total_amount": booking_data.total_amount,
                "attendee_details": [attendee.dict() for attendee in booking_data.attendee_details] if booking_data.attendee_details else None,
                "special_requests": booking_data.special_requests,
                "status": "pending",
                "booking_date": datetime.now(),
                "created_at": datetime.now(),
                "updated_at": None,
            }

            result = await BookingRepo.create_booking(booking_dict)
            print(f"create_booking result: {result}")
            if result:
                def convert_object_ids(doc: dict) -> dict:
                    for key, value in doc.items():
                        if isinstance(value, ObjectId):
                            doc[key] = str(value)
                        elif isinstance(value, list):
                            doc[key] = [convert_object_ids(item) if isinstance(item, dict) else item for item in value]
                        elif isinstance(value, dict):
                            doc[key] = convert_object_ids(value)
                    return doc
                result = convert_object_ids(result)
                return BookingSchemaRes(**result)
            return None
        except PyMongoError as e:
            raise HTTPException(status_code=500, detail="Database error occurred")
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def get_user_bookings(user_id: str) -> List[Dict]:
        try:
            # Validate user ID
            if not ObjectId.is_valid(user_id):
                raise HTTPException(status_code=400, detail="Invalid user ID")

            # Call the repository to get user bookings
            result = await BookingRepo.get_user_bookings(user_id)
            print(f"get_user_bookings result: {result}")
            return result
        except PyMongoError as e:
            raise HTTPException(status_code=500, detail="Database error occurred")
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def get_event_bookings(event_id: str) -> List[Dict]:
        try:
            # Validate event ID
            if not ObjectId.is_valid(event_id):
                raise HTTPException(status_code=400, detail="Invalid event ID")

            # Call the repository to get event bookings
            result = await BookingRepo.get_event_bookings(event_id)
            return result
        except PyMongoError as e:
            raise HTTPException(status_code=500, detail="Database error occurred")
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def get_booking_by_id(booking_id: str) -> Optional[Dict]:
        try:
            # Validate booking ID
            if not ObjectId.is_valid(booking_id):
                raise HTTPException(status_code=400, detail="Invalid booking ID")

            # Call the repository to get booking by ID
            result = await BookingRepo.get_booking_by_id(booking_id)
            return result
        except PyMongoError as e:
            raise HTTPException(status_code=500, detail="Database error occurred")
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def update_booking_status(booking_id: str, status: str) -> Optional[Dict]:
        try:
            # Validate booking ID and status
            if not ObjectId.is_valid(booking_id):
                raise HTTPException(status_code=400, detail="Invalid booking ID")
            if status not in ["pending", "confirmed", "cancelled", "completed"]:
                raise HTTPException(status_code=400, detail="Invalid status")

            # Call the repository to update booking status
            result = await BookingRepo.update_booking_status(booking_id, status)
            return result
        except PyMongoError as e:
            raise HTTPException(status_code=500, detail="Database error occurred")
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def delete_booking(booking_id: str) -> bool:
        try:
            # Validate booking ID
            if not ObjectId.is_valid(booking_id):
                raise HTTPException(status_code=400, detail="Invalid booking ID")

            # Call the repository to delete booking
            result = await BookingRepo.delete_booking(booking_id)
            return result
        except PyMongoError as e:
            raise HTTPException(status_code=500, detail="Database error occurred")
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        
    @staticmethod
    async def getAllBookings() -> List[Dict]:
        """
        Get All Bookings
        """
        try:
            response = await BookingRepo.getAllBookings()
            if not response:
                raise HTTPException(status_code=404, detail="No bookings found")
            return response
        except PyMongoError as e:
            raise HTTPException(status_code=500, detail="Database error occurred")
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))