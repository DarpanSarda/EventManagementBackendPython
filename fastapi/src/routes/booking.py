from fastapi import APIRouter

bookingRouter = APIRouter(
    prefix="/bookings",
    tags=["bookings"],
)   

@bookingRouter.get("/")
async def get_bookings():
    pass

@bookingRouter.post("/")
async def create_booking():
    pass

@bookingRouter.get("/{booking_id}")
async def get_booking(booking_id: int):
    pass

@bookingRouter.put("/{booking_id}")
async def update_booking(booking_id: int):
    pass

@bookingRouter.delete("/{booking_id}")
async def delete_booking(booking_id: int):
    pass

@bookingRouter.get("/user/{user_id}")
async def get_user_bookings(user_id: int):
    pass

@bookingRouter.get("/event/{event_id}")
async def get_event_bookings(event_id: int):
    pass

@bookingRouter.get("/user/{user_id}/event/{event_id}")
async def get_user_event_bookings(user_id: int, event_id: int):
    pass

