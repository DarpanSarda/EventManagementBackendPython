from fastapi import APIRouter, status , Depends
from fastapi.responses import JSONResponse
from schemas.eventSchema import EventSchemaAdminReq
from services.eventService import EventService
from bson import ObjectId
from typing import List 
from dependency.auth import admin_only

eventRouter = APIRouter(
    prefix="/events",
    tags=["events"],
)

def convert_objectid_to_str(data):
    """Recursively convert ObjectId fields in a dictionary to strings."""
    if isinstance(data, dict):
        return {k: convert_objectid_to_str(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_objectid_to_str(item) for item in data]
    elif isinstance(data, ObjectId):
        return str(data)  # Convert ObjectId to string
    return data  # Return as is if it's not an ObjectId

@eventRouter.get("/")
async def get_events():
    try:
        events = await EventService.getEvents()
        if events:
            events = convert_objectid_to_str(events)  # Convert ObjectId fields to strings
            response = {
                "status": "success",
                "data": events,
            }
            print(f"events : {events}")
            return JSONResponse(content=response, status_code=status.HTTP_200_OK)
        response = {
            "status": "failed",
            "message": "No events found",
        }
        return JSONResponse(content=response, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        response = {
            "status": "error",
            "message": str(e),
        }
        return JSONResponse(content=response, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@eventRouter.post("/" , response_model=EventSchemaAdminReq)
async def create_event(event: EventSchemaAdminReq):
    try:
        event = await EventService.createEvent(event)
        if event is not None:
            response = {
                "status": "success",
                "data": event,
                "message": "Event created successfully",
            }
            return await JSONResponse(content=response, status_code=status.HTTPStatus.CREATED)
        response = {
            "status": "failed", 
            "message": "Event creation failed",
        }
        return await JSONResponse(content=response, status_code=status.HTTPStatus.BAD_REQUEST)
    except Exception as e:
        response = {
            "status": "error",
            "message": str(e),
        }
        return JSONResponse(content=response, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
@eventRouter.get("/filter", response_model=List[EventSchemaAdminReq])
async def get_events_by_location(state: str | None = None, city: str | None = None):
    """
    Get events filtered by state and/or city using query parameters
    
    Args:
        state (str, optional): Query parameter for state name
        city (str, optional): Query parameter for city name
        
    Returns:
        JSONResponse: The filtered events data or error message
    
    Example:
        /events/filter?state=California
        /events/filter?state=California&city=San Francisco
    """
    try:
        # Validate input parameters
        if not state:
            response = {
                "status": "failed",
                "message": "State parameter is required",
            }
            return JSONResponse(content=response, status_code=status.HTTP_400_BAD_REQUEST)
            
        # Clean input parameters
        state = state.strip()
        city = city.strip() if city else None
        
        if city:
            events = EventService.getEventByCityName(state, city)
            location_msg = f"city: {city}, state: {state}"
        else:
            events = EventService.getEventByStateName(state)
            location_msg = f"state: {state}"

        if events:
            events = convert_objectid_to_str(events)  # Convert ObjectId to string
            response = {
                "status": "success",
                "data": events,
                "message": f"Found events in {location_msg}"
            }
            return JSONResponse(content=response, status_code=status.HTTP_200_OK)
        
        response = {
            "status": "failed",
            "message": f"No events found in {location_msg}",
        }
        return JSONResponse(content=response, status_code=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        response = {
            "status": "error",
            "message": f"Error retrieving events: {str(e)}",
        }
        return JSONResponse(content=response, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@eventRouter.get("/{event_id}", response_model=EventSchemaAdminReq)
async def get_event(event_id: str):
    """
    Get a single event by its ID
    
    Args:
        event_id (str): The ID of the event to retrieve
        
    Returns:
        JSONResponse: The event data or error message
    """
    try:
        event = await EventService.getEventById(event_id)
        if event:
            event = convert_objectid_to_str(event)  # Convert ObjectId to string
            response = {
                "status": "success",
                "data": event,
            }
            print(f"event : {event}")
            return JSONResponse(content=response, status_code=status.HTTP_200_OK)
        
        response = {
            "status": "failed",
            "message": "Event not found",
        }
        return JSONResponse(content=response, status_code=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        response = {
            "status": "error",
            "message": str(e),
        }
        return JSONResponse(content=response, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

# @eventRouter.put("/{event_id}")
# async def update_event(event_id: int):
#     pass

# @eventRouter.delete("/{event_id}")
# async def delete_event(event_id: int):
#     pass

@eventRouter.get("/name/{event_name}", response_model=List[EventSchemaAdminReq])
async def get_event_by_name(event_name: str):
    """
    Get a single event by its name
    
    Args:
        event_name (str): The name of the event to retrieve
        
    Returns:
        JSONResponse: The event data or error message
    """
    try:
        event = EventService.getEventByName(event_name)
        if event:
            event = convert_objectid_to_str(event)  # Convert ObjectId to string
            response = {
                "status": "success",
                "data": event,
            }
            return JSONResponse(content=response, status_code=status.HTTP_200_OK)
        
        response = {
            "status": "failed",
            "message": "Event not found",
        }
        return JSONResponse(content=response, status_code=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        response = {
            "status": "error",
            "message": str(e),
        }
        return JSONResponse(content=response, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@eventRouter.put("/{event_id}", response_model=EventSchemaAdminReq)
async def update_event(event_id: str, event: EventSchemaAdminReq):
    """
    Update an event by its ID
    
    Args:
        event_id (str): The ID of the event to update
        event (EventSchemaAdminReq): The updated event data
        
    Returns:
        JSONResponse: The updated event data or error message
    """
    print("route event update")
    try:
        print("Inside tryyy", event)
        updated_event = await EventService.updateEvent(event_id, event)
        if updated_event:
            updated_event = convert_objectid_to_str(updated_event)  # Convert ObjectId to string
            response = {
                "status": "success",
                "data": updated_event,
                "message": "Event updated successfully",
            }
            return JSONResponse(content=response, status_code=status.HTTP_200_OK)
        
        response = {
            "status": "failed",
            "message": "Event not found or update failed",
        }
        return JSONResponse(content=response, status_code=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        response = {
            "status": "error",
            "message": str(e),
        }
        return JSONResponse(content=response, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@eventRouter.get("/category/{categoryName}")
async def get_event_by_category(categoryName: str):
    """
    Get events By category name
    Args:
        categoryName (str): The category name to filter events by
    Returns:
        JSONResponse: The filtered events data or error message
    """
    try:
        events =  await EventService.getEventsBycategory(categoryName)
        if events:
            events = convert_objectid_to_str(events)
            response = {
                "status": "success",
                "data": events,
            }
            return JSONResponse(content=response, status_code=status.HTTP_200_OK)
        response = {
            "status": "failed",
            "message": "No events found for the given category",
        }
        return JSONResponse(content=response, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        response = {
            "status": "error",
            "message": str(e),
        }
        return JSONResponse(content=response, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)