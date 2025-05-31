from models import event
from db.connect import MongoDBSingleton
from bson import ObjectId
from schemas.eventSchema import EventSchemaAdminReq
import re

db = MongoDBSingleton().get_database()
if db is not None:
    events_collection = db["events"]
else:
    events_collection = None


class EventsRepo():

    @staticmethod
    async def findEvents():
        try:
            if events_collection is None:
                raise Exception("Database connection not initialized")
    
            print("Fetching events from database...")
            # Remove the '_id': 0 projection to allow ID conversion
            print(f"Events collection: {events_collection.find({})}")
            events_cursor = events_collection.find({})
            print(f"Events cursor: {events_cursor}")
            events = []
            for event in events_cursor:
                print(f"Event: {event}")
                events.append(event)

            # Transform the events to handle ObjectId
            transformed_events = []
            for event in events:
                event['_id'] = str(event['_id'])  # Convert ObjectId to string
                transformed_events.append(event)
    
            print(f"Found {len(transformed_events)} events")
            return transformed_events
    
        except Exception as e:
            print(f"Error in findEvents: {str(e)}")
            raise Exception(f"Failed to fetch events: {str(e)}")
    
    @staticmethod
    async def findEventById(eventId : str):
        event = events_collection.find_one({"_id": ObjectId(eventId)})
        print(f"eventttt {event}")
        return event
    
    @staticmethod
    def findEventByName(eventName : str):
        return events_collection.find_one({"name": eventName})
        
    @staticmethod
    def findEventByStateName(stateName : str):
        return events_collection.find_one({"state": stateName})
    
    @staticmethod
    def findEventByCityName(stateName : str , cityName : str):
        return events_collection.find_one({"state": stateName , "city": cityName})
    
    @staticmethod
    def createEvent(event : EventSchemaAdminReq):
        """Create event"""
        try:
            if events_collection is None:
                raise Exception("Database connection failed")
            returned_event = events_collection.insert_one(event)
            if returned_event is not None:
                return event
            return None
        except Exception as e:
            raise Exception(f"Error creating event: {str(e)}")
        
    @staticmethod
    async def updateEvent(eventId : str , event : EventSchemaAdminReq):
        """
        update event
        """
        try:
            print(f"eeefefererrfef {event}")
            if events_collection is None:
                raise Exception("Database connection failed")
            existing_event = await EventsRepo.findEventById(eventId)
            print(f"exxxxxx {existing_event}")
            if not existing_event:
                raise Exception("Event not found")
            update_data = event if isinstance(event, dict) else event.model_dump(exclude_unset=True)
            print(f"upppppppp {update_data}")
            result = events_collection.update_one(
                {"_id": ObjectId(eventId)},
                {"$set": update_data}
            )

            print(f"Modified count: {result.modified_count}")
        
            if result.modified_count > 0:
                # Get and return the updated document
                updated_event = await EventsRepo.findEventById(eventId)
                return updated_event
                
            return None
        except Exception as e:
            raise Exception(f"Error updating event: {str(e)}")


    @staticmethod
    async def geteventbycategory(category: str):
        """
        Get events by partial category name match using regex
        Returns list of events matching the category pattern
        """
        try:
            if events_collection is None:
                raise Exception("Database connection failed")
            # Find all events matching the category pattern
            cursor = events_collection.find({"$text": {"$search": "music"}})
            events = []
            for event in cursor:
                events.append(event)
            # Transform events to handle ObjectId
            transformed_events = []
            for event in events:
                event['_id'] = str(event['_id'])
                transformed_events.append(event)
            return transformed_events
        except Exception as e:
            print(f"Error in geteventbycategory: {str(e)}")
            raise Exception(f"Error fetching events by category: {str(e)}")